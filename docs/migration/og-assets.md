# OGP画像

制作・目視確認: 2026-09-06。

`static/images/og/` に、共通フォールバック `default.png` と8アプリの `<app-id>.png` を保存した。全9枚が1200×630px、PNG形式、各15〜32KiB。サイトの通常ビルドは保存済み画像を配信するため、画像生成ツールや追加フォントに依存しない。

## 素材と表現

- 画像は既存の実アプリアイコン `static/images/apps/<app-id>/icon.webp` のみ。元の出典は `docs/homepage/asset-manifest.json` を参照。
- ブランドはKUMAKIKAI、アプリ名・プラットフォーム・Featuredのキャッチコピーは `data/home/ja.json`、掲載順と公開状況は `data/apps.json` から取得。
- 共通画像は現在のHeroコピーと8アイコン、`iPhone & iPad Apps` を組み合わせる。アプリがすべて公開済みであるとは表示しない。
- 個別画像はアプリ名とアイコンを中心に、Featuredのみ現在採用済みのキャッチコピーをそのまま掲載。Otherの長い説明は省略する。
- Noccaの個別画像には「開発中」を表示する。
- 白に近い背景、濃い文字、淡い青のパネルで統一。アイコンは原寸256px以下に縮小し、控えめな角丸を付ける。
- AI生成画像、ダミーUI、新たなコピー、法人格・実績・価格・世界配信等の主張は追加していない。
- 画像内の文章は日本語版を使用する。各ページのHTMLタイトル・description・OGPテキストの翻訳とは別に、画像は共通素材として管理する。

## 再生成

任意の保守用スクリプトは `scripts/generate-og.mjs`。SVGテキストと既存アイコンをsharpで合成し、パレットPNGに圧縮する。ビルド用のnpm依存やpackage-lockには追加しない。

sharpが利用可能なNode.js環境で実行する:

```sh
NODE_PATH=/path/to/existing/node_modules node scripts/generate-og.mjs
```

今回利用した既存のバンドル:

```sh
NODE_PATH=/Users/yuya/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules node scripts/generate-og.mjs
```

フォントはOSにあるHiragino Sansを使用した。スクリプトはNoto Sans CJK JP / Yu Gothic / sans-serifへフォールバックする。フォントファイルをサイトへ配信しない。別OSで再生成する場合は日本語フォントの有無と文字組みを目視確認する。

## 検証

- 9枚の実画像をすべて開き、日本語の文字化け・欠け・重なり、アプリ名、既存コピー、アイコン、Noccaの開発中表示を目視確認した。
- sharpのmetadataで全画像が1200×630pxであることを確認した。
- 全画像が目標150KBを下回ることを確認した。
- 元のアイコンと既存のコピー用JSONは変更していない。
