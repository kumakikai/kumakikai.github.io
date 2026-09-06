#!/usr/bin/env node
// Focused Company/News browser QA; provide playwright and axe-core through NODE_PATH.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const output = path.resolve(process.env.TEST_OUTPUT || 'artifacts/company/browser');
const report = path.resolve(process.env.TEST_REPORT || 'docs/company/browser-verification.json');
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const apps = read('data/apps.json');
const news = read('data/news.json');
const locales = ['ja', 'en', 'ko', 'de', 'fr', 'zh-hant'];
const categories = ['press-release', 'blog', 'information'];
const categoryCountsByLocale = {};
const publishedCount = apps.filter(app => app.status === 'published').length;
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const prefix = locale => locale === 'ja' ? '' : '/' + locale;
const results = [];
fs.mkdirSync(output, { recursive: true });
fs.mkdirSync(path.dirname(report), { recursive: true });

function writeReport(pending) {
  const failures = results.filter(result => !result.ok).map(result => result.name);
  const summary = { ok: !pending && !failures.length, pending, cases: results.length, base, publishedCount, categoryCountsByLocale, newsCountSource: 'Initial unfiltered DOM in each locale; existing metadata entries remain required.', failures, results };
  fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify(summary, null, 2) + '\n');
  if (!pending) fs.writeFileSync(report, JSON.stringify(summary, null, 2) + '\n');
}

async function loadImages(page) {
  // This helper is used only with JavaScript enabled. Native no-JS checks below
  // avoid browser timers, which do not execute in that context.
  for (const image of await page.locator('img:visible').all()) await image.scrollIntoViewIfNeeded();
  await page.evaluate(async () => {
    await Promise.all([...document.images].filter(image => image.checkVisibility()).map(image =>
      Promise.race([image.decode().catch(() => {}), new Promise(resolve => setTimeout(resolve, 10000))])));
    scrollTo(0, 0);
  });
}

async function layout(page) {
  const result = await page.evaluate(() => {
    const visible = element => element.checkVisibility();
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(visible).map(element => ({ level: Number(element.tagName[1]), text: element.textContent.trim() }));
    const ids = [...document.querySelectorAll('[id]')].map(element => element.id);
    return {
      width: innerWidth, scrollWidth: document.documentElement.scrollWidth, height: document.body.scrollHeight,
      h1Count: document.querySelectorAll('h1').length,
      duplicateIDs: ids.filter((id, index) => ids.indexOf(id) !== index),
      headingSkips: headings.filter((heading, index) => index && heading.level > headings[index - 1].level + 1),
      brokenImages: [...document.images].filter(image => visible(image) && !image.naturalWidth).map(image => image.getAttribute('src')),
    };
  });
  assert.ok(result.scrollWidth <= result.width, `Horizontal overflow: ${result.scrollWidth - result.width}px`);
  assert.equal(result.h1Count, 1, 'One page heading');
  assert.deepEqual(result.duplicateIDs, [], 'Unique IDs');
  assert.deepEqual(result.headingSkips, [], 'Sequential heading hierarchy');
  assert.deepEqual(result.brokenImages, [], 'Visible images loaded');
  return result;
}

async function accessibility(page) {
  const violations = await page.evaluate(async () => (await axe.run(document, {
    runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] },
  })).violations.map(item => ({ id: item.id, impact: item.impact, targets: item.nodes.map(node => node.target) })));
  assert.deepEqual(violations, [], 'Accessibility checks');
  return violations;
}

async function keyboardFocus(page, link) {
  await link.focus();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Shift+Tab');
  assert.equal(await link.evaluate(element => {
    const style = getComputedStyle(element);
    return element === document.activeElement && element.matches(':focus-visible') && style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0;
  }), true, 'Keyboard focus is visible');
}

