#!/usr/bin/env node
// Japanese editorial/layout QA. Dependencies are supplied through NODE_PATH.
const { chromium, webkit, firefox } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const baseline = process.env.TEST_PHASE === 'before';
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const folder = path.join(root, 'docs/copy-audit');
const screenshots = path.join(folder, 'screenshots');
const reportPath = path.resolve(process.env.TEST_REPORT || path.join(folder, baseline ? 'typography-before.json' : 'browser-verification.json'));
const results = [];
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const runtimeAvailability = Object.fromEntries(Object.entries({ webkit, firefox }).map(([name, runtime]) => [name, fs.existsSync(runtime.executablePath())]));
const apps = JSON.parse(fs.readFileSync(path.join(root, 'data/apps.json'), 'utf8'));
fs.mkdirSync(screenshots, { recursive: true });
fs.mkdirSync(path.dirname(reportPath), { recursive: true });

function report(pending) {
  fs.writeFileSync(reportPath, JSON.stringify({
    checkedAt: new Date().toISOString(), base, phase: baseline ? 'before' : 'after', pending,
    ok: !pending && results.every(result => result.ok), cases: results.length,
    failures: results.filter(result => !result.ok).map(result => ({ name: result.name, errors: result.errors })),
    browser: 'Installed Google Chrome, headless', defaultPlaywrightCacheAvailability: runtimeAvailability,
    method: 'DOM Range character rectangles reconstruct visual lines. Japanese word-boundary candidates from Intl.Segmenter are recorded for editorial review, not treated as a universal pass/fail rule. CSS normal fallback disables auto-phrase without changing text or widths.',
    limitations: ['Chrome desktop emulation, not physical iPad or iPhone.', 'This script runs Chrome only. Normal word-break fallback is a compatibility check, not evidence of running WebKit or Firefox; separate browser reports document other engines.', 'Automated accessibility and line geometry do not replace visual/editorial review.'],
    results,
  }, null, 2) + '\n');
}

async function visualLines(page) {
  return page.evaluate(() => {
    const segmenter = new Intl.Segmenter('ja', { granularity: 'word' });
    function lines(element) {
      const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      const units = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement.checkVisibility() || node.parentElement.closest('[aria-hidden="true"]')) continue;
        let offset = 0;
        for (const char of node.textContent) {
          const range = document.createRange();
          range.setStart(node, offset); offset += char.length; range.setEnd(node, offset);
          const bounds = range.getBoundingClientRect();
          if (bounds.width && bounds.height) units.push({ char, top: Math.round(bounds.top * 2) / 2, left: Math.round(bounds.left * 2) / 2 });
        }
      }
      const rows = [];
      for (const unit of units) {
        let row = rows.find(row => Math.abs(row.top - unit.top) < 3);
        if (!row) rows.push(row = { top: unit.top, text: '' });
        row.text += unit.char;
      }
      const textLines = rows.sort((a,b) => a.top - b.top).map(row => row.text.trim()).filter(Boolean);
      const joined = textLines.join('');
      const boundaries = []; let length = 0;
      textLines.slice(0,-1).forEach(line => { length += line.length; boundaries.push(length); });
      const splitWords = [...segmenter.segment(joined)].filter(word => word.isWordLike && /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]/u.test(word.segment) && boundaries.some(index => index > word.index && index < word.index + word.segment.length)).map(word => word.segment);
      const style = getComputedStyle(element);
      return { tag: element.tagName.toLowerCase(), class: element.className, text: element.textContent.trim().replace(/\s+/g,' '), lines: textLines, splitWords,
        width: Math.round(element.getBoundingClientRect().width), fontSize: style.fontSize, lineHeight: style.lineHeight,
        letterSpacing: style.letterSpacing, wordBreak: style.wordBreak, overflowWrap: style.overflowWrap, lineBreak: style.lineBreak, textWrap: style.textWrap };
    }
    const main = document.querySelector('main');
    return {
      supportsAutoPhrase: CSS.supports('word-break', 'auto-phrase'),
      headings: [...main.querySelectorAll('h1,h2,h3')].filter(element => element.checkVisibility()).map(lines),
      contact: [...document.querySelectorAll('#contact p,.contact-panel h2,.contact-panel p')].filter(element => element.checkVisibility()).filter((element,index,all) => all.indexOf(element) === index).map(lines),
    };
  });
}

