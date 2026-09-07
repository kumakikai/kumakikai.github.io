#!/usr/bin/env python3
"""Read-only release inventory, HTTP bytes, shared templates and cache variants."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
spec = importlib.util.spec_from_file_location('site_verifier', Path(__file__).with_name('verify-migration.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Document, route_for = module.Document, module.route_for
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--build', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--base', default='https://kumakikai.github.io')
args = parser.parse_args()
base=args.base.rstrip('/')
HEADERS = ['date','cache-control','age','etag','last-modified','vary','x-cache','x-cache-hits','x-served-by','content-type','server']
OLD = ['iPad専用','日本のApp Storeで提供中','サポートを見る','Uni:Noteは、自分が欲しい','すわなびは、喫煙している友人']
def digest(data): return hashlib.sha256(data).hexdigest()
def analyze(data):
    doc=Document(data.decode('utf-8'))
    if doc.redirect():return {'kind':'compatibility-redirect','destination':doc.redirect()}
    headers=[n for n in doc.tagged('header') if n.has_class('site-header')]
    footers=[n for n in doc.tagged('footer') if n.has_class('site-footer')]
    navs=[n for h in headers for n in h.descendants('nav') if n.has_class('desktop-nav')]
    nav=[a.text().strip() for n in navs for a in n.descendants('a')]
    footer=[a.text().strip() for f in footers for n in f.descendants('nav') for a in n.descendants('a')]
    flat=re.sub(r'\s+','',doc.root.text())
    return {'kind':'current-content','headerCount':len(headers),'footerCount':len(footers),'nav':nav,'footerLinks':footer,
            'oldStrings':[text for text in OLD if re.sub(r'\s+','',text) in flat],
            'oldStoreCTA':[n.attrs.get('href') for n in doc.tagged('a') if 'AppStoreで見る' in re.sub(r'\s+','',n.text())],
            # post-content is intentionally retained on the current shared article
            # body for compatibility. It is not by itself an old-theme fingerprint.
            'paperModMarkers':[name for name in ['post-single','post-entry','first-entry'] if any(n.has_class(name) for n in doc.nodes)],
            'canonical':doc.canonical(),
            'styles':[n.attrs.get('href') for n in doc.tagged('link') if n.attrs.get('rel')=='stylesheet']}
def fetch(route, expected, headers=None, inspect=False):
    url=base+route
    result={'route':route,'expectedSHA256':digest(expected)}
    try:
        request=Request(url,headers={'User-Agent':'KUMAKIKAI-Release-Audit/1.0',**(headers or {})})
        with urlopen(request,timeout=30) as response:
            data=response.read(); result.update(status=response.status,finalURL=response.url,actualSHA256=digest(data),headers={h:response.headers.get(h) for h in HEADERS if response.headers.get(h)})
            result['ok']=response.status==200 and data==expected
            if inspect:result['page']=analyze(data)
    except Exception as error:result.update(ok=False,error=str(error))
    return result
files=sorted(f for f in args.build.rglob('*') if f.is_file() and not any(p.startswith('.') for p in f.relative_to(args.build).parts))
html=[f for f in files if f.suffix=='.html']
assets=[f for f in files if f.suffix!='.html']
def inspect_file(file):
    route=route_for(file.relative_to(args.build)) if file.suffix=='.html' else '/'+file.relative_to(args.build).as_posix()
    return fetch(route,file.read_bytes(),inspect=file.suffix=='.html')
with ThreadPoolExecutor(max_workers=8) as pool:
    pages=list(pool.map(inspect_file,html))
    resources=list(pool.map(inspect_file,assets))
cache=[]
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
for path in ['/products/uni-note/','/company/','/news/']:
    expected=(args.build/path.lstrip('/')/'index.html').read_bytes()
    variants=[('default',path,{}),('revalidate',path,{'Cache-Control':'no-cache','Pragma':'no-cache'}),
              ('unique-query',path+'?release-audit='+stamp,{}),('explicit-index',path+'index.html',{}),
              ('mobile-UA',path,{'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'}),
              ('crawler-UA',path,{'User-Agent':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})]
    for label,url,headers in variants:cache.append({'variant':label,'pageRoute':path,**fetch(url,expected,headers,True)})
normal=[r for r in pages if r.get('page',{}).get('kind')=='current-content']
issues=[]
for row in normal:
    p=row['page']
    if p['headerCount']!=1 or p['footerCount']!=1 or p['nav']!=['Products','News','About'] or p['footerLinks']!=['Contact'] or p['paperModMarkers']:
        issues.append({'route':row['route'],'issue':'mixed-shell','page':p})
    if p['oldStrings'] or p['oldStoreCTA']:issues.append({'route':row['route'],'issue':'old-public-copy','page':p})
report={'checkedAt':datetime.now(timezone.utc).isoformat(),'base':base,'build':str(args.build),
        'ok':all(r['ok'] for r in pages+resources+cache) and not issues,
        'counts':{'html':len(pages),'contentPages':len(normal),'compatibilityRedirects':len(pages)-len(normal),'assets':len(resources),'cacheVariants':len(cache),'http200':sum(r.get('status')==200 for r in pages+resources)},
        'failures':[r for r in pages+resources+cache if not r['ok']], 'contentIssues':issues,
        'method':'Every non-hidden deployed file is fetched with a normal GET and compared byte-for-byte to the supplied artifact. Every full HTML page is parsed for current shell and obsolete public strings. Known compatibility redirects are classified separately. Selected pages are additionally fetched with revalidation, unique query, explicit index and multiple user agents. This does not inspect a third-party search/extraction provider cache.',
        'pages':pages,'resources':resources,'cacheVariants':cache}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'ok':report['ok'],'counts':report['counts'],'failures':[{'route':r['route'],'error':r.get('error','HTTP/body mismatch')} for r in report['failures']],'contentIssues':[{'route':r['route'],'issue':r['issue']} for r in issues]},ensure_ascii=False,indent=2))
sys.exit(0 if report['ok'] else 1)
