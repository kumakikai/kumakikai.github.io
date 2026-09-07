"""One fixed Korean feature-name correction; no editable review catalog."""
import hashlib
import json

ROUTE = "/ko/privacy/uni-note/"
BASELINE_SHA256 = "2c4622b9425b03b9932decb374e7ae77f52fbb3289eeedc7455807c94d73c5cb"


def expected_body(route, old):
    if route != ROUTE:
        raise ValueError("Only Korean Uni:Note Privacy may use this correction")
    data = json.dumps(old, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(data).hexdigest() != BASELINE_SHA256:
        raise ValueError("Immutable Korean Privacy baseline mismatch")
    if old["text"].count("AI잔량") != 2 or not old["text"].endswith("최종업데이트:2026-06-28"):
        raise ValueError("Expected the two original feature labels and update date")
    return old["text"].replace("AI잔량", "AI잔액").removesuffix("2026-06-28") + "2026-09-08"


def check_article(route, old, text, links):
    expected = expected_body(route, old)
    if text != expected:
        raise ValueError("Only the two Korean AI Balance labels and final update date may change")
    if links != old['links']:
        raise ValueError("Keep exactly the original body links in their original order")
