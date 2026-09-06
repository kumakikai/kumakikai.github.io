#!/usr/bin/env node
// Focused random product-selection QA. Supply existing Playwright and axe via NODE_PATH.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const phase = process.env.TEST_PHASE || 'all';
assert.ok(['all', 'coverage'].includes(phase), 'Supported TEST_PHASE');
const coverageInput = phase === 'coverage' ? path.resolve(process.env.TEST_COVERAGE_INPUT || 'artifacts/selection/browser-before-coverage-correction.json') : null;
const reportPath = path.resolve(process.env.TEST_REPORT || 'docs/selection/browser-verification.json');
const screenshotPath = path.resolve(process.env.TEST_SCREENSHOTS || 'docs/selection/screenshots');
const progressPath = path.resolve(`artifacts/selection/${phase === 'coverage' ? 'coverage' : 'browser'}-progress.json`);
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const apps = read('data/apps.json');
const appByID = Object.fromEntries(apps.map(app => [app.id, app]));
const candidates = apps.filter(app => app.id !== 'uni-note').map(app => app.id);
const locales = ['ja', 'en', 'ko', 'de', 'fr', 'zh-hant'];
const areas = {
  learning: ['uni-note', 'uni-note-pocket'],
  communication: ['oto-miru', 'nocca'],
  'utilities': ['giga-poke', 'balance-calendar', 'smokeless', 'signal'],
};
const selectionSource = fs.readFileSync(path.join(root, 'assets/js/select-products.js'), 'utf8');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const results = [], warnings = [], homeCoverage = new Set(), areaCoverage = {};
for (const area of Object.keys(areas)) areaCoverage[area] = new Set();
if (coverageInput) {
  // Reuse successful deterministic seed observations from the unchanged build.
  // Unseeded reloads and the multi-viewport suite are never used to fill coverage.
  for (const result of JSON.parse(fs.readFileSync(coverageInput, 'utf8')).results) {
    if (!result.ok || !/^seed-/.test(result.name)) continue;
    if (result.pageType === 'home') result.selected.forEach(id => homeCoverage.add(id));
    else for (const [area, id] of Object.entries(result.selected)) areaCoverage[area].add(id);
  }
}
const prefix = locale => locale === 'ja' ? '' : '/' + locale;
const route = (pageType, locale) => `${prefix(locale)}/${pageType === 'company' ? 'company/' : ''}`;
const norm = text => text.replace(/\s+/g, '');
for (const folder of [path.dirname(reportPath), screenshotPath, path.dirname(progressPath)]) fs.mkdirSync(folder, { recursive: true });

function writeReport(pending) {
  const summary = {
    checkedAt: new Date().toISOString(), base, phase, coverageInput, ok: !pending && results.every(result => result.ok), pending,
    cases: results.length, failures: results.filter(result => !result.ok).map(result => result.name), warnings,
    expectedHomeRandomCandidates: candidates, expectedHomeVisibleCoverage: apps.map(app => app.id), homeCandidateCoverage: [...homeCoverage].sort(),
    expectedAreaCandidates: areas, areaCandidateCoverage: Object.fromEntries(Object.entries(areaCoverage).map(([key, ids]) => [key, [...ids].sort()])),
    method: 'Browser navigation/reloads, deterministic seeded Math.random coverage, actual shipped selection script on minimal DOM, no-JS fallback, external-script blocking, axe, and layout-shift observation. No source/data/UI changes from this test.',
    limitations: ['Local Chrome lab verification; not real-device or production field data.', 'Unseeded reload variation is observational and never used as a probabilistic pass/fail condition.', 'PerformanceObserver CLS samples cover initial navigation and controlled full image loading; Fast 3G is Chrome CDP emulation, not a cellular-device measurement.'],
    results,
  };
  fs.writeFileSync(progressPath, JSON.stringify(summary, null, 2) + '\n');
  if (!pending) fs.writeFileSync(reportPath, JSON.stringify(summary, null, 2) + '\n');
}

async function record(name, task) {
  try { results.push({ name, ok: true, ...await task() }); console.log(`PASS ${name}`); }
  catch (error) { results.push({ name, ok: false, error: error.message }); console.log(`FAIL ${name}: ${error.message}`); }
  writeReport(true);
}

