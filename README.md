# 🤖 AI Interview Agent

An AI-powered mock interview platform built using **Python, Streamlit, and Groq LLM**. The application generates role-specific interview questions, evaluates candidate answers using AI, and provides a final hiring recommendation.

---

## 📌 Features

- 👤 Candidate Details
- 📄 Resume Upload (PDF)
- 🤖 AI-Generated Interview Questions
- 💬 One Question at a Time
- 📝 AI Answer Evaluation
- ⭐ Score (0–10) for Each Answer
- 📊 Overall Score
- 📈 Average Score
- 💪 Strengths & Weaknesses
- ✅ Hiring Recommendation
- 💾 Interview Transcript (JSON)
- 📋 Evaluation Report (JSON)

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.3 70B Versatile
- PyPDF2
- JSON

---

## 📂 Project Structure

```text
AI-Interview-Agent/
│
├── app.py
├── interview_agent.py
├── prompts.py
├── resume_parser.py
├── utils.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── transcript.json
├── evaluation.json
├── Screenshots
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Kirangr5/AI-Interview-Agent.git
```

### Go to the project folder

```bash
cd AI-Interview-Agent
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Groq API Setup

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---



## 🚀 Future Improvements

- Voice Interview
- PDF Report
- Database Integration
- User Authentication
- Interview History
- Company-Specific Interview Modes

---

