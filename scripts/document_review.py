"""Reviewed 2026-09-08 product documents; immutable inputs and exact output bindings.

This explicit all-product revision supersedes older narrow exceptions only for
the 69 inventoried documents and five newly authorized Japanese Terms pages.
News, Product content, old route identities and the migration baseline remain
outside this exception. The catalog is recorded after content review.
"""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

DIRECTORY = 'docs/audits/2026-09-08-document-unification'
CATALOG = DIRECTORY + '/reviewed-content.json'
PURPOSE = 'all-product-document-unification-2026-09-08'
PINNED = {
    DIRECTORY + '/before/inventory.json': '41437ed54ffa7f11b7e07ae281e6017383f9784abd948efb9f6f46d500817823',
    DIRECTORY + '/before/bodies.json': 'db5eaad3ac9033b9a080c5158e015df132a8c48b815f9f6a3c008df095f4051e',
    'docs/migration/baseline.json': 'a09c6b7570cb4369b944309c9474bbe0353ae009c25cbc23069b626f0f9b8e49',
}
NEW_TERMS = {'uni-note', 'uni-note-pocket', 'smokeless', 'balance-calendar', 'signal'}
FAMILIES = {
    'uni-note': 'learning', 'uni-note-pocket': 'learning',
    'nocca': 'communication', 'oto-miru': 'communication',
    'giga-poke': 'utilities', 'smokeless': 'utilities', 'balance-calendar': 'utilities', 'signal': 'utilities',
}
SITE = 'https://kumakikai.github.io'


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def flat(value):
    return re.sub(r'\s+', ' ', value).strip()


def issue(route, kind, detail):
    return {'page': route, 'check': 'document_review_' + kind, 'detail': detail}


def inputs(root):
    for name, checksum in PINNED.items():
        path = root / name
        if path.is_symlink() or digest(path.read_bytes()) != checksum:
            raise ValueError('Immutable review input changed: ' + name)
    inventory = json.loads((root / DIRECTORY / 'before/inventory.json').read_text())
    before = json.loads((root / DIRECTORY / 'before/bodies.json').read_text())
    scope = {p['route']: p['source'] for p in inventory['pages']}
    if len(scope) != 69 or set(scope) != set(before):
        raise ValueError('The original 69 documents must be inventoried exactly')
    scope.update({f'/terms/{app}/': f'content/terms/{app}.md' for app in NEW_TERMS})
    return scope, before


def body_links(route, body):
    return sorted({urljoin(SITE + route, n.attrs['href']) for n in body.descendants('a') if n.attrs.get('href')})


def load_reviews(root, baseline):
    try:
        scope, before = inputs(root)
        catalog = json.loads((root / CATALOG).read_text())
        if set(catalog) != {'schemaVersion', 'purpose', 'reviews'} or catalog['schemaVersion'] != 1 or catalog['purpose'] != PURPOSE:
            raise ValueError('Catalog schema or purpose mismatch')
        reviews = catalog['reviews']
        if not isinstance(reviews, dict) or set(reviews) != set(scope):
            raise ValueError('Review must cover exactly the 69 existing documents and five new Terms')
        fields = {'source', 'sourceSHA256', 'beforeSourceSHA256', 'baselineTextSHA256', 'reviewedTextSHA256', 'reviewedLinks', 'removedLinks', 'reason', 'evidence'}
        for route, source_name in scope.items():
            row = reviews[route]
            if not isinstance(row, dict) or set(row) != fields or row['source'] != source_name:
                raise ValueError('Review source/fields mismatch: ' + route)
            source = root / source_name
            if not source.is_file() or source.is_symlink() or digest(source.read_bytes()) != row['sourceSHA256']:
                raise ValueError('Source changed since review: ' + route)
            old = baseline['articles'].get(route)
            if row['beforeSourceSHA256'] != before.get(route, {}).get('sourceSHA256') or row['baselineTextSHA256'] != (digest(old['text']) if old else None):
                raise ValueError('Original source or migration body mismatch: ' + route)
            for key in ('sourceSHA256', 'reviewedTextSHA256'):
                if not isinstance(row[key], str) or not re.fullmatch('[0-9a-f]{64}', row[key]):
                    raise ValueError('Invalid SHA256 binding: ' + route)
            for key in ('reviewedLinks', 'removedLinks'):
                if not isinstance(row[key], list) or any(not isinstance(x, str) for x in row[key]) or row[key] != sorted(set(row[key])):
                    raise ValueError('Links must be a sorted exact set: ' + route)
            expected_removed = sorted(set(old['links']) - set(row['reviewedLinks'])) if old else []
            if row['removedLinks'] != expected_removed:
                raise ValueError('Unexplained old-link changes: ' + route)
            app = route.strip('/').split('/')[-1]
            evidence = [DIRECTORY + '/' + FAMILIES[app] + '-phase1.md', DIRECTORY + '/' + FAMILIES[app] + '-phase3.md']
            if row['evidence'] != evidence or not all((root / x).is_file() for x in evidence) or not isinstance(row['reason'], str) or len(row['reason'].strip()) < 30:
                raise ValueError('A product-specific audit and review reason are required: ' + route)
        return reviews, before, []
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {}, {}, [issue('/', 'catalog', str(exc))]


