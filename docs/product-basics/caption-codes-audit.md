# オトミル・ギガポケ: 対応環境と用語の確認

確認日: 2026-09-07。両アプリで `git status --short` を先に取得し、既存の未コミット作業を維持。アプリ側ファイルの編集・ビルド・Simulator操作はしていません。

| Product | 対応端末 | 確認済み最低OS | ローカル Version / Build |
|---|---|---|---|
| オトミル | iPhone / iPad | iOS 26.0以降 / iPadOS 26.0以降 | 1.1 / 1 |
| ギガポケ | iPhone | iOS 17.0以降 | 0.1.0 / 1 |

オトミルは `OtoMiru.xcodeproj/project.pbxproj:608-634` のアプリ用 Release 設定で Deployment Target と Device Family を確認。`DeviceSupportPolicy.swift:68-76` では OS 要件に加え、Apple の音声認識と日本語の対応可否を確認しています。OS の数字だけで全端末が字幕を使えるとは断定しません。

ギガポケは `PovoCodeManager.xcodeproj/project.pbxproj:711-736` のアプリ用 Release Device Family と、プロジェクト Release → `Config/Release.xcconfig:1` → `Config/Shared.xcconfig:14-16` の設定継承を確認。iPhone / iOS 17.0 の既存Webデータと一致しています。

## 公開状態との区別

サイト側は両アプリとも `published`。本監査は最新ローカル設定の確認であり、上表のローカル版が App Store 公開済みであることを意味しません。特にオトミルの `docs/APP_STORE_METADATA.md:63` は v1.1 の App Store Connect 新バージョン作成・提出・公開が未実施と明記しています。公開状況の最終判断は別途、本番ストア情報と突き合わせます。

## 用語

- 両アプリの基本情報 notes に `quota`、`credit`、`entitlement`、`クォータ` はありません。
- オトミルのWeb本文は App Store 説明と同じ「シンプルモード」を使用していますが、最新設定の実ラベルは「高齢者向け」(`Views/SettingsView.swift:136`) です。機能紹介と設定操作ラベルの差として報告します。マーケティング画像や未公開版に関わるため、画像やアプリ側の文言を機械置換していません。
- ギガポケの「ギガコード」「外部特典」「ペースト」「povo 2.0」「非公式」は現行画面で確認でき、基本情報 notes と矛盾しません。

詳細な出典・行番号・確認時の SHA-256 は [caption-codes-audit.json](caption-codes-audit.json) に記録しています。
