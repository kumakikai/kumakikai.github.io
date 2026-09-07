# Product基本情報の統一

確認日: 2026-09-07。対象は8アプリ × 6言語 = 48 Product詳細。既存のデザイン、アプリ本文URL、公開／開発中の区分を維持した。

## 対応環境と公開状況

アプリ本体のRelease設定と継承先xcconfigを確認した。公開済み7アプリはApple公開lookup APIとも照合した。ローカルの新バージョン番号を一般公開の根拠にしていない。

| Product | 対応端末 | 確認済み最低OS | 公開状況 |
| --- | --- | --- | --- |
| Uni:Note | iPad | iPadOS 17.0以降 | 公開中・App Store |
| オトミル | iPhone / iPad | iOS 26.0以降 / iPadOS 26.0以降 | 公開中・App Store |
| ギガポケ | iPhone | iOS 17.0以降 | 公開中・App Store |
| Nocca | iPhone | iOS 17.0以降 | 開発中 |
| Uni:Note Pocket | iPhone | iOS 17.0以降 | 公開中・App Store |
| ギャンカレ | iPhone | iOS 14.0以降 | 公開中・App Store |
| すわなび | iPhone / Apple Watch（近日対応） | iOS 14.0以降 / watchOS 9.0以降（近日対応） | iPhone版は公開中・App Store。Watch対応版は審査中として区別 |
| SIGNAL | iPhone | iOS 13.0以降 | 公開中・App Store |

対応OSの欠落はNoccaのみで、iOS 17.0を追加した。他7アプリの既存値は本体Release設定と一致。すわなびの既存WatchデータにあったwatchOS 9.0も、共通表のOS欄へ追加した。iOS 14.0はiPhone単体のアプリ最低要件であり、Watchとのペアリングを保証する値ではない。互換性のあるペアリング済みiPhoneが必要という補足を全言語に追加した。

出典: [学習系・Nocca](learning-audit.md)、[オトミル・ギガポケ](caption-codes-audit.md)、[ユーティリティ](utilities-audit.md)、[Apple公開確認](app-store-verification.json)。各監査JSONにファイル・ターゲット・行番号・確認時ハッシュを記録。関連アプリリポジトリは読み取りのみで、既存の作業ツリーを変更していない。

## 共通表示と用語

- `layouts/_partials/product-facts.html` を新設し、全48ページで **対応端末 → 対応OS → 公開状況** の3行だけを同じdefinition listとして出力。「開発元」行と6言語の対応ラベルを削除した。サイトのブランド情報やSEOの人物・ブランド関係は維持。
- Product固有の補足は共通の `ul.product-notes`、料金案内は `p.product-price-note`。既存のTypography・余白を使う。未公開NoccaにApp Store料金案内やダウンロードCTAを追加しない。
- `minimum-os.html` と共通CSSでOS名・バージョンを一組として折り返す。各OSにそれぞれ「以降」を付け、狭い画面でも `watchOS` と `9.0` が分離しないようにした。
- `data/product_details/uni-note.json` の補足を **AIクォータ → AI残量** に修正。アプリ内リソースに合わせて他5言語も AI Balance / AI 잔액 / KI-Guthaben / Solde IA / AI 餘額 に統一。全言語でApple Pencil、インターネット接続とAI残量、AI回答の確認の3項目とした。
- オトミルの設定説明は「シンプルモード」から、現在の設定画面の正式ラベル **「高齢者向け」** へ変更。翻訳ページも日本語UIラベルと短い訳を併記。正式なApp Store画像内のコピーは加工していない。
- 他アプリの基本情報・補足では、今回確認した範囲でquota / credit / entitlement等の内部用語の混入やユーザー向け名称の不一致は見つからなかった。

## 再発防止と運用

`scripts/sync-products.py` が全Productの最低OS・端末・既知の公開statusを必須確認する。OS名を伴わない値や空値はproduction build前に失敗する。Watchがある場合はwatchOSの最低バージョンも必須。Hugo共通partialにも欠落チェックを置いた。実装の正しさは構文検証だけでは保証できないため、最低値そのものは最新アプリプロジェクトと照合する。

[WEBSITE_MAINTENANCE.md](../WEBSITE_MAINTENANCE.md) に3項目の固定順、開発元を追加しないこと、Release設定の調べ方、公開前Watchの扱い、正式なアプリ内用語、補足表示、公開後確認を記載。READMEの「最低OSが不明なら省略する」旧ルールも廃止した。

## 検証

- Hugo Extended 0.158.0 / Node 22.22.0でproduction build成功。build警告なし。
- 全48 Product・144行の順序、値、補足、料金案内、Watch近日表示を検証。[生成HTML検証](regression-tests.json)
- OS欠落、開発元行の復活、行順逆転、WatchOS欠落、6言語の近日表示欠落など17個の負例も検出。入力段階の最低OS欠落・不正値11ケースも拒否。[入力検証](metadata-validation.json)
- 全277 HTML、既存191 URL、10,481内部参照の互換性検証: エラー・警告0。[URL・画像・共通UI検証](migration-verification.json)
- SEO検証: 全277 HTML、検索対象156 URL、全48 Productのメタデータ・schema維持。エラー・警告0。[SEO検証](seo-verification.json)
- Nocca法務ページ保全テスト18件成功。
- Desktop / Mobile / Light / Darkと翻訳を実ブラウザ確認。[47条件の記録](browser/verification.json)、[目視記録](browser/visual-review.md)

## スクリーンショット

- [Uni:Note Desktop](browser/ja-uni-note-1440-light.png) / [Mobile](browser/ja-uni-note-390-light.png)
- [すわなび Desktop](browser/ja-smokeless-1440-light.png) / [Mobile](browser/ja-smokeless-390-light.png)
- [オトミル Desktop](browser/ja-oto-miru-1440-light.png) / [Mobile](browser/ja-oto-miru-390-light.png)

## 本番反映

- 実装commit: `d8a43938c0c154daeb11c55eb5dc9dab8824564c`。
- [production build / 検証 / gh-pages更新](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34093533998): success。
- 公開成果物: `170e4711df32171524eb61dbc092148c482bf0f0`。
- [GitHub Pages公開](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34093578117): success。
- [ローカルとCIのHTML比較](local-ci-comparison.json): 277件すべてbyte一致。
- [CI成果物のProduct基本情報検証](deployed-regression.json): 全48ページ・17負例PASS。
- [CI成果物のSEO検証](deployed-seo.json): エラー・警告0。
- [本番HTTP検証](live-http.json): 277 HTML + 384リソース = **661ファイルがHTTP 200・公開成果物とbyte一致**。全48 Productを含む。追加の18キャッシュ／User-Agent条件も一致。旧テンプレート・旧文言・旧CTAの検出0。
- 既存191 URLとApp Store Connect参照用ページの本文・URLを移動／削除していない。ヘッダー、フッター、画像、sitemap/robots/canonicalも現行成果物を維持。

基本情報の未確認値・未解決UI回帰はなし。Noccaは開発中、すわなびのWatch対応は一般公開前として継続表示する。Actionsには既存checkout/setup-node actionランタイムのNode 20廃止予告注記があるが、今回のHugo生成・サイト検証・Pages公開は成功している。アプリの対応OSを変更する作業ではなく、確認済み要件をWebへ反映する作業として完了。
