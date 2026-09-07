# SEO・検索インデックス強化

対象： https://kumakikai.github.io/ 。変更前 source `3d0f034`、公開物 `dac80f6`。

デザイン・主要コピー・ランダムFeatured・正式URLを維持し、初期HTMLのメタデータ、構造化データ、クロール対象の整理と検証を実施した。Google Search Consoleはユーザー回答で未登録。検索順位・インデックス登録完了を意味する作業ではない。

## 実装と確認項目

| 項目 | 対応 |
| --- | --- |
| Home | `KUMAKIKAI \| iPhone・iPadアプリ`。descriptionに開発ブランド、Yuya Nakamura、Uni:Note・オトミルとの関係を明示 |
| About | `About \| KUMAKIKAI - Yuya Nakamura`。Software Engineer / App Developer、開発経験、iPhone・iPadアプリとの関係を固有descriptionで説明 |
| Product | 全8アプリ×6言語に正式名称＋KUMAKIKAIのtitleと固有description。本文・H1・既存キャッチコピーは維持 |
| canonical | 検索対象は全件正式URLのself canonical。言語間の日本語への統合なし |
| sitemap | root sitemapへ全6言語の検索対象156URLを集約。旧各言語sitemapもHTTP互換性のため維持 |
| robots | `User-agent: *`、`Allow: /`、root sitemap。通常クローラーの拒否なし |
| hreflang | 実在する相互翻訳だけをja/en/ko/de/zh-Hant/frで出力。対応する日本語ページがある場合のみx-default。言語とApp Store地域は別管理 |
| Brand / Person | KUMAKIKAIはBrand、Yuya NakamuraはPerson。Person.brandで関係付け。法人・架空の勤務先・SNSを作らない |
| SoftwareApplication | 全48 Product。正式名、固有description、OS、アイコン、スクリーンショット、分野、公開済みdownloadUrl。creator/publisherは共通Person、PersonからBrandへ接続 |
| Article | Press Release 8件はArticle、Blog 7件はBlogPosting。全15記事の固有description、実際の公開日・更新日・著者・関連Productを設定 |
| Breadcrumb | Productの既存Products→アプリの可視パンくずと同じBreadcrumbList |
| 静的内部リンク | 全言語Productsから全8アプリ。全8 Press ReleaseからProductへの既存リンクを維持。Blogのうち言及がある6記事の既存Productリンクを維持 |
| 画像 | 既存の具体的alt、WebP/srcset、width/height、遅延読込、OGPフォールバックを維持。欠落やSEOキーワード列は追加していない |
| 名称 | 共通Productデータの正式名を維持。検索されそうという推測だけで別名・alternateNameを追加しない |
| 人物検索 | JA Homeの既存人物紹介を維持し、他5言語の同じ段落を忠実に翻訳。Home/About本文、meta、Personの氏名を一致 |
| ブランド検索 | site name・favicon・OGPのKUMAKIKAIを維持。Home/meta/entity graphでブランドと人物・Productを関連付け |
| noindex | 旧一覧ハブ・pagination・空taxonomy・404の54ページ。全アプリ固有Guide/FAQ/Privacy/Termsと既存記事は検索対象を維持 |
| 互換ページ | 全277 HTMLのURLを維持。既存67 redirect文書は実在の移行先へ即時meta refreshとcanonical。新redirectやslug変更なし |
| 最終更新日 | 明示lastmod→modified→Git履歴→公開日の順。CI fetch-depth:0。build時計は使わない |
| 運用 | SEOデータ一元管理、Product同期検査、独立SEO検証をCIへ追加。Google/Bing発行済みverification値をconfigで管理可能 |
| GitHub | public repository、Pages有効、READMEの公式サイトリンクを維持。description/Website設定は空欄であることを確認。不要なリポジトリ設定変更なし |

Home/About/全Productの採用title・descriptionとBefore/After全文は [metadata.md](metadata.md)、6言語の管理値は `data/seo/`、全Newsの変更前後は [news-metadata.md](news-metadata.md) と [news-metadata.json](news-metadata.json)。News本文・タイトル・公開日・URLは変更していない。

構造化データの型・propertyの根拠は [schema.md](schema.md)。Brandをcreator/publisherに直接置くとschema.orgの許容型と合わないためPersonを使用し、そのPerson.brandでブランドへつなぐ。Noccaは開発中でdownloadUrlなし。すわなびのWatchは審査中のため公開済みOSにwatchOSを追加していない。価格・評価・レビューを捏造してGoogle Software Appリッチリザルトの要件を埋めていない。JSON-LDの正しさとGoogleのリッチリザルト適格性は別である。

