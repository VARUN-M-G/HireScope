# utils.py – shared helpers for HireScope
import os, json, re
from datetime import datetime
import openai, chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import streamlit as st

# ---------- OpenAI key ----------
with open("config.json") as f:
    OPENAI_API_KEY = json.load(f)["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# ---------- Persistent Chroma client ----------
PERSIST_DIR = "./chroma_store"
os.makedirs(PERSIST_DIR, exist_ok=True)

@st.cache_resource
def get_persistent_client():
    # always PersistentClient so .persist() is available
    return chromadb.PersistentClient(path=PERSIST_DIR)

chroma_client = get_persistent_client()

def get_collection():
    return chroma_client.get_or_create_collection(
        name="resumes",
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name="text-embedding-3-small"
        )
    )

collection = get_collection()

# ---------- summariser ----------
def summarize_resume(raw: str) -> str:
    prompt = f"""
Return the résumé as structured **plain text** (NOT JSON) like:

Name: ...
Email: ...
Phone: ...
Location: ...
Skills: python, sql, ...
Languages: english, ...
Certifications: ...
Education:
  • Degree at University
Work Experience:
  • Role at Company (dates) – short summary
Latest Role: ...

Résumé:
\"\"\"{raw[:3000]}\"\"\""""
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()

# ---------- candidate ID ----------
def make_candidate_id(name: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]", "", name.lower())
    return f"{clean}_{datetime.now():%Y%m%d%H%M%S}"
