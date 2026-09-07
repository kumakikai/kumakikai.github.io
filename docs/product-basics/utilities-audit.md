# Utility products: current device and minimum OS source audit

Audited 2026-09-07. App repositories were read only. Existing dirty worktrees were checked first and preserved. No app builds, tests, source edits, Store uploads, or publication changes were performed. Structured extraction: `utilities-audit.json`. Current public Apple lookup results are recorded separately in `app-store-verification.json`.

| Product | Current Release app target | Minimum OS | Device | Publication distinction |
|---|---|---|---|---|
| すわなび | Runner | iOS 14.0 | iPhone | Public 1.1.1 uses iOS 14.0. Local 1.2.0 (3) contains Watch support; it is not the public binary. Preserve the existing Watch review notice. |
| すわなび Apple Watch | SmokelessWatchApp | watchOS 9.0 | Apple Watch | Upcoming companion feature; do not present it as available in public 1.1.1. |
| ギャンカレ | Runner | iOS 14.0 | iPhone | Public 1.4.0; current project version 1.4.0 (2). |
| SIGNAL | Runner | iOS 13.0 | iPhone | Public 1.1.1; current project version 1.1.1 (1). |

## すわなび

All source paths below are relative to `/Users/yuya/Projects/smokeless`.

- `ios/Runner.xcodeproj/project.pbxproj:1083` maps project Release configuration; `:1093` maps Runner Release to `97C147071CF9000F007C117D`.
- Project Release `IPHONEOS_DEPLOYMENT_TARGET = 14.0` is at `:766`. Runner Release inherits this value and overrides device family to `TARGETED_DEVICE_FAMILY = 1` at `:835`.
- Project-level family `1,2` at `:772` does **not** mean the app supports native iPad: the Runner target override is authoritative.
- Watch Release configuration starts at `:1019`, `SDKROOT = watchos` at `:1039`, family `4` at `:1044`, and `WATCHOS_DEPLOYMENT_TARGET = 9.0` at `:1046`. Companion bundle is set at `:1031`; its version is 1.2.0 at `:1036`.
- Widget Release is a separate app-extension target: deployment target 14.0 at `:913`, family 1 at `:935`. These values do not substitute for the app target.
- `ios/Flutter/Release.xcconfig:1–2` includes Pods Runner Release and Generated settings. Neither included file overrides deployment target or device family. `ios/Podfile:2` and `:40` both use 14.0.
- `ios/Flutter/AppFrameworkInfo.plist:23–24` says 13.0 for the Flutter **framework**, not the Runner app. Do not lower the website requirement to that value.
- `pubspec.yaml:22` and `ios/Flutter/Generated.xcconfig:7–8` set 1.2.0 (3).
- `docs/RELEASE_NOTES_1_2_0.md:3` labels the version as an upload draft and says submission/publication was not performed in that documented task; `docs/APP_STORE_METADATA.md:69` says Store entry/publication unconfirmed. Those older task notes do not override the user's newer confirmation that Watch is in review. The separate current public lookup establishes that 1.2.0 is not public.
- iOS 14.0 is the iPhone app's deployment target, not a claim that every iOS 14 iPhone can pair with watchOS 9. The existing Watch notes must retain the requirement for a compatible paired iPhone and supporting app versions on both devices.

## ギャンカレ

All source paths below are relative to `/Users/yuya/Projects/gamble_pnl`.

- `ios/Runner.xcodeproj/project.pbxproj:883` maps project Release; `:893` maps Runner Release.
- Project Release deployment target 14.0 is at `:659`; Runner Release inherits it and overrides family to 1 at `:728`.
- Project family `1,2` at `:665` is superseded by the Runner target's family 1. No native iPad claim is supported by this app target.
- Widget Release is a separate app-extension target: deployment target 14.0 at `:806`, family 1 at `:828`, version 1.4.0 at `:813`.
- `ios/Flutter/Release.xcconfig:1–2` includes Pods Runner Release and Generated settings, with no deployment-target/device-family overrides. `ios/Podfile:2` and `:40` both use 14.0.
- `ios/Flutter/AppFrameworkInfo.plist:23–24` contains framework minimum 13.0, which does not override Runner 14.0.
- `pubspec.yaml:25`, `ios/Flutter/Generated.xcconfig:7–8`, and `docs/APP_STORE_METADATA.md:82–85` establish local 1.4.0 (2). The metadata states that the earlier version-update task did not finalize release copy; it is not proof that the current public version is unpublished. Current public lookup is the publication source.

## SIGNAL

All source paths below are relative to `/Users/yuya/Projects/signal`.

- `ios/Runner.xcodeproj/project.pbxproj:766` maps project Release; `:776` maps Runner Release.
- Project Release deployment target 13.0 is at `:685`; Runner Release inherits it and uses family 1 at `:748`.
- `RunnerTests` is a unit-test target mapped at `:756`; its `MARKETING_VERSION = 1.0` at `:548` is **not** the app release version.
- `ios/Flutter/Release.xcconfig:1–2` includes Pods Runner Release and Generated settings, with no deployment-target/device-family overrides. `ios/Podfile:1` and the Flutter framework minimum both use 13.0.
- `pubspec.yaml:19` and `ios/Flutter/Generated.xcconfig:7–8` establish local 1.1.1 (1). Current public lookup separately confirms version 1.1.1 and minimum iOS 13.0.

## Outcome for website data

All three existing `data/product_details/<id>.json` minimumOS values match the current Release app targets. No OS version correction is required for these three products. Keep these required fields when unifying the shared table; keep Watch 9.0 explicitly conditional on the pending Watch release.
