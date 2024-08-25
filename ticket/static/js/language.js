// Populate the select element with language options
const LANGUAGES = {
  'en': 'english',
  'ar': 'العربية',
  'bn': 'বাংলা',
  'bg': 'български',
  'zh-CN': '中文 (简体)',
  'zh-TW': '中文 (繁體)',
  'hr': 'hrvatski',
  'cs': 'čeština',
  'da': 'dansk',
  'nl': 'Nederlands',
  'et': 'eesti',
  'fa': 'فارسی',
  'fi': 'suomi',
  'fr': 'français',
  'de': 'Deutsch',
  'gu': 'ગુજરાતી',
  'el': 'ελληνικά',
  'hi-IN': 'हिन्दी',
  'hu': 'magyar',
  'it': 'italiano',
  'ja': '日本語',
  'kn': 'ಕನ್ನಡ',
  'ko': '한국어',
  'lv': 'latviešu',
  'lt': 'lietuvių',
  'ml': 'മലയാളം',
  'mr': 'मराठी',
  'no': 'norsk',
  'pl': 'polski',
  'pt': 'português',
  'ro': 'română',
  'ru': 'русский',
  'sr': 'српски',
  'sk': 'slovenčina',
  'sl': 'slovenščina',
  'es': 'español',
  'sw': 'Kiswahili',
  'ta': 'தமிழ்',
  'te': 'తెలుగు',
  'th': 'ไทย',
  'tr': 'Türkçe',
  'uk': 'українська',
  'ur': 'اردو',
  'vi': 'Tiếng Việt'
};

const select = document.getElementById('language');
for (const [code, name] of Object.entries(LANGUAGES)) {
  const option = document.createElement('option');
  option.value = code;
  option.textContent = name;
  select.appendChild(option);
}

// Function to change the language of specific elements
function changeLanguage() {
  const selectedLang = select.value;
  const translatableElements = document.querySelectorAll('.translatable');

  translatableElements.forEach(element => {
    const originalText = element.dataset.originalText || element.textContent;
    element.dataset.originalText = originalText; // Store original text for future reference
    // Here you would typically call a translation API, but for demonstration, we'll just simulate it
    fetchTranslation(originalText, selectedLang).then(translatedText => {
      element.textContent = translatedText;
    });
  });
}

select.addEventListener('change', changeLanguage);

// for text to speech
function speak(event) {
  const text = event.parentElement.children[2].innerText;
  console.log(text);
  const sy = window.speechSynthesis;
  const speakThis = new SpeechSynthesisUtterance(text);
  speakThis.lang = select.value;
  speakThis.voice = speechSynthesis.getVoices()[0];
  console.log(speakThis)
  sy.speak(speakThis);
}
