# KUMAKIKAI公式サイト

[kumakikai.github.io](https://kumakikai.github.io/) のソースです。Hugo ExtendedとHugoplateを基盤に、iPhone・iPadアプリのProducts、News、Aboutを提供します。Productsは製品情報とアプリ別サポートへ入る共通ハブです。日本語、英語、韓国語、ドイツ語、繁体字中国語、フランス語に対応しています。Aboutの公開URLは既存の`/company/`を維持します。

トップページはUni:Noteを先頭の主力プロダクトとして扱い、ほかのアプリを共通の紹介候補から表示します。全アプリの入口はProductsにまとめ、既存の主要キャッチコピーと実画面を使います。既存の使い方、FAQ、プライバシーポリシー、利用規約、Notesの記事URLを保護することを優先します。

## 必要な環境

| ツール | 使用するバージョン・用途 |
|---|---|
| Hugo Extended | **0.158.0**。`.hugo-version`で固定 |
| Node.js | **22.22.0**。CIは`.node-version`を使用。日本語の単語境界も同じ実行環境で生成 |
| npm | `package-lock.json`から依存をインストール |
| Python | Python 3。ページ同期・移行検証に標準ライブラリのみを使用 |

Hugoは[公式インストール案内](https://gohugo.io/installation/)を参照してください。通常版ではなくExtended版を使用します。Go Modulesは使用せず、必要なHugoplateのruntimeをリポジトリに含めています。

```sh
npm ci
npm run dev
```

開発サーバーは通常 `http://localhost:1313/` で起動します。Hugoのバージョンが一致しない場合、起動・buildスクリプトは理由を表示して終了します。

グローバルに入っているHugoを変更したくない場合は、実行ファイルを指定できます。

```sh
HUGO_BINARY=/path/to/hugo-extended-0.158.0 npm run dev
HUGO_BINARY=/path/to/hugo-extended-0.158.0 npm run build
```

必要な環境ではHugoのキャッシュ先も指定できます。CIでは通常のキャッシュ先でbuildします。

```sh
HUGO_CACHEDIR=/tmp/kumakikai-hugo-cache npm run build
```

## コマンド

| コマンド | 内容 |
|---|---|
| `npm ci` | lockfileと一致する依存をインストール |
| `npm run dev` | theme tokenを生成し、Hugo開発サーバーを起動 |
| `npm run preview` | production build後、完成HTMLを`http://127.0.0.1:1313/`で配信 |
| `npm run theme:generate` | `data/theme.json`からCSS tokenを再生成 |
| `npm run sync:products` | 共通データからProducts等のMarkdown入口を同期 |
| `npm run build` | 同期状態を確認し、Hugo生成と日本語組版を経て`public/`へ出力 |
| `npm run verify` | `public/`の既存URL・記事本文・リンク・メタデータ等を検証 |

通常の確認手順は次のとおりです。

```sh
npm run sync:products
npm run build
npm run verify
```

`npm run build`の`prebuild`は生成ページを勝手に書き換えず、データとのずれを検出します。差がある場合は`npm run sync:products`を実行し、生成されたMarkdownも変更に含めてください。

`npm run dev`は起動時にtheme tokenを生成します。開発中に`data/theme.json`を変更した場合は、別ターミナルで`npm run theme:generate`を実行するか、サーバーを再起動してください。

### 日本語の組版と最終プレビュー

見出し・本文・リストの日本語は、`postbuild`の`scripts/format-japanese.mjs`で文節の区切りに`<wbr>`を挿入します。BudouXの候補を`Intl.Segmenter`の単語境界で絞り、共通`.jp-text`ルールで語中分割を抑えます。`<br>`と異なり、実際に折り返す位置は画面幅に応じてブラウザが決めます。非常に長い語は、はみ出しを防ぐため折り返せます。

この処理はビルド時だけ実行し、文言・リンク・見出しID・構造化データを変えません。ランダム候補の`template`も対象ですが、コードや他言語の本文は対象外です。`scripts/verify-japanese.mjs`でこれらの保持と再実行時の安定性を検証します。依存はdevDependenciesのみで、閲覧者へ解析用JavaScriptを配信しません。

`npm run dev`はHugoの高速な更新確認用で、ビルド後の組版は実行しません。日本語の改行を最終確認するときは`npm run preview`を使用してください。変更後はプレビューを停止して再起動します。CIも必ず`npm run build`を使用し、Hugoコマンドだけで生成したHTMLはデプロイしません。

## 主な構成

| 場所 | 役割 |
|---|---|
| `hugo.toml` | 言語・公開URL・theme・Tailwind buildの設定 |
| `data/apps.json` | アプリID、一覧の表示順、Home掲載候補、開発領域、公開状態、Store URL、既存詳細URL、画像、Supportの本文URL |
| `data/support.json` | 共通問い合わせ先とApple Standard EULAのフォールバックURL |
| `data/home/<lang>.json` | 6言語の既存トップコピー、アプリ名・説明・対応端末・画像alt |
| `data/product_details/<id>.json` | 各Product専用の概要・機能・画像付き紹介・利用シーン・確認済み対応OS |
| `data/product_ui/<lang>.json` | Product詳細の見出し・基本情報ラベル・下部CTAの6言語コピー |
| `data/company/<lang>.json` | 6言語のAbout紹介、公開許可済みFounder、開発領域、For Media、News絞り込みラベル |
| `data/corporate/<lang>.json` | 6言語のナビゲーション、会社紹介、各一覧・CTAのコピー |
| `data/theme.json` | Hugoplateの色・フォント・文字サイズtoken |
| `data/hero.json` | 実UIを使ったHero画像の寸法、responsive画像、alt |
| `data/news.json` | 既存Notes記事のカテゴリ・関連プロダクトを補うメタデータ |
| `content/products/` | 各ProductとProducts一覧の生成Markdown |
| `content/support/`、`content/news/`、`content/company/` | 主要セクションと旧Support互換ページの生成入口、追加する編集記事 |
| `content/htu/`、`content/faq/`、`content/privacy/`、`content/terms/` | 既存サポート本文。URLを維持 |
| `content/notes/` | 公開済みNotes／Press Release。URLを維持 |
| `layouts/` | KUMAKIKAIの共通shell、トップ、記事、Product、一覧レイアウト |
| `layouts/_partials/` | header、footer、SEO、アプリ紹介、画像、CTA等 |
| `assets/css/main.css`、`assets/css/site.css` | Hugoplateの基礎CSS読み込みとKUMAKIKAIの上書き |
| `assets/js/site.js` | ナビゲーション、ダークモード、言語メニューの最小処理 |
| `static/images/apps/`、`static/images/hero/`、`static/images/og/` | Web配信用の実画像・OGP |
| `themes/hugoplate/` | commitを固定した公式Hugoplateの必要runtimeとMITライセンス |
| `docs/migration/` | URL・本文baseline、素材出典、公開地域調査、移行検証記録 |

`public/`、`resources/`、`node_modules/`、`hugo_stats.json`、`assets/css/generated-theme.css`は生成物です。コミット対象に含めません。

## アプリを追加・更新する

1. `data/apps.json`にアプリを追加します。`id`はURLに使用する固定slug、配列順はProducts一覧の表示順です。`featured: true`はHomeの紹介候補を意味し、常時表示や公開済みという意味ではありません。現在の全8アプリを候補に含め、Uni:Noteの先頭固定はレイアウト側で扱います。`area`には下表の開発領域を設定します。
2. `data/home/`の6言語すべてへ、同じIDでアプリ名・短い説明・`platform`・必要な`taglineLines`・`imageAlts`を追加します。既存コピーの変更には仕様上の根拠が必要です。`taglineLines`がないアプリは、`data/product_details/<id>.json`の各言語の既存`overviewTitle`を共通紹介の見出しとして参照します。同じコピーを重複定義する必要はありません。Uni:Noteの対応端末表記は全言語で`iPad`に統一します。
3. 実際のアイコン・スクリーンショットを`static/images/apps/<id>/`へ配置し、`data/apps.json`に幅・高さとsmall／large画像を登録します。素材がない場合は`screenshots: []`にします。
4. 使い方、FAQ、Privacy、Termsがある場合は既存の規則で`content/<section>/<id>.md`を用意し、`data/apps.json`の`support`に`guideURL`・`faqURL`・`privacyURL`・必要なら`termsURL`を設定します。既存ページは現在のURLをそのまま指定します。問い合わせ先が共通と異なる場合だけ`contactURL`を設定してください。翻訳がなければ日本語ページへ案内します。
5. `data/product_details/<id>.json`へ、Homeとは別の製品紹介を6言語で追加します。公開版とローカル開発版を区別して確認し、根拠と素材の出典を`docs/products/`へ残します。下の「Product詳細の編集」を参照してください。
6. `npm run sync:products`、`npm run build`、`npm run verify`を実行し、差分とブラウザ表示を確認します。

現在は8アプリ×6言語の48 Productページと、主要3セクション＋Support互換ページ×6言語の24入口、計72 Markdownを`scripts/sync-products.py`で同期します。生成ページにはマーカーがあり、直接編集せず共通JSONを変更します。手書きの記事は同期スクリプトの上書き対象になりません。

| `area` | 領域 | 現在のアプリ |
|---|---|---|
| `learning` | 学習 | `uni-note`、`uni-note-pocket` |
| `communication` | コミュニケーション | `oto-miru`、`nocca` |
| `utilities` | ユーティリティ | `giga-poke`、`balance-calendar`、`smokeless`、`signal` |

開発領域は個別機能ではなく大分類です。Aboutでは各`area`の候補から代表アプリを1件選びます。新規アプリも上記の分類へ追加し、他領域から候補を補充しません。

HomeとProduct詳細は同じ実画面データを使用します。旧Other Appsとして追加した素材の出典は[既存の素材記録](docs/homepage/other-app-assets.md)に残しています。Homeへ掲載しない候補もProductsから閲覧できます。

アプリをデータから取り除く場合、生成ページを自動削除することはありません。旧URLからの到達方法を決めてから対応してください。ID変更もURL変更になるため、表示名の変更だけを目的にIDを変えないでください。

### Product詳細の編集

Homeは短い紹介、Product詳細は具体的な用途と条件、Supportは操作方法・FAQを担当します。詳細本文を増やすために`data/home/`の既存コピーやサポート本文を変更する必要はありません。

`data/product_details/<id>.json`の`locales`に`ja`・`en`・`ko`・`de`・`fr`・`zh-hant`を用意します。各言語には`overviewTitle`、`overview`（2段落）、`features`（アプリに合う3〜6項目のtitle／description）、`stories`（画像と説明を組み合わせた2〜3項目）、`audienceTitle`、`audience`（3項目のtitle／description）、`notes`（利用条件）を設定します。項目数をそろえる目的で機能を作らないでください。

`stories`は`image: 0`のように`data/apps.json`の既存画像を参照できます。詳細だけに使う実素材は同じファイルの`media`にsmall／large／width／height／largeWidthを登録し、storyから`media: "pdf"`等のキーと、その言語の`alt`で参照します。新しい画像をHomeへ追加する必要はありません。画像は縦横比を維持したWebPを2サイズ用意し、原本・SHA256・採用根拠を記録します。

`minimumOS`はApp Store公開情報とプロジェクトのdeployment targetを照合してから記入します。不明な場合は省略します。開発中アプリの最低OSや価格を推測して埋めないでください。料金の固定値は避け、公開中アプリだけApp Storeの最新情報へ案内します。

Product詳細の公式バッジはHeroと主要説明後の2箇所です。国旗はHeroだけ、Supportは最下部の直接リンクを維持します。Homeのバッジは各アプリ1箇所のままです。[詳細ページ拡張の記録](docs/products/REPORT.md)に、採用した内容・素材・検証結果をまとめています。

### すわなびのApple Watch対応版

`data/product_details/smokeless.json`の`watch.status`は現在`review`です。公開済みのiPhone版と区別し、Home・Products・Product・Aboutの対応端末には「Apple Watch（近日対応）」、Productと使い方には審査中の説明を表示します。既存のiPhone版App Store導線は維持します。

**1.2.0の一般公開をApp Storeで確認した後**にだけ`watch.status`を`published`へ変更してください。共通partialによって待機表記・Hero・機能説明・使い方の状態がまとめて変わります。アプリ本体の`data/apps.json.status`、配信地域、審査提出と一般公開は別の状態です。公開前は構造化データの対応OSへwatchOSを追加しません。

Watch文言は6言語、実操作の使い方は既存の5言語ページ末尾にshortcodeで追加しています。ドイツ語の使い方本文は元からないため、既存の日本語フォールバックを維持します。使い方URLやポリシーURLは移動しません。

素材は`assets/images/apps/smokeless/watch/`の実画面と正式な提出用画像を使い、Hugoで原寸／半幅のWebPを生成します。日本語・韓国語・繁体字・フランス語は各言語の提出用画像、英語・ドイツ語は数字のみの実画面です。出典・SHA・仕様・公開版の確認記録は[Watch対応と組版監査](docs/watch-typography/REPORT.md)を参照してください。

### 公開状態とApp Store

- 公開済みは`status: "published"`、開発中は`status: "development"`です。
- 開発中アプリにはApp Store URLを設定しません。Download／Store CTAも表示しません。
- `availability.verifiedStorefronts`には実際に確認できた地域だけを記録します。`coverage: "partial"`は全世界の提供状況を確認済みという意味ではありません。
- 現在のCTAは確認済みの**日本のApp Store**を指します。サイトの表示言語を変更しても、未確認の地域URLを自動生成しません。
- Primary CTAにはApple公式の黒背景SVGを使用します。`data/app-store-badges.json`に6言語の配布元・寸法・SHA256、`static/images/badges/`に無改変の原本があります。表示言語はバッジの言語だけに対応し、リンク先の地域は変更しません。
- 国旗リンクは`availability.storefrontURLs`に保存したApple Lookup返却URLを使います。国コードを差し替えてURLを生成せず、提供とリンク先を確認した地域だけ登録してください。原本と確認済みURLは`npm run verify`でも照合します。
- `screenshotsStatus: "review"`は審査提出版の画像を表示する場合に設定します。公開中アプリの`status`と区別し、公開されていない機能を公開版の事実と混同しません。
- `checkedAt`と確認根拠を更新し、[提供地域の調査記録](docs/migration/availability.md)も参照します。

## News／Press Releaseを追加する

新規記事は`content/news/YYYY-MM-DD-slug.md`にMarkdownを追加します。HTMLやトップレイアウトの編集は不要です。

```yaml
---
title: "記事タイトル"
description: "記事の内容を短く説明します。"
date: 2026-09-07T10:00:00+09:00
news_category: "information"
related_products: ["uni-note"]
draft: true
---
```

カテゴリは正式なアプリ紹介・発表の`press-release`、開発・運営の読み物の`blog`、利用者へのサービス告知の`information`を使います。画面の表記は全言語でPress Release／Blog／Informationに統一します。該当する告知がなければInformationは0件で構いません。発表記事のタイトルは「正式アプリ名＋について」とし、既存URLを維持します。関連プロダクトがなければ`related_products`は省略できます。本文を記入し、公開時は`draft: false`に変更します。Hugoは通常、未来の日付の記事を公開対象に含めません。

必要に応じて`lastmod`に実際の更新日時を設定できます。記事ごとのOGPには次のように`static/`以下の画像を指定します。未指定時は関連プロダクトのOGP、または共通OGPを使います。

```yaml
images: ["/images/og/uni-note.png"]
```

翻訳を追加する場合は同じbasenameで`.en.md`、`.ko.md`、`.de.md`、`.zh-hant.md`、`.fr.md`を作成します。現在日本語だけの記事は、他言語のNewsにも日本語の記事として案内しています。

既存の`content/notes/`記事をNewsへ表示するために移動する必要はありません。`/notes/.../`を維持したままNews一覧へ集約します。旧記事のカテゴリ・関連アプリは`data/news.json`、新記事はfront matterで管理できます。

Newsの`#press-release`・`#blog`・`#information`は同じ一覧のカテゴリー絞り込みです。`#all-news`で全記事へ戻ります。CSSの`:target`／`:has()`で動作し、JavaScriptや重複したカテゴリー一覧ページは追加しません。Aboutの取材・開発記事リンクもこの直接URLを使います。記事がないカテゴリーには件数を埋めるための記事を作らず、空の状態を表示します。

## About・公開プロフィールを編集する

`data/company/`の6言語を編集します。画面の名称はAbout、データの場所と公開URLは`company`のまま維持します。氏名は`founderName: "Yuya Nakamura"`に統一し、英字氏名の別フィールドや漢字氏名を重複表示しません。画像altも同じ氏名を使います。肩書き・経歴は、本人が公開を許可した事実または確認できる既存公開情報に限定してください。出典と非掲載判断は[Company拡張レポート](docs/company/REPORT.md)と[根拠](docs/company/evidence.json)に記録しています。名刺の電話番号と名刺全体はWebへ掲載しません。本人が利用を許可した人物イラストの編集方法・出典は[人物画像の記録](docs/company/portrait/asset.json)を参照してください。

Aboutの紹介文には固定の件数や`%d`による数値の差し込みを使いません。`areas`の各行には`area`を設定し、同じ領域の`data/apps.json`から紹介候補を参照します。既存の`product`はJavaScript無効時の表示用IDとして残し、該当する領域内のアプリを指定します。アイコン・名称・端末・URLはProductデータを共用します。`featured`や`area`を変更しても、`status`・Store URL・提供地域の根拠は変更しません。実績のために未確認のDL数、勤務先・経験年数・学歴、法人格・所在地等を追加しないでください。主要CTAは末尾の既存メール窓口です。For Mediaから同じページの`#contact`へ直接移動できます。

Aboutの基本情報は名称・開発者・事業内容だけとし、Webやメールを重ねて載せません。問い合わせ先はContactのメールCTAへ集約します。抽象的な開発理念の3項目は使わず、Founderで出典のある開発背景を短く紹介します。日本語コピーと改行の監査記録は[コピー監査レポート](docs/copy-audit/REPORT.md)を参照してください。日本語の改行は`assets/css/site.css`で禁則処理、見出しの均等な折り返し、幅・余白を調整し、対応ブラウザでは`auto-phrase`を補助的に使用します。文章へ改行タグを足して表示幅を固定しないでください。

AboutのSEO説明は`data/corporate/<lang>.json`の`companyDescription`で管理し、画面名は`nav.company: "About"`とします。変更時は`npm run sync:products`を実行します。同期スクリプトはこのナビゲーション名をページtitleにも使いますが、`/company/`と各言語の既存URLは変更しません。Aboutだけに公開許可済みFounderのPerson情報をOrganization schemaへ補足しています。

日本語の長いNewsタイトルで語中改行が起きる場合は、`data/heading_phrases.json`に元タイトルと意味のまとまりを登録できます。共通partialがNews一覧と記事見出し（本文内の見出しを含む）に同じまとまりを使い、画面幅に応じて折り返します。改行位置を固定する指定ではありません。各部分の連結は元のタイトルと必ず一致させ、1部分を長くしすぎないでください。記事本文・URL・SEOのタイトルは変わりません。

## URL・コンテンツの互換性

既存の`/htu/`、`/faq/`、`/privacy/`、`/terms/`、`/notes/`と各言語URLはApp Store Connectや外部記事から参照されている可能性があります。ファイル名・slugを変更する場合は、旧URLを維持するかHugoの`aliases`で到達可能にしてください。各アプリのPrivacy／Termsは統合しません。

Product下部の`#support`は使い方・FAQ・問い合わせ・Privacy・Termsの5項目へ直接案内します。ProductからSupport一覧へ移動して同じアプリを再選択させないでください。HeaderはProducts／News／About、FooterはContactだけを担当します。アプリ選択はProductsに一本化し、各カードの「製品を見る」は`/products/<id>/`、「サポート」は同じProductページの`#support`へ直接進めます。アプリ名・端末・既存のキャッチコピーまたは説明・公開状況は共通データから表示し、一覧には使い方やFAQを展開しません。

Product・使い方・FAQは`support-data.html`で同じSupportデータを解決し、`support-links.html`で同じ行UIを表示します。使い方・FAQでは閲覧中の項目を省きます。`termsURL`が未設定の場合だけ、`data/support.json`のApple Standard EULAへ案内します。独自規約のURLが設定されているのにページがない場合はbuildエラーにし、別の規約へ黙って切り替えません。外部リンクも同じタブで開き、EULAは外部矢印・title・読み上げ用補足で行き先を示します。Press ReleaseはNewsから案内し、ProductやSupportの末尾に重ねて載せません。

この構成の監査記録は[Support統一レポート](docs/support-consistency/REPORT.md)を参照してください。`npm run verify`は5項目の順序・文言・URL・EULA・閲覧中ページの除外も検証します。実ブラウザではローカルpreviewを起動し、`TEST_BASE_URL=http://127.0.0.1:1313 NODE_PATH=/path/to/qa/node_modules node scripts/verify-support.cjs`で全Product・使い方・FAQを確認できます。

旧`/support/`、`/htu/`、`/faq/`、`/privacy/`、`/terms/`の集約URLは互換用にHTTP成功・自己canonicalを維持し、`noindex, follow`とProductsへの簡潔な案内を付けます。これらは主要ナビやHomeから案内しません。旧Supportの`#<id>`・`#support-<id>`はCSSの`:target`で対象アプリの直接Supportリンクだけを表示し、`#contact`も維持します。個別本文・Privacy・利用規約URLは変更しません。Homeの旧`#support`はHeroのProducts CTAへ接続します。

Productsへのハブ統合は[統合レポート](docs/hub/REPORT.md)、以前の素材・CTA・News・Privacy・Footer整理は[UX修正レポート](docs/ux/REPORT.md)を参照してください。

`docs/migration/baseline.json`は移行前の191 HTML URL、記事本文・アンカー等を保存した検証基準です。`npm run verify`で既存コンテンツ、新しいProduct／主要一覧、内部参照、Store CTA、SEO・OGP、sitemap・robotsを検査します。

baselineは意図しないURL削除や本文変更を検出するためのものです。チェックを通す目的で作り直さず、意図した使い方・FAQの改訂は、下記の個別レビュー記録で扱い、元のbaseline自体は変更しません。外部App Storeの最新提供状態、端末実機、ブラウザの見た目をこの静的検査だけで証明することはできません。

## デザイン・画像・themeの保守

HugoplateのTailwind CSS v4、base typography、content typography、container／section、button primitivesを利用します。`templates.Defer`でHTML生成後にCSSを処理し、fingerprint付きCSSを配信します。KUMAKIKAIの変更はrootの`layouts/`・`assets/`・`data/`に置き、vendor内部へ直接加えません。

採用元は[Hugoplate公式commit `2f5a454ee708f5f2666414af9ef48df65570752a`](https://github.com/zeon-studio/hugoplate/tree/2f5a454ee708f5f2666414af9ef48df65570752a)、package 3.5.1です。`themes/hugoplate/UPSTREAM.json`に採用ファイルとSHA-256、同ディレクトリにMIT LICENSEを保存しています。デモ記事、イラスト、testimonial、slider、不要なGo Modulesは含めません。

上流更新時は固定commitとの差分を調べ、採用しているruntimeだけを更新し、SHA・出典・必要バージョンを更新します。公式starterの`project-setup`／`update-theme`をこのサイトでそのまま実行すると既存構成と衝突するため、使用しません。更新後はbuild、移行検証、主要画面のresponsive／Light／Dark／キーボード操作を確認します。

build依存はTailwind、Tailwind CLI、Typographyと、日本語組版用のBudouX・parse5です。追加のWeb Font、SPA、animation frameworkは使用していません。色・フォントは`data/theme.json`と`assets/css/site.css`の既存変数を確認して変更します。

Tailwindの自動ファイル探索は`source(none)`で無効化し、Hugoが実際に出力した`hugo_stats.json`だけを明示的に読み込みます。README・検証JSON・vendorデモ等の単語がCSS候補へ混ざり、ローカルとCIのfingerprintが変わることを防ぎます。JavaScriptで追加するクラスは現在`js`・`dark`・`menu-open`で、`site.css`に明示的な定義があります。

画像にはWebPのresponsive variantsと実寸を設定し、Hero以外は原則lazy loadingにします。実在しないUIや未公開機能を画像で補いません。HeroとOGPの出典・加工内容は[Hero素材記録](docs/migration/hero-assets.md)、[OGP素材記録](docs/migration/og-assets.md)を参照してください。OGPのPNGはコミット済みで、通常のbuild時には再生成しません。既存のsharp環境を使い、`node scripts/generate-og.mjs uni-note`で指定Productだけ再生成できます。引数なしなら共通画像と全Productを生成します。

## GitHub Pagesへのデプロイ

`.github/workflows/deploy.yaml`は`main`へのpush、または手動実行で起動します。

1. Hugo 0.158.0 ExtendedとNode 22を準備。
2. npm cacheを利用し、`npm ci`でlockfile通りにインストール。
3. `npm run build`でproduction出力を作成。
4. rootの`app-ads.txt`があれば`public/app-ads.txt`へコピー。
5. 移行・リンク・SEO検証に成功した場合だけ`public/`を`gh-pages`へ公開。

GitHub Pagesは既存の`gh-pages`公開方式を維持します。生成物を手動で`main`に追加する必要はありません。公開完了はActionsの成功だけでなく、`gh-pages`の生成物と[公開サイト](https://kumakikai.github.io/)への反映を確認してください。ローカルbuild成功は公開反映の証明ではありません。

## ブラウザ・公開後の確認

ブラウザ検証は任意のQA環境に用意したPlaywrightとaxe-coreを使います。通常のbuild依存へは追加しません。production出力をローカルHTTPサーバーで表示したうえで実行します。

```sh
NODE_PATH=/path/to/qa/node_modules node scripts/verify-browser.cjs
```

Aboutの公開プロフィール、取材導線、News絞り込みを確認する場合は、同じQA依存で`node scripts/verify-company.cjs`を実行します。結果の保存先は`TEST_REPORT`、画像の保存先は`TEST_OUTPUT`で指定できます。過去の`docs/company/`配下の検証記録は当時の画面の証拠として残し、新しい表示条件の結果で上書きしません。

既定の表示先は`http://127.0.0.1:1314`、Chromeの場所は`CHROME_PATH`、表示先は`TEST_BASE_URL`で変更できます。結果は`artifacts/migration/browser/`へ保存します。

App Store Connect関連の既存ページは同じURLの正式ページとして保持します。対応一覧・既存aliasと正規ページの区別は[恒久URL一覧](docs/migration/permanent-urls.md)を参照してください。公開済みの正規ページをredirectへ置換したりcanonicalを変えたりすると移行検証が失敗します。

GitHub Pagesへのデプロイ完了後、同じcommitのproduction buildと全HTMLのHTTP応答を照合できます。過去のbuildを使って実行しないでください。

```sh
python3 scripts/verify-live.py --build public
```

macOSのPython環境でCA証明書が見つからない場合は、OSのCAファイルを指定できます。HTTPSの証明書検証は無効化しないでください。

```sh
SSL_CERT_FILE=/etc/ssl/cert.pem python3 scripts/verify-live.py --build public
```

この確認はHTTP GETのみで、App Store Connectの登録内容を変更しません。詳しい移行・画面検証は[移行報告](docs/migration/REPORT.md)を参照してください。

Home／Aboutのランダム選出は、同じQA依存で`node scripts/verify-selection.cjs`を実行します。既存URL・コピー保護は`npm run verify`を併用してください。選出の重複・カテゴリ・Uni:Note固定、再読み込み、JavaScript無効時、多言語・画面幅・配色、CLSの結果とスクリーンショットを`docs/selection/`へ保存します。

## 大きなブラウザ検証記録

全条件のDOM行情報を残す監査では、完了後に`python3 scripts/archive-verification.py docs/watch-typography`を実行すると、128KB以上の結果を要約JSONと無損失の`.json.gz`原本に分けられます。実行中のレポートには使用しません。原本は`gzip -dc path/to/report.json.gz`で読み出せます。サイトのbuild・配信はこれらの記録に依存しません。

## 実画面付きの使い方ガイド

`content/htu/<app>[.<lang>].md` が操作説明、`content/faq/` が問題・例外の説明です。操作手順をFAQへ重複掲載せず、該当する使い方の見出しへ直接リンクします。既存URLは維持し、見出し名を変える場合も従来のアンカーを対応する新しい説明の近くに `{{< guide-anchor "旧ID" >}}` で残してください。raw HTMLを許可する設定変更は不要です。

現在の実装・実UIと照合した画像を `assets/images/guides/<app>/` に保存します。操作対象のcropを優先し、全画面が必要な場合だけ `screen`（iPhone）または `tablet` を指定します。画像内のボタン・文言を描き換えません。

```go-html-template
{{< guide-image src="images/guides/example/add-item.png"
    alt="記録画面右上の追加ボタン" mode="crop" >}}
```

共通shortcodeがWebPと1x/2xの`srcset`、サイズ予約、遅延読込、拡大リンクを生成します。配信画像は原寸より拡大しません。表示の最大幅はcrop 560px、iPhone全画面320px、iPad 760pxです。日本語組版・目次・更新日も共通テンプレートに従います。更新したMarkdownに実際の日付の`lastmod`を設定してください。

画像の取得元・元ファイルのhash・crop範囲・照合した実装と公開バージョンは `docs/visual-guides/` に記録します。審査提出中の画面は公開済みと断定せず、対象バージョンを明示してください。Simulatorで取得する場合はデモデータを使い、自分が起動した端末だけを終了します。

今回の使い方・FAQ本文の更新は、変更前の `docs/migration/baseline.json` を書き換えず、`docs/visual-guides/reviewed-content.json` に個別に記録しています。以後も既存ガイドを改訂する場合は、実装と画面を確認して監査記録を更新し、production build後に `python3 scripts/record-guide-review.py` を実行して差分を確認します。その後 `npm run verify` を実行します。これは使い方・FAQ本文だけに限定した仕組みで、Privacy・Terms・News本文、正式URL、canonical、既存アンカーの保護は継続します。

画像の読込・幅・アクセシビリティ・目次・拡大リンクは、QA用のPlaywright／axe-coreで `node scripts/verify-guides.cjs` を実行して確認できます。`TEST_ENGINE=webkit` でWebKit、`TEST_WIDTHS=375,390,1440` と `TEST_LOCALES=ja` で対象を絞れます。結果は `docs/visual-guides/` に保存します。機械チェックに加えて、画面内の文字と操作対象が読めるかを実際のスクリーンショットで確認してください。
