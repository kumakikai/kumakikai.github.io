#!/usr/bin/env python3
"""Validate the scoped Japanese Uni:Note guide and its unpublished image slots.

No network, app launch, screenshot generation, or baseline rewriting.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'docs/uni-note-guide-phase2'
SITE = 'https://kumakikai.github.io'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(build):
    spec = importlib.util.spec_from_file_location('migration', ROOT / 'scripts/verify-migration.py')
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    plan = json.loads((DIRECTORY / 'plan.json').read_text())
    mapping = json.loads((DIRECTORY / 'implementation-map.json').read_text())
    slots = json.loads((ROOT / 'data/uni_guide_images.json').read_text())
    navigation = json.loads((ROOT / 'data/uni_guide_navigation.json').read_text())
    errors = []
    def require(condition, detail):
        if not condition:
            errors.append(detail)
    original_ids = {o['id'] for o in plan['operations']}
    ids = [i for p in mapping['pages'] for i in p['operations']]
    require(len(ids) == len(set(ids)) == 196 and set(ids) == original_ids, '196 primary operation assignments must be exact')
    require(slots == mapping['slots'], 'Image data differs from the implementation map')
    require(len(navigation['categories']) == 16, 'Expected 16 categories')
    require({p['key'] for p in navigation['pages']} == {p['key'] for p in mapping['pages']}, 'Navigation/article mismatch')
    masters = {m['id']: m for m in mapping['masters']}
    routes = {'/htu/uni-note/': 'content/htu/uni-note.md'}
    routes.update({p['url'].split('#')[0]: p['source'] for p in mapping['pages']})
    routes.update({'/htu/uni-note/' + c + '/': 'content/uni-note-guide/' + c + '.md' for c in mapping['categories']})
    require(len(routes) == 29, 'Expected top + 16 categories + 12 recipes')
    documents = {}
    used_slots = []
    internal_references = 0
    public_images = []
    for route, source_name in routes.items():
        source = ROOT / source_name
        target = build / route.strip('/') / 'index.html'
        require(source.is_file() and target.is_file(), 'Missing source/output: ' + route)
        if not source.is_file() or not target.is_file():
            continue
        text = source.read_text()
        used_slots += re.findall(r'uni-guide-image slot="([^"]+)"', text)
        sections = [p for p in mapping['pages'] if p['url'].split('#')[0] == route]
        if sections:
            match = re.search(r'^operation_ids: (.+)$', text, re.M)
            expected = [i for p in sections for i in p['operations']]
            require(match is not None and json.loads(match[1]) == expected, 'Operation IDs differ in source: ' + route)
            for section in sections:
                fragment = section.get('anchor')
                section_text = text
                if fragment:
                    require('{#' + fragment + '}' in text, 'Missing section: ' + section['url'])
                    marker = re.search(r'^## .+ \{#' + re.escape(fragment) + r'\}\n', text, re.M)
                    section_text = re.split(r'\n## ', text[marker.end():], maxsplit=1)[0] if marker else ''
                require('## 完了の確認' in section_text and '## 関連する使い方' in section_text, 'Section structure missing: ' + section['url'])
                require('## ' in section_text.split('## 完了の確認')[0], 'Missing instructions: ' + section['url'])
        html = target.read_text()
        doc = migration.Document(html)
        documents[route] = doc
        body = doc.body_content()
        require(body is not None, 'Missing content wrapper: ' + route)
        if body is None:
            continue
        visible = body.text()
        require(not re.search(r'指描画|指で描画|指で書き|CoreHandwriting|Premium Plus|SHOT-|CAP-\d|[NMSR]-M\d|画像準備中|3\.4\.0|公開前情報', visible), 'Unreleased/internal/old-version text: ' + route)
        require(not re.search(r'ノートの向きは作成後に変更でき|写真・PDF・付箋は個別に動か', visible), 'HOLD assertion reintroduced: ' + route)
        require(not re.search(r'学習支援.{0,12}暗記マーカー.{0,8}オン|設定でオンにしてから', visible), 'Old activation route: ' + route)
        require(not re.search(r'(?<![A-Za-z])(?:top|[a-z]+-[a-z]+)--[nmsr]-m\d+', html), 'Slot ID leaked in HTML: ' + route)
        require(not [k for k,v in Counter(doc.ids).items() if v > 1], 'Duplicate HTML ID: ' + route)
        public_images += [n.attrs for n in body.descendants('img')]
        for node in doc.nodes:
            for attr in ('href','src','poster'):
                if not (value := node.attrs.get(attr)):
                    continue
                url = urlsplit(urljoin(SITE + route, value))
                if url.scheme not in ('https','http') or url.netloc != 'kumakikai.github.io':
                    continue
                path = build / unquote(url.path).lstrip('/')
                if url.path.endswith('/'):
                    path /= 'index.html'
                require(path.is_file(), 'Broken internal link: ' + route + ' -> ' + value)
                internal_references += 1
                if url.fragment and path.is_file() and path.suffix == '.html':
                    linked = migration.Document(path.read_text())
                    require(unquote(url.fragment) in linked.ids, 'Broken fragment: ' + route + ' -> ' + value)
    require(len(used_slots) == len(set(used_slots)) and set(used_slots) == set(slots), 'Slots must each appear once in source')
    for sid, slot in slots.items():
        require(slot['master'] in masters, 'Unknown master: ' + sid)
        m = masters.get(slot['master'], {})
        require(slot['session'] == m.get('session_id') and slot['shot_ids'] == m.get('shot_ids'), 'Phase 1.5 references changed: ' + sid)
        require(slot['status'] in ('pending','approved','legacy-approved'), 'Unapproved image status: ' + sid)
        if slot['status'] == 'pending':
            require(not slot.get('src'), 'Pending image has public source: ' + sid)
        else:
            path = ROOT / 'assets' / slot['src']
            require(path.is_file() and digest(path) == slot['source_sha256'], 'Approved screenshot altered: ' + sid)
            require(bool(slot.get('alt')) and bool(slot.get('caption')), 'Missing image explanation: ' + sid)
    require({s['master'] for s in slots.values()} == {m['id'] for m in masters.values() if m['importance'] == 'must'}, 'All 110 standard masters need a slot')
    approved = [s for s in slots.values() if s['status'] in ('approved','legacy-approved')]
    require(len(public_images) == len(approved), 'Pending image rendered or approved image missing')
    for image in public_images:
        require(image.get('alt') and image.get('width') and image.get('height') and image.get('srcset') and image.get('loading') == 'lazy', 'Invalid responsive image')
    top = documents.get('/htu/uni-note/')
    if top:
        require(set(plan['anchors']) <= set(top.ids), 'Legacy anchor lost')
        require({'はじめに','基本的な使い方','困ったとき','お問い合わせ'} <= set(top.ids), 'Original section anchor lost')
        require(top.canonical() == [SITE + '/htu/uni-note/'] and not top.redirect(), 'Top URL identity changed')
    workflow_pages = [p for p in mapping['pages'] if p['category'] == 'workflows']
    require(len(workflow_pages) == 12 and all(p['hero_masters'] for p in workflow_pages), '12 workflows each need hero reservations')
    preservation = json.loads((DIRECTORY / 'preservation.json').read_text())['tracked']
    for f, old_hash in preservation.items():
        if f.startswith(('assets/images/','static/images/')) or re.match(r'content/htu/uni-note\.[^.]+\.md$', f):
            require((ROOT/f).is_file() and digest(ROOT/f) == old_hash, 'Protected image/translation changed: ' + f)
    return {'ok':not errors,'pages':len(documents),'operations':len(ids),'legacy_anchors':len(plan['anchors']), 'slots':len(slots), 'pending_slots':sum(s['status']=='pending' for s in slots.values()),'standard_masters':len({s['master'] for s in slots.values()}),'reused_assets':len({s['src'] for s in approved}),'rendered_image_placements':len(public_images),'internal_references':internal_references,'errors':errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, default=ROOT/'public')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.build.resolve())
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end='')
    raise SystemExit(0 if result['ok'] else 1)
