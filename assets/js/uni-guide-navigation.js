// Keep links available without JavaScript; enhance only the separate buttons.
document.querySelectorAll('[data-guide-toggle]').forEach((button) => {
  if (button.dataset.guideEnhanced === 'true') return;
  button.dataset.guideEnhanced = 'true';
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

if (searchInput && searchResults && searchStatus && searchIndex && searchInput.dataset.guideSearchEnhanced !== 'true') {
  searchInput.dataset.guideSearchEnhanced = 'true';
  const searchRoot = searchInput.closest('[data-guide-search-mode]');
  let items = JSON.parse(searchIndex.textContent);
  if (searchRoot?.dataset.guideSearchMode === 'local') {
    const content = searchRoot.closest('[data-content-body]');
    const headings = content ? [...content.querySelectorAll('h2[id], h3[id]')].filter((heading) => !searchRoot.contains(heading)) : [];
    let category = '';
    items = headings.map((heading) => {
      if (heading.tagName === 'H2') category = heading.textContent.trim();
      const description = [];
      let sibling = heading.nextElementSibling;
      while (sibling && !/^H[23]$/.test(sibling.tagName)) {
        description.push(sibling.textContent.trim());
        sibling = sibling.nextElementSibling;
      }
      return {
        title: heading.textContent.trim(),
        category,
        description: description.join(' '),
        url: `#${heading.id}`,
      };
    });
  }
  const normalize = (value) => String(value || '').toLocaleLowerCase(document.documentElement.lang || undefined).normalize('NFKC').replace(/[\s　]+/g, '');
  let composing = false;
  const render = () => {
    const query = normalize(searchInput.value);
    searchResults.replaceChildren();
    if (!query) {
      searchResults.hidden = true;
      searchStatus.textContent = '';
      return;
    }
    const matches = items.filter((item) => normalize(`${item.title}${item.category}${item.description}`).includes(query)).slice(0, 12);
    searchStatus.textContent = matches.length
      ? searchRoot.dataset.resultMessage.replace('{count}', String(matches.length))
      : searchRoot.dataset.noResultsMessage;
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
  searchInput.addEventListener('compositionstart', () => { composing = true; });
  searchInput.addEventListener('compositionend', () => { composing = false; render(); });
  searchInput.addEventListener('input', () => { if (!composing) render(); });
  searchInput.addEventListener('search', render);
}
