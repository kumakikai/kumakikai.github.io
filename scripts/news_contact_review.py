"""One fixed GigaPoke News contact change; no catalog or general opt-in.

The user requested email-only website contact. Only the article's two contact
links become one existing-mailbox link, and lastmod becomes 2026-09-08.
The original migration baseline, article identity and all other copy stay fixed.
"""
import hashlib
import json

ROUTE = "/notes/2026-09-02-giga-poke/"
SOURCE = "content/notes/2026-09-02-giga-poke.md"
BASELINE_SHA256 = "87550ab46e14c4ddc1c00f5600c1bf19376409b589c86a915d5948364f0d7221"
SOURCE_SHA256 = "60e1f3e723a52ceba9d71bc3c6b9de059c2d0183026a05cca4a04eb1de5e3f96"
FORM = "https://forms.gle/Enzmm94LdXRZjP8k9"
EMAIL = "mailto:kumakikai.apps@gmail.com"
OLD_CONTACT = "お問い合わせフォームkumakikai.apps@gmail.com"
NEW_CONTACT = "メールで問い合わせる"


def original_article(route, old):
    if route != ROUTE:
        raise ValueError("Only the fixed GigaPoke News route may use this change")
    data = json.dumps(old, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(data).hexdigest() != BASELINE_SHA256:
        raise ValueError("Immutable GigaPoke News baseline mismatch")
    if old["text"].count(OLD_CONTACT) != 1 or old["links"][-2:] != [FORM, EMAIL]:
        raise ValueError("Expected exactly the original contact label and final form/email links")
    return old


def expected_body(route, old):
    return original_article(route, old)["text"].replace(OLD_CONTACT, NEW_CONTACT, 1)


def expected_links(route, old):
    links = original_article(route, old)["links"]
    return links[:-2] + [EMAIL]


def removed_links(route):
    return [FORM] if route == ROUTE else []


def check_article(root, route, old, text, links):
    """Require the exact reviewed source, text and ordered body links.

    The caller retains the ordinary route, canonical, image and anchor checks.
    Only removed_links(ROUTE) may bypass the old-link-presence comparison.
    """
    def error(kind, detail):
        return {"page": route, "check": "news_contact_" + kind, "detail": detail}

    try:
        expected = expected_body(route, old)
        retained = expected_links(route, old)
    except (ValueError, KeyError, TypeError) as exc:
        return [error("baseline", str(exc))]
    errors = []
    source = root / SOURCE
    try:
        if source.is_symlink() or not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
            errors.append(error("source", "Only the fixed two-to-one contact link edit and lastmod change are authorized"))
    except OSError as exc:
        errors.append(error("source", str(exc)))
    if text != expected:
        errors.append(error("body", "Only the original form/email labels may become the single email action label"))
    if links != retained:
        errors.append(error("links", "Remove only the original form URL; preserve every other body link and its order"))
    return errors
