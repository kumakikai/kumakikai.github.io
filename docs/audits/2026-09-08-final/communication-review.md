# KUMAKIKAI final audit: OtoMiru / Nocca content consistency (before fixes)

Audit date: 2026-09-08. Website source: `/Users/yuya/Projects/homepage`, branch `main`, HEAD `0fba8cf`. At first check only untracked `.DS_Store` was present. This audit is read-only; no website/application source was changed. No search, cached public page, or live public HTML was used.

## Scope and method

- Read website maintenance guide and latest local app data: the OtoMiru and Nocca records in `data/apps.json`, both `data/product_details/*.json` (all six locales), all six `data/home/*.json` and `data/seo/*.json` entries, twelve generated Product Markdown entries, eight Japanese Guide/FAQ/Privacy/Terms documents, and the two existing News/Notes articles. These correspond to 22 app-specific generated HTML pages, with shared data also displayed in Home/Products/About surfaces.
- Compared device, purchase, trial, permissions, offline/remote processing and retention claims against the latest working-tree contents of `/Users/yuya/Projects/oto_miru` and `/Users/yuya/Projects/Nocca`. Both application repositories have many existing uncommitted changes. They were preserved. Their local code is evidence of the current implementation, not proof of App Store publication or successful real purchases.
- Site-wide extraction/link/anchor counts and text similarity inventory belong to the parent audit. This report records content judgments and local evidence.

## Findings requiring correction

### C-COM-01 — OtoMiru Terms has an outdated one-month free trial

Status: **confirmed mismatch with current local app source; P2**.

- Website `content/terms/oto-miru.md:67-70`: `月額 480 円` / `年額 3,800 円` / `1ヶ月無料トライアル` / `ファミリー共有に対応`.
- Current application `OtoMiru/Views/PaywallView.swift:26`: `feature("2週間無料トライアル")`.
- Current authoritative app spec `docs/FEATURE_SUBSCRIPTION.md:24-26`: historical reference prices, StoreKit `Product.displayPrice`, and `2週間無料トライアル`.
- `OtoMiru/Services/SubscriptionManager.swift:157-165` actually loads StoreKit products and passes `product.displayPrice`; there is no basis for treating the website's fixed reference prices as currently verified Store prices.
- Website Guide already sends readers to purchase conditions: `content/htu/oto-miru.md:71`; FAQ does likewise: `content/faq/oto-miru.md:154`.

Recommendation: remove the stale fixed-price/one-month list from Terms. State monthly/yearly auto-renewing plan structure, retain Family Sharing, and direct the actual price and trial duration/eligibility to the purchase screen. Do not replace it with an unconditional current public two-week promise based solely on a dirty development checkout. The current two-week code is enough to prove the one-month text is stale relative to local source, not enough to assert the live storefront's current conditions.

### C-COM-02 — OtoMiru old announcement presents Apple Intelligence as a current requirement

Status: **confirmed inconsistency between article and current Guide/FAQ; historical-source distinction required; P2**.

- `content/notes/2026-05-19-oto-miru.md:97-107`: begins `現時点では` and says supported devices must have `Apple Intelligence / Foundation Models`.
- `content/htu/oto-miru.md:13-15`: iOS/iPadOS 26 + Apple Japanese speech recognition required, `Apple Intelligenceの有効化は必須ではありません`.
- `content/faq/oto-miru.md:43-47`: explicitly answers Apple Intelligence is not mandatory.
- Related local app `docs/FEATURE_DEVICE_SUPPORT.md:7-15` makes Foundation Models optional; `OtoMiru/Services/DeviceSupportPolicy.swift:68-74` and `SpeechRecognitionService.swift:307-312` gate on SpeechTranscriber availability and supported locale.

The article is a real dated announcement (2026-05-19), and its description already calls its design statements `公開当初の設計方針` (`content/notes/2026-05-19-oto-miru.md:4`). It is also explicitly a support page (`:125-128`). Preserve its URL and historical body. Add a concise current-information note near the old condition that says it describes the initial design, and that Apple Intelligence is not mandatory under the current Guide's documented conditions. Reuse the existing Guide link rather than adding a second bare `/htu/oto-miru/` navigation link if the structural cleanup can place the note next to the existing guide entry.

