#!/usr/bin/env python3
"""Read-only HTTP check of the deployed HTML against a known local build.

Run after GitHub Pages finishes, not during a deployment. All explicit HTML
URLs (including historical aliases) must return 200 and exactly match this
build. Meta refresh targets and bodies are covered by verify-migration.py.
No App Store Connect settings are changed by this check.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument('--build', type=Path, default=Path('public'))
parser.add_argument('--base-url', default='https://kumakikai.github.io')
parser.add_argument('--output', type=Path, default=Path('artifacts/migration/live.json'))
args = parser.parse_args()

def check(file):
    rel = file.relative_to(args.build).as_posix()
    route = '/' + (rel[:-10] if rel.endswith('index.html') else rel)
    expected = hashlib.sha256(file.read_bytes()).hexdigest()
    result = {'route': route, 'expected_sha256': expected}
    try:
        req = Request(args.base_url.rstrip('/') + route, headers={'User-Agent': 'KUMAKIKAI-URL-Compatibility-Check/1.0', 'Cache-Control': 'no-cache'})
        with urlopen(req, timeout=30) as response:
            data = response.read()
            result.update(status=response.status, final_url=response.url, actual_sha256=hashlib.sha256(data).hexdigest())
            result['ok'] = response.status == 200 and result['actual_sha256'] == expected
    except Exception as error:
        result.update(ok=False, error=str(error))
    return result

files = sorted(args.build.rglob('*.html'))
with ThreadPoolExecutor(max_workers=8) as pool:
    checks = list(pool.map(check, files))
report = {'checked_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'base_url': args.base_url, 'ok': all(x['ok'] for x in checks), 'count': len(checks), 'http_200': sum(x.get('status') == 200 for x in checks), 'failures': [x for x in checks if not x['ok']], 'results': checks}
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k != 'results'}, ensure_ascii=False, indent=2))
raise SystemExit(0 if report['ok'] else 1)
