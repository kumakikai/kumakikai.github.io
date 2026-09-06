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
async function loaded(page) {
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += 800) {
      scrollTo(0, y); await new Promise(r => setTimeout(r, 25));
    }
    scrollTo(0, 0);
    await Promise.all([...document.images].map(img => img.decode().catch(() => {})));
  });
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
        brokenImages: [...document.images].filter(i => !i.naturalWidth).map(i => i.src),
        headingSkips: headings.filter((h, i) => i && h.level > headings[i - 1].level + 1),
        height: document.body.scrollHeight,
        dark: document.documentElement.classList.contains('dark'),
      };
    });
    let violations = [];
    if (axe) {
      await page.addScriptTag({ content: axeSource });
      violations = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] } })).violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => ({ target: n.target, summary: n.failureSummary })) })));
    }
    if (screenshot) {
      await page.screenshot({ path: path.join(output, name + '.png'), fullPage: true });
      await page.screenshot({ path: path.join(output, name + '-viewport.png') });
    }
    const ok = !errors.length && !violations.length && layout.h1Count === 1 && layout.scrollWidth <= width && !layout.duplicateIDs.length && !layout.brokenImages.length && !layout.headingSkips.length;
    const result = { name, route, theme, ...layout, errors, violations, ok };
    results.push(result); if (!ok) failures.push(name);
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify({ ok: false, pending: true, failures, results }, null, 2));
    console.log(JSON.stringify({ name, ok, overflow: layout.scrollWidth - width, violations: violations.map(v => v.id), headingSkips: layout.headingSkips.length }));
    await context.close();
  }
  for (const [device, width, height] of [['desktop1440',1440,1000],['desktop1280',1280,900],['ipad',834,1194],['iphone-pro',393,852],['iphone-small',320,568]]) {
    for (const theme of ['light','dark']) await inspect(`home-${device}-${theme}`, '/', width, height, theme, true);
  }
  const routes = ['/products/','/support/','/news/','/company/','/products/uni-note/','/products/oto-miru/','/products/giga-poke/','/products/nocca/','/notes/2026-09-02-giga-poke/','/htu/uni-note/','/faq/uni-note/','/privacy/uni-note/','/404.html'];
  for (const route of routes) for (const theme of ['light','dark']) await inspect(route.replace(/\W+/g,'-') + theme, route, theme === 'light' ? 1280 : 393, 900, theme);
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
  // User journey: one app selection, then the existing Uni:Note guide URL.
  await page.goto(base + '/support/'); await page.locator('#uni-note a[href="/htu/uni-note/"]').click();
  await page.waitForURL(base + '/htu/uni-note/'); await context.close();
  const noJS = await browser.newContext({ viewport: { width: 393, height: 852 }, javaScriptEnabled: false, colorScheme: 'dark' });
  const noPage = await noJS.newPage(); await noPage.goto(base); await noPage.waitForLoadState('networkidle');
  assert.equal(await noPage.locator('.desktop-nav').isVisible(), true);
  assert.equal(await noPage.locator('#theme-toggle').isVisible(), false);
  assert.equal(await noPage.locator('body').evaluate(b => getComputedStyle(b).backgroundColor), 'rgb(23, 25, 29)');
  await noPage.screenshot({ path: path.join(output, 'no-js-dark.png') }); await noJS.close();
  await browser.close();
  fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify({ ok: !failures.length, cases: results.length, interactions: 'passed', failures, results }, null, 2));
  if (failures.length) process.exitCode = 1;
})().catch(error => { console.error(error); process.exit(1); });
