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

const languSelector = () => {
  // Populate the select element with language options
  console.log("hi")
  const select = document.getElementById('language');
  document.getElementsByClassName("VIpgJd-ZVi9od-xl07Ob-lTBxed")[0].click();
  document.getElementsByClassName("VIpgJd-ZVi9od-vH1Gmf-ibnC6b-gk6SMd")[0].click();
  for (tags of document.getElementsByClassName("VIpgJd-ZVi9od-vH1Gmf-ibnC6b")) {
    console.log(tags);
    const option = document.createElement('option');
    option.value = tags.value;
    option.textContent = LANGUAGES[tags.value];
    option.onclick = () => tags.click()
    select.appendChild(option);
  }
}
// Google Translate initialization
function googleTranslateElementInit() {
  new google.translate.TranslateElement({
    pageLanguage: 'en',
    includedLanguages: 'ar,bn,bg,zh-CN,zh-TW,hr,cs,da,nl,et,fa,fi,fr,de,gu,el,hi,hu,it,ja,ko,kn,lv,lt,ml,mr,no,pl,pt,ro,ru,sr,sk,sl,es,sw,su,ta,te,th,tr,uk,ur,vi',
    layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
  }, 'google_translate_element');
  // let isLoaded = document.getElementById(":2.container") != null;
  // const intervalId = setInterval(() => {
  //   isLoaded = document.getElementById(":2.container") != null;
  //   console.log("hello")
  //   if (isLoaded) {
  //     document.getElementById(":2.container").parentElement.innerHTML = "";
  //     document.body.style = "";
  //     languSelector();
  //     clearInterval(intervalId);
  //   }
  // }, 100);

  setTimeout(() => {
    document.getElementById(":2.container").parentElement.innerHTML = "";
    document.body.style = "";
    // languSelector();
  }, 1000);

}
