import streamlit as st, PyPDF2, re
from Hirescope_Project.utils import summarize_resume, make_candidate_id, chroma_client, collection
from PyPDF2.errors import PdfReadError

st.set_page_config(page_title="HR Upload – HireScope", page_icon="📄")
st.title("📂 HR Bulk Résumé Uploader")

hr_name = st.text_input("Your (HR) name")
files = st.file_uploader("Upload up to 10 résumé PDFs", type="pdf", accept_multiple_files=True)

if not hr_name:
    st.warning("Enter your name first.")
    st.stop()

if files and len(files) > 10:
    st.error("⚠️ Please upload no more than 10 PDFs at once.")
    st.stop()

# ---------- process files ----------
if files:
    for pdf in files:
        st.markdown(f"---\n#### Processing `{pdf.name}`")
        try:
            reader = PyPDF2.PdfReader(pdf)
            text = "".join(page.extract_text() or "" for page in reader.pages)
        except PdfReadError:
            st.error(f"❌ `{pdf.name}` is corrupted or unreadable. Skipped.")
            continue
        except Exception as e:
            st.error(f"❌ Error reading `{pdf.name}`: {e}")
            continue

        if not text.strip():
            st.warning(f"⚠️ No extractable text in `{pdf.name}`. Skipped.")
            continue

        with st.spinner("Summarizing résumé…"):
            summary = summarize_resume(text)

        m = re.search(r"(?i)^name[:\-]?\s*(.+)", summary, re.M)
        name = m.group(1).strip() if m else "Unknown"
        cid  = make_candidate_id(name)

        existing = collection.get(where={"name": name})
        if existing["ids"]:
            if not st.checkbox(f"🔄 `{name}` exists. Overwrite with {pdf.name}?", key=cid):
                st.info(f"Skipped `{name}` (duplicate not overwritten).")
                continue
            collection.delete(ids=existing["ids"])

        collection.add(
            documents=[summary],
            metadatas=[{"candidate_id": cid, "name": name, "uploaded_by": hr_name}],
            ids=[cid]
        )
        if hasattr(chroma_client, "persist"):
            chroma_client.persist()

        st.success(f"✅ Stored résumé for **{name}** (ID: `{cid}`)")
        st.text_area("Résumé summary", summary, height=250)

# ---------- display stored candidates ----------
st.divider()
total = collection.count()
st.subheader(f"📇 Stored Candidates ({total})")

res = collection.get(include=["metadatas", "documents"])
metas, docs = res["metadatas"], res["documents"]

if metas:
    for i, meta in enumerate(metas):
        with st.container(border=True):
            st.markdown(f"### 👤 {meta['name']}")
            st.caption(f"ID: `{meta['candidate_id']}` • Uploaded by: {meta['uploaded_by']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👁️ View Profile", key=f"view_{i}"):
                    st.text_area("Résumé Summary", docs[i], height=320)
            with col2:
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    collection.delete(ids=[meta["candidate_id"]])
                    if hasattr(chroma_client, "persist"):
                        chroma_client.persist()
                    st.experimental_rerun()
else:
    st.info("No résumés in the database yet.")
