#!/usr/bin/env node
// Read-only release audit against the published site, using production routes.
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const base=process.env.TEST_BASE_URL||'https://kumakikai.github.io';
const out='docs/release-audit';
const run=process.env.AUDIT_RUN||'before';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const apps=read('data/apps.json');
const locales=['ja','en','de','fr','ko','zh-hant'];
const home=Object.fromEntries(locales.map(l=>[l,read(`data/home/${l}.json`)]));
const company=Object.fromEntries(locales.map(l=>[l,read(`data/company/${l}.json`)]));
const badges=read('data/app-store-badges.json');
const normalize=s=>s.replace(/[\s\u200b]/gu,'');
function files(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name)):[path.join(dir,e.name)]);}
const all=files('public').filter(f=>f.endsWith('.html')).map(file=>{
  const html=fs.readFileSync(file,'utf8');
  const route='/'+file.slice(7).replace(/index\.html$/,'');
  const parts=route.split('/').filter(Boolean);
  const locale=locales.slice(1).includes(parts[0])?parts.shift():'ja';
  return {route,locale,section:parts[0]||'home',id:parts[1],alias:/<meta[^>]+http-equiv=["']?refresh/i.test(html)};
});
const routes=all.filter(p=>!p.alias);
const cases=routes.flatMap(p=>[1440,...(['products','company'].includes(p.section)&&(p.section==='company'||p.id)?[390]:[])].map(width=>({...p,width})));
const selected=process.env.AUDIT_ROUTES?cases.filter(p=>process.env.AUDIT_ROUTES.split(',').includes(p.route)):cases;
fs.mkdirSync(`${out}/screenshots`,{recursive:true});
const results=[];
function save(pending,fatal){fs.writeFileSync(`${out}/browser-${run}.json`,JSON.stringify({checkedAt:new Date().toISOString(),base,engine:'Chrome',method:'Live navigation and computed browser state. All ordinary published HTML routes are discovered from the production build. Redirect compatibility documents are audited separately by HTTP. Mobile uses viewport emulation, not a physical device. Each image is decoded after eager loading.',pending,fatal,ok:!pending&&!fatal&&results.every(r=>r.ok),discovered:{html:all.length,ordinary:routes.length,aliases:all.filter(p=>p.alias).length},cases:results.length,failures:results.filter(r=>!r.ok),results},null,2)+'\n');}
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
  let next=0;
  async function worker(){
    const ctx=await browser.newContext({viewport:{width:1440,height:1000},colorScheme:'light'});
    const page=await ctx.newPage();
    while(next<selected.length){
      const p=selected[next++],r={...p,errors:[],requestFailures:[],httpFailures:[],consoleErrors:[]};
      const fail=req=>r.requestFailures.push({url:req.url(),error:req.failure()?.errorText});
      const response=res=>{if(res.status()>=400)r.httpFailures.push({url:res.url(),status:res.status()});};
      const err=e=>r.consoleErrors.push(e.message);
      page.on('requestfailed',fail);page.on('response',response);page.on('pageerror',err);
      try{
        await page.setViewportSize({width:p.width,height:1000});
        const res=await page.goto(base+p.route,{waitUntil:'load',timeout:45000});
        r.status=res.status();if(r.status!==200)r.errors.push(`HTTP ${r.status}`);
        await page.evaluate(async()=>{
          const images=[...document.images];for(const i of images)i.loading='eager';
          await Promise.race([Promise.all(images.map(i=>i.decode().catch(()=>{}))),new Promise(resolve=>setTimeout(resolve,15000))]);
        });
        r.render=await page.evaluate(()=>{
          const text=n=>n?.textContent.trim()||'';
          const links=s=>[...document.querySelectorAll(s)].map(a=>({text:text(a),href:a.getAttribute('href')}));
          const visible=n=>n.getClientRects().length>0&&getComputedStyle(n).visibility!=='hidden'&&getComputedStyle(n).display!=='none';
          const body=document.body.innerText;
          return {
            headerCount:document.querySelectorAll('.site-header').length,
            nav:links('.desktop-nav a'),mobileNav:links('#mobile-menu nav a'),footer:links('.site-footer nav a'),
            footerCount:document.querySelectorAll('.site-footer').length,
            legacyTemplates:[...document.querySelectorAll('#menu,.post-header,.post-entry,.first-entry')].map(n=>n.className||n.id),
            unwantedHubs:links('.site-header .desktop-nav a,#mobile-menu nav a,.site-footer a,.product-page a,.portfolio-home a').filter(a=>/^\/(?:en\/|de\/|fr\/|ko\/|zh-hant\/)?(?:support|privacy)\/(?:#.*)?$/.test(a.href)),
            brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>({src:i.currentSrc||i.src,alt:i.alt})),
            imageCount:document.images.length,overflow:document.documentElement.scrollWidth>innerWidth,
            productCount:document.querySelectorAll('.product-page').length,
            hero:{name:text(document.querySelector('.product-copy h1')),platform:text(document.querySelector('.product-copy .app-identity p')),description:text(document.querySelector('.product-copy .app-description')),tagline:text(document.querySelector('.product-copy .app-tagline')),text:text(document.querySelector('.product-copy')),links:links('.product-copy a'),badgeImages:[...document.querySelectorAll('.product-copy .app-store-badge img')].map(i=>i.getAttribute('src')),regions:[...document.querySelectorAll('.product-copy .app-availability [data-country]')].map(n=>n.dataset.country),screens:[...document.querySelectorAll('.product-intro .app-screenshots img')].map(i=>({src:i.getAttribute('src'),alt:i.alt}))},
            supportKinds:[...document.querySelectorAll('.product-resources [data-support-kind]')].map(n=>n.dataset.supportKind),
            founder:[...document.querySelectorAll('.founder-bio>p')].map(text),founderName:text(document.querySelector('.founder-identity h3')),
            newsEmpty:[...document.querySelectorAll('.news-filter-empty')].map(n=>({text:text(n),category:n.dataset.category,hidden:n.hidden,visible:visible(n),display:getComputedStyle(n).display})),
            legacyPhrases:['iPad専用','日本のApp Storeで提供中','サポートを見る','Uni:Noteは、自分が','すわなびは、喫煙'].flatMap(phrase=>{const at=body.indexOf(phrase);return at<0?[]:[{phrase,snippet:body.slice(Math.max(0,at-50),at+phrase.length+80)}];})
          };
        });
        const v=r.render;
        const check=(truth,label)=>{if(!truth)r.errors.push(label);};
        check(v.headerCount===1&&v.footerCount===1,'Current shared header/footer missing or duplicated');
        check(JSON.stringify(v.nav.map(x=>x.text))===JSON.stringify(['Products','News','About']),'Desktop nav differs');
        check(JSON.stringify(v.mobileNav.map(x=>x.text.replace(/\s*→$/,'')))===JSON.stringify(['Products','News','About']),'Mobile nav differs');
        check(v.footer.length===1&&v.footer[0].text==='Contact'&&v.footer[0].href.endsWith('/company/#contact'),'Footer differs');
        check(!v.legacyTemplates.length,'Legacy template signatures');check(!v.unwantedHubs.length,'Obsolete support/privacy hub links');
        check(!v.brokenImages.length,'Broken/incomplete images');check(!v.overflow,'Viewport overflow');
        if(p.section==='products'&&p.id){
          const app=apps.find(a=>a.id===p.id),expected=home[p.locale].apps[p.id];
          check(v.productCount===1,'Shared Product template missing');
          check(normalize(v.hero.name)===normalize(expected.name),'Product name differs from metadata');
          check(normalize(v.hero.description)===normalize(expected.description),'Product description differs from metadata');
          check(normalize(v.hero.tagline)===normalize((expected.taglineLines||[]).join('')),'Product tagline differs from metadata');
          check(v.hero.links.every(a=>a.href.startsWith('https://apps.apple.com/')),'Extra Product Hero CTA');
          check(!/iPad専用|日本のApp Storeで提供中|サポートを見る/.test(v.hero.text),'Legacy Product Hero copy');
          const published=app.status==='published';
          check(JSON.stringify(v.hero.badgeImages)===JSON.stringify(published?[badges[p.locale].path]:[]),'Official App Store badge differs');
          check(JSON.stringify(v.hero.regions)===JSON.stringify(app.availability.verifiedStorefronts),'Availability differs');
          check(JSON.stringify(v.hero.screens.map(s=>s.src))===JSON.stringify(app.screenshots.map(s=>s.small)),'Product screenshots differ');
          check(JSON.stringify(v.supportKinds)===JSON.stringify(['guide','faq','contact','privacy','terms']),'Five shared support rows differ');
        }
        if(p.section==='company'){
          check(JSON.stringify(v.founder.map(normalize))===JSON.stringify(company[p.locale].founderBio.map(normalize)),'Founder copy differs from current data');
          check(v.founderName==='Yuya Nakamura','Founder name differs');
          check(!v.founder.some(s=>/Uni:Note|すわなび|Smokeless/.test(s)),'Old Founder product anecdote');
        }
        if(p.section==='news')check(!v.newsEmpty.some(n=>n.visible),'News empty state visible with default All filter');
        if(p.width===390&&p.section==='products'&&p.id){
          await page.locator('.menu-toggle').click();
          r.mobileMenu={open:await page.locator('#mobile-menu').evaluate(n=>n.open),links:await page.locator('#mobile-menu nav a').allTextContents()};
          check(r.mobileMenu.open,'Mobile menu does not open');await page.keyboard.press('Escape');
          check(!await page.locator('#mobile-menu').evaluate(n=>n.open),'Mobile menu Escape does not close');
        }
        if(p.locale==='ja'&&['/','/products/uni-note/','/company/','/news/'].includes(p.route)){
          const label=p.route==='/'?'home':p.section==='products'?'uni-note':p.section;
          r.screenshot=`screenshots/browser-${run}-${label}-${p.width}.jpg`;
          await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`${out}/${r.screenshot}`,type:'jpeg',quality:87});
          if(p.section==='company'){
            await page.locator('#founder').scrollIntoViewIfNeeded();
            r.founderScreenshot=`screenshots/browser-${run}-founder-${p.width}.jpg`;
            await page.screenshot({path:`${out}/${r.founderScreenshot}`,type:'jpeg',quality:87});
          }
          if(p.route==='/products/uni-note/'){
            await page.locator('.site-footer').scrollIntoViewIfNeeded();
            r.footerScreenshot=`screenshots/browser-${run}-footer-${p.width}.jpg`;
            await page.screenshot({path:`${out}/${r.footerScreenshot}`,type:'jpeg',quality:87});
          }
        }
        check(!r.consoleErrors.length,'JavaScript exception');check(!r.httpFailures.length,'HTTP request failure');check(!r.requestFailures.length,'Network request failure');
      }catch(error){r.errors.push(error.message);}
      page.off('requestfailed',fail);page.off('response',response);page.off('pageerror',err);
      r.ok=!r.errors.length;results.push(r);save(true);
      if(results.length%20===0||!r.ok)console.log(`${results.length}/${selected.length} ${p.route} ${p.width} ${r.ok?'PASS':r.errors.join('; ')}`);
    }
    await ctx.close();
  }
  try{await Promise.all([worker(),worker(),worker()]);}finally{await browser.close();save(false);}
  console.log(JSON.stringify({cases:results.length,failures:results.filter(r=>!r.ok).map(r=>({route:r.route,width:r.width,errors:r.errors}))}));
  process.exitCode=results.every(r=>r.ok)?0:1;
})().catch(error=>{console.error(error);save(false,error.message);process.exitCode=1;});
