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
