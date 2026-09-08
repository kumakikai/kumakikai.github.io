#!/usr/bin/env python3
"""Record this authorized document revision after reviewing source and output.

Never part of CI. The output hashes are not content evidence by themselves: the
per-product Phase 1 and Phase 3 reports must exist and be reviewed first.
"""
import argparse
import importlib.util
import json
from pathlib import Path
from urllib.parse import urlsplit
from document_review import CATALOG, DIRECTORY, PURPOSE, FAMILIES, inputs, digest, flat, body_links, check_structure

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--build', type=Path, required=True)
args = parser.parse_args()
spec = importlib.util.spec_from_file_location('migration', root / 'scripts/verify-migration.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
scope, before = inputs(root)
baseline = json.loads((root / 'docs/migration/baseline.json').read_text())
reviews = {}
product_reason = {
    'uni-note': 'Distinguish local notes, selected AI inputs, AWS/Gemini processing, purchase ledgers, Speech and Crashlytics; retain version and recording limits.',
    'uni-note-pocket': 'Preserve read-only backup import, optional iCloud refresh, original backup independence and the absence of app AI or purchases.',
    'nocca': 'Preserve AWS family communication, identifier and retention exceptions, owner/member deletion, trial and subscription distinctions.',
    'oto-miru': 'Separate on-device speech, limited temporary review after manual stop, AdMob diagnostics and Plus subscriptions; remove obsolete recognition requirements.',
    'giga-poke': 'Preserve local reward-code handling, transient mail parsing, external redemption and secret-code precautions; remove unrelated site-hosting details.',
    'smokeless': 'Preserve local smoking records, actual advertising data, two one-time purchases and the unconfirmed Watch release boundary.',
    'balance-calendar': 'Preserve local income/expense records and PIN controls, actual advertising data and three one-time purchases; do not infer cloud sync from an entitlement.',
    'signal': 'Separate local feed/learning settings from feed, thumbnail and article-site requests; distinguish learning reset from clearing all web data.',
}
watch = json.loads((root / 'data/product_details/smokeless.json').read_text())['watch']
if watch['status'] == 'published':
    product_reason['smokeless'] = 'Preserve local smoking records, actual advertising data, two one-time purchases and the published Watch support conditions.'
for route, source in sorted(scope.items()):
    doc = m.Document((args.build / route.strip('/') / 'index.html').read_text())
    if errors := check_structure(root, route, doc):
        raise SystemExit(json.dumps(errors, ensure_ascii=False, indent=2))
    app = route.strip('/').split('/')[-1]
    evidence = [DIRECTORY + '/' + FAMILIES[app] + '-phase1.md', DIRECTORY + '/' + FAMILIES[app] + '-phase3.md']
    if not all((root / x).is_file() for x in evidence):
        raise SystemExit('Missing product review evidence: ' + route)
    old = baseline['articles'].get(route)
    body = doc.body_content(); links = body_links(route, body)
    removed = sorted(set(old['links']) - set(links)) if old else []
    reason = 'User-authorized four-document unification. ' + product_reason[app]
    reason += ' Common operator, terminology, headings, dates and official contact use the shared standard.'
    if app in {'nocca', 'giga-poke'}:
        reason += ' Follow-up user decision recorded in STANDARD.md: website contact uses the official mailbox; inquiry forms remain app-only navigation. Product-specific data handling is unchanged.'
    if any(x.startswith('mailto:') for x in removed):
        reason += ' Bare email references are replaced by the same official mailbox with a localized product subject.'
    if any(urlsplit(x).netloc == 'kumakikai.github.io' for x in removed):
        reason += ' Generic document-root links move to shared Product/Guide/FAQ navigation or a meaning-matched section reference; all formal routes remain.'
    if any(urlsplit(x).netloc == 'docs.github.com' for x in removed):
        reason += ' The site-hosting privacy reference is outside this app privacy document and is removed with that unrelated explanation.'
    reviews[route] = {
        'source': source, 'sourceSHA256': digest((root / source).read_bytes()),
        'beforeSourceSHA256': before.get(route, {}).get('sourceSHA256'),
        'baselineTextSHA256': digest(old['text']) if old else None,
        'reviewedTextSHA256': digest(flat(body.text())), 'reviewedLinks': links,
        'removedLinks': removed,
        'reason': reason,
        'evidence': evidence,
    }
output = root / CATALOG
output.write_text(json.dumps({'schemaVersion': 1, 'purpose': PURPOSE, 'reviews': reviews}, ensure_ascii=False, indent=2) + '\n')
print(f'Recorded {len(reviews)} documents. Review source/body/link diffs before accepting {output.relative_to(root)}.')