## 検証記録

- [変更前監査](baseline.md)：全277HTML、主要28HTTP、本番Lighthouse6条件。
- [SEO全件検証](verification.json)：初期HTMLを解析。277HTML、index156=sitemap156、全48Product、156graph、Article8/BlogPosting7、errors/warnings0。
- [負テスト](verification-negative-tests.json)：localhost canonical、誤noindex、不正JSON-LD、存在しないhreflang、公開download欠落、架空ratingの6件を全て検出。
- [既存URL・本文・リンク検証](migration-verification.json)：旧191URL、138正式URL、53旧alias、84記事、全48Product、416Support行、画像・内部リンクを検証。
- Nocca法務保護テスト18件PASS。SEOdescription/lastmod変更による厳密なファイルhash更新のみ、本文・法務・リンクの許可範囲は変更なし。[照合記録](nocca-source-review.json)
- [ブラウザ回帰検証](browser/results.json)：39条件・全interactionで成功。全Product、Home/Products/About/News、代表Guide/FAQ/Press Release、5言語Home、Light/Darkを確認。キーボード操作、画像、overflow、heading、axeに問題なし。
- production build：Hugo Extended0.158.0、Node22.22.0、npm lockfile。エラー・警告なし。CIへSEO全件チェックを追加。

## 本番確認

- source `106f7d943e2302436687604b2f4cbf3a749a15ef`。CI [34091249305](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34091249305) と Pages [34091346043](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34091346043) が成功。
- 公開生成物 `14e8efc84d61858c86e23986ea7409c3e3d1cb3c` を取得。[全277HTMLがローカルとbyte一致](local-deployed-comparison.json)。[公開生成物に対するSEO独立検証](deployed-verification.json)も全件成功。
- [本番HTTP全件照合](live-http.json)：277 HTML＋384リソース＝661件すべてHTTP 200、SHA-256一致。画像・CSS・JS・robots・全言語sitemapを含む。210本文ページは共通Header `Products / News / About` とContact中心Footer、旧文言・旧テンプレート混在なし。
- Uni:Note/About/Newsは通常・再検証・query・明示index.html・Mobile UA・Googlebot UAの計18条件でも同一。第三者検索サービスの内部キャッシュまで照合したという意味ではない。
- [本番routing](live-routing.json)：主要ページにクロール拒否のX-Robots-Tagなし。末尾スラッシュなしProductは301で正式URLへ、存在しないURLはHTTP 404。robotsはAllow:/とroot sitemapを出力。
- サイトマップの156URL、全48Productの固有title/description/canonical/構造化データが初期HTMLで配信されている。検索エンジンのJS実行を前提としない。

大型の監査JSONは要約と無損失 `.json.gz` 原本に分離。要約の `fullEvidence` を参照し、必要に応じて `gzip -dc` で展開できる。[公開後Lighthouse比較](performance-comparison.md)：Home／Uni:Note Product／GuideのMobile・Desktop計6条件でPerformance／Accessibility／Best Practices／SEOが100。Mobile LCPは1.23〜1.53秒、Desktopは0.28〜0.34秒、CLS0、TBT0。ラボ値であり実ユーザーINPは未計測。

監査スクリプトで変更前のDesktopラベル3件が実際Mobile設定になっていたことを発見し、正式Desktop設定とformFactor検査へ修正した。変更前Desktopは「未計測」と訂正し、原本を無損失保存している。Mobileのみを変更前との同条件比較に用い、100点をSEO変更による速度向上やGoogle掲載保証とは解釈しない。

## Search Consoleと残課題

[Google検索の観測](search-observation.md)では、旧タイトルの記事2件が検索画面に残っていた。現在の本番が旧テンプレートだという意味ではなく、検索結果の更新はGoogleの再クロールを待つ必要がある。表示件数をサイト全体のindex件数とは扱わない。

ユーザー側でSearch ConsoleのURLプレフィックス `https://kumakikai.github.io/` を作成し、発行されたHTMLタグのcontent値を設定する。値は現在空欄。所有権確認後に `https://kumakikai.github.io/sitemap.xml` を送信し、Home・Products・About・全Productと旧タイトルが残る2記事をURL検査する。詳しい手順・優先URL・追加運用は [OPERATIONS.md](OPERATIONS.md)。Bingも同じサイトマップを使用できる。

Lighthouseはラボ計測。実ユーザーINP/CrUX、Search ConsoleのIndexing/Search Results/Core Web Vitalsは登録後・データ収集後の確認事項。検索順位やGoogleのindex登録完了は保証・未確認の報告をしない。
