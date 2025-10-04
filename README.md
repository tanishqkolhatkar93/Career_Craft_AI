# 🚀 CareerCraft AI — End-to-End AI Career Copilot  

> 🧠 Empowering students and jobseekers with ATS-optimized resumes, intelligent job matching, and AI-driven interview preparation — all in one platform.  

---

## 🌟 Overview  

**CareerCraft AI** is an **AI-powered career acceleration platform** designed to help users:  
1. Build **ATS-friendly resumes** aligned with specific job descriptions.  
2. Get **AI-based interview preparation** (technical, HR, behavioral, scenario-based).  
3. Interact with an intelligent **RAG chatbot** trained on CareerCraft documentation — answering queries about ATS optimization, interview readiness, and platform use.  

This project combines **Natural Language Processing (NLP)**, **Retrieval-Augmented Generation (RAG)**, **LLMs (Groq LLaMA)**, and a **Streamlit-based UI** to deliver a seamless experience from **resume to recruitment**.  

---

## 🎯 Key Features  

### 🧩 1. ATS Resume Optimizer  
- Parses uploaded resumes and job descriptions.  
- Uses **Groq LLaMA-based LLMs** to rewrite and optimize resumes for **100% ATS compliance**.  
- Suggests skill alignment and keyword improvements dynamically.  

### 💬 2. AI Interview Coach  
- Personalized interview prep based on user’s resume + job role.  
- Generates **scenario, technical, HR, and behavioral** questions using Groq LLM API.  
- Integrated **speech-based response** evaluation using `streamlit-webrtc`.  

### 🔍 3. RAG Chatbot (CareerCraft Assistant)  
- Retrieval-Augmented Generation system built with **LangChain + FAISS + Groq API**.  
- Upload PDFs (e.g., platform guides or FAQs) — the bot answers questions using contextual retrieval.  
- Elegant Streamlit UI with real-time chat bubbles, fallbacks, and Groq-based text generation.  

### ☁️ 4. Scalable Cloud Architecture  
- Backend services containerized via **Docker**.  
- Designed for **AWS / Render deployment** with persistent FAISS or Pinecone vector DB.  
- Supports continuous improvement through modular API layers.  

---

## 🧠 Tech Stack  

| Category | Technology |
|-----------|-------------|
| **Frontend / UI** | Streamlit (custom CSS + animations) |
| **Backend** | Python, Flask (optional integration) |
| **AI / NLP** | LangChain, Groq LLaMA, Sentence-BERT |
| **Vector Store** | FAISS (local) or Pinecone (scalable) |
| **Embeddings** | Groq API + SBERT fallback |
| **Audio / Speech** | streamlit-webrtc |
| **Version Control** | GitHub |
| **Deployment** | Docker + AWS EC2 / Streamlit Cloud |

---

## 🏗️ System Architecture  

```
                ┌────────────────────────────┐
                │  PDF / Resume / JD Upload  │
                └──────────────┬─────────────┘
                               │
                         Text Extraction
                               │
                        Chunking + Embeddings
                         (Groq / SBERT)
                               │
                 ┌─────────────▼──────────────┐
                 │  FAISS Vector DB Storage   │
                 └─────────────┬──────────────┘
                               │
                         Query Embedding
                               │
                     Top-K Document Retrieval
                               │
                     LLM (Groq LLaMA) Response
                               │
                ┌──────────────▼───────────────┐
                │ Streamlit Chat + Dashboard   │
                └──────────────────────────────┘
```

---

## 💻 Installation  

```bash
# Clone the repository
git clone https://github.com/tanishqkolhatkar93/Career_Craft_AI.git
cd Career_Craft_AI

# Create environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🔑 Environment Variables  

Create a `.streamlit/secrets.toml` file or set environment variables:  
```toml
[GROQ]
GROQ_API_KEY = "your_groq_api_key_here"
```

---

## 📊 Project Highlights  

| Component | Description |
|------------|--------------|
| **RAG Chatbot** | Answers CareerCraft-related queries using vector retrieval |
| **Resume Optimizer** | Enhances resume keyword density for target JD |
| **Interview Module** | LLM-driven personalized Q&A generation |
| **Dashboard** | Tracks upload status, indexing progress, and user interaction |

---

## 🧩 Sample Use Case  

1. Upload your resume and a Job Description.  
2. CareerCraft AI optimizes it for ATS compliance.  
3. Get a ranked list of job matches.  
4. Practice interviews via AI voice Q&A.  
5. Use the built-in chatbot for platform help and career guidance.  

---

## 📈 Results / Screenshots  

![CareerCraft Dashboard](assets/dashboard.png)
![RAG Chatbot Demo](assets/rag_chatbot.png)
![ATS Resume Optimizer](assets/resume_optimizer.png)

---

## 🧩 Future Roadmap  

✅ **Phase 1:** ATS Resume Optimizer + Job Matching  
✅ **Phase 2:** RAG Chatbot Integration  
🚧 **Phase 3:** Voice-based Interview Simulation  
🚧 **Phase 4:** Analytics Dashboard + Global Deployment  

---

## 🤝 Contributing  

Pull requests are welcome! For major changes, open an issue first to discuss the proposed modifications.  
Please ensure your code follows the repo’s linting and formatting conventions.  

---

## 📬 Contact  

**👨‍💻 Tanishq Kolhatkar**  
📧 [tanishqkolhatkar93@gmail.com](mailto:tanishqkolhatkar93@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/tanishqkolhatkar93/)  
💻 [GitHub](https://github.com/tanishqkolhatkar93)  

---

## ⭐ Support  

If you found this project helpful or inspiring, please ⭐ **star the repository** and share it with your network!  

> “CareerCraft AI — Redefining how students and professionals prepare, apply, and get hired.”  
