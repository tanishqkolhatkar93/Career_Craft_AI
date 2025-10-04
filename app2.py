import streamlit as st
import requests, os
from PyPDF2 import PdfReader

# --- CONFIG ---
st.set_page_config(page_title="AI Interview Prep", page_icon="🤖", layout="wide")

# --- GET API KEY ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
if not GROQ_API_KEY:
    st.error("❌ Missing API key. Please add GROQ_API_KEY to .streamlit/secrets.toml.")
    st.stop()

# --- HELPER: Extract text from PDF ---
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# --- HELPER: Generate questions using Groq ---
def generate_questions(job_role, resume_text):
    prompt = f"""
    You are an experienced technical interviewer. 
    Based on the following job role and resume, generate **6 interview questions**:
    - Mix: 2 technical (specific to the role), 2 behavioral, 2 scenario-based.
    - Be concise and clear.
    
    Job Role: {job_role}
    Resume Summary: {resume_text[:1500]}  # limited for context
    """
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=30
        )
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        return f"⚠️ API Error: {data}"
    except Exception as e:
        return f"⚠️ Request failed: {e}"

# --- UI ---
st.title("🤖 AI Interview Preparation")
st.markdown("Upload your resume and specify a job role to generate tailored interview questions.")

col1, col2 = st.columns(2)
with col1:
    job_role = st.text_input("Enter Job Role", placeholder="e.g., Data Scientist, NLP Engineer")

with col2:
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file and job_role:
    resume_text = extract_text_from_pdf(uploaded_file)
    if st.button("Generate Interview Questions"):
        with st.spinner("🔎 Analyzing resume and job role... Generating questions..."):
            questions = generate_questions(job_role, resume_text)
        st.subheader("📋 AI-Generated Interview Questions")
        st.write(questions)
else:
    st.info("ℹ️ Please upload a resume and enter a job role to proceed.")

# --- Footer ---
st.markdown("---")
st.caption("⚡ Built with Streamlit + Groq LLM | Tailored AI Interview Prep")
