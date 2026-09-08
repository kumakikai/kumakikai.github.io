#!/usr/bin/env node
// News regression: every category, including All, uses its actual matching count.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium, webkit } = require('playwright');
const engine = process.env.TEST_ENGINE || 'chrome';
const base = (process.env.TEST_BASE_URL || 'http://127.0.0.1:1314').replace(/\/$/, '');
const tag = process.env.TEST_TAG || 'local';
const requireHidden = process.env.EXPECT_NATIVE_HIDDEN !== '0';
const output = process.env.TEST_OUTPUT_DIR || 'docs/release-audit';
const supportedLocales = ['ja', 'en', 'de', 'fr', 'ko', 'zh-hant'];
const locales = process.env.TEST_LOCALES ? process.env.TEST_LOCALES.split(',').map(value => value.trim()).filter(Boolean) : supportedLocales;
assert(locales.length > 0 && locales.every(locale => supportedLocales.includes(locale)), 'TEST_LOCALES contains supported comma-separated site locales');
const categories = ['all-news', 'press-release', 'blog', 'information'];
let scenarios = locales.map(locale => ({ locale, fixture: 'actual' }));
for (const fixture of ['all-empty', 'information-present']) scenarios.push({ locale: 'ja', fixture });
if (process.env.TEST_FIXTURES) {
  const fixtures = process.env.TEST_FIXTURES.split(',');
  assert(fixtures.every(fixture => ['actual', 'all-empty', 'information-present'].includes(fixture)), 'TEST_FIXTURES contains supported scenario names');
  scenarios = scenarios.filter(scenario => fixtures.includes(scenario.fixture));
}
const expectedCases = scenarios.length * 2 * 2;
const results = [];
fs.mkdirSync(path.join(output, 'screenshots'), { recursive: true });

function save(fatal = null) {
  fs.writeFileSync(path.join(output, `news-${tag}-${engine}.json`), JSON.stringify({
    checkedAt: new Date().toISOString(), base, engine, locales, requireNativeHidden: requireHidden,
    ok: !fatal && results.length === expectedCases && results.every(result => result.ok),
    cases: results.length, expectedCases, failures: results.filter(result => !result.ok),
    ...(fatal ? { fatal } : {}),
    method: 'Actual browser rendering and accessibility snapshots. Configured languages, desktop/mobile, JavaScript on/off. Initial state, every direct fragment, repeated transitions, same-category click, keyboard, Back and unknown-fragment fallback. Intercepted Japanese HTML fixtures cover zero total articles and populated Information without editing content. Stylesheet-blocked initial state and JS filtering also checked. No physical-device test.',
    results,
  }, null, 2) + '\n');
}

async function fixtureHTML(html, fixture, javaScriptEnabled) {
  const { parse, serialize } = await import('parse5');
  const document = parse(html);
  const nodes = [];
  function visit(node) { nodes.push(node); for (const child of node.childNodes || []) visit(child); }
  visit(document);
  const attr = (node, name) => node.attrs?.find(value => value.name === name)?.value;
  const hasClass = (node, name) => (attr(node, 'class') || '').split(/\s+/).includes(name);
  const setAttr = (node, name, value) => {
    const existing = node.attrs.find(attribute => attribute.name === name);
    if (existing) existing.value = value;
    else node.attrs.push({ name, value });
  };
  const rows = nodes.filter(node => hasClass(node, 'news-row'));
  const empty = nodes.filter(node => hasClass(node, 'news-filter-empty'));
  assert.equal(empty.length, 1, 'Fixture expects one shared News empty-state element');
  assert(rows.length > 0, 'Fixture starts with real editorial rows');
  if (fixture === 'all-empty') {
    for (const row of rows) row.parentNode.childNodes.splice(row.parentNode.childNodes.indexOf(row), 1);
  } else {
    assert.equal(fixture, 'information-present');
    setAttr(rows[0], 'data-category', 'information');
  }
  const remaining = fixture === 'all-empty' ? [] : rows;
  const emptyCategories = categories.filter(category => category === 'all-news' ? remaining.length === 0 : !remaining.some(row => attr(row, 'data-category') === category));
  // With JS, retain stale build metadata/hidden to prove runtime row counting.
  // Without JS, match the metadata Hugo would produce for the fixture collection.
  if (!javaScriptEnabled) {
    setAttr(empty[0], 'data-empty-categories', emptyCategories.join(' '));
    empty[0].attrs = empty[0].attrs.filter(attribute => attribute.name !== 'hidden');
    if (remaining.length > 0) setAttr(empty[0], 'hidden', '');
  }
  return serialize(document);
}

