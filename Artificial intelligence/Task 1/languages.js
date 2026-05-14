/**
 * languages.js
 * ------------
 * A list of popular languages with their BCP-47 codes.
 * These codes are used by:
 *  - The Claude API prompt (for translation accuracy)
 *  - The Web Speech API (text-to-speech)
 *
 * To add more languages, simply extend the LANGUAGES array below.
 */

const LANGUAGES = [
  { code: "auto",  name: "Auto Detect",     speechCode: null },
  { code: "en",    name: "English",          speechCode: "en-US" },
  { code: "ur",    name: "Urdu",             speechCode: "ur-PK" },
  { code: "ar",    name: "Arabic",           speechCode: "ar-SA" },
  { code: "zh",    name: "Chinese (Simplified)", speechCode: "zh-CN" },
  { code: "zh-TW", name: "Chinese (Traditional)", speechCode: "zh-TW" },
  { code: "fr",    name: "French",           speechCode: "fr-FR" },
  { code: "de",    name: "German",           speechCode: "de-DE" },
  { code: "hi",    name: "Hindi",            speechCode: "hi-IN" },
  { code: "id",    name: "Indonesian",       speechCode: "id-ID" },
  { code: "it",    name: "Italian",          speechCode: "it-IT" },
  { code: "ja",    name: "Japanese",         speechCode: "ja-JP" },
  { code: "ko",    name: "Korean",           speechCode: "ko-KR" },
  { code: "ms",    name: "Malay",            speechCode: "ms-MY" },
  { code: "nl",    name: "Dutch",            speechCode: "nl-NL" },
  { code: "pl",    name: "Polish",           speechCode: "pl-PL" },
  { code: "pt",    name: "Portuguese",       speechCode: "pt-BR" },
  { code: "ru",    name: "Russian",          speechCode: "ru-RU" },
  { code: "es",    name: "Spanish",          speechCode: "es-ES" },
  { code: "sv",    name: "Swedish",          speechCode: "sv-SE" },
  { code: "tr",    name: "Turkish",          speechCode: "tr-TR" },
  { code: "vi",    name: "Vietnamese",       speechCode: "vi-VN" },
  { code: "th",    name: "Thai",             speechCode: "th-TH" },
  { code: "fa",    name: "Persian (Farsi)",  speechCode: "fa-IR" },
  { code: "bn",    name: "Bengali",          speechCode: "bn-BD" },
  { code: "sw",    name: "Swahili",          speechCode: "sw-KE" },
  { code: "ro",    name: "Romanian",         speechCode: "ro-RO" },
  { code: "uk",    name: "Ukrainian",        speechCode: "uk-UA" },
  { code: "cs",    name: "Czech",            speechCode: "cs-CZ" },
  { code: "el",    name: "Greek",            speechCode: "el-GR" },
];
