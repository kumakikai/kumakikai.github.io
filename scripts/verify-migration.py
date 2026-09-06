#!/usr/bin/env python3
"""Check the Hugoplate migration against an immutable pre-migration Hugo build.

Usage:
  python3 scripts/verify-migration.py public --baseline /path/to/papermod-build
  python3 scripts/verify-migration.py --snapshot /path/to/papermod-build --output /tmp/baseline.json

Uses Python's standard library and never accesses the network. A passing result
proves generated route/content/link integrity, not a successful live deployment.
Visual, keyboard, browser, external App Store, and Lighthouse checks are separate.
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

SITE = "https://kumakikai.github.io"
LOCAL_HOSTS = {"kumakikai.github.io", "localhost", "127.0.0.1", "::1"}
LANGUAGES = ("ja", "en", "ko", "de", "zh-hant", "fr")
FEATURED = ("uni-note", "oto-miru", "giga-poke", "nocca")
OTHER = ("uni-note-pocket", "balance-calendar", "smokeless", "signal")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
LEGACY_SECTIONS = {"htu", "faq", "privacy", "terms", "notes"}
DEMO_TEXT = re.compile(r"\blorem ipsum\b|\bJohn Doe\b|\bJane Doe\b|\bYour Company\b|\bAcme Inc\b|\bHugoplate Demo\b", re.I)


def normalized(value):
    return re.sub(r"\s+", "", value)


def route_for(path):
    value = "/" + path.as_posix()
    return value[:-10] if value.endswith("index.html") else value


def localized(lang, route):
    return route if lang == "ja" else "/" + lang + route


class Node:
    def __init__(self, tag, attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.parts = []

    def has_class(self, value):
        return value in self.attrs.get("class", "").split()

    def descendants(self, tag=None):
        for node in self.parts:
            if isinstance(node, Node):
                if tag is None or node.tag == tag:
                    yield node
                yield from node.descendants(tag)

    def text(self):
        if self.tag in {"style", "script"} or self.has_class("anchor") or self.has_class("heading-anchor"):
            return ""
        return " ".join(part if isinstance(part, str) else part.text() for part in self.parts)


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
        self.stack[-1].parts.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].parts.append(data)

    def tagged(self, tag):
        return [n for n in self.nodes if n.tag == tag]

    def body_content(self):
        return next((n for n in self.nodes if n.has_class("post-content") or "data-content-body" in n.attrs), None)

    def redirect(self):
        for node in self.tagged("meta"):
            if node.attrs.get("http-equiv", "").lower() == "refresh":
                match = re.search(r"url\s*=\s*(.+)$", node.attrs.get("content", ""), re.I)
                if match:
                    return match.group(1).strip(" '\"")
        return None

    def meta(self, key):
        return [n.attrs.get("content", "") for n in self.tagged("meta") if n.attrs.get("name") == key or n.attrs.get("property") == key]

    def canonical(self):
        return [n.attrs.get("href", "") for n in self.tagged("link") if "canonical" in n.attrs.get("rel", "").split()]


def snapshot(build):
    result = {"build": str(build.resolve()), "html_routes": [], "redirects": {}, "articles": {}, "home_app_copy": {}, "nonredirect_canonicals": {}, "sitemaps": {}, "robots": {}}
    for path in sorted(build.rglob("*.html")):
        route = route_for(path.relative_to(build))
        doc = Document(path.read_text(encoding="utf-8"))
        result["html_routes"].append(route)
        if doc.redirect():
            result["redirects"][route] = doc.redirect()
        else:
            result["nonredirect_canonicals"][route] = doc.canonical()
        if route in {localized(lang, "/") for lang in LANGUAGES}:
            copies = {}
            for node in doc.tagged("article"):
                app_id = node.attrs.get("aria-labelledby", "").removesuffix("-name")
                if app_id not in FEATURED + OTHER:
                    continue
                copies[app_id] = {"featured": node.has_class("app-showcase")}
                for field, class_name in (("tagline", "app-tagline"), ("description", "app-description")):
                    match = next((n for n in node.descendants() if n.has_class(class_name)), None)
                    if match:
                        copies[app_id][field] = normalized(match.text())
                if not copies[app_id]["featured"]:
                    paragraph = next(node.descendants("p"), None)
                    if paragraph:
                        copies[app_id]["description"] = normalized(paragraph.text())
                note = next((n for n in node.descendants() if n.has_class("app-note")), None)
                if note:
                    copies[app_id]["note"] = normalized(note.text())
                heading = next((n for n in node.descendants() if n.attrs.get("id") == app_id + "-name"), None)
                if heading:
                    copies[app_id]["name"] = normalized(heading.text())
            result["home_app_copy"][route] = copies
        content = doc.body_content()
        is_article = any(n.has_class("post-single") for n in doc.nodes)
        if content and is_article:
            result["articles"][route] = {
                "text": normalized(content.text()),
                "ids": [n.attrs["id"] for n in content.descendants() if n.attrs.get("id")],
                "links": [urljoin(SITE + route, n.attrs["href"]) for n in content.descendants("a") if n.attrs.get("href") and not n.has_class("anchor")],
            }
    for path in sorted(build.rglob("sitemap.xml")):
        xml = ET.parse(path)
        result["sitemaps"][str(path.relative_to(build))] = [node.text for node in xml.iter() if node.tag.endswith("}loc") or node.tag == "loc"]
    for path in sorted(build.rglob("robots.txt")):
        result["robots"][str(path.relative_to(build))] = path.read_text(encoding="utf-8")
    return result


class Verification:
    def __init__(self, build, baseline, data_file):
        self.build = build.resolve()
        self.baseline = baseline
        self.data_file = data_file
        self.docs = {}
        self.errors = []
        self.warnings = []
        self.counts = Counter()

    def require(self, condition, route, check, detail):
        if not condition:
            self.errors.append({"page": route, "check": check, "detail": detail})

    def document(self, path):
        if path not in self.docs:
            self.docs[path] = Document(path.read_text(encoding="utf-8"))
        return self.docs[path]

    def target(self, value, current):
        parsed = urlsplit(urljoin(SITE + current, value))
        if parsed.scheme not in {"https", "http"} or parsed.hostname not in LOCAL_HOSTS:
            return None
        path = (self.build / unquote(parsed.path).lstrip("/")).resolve()
        if path != self.build and self.build not in path.parents:
            raise ValueError("Reference escapes build directory")
        if parsed.path.endswith("/") or path.is_dir():
            path /= "index.html"
        return path, unquote(parsed.fragment)

    def reference(self, value, current, kind):
        if not value or value.startswith("javascript:"):
            self.require(False, current, "reference", f"Empty or JavaScript {kind}: {value}")
            return
        try:
            target = self.target(value, current)
        except ValueError as error:
            self.require(False, current, "reference", str(error))
            return
        if not target:
            return
        path, fragment = target
        self.counts["local_references"] += 1
        self.require(path.is_file(), current, "reference", f"Missing {kind}: {value}")
        if path.is_file() and fragment and path.suffix == ".html":
            self.require(fragment in self.document(path).ids, current, "fragment", f"Missing {kind} anchor: {value}")

    def verify_baseline(self):
        for route in self.baseline["html_routes"]:
            target = self.target(route, "/")
            self.require(target and target[0].is_file(), route, "legacy_url", "Pre-migration HTML route disappeared")
            self.counts["legacy_html_routes"] += 1
        original_direct = set(self.baseline["html_routes"]) - set(self.baseline["redirects"])
        original_canonicals = self.baseline.get("nonredirect_canonicals", {})
        self.require(set(original_canonicals) == original_direct, "/", "permanent_baseline", "Baseline must include original canonical metadata for every nonredirect URL")
        for route in sorted(original_direct):
            target = self.target(route, "/")
            if not target or not target[0].is_file():
                continue
            doc = self.document(target[0])
            self.require(not doc.redirect(), route, "permanent_direct_url", "An original content URL must never become a redirect to a new company/product URL")
            self.require(doc.canonical() == original_canonicals.get(route), route, "permanent_canonical", "Original canonical URL changed; externally registered URLs must retain their canonical identity")
            self.counts["permanent_direct_urls"] += 1
        for route, destination in self.baseline["redirects"].items():
            target = self.target(route, "/")
            if not target or not target[0].is_file():
                continue
            doc = self.document(target[0])
            self.require(doc.redirect() == destination, route, "permanent_alias", "Original compatibility alias destination changed")
            self.require(doc.canonical() == [destination], route, "permanent_alias", "Original compatibility alias canonical destination changed")
            self.counts["permanent_aliases"] += 1
        for route, old in self.baseline["articles"].items():
            target = self.target(route, "/")
            if not target or not target[0].is_file():
                continue
            doc = self.document(target[0])
            body = doc.body_content()
            self.require(body is not None, route, "legacy_content", "Original article needs .post-content or data-content-body wrapper")
            if body is None:
                continue
            new_text = normalized(body.text())
            self.require(old["text"] in new_text, route, "legacy_content", "Original rendered article body was dropped, changed, or reordered")
            missing = sorted(set(old["ids"]) - set(doc.ids))
            self.require(not missing, route, "legacy_anchor", f"Original article anchors disappeared: {missing}")
            links = {urljoin(SITE + route, node.attrs["href"]) for node in body.descendants("a") if node.attrs.get("href")}
            missing_links = sorted(set(old["links"]) - links)
            self.require(not missing_links, route, "legacy_content_link", f"Original article links disappeared: {missing_links}")
            self.counts["legacy_articles"] += 1
        for sitemap, urls in self.baseline["sitemaps"].items():
            for url in urls:
                self.reference(url, "/", "legacy sitemap URL")

    def available(self, app):
        published = app.get("status") in {"published", "available"}
        availability = app.get("availability")
        if not availability:
            return published and bool(app.get("appStoreURL"))
        return published and bool(app.get("appStoreURL")) and availability.get("storefront") in availability.get("verifiedStorefronts", [])

    def verify_contract(self):
        apps = json.loads(self.data_file.read_text(encoding="utf-8"))
        if isinstance(apps, dict):
            apps = apps.get("apps", [])
        by_id = {app["id"]: app for app in apps}
        self.require(tuple(app["id"] for app in apps if app.get("featured")) == FEATURED,
                     "/", "featured_order", "Existing Featured classification/order must be preserved")
        self.require(tuple(app["id"] for app in apps if not app.get("featured")) == OTHER,
                     "/", "other_order", "Existing Other classification/order must be preserved")
        for app in apps:
            availability = app.get("availability")
            if availability and app.get("appStoreURL"):
                storefront = availability.get("storefront")
                self.require(storefront in availability.get("verifiedStorefronts", []), "/products/" + app["id"] + "/", "store_availability", "App Store CTA storefront has not been verified")
                store_path = urlsplit(app["appStoreURL"]).path.strip("/").split("/")
                self.require(bool(store_path) and store_path[0] == storefront, "/products/" + app["id"] + "/", "store_availability", "App Store URL country differs from verified CTA storefront")
                self.counts["verified_storefront_ctas"] += 1
        for lang in LANGUAGES:
            home_route = localized(lang, "/")
            home_target = self.target(home_route, "/")
            if home_target and home_target[0].is_file():
                home = self.document(home_target[0])
                for app_id, old in self.baseline.get("home_app_copy", {}).get(home_route, {}).items():
                    copy_file = self.data_file.parent / "home" / (lang + ".json")
                    if copy_file.is_file():
                        current_copy = json.loads(copy_file.read_text(encoding="utf-8"))["apps"][app_id]
                        for field in ("tagline", "description", "name", "note"):
                            if field not in old:
                                continue
                            current_value = "".join(current_copy.get("taglineLines", [])) if field == "tagline" else current_copy.get(field, "")
                            self.require(normalized(current_value) == old[field], home_route, "fixed_product_copy", f"{app_id}: accepted {field} copy changed")
                            self.require(old[field] in normalized(home.root.text()), home_route, "rendered_product_copy", f"{app_id}: accepted {field} is missing from rendered home")
                            self.counts["fixed_product_copy_fields"] += 1
                    containers = [n for n in home.nodes if n.attrs.get("aria-labelledby") == app_id + "-name" or n.attrs.get("data-app-id") == app_id]
                    self.require(len(containers) == 1, home_route, "home_product_container", f"{app_id}: expected one accessible Featured/Other app container")
                    if containers:
                        stores = [n.attrs.get("href") for n in containers[0].descendants("a") if urlsplit(n.attrs.get("href", "")).hostname == "apps.apple.com"]
                        app = by_id.get(app_id, {})
                        if self.available(app) and old["featured"]:
                            self.require(app.get("appStoreURL") in stores, home_route, "home_store_cta", f"{app_id}: published app needs a direct Store CTA")
                        elif not self.available(app):
                            self.require(not stores, home_route, "home_publication", f"{app_id}: development app has a Store CTA")
            for route in ("/", "/products/", "/support/", "/news/", "/company/"):
                translated = localized(lang, route)
                target = self.target(translated, "/")
                self.require(target and target[0].is_file(), translated, "required_route", "Required localized company route is missing")
                if target and target[0].is_file():
                    self.require(not self.document(target[0]).redirect(), translated, "required_route", "New company pages must contain real page content")
                self.counts["new_company_routes"] += 1
            for app_id, app in by_id.items():
                route = localized(lang, f"/products/{app_id}/")
                target = self.target(route, "/")
                self.require(target and target[0].is_file(), route, "product_route", "Localized product detail page is missing")
                if not target or not target[0].is_file():
                    continue
                doc = self.document(target[0])
                store_links = [node.attrs.get("href", "") for node in doc.tagged("a") if urlsplit(node.attrs.get("href", "")).hostname == "apps.apple.com"]
                if self.available(app):
                    self.require(app.get("appStoreURL") in store_links, route, "store_cta", "Published product must link to its verified App Store URL")
                else:
                    self.require(not store_links, route, "publication", "Development product must not have an App Store link")
                    if app.get("status") not in {"published", "available"}:
                        self.require(not app.get("appStoreURL"), route, "publication", "Development product data must not contain a download URL")
                self.counts["product_routes"] += 1

    def verify_seo(self, doc, route):
        title = doc.tagged("title")
        self.require(len(title) == 1 and title[0].text().strip(), route, "title", "Expected one nonempty title")
        description = doc.meta("description")
        self.require(len(description) == 1 and description[0].strip(), route, "description", "Expected one nonempty meta description")
        canonical = doc.canonical()
        self.require(len(canonical) == 1 and canonical[0].startswith(SITE + "/"), route, "canonical", "Expected one production canonical URL")
        if canonical:
            self.reference(canonical[0], route, "canonical")
        for key in ("og:title", "og:description", "og:type", "og:url", "og:image", "twitter:card"):
            values = doc.meta(key)
            self.require(len(values) == 1 and values[0].strip(), route, "seo", f"Expected one nonempty {key}")
        self.require(doc.meta("og:url") == canonical, route, "ogp", "Open Graph URL must match canonical")
        for key in ("og:image", "twitter:image"):
            for value in doc.meta(key):
                self.require(value.startswith(SITE + "/"), route, "ogp", f"Expected absolute production {key}")
                self.reference(value, route, key)
        language = doc.tagged("html")
        self.require(len(language) == 1 and language[0].attrs.get("lang"), route, "language", "Missing document language")
        favicons = [n for n in doc.tagged("link") if "icon" in n.attrs.get("rel", "").split()]
        self.require(bool(favicons), route, "favicon", "Missing favicon")
        for node in doc.tagged("script"):
            if node.attrs.get("type") == "application/ld+json":
                try:
                    json.loads("".join(part for part in node.parts if isinstance(part, str)))
                    self.counts["structured_data_blocks"] += 1
                except (ValueError, TypeError) as error:
                    self.require(False, route, "structured_data", f"Invalid JSON-LD: {error}")
        self.counts["seo_pages"] += 1

    def verify_pages(self):
        for path in sorted(self.build.rglob("*.html")):
            route = route_for(path.relative_to(self.build))
            doc = self.document(path)
            self.counts["html_pages"] += 1
            redirect = doc.redirect()
            if redirect:
                self.reference(redirect, route, "redirect")
                chain, current = {route}, redirect
                for _ in range(10):
                    target = self.target(current, route)
                    if not target or not target[0].is_file():
                        break
                    next_route = route_for(target[0].relative_to(self.build))
                    if next_route in chain:
                        self.require(False, route, "redirect_loop", f"Redirect cycle includes {next_route}")
                        break
                    chain.add(next_route)
                    current = self.document(target[0]).redirect()
                    if not current:
                        break
                self.counts["redirects"] += 1
                continue
            if not route.endswith("404.html"):
                self.verify_seo(doc, route)
            self.require(not DEMO_TEXT.search(doc.root.text()), route, "demo_content", "Hugoplate demo/placeholder text was published")
            for node in doc.nodes:
                for attr in ("href", "src", "poster"):
                    if attr in node.attrs:
                        self.reference(node.attrs[attr], route, attr)
                if "srcset" in node.attrs and not node.attrs["srcset"].startswith("data:"):
                    for item in node.attrs["srcset"].split(","):
                        if item.strip():
                            self.reference(item.strip().split()[0], route, "srcset")
                if node.tag == "img":
                    self.require("alt" in node.attrs, route, "image_alt", f"Image lacks alt attribute: {node.attrs.get('src')}")
                    if "/images/apps/" in node.attrs.get("src", ""):
                        dimensions = all(re.fullmatch(r"[1-9][0-9]*", node.attrs.get(key, "")) for key in ("width", "height"))
                        self.require(dimensions, route, "image_dimensions", "Product image must reserve width/height")
            duplicates = [key for key, count in Counter(doc.ids).items() if count > 1]
            self.require(not duplicates, route, "duplicate_id", f"Duplicate element IDs: {duplicates}")
        for path in sorted(self.build.rglob("sitemap.xml")):
            try:
                root = ET.parse(path).getroot()
                for node in root.iter():
                    if node.tag.endswith("}loc") or node.tag == "loc":
                        self.reference(node.text or "", "/", "sitemap")
                        self.counts["sitemap_entries"] += 1
            except ET.ParseError as error:
                self.require(False, str(path), "sitemap", str(error))
        robots = self.build / "robots.txt"
        self.require(robots.is_file(), "/robots.txt", "robots", "Missing robots.txt")
        if robots.is_file():
            text = robots.read_text(encoding="utf-8")
            self.require(not re.search(r"^Disallow:\s*/\s*$", text, re.M), "/robots.txt", "robots", "Production site is blocked from crawling")
            self.require(SITE + "/sitemap.xml" in text, "/robots.txt", "robots", "Missing production sitemap declaration")

    def run(self):
        self.verify_baseline()
        self.verify_contract()
        self.verify_pages()
        return {"ok": not self.errors, "build": str(self.build), "baseline": self.baseline["build"], "checks": dict(self.counts), "warnings": self.warnings, "errors": self.errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path, nargs="?")
    parser.add_argument("--baseline", type=Path, help="Original build directory or a JSON snapshot")
    parser.add_argument("--snapshot", type=Path, help="Only snapshot the original Hugo build")
    parser.add_argument("--output", type=Path, help="Write the full JSON result to a file")
    parser.add_argument("--apps", type=Path, default=Path(__file__).resolve().parents[1] / "data/apps.json")
    args = parser.parse_args()
    if args.snapshot:
        result = snapshot(args.snapshot)
    else:
        if not args.build or not args.baseline:
            parser.error("A build directory and --baseline are required")
        baseline = snapshot(args.baseline) if args.baseline.is_dir() else json.loads(args.baseline.read_text(encoding="utf-8"))
        result = Verification(args.build, baseline, args.apps).run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    if args.snapshot and args.output:
        print(json.dumps({"snapshot": str(args.output), "html_routes": len(result["html_routes"]), "articles": len(result["articles"]), "redirects": len(result["redirects"]), "sitemaps": len(result["sitemaps"])}, ensure_ascii=False))
    else:
        print(encoded, end="")
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
