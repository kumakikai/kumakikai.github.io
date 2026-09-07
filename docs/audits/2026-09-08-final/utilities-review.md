# Utilities content audit — source HEAD 0fba8cf

Audit basis: `/Users/yuya/Projects/homepage` local source at `0fba8cf`, read-only. No web search, public pages, or cached public HTML was used. Related app repositories were read only at their current working trees; those trees contain pre-existing dirty changes. This report does not establish which app build is currently released.

## Scope

- 4 apps: GigaPoke (`giga-poke`), Smokeless (`smokeless`), Balance Calendar (`balance-calendar`), SIGNAL (`signal`).
- Metadata: the 4 app entries in `data/apps.json`; all 4 `data/product_details/*.json` files including all 6 locales and Smokeless Watch copy; corresponding 24 entries in each of `data/home/<locale>.json` and `data/seo/<locale>.json`.
- 49 current canonical app pages: 24 generated Product pages, 8 Guide, 8 FAQ, 8 Privacy, and 1 custom Terms (GigaPoke). Guide/FAQ/Privacy translations exist in ja/en/ko/fr/zh-hant only for Smokeless; the other 3 apps have Japanese support bodies and use fallback links from translated Products. There is no app-specific Terms body for the other 3 apps; common Apple EULA fallback is intentional.
- 10 dated articles whose bodies refer to these apps: `2026-01-23-introduction`, `2026-01-26-roadmap`, `2026-01-27-philosophy`, `2026-02-14-blog`, `2026-02-22-signal`, `2026-03-13-blog`, `2026-03-21-smokeless`, `2026-03-25-blog`, `2026-04-12-uni-note-10000`, `2026-09-02-giga-poke` in `content/notes/`. Their original context and existing support URLs must remain intact. Only utility-related facts were assessed in articles that also discuss Uni:Note.
- App source spot-checks: `/Users/yuya/Projects/povo_manager` (notification schedule, widget, storage exclusion from backup, clipboard, OS, current monetization policy); `/Users/yuya/Projects/smokeless` (OS and Watch targets, branding, IAP/release docs, graph intervals and weekly-ad logic); `/Users/yuya/Projects/gamble_pnl` (actual buttons, yearly total, tags, OS); `/Users/yuya/Projects/signal` (source catalog, visible count limits, refresh fallback, settings and OS).

## Confirmed findings

### U1 — P2: Korean Smokeless product name differs within the same product journey

Evidence:
- `data/home/ko.json:107`: `"name": "스와나비"`.
- `data/seo/ko.json:36-37`: title and description begin with `스와나비`.
- `content/products/smokeless.ko.md:3-5`: generated Product title/description/seo_title likewise use `스와나비`.
- `data/product_details/smokeless.json:287`: the same Korean Product body starts `Smokeless는 ...`.
- `content/htu/smokeless.ko.md:2`, `content/faq/smokeless.ko.md:2,9`, `content/privacy/smokeless.ko.md:2,6`: all use `Smokeless`.
- App-local corroboration only: `/Users/yuya/Projects/smokeless/docs/APP_STORE_METADATA.md:11-16` records Korean device/app name `smokeless` and the previously checked Korean Store name `SmokeLess - 금연 카운터`; `/Users/yuya/Projects/smokeless/ios/Runner/en.lproj/InfoPlist.strings:1` sets the default display name to `smokeless`. The dated Store note is not fresh external verification.

Impact: Korean Home/Products/Product heading identifies the app with one name, then the Product body and all support/legal destinations identify it with another. `스와나비` is the Japanese name transliterated into Korean, and is not supported by the current local naming evidence.

Scoped correction: normalize the Korean Home name and SEO references to the same established `Smokeless` name already used in the Korean body/support pages, then regenerate the Product entry with `sync-products.py`. Do not modify the App Store title, app repo, or other languages as part of this fix. A separate broad rebranding/casing change is unnecessary.

### U2 — P3: Balance Calendar describes actual arrow controls as plus/minus buttons

Evidence:
- `data/product_details/balance-calendar.json:25`: `ホーム画面のプラス・マイナスから...`.
- English/KO/DE/FR/zh-hant equivalents are at `:81`, `:137`, `:193`, `:249`, `:305`; the English explicitly says `widget’s plus and minus buttons`.
- `data/home/ja.json:100`, `data/home/en.json:102`, `data/home/fr.json:102` and corresponding other locale imageAlts describe the registration screen's buttons as plus/minus.
- The current Guide already correctly names the UI: `content/htu/balance-calendar.md:16` (`収入は緑の「↑」、支出は赤の「↓」`), and `:46` describes the same arrows on the widget.
- App source: `/Users/yuya/Projects/gamble_pnl/lib/features/register/register_page.dart:440-445,463-468` uses tutorial text `↑` / `↓` and corresponding income/outgoing ActionButtons. `/Users/yuya/Projects/gamble_pnl/ios/HiLowWidgetExtension/HiLowWidgetExtension.swift:44-59` renders `Text("↑")` and `Text("↓")`.

