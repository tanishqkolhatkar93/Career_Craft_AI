# rag_groq_chatbot.py
import streamlit as st
import PyPDF2
from io import BytesIO
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import requests

# ---- Streamlit Config ----
st.set_page_config(page_title="CareerCraft AI - RAG Chatbot", layout="wide")

st.markdown("""
<style>
.chat-user {background:#000c0e; border-radius:10px; padding:10px; margin:6px 0;}
.chat-bot {background: #000c0e; border-radius:10px; padding:10px; margin:6px 0;}
.error-box {background:#000c0e; color:#991B1B; padding:10px; border-radius:8px; margin:6px 0;}
</style>
""", unsafe_allow_html=True)

# ---- Groq Setup ----
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None) or "your_api_key_here"
GROQ_LLM_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# ---- Helpers ----
def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    text = [p.extract_text() or "" for p in reader.pages]
    return "\n".join(text)

def embed_texts(texts, model):
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def build_faiss_index(embs):
    dim = embs.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embs)
    return index

def search_index(query, chunks, model, index, embs, k=3):
    q_emb = embed_texts([query], model)
    D, I = index.search(q_emb, k)
    return [chunks[i] for i in I[0]]

def call_groq(prompt):
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        payload = {
            "model": "llama-3.1-8b-instant",  # Groq recommended fast LLM
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 300
        }
        r = requests.post(GROQ_LLM_ENDPOINT, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.markdown(f'<div class="error-box">⚠️ Error: {e}</div>', unsafe_allow_html=True)
        return None

# ---- App Logic ----
st.title("💬 CareerCraft AI — RAG Chatbot")

if "convo" not in st.session_state:
    st.session_state.convo = []
if "chunks" not in st.session_state:
    st.session_state.chunks, st.session_state.embs, st.session_state.index = [], None, None

uploaded = st.file_uploader("📄 Upload PDF (Knowledge Base)", type=["pdf"], accept_multiple_files=False)
if uploaded and st.button("Process PDF"):
    with st.spinner("Processing PDF..."):
        text = extract_text_from_pdf(uploaded.read())
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embs = embed_texts(chunks, model)
        index = build_faiss_index(embs)

        st.session_state.chunks = chunks
        st.session_state.embs = embs
        st.session_state.index = index
    st.success("✅ PDF indexed. Ask questions now!")

st.markdown("---")

for role, msg in st.session_state.convo:
    if role == "user":
        st.markdown(f'<div class="chat-user"><b>You:</b> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot"><b>CareerCraft Bot:</b> {msg}</div>', unsafe_allow_html=True)

user_q = st.text_input("💡 Ask a question:")

if st.button("Ask") and user_q.strip():
    if not st.session_state.index:
        st.warning("⚠️ Please upload and process a PDF first.")
    else:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        context = search_index(user_q, st.session_state.chunks, model, st.session_state.index, st.session_state.embs)
        context_text = "\n".join(context)

        prompt = f"""You are CareerCraft AI assistant.
Use the following context to answer the user's question.

Context:
{context_text}

Question: {user_q}
Answer clearly for a student/job seeker:"""

        answer = call_groq(prompt)
        if not answer:  # Fallback if Groq fails
            answer = "Fallback Answer:\n" + context_text[:300]

        st.session_state.convo.append(("user", user_q))
        st.session_state.convo.append(("bot", answer))
        st.rerun()