async function company(page, locale, name) {
  const copy = read(`data/company/${locale}.json`);
  const corp = read(`data/corporate/${locale}.json`);
  assert.equal((await page.locator('.page-heading h1').textContent()).trim(), corp.companyTitle, 'Existing Company hero title stays unchanged');
  assert.equal((await page.locator('.page-heading > p').last().textContent()).trim(), corp.companyIntro);
  const sections = ['.company-about', '.company-profile', '.company-build', '.company-philosophy', '.company-media', '.company-information', '#contact'];
  let previousBottom = 0;
  for (const selector of sections) {
    const section = page.locator('.company-page ' + selector);
    assert.equal(await section.count(), 1, selector);
    assert.equal(await section.isVisible(), true, selector);
    const bounds = await section.boundingBox();
    assert.ok(bounds.y >= previousBottom - 1, 'Company sections do not overlap');
    previousBottom = bounds.y + bounds.height;
  }
  assert.deepEqual(await page.locator('.company-about > div > p').allTextContents(), copy.about);
  assert.equal((await page.locator('.founder-identity h3').textContent()).trim(), copy.founderName);
  assert.equal((await page.locator('.founder-english').textContent()).trim(), copy.founderEnglishName);
  assert.equal((await page.locator('.founder-role').textContent()).trim(), copy.founderRole);
  assert.deepEqual(await page.locator('.founder-bio > p').allTextContents(), copy.founderBio);
  assert.equal((await page.locator('.founder-experience dd').first().textContent()).trim(), copy.experience.join(' / '));
  assert.equal((await page.locator('.founder-experience dd').last().textContent()).trim(), 'C / C++ / C# / Java / Python / Dart / Swift');
  assert.equal((await page.locator('.company-build-intro').textContent()).trim(), copy.buildIntro.replace('%d', publishedCount));
  assert.deepEqual(await page.locator('.company-areas h3').allTextContents(), copy.areas.map(area => area.title));
  assert.deepEqual(await page.locator('.company-areas li > div > p').allTextContents(), copy.areas.map(area => area.description));
  assert.deepEqual(await page.locator('.company-product-link').evaluateAll(links => links.map(link => link.getAttribute('href'))), copy.areas.map(area => `${prefix(locale)}/products/${area.product}/`));
  assert.deepEqual(await page.locator('.company-philosophy h3').allTextContents(), copy.principles.map(principle => principle.title));
  assert.deepEqual(await page.locator('.company-philosophy li > p').allTextContents(), copy.principles.map(principle => principle.description));
  assert.equal(await page.locator('a[href^="mailto:"]').count(), 1, 'Email CTA appears only in Contact');
  assert.equal(await page.locator('#contact a[href^="mailto:"]').count(), 1);
  assert.equal(await page.locator('a[href^="tel:"]').count(), 0, 'No telephone link');
  const body = await page.locator('body').innerText();
  // Only report the boolean result; never write a matching number to an artifact.
  assert.equal(/\d{10,}|\b\d{2,4}[- ]\d{2,4}[- ]\d{3,4}\b/.test(body), false, 'No telephone-like number is published');
  for (const script of await page.locator('script[type="application/ld+json"]').allTextContents()) {
    assert.equal(/"telephone"\s*:/.test(script), false, 'Structured data does not publish a telephone number');
  }
  assert.equal(await page.locator('.company-philosophy a').getAttribute('href'), `${prefix(locale)}/news/#blog`);
  assert.equal(await page.locator('.company-media a').first().getAttribute('href'), `${prefix(locale)}/news/#press-release`);
  const contact = page.locator('.company-media a[href="#contact"]');
  await keyboardFocus(page, contact);
  await page.keyboard.press('Enter');
  assert.equal(new URL(page.url()).hash, '#contact');
  assert.equal(await page.locator('#contact h2').evaluate(element => {
    const bounds = element.getBoundingClientRect();
    return bounds.top >= 0 && bounds.top < innerHeight && bounds.bottom > 0;
  }), true, 'Media CTA reaches the Contact heading');
  await keyboardFocus(page, page.locator('#contact a'));
  const position = await layout(page);
  const violations = await accessibility(page);
  await page.locator('.page-heading').scrollIntoViewIfNeeded();
  await page.evaluate(() => scrollTo(0, 0));
  await page.screenshot({ path: path.join(output, `${name}.png`), fullPage: true });
  await page.screenshot({ path: path.join(output, `${name}-viewport.png`) });
  return { ...position, sections: sections.length, publishedCount, violations, mediaContact: 'passed', keyboardFocus: 'passed', phoneNotPublished: true };
}

async function newsState(page, locale, category, useAxe, counts) {
  const expectedCount = counts[category];
  const rows = page.locator('.news-row:visible');
  assert.equal(await rows.count(), expectedCount, `Visible ${category} article count`);
  if (category !== 'all-news') assert.equal(await rows.evaluateAll((nodes, value) => nodes.every(node => node.dataset.category === value), category), true);
  const empty = page.locator('.news-filter-empty:visible');
  assert.equal(await empty.count(), expectedCount === 0 ? 1 : 0, 'Empty notice appears only for an empty selected category');
  if (expectedCount === 0) assert.equal((await empty.textContent()).trim(), read(`data/company/${locale}.json`).newsEmpty);
  const active = page.locator(`.news-filters #${category}`);
  assert.equal(await active.evaluate(element => {
    const style = getComputedStyle(element);
    return style.borderBottomColor !== 'rgba(0, 0, 0, 0)' && Number(style.fontWeight) >= 600;
  }), true, 'Selected filter has a visible state');
  return { category, count: expectedCount, ...await layout(page), violations: useAxe ? await accessibility(page) : undefined };
}

