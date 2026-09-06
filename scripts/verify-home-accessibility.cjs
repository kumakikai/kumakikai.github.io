const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');

(async()=>{
  const browser = await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  const base = process.env.HOME_PREVIEW_URL || 'http://127.0.0.1:1313';
  const output = process.env.HOME_SCREENSHOT_DIR || '/private/tmp/kumakikai-home-qa';
  const reports=[];
  try {
    for(const lang of ['','en/','ko/','de/','zh-hant/','fr/']) {
      for(const theme of ['light','dark']) {
        const page=await browser.newPage({viewport:{width:390,height:844},colorScheme:theme});
        await page.goto(`${base}/${lang}`,{waitUntil:'networkidle'});
        await page.addScriptTag({path:require.resolve('axe-core/axe.min.js')});
        // Expanded panels are also part of the accessible experience.
        await page.locator('.portfolio-support-links summary').first().click();
        const result=await page.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}}));
        const violations=result.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}));
        reports.push({language:lang||'ja',theme,violations});
        await page.close();
      }
    }
    for (const theme of ['light','dark']) {
      const page=await browser.newPage({viewport:{width:390,height:844},colorScheme:theme,javaScriptEnabled:false});
      await page.goto(base,{waitUntil:'networkidle'});
      assert.equal(await page.locator('html').getAttribute('data-theme'),'auto');
      assert.equal(await page.locator('#theme-toggle').evaluate(e=>getComputedStyle(e).display),'none');
      const background=await page.locator('.app-showcase--uni-note').evaluate(e=>getComputedStyle(e).backgroundColor);
      assert.equal(background,theme==='dark'?'rgb(43, 41, 37)':'rgb(246, 243, 237)');
      await page.locator('.portfolio-language summary').click();
      assert.equal(await page.locator('.portfolio-language a:visible').count(),6);
      await page.screenshot({path:path.join(output,`iphone-${theme}-nojs.png`)});
      await page.close();
    }
    const violations=reports.flatMap(r=>r.violations);
    await fs.writeFile(path.join(output,'accessibility-report.json'),JSON.stringify({passed:violations.length===0,noJS:true,reports},null,2));
    assert.equal(violations.length,0,JSON.stringify(violations,null,2));
    console.log(JSON.stringify({passed:true,axeRuns:reports.length,violations:0,noJS:'light/dark passed'}));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
