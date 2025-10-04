import streamlit as st
import requests, json, base64, os
import pandas as pd
from io import StringIO
import PyPDF2

# Optional audio recorder
try:
    from streamlit_audio_recorder import audio_recorder
    AUDIO = True
except:
    AUDIO = False

st.set_page_config(page_title="CareerCraft AI - Groq Interview Coach", layout="centered")

# --- Helper functions ---
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_text_file(file):
    return StringIO(file.getvalue().decode("utf-8")).read()

def groq_request(api_key, prompt, max_tokens=600):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        st.error(f"Groq API Error: {resp.text}")
        return None
    return resp.json()["choices"][0]["message"]["content"]

def generate_questions(api_key, resume, job_title, jd, n_each=3):
    prompt = f"""
Generate {n_each} interview questions each for:
1. Technical
2. Scenario-based
3. Behavioral
4. HR

Tailor them for Job Title: {job_title}
Job Description: {jd or 'N/A'}
Resume (first 1000 chars): {resume[:1000]}

Return JSON with keys: Technical, Scenario, Behavioral, HR.
"""
    out = groq_request(api_key, prompt)
    try:
        return json.loads(out)
    except:
        # fallback parse
        return {"Technical": [out]}

def evaluate_answer(api_key, question, answer):
    prompt = f"""
Question: {question}
Candidate Answer: {answer}

Rate this answer on a scale of 1–5 and provide one-sentence constructive feedback.
Return JSON: {{"score": int, "feedback": "string"}}
"""
    out = groq_request(api_key, prompt)
    try:
        return json.loads(out)
    except:
        return {"score": 3, "feedback": out}

# --- UI ---
st.title("🤖 CareerCraft AI — Groq Interview Coach")
st.markdown("Practice AI-powered mock interviews tailored to your **resume** and **job title**.")

with st.sidebar:
    n_each = st.slider("Questions per Category", 1, 5, 3)
    use_audio = st.checkbox("Enable Audio Recorder", value=AUDIO)

st.subheader("Step 1: Upload Your Resume")
uploaded = st.file_uploader("Upload PDF or TXT resume", type=["pdf","txt"])
resume_text = ""
if uploaded:
    if uploaded.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded)
    else:
        resume_text = load_text_file(uploaded)

resume_text = st.text_area("Or paste your resume:", value=resume_text, height=200)

job_title = st.text_input("Step 2: Enter Job Title", placeholder="e.g. Data Scientist - NLP")
jd = st.text_area("Step 3: Paste Job Description (optional)")

if st.button("🚀 Generate Questions") and api_key:
    with st.spinner("Generating tailored questions..."):
        qs = generate_questions(api_key, resume_text, job_title, jd, n_each=n_each)
        st.session_state["qs"] = qs
        st.session_state["answers"] = []
        st.success("Questions ready! Scroll down.")

if "qs" in st.session_state:
    st.subheader("Step 4: Practice Interview")
    for cat, qlist in st.session_state["qs"].items():
        st.markdown(f"### 📌 {cat}")
        for idx, q in enumerate(qlist):
            st.write(f"**Q{idx+1}:** {q}")
            ans = st.text_area(f"Your Answer for {cat}-{idx+1}", key=f"a_{cat}_{idx}")
            if use_audio and AUDIO:
                audio = audio_recorder(f"Record Answer {cat}-{idx+1}", key=f"aud_{cat}_{idx}")
                if audio:
                    st.audio(audio)
            if st.button(f"Evaluate Answer {cat}-{idx+1}", key=f"eval_{cat}_{idx}") and api_key:
                feedback = evaluate_answer(api_key, q, ans)
                st.session_state["answers"].append({
                    "category": cat,
                    "question": q,
                    "answer": ans,
                    "score": feedback.get("score"),
                    "feedback": feedback.get("feedback")
                })
                st.success(f"Score: {feedback.get('score')} — {feedback.get('feedback')}")

if st.session_state.get("answers"):
    st.subheader("📊 Session Summary")
    df = pd.DataFrame(st.session_state["answers"])
    st.dataframe(df)
    st.download_button("⬇ Download CSV", df.to_csv(index=False), "interview_results.csv")

