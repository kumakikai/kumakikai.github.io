#!/usr/bin/env python3
"""Inventory a fresh Hugo output; fragments are part of destination identity.

No network. Raw link duplicates are evidence, not automatic defects: responsive
menus, language selection, article citations and section CTAs need human review.
"""
import argparse
from collections import Counter, defaultdict
import csv
from difflib import SequenceMatcher
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

sys.path.insert(0, str(Path(__file__).parent))
spec = importlib.util.spec_from_file_location('migration', Path(__file__).with_name('verify-migration.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SITE = 'https://kumakikai.github.io'
LOCALES = {'en', 'ko', 'de', 'zh-hant', 'fr'}
STATE = re.compile(r'開発中|開発しています|現在のところ|公開中|予定|審査中|審査待ち|近日(?:対応|公開|予定)?|公開前|公開準備|現在の(?:バージョン|公開版)|未公開|次回|今後|準備中|リリース予定|coming soon|under review|in review|upcoming|not released|in development|currently|current (?:version|release)|not yet|unreleased|bientôt|en cours|demnächst|derzeit|noch nicht|veröffentlicht|개발 중|심사 중|출시 예정|출시 전|출시된|검토 중|目前|即將|審核|尚未', re.I)
RELATED = re.compile(r'^(?:関連ページ|関連リンク|Related (?:pages|links)|관련 페이지|관련 링크|相關頁面|相關連結|Verwandte Seiten|Pages connexes)\s*[:：]?$', re.I)

def flat(text): return re.sub(r'\s+', ' ', text).strip()
def key(text): return re.sub(r'[\s\u200b]+', '', text).casefold()
def ancestors(node):
    while node:
        yield node
        node = node.parent
def has(node, cls): return any(n.has_class(cls) for n in ancestors(node))
def context(node):
    for cls in ('desktop-nav','mobile-menu','language-menu','site-header','site-footer','breadcrumbs','support-resources','article-related','article-about','news-filters','app-availability','app-actions','company-area-products','post-content','product-page','home-hero','portfolio-featured','home-news','home-about','company-page'):
        if has(node, cls): return cls
    return 'main' if any(n.tag == 'main' for n in ancestors(node)) else 'document'
def locator(node):
    result = []
    for n in ancestors(node):
        if n.tag == 'document': break
        item = n.tag
        if n.attrs.get('id'):
            result.append(item+'#'+n.attrs['id']); break
        if n.attrs.get('class'): item += '.'+'.'.join(n.attrs['class'].split()[:2])
        elif n.parent:
            siblings = [s for s in n.parent.parts if isinstance(s,m.Node) and s.tag == n.tag]
            if len(siblings)>1: item += ':nth-of-type('+str(siblings.index(n)+1)+')'
        result.append(item)
        if len(result)==5: break
    return ' > '.join(reversed(result))
def label(node):
    def text(n):
        if n.attrs.get('aria-hidden')=='true': return ''
        if n.tag=='img': return n.attrs.get('alt','')
        return ''.join(p if isinstance(p,str) else text(p) for p in n.parts)
    return flat(text(node))
def locale(route): return route.strip('/').split('/')[0] if route.strip('/').split('/')[0] in LOCALES else 'ja'
def destination(href, route):
    absolute=urljoin(SITE+route, href)
    p=urlsplit(absolute)
    internal=p.scheme in ('https','http') and p.netloc.lower()==urlsplit(SITE).netloc
    path=unquote(p.path)
    if internal and path.endswith('/index.html'): path=path[:-10]
    if internal and not path: path='/'
    # Keep query AND decoded fragment; /p/ and /p/#support are different.
    normalized=urlunsplit((p.scheme.lower(),p.netloc.lower(),path,p.query,unquote(p.fragment)))
    return {'url':normalized,'kind':'internal' if internal else 'external' if p.scheme in ('https','http') else p.scheme or 'other','path':path,'fragment':unquote(p.fragment),'query':p.query}
def target_file(build,path):
    f=build/path.lstrip('/')
    return f/'index.html' if path.endswith('/') or f.is_dir() else f
def dump(out,name,value): (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def audit(build,source,out):
    out.mkdir(parents=True,exist_ok=True)
    files=sorted(p for p in build.rglob('*') if p.is_file())
    html=[p for p in files if p.suffix.lower()=='.html']
    docs={m.route_for(p.relative_to(build)):m.Document(p.read_text()) for p in html}
    origins={}
    for p in (source/'content').rglob('*.md'):
        parts=p.relative_to(source/'content').parts
        base=p.stem.split('.'); lang=base[1] if len(base)>1 else 'ja'
        route='/'+'/'.join((*parts[:-1], '' if base[0]=='_index' else base[0]))+'/'
        route=re.sub('/+','/',route)
        if lang!='ja': route='/'+lang+route
        origins[route]=str(p.relative_to(source))
    inventory=[]; links=[]; refs=[]; paragraphs=[]; related=[]; bad=[]; invalid=[]; semantics=[]; duplicate_ids=[]
    for route,doc in docs.items():
        p=build/route.lstrip('/')/'index.html' if route.endswith('/') else build/route.lstrip('/')
        robots=doc.meta('robots')
        redirect=doc.redirect()
        inventory.append({'route':route,'file':str(p.relative_to(build)),'source':origins.get(route),'locale':locale(route),'title':flat(''.join(n.text() for n in doc.tagged('title'))),'canonical':doc.canonical(),'redirect':redirect,'noindex':any('noindex' in r for r in robots),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ids':doc.ids})
        for id_,count in Counter(doc.ids).items():
            if count>1: duplicate_ids.append({'page':route,'id':id_,'count':count})
        for node in doc.nodes:
            if node.tag in ('a','area') and 'href' in node.attrs:
                href=node.attrs['href'];dest=destination(href,route)
                entry={'id':len(links)+1,'page':route,'source':origins.get(route),'href':href,**dest,'label':label(node),'accessibleLabel':node.attrs.get('aria-label') or label(node),'context':context(node),'template':node.inside_template(),'locator':locator(node)}
                links.append(entry)
            attrs=[]
            if node.tag in ('a','area','link') and 'href' in node.attrs: attrs.append(('href',node.attrs['href']))
            for attr in ('src','poster','action'):
                if attr in node.attrs: attrs.append((attr,node.attrs[attr]))
            if 'srcset' in node.attrs:
                attrs += [('srcset',x.strip().split()[0]) for x in node.attrs['srcset'].split(',') if x.strip()]
            for attr,href in attrs:
                dest=destination(href,route)
                ref={'page':route,'tag':node.tag,'attribute':attr,'href':href,**dest,'template':node.inside_template(),'locator':locator(node)}
                refs.append(ref)
                if dest['kind']=='internal':
                    f=target_file(build,dest['path'])
                    if not f.is_file(): bad.append(ref)
                    elif dest['fragment'] and ':~:text=' not in dest['fragment'] and f.suffix=='.html':
                        target_route=m.route_for(f.relative_to(build)); td=docs.get(target_route)
                        if td and dest['fragment'] not in td.ids: invalid.append(ref)
            if node.tag in ('p','h2','h3','h4') and RELATED.fullmatch(flat(node.text())):
                related.append({'page':route,'text':flat(node.text()),'context':context(node),'locator':locator(node)})
            if node.tag in ('p','li','dd') and not any(n.tag in ('p','li','dd') for n in node.descendants()):
                text=flat(node.text())
                if len(key(text))>=24 and context(node) not in ('document','site-header','site-footer','mobile-menu','language-menu','desktop-nav'):
                    paragraphs.append({'id':len(paragraphs),'page':route,'locale':locale(route),'context':context(node),'template':node.inside_template(),'text':text,'locator':locator(node)})
    duplicates=[]; different=[]
    groups=defaultdict(list)
    for link in links: groups[(link['page'],link['url'])].append(link)
    for (page,url),group in groups.items():
        if len(group)<2:continue
        ctx={x['context'] for x in group}
        classification='needs-review'
        if ctx<= {'desktop-nav','mobile-menu'}: classification='responsive-alternatives'
        elif any(x['template'] for x in group): classification='includes-inert-template'
        elif ctx<= {'site-header','site-footer','language-menu'}: classification='global-brand-language-navigation'
        elif ctx<= {'post-content','support-resources'}: classification='body-reference-and-shared-support'
        elif ctx & {'site-header','site-footer','desktop-nav','mobile-menu','breadcrumbs','language-menu'}: classification='global-and-content-navigation'
        entry={'page':page,'destination':url,'count':len(group),'labels':sorted({x['label'] for x in group}),'classification':classification,'occurrences':group}
        duplicates.append(entry)
        if len({key(x['label']) for x in group})>1: different.append(entry)
    graph=defaultdict(set);inbound=defaultdict(set)
    for link in links:
        if link['kind']!='internal':continue
        f=target_file(build,link['path'])
        if not f.is_file() or f.suffix!='.html':continue
        target=m.route_for(f.relative_to(build))
        if target!=link['page']:
            graph[link['page']].add(target);inbound[target].add(link['page'])
        td=docs.get(target);fragment=link['fragment']
        if not td:continue
        node=next((n for n in td.nodes if n.attrs.get('id')==fragment),None) if fragment else None
        target_text=flat(node.text())[:180] if node else flat(''.join(n.text() for n in td.tagged('h1')))[:180]
        if node and not target_text:
            after=td.nodes[td.nodes.index(node)+1:]
            heading=next((n for n in after if n.tag in ('h1','h2','h3','h4')),None)
            target_text=flat(heading.text())[:180] if heading else ''
        semantic={'linkId':link['id'],'page':link['page'],'label':link['label'],'destination':link['url'],'fragment':fragment,'targetText':target_text,'context':link['context'],'status':'manual-context'}
        bare=key(link['label']).strip('→↗↓')
        if bare in ('support','サポート'):
            semantic['status']='match' if fragment=='support' and node is not None and has(node,'product-resources') else 'review-label-target'
        elif bare in ('contact','お問い合わせ','取材・掲載について') and '/company/' in target:
            semantic['status']='match' if fragment=='contact' and node is not None else 'review-label-target'
        elif bare in ('product','products'):
            semantic['status']='match' if '/products/' in target and not fragment else 'review-label-target'
        elif fragment:
            semantic['status']='anchor-exists-context-review' if node else 'invalid-anchor'
        semantics.append(semantic)
    reached=set();pending=['/']
    while pending:
        page=pending.pop()
        if page in reached:continue
        reached.add(page);pending.extend(graph[page]-reached)
    orphan=[]
    for row in inventory:
        if row['route'] not in reached or not inbound[row['route']]:
            kind='compatibility-alias' if row['redirect'] else 'noindex-legacy-or-utility' if row['noindex'] else 'indexable-orphan'
            if row['route']=='/':kind='root'
            orphan.append({**row,'classification':kind,'reachableFromHome':row['route'] in reached,'inboundPages':sorted(inbound[row['route']])})
    exact=defaultdict(list)
    for paragraph in paragraphs: exact[key(paragraph['text'])].append(paragraph)
    repeated=[{'text':rows[0]['text'],'occurrences':rows,'samePage':any(c>1 for c in Counter(x['page'] for x in rows).values())} for rows in exact.values() if len(rows)>1]
    unique=[rows[0] for rows in exact.values() if len(key(rows[0]['text']))>=60 and rows[0]['context'] not in ('support-resources','app-availability')]
    shingles={p['id']:{key(p['text'])[i:i+5] for i in range(max(0,len(key(p['text']))-4))} for p in unique}
    inverted=defaultdict(set)
    for p in unique:
        for s in shingles[p['id']]: inverted[(p['locale'],s)].add(p['id'])
    lookup={p['id']:p for p in unique};pairs=set();similar=[]
    for p in unique:
        candidates=set()
        rare=sorted(shingles[p['id']],key=lambda s:len(inverted[(p['locale'],s)]))[:12]
        for s in rare:candidates.update(inverted[(p['locale'],s)])
        for qid in candidates:
            if qid<=p['id']:continue
            pair=(p['id'],qid)
            if pair in pairs:continue
            pairs.add(pair);q=lookup[qid];a=key(p['text']);b=key(q['text'])
            if min(len(a),len(b))/max(len(a),len(b))<.75:continue
            shared=len(shingles[p['id']]&shingles[qid])
            if shared/max(1,min(len(shingles[p['id']]),len(shingles[qid])))<.6:continue
            ratio=SequenceMatcher(None,a,b,autojunk=False).ratio()
            if ratio>=.88:similar.append({'similarity':round(ratio,4),'first':p,'second':q})
    states=[]
    for folder in ('content','data','layouts','assets/js'):
        for p in (source/folder).rglob('*'):
            if not p.is_file() or p.suffix not in ('.md','.json','.html','.js'):continue
            for number,line in enumerate(p.read_text().splitlines(),1):
                matches=STATE.findall(line)
                if matches:states.append({'source':str(p.relative_to(source)),'line':number,'matches':matches,'text':line.strip()})
    summary={'htmlPages':len(inventory),'ordinaryPages':sum(not p['redirect'] for p in inventory),'aliases':sum(bool(p['redirect']) for p in inventory),'indexable':sum(not p['noindex'] and not p['redirect'] for p in inventory),'navigationLinkOccurrences':len(links),'internalLinkOccurrences':sum(l['kind']=='internal' for l in links),'externalHTTPLinkOccurrences':sum(l['kind']=='external' for l in links),'allReferenceOccurrences':len(refs),'distinctExternalHTTPURLs':len({urlunsplit((*urlsplit(l['url'])[:4],'')) for l in refs if l['kind']=='external'}),'duplicateDestinationGroups':len(duplicates),'differentLabelGroups':len(different),'brokenInternalReferences':len(bad),'invalidAnchorReferences':len(invalid),'duplicateIDs':len(duplicate_ids),'genericRelatedBlocks':len(related),'indexableOrphans':sum(p['classification']=='indexable-orphan' for p in orphan),'exactRepeatedParagraphGroups':len(repeated),'samePageRepeatedParagraphGroups':sum(r['samePage'] for r in repeated),'similarParagraphPairs':len(similar),'timeSensitiveSourceLines':len(states)}
    for name,value in [('summary',summary),('pages',inventory),('links',links),('references',refs),('duplicate-links',duplicates),('different-label-links',different),('broken-links',bad),('invalid-anchors',invalid),('duplicate-ids',duplicate_ids),('anchor-label-semantics',semantics),('related-blocks',related),('orphan-pages',orphan),('repeated-paragraphs',repeated),('similar-paragraphs',sorted(similar,key=lambda r:-r['similarity'])),('time-sensitive-source',states)]:dump(out,name+'.json',value)
    with (out/'links.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(links[0]) if links else []);writer.writeheader();writer.writerows(links)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary

def structural_errors(output):
    """Fail on concrete defects; never fail on raw repeated-link counts."""
    read = lambda name: json.loads((output / (name + '.json')).read_text())
    summary = read('summary')
    errors = [name for name in ('brokenInternalReferences', 'invalidAnchorReferences', 'duplicateIDs', 'genericRelatedBlocks', 'indexableOrphans') if summary[name]]
    for duplicate in read('duplicate-links'):
        contexts = {o['context'] for o in duplicate['occurrences']}
        if duplicate['destination'].startswith('mailto:') and {'article-about', 'post-content'} <= contexts:
            errors.append('Repeated shared article contact: ' + duplicate['page'])
    errors += ['Label/section mismatch: ' + row['page'] + ' → ' + row['destination'] for row in read('anchor-label-semantics') if row['status'] == 'review-label-target']
    return errors

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--check', action='store_true', help='Fail on broken targets, bad anchors/IDs, or redundant shared blocks; retain intentional repeated links')
    a=p.parse_args();audit(a.build.resolve(),a.source.resolve(),a.output.resolve())
    if a.check:
        errors = structural_errors(a.output)
        if errors:
            print(json.dumps({'structuralErrors': errors}, ensure_ascii=False, indent=2))
            raise SystemExit(1)