(async () => {
  const browser = await (engine === 'webkit' ? webkit : chromium).launch({ headless: true,
    ...(engine === 'chrome' ? { executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' } : {}),
  });
  try {
    for (const { locale, fixture } of scenarios) for (const width of [1440, 390]) for (const javaScriptEnabled of [true, false]) {
      const result = { locale, fixture, width, javaScriptEnabled, states: [] };
      const context = await browser.newContext({ viewport: { width, height: 1000 }, javaScriptEnabled });
      const page = await context.newPage();
      const route = `${base}${locale === 'ja' ? '' : '/' + locale}/news/`;
      const emptyText = JSON.parse(fs.readFileSync(`data/company/${locale}.json`, 'utf8')).newsEmpty;
      const browserErrors = [];
      const consoleErrors = [];
      let stylesheetsBlocked = false;
      page.on('pageerror', error => browserErrors.push(String(error)));
      page.on('console', message => {
        // Aborted stylesheets intentionally emit browser resource errors.
        if (message.type() === 'error' && !(stylesheetsBlocked && /Failed to load resource|net::ERR_FAILED/i.test(message.text()))) consoleErrors.push(message.text());
      });
      try {
        if (fixture !== 'actual') await page.route(route, async request => {
          const response = await request.fetch();
          assert.equal(response.status(), 200);
          await request.fulfill({ response, body: await fixtureHTML(await response.text(), fixture, javaScriptEnabled) });
        });
        const response = await page.goto(route, { waitUntil: 'load' });
        assert.equal(response.status(), 200);
        assert.deepEqual(await page.locator('.news-filters a').evaluateAll(links => links.map(link => link.getAttribute('href'))), categories.map(category => '#' + category), 'Existing category fragment URLs are preserved');
        assert.equal(await page.locator('.news-filter-empty').count(), 1, 'One shared empty state');
        const readRows = () => page.locator('.news-row').evaluateAll(rows => rows.map(row => ({ category: row.dataset.category, href: row.querySelector('h2 a').getAttribute('href'), title: row.querySelector('h2 a').textContent })));
        const originalRows = await readRows();
        const rawCategories = originalRows.map(row => row.category);
        const counts = Object.fromEntries(categories.map(category => [category, category === 'all-news' ? rawCategories.length : rawCategories.filter(value => value === category).length]));
        if (fixture === 'actual') assert(counts['all-news'] > 0, 'The current published collection contains articles');
        if (fixture === 'all-empty') assert.equal(counts['all-news'], 0);
        if (fixture === 'information-present') assert(counts.information > 0);
        result.counts = counts;
        async function checkState(category, label = category) {
          const expectedCount = counts[category];
          // Native navigation can return before its hashchange listener runs.
          await page.waitForFunction(({ expectedCount, category }) => {
            const visible = node => !!(node.offsetWidth || node.offsetHeight || node.getClientRects().length);
            const rows = [...document.querySelectorAll('.news-row')].filter(visible);
            return rows.length === expectedCount
              && (category === 'all-news' || rows.every(row => row.dataset.category === category))
              && [...document.querySelectorAll('.news-filter-empty')].filter(visible).length === (expectedCount === 0 ? 1 : 0);
          }, { expectedCount, category }, { timeout: 10000 });
          const visibleRows = await page.locator('.news-row:visible').count();
          const visibleEmpty = await page.locator('.news-filter-empty:visible').count();
          assert.equal(visibleRows, expectedCount, `${label}: matching articles`);
          assert.equal(visibleEmpty, expectedCount === 0 ? 1 : 0, `${label}: actual matching count controls empty state, including All`);
          if (category !== 'all-news') assert(await page.locator('.news-row:visible').evaluateAll((rows, selected) => rows.every(row => row.dataset.category === selected), category), `${label}: rows belong to selected category`);
          if (javaScriptEnabled || (category === 'all-news' && requireHidden)) assert.equal(await page.locator('.news-filter-empty').evaluate(node => node.hidden), expectedCount > 0, `${label}: native hidden matches the count`);
          const aria = await page.locator('main').ariaSnapshot();
          assert.equal(aria.includes(emptyText), visibleEmpty === 1, `${label}: accessibility matches visual state`);
          assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${label}: no horizontal overflow`);
          if (!stylesheetsBlocked) assert(await page.locator(`.news-filters #${category}`).evaluate(node => {
            const style = getComputedStyle(node);
            return style.borderBottomColor !== 'rgba(0, 0, 0, 0)' && Number(style.fontWeight) >= 600;
          }), `${label}: selected category styling is retained`);
          result.states.push({ category: label, visibleRows, visibleEmpty, accessibilityMatches: true });
        }
        async function clickCategory(category, label = category) {
          await page.locator(`.news-filters #${category}`).click();
          assert.equal(new URL(page.url()).hash, '#' + category);
          await checkState(category, label);
        }
        await checkState('all-news', 'initial-no-fragment');
        if (locale === 'ja' && fixture === 'actual' && javaScriptEnabled) await page.screenshot({ path: path.join(output, `screenshots/news-${tag}-${engine}-${width}-all.jpg`), type: 'jpeg', quality: 85 });
        for (const category of categories.slice(1)) await clickCategory(category);
        if (locale === 'ja' && fixture === 'actual' && javaScriptEnabled) await page.screenshot({ path: path.join(output, `screenshots/news-${tag}-${engine}-${width}-information.jpg`), type: 'jpeg', quality: 85 });
        await page.goBack();
        assert.equal(new URL(page.url()).hash, '#blog', 'Native Back restores the previous filter URL');
        await checkState('blog', 'back-to-blog');
        for (const category of ['all-news', 'information', 'press-release', 'information', 'blog', 'all-news', 'information', 'all-news']) await clickCategory(category, `repeat-${category}`);
        await clickCategory('all-news', 'same-category-click');
        await page.locator('.news-filters #blog').focus();
        await page.keyboard.press('Enter');
        await checkState('blog', 'keyboard-blog');
        assert.equal(new URL(page.url()).hash, '#blog');
        assert.deepEqual(await readRows(), originalRows, 'Filtering preserves article rows, titles and URLs');
        for (const [category, fragment] of [...categories.map(category => [category, category]), ['blog', 'b%6Cog'], ['all-news', 'unknown-category']]) {
          await page.goto('about:blank');
          await page.goto(route + '#' + fragment, { waitUntil: 'load' });
          await checkState(category, `direct-${fragment}-fragment`);
        }
        if (requireHidden) {
          stylesheetsBlocked = true;
          await page.route('**/*', request => request.request().resourceType() === 'stylesheet' ? request.abort() : request.fallback());
          await page.goto('about:blank');
          await page.goto(route, { waitUntil: 'load' });
          await checkState('all-news', 'stylesheets-blocked-initial');
          if (javaScriptEnabled) for (const category of ['information', 'press-release', 'blog', 'all-news']) await clickCategory(category, `stylesheets-blocked-${category}`);
          result.stylesheetsBlockedInitial = 'passed';
        }
        assert.deepEqual(browserErrors, [], 'No JavaScript execution errors');
        assert.deepEqual(consoleErrors, [], 'No unexpected browser console errors');
        result.browserErrors = browserErrors;
        result.consoleErrors = consoleErrors;
        result.ok = true;
      } catch (error) {
        result.ok = false;
        result.error = String(error.stack || error);
        result.browserErrors = browserErrors;
        result.consoleErrors = consoleErrors;
      }
      await context.close();
      results.push(result);
      save();
      console.log(`${tag}/${engine} ${locale} ${fixture} ${width} JS=${javaScriptEnabled}: ${result.ok ? 'PASS' : result.error}`);
    }
  } finally { await browser.close(); }
  save();
  if (results.some(result => !result.ok)) process.exitCode = 1;
})().catch(error => { save(String(error.stack || error)); console.error(error); process.exitCode = 1; });
