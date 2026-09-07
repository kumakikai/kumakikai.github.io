#!/usr/bin/env python3
"""Small authored HTML cases for the offline site-structure audit."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "site_structure_audit", Path(__file__).with_name("audit-site-structure.py")
)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class SiteStructureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="site-structure-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.build = self.root / "build"
        self.source = self.root / "source"
        self.output = self.root / "report"
        self.build.mkdir()
        self.source.mkdir()

    def page(self, route, body, head=""):
        relative = route.lstrip("/")
        path = self.build / (relative + "index.html" if route.endswith("/") else relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "<!doctype html><html><head><title>Fixture</title>"
            + head + "</head><body><main>" + body + "</main></body></html>",
            encoding="utf-8",
        )

    def run_audit(self):
        with redirect_stdout(io.StringIO()):
            return audit.audit(self.build, self.source, self.output)

    def report(self, name):
        return json.loads((self.output / (name + ".json")).read_text(encoding="utf-8"))

    def test_fragments_and_queries_keep_distinct_destinations(self):
        self.page("/", """
            <a href="/products/example/">Product</a>
            <a href="/products/example/#support">Support</a>
            <a href="/products/example/#features">Features</a>
            <a href="/products/example/#質問">質問</a>
            <a href="/products/example/#%E8%B3%AA%E5%95%8F">よくある質問</a>
            <a href="/products/example/?view=compact#質問">簡易表示の質問</a>
        """)
        self.page("/products/example/", """
            <h1>Example</h1><h2 id="features">特徴</h2><h2 id="質問">質問</h2>
            <section class="product-resources" id="support"><h2>使い方とサポート</h2></section>
        """)
        result = self.run_audit()
        self.assertEqual(result["invalidAnchorReferences"], 0)
        self.assertEqual(result["duplicateDestinationGroups"], 1)
        duplicate = self.report("duplicate-links")[0]
        self.assertEqual(duplicate["destination"], audit.SITE + "/products/example/#質問")
        self.assertEqual(duplicate["count"], 2)
        self.assertEqual(duplicate["labels"], ["よくある質問", "質問"])
        self.assertEqual(len(self.report("different-label-links")), 1)
        destinations = {link["url"] for link in self.report("links")}
        self.assertEqual(len(destinations), 5)
        self.assertIn(audit.SITE + "/products/example/", destinations)
        self.assertIn(audit.SITE + "/products/example/#support", destinations)
        self.assertIn(audit.SITE + "/products/example/#features", destinations)
        self.assertIn(audit.SITE + "/products/example/?view=compact#質問", destinations)
        self.assertEqual(audit.structural_errors(self.output), [])

    def test_support_label_requires_the_support_section_not_just_an_existing_id(self):
        self.page("/", """
            <a href="/products/right/#support">Support <span aria-hidden="true">↓</span></a>
            <a href="/products/right/#features">Support</a>
            <a href="/products/wrong/#support">Support</a>
            <a href="/products/right/">Support</a>
        """)
        self.page("/products/right/", """
            <h1>Right</h1><h2 id="features">Features</h2>
            <section class="product-resources" id="support"><h2>使い方とサポート</h2></section>
        """)
        self.page("/products/wrong/", """
            <h1>Wrong</h1><section class="product-features" id="support"><h2>機能紹介</h2></section>
        """)
        result = self.run_audit()
        self.assertEqual(result["brokenInternalReferences"], 0)
        self.assertEqual(result["invalidAnchorReferences"], 0)
        semantics = {row["destination"]: row["status"] for row in self.report("anchor-label-semantics")}
        self.assertEqual(semantics[audit.SITE + "/products/right/#support"], "match")
        for target in ("/products/right/#features", "/products/wrong/#support", "/products/right/"):
            with self.subTest(target=target):
                self.assertEqual(semantics[audit.SITE + target], "review-label-target")
        self.assertEqual(len(audit.structural_errors(self.output)), 3)

    def test_missing_files_and_missing_anchors_are_separate_failures(self):
        self.page("/", """
            <a href="/missing/#also-missing">Missing page</a>
            <a href="/existing/#missing">Missing anchor</a>
            <a href="/existing/#present">Present anchor</a>
            <img src="/images/missing.webp" alt="Missing image">
            <a href="https://example.com/unknown/#anchor">External resource</a>
        """)
        self.page("/existing/", '<h1>Existing</h1><h2 id="present">Present</h2>')
        result = self.run_audit()
        self.assertEqual(result["brokenInternalReferences"], 2)
        self.assertEqual(result["invalidAnchorReferences"], 1)
        self.assertEqual({row["href"] for row in self.report("broken-links")},
                         {"/missing/#also-missing", "/images/missing.webp"})
        invalid = self.report("invalid-anchors")
        self.assertEqual(invalid[0]["href"], "/existing/#missing")
        self.assertFalse(any(row["kind"] == "external" for row in invalid))

    def test_duplicate_ids_are_reported_even_when_the_anchor_exists(self):
        self.page("/", '<a href="/repeated/#same">Section</a>')
        self.page("/repeated/", '<h2 id="same">First</h2><h2 id="same">Second</h2>')
        result = self.run_audit()
        self.assertEqual(result["invalidAnchorReferences"], 0)
        self.assertEqual(result["duplicateIDs"], 1)
        self.assertEqual(self.report("duplicate-ids"), [{"page": "/repeated/", "id": "same", "count": 2}])

    def test_body_and_shared_email_duplicates_keep_their_contexts(self):
        self.page("/", '<a href="/privacy/example/">Privacy</a><a href="/news/example/">News</a>')
        self.page("/privacy/example/", """
            <div class="post-content"><p><a href="mailto:support@example.com">メールで問い合わせる</a></p></div>
            <aside class="support-resources"><a href="mailto:support@example.com">お問い合わせ</a></aside>
        """)
        self.page("/news/example/", """
            <div class="post-content"><p><a href="mailto:support@example.com">support@example.com</a></p></div>
            <aside class="article-about"><a href="mailto:support@example.com">Contact</a></aside>
        """)
        result = self.run_audit()
        self.assertEqual(result["duplicateDestinationGroups"], 2)
        self.assertEqual(result["differentLabelGroups"], 2)
        duplicates = {row["page"]: row for row in self.report("duplicate-links")}
        for page, expected_contexts in (
            ("/privacy/example/", {"post-content", "support-resources"}),
            ("/news/example/", {"post-content", "article-about"}),
        ):
            with self.subTest(page=page):
                row = duplicates[page]
                self.assertEqual(row["destination"], "mailto:support@example.com")
                self.assertEqual(row["count"], 2)
                self.assertEqual({link["context"] for link in row["occurrences"]}, expected_contexts)
        self.assertEqual(audit.structural_errors(self.output), ['Repeated shared article contact: /news/example/'])

    def test_indexable_orphans_are_distinct_from_aliases_and_noindex_utilities(self):
        self.page("/", '<a href="/linked/">Linked page</a>')
        self.page("/linked/", "<h1>Linked page</h1>")
        self.page("/orphan/", '<h1 id="self">Orphan</h1><a href="#self">Self</a>')
        self.page("/old/", "<h1>Old alias</h1>",
                  '<meta http-equiv="refresh" content="0; url=/linked/">')
        self.page("/utility/", "<h1>Utility</h1>", '<meta name="robots" content="noindex, follow">')
        self.page("/cluster-a/", '<a href="/cluster-b/">B</a>')
        self.page("/cluster-b/", '<a href="/cluster-a/">A</a>')
        result = self.run_audit()
        self.assertEqual(result["aliases"], 1)
        self.assertEqual(result["indexableOrphans"], 3)
        orphans = {row["route"]: row for row in self.report("orphan-pages")}
        self.assertNotIn("/linked/", orphans)
        self.assertEqual(orphans["/old/"]["classification"], "compatibility-alias")
        self.assertEqual(orphans["/utility/"]["classification"], "noindex-legacy-or-utility")
        self.assertEqual(orphans["/orphan/"]["classification"], "indexable-orphan")
        self.assertEqual(orphans["/orphan/"]["inboundPages"], [])
        for route in ("/cluster-a/", "/cluster-b/"):
            with self.subTest(route=route):
                self.assertEqual(orphans[route]["classification"], "indexable-orphan")
                self.assertFalse(orphans[route]["reachableFromHome"])
                self.assertEqual(len(orphans[route]["inboundPages"]), 1)

    def test_legacy_related_blocks_do_not_match_the_current_support_heading(self):
        self.page("/", """
            <div class="post-content"><p>関連ページ:</p><h2>Related links</h2></div>
            <aside class="article-related"><h2>使い方とサポート</h2></aside>
        """)
        result = self.run_audit()
        self.assertEqual(result["genericRelatedBlocks"], 2)
        self.assertEqual({row["text"] for row in self.report("related-blocks")}, {"関連ページ:", "Related links"})


if __name__ == "__main__":
    unittest.main()
