# KUMAKIKAI Webサイトの保守

Hugo・Hugoplateの既存デザインと公開URLを維持する。ローカル実装、審査提出、App Store一般公開、Web本番反映は別の状態として確認する。

## Productの対応環境・基本情報

すべてのProduct・サイト言語で、次の3項目をこの順序で表示する。

1. 対応端末
2. 対応OS
3. 公開状況

「開発元」は追加しない。基本情報は `layouts/_partials/product-facts.html` で生成し、個別ページへHTMLを記述しない。既存のdefinition list、余白、文字サイズを使う。

| 内容 | 管理場所 | 確認方法 |
| --- | --- | --- |
| 対応端末 | `data/home/<lang>.json` の `apps.<id>.platform` | 最新アプリ本体のRelease `TARGETED_DEVICE_FAMILY`、実装、公開版と照合 |
| 最低対応OS（必須） | `data/product_details/<id>.json` の `minimumOS` | 本体ReleaseのDeployment Targetと、継承するxcconfigを確認。公開済みアプリはApple公開情報とも照合 |
| 公開状況 | `data/apps.json` の `status` | `published` は一般公開確認済み。`development` は未公開。ローカルversionの更新だけで公開中にしない |
| Watch対応 | `data/product_details/<id>.json` の `watch` | Watchアプリ本体の最低OSを `watch.minimumOS` へ。`watch.status: review` は公開済みiPhone版と分ける |
| 補足 | `data/product_details/<id>.json` の `locales.<lang>.notes` | Product固有の重要な利用条件だけを、短い文の配列で記録 |

`minimumOS` は例として `iPadOS 17.0`、`iOS 26.0 / iPadOS 26.0` のようにOS名と確認した最低バージョンを記録する。「以降」は共通翻訳リソースが付けるためデータへ重複記入しない。Watchは `watchOS 9.0` の形式。

最低OSが未確認なら公開前に確認する。空値・任意省略・推測値で新Productを追加しない。`npm run build` 前の `sync-products.py --check` が必須フィールドを検証し、Hugoの共通partialも欠落をエラーにする。CIで他のアプリリポジトリを読めないため、**値の正しさ自体は最新プロジェクトとの照合が必要**。確認したファイル・ターゲット・行番号・公開版の記録を残す。

Project全体の設定とアプリターゲットの上書きを区別する。Unit Test、Widget、FlutterのAppFramework.plistの最低OSをアプリ本体の要件に流用しない。iPhone互換表示やApple Silicon Mac上の互換動作だけを理由に、ネイティブiPad/Mac対応を追加しない。

Apple Watch版が審査中なら、端末・OS欄にも待機表示を付ける。iPhone単体の最低OSとWatchをペアリングできるiOSの条件は同一ではない。互換性のあるペアリング済みiPhoneが必要という補足を残す。App Store公開確認後にだけWatchのstatusをpublishedへ変更する。

現在のProduct statusは `published` / `development`。新しいstatusが必要なら、データだけ追加せず全言語の表示・CTA・SEOと検証を同時に対応させる。未知のstatusを公開中と解釈しない。

## 補足・料金・アプリ内用語

`notes`は共通の箇条書き・Typography・余白で表示する。独自の小リンクやカードでアプリごとに形式を変えない。料金は公開済みアプリだけ、共通の「料金・App内課金の詳細はApp Storeをご確認ください。」へ案内し、変動する価格を固定記載しない。

ユーザー向けの機能名・課金名・設定名は、最新アプリの画面とローカライズリソースを正とする。内部名のquota・credit・entitlement等で独自に言い換えない。

- Uni:Note：日本語は **AI残量**。英語はAI Balance、韓国語はAI 잔액、ドイツ語はKI-Guthaben、フランス語はSolde IA、繁体字はAI 餘額。表示名の変更時は実際のアプリリソースと再照合する。
- オトミル：設定を説明するときは **高齢者向け**。Store素材の訴求表現「シンプルモード」を実際の設定項目名として案内しない。日本語UIだけの場合、翻訳ページでは実際の日本語ラベルと必要な訳を併記する。
- スクリーンショット内の正式なStoreコピーを、Web本文の用語修正だけを理由に加工しない。

## 新しいProductの追加と確認

1. [README](../README.md)の手順で共通Productデータ・6言語本文・実画像・既存Supportリンク・SEO情報を登録する。
2. 対応端末、**必須の最低OS**、公開状況を上記の方法で確認する。公開前機能は区別する。
3. `npm run sync:products` → `npm run build` → `npm run verify` → `npm run verify:seo` を実行する。
4. 全言語の基本情報が3行で順序一致、補足が共通形式、未公開のStore CTAがないことを確認する。
5. Desktop・Mobile・Light/Darkで実際の基本情報を読み、長いOS行の折り返し・横overflow・補足の可読性を確認する。
6. commit/push、Actions・Pages成功後、本番URLを再取得して反映を確認する。

既存のProduct・Guide・FAQ・Privacy・Terms・Press Release URLを移動しない。SEO運用とSearch Consoleは [SEO運用メモ](seo/OPERATIONS.md)、実画面付きGuideはREADMEの該当節を参照する。
