/**
 * app.js
 * ------
 * Main application controller.
 * Wires together: ui.js, api.js, languages.js.
 *
 * Responsibilities:
 *  - Initialise the page (dropdowns, theme)
 *  - Attach all event listeners
 *  - Orchestrate: collect input → call API → display result
 */

/* ============================================================
   INITIALISATION
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Populate language dropdowns from languages.js
  populateLanguageDropdowns();

  // 2. Apply saved/system theme
  initTheme();

  // 3. Attach all event listeners
  attachEventListeners();
});


/* ============================================================
   EVENT LISTENERS
   ============================================================ */
function attachEventListeners() {

  /* -- Translate button -- */
  dom.translateBtn.addEventListener('click', handleTranslate);

  /* -- Keyboard shortcut: Ctrl+Enter (or Cmd+Enter on Mac) -- */
  dom.sourceText.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleTranslate();
    }
  });

  /* -- Character counter (live update while typing) -- */
  dom.sourceText.addEventListener('input', () => {
    updateCharCount(dom.sourceText.value);
    // Reset result when user changes source text
    if (dom.sourceText.value === '') resetResult();
  });

  /* -- Clear button -- */
  dom.clearBtn.addEventListener('click', () => {
    dom.sourceText.value = '';
    updateCharCount('');
    resetResult();
    hideError();
    dom.sourceText.focus();
  });

  /* -- Swap languages button -- */
  dom.swapBtn.addEventListener('click', handleSwapLanguages);

  /* -- Copy button -- */
  dom.copyBtn.addEventListener('click', handleCopy);

  /* -- Speak source text -- */
  dom.speakSourceBtn.addEventListener('click', () => {
    speakText(dom.sourceText.value, dom.sourceLang.value);
  });

  /* -- Speak translated text -- */
  dom.speakResultBtn.addEventListener('click', () => {
    speakText(dom.resultText.textContent, dom.targetLang.value);
  });

  /* -- Theme toggle -- */
  dom.themeToggle.addEventListener('click', toggleTheme);
}


/* ============================================================
   CORE: TRANSLATE
   ============================================================ */
async function handleTranslate() {
  const text       = dom.sourceText.value.trim();
  const sourceLang = dom.sourceLang.value;
  const targetLang = dom.targetLang.value;

  /* --- Validation --- */
  if (!text) {
    showError('Please enter some text to translate.');
    dom.sourceText.focus();
    return;
  }

  if (sourceLang !== 'auto' && sourceLang === targetLang) {
    showError('Source and target languages are the same. Please choose different languages.');
    return;
  }

  /* --- Start loading state --- */
  hideError();
  setLoading(true);
  resetResult();

  try {
    /* --- Call the API (api.js) --- */
    const translated = await translateText(text, sourceLang, targetLang);

    /* --- Display the result --- */
    displayResult(translated);

  } catch (error) {
    /* --- Friendly error messages --- */
    console.error('Translation error:', error);

    let userMessage = 'Something went wrong. Please try again.';

    if (error.message.includes('401') || error.message.includes('auth')) {
      userMessage = 'API authentication failed. Check your API key configuration.';
    } else if (error.message.includes('429')) {
      userMessage = 'Too many requests. Please wait a moment and try again.';
    } else if (error.message.includes('500') || error.message.includes('502')) {
      userMessage = 'The translation service is temporarily unavailable. Please try again shortly.';
    } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      userMessage = 'Network error. Please check your internet connection.';
    } else if (error.message.includes('API Error')) {
      userMessage = error.message; // show the actual API error message
    }

    showError(userMessage);
    resetResult();

  } finally {
    /* --- Always stop loading state --- */
    setLoading(false);
  }
}


/* ============================================================
   SWAP LANGUAGES
   ============================================================ */
function handleSwapLanguages() {
  const currentSource = dom.sourceLang.value;
  const currentTarget = dom.targetLang.value;

  // Don't swap if source is "Auto Detect"
  if (currentSource === 'auto') {
    dom.sourceLang.value = currentTarget;
    dom.targetLang.value = 'en'; // fall back to English
    return;
  }

  // Swap the dropdown values
  dom.sourceLang.value = currentTarget;
  dom.targetLang.value = currentSource;

  // Also swap the textarea content with the result (if there's a result)
  const resultContent = dom.resultText.querySelector('.result-placeholder')
    ? ''
    : dom.resultText.textContent;

  if (resultContent) {
    dom.sourceText.value = resultContent;
    updateCharCount(resultContent);
    resetResult();
  }
}


/* ============================================================
   COPY TO CLIPBOARD
   ============================================================ */
async function handleCopy() {
  const textToCopy = dom.resultText.textContent;

  if (!textToCopy || dom.resultText.querySelector('.result-placeholder')) return;

  try {
    await navigator.clipboard.writeText(textToCopy);
    showToast('✓ Copied to clipboard!');
  } catch (err) {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = textToCopy;
    textarea.style.position = 'fixed';
    textarea.style.opacity  = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('✓ Copied!');
  }
}


/* ============================================================
   TEXT-TO-SPEECH
   ============================================================ */
/**
 * Speaks text using the Web Speech API.
 * @param {string} text  - Text to read aloud.
 * @param {string} langCode - Language code (BCP-47).
 */
function speakText(text, langCode) {
  if (!text || text.includes('Translation will appear here')) return;

  // Cancel any speech that's currently playing
  window.speechSynthesis.cancel();

  // Find the speech code for this language
  const langData   = LANGUAGES.find(l => l.code === langCode);
  const speechCode = langData?.speechCode || langCode;

  const utterance  = new SpeechSynthesisUtterance(text);
  utterance.lang   = speechCode || 'en-US';
  utterance.rate   = 0.95;  // slightly slower for clarity
  utterance.pitch  = 1.0;

  // Optional: pick the best available voice for the language
  const voices     = window.speechSynthesis.getVoices();
  const matchVoice = voices.find(v => v.lang.startsWith(speechCode?.split('-')[0] || langCode));
  if (matchVoice) utterance.voice = matchVoice;

  window.speechSynthesis.speak(utterance);
}

// Voices load asynchronously — trigger load early
if ('speechSynthesis' in window) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
}
