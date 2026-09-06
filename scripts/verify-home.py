#!/usr/bin/env python3
"""Verify a built Hugo portfolio without network access or third-party packages.

Usage:
    python3 scripts/verify-home.py /path/to/build --baseline /path/to/old-build

The optional baseline checks existing HTML URLs, including support and Notes.
Former home pagination URLs must redirect to the matching language's home.
"""

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


LANGUAGES = ("ja", "en", "ko", "de", "zh-hant", "fr")
SITE = "https://kumakikai.github.io"
LOCAL_HOSTS = {"kumakikai.github.io", "localhost", "127.0.0.1", "::1"}
FEATURED = {"uni-note", "oto-miru", "giga-poke", "nocca"}
OTHER = {"uni-note-pocket", "balance-calendar", "smokeless", "signal"}
STORE_IDS = {
    "uni-note": "6760258084",
    "oto-miru": "6770774613",
    "giga-poke": "6807501268",
    "uni-note-pocket": "6761449487",
    "balance-calendar": "6757731648",
    "smokeless": "6760842941",
    "signal": "6759493613",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
RETIRED_PAGINATION = re.compile(
    r"^(?:(?:en|ko|de|zh-hant|fr)/)?page/[0-9]+/index\.html$"
)


class Node:
    def __init__(self, tag, attrs=(), parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.children = []
        self.text = []

    def has_class(self, value):
        return value in self.attrs.get("class", "").split()

    def descendants(self, tag=None):
        for child in self.children:
            if tag is None or child.tag == tag:
                yield child
            yield from child.descendants(tag)

    def plain_text(self):
        return " ".join(self.text).strip()


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.feed(source)
        self.close()
        self.nodes = list(self.root.descendants())
        self.ids = [n.attrs["id"] for n in self.nodes if n.attrs.get("id")]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        for node in self.stack:
            node.text.append(data)

    def tagged(self, tag):
        return [node for node in self.nodes if node.tag == tag]

    def classed(self, value):
        return [node for node in self.nodes if node.has_class(value)]


class Verification:
    def __init__(self, build, baseline):
        self.build = build.resolve()
        self.baseline = baseline.resolve() if baseline else None
        self.errors = []
        self.warnings = []
        self.documents = {}
        self.references_checked = 0
        self.homes = []

    def error(self, page, check, detail):
        self.errors.append({"page": page, "check": check, "detail": detail})

    def require(self, condition, page, check, detail):
        if not condition:
            self.error(page, check, detail)

    def document(self, path):
        if path not in self.documents:
            try:
                self.documents[path] = Document(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as error:
                self.error(str(path), "read_html", str(error))
                return None
        return self.documents[path]

    def local_target(self, value, current_url):
        """Return (file, fragment) for local URLs, or None for external URLs."""
        parsed = urlsplit(urljoin(current_url, value))
        if parsed.scheme not in ("http", "https"):
            return None
        if parsed.hostname not in LOCAL_HOSTS:
            return None
        path = (self.build / unquote(parsed.path).lstrip("/")).resolve()
        if self.build != path and self.build not in path.parents:
            raise ValueError("Reference escapes the build directory")
        if parsed.path.endswith("/") or path.is_dir():
            path = path / "index.html"
        return path, unquote(parsed.fragment)

    def reference(self, value, current_url, page, kind):
        if not value:
            self.error(page, "internal_reference", f"Empty {kind}")
            return
        if value.lower().startswith("javascript:"):
            self.error(page, "internal_reference", f"JavaScript URL in {kind}")
            return
        try:
            target = self.local_target(value, current_url)
        except ValueError as error:
            self.error(page, "internal_reference", f"{kind}: {value}: {error}")
            return
        if target is None:
            return
        path, fragment = target
        self.references_checked += 1
        if not path.is_file():
            self.error(page, "internal_reference", f"Missing {kind} target: {value}")
            return
        if fragment and path.suffix.lower() in (".html", ".htm"):
            document = self.document(path)
            if document is not None and fragment not in document.ids:
                self.error(page, "fragment", f"Missing fragment in {kind}: {value}")

    def srcset(self, value, current_url, page, check_links=True):
        candidates = []
        for entry in value.split(","):
            parts = entry.strip().split()
            if len(parts) != 2 or not re.fullmatch(r"[1-9][0-9]*w", parts[1]):
                self.error(page, "srcset", f"Invalid width candidate: {entry}")
                continue
            candidates.append((parts[0], int(parts[1][:-1])))
            if check_links:
                self.reference(parts[0], current_url, page, "srcset")
        return candidates

    def verify_seo(self, doc, route):
        expected = SITE + route
        titles = doc.tagged("title")
        self.require(len(titles) == 1 and titles[0].plain_text() == "KUMAKIKAI",
                     route, "title", "Expected one title containing KUMAKIKAI")
        descriptions = [node.attrs.get("content", "").strip()
                        for node in doc.tagged("meta")
                        if node.attrs.get("name") == "description"]
        self.require(len(descriptions) == 1 and bool(descriptions[0]), route,
                     "description", "Expected one nonempty meta description")
        canonicals = [node.attrs.get("href") for node in doc.tagged("link")
                      if "canonical" in node.attrs.get("rel", "").split()]
        self.require(canonicals == [expected], route, "canonical",
                     f"Expected production canonical {expected}; got {canonicals}")
        og = {node.attrs.get("property"): node.attrs.get("content", "")
              for node in doc.tagged("meta")
              if node.attrs.get("property", "").startswith("og:")}
        for key in ("og:title", "og:description", "og:url", "og:type", "og:site_name"):
            self.require(bool(og.get(key, "").strip()), route, "ogp", f"Missing {key}")
        self.require(og.get("og:url") == expected, route, "ogp", "og:url differs from canonical")
        self.require(og.get("og:type") == "website", route, "ogp", "og:type must be website")
        if descriptions:
            self.require(og.get("og:description") == descriptions[0], route,
                         "ogp", "OG description differs from meta description")
        if not og.get("og:image"):
            self.warnings.append({"page": route, "check": "ogp_image",
                                  "detail": "No og:image is configured"})
        return {"canonical": canonicals[0] if canonicals else None,
                "description": descriptions[0] if descriptions else None,
                "og_image": bool(og.get("og:image"))}

    def verify_app(self, article, route, current_url, featured):
        app_id = article.attrs.get("aria-labelledby", "").removesuffix("-name")
        links = list(article.descendants("a"))
        store_links = [node for node in links
                       if urlsplit(node.attrs.get("href", "")).hostname == "apps.apple.com"]
        if app_id == "nocca":
            self.require(not store_links, route, "publication", "Nocca must not have an App Store CTA")
            self.require(any(node.has_class("app-status") for node in article.descendants()),
                         route, "publication", "Nocca must show its development status")
        elif app_id in STORE_IDS:
            expected = STORE_IDS[app_id]
            valid = len(store_links) == 1 and re.search(
                rf"/id{expected}(?:[/?#]|$)", store_links[0].attrs.get("href", ""))
            self.require(valid, route, "store_cta", f"{app_id}: expected one CTA for Store ID {expected}")
        details = [node for node in links if node.has_class("portfolio-text-link")]
        self.require(bool(details), route, "detail_cta", f"{app_id}: missing detail link")
        for link in details:
            target = self.local_target(link.attrs.get("href", ""), current_url)
            self.require(target is not None and target[0].suffix == ".html", route,
                         "detail_cta", f"{app_id}: detail link must lead to an existing site page")
        shots = [node for node in article.descendants("a") if node.has_class("app-screenshot")]
        if featured:
            self.require(1 <= len(shots) <= 3, route, "screenshots",
                         f"{app_id}: expected 1–3 real screenshots, found {len(shots)}")
        for index, shot in enumerate(shots):
            images = list(shot.descendants("img"))
            self.require(len(images) == 1, route, "screenshots", f"{app_id}: screenshot must contain one image")
            for img in images:
                attrs = img.attrs
                self.require(bool(attrs.get("alt", "").strip()), route, "image_alt",
                             f"{app_id}: screenshot {index + 1} lacks descriptive alt")
                for dimension in ("width", "height"):
                    self.require(bool(re.fullmatch(r"[1-9][0-9]*", attrs.get(dimension, ""))),
                                 route, "image_dimensions", f"{app_id}: invalid {dimension}")
                candidates = self.srcset(attrs.get("srcset", ""), current_url, route, check_links=False)
                widths = [width for _, width in candidates]
                self.require(len(set(widths)) >= 2, route, "responsive_image",
                             f"{app_id}: screenshot needs two distinct srcset widths")
                self.require(attrs.get("src") in [url for url, _ in candidates], route,
                             "responsive_image", f"{app_id}: src missing from srcset")
                self.require(bool(attrs.get("sizes")), route, "responsive_image", f"{app_id}: missing sizes")
                primary = app_id == "uni-note" and index == 0
                self.require(attrs.get("loading") == ("eager" if primary else "lazy"), route,
                             "image_loading", f"{app_id}: incorrect loading on screenshot {index + 1}")
                if primary:
                    self.require(attrs.get("fetchpriority") == "high", route,
                                 "image_loading", "Primary Uni:Note screenshot needs high fetch priority")
        return app_id, len(shots)

    def verify_home(self, lang):
        route = "/" if lang == "ja" else f"/{lang}/"
        path = self.build / route.lstrip("/") / "index.html"
        if not path.is_file():
            self.error(route, "home_exists", "Home index.html is missing")
            return
        doc = self.document(path)
        if doc is None:
            return
        current_url = SITE + route
        self.require(len(doc.tagged("h1")) == 1, route, "h1", "Expected exactly one h1")
        duplicates = [value for value, count in Counter(doc.ids).items() if count > 1]
        self.require(not duplicates, route, "duplicate_ids", f"Duplicate IDs: {duplicates}")
        featured = [self.verify_app(node, route, current_url, True)
                    for node in doc.classed("app-showcase")]
        other = [self.verify_app(node, route, current_url, False)
                 for node in doc.classed("portfolio-app-card")]
        featured_ids = [app_id for app_id, _ in featured]
        other_ids = [app_id for app_id, _ in other]
        self.require(len(featured_ids) == 4 and set(featured_ids) == FEATURED, route,
                     "featured_apps", f"Expected four Featured apps; got {featured_ids}")
        self.require(len(other_ids) == 4 and set(other_ids) == OTHER, route,
                     "other_apps", f"Expected four Other apps; got {other_ids}")
        self.require(not set(featured_ids) & set(other_ids), route, "app_overlap",
                     "Featured and Other apps must not overlap")
        for node in doc.nodes:
            for attribute in ("href", "src"):
                if attribute in node.attrs:
                    self.reference(node.attrs[attribute], current_url, route, f"{node.tag}[{attribute}]")
            if "srcset" in node.attrs:
                self.srcset(node.attrs["srcset"], current_url, route)
        seo = self.verify_seo(doc, route)
        self.homes.append({"language": lang, "route": route,
                           "featured": featured_ids, "other": other_ids,
                           "screenshots": sum(count for _, count in featured), "seo": seo})

    def verify_sitemap(self):
        seen = set()
        urls = set()

        def visit(path):
            if path in seen:
                return
            seen.add(path)
            if not path.is_file():
                self.error("sitemap", "exists", f"Missing {path.relative_to(self.build)}")
                return
            try:
                root = ET.parse(path).getroot()
            except (OSError, ET.ParseError) as error:
                self.error("sitemap", "xml", str(error))
                return
            for node in root.iter():
                if node.tag.rsplit("}", 1)[-1] != "loc" or not node.text:
                    continue
                url = node.text.strip()
                target = self.local_target(url, SITE + "/")
                if root.tag.rsplit("}", 1)[-1] == "sitemapindex" and target:
                    visit(target[0])
                else:
                    urls.add(url)

        visit(self.build / "sitemap.xml")
        for lang in LANGUAGES:
            url = SITE + ("/" if lang == "ja" else f"/{lang}/")
            self.require(url in urls, "sitemap", "home_entry", f"Missing home URL: {url}")
        return {"files": len(seen), "urls": len(urls)}

    def verify_home_aliases(self):
        aliases = {("" if lang == "ja" else f"{lang}/") + "page/1/index.html"
                   for lang in LANGUAGES}
        for root in (self.build, self.baseline):
            if root is not None and root.is_dir():
                aliases.update(path.relative_to(root).as_posix()
                               for path in root.rglob("*.html")
                               if RETIRED_PAGINATION.fullmatch(path.relative_to(root).as_posix()))
        checked = []
        for relative in sorted(aliases):
            path = self.build / relative
            first = relative.split("/", 1)[0]
            target = SITE + (f"/{first}/" if first in LANGUAGES else "/")
            route = "/" + relative.removesuffix("index.html")
            if not path.is_file():
                self.error(route, "home_alias", "Missing former-home pagination redirect")
                continue
            doc = self.document(path)
            if doc is None:
                continue
            canonicals = [node.attrs.get("href") for node in doc.tagged("link")
                          if "canonical" in node.attrs.get("rel", "").split()]
            refreshes = [node.attrs.get("content", "") for node in doc.tagged("meta")
                         if node.attrs.get("http-equiv", "").lower() == "refresh"]
            self.require(canonicals == [target], route, "home_alias",
                         f"Alias canonical must target {target}; got {canonicals}")
            match = re.fullmatch(r"0\s*;\s*url\s*=\s*(.+)", refreshes[0], re.IGNORECASE) if len(refreshes) == 1 else None
            self.require(match is not None and match.group(1).strip("\"'") == target,
                         route, "home_alias", f"Alias refresh must target {target}; got {refreshes}")
            self.reference(target, SITE + route, route, "alias target")
            checked.append({"route": route, "target": target})
        return checked

    def verify_baseline(self):
        if self.baseline is None:
            return {"checked": False}
        if not self.baseline.is_dir():
            self.error("baseline", "exists", f"Missing baseline directory: {self.baseline}")
            return {"checked": False}
        html = sorted(self.baseline.rglob("*.html"))
        self.require(bool(html), "baseline", "html", "Baseline contains no HTML files")
        preserved = 0
        retired = []
        support = 0
        for path in html:
            relative = path.relative_to(self.baseline)
            name = relative.as_posix()
            if not (self.build / relative).is_file():
                if RETIRED_PAGINATION.fullmatch(name):
                    retired.append(name)
                    continue
                self.error(name, "url_preservation", "Existing HTML URL missing from new build")
                continue
            preserved += 1
            if re.search(r"(?:^|/)(?:htu|faq|privacy|terms|notes)/", name):
                support += 1
        return {"checked": True, "baseline_html": len(html), "preserved_html": preserved,
                "preserved_support_and_notes": support, "retired_home_pagination": retired}

    def run(self):
        if not self.build.is_dir():
            self.error("build", "exists", f"Missing build directory: {self.build}")
        for lang in LANGUAGES:
            self.verify_home(lang)
        aliases = self.verify_home_aliases()
        sitemap = self.verify_sitemap()
        baseline = self.verify_baseline()
        return {"ok": not self.errors, "build": str(self.build),
                "homes": self.homes, "home_aliases": aliases,
                "sitemap": sitemap, "baseline": baseline,
                "internal_references_checked": self.references_checked,
                "warnings": self.warnings, "errors": self.errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path, help="Hugo output directory")
    parser.add_argument("--baseline", type=Path, help="Previous Hugo output for URL preservation checks")
    args = parser.parse_args()
    report = Verification(args.build, args.baseline).run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
