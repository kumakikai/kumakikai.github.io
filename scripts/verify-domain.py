#!/usr/bin/env python3
"""Check the production domain in the complete deployable Hugo output."""
import argparse
import json
from pathlib import Path
import re
import sys
import tomllib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'kumakikai.top'
SITE = 'https://' + DOMAIN + '/'
OLD_DOMAIN = 'kumakikai.github.io'


def verify(build):
    errors = []
    config = tomllib.loads((ROOT / 'hugo.toml').read_text())
    if config.get('baseURL') != SITE:
        errors.append('hugo.toml baseURL must be ' + SITE)
    for path in (ROOT / 'static/CNAME', build / 'CNAME'):
        if not path.is_file() or path.read_text() != DOMAIN + '\n':
            errors.append('Missing or incorrect CNAME: ' + str(path))
    counts = {'textFiles': 0, 'rssFeeds': 0, 'sitemaps': 0}
    for path in sorted(build.rglob('*')):
        if not path.is_file() or path.suffix not in {'.html', '.xml', '.txt', '.json', '.webmanifest', '.js', '.css', '.svg'}:
            continue
        text = path.read_text()
        route = str(path.relative_to(build))
        counts['textFiles'] += 1
        if OLD_DOMAIN in text.lower():
            errors.append('Old production domain remains: ' + route)
        if re.search(r'https?://www\.kumakikai\.top(?:[/:"\s<]|$)', text, re.I):
            errors.append('Noncanonical www origin remains: ' + route)
        if re.search(r'http://kumakikai\.top(?:[/:"\s<]|$)', text, re.I):
            errors.append('Insecure production URL remains: ' + route)
        if path.suffix != '.xml':
            continue
        try:
            tree = ET.fromstring(text)
        except ET.ParseError as exc:
            errors.append(f'Invalid XML {route}: {exc}')
            continue
        if tree.tag == 'rss':
            counts['rssFeeds'] += 1
            urls = [n.text for n in tree.findall('./channel/link') + tree.findall('./channel/item/link') + tree.findall('./channel/item/guid')]
            urls += [n.attrib.get('href') for n in tree.findall('./channel/{http://www.w3.org/2005/Atom}link')]
        elif tree.tag.endswith('}urlset') or tree.tag.endswith('}sitemapindex'):
            counts['sitemaps'] += 1
            urls = [n.text for n in tree.iter() if n.tag.endswith('}loc')]
        else:
            continue
        if not urls or any(not u or not u.startswith(SITE) for u in urls):
            errors.append('Noncanonical feed/sitemap URLs: ' + route)
    return {'ok': not errors, 'site': SITE, **counts, 'errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, default=Path('public'))
    args = parser.parse_args()
    result = verify(args.build)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result['ok'] else 1)
