# 最終リリース監査（2026-09-07）

## 対象と結論

監査開始時のsourceは `2b4ff1cbb1d2c3996ca2e1f88c615884edf15357`、公開artifactは `2e860118451ce5f2c77359ab06dc6d4393bd2104`。
本番の全277 HTML URL（通常ページ210、互換redirect 67）と公開asset 384件、計661件をGETし、すべてHTTP 200かつ公開gh-pages artifactとバイト単位で一致した。全URLは [http-before.json](http-before.json) に記録。

通常ページ210件のHeaderは **Products / News / About**、Footerのナビゲーションは **Contact** のみ。旧PaperModや移行初期Productテンプレートの混在はなかった。互換redirectは本文のない最小限のHTMLとして別集計し、旧テーマとは判定していない。現行記事本文にも残る `post-content` クラス単独は旧テーマの証拠にしない。

## 変更した項目

1. **Newsのempty state**：初期HTMLへnative `hidden` を付け、実際に0件のカテゴリを選んだときだけ既存CSSのカテゴリ条件で表示する。Tailwindのhidden resetと同じ `@layer base` 内で限定的に上書きした。新しいJavaScriptやUIは追加していない。
   - 修正前も通常ブラウザでは初期15件・empty非表示だったが、CSS取得遮断時に初期一覧とemptyが同時表示されることを再現した。CSSだけに非表示を依存していたことが原因。
   - CSSを評価しない抽出ツールがHTML内の非表示文を拾う場合と、画面上の誤表示は区別する。native `hidden` を無視する任意の外部抽出器の出力までは保証しない。
2. **Aboutの日本語meta description**：削除済みFounderエピソードを示唆する「Uni:Noteなどの開発背景、」だけを共通データから削除し、生成front matterへ同期した。Founder本文は公開前から最新の開発スタンス文であり、再創作していない。

その他のデザイン、機能、本文、URL、Support/Privacy導線は変更していない。

## 旧Product表示の原因切り分け

報告された旧表示は、gh-pagesの履歴 `8e0500e1f14821aed26033b7adda7582faf72c29`（2026-09-07 00:22:37 JST）の `/products/uni-note/` と一致する。`iPad専用`、`日本のApp Storeで提供中`、文字ボタン `App Storeで見る`、上部Support CTA、Header Support/Company、6項目Footerを同時に含む。これは**Hugoplate移行初期に実際に配信した旧版**であり、現在のサイト内に残ったPaperModページではない。全16履歴の比較は [product-history.json](product-history.json)。

現行の同URLでは、通常GET・再検証指定・一意query・`index.html`明示・Mobile UA・Googlebot UAの全6条件で同じ現行HTMLを取得した。About/Newsを含む18条件すべてが公開artifactと一致。CDN HITだけでなくMISS応答も一致し、`Vary`は `Accept-Encoding`、`Cache-Control`は `max-age=600`。GitHub Pagesの公開元も `gh-pages` branchで正常だった。

したがって、現在の公開元・CDN条件・ローカル生成物による新旧出し分けは再現していない。**過去の取得結果や外部抽出側のキャッシュという可能性はあるが、報告元のツール名・取得日時・元レスポンスが未提供のため、具体的なキャッシュ層までは断定できない。** 本番に存在しない旧ページを修正したとは報告しない。

`public/`はGit管理対象外で、buildは `--cleanDestinationDir`、deployは `keep_files`なし。監査開始前のローカルpublicとgh-pagesは全HTMLが一致し、古いHTMLがローカルに残っている事実もなかった。

## 全Product詳細

以下8アプリ × 6言語（ja / en / de / fr / ko / zh-hant）、全48ページが `layouts/product/single.html` と共通base/header/footerを使用。1440px・390pxで全48ページを本番ブラウザ確認し、現行データ、公式App Storeバッジ、配信地域、下部Support 5項目、旧上部Support CTAの不在を確認した。開発中NoccaのStoreバッジ非表示も維持。

| Product | 日本語正式URL | 6言語の共通テンプレート・現行UI |
|---|---|---|
| Uni:Note | `/products/uni-note/` | PASS（端末表記iPad） |
| オトミル | `/products/oto-miru/` | PASS |
| ギガポケ | `/products/giga-poke/` | PASS |
| Nocca | `/products/nocca/` | PASS（開発中） |
| Uni:Note Pocket | `/products/uni-note-pocket/` | PASS |
| ギャンカレ | `/products/balance-calendar/` | PASS |
| すわなび | `/products/smokeless/` | PASS（Watchの審査状態を維持） |
| SIGNAL | `/products/signal/` | PASS |

