# ⬡ LinguaFlow — Language Translation Tool

A clean, responsive, beginner-friendly web application that translates text between 30+ languages using in this project. Built with pure HTML, CSS, and JavaScript — no frameworks, no build tools.

![LinguaFlow Screenshot](assets/screenshot.png)

---

## ✨ Features

| Feature | Details |
|---|---|
| 🌍 30+ Languages | Urdu, Arabic, Chinese, French, Spanish, Hindi, and more |
| 🤖 AI-Powered | Uses Claude (Anthropic) for context-aware, idiomatic translation |
| 🔊 Text-to-Speech | Speak source text or translation aloud (Web Speech API) |
| 📋 Copy Button | One-click copy of translated output |
| 🔄 Swap Languages | Instantly swap source ↔ target language + text |
| 🌙 Dark / Light Mode | System preference detected; toggle saved to localStorage |
| ⌨️ Keyboard Shortcut | `Ctrl+Enter` (or `Cmd+Enter`) to translate |
| 📱 Responsive | Works on mobile, tablet, and desktop |
| ⚠️ Error Handling | Friendly messages for network errors, API limits, auth issues |
| ⚡ Loading Animation | Shimmer skeleton while waiting for the API response |

---

## 🗂️ Project Structure

```
language-translation-tool/
├── index.html          ← Main page (markup + structure)
├── css/
│   └── style.css       ← All styles (CSS variables, responsive, dark mode)
├── js/
│   ├── languages.js    ← Language list (codes + speech codes)
│   ├── ui.js           ← DOM references + visual state functions
│   ├── api.js          ← Anthropic API call logic
│   └── app.js          ← Main controller — wires everything together
├── assets/
│   └── screenshot.png  ← (add your own screenshot here)
└── README.md
```

---

## 🚀 Quick Start (Local)

### Option A — Open Directly (Simplest)

1. Clone or download this repo.
2. Open `index.html` in your browser.
3. **Add your API key** (see below).
4. Start translating.

```bash
git clone https://github.com/YOUR_USERNAME/language-translation-tool.git
cd language-translation-tool
# Open index.html in your browser
```

### Option B — Local Server (Recommended)

```bash
# Using Python 3
python -m http.server 3000
# Visit http://localhost:3000
```

```bash
# Using Node.js / npx
npx serve .
```

---

## 🔑 API Setup

This project uses the **Anthropic Claude API** for translation.

### Get Your API Key

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create an account and go to **API Keys**
3. Click **Create Key** and copy it

### Add the API Key

Open `js/api.js` and find this section in the `fetch` headers:

```javascript
headers: {
  'Content-Type': 'application/json',
  // Add your key here:
  'x-api-key': 'YOUR_API_KEY_HERE',
  'anthropic-version': '2023-06-01',
  'anthropic-dangerous-direct-browser-access': 'true', // required for browser calls
},
```

> ⚠️ **Security Warning**: Embedding API keys in client-side JavaScript is only acceptable for local development or learning projects. For a production/public app, you must route API calls through your own backend server to keep the key secret.

### Backend Proxy (Production Setup)

For a real deployed app, create a simple Node.js/Express backend:

```javascript
// server.js (Node.js + Express)
const express = require('express');
const app = express();
app.use(express.json());

app.post('/translate', async (req, res) => {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': process.env.ANTHROPIC_API_KEY, // stored in .env
      'anthropic-version': '2023-06-01',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(req.body),
  });
  const data = await response.json();
  res.json(data);
});

app.listen(3000);
```

Then in `api.js`, change the URL to:
```javascript
const response = await fetch('/translate', { ... });
```

---

## 🧠 How It Works

1. **User selects** source language (or Auto Detect) and target language.
2. **User types** text into the source panel.
3. **On click** (or `Ctrl+Enter`), `app.js` validates the input and calls `translateText()` in `api.js`.
4. **`api.js`** builds a structured prompt and sends it to Claude via `fetch`.
5. **Claude returns** only the translated text (no extra commentary).
6. **`ui.js`** displays the result, enables the Copy and Speak buttons.

---

## 🔧 Customisation

- **Add languages**: Edit the `LANGUAGES` array in `js/languages.js`.
- **Change the default target language**: In `ui.js`, change `dom.targetLang.value = 'ur'` to any language code.
- **Change the AI model**: In `api.js`, update the `model` field (e.g., `claude-opus-4-20250514` for highest quality).
- **Adjust character limit**: Change `maxlength="1000"` in `index.html` and the `max` variable in `ui.js`.

---

## 🚧 Future Improvements

- [ ] **Translation history** — localStorage-based list of past translations
- [ ] **Favourite languages** — pin frequently used pairs
- [ ] **Romanisation/transliteration** — show phonetic pronunciation alongside script
- [ ] **Auto-detect language display** — show which language was detected
- [ ] **Word-by-word mode** — hover a word to see its individual translation
- [ ] **Backend proxy** — Express/FastAPI server so the API key is never exposed
- [ ] **Progressive Web App (PWA)** — offline support + installable icon
- [ ] **Multiple translation styles** — formal / casual / literal toggle
- [ ] **File upload** — translate .txt or .docx files

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| HTML5 | Structure and semantics |
| CSS3 | Styling, CSS variables, animations, responsive grid |
| JavaScript (ES6+) | Logic, fetch API, DOM manipulation |
| Claude API (Anthropic) | AI-powered translation |
| Web Speech API | Text-to-speech (browser built-in) |
| Clipboard API | Copy to clipboard |
| localStorage | Theme preference persistence |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👤 Author

Built as a portfolio project demonstrating:
- Clean modular JavaScript architecture
- API integration with proper error handling
- Modern, accessible UI design
- Responsive layout and dark mode