async function addInstrumentation(context, seed) {
  await context.addInitScript(({ seed }) => {
    if (Number.isInteger(seed)) {
      let state = seed >>> 0;
      Math.random = () => {
        state = (state + 0x6D2B79F5) >>> 0;
        let value = state;
        value = Math.imul(value ^ value >>> 15, value | 1);
        value ^= value + Math.imul(value ^ value >>> 7, value | 61);
        return ((value ^ value >>> 14) >>> 0) / 4294967296;
      };
    }
    window.__selectionQA = { shifts: [], paints: [] };
    new PerformanceObserver(list => {
      for (const entry of list.getEntries()) if (!entry.hadRecentInput) {
        window.__selectionQA.shifts.push({ value: entry.value, startTime: entry.startTime,
          sources: (entry.sources || []).map(source => source.node?.getAttribute?.('class') || source.node?.nodeName || 'unknown') });
      }
    }).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver(list => {
      for (const entry of list.getEntries()) window.__selectionQA.paints.push({ name: entry.name, startTime: entry.startTime,
        groups: [...document.querySelectorAll('[data-product-selection]')].map(group => ({ count: group.dataset.productSelection, ready: group.hasAttribute('data-selection-ready') })) });
    }).observe({ type: 'paint', buffered: true });
  }, { seed });
}

async function cls(page) {
  return page.evaluate(() => {
    const data = window.__selectionQA || { shifts: [], paints: [] };
    let maxWindow = 0, windowValue = 0, start = 0, previous = 0;
    for (const shift of data.shifts) {
      if (shift.startTime - previous > 1000 || shift.startTime - start > 5000) { windowValue = 0; start = shift.startTime; }
      windowValue += shift.value; previous = shift.startTime; maxWindow = Math.max(maxWindow, windowValue);
    }
    return { cls: maxWindow, totalShift: data.shifts.reduce((sum, entry) => sum + entry.value, 0), shifts: data.shifts, paints: data.paints };
  });
}

async function loadImages(page) {
  // Driver-side waits work with JavaScript disabled too. Native lazy loading is
  // observed at real scroll positions; absent template images are not requested.
  for (const img of await page.locator('img:visible').all()) {
    await img.evaluate(element => element.scrollIntoView({ block: 'center' }));
    await page.waitForTimeout(35);
  }
  let broken = [];
  for (let attempt = 0; attempt < 25; attempt++) {
    broken = await page.evaluate(() => [...document.images].filter(image => image.checkVisibility() && (!image.complete || !image.naturalWidth)).map(image => image.getAttribute('src')));
    if (!broken.length) break;
    await page.waitForTimeout(150);
  }
  assert.deepEqual(broken, [], 'Visible images load after scrolling; inactive template images are ignored');
  await page.evaluate(() => scrollTo(0, 0));
  await page.waitForTimeout(60);
}

async function layout(page, theme) {
  const data = await page.evaluate(() => {
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(node => node.checkVisibility()).map(node => ({ level: Number(node.tagName[1]), text: node.textContent.trim() }));
    const ids = [...document.querySelectorAll('[id]')].map(node => node.id);
    return {
      viewport: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      h1: document.querySelectorAll('h1').length, dark: document.documentElement.classList.contains('dark'),
      backgroundColor: getComputedStyle(document.body).backgroundColor, colorScheme: getComputedStyle(document.documentElement).colorScheme,
      duplicateIDs: ids.filter((id, i) => ids.indexOf(id) !== i),
      headingSkips: headings.filter((heading, i) => i && heading.level > headings[i - 1].level + 1),
      brokenImages: [...document.images].filter(image => image.checkVisibility() && !image.naturalWidth).map(image => image.getAttribute('src')),
    };
  });
  assert.ok(data.scrollWidth <= data.viewport, `Horizontal overflow at ${data.viewport}px`);
  assert.equal(data.h1, 1); assert.deepEqual(data.duplicateIDs, []); assert.deepEqual(data.headingSkips, []); assert.deepEqual(data.brokenImages, []);
  // No-JS themes are checked through CSS media emulation separately below.
  if (theme) assert.equal(data.dark, theme === 'dark');
  return data;
}

