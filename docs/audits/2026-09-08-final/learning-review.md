# Learning products: local-source consistency audit

Audit basis: `/Users/yuya/Projects/homepage`, branch `main`, HEAD `0fba8cf`; initial status only `?? .DS_Store`. Read-only. No search engine, browser/cache, or public-page evidence was used. Application repositories were inspected read-only; both contain unrelated dirty work, preserved. Their current local implementation is evidence of implementation only, not public App Store release state.

## Scope

- Uni:Note + Uni:Note Pocket: `data/apps.json`, both `data/product_details/*.json`, both product entries in all 6 `data/home/*.json` and `data/seo/*.json`.
- 48 product-specific content pages: 12 generated Product entries, 12 Guide, 12 FAQ, 12 Privacy, covering ja/en/ko/de/fr/zh-hant. No custom Terms files or termsURL for these 2 apps; common Apple Standard EULA fallback in `data/support.json:2` is intentional.
- 3 Japanese historical News/Notes articles: `content/notes/2026-03-12-uni-note.md`, `2026-04-01-uni-note-pocket.md`, `2026-04-12-uni-note-10000.md`.
- Relevant shared article/support template and WEBSITE_MAINTENANCE rules. Root audit owns complete generated HTML link/anchor/graph scan, so no sitewide totals are asserted here.

## Finding L1 — confirmed terminology mismatch, low impact

Korean Uni:Note Guide/FAQ/Privacy call the same AI balance feature `AI 잔량`, while Product and actual app call it `AI 잔액`.

- `content/htu/uni-note.ko.md:70,86`: `AI 잔량`.
- `content/faq/uni-note.ko.md:55`: `공통 AI 잔량`.
- `content/privacy/uni-note.ko.md:41,45`: heading/body `AI 잔량`.
- Canonical site Product: `data/product_details/uni-note.json:232`: `AI 잔액`.
- Current app: `/Users/yuya/Projects/uni_note/ko.lproj/Localizable.strings:522`: `premium.settings.card.ai_balance.title = AI 잔액` (additional current labels at 523, 528, 530).
- Website maintenance section 4 also explicitly prescribes `AI 잔액`.

Recommendation: replace the feature-name phrase in those 5 content lines with `AI 잔액`; leave the compatibility anchor `ai-잔량은-무엇인가요` in FAQ line 49 intact, and do not mechanically change every ordinary-language use of 잔량. This is label consistency, not a change of feature/purchase terms. Source/content review manifest requirements still apply.

## Finding L2 — time-sensitive state claims, not proven stale

All 6 Uni:Note Guide and FAQ translations directly identify 3.4.0 as the public version and 3.5.0 as upcoming. Examples:

- `content/htu/uni-note.md:6`: `公開中の3.4.0`.
- `content/htu/uni-note.md:44,96`: `3.5.0の公開前情報` and `公開中の3.4.0`.
- `content/faq/uni-note.md:54,72`: `3.5.0公開前`, `公開中の3.4.0と、開発中の3.5.0`.
- en/de/fr/ko/zh-hant equivalent Guide lines 7/44/88 and FAQ 55/73.

Both Guides/FAQs have lastmod 2026-09-07. Current app source has local MARKETING_VERSION 3.5.0 (`UniNote.xcodeproj/project.pbxproj:1068`) and dirty upcoming features, but this does not establish 3.5.0 general release or prove website state wrong. Local source contains historical evidence only. Recommendation: attach an explicit source-verification date to the release comparison, or use a version-scoped Guide description which does not assert an always-current Store state. Do not silently advertise the upcoming features as released.

## Finding L3 — historical status wording, preserve article meaning

- `content/notes/2026-03-12-uni-note.md:8,42,52`: `開発しています`, `現在のところ`, `入れていく予定`.
- `content/notes/2026-04-01-uni-note-pocket.md:27-43`: manual-backup-only path and future automatic-backup consideration; `:47-51` uses old memorization-mask wording.
- `content/notes/2026-04-12-uni-note-10000.md:26-37`: slow review, AI under development, subscription plan, next/next-next update, overseas release planned.

Current Product/Guide/FAQ describe implemented backup, AI Balance, all six localized surfaces, etc. These articles have explicit March/April publication dates, and current metadata descriptions intentionally identify them as development history / original launch workflow / April record. `layouts/single.html:5` displays publication and update dates, and line 9 already appends related current Product links. Classify as historical content, not a proven present-day product contradiction. Their lastmod 2026-09-07 can still make the historical tense unclear. Recommendation: one shared dated historical-context note if the root audit decides clarification is necessary; do not rewrite the original articles to invent an updated release announcement or current commercial terms.

