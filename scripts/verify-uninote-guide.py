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
SITE = 'https://kumakikai.top'


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
    additions = json.loads((ROOT / 'docs/uni-note-guide-v4/additions.json').read_text())
    release = json.loads((ROOT / 'data/uni_note_release.json').read_text())
    phase2_slots = {k: v for k, v in slots.items() if not k.startswith('v4-')}
    v4_slots = {k: v for k, v in slots.items() if k.startswith('v4-')}
    errors = []
    def require(condition, detail):
        if not condition:
            errors.append(detail)
    require(release.get('mode') in ('upcoming', 'released', 'hidden'), 'Unknown Uni:Note release mode')
    original_ids = {o['id'] for o in plan['operations']}
    ids = [operation['id'] for operation in mapping['operations']]
    require(len(ids) == len(set(ids)) == 196 and set(ids) == original_ids, '196 primary operation assignments must be exact')
    require(phase2_slots.keys() == mapping['slots'].keys() and all({k: v for k, v in phase2_slots[i].items() if k not in ('status', 'retired_reason')} == {k: v for k, v in mapping['slots'][i].items() if k not in ('status', 'retired_reason')} for i in phase2_slots), 'Image data differs from the implementation map')
    require(len(navigation['categories']) == 15 + len(additions['categories']), 'Expected 15 categories plus 4.0.0 additions')
    mapped_keys = {p['key'] for p in mapping['pages']}
    navigation_keys = {p['key'] for p in navigation['pages']}
    require(navigation_keys - mapped_keys == set(additions['navigation_keys']) and mapped_keys <= navigation_keys,
            'Navigation/article mismatch')
    require(any(p['key'] == 'writing/text-shapes' and p['url'] == '/htu/uni-note/writing/#text-shapes'
                for p in navigation['pages']), '3.7.0 text and shapes guide link missing')
    masters = {m['id']: m for m in mapping['masters']}
    routes = {'/htu/uni-note/': 'content/htu/uni-note.md'}
    routes.update({p['url'].split('#')[0]: p['source'] for p in mapping['pages']})
    routes.update({'/htu/uni-note/' + c + '/': 'content/uni-note-guide/' + c + '.md' for c in mapping['categories']})
    routes.update(additions['routes'])
    require(len(routes) == 28 + len(additions['routes']), 'Expected top + 15 categories + 12 recipes plus 4.0.0 additions')
    documents = {}
    used_slots = []
    internal_references = 0
    public_images = []
    material_sources = [
        ROOT / 'content/uni-note-guide/materials.md',
        ROOT / 'content/uni-note-guide/workflows-material-margin.md',
        ROOT / 'content/uni-note-guide/workflows-vertical-annotate.md',
        ROOT / 'content/uni-note-guide/workflows-sticky-material.md',
    ]
    material_text = '\n'.join(path.read_text() for path in material_sources)
    require('固定中の資料をダブルタップして固定を解除し' in material_text, 'Finger Drawing OFF material unlock must use a double tap')
    require('「編集」ボタンを押して青い状態にし' in material_text, 'Finger Drawing ON material selection must use the Edit button')
    require('素材選択中' not in material_text, 'Retired material selection status label remains')
    require('素材操作のためにOFFへ切り替える必要はありません' in material_text, 'Finger Drawing ON must remain enabled for material operations')
    require('長押しし、表示されるメニューから「移動・サイズ変更」' not in material_text,
            'Retired Finger Drawing ON long-press selection remains')
    require(not re.search(r'指で描画.{0,24}OFFにし|指で描画.{0,24}OFFにして', material_text), 'Material operation must not require turning Finger Drawing off')
    localized_material_markers = {
        'en': ('double-tap a locked photo or PDF', '**Edit**'),
        'ko': ('두 번 탭해 잠금을 해제', '**편집**'),
        'de': ('durch Doppeltippen', '**Bearbeiten**'),
        'zh-hant': ('點兩下固定中的照片或 PDF', '**編輯**'),
        'fr': ('touchez deux fois une photo ou un PDF', '**Modifier**'),
    }
    retired_status_labels = ('Selecting Objects', '개체 선택 중', 'Objektauswahl', '正在選取物件', 'Sélection d’objets')
    for lang, markers in localized_material_markers.items():
        localized_source = (ROOT / f'content/htu/uni-note.{lang}.md').read_text()
        require(all(marker in localized_source for marker in markers), 'Localized material selection is incomplete: ' + lang)
        require(not any(label in localized_source for label in retired_status_labels), 'Retired material selection status label remains: ' + lang)
        require(not re.search(r'touch and hold the material|자료를 길게 누른 뒤|halte das Material gedrückt|長按素材|appui prolongé sur le document', localized_source),
                'Retired Finger Drawing ON long-press selection remains: ' + lang)
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
                require('## 完了の確認' in section_text, 'Section structure missing: ' + section['url'])
                require('## ' in section_text.split('## 完了の確認')[0], 'Missing instructions: ' + section['url'])
        html = target.read_text()
        doc = migration.Document(html)
        documents[route] = doc
        body = doc.body_content()
        require(body is not None, 'Missing content wrapper: ' + route)
        if body is None:
            continue
        visible = body.text()
        require(not re.search(r'CoreHandwriting|SHOT-|CAP-\d|[NMSR]-M\d|画像準備中|3\.4\.0|公開前情報', visible), 'Unreleased/internal/old-version text: ' + route)
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
                if url.scheme not in ('https','http') or url.netloc != 'kumakikai.top':
                    continue
                path = build / unquote(url.path).lstrip('/')
                if url.path.endswith('/'):
                    path /= 'index.html'
                require(path.is_file(), 'Broken internal link: ' + route + ' -> ' + value)
                internal_references += 1
                if url.fragment and path.is_file() and path.suffix == '.html':
                    linked = migration.Document(path.read_text())
                    require(unquote(url.fragment) in linked.ids, 'Broken fragment: ' + route + ' -> ' + value)
    active_slots = {k for k, v in slots.items() if v['status'] != 'retired'}
    require(len(used_slots) == len(set(used_slots)) and set(used_slots) == active_slots, 'Slots must each appear once in source; retired slots must not appear')
    for sid, slot in v4_slots.items():
        require(slot['status'] in ('pending', 'approved'), 'Unapproved 4.0.0 image status: ' + sid)
        if slot['status'] == 'approved':
            path = ROOT / 'assets' / slot['src']
            require(path.is_file() and digest(path) == slot['source_sha256'], 'Approved 4.0.0 screenshot altered: ' + sid)
            require(bool(slot.get('alt')) and bool(slot.get('caption')) and bool(slot.get('capture_version')), 'Missing 4.0.0 image explanation: ' + sid)
        else:
            require(not slot.get('src'), 'Pending image has public source: ' + sid)
    for sid, slot in phase2_slots.items():
        require(slot['master'] in masters, 'Unknown master: ' + sid)
        m = masters.get(slot['master'], {})
        require(slot['session'] == m.get('session_id') and slot['shot_ids'] == m.get('shot_ids'), 'Phase 1.5 references changed: ' + sid)
        require(slot['status'] in ('pending','approved','legacy-approved','retired'), 'Unapproved image status: ' + sid)
        if slot['status'] == 'pending':
            require(not slot.get('src'), 'Pending image has public source: ' + sid)
        elif slot['status'] == 'retired':
            pass
        else:
            path = ROOT / 'assets' / slot['src']
            require(path.is_file() and digest(path) == slot['source_sha256'], 'Approved screenshot altered: ' + sid)
            require(bool(slot.get('alt')) and bool(slot.get('caption')), 'Missing image explanation: ' + sid)
    require({s['master'] for s in phase2_slots.values()} == {m['id'] for m in masters.values() if m['importance'] == 'must'}, 'All 110 standard masters need a slot')
    approved = [s for s in slots.values() if s['status'] in ('approved','legacy-approved')]
    require(len(public_images) == len(approved), 'Pending image rendered or approved image missing')
    for image in public_images:
        require(image.get('alt') and image.get('width') and image.get('height') and image.get('srcset') and image.get('loading') == 'lazy', 'Invalid responsive image')
    top = documents.get('/htu/uni-note/')
    if top:
        require(set(plan['anchors']) <= set(top.ids), 'Legacy anchor lost')
        require('機能から探す' in top.ids, 'Guide category section missing')
        require(top.canonical() == [SITE + '/htu/uni-note/'] and not top.redirect(), 'Top URL identity changed')
        top_html = (build / 'htu/uni-note/index.html').read_text()
        index_match = re.search(r'<script[^>]+id=["\']?uni-guide-search-index["\']?[^>]*>(.*?)</script>', top_html, re.S)
        try:
            search_items = json.loads(index_match.group(1)) if index_match else None
        except json.JSONDecodeError:
            search_items = None
        visible_pages = [p for p in navigation['pages'] if not (p.get('release') and release['mode'] == 'hidden')]
        require(isinstance(search_items, list) and len(search_items) == len(visible_pages), 'Guide search index must be a JSON array generated from navigation data')
        require('data-guide-search-input' in top_html and 'data-guide-search-status' in top_html, 'Guide search controls missing')
        require('class="sr-only" for="uni-guide-search-input"' in top_html, 'Guide search label must remain accessible without repeating visually')
        require(top_html.find('article-related') < top_html.find('site-footer'), 'Shared support navigation must precede the site footer')
    search_ui = json.loads((ROOT / 'data/uni_guide_search_ui.json').read_text())
    for lang in ('en', 'ko', 'de', 'zh-hant', 'fr'):
        localized = build / lang / 'htu/uni-note/index.html'
        require(localized.is_file(), 'Missing localized Uni:Note guide: ' + lang)
        if localized.is_file():
            localized_html = localized.read_text()
            require('data-guide-search-mode="local"' in localized_html and search_ui[lang]['title'] in localized_html, 'Localized guide search missing: ' + lang)
            require(localized_html.find('article-related') < localized_html.find('site-footer'), 'Localized support navigation must precede site footer: ' + lang)
    workflow_pages = [p for p in mapping['pages'] if p['category'] == 'workflows']
    require(len(workflow_pages) == 12 and all(p['hero_masters'] for p in workflow_pages), '12 workflows each need hero reservations')
    preservation = json.loads((DIRECTORY / 'preservation.json').read_text())['tracked']
    for f, old_hash in preservation.items():
        if f.startswith(('assets/images/','static/images/')):
            require((ROOT/f).is_file() and digest(ROOT/f) == old_hash, 'Protected image/translation changed: ' + f)
    return {'ok':not errors,'pages':len(documents),'operations':len(ids),'legacy_anchors':len(plan['anchors']), 'slots':len(slots), 'pending_slots':sum(s['status']=='pending' for s in slots.values()),'standard_masters':len({s['master'] for s in phase2_slots.values()}),'v4_slots':len(v4_slots),'v4_approved':sum(s['status']=='approved' for s in v4_slots.values()),'reused_assets':len({s['src'] for s in approved}),'rendered_image_placements':len(public_images),'internal_references':internal_references,'errors':errors}


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