async function inspect(browser, route, width, options = {}) {
  const name = `${route.replaceAll('/','-') || 'home'}-${width}-${options.fallback ? 'normal-fallback' : options.theme || 'light'}`;
  if (process.env.TEST_FILTER && !new RegExp(process.env.TEST_FILTER).test(name)) return;
  const context = await browser.newContext({ viewport: { width, height: width <= 393 ? 852 : 1000 }, deviceScaleFactor: 1, colorScheme: options.theme || 'light' });
  await context.addInitScript(() => { let state = 1; Math.random = () => { state = (state * 16807) % 2147483647; return (state - 1) / 2147483646; }; });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.setDefaultTimeout(15000);
  let detail = {};
  try {
    const response = await page.goto(base + route, { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200, 'Page exists');
    if (options.fallback) await page.evaluate(() => {
      // Simulate unsupported auto-phrase without disabling explicit keep-all
      // rules that are part of the intended cross-browser fallback.
      const enhanced = [...document.querySelectorAll(':lang(ja)')].filter(element => getComputedStyle(element).wordBreak === 'auto-phrase');
      for (const element of enhanced) element.style.setProperty('word-break', 'normal', 'important');
    });
    for (const image of await page.locator('main img:visible').all()) await image.scrollIntoViewIfNeeded();
    await page.evaluate(async () => {
      await Promise.all([...document.images].filter(image => image.checkVisibility()).map(image => image.decode().catch(() => {})));
      await document.fonts.ready; scrollTo(0,0);
    });
    const layout = await page.evaluate(() => {
      const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(element => element.checkVisibility()).map(element => ({ level: +element.tagName.slice(1), text: element.textContent.trim() }));
      return { viewport: innerWidth, scrollWidth: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight,
        brokenImages: [...document.images].filter(image => image.checkVisibility() && !image.naturalWidth).map(image => image.src),
        headingSkips: headings.filter((heading,index) => index && heading.level > headings[index - 1].level + 1),
        h1Count: document.querySelectorAll('h1').length,
        horizontalElements: [...document.querySelectorAll('main *')].filter(element => element.checkVisibility() && element.getBoundingClientRect().right > innerWidth + 1).slice(0,12).map(element => ({ tag: element.tagName, class: element.className })),
      };
    });
    assert.ok(layout.scrollWidth <= width, `No horizontal overflow (${layout.scrollWidth} > ${width})`);
    assert.deepEqual(layout.brokenImages, [], 'Images load');
    assert.equal(layout.h1Count, 1, 'One h1');
    assert.deepEqual(layout.headingSkips, [], 'Heading hierarchy');
    detail = { route, width, theme: options.theme || 'light', normalFallback: Boolean(options.fallback), layout, ...await visualLines(page) };
    if (!baseline) {
      if (route === '/company/') {
        const copy = JSON.parse(fs.readFileSync(path.join(root, 'data/company/ja.json'), 'utf8'));
        const body = await page.locator('body').innerText();
        assert.equal(/中村\s*裕也|iPad専用/.test(body), false, 'Founder and device naming');
        assert.equal(await page.locator('.company-facts dt').count(), 3, 'Three useful facts only');
        assert.equal((await page.locator('.company-facts').innerText()).includes('kumakikai.apps@gmail.com'), false, 'Email omitted from facts');
        assert.equal(await page.locator('.company-philosophy').count(), 0, 'Generic principles section removed in Japanese');
        assert.equal(await page.locator('#contact a[href^="mailto:"]').count(), 1, 'One direct Contact CTA');
        const areas = [];
        for (const item of copy.areas) {
          const row = page.locator(`.company-areas li[data-area="${item.area}"]`);
          const id = await row.locator('[data-product-option]').getAttribute('data-product-id');
          assert.equal(apps.find(app => app.id === id).area, item.area, 'Category membership is respected');
          assert.equal((await row.locator('h3').innerText()).trim(), item.title);
          areas.push({ area: item.area, product: id, title: item.title });
        }
        detail.areaSelection = areas;
        assert.deepEqual(areas.map(area => area.area), ['learning','communication','utilities']);
      }
      if (options.axe !== false) {
        await page.addScriptTag({ content: axeSource });
        detail.axe = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice'] } })).violations.map(violation => ({ id: violation.id, impact: violation.impact, targets: violation.nodes.map(node => node.target) })));
        assert.deepEqual(detail.axe, [], 'axe accessibility');
      }
    }
    if (route === '/company/' && [1440,393].includes(width) && !options.fallback && !options.theme) {
      const label = width === 1440 ? 'desktop' : 'mobile';
      const phaseLabel = baseline ? '-before' : '';
      await page.screenshot({ path: path.join(screenshots, `about-${label}${phaseLabel}.jpg`), fullPage: true, quality: 82 });
      await page.locator('#contact').screenshot({ path: path.join(screenshots, `contact-${label}${phaseLabel}.jpg`), type: 'jpeg', quality: 88 });
    }
  } catch(error) { errors.push(error.message); }
  results.push({ name, ok: !errors.length, errors, ...detail });
  console.log(`${errors.length ? 'FAIL' : 'PASS'} ${name}${errors.length ? ': ' + errors.join('; ') : ''}`);
  report(true);
  await context.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  try {
    for (const width of [1440,1280,834,393,320]) await inspect(browser, '/company/', width);
    if (!baseline) {
      for (const width of [1440,1280,834,393,320]) await inspect(browser, '/company/', width, { fallback: true, axe: false });
      await inspect(browser, '/company/', 393, { theme: 'dark' });
      const routes = ['/', '/products/', ...apps.map(app => `/products/${app.id}/`), '/news/', '/support/', '/htu/uni-note/', '/faq/uni-note/', '/notes/2026-09-02-giga-poke/'];
      for (const route of routes) for (const width of [1440,393]) await inspect(browser, route, width);
      for (const width of [1280,834,320]) await inspect(browser, '/', width, { axe: false });
      for (const width of [1280,834,320]) await inspect(browser, '/products/uni-note/', width, { axe: false });
      await inspect(browser, '/news/', 320);
      for (const width of [1440,393,320]) await inspect(browser, '/news/', width, { fallback: true, axe: false });
      const phraseArticles = ['2026-01-26-roadmap','2026-02-14-blog','2026-03-13-blog','2026-03-25-blog','2026-04-12-uni-note-10000','2026-05-26-android-release'];
      for (const article of phraseArticles) for (const width of [393,320]) await inspect(browser, `/notes/${article}/`, width, { fallback: true, axe: width === 393 });
    }
  } finally { await browser.close(); report(false); }
  process.exitCode = results.every(result => result.ok) ? 0 : 1;
})().catch(error => { console.error(error); report(false); process.exitCode = 1; });
