#!/usr/bin/env node
const { assertLightTheme, seedLegacyDarkPreference } = require('./assert-light-theme.cjs');
// Browser checks for shared Product / Guide / FAQ / Privacy / Terms resources.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const {chromium, webkit} = require('playwright');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const engine = process.env.TEST_ENGINE || 'chrome';
const read = path => JSON.parse(fs.readFileSync(path, 'utf8'));
const apps = read('data/apps.json');
const defaults = read('data/support.json');
const out = process.env.TEST_OUTPUT_DIR || 'docs/support-consistency';
fs.mkdirSync(`${out}/screenshots`, {recursive:true});
const results = [];
const routes = ['products','htu','faq','privacy','terms'].flatMap(section => fs.readdirSync(`content/${section}`).filter(file => file.endsWith('.md')&&!file.startsWith('_')).map(file => {
  const [id, locale='ja'] = file.slice(0,-3).split('.');
  return {section,id,locale,route:`${locale==='ja'?'':'/'+locale}/${section}/${id}/`};
})).filter(p => apps.some(app => app.id===p.id));
const contactSubjects = Object.fromEntries([...new Set(routes.map(p=>p.locale))].map(locale => {
  const copy=read(`data/home/${locale}.json`),corporate=read(`data/corporate/${locale}.json`);
  return [locale,Object.fromEntries(apps.map(app=>[app.id,`${copy.apps[app.id].name} — ${corporate.contactLabel}`]))];
}));
const axe = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
function save(pending, fatal=null) {
  fs.writeFileSync(`${out}/${engine}-browser.json`, JSON.stringify({checkedAt:new Date().toISOString(),base,engine,pending,ok:!pending&&!fatal&&results.length>0&&results.every(r=>r.ok),...(fatal?{fatal}:{}),pages:routes.length,cases:results.length,failures:results.filter(r=>!r.ok),method:'Actual browser viewport rendering, shared rows and keyboard focus. Source/URL preservation is checked separately. Viewport emulation is not a physical device test.',results},null,2)+'\n');
}
function expectedURL(app, kind, locale) {
  let url = app.support[`${kind}URL`];
  if (kind==='contact') return app.support.contactURL||defaults.contactURL;
  if (kind==='terms'&&!url) return defaults.standardEULAURL;
  if (url.startsWith('/')&&locale!=='ja') {
    const [section,id] = url.split('/').filter(Boolean);
    if (fs.existsSync(`content/${section}/${id}.${locale}.md`)) return `/${locale}${url}`;
  }
  return url;
}
(async()=>{
  const probe=await fetch(base+'/products/',{signal:AbortSignal.timeout(10000)});
  assert.equal(probe.status,200,'Start a server for the production build before browser checks');
  const browser=await(engine==='webkit'?webkit:chromium).launch({headless:true,...(engine==='chrome'?{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:{})});
  try {
    for (const p of routes) for (const width of (p.locale==='ja'?[1440,768,390]:[1440,390])) for (const theme of (width===390&&p.locale==='ja'?['light','dark']:['light'])) {
      const r={...p,width,theme};
      const ctx=await browser.newContext({viewport:{width,height:1000},colorScheme:theme});
      if (theme === 'dark') await seedLegacyDarkPreference(ctx);
      const page=await ctx.newPage();
      try {
        const response=await page.goto(base+p.route,{waitUntil:'load'});assert.equal(response.status(),200);
        const legal=['privacy','terms'].includes(p.section);
        const resourcePanel=page.locator('.support-resources');assert.equal(await resourcePanel.count(),legal?0:1);
        const contact=page.locator('[data-document-contact]');assert.equal(await contact.count(),p.section==='products'?0:1);
        const panel=legal?contact:resourcePanel;
        await panel.scrollIntoViewIfNeeded();
        r.rows=await resourcePanel.locator('li').evaluateAll(nodes=>nodes.map(n=>{
          const a=n.querySelector('a'),title=a.querySelector('.resource-title'),desc=a.querySelector('.resource-description'),style=getComputedStyle(a);
          return {kind:n.dataset.supportKind,href:a.getAttribute('href'),title:title?.textContent.trim(),description:desc?.textContent.trim(),target:a.getAttribute('target'),rel:a.getAttribute('rel'),note:a.querySelector('.sr-only')?.textContent,arrow:a.querySelector('[aria-hidden]')?.textContent.trim(),height:a.getBoundingClientRect().height,style:[style.display,style.fontSize,style.borderBottomStyle,style.borderBottomWidth,style.paddingTop,style.paddingBottom],titleSize:getComputedStyle(title).fontSize,descriptionSize:desc&&getComputedStyle(desc).fontSize};
        }));
        const currentKind=p.section==='htu'?'guide':p.section;
        const kinds=legal?[]:['guide','faq','contact','privacy','terms'].filter(k=>k!==currentKind&&(p.section==='products'||k!=='contact'));
        assert.deepEqual(r.rows.map(row=>row.kind),kinds);
        const app=apps.find(a=>a.id===p.id);
        if(p.section!=='products'){
          const contactLinks=await contact.locator('a').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href')));
          const expected=expectedURL(app,'contact',p.locale);
          if(expected.startsWith('mailto:')){
            assert.equal(contactLinks.length,1);
            const url=new URL(contactLinks[0]);assert.equal(url.href.split('?')[0],expected);
            assert.equal(url.searchParams.get('subject'),contactSubjects[p.locale][p.id]);
          }else{
            assert.equal(contactLinks.length,2);assert.equal(contactLinks[0],expected);
            assert(contactLinks[1].startsWith('mailto:kumakikai.apps@gmail.com?subject='));
          }
          const bodyLinks=await page.locator('[data-content-body] a[href]').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href')));
          for(const url of contactLinks)assert.equal(bodyLinks.filter(h=>h===url).length,1,'Contact appears once in body');
          r.contact=contactLinks;
        }
        for (const row of r.rows) {
          const expected=expectedURL(app,row.kind,p.locale);
          if(row.kind==='contact'&&expected.startsWith('mailto:')&&!expected.includes('?')){
            const actual=new URL(row.href);
            assert.equal(actual.href.split('?')[0],expected,'Direct contact destination');
            assert.deepEqual([...actual.searchParams.entries()],[['subject',contactSubjects[p.locale][p.id]]],'Localized contact subject');
          }else{
            assert.equal(row.href,expected,'Direct metadata destination');
          }
          assert(row.title&&row.description&&row.arrow&&row.height>=44);
          assert.deepEqual(row.style,r.rows[0].style,'Terms has the same row design');
          assert.equal(row.titleSize,r.rows[0].titleSize);assert.equal(row.descriptionSize,r.rows[0].descriptionSize);
          assert.equal(row.target,null,'Consistent same-tab external links');
          if (row.href===defaults.standardEULAURL) assert(row.rel==='external'&&row.note&&row.arrow==='↗');
        }
        r.layout=await page.evaluate(()=>({width:document.documentElement.scrollWidth,dark:document.documentElement.classList.contains('dark'),oldUI:document.querySelectorAll('.related-resource,.resource-terms').length,articleLinks:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>/\/(notes|news)\/[^#/?]+\//.test(h))}));
        r.lightTheme=await assertLightTheme(page);assert(r.layout.width<=width);assert.equal(r.layout.dark,false);assert.equal(r.layout.oldUI,0);assert.deepEqual(r.layout.articleLinks,[]);
        if(['privacy','terms'].includes(p.section)){
          // Legal pages finish with contact; Product retains the five destinations.
          r.genericRelatedLabels=await page.locator('[data-content-body] p, [data-content-body] h2, [data-content-body] h3, [data-content-body] h4').evaluateAll(nodes=>nodes.map(n=>n.textContent.trim()).filter(text=>/^(?:関連ページ|Related pages|관련 페이지|関連頁面|相關頁面|Verwandte Seiten|Pages connexes)\s*[:：]?$/i.test(text)));
          assert.deepEqual(r.genericRelatedLabels,[],'Legal pages must not repeat generic Related Pages lists');
        }
        const links=panel.locator('a');
        for (const link of [links.first(),links.last()]) {
          await page.keyboard.press('Tab');await link.focus();
          assert(await link.evaluate(n=>document.activeElement===n&&getComputedStyle(n).outlineStyle!=='none'&&parseFloat(getComputedStyle(n).outlineWidth)>0),'Visible keyboard focus');
        }
        if(p.locale==='ja'&&width===1440){
          await page.addScriptTag({content:axe});
          r.accessibility=await page.evaluate(async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})).violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})));
          assert.deepEqual(r.accessibility,[]);
        }
        if(p.locale==='ja'&&[1440,390].includes(width)&&['uni-note','giga-poke'].includes(p.id)){
          await page.evaluate(async()=>{document.activeElement?.blur();for(const i of document.images)i.loading='eager';await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
          await panel.evaluate(n=>{const section=n.closest('section,aside')||n;scrollTo(0,section.getBoundingClientRect().top+scrollY-40);});
          r.screenshot=`screenshots/${engine}-${p.section}-${p.id}-${width}-${theme}.jpg`;
          await page.screenshot({path:`${out}/${r.screenshot}`,type:'jpeg',quality:88});
        }
        r.ok=true;
      }catch(error){r.ok=false;r.error=error.message;}
      results.push(r);if(results.length%20===0||!r.ok)console.log(`${results.length}: ${p.route} ${width} ${theme} ${r.ok?'PASS':r.error}`);
      save(true);await ctx.close();
    }
  }finally{await browser.close();save(false);}
  process.exitCode=results.every(r=>r.ok)?0:1;
})().catch(error=>{console.error(error);save(false,error.message);process.exitCode=1;});
