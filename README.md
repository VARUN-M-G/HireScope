# 💼 HireScopeAI – AI-Powered Résumé Assistant

HireScopeAI is a Streamlit app that allows HR professionals to upload, summarize, store, and query candidate résumés using OpenAI's GPT‑4o and vector search via ChromaDB.

🚀 **Demo Deployed on Hugging Face Spaces**  
⚠️ Note: This demo uses **in-memory** storage. Uploaded résumés will reset on refresh or restart.

---

## ✨ Features

- 📂 Upload single or bulk résumé PDFs (max 10 at once)
- 🧠 Automatic résumé summarization with GPT‑4o
- 🗂️ Structured storage using vector embeddings
- 💬 AI chatbot to query candidate qualifications, experience, and skills
- 🧹 Duplicate detection and résumé overwrite prompts
- 🚫 Handles corrupted PDFs with user feedback

---

## 🔧 Tech Stack

- [Streamlit](https://streamlit.io/) – UI
- [OpenAI GPT‑4o](https://platform.openai.com/docs/models/gpt-4) – Summarization & Chat
- [ChromaDB (in-memory)](https://docs.trychroma.com/) – Vector storage
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF parsing

---

## 🧪 Demo Mode Limitations

- This Hugging Face Space uses **in-memory ChromaDB**  
- Résumé data is **not persisted** after page refresh or app restart

For production or persistent use, you can run this locally with:

```bash
pip install -r requirements.txt
streamlit run app.py
