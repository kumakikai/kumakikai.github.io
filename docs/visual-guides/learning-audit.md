# Uni:Note / Uni:Note Pocket visual-guide audit

Updated: 2026-09-07 (JST).

## Scope and publication boundary

- Updated all existing guides and FAQs for **Uni:Note** and **Uni:Note Pocket** in ja, en, de, fr, ko and zh-hant: **24 Markdown pages**.
- Kept every page URL, front-matter alias and app-specific Privacy Policy URL. Privacy/Terms/Product/News content was not edited by this work.
- Uni:Note public version is **3.4.0**, verified by the root agent in `store-snapshot.json`. The current local worktree identifies itself as **3.5.0** and contains unpublished UI changes. Basic instructions and reused screenshots describe applicable 3.4.0 flows. The four 3.5.0 additions are explicitly marked as **before release**, in all six languages: subject-card Note List shortcut, toolbar/palette customization, manual/editable question sets, Home question-set visibility.
- Pocket public and local versions are **3.4.0**. Title search and Easy Backup file-status refresh were added to every guide.
- Both application worktrees already contained changes. No source, app data, release setting, translation, entitlement or purchase was changed.

## Guide structure

Uni:Note changed from 16 long sections to nine practical sections:

1. Create a subject and first note; folders.
2. Select tools and write; Pencil versus finger, zoom, ruler, range move.
3. Switch notes and search titles.
4. Attach photos/document photos/PDFs and export PDF.
5. Record, save and play a lecture; transcription/AI conditions.
6. Sticky-marker review, Problem Solver Assistant, generated practice sets.
7. Protect, delete and restore.
8. Backup and audio-inclusion setting.
9. iPad multiwindow notes, without prescribing one obsolete OS gesture.

Pocket changed from 11 sections to six:

1. Import an intact Uni:Note backup zip.
2. Open/search/read a note and resume a page.
3. Review sticky markers and imported question sets.
4. Play imported recordings, with audio-inclusion condition.
5. Reading preferences.
6. Refresh Easy Backup metadata, load manually or enable load-on-launch.

The shared `guide-image` component provides WebP, responsive size, lazy loading, dimensions and click-to-enlarge. `lastmod` is the actual edit date. The framework supplies the TOC and related support links; duplicated FAQ/Privacy link lists at the end of articles were removed.

## Confirmed stale or redundant content

| Old material | Change and current evidence |
|---|---|
| Uni FAQ listed Range Move as Premium and repeated the selection steps | Explicitly Free, matching current `FEATURE_SUBSCRIPTION`, `FEATURE_NOTE_TITLE_SEARCH` and `NotebookViewController`; full operations live in guide. |
| Uni guide/FAQ warned that going Home or sleeping may corrupt audio, immediately after saying it is saved | Removed unqualified corruption claim. Kept practical stop-and-save instruction; current recording implementation prioritizes safe save and stops navigation on save failure. No claim that a known crash is fixed. |
| Fixed transcription model list based on old external platform description | Replaced by actual runtime conditions: iPadOS 26+, `SpeechTranscriber.isAvailable`, supported locale/model. App displays unavailable reason; recording/playback remain. |
| Old “recent updates” changelog list in FAQ | Removed obsolete history from task-oriented FAQ. Direct to app Notices; local 3.5.0 additions are marked before release. |
| Old v3.0.0 marker/import wording | Removed version-specific migration explanations. Explain the current per-marker tap behavior and importing a current exported backup. |
| Pocket guide lacked note-title search and refresh-next-to-last-updated | Added in six languages; `MemoBookshelfViewController` search and `MemoSettingsViewController` refresh/manual-load implementation confirmed. |
| Pocket memorization doc still described a whole-page eye control | Treated as outdated project documentation. `MemoPageViewController` has `MemoStickyNoteOverlayView` and per-entry `isTransparent.toggle()` (around line 1258); guide uses the actual per-marker behavior. No app source/doc modification. |
| Duplicate creation, PDF, recording and AI step lists in FAQ | Replaced by conditions/exceptions and direct guide anchors. No Support hub or app re-selection. |
| Detailed setting inventories and repeated marketing description | Reduced to normal operations and conditions. No new pricing values or unsupported functionality. |

