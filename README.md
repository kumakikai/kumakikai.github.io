# KUMAKIKAI公式サイト

[kumakikai.github.io](https://kumakikai.github.io/) のソースです。Hugo ExtendedとHugoplateを基盤に、iPhone・iPadアプリのProducts、Support、News、Companyを提供します。日本語、英語、韓国語、ドイツ語、繁体字中国語、フランス語に対応しています。

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
| `data/corporate/<lang>.json` | 6言語のナビゲーション、会社紹介、各一覧・CTAのコピー |
| `data/theme.json` | Hugoplateの色・フォント・文字サイズtoken |
| `data/hero.json` | 実UIを使ったHero画像の寸法、responsive画像、alt |
| `data/news.json` | 既存Notes記事のカテゴリ・関連プロダクトを補うメタデータ |
| `content/products/` | 各ProductとProducts一覧の生成Markdown |
| `content/support/`、`content/news/`、`content/company/` | 各セクションの生成入口と、追加する編集記事 |
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

1. `data/apps.json`にアプリを追加します。`id`はURLに使用する固定slugです。配列順が掲載順、`featured: true`がFeatured、`false`がOtherになります。
2. `data/home/`の6言語すべてへ、同じIDでアプリ名・短い説明・`platform`・必要な`taglineLines`・`imageAlts`を追加します。既存Featuredのコピー変更には仕様上の根拠が必要です。
3. 実際のアイコン・スクリーンショットを`static/images/apps/<id>/`へ配置し、`data/apps.json`に幅・高さとsmall／large画像を登録します。素材がない場合は`screenshots: []`にします。
4. 使い方、FAQ、Privacy、Termsがある場合は既存の規則で`content/<section>/<id>.md`を用意します。Support／Productは同じIDからこれらのページを探し、翻訳がなければ日本語ページへ案内します。
5. `npm run sync:products`、`npm run build`、`npm run verify`を実行し、差分とブラウザ表示を確認します。

現在は8アプリ×6言語の48 Productページと、4セクション×6言語の24入口、計72 Markdownを`scripts/sync-products.py`で同期します。生成ページにはマーカーがあり、直接編集せず共通JSONを変更します。手書きの記事は同期スクリプトの上書き対象になりません。

アプリをデータから取り除く場合、生成ページを自動削除することはありません。旧URLからの到達方法を決めてから対応してください。ID変更もURL変更になるため、表示名の変更だけを目的にIDを変えないでください。

### 公開状態とApp Store

- 公開済みは`status: "published"`、開発中は`status: "development"`です。
- 開発中アプリにはApp Store URLを設定しません。Download／Store CTAも表示しません。
- `availability.verifiedStorefronts`には実際に確認できた地域だけを記録します。`coverage: "partial"`は全世界の提供状況を確認済みという意味ではありません。
- 現在のCTAは確認済みの**日本のApp Store**を指します。サイトの表示言語を変更しても、未確認の地域URLを自動生成しません。
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

カテゴリは`information`または`press-release`を使います。関連プロダクトがなければ`related_products`は省略できます。本文を記入し、公開時は`draft: false`に変更します。Hugoは通常、未来の日付の記事を公開対象に含めません。

必要に応じて`lastmod`に実際の更新日時を設定できます。記事ごとのOGPには次のように`static/`以下の画像を指定します。未指定時は関連プロダクトのOGP、または共通OGPを使います。

```yaml
images: ["/images/og/uni-note.png"]
```

翻訳を追加する場合は同じbasenameで`.en.md`、`.ko.md`、`.de.md`、`.zh-hant.md`、`.fr.md`を作成します。現在日本語だけの記事は、他言語のNewsにも日本語の記事として案内しています。

既存の`content/notes/`記事をNewsへ表示するために移動する必要はありません。`/notes/.../`を維持したままNews一覧へ集約します。旧記事のカテゴリ・関連アプリは`data/news.json`、新記事はfront matterで管理できます。

## URL・コンテンツの互換性

既存の`/htu/`、`/faq/`、`/privacy/`、`/terms/`、`/notes/`と各言語URLはApp Store Connectや外部記事から参照されている可能性があります。ファイル名・slugを変更する場合は、旧URLを維持するかHugoの`aliases`で到達可能にしてください。各アプリのPrivacy／Termsは統合しません。

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

この確認はHTTP GETのみで、App Store Connectの登録内容を変更しません。詳しい移行・画面検証は[移行報告](docs/migration/REPORT.md)を参照してください。
