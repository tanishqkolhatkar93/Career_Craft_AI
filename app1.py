import streamlit as st
import os
import requests

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="CareerCraft AI Prototype",
    page_icon="💼",
    layout="wide"
)

# ------------------- CUSTOM CSS -------------------
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .big-title {
        font-size: 32px !important;
        font-weight: 700;
        color: #2E86C1;
        margin-bottom: 15px;
    }
    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f9f9f9;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .metric {
        background: #eaf2f8;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric h2 {
        margin: 0;
        font-size: 28px;
        color: #1A5276;
    }
    .metric p {
        margin: 0;
        font-size: 14px;
        color: #424949;
    }
    </style>
""", unsafe_allow_html=True)



# ------------------- LLM (Groq) -------------------

GROQ_API_KEY = "***********************************************"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"



def get_llm_response(prompt):
    if not GROQ_API_KEY:
        return "⚠️ Please set your GROQ_API_KEY."
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.7
        }
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=30)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error: {e}"


import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        data = response.json()

        # ✅ Check if 'choices' exists before accessing
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return f"⚠️ API returned unexpected response: {data}"
    except Exception as e:
        return f"❌ Error: {str(e)}"




# ------------------- SIDEBAR -------------------
st.sidebar.title("🧭 CareerCraft AI ")
page = st.sidebar.radio(
    "Choose a feature:",
    ["📄 ATS Resume Optimizer", "💼 Job Matcher", "🎤 AI Interview Prep"]
)

# ------------------- PAGE 1: ATS Resume Optimizer -------------------
if page == "📄 ATS Resume Optimizer":
    st.markdown("<p class='big-title'>📄 ATS Resume Optimizer</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📂 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric'><h2>85%</h2><p>ATS Score</p></div>", unsafe_allow_html=True)
        st.markdown("**Suggestions to improve:**")
        st.markdown("""
        - Add **job-specific keywords**.  
        - Highlight **quantifiable achievements** (e.g., *boosted accuracy by 20%*).  
        - Optimize **Skills** & **Experience** for the target job.  
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------- PAGE 2: Job Matcher -------------------
elif page == "💼 Job Matcher":
    st.markdown("<p class='big-title'>💼 Smart Job Matcher</p>", unsafe_allow_html=True)
    jobs = [
        {"role": "Data Scientist Intern", "company": "TechCorp", "match": 92},
        {"role": "NLP Engineer", "company": "OpenAI", "match": 85},
        {"role": "AI Research Assistant", "company": "DeepMind", "match": 78},
    ]
    for job in jobs:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"🔹 {job['role']} @ {job['company']}")
        st.progress(job['match']/100)
        st.write(f"✅ Match Score: **{job['match']}%**")
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------- PAGE 3: AI Interview Prep -------------------
elif page == "🎤 AI Interview Prep":
    st.markdown("<p class='big-title'>🎤 AI Interview Prep (Powered by LLaMA-3)</p>", unsafe_allow_html=True)
    role = st.text_input("Enter Job Role", placeholder="e.g., Data Scientist")
    if st.button("🚀 Generate AI Questions"):
        if role:
            prompt = (f"Generate 5 interview questions for a {role} role. "
                      "Mix HR, behavioral, scenario-based, and technical questions.")
            st.info("⏳ Fetching interview questions from LLaMA-3 (Groq API)...")
            result = get_llm_response(prompt)
            st.subheader("🤖 AI-Generated Questions:")
            st.write(result)
        else:
            st.warning("⚠️ Please enter a job role first.")