async function inspectHome(page, locale, noJS = false) {
  const copy = read(`data/home/${locale}.json`), badges = read('data/app-store-badges.json');
  const section = page.locator('.portfolio-featured');
  const cards = section.locator('article.app-showcase[data-product-option]');
  const ids = await cards.evaluateAll(nodes => nodes.map(node => node.dataset.productId));
  assert.equal(ids.length, 4, 'Home displays exactly four full product sections');
  assert.equal(ids[0], 'uni-note', 'Uni:Note is always first');
  assert.equal(new Set(ids).size, 4, 'Selection contains no duplicate products');
  assert.ok(ids.every(id => appByID[id]));
  const group = section.locator('[data-product-selection="3"]');
  assert.equal(await group.count(), 1);
  assert.equal(await group.locator(':scope > [data-product-option]').count(), 3);
  assert.equal(await group.getAttribute('data-selection-ready') !== null, !noJS);
  assert.equal(await group.locator('template[data-product-candidates]').count(), noJS ? 1 : 0);
  if (noJS) assert.deepEqual(ids, ['uni-note', ...candidates.slice(0, 3)], 'Original four-product fallback stays usable');
  for (const id of ids) {
    const app = appByID[id], text = copy.apps[id], card = cards.filter({ has: page.locator(`h3#${id}-name`) });
    assert.equal(await card.count(), 1); assert.equal(await card.isVisible(), true);
    assert.equal(await card.locator('.app-icon').getAttribute('src'), app.icon);
    assert.equal((await card.locator('.app-identity h3').textContent()).trim(), text.name);
    assert.equal((await card.locator('.app-identity p').textContent()).trim(), text.platform);
    const tagline = text.taglineLines?.length ? text.taglineLines.join('') : read(`data/product_details/${id}.json`).locales[locale].overviewTitle;
    assert.equal(norm(await card.locator('.app-tagline').textContent()), norm(tagline), 'Every candidate retains its own approved tagline or product overview title');
    assert.equal((await card.locator('.app-description').textContent()).trim(), text.description);
    const shots = card.locator('.app-screenshots img');
    assert.equal(await shots.count(), app.screenshots.length);
    for (let i = 0; i < app.screenshots.length; i++) {
      assert.equal(await shots.nth(i).getAttribute('src'), app.screenshots[i].small);
      assert.equal(await shots.nth(i).getAttribute('alt'), text.imageAlts[i]);
      assert.ok(Number(await shots.nth(i).getAttribute('width')) > 0 && Number(await shots.nth(i).getAttribute('height')) > 0);
    }
    const detail = card.locator(`a[href="${prefix(locale)}/products/${id}/"]`);
    assert.equal(await detail.count(), 1, 'One direct product detail action');
    if (app.status === 'published') {
      const badge = card.locator('a.app-store-badge');
      assert.equal(await badge.count(), 1); assert.equal(await badge.getAttribute('href'), app.appStoreURL);
      assert.equal(await badge.locator('img').getAttribute('src'), badges[locale].path);
      assert.deepEqual(await card.locator('.storefront-link').evaluateAll(nodes => nodes.map(node => node.dataset.country)), app.availability.verifiedStorefronts);
    } else {
      assert.equal(await card.locator('a[href^="https://apps.apple.com/"]').count(), 0, 'Nocca never receives a Store CTA');
      assert.equal((await card.locator('.status-label').textContent()).trim(), copy.development);
    }
    homeCoverage.add(id);
  }
  assert.equal(await page.locator('details.app-disclosure, .section-index').count(), 0, 'No old disclosure list or numbered Featured labels');
  return ids;
}

async function inspectCompany(page, locale, noJS = false) {
  const copy = read(`data/home/${locale}.json`), selected = {};
  for (const [area, allowed] of Object.entries(areas)) {
    const group = page.locator(`.company-areas li[data-area="${area}"] .company-area-products[data-product-selection="1"][data-area="${area}"]`);
    assert.equal(await group.count(), 1);
    const links = group.locator(':scope > a.company-product-link[data-product-option]');
    assert.equal(await links.count(), 1, 'Each area has exactly one direct product choice');
    const id = await links.getAttribute('data-product-id');
    assert.ok(allowed.includes(id), `${area} only chooses from its own candidates`);
    if (noJS) assert.equal(id, allowed[0], 'Area first candidate remains the no-JS fallback');
    assert.equal(await links.getAttribute('href'), `${prefix(locale)}/products/${id}/`);
    assert.equal(await links.locator('img').getAttribute('src'), appByID[id].icon);
    const platformStatus = copy.apps[id].platform + (appByID[id].status === 'published' ? '' : ' · ' + copy.development);
    assert.equal((await links.locator('.company-product-platform').textContent()).trim(), platformStatus, 'Development status accompanies the correct platform');
    assert.ok((await links.innerText()).includes(copy.apps[id].name));
    assert.equal(await group.getAttribute('data-selection-ready') !== null, !noJS);
    assert.equal(await group.locator('template[data-product-candidates]').count(), noJS ? 1 : 0);
    assert.equal(await group.locator('a[href^="https://apps.apple.com/"]').count(), 0);
    selected[area] = id; areaCoverage[area].add(id);
  }
  return selected;
}