全通常ページDesktop + Product48/About6のMobile = **264ブラウザケースPASS**。1,322回の画像decode確認でbroken imageなし、HTTP/JS error・横overflowなし。[browser-before.json](browser-before.json)、[source-audit.md](source-audit.md) に詳細。

## Founder・Support・既存URL

6言語のFounder本文は共通データの現行文と一致し、Uni:Note/すわなびの旧エピソードなし。日本語本文は、組み込み・業務・モバイル開発経験に続け、「作るものの分野は特に決めていません。自分が使っていて不便に感じたことや、身近な人から聞いた困りごとをきっかけに、必要だと思ったものをアプリにしています。」という決定済みの開発スタンス。氏名はYuya Nakamuraのみ。

Home/Product/Guide/FAQ/Header/Footerから不要なSupport・Privacy総合ハブへ戻す導線なし。互換入口はnoindexで残し、アプリ固有Support/Privacy/Terms、Press Releaseを維持する。今回のURL削除・移動・aliases追加は0件。

## buildと検証

- Hugo Extended 0.158.0 / Node 22.22.0のproduction build成功。
- Nocca法務・審査回帰テスト18件PASS。
- migration検証：277 HTML、旧191ルート、138恒久本文URL、53旧alias、10,507内部参照、Support Product48/Guide22/FAQ22、警告0・エラー0。
- News：Chrome24 + WebKit24 = 48ケースPASS。6言語、1440/390px、JS on/off、初期一覧、各カテゴリ、All復帰、emptyカテゴリへの直接fragment、アクセシビリティ可視性、CSS遮断時の初期非表示を確認。

## 画像生成の差異

HTMLとは別に、ローカルMacとCI artifactで1つの操作説明WebPに8 byteのサイズ差があった（560×150、同一source）。空のHugo cacheで再生成してもローカル版と完全一致し、古いcacheの再利用ではなかった。比較画像の差は84,000 pixel中424 pixel、最大channel差10/255、平均絶対差約0.009/255。プラットフォーム間のWebP生成差と考えられ、旧UI素材や旧テンプレートの残存ではない。画像パイプラインは変更せず、公開assetのHTTP比較にはCIから発行されたgh-pagesを正としている。[webp-comparison.json](webp-comparison.json)

## 公開後の証跡

- 修正source：`0a957df2b2e3281922aea524f76cee7977a6b78c`。
- 公開gh-pages：`dac80f68e1052e4e7053b6263176889372640c22`。
- [production build / deploy 34088380110](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34088380110) **success**。
- [Pages deployment 34088417580](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34088417580) **success**。
- 公開後の全277 HTML + 384 asset = **661/661 HTTP 200、全件最新gh-pagesと完全一致**。追加18 cache条件も一致し、旧Header/Footer・旧文言の検出0件。[http-after.json](http-after.json)
- ローカルproduction buildと本番全277 HTMLも完全一致。[html-after.json](html-after.json)、[after-artifact-comparison.json](after-artifact-comparison.json)
- 全48 Productの現行本文・共通構造は公開後HTTP照合でも維持。Home・Uni:Note・AboutのDesktop、Uni:Note・AboutのMobileを公開後に再表示し5ケースPASS。Founderの最新本文・公式バッジ・地域・下部Support・Mobileメニュー・画像decodeも正常。[browser-after.json](browser-after.json)
- 公開後News：**Chrome24 / WebKit24、計48ケースPASS**。全6言語で初期15記事・emptyなし、Information0件のみempty表示、All復帰、CSS遮断、JS on/off、アクセシビリティ可視性を再確認。[news-live-chrome.json](news-live-chrome.json)、[news-live-webkit.json](news-live-webkit.json)
- サイトbuild・URL検証の警告/エラーは0件。Actions基盤では既存 `checkout@v4` / `setup-node@v4` のNode20非推奨通知と `url.parse()` 非推奨警告が出るが、全ジョブは成功。今回の限定修正ではworkflow依存を更新していない。

公開後の代表画面：

- [Uni:Note Desktop](screenshots/browser-after-uni-note-1440.jpg) / [Mobile](screenshots/browser-after-uni-note-390.jpg)
- [Founder Desktop](screenshots/browser-after-founder-1440.jpg) / [Mobile](screenshots/browser-after-founder-390.jpg)
- [News 全件 Desktop](screenshots/news-live-chrome-1440-all.jpg) / [Mobile](screenshots/news-live-chrome-390-all.jpg)
- [Information 空カテゴリ Mobile](screenshots/news-live-chrome-390-information.jpg)
- [Footer Desktop](screenshots/browser-after-footer-1440.jpg)

HTTP確認時刻は各JSONにUTCで記録。公開後再取得は2026-09-07 14:53–14:54 JSTに実施。元の外部取得ツール・日時は引き続き未確認であり、そのキャッシュ内部を確認したとは扱わない。
