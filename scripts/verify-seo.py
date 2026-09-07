#!/usr/bin/env python3
"""Verify crawlable SEO directly in generated HTML, without JavaScript or network.

python3 scripts/verify-seo.py --build public --output docs/seo/verification.json
python3 scripts/verify-seo.py --build public --self-test

Uses only the standard library. Does not assert Google indexing, ranking, rich
result eligibility, live HTTP status or field Core Web Vitals. Those are separate.
The migration checker remains responsible for preserved bodies, links and images.
"""
import argparse
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

SITE = "https://kumakikai.github.io/"
LANGS = ("ja", "en", "ko", "de", "zh-hant", "fr")
HREFLANG = {"ja": "ja", "en": "en", "ko": "ko", "de": "de", "zh-hant": "zh-Hant", "fr": "fr"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
FORBIDDEN_CLAIMS = {"offers", "price", "priceCurrency", "aggregateRating", "ratingValue", "review", "reviewCount", "award", "alumniOf", "worksFor"}


def route_for(path):
    route = "/" + path.as_posix()
    return route[:-10] if route.endswith("index.html") else route


def lang_route(route):
    parts = route.lstrip("/").split("/", 1)
    if parts[0] in LANGS[1:]:
        return parts[0], "/" + (parts[1] if len(parts) > 1 else "")
    return "ja", route


def localized(lang, route):
    return route if lang == "ja" else "/" + lang + route


def compact(value):
    return re.sub(r"\s+", "", value)


def iso(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError):
        return None


def frontmatter_value(text, key):
    """Read a scalar/folded field from this site's YAML Markdown front matter.

    This deliberately is not a YAML implementation. Hugo remains the YAML
    parser; here we independently ensure editorial fields are declared rather
    than silently supplied by Summary/global fallbacks.
    """
    if not text.startswith("---\n"):
        return None
    block = text[4:].split("\n---", 1)[0]
    match = re.search(r"(?m)^" + re.escape(key) + r":[ \t]*(.*)$", block)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith((">", "|")) or not value:
        tail = block[match.end():]
        lines = []
        for line in tail.splitlines():
            if line and not line[0].isspace():
                break
            if line.strip():
                lines.append(line.strip())
        return " ".join(lines)
    if value.startswith('"'):
        try:
            return json.loads(value)
        except ValueError:
            return value.strip('"')
    return value.strip("'")


class Node:
    def __init__(self, tag, attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def visible_text(self):
        if self.tag in {"script", "style", "template"} or "hidden" in self.attrs or self.attrs.get("aria-hidden") == "true":
            return ""
        return "".join(c if isinstance(c, str) else c.visible_text() for c in self.children)

    def in_template(self):
        current = self.parent
        while current:
            if current.tag == "template":
                return True
            current = current.parent
        return False


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack, self.nodes = [self.root], []
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        self.nodes.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)

    def tagged(self, tag):
        return [n for n in self.nodes if n.tag == tag and not n.in_template()]

    def meta(self, name):
        return [n.attrs.get("content", "") for n in self.tagged("meta") if n.attrs.get("name", "").lower() == name or n.attrs.get("property", "").lower() == name]

    def links(self, rel):
        return [n for n in self.tagged("link") if rel in n.attrs.get("rel", "").split()]

    def noindex(self):
        return bool(re.search(r"\b(?:noindex|none)\b", ",".join(self.meta("robots") + self.meta("googlebot")), re.I))

    def redirect(self):
        return any(n.attrs.get("http-equiv", "").lower() == "refresh" for n in self.tagged("meta"))

    def redirect_target(self):
        for node in self.tagged("meta"):
            if node.attrs.get("http-equiv", "").lower() == "refresh":
                match = re.fullmatch(r"\s*0\s*;\s*url\s*=\s*(.+?)\s*", node.attrs.get("content", ""), re.I)
                if match:
                    return match.group(1).strip("\"'")
        return None

    def anchors(self, route):
        return {urljoin(SITE + route.lstrip("/"), n.attrs["href"]).split("#", 1)[0] for n in self.tagged("a") if n.attrs.get("href")}


class Audit:
    def __init__(self, build, source):
        self.build, self.source = build.resolve(), source.resolve()
        self.apps = json.loads((source / "data/apps.json").read_text())
        self.news = json.loads((source / "data/news.json").read_text())
        self.seo = {lang: json.loads((source / "data/seo" / f"{lang}.json").read_text()) for lang in LANGS}
        self.home = {lang: json.loads((source / "data/home" / f"{lang}.json").read_text()) for lang in LANGS}
        self.docs = {route_for(path.relative_to(build)): Document(path.read_text()) for path in sorted(build.rglob("*.html"))}
        self.errors, self.warnings, self.pages = [], [], []
        self.counts = Counter()
        self.sitemap = {}
        self.indexed = {route for route, doc in self.docs.items() if not doc.redirect() and not doc.noindex()}
        self.brand_id, self.person_id, self.website_id = SITE + "#brand", SITE + "company/#person", SITE + "#website"

    def require(self, condition, route, check, detail):
        if not condition:
            self.errors.append({"page": route, "check": check, "detail": detail})

    def content_file(self, route):
        lang, base = lang_route(route)
        suffix = "" if lang == "ja" else "." + lang
        stem = base.strip("/")
        candidates = ([self.source / "content" / (stem + suffix + ".md")] if stem else [])
        candidates += [self.source / "content" / stem / (name + suffix + ".md") for name in ("_index", "index")]
        return next((p for p in candidates if p.is_file()), None)

    def explicit_lastmod(self, route):
        path = self.content_file(route)
        if not path:
            return
        declared = frontmatter_value(path.read_text(), "lastmod")
        if declared:
            expected = iso(declared)
            actual = iso(self.sitemap.get(SITE + route.lstrip("/")))
            self.require(expected is not None and actual is not None and expected.date() == actual.date(), route, "declared_lastmod", {"source": declared, "sitemap": self.sitemap.get(SITE + route.lstrip("/"))})
            self.counts["explicit_lastmod_checked"] += 1

    def xml_sitemap(self):
        try:
            tree = ET.parse(self.build / "sitemap.xml")
            root = tree.getroot()
            self.require(root.tag.rsplit("}", 1)[-1] == "urlset", "/sitemap.xml", "sitemap_root", "Root sitemap must directly list all indexed languages")
            for item in root:
                fields = {node.tag.rsplit("}", 1)[-1]: node.text for node in item if node.tag.rsplit("}", 1)[-1] in {"loc", "lastmod"}}
                loc = fields.get("loc", "")
                self.require(loc not in self.sitemap, "/sitemap.xml", "sitemap_duplicate", loc)
                self.sitemap[loc] = fields.get("lastmod")
                if fields.get("lastmod"):
                    self.require(iso(fields["lastmod"]) is not None, loc, "sitemap_lastmod", fields["lastmod"])
        except (OSError, ET.ParseError) as error:
            self.require(False, "/sitemap.xml", "sitemap_parse", str(error))
        expected = {SITE + route.lstrip("/") for route in self.indexed}
        actual = set(self.sitemap)
        self.require(actual == expected, "/sitemap.xml", "sitemap_coverage", {"missing": sorted(expected - actual), "unexpected": sorted(actual - expected)})
        self.counts["sitemap_urls"] = len(actual)
        # Previously published per-language sitemap URLs remain usable.
        for lang in LANGS[1:]:
            path = self.build / lang / "sitemap.xml"
            try:
                tree = ET.parse(path)
                urls = {n.text for n in tree.iter() if n.tag.rsplit("}", 1)[-1] == "loc"}
                expected_lang = {SITE + r.lstrip("/") for r in self.indexed if lang_route(r)[0] == lang}
                self.require(urls == expected_lang, f"/{lang}/sitemap.xml", "localized_sitemap", {"missing": sorted(expected_lang - urls), "unexpected": sorted(urls - expected_lang)})
            except (OSError, ET.ParseError) as error:
                self.require(False, f"/{lang}/sitemap.xml", "sitemap_parse", str(error))

    def robots(self):
        try:
            text = (self.build / "robots.txt").read_text()
            # This site's intended policy is a public Allow /, without Disallow.
            entries = [(a.lower().strip(), b.strip()) for a, b in re.findall(r"^\s*([^:#\n]+):\s*([^\n]*)", text, re.M)]
            self.require(("user-agent", "*") in entries and ("allow", "/") in entries, "/robots.txt", "robots_allow", "Expected User-agent: * and Allow: /")
            self.require(not any(a == "disallow" and b for a, b in entries), "/robots.txt", "robots_block", "Unexpected crawl restriction")
            self.require(("sitemap", SITE + "sitemap.xml") in entries, "/robots.txt", "robots_sitemap", "Missing canonical root sitemap")
        except OSError as error:
            self.require(False, "/robots.txt", "robots_missing", str(error))

    def metadata(self, route, doc):
        url = SITE + route.lstrip("/")
        titles = [n.text().strip() for n in doc.tagged("title")]
        self.require(len(titles) == 1 and bool(titles[0]), route, "title", titles)
        title = titles[0] if titles else ""
        descriptions = doc.meta("description")
        self.require(len(descriptions) == 1 and bool(descriptions[0].strip()), route, "description", descriptions)
        description = descriptions[0] if descriptions else ""
        self.require(not doc.meta("keywords"), route, "keywords", "Do not add meta keywords")
        canonicals = [n.attrs.get("href") for n in doc.links("canonical")]
        self.require(canonicals == [url], route, "canonical", canonicals)
        self.require(doc.meta("og:title") == [title] and doc.meta("og:description") == [description], route, "og_text", "OG title/description must match source SEO fields")
        self.require(doc.meta("og:url") == [url] and doc.meta("og:site_name") == ["KUMAKIKAI"], route, "og_identity", "OG url/site name mismatch")
        self.require(doc.meta("twitter:title") == [title] and doc.meta("twitter:description") == [description], route, "twitter_text", "Twitter title/description mismatch")
        self.require(doc.meta("twitter:card") == ["summary_large_image"], route, "twitter_card", doc.meta("twitter:card"))
        images = doc.meta("og:image")
        self.require(len(images) == 1 and images == doc.meta("twitter:image"), route, "social_image", images)
        for image in images:
            parsed = urlsplit(image)
            self.require(image.startswith(SITE) and (self.build / unquote(parsed.path).lstrip("/")).is_file(), route, "social_image_exists", image)
        h1 = doc.tagged("h1")
        self.require(len(h1) == 1 and bool(h1[0].text().strip()), route, "h1", [n.text() for n in h1])
        language, _ = lang_route(route)
        html = doc.tagged("html")
        html_lang = html[0].attrs.get("lang", "") if html else ""
        self.require(html_lang.lower() == HREFLANG[language].lower() or html_lang.lower().startswith(HREFLANG[language].lower() + "-"), route, "html_lang", html_lang)
        for image in doc.tagged("img"):
            self.require("alt" in image.attrs, route, "image_alt", image.attrs.get("src"))
        for name in ("header", "nav", "main", "footer"):
            self.require(bool(doc.tagged(name)), route, "semantic_landmark", name)
        return title, description

    def alternates(self, route, doc):
        nodes = [n for n in doc.links("alternate") if n.attrs.get("hreflang")]
        pairs = [(n.attrs["hreflang"], n.attrs.get("href", "")) for n in nodes]
        self.require(len({lang for lang, _ in pairs}) == len(pairs), route, "hreflang_duplicate", pairs)
        links = dict(pairs)
        language, family = lang_route(route)
        expected = {HREFLANG[lang]: SITE + localized(lang, family).lstrip("/") for lang in LANGS if localized(lang, family) in self.indexed}
        if family in self.indexed:
            expected["x-default"] = SITE + family.lstrip("/")
        self.require(links == expected, route, "hreflang_family", {"expected": expected, "actual": links})
        for code, target in links.items():
            parsed = urlsplit(target)
            target_route = parsed.path
            self.require(target.startswith(SITE) and target_route in self.indexed, route, "hreflang_target", target)
            if target_route not in self.indexed or code == "x-default":
                continue
            reciprocal = {(n.attrs.get("hreflang"), n.attrs.get("href")) for n in self.docs[target_route].links("alternate")}
            self.require((HREFLANG[language], SITE + route.lstrip("/")) in reciprocal, route, "hreflang_reciprocal", target)

    def schema(self, route, doc, title, description):
        scripts = [n for n in doc.tagged("script") if n.attrs.get("type") == "application/ld+json"]
        self.require(len(scripts) == 1, route, "jsonld_count", len(scripts))
        if len(scripts) != 1:
            return []
        try:
            data = json.loads(scripts[0].text())
        except (ValueError, TypeError) as error:
            self.require(False, route, "jsonld_parse", str(error))
            return []
        self.require(isinstance(data, dict) and data.get("@context") == "https://schema.org" and isinstance(data.get("@graph"), list), route, "jsonld_graph", "Expected one schema.org @graph")
        graph = data.get("@graph", []) if isinstance(data, dict) else []
        if not graph or not all(isinstance(n, dict) for n in graph):
            return []
        ids = [n.get("@id") for n in graph]
        self.require(all(ids) and len(set(ids)) == len(ids), route, "schema_ids", ids)
        entities = {n.get("@id"): n for n in graph}
        self.require(entities.get(self.brand_id, {}).get("@type") == "Brand" and entities.get(self.brand_id, {}).get("name") == "KUMAKIKAI", route, "schema_brand", "Stable canonical Brand ID required")
        person = entities.get(self.person_id, {})
        self.require(person.get("@type") == "Person" and person.get("name") == "Yuya Nakamura" and person.get("jobTitle") == "Software Engineer / App Developer" and person.get("url") == SITE + "company/" and person.get("brand") == {"@id": self.brand_id}, route, "schema_person", "Person / Brand relationship mismatch")
        website = entities.get(self.website_id, {})
        self.require(website.get("@type") == "WebSite" and website.get("name") == "KUMAKIKAI" and website.get("publisher") == {"@id": self.person_id}, route, "schema_website", "Stable WebSite identity required")
        page_id = SITE + route.lstrip("/") + "#webpage"
        page = entities.get(page_id, {})
        self.require(page.get("name") == title and page.get("description") == description and page.get("url") == SITE + route.lstrip("/") and page.get("isPartOf") == {"@id": self.website_id}, route, "schema_webpage", "WebPage SEO fields / website relationship mismatch")
        def inspect(value):
            if isinstance(value, dict):
                self.require(value.get("@type") not in ("Organization", "Corporation"), route, "schema_company_type", "This site describes a developer's brand, not a corporation")
                self.require(not FORBIDDEN_CLAIMS.intersection(value), route, "schema_unverified_claim", sorted(FORBIDDEN_CLAIMS.intersection(value)))
                if set(value) == {"@id"}:
                    self.require(value["@id"] in entities, route, "schema_reference", value["@id"])
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
        inspect(data)
        self.counts["jsonld_graphs"] += 1
        return graph

    def product(self, route, doc, graph, app, lang, title, description):
        app_id = app["id"]
        self.counts["product_pages"] += 1
        expected = self.seo[lang]["products"][app_id]
        name = self.home[lang]["apps"][app_id]["name"]
        self.require(title == expected["title"] == name + " | KUMAKIKAI" and description == expected["description"], route, "product_metadata", "Expected Product-specific SEO JSON")
        self.require([compact(n.text()) for n in doc.tagged("h1")] == [compact(name)], route, "product_h1", name)
        applications = [n for n in graph if n.get("@type") == "SoftwareApplication"]
        self.require(len(applications) == 1, route, "schema_application", len(applications))
        if applications:
            application = applications[0]
            self.require(application.get("@id") == SITE + "products/" + app_id + "/#software" and application.get("name") == name and application.get("description") == description, route, "schema_application_identity", application.get("@id"))
            self.require(application.get("creator") == {"@id": self.person_id} and application.get("publisher") == {"@id": self.person_id}, route, "schema_application_creator", "Use the declared developer entity")
            systems = list(app["operatingSystems"])
            details = json.loads((self.source / "data/product_details" / f"{app_id}.json").read_text())
            if details.get("watch", {}).get("status") == "published":
                systems.append("watchOS")
            self.require(set(application.get("operatingSystem", [])) == set(systems), route, "schema_os", {"expected": systems, "actual": application.get("operatingSystem")})
            if app["status"] == "published":
                self.require(application.get("downloadUrl") == app.get("appStoreURL"), route, "schema_download", application.get("downloadUrl"))
            else:
                self.require("downloadUrl" not in application and application.get("creativeWorkStatus") == "In development", route, "schema_unreleased", "Do not advertise an unavailable download")
        breadcrumbs = [n for n in graph if n.get("@type") == "BreadcrumbList"]
        expected_items = [SITE + localized(lang, "/products/").lstrip("/"), SITE + route.lstrip("/")]
        self.require(len(breadcrumbs) == 1 and [n.get("item") for n in breadcrumbs[0].get("itemListElement", [])] == expected_items and [n.get("position") for n in breadcrumbs[0].get("itemListElement", [])] == [1, 2], route, "breadcrumb", expected_items)

    def article(self, route, doc, graph, meta):
        expected_type = "BlogPosting" if meta["category"] == "blog" else "Article"
        articles = [n for n in graph if n.get("@type") in {"Article", "BlogPosting", "NewsArticle"}]
        self.require(len(articles) == 1 and articles[0].get("@type") == expected_type, route, "article_type", expected_type)
        if not articles:
            return
        article = articles[0]
        self.counts[expected_type] += 1
        path = self.content_file(route)
        editorial = path.read_text() if path else ""
        declared_description = frontmatter_value(editorial, "description")
        self.require(isinstance(declared_description, str) and bool(declared_description.strip()), route, "article_description_source", "News requires an explicit, nonempty description in Markdown front matter")
        if declared_description:
            self.require(compact(article.get("description", "")) == compact(declared_description), route, "article_description_match", str(path))
        declared_date = frontmatter_value(editorial, "date")
        self.require(iso(declared_date) is not None, route, "article_date_source", "News requires an explicit date in Markdown front matter")
        self.require(compact(article.get("headline", "")) == compact(doc.tagged("h1")[0].text()) if doc.tagged("h1") else False, route, "article_headline", article.get("headline"))
        self.require(article.get("author") == {"@id": self.person_id} and article.get("publisher") == {"@id": self.person_id}, route, "article_author", "Article must reference the same developer")
        published, modified = iso(article.get("datePublished")), iso(article.get("dateModified"))
        self.require(published is not None and modified is not None, route, "article_dates", [article.get("datePublished"), article.get("dateModified")])
        if published and modified:
            if iso(declared_date):
                self.require(iso(declared_date).date() == published.date(), route, "article_published_source", {"source": declared_date, "schema": article.get("datePublished")})
            try:
                self.require(modified >= published, route, "article_date_order", [article.get("datePublished"), article.get("dateModified")])
            except TypeError:
                self.require(False, route, "article_date_zone", "Dates must have consistent time zone information")
        lastmod = self.sitemap.get(SITE + route.lstrip("/"))
        if lastmod and modified:
            self.require(iso(lastmod) == modified, route, "article_sitemap_lastmod", [lastmod, article.get("dateModified")])
        lang, _ = lang_route(route)
        for app_id in meta.get("relatedProducts", []):
            target = SITE + localized(lang, "/products/" + app_id + "/").lstrip("/")
            self.require(target in doc.anchors(route), route, "article_product_link", target)

    def run(self):
        self.counts["html_pages"] = len(self.docs)
        self.require(bool(self.docs), "/", "build_empty", str(self.build))
        self.xml_sitemap()
        self.robots()
        for route, doc in self.docs.items():
            lang, base = lang_route(route)
            alternates = [n for n in doc.links("alternate") if n.attrs.get("hreflang")]
            if doc.redirect():
                self.counts["redirects"] += 1
                target = doc.redirect_target()
                self.require(bool(target), route, "redirect_immediate", "Compatibility redirect must be immediate and must not depend on JavaScript")
                self.require([n.attrs.get("href") for n in doc.links("canonical")] == [target], route, "redirect_canonical", target)
                parsed = urlsplit(target or "")
                self.require(bool(target) and target.startswith(SITE) and parsed.path in self.docs and not self.docs[parsed.path].redirect(), route, "redirect_target", target)
                continue
            if base in {"/support/", "/privacy/", "/htu/", "/faq/", "/terms/", "/notes/", "/404.html"} or re.fullmatch(r"/(?:notes|htu|faq|privacy|terms)/page/\d+/", base):
                self.require(doc.noindex(), route, "compatibility_noindex", "Duplicate / compatibility hub should not be indexed")
            if doc.noindex():
                self.counts["noindex_pages"] += 1
                self.require(not alternates, route, "noindex_hreflang", "Do not nominate non-indexable alternates")
                continue
            self.counts["indexable_pages"] += 1
            self.explicit_lastmod(route)
            title, description = self.metadata(route, doc)
            self.alternates(route, doc)
            graph = self.schema(route, doc, title, description)
            if base in ("/", "/company/"):
                expected = self.seo[lang]["home" if base == "/" else "about"]
                self.require(title == expected["title"] and description == expected["description"], route, "brand_metadata", expected)
                self.require(any("YuyaNakamura" in compact(n.visible_text()) for n in doc.tagged("main")), route, "visible_developer", "Developer name must be visible HTML text, not only an image or JSON-LD")
            for app in self.apps:
                if base == "/products/" + app["id"] + "/":
                    self.product(route, doc, graph, app, lang, title, description)
            if base == "/products/":
                for app in self.apps:
                    target = SITE + localized(lang, "/products/" + app["id"] + "/").lstrip("/")
                    self.require(target in doc.anchors(route), route, "static_product_link", target)
                self.require(len({v["description"] for v in self.seo[lang]["products"].values()}) == len(self.apps), route, "unique_product_descriptions", lang)
            if base == "/":
                for target in ("/products/", "/company/", "/news/", "/products/uni-note/"):
                    self.require(SITE + localized(lang, target).lstrip("/") in doc.anchors(route), route, "static_home_links", target)
            if base == "/company/":
                self.require(SITE + localized(lang, "/products/").lstrip("/") in doc.anchors(route), route, "about_products_link", "A static Products link is required")
            slug = base.rstrip("/").split("/")[-1]
            if re.fullmatch(r"/(?:notes|news)/[^/]+/", base):
                path = self.content_file(route)
                category = frontmatter_value(path.read_text(), "news_category") if path else None
                meta = dict(self.news.get(slug, {}))
                meta["category"] = category or meta.get("category", "information")
                self.require(meta["category"] in {"press-release", "blog", "information"}, route, "news_category", meta["category"])
                self.article(route, doc, graph, meta)
            self.pages.append({"url": SITE + route.lstrip("/"), "language": lang, "title": title, "description": description, "schemaTypes": [n.get("@type") for n in graph]})
        for lang in LANGS:
            for base in ("/", "/products/", "/company/", "/news/"):
                self.require(localized(lang, base) in self.indexed, localized(lang, base), "primary_indexable", "Primary page must be crawlable")
            for app in self.apps:
                self.require(localized(lang, "/products/" + app["id"] + "/") in self.indexed, localized(lang, "/products/" + app["id"] + "/"), "product_indexable", "All Products must be indexed independently of random Featured")
        for route in self.docs:
            _, base = lang_route(route)
            if re.fullmatch(r"/(?:htu|faq|privacy|terms)/[^/]+/", base) or re.fullmatch(r"/(?:notes|news)/[^/]+/", base) and base.rstrip("/").split("/")[-1] in self.news:
                if not self.docs[route].redirect():
                    self.require(route in self.indexed, route, "protected_indexable", "Do not noindex existing app support, policy or article pages")
        return {"ok": not self.errors, "build": str(self.build), "counts": dict(self.counts), "errors": self.errors, "warnings": self.warnings, "pages": self.pages, "noindex": sorted(r for r, d in self.docs.items() if d.noindex() and not d.redirect()), "redirects": sorted(r for r, d in self.docs.items() if d.redirect())}


def negative_tests(build, source):
    """Mutate only parsed in-memory HTML; never alter the production build."""
    baseline = Audit(build, source).run()
    if not baseline["ok"]:
        return {"ok": False, "reason": "Baseline must pass before negative tests", "baselineErrors": baseline["errors"][:10]}
    cases = []
    target = "/products/uni-note/"
    for name, code in (("localhost canonical", "canonical"), ("accidental noindex", "sitemap_coverage"), ("invalid JSON-LD", "jsonld_parse"), ("nonexistent alternate", "hreflang_target"), ("missing published download", "schema_download"), ("fabricated rating", "schema_unverified_claim")):
        audit = Audit(build, source)
        doc = audit.docs[target]
        if code == "canonical":
            doc.links("canonical")[0].attrs["href"] = "http://localhost:1313/products/uni-note/"
        elif code == "sitemap_coverage":
            node = Node("meta", {"name": "robots", "content": "noindex"})
            doc.nodes.append(node)
            audit.indexed.remove(target)
        elif code == "hreflang_target":
            next(n for n in doc.links("alternate") if n.attrs.get("hreflang") == "en").attrs["href"] = SITE + "en/missing-product/"
        else:
            script = next(n for n in doc.tagged("script") if n.attrs.get("type") == "application/ld+json")
            if code == "jsonld_parse":
                script.children = ["{invalid json"]
            else:
                data = json.loads(script.text())
                app = next(n for n in data["@graph"] if n.get("@type") == "SoftwareApplication")
                if code == "schema_download":
                    app.pop("downloadUrl", None)
                else:
                    app["aggregateRating"] = {"ratingValue": 5, "reviewCount": 99999}
                script.children = [json.dumps(data)]
        result = audit.run()
        detected = any(e["check"] == code for e in result["errors"])
        cases.append({"case": name, "expectedCheck": code, "detected": detected})
    return {"ok": all(c["detected"] for c in cases), "cases": cases, "filesModified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, default=Path("public"))
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        result = negative_tests(args.build, args.source) if args.self_test else Audit(args.build, args.source).run()
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {"ok": False, "error": str(error)}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"pages", "noindex", "redirects"}}, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
