#!/usr/bin/env python3
r"""Compare a local build, a deployed artifact, and every directly fetched file.

Example (run only after Pages has finished publishing):
  python3 scripts/verify-published-site.py --local-build public \
    --deployed-build /tmp/gh-pages-artifact --output /tmp/published-check \
    --base-url https://kumakikai.github.io

The output directory must be new or empty. report.json and both complete file
manifests are saved there. responses/ mirrors the deployed directory layout so
the saved responses can be passed to the site's local HTML/link scanner.
headers/ contains curl's raw response headers, including redirect hops.

Only Git checkout metadata is omitted from inventories. An empty .nojekyll is
recorded as a deployment control file: actions-gh-pages adds it, and Pages does
not serve it as site content. No other files are silently excluded.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from urllib.parse import quote, urlencode, urlsplit
import uuid


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root):
    """Include hidden deployment files; exclude only checkout administration."""
    files = []
    ignored = []
    for directory, subdirs, names in os.walk(root, followlinks=False):
        parent = Path(directory)
        if '.git' in subdirs:
            subdirs.remove('.git')
            ignored.append((parent / '.git').relative_to(root).as_posix() + '/')
        for name in subdirs:
            if (parent / name).is_symlink():
                raise ValueError(f'Symlink in build: {parent / name}')
        for name in names:
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if name == '.git':
                ignored.append(relative)
                continue
            if path.is_symlink() or not path.is_file():
                raise ValueError(f'Non-regular file in build: {path}')
            files.append({'path': relative, 'bytes': path.stat().st_size,
                          'sha256': sha256(path)})
    return {'files': sorted(files, key=lambda row: row['path']),
            'ignoredGitMetadata': sorted(ignored)}


def compare_manifests(local, deployed):
    left = {row['path']: row for row in local['files']}
    right = {row['path']: row for row in deployed['files']}
    control_files = []
    control_errors = []
    for name, table in [('local', left), ('deployed', right)]:
        control = table.pop('.nojekyll', None)
        if control is not None:
            control_files.append({'build': name, **control})
            if control['bytes'] != 0:
                control_errors.append(f'{name} .nojekyll must be empty')
    missing = sorted(left.keys() - right.keys())
    extra = sorted(right.keys() - left.keys())
    changed = [{'path': path, 'localSHA256': left[path]['sha256'],
                'deployedSHA256': right[path]['sha256']}
               for path in sorted(left.keys() & right.keys())
               if left[path]['sha256'] != right[path]['sha256']]
    return {'ok': not (missing or extra or changed or control_errors),
            'missingFromDeployed': missing, 'onlyInDeployed': extra,
            'changed': changed, 'deploymentControlFiles': control_files,
            'deploymentControlErrors': control_errors,
            'exception': 'Only an empty root .nojekyll may differ; it is not HTTP content.'}


def route_for(relative):
    path = Path(relative)
    if path.name == 'index.html':
        parent = path.parent.as_posix()
        return '/' if parent == '.' else '/' + parent + '/'
    return '/' + path.as_posix()


def parse_header_blocks(raw):
    blocks = []
    current = None
    for line in raw.splitlines():
        match = re.match(r'^HTTP/\S+\s+(\d{3})(?:\s|$)', line)
        if match:
            current = {'statusLine': line, 'status': int(match.group(1)),
                       'headers': []}
            blocks.append(current)
        elif current is not None and ':' in line:
            name, value = line.split(':', 1)
            current['headers'].append({'name': name.strip(), 'value': value.strip()})
    return blocks


def get_git_commit(path):
    result = subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def fetch_file(row, args, run_id, curl):
    relative = row['path']
    route = route_for(relative)
    query = urlencode({'published-site-check': f'{run_id}-{row["sha256"][:12]}'})
    url = args.base_url.rstrip('/') + quote(route, safe='/') + '?' + query
    body_path = args.output / 'responses' / relative
    header_path = args.output / 'headers' / (relative + '.headers.txt')
    body_path.parent.mkdir(parents=True, exist_ok=True)
    header_path.parent.mkdir(parents=True, exist_ok=True)
    result = {'path': relative, 'route': route, 'url': url,
              'startedAt': utc_now(), 'expectedSHA256': row['sha256'],
              'expectedBytes': row['bytes'],
              'bodyFile': body_path.relative_to(args.output).as_posix(),
              'headersFile': header_path.relative_to(args.output).as_posix()}
    command = [curl, '--silent', '--show-error', '--location', '--max-redirs', '5',
               '--proto', '=http,https', '--proto-redir', '=http,https',
               '--compressed', '--connect-timeout', '10',
               '--max-time', str(args.timeout), '--retry', str(args.retries),
               '--retry-delay', '1', '--retry-max-time', str(args.timeout * 2),
               '--header', 'Cache-Control: no-cache', '--header', 'Pragma: no-cache',
               '--user-agent', 'KUMAKIKAI-Published-Site-Verification/1.0',
               '--dump-header', str(header_path), '--output', str(body_path),
               '--write-out', '%{http_code}\n%{url_effective}\n%{num_redirects}\n%{content_type}\n%{size_download}\n%{time_total}\n',
               '--url', url]
    errors = []
    try:
        completed = subprocess.run(command, capture_output=True, text=True,
                                   check=False, timeout=args.timeout * (args.retries + 2) + 15)
        result['curlExitCode'] = completed.returncode
        fields = completed.stdout.splitlines()
        if len(fields) >= 6:
            result.update(status=int(fields[0]), effectiveURL=fields[1],
                          redirects=int(fields[2]), contentType=fields[3],
                          transferredBytes=float(fields[4]), transferSeconds=float(fields[5]))
        else:
            errors.append('curl did not return complete response metadata')
        if completed.returncode:
            errors.append('curl failed: ' + completed.stderr.strip())
        elif completed.stderr.strip():
            result['curlWarnings'] = completed.stderr.strip()
    except (OSError, subprocess.TimeoutExpired, ValueError) as error:
        errors.append(str(error))
    if header_path.exists():
        result['headerBlocks'] = parse_header_blocks(header_path.read_text(errors='replace'))
    allowed = [200, 404] if Path(relative).name == '404.html' else [200]
    result['expectedStatuses'] = allowed
    result['statusOK'] = result.get('status') in allowed
    if not result['statusOK']:
        errors.append(f'Unexpected HTTP status {result.get("status")}; expected {allowed}')
    if body_path.exists():
        result['actualSHA256'] = sha256(body_path)
        result['actualBytes'] = body_path.stat().st_size
        result['bodyMatches'] = result['actualSHA256'] == row['sha256']
        if not result['bodyMatches']:
            errors.append('Public response body differs from deployed artifact')
    else:
        result['bodyMatches'] = False
        errors.append('No response body saved')
    result.update(ok=not errors, errors=errors, finishedAt=utc_now())
    return result


def write_json(path, value):
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--local-build', type=Path, required=True)
    parser.add_argument('--deployed-build', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True,
                        help='New or empty run directory (report.json, manifests, responses, headers)')
    parser.add_argument('--base-url', default='https://kumakikai.github.io')
    parser.add_argument('--jobs', type=int, default=4, help='Concurrent curl GETs, 1–8 (default: 4)')
    parser.add_argument('--timeout', type=int, default=30, help='Maximum seconds per curl transfer')
    parser.add_argument('--retries', type=int, default=1, help='curl retries for transient failures (0–3)')
    parser.add_argument('--source-commit', help='Optional source commit for an extracted local build')
    parser.add_argument('--deployed-commit', help='Optional gh-pages commit for an extracted artifact')
    args = parser.parse_args(argv)
    for key in ['local_build', 'deployed_build', 'output']:
        setattr(args, key, getattr(args, key).resolve())
    for root in [args.local_build, args.deployed_build]:
        if not root.is_dir():
            parser.error(f'Build directory not found: {root}')
        if args.output == root or args.output in root.parents or root in args.output.parents:
            parser.error('--output must be separate from both build trees')
    if args.output.exists() and (not args.output.is_dir() or any(args.output.iterdir())):
        parser.error('--output must be a new or empty directory to prevent stale response files')
    url = urlsplit(args.base_url)
    if url.scheme not in ('http', 'https') or not url.netloc or url.username or url.password or url.query or url.fragment:
        parser.error('--base-url must be an HTTP(S) base URL without credentials, query or fragment')
    if not 1 <= args.jobs <= 8 or not 1 <= args.timeout <= 300 or not 0 <= args.retries <= 3:
        parser.error('Require jobs 1–8, timeout 1–300, retries 0–3')
    return args


def main(argv=None):
    args = arguments(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    report = {'ok': False, 'status': 'running', 'runID': str(uuid.uuid4()),
              'startedAt': utc_now(), 'baseURL': args.base_url,
              'localBuild': str(args.local_build), 'deployedBuild': str(args.deployed_build),
              'responsesDirectory': str(args.output / 'responses'),
              'sourceCommit': args.source_commit or get_git_commit(args.local_build),
              'deployedCommit': args.deployed_commit or get_git_commit(args.deployed_build),
              'method': 'All artifact files inventoried and SHA256 compared. All serving files fetched with curl GET, no-cache, Pragma and a unique query; decompressed response bytes compared with the deployed artifact. HTTP redirect headers and final URLs are retained. Only root .nojekyll is a non-serving deployment control file.',
              'requestHeaders': {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'},
              'jobs': args.jobs, 'results': []}
    report_path = args.output / 'report.json'
    write_json(report_path, report)
    try:
        curl = shutil.which('curl')
        if not curl:
            raise ValueError('curl is required')
        version = subprocess.run([curl, '--version'], capture_output=True, text=True,
                                 check=True)
        report['curlVersion'] = version.stdout.splitlines()[0]
        local = inventory(args.local_build)
        deployed = inventory(args.deployed_build)
        if not local['files'] or not deployed['files']:
            raise ValueError('Build inventories must not be empty')
        write_json(args.output / 'local-manifest.json', local)
        write_json(args.output / 'deployed-manifest.json', deployed)
        report['manifests'] = {'local': 'local-manifest.json', 'deployed': 'deployed-manifest.json'}
        report['artifactComparison'] = compare_manifests(local, deployed)
        serving = [row for row in deployed['files'] if row['path'] != '.nojekyll']
        report['counts'] = {'localFiles': len(local['files']), 'deployedFiles': len(deployed['files']),
                            'servingFiles': len(serving), 'htmlFiles': sum(row['path'].endswith('.html') for row in serving),
                            'expectedBytes': sum(row['bytes'] for row in serving), 'completed': 0}
        write_json(report_path, report)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            pending = [pool.submit(fetch_file, row, args, report['runID'], curl) for row in serving]
            for future in as_completed(pending):
                report['results'].append(future.result())
                report['counts']['completed'] = len(report['results'])
                if len(report['results']) % 20 == 0:
                    write_json(report_path, report)
                    print(f'Checked {len(report["results"])}/{len(serving)} public files', flush=True)
        report['results'].sort(key=lambda row: row['path'])
        report['inputsUnchanged'] = {'local': inventory(args.local_build) == local,
                                     'deployed': inventory(args.deployed_build) == deployed}
        report['failures'] = [row for row in report['results'] if not row['ok']]
        report['counts'].update(http200=sum(row.get('status') == 200 for row in report['results']),
                                expected404=sum(row.get('status') == 404 and row['statusOK'] for row in report['results']),
                                matchingBodies=sum(row['bodyMatches'] for row in report['results']),
                                failed=len(report['failures']))
        report['ok'] = (report['artifactComparison']['ok'] and not report['failures']
                        and all(report['inputsUnchanged'].values())
                        and len(report['results']) == len(serving) and bool(serving))
        report['status'] = 'complete'
    except Exception as error:
        report.update(status='failed', fatalError=str(error))
    report.update(finishedAt=utc_now(), durationSeconds=round(time.monotonic() - start, 3))
    write_json(report_path, report)
    print(json.dumps({'ok': report['ok'], 'report': str(report_path),
                      'responsesDirectory': report['responsesDirectory'],
                      'counts': report.get('counts'), 'fatalError': report.get('fatalError'),
                      'artifactComparison': report.get('artifactComparison'),
                      'failures': [{'path': row['path'], 'status': row.get('status'), 'errors': row['errors']}
                                   for row in report.get('failures', [])[:20]],
                      'omittedFailures': max(0, len(report.get('failures', [])) - 20)},
                     ensure_ascii=False, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