def check_article(route, row, doc, before):
    errors = []
    body = doc.body_content()
    if body is None:
        return [issue(route, 'body', 'Missing formal document body')]
    if digest(flat(body.text())) != row['reviewedTextSHA256']:
        errors.append(issue(route, 'body', 'Rendered text differs from reviewed output'))
    links = body_links(route, body)
    if links != row['reviewedLinks']:
        errors.append(issue(route, 'links', 'Rendered links differ from reviewed output'))
    if missing := sorted(set(before.get(route, {}).get('ids', [])) - set(doc.ids)):
        errors.append(issue(route, 'anchors', 'Pre-revision anchors disappeared: ' + repr(missing)))
    # User requested structural editing, not replacing real operation pictures.
    images = [n.attrs for n in body.descendants('img')]
    if images != before.get(route, {}).get('images', []):
        errors.append(issue(route, 'images', 'Operation images, alternatives, or dimensions changed'))
    if route.endswith('/nocca/'):
        from nocca_legal_review import has_form_reference, APPROVED_FORM
        if any(has_form_reference(x) and x != APPROVED_FORM for x in links):
            errors.append(issue(route, 'contact', 'Only the exact approved Nocca form is valid'))
    return errors


def check_structure(root, route, doc):
    """Independent semantic skeleton and contact checks for all 74 documents."""
    errors = []
    def require(ok, kind, detail):
        if not ok:
            errors.append(issue(route, kind, detail))
    parts = route.strip('/').split('/')
    lang = parts.pop(0) if len(parts) == 3 else 'ja'
    section, app_id = parts
    ui = json.loads((root / 'data/document_ui.json').read_text())[lang]
    body = doc.body_content()
    require(body is not None, 'structure', 'A formal body is required')
    if body is None:
        return errors
    h2 = [flat(n.text()) for n in body.descendants('h2')]
    h3 = [flat(n.text()) for n in body.descendants('h3')]
    contacts = [n for n in body.descendants() if 'data-document-contact' in n.attrs]
    require(len(contacts) == 1, 'contact', 'Exactly one shared contact block is required')
    app = next(a for a in json.loads((root / 'data/apps.json').read_text()) if a['id'] == app_id)
    expected = app['support'].get('contactURL', 'mailto:kumakikai.apps@gmail.com')
    all_links = [n.attrs.get('href') for n in body.descendants('a')]
    if contacts:
        contact_links = [n.attrs.get('href') for n in contacts[0].descendants('a')]
        if expected.startswith('mailto:'):
            require(len(contact_links) == 1 and contact_links[0].split('?')[0] == expected, 'contact', 'Official support email required')
        else:
            require(len(contact_links) == 2 and contact_links[0] == expected and contact_links[1].startswith('mailto:kumakikai.apps@gmail.com?subject='), 'contact', 'Official form plus fallback email required')
        require(all(all_links.count(url) == 1 for url in contact_links), 'contact', 'Contact destinations repeated in body')
    if section == 'htu':
        require(h2[:2] == [ui['introduction'], ui['basics']], 'structure', 'Guide must begin with introduction and basic use')
        require(h2[-2:] == [ui['trouble'], ui['contact']], 'structure', 'Guide must end with help and contact')
        faq_route = route.replace('/htu/', '/faq/') + '#help'
        require(faq_route in all_links, 'help', 'Guide help must lead to the corresponding FAQ help section')
    elif section == 'faq':
        require(h2 and h2[0] == ui['introduction'] and h2[-1] == ui['trouble'], 'structure', 'FAQ must begin with introduction and end with help')
        require(h3[-2:] == [ui['failureQuestion'], ui['contactQuestion']], 'structure', 'FAQ must end with the shared troubleshooting and contact questions')
        require(ui['environmentQuestion'] in h3, 'structure', 'FAQ needs its supported-device question')
        require(any(n.attrs.get('id') == 'help' and flat(n.text()) == ui['trouble'] for n in body.descendants('h2')), 'help', 'FAQ help anchor must identify its troubleshooting section')
    else:
        require(bool(h2) and all(re.match(rf'^{i}\.\s', text) for i, text in enumerate(h2, 1)), 'numbering', 'Legal headings must have consecutive section numbers')
        require(bool(h2) and h2[-1].split('. ', 1)[-1] == ui['contact'], 'structure', 'Legal contact must be the final section')
        require(not any(n.has_class('support-resources') or n.has_class('article-related') for n in body.descendants()), 'navigation', 'Shared support navigation belongs after the formal legal body')
        require(sum(n.has_class('article-related') for n in doc.nodes) == 1 and sum(n.has_class('support-resources') for n in doc.nodes) == 1, 'navigation', 'Legal pages need one shared support area after the body')
        require(sum(n.has_class('legal-dates') for n in doc.nodes) == 1, 'dates', 'Legal dates must appear once above the body')
        require('Yuya Nakamura' in body.text() and 'KUMAKIKAI' in body.text(), 'operator', 'Name the common operator')
        require(not re.search(r'GitHub|Privacy Manifest|PrivacyInfo|リポジトリ|サイト生成|ホスティング', body.text(), re.I), 'internal_details', 'Internal website/build details do not belong in app legal text')
        if section == 'privacy':
            names = [re.sub(r'^\d+\.\s*', '', text) for text in h2]
            standard = ui['privacyHeadings']
            require(names[:5] == standard[:5] and standard[5] in names and names[-2:] == standard[-2:], 'structure', 'Privacy must use the same common topic names and order in its language')
        if section == 'terms':
            require('https://www.apple.com/legal/internet-services/itunes/dev/stdeula/' in all_links, 'license', 'Retain the Apple license reference')
    return errors
