function googleTranslateElementInit() {
  new google.translate.TranslateElement({
      pageLanguage: 'hi',
      includedLanguages: 'ar,bn,bg,zh-CN,zh-TW,hr,cs,da,nl,et,fa,fi,fr,de,gu,el,hi,hu,it,ja,ko,kn,lv,lt,ml,mr,no,pl,pt,ro,ru,sr,sk,sl,es,sw,su,ta,te,th,tr,uk,ur,vi',
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE
  }, 'google_translate_element');
}

// Populate the select element with language options
const LANGUAGES = {
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
  'hi': 'हिन्दी',
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

// Function to change the page language
function changeLanguage() {
  const selectedLang = select.value;
  const translateElement = new google.translate.TranslateElement();
  translateElement.setEnabledLanguages([selectedLang]);
  translateElement.translate();
}

select.addEventListener('change', changeLanguage);