## Finding L4 — Privacy wording ambiguity, no automatic factual rewrite recommended

`content/privacy/uni-note.md:19` says selected images/files are processed by user operation and `開発者が内容を取得することはありません`; section 4, lines 31-33, states selected images/PDF excerpts/transcripts can be sent to external AI services. Section 6 line 55 also broadly says those contents `送信しません` within its diagnostics heading. All 5 translations preserve the same structure (section-2 phrase line 20, diagnostics phrase line 55).

The intended scopes are probably file/backup operations and diagnostic logs. Those scopes are apparent from headings but the standalone statements can be read too broadly. Current implementation sends selected image base64 through AWS AI Proxy (`/Users/yuya/Projects/uni_note/App/ProblemAssistOCRService.swift:382-425`, `App/AIProxyClient.swift:164`) and sends transcript text for summaries (`App/LectureAISummaryService.swift:517,725-738`). This proves a relevant transmission path, not human access or retention. Current FAQ already scopes the exclusion to diagnostics (`content/faq/uni-note.md:64`). Recommendation: if changing legal wording in scope, explicitly qualify existing section-2 statement to attachment/backup processing and section-6 exclusion to diagnostic logs, preserving section 4 exception. Do not invent AI-provider retention periods or assert unverified production processing facts. This is an ambiguity / review item, not a confirmed storage-policy contradiction.

## No-issue areas checked

- Device/OS values agree in Product and all FAQ translations and current app Release settings: Uni:Note iPad/iPadOS 17.0 (`UniNote.xcodeproj/project.pbxproj:1063,1081`); Pocket iPhone/iOS 17.0 (`UniNotePocket.xcodeproj/project.pbxproj:334,348`). Pocket core package macOS test support was not misrepresented as product availability.
- Uni:Note Free 10 subjects and 6 notes/subject matches `App/PremiumAccessController.swift:23-25`; 150-page limit matches `Domain/Section.swift:7`; 5 recordings/30-minute split matches `UI/NotebookViewController.swift:2074-2075`.
- Guide and FAQ consistently distinguish recording playback/transcript Premium and transcription supported iPadOS 26 environments from the general iPadOS 17 app minimum.
- Guide/FAQ/Privacy agree that AI summary uses transcript text rather than uploading the recording audio; current summary request payload confirms transcript input.
- Both apps consistently describe imported/local note data and iCloud file backup, rather than live/bidirectional synchronization. Pocket auto-load on launch is expressly loading an existing snapshot and is not in conflict with no-realtime-sync. Source `MemoSystemBackup.swift:45` downloads the cloud file; no syncing of edited Pocket data is claimed.
- Pocket Product/Guide/FAQ/Privacy consistently restrict creating/editing/reordering/recording/transcription/AI generation to the iPad app. Search consistently covers explicit note titles and excludes handwriting/PDF/body/subject names.
- Pocket package has no external SDK dependencies; targeted current app/package/project scan found no Firebase/Crashlytics/Analytics/GoogleMobileAds/AdMob. Website no-ad/analytics-SDK statement is supported by this local dependency scan, not a guarantee about unseen external distributions.
- Uni:Note current diagnostics imports FirebaseCrashlytics and uses typed/sanitized diagnostics metadata; FAQ/Privacy acknowledge Crashlytics and exclude content from diagnostic logs. No unsupported claim of complete absence of all telemetry was found.
- No legacy `関連ページ` block in either app’s current Guide/FAQ/Privacy source. FAQ links to individual Guide anchors carry a specific answer context and should remain.
- Historical News retains contact/support references; generic `article-about` mail link in shared template can duplicate their body contact link. Root generated-link scanner should classify this structural duplication rather than deleting historical article bodies.
- Expected repetition (legal policy boilerplate across related apps, common support UI, product names/minimum OS, brief Guide prerequisite restatement in FAQ) was not treated as excessive duplicate prose.

## Verification limits

No edits, app builds, Store requests, purchases, retention-service requests, or public-page fetches performed by this subaudit. Current release/storefront verification is not proven by local app source; existing `data/apps.json` published state and 2026-09-07 storefront metadata remain site assertions for root to treat separately. No new numerical retention/purchase claim has been proposed.

Memory registry was consulted only to locate relevant areas and reinforce the public/local-version boundary; every finding above is grounded in current files. If the parent needs a memory citation: MEMORY.md:24-25 (registry used only for public/local boundary), rollout id `01a079e4-55f5-7712-abcc-57bb10aac81f`. No prior release-version fact was accepted as current evidence.
