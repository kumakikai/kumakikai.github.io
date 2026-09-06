#!/usr/bin/env node
// Render every existing app guide and FAQ. UI images remain static and work
// without site JavaScript; forced decoding here only makes QA deterministic.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium,webkit}=require('playwright');
const base=process.env.TEST_BASE_URL||'http://127.0.0.1:1314';
const engine=process.env.TEST_ENGINE||'chrome';
const output=process.env.TEST_REPORT||`docs/visual-guides/${engine}-browser.json`;
const shots='docs/visual-guides/screenshots';
const widths=(process.env.TEST_WIDTHS||'1440,1280,1024,768,430,390,375').split(',').map(Number);
const locales=process.env.TEST_LOCALES?.split(',');
const results=[];
const axeSource=fs.readFileSync(require.resolve('axe-core/axe.min.js'),'utf8');
const pages=['htu','faq'].flatMap(section=>fs.readdirSync(`content/${section}`).filter(f=>f.endsWith('.md')&&!f.startsWith('_')).map(file=>{
 const [app,locale='ja']=file.slice(0,-3).split('.');
 return {section,app,locale,route:(locale==='ja'?'':'/'+locale)+`/${section}/${app}/`};
})).filter(p=>(!locales||locales.includes(p.locale))&&(!process.env.TEST_APP||p.app===process.env.TEST_APP));
fs.mkdirSync(shots,{recursive:true});
function save(pending){fs.writeFileSync(output,JSON.stringify({checkedAt:new Date().toISOString(),base,engine,pending,ok:!pending&&results.every(r=>r.ok),cases:results.length,widths,pages:pages.length,method:'Actual desktop-browser viewport renders. Every guide image decoded; dimensions, alt, links, focus, TOC, overflow and accessibility checked. Japanese lines reconstructed from DOM Range for editorial review. Screenshots and human visual reading are separate from these mechanical checks.',limitations:['Viewport emulation, not physical devices. Browser rendering does not prove operation inside the app; current source and app capture evidence is in the app audit reports.'],failures:results.filter(r=>!r.ok),results},null,2)+'\n');}
async function inspect(browser,p,width,theme,noJS=false){
 const name=`${p.section}-${p.app}-${p.locale}-${width}-${theme}${noJS?'-no-js':''}`;
 const ctx=await browser.newContext({viewport:{width,height:900},deviceScaleFactor:1,colorScheme:theme,javaScriptEnabled:!noJS});
 if(!noJS&&engine==='chrome')await ctx.addInitScript(()=>{window.__guideShifts=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.__guideShifts.push({value:e.value,startTime:e.startTime});}).observe({type:'layout-shift',buffered:true});});
 const page=await ctx.newPage();page.setDefaultTimeout(15000);
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
 const result={name,...p,width,theme,noJS};
 try {
  const response=await page.goto(base+p.route,{waitUntil:'load'});assert.equal(response.status(),200);
  await page.evaluate(async()=>{for(const img of document.images)img.loading='eager';await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready;});
  result.layout=await page.evaluate(()=>{
   const body=document.querySelector('[data-content-body]');
   const figures=[...body.querySelectorAll('.guide-figure, .watch-guide-figure')];
   const visible=n=>n.getBoundingClientRect().width>0;
   function lines(el){
    const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),rows=[];
    while(w.nextNode()){
     const n=w.currentNode;if(n.parentElement.closest('[aria-hidden="true"]'))continue;
     let offset=0;for(const char of n.textContent){const r=document.createRange();r.setStart(n,offset);offset+=char.length;r.setEnd(n,offset);const box=r.getBoundingClientRect();if(!box.width)continue;const middle=(box.top+box.bottom)/2;let row=rows.find(v=>Math.abs(v.middle-middle)<box.height*.5);if(!row)rows.push(row={middle,text:''});row.text+=char;}
    }
    return rows.sort((a,b)=>a.middle-b.middle).map(r=>r.text.trim()).filter(Boolean);
   }
   const blocks=[...body.querySelectorAll('h2,h3,p,li,figcaption')].filter(n=>!n.querySelector('p,li,figcaption,h2,h3')).map(n=>({tag:n.tagName,text:n.textContent.trim(),lines:lines(n)}));
   const images=figures.map(f=>{const i=f.querySelector('img'),r=f.getBoundingClientRect();return {src:i.currentSrc,alt:i.alt,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,width:Math.round(r.width),height:Math.round(r.height),mode:f.className,explicitWidth:i.getAttribute('width'),explicitHeight:i.getAttribute('height'),srcset:i.getAttribute('srcset'),sizes:i.getAttribute('sizes'),url:f.querySelector('a').getAttribute('href')};});
   const ids=[...document.querySelectorAll('[id]')].map(n=>n.id);
   return {scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,images,brokenImages:[...document.images].filter(i=>visible(i)&&!i.naturalWidth).map(i=>i.src),duplicateIDs:ids.filter((v,i)=>ids.indexOf(v)!==i),headingCount:document.querySelectorAll('h1').length,bodyWidth:body.getBoundingClientRect().width,headings:blocks.filter(b=>/^H/.test(b.tag)),tinyTails:blocks.filter(b=>b.lines.length>1&&b.lines.at(-1).replace(/[\s。、！？]/g,'').length<=2),dark:document.documentElement.classList.contains('dark')};
  });
  assert.equal(result.layout.headingCount,1);assert.deepEqual(result.layout.duplicateIDs,[]);assert.deepEqual(result.layout.brokenImages,[]);assert(result.layout.scrollWidth<=width,'No horizontal overflow');
  // No-JS mode may use data-theme=auto plus CSS rather than a JS class.
  if(!noJS)assert.equal(result.layout.dark,theme==='dark');
  if(p.section==='htu'){
   assert(result.layout.images.length>0,'Every app guide has real UI images');
   for(const i of result.layout.images){assert(i.alt.trim()&&i.srcset&&i.sizes&&Number(i.explicitWidth)>0&&Number(i.explicitHeight)>0);assert(i.naturalWidth>0);assert(i.width<=Math.min(result.layout.bodyWidth,762));assert(i.src.includes('.webp'),'Optimized image');}
   const toc=page.locator('.guide-toc');
   if(await toc.count()){
    await toc.locator('summary').focus();await page.keyboard.press('Enter');assert(await toc.getAttribute('open')!==null,'Keyboard opens contents');
    const first=toc.locator('a').first();const anchor=await first.getAttribute('href');await first.click();assert.equal(decodeURIComponent(new URL(page.url()).hash),decodeURIComponent(anchor),'Contents jumps directly to guide section');
    await toc.locator('summary').click();
   }
   // WebKit's default macOS Tab traversal skips links. Establish keyboard
   // modality first, then focus the specific link; do not assume Shift+Tab
   // returns to it. The focused node itself must have a visible outline.
   const link=page.locator('.guide-figure a,.watch-guide-figure a').first();await page.keyboard.press('Tab');await link.focus();
   result.visibleFocus=await link.evaluate(n=>document.activeElement===n&&getComputedStyle(n).outlineStyle!=='none'&&parseFloat(getComputedStyle(n).outlineWidth)>0);assert(result.visibleFocus,'Visible image-link focus');
   const target=await link.getAttribute('href');const imageResponse=await page.request.get(new URL(target,base).href);assert.equal(imageResponse.status(),200,'Enlargement source resolves');
  }
  if(!noJS&&engine==='chrome'){result.layoutShifts=await page.evaluate(()=>window.__guideShifts||[]);assert(result.layoutShifts.reduce((v,s)=>v+s.value,0)<=.1,'No material image layout shift');}
  if(!noJS&&[390,1440].includes(width)){
   await page.addScriptTag({content:axeSource});
   result.axe=await page.evaluate(async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})).violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})));
   assert.deepEqual(result.axe,[],'No automated accessibility violations');
  }
  if(p.section==='htu'&&p.locale==='ja'&&[390,1440].includes(width)&&theme==='light'&&!noJS){
   await page.evaluate(()=>{document.activeElement?.blur();scrollTo(0,0);});await page.mouse.move(0,0);
   result.screenshot=`${engine}-${p.app}-${width}.jpg`;await page.screenshot({path:path.join(shots,result.screenshot),fullPage:true,type:'jpeg',quality:86});
   if(p.app==='uni-note'){await page.screenshot({path:path.join(shots,`${engine}-uni-note-top-${width}.jpg`),type:'jpeg',quality:90});}
  }
  assert.deepEqual(errors,[]);result.ok=true;
 }catch(e){result.ok=false;result.error=e.message;}
 results.push(result);if(results.length%10===0||!result.ok)console.log(`${results.length} ${name}: ${result.ok?'OK':result.error}`);save(true);await ctx.close();
}
(async()=>{
 const browser=await(engine==='webkit'?webkit:chromium).launch({headless:true,...(engine==='chrome'?{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:{})});
 try {
  for(const p of pages){
   const sizes=p.section==='faq'||p.locale!=='ja'?widths.filter(w=>[390,1440].includes(w)):widths;
   for(const width of sizes)for(const theme of(p.section==='htu'?['light','dark']:['light']))await inspect(browser,p,width,theme);
  }
  if(engine==='chrome')for(const p of pages.filter(p=>p.section==='htu'&&p.locale==='ja'))await inspect(browser,p,390,'light',true);
 }finally{await browser.close();save(false);}
 process.exitCode=results.every(r=>r.ok)?0:1;
})().catch(e=>{console.error(e);save(false);process.exitCode=1;});
