"""Protect the exact scope of the Korean Privacy label correction."""
import copy
import json
from pathlib import Path
import unittest
from legal_terminology_review import ROUTE, expected_body, check_article


class TerminologyReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = json.loads((Path(__file__).resolve().parents[1] / 'docs/migration/baseline.json').read_text())['articles'][ROUTE]

    def test_only_feature_labels_and_date_change(self):
        result = expected_body(ROUTE, self.old)
        self.assertEqual(result.count('AI잔액'), 2)
        self.assertEqual(result.replace('AI잔액', 'AI잔량').removesuffix('2026-09-08') + '2026-06-28', self.old['text'])

    def test_other_languages_and_products_cannot_opt_in(self):
        for route in ['/privacy/uni-note/', '/ko/privacy/uni-note-pocket/', '/ko/faq/uni-note/']:
            with self.subTest(route=route), self.assertRaises(ValueError):
                expected_body(route, self.old)

    def test_modified_baseline_text_links_or_ids_are_rejected(self):
        for field in ['text', 'links', 'ids']:
            altered = copy.deepcopy(self.old)
            altered[field] += 'x' if field == 'text' else ['x']
            with self.subTest(field=field), self.assertRaises(ValueError):
                expected_body(ROUTE, altered)

    def test_adding_replacing_or_removing_links_is_rejected(self):
        text = expected_body(ROUTE, self.old)
        for links in [[], ['https://example.com/'], self.old['links'] + ['https://example.com/']]:
            with self.subTest(links=links), self.assertRaises(ValueError):
                check_article(ROUTE, self.old, text, links)

    def test_unrelated_text_change_is_rejected(self):
        with self.assertRaises(ValueError):
            check_article(ROUTE, self.old, expected_body(ROUTE, self.old) + 'new policy', self.old['links'])

    def test_reviewed_body_and_original_links_are_accepted(self):
        check_article(ROUTE, self.old, expected_body(ROUTE, self.old), self.old['links'])


if __name__ == '__main__':
    unittest.main()
