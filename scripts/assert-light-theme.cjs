// Site brand contract: the OS preference is test input, never the site theme.
const assert = require('node:assert/strict');

async function assertLightTheme(page) {
  const state = await page.evaluate(() => ({
    colorScheme: getComputedStyle(document.documentElement).colorScheme,
    metaColorScheme: document.querySelector('meta[name="color-scheme"]')?.content,
    themeColors: [...document.querySelectorAll('meta[name="theme-color"]')].map(node => ({ content: node.content, media: node.media })),
    background: getComputedStyle(document.body).backgroundColor,
    color: getComputedStyle(document.body).color,
    darkClass: document.documentElement.classList.contains('dark'),
    dataTheme: document.documentElement.getAttribute('data-theme'),
    themeControls: document.querySelectorAll('#theme-toggle, .theme-toggle, [data-theme-switcher]').length,
  }));
  assert.ok(['light', 'only light', 'light only'].includes(state.colorScheme), 'Site stays light regardless of OS preference or JavaScript');
  assert.equal(state.metaColorScheme, 'light', 'Initial HTML advertises only the light theme');
  assert.deepEqual(state.themeColors, [{ content: '#ffffff', media: '' }], 'Browser chrome uses the fixed light brand color');
  assert.equal(state.background, 'rgb(255, 255, 255)', 'The existing white page surface is retained');
  assert.equal(state.color, 'rgb(23, 25, 29)', 'The existing light body text color is retained');
  assert.equal(state.darkClass, false, 'The removed dark class is never applied');
  assert.equal(state.dataTheme, null, 'There is no automatic or persisted theme selector');
  assert.equal(state.themeControls, 0, 'Theme switching UI is removed, not hidden');
  return state;
}

// Seed only the retired website preference. This is QA setup, not site code.
async function seedLegacyDarkPreference(context) {
  await context.addInitScript(() => {
    try { localStorage.setItem('pref-theme', 'dark'); } catch (_) {}
  });
}

module.exports = { assertLightTheme, seedLegacyDarkPreference };
