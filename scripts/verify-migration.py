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
import hashlib
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
PRODUCT_AREAS = {
    "uni-note": "learning", "uni-note-pocket": "learning",
    "oto-miru": "communication", "nocca": "communication",
    "giga-poke": "utilities", "balance-calendar": "utilities",
    "smokeless": "utilities", "signal": "utilities",
}
# Keep the pre-migration snapshot immutable. The user explicitly authorized
# removing "専用" in these two Japanese sentences only; all remaining article
# text, IDs, links, URLs, and canonical identities keep the original checks.
AUTHORIZED_ARTICLE_REPLACEMENTS = {
    "/htu/uni-note/": ("対応環境:iPad専用ApplePencil", "対応環境:iPadApplePencil"),
    "/faq/uni-note/": ("対応端末は？iPad専用です。無料版に制限", "対応端末は？iPadです。無料版に制限"),
}
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

    def inside_template(self):
        parent = self.parent
        while parent:
            if parent.tag == "template":
                return True
            parent = parent.parent
        return False

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

    def visible_label(self):
        """Navigation labels omit decorative aria-hidden arrows, not article text."""
        if self.attrs.get("aria-hidden") == "true":
            return ""
        return " ".join(part if isinstance(part, str) else part.visible_label() for part in self.parts).strip()


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
            expected_text = old["text"]
            if route in AUTHORIZED_ARTICLE_REPLACEMENTS:
                before, after = AUTHORIZED_ARTICLE_REPLACEMENTS[route]
                self.require(expected_text.count(before) == 1, route, "authorized_article_change", "The explicitly authorized sentence must occur exactly once in the immutable baseline")
                expected_text = expected_text.replace(before, after, 1)
                self.require("iPad専用" not in new_text, route, "authorized_article_change", "The authorized iPad wording change was not applied")
                self.counts["authorized_article_wording_changes"] += 1
            self.require(expected_text in new_text, route, "legacy_content", "Original rendered article body was dropped, changed, or reordered beyond the exact authorized wording change")
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

    def verify_store_controls(self, container, app, lang, route, badges, show_regions=True):
        nodes = list(container.descendants())
        store_badges = [n for n in nodes if n.has_class("app-store-badge")]
        flags = [n for n in nodes if n.has_class("storefront-link")]
        self.require(not any(n.has_class("availability-note") for n in nodes), route, "store_controls", "Obsolete Japan-only availability note must be removed")
        if not self.available(app):
            self.require(not store_badges and not flags, route, "publication", "Development app must not have a Store badge or country links")
            return
        self.require(len(store_badges) == 1, route, "store_badge", f"{app['id']}: expected one official Store badge")
        if store_badges:
            badge = store_badges[0]
            self.require(badge.tag == "a" and badge.attrs.get("href") == app["appStoreURL"], route, "store_badge", "Primary badge must retain the existing verified Store URL")
            images = list(badge.descendants("img"))
            self.require(len(images) == 1, route, "store_badge", "Official badge requires one SVG image")
            if images:
                image = images[0]
                self.require(image.attrs.get("src") == badges[lang]["path"] and bool(image.attrs.get("alt", "").strip()), route, "store_badge", "Badge SVG and alternative text must match the display locale")
                try:
                    # HTML dimensions are unsigned integers; CSS/SVG retain the
                    # exact intrinsic ratio, which the browser check verifies.
                    dimensions = all(re.fullmatch(r"[1-9][0-9]*", image.attrs[key]) and abs(int(image.attrs[key]) - badges[lang][key]) <= .5 for key in ("width", "height"))
                    self.require(dimensions, route, "store_badge", "Badge must reserve the official dimensions rounded to valid integer attributes")
                except (KeyError, ValueError):
                    self.require(False, route, "store_badge", "Badge must reserve valid width and height")
        availability = app["availability"]
        expected = availability.get("verifiedStorefronts", []) if show_regions else []
        actual = [n.attrs.get("data-country") for n in flags]
        self.require(actual == expected, route, "storefront_links", f"{app['id']}: country links must match verified regions independently of display language")
        for flag in flags:
            country = flag.attrs.get("data-country")
            self.require(flag.tag == "a" and flag.attrs.get("href") == availability.get("storefrontURLs", {}).get(country), route, "storefront_links", "Country link must use its exact Apple-returned URL")
            self.require(bool(flag.attrs.get("aria-label", "").strip()) and bool(flag.attrs.get("title", "").strip()), route, "storefront_accessibility", "Country flags need an accessible name and readable title")
        self.counts["official_badge_instances"] += 1
        self.counts["storefront_link_instances"] += len(flags)

    def verify_product_support(self, doc, app, lang, route):
        intros = [n for n in doc.nodes if n.has_class("product-intro")]
        self.require(len(intros) == 1, route, "product_intro", "Product needs one introduction")
        if intros:
            actions = [n for n in intros[0].descendants() if n.has_class("app-actions")]
            action_links = [n for action in actions for n in action.descendants("a")]
            self.require(all(urlsplit(n.attrs.get("href", "")).hostname == "apps.apple.com" for n in action_links), route, "product_intro", "Product introduction must not repeat internal Support/Details buttons")
        sections = [n for n in doc.nodes if n.attrs.get("id") == "support" and n.tag == "section"]
        self.require(len(sections) == 1, route, "product_support", "Product needs a directly linkable #support section")
        if not sections:
            return
        hrefs = [n.attrs.get("href", "") for n in sections[0].descendants("a")]
        for kind in ("htu", "faq", "privacy", "terms"):
            original = f"/{kind}/{app['id']}/"
            preferred = localized(lang, original)
            target = self.target(preferred, route)
            if not target or not target[0].is_file():
                preferred = original
                target = self.target(preferred, route)
            if target and target[0].is_file():
                self.require(hrefs.count(preferred) == 1, route, "product_support", f"Expected one direct existing resource link: {preferred}")
                self.counts["direct_product_support_links"] += 1
        self.require(sum(urlsplit(href).scheme == "mailto" and urlsplit(href).path == "kumakikai.apps@gmail.com" for href in hrefs) == 1, route, "product_contact", "Product support needs one direct contact email link")
        self.require(not any(re.match(r"^/(?:en/|ko/|de/|zh-hant/|fr/)?support/", urlsplit(href).path) for href in hrefs), route, "product_support", "Product resources must not detour through the Support directory")

    def verify_product_content(self, doc, app, detail, lang, route):
        text = detail["locales"][lang]
        home = json.loads((self.data_file.parent / "home" / (lang + ".json")).read_text(encoding="utf-8"))
        ui = json.loads((self.data_file.parent / "product_ui" / (lang + ".json")).read_text(encoding="utf-8"))
        corporate = json.loads((self.data_file.parent / "corporate" / (lang + ".json")).read_text(encoding="utf-8"))
        sections = {}
        for name in ("overview", "features", "audience", "facts"):
            matches = [n for n in doc.tagged("section") if n.has_class("product-" + name)]
            self.require(len(matches) == 1, route, "product_sections", f"Expected one product {name} section")
            if matches:
                sections[name] = matches[0]
                labelled = matches[0].attrs.get("aria-labelledby")
                self.require(labelled and any(n.tag == "h2" and n.attrs.get("id") == labelled for n in matches[0].descendants()), route, "product_sections", f"Product {name} needs its own accessible heading")
        if len(sections) != 4:
            return
        self.require(sections["overview"].attrs.get("id") == "overview" and sections["features"].attrs.get("id") == "features", route, "product_sections", "Overview and features need stable section anchors")
        self.require(len(text["overview"]) == 2 and [n.text().strip() for n in sections["overview"].descendants("p")] == text["overview"], route, "product_overview", "The two overview paragraphs must match this locale's product data")
        self.require(normalized(text["overviewTitle"]) in normalized(sections["overview"].text()), route, "product_overview", "Localized overview heading is missing")
        for name in ("features", "audience"):
            expected = text[name]
            valid_count = 3 <= len(expected) <= 6 if name == "features" else len(expected) == 3
            self.require(valid_count, route, "product_content", f"Invalid {name} item count")
            items = list(sections[name].descendants("li"))
            self.require(len(items) == len(expected), route, "product_content", f"Rendered {name} list differs from product data")
            for item, source in zip(items, expected):
                self.require([n.text().strip() for n in item.descendants("h3")] == [source["title"]] and [n.text().strip() for n in item.descendants("p")] == [source["description"]], route, "product_content", f"Localized {name} title/description was omitted or altered")
        self.require(normalized(text["audienceTitle"]) in normalized(sections["audience"].text()), route, "product_content", "Localized audience heading is missing")
        stories = [n for n in doc.tagged("section") if n.has_class("product-story")]
        self.require(2 <= len(text["stories"]) <= 3 and len(stories) == len(text["stories"]), route, "product_stories", "Products need their two or three illustrated use cases")
        for story, source in zip(stories, text["stories"]):
            self.require([n.text().strip() for n in story.descendants("h2")] == [source["title"]] and [n.text().strip() for n in story.descendants("p")] == [source["description"]], route, "product_stories", "Localized use-case title/description differs from source data")
            if source.get("media"):
                shot = detail.get("media", {}).get(source["media"], {})
                alt = source.get("alt", "")
            else:
                index = source.get("image")
                valid = isinstance(index, int) and 0 <= index < len(app.get("screenshots", []))
                self.require(valid, route, "product_media", "Use-case screenshot index does not identify an existing asset")
                shot = app["screenshots"][index] if valid else {}
                alt = home["apps"][app["id"]]["imageAlts"][index] if valid else ""
            images = list(story.descendants("img"))
            self.require(bool(shot) and bool(alt) and len(images) == 1, route, "product_media", "Each use case needs one real image and localized alternative text")
            if images and shot:
                image = images[0]
                expected = {"src": shot["small"], "width": str(shot["width"]), "height": str(shot["height"]), "alt": alt, "loading": "lazy", "decoding": "async"}
                self.require(all(image.attrs.get(key) == value for key, value in expected.items()), route, "product_media", "Use-case image must preserve its asset, dimensions, alt, and lazy decoding")
                self.require(bool(image.attrs.get("sizes")) and shot["large"] in image.attrs.get("srcset", ""), route, "product_media", "Use-case image needs responsive sizes and its larger source")
                self.require([n.attrs.get("href") for n in story.descendants("a")] == [shot["large"]], route, "product_media", "Use-case image must open the real larger asset")
            self.counts["product_story_images"] += 1
        facts = sections["facts"]
        labels = [n.text().strip() for n in facts.descendants("dt")]
        values = [n.text().strip() for n in facts.descendants("dd")]
        expected_labels, expected_values = [ui["platform"]], [home["apps"][app["id"]]["platform"]]
        if detail.get("minimumOS"):
            expected_labels.append(ui["os"])
            expected_values.append(ui["minimumOSFormat"] % detail["minimumOS"])
        expected_labels += [ui["developer"], ui["status"]]
        expected_values += ["KUMAKIKAI", corporate["available"] + " · App Store" if self.available(app) else home["development"]]
        self.require(len(list(facts.descendants("dl"))) == 1 and labels == expected_labels and values == expected_values, route, "product_facts", "Platform, confirmed minimum OS, developer, and publication status must match verified data")
        notes = [n for n in facts.descendants() if n.has_class("product-notes")]
        rendered_notes = [n.text().strip() for group in notes for n in group.descendants("li")]
        self.require(rendered_notes == text.get("notes", []), route, "product_facts", "Product-specific limitations must remain visible")
        price_notes = [n.text().strip() for n in facts.descendants() if n.has_class("product-price-note")]
        self.require(price_notes == ([ui["priceNote"]] if self.available(app) else []), route, "product_facts", "Pricing guidance must refer published products to the Store without invented prices")
        ordered = [sections["overview"], sections["features"]] + stories + [sections["audience"], facts]
        self.require([doc.nodes.index(n) for n in ordered] == sorted(doc.nodes.index(n) for n in ordered), route, "product_sections", "Product information sections are out of order")
        self.counts["expanded_product_pages"] += 1

    def verify_products_hub(self, doc, apps, lang, route):
        cards = [n for n in doc.nodes if n.has_class("product-card")]
        self.require([n.attrs.get("data-app-id") for n in cards] == [app["id"] for app in apps], route, "products_hub", "Products must list the same eight apps in every display language")
        for card in cards:
            app_id = card.attrs.get("data-app-id")
            for class_name, suffix in (("product-view", ""), ("product-support", "#support")):
                links = [n for n in card.descendants("a") if n.has_class(class_name)]
                expected = localized(lang, f"/products/{app_id}/") + suffix
                self.require(len(links) == 1 and links[0].attrs.get("href") == expected, route, "products_hub", f"{app_id}: card needs one direct {class_name} link")
                if links:
                    self.require(bool(links[0].text().strip()) and bool(links[0].attrs.get("aria-label", "").strip()), route, "products_hub_accessibility", f"{app_id}: card links need readable app-specific labels")
            self.require(len(list(card.descendants("a"))) == 2, route, "products_hub", f"{app_id}: use the product and product-support actions without extra selection routes")
        self.counts["products_hub_cards"] += len(cards)

    def verify_about(self, doc, apps, lang, route):
        copy = json.loads((self.data_file.parent / "company" / (lang + ".json")).read_text(encoding="utf-8"))
        self.require(copy.get("founderName") == "Yuya Nakamura" and "founderEnglishName" not in copy, route, "about_founder", "About uses one authorized Roman-name field in every locale")
        self.require("webLabel" not in copy and "buildIntro" not in copy, route, "about_copy", "About must omit the redundant Web label and category introduction")
        title = doc.tagged("title")
        self.require(len(title) == 1 and re.match(r"^About(?:\s|$)", title[0].text()), route, "about_title", "The page title must be About while retaining /company/")
        facts = [n for n in doc.nodes if n.has_class("company-facts")]
        corp = json.loads((self.data_file.parent / "corporate" / (lang + ".json")).read_text(encoding="utf-8"))
        self.require(len(facts) == 1 and [n.text().strip() for n in facts[0].descendants("dt")] == [corp["companyNameLabel"], copy["founderLabel"], corp["businessLabel"]], route, "about_facts", "Basic information contains only the brand, developer, and business activity")
        self.require(len(facts) == 1 and "kumakikai.apps@gmail.com" not in facts[0].text(), route, "about_contact", "The contact email must not be duplicated in basic information")
        areas = copy.get("areas", [])
        self.require([area.get("area") for area in areas] == ["learning", "communication", "utilities"], route, "about_areas", "About must cover the three explicit product areas")
        for area in areas:
            groups = [n for n in doc.nodes if n.has_class("company-area-products") and n.attrs.get("data-area") == area["area"]]
            self.require(len(groups) == 1 and groups[0].attrs.get("data-product-selection") == "1", route, "about_selection", "Each area needs one single-product selection group")
            if not groups:
                continue
            group = groups[0]
            links = [n for n in group.descendants("a") if n.has_class("company-product-link")]
            active = [n for n in links if not n.inside_template()]
            candidates = [app for app in apps if app.get("area") == area["area"]]
            self.require(len(active) == 1 and active[0].attrs.get("data-product-id") == area["product"], route, "about_static_fallback", "Each area must preserve its one static fallback without JavaScript")
            self.require(Counter(n.attrs.get("data-product-id") for n in links) == Counter(app["id"] for app in candidates), route, "about_candidates", "Fallback plus inert templates must contain every product from the area exactly once")
            for link in links:
                app_id = link.attrs.get("data-product-id")
                self.require("data-product-option" in link.attrs and link.attrs.get("href") == localized(lang, f"/products/{app_id}/"), route, "about_direct_product", "Area representatives must link directly to their localized Product page")
            self.counts["about_static_representatives"] += len(active)
            self.counts["about_inert_candidates"] += len(links) - len(active)

    def verify_compatibility_page(self, doc, apps, lang, route, section):
        self.require(not doc.redirect() and doc.canonical() == [SITE + route], route, "directory_compatibility", "Old directory URLs must remain real pages with their own canonical")
        robots = " ".join(doc.meta("robots"))
        self.require(re.search(r"\bnoindex\b", robots) and re.search(r"\bfollow\b", robots), route, "directory_compatibility", "Compatibility directories must use noindex, follow")
        self.require(not any(n.has_class("privacy-directory-links") or n.has_class("product-card") or n.has_class("support-grid") or n.has_class("support-card") or (n.tag == "article" and n.parent.has_class("legacy-list")) for n in doc.nodes), route, "directory_compatibility", "Compatibility directories must not duplicate the Products app list")
        main = doc.tagged("main")
        links = list(main[0].descendants("a")) if main else []
        products = localized(lang, "/products/")
        self.require(sum(n.attrs.get("href") == products for n in links) == 1, route, "directory_compatibility", "Compatibility notice needs one direct Products link")
        if section != "support":
            self.require(len(links) == 1, route, "directory_compatibility", "Resource compatibility notice needs only the Products destination")
        else:
            for app in apps:
                targets = [n for n in doc.nodes if n.attrs.get("id") == app["id"]]
                expected = localized(lang, f"/products/{app['id']}/#support")
                self.require(len(targets) == 1 and [n.attrs.get("href") for n in targets[0].descendants("a")] == [expected], route, "support_hash_compatibility", f"Old #{app['id']} links must reach the product's support section")
                self.require(len(targets) == 1 and any(n.attrs.get("id") == "support-" + app["id"] for n in targets[0].descendants()), route, "support_hash_compatibility", f"Old #support-{app['id']} heading fragment must remain inside its support notice")
                self.counts["support_compatibility_targets"] += 1
            contacts = [n for n in doc.nodes if n.attrs.get("id") == "contact"]
            contact_links = list(contacts[0].descendants("a")) if contacts else []
            self.require(len(contacts) == 1 and len(contact_links) == 1 and urlsplit(contact_links[0].attrs.get("href", "")).scheme == "mailto", route, "support_hash_compatibility", "Old #contact links must retain direct contact access")
        self.counts[section + "_compatibility_pages"] += 1

    def verify_contract(self):
        apps = json.loads(self.data_file.read_text(encoding="utf-8"))
        if isinstance(apps, dict):
            apps = apps.get("apps", [])
        by_id = {app["id"]: app for app in apps}
        details = {app["id"]: json.loads((self.data_file.parent / "product_details" / (app["id"] + ".json")).read_text(encoding="utf-8")) for app in apps}
        for app_id, detail in details.items():
            self.require(set(detail.get("locales", {})) == set(LANGUAGES), "/products/" + app_id + "/", "product_locales", "Every product requires all six localized content records")
            original = detail["locales"]["ja"]
            for lang, text in detail["locales"].items():
                self.require(all(len(text.get(key, [])) == len(original.get(key, [])) for key in ("overview", "features", "stories", "audience", "notes")), localized(lang, f"/products/{app_id}/"), "product_locales", "Localized product sections and limitations must retain the same information structure")
                if lang != "ja":
                    self.require(normalized("".join(text.get("overview", []))) != normalized("".join(original.get("overview", []))), localized(lang, f"/products/{app_id}/"), "product_locales", "Product overview must use its translation instead of silently repeating Japanese")
        news_metadata = json.loads((self.data_file.parent / "news.json").read_text(encoding="utf-8"))
        badges = json.loads((self.data_file.parent / "app-store-badges.json").read_text(encoding="utf-8"))
        evidence_path = self.data_file.parent.parent / "docs/ux/storefront-verification.json"
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        for lang in LANGUAGES:
            badge = badges[lang]
            target = self.target(badge["path"], "/")
            self.require(target and target[0].is_file(), "/", "official_badge", f"Missing localized official badge: {lang}")
            if target and target[0].is_file():
                self.require(hashlib.sha256(target[0].read_bytes()).hexdigest() == badge["sha256"], "/", "official_badge", f"Official {lang} SVG was modified")
            self.require(urlsplit(badge["source"]).hostname == "toolbox.marketingtools.apple.com", "/", "official_badge", "Badge provenance must be Apple's official marketing tools")
            self.counts["official_badge_assets"] += 1
        ids = [app["id"] for app in apps]
        self.require(len(ids) == len(set(ids)) and tuple(app_id for app_id in ids if app_id in FEATURED + OTHER) == FEATURED + OTHER,
                     "/", "product_order", "Existing products must retain their relative order and every product ID must be unique; new apps may be added")
        eligible = [app for app in apps if app.get("featured") is True]
        candidates = [app["id"] for app in eligible if app["id"] != "uni-note"]
        self.require(by_id.get("uni-note", {}).get("featured") is True and len(candidates) >= 3,
                     "/", "featured_candidates", "Uni:Note must remain eligible and fixed first, with at least three other selectable products")
        self.require(all(app.get("area") in set(PRODUCT_AREAS.values()) for app in apps) and all(by_id.get(app_id, {}).get("area") == area for app_id, area in PRODUCT_AREAS.items()),
                     "/company/", "product_areas", "Preserve known product areas; new products must use learning, communication, or utilities")
        for app in apps:
            availability = app.get("availability")
            if availability and app.get("appStoreURL"):
                storefront = availability.get("storefront")
                self.require(storefront in availability.get("verifiedStorefronts", []), "/products/" + app["id"] + "/", "store_availability", "App Store CTA storefront has not been verified")
                store_path = urlsplit(app["appStoreURL"]).path.strip("/").split("/")
                self.require(bool(store_path) and store_path[0] == storefront, "/products/" + app["id"] + "/", "store_availability", "App Store URL country differs from verified CTA storefront")
                urls = availability.get("storefrontURLs", {})
                proof = evidence["apps"].get(app["id"], {})
                self.require(set(urls) == set(availability.get("verifiedStorefronts", [])), "/", "storefront_evidence", f"{app['id']}: each verified region needs an explicit URL")
                self.require(urls == proof.get("storefrontURLs"), "/", "storefront_evidence", f"{app['id']}: URLs must exactly match the stored Apple Lookup evidence")
                for country, url in urls.items():
                    parsed = urlsplit(url)
                    primary_id = re.search(r"/id(\d+)", app["appStoreURL"])
                    correct = parsed.scheme == "https" and parsed.hostname == "apps.apple.com" and parsed.path.startswith("/" + country + "/") and primary_id and re.search(r"/id" + primary_id.group(1) + r"(?:/|$)", parsed.path)
                    self.require(correct, "/", "storefront_evidence", f"{app['id']}/{country}: URL must identify the same app and verified Store region")
                    page_proof = evidence.get("pageEvidence", {}).get(app["id"], {}).get(country, {})
                    self.require(page_proof.get("url") == url and page_proof.get("httpStatus") == 200 and page_proof.get("sameAppAndStorefront") is True, "/", "storefront_evidence", f"{app['id']}/{country}: missing successful HTTP/app identity evidence")
                    self.counts["verified_storefront_urls"] += 1
                self.counts["verified_storefront_ctas"] += 1
        for lang in LANGUAGES:
            home_route = localized(lang, "/")
            home_target = self.target(home_route, "/")
            if home_target and home_target[0].is_file():
                home = self.document(home_target[0])
                home_copy = json.loads((self.data_file.parent / "home" / (lang + ".json")).read_text(encoding="utf-8"))
                self.require(home_copy["apps"]["uni-note"].get("platform") == "iPad", home_route, "ipad_wording", "Uni:Note platform must use iPad without an exclusivity claim in every language")
                for app_id, old in self.baseline.get("home_app_copy", {}).get(home_route, {}).items():
                    copy_file = self.data_file.parent / "home" / (lang + ".json")
                    if copy_file.is_file():
                        current_copy = json.loads(copy_file.read_text(encoding="utf-8"))["apps"][app_id]
                        for field in ("tagline", "description", "name", "note"):
                            if field not in old:
                                continue
                            current_value = "".join(current_copy.get("taglineLines", [])) if field == "tagline" else current_copy.get(field, "")
                            self.require(normalized(current_value) == old[field], home_route, "fixed_product_copy", f"{app_id}: accepted {field} copy changed")
                            if by_id.get(app_id, {}).get("featured") is True:
                                self.require(old[field] in normalized(home.root.text()), home_route, "rendered_product_copy", f"{app_id}: accepted {field} is missing from rendered home")
                            self.counts["fixed_product_copy_fields"] += 1
                for app in eligible:
                    app_id = app["id"]
                    containers = [n for n in home.tagged("article") if n.attrs.get("aria-labelledby") == app_id + "-name" or n.attrs.get("data-app-id") == app_id]
                    self.require(len(containers) == 1, home_route, "home_product_container", f"{app_id}: expected one accessible app showcase, including inert selection candidates")
                    if containers:
                        self.verify_store_controls(containers[0], by_id[app_id], lang, home_route, badges)
                        stores = [n.attrs.get("href") for n in containers[0].descendants("a") if urlsplit(n.attrs.get("href", "")).hostname == "apps.apple.com"]
                        app = by_id.get(app_id, {})
                        if self.available(app):
                            self.require(app.get("appStoreURL") in stores, home_route, "home_store_cta", f"{app_id}: published app needs a direct Store CTA")
                        elif not self.available(app):
                            self.require(not stores, home_route, "home_publication", f"{app_id}: development app has a Store CTA")
                showcases = [n for n in home.tagged("article") if n.has_class("app-showcase")]
                app_id = lambda n: n.attrs.get("data-product-id") or n.attrs.get("data-app-id") or n.attrs.get("aria-labelledby", "").removesuffix("-name")
                active = [n for n in showcases if not n.inside_template()]
                inert = [n for n in showcases if n.inside_template()]
                self.require([app_id(n) for n in active] == ["uni-note"] + candidates[:3], home_route, "home_static_fallback", "Without JavaScript Home must show Uni:Note followed by the first three eligible products in data order")
                self.require([app_id(n) for n in inert] == candidates[3:], home_route, "home_inert_candidates", "Remaining eligible showcases must stay in inert template content until selected")
                self.require(len(showcases) == len(eligible) and set(app_id(n) for n in showcases) == {app["id"] for app in eligible}, home_route, "home_selection_pool", "Home must contain every eligible showcase exactly once across the fallback and inert candidates")
                self.require(not any(n.has_class("app-disclosure") or n.has_class("portfolio-other") or n.has_class("other-apps") or n.attrs.get("id") == "other-apps" for n in home.nodes), home_route, "home_other_removed", "Home must not render a separate Other Apps section or collapsed product rows")
                self.require(not any(n.has_class("section-index") for n in home.nodes), home_route, "home_numbering", "Featured app numbering must remain removed")
                self.counts["home_static_showcases"] += len(active)
                self.counts["home_inert_showcases"] += len(inert)
                self.require(not any(n.has_class("home-support") or n.has_class("support-shortcuts") for n in home.nodes), home_route, "home_support", "Home must not repeat the Support app-selection section")
                old_support = [n for n in home.nodes if n.attrs.get("id") == "support"]
                self.require(len(old_support) == 1 and old_support[0].tag == "a" and old_support[0].attrs.get("href") == localized(lang, "/products/"), home_route, "home_support_compatibility", "The former Home #support anchor must now lead to Products")
            for route in ("/", "/products/", "/support/", "/news/", "/company/"):
                translated = localized(lang, route)
                target = self.target(translated, "/")
                self.require(target and target[0].is_file(), translated, "required_route", "Required localized company route is missing")
                if target and target[0].is_file():
                    self.require(not self.document(target[0]).redirect(), translated, "required_route", "New company pages must contain real page content")
                self.counts["new_company_routes"] += 1
            hub_route = localized(lang, "/products/")
            hub_target = self.target(hub_route, "/")
            if hub_target and hub_target[0].is_file():
                self.verify_products_hub(self.document(hub_target[0]), apps, lang, hub_route)
            about_route = localized(lang, "/company/")
            about_target = self.target(about_route, "/")
            if about_target and about_target[0].is_file():
                self.verify_about(self.document(about_target[0]), apps, lang, about_route)
            for section in ("privacy", "support", "htu", "faq", "terms"):
                compat_route = localized(lang, f"/{section}/")
                compat_target = self.target(compat_route, "/")
                if section in ("privacy", "support"):
                    self.require(compat_target and compat_target[0].is_file(), compat_route, "directory_compatibility", "Legacy directory must remain reachable")
                if compat_target and compat_target[0].is_file():
                    self.verify_compatibility_page(self.document(compat_target[0]), apps, lang, compat_route, section)
            news_route = localized(lang, "/news/")
            news_target = self.target(news_route, "/")
            if news_target and news_target[0].is_file():
                news = self.document(news_target[0])
                rows = [n for n in news.nodes if n.has_class("news-row")]
                categories = {n.attrs.get("data-category") for n in rows}
                labels_copy = json.loads((self.data_file.parent / "corporate" / (lang + ".json")).read_text(encoding="utf-8"))
                labels = {key: labels_copy[value] for key, value in (("press-release", "pressRelease"), ("blog", "blog"), ("information", "information"))}
                self.require(categories <= set(labels), news_route, "news_categories", "News contains an unknown category; empty categories need no placeholder articles")
                for row in rows:
                    dates = list(row.descendants("time"))
                    self.require(len(dates) == 1 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", dates[0].attrs.get("datetime", "")), news_route, "news_date", "Each News item needs a readable publication date")
                    links = list(row.descendants("a"))
                    self.require(len(links) == 1, news_route, "news_link", "Each News row needs one direct article link")
                    if links:
                        parts = urlsplit(links[0].attrs.get("href", "")).path.strip("/").split("/")
                        source_lang = parts[0] if parts[0] in LANGUAGES else "ja"
                        key = parts[-1]
                        expected = news_metadata.get(key, {}).get("category", "information")
                        if len(parts) >= 2:
                            directory = self.data_file.parent.parent / "content" / parts[-2]
                            source = directory / (key + ("" if source_lang == "ja" else "." + source_lang) + ".md")
                            if source.is_file():
                                text = source.read_text(encoding="utf-8")
                                front_matter = text.split("---", 2)[1] if text.startswith("---") else ""
                                override = re.search(r"^news_category:\s*([^\n#]+)", front_matter, re.M)
                                if override:
                                    expected = override.group(1).strip().strip("\"'")
                        category = row.attrs.get("data-category")
                        self.require(expected in labels and category == expected, news_route, "news_category_source", f"{key}: rendered category differs from the article metadata")
                        rendered_labels = [n.text().strip() for n in row.descendants() if n.has_class("news-category")]
                        self.require(rendered_labels == [labels.get(expected)], news_route, "news_category_label", f"{key}: category label differs from its data-category value")
                self.counts["news_category_pages"] += 1
            for app_id, app in by_id.items():
                route = localized(lang, f"/products/{app_id}/")
                target = self.target(route, "/")
                self.require(target and target[0].is_file(), route, "product_route", "Localized product detail page is missing")
                if not target or not target[0].is_file():
                    continue
                doc = self.document(target[0])
                self.verify_product_content(doc, app, details[app_id], lang, route)
                intro = [n for n in doc.nodes if n.has_class("product-intro")]
                download = [n for n in doc.nodes if n.has_class("product-download")]
                if intro:
                    self.verify_store_controls(intro[0], app, lang, route, badges)
                self.require(len(download) == int(self.available(app)), route, "product_download", "Published products need one lower download section; development products need none")
                if download:
                    self.verify_store_controls(download[0], app, lang, route, badges, show_regions=False)
                self.require(sum(n.has_class("app-store-badge") for n in doc.nodes) == (2 if self.available(app) else 0), route, "product_download", "Product Store badges belong only to the hero and lower download sections")
                self.require(sum(n.has_class("storefront-link") for n in doc.nodes) == len(app.get("availability", {}).get("verifiedStorefronts", [])), route, "storefront_links", "Product country links must appear only once in the hero")
                self.verify_product_support(doc, app, lang, route)
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
            lang = route.strip("/").split("/")[0]
            if lang not in LANGUAGES:
                lang = "ja"
            footer_tops = [n for n in doc.nodes if n.has_class("footer-top")]
            footer_nav_links = [link for top in footer_tops for nav in top.descendants("nav") for link in nav.descendants("a")]
            self.require([(n.text().strip(), n.attrs.get("href")) for n in footer_nav_links] == [("Contact", localized(lang, "/company/#contact"))], route, "footer_navigation", "Footer navigation must contain only Contact")
            navs = [n for n in doc.nodes if n.has_class("desktop-nav")]
            navs += [nav for menu in doc.nodes if menu.attrs.get("id") == "mobile-menu" for nav in menu.descendants("nav")]
            self.require(len(navs) == 2, route, "header_navigation", "Desktop and mobile navigation must both be present")
            for nav in navs:
                self.require([(n.visible_label(), n.attrs.get("href")) for n in nav.descendants("a")] == [(label, localized(lang, f"/{section}/")) for label, section in (("Products", "products"), ("News", "news"), ("About", "company"))], route, "header_navigation", "Primary navigation must use Products, News, and About while retaining /company/")
            if route.endswith("404.html"):
                self.require(not any(urlsplit(n.attrs.get("href", "")).path == localized(lang, "/support/") for n in doc.tagged("a")), route, "404_navigation", "404 recovery must lead to Products instead of the old Support directory")
            for aside in [n for n in doc.nodes if n.has_class("article-related")]:
                for resource in [n for n in aside.descendants() if n.has_class("resource-links")]:
                    for link in resource.descendants("a"):
                        target = self.target(link.attrs.get("href", ""), route)
                        self.require(not target or target[0] != path.resolve(), route, "support_self_link", "Related support resources must omit the current page")
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
