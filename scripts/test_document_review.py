"""Negative contracts for the explicitly authorized full document revision."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import document_review as r

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('migration', ROOT / 'scripts/verify-migration.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in r.PINNED:
            p = self.root / name; p.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / name, p)
        self.scope, self.before = r.inputs(self.root)
        self.baseline = json.loads((self.root / 'docs/migration/baseline.json').read_text())
        self.catalog = {'schemaVersion': 1, 'purpose': r.PURPOSE, 'reviews': {}}
        for route, source in self.scope.items():
            p = self.root / source; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('Fixture for ' + route)
            app = route.strip('/').split('/')[-1]
            evidence = [r.DIRECTORY + '/' + r.FAMILIES[app] + '-phase1.md', r.DIRECTORY + '/' + r.FAMILIES[app] + '-phase3.md']
            for name in evidence:
                (self.root / name).write_text('Reviewed implementation and wording evidence')
            old = self.baseline['articles'].get(route)
            self.catalog['reviews'][route] = {
                'source': source, 'sourceSHA256': r.digest(p.read_bytes()), 'beforeSourceSHA256': self.before.get(route, {}).get('sourceSHA256'),
                'baselineTextSHA256': r.digest(old['text']) if old else None, 'reviewedTextSHA256': r.digest('Reviewed text'),
                'reviewedLinks': [], 'removedLinks': sorted(set(old['links'])) if old else [],
                'reason': 'Deliberately reviewed product wording against current implementation evidence.', 'evidence': evidence,
            }
        self.path = self.root / r.CATALOG; self.write()

    def write(self):
        self.path.write_text(json.dumps(self.catalog))

    def rejected(self):
        rows, before, errors = r.load_reviews(self.root, self.baseline)
        self.assertEqual(rows, {}); self.assertEqual(before, {}); self.assertTrue(errors)

    def test_complete_catalog(self):
        rows, before, errors = r.load_reviews(self.root, self.baseline)
        self.assertEqual(len(rows), 74); self.assertEqual(len(before), 69); self.assertEqual(errors, [])

    def test_missing_catalog_fails_closed(self):
        self.path.unlink(); self.rejected()

    def test_news_cannot_opt_in(self):
        self.catalog['reviews']['/notes/new/'] = copy.deepcopy(next(iter(self.catalog['reviews'].values())))
        self.write(); self.rejected()

    def test_missing_document_fails(self):
        self.catalog['reviews'].pop('/privacy/nocca/'); self.write(); self.rejected()

    def test_immutable_inventory_cannot_be_rebaselined(self):
        (self.root / r.DIRECTORY / 'before/inventory.json').write_text('{}'); self.rejected()

    def test_source_change_fails(self):
        (self.root / 'content/privacy/nocca.md').write_text('Unreviewed change'); self.rejected()

    def test_wrong_source_path_fails(self):
        self.catalog['reviews']['/privacy/nocca/']['source'] = 'content/notes/anything.md'; self.write(); self.rejected()

    def test_original_body_change_fails(self):
        self.baseline['articles']['/privacy/nocca/']['text'] += 'changed'; self.rejected()

    def test_missing_product_evidence_fails(self):
        (self.root / r.DIRECTORY / 'learning-phase1.md').unlink(); self.rejected()

    def test_removed_links_must_be_exact(self):
        self.catalog['reviews']['/privacy/nocca/']['removedLinks'] = []; self.write(); self.rejected()

    def test_rendered_text_and_link_changes_fail(self):
        row = self.catalog['reviews']['/terms/signal/']
        good = m.Document('<div data-content-body><p>Reviewed text</p></div>')
        self.assertEqual(r.check_article('/terms/signal/', row, good, self.before), [])
        for html in ['<p>Extra text</p>', '<p>Reviewed text</p><a href="https://example.com/"></a>']:
            self.assertTrue(r.check_article('/terms/signal/', row, m.Document('<div data-content-body>' + html + '</div>'), self.before))

    def test_old_anchor_and_image_cannot_disappear(self):
        route = '/htu/signal/'; row = self.catalog['reviews'][route]
        doc = m.Document('<div data-content-body>Reviewed text</div>')
        errors = r.check_article(route, row, doc, self.before)
        self.assertTrue(any(e['check'].endswith('_anchors') for e in errors))
        self.assertTrue(any(e['check'].endswith('_images') for e in errors))

    def test_nocca_form_cannot_be_relabelled_to_other_form(self):
        route = '/privacy/nocca/'; row = copy.deepcopy(self.catalog['reviews'][route])
        doc = m.Document('<div data-content-body><a href="https://forms.gle/Enzmm94LdXRZjP8k9">Reviewed text</a></div>')
        row['reviewedLinks'] = r.body_links(route, doc.body_content())
        self.assertTrue(any(e['check'].endswith('_contact') for e in r.check_article(route, row, doc, self.before)))


if __name__ == '__main__':
    unittest.main()
