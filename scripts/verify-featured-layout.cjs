#!/usr/bin/env node
// Focused rendering regression for display-order-based Home Featured layout.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const {chromium, webkit} = require('playwright');
const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:1314';
const engine = process.env.TEST_ENGINE || 'chrome';
const out = 'docs/featured-layout';
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const apps = read('data/apps.json'), copy = read('data/home/ja.json');
const byID = Object.fromEntries(apps.map(app => [app.id, app]));
const candidates = apps.filter(app => app.featured && app.id !== 'uni-note').map(app => app.id);
const results = [], coverage = Object.fromEntries(candidates.map(id => [id, new Set()]));
const visualSignatures = new Map();
const seeds = [1, 2, 3, 4, 8, 9, 11, 22];
fs.mkdirSync(`${out}/screenshots`, {recursive:true});
function save(pending, fatal) {
  fs.writeFileSync(`${out}/${engine}-browser.json`, JSON.stringify({
    checkedAt:new Date().toISOString(), base, engine, pending,
    ok:!pending&&!fatal&&results.length>0&&results.every(result=>result.ok),
    ...(fatal?{fatal}:{}), cases:results.length, failures:results.filter(result=>!result.ok),
    candidates, deterministicSideCoverage:Object.fromEntries(Object.entries(coverage).map(([id,sides])=>[id,[...sides].sort()])),
    method:'Actual browser bounding boxes after production selection, 10 unseeded reloads, deterministic seeded browser selection for each candidate on both sides, mobile source order, image/copy/CTA integrity, no-JS fallback, and initial/full-image CLS observations. No production random override is introduced.',
    limitations:['Local browser viewport emulation, not a physical-device test or field performance measurement.','Random reload variety is recorded but not used as a probabilistic assertion.','Layout-shift observation is supported by Chromium; WebKit geometry is verified without claiming a CLS measurement.'], results
  },null,2)+'\n');
}
function normalize(text) { return text.replace(/\s+/g,''); }
async function setup(context, seed) {
  await context.addInitScript(({seed})=>{
    if(Number.isInteger(seed)) {
      let state=seed;
      Math.random=()=>{state=(state+0x6D2B79F5)>>>0;let value=state;value=Math.imul(value^value>>>15,value|1);value^=value+Math.imul(value^value>>>7,value|61);return((value^value>>>14)>>>0)/4294967296;};
    }
    window.__featuredQA={shifts:[],paints:[],supported:PerformanceObserver.supportedEntryTypes.includes('layout-shift')};
    if(window.__featuredQA.supported)new PerformanceObserver(list=>{
      for(const entry of list.getEntries())if(!entry.hadRecentInput)window.__featuredQA.shifts.push({value:entry.value,start:entry.startTime});
    }).observe({type:'layout-shift',buffered:true});
    if(PerformanceObserver.supportedEntryTypes.includes('paint'))new PerformanceObserver(list=>{
      for(const entry of list.getEntries())window.__featuredQA.paints.push({name:entry.name,selected:document.querySelector('[data-product-selection="3"]')?.hasAttribute('data-selection-ready')||false});
    }).observe({type:'paint',buffered:true});
  },{seed});
}
async function performance(page) {
  return page.evaluate(()=>{
    const state=window.__featuredQA;
    if(!state||!state.supported)return null;
    let max=0,value=0,start=0,previous=0;
    for(const shift of state.shifts){if(shift.start-previous>1000||shift.start-start>5000){value=0;start=shift.start;}value+=shift.value;previous=shift.start;max=Math.max(max,value);}
    return{cls:max,shifts:state.shifts,paints:state.paints};
  });
}
async function inspect(page,{width,theme,noJS,seed}) {
  const rows=await page.locator('.portfolio-featured article[data-product-id]').evaluateAll(nodes=>nodes.map((node,index)=>{
    const copy=node.querySelector('.app-showcase-copy'),visual=node.querySelector('.app-visuals');
    const rect=element=>{const b=element.getBoundingClientRect();return{x:b.x,y:b.y,width:b.width,height:b.height,right:b.right,bottom:b.bottom};};
    const c=rect(copy),v=rect(visual);
    const screenshotNodes=[...visual.querySelectorAll('.app-screenshot')];
    return{id:node.dataset.productId,index,copy:c,visual:v,card:rect(node),position:v.y>=c.bottom?'below':v.x<c.x?'left':'right',
      children:[...node.children].map(n=>n.className),name:node.querySelector('.app-identity h3')?.textContent.trim(),
      description:node.querySelector('.app-description')?.textContent.trim(),tagline:node.querySelector('.app-tagline')?.textContent.trim(),
      note:copy.querySelector('.app-note')?.textContent.trim()||null,
      actions:[...copy.querySelectorAll('.app-actions a')].map(n=>({href:n.getAttribute('href'),badge:n.matches('.app-store-badge')})),
      regions:[...copy.querySelectorAll('.storefront-link')].map(n=>({country:n.dataset.country,href:n.getAttribute('href')})),
      screenshots:screenshotNodes.map(n=>{const img=n.querySelector('img'),style=getComputedStyle(n);return{src:img.getAttribute('src'),href:n.getAttribute('href'),alt:img.alt,width:img.width,height:img.height,rect:rect(n),naturalWidth:img.naturalWidth,loading:img.loading,style:{boxShadow:style.boxShadow,transform:style.transform,overflow:style.overflow,borderRadius:style.borderRadius,marginTop:style.marginTop}};}),
      status:copy.querySelector('.status-label')?.textContent.trim()||null,
      caption:visual.querySelector('.app-visual-caption')?.textContent.trim()||null,
      noteInside:!node.querySelector('.app-note')||copy.contains(node.querySelector('.app-note')),
      actionsInside:!node.querySelector('.app-actions')||copy.contains(node.querySelector('.app-actions')),
      regionInside:!node.querySelector('.app-availability')||copy.contains(node.querySelector('.app-availability'))};
  }));
  assert.equal(rows.length,4,'Exactly four rendered Featured sections');
  assert.equal(rows[0].id,'uni-note','Uni:Note fixed first');
  assert.equal(new Set(rows.map(r=>r.id)).size,4,'No duplicate selection');
  assert.deepEqual(rows.map(row=>row.position),width>900?['right','left','right','left']:['below','below','below','below'],'Final display index controls geometry');
  const pageLayout=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,theme:getComputedStyle(document.documentElement).colorScheme,reverseClasses:document.querySelectorAll('.app-showcase--reverse').length,groupReady:document.querySelector('[data-product-selection="3"]').hasAttribute('data-selection-ready')}));
  assert(pageLayout.scrollWidth<=width,'No horizontal overflow');
  assert.equal(pageLayout.theme,theme);assert.equal(pageLayout.reverseClasses,0,'No product-specific reverse class');
  assert.equal(pageLayout.groupReady,!noJS);
  if(noJS)assert.deepEqual(rows.map(row=>row.id),['uni-note',...candidates.slice(0,3)]);
  for(const row of rows) {
    const app=byID[row.id],text=copy.apps[row.id];
    assert(app&&app.featured,'Only current eligible products');
    assert.deepEqual(row.children,['app-showcase-copy','app-visuals'],'Reading order remains copy then visuals');
    assert.equal(row.name,text.name);assert.equal(row.description,text.description);
    const tagline=text.taglineLines?.join('')||read(`data/product_details/${row.id}.json`).locales.ja.overviewTitle;
    assert.equal(normalize(row.tagline),normalize(tagline));
    assert.equal(row.note,text.note||null,'Product-specific notice remains on the copy side');
    assert(row.noteInside&&row.actionsInside&&row.regionInside,'Notes, CTA and regions belong to the text container');
    assert.equal(row.screenshots.length,app.screenshots.length);
    for(let index=0;index<row.screenshots.length;index++) {
      const shot=row.screenshots[index],source=app.screenshots[index];
      assert.equal(shot.src,source.small);assert.equal(shot.href,source.large);assert.equal(shot.alt,text.imageAlts[index]);
      assert(shot.naturalWidth>0&&shot.width>0&&shot.height>0,'Real screenshot loaded with intrinsic space');
      assert(shot.rect.x>=row.card.x&&shot.rect.right<=row.card.right+.5,'Screenshots remain inside the section');
    }
    if(row.screenshots.length>1) {
      const[first,second]=row.screenshots;
      assert(width>600?second.rect.x>first.rect.x:second.rect.y>=first.rect.bottom,'Screenshot order remains unchanged inside visuals');
    }
    const expectedActions=app.status==='published'?[app.appStoreURL,`/products/${app.id}/`]:[`/products/${app.id}/`];
    assert.deepEqual(row.actions.map(a=>a.href),expectedActions);
    assert.equal(row.actions.filter(a=>a.badge).length,app.status==='published'?1:0);
    assert.deepEqual(row.regions,app.status==='published'?app.availability.verifiedStorefronts.map(country=>({country,href:app.availability.storefrontURLs[country]})):[]);
    if(app.status!=='published')assert(row.status===copy.development&&row.caption===copy.developmentScreenshot);
    if(Number.isInteger(seed)&&width===1440&&!noJS&&row.id!=='uni-note')coverage[row.id].add(row.position);
    const key=[row.id,width,theme].join(':');
    const signature=row.screenshots.map(s=>({src:s.src,href:s.href,alt:s.alt,width:s.width,height:s.height,style:s.style}));
    if(visualSignatures.has(key))assert.deepEqual(signature,visualSignatures.get(key),'Screenshots preserve sizing, crop, overlap, shadow and order on either side');
    else visualSignatures.set(key,signature);
  }
  const bounds=rows.map(row=>({id:row.id,copy:[row.copy.x,row.copy.y,row.copy.width,row.copy.height].map(Math.round),visual:[row.visual.x,row.visual.y,row.visual.width,row.visual.height].map(Math.round)}));
  return {selected:rows.map(r=>r.id),positions:rows.map(r=>r.position),bounds,pageLayout,
    integrity:{imageSourceOrderSizingAndStyles:true,approvedCopy:true,ctaAndRegions:true,noticesOnCopySide:true,mobileSourceOrder:true}};
}
async function checkPage(page,options) {
  const initial=await performance(page);
  await page.evaluate(async()=>{for(const img of document.images)img.loading='eager';await Promise.all([...document.images].map(img=>img.decode().catch(()=>{})));});
  await page.waitForTimeout(60);
  const data=await inspect(page,options);
  const afterImages=await performance(page);
  if(initial)assert(initial.cls<=.1,'Initial CLS <= 0.1');
  if(afterImages)assert(afterImages.cls<=.1,'Full-image CLS <= 0.1');
  return {...data,initial,afterImages};
}
async function record(name,task) {
  try{results.push({name,ok:true,...await task()});console.log(`PASS ${name}`);}
  catch(error){results.push({name,ok:false,error:error.message});console.log(`FAIL ${name}: ${error.message}`);}
  save(true);
}
(async()=>{
  assert.equal((await fetch(base,{signal:AbortSignal.timeout(10000)})).status,200,'Start a production build server before the checks');
  const browser=await(engine==='webkit'?webkit:chromium).launch({headless:true,...(engine==='chrome'?{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'}:{})});
  async function sample({name,width=1440,theme='light',seed=1,noJS=false,screenshot=false}) {
    const ctx=await browser.newContext({viewport:{width,height:1000},colorScheme:theme,javaScriptEnabled:!noJS});
    const errors=[];
    try{
      if(!noJS)await setup(ctx,seed);
      const page=await ctx.newPage();page.on('pageerror',error=>errors.push(error.message));page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
      assert.equal((await page.goto(base,{waitUntil:'networkidle'})).status(),200);
      const data=await checkPage(page,{width,theme,seed,noJS});assert.deepEqual(errors,[]);
      if(screenshot){
        await page.evaluate(()=>scrollTo(0,0));
        data.screenshot=`screenshots/${engine}-${name}.jpg`;
        await page.locator('.portfolio-featured').screenshot({path:`${out}/${data.screenshot}`,type:'jpeg',quality:86});
      }
      return{width,theme,seed,noJS,...data};
    }finally{await ctx.close();}
  }
  try{
    if(engine==='chrome')await record('10-unseeded-reloads',async()=>{
      const ctx=await browser.newContext({viewport:{width:1440,height:1000}}),choices=[];
      try{
        await setup(ctx);const page=await ctx.newPage();
        await page.goto(base,{waitUntil:'networkidle'});
        for(let index=0;index<10;index++){
          await page.reload({waitUntil:'networkidle'});
          const checked=await checkPage(page,{width:1440,theme:'light',noJS:false});
          choices.push({selected:checked.selected,positions:checked.positions,initialCLS:checked.initial?.cls,fullImageCLS:checked.afterImages?.cls});
        }
        return{reloads:10,choices,distinctOrders:new Set(choices.map(c=>c.selected.join(','))).size};
      }finally{await ctx.close();}
    });
    for(const seed of seeds)await record(`seed-${seed}-desktop-both-side-coverage`,()=>sample({name:`seed-${seed}-desktop`,seed,screenshot:seed===1||seed===11}));
    await record('every-candidate-left-and-right',async()=>{
      for(const id of candidates)assert.deepEqual([...coverage[id]].sort(),['left','right'],`${id} occupies both left and right in seeded rendered cases`);
      return{coverage:Object.fromEntries(Object.entries(coverage).map(([id,sides])=>[id,[...sides]]))};
    });
    for(const width of [1280,1024,901,900,834,768,430,390,375])for(const theme of ['light','dark'])await record(`viewport-${width}-${theme}`,()=>sample({name:`${width}-${theme}`,width,theme,seed:width===390?11:1,screenshot:[1024,390].includes(width)}));
    await record('desktop-dark',()=>sample({name:'desktop-dark',theme:'dark',seed:1,screenshot:true}));
    for(const width of [1440,390])for(const theme of ['light','dark'])await record(`no-js-${width}-${theme}`,()=>sample({name:`no-js-${width}-${theme}`,width,theme,noJS:true}));
  }finally{await browser.close();save(false);}
  console.log(JSON.stringify({ok:results.every(r=>r.ok),cases:results.length,failures:results.filter(r=>!r.ok).map(r=>r.name)}));
  process.exitCode=results.every(r=>r.ok)?0:1;
})().catch(error=>{console.error(error);save(false,error.stack);process.exitCode=1;});
