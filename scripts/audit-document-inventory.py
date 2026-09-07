#!/usr/bin/env python3
"""List every real product document and its source structure; no network or edits."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ('htu', 'faq', 'privacy', 'terms')
TOPICS = {
    'introduction': r'はじめに|基本|About|Introduction|Getting started|Einführung|소개|簡介|基本',
    'environment': r'対応|環境|OS|device|compatib|Voraussetzung|Gerät|지원|裝置',
    'data': r'データ|保存|削除|バックアップ|data|storage|backup|Daten|données|데이터|資料|備份',
    'purchase': r'課金|購入|料金|サブスクリプション|Premium|Plus|purchase|subscription|Kauf|abonnement|구매|購買',
    'troubleshooting': r'困った|不具合|できない|トラブル|troubleshoot|problem|Proble|문제|問題',
    'contact': r'問い合わせ|contact|Kontakt|문의|聯絡',
    'operator': r'運営|当方|開発者|KUMAKIKAI|Yuya Nakamura|developer|développeur|Entwickler|개발자|開發者',
    'ai': r'\bAI\b|人工知能|人工智慧',
    'ads_analytics': r'広告|解析|Analytics|Crashlytics|AdMob|advertis|publicité|Werbung|광고|廣告',
    'external': r'外部|第三者|AWS|Google|Apple|OpenAI|GitHub|third.party|tiers|Dritt|제3|第三',
    'account': r'アカウント|ログイン|account|compte|Konto|계정|帳號',
    'law': r'準拠法|管轄|免責|禁止事項|知的財産|governing law|liability|intellectual|juridiction',
}


def inventory(root):
    apps = json.loads((root / 'data/apps.json').read_text())
    pages = []
    for app in apps:
        for section in SECTIONS:
            for path in sorted((root / 'content' / section).glob(app['id'] + '*.md')):
                stem = path.stem.split('.')
                if stem[0] != app['id']:
                    continue
                lang = stem[1] if len(stem) == 2 else 'ja'
                text = path.read_text()
                body = text.split('---', 2)[-1]
                headings = [{'line': i, 'level': len(m[1]), 'text': m[2]} for i, line in enumerate(text.splitlines(), 1) if (m := re.match(r'^(#{2,4})\s+(.*)', line))]
                pages.append({
                    'product': app['id'], 'section': section, 'language': lang,
                    'source': str(path.relative_to(root)),
                    'route': ('' if lang == 'ja' else '/' + lang) + '/' + section + '/' + app['id'] + '/',
                    'sourceSHA256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'characters': len(body), 'headings': headings,
                    'dates': [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1) if re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', line)],
                    'topics': {topic: bool(re.search(pattern, body, re.I)) for topic, pattern in TOPICS.items()},
                    'images': re.findall(r'guide-image\s+src="([^"]+)"', text),
                    'externalURLs': sorted(set(re.findall(r'https?://[^\s)\]>"}]+', body))),
                })
    return {'products': len(apps), 'documents': len(pages), 'bySection': dict(Counter(p['section'] for p in pages)), 'pages': pages}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = inventory(ROOT)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'inventory.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    lines = ['# Product document source inventory', '', 'Generated from local source. Topic matches are candidates for manual review, not semantic conclusions.', '', f"{data['products']} products / {data['documents']} documents / {data['bySection']}", '']
    for page in data['pages']:
        lines += [f"## {page['route']}", '', f"Source: `{page['source']}` — {page['characters']} characters", '']
        lines += [f"- L{h['line']} {'#' * h['level']} {h['text']}" for h in page['headings']]
        lines += ['', 'Dates: ' + '; '.join(x['text'] for x in page['dates']), '']
    (args.output / 'headings.md').write_text('\n'.join(lines))
    print(json.dumps({k: v for k, v in data.items() if k != 'pages'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
