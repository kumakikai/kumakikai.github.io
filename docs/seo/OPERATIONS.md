# SEO・検索インデックスの運用

## 正式URLと管理場所

正式サイトは `https://kumakikai.github.io/`。Aboutは `/company/`、既存記事は `/notes/<既存slug>/` のまま。検索対策を理由にSupport・Privacy・Guide・FAQ・Press ReleaseのURLを移動しない。

- `data/seo/<lang>.json`：Home・About・全Productの固有title／description。
- `scripts/sync-products.py`：Product／Aboutの `seo_title` とdescriptionを生成。H1用のtitleは正式名称を維持。
- `layouts/_partials/seo/`：検索対象の判定、実在翻訳のalternate、Brand／Person／SoftwareApplication等。
- `layouts/sitemapindex.xml`：root `/sitemap.xml` へ全言語の検索対象を集めるurlsetを生成。日本語URLは `/ja/` 配下にないため、rootに全URLを置いてsitemapの範囲を明確にする。
- `layouts/sitemap.xml`：従来の各言語sitemap URLも維持。提出するのはrootの `/sitemap.xml` だけでよい。
- `hugo.toml`：verification値、言語、Gitによる更新日fallback。

## 新しいProduct

READMEの追加手順に沿い、正式アプリ名、固有description、実画像、操作内容を説明するalt、公開状態、確認済みApp Store URL、対応OSを登録する。未公開はdownloadUrlを出さない。すわなびのWatchは `watch.status` が `published` となるまでschemaの対応OSへ含めない。

タイトル・短い説明・OS・URL等は共通データから生成し、本文の主力コピーをSEOキーワードの羅列へ変えない。既存の主要キャッチコピーと画像altは維持する。検索上意味があるという推測だけでアプリの別名やsameAsを足さない。

Products一覧は全アプリへ静的リンクを持つ。Home・Aboutのランダム候補に選ばれなくても発見可能。全アプリをHomeの不可視テキストへ追加する必要はない。

## 新しいNews・Press Release・Blog

新規記事はMarkdownで追加する。既存記事のslug・公開日は維持する。

```yaml
---
title: "記事の正式タイトル"
description: "その記事で発表・記録している内容を具体的にまとめた固有の説明。"
date: 2026-09-07
lastmod: 2026-09-07
news_category: "information"
related_products: []
---
```

`news_category` は `press-release` / `blog` / `information`。正式なアプリ紹介はPress Release、開発・運営の読み物はBlog、利用者向け告知はInformation。既存Notesは `data/news.json` の分類補助も参照する。関連Productが実際に登場する場合のみ `related_products: ["uni-note"]` 等を指定し、既存の関連Product欄へ静的リンクを出す。

`lastmod` は本文・タイトル・説明などを実際に更新した日。単なる再buildで変更しない。明示値がない既存ページはHugoのGit履歴、それもなければ記事のdateへfallbackする。CIは `fetch-depth: 0` を維持する。共通データを変更したときは同期されたMarkdownをコミットし、Homeの実質的な内容・SEOを更新したときは各 `content/_index*.md` のlastmodも更新する。

SoftwareApplicationのcreator/publisherはPerson、Person.brandはKUMAKIKAIのBrandを参照する。Brandをschema.orgで許可されないcreator/publisher型へ無理に割り当てない。Article/BlogPostingの著者も同じPerson。価格・評価を管理していないため、GoogleのSoftware Appリッチリザルト適格性は主張しない。

## 検索対象外のURL

旧 `/support/`、`/privacy/`、`/htu/`、`/faq/`、`/terms/`、`/notes/` の一覧、旧pagination、空のtaxonomy、404はnoindex。HTTP互換性と必要なリンクを維持し、robots.txtでクロールを遮断しない。各アプリ固有Guide／FAQ／Privacy／TermsとPress Releaseはindex対象。

新規ページを明示的に検索対象外へする場合は `noindex: true`。同じ判定がrobots meta・sitemap・hreflang・schemaへ反映される。404を200で返す独自routingは追加しない。

## Google Search Console（ユーザー対応）

2026-09-07、ユーザー回答で未登録を確認。verification値は発行されておらず、空欄のまま公開する。

1. [Search Console](https://search.google.com/search-console/) を開き、**URLプレフィックス**のプロパティとして `https://kumakikai.github.io/` を登録する。GitHub管理の `github.io` DNSを編集するDomain方式は使わない。
2. 所有権確認で **HTMLタグ** を選ぶ。発行された `<meta name="google-site-verification" content="…">` の **content値だけ**を `hugo.toml` の `[params.verification] google` へ設定する。値の発行・推測・生成をサイト側で行わない。
3. production build・commit・push後、トップのHTML sourceにmetaがあることを確認してから、Search Consoleの「確認」を実行する。確認後もタグを削除しない。
4. 「サイトマップ」で **`https://kumakikai.github.io/sitemap.xml`** を送信する。全言語の検索対象URLを含む。
5. 「URL検査」で以下を確認し、必要に応じて「公開URLをテスト」→「インデックス登録をリクエスト」を実行する。大量の自動送信はしない。

優先URL：

- https://kumakikai.github.io/
- https://kumakikai.github.io/products/
- https://kumakikai.github.io/company/
- https://kumakikai.github.io/products/uni-note/
- https://kumakikai.github.io/products/oto-miru/
- https://kumakikai.github.io/products/giga-poke/
- https://kumakikai.github.io/products/nocca/
- https://kumakikai.github.io/products/signal/
- https://kumakikai.github.io/products/smokeless/
- https://kumakikai.github.io/products/uni-note-pocket/
- https://kumakikai.github.io/products/balance-calendar/
- https://kumakikai.github.io/news/

旧タイトルが検索表示に残った `/notes/2026-01-23-introduction/` と `/notes/2026-04-01-uni-note-pocket/` もURL検査対象にする。以後「ページのインデックス登録」「サイトマップ」「ウェブに関する主な指標」「検索パフォーマンス」を確認し、KUMAKIKAI／kumakikai、Yuya Nakamura、正式アプリ名とブランド・氏名の組み合わせを観測する。

HTMLタグ方式の条件と継続保持：[Google公式・所有権の確認](https://support.google.com/webmasters/answer/9008080?hl=ja)。sitemapの掲載・lastmod：[Google公式・サイトマップ作成](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=ja)。リクエストはクロールや掲載の保証ではなく、反映を待つ間にURLやtitleを毎日変更しない。

## Bing

Google登録後、[Bing Webmaster Tools](https://www.bing.com/webmasters/) でSearch Consoleから既存プロパティをimportできる。手動登録する場合も同じroot sitemapを使い、発行されたmeta値を `[params.verification] bing` へ設定すると `msvalidate.01` を出力する。専用のSEOページ・IndexNow・大量送信ツールは不要。[Bing公式・追加と確認](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b)

## build・公開後の検証

```sh
npm run sync:products
npm run build
npm run verify
python3 scripts/verify-seo.py --build public --output docs/seo/verification.json
```

最後にGitHub Actions・Pages成功を確認し、本番HTML／robots.txt／sitemap.xmlを再取得する。ローカル検査のみで公開完了にしない。LighthouseのLCP/CLS/TBTはラボ計測であり、実ユーザーのINPやCore Web Vitals合格と同一視しない。Search Consoleのデータが集まった後に実ユーザー指標を確認する。