async function newsFilters(page, locale, name, noJS) {
  const route = `${prefix(locale)}/news/`;
  assert.deepEqual(await page.locator('.news-filters a').evaluateAll(links => links.map(link => link.getAttribute('href'))), ['#all-news', ...categories.map(category => '#' + category)]);
  const rendered = await page.locator('.news-row').evaluateAll(rows => rows.map(row => ({
    id: new URL(row.querySelector('h2 a').href).pathname.split('/').filter(Boolean).at(-1),
    category: row.dataset.category, label: row.querySelector('.news-category').textContent.trim(),
  })));
  const renderedIDs = new Set(rendered.map(row => row.id));
  for (const id of Object.keys(news)) assert.ok(renderedIDs.has(id), `Existing article remains listed: ${id}`);
  const corp = read(`data/corporate/${locale}.json`);
  const labels = { 'press-release': corp.pressRelease, blog: corp.blog, information: corp.information };
  for (const row of rendered) {
    assert.ok(categories.includes(row.category), 'Every article uses a supported category');
    if (news[row.id]) assert.equal(row.category, news[row.id].category, 'Existing article category matches source metadata');
    assert.equal(row.label, labels[row.category], 'Visible category label matches its category');
  }
  // New Markdown articles may define their category in front matter and need no
  // data/news.json entry. Capture counts before any filter transition instead.
  const counts = Object.fromEntries(categories.map(category => [category, rendered.filter(row => row.category === category).length]));
  counts['all-news'] = rendered.length;
  categoryCountsByLocale[locale] = counts;
  const states = [await newsState(page, locale, 'all-news', !noJS, counts)];
  for (const category of categories) {
    const link = page.locator(`.news-filters #${category}`);
    if (category === 'blog') {
      await keyboardFocus(page, link);
      await page.keyboard.press('Enter');
    } else await link.click();
    assert.equal(new URL(page.url()).hash, '#' + category);
    states.push(await newsState(page, locale, category, !noJS, counts));
    if (locale === 'ja') await page.screenshot({ path: path.join(output, `${name}-${category}.png`), fullPage: true });
  }
  await page.goBack();
  assert.equal(new URL(page.url()).hash, '#blog', 'Back restores the previous native filter URL');
  await newsState(page, locale, 'blog', !noJS, counts);
  await page.locator('.news-filters #all-news').click();
  assert.equal(new URL(page.url()).hash, '#all-news');
  await newsState(page, locale, 'all-news', !noJS, counts);
  if (noJS) {
    for (const category of [...categories, 'all-news']) {
      await page.goto('about:blank');
      const response = await page.goto(base + route + '#' + category, { waitUntil: 'load' });
      assert.equal(response.status(), 200);
      await newsState(page, locale, category, false, counts);
    }
  }
  return { categoryCounts: counts, states, interaction: 'click, keyboard Enter, Back and All passed', initialHashWithoutJavaScript: noJS ? '4 targets passed' : undefined };
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  try {
    async function inspect(name, locale, kind, width, height, theme, noJS = false) {
      if (process.env.TEST_FILTER && !new RegExp(process.env.TEST_FILTER).test(name)) return;
      const route = `${prefix(locale)}/${kind === 'home' ? '' : kind + '/'}`;
      const context = await browser.newContext({ viewport: { width, height }, colorScheme: theme, javaScriptEnabled: !noJS, deviceScaleFactor: 1 });
      const page = await context.newPage();
      page.setDefaultTimeout(15000);
      const errors = [];
      page.on('pageerror', error => errors.push(String(error)));
      page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
      let detail = {};
      try {
        const response = await page.goto(base + route, { waitUntil: 'networkidle' });
        assert.equal(response.status(), 200);
        if (!noJS) {
          await loadImages(page);
          await page.addScriptTag({ content: axeSource });
        }
        if (kind === 'company') detail = await company(page, locale, name);
        else if (kind === 'news') detail = await newsFilters(page, locale, name, noJS);
        else {
          assert.equal(await page.locator('.news-filters, .news-filter-empty').count(), 0, 'Home has no category filter UI');
          assert.equal(await page.locator('.news-row').count(), 3, 'Home retains its three latest news items');
          detail = { ...await layout(page), violations: await accessibility(page), newsFilters: 'absent' };
        }
      } catch (error) {
        errors.push(error.message);
        await page.screenshot({ path: path.join(output, `${name}-failure.png`), fullPage: true }).catch(() => {});
      }
      results.push({ name, locale, kind, route, width, height, theme, javaScript: !noJS, ...detail, errors, ok: !errors.length });
      writeReport(true);
      console.log(JSON.stringify({ name, ok: !errors.length, errors }));
      await context.close();
    }
    for (const [device, width, height] of [['desktop1440',1440,1000], ['desktop1280',1280,900], ['ipad',834,1194], ['iphone-pro',393,852], ['iphone-small',320,568]]) {
      for (const theme of ['light', 'dark']) await inspect(`company-ja-${device}-${theme}`, 'ja', 'company', width, height, theme);
    }
    for (const locale of locales.filter(locale => locale !== 'ja')) {
      await inspect(`company-${locale}-desktop-light`, locale, 'company', 1280, 900, 'light');
      await inspect(`company-${locale}-mobile-dark`, locale, 'company', 393, 852, 'dark');
    }
    for (const locale of locales) {
      await inspect(`news-${locale}-desktop-light`, locale, 'news', 1280, 900, 'light');
      await inspect(`news-${locale}-mobile-dark`, locale, 'news', 393, 852, 'dark');
      await inspect(`news-${locale}-no-js`, locale, 'news', 393, 852, 'dark', true);
      await inspect(`home-${locale}-mobile-light`, locale, 'home', 393, 852, 'light');
    }
  } finally {
    await browser.close();
    writeReport(false);
  }
  process.exitCode = results.some(result => !result.ok) ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
