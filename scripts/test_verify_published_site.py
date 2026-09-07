#!/usr/bin/env python3
"""Local-only HTTP fixtures for the publication verifier; no public requests."""

from contextlib import contextmanager, redirect_stderr, redirect_stdout
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.parse import unquote, urlsplit


spec = importlib.util.spec_from_file_location(
    'published_verifier', Path(__file__).with_name('verify-published-site.py'))
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@contextmanager
def fixture_server(routes):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlsplit(self.path)
            route = unquote(parsed.path)
            requests.append({'route': route, 'query': parsed.query,
                             'cacheControl': self.headers.get('Cache-Control'),
                             'pragma': self.headers.get('Pragma')})
            status, body, headers = routes.get(route, (404, b'unknown route', {}))
            self.send_response(status)
            for name, value in headers.items():
                self.send_header(name, value)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}', requests
    finally:
        server.shutdown()
        server.server_close()
        worker.join()


class PublishedSiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='published-site-fixture-')
        self.root = Path(self.temporary.name)
        self.local = self.root / 'local'
        self.deployed = self.root / 'deployed'
        self.output = self.root / 'evidence'
        self.local.mkdir()
        self.deployed.mkdir()

    def tearDown(self):
        self.temporary.cleanup()

    def put(self, root, relative, body):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)

    def matching(self, files):
        for root in [self.local, self.deployed]:
            for relative, body in files.items():
                self.put(root, relative, body)

    def run_verifier(self, base):
        with redirect_stdout(io.StringIO()):
            code = verifier.main(['--local-build', str(self.local),
                                  '--deployed-build', str(self.deployed),
                                  '--output', str(self.output), '--base-url', base,
                                  '--jobs', '2', '--retries', '0', '--timeout', '5',
                                  '--source-commit', 'fixture-source',
                                  '--deployed-commit', 'fixture-pages'])
        return code, json.loads((self.output / 'report.json').read_text())

    def test_all_bytes_redirect_headers_cache_controls_and_404_variants(self):
        files = {'index.html': b'<html>home</html>',
                 'guide/index.html': b'<html>guide</html>',
                 '404.html': b'<html>not found</html>',
                 'en/404.html': b'<html>localized not found</html>',
                 'images/example icon.svg': b'<svg>\x00\x01\xff</svg>',
                 'assets/site.css': b'body { color: #111; }'}
        self.matching(files)
        self.put(self.deployed, '.nojekyll', b'')
        routes = {verifier.route_for(path): (200, body, {}) for path, body in files.items()}
        routes['/404.html'] = (404, files['404.html'], {})
        routes['/guide/'] = (302, b'', {'Location': '/published-guide/'})
        routes['/published-guide/'] = (200, files['guide/index.html'], {'ETag': '"fixture"'})
        routes['/assets/site.css'] = (200, gzip.compress(files['assets/site.css']),
                                      {'Content-Encoding': 'gzip'})
        with fixture_server(routes) as (base, requests):
            code, report = self.run_verifier(base)
        self.assertEqual(code, 0)
        self.assertTrue(report['ok'])
        self.assertEqual(report['counts']['servingFiles'], len(files))
        self.assertEqual(report['counts']['matchingBodies'], len(files))
        self.assertEqual(report['counts']['expected404'], 1)
        self.assertEqual(report['counts']['http200'], len(files) - 1)
        self.assertEqual(report['sourceCommit'], 'fixture-source')
        self.assertTrue(all(report['inputsUnchanged'].values()))
        for relative, body in files.items():
            self.assertEqual((self.output / 'responses' / relative).read_bytes(), body)
        rows = {row['path']: row for row in report['results']}
        guide = rows['guide/index.html']
        self.assertEqual(guide['redirects'], 1)
        self.assertTrue(guide['effectiveURL'].endswith('/published-guide/'))
        self.assertEqual([block['status'] for block in guide['headerBlocks']], [302, 200])
        self.assertIn('Location: /published-guide/',
                      (self.output / guide['headersFile']).read_text())
        initial = [request for request in requests if request['route'] != '/published-guide/']
        self.assertEqual(len(initial), len(files))
        self.assertTrue(all(request['query'].startswith('published-site-check=') for request in initial))
        self.assertEqual(len({request['query'] for request in initial}), len(initial))
        self.assertTrue(all(request['cacheControl'] == 'no-cache' and request['pragma'] == 'no-cache'
                            for request in requests))
        deployed = json.loads((self.output / 'deployed-manifest.json').read_text())
        self.assertIn('.nojekyll', [row['path'] for row in deployed['files']])
        self.assertFalse((self.output / 'responses' / '.nojekyll').exists())

    def test_matching_body_with_404_on_normal_file_is_failure(self):
        self.matching({'asset.txt': b'matching body'})
        with fixture_server({'/asset.txt': (404, b'matching body', {})}) as (base, _):
            code, report = self.run_verifier(base)
        self.assertEqual(code, 1)
        self.assertTrue(report['results'][0]['bodyMatches'])
        self.assertFalse(report['results'][0]['statusOK'])
        self.assertEqual(report['counts']['expected404'], 0)

    def test_http_200_with_different_bytes_is_failure(self):
        self.matching({'index.html': b'expected'})
        with fixture_server({'/': (200, b'outdated', {})}) as (base, _):
            code, report = self.run_verifier(base)
        self.assertEqual(code, 1)
        self.assertTrue(report['results'][0]['statusOK'])
        self.assertFalse(report['results'][0]['bodyMatches'])
        self.assertEqual((self.output / 'responses/index.html').read_bytes(), b'outdated')

    def test_local_deployed_mismatch_fails_even_if_public_matches(self):
        self.put(self.local, 'index.html', b'local')
        self.put(self.deployed, 'index.html', b'deployed')
        with fixture_server({'/': (200, b'deployed', {})}) as (base, _):
            code, report = self.run_verifier(base)
        self.assertEqual(code, 1)
        self.assertEqual(report['counts']['matchingBodies'], 1)
        self.assertEqual(report['artifactComparison']['changed'][0]['path'], 'index.html')

    def test_manifest_preserves_all_files_and_reports_mismatches(self):
        self.matching({'index.html': b'home', '.hidden-file': b'included'})
        self.put(self.local, 'removed.txt', b'local only')
        self.put(self.deployed, 'added.txt', b'deployed only')
        self.put(self.deployed, '.hidden-file', b'changed')
        self.put(self.deployed, '.nojekyll', b'nonempty must fail')
        self.put(self.deployed, '.git/HEAD', b'checkout metadata')
        manifest = verifier.inventory(self.deployed)
        self.assertEqual(manifest['ignoredGitMetadata'], ['.git/'])
        result = verifier.compare_manifests(verifier.inventory(self.local), manifest)
        self.assertFalse(result['ok'])
        self.assertEqual(result['missingFromDeployed'], ['removed.txt'])
        self.assertEqual(result['onlyInDeployed'], ['added.txt'])
        self.assertEqual(result['changed'][0]['path'], '.hidden-file')
        self.assertEqual(result['deploymentControlErrors'], ['deployed .nojekyll must be empty'])

    def test_refuses_stale_response_directory_and_overlapping_input(self):
        self.matching({'index.html': b'home'})
        self.put(self.output, 'responses/stale.html', b'old')
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as context:
            verifier.arguments(['--local-build', str(self.local), '--deployed-build', str(self.deployed),
                                '--output', str(self.output)])
        self.assertEqual(context.exception.code, 2)
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as context:
            verifier.arguments(['--local-build', str(self.local), '--deployed-build', str(self.deployed),
                                '--output', str(self.local / 'downloaded')])
        self.assertEqual(context.exception.code, 2)

    def test_rejects_symlinked_artifact_content(self):
        self.put(self.local, 'index.html', b'home')
        (self.deployed / 'index.html').symlink_to(self.local / 'index.html')
        with self.assertRaisesRegex(ValueError, 'Non-regular file'):
            verifier.inventory(self.deployed)


if __name__ == '__main__':
    unittest.main()
