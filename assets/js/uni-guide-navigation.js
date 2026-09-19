// Keep links available without JavaScript; enhance only the separate buttons.
document.querySelectorAll('[data-guide-toggle]').forEach((button) => {
  const panel = document.getElementById(button.getAttribute('aria-controls'));
  if (!panel) return;
  const setExpanded = (expanded) => {
    panel.hidden = !expanded;
    button.setAttribute('aria-expanded', String(expanded));
    button.setAttribute('aria-label', `${button.dataset.categoryTitle}の項目を${expanded ? '収納' : '展開'}`);
  };
  setExpanded(false);
  button.hidden = false;
  button.addEventListener('click', () => {
    setExpanded(button.getAttribute('aria-expanded') !== 'true');
  });
});

const searchInput = document.querySelector('[data-guide-search-input]');
const searchResults = document.querySelector('[data-guide-search-results]');
const searchStatus = document.querySelector('[data-guide-search-status]');
const searchIndex = document.getElementById('uni-guide-search-index');

if (searchInput && searchResults && searchStatus && searchIndex) {
  const items = JSON.parse(searchIndex.textContent);
  const normalize = (value) => value.toLocaleLowerCase('ja-JP').replace(/[\s　]+/g, '');
  const render = () => {
    const query = normalize(searchInput.value);
    searchResults.replaceChildren();
    if (!query) {
      searchResults.hidden = true;
      searchStatus.textContent = '';
      return;
    }
    const matches = items.filter((item) => normalize(`${item.title}${item.category}${item.description}`).includes(query)).slice(0, 12);
    searchStatus.textContent = matches.length ? `${matches.length}件の使い方が見つかりました。` : '該当する使い方が見つかりませんでした。別の言葉で検索してください。';
    matches.forEach((item) => {
      const link = document.createElement('a');
      link.href = item.url;
      link.textContent = item.title;
      const category = document.createElement('span');
      category.textContent = item.category;
      const entry = document.createElement('li');
      entry.append(link, category);
      searchResults.append(entry);
    });
    searchResults.hidden = matches.length === 0;
  };
  searchInput.addEventListener('input', render);
}
