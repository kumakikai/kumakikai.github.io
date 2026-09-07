"""Exact legal navigation and OtoMiru offer cleanup; baseline stays immutable."""
import hashlib
import json
from urllib.parse import urljoin

SITE = "https://kumakikai.github.io"
UPDATED = "2026-09-08"
# No catalog or opt-in: only these original Japanese pages may use this change.
# Hashes bind each complete baseline article (normalized text, links and IDs).
SCOPE = {
    "/privacy/giga-poke/": ("fa94faa7e997ec4458b930ee54a13a2a8cb89452271ea598378aa0659208f86b", "ギガポケ", "2026-09-02"),
    "/terms/giga-poke/": ("ae0a507026e49ab107b8a85812ce7c15ec0234e32afc138b07c304e32c4f5652", "ギガポケ", "2026-09-02"),
    "/privacy/oto-miru/": ("3c96e4e89b9a47adb940d32eab3cc8a90a8a3d7a80f748c1a0a42dd700837857", "オトミル", "2026-05-19"),
    "/terms/oto-miru/": ("04145fbac4df9d140bea5cef636a5a21c0df26f99eb9baa1b9ec15ecb3513279", "オトミル", "2026-05-19"),
}
OTO_MIRU_TERMS = "/terms/oto-miru/"
RETIRED_OTO_MIRU_OFFER = "月額480円年額3,800円1ヶ月無料トライアル"


def navigation_links(route):
    if route not in SCOPE:
        return []
    section, app_id = route.strip("/").split("/")
    other = "terms" if section == "privacy" else "privacy"
    return [urljoin(SITE, f"/{kind}/{app_id}/") for kind in ("htu", "faq", other)]


def expected_body(route, old):
    """Apply fixed navigation edits and the reviewed OtoMiru offer removal only."""
    if route not in SCOPE:
        raise ValueError("Only the four fixed legal routes may use this change")
    old_hash, name, old_date = SCOPE[route]
    baseline_bytes = json.dumps(old, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(baseline_bytes).hexdigest() != old_hash:
        raise ValueError("Immutable legal baseline article mismatch")
    if old["links"][-3:] != navigation_links(route):
        raise ValueError("Immutable final navigation links mismatch")
    other_label = "利用規約" if route.startswith("/privacy/") else "プライバシーポリシー"
    related = f"関連ページ:使い方({name})よくある質問({name}){other_label}({name})"
    dates = ("制定日:2026-09-02" if "giga-poke" in route else "") + f"最終更新日:{old_date}"
    if old["text"].count(related) != 1 or not old["text"].endswith(related + dates):
        raise ValueError("Expected exactly one final related-page block and original dates")
    expected = old["text"][:-len(related + dates)] + dates.removesuffix(old_date) + UPDATED
    if route == OTO_MIRU_TERMS:
        # The current app uses StoreKit prices and a two-week introductory
        # offer. Keep the existing purchase-screen precedence and Family
        # Sharing wording, removing just these three stale fixed list items.
        original_offer = "自動更新サブスクリプションです。" + RETIRED_OTO_MIRU_OFFER + "ファミリー共有に対応"
        if expected.count(original_offer) != 1:
            raise ValueError("Expected exactly one original OtoMiru Plus price and trial list")
        expected = expected.replace(original_offer, original_offer.replace(RETIRED_OTO_MIRU_OFFER, ""), 1)
    return expected


def check_article(route, old, text, links, validated_support_links):
    """Shared destinations count only after the caller validates the component."""
    def error(check, detail):
        return {"page": route, "check": "legal_navigation_" + check, "detail": detail}

    if route not in SCOPE:
        return [error("scope", "A different route cannot use this exception")]
    try:
        expected = expected_body(route, old)
    except (ValueError, KeyError, TypeError) as exc:
        return [error("baseline", str(exc))]
    errors = []
    if text != expected:
        errors.append(error("body", "Only the final related-page block removal, final update date change, and the three fixed OtoMiru Terms price/trial items are authorized"))
    if links != old["links"][:-3]:
        errors.append(error("links", "Keep every other body link in its original order, including inline legal and contact references"))
    missing = sorted(set(navigation_links(route)) - set(validated_support_links))
    if missing:
        errors.append(error("support", f"Original navigation must remain in validated same-app support rows: {missing}"))
    return errors
