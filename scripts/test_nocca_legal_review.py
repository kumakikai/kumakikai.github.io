#!/usr/bin/env python3
"""Local negative contracts; no network, publishing, or source mutation."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import nocca_legal_review as review

REPO = Path(__file__).resolve().parent.parent


class NoccaLegalReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.baseline = json.loads((REPO / "docs/migration/baseline.json").read_text())
        self.catalog = {"schemaVersion": 1, "purpose": review.PURPOSE, "reviews": {}}
        for route, (source, old_hash) in review.SCOPE.items():
            content = (REPO / source).read_bytes()
            target = self.root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            links = sorted(set(self.baseline["articles"][route]["links"]) - {review.BAD_FORM})
            self.catalog["reviews"][route] = {
                "source": source, "sourceSHA256": review.digest(content),
                "baselineTextSHA256": old_hash,
                "reviewedTextSHA256": review.digest("approved rendered text"),
                "reviewedLinks": links,
                "removedLinks": [review.BAD_FORM] if route == review.NOTES else [],
                "reason": "User-authorized Nocca-only legal update; independently reviewed.",
            }
        self.path = self.root / review.CATALOG
        self.path.parent.mkdir(parents=True)
        self.write()

    def write(self):
        self.path.write_text(json.dumps(self.catalog))

    def rejected(self):
        entries, errors = review.load_reviews(self.root, self.baseline)
        self.assertEqual(entries, {})
        self.assertTrue(errors)

    def test_exact_catalog_accepts(self):
        entries, errors = review.load_reviews(self.root, self.baseline)
        self.assertEqual(set(entries), set(review.SCOPE))
        self.assertEqual(errors, [])

    def test_missing_catalog_keeps_original_checks(self):
        self.path.unlink()
        self.assertEqual(review.load_reviews(self.root, self.baseline), ({}, []))

    def test_other_app_route_rejected(self):
        self.catalog["reviews"]["/privacy/other-app/"] = copy.deepcopy(next(iter(self.catalog["reviews"].values())))
        self.write()
        self.rejected()

    def test_missing_authorized_route_rejected(self):
        self.catalog["reviews"].pop("/terms/nocca/")
        self.write()
        self.rejected()

    def test_modified_baseline_rejected(self):
        self.baseline["articles"]["/privacy/nocca/"]["text"] += "extra"
        self.rejected()

    def test_updated_catalog_cannot_override_pinned_old_hash(self):
        self.catalog["reviews"]["/privacy/nocca/"]["baselineTextSHA256"] = "0" * 64
        self.write()
        self.rejected()

    def test_source_path_swap_rejected(self):
        self.catalog["reviews"]["/privacy/nocca/"]["source"] = "content/privacy/another.md"
        self.write()
        self.rejected()

    def test_extra_source_change_after_review_rejected(self):
        p = self.root / "content/privacy/nocca.md"
        p.write_text(p.read_text() + "\nUnreviewed additional promise.\n")
        self.rejected()

    def test_article_extra_change_even_rehashed_rejected(self):
        source = self.root / review.SCOPE[review.NOTES][0]
        source.write_text(source.read_text() + "\nUnrelated change.\n")
        self.catalog["reviews"][review.NOTES]["sourceSHA256"] = review.digest(source.read_bytes())
        self.write()
        self.rejected()

    def test_extra_catalog_field_rejected(self):
        self.catalog["allowAnyRoute"] = True
        self.write()
        self.rejected()

    def test_extra_removed_link_rejected(self):
        self.catalog["reviews"]["/privacy/nocca/"]["removedLinks"] = ["mailto:kumakikai.apps@gmail.com"]
        self.write()
        self.rejected()

    def test_form_remaining_in_source_even_rehashed_rejected(self):
        route = "/privacy/nocca/"
        source = self.root / review.SCOPE[route][0]
        source.write_text(source.read_text() + "\n[wrong form](" + review.BAD_FORM + ")\n")
        self.catalog["reviews"][route]["sourceSHA256"] = review.digest(source.read_bytes())
        self.write()
        self.rejected()

    def test_truncated_catalog_rejected(self):
        self.path.write_text('{"schemaVersion":')
        self.rejected()

    def test_reviewed_render_accepts(self):
        entry = self.catalog["reviews"]["/privacy/nocca/"]
        self.assertEqual(review.check_article("/privacy/nocca/", entry, "approved rendered text", entry["reviewedLinks"]), [])

    def test_extra_rendered_text_rejected(self):
        entry = self.catalog["reviews"]["/privacy/nocca/"]
        errors = review.check_article("/privacy/nocca/", entry, "approved rendered text plus extra", entry["reviewedLinks"])
        self.assertTrue(any(e["check"] == "nocca_legal_body" for e in errors))

    def test_extra_rendered_link_rejected(self):
        entry = self.catalog["reviews"]["/privacy/nocca/"]
        errors = review.check_article("/privacy/nocca/", entry, "approved rendered text", entry["reviewedLinks"] + ["https://example.com/unreviewed"])
        self.assertTrue(any(e["check"] == "nocca_legal_links" for e in errors))

    def test_form_in_render_rejected_even_if_catalog_includes_it(self):
        entry = copy.deepcopy(self.catalog["reviews"]["/privacy/nocca/"])
        entry["reviewedLinks"] = sorted(entry["reviewedLinks"] + [review.BAD_FORM])
        errors = review.check_article("/privacy/nocca/", entry, "approved rendered text", entry["reviewedLinks"])
        self.assertTrue(any(e["check"] == "nocca_legal_form" for e in errors))

    def test_other_render_route_rejected(self):
        entry = self.catalog["reviews"]["/privacy/nocca/"]
        self.assertTrue(review.check_article("/terms/another-app/", entry, "approved rendered text", entry["reviewedLinks"]))


    def test_exact_nocca_form_accepted_in_legal_source_and_render(self):
        for route in review.FORM_ROUTES:
            self.assertTrue(review.source_forms_allowed(route, "[Nocca](" + review.APPROVED_FORM + ")"))
            entry = copy.deepcopy(self.catalog["reviews"][route])
            entry["reviewedLinks"] = sorted(set(entry["reviewedLinks"] + [review.APPROVED_FORM]))
            self.assertEqual(review.check_article(route, entry, "approved rendered text", entry["reviewedLinks"]), [])

    def test_form_variants_rejected_even_if_reviewed(self):
        for form in (review.APPROVED_FORM + "?entry.123=diagnostics", review.APPROVED_FORM + "#fragment",
                     review.APPROVED_FORM + "/", review.APPROVED_FORM.replace("https:", "http:"),
                     review.APPROVED_FORM.replace("forms.gle", "forms.gle.evil.example"),
                     review.APPROVED_FORM.replace("forms.gle", "forms.gle@evil.example"),
                     "https://docs.google.com/forms/d/another-form/viewform", "https://forms.gle/another-form"):
            with self.subTest(form=form):
                self.assertFalse(review.source_forms_allowed("/privacy/nocca/", "[form](" + form + ")"))
                entry = copy.deepcopy(self.catalog["reviews"]["/privacy/nocca/"])
                entry["reviewedLinks"] = [form]
                errors = review.check_article("/privacy/nocca/", entry, "approved rendered text", [form])
                self.assertTrue(any(e["check"] == "nocca_legal_form" for e in errors))

    def test_google_forms_explicit_port_rejected_at_all_review_boundaries(self):
        route = "/privacy/nocca/"
        source = self.root / review.SCOPE[route][0]
        original = source.read_text()
        for form in ("https://docs.google.com:443/forms/d/another-form/viewform",
                     "https://docs.google.com.:443/forms/d/another-form/viewform",
                     "https://docs.google.com:443/%66orms/d/another-form/viewform"):
            with self.subTest(form=form):
                self.assertFalse(review.source_forms_allowed(route, "[form](" + form + ")"))
                self.assertFalse(review.form_links_allowed(route, [form]))
                entry = copy.deepcopy(self.catalog["reviews"][route])
                entry["reviewedLinks"] = [form]
                errors = review.check_article(route, entry, "approved rendered text", [form])
                self.assertTrue(any(e["check"] == "nocca_legal_form" for e in errors))
                source.write_text(original + "\n[form](" + form + ")\n")
                self.catalog["reviews"][route]["sourceSHA256"] = review.digest(source.read_bytes())
                self.write()
                self.rejected()

    def test_raw_or_non_http_form_references_rejected(self):
        for value in ("forms.gle/JwDoPvzAh1zKaR2M8", "//forms.gle/JwDoPvzAh1zKaR2M8",
                      "HTTPS://forms.gle/JwDoPvzAh1zKaR2M8", "https://FORMS.GLE/JwDoPvzAh1zKaR2M8"):
            with self.subTest(value=value):
                self.assertFalse(review.source_forms_allowed("/privacy/nocca/", value))

    def test_approved_form_cannot_expand_to_legacy_article_or_other_app(self):
        for route in (review.NOTES, "/privacy/other-app/"):
            self.assertFalse(review.source_forms_allowed(route, "[form](" + review.APPROVED_FORM + ")"))
            self.assertFalse(review.form_links_allowed(route, [review.APPROVED_FORM]))

    def test_approved_form_in_article_even_rehashed_still_rejected(self):
        source = self.root / review.SCOPE[review.NOTES][0]
        source.write_text(source.read_text() + "\n[Nocca](" + review.APPROVED_FORM + ")\n")
        self.catalog["reviews"][review.NOTES]["sourceSHA256"] = review.digest(source.read_bytes())
        self.write()
        self.rejected()

    def test_unreviewed_form_variant_in_real_source_rejected(self):
        route = "/privacy/nocca/"
        source = self.root / review.SCOPE[route][0]
        source.write_text(source.read_text() + "\n[form](" + review.APPROVED_FORM + "?prefill=1)\n")
        self.catalog["reviews"][route]["sourceSHA256"] = review.digest(source.read_bytes())
        self.write()
        self.rejected()


if __name__ == "__main__":
    unittest.main()
