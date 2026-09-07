"""Protect the one authorized GigaPoke News email navigation change."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import news_contact_review as review

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "docs/migration/baseline.json").read_text())["articles"][review.ROUTE]


class NewsContactReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / review.SOURCE
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes((ROOT / review.SOURCE).read_bytes())

    def check(self, route=review.ROUTE, old=None, text=None, links=None):
        return review.check_article(
            self.root, route, BASELINE if old is None else old,
            review.expected_body(review.ROUTE, BASELINE) if text is None else text,
            review.expected_links(review.ROUTE, BASELINE) if links is None else links,
        )

    def test_exact_reviewed_change_is_accepted(self):
        self.assertEqual(self.check(), [])
        self.assertEqual(review.removed_links(review.ROUTE), [review.FORM])

    def test_source_contains_only_authorized_contact_and_lastmod_edits(self):
        text = self.source.read_text()
        new = "- [メールで問い合わせる](mailto:kumakikai.apps@gmail.com)"
        old = "- [お問い合わせフォーム](https://forms.gle/Enzmm94LdXRZjP8k9)\n- [kumakikai.apps@gmail.com](mailto:kumakikai.apps@gmail.com)"
        self.assertEqual(text.count(new), 1)
        self.assertEqual(text.count("lastmod: 2026-09-08"), 1)
        restored = text.replace(new, old, 1).replace("lastmod: 2026-09-08", "lastmod: 2026-09-07", 1)
        self.assertEqual(hashlib.sha256(restored.encode()).hexdigest(), "7e923cb2a0d7d7559c051e329b12714b4b1650d3d6b5ac05053cb6a4a598399e")

    def test_other_articles_products_and_languages_cannot_opt_in(self):
        for route in ["/notes/2026-09-06-nocca/", "/privacy/giga-poke/", "/terms/giga-poke/", "/en/notes/2026-09-02-giga-poke/", review.ROUTE.rstrip("/")]:
            with self.subTest(route=route):
                self.assertTrue(self.check(route=route))
                self.assertEqual(review.removed_links(route), [])

    def test_modified_baseline_text_links_and_anchors_are_rejected(self):
        for key in ["text", "links", "ids"]:
            old = copy.deepcopy(BASELINE)
            old[key] += "changed" if key == "text" else ["changed"]
            with self.subTest(key=key):
                self.assertTrue(self.check(old=old))

    def test_original_contact_label_is_rejected(self):
        self.assertTrue(self.check(text=BASELINE["text"]))

    def test_unrelated_text_changes_are_rejected(self):
        expected = review.expected_body(review.ROUTE, BASELINE)
        for text in [expected + "新たな説明", expected[1:], expected.replace("全機能無料", "一部有料", 1), expected.replace(review.NEW_CONTACT, "お問い合わせフォーム", 1)]:
            with self.subTest(text=text[-30:]):
                self.assertTrue(self.check(text=text))

    def test_form_variants_and_duplicate_contact_are_rejected(self):
        links = review.expected_links(review.ROUTE, BASELINE)
        for extra in [review.FORM, review.FORM + "?from=website", review.FORM + "#contact", "https://forms.gle/JwDoPvzAh1zKaR2M8", review.EMAIL]:
            with self.subTest(extra=extra):
                self.assertTrue(self.check(links=links + [extra]))

    def test_email_destination_and_query_changes_are_rejected(self):
        links = review.expected_links(review.ROUTE, BASELINE)
        for email in ["mailto:other@example.com", review.EMAIL + "?subject=changed", "https://example.com/contact", review.FORM]:
            with self.subTest(email=email):
                self.assertTrue(self.check(links=links[:-1] + [email]))

    def test_all_other_body_links_and_their_order_are_required(self):
        links = review.expected_links(review.ROUTE, BASELINE)
        for index in range(len(links)):
            with self.subTest(index=index):
                self.assertTrue(self.check(links=links[:index] + links[index + 1:]))
        self.assertTrue(self.check(links=list(reversed(links))))
        self.assertTrue(self.check(links=links + ["https://example.com/"]))

    def test_unrelated_source_or_date_changes_are_rejected(self):
        original = self.source.read_text()
        for text in [original + "\n追加\n", original.replace("date: 2026-09-02", "date: 2026-09-08", 1), original.replace("lastmod: 2026-09-08", "lastmod: 2026-09-07", 1)]:
            with self.subTest(text=text[-30:]):
                self.source.write_text(text)
                self.assertTrue(any(e["check"] == "news_contact_source" for e in self.check()))

    def test_missing_source_is_rejected(self):
        self.source.unlink()
        self.assertTrue(any(e["check"] == "news_contact_source" for e in self.check()))

    def test_symlinked_source_is_rejected(self):
        target = self.root / "article.md"
        target.write_bytes(self.source.read_bytes())
        self.source.unlink()
        self.source.symlink_to(target)
        self.assertTrue(any(e["check"] == "news_contact_source" for e in self.check()))


if __name__ == "__main__":
    unittest.main()
