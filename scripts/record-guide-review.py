#!/usr/bin/env python3
"""Record reviewed guide/FAQ bodies after a deliberate content audit.

Not part of CI. Run only after checking the source/UI evidence in the audit
reports, then inspect the manifest diff. The immutable migration baseline is
never rewritten. verify-migration.py still enforces URLs, IDs and legal pages.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('migration', root / 'scripts/verify-migration.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
baseline = json.loads((root / 'docs/migration/baseline.json').read_text())
reviews = {}
audit_for = {app: audit for audit, apps in {
    'learning-audit.md': ['uni-note', 'uni-note-pocket'],
    'communication-codes-audit.md': ['oto-miru', 'giga-poke', 'nocca'],
    'utilities-audit.md': ['smokeless', 'balance-calendar'],
    'signal-audit.md': ['signal'],
}.items() for app in apps}
digest = lambda text: hashlib.sha256(text.encode()).hexdigest()
for route, old in baseline['articles'].items():
    parts = route.strip('/').split('/')
    lang = parts.pop(0) if parts[0] in m.LANGUAGES and parts[0] != 'ja' else 'ja'
    if len(parts) != 2 or parts[0] not in {'htu', 'faq'}:
        continue
    section, app = parts
    suffix = '' if lang == 'ja' else '.' + lang
    source = root / f'content/{section}/{app}{suffix}.md'
    audit = root / 'docs/visual-guides' / audit_for[app]
    if not audit.is_file():
        raise SystemExit(f'Missing content audit: {audit}')
    page = root / 'public' / route.strip('/') / 'index.html'
    doc = m.Document(page.read_text())
    body = doc.body_content()
    if body is None:
        raise SystemExit(f'Missing rendered content: {route}')
    links = {m.urljoin(m.SITE + route, n.attrs['href']) for n in body.descendants('a') if n.attrs.get('href')}
    reviews[route] = {
        'source': str(source.relative_to(root)),
        'sourceSHA256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'baselineTextSHA256': digest(old['text']),
        'reviewedTextSHA256': digest(m.normalized(body.text())),
        'reason': 'Replace outdated operation text with current-UI steps and real screenshots; keep FAQ focused on problems and link to operations. See ' + str(audit.relative_to(root)),
        'removedLinks': sorted(set(old['links']) - links),
    }
output = root / 'docs/visual-guides/reviewed-content.json'
output.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + '\n')
print(f'Recorded {len(reviews)} individually reviewed guide/FAQ bodies. Inspect {output.relative_to(root)} before committing.')
