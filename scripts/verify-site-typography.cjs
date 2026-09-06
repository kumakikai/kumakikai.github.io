#!/usr/bin/env node
// Cross-page Japanese line geometry and browser review evidence. No source UI mutation.
const { chromium, webkit } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const phase = process.env.TEST_PHASE || 'initial';
const engine = process.env.TEST_ENGINE || 'chrome';
const widths = (process.env.TEST_WIDTHS || (phase === 'initial' ? '1024,768,390,375' : '1440,1280,1024,768,430,390,375')).split(',').map(Number);
const homeSeeds = (process.env.TEST_HOME_SEEDS || '1,2,3,6,7').split(',').map(Number);
const output = path.resolve(process.env.TEST_REPORT || `docs/watch-typography/${engine}-${phase}.json`);
const shots = path.resolve('docs/watch-typography/screenshots');
const apps = JSON.parse(fs.readFileSync(path.join(root,'data/apps.json'),'utf8'));
const ids = apps.map(a=>a.id);
const notes = fs.readdirSync(path.join(root,'content/notes')).filter(f=>/^\d.*\.md$/.test(f)).map(f=>`/notes/${f.replace(/\.md$/,'')}/`);
const routes = phase === 'initial' ? ['/', '/products/', ...ids.map(id=>`/products/${id}/`), '/company/', '/news/'] : ['/', '/products/', ...ids.map(id=>`/products/${id}/`), '/company/', '/news/', ...notes, ...['htu','faq'].flatMap(section=>ids.map(id=>`/${section}/${id}/`)), '/support/', '/privacy/', ...ids.map(id=>`/privacy/${id}/`), ...['giga-poke','nocca','oto-miru'].map(id=>`/terms/${id}/`), '/htu/', '/faq/', '/terms/', '/notes/', '/404.html'];
const results = [];
let browserVersion = null;
function save(pending) {
 fs.mkdirSync(path.dirname(output),{recursive:true});
 fs.writeFileSync(output, JSON.stringify({ checkedAt:new Date().toISOString(), base, phase, engine, browserVersion, widths, homeSeeds, pending,
 mechanicalPass:!pending&&results.every(r=>r.mechanicalPass), cases:results.length,
 method:'Real browser renders; DOM Range per-character rectangles reconstruct Japanese visual lines. Candidate word splits and short terminal lines require editorial reading; they are not automatically errors. All headings and flagged body paragraphs are recorded. Seeded Math.random changes selection only in the test context. All app IDs must appear as actual live Home Featured.',
 limitations:['Desktop browser viewport emulation, not physical iPhone/iPad. DOM word segmentation is an editorial aid, not a Japanese copy verdict. Editorial decisions and screenshots are separately reported.'],
 homeCoverage: [...new Set(results.filter(r=>r.route==='/').flatMap(r=>r.selected||[]))],
 homeCoverageByWidth: Object.fromEntries(widths.map(width=>[width,[...new Set(results.filter(r=>r.route==='/'&&r.width===width).flatMap(r=>r.selected||[]))].sort()])),
 expectedFeaturedCandidates: ids, results }, null,2)+'\n');
}
async function inspect(browser, route, width, seed=1) {
 const name=`${engine}-${route.replaceAll('/','-')||'home'}-${width}-seed${seed}`;
 if(process.env.TEST_FILTER&&!new RegExp(process.env.TEST_FILTER).test(name))return;
 const context=await browser.newContext({viewport:{width,height:1000},deviceScaleFactor:1,colorScheme:'light'});
 await context.addInitScript(({seed})=> {let state=seed;Math.random=()=>{state=(state+0x6D2B79F5)>>>0;let x=state;x=Math.imul(x^x>>>15,x|1);x^=x+Math.imul(x^x>>>7,x|61);return((x^x>>>14)>>>0)/4294967296;};},{seed});
 const auditPerformance = process.env.TEST_PERF_AXE === '1' && engine === 'chrome' && route === '/' && [1440,390].includes(width) && seed === 1;
 if(auditPerformance)await context.addInitScript(()=>{window.__jpShifts=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.__jpShifts.push({value:e.value,startTime:e.startTime});}).observe({type:'layout-shift',buffered:true});});
 const page=await context.newPage(); const errors=[]; page.on('pageerror',e=>errors.push(e.message));
 let detail={};
 try {
 const response=await page.goto(base+route,{waitUntil:'load'}); assert.equal(response.status(),200);
 await page.evaluate(async()=>{for(const img of document.images)img.loading='eager';await Promise.all([...document.images].map(img=>img.decode().catch(()=>{})));await document.fonts.ready;});
 detail=await page.evaluate(()=>{
 const segmenter=new Intl.Segmenter('ja',{granularity:'word'});
 function visible(el){const r=el.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(el).visibility!=='hidden';}
 function lines(el){
  const walker=document.createTreeWalker(el,NodeFilter.SHOW_TEXT), units=[];
  while(walker.nextNode()){
   const node=walker.currentNode;if(!visible(node.parentElement)||node.parentElement.closest('[aria-hidden="true"]'))continue;
   let offset=0;for(const char of node.textContent){const r=document.createRange();r.setStart(node,offset);offset+=char.length;r.setEnd(node,offset);const b=r.getBoundingClientRect();if(b.width&&b.height)units.push({char,top:Math.round(b.top*2)/2,middle:(b.top+b.bottom)/2,height:b.height,left:b.left});}
  }
  const rows=[];for(const u of units){let row=rows.find(r=>Math.abs(r.middle-u.middle)<Math.min(r.height,u.height)*.6);if(!row)rows.push(row={top:u.top,middle:u.middle,height:u.height,text:''});row.text+=u.char;}
  const textLines=rows.sort((a,b)=>a.top-b.top).map(r=>r.text.trim()).filter(Boolean);
  const joined=textLines.join('');const ends=[];let n=0;textLines.slice(0,-1).forEach(line=>{n+=line.length;ends.push(n);});
  const splitWords=[...segmenter.segment(joined)].filter(w=>w.isWordLike&&/[\p{Script=Han}\p{Script=Katakana}]/u.test(w.segment)&&ends.some(i=>i>w.index&&i<w.index+w.segment.length)).map(w=>({word:w.segment, cuts:ends.filter(i=>i>w.index&&i<w.index+w.segment.length).map(i=>[joined.slice(Math.max(0,i-12),i),joined.slice(i,i+12)])}));
  const last=textLines.at(-1)||'';const tinyTail=textLines.length>1&&last.replace(/[\s。、「」・！？：]/g,'').length<=2;
  const orphanParticle=textLines.length>1&&/^[はがをにでとへのもやねよ。！？]+$/.test(last);
  const style=getComputedStyle(el);const rect=el.getBoundingClientRect();
  return {tag:el.tagName.toLowerCase(),class:el.className,text:el.textContent.trim().replace(/\s+/g,' '),lines:textLines,splitWords,tinyTail,orphanParticle,width:Math.round(rect.width),top:Math.round(rect.top),fontSize:style.fontSize,lineHeight:style.lineHeight,wordBreak:style.wordBreak,overflowWrap:style.overflowWrap,textWrap:style.textWrap};
 }
 const main=document.querySelector('main');
 const headings=[...main.querySelectorAll('h1,h2,h3,h4,h5,h6,.app-tagline')].filter(visible).map(lines);
 const bodies=[...main.querySelectorAll('p,li,dd,figcaption')].filter(el=>visible(el)&&!el.querySelector('p,li,dd,figcaption,h1,h2,h3,h4,h5,h6')&&!el.matches('.app-tagline')).map(lines);
 return {viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,
 supportsAutoPhrase:CSS.supports('word-break','auto-phrase'),selected:[...document.querySelectorAll('.portfolio-featured article[data-product-id]')].map(el=>el.dataset.productId),
 brokenImages:[...document.images].filter(img=>visible(img)&&!img.naturalWidth).map(img=>img.src),
 headings,footerText:[...document.querySelectorAll('.footer-trademarks')].filter(visible).map(lines),heroLead:bodies.find(b=>b.class.split(/\s+/).includes('hero-lead'))||null,bodyCount:bodies.length,bodyLineCount:bodies.reduce((n,b)=>n+b.lines.length,0),bodyCandidates:bodies.filter(b=>b.splitWords.length||b.tinyTail||b.orphanParticle)};
 });
 if(process.env.TEST_AUDIT_FOOTER==='1')assert.ok(detail.footerText.length&&detail.footerText.every(text=>!text.splitWords.length&&!text.tinyTail&&!text.orphanParticle),'Footer Japanese words and terminal lines remain intact');
 assert.ok(detail.scrollWidth<=width,`Overflow ${detail.scrollWidth}/${width}`);assert.deepEqual(detail.brokenImages,[]);
 if(route==='/'){assert.equal(detail.selected.length,4);assert.equal(detail.selected[0],'uni-note');assert.equal(new Set(detail.selected).size,4);
  if(process.env.TEST_REQUIRE_HERO_PHRASE==='1')assert.ok(detail.heroLead?.lines.some(line=>line.includes('企画・開発・運営')), 'The complete development activity phrase stays on one visual line');
 }
 if(auditPerformance){
  await page.waitForTimeout(80);
  detail.performance=await page.evaluate(()=>{let start=0,previous=0,windowValue=0,cls=0;for(const s of window.__jpShifts){if(s.startTime-previous>1000||s.startTime-start>5000){windowValue=0;start=s.startTime;}windowValue+=s.value;previous=s.startTime;cls=Math.max(cls,windowValue);}return{cls,shifts:window.__jpShifts};});
  assert.ok(detail.performance.cls<=.1,'Home CLS remains at or below 0.1');
  await page.addScriptTag({content:fs.readFileSync(require.resolve('axe-core/axe.min.js'),'utf8')});
  detail.axeViolations=await page.evaluate(async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})).violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})));
  assert.deepEqual(detail.axeViolations,[],'Home axe accessibility');
 }
 if(process.env.TEST_SCREENSHOTS==='1'&&[1440,390].includes(width)&&seed===1&&['/','/products/smokeless/','/products/uni-note/','/company/','/htu/smokeless/'].includes(route)){
  fs.mkdirSync(shots,{recursive:true});await page.screenshot({path:path.join(shots,`${engine}-${route==='/'?'home':route.slice(1,-1).replaceAll('/','-')}-${width}-${phase}.jpg`),fullPage:true,quality:82});
  if(route==='/'){await page.locator('.home-hero').screenshot({path:path.join(shots,`${engine}-home-hero-${width}-${phase}.jpg`),type:'jpeg',quality:88});await page.locator('.site-footer').screenshot({path:path.join(shots,`${engine}-footer-${width}-${phase}.jpg`),type:'jpeg',quality:88});}
 }
 }catch(e){errors.push(e.message);}
 results.push({name,route,width,seed,mechanicalPass:!errors.length,errors,...detail});
 if(results.length%10===0||errors.length)console.log(`${results.length} ${name} ${errors.length?'FAIL '+errors.join('; '):'OK'}`);
 save(true);await context.close();
}
(async()=>{
 const browser=await(engine==='webkit'?webkit:chromium).launch({headless:true,...(engine==='chrome'?{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:{})});
 browserVersion = browser.version();
 try{for(const width of widths){for(const route of routes)await inspect(browser,route,width);for(const seed of homeSeeds.filter(seed=>seed!==1))await inspect(browser,'/',width,seed);}}finally{await browser.close();save(false);}
 process.exitCode=results.every(r=>r.mechanicalPass)?0:1;
})().catch(e=>{console.error(e);save(false);process.exitCode=1;});
