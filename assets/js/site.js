(() => {
  const menu = document.getElementById('mobile-menu');
  const toggle = document.querySelector('.menu-toggle');
  const close = () => menu.close();
  toggle?.addEventListener('click', () => {
    menu.showModal();
    document.body.classList.add('menu-open');
    toggle.setAttribute('aria-expanded', 'true');
  });
  menu?.querySelector('.menu-close')?.addEventListener('click', close);
  menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  menu?.addEventListener('click', e => { if (e.target === menu && e.clientY > menu.getBoundingClientRect().bottom) close(); });
  menu?.addEventListener('keydown', e => {
    if (e.key !== 'Tab') return;
    const items = [...menu.querySelectorAll('a[href], button:not([disabled])')];
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  menu?.addEventListener('close', () => {
    document.body.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.focus();
  });
  matchMedia('(min-width: 901px)').addEventListener('change', e => { if (e.matches && menu.open) close(); });
  const languages = document.querySelector('.language-menu');
  document.addEventListener('click', e => { if (!languages?.contains(e.target)) languages?.removeAttribute('open'); });
  languages?.addEventListener('keydown', e => { if (e.key === 'Escape') { languages.removeAttribute('open'); languages.querySelector('summary').focus(); } });

  const news = document.querySelector('.news-directory');
  const emptyNews = news?.querySelector('.news-filter-empty');
  if (emptyNews) {
    const categories = new Set([...news.querySelectorAll('.news-filters a')].map(link => link.hash.slice(1)));
    const filterNews = () => {
      let fragment = location.hash.slice(1);
      try { fragment = decodeURIComponent(fragment); } catch { /* Invalid fragments use All. */ }
      const category = categories.has(fragment) ? fragment : 'all-news';
      let visibleCount = 0;
      news.querySelectorAll('.news-row').forEach(row => {
        const matches = category === 'all-news' || row.dataset.category === category;
        row.hidden = !matches;
        if (matches) visibleCount += 1;
      });
      emptyNews.hidden = visibleCount > 0;
      // Native hidden now owns visibility; :target remains the no-JS fallback.
      news.dataset.newsFilterReady = '';
    };
    filterNews();
    window.addEventListener('hashchange', filterNews);
  }
})();