Confirmed constraints retained: Pencil handwriting, 150 pages per note, Free 10 subjects/6 notes per subject, Premium recording/Easy Backup, shared AI balance, AI summaries from transcript rather than audio upload, audio opt-in for backups, no realtime sync, Pocket read-only, no Pocket recording/transcription/AI generation.

## Images and provenance

`learning-assets.json` records the source absolute path, original SHA-256, dimensions, exact crop rectangle, output SHA-256, locale and selection reason for every image. It also records app source/document hashes and worktree commit identities.

Initial asset set: **58 unique image files**, **84 guide references**, all referenced. The root integration may add newly captured backup screenshots or refine the small control crops; its later manifest entries supersede this initial count.

- Sources are real Simulator captures from the projects’ 2026-09-02 Store-asset working folders, including 2026-09-03 localized recaptures. **No marketing background/copy images were used as operation screenshots.**
- Uni:Note: shared Add button, real palette, lecture PDF with handwriting, sticky-marker area, recording controls; localized search field, attachment menu, assistant result. The menu crop deliberately includes only the four ordinary attachment/export entries, excluding debug-only items present in some localized source captures.
- Pocket: localized backup-import control, Notes/recent/subject area, continuous page reading, question-and-answer card, sticky review, search field.
- Crop was preferred for controls and panels. Pocket’s continuous page viewer retains a full screen because the relationship between pages and scrolling is the subject. Its question card retains answer and next/previous buttons together. Uni’s PDF view keeps the attachment and handwriting together.
- The Japanese Pocket search example initially uses the current English UI capture; it is explicitly captioned as English rather than presenting it as a Japanese screen. Other localized guide controls use their matching existing raw locale. Shared handwriting content is clearly educational demo material, without real personal information.
- No AI image creation, UI reconstruction, production payment, live-user data or real email/contact was used.
- No old website images were removed: they may remain in Product/Home use, and these are new guide-specific assets.

## URL/fragment compatibility

All **654** original FAQ/guide fragment IDs across the 24 pages are retained with the shared `guide-anchor` shortcode, mapped to the corresponding current topic. The original body texts remain in immutable `docs/migration/baseline.json`; authorized revisions are handled by the root’s reviewed-content guard.

Mappings:

- Uni guide old first-subject/first-note → `#create`; writing/zoom/tools/ruler → `#write`; Note List → `#find`; More/photo/PDF → `#pdf`; recording → `#recording`; memorization/solver/practice sets → `#review`; protection/Trash → `#protect`; settings/backup → `#backup`; multiwindow → `#windows`.
- Pocket guide first-use/import → `#import`; Home/note/page → `#read`; markers/practice sets → `#review`; audio → `#recordings`; settings → `#settings`; Easy Backup/newer import → `#refresh`.
- FAQ original headings and questions are grouped at the same current topic: Uni requirements, notes, PDF, recording, study, backup/diagnostics, display settings; Pocket requirements, import/update, reading/audio/markers, display settings.
- Direct FAQ links use localized Hugo `relref` plus stable guide fragment IDs. Privacy is still reachable from the common app-specific support links immediately below the content.

## Verification and remaining capture details

- `git diff --check` for the 24 owned Markdown files: PASS.
- Original fragment-ID coverage check: **654/654**, no missing IDs.
- Asset-reference check: **58/58 used**, no missing referenced source images in the initial set.
- Raw images and representative crop contact sheets inspected visually before use. Root completed initial Japanese guide browser QA at 1440px and 390px, across seven conditions (light/dark, FAQ and no-JavaScript checks). The separate final seven-viewport, all-locale/layout/image checks remain root integration work.
- Current Uni:Note 3.5.0 Simulator Debug build: **BUILD SUCCEEDED** with a task-specific DerivedData path `/private/tmp/kumakikai-guide-uninote-derived`. No product source edits. This is a build check, not App Store publication proof.
- CUA `getApp("Simulator")` became unresponsive for approximately 25 minutes; no image was captured or reused from that failed interaction. Subsequent capture is handled by the root through simulator CLI and actual UI interaction.
- Assigned iPad was booted by this work, had no Uni:Note installed at the initial inventory, and was handed to root for backup-settings capture. Assigned iPhone was not booted by this agent. Root owns finishing capture and shutdown of only these task-started devices.
- No Apple Pencil hardware, production AI request, StoreKit purchase, iCloud account flow or real-device operation was executed. Source/spec/real existing screen checks do not claim those end-to-end validations.

