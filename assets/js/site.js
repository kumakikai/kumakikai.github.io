(() => {
  const root = document.documentElement;
  const media = matchMedia('(prefers-color-scheme: dark)');
  const syncTheme = () => root.classList.toggle('dark', root.dataset.theme === 'dark' || (root.dataset.theme === 'auto' && media.matches));
  document.getElementById('theme-toggle')?.addEventListener('click', () => {
    root.dataset.theme = root.classList.contains('dark') ? 'light' : 'dark';
    try { localStorage.setItem('pref-theme', root.dataset.theme); } catch (_) {}
    syncTheme();
  });
  media.addEventListener('change', syncTheme);
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
})();
