# KUMAKIKAI公式サイト

[kumakikai.github.io](https://kumakikai.github.io/) のソースです。Hugo ExtendedとHugoplateを基盤に、iPhone・iPadアプリのProducts、News、Companyを提供します。Productsは製品情報とアプリ別サポートへ入る共通ハブです。日本語、英語、韓国語、ドイツ語、繁体字中国語、フランス語に対応しています。

トップページのFeatured／Other分類、Featuredの順序、主要キャッチコピーを維持しながら、サイト全体を共通のレイアウト・CSSへ統一しています。既存の使い方、FAQ、プライバシーポリシー、利用規約、Notesの記事URLを保護することを優先します。

## 必要な環境

| ツール | 使用するバージョン・用途 |
|---|---|
| Hugo Extended | **0.158.0**。`.hugo-version`で固定 |
| Node.js | **22**。CIは`.node-version`を使用 |
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
| `npm run preview` | production設定・minify付きでプレビュー |
| `npm run theme:generate` | `data/theme.json`からCSS tokenを再生成 |
| `npm run sync:products` | 共通データからProducts等のMarkdown入口を同期 |
| `npm run build` | 生成ページの同期状態を確認し、production buildを`public/`へ出力 |
| `npm run verify` | `public/`の既存URL・記事本文・リンク・メタデータ等を検証 |

通常の確認手順は次のとおりです。

```sh
npm run sync:products
npm run build
npm run verify
```

`npm run build`の`prebuild`は生成ページを勝手に書き換えず、データとのずれを検出します。差がある場合は`npm run sync:products`を実行し、生成されたMarkdownも変更に含めてください。

`npm run dev`は起動時にtheme tokenを生成します。開発中に`data/theme.json`を変更した場合は、別ターミナルで`npm run theme:generate`を実行するか、サーバーを再起動してください。

## 主な構成

| 場所 | 役割 |
|---|---|
| `hugo.toml` | 言語・公開URL・theme・Tailwind buildの設定 |
| `data/apps.json` | アプリID、表示順、Featured、公開状態、Store URL、既存詳細URL、画像 |
| `data/home/<lang>.json` | 6言語の既存トップコピー、アプリ名・説明・対応端末・画像alt |
| `data/product_details/<id>.json` | 各Product専用の概要・機能・画像付き紹介・利用シーン・確認済み対応OS |
| `data/product_ui/<lang>.json` | Product詳細の見出し・基本情報ラベル・下部CTAの6言語コピー |
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

1. `data/apps.json`にアプリを追加します。`id`はURLに使用する固定slugです。配列順が掲載順、`featured: true`が常時表示のFeatured、`false`がタイトルだけを初期表示するOtherになります。Otherを開くとFeaturedと共通の`app-showcase.html`で説明・実画像・CTAを表示します。開閉は標準の`details`／`summary`を使い、JavaScript不要で複数同時に開けます。
2. `data/home/`の6言語すべてへ、同じIDでアプリ名・短い説明・`platform`・必要な`taglineLines`・`imageAlts`を追加します。既存Featuredのコピー変更には仕様上の根拠が必要です。
3. 実際のアイコン・スクリーンショットを`static/images/apps/<id>/`へ配置し、`data/apps.json`に幅・高さとsmall／large画像を登録します。素材がない場合は`screenshots: []`にします。
4. 使い方、FAQ、Privacy、Termsがある場合は既存の規則で`content/<section>/<id>.md`を用意します。Product下部のSupportは同じIDからこれらのページを探し、翻訳がなければ日本語ページへ案内します。
5. `data/product_details/<id>.json`へ、Homeとは別の製品紹介を6言語で追加します。公開版とローカル開発版を区別して確認し、根拠と素材の出典を`docs/products/`へ残します。下の「Product詳細の編集」を参照してください。
6. `npm run sync:products`、`npm run build`、`npm run verify`を実行し、差分とブラウザ表示を確認します。

現在は8アプリ×6言語の48 Productページと、主要3セクション＋Support互換ページ×6言語の24入口、計72 Markdownを`scripts/sync-products.py`で同期します。生成ページにはマーカーがあり、直接編集せず共通JSONを変更します。手書きの記事は同期スクリプトの上書き対象になりません。

Other Appsの実画面も同じ画像データからHomeとProduct詳細へ反映します。[追加素材の出典](docs/homepage/other-app-assets.md)を参照してください。

アプリをデータから取り除く場合、生成ページを自動削除することはありません。旧URLからの到達方法を決めてから対応してください。ID変更もURL変更になるため、表示名の変更だけを目的にIDを変えないでください。

### Product詳細の編集

Homeは短い紹介、Product詳細は具体的な用途と条件、Supportは操作方法・FAQを担当します。詳細本文を増やすために`data/home/`の既存コピーやサポート本文を変更する必要はありません。

`data/product_details/<id>.json`の`locales`に`ja`・`en`・`ko`・`de`・`fr`・`zh-hant`を用意します。各言語には`overviewTitle`、`overview`（2段落）、`features`（アプリに合う3〜6項目のtitle／description）、`stories`（画像と説明を組み合わせた2〜3項目）、`audienceTitle`、`audience`（3項目のtitle／description）、`notes`（利用条件）を設定します。項目数をそろえる目的で機能を作らないでください。

`stories`は`image: 0`のように`data/apps.json`の既存画像を参照できます。詳細だけに使う実素材は同じファイルの`media`にsmall／large／width／height／largeWidthを登録し、storyから`media: "pdf"`等のキーと、その言語の`alt`で参照します。新しい画像をHomeへ追加する必要はありません。画像は縦横比を維持したWebPを2サイズ用意し、原本・SHA256・採用根拠を記録します。

`minimumOS`はApp Store公開情報とプロジェクトのdeployment targetを照合してから記入します。不明な場合は省略します。開発中アプリの最低OSや価格を推測して埋めないでください。料金の固定値は避け、公開中アプリだけApp Storeの最新情報へ案内します。

Product詳細の公式バッジはHeroと主要説明後の2箇所です。国旗はHeroだけ、Supportは最下部の直接リンクを維持します。Homeのバッジは各アプリ1箇所のままです。[詳細ページ拡張の記録](docs/products/REPORT.md)に、採用した内容・素材・検証結果をまとめています。

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

## URL・コンテンツの互換性

既存の`/htu/`、`/faq/`、`/privacy/`、`/terms/`、`/notes/`と各言語URLはApp Store Connectや外部記事から参照されている可能性があります。ファイル名・slugを変更する場合は、旧URLを維持するかHugoの`aliases`で到達可能にしてください。各アプリのPrivacy／Termsは統合しません。

Product下部の`#support`は使い方・FAQ・問い合わせ・Privacyへ直接案内します。ProductからSupport一覧へ移動して同じアプリを再選択させないでください。HeaderはProducts／News／Company、Footerは会社Contactだけを担当します。アプリ選択はProductsに一本化し、各カードの「製品を見る」は`/products/<id>/`、「サポート」は同じProductページの`#support`へ直接進めます。アプリ名・端末・既存のキャッチコピーまたは説明・公開状況は共通データから表示し、一覧には使い方やFAQを展開しません。

旧`/support/`、`/htu/`、`/faq/`、`/privacy/`、`/terms/`の集約URLは互換用にHTTP成功・自己canonicalを維持し、`noindex, follow`とProductsへの簡潔な案内を付けます。これらは主要ナビやHomeから案内しません。旧Supportの`#<id>`・`#support-<id>`はCSSの`:target`で対象アプリの直接Supportリンクだけを表示し、`#contact`も維持します。個別本文・Privacy・利用規約URLは変更しません。Homeの旧`#support`はHeroのProducts CTAへ接続します。

Productsへのハブ統合は[統合レポート](docs/hub/REPORT.md)、以前の素材・CTA・News・Privacy・Footer整理は[UX修正レポート](docs/ux/REPORT.md)を参照してください。

`docs/migration/baseline.json`は移行前の191 HTML URL、記事本文・アンカー等を保存した検証基準です。`npm run verify`で既存コンテンツ、新しいProduct／主要一覧、内部参照、Store CTA、SEO・OGP、sitemap・robotsを検査します。

baselineは意図しないURL削除や本文変更を検出するためのものです。チェックを通す目的で作り直さず、意図した既存記事の改訂では、変更根拠と差分を確認したうえで基準更新を扱ってください。外部App Storeの最新提供状態、端末実機、ブラウザの見た目をこの静的検査だけで証明することはできません。

## デザイン・画像・themeの保守

HugoplateのTailwind CSS v4、base typography、content typography、container／section、button primitivesを利用します。`templates.Defer`でHTML生成後にCSSを処理し、fingerprint付きCSSを配信します。KUMAKIKAIの変更はrootの`layouts/`・`assets/`・`data/`に置き、vendor内部へ直接加えません。

採用元は[Hugoplate公式commit `2f5a454ee708f5f2666414af9ef48df65570752a`](https://github.com/zeon-studio/hugoplate/tree/2f5a454ee708f5f2666414af9ef48df65570752a)、package 3.5.1です。`themes/hugoplate/UPSTREAM.json`に採用ファイルとSHA-256、同ディレクトリにMIT LICENSEを保存しています。デモ記事、イラスト、testimonial、slider、不要なGo Modulesは含めません。

上流更新時は固定commitとの差分を調べ、採用しているruntimeだけを更新し、SHA・出典・必要バージョンを更新します。公式starterの`project-setup`／`update-theme`をこのサイトでそのまま実行すると既存構成と衝突するため、使用しません。更新後はbuild、移行検証、主要画面のresponsive／Light／Dark／キーボード操作を確認します。

build依存はTailwind、Tailwind CLI、Typographyの3種類です。追加のWeb Font、SPA、animation frameworkは使用していません。色・フォントは`data/theme.json`と`assets/css/site.css`の既存変数を確認して変更します。

画像にはWebPのresponsive variantsと実寸を設定し、Hero以外は原則lazy loadingにします。実在しないUIや未公開機能を画像で補いません。HeroとOGPの出典・加工内容は[Hero素材記録](docs/migration/hero-assets.md)、[OGP素材記録](docs/migration/og-assets.md)を参照してください。OGPのPNGはコミット済みで、通常のbuild時には再生成しません。

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