## Added backup capture and final independent review

- Added the newly captured Japanese Backup file-actions image to all six Uni:Note guides. Crop `[40,1090,1120,335]` preserves the File heading, Export Backup and Restore from File rows, and removes the disabled Premium/iCloud panel and unrelated screen area. Other-language captions explicitly identify the Japanese UI and map the upper/lower action. Initial 58 assets/84 references are now **59 assets/90 references**, before further root-owned refinements.
- Compared the captured current worktree to the Uni:Note 3.4.0 release commit `12d91ce`: `BackupRow`, `BackupDetailSection`, `makeBackupCell`, `makeBackupRecordingAudioCell`, `makeBackupFileCell`, `handleBackupSelection`, `exportBackupFile` and the audio-switch handler match byte-for-byte, as do the Japanese backup file/audio labels. This makes the cropped actions applicable to the public 3.4.0 despite capture from the local 3.5.0 build. Symbol hashes are recorded in the asset manifest.
- Put the optional audio-inclusion step before Export in all six guides. Clarified sticky-marker deletion as long-press **then tap the displayed Delete button**, matching `NotebookViewController.handleStickyNoteLongPress` and `stickyNoteDeleteButton`. Added verified iPadOS 17.0 / iOS 17.0 requirements to all twelve FAQs.
- Read-only review of `guide-image`, `guide-anchor`, `guide-toc`, `single.html`, guide CSS, `record-guide-review.py` and `verify-migration.py`: no blocking issue found. Native link/details controls preserve keyboard behavior; visible focus, useful alt text, lazy WebP/srcset, intrinsic dimensions and no-upscaling are present. The review exception is limited to the exact existing app HTU/FAQ routes and matches source/baseline/rendered hashes; all legacy routes, canonical URLs, aliases and fragment IDs remain checked. Privacy/Terms/News cannot opt into this exception. Link removals must match the explicit reviewed list; duplicate IDs and image references remain checked. No shared component or verifier was modified by this independent review.

## Editorial correction after production-browser reading

The first production rendering was reviewed at 1440px and 390px. This revealed three image-quality issues that mechanical checks did not catch: icon-only Add/import context, a too-small backup label crop on mobile, and too-small answer-sheet controls. Findings and screenshots are documented in `editorial-learning-signal.md`.

- Pocket imports now include the actual bottom search field and import control from current localized raw UI (`[30,2020,1110,445]`). The Japanese example uses current English UI and is explicitly captioned.
- Uni answer controls now use `[1380,815,260,145]`, paired with the result state's Copy-left / Share-right instruction. All six languages now put the instruction before its image.
- Backup now uses `[40,1090,680,335]`, preserving both complete primary labels while prioritizing mobile legibility over secondary row descriptions.
- Uni's isolated Add icon was replaced by six newly captured creation menus. The first instruction names the actual localized action, followed by the menu image before the fields/note steps. Root's `uninote-create-assets.json` records their source and compatibility; the now-unreferenced old Add asset was removed.
- After this correction the learning portion has **64 distinct assets** across the learning and root creation-menu manifests, with **90 guide references**. Counts remain subject to root integration's final asset inventory.

- Final Korean cross-check clarified that deleting the **only remaining page** clears that page; it does not describe deleting the notebook itself. This preserves the same operation distinction as the other five languages.

- Post-correction production browser recheck completed: Uni creation-menu, answer-actions and backup plus Pocket import at both 390px and 1440px, **8/8 editorial checks passed**. Saved readable viewport captures ending `-final.jpg`; detailed results are in `editorial-learning-signal.md`. No guide/asset edits followed this production check.
