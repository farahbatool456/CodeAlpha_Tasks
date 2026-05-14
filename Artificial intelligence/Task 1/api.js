/**
 * api.js
 * ------
 * API module: sends text to Claude (Anthropic) for translation.
 *
 * Why Claude instead of Google/Microsoft Translate?
 *  - No separate API key setup for the demo (uses the built-in
 *    Anthropic API available in this environment).
 *  - Claude handles context, idioms, and nuance better than
 *    phrase-by-phrase statistical translation.
 *  - One API covers all languages without per-language pricing tiers.
 *
 * NOTE: In a real deployed project, you would:
 *  1. Store your API key on a backend server (Node.js / Python).
 *  2. Call YOUR backend from the frontend.
 *  3. Never expose API keys in client-side JavaScript.
 */

/**
 * translateText
 * @param {string} text        - The text to translate.
 * @param {string} sourceLang  - BCP-47 language code or "auto".
 * @param {string} targetLang  - BCP-47 language code.
 * @returns {Promise<string>}  - The translated text.
 */
async function translateText(text, sourceLang, targetLang) {

  // --- Build a clear, structured prompt for Claude ---
  const sourceLabel = sourceLang === 'auto'
    ? 'the source language (detect it automatically)'
    : `${getLanguageName(sourceLang)}`;

  const targetLabel = getLanguageName(targetLang);

  const prompt = `You are a professional translator. 
Translate the following text from ${sourceLabel} to ${targetLabel}.

Rules:
- Output ONLY the translated text. No explanations, no preamble, no notes.
- Preserve the original formatting (line breaks, punctuation, capitalisation style).
- If the input is already in ${targetLabel}, return it unchanged.

Text to translate:
"""
${text}
"""`;

  // --- Make the fetch call to Anthropic's API ---
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // API key is injected automatically in this sandboxed environment.
      // In your own project, replace with: 'x-api-key': 'YOUR_API_KEY'
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514', // Use Sonnet 4 — fast + capable
      max_tokens: 1000,
      messages: [
        { role: 'user', content: prompt }
      ]
    })
  });

  // --- Handle HTTP-level errors ---
  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    const errMsg  = errData?.error?.message || `HTTP ${response.status}: ${response.statusText}`;
    throw new Error(`API Error: ${errMsg}`);
  }

  const data = await response.json();

  // --- Extract the translation from the response ---
  const translatedText = data?.content?.[0]?.text;

  if (!translatedText) {
    throw new Error('Unexpected API response: no content returned.');
  }

  return translatedText.trim();
}

/**
 * Helper: get human-readable language name from code.
 * Falls back to the code itself if not found.
 */
function getLanguageName(code) {
  const found = LANGUAGES.find(l => l.code === code);
  return found ? found.name : code;
}
