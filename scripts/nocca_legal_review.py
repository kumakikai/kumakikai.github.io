"""Exact, reviewed exceptions for the authorized 2026-09-07 Nocca legal update.

This does not rewrite the migration baseline or permit other apps to opt in.
Source and rendered text/links must match a separately reviewed catalog.
"""
import hashlib
import json
from pathlib import Path
import re

PURPOSE = "nocca-legal-update-2026-09-07"
CATALOG = "docs/legal/reviewed-nocca-content.json"
BAD_FORM = "https://forms.gle/Enzmm94LdXRZjP8k9"
NOTES = "/notes/2026-09-06-nocca/"
NOTES_SOURCE_SHA256 = "69d646a783b4b7e6312de61ba3673343d10a419b9a4a469b3a995ab86ad87af7"
SCOPE = {
    "/privacy/nocca/": ("content/privacy/nocca.md", "e01d5993ef49c080b2b2a9c5b30ce12b125ce15e6cca69d3c5d51cd3bf7a1fff"),
    "/terms/nocca/": ("content/terms/nocca.md", "150df3841135c7542cbe39b7318c9d1cb53b68bb2a4e2fff8c8718855da46946"),
    NOTES: ("content/notes/2026-09-06-nocca.md", "b27985ee2867507911f4fa7dbd3bfd22b314edf51ef30c03ccd15bb852096da5"),
}
FIELDS = {"source", "sourceSHA256", "baselineTextSHA256", "reviewedTextSHA256", "reviewedLinks", "removedLinks", "reason"}


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def error(route, check, detail):
    return {"page": route, "check": "nocca_legal_" + check, "detail": detail}


def load_reviews(root, baseline):
    path = root / CATALOG
    if not path.exists():
        return {}, []  # Without a catalog, all original baseline checks still apply.
    errors = []
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
        if set(catalog) != {"schemaVersion", "purpose", "reviews"} or catalog["schemaVersion"] != 1 or catalog["purpose"] != PURPOSE:
            raise ValueError("Catalog schema or purpose mismatch")
        reviews = catalog["reviews"]
        if not isinstance(reviews, dict) or set(reviews) != set(SCOPE):
            raise ValueError("Only the exact three authorized Nocca routes may be reviewed")
        for route, (source_name, old_hash) in SCOPE.items():
            review = reviews[route]
            if not isinstance(review, dict) or set(review) != FIELDS:
                raise ValueError("Review fields mismatch")
            if review["source"] != source_name:
                raise ValueError("Review source must match its fixed Nocca route")
            for field in ("sourceSHA256", "baselineTextSHA256", "reviewedTextSHA256"):
                if not isinstance(review[field], str) or not re.fullmatch(r"[0-9a-f]{64}", review[field]):
                    raise ValueError("Review must have exact SHA256 bindings")
            if review["baselineTextSHA256"] != old_hash or digest(baseline["articles"][route]["text"]) != old_hash:
                raise ValueError("Immutable Nocca baseline text mismatch")
            source = root / source_name
            if not source.is_file() or source.is_symlink() or digest(source.read_bytes()) != review["sourceSHA256"]:
                raise ValueError("Nocca source changed since review")
            if route == NOTES and review["sourceSHA256"] != NOTES_SOURCE_SHA256:
                raise ValueError("Nocca article may only remove the known incorrect form line")
            if not isinstance(review["reason"], str) or not review["reason"].strip():
                raise ValueError("A concrete review reason is required")
            links = review["reviewedLinks"]
            if not isinstance(links, list) or any(not isinstance(link, str) for link in links) or links != sorted(set(links)):
                raise ValueError("Reviewed links must be a sorted exact set")
            removed = [BAD_FORM] if route == NOTES else []
            if review["removedLinks"] != removed:
                raise ValueError("Only the incorrect Nocca article form link may be removed")
            if "forms.gle/" in source.read_text() or "docs.google.com/forms/" in source.read_text():
                raise ValueError("A form link remains in the authorized Nocca sources")
        return reviews, []
    except (ValueError, TypeError, KeyError, OSError) as exc:
        errors.append(error("/", "catalog", str(exc)))
        return {}, errors  # Malformed catalog never disables the original checks.


def check_article(route, review, text, links):
    errors = []
    if route not in SCOPE:
        return [error(route, "scope", "A different route cannot use this exception")]
    if digest(text) != review["reviewedTextSHA256"]:
        errors.append(error(route, "body", "Rendered text changed since the Nocca legal review"))
    if sorted(set(links)) != review["reviewedLinks"]:
        errors.append(error(route, "links", "Rendered links changed since the Nocca legal review"))
    if any("forms.gle/" in link or "docs.google.com/forms/" in link for link in links):
        errors.append(error(route, "form", "Incorrect or unreviewed form link remains"))
    return errors
