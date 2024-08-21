// JavaScript dictionary of languages
const LANGUAGES = {
  'en': 'English',
  'ja': 'Japanese',
  'ko': 'Korean',
  'ar': 'Arabic',
  'id': 'Bahasa Indonesia',
  'bn': 'Bengali',
  'bg': 'Bulgarian',
  'zh-hans': 'Chinese (Simplified)',
  'zh-hant': 'Chinese (Traditional)',
  'hr': 'Croatian',
  'cs': 'Czech',
  'da': 'Danish',
  'nl': 'Dutch',
  'et': 'Estonian',
  'fa': 'Farsi',
  'fi': 'Finnish',
  'fr': 'French',
  'de': 'German',
  'gu': 'Gujarati',
  'el': 'Greek',
  'hi': 'Hindi',
  'hu': 'Hungarian',
  'it': 'Italian',
  'kn': 'Kannada',
  'lv': 'Latvian',
  'lt': 'Lithuanian',
  'ml': 'Malayalam',
  'mr': 'Marathi',
  'no': 'Norwegian',
  'pl': 'Polish',
  'pt': 'Portuguese',
  'ro': 'Romanian',
  'ru': 'Russian',
  'sr': 'Serbian',
  'sk': 'Slovak',
  'sl': 'Slovenian',
  'es': 'Spanish',
  'sw': 'Swahili',
  'ta': 'Tamil',
  'te': 'Telugu',
  'th': 'Thai',
  'tr': 'Turkish',
  'uk': 'Ukrainian',
  'ur': 'Urdu',
  'vi': 'Vietnamese'
};

// Populate the select element with language options
const select = document.getElementById('language');
for (const [code, name] of Object.entries(LANGUAGES)) {
  const option = document.createElement('option');
  option.value = code;
  option.textContent = name;
  select.appendChild(option);
}

// Function to change the page language
// function changeLanguage() {
//   const selectedLang = select.value;
//   if (google.translate) {
//     const frame = document.querySelector('iframe.goog-te-frame');
//     if (frame) {
//       const doc = frame.contentDocument || frame.contentWindow.document;
//       doc.documentElement.lang = selectedLang;
//       google.translate.TranslateElement.getInstance().setEnabledLanguage(selectedLang);
//     }
//   } else {
//     document.documentElement.lang = selectedLang;
//     window.location.reload();
//   }
// }

// Google Translate initialization
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'ar',
    includedLanguages: 'ar,bn,bg,zh-CN,zh-TW,hr,cs,da,nl,et,fa,fi,fr,de,gu,el,hi,hu,it,ja,ko,kn,lv,lt,ml,mr,no,pl,pt,ro,ru,sr,sk,sl,es,sw,su,ta,te,th,tr,uk,ur,vi',
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
    autoDisplay: false
  }, 'google_translate_element');
}

const root = document.getElementById("root");
function googleTranslateElementInit() {
  function translateThediv() {
    const content = root.innerHTML;
    const output = new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'ar,bn,bg,zh-CN,zh-TW,hr,cs,da,nl,et,fa,fi,fr,de,gu,el,hi,hu,it,ja,ko,kn,lv,lt,ml,mr,no,pl,pt,ro,ru,sr,sk,sl,es,sw,su,ta,te,th,tr,uk,ur,vi',
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
      autoDisplay: false
    }, 'google_translate_element');
    output.lang = "ko";
    const translatedContent = output.translate(content);
    console.log(translatedContent, content)
    root.innerHTML = translatedContent;
  }
  translateThediv();
}

// Load Google Translate script
// (function () {
//   const script = document.createElement('script');
//   script.type = 'text/javascript';
//   script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
//   document.body.appendChild(script);
// })();
