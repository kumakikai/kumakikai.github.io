# Other Appsの展開表示と実画面素材

更新日: 2026-09-07

Homeの先頭4アプリは常時表示を維持し、後半4アプリはタイトルだけの`details`／`summary`に変更。開くとFeaturedと共通の`app-showcase.html`でアイコン・対応機種・既存説明・App Store／詳細CTA・実画面2枚を表示する。複数同時に開け、JavaScript無効時も操作できる。Featured右側の「01 — 04」は削除した。

既存のアプリ分類、順序、名前、説明、Featuredのキャッチコピー、App Store提供地域の扱いは変更していない。画像は同じデータからProduct詳細にも表示する。既存のSupport、使い方、FAQ、Privacy、NotesのURL・本文・リダイレクト設定は変更していない。

## 採用素材

すべて既存アプリリポジトリにある実UIのキャプチャ、または実UIから制作済みのApp Store素材。AI生成やUIの描き直しは行っていない。今回確認したのは制作済み素材と現行機能の対応であり、これらの画像のApp Store掲載状況は未確認。

原本パス・SHA256・変換後寸法・ハッシュ・SIGNALのcrop矩形は[素材記録](other-app-assets.json)に保存。

| アプリ | 使用した2画面 | 元素材 |
|---|---|---|
| Uni:Note Pocket | 手書きノート閲覧／バックアップから読み込んだ本棚 | `uni_memo/artifacts/app_store_screenshots_2026-09-02/final/SS01_review_now.png`、`SS02_import_backup.png` |
| ギャンカレ | 収支の登録／日・月・年の収支確認 | `gamble_pnl/artifacts/app_store_screenshots_2026-09-03/final/01_gambling_instant.png`、`04_day_month_year.png` |
| すわなび | 喫煙・我慢の記録／本数の集計 | `smokeless/design/app-store-screenshots-2026-09-03/final/1284x2778-upload/01-value.png`、`03-counts.png` |
| SIGNAL | CREATORSフィード／配信源設定 | `signal/artifacts/app_store_screenshots_2026-09-03/source/ui_captures_clean/creators.png`、`source/ui_captures/settings.png` |

SIGNALは価格・無料表現入りの販促素材を使わず、実UIを使用。設定画面は元画像上端150pxのOSステータスバーのみを除き、アプリのタイトル・表示内容を保持した。

## 配信

- 各画像を横420px／840px、品質86のWebPに縮小し、原本は変更しない。
- `data/apps.json`に2解像度と実寸を登録。`srcset`、`sizes`、`width`／`height`、`loading="lazy"`、`decoding="async"`は共通partialで付与する。
- 6言語の`imageAlts`を追加。日本語以外では日本語画面である旨を既存の表示で案内する。
- 閉じた詳細の画像を初期ロード必須にしない。検証では開いた後に画像・説明・CTA・横はみ出し・アクセシビリティを確認する。

## 検証方法

`npm run build`、`npm run verify`に加え、`scripts/verify-browser.cjs`で各画面幅・Light／Dark、6言語、Enter／Space／クリックによる開閉、複数同時展開、JavaScript無効時を確認する。閉状態と展開状態の比較画像も出力する。
