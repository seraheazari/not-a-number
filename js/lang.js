let lang = 'fa';
const search = new URL(document.URL).search;
if (search.includes('lang=en')) {
  lang = 'en';
}

const languages = ['fa', 'en'];

languages.forEach(function(l) {
  const elements = document.querySelectorAll(`.${l}`);
  if (l == lang) {
    elements.forEach(function(el) {
      el.classList.remove('hidden');
    });
  } else {
    elements.forEach(function(el) {
      el.classList.add('hidden');
    });
  }
});
