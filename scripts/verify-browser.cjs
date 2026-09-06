#!/usr/bin/env node
// Optional browser QA: provide playwright and axe-core through NODE_PATH.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const output = path.resolve(process.env.TEST_OUTPUT || 'artifacts/migration/browser');
fs.mkdirSync(output, { recursive: true });
const results = [], failures = [];
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const appData = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/apps.json'), 'utf8'));
const badgeData = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/app-store-badges.json'), 'utf8'));
const homeRoute = /^\/(?:en\/|ko\/|de\/|zh-hant\/|fr\/)?$/;
function localeFor(route) { return route.match(/^\/(en|ko|de|zh-hant|fr)\//)?.[1] || 'ja'; }
async function loaded(page) {
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 800) {
      scrollTo(0, y); await new Promise(r => setTimeout(r, 25));
    }
    scrollTo(0, 0);
    // Closed native disclosures intentionally leave their lazy images unloaded.
    await Promise.all([...document.images].filter(img => img.checkVisibility()).map(img =>
      Promise.race([img.decode().catch(() => {}), new Promise(r => setTimeout(r, 10000))])));
  });
}
async function accessibility(page) {
  return page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] } })).violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) })));
}
async function inspectStoreControls(page, route) {
  const locale = localeFor(route);
  const productID = route.match(/\/products\/([^/]+)\/$/)?.[1];
  if (!homeRoute.test(route) && !productID) return;
  const apps = productID ? appData.filter(app => app.id === productID) : appData;
  let badges = 0, regions = 0;
  for (const app of apps) {
    const scope = productID ? page.locator('.product-intro') : page.locator(`article[aria-labelledby="${app.id}-name"]`);
    assert.equal(await scope.count(), 1);
    const badge = scope.locator('a.app-store-badge');
    const flags = scope.locator('.app-availability a.storefront-link');
    assert.equal(await scope.locator('.availability-note').count(), 0);
    if (app.status !== 'published') {
      assert.equal(await scope.locator('a[href^="https://apps.apple.com/"]').count(), 0, 'Development app has no Store links');
      assert.equal(await badge.count(), 0); assert.equal(await flags.count(), 0);
      continue;
    }
    assert.equal(await badge.count(), 1, 'One official badge per published product');
    assert.equal(await badge.getAttribute('href'), app.appStoreURL, 'Badge keeps the existing verified Store URL regardless of display locale');
    const image = badge.locator('img');
    assert.equal(await image.count(), 1);
    assert.equal(await image.getAttribute('src'), badgeData[locale].path, 'Official badge uses the page display locale');
    assert.ok((await image.getAttribute('alt'))?.trim());
    if (await scope.isVisible()) {
      assert.equal(await badge.isVisible(), true);
      const bounds = await image.boundingBox();
      assert.ok(bounds.height >= 40 - .1, 'Official badge is at least 40 CSS pixels high');
      assert.ok(Math.abs(bounds.width / bounds.height - badgeData[locale].width / badgeData[locale].height) < .01, 'Badge keeps the official aspect ratio');
      assert.equal(await image.evaluate(el => getComputedStyle(el).filter), 'none', 'Official badge colors are unchanged');
    }
    assert.deepEqual(await flags.evaluateAll(nodes => nodes.map(n => n.dataset.country)), app.availability.verifiedStorefronts);
    for (const flag of await flags.all()) {
      const country = await flag.getAttribute('data-country');
      assert.equal(await flag.getAttribute('href'), app.availability.storefrontURLs[country], 'Flag uses the Apple-returned region URL');
      assert.ok((await flag.getAttribute('aria-label'))?.trim(), 'Flag needs a readable accessible name');
      assert.ok((await flag.getAttribute('title'))?.trim(), 'Flag needs a readable tooltip');
      if (await scope.isVisible()) {
        assert.equal(await flag.isVisible(), true, 'Verified region link is visible with the product');
        const bounds = await flag.boundingBox();
        assert.ok(bounds.width >= 44 - .1 && bounds.height >= 44 - .1, 'Country link has a 44px tap target');
      }
      regions++;
    }
    badges++;
  }
  if (productID) {
    assert.equal(await page.locator('.product-intro .app-actions a').evaluateAll(nodes => nodes.every(n => new URL(n.href).hostname === 'apps.apple.com')), true, 'Product introduction has no redundant internal CTA');
    const support = page.locator('section#support');
    assert.equal(await support.count(), 1);
    assert.equal(await support.locator('a[href^="mailto:kumakikai.apps@gmail.com"]').isVisible(), true, 'Support links directly to contact email');
    assert.equal(await support.locator('a').evaluateAll(nodes => nodes.every(n => !/^\/(?:en\/|ko\/|de\/|zh-hant\/|fr\/)?support\//.test(new URL(n.href).pathname))), true, 'Support resources do not detour through the directory');
    const privacy = support.locator(`a[href*="/privacy/${productID}/"]`);
    // Nocca has no published policy yet; all currently published apps do.
    if (apps[0].status === 'published') assert.equal(await privacy.isVisible(), true);
  }
  return { badges, regions };
}
async function inspectDisclosures(page, name, screenshot, axe) {
  const disclosures = page.locator('details.app-disclosure');
  assert.equal(await disclosures.count(), 4, 'Four Other Apps use disclosures');
  assert.equal(await page.locator('.section-index').count(), 0, 'Featured numbering is removed');
  assert.equal(await page.locator('.portfolio-featured .app-showcase').count(), 4);
  for (const featured of await page.locator('.portfolio-featured .app-showcase').all()) {
    assert.equal(await featured.isVisible(), true, 'Featured apps remain expanded');
    assert.equal(await featured.evaluate(el => !!el.closest('details')), false);
  }
  for (const disclosure of await disclosures.all()) {
    const summary = disclosure.locator('summary');
    assert.equal(await disclosure.evaluate(el => el.open), false, 'Other Apps start closed');
    assert.equal(await summary.isVisible(), true);
    assert.equal(await summary.locator('img, a, button').count(), 0, 'Closed summaries show titles only');
    const title = await summary.evaluate(el => {
      const copy = el.cloneNode(true); copy.querySelectorAll('[aria-hidden="true"]').forEach(n => n.remove());
      return copy.textContent.trim();
    });
    assert.equal(title, (await disclosure.locator('.app-identity h3').textContent()).trim());
    assert.equal(await disclosure.locator('.app-showcase').isVisible(), false);
  }
  const capture = screenshot && /^home-(desktop1440|iphone-pro)-/.test(name);
  const section = page.locator('section').filter({ has: page.locator('details.app-disclosure') });
  if (capture) await section.screenshot({ path: path.join(output, name + '-other-closed.png') });
  for (const disclosure of await disclosures.all()) {
    const summary = disclosure.locator('summary');
    await summary.focus(); await page.keyboard.press('Enter');
    assert.equal(await disclosure.evaluate(el => el.open), true, 'Enter opens the product');
    assert.equal(await summary.evaluate(el => {
      const style = getComputedStyle(el);
      return el === document.activeElement && el.matches(':focus-visible') && style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0;
    }), true, 'Keyboard focus has a visible outline');
    await page.keyboard.press('Space');
    assert.equal(await disclosure.evaluate(el => el.open), false, 'Space closes the product');
    await summary.click();
    assert.equal(await disclosure.evaluate(el => el.open), true, 'Click opens the product');
    assert.equal(await disclosure.locator('.app-showcase').isVisible(), true);
    assert.equal(await disclosure.locator('.app-description').isVisible(), true);
    assert.ok((await disclosure.locator('.app-description').textContent()).trim());
    assert.equal(await disclosure.locator('.app-actions a.app-store-badge[href^="https://apps.apple.com/"]').isVisible(), true);
    assert.equal(await disclosure.locator('.app-actions a[href*="/products/"]').isVisible(), true);
    const images = disclosure.locator('.app-screenshots img');
    assert.equal(await images.count(), 2, 'Each expanded product has two real screenshots');
    for (const image of await images.all()) assert.equal(await image.isVisible(), true);
  }
  assert.equal(await page.locator('details.app-disclosure[open]').count(), 4, 'All products can remain open together');
  await loaded(page);
  const storeControls = await inspectStoreControls(page, new URL(page.url()).pathname);
  const expanded = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    viewport: innerWidth,
    brokenImages: [...document.images].filter(i => i.checkVisibility() && !i.naturalWidth).map(i => i.src),
  }));
  expanded.violations = axe ? await accessibility(page) : [];
  if (capture) await section.screenshot({ path: path.join(output, name + '-other-expanded.png') });
  for (const disclosure of await disclosures.all()) await disclosure.locator('summary').click();
  await page.evaluate(() => scrollTo(0, 0));
  return { count: 4, interactions: 'passed', storeControls, ...expanded };
}
(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  async function inspect(name, route, width, height, theme, screenshot = false, axe = true) {
    if (process.env.TEST_FILTER && !new RegExp(process.env.TEST_FILTER).test(name)) return;
    const context = await browser.newContext({ viewport: { width, height }, colorScheme: theme, deviceScaleFactor: 1 });
    const page = await context.newPage(), errors = [];
    page.on('pageerror', error => errors.push(String(error)));
    page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
    await page.goto(base + route, { waitUntil: 'networkidle' });
    await loaded(page);
    const layout = await page.evaluate(() => {
      const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => ({ level: +h.tagName[1], text: h.textContent.trim() }));
      const ids = [...document.querySelectorAll('[id]')].map(n => n.id);
      return {
        viewport: innerWidth, scrollWidth: document.documentElement.scrollWidth,
        h1Count: document.querySelectorAll('h1').length,
        duplicateIDs: ids.filter((id, i) => ids.indexOf(id) !== i),
        brokenImages: [...document.images].filter(i => i.checkVisibility() && !i.naturalWidth).map(i => i.src),
        headingSkips: headings.filter((h, i) => i && h.level > headings[i - 1].level + 1),
        height: document.body.scrollHeight,
        dark: document.documentElement.classList.contains('dark'),
      };
    });
    let violations = [];
    if (axe) {
      await page.addScriptTag({ content: axeSource });
      violations = await accessibility(page);
    }
    let storeControls;
    try { storeControls = await inspectStoreControls(page, route); }
    catch (error) { errors.push(`Store controls: ${error.message}`); }
    try {
      const prefix = localeFor(route) === 'ja' ? '' : '/' + localeFor(route);
      assert.deepEqual(await page.locator('.desktop-nav a').evaluateAll(nodes => nodes.map(n => n.getAttribute('href'))), ['products','support','news','company'].map(section => `${prefix}/${section}/`));
      assert.deepEqual(await page.locator('.footer-top nav a').evaluateAll(nodes => nodes.map(n => ({ text: n.textContent.trim(), href: n.getAttribute('href') }))), [{ text: 'Contact', href: `${prefix}/company/#contact` }], 'Footer contains only the Contact navigation link');
      assert.ok((await page.locator('.site-footer').textContent()).includes('Apple'), 'Official badge legal credit remains visible');
    } catch (error) { errors.push(`Site navigation: ${error.message}`); }
    if (screenshot) {
      await page.screenshot({ path: path.join(output, name + '.png'), fullPage: true });
      await page.screenshot({ path: path.join(output, name + '-viewport.png') });
    }
    let disclosures;
    if (homeRoute.test(route)) {
      try { disclosures = await inspectDisclosures(page, name, screenshot, axe); }
      catch (error) { errors.push(`Disclosures: ${error.message}`); }
    }
    const expandedOK = !disclosures || (disclosures.scrollWidth <= width && !disclosures.brokenImages.length && !disclosures.violations.length);
    const ok = !errors.length && !violations.length && expandedOK && layout.h1Count === 1 && layout.scrollWidth <= width && !layout.duplicateIDs.length && !layout.brokenImages.length && !layout.headingSkips.length;
    const result = { name, route, theme, ...layout, storeControls, disclosures, errors, violations, ok };
    results.push(result); if (!ok) failures.push(name);
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify({ ok: false, pending: true, failures, results }, null, 2));
    console.log(JSON.stringify({ name, ok, overflow: layout.scrollWidth - width, violations: violations.map(v => v.id), headingSkips: layout.headingSkips.length }));
    await context.close();
  }
  for (const [device, width, height] of [['desktop1440',1440,1000],['desktop1280',1280,900],['ipad',834,1194],['iphone-pro',393,852],['iphone-small',320,568]]) {
    for (const theme of ['light','dark']) await inspect(`home-${device}-${theme}`, '/', width, height, theme, true);
  }
  const routes = ['/products/','/support/','/news/','/company/','/products/uni-note/','/products/oto-miru/','/products/giga-poke/','/products/nocca/','/products/uni-note-pocket/','/products/balance-calendar/','/products/smokeless/','/products/signal/','/notes/2026-09-02-giga-poke/','/htu/uni-note/','/faq/uni-note/','/privacy/uni-note/','/404.html'];
  for (const route of routes) for (const theme of ['light','dark']) await inspect(route.replace(/\W+/g,'-') + theme, route, theme === 'light' ? 1280 : 393, 900, theme, route === '/products/uni-note/');
  for (const locale of ['en','ko','de','zh-hant','fr']) {
    await inspect(`locale-${locale}-home`, `/${locale}/`, 393, 852, 'light', true);
    await inspect(`locale-${locale}-products`, `/${locale}/products/`, 393, 852, 'dark');
  }
  // Native modal: focus confinement, Escape, return focus, scroll locking and all routes.
  const context = await browser.newContext({ viewport: { width: 393, height: 852 } });
  const page = await context.newPage(); await page.goto(base, { waitUntil: 'networkidle' });
  await page.locator('.menu-toggle').focus(); await page.keyboard.press('Enter');
  assert.equal(await page.locator('#mobile-menu').evaluate(d => d.open), true);
  assert.equal(await page.locator('body').evaluate(b => getComputedStyle(b).overflow), 'hidden');
  for (let i=0; i<12; i++) {
    await page.keyboard.press('Tab');
    assert.equal(await page.evaluate(() => document.querySelector('#mobile-menu').contains(document.activeElement)), true);
  }
  await page.keyboard.press('Escape');
  // The native dialog queues its close event after updating `open`.
  await page.waitForFunction(() => !document.body.classList.contains('menu-open'));
  assert.equal(await page.locator('#mobile-menu').evaluate(d => d.open), false);
  assert.equal(await page.locator('.menu-toggle').evaluate(b => b === document.activeElement), true);
  assert.equal(await page.locator('body').evaluate(b => getComputedStyle(b).overflow !== 'hidden'), true);
  for (const route of ['products','support','news','company']) {
    await page.goto(base); await page.locator('.menu-toggle').click();
    await page.locator(`#mobile-menu a[href="/${route}/"]`).click();
    await page.waitForURL(base + '/' + route + '/');
  }
  await page.goto(base); await page.locator('#theme-toggle').click();
  const chosen = await page.locator('html').getAttribute('data-theme'); await page.reload();
  assert.equal(await page.locator('html').getAttribute('data-theme'), chosen);
  // Home's app shortcut goes directly to product support, then the permanent guide URL.
  await page.goto(base); await page.locator('.support-shortcuts a[href="/products/uni-note/#support"]').click();
  await page.waitForURL(base + '/products/uni-note/#support');
  await page.locator('#support a[href="/htu/uni-note/"]').click();
  await page.waitForURL(base + '/htu/uni-note/');
  assert.equal(await page.locator('.article-related .resource-links a[href="/htu/uni-note/"]').count(), 0, 'Legacy support navigation omits its own page');
  // The independent Support directory still links directly to the permanent guide.
  await page.goto(base + '/support/'); await page.locator('#uni-note a[href="/htu/uni-note/"]').click();
  await page.waitForURL(base + '/htu/uni-note/');
  for (const locale of ['ja','en','ko','de','zh-hant','fr']) {
    const route = (locale === 'ja' ? '' : '/' + locale) + '/privacy/';
    const response = await page.goto(base + route, { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200, 'The legacy Privacy directory remains reachable');
    assert.match(await page.locator('meta[name="robots"]').getAttribute('content'), /noindex/);
    assert.equal(await page.locator('.privacy-directory-links, .legacy-list article, .product-card').count(), 0, 'Privacy compatibility page does not duplicate the app list');
    assert.equal(await page.locator('main h1').count(), 1);
  }
  await context.close();
  const noJS = await browser.newContext({ viewport: { width: 393, height: 852 }, javaScriptEnabled: false, colorScheme: 'dark' });
  const noPage = await noJS.newPage(); await noPage.goto(base); await noPage.waitForLoadState('networkidle');
  assert.equal(await noPage.locator('.desktop-nav').isVisible(), true);
  assert.equal(await noPage.locator('#theme-toggle').isVisible(), false);
  assert.equal(await noPage.locator('body').evaluate(b => getComputedStyle(b).backgroundColor), 'rgb(23, 25, 29)');
  for (const disclosure of await noPage.locator('details.app-disclosure').all()) {
    assert.equal(await disclosure.evaluate(el => el.open), false);
    await disclosure.locator('summary').click();
    assert.equal(await disclosure.evaluate(el => el.open), true, 'Products expand without JavaScript');
    assert.equal(await disclosure.locator('.app-actions').isVisible(), true);
  }
  assert.equal(await noPage.locator('details.app-disclosure[open]').count(), 4);
  // Browser timers are disabled in this context; native image loading still works.
  assert.deepEqual(await noPage.evaluate(() => [...document.images].filter(i => i.checkVisibility() && !i.naturalWidth).map(i => i.src)), []);
  assert.equal(await noPage.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  await noPage.screenshot({ path: path.join(output, 'no-js-dark.png') }); await noJS.close();
  await browser.close();
  fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify({ ok: !failures.length, cases: results.length, interactions: 'passed', failures, results }, null, 2));
  if (failures.length) process.exitCode = 1;
})().catch(error => { console.error(error); process.exit(1); });
