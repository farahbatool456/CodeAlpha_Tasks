# 🤖 FAQ Chatbot — AI-Powered Question Answering System

> A smart, beginner-friendly FAQ chatbot built with Python, NLP, and Streamlit.  
> Uses **TF-IDF + Cosine Similarity** to match user questions with the most relevant stored FAQ.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red?style=flat-square&logo=streamlit)
![NLTK](https://img.shields.io/badge/NLTK-3.8%2B-green?style=flat-square)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## 📋 Table of Contents

- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [FAQ Dataset](#-faq-dataset)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)
- [LinkedIn Description](#-linkedin-project-description)

---

## ✨ Features

### Core Features
- 🔍 **Smart Question Matching** — TF-IDF + Cosine Similarity finds the most relevant FAQ
- 🧹 **NLP Preprocessing** — Tokenization, stop word removal, and lemmatization
- 📊 **Confidence Scoring** — Shows how confident the bot is in its answer (High / Medium / Low)
- 📂 **Multi-Category FAQs** — 50 FAQs across College, E-commerce, Banking, Internship, General
- 🔽 **Category Filter** — Narrow searches to a specific topic for better accuracy

### UI Features
- 💬 **Modern Chat Interface** — User/bot chat bubbles with animations
- 🌙 **Dark / Light Mode** — Toggle between themes in the sidebar
- 📜 **Chat History** — Persistent conversation during the session
- 🗑️ **Clear Chat** — Reset conversation with one click
- ⚡ **Quick-Ask Buttons** — Pre-built sample questions for fast testing
- 📥 **Export Chat** — Download conversation history as a .txt file

### Error Handling
- Empty input detection
- Dataset file not found
- Invalid JSON format
- No matching answer found
- NLP processing failures

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Frontend web UI framework |
| **NLTK** | Tokenization, stop word removal, lemmatization |
| **scikit-learn** | TF-IDF vectorization, cosine similarity |
| **NumPy** | Numerical operations on similarity score arrays |
| **JSON** | FAQ dataset storage format |

---

## 📁 Project Structure

```
FAQ_Chatbot_Project/
│
├── app.py                  ← Main Streamlit app (UI entry point)
├── chatbot.py              ← NLP engine (TF-IDF + cosine similarity)
├── faq_data.json           ← FAQ dataset (50 Q&As across 5 categories)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
│
├── utils/
│   ├── __init__.py         ← Makes utils a Python package
│   ├── preprocessor.py     ← NLP preprocessing functions
│   └── faq_loader.py       ← JSON loading and validation
│
├── styles/
│   └── chat.css            ← Custom CSS for chat bubbles and animations
│
├── assets/                 ← Icons, logos (optional)
├── models/                 ← Saved model files (future use)
└── screenshots/            ← App screenshots for README/portfolio
```

---

## 🧠 How It Works

### Step-by-Step Flow

```
User types question
        ↓
1. VALIDATION: Check if input is valid (not empty, not too short/long)
        ↓
2. PREPROCESSING (utils/preprocessor.py):
   "How do I RESET my Password??"
        ↓ lowercase
   "how do i reset my password"
        ↓ remove special chars
   "how do i reset my password"
        ↓ tokenize
   ["how", "do", "i", "reset", "my", "password"]
        ↓ remove stopwords (do, i, my)
   ["reset", "password"]
        ↓ lemmatize
   ["reset", "password"]
        ↓
3. TF-IDF VECTORIZATION (chatbot.py):
   ["reset", "password"] → [0.0, 0.71, 0.0, 0.52, 0.0, ...]  (numerical vector)
        ↓
4. COSINE SIMILARITY:
   Compare query vector vs every FAQ vector
   FAQ #1: similarity = 0.12
   FAQ #2: similarity = 0.87  ← BEST MATCH
   FAQ #3: similarity = 0.04
   ...
        ↓
5. THRESHOLD CHECK:
   Score ≥ 0.50 → High confidence answer
   Score 0.25–0.49 → Medium confidence (show answer with warning)
   Score < 0.10 → No match (fallback message)
        ↓
6. DISPLAY answer in chat bubble with confidence badge
```

### What is TF-IDF? (Simple Explanation)

**TF = Term Frequency**: How often a word appears in one question.  
**IDF = Inverse Document Frequency**: How rare a word is across ALL questions.

- "the" appears in 50/50 FAQs → low IDF → almost ignored
- "lemmatization" appears in 1/50 FAQs → high IDF → very important

**TF-IDF = TF × IDF**  
Words common in ONE question but rare everywhere else get high scores.  
These are the "fingerprint words" that identify what a question is about.

### What is Cosine Similarity? (Simple Explanation)

Imagine each text as an arrow pointing in some direction in space.

- Two texts about the same topic → arrows point in similar directions → angle ≈ 0° → similarity ≈ 1.0
- Two unrelated texts → arrows point in different directions → angle ≈ 90° → similarity ≈ 0.0

We don't care how long the texts are — only the DIRECTION (topic).

```
Similarity = cos(θ) = (A · B) / (|A| × |B|)

Where A = query vector, B = FAQ vector, θ = angle between them
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone or Download the Project

```bash
# Option A: Clone with Git
git clone https://github.com/YOUR_USERNAME/faq-chatbot.git
cd faq-chatbot

# Option B: Download ZIP from GitHub and extract it
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab')"
```

> **Note:** The app also does this automatically on first run. But running it manually ensures there are no delays.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🚀 Usage

1. **Type a question** in the input box at the bottom and press Enter or click **Send**
2. **Select a category** from the sidebar to narrow the search scope
3. **Click quick-ask buttons** to test pre-built questions instantly
4. **Toggle dark mode** in the sidebar for a different look
5. **Clear chat** with the button in the sidebar
6. **Export** your conversation with the Export Chat option

---

## 📚 FAQ Dataset

The `faq_data.json` file contains **50 real-world FAQs** across 5 categories:

| Category | Count | Example Topics |
|---|---|---|
| 🎓 College | 10 | Admissions, financial aid, registration, housing |
| 🛒 Ecommerce | 10 | Orders, payments, returns, delivery, tracking |
| 🏦 Banking | 10 | Accounts, transactions, loans, security, ATM |
| 💼 Internship | 10 | Application, pay, duration, skills, projects |
| 🌐 General | 10 | Password reset, mobile app, 2FA, referrals |

To add more FAQs, simply follow the existing JSON structure:

```json
{
  "id": "X001",
  "question": "Your question here?",
  "answer": "Your detailed answer here."
}
```

---

## 📸 Screenshots

> Add screenshots to the `screenshots/` folder and update the paths below.

### Light Mode Chat Interface
```
screenshots/light_mode.png
```

### Dark Mode
```
screenshots/dark_mode.png
```

### Sidebar with Stats
```
screenshots/sidebar.png
```

### Confidence Score Display
```
screenshots/confidence_score.png
```

**How to take screenshots:**
1. Run the app with `streamlit run app.py`
2. Press `F12` → Browser screenshot, OR use `Windows + Shift + S` (Windows) / `Cmd + Shift + 4` (Mac)
3. Save screenshots in the `screenshots/` folder
4. Update the image paths above in this README

---

## 🔮 Future Improvements

| Feature | Description | Difficulty |
|---|---|---|
| 🎤 Voice Input | Speech-to-text using `SpeechRecognition` | Medium |
| 🔊 Text-to-Speech | Bot reads answers aloud using `gTTS` or `pyttsx3` | Medium |
| 🌍 Multi-language | Translate queries using `googletrans` | Medium |
| 🧠 Transformer Model | Use `sentence-transformers` for better semantic matching | Advanced |
| 💾 Persistent History | Save chat history using SQLite or JSON file | Easy |
| 📊 Analytics Dashboard | Track popular questions and match rates | Medium |
| 🔄 Live FAQ Updates | Edit FAQs through the UI without touching JSON | Medium |
| 🤖 GPT Fallback | Use OpenAI API when no FAQ match found | Advanced |
| 📧 Email Integration | Email unanswered questions to support team | Medium |

---

## 🔗 LinkedIn Project Description

Use this text when posting the project on LinkedIn:

---

**🤖 Built an AI-Powered FAQ Chatbot using Python & NLP!**

Excited to share my latest project — a smart FAQ chatbot that answers user questions using Natural Language Processing!

**🛠️ Tech Stack:**
• Python + Streamlit (frontend)
• NLTK (tokenization, lemmatization, stop word removal)
• TF-IDF Vectorization (scikit-learn)
• Cosine Similarity (semantic matching)

**✨ Key Features:**
✅ 50 FAQs across 5 categories (College, E-commerce, Banking, Internship)
✅ Smart NLP preprocessing pipeline
✅ Confidence score for every answer
✅ Dark/Light mode toggle
✅ Real-time chat interface with animations
✅ Category filter for focused searching
✅ Export chat history

**📐 How it works:**
User query → NLP preprocessing → TF-IDF vectorization → Cosine similarity → Best matching FAQ

The chatbot doesn't just search for keywords — it understands the *intent* behind questions using vector mathematics!

**🔗 GitHub:** [your-github-link]
**🎥 Demo:** [your-demo-link]

#Python #MachineLearning #NLP #Streamlit #AIChatbot #Internship #Portfolio #DataScience

---

## 📄 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this project for educational and commercial purposes.

---

## 🙋 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

---

*Built as an internship portfolio project demonstrating NLP fundamentals and Python web development.*
