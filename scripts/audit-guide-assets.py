#!/usr/bin/env python3
"""Inventory the real guide image assets and generated responsive files.

Provenance/current-UI review is recorded by the app audits. This inventory
checks only references, optimized output and source reuse, without editing it.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shlex
import sys

root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('migration', root / 'scripts/verify-migration.py')
m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pages = []
source_assets = {}
generated = {}
errors = []
for source in sorted((root/'content/htu').glob('*.md')):
    if source.name.startswith('_'):
        continue
    app, *lang = source.stem.split('.')
    lang = lang[0] if lang else 'ja'
    route = ('' if lang=='ja' else '/'+lang)+'/htu/'+app+'/'
    shots=[]
    for attrs in re.findall(r'{{<\s*guide-image\b(.*?)>}}',source.read_text(),re.S):
        params = dict(piece.split('=',1) for piece in shlex.split(attrs))
        file = root/'assets'/params['src']
        if not file.is_file():
            errors.append(f'Missing source {file}');continue
        key=str(file.relative_to(root))
        source_assets[key]={'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
        shots.append({'source':key,'mode':params.get('mode','crop'),'alt':params.get('alt'),'caption':params.get('caption')})
    page=root/'public'/route.strip('/')/'index.html'
    doc=m.Document(page.read_text())
    for figure in doc.tagged('figure'):
        if not (figure.has_class('guide-figure') or figure.has_class('watch-guide-figure')):
            continue
        for img in figure.descendants('img'):
            for token in img.attrs.get('srcset','').split(','):
                url=token.strip().split()[0]
                output=root/'public'/url.lstrip('/')
                if not output.is_file():errors.append(f'Missing generated {url}');continue
                generated[url]={'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    pages.append({'source':str(source.relative_to(root)),'route':route,'app':app,'locale':lang,'images':shots,'watchGuide':'{{< watch-guide' in source.read_text()})
unused=[str(p.relative_to(root)) for p in (root/'assets/images/guides').rglob('*') if p.is_file() and str(p.relative_to(root)) not in source_assets]
if unused:errors.append('Unreferenced guide source assets: '+', '.join(unused))
result={'ok':not errors,'guidePages':len(pages),'apps':sorted({p['app'] for p in pages}),'sourceImages':len(source_assets),'renderedUses':sum(len(p['images']) for p in pages),'modes':dict(Counter(i['mode'] for p in pages for i in p['images'])),'sourceBytes':sum(x['bytes'] for x in source_assets.values()),'generatedVariants':len(generated),'generatedBytes':sum(x['bytes'] for x in generated.values()),'errors':errors,'pages':pages,'sourceAssets':source_assets,'generatedAssets':generated}
output=root/'docs/visual-guides/asset-inventory.json'
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'pages','sourceAssets','generatedAssets'}},ensure_ascii=False,indent=2))
sys.exit(0 if result['ok'] else 1)