## Structural duplication / semantics for the parent inventory

1. OtoMiru Terms links to Privacy twice in the body (`content/terms/oto-miru.md:9`, `:51`) and the common support block also links to it (`layouts/single.html:10` -> `support-links.html`). The opening acceptance reference and data-treatment reference have different legal purposes; flag all occurrences, but do not delete merely by URL count. One body reference may be rewritten without a link if consolidating is appropriate while keeping the actual clause.
2. OtoMiru FAQ, Privacy and Terms each end with a bare email address (`content/faq/oto-miru.md:218`, `content/privacy/oto-miru.md:92`, `content/terms/oto-miru.md:116`) while the common support block has the app-specific contact route. The mailto query can differ, but the recipient is the same. Prefer the common contact row for operational navigation; preserve any clause stating the purpose or handling of an inquiry. Nocca already uses `ページ下部の「お問い合わせ」` and keeps a distinct email fallback (`privacy/nocca.md:97-99`, `terms/nocca.md:88-90`) because its primary contact is a form.
3. Existing OtoMiru article `content/notes/2026-05-19-oto-miru.md:111-121` and Nocca article `content/notes/2026-09-06-nocca.md:27-32` contain Guide/FAQ/Privacy/Terms lists. Their current News template **does not render the common five-row support block**; it renders a related Product card and company/contact aside (`layouts/single.html:9`), whereas support pages use the five-row block on line 10. Therefore these article lists must not automatically be counted as leftover duplicate five-row navigation without checking rendered destinations. Both articles still identify themselves as support URLs and must remain real bodies.
4. Both articles' body email contact also appears in the News common contact aside. This is a true duplicate destination but the body is an old registered support route. Consolidation should retain a usable app contact and distinguish brand contact if the template changes.
5. Guide FAQs deliberately link to specific anchors (Nocca role/connect/send/reply/talk etc., OtoMiru start/orientation/settings/usage). A URL with a different target anchor is a different task destination; do not collapse it to the base page merely to make counts zero.

## Repeated text (reviewed for necessity)

- OtoMiru Privacy repeats the substance `字幕本文、音声データ、会話内容、テレビ内容、映画内容` across scope, collection/use, ad disclosure, and deletion sections (`content/privacy/oto-miru.md:13,48,62`), and the FAQ/Terms also repeat the no-persistence/no-server-transfer guarantee. This is repetitive writing, but these sections address different user questions and legal purposes. Current local code has retired the AI service path (deleted `HighAccuracyTranscriptionService.swift`; `docs/FEATURE_HIGH_ACCURACY_TRANSCRIPTION.md:3` declares retirement). Do not remove the privacy guarantee as obsolete or infer that a remembered old AI backend is still used.
- `content/faq/oto-miru.md:100-108` gives short yes/no answers then expands them; this is intentional FAQ structure, not redundant navigation.
- Nocca's development note appears in Product, SEO, Guide, FAQ, and dated article. This is intentional publication-state qualification across direct landing pages. The seven-day trial / Apple fourteen-day trial / deletion-does-not-cancel distinction is intentionally repeated in Privacy and Terms. Keeping these aligned is more important than suppressing every repeated sentence.

## Time-sensitive wording inventory / current judgment

