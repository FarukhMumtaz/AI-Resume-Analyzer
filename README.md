# 🚀 AI Resume Analyzer — Smart ATS & Job Match Assistant

> **Hackathon Edition** · Powered by OpenAI / Gemini · Built with Streamlit

A complete AI-powered Resume Analyzer that extracts skills, calculates job match percentage, estimates ATS score, suggests missing skills, generates interview questions, and provides voice feedback — all dynamically based on your actual resume content.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Resume Upload | PDF, DOCX, TXT support |
| 🧠 Skill Extraction | 50+ skills across 8 categories |
| 🎯 Job Match % | Dynamic, resume-specific scoring |
| 🤖 ATS Score | 6-factor weighted ATS analysis |
| ⚠️ Missing Skills | Only shows skills genuinely absent from your resume |
| ❓ Interview Questions | 5 personalized questions per resume |
| 🔊 Voice Feedback | Audio feedback via gTTS |
| 📥 Download Report | Full analysis as TXT |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (wide layout, custom CSS, dark theme)
- **AI**: OpenAI GPT-4o-mini / Google Gemini 1.5 Flash
- **PDF Parsing**: pypdf
- **DOCX Parsing**: python-docx
- **Voice**: gTTS
- **Fallback**: Dynamic keyword-based scoring (no API needed)

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py              ← Main Streamlit frontend
├── ai_utils.py         ← AI integration (OpenAI + Gemini + fallback)
├── resume_parser.py    ← PDF/DOCX/TXT text extraction
├── scoring.py          ← Skill extraction, ATS & job match scoring
├── requirements.txt
├── .env.example
├── .gitignore
└── .streamlit/
    └── config.toml
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY or GEMINI_API_KEY

# 5. Run the app
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub (without `.env` or `secrets.toml`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as the main file
4. Go to **App Settings → Secrets** and add:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   # OR
   GEMINI_API_KEY = "AI-your-key-here"
   ```
5. Deploy!

---

## 🔑 API Keys

| Variable | Provider | Get Key |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI (preferred) | [platform.openai.com](https://platform.openai.com/api-keys) |
| `GEMINI_API_KEY` | Google Gemini | [aistudio.google.com](https://aistudio.google.com/app/apikey) |

> The app works **without an API key** using the built-in dynamic keyword fallback engine.

---

## 🎯 Demo Presentation (5 min)

1. Open the app → show the professional UI
2. Upload a **Python Developer** resume → analyze → show skills, match %, ATS score
3. Upload a **Cybersecurity** resume → show different results instantly
4. Paste a job description → show how missing skills change
5. Play voice feedback → download report

**Key message**: *"Every resume produces a unique, AI-driven analysis. The results you see are based exclusively on the content of the uploaded resume."*

---

## 📌 Notes

- Scores are estimated using AI + keyword matching and reflect actual resume content
- Image-based/scanned PDFs are not supported (text must be extractable)
- Results will always differ between different resumes

---

*Built for the AI Hackathon · Smart ATS & Job Match Assistant*
