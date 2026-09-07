#!/usr/bin/env python3
"""Check every generated Product fact table and reject in-memory regressions.

Reads a production build without modifying HTML or application repositories.
Mutations exercise the migration verifier against accidental missing OS data,
extra developer rows, reordered rows and premature Apple Watch availability.
"""
import argparse
from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("migration", ROOT / "scripts/verify-migration.py")
migration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migration)


def check(facts, app, detail, locale, route):
    verifier = migration.Verification.__new__(migration.Verification)
    verifier.data_file = ROOT / "data/apps.json"
    verifier.errors = []
    verifier.counts = Counter()
    verifier.verify_product_facts(facts, app, detail, locale, route)
    return verifier.errors


def rows(facts):
    table = next(facts.descendants("dl"))
    return table, [part for part in table.parts if isinstance(part, migration.Node)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, default=ROOT / "public")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    apps = json.loads((ROOT / "data/apps.json").read_text())
    generated, negative, failures = [], [], []
    fixtures = {}
    for locale in migration.LANGUAGES:
        for app in apps:
            route = migration.localized(locale, "/products/" + app["id"] + "/")
            path = args.build / route.lstrip("/") / "index.html"
            detail = json.loads((ROOT / "data/product_details" / (app["id"] + ".json")).read_text())
            doc = migration.Document(path.read_text())
            sections = [node for node in doc.tagged("section") if node.has_class("product-facts")]
            errors = check(sections[0], app, detail, locale, route) if len(sections) == 1 else [{"check": "product_facts", "detail": "Exactly one compatibility section is required"}]
            result = {"route": route, "ok": not errors, "errors": errors}
            generated.append(result)
            if errors:
                failures.append(result)
            else:
                fixtures[(locale, app["id"])] = (sections[0], app, detail, locale, route)

    def rejection(name, source, mutate, expected_check):
        if source not in fixtures:
            failures.append({"name": name, "detail": "Generated source failed; negative test not run"})
            return
        facts, app, detail, locale, route = copy.deepcopy(fixtures[source])
        mutate(facts, detail)
        errors = check(facts, app, detail, locale, route)
        result = {"name": name, "ok": any(error["check"] == expected_check for error in errors), "detectedChecks": sorted({error["check"] for error in errors})}
        negative.append(result)
        if not result["ok"]:
            failures.append(result)

    def remove_os_row(facts, _):
        table, entries = rows(facts)
        table.parts.remove(entries[1])

    def add_developer(facts, _):
        table, _ = rows(facts)
        injected = next(migration.Document("<div><dt>開発元</dt><dd>KUMAKIKAI</dd></div>").root.descendants("div"))
        injected.parent = table
        table.parts.append(injected)

    def reorder_rows(facts, _):
        table, entries = rows(facts)
        first, second = table.parts.index(entries[0]), table.parts.index(entries[1])
        table.parts[first], table.parts[second] = table.parts[second], table.parts[first]

    def remove_pending(index):
        def mutate(facts, _):
            pending = [node for node in facts.descendants() if node.has_class("platform-upcoming")][index]
            pending.parent.parts.remove(pending)
        return mutate

    rejection("missing OS row", ("ja", "uni-note"), remove_os_row, "product_facts")
    rejection("missing minimumOS metadata", ("ja", "uni-note"), lambda _, detail: detail.pop("minimumOS"), "product_minimum_os")
    rejection("developer row reintroduced", ("ja", "uni-note"), add_developer, "product_facts")
    rejection("device/OS row order reversed", ("ja", "uni-note"), reorder_rows, "product_facts")
    rejection("missing watchOS metadata", ("ja", "smokeless"), lambda _, detail: detail["watch"].pop("minimumOS"), "product_minimum_os")
    for locale in migration.LANGUAGES:
        fixture = fixtures.get((locale, "smokeless"))
        if fixture and fixture[2]["watch"]["status"] != "published":
            rejection(f"{locale}: Watch device pending qualifier removed", (locale, "smokeless"), remove_pending(0), "product_watch_pending")
            rejection(f"{locale}: watchOS pending qualifier removed", (locale, "smokeless"), remove_pending(1), "product_watch_pending")

    result = {"ok": not failures, "build": str(args.build.resolve()), "productPages": len(generated), "negativeCases": len(negative), "generated": generated, "negative": negative, "failures": failures}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("ok", "productPages", "negativeCases", "failures")}, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
