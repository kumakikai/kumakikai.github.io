// Run immediately after the server-rendered selection groups, before first paint.
// HTML remains the complete fallback when JavaScript is unavailable.
(() => {
  for (const group of document.querySelectorAll('[data-product-selection]:not([data-selection-ready])')) {
    const template = group.querySelector('template[data-product-candidates]');
    if (!template) continue;
    const options = [
      ...Array.from(group.children).filter(node => node.hasAttribute('data-product-option')),
      ...Array.from(template.content.children)
    ];
    const count = Number(group.dataset.productSelection);
    if (!Number.isInteger(count) || count < 1 || options.length < count) continue;
    // Fisher–Yates: choose without replacement; no timer, storage or network.
    for (let i = options.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [options[i], options[j]] = [options[j], options[i]];
    }
    group.replaceChildren(...options.slice(0, count));
    group.dataset.selectionReady = 'true';
  }
})();