| Surface | Source evidence | Judgment |
|---|---|---|
| Nocca release state | `data/apps.json:157` development; `data/product_details/nocca.json:8,58`; `content/htu/nocca.md:9`; `content/faq/nocca.md:7,17-21`; `content/notes/2026-09-06-nocca.md:10`; Privacy/Terms line 13; all six SEO entries | Consistent unpublished/development qualification. Retain; no local proof of Store public release. App repo `docs/APP_STORE_METADATA.md:34` says NOT SUBMITTED. |
| Nocca iPhone/Japanese/Japan only | `content/faq/nocca.md:25-27`, all Product locale platform/OS values | Matches local `Nocca.xcodeproj/project.pbxproj:510,523` and `docs/APP_STORE_METADATA.md:156-161`. Six site languages do not imply app localization. |
| Nocca `現在の実装ではAIを使いません` | `content/faq/nocca.md:99` | Current design condition, not proven obsolete. |
| Nocca `対応版のサポート情報をコピー` | `content/privacy/nocca.md:25` | Deliberately distinguishes new working-tree UI from uploaded build; app repo `docs/APP_STORE_METADATA.md:48` explicitly says support-copy source change is not included in existing uploaded build 2. Retain version-neutral qualification. |
| OtoMiru submitted/development-screen notice | `content/htu/oto-miru.md:9`, `content/faq/oto-miru.md:7`, `data/apps.json:98` screenshotsStatus review, `data/ux/ja.json:38` | Kept separate from published app state. Local `docs/ux/REPORT.md:270` records public 1.0.1 vs submitted 1.1.0 at its check; no new public-state inference from that dated report. |
| OtoMiru `初期リリースでは日本語字幕` | `content/faq/oto-miru.md:29` | Matches all Product locale notes and current app metadata. Could be tightened to supported Japanese language without `初期` on the living FAQ, but no contradiction. |
| OtoMiru `現在の字幕機能` / `現在の仕様` | `content/faq/oto-miru.md:47,202` | Consistent with current code; version qualifications at top remain important. |
| OtoMiru article `今のオトミル`, `現時点では`, `初期リリース` | `content/notes/2026-05-19-oto-miru.md:57,97,107` | Historical article; preserve history and mark current-vs-initial conditions (C-COM-02). |

## Confirmed alignment (no content correction proposed)

- OtoMiru minimum iOS/iPadOS 26, iPhone+iPad support: `data/product_details/oto-miru.json:2`, `content/htu/oto-miru.md:13`, `content/faq/oto-miru.md:43`, app project Release config `project.pbxproj:620,632`.
- OtoMiru free 15 minutes/day, rewarded +5 minutes at most three/day: Guide `:67`, FAQ `:136-142`, Terms `:55-59`, app `FreeUsageLimiter.swift:18-20` (`900`, `300`, `3`). Plus standard offline unlimited/no ads matches current app spec and all six locale descriptions; no AI or Pro sales claim was found in current site text.
- Nocca trial starts only on first approved connection (7 days); Apple eligible intro is separately 14 days; one currently connected Nocca-family member's active plan covers family; Apple Family Sharing is a different system. Website `privacy/nocca.md:41-47`, `terms/nocca.md:29-53` match current app `docs/FEATURE_SUBSCRIPTION.md:5-13,39-43`.
- Nocca retention: invitation 30 days, transfer 7 days, recovery 24 hours (`handler.py:29-31`); subscription ledger 400-day TTL (`subscriptions.py:16,454,516,531`); logs 30 days (`cloudformation.yaml:315,357`); backup/inquiry operations distinguish actual auto-retention from manual policy (`docs/PRIVACY_OPERATIONS.md:11,23-24`). These align with `content/privacy/nocca.md:53-69`. No reinterpretation of the legal policy or remote operations validation was performed.
- Nocca owner-led communication, invitation approval, preset progress/completion replies, chat only while owner opens it, pause/mute, no read/typing/GPS, family-side deletion vs owner deletion are consistently described across Product/Guide/FAQ/Privacy/Terms.

## Limits

This is current local content consistency analysis. It does not establish live store prices, trial eligibility, purchase success, App Store public availability, legal compliance, current deployed backend configuration, or cache-free public-site equivalence. Those require the parent task's appropriate direct checks; none was silently inferred.

Memory was only a lightweight source-discovery aid, and product assertions above were rechecked in local files. Relevant registry pointers read: `MEMORY.md:524-528` (OtoMiru StoreKit display-price workflow) and `MEMORY.md:1092-1114` (Nocca release-state separation); rollout IDs `01a07535-f534-7080-a797-5c07dbe3f66e`, `01a0761a-4beb-7ab3-8a86-7495d86735e4`.
