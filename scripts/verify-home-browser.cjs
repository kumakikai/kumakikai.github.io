// Run with Playwright installed; CHROME_PATH can select a local Chrome binary.
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');

async function main() {
  const baseURL = process.env.HOME_PREVIEW_URL || 'http://127.0.0.1:1313';
  const output = process.env.HOME_SCREENSHOT_DIR || '/private/tmp/kumakikai-home-qa';
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
  });
  const report = [];
  try {
    for (const [device, width, height] of [['desktop',1440,1000],['ipad',820,1180],['iphone',390,844]]) {
      for (const theme of ['light','dark']) {
        const context = await browser.newContext({viewport:{width,height},deviceScaleFactor:1,colorScheme:theme});
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', e => errors.push(e.message));
        page.on('response', r => { if(r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });
        await page.goto(baseURL,{waitUntil:'networkidle'});
        assert.equal(await page.locator('html').getAttribute('data-theme'),theme);
        // Load deferred screenshots in their actual document positions before capture.
        for (const screenshot of await page.locator('.app-screenshot img').all()) {
          await screenshot.scrollIntoViewIfNeeded();
          await screenshot.evaluate(img => img.decode());
        }
        await page.evaluate(() => window.scrollTo(0,0));
        await page.waitForFunction(() => window.scrollY === 0 && getComputedStyle(document.querySelector('.top-link')).visibility === 'hidden');
        await page.screenshot({path:path.join(output,`${device}-${theme}.jpg`),fullPage:true,type:'jpeg',quality:90});
        await page.screenshot({path:path.join(output,`${device}-${theme}-first-view.png`)});
        const metrics = await page.evaluate(() => ({
          viewport:window.innerWidth, documentWidth:document.documentElement.scrollWidth,
          images:[...document.querySelectorAll('.portfolio-home img')].map(i=>({src:i.currentSrc,loaded:i.complete&&i.naturalWidth>0,width:Math.round(i.getBoundingClientRect().width)})),
          overflow:[...document.querySelectorAll('.portfolio-home *, .portfolio-header *')].filter(e=>e.getBoundingClientRect().right>window.innerWidth+1).map(e=>e.className),
          resources:performance.getEntriesByType('resource').reduce((n,e)=>n+e.transferSize,0),
        }));
        assert.equal(metrics.documentWidth,width,`${device} ${theme}: horizontal overflow`);
        assert(metrics.images.every(i=>i.loaded),`${device} ${theme}: image failed`);
        assert.equal(metrics.overflow.length,0,JSON.stringify(metrics.overflow));
        assert.equal(errors.length,0,errors.join('\n'));
        await page.getByRole('button',{name:'明るい表示と暗い表示を切り替える'}).click();
        assert.equal(await page.locator('html').getAttribute('data-theme'),theme==='light'?'dark':'light');
        await page.reload();
        assert.equal(await page.locator('html').getAttribute('data-theme'),theme==='light'?'dark':'light');
        await page.locator('.portfolio-support-links summary').first().click();
        assert(await page.locator('.portfolio-support-links details').first().getAttribute('open')!==null);
        await page.locator('.portfolio-language summary').click();
        assert.equal(await page.locator('.portfolio-language a:visible').count(),6);
        report.push({device,theme,...metrics});
        await context.close();
      }
    }
    // Long translations, small phones, zoom-equivalent viewport, reduced motion and keyboard.
    for (const width of [320,375,768,1024]) {
      const page = await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
      for (const lang of ['','en/','ko/','de/','zh-hant/','fr/']) {
        await page.goto(`${baseURL}/${lang}`);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`${width} ${lang}: horizontal overflow`);
      }
      await page.goto(baseURL);
      await page.keyboard.press('Tab');
      assert.equal(await page.locator(':focus').getAttribute('class'),'portfolio-skip');
      await page.keyboard.press('Enter');
      assert.equal(await page.locator(':focus').getAttribute('id'),'main-content');
      assert.equal(await page.locator('.app-screenshot').first().evaluate(e=>getComputedStyle(e).transitionDuration),'0s');
      await page.close();
    }
    await fs.writeFile(path.join(output,'browser-report.json'),JSON.stringify({passed:true,report},null,2));
    console.log(JSON.stringify({passed:true,screenshots:output,viewports:7,themes:2,languages:6},null,2));
  } finally { await browser.close(); }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
