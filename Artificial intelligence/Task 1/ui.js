/**
 * ui.js
 * -----
 * UI module: handles all DOM references and visual state changes.
 * Keeps DOM manipulation separate from API logic (separation of concerns).
 *
 * Exported-style functions are just globals here (no bundler needed).
 */

/* ---- Grab all the DOM elements we'll need ---- */
const dom = {
  sourceLang:     document.getElementById('sourceLang'),
  targetLang:     document.getElementById('targetLang'),
  swapBtn:        document.getElementById('swapBtn'),
  sourceText:     document.getElementById('sourceText'),
  charCount:      document.getElementById('charCount'),
  clearBtn:       document.getElementById('clearBtn'),
  speakSourceBtn: document.getElementById('speakSourceBtn'),
  resultText:     document.getElementById('resultText'),
  copyBtn:        document.getElementById('copyBtn'),
  speakResultBtn: document.getElementById('speakResultBtn'),
  loadingSkeleton:document.getElementById('loadingSkeleton'),
  translateBtn:   document.getElementById('translateBtn'),
  errorBox:       document.getElementById('errorBox'),
  themeToggle:    document.getElementById('themeToggle'),
  themeIcon:      document.getElementById('themeIcon'),
};

/* ---- Populate language <select> dropdowns ---- */
function populateLanguageDropdowns() {
  LANGUAGES.forEach((lang) => {
    // Source dropdown — include "Auto Detect"
    const optionSrc = document.createElement('option');
    optionSrc.value = lang.code;
    optionSrc.textContent = lang.name;
    dom.sourceLang.appendChild(optionSrc);

    // Target dropdown — skip "Auto Detect"
    if (lang.code !== 'auto') {
      const optionTgt = document.createElement('option');
      optionTgt.value = lang.code;
      optionTgt.textContent = lang.name;
      dom.targetLang.appendChild(optionTgt);
    }
  });

  // Set sensible defaults
  dom.sourceLang.value = 'auto';
  dom.targetLang.value = 'ur'; // default target: Urdu (relevant for Pakistani users)
}

/* ---- Show loading state ---- */
function setLoading(isLoading) {
  if (isLoading) {
    // Hide result, show skeleton, disable button
    dom.resultText.style.display = 'none';
    dom.loadingSkeleton.classList.add('active');
    dom.translateBtn.disabled = true;
    dom.translateBtn.classList.add('loading');
    dom.translateBtn.querySelector('.translate-btn__text').textContent = 'Translating';
  } else {
    // Hide skeleton, show result
    dom.loadingSkeleton.classList.remove('active');
    dom.resultText.style.display = '';
    dom.translateBtn.disabled = false;
    dom.translateBtn.classList.remove('loading');
    dom.translateBtn.querySelector('.translate-btn__text').textContent = 'Translate';
  }
}

/* ---- Display the translated text ---- */
function displayResult(text) {
  dom.resultText.innerHTML = '';           // clear previous content
  dom.resultText.textContent = text;       // set new text safely (no XSS)
  dom.copyBtn.disabled = false;
  dom.speakResultBtn.disabled = false;
}

/* ---- Show an error message ---- */
function showError(message) {
  dom.errorBox.textContent = message;
  dom.errorBox.style.display = 'block';
  // Auto-hide after 6 seconds
  setTimeout(() => { dom.errorBox.style.display = 'none'; }, 6000);
}

/* ---- Hide the error box ---- */
function hideError() {
  dom.errorBox.style.display = 'none';
}

/* ---- Reset result panel to placeholder state ---- */
function resetResult() {
  dom.resultText.innerHTML = '<span class="result-placeholder">Translation will appear here…</span>';
  dom.copyBtn.disabled = true;
  dom.speakResultBtn.disabled = true;
}

/* ---- Update character counter ---- */
function updateCharCount(text) {
  const len  = text.length;
  const max  = 1000;
  dom.charCount.textContent = `${len} / ${max}`;

  dom.charCount.classList.remove('near-limit', 'at-limit');
  if      (len >= max)       dom.charCount.classList.add('at-limit');
  else if (len >= max * 0.8) dom.charCount.classList.add('near-limit');
}

/* ---- Show a temporary toast notification ---- */
function showToast(message) {
  // Create toast element if it doesn't exist
  let toast = document.getElementById('copyToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'copyToast';
    toast.className = 'copy-success';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2000);
}

/* ---- Theme toggle ---- */
function initTheme() {
  // Check for a saved preference, otherwise use system default
  const saved = localStorage.getItem('linguaflow-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = saved ? saved === 'dark' : prefersDark;

  applyTheme(isDark);
}

function applyTheme(isDark) {
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  dom.themeIcon.textContent = isDark ? '☀︎' : '☾';
  localStorage.setItem('linguaflow-theme', isDark ? 'dark' : 'light');
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  applyTheme(current !== 'dark');
}
