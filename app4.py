import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av, numpy as np, requests, json, pandas as pd, PyPDF2
from io import StringIO
import os


# --- CONFIG ---
st.set_page_config(page_title="CareerCraft AI – Interview Coach", layout="wide")

#GROQ_API_KEY = st.secrets["************************************"]

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

# --- UTILITIES ---
def extract_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def groq_request(prompt, max_tokens=400):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()["choices"][0]["message"]["content"]

def generate_questions(resume, job_title, jd):
    prompt = f"""
Create 1 questions each for Technical, Scenario-based, Behavioral, and HR interviews.
Job Title: {job_title}
Job Description: {jd}
Resume: {resume[:1000]}
Format response oganized subheadings as : Technical, Scenario, Behavioral, HR.
"""
    out = groq_request(prompt)
    try:
        return json.loads(out)
    except:
        return {"Technical": [out]}

def evaluate_answer(question, answer):
    prompt = f"""
Evaluate this answer:
Question: {question}
Answer: {answer}
Rate 1-5 and give concise feedback. Return JSON: {{"score":int,"feedback":"string"}}.
"""
    out = groq_request(prompt)
    try:
        return json.loads(out)
    except:
        return {"score": 3, "feedback": out}

def transcribe_audio(audio_array):
    prompt = "Simulate transcription: summarize the user’s audio response as text."
    return groq_request(prompt)

# --- HEADER ---
st.markdown(
    "<h1 style='text-align:center; color:#4CAF50;'>🎙 CareerCraft AI – AI Interview Coach</h1>"
    "<p style='text-align:center;'>Upload your resume, select a job title, and practice interviews with AI-driven feedback.</p><hr>",
    unsafe_allow_html=True,
)

# --- INPUT ---
uploaded = st.file_uploader("📄 Upload Resume (PDF or TXT):", type=["pdf", "txt"])
resume_text = ""
if uploaded:
    if uploaded.type == "application/pdf":
        resume_text = extract_pdf(uploaded)
    else:
        resume_text = StringIO(uploaded.getvalue().decode("utf-8")).read()

resume_text = st.text_area("Or paste your resume:", value=resume_text, height=200)
job_title = st.text_input("🎯 Job Title", placeholder="e.g., Data Scientist")
jd = st.text_area("📝 Job Description (Optional)")

# --- GENERATE QUESTIONS ---
if st.button("🚀 Generate Questions"):
    if not resume_text or not job_title:
        st.error("Please upload/paste a resume and enter a job title.")
    else:
        with st.spinner("Generating questions..."):
            st.session_state["qs"] = generate_questions(resume_text, job_title, jd)
            st.session_state["results"] = []

# --- AUDIO PROCESSOR CLASS ---
class AudioProcessor(AudioProcessorBase):
    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        mono = audio.mean(axis=1) if audio.ndim > 1 else audio
        # Here we just store audio samples for later transcription
        if not hasattr(self, "recorded"):
            self.recorded = []
        self.recorded.extend(mono.tolist())
        return frame

# --- DISPLAY QUESTIONS ---
if "qs" in st.session_state:
    st.subheader("📋 Your AI Interview Questions")
    for category, qlist in st.session_state["qs"].items():
        st.markdown(f"### {category}")
        for i, q in enumerate(qlist):
            st.markdown(f"**Q{i+1}:** {q}")
            ans = st.text_area(f"Your Text Answer (Optional)", key=f"a_{category}_{i}")

            st.write("🎤 Record your answer (optional):")
            ctx = webrtc_streamer(
                key=f"audio_{category}_{i}",
                mode=WebRtcMode.SENDONLY,
                audio_receiver_size=256,
                media_stream_constraints={"audio": True, "video": False},
                audio_processor_factory=AudioProcessor
            )

            audio_text = ""
            if ctx and ctx.audio_receiver and st.button(f"📝 Transcribe {category}-{i+1}", key=f"t_{category}_{i}"):
                with st.spinner("Transcribing..."):
                    audio_data = np.array(ctx.audio_processor.recorded) if hasattr(ctx.audio_processor, "recorded") else np.array([])
                    audio_text = transcribe_audio(audio_data)
                    st.success(f"Transcribed Answer: {audio_text}")

            final_answer = ans if ans else audio_text
            if final_answer and st.button(f"✅ Evaluate {category}-{i+1}", key=f"eval_{category}_{i}"):
                with st.spinner("Evaluating..."):
                    feedback = evaluate_answer(q, final_answer)
                    st.success(f"⭐ Score: {feedback['score']} — {feedback['feedback']}")
                    st.session_state["results"].append({
                        "category": category,
                        "question": q,
                        "answer": final_answer,
                        "score": feedback['score'],
                        "feedback": feedback['feedback'],
                    })

# --- SUMMARY ---
if st.session_state.get("results"):
    st.subheader("📊 Performance Summary")
    df = pd.DataFrame(st.session_state["results"])
    st.dataframe(df)
    st.download_button("⬇ Download Results", df.to_csv(index=False), "interview_results.csv")