async function checkSelection(page, pageType, locale, noJS = false) {
  return pageType === 'home' ? inspectHome(page, locale, noJS) : inspectCompany(page, locale, noJS);
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  async function sample({ name, pageType, locale = 'ja', width = 1440, height = 1000, theme = 'light', seed = 37, noJS = false, blockExternalJS = false, screenshot = false, fast3G = false, axe = true }) {
    const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1, colorScheme: theme, javaScriptEnabled: !noJS });
    const errors = [], blocked = [];
    try {
      if (!noJS) await addInstrumentation(context, seed);
      if (blockExternalJS) await context.route('**/*', request => {
        if (request.request().resourceType() === 'script') { blocked.push(request.request().url()); return request.abort(); }
        return request.continue();
      });
      const page = await context.newPage();
      page.on('pageerror', error => errors.push(error.message));
      page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
      if (fast3G) {
        const cdp = await context.newCDPSession(page);
        await cdp.send('Network.enable');
        await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8, connectionType: 'cellular3g' });
        await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
      }
      await page.goto(base + route(pageType, locale), { waitUntil: 'networkidle', timeout: 60000 });
      const selected = await checkSelection(page, pageType, locale, noJS);
      const initialLayoutShift = noJS ? null : await cls(page);
      await loadImages(page);
      const position = await layout(page, noJS ? null : theme);
      assert.equal(position.colorScheme, theme, 'CSS applies the requested Light/Dark theme even without JavaScript');
      const afterImageLoading = noJS ? null : await cls(page);
      if (!noJS) {
        assert.ok(initialLayoutShift.cls <= .1, 'Initial navigation CLS remains at or below 0.1');
        assert.ok(afterImageLoading.cls <= .1, 'Full image loading does not introduce a large layout shift');
      }
      assert.deepEqual(await checkSelection(page, pageType, locale, noJS), selected, 'Selection stays stable after images and scrolling');
      let violations = [];
      if (axe && !noJS) {
        await page.addScriptTag({ content: axeSource });
        violations = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] } })).violations.map(v => ({ id: v.id, impact: v.impact, targets: v.nodes.map(n => n.target) })));
        assert.deepEqual(violations, [], 'No axe violations');
      }
      if (blockExternalJS) assert.ok(blocked.length >= 1, 'External site JS was actually blocked');
      assert.deepEqual(errors, [], 'No script or HTTP errors');
      const screenshots = [];
      if (screenshot) {
        const file = path.join(screenshotPath, `${pageType === 'company' ? 'about' : 'home'}-${width === 1440 ? 'desktop' : 'mobile'}-${theme}.jpg`);
        await page.screenshot({ path: file, fullPage: true, type: 'jpeg', quality: 88 }); screenshots.push(path.relative(root, file));
      }
      return { pageType, locale, width, height, theme, noJS, blockExternalJS, fast3G, seed, selected, layout: position, initialLayoutShift, afterImageLoading, violations, blockedScripts: blocked, screenshots };
    } finally { await context.close(); }
  }
  try {
    // The shipped script, not a duplicate implementation, handles a one-option group.
    if (phase === 'all') await record('single-candidate-and-idempotence', async () => {
      const context = await browser.newContext(); const page = await context.newPage();
      try {
        await page.setContent('<main><div data-product-selection="1"><a data-product-option data-product-id="only" href="/products/only/">Only product</a><template data-product-candidates></template></div></main>');
        await page.addScriptTag({ content: selectionSource });
        assert.equal(await page.locator('[data-selection-ready] > [data-product-option]').getAttribute('data-product-id'), 'only');
        assert.equal(await page.locator('template').count(), 0);
        const first = await page.locator('main').innerHTML();
        await page.addScriptTag({ content: selectionSource });
        assert.equal(await page.locator('main').innerHTML(), first, 'Repeated execution leaves an already selected group unchanged');
        return { selected: 'only', idempotence: true, source: 'assets/js/select-products.js' };
      } finally { await context.close(); }
    });
    // A reproducible seed matrix makes candidate coverage a deterministic assertion.
    for (const seed of (phase === 'coverage' ? [6] : [1, 2, 3, 4, 5, 6, 7, 11, 19])) {
      for (const pageType of ['home', 'company']) await record(`seed-${seed}-${pageType}`, async () => {
        const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
        try {
          await addInstrumentation(context, seed); const page = await context.newPage();
          await page.goto(base + route(pageType, 'ja'), { waitUntil: 'domcontentloaded' });
          const selected = await checkSelection(page, pageType, 'ja');
          await page.addScriptTag({ content: selectionSource });
          assert.deepEqual(await checkSelection(page, pageType, 'ja'), selected, 'Page selection is idempotent');
          return { seed, pageType, selected };
        } finally { await context.close(); }
      });
    }
    await record('deterministic-candidate-coverage', async () => {
      assert.deepEqual([...homeCoverage].sort(), apps.map(app => app.id).sort());
      for (const [area, allowed] of Object.entries(areas)) assert.deepEqual([...areaCoverage[area]].sort(), [...allowed].sort());
      return { home: [...homeCoverage].sort(), company: Object.fromEntries(Object.entries(areaCoverage).map(([key, ids]) => [key, [...ids].sort()])) };
    });
    if (phase === 'all') {
    // Real reloads use browser randomness. Report variety without a flaky assertion.
    for (const pageType of ['home', 'company']) await record(`unseeded-real-reloads-${pageType}`, async () => {
      const context = await browser.newContext(); const page = await context.newPage(); const choices = [];
      try {
        for (let i = 0; i < 6; i++) {
          if (i) await page.reload({ waitUntil: 'domcontentloaded' });
          else await page.goto(base + route(pageType, 'ja'), { waitUntil: 'domcontentloaded' });
          choices.push(await checkSelection(page, pageType, 'ja'));
        }
        const combinations = new Set(choices.map(value => JSON.stringify(Array.isArray(value) ? [...value].sort() : value)));
        if (combinations.size < 2) warnings.push(`${pageType}: six unseeded reloads happened to repeat; deterministic coverage is the acceptance check.`);
        return { reloads: 5, initialNavigations: 1, choices, distinctCombinations: combinations.size, varietyObserved: combinations.size > 1 };
      } finally { await context.close(); }
    });
    for (const locale of locales) for (const [device, width, height] of [['desktop', 1440, 1000], ['mobile', 393, 852]]) for (const theme of ['light', 'dark']) for (const pageType of ['home', 'company']) {
      await record(`${pageType}-${locale}-${device}-${theme}`, () => sample({ name: `${pageType}-${locale}-${device}-${theme}`, pageType, locale, width, height, theme, screenshot: locale === 'ja', seed: locale === 'ja' ? 11 : 19 }));
    }
    for (const [device, width, height] of [['small-iphone', 320, 740], ['ipad', 834, 1194]]) for (const theme of ['light', 'dark']) for (const pageType of ['home', 'company']) {
      await record(`${pageType}-ja-${device}-${theme}`, () => sample({ pageType, width, height, theme, seed: 7 }));
    }
    for (const theme of ['light', 'dark']) for (const pageType of ['home', 'company']) {
      await record(`${pageType}-ja-no-js-${theme}`, () => sample({ pageType, width: 393, height: 852, theme, noJS: true, axe: false }));
      await record(`${pageType}-ja-external-js-blocked-${theme}`, () => sample({ pageType, width: 393, height: 852, theme, blockExternalJS: true, seed: 5 }));
    }
    for (const pageType of ['home', 'company']) await record(`${pageType}-ja-fast-3g-cls`, () => sample({ pageType, width: 393, height: 852, seed: 3, fast3G: true, axe: false }));
    }
  } finally {
    await browser.close(); writeReport(false);
  }
  console.log(JSON.stringify({ ok: results.every(r => r.ok), cases: results.length, failures: results.filter(r => !r.ok).map(r => r.name), report: reportPath, screenshots: screenshotPath }));
  if (results.some(result => !result.ok)) process.exitCode = 1;
})().catch(error => { results.push({ name: 'runner', ok: false, error: error.stack }); writeReport(false); console.error(error); process.exitCode = 1; });
