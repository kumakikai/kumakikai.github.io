# Visual guide editorial QA — learning apps, SIGNAL and ギャンカレ

Date: 2026-09-07 JST. Reviewer: learning guide agent.

## Method and scope

- Opened the fixed production build at `http://127.0.0.1:1314` in actual headless Google Chrome, with 1440 × 900 and 390 × 900 CSS-pixel viewports, light mode, device scale 1.
- Routes: `/htu/uni-note/`, `/htu/uni-note-pocket/`, `/htu/signal/`, `/htu/balance-calendar/` (Japanese).
- Loaded the real generated WebP images and scrolled each image into the viewport with its preceding instructions. Captured 50 individual viewport images: Uni 9 × 2, Pocket 6 × 2, SIGNAL 4 × 2, ギャンカレ 6 × 2. Read 34 representative viewport captures at readable size, including every mobile control type and all six ギャンカレ desktop image areas. This was not a full-page miniature or overflow-only assessment.
- Capture paths: `screenshots/editorial-<app>-<width>-<image-name>.jpg`. Automated all-locale/viewport, dark mode, keyboard and broken-image verification is maintained separately by root. These browser observations do not prove the operation inside the apps.

## Findings in the initial production build

| Item | Observation | Disposition |
|---|---|---|
| Uni Home + / Pocket import | Icon-only crops were large and readable, but stripped the surrounding position/context. The screenshot taught the symbol more than where to find it. | Root captured the real Uni creation menu in six languages. Learning guides now place this after step 1 and name the actual Create Subject action. Pocket now includes the import control and adjacent bottom search field from current localized raw UI. |
| Uni backup at 390px | The 1120px-wide crop was rendered at 330px; its two action labels were much smaller than body text. | Narrowed to the left 680px while retaining both complete action labels and the File heading. Secondary explanatory text is not the target of this crop. |
| Uni assistant result at 390px | Full-width answer panel and copy/share icons became too small to identify comfortably. Several translated guides also put the image before its instruction. | Changed to the actual answer-sheet Copy/Share controls, with explicit left/right operation explanation immediately before the image in all six languages. |
| ギャンカレ widget at 1440px | Its simple two-arrow widget occupied approximately 540 × 589px, larger than needed for this operation. | Low-priority size improvement reported to root; root owns the page. |
| ギャンカレ section labels | Markdown inline-code styling exposed backtick marks around ordinary Japanese UI names. | Suggested ordinary Japanese brackets rather than code formatting; root owns the page. |

No wrong operation/image pairing was found in SIGNAL or ギャンカレ. SIGNAL's tab/card controls, close/menu bar, source switches and text/theme selectors remain easy to identify at 390px. ギャンカレ's amount keypad retains Confirm; the daily view retains tabs and bottom navigation; tag settings preserve both edit rows and widget default selection. These screens keep necessary context rather than filling pages with unrelated full-device captures.

Pocket's reading view appropriately retains a full screen to show page scrolling; its exercise crop retains the question, answer area and Previous/Next controls. Current English UI use in the Japanese search/import examples is expressly captioned. Uni attachment-menu and palette controls are legible, and PDF handwriting remains an illustrative result rather than an operation requiring tiny document text to be read.

## Corrective pass

- Updated 13 crops: six Pocket import areas, six Uni answer-sheet controls, and one Uni backup area. Source SHA-256, crop rectangles and output hashes are updated in `learning-assets.json`.
- Replaced Uni's one common Add-icon source with six real creation-menu captures recorded separately by root in `uninote-create-assets.json`. Removed the old file only after confirming no content references remain.
- Corrected all six guide variants for each affected app. Preserved legacy fragment IDs and URLs; no FAQ/legal body changes in this corrective pass.
- `git diff --check`, image-shortcode argument parsing, nonempty alt text and source-file existence passed after editing.
- Root rebuilt production after the corrective pass. All four changed image areas were reopened at 390px and 1440px, recaptured as eight viewport images, and individually read at normal readable size. All eight corrective checks passed. The initial findings above remain as before/after evidence; the following files are the corrected build.

## Corrected production viewport results

| Area | 390px | 1440px | Visual result |
|---|---|---|---|
| Uni creation menu | [Mobile](screenshots/editorial-uni-note-390-create-menu-final.jpg) | [Desktop](screenshots/editorial-uni-note-1440-create-menu-final.jpg) | Both actions are readable; the menu is immediately after the +/Create Subject instruction and before the following steps. |
| Uni answer actions | [Mobile](screenshots/editorial-uni-note-390-problem-answer-final.jpg) | [Desktop](screenshots/editorial-uni-note-1440-problem-answer-final.jpg) | Copy and Share are clearly distinguishable; the preceding paragraph states the result-sheet position and left/right mapping. |
| Uni backup | [Mobile](screenshots/editorial-uni-note-390-backup-file-actions-final.jpg) | [Desktop](screenshots/editorial-uni-note-1440-backup-file-actions-final.jpg) | Export Backup and Restore from File labels are complete and readable. The crop intentionally truncates only secondary text; the guide supplies the operation meaning. |
| Pocket import | [Mobile](screenshots/editorial-uni-note-pocket-390-import-backup-final.jpg) | [Desktop](screenshots/editorial-uni-note-pocket-1440-import-backup-final.jpg) | Import control retains its bottom-right relationship to title search. English-UI caption is visible and no oversized isolated icon remains. |

No new text/image-order, clipping of target labels, or viewport layout issue was found in this corrective recheck. This is a light-mode Japanese editorial pass; root's separate browser matrix covers the broader conditions.
