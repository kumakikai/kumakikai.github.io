#!/usr/bin/env node
// Browser QA for the preview of Smokeless Apple Watch support. No app/Store actions.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const reportPath = path.resolve(process.env.TEST_REPORT || path.join(root, 'docs/watch-typography/watch-browser.json'));
const screenshotDir = path.resolve(process.env.TEST_SCREENSHOTS || path.join(root, 'docs/watch-typography/screenshots'));
const details = JSON.parse(fs.readFileSync(path.join(root, 'data/product_details/smokeless.json'), 'utf8'));
const app = JSON.parse(fs.readFileSync(path.join(root, 'data/apps.json'), 'utf8')).find(item => item.id === 'smokeless');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const prefix = locale => locale === 'ja' ? '' : '/' + locale;
const results = [];
fs.mkdirSync(screenshotDir, { recursive: true });
const report = pending => {
  const failures = results.filter(item => !item.ok);
  fs.writeFileSync(reportPath, JSON.stringify({ checkedAt: new Date().toISOString(), base, pending, ok: !pending && !failures.length, cases: results.length, failures: failures.map(item => ({ name: item.name, error: item.error })), screenshotNote: 'Real Chrome screenshots of the built website. Section captures keep tested width and temporarily enlarge viewport height to fit the section, preventing Chrome from painting off-screen fixed elements into a beyond-viewport clip. Test viewport is restored; no CSS or element visibility is modified.', results }, null, 2) + '\n');
};
async function loadImages(page, noJS) {
  for (const image of await page.locator('img:visible').all()) {
    await image.scrollIntoViewIfNeeded();
    if (noJS) await page.waitForLoadState('networkidle');
  }
  if (!noJS) await page.evaluate(async () => {
    await Promise.all([...document.images].filter(i => i.checkVisibility()).map(i => Promise.race([i.decode().catch(() => {}), new Promise(r => setTimeout(r, 10000))])));
  });
}
async function screenshotSection(page, section, filename) {
  // Chrome's beyond-viewport element capture can paint a fixed, off-screen skip
  // link into the clip. Keep the tested width, fit the section vertically, then
  // restore the test viewport. No page CSS or visibility is changed.
  const viewport = page.viewportSize();
  const box = await section.boundingBox();
  if (box.height > viewport.height) await page.setViewportSize({ width: viewport.width, height: Math.ceil(box.height) + 160 });
  await section.scrollIntoViewIfNeeded();
  await section.screenshot({ path: filename, type: 'jpeg', quality: 90 });
  await page.setViewportSize(viewport);
}
async function inspect(browser, locale, kind, width, theme, noJS = false) {
  const name = `${kind}-${locale}-${width}-${theme}${noJS ? '-no-js' : ''}`;
  if (process.env.TEST_FILTER && !new RegExp(process.env.TEST_FILTER).test(name)) return;
  const url = base + prefix(locale) + (kind === 'product' ? '/products/smokeless/' : '/htu/smokeless/');
  const context = await browser.newContext({ viewport: { width, height: width > 700 ? 1000 : 844 }, colorScheme: theme, javaScriptEnabled: !noJS, deviceScaleFactor: 1 });
  const page = await context.newPage();
  page.setDefaultTimeout(12000);
  const failures = [];
  page.on('pageerror', e => failures.push(String(e)));
  page.on('response', r => { if (r.status() >= 400) failures.push(`${r.status()} ${r.url()}`); });
  const result = { name, locale, kind, width, theme, javaScript: !noJS, url };
  try {
    const response = await page.goto(url, { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200, 'Existing page stays HTTP 200');
    result.documentSHA256 = crypto.createHash('sha256').update(await response.body()).digest('hex');
    await loadImages(page, noJS);
    const copy = details.watch.locales[locale];
    const section = page.locator('#apple-watch');
    assert.equal(await section.count(), 1, 'One Watch section');
    assert.equal(await section.getAttribute('data-watch-status'), details.watch.status);
    const review = section.locator('.watch-review-note');
    assert.equal(await review.count(), details.watch.status === 'published' ? 0 : 1, 'Release-specific preview notice');
    if (details.watch.status !== 'published') assert.equal((await review.textContent()).trim(), copy.reviewNotice);
    const sectionText = await section.textContent();
    assert(sectionText.includes(copy.requirement), 'Purchase prerequisite is stated');
    assert(sectionText.includes(copy.environment), 'Paired devices and OS requirement are stated');
    if (kind === 'product') {
      assert.equal((await section.locator('h2').textContent()).trim(), copy.title);
      assert(sectionText.includes(copy.description), 'Watch tap actions are concrete');
      assert(sectionText.includes(copy.counts), 'Daily counts and iPhone history distinction are stated');
      assert(sectionText.includes(copy.sync), 'Disconnected recording and first unlock prerequisite are stated');
      assert.equal(await section.locator('img').count(), 2, 'Actual iPhone and Watch UI are paired');
      assert.equal(await section.locator('.watch-device-figure img').getAttribute('alt'), copy.watchAlt);
      const fallback = !details.watch.media.localized[locale];
      assert.equal(await section.locator('.watch-device-figure--raw').count(), fallback ? 1 : 0, 'Missing localized marketing uses actual number-only Watch UI');
      const badgeURLs = await page.locator('main .app-store-badge').evaluateAll(items => items.map(i => i.getAttribute('href')));
      assert.deepEqual(badgeURLs, [app.appStoreURL, app.appStoreURL], 'Existing iPhone download remains available in Hero and after product explanation');
      assert.equal(await section.locator('.app-store-badge').count(), 0, 'Preview feature adds no misleading Watch download CTA');
      const hero = page.locator('.product-intro');
      assert.equal((await hero.locator('.watch-hero-note').textContent()).trim(), details.watch.status === 'published' ? copy.heroPublished : copy.heroReview);
      const platform = await hero.locator('.app-identity p').textContent();
      assert(platform.includes('iPhone / Apple Watch'), 'Hero names both devices');
      if (details.watch.status !== 'published') assert(platform.includes(copy.platformPending), 'Apple Watch platform is marked upcoming');
      const badges = await page.locator('main .app-store-badge').evaluateAll(items => items.map(i => ({ top: i.getBoundingClientRect().top + scrollY, bottom: i.getBoundingClientRect().bottom + scrollY })));
      assert(badges[1].top - badges[0].bottom > 844, 'Two badges are separated by product explanation');
      result.badges = { count: badgeURLs.length, href: badgeURLs[0], verticalSeparation: badges[1].top - badges[0].bottom };
    } else {
      assert.equal((await section.locator('h2').textContent()).trim(), copy.guideTitle);
      assert.equal(await section.locator('ol.watch-guide-steps > li').count(), 4, 'Four operation steps');
      for (const step of copy.guideSteps) { assert(sectionText.includes(step.title)); assert(sectionText.includes(step.description)); }
      assert.equal(await section.locator('img').getAttribute('alt'), copy.guideImageAlt);
      assert.equal(await section.locator('.app-store-badge').count(), 0, 'Guide is operational, without a duplicate Store CTA');
    }
    result.layout = await page.evaluate(() => {
      const visible = n => n.checkVisibility();
      const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(visible);
      const ids = [...document.querySelectorAll('[id]')].map(n => n.id);
      return { width: innerWidth, scrollWidth: document.documentElement.scrollWidth, h1Count: document.querySelectorAll('h1').length,
        duplicateIDs: ids.filter((id, i) => ids.indexOf(id) !== i),
        headingSkips: hs.flatMap((n, i) => i && Number(n.tagName[1]) > Number(hs[i-1].tagName[1]) + 1 ? [n.textContent] : []),
        images: [...document.querySelectorAll('#apple-watch img')].map(i => ({ src: i.currentSrc, width: i.naturalWidth, height: i.naturalHeight, displayedWidth: i.getBoundingClientRect().width, alt: i.alt, loading: i.loading, explicitWidth: i.getAttribute('width'), explicitHeight: i.getAttribute('height') })),
        brokenImages: [...document.images].filter(i => visible(i) && !i.naturalWidth).map(i => i.getAttribute('src')),
        darkMode: document.documentElement.classList.contains('dark') };
    });
    assert(result.layout.scrollWidth <= width, 'No horizontal overflow');
    assert.equal(result.layout.h1Count, 1);
    assert.deepEqual(result.layout.duplicateIDs, []);
    assert.deepEqual(result.layout.headingSkips, []);
    assert.deepEqual(result.layout.brokenImages, []);
    assert.equal(result.layout.darkMode, theme === 'dark', 'Theme follows preference with or without JavaScript');
    for (const i of result.layout.images) { assert(i.alt && i.explicitWidth && i.explicitHeight); assert.equal(i.loading, 'lazy'); assert(i.displayedWidth > 90); }
    if (!noJS) {
      await page.addScriptTag({ content: axeSource });
      result.axe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice'] } })).violations.map(v => ({ id:v.id, impact:v.impact, targets:v.nodes.map(n=>n.target) })));
      assert.deepEqual(result.axe, [], 'No automated accessibility violations');
      const imageLink = section.locator('figure a').last();
      await imageLink.focus(); await page.keyboard.press('Tab'); await page.keyboard.press('Shift+Tab');
      result.keyboardFocus = await imageLink.evaluate(n => n === document.activeElement && getComputedStyle(n).outlineStyle !== 'none' && parseFloat(getComputedStyle(n).outlineWidth) > 0);
      assert(result.keyboardFocus, 'Image link keyboard focus is visible');
    } else result.axe = 'not run: JavaScript disabled; semantic DOM, image, release, links and layout checks performed';
    if (!noJS && locale === 'ja' && theme === 'light') {
      await page.evaluate(() => document.activeElement?.blur());
      await page.mouse.move(0, 0);
      if (kind === 'product') {
        const file = `watch-product-section-${width}.jpg`;
        await screenshotSection(page, section, path.join(screenshotDir, file));
        result.screenshot = file;
        await page.evaluate(() => scrollTo(0,0));
        const heroFile = `smokeless-hero-${width}.jpg`;
        await page.screenshot({ path: path.join(screenshotDir, heroFile), type: 'jpeg', quality: 90 });
        result.heroScreenshot = heroFile;
      } else if (width === 390) {
        const file = 'watch-guide-390.jpg';
        await screenshotSection(page, section, path.join(screenshotDir, file));
        result.screenshot = file;
      }
    }
    assert.deepEqual(failures, [], 'No browser or HTTP errors');
    result.ok = true;
  } catch (e) {
    result.ok = false; result.error = e.message; result.browserErrors = failures;
    await page.screenshot({ path: path.join(screenshotDir, `${name}-failure.jpg`), type: 'jpeg', quality: 80, fullPage: true }).catch(() => {});
  }
  results.push(result); report(true);
  console.log(JSON.stringify({ name, ok: result.ok, error: result.error }));
  await context.close();
}
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
  try {
    for (const locale of ['ja','en','ko','de','fr','zh-hant']) for (const width of [1440,390]) for (const theme of ['light','dark']) await inspect(browser,locale,'product',width,theme);
    for (const locale of ['ja','en','ko','fr','zh-hant']) for (const width of [1440,390]) for (const theme of ['light','dark']) await inspect(browser,locale,'guide',width,theme);
    for (const kind of ['product','guide']) for (const width of [1440,390]) await inspect(browser,'ja',kind,width,'light',true);
  } finally { await browser.close(); report(false); }
  process.exitCode = results.some(r => !r.ok) ? 1 : 0;
})().catch(e => { console.error(e); process.exitCode = 1; });
