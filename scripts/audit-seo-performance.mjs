#!/usr/bin/env node
// Browser-based lab diagnostics only; this is not field Core Web Vitals or INP.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const modules=process.env.SEO_QA_MODULES||'/private/tmp/kumakikai-home-tools/node_modules';
const {default:lighthouse}=await import(pathToFileURL(path.join(modules,'lighthouse/core/index.js')).href);
const launcher=await import(pathToFileURL(path.join(modules,'chrome-launcher/dist/index.js')).href);
const base=process.env.TEST_BASE_URL||'https://kumakikai.github.io';
const run=process.env.AUDIT_RUN||'before';
const out=`docs/seo/${run}-performance.json`;
const routes=['/','/products/uni-note/','/htu/uni-note/'];
const modes=(process.env.AUDIT_MODES||'mobile,desktop').split(',');
const results=[];
const save=pending=>fs.writeFileSync(out,JSON.stringify({capturedAt:new Date().toISOString(),base,lighthouseVersion:results[0]?.version,method:'One Lighthouse lab navigation per route and form factor. Simulated mobile/desktop throttling on local Chrome; no production-user CrUX/INP data. TBT is a lab metric, not INP. Scores vary with network and host load.',pending,results},null,2)+'\n');
fs.mkdirSync('docs/seo',{recursive:true});
for(const mode of modes){
 for(const route of routes){
  const chrome=await launcher.launch({chromePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromeFlags:['--headless=new','--no-first-run','--no-default-browser-check']});
  try{
   const r=await lighthouse(base+route,{port:chrome.port,logLevel:'error',onlyCategories:['performance','accessibility','best-practices','seo'],...(mode==='desktop'?{preset:'desktop'}:{})});
   const l=r.lhr;
   const ids=['first-contentful-paint','largest-contentful-paint','cumulative-layout-shift','total-blocking-time','speed-index','interactive','uses-responsive-images','offscreen-images','modern-image-formats','uses-optimized-images','image-delivery-insight','lcp-discovery-insight','font-display-insight','render-blocking-insight','document-latency-insight','layout-shifts','largest-contentful-paint-element','unused-javascript','unused-css-rules','document-title','meta-description','is-crawlable','robots-txt','canonical','hreflang','link-text','image-alt','structured-data','heading-order'];
   results.push({route,mode,version:l.lighthouseVersion,fetchTime:l.fetchTime,finalURL:l.finalDisplayedUrl||l.finalUrl,requestedURL:l.requestedUrl,settings:l.configSettings,scores:Object.fromEntries(Object.entries(l.categories).map(([k,v])=>[k,Math.round(v.score*100)])),audits:Object.fromEntries(ids.filter(id=>l.audits[id]).map(id=>{const a=l.audits[id];return[id,{title:a.title,score:a.score,numericValue:a.numericValue,numericUnit:a.numericUnit,displayValue:a.displayValue,description:a.description,details:a.details}]})),failedAudits:Object.values(l.audits).filter(a=>a.score!==null&&a.score<1&&a.scoreDisplayMode!=='informative').map(a=>({id:a.id,title:a.title,score:a.score,displayValue:a.displayValue})),warnings:l.runWarnings,runtimeError:l.runtimeError});
   console.log(JSON.stringify({route,mode,scores:results.at(-1).scores,LCP:l.audits['largest-contentful-paint'].numericValue,CLS:l.audits['cumulative-layout-shift'].numericValue,TBT:l.audits['total-blocking-time'].numericValue}));
  }catch(e){results.push({route,mode,error:e.message});console.error(e.message);}finally{await chrome.kill();save(true);}
 }
}
save(false);
