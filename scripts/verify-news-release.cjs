#!/usr/bin/env node
// Release regression: only a selected empty News category exposes its notice.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium, webkit } = require('playwright');
const engine = process.env.TEST_ENGINE || 'chrome';
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const tag = process.env.TEST_TAG || 'local';
const requireHidden = process.env.EXPECT_NATIVE_HIDDEN !== '0';
const output = 'docs/release-audit';
const locales = ['ja', 'en', 'de', 'fr', 'ko', 'zh-hant'];
const categories = ['all-news', 'press-release', 'blog', 'information'];
const results = [];
fs.mkdirSync(`${output}/screenshots`, { recursive: true });

function save(fatal = null) {
  fs.writeFileSync(`${output}/news-${tag}-${engine}.json`, JSON.stringify({
    checkedAt: new Date().toISOString(), base, engine, requireNativeHidden: requireHidden,
    ok: !fatal && results.length === 24 && results.every(result => result.ok),
    cases: results.length, failures: results.filter(result => !result.ok),
    ...(fatal ? { fatal } : {}),
    method: 'Actual browser viewport rendering and accessibility snapshots. Six site languages, desktop/mobile, JavaScript on/off. Initial no-hash, each category, All reset and direct empty-category fragment. Native-hidden check also blocks CSS before page navigation. No physical-device test.',
    results,
  }, null, 2) + '\n');
}

(async () => {
  const browser = await (engine === 'webkit' ? webkit : chromium).launch({ headless: true,
    ...(engine === 'chrome' ? { executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' } : {}),
  });
  try {
    for (const locale of locales) for (const width of [1440, 390]) for (const javaScriptEnabled of [true, false]) {
      const result = { locale, width, javaScriptEnabled, states: [] };
      const context = await browser.newContext({ viewport: { width, height: 1000 }, javaScriptEnabled });
      const page = await context.newPage();
      const route = `${base}${locale === 'ja' ? '' : '/' + locale}/news/`;
      const emptyText = JSON.parse(fs.readFileSync(`data/company/${locale}.json`, 'utf8')).newsEmpty;
      const browserErrors = [];
      page.on('pageerror', error => browserErrors.push(String(error)));
      try {
        const response = await page.goto(route, { waitUntil: 'load' });
        assert.equal(response.status(), 200);
        const rawCategories = await page.locator('.news-row').evaluateAll(rows => rows.map(row => row.dataset.category));
        assert(rawCategories.length > 0, 'The all-news list contains articles');
        const counts = Object.fromEntries(categories.map(category => [category, category === 'all-news' ? rawCategories.length : rawCategories.filter(value => value === category).length]));
        async function checkState(category, label = category) {
          const expectedCount = counts[category];
          const visibleRows = await page.locator('.news-row:visible').count();
          const visibleEmpty = await page.locator('.news-filter-empty:visible').count();
          assert.equal(visibleRows, expectedCount, `${label}: matching articles`);
          assert.equal(visibleEmpty, category !== 'all-news' && expectedCount === 0 ? 1 : 0, `${label}: only an empty selected category shows its notice`);
          const aria = await page.locator('main').ariaSnapshot();
          assert.equal(aria.includes(emptyText), visibleEmpty === 1, `${label}: accessibility visibility matches visual state`);
          assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${label}: no horizontal overflow`);
          result.states.push({ category: label, visibleRows, visibleEmpty, accessibilityMatches: true });
        }
        await checkState('all-news', 'initial-no-fragment');
        if (requireHidden) assert(await page.locator('.news-filter-empty').evaluateAll(nodes => nodes.every(node => node.hasAttribute('hidden'))), 'Empty notices are natively hidden before CSS');
        if (locale === 'ja' && javaScriptEnabled) await page.screenshot({ path: `${output}/screenshots/news-${tag}-${engine}-${width}-all.jpg`, type: 'jpeg', quality: 85 });
        for (const category of categories.slice(1)) {
          await page.locator(`.news-filters #${category}`).click();
          await checkState(category);
        }
        if (locale === 'ja' && javaScriptEnabled) await page.screenshot({ path: `${output}/screenshots/news-${tag}-${engine}-${width}-information.jpg`, type: 'jpeg', quality: 85 });
        await page.locator('.news-filters #all-news').click();
        await checkState('all-news', 'all-reset');
        await page.goto('about:blank');
        await page.goto(route + '#information', { waitUntil: 'load' });
        await checkState('information', 'direct-information-fragment');
        if (requireHidden) {
          await page.route('**/*', request => request.request().resourceType() === 'stylesheet' ? request.abort() : request.continue());
          await page.goto('about:blank');
          await page.goto(route, { waitUntil: 'load' });
          assert.equal(await page.locator('.news-filter-empty:visible').count(), 0, 'No false empty message before any stylesheet loads');
          assert(!(await page.locator('main').ariaSnapshot()).includes(emptyText), 'Native hidden also keeps an unstyled notice out of the accessibility tree');
          result.stylesheetsBlockedInitial = 'passed';
        }
        assert.deepEqual(browserErrors, []);
        result.ok = true;
      } catch (error) {
        result.ok = false;
        result.error = String(error.stack || error);
      }
      await context.close();
      results.push(result);
      save();
      console.log(`${tag}/${engine} ${locale} ${width} JS=${javaScriptEnabled}: ${result.ok ? 'PASS' : result.error}`);
    }
  } finally { await browser.close(); }
  save();
  if (results.some(result => !result.ok)) process.exitCode = 1;
})().catch(error => { save(String(error.stack || error)); console.error(error); process.exitCode = 1; });
