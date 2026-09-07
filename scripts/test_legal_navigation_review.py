#!/usr/bin/env python3
"""Focused negative contracts for the four-page navigation-only exception."""
import copy
import json
from pathlib import Path
import unittest

import legal_navigation_review as review

BASELINE = json.loads((Path(__file__).resolve().parent.parent / "docs/migration/baseline.json").read_text())


class LegalNavigationReviewTests(unittest.TestCase):
    def check(self, route, text=None, links=None, support=None, old=None):
        original = BASELINE["articles"][route]
        return review.check_article(
            route, original if old is None else old,
            review.expected_body(route, original) if text is None else text,
            original["links"][:-3] if links is None else links,
            review.navigation_links(route) if support is None else support,
        )

    def test_exact_changes_accept_for_all_four_routes(self):
        self.assertEqual(len(review.SCOPE), 4)
        for route in review.SCOPE:
            with self.subTest(route=route):
                self.assertEqual(self.check(route), [])

    def test_original_or_missing_or_changed_clauses_rejected(self):
        for route in review.SCOPE:
            original = BASELINE["articles"][route]["text"]
            expected = review.expected_body(route, BASELINE["articles"][route])
            for text in (original, expected[1:], expected + "追加条項", expected.replace("お問い合わせ", "ご連絡", 1)):
                with self.subTest(route=route, text=text[:20]):
                    self.assertTrue(self.check(route, text=text))

    def test_incorrect_update_and_enactment_dates_rejected(self):
        for route, (_, _, old_date) in review.SCOPE.items():
            expected = review.expected_body(route, BASELINE["articles"][route])
            for date in (old_date, "2026-09-09", ""):
                with self.subTest(route=route, date=date):
                    self.assertTrue(self.check(route, text=expected.removesuffix(review.UPDATED) + date))
            if "giga-poke" in route:
                self.assertTrue(self.check(route, text=expected.replace("制定日:2026-09-02", "制定日:2026-09-08")))

    def test_missing_or_changed_baseline_block_rejected(self):
        for route in review.SCOPE:
            old = copy.deepcopy(BASELINE["articles"][route])
            for replacement in ("", "別のページ:"):
                with self.subTest(route=route, replacement=replacement):
                    old["text"] = BASELINE["articles"][route]["text"].replace("関連ページ:", replacement)
                    self.assertTrue(self.check(route, old=old))

    def test_baseline_link_changes_rejected(self):
        for route in review.SCOPE:
            for index in (0, -1):
                old = copy.deepcopy(BASELINE["articles"][route])
                old["links"][index] += "#changed"
                self.assertTrue(self.check(route, old=old))

    def test_missing_or_incorrect_relocated_links_rejected(self):
        for route in review.SCOPE:
            support = review.navigation_links(route)
            for destination in support:
                for replacement in (None, destination + "#section", destination + "?from=legal", destination.rstrip("/"),
                                    destination.replace("https:", "http:"), destination.replace(route.split("/")[2], "nocca")):
                    with self.subTest(route=route, replacement=replacement):
                        changed = [link for link in support if link != destination]
                        if replacement is not None:
                            changed.append(replacement)
                        self.assertTrue(self.check(route, support=changed))

    def test_every_non_navigation_link_must_stay_in_body(self):
        for route in review.SCOPE:
            links = BASELINE["articles"][route]["links"][:-3]
            for index in range(len(links)):
                with self.subTest(route=route, removed=links[index]):
                    # Presence in shared support never excuses a missing inline
                    # Privacy/EULA reference, email, form or service policy.
                    self.assertTrue(self.check(route, links=links[:index] + links[index + 1:], support=review.navigation_links(route) + links))
            self.assertTrue(self.check(route, links=links + ["https://example.com/"]))
            self.assertTrue(self.check(route, links=list(reversed(links))))

    def test_other_routes_cannot_opt_in(self):
        old = BASELINE["articles"]["/privacy/oto-miru/"]
        for route in ("/privacy/nocca/", "/terms/uni-note/", "/en/privacy/oto-miru/", "/faq/oto-miru/"):
            with self.subTest(route=route):
                self.assertEqual(review.navigation_links(route), [])
                self.assertTrue(review.check_article(route, old, old["text"], old["links"], old["links"]))
                with self.assertRaises(ValueError):
                    review.expected_body(route, old)


if __name__ == "__main__":
    unittest.main()