Impact: A small but concrete Product/Guide discrepancy; especially relevant to image alt text and locating a control by its visible symbol.

Scoped correction: for references specifically naming a visible button, use income/expense or up/down arrow controls, matching the Guide and app. Preserve prose about positive/negative amounts and totals; that is accurate and should not be mechanically replaced. No screenshot re-creation or app changes are required for this copy correction.

## Temporal clarity item (not an implementation contradiction)

### U3 — P3 / editorial: old roadmap promises lack a visible historical qualification

Evidence:
- `content/notes/2026-01-26-roadmap.md:3-5` has original date `2026-01-23`, description explicitly calling the content a January 2026 plan, but `lastmod: 2026-09-07`.
- Body `:18-19` still says `今後の対応予定`; `:74-83` promises CSV/PDF exports and premium cloud backup, and `:87-98` describes future subscription bundles.
- Current `content/faq/balance-calendar.md:53-54` says backup, automatic sync and export are not available. These statements are not logically inconsistent when the roadmap is read as a dated plan.
- `layouts/single.html:5` displays article original/updated dates but does not display the front-matter description in the article body; the historic qualification in `description` does not become a visible notice.

Suggested optional correction: add one visible, dated sentence to the roadmap saying it records the January 2026 plan and point readers to the current Product/FAQ for available functions. Preserve the original article body, dates, URL and unimplemented status; do not rewrite the old promises as present product capabilities, and do not declare the plan canceled without a user decision. This should be an editorial follow-up, not a release blocker.

## Time-sensitive status / evidence boundary

- Smokeless Watch is consistently marked `review` in the website source (`data/product_details/smokeless.json:4,19-22`, plus all other Watch locales and `content/faq/smokeless*.md` final answer). It is not presented as publicly released; minimum watchOS 9 and compatible paired-iPhone wording are retained.
- There is a local record disagreement: `/Users/yuya/Projects/smokeless/docs/RELEASE_NOTES_1_2_0.md:3` says Store entry/publication not performed; website `docs/visual-guides/utilities-audit.md:40,57,62-63,87` records 1.2.0 under review and explains use of its existing iPhone controls. Neither proves today's external state. Preserve `review` for this source-only audit; actual Store status is a separate verification item, not an inferred change.
- Before publicly changing Watch to released, Smokeless Privacy in all 5 existing languages should be reviewed against the actual Watch data transfer: currently `content/privacy/smokeless.md:14-18` only describes same-device app/widget sharing and says those data stay on device. With a pending feature, this is a release follow-up rather than evidence of a current published mismatch.

## Checked and not findings

- **Balance Calendar yearly totals are real.** `data/product_details/balance-calendar.json` and Home/SEO refer to daily/monthly/year totals while Guide/FAQ list day/month/category tabs. The monthly view actually sums and displays the selected year's total in `/Users/yuya/Projects/gamble_pnl/lib/features/graph/graph_page.dart:879-930`; `lib/l10n/app_ja.arb:107` labels it `当年合計`. Do not delete this feature because there is no separate year tab.
- GigaPoke's free/no ads/no account copy matches the current local acquisition-phase policy (`/Users/yuya/Projects/povo_manager/docs/MONETIZATION_STRATEGY.md:13-26`). Future ads/IAP plans in that file are explicitly not current implementations. The website does not need to advertise them.
- GigaPoke's iOS 17 / iPhone requirement matches `Config/Shared.xcconfig:16` and app target device family. Clipboard `localOnly`, backup exclusion and 9 a.m. notification schedule are backed by current source; guide/FAQ clearly separate app management state from external redemption success.
- SIGNAL's 7 built-in sources match `lib/data/catalog/source_catalog.dart:4-61`, and FAQ caps of TODAY 75 / other shelves 45 match `lib/presentation/home/home_screen.dart:79-80`. Its failed-refresh preservation matches current `lib/data/repositories/feed_repository_impl.dart:26-45`. Do not infer article-body offline storage from the cached headlines.
- No further generic related-page list remains in the 25 support/legal source pages under this assignment. The retained GigaPoke form/email and contextual links are intentional. The dated GigaPoke Notes article has a Privacy reference at `:30` and the support list entry at `:36`; that legacy support article is separate from the shared app-page footer and its substantive URL role is preserved.
- No substantial duplicated explanatory paragraph was found that warrants deleting app-specific content. Exact repeated long text was limited to necessary contact boilerplate and the valid no-registration/no-personal-input statement shared by Smokeless and SIGNAL Privacy. Overview, features and stories repeat some concepts at different detail levels but do not contain a redundant second generic navigation list.

No source files were edited; only this report was created under `/private/tmp`.
