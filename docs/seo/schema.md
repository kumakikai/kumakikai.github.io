# 構造化データの設計と検証契約

確認日: 2026-09-07。実装: `layouts/_partials/seo/schema.html`。

## ブランド・人物・アプリの関係

KUMAKIKAIはYuya Nakamuraが運営する開発ブランドとして扱う。法人・組織を推定せず、`Organization` / `Corporation`、勤務先、受賞、学歴、未確認SNSを追加しない。

| Entity | 全言語共通の `@id` | 主な接続 |
| --- | --- | --- |
| Brand: KUMAKIKAI | `https://kumakikai.github.io/#brand` | Personの`brand`から参照 |
| Person: Yuya Nakamura | `https://kumakikai.github.io/company/#person` | `brand` → KUMAKIKAI |
| WebSite: KUMAKIKAI | `https://kumakikai.github.io/#website` | `publisher` → Person、`about` → Brand |
| SoftwareApplication | `https://kumakikai.github.io/products/<id>/#software` | `creator` / `publisher` → Person |
| WebPage / AboutPage | 各言語ページのcanonical URL + `#webpage` | `isPartOf` → WebSite、製品や人物を`mainEntity`で参照 |

[Personのbrand](https://schema.org/brand)は、事業者個人が維持するブランドを表現できる。[Brand](https://schema.org/Brand)は法人格を意味しない。[creator](https://schema.org/creator)と[publisher](https://schema.org/publisher)の値はPersonまたはOrganizationであり、Brandを直接代入しない。アプリ → Yuya Nakamura → KUMAKIKAIの順に、同じIDを参照して接続する。

Personの名前・肩書きは、各言語の既存Aboutデータを使用。名前は`Yuya Nakamura`のみ。人物URLは既存`/company/`を維持。Aboutはブランドと人物の両方を紹介するため`AboutPage`とし、人物だけの専用プロフィールページだとは扱わない。WebSiteは全言語で一つ。ルートHomeに`name: KUMAKIKAI`と正式URLを出力し、言語別の別サイト名を作らない。[Googleのサイト名仕様](https://developers.google.com/search/docs/appearance/site-names)

## Product

- 正式名: 表示中の言語の`data/home/*.json`。同じアプリは翻訳名が異なっても共通IDを使う。検索語を推測した別名は追加しない。
- description: headから受け取る、そのProduct固有の最終description。
- `operatingSystem`: `data/apps.json`の確認済み値。Uni:Noteは`iPadOS`。Apple Watchは`product_details/<id>.watch.status == published`の場合だけ`watchOS`を追加し、審査中は利用可能OSとして追加しない。
- `downloadUrl`: `status == published`かつ既存App Store URLがある場合のみ。Noccaは`creativeWorkStatus: In development`で紹介し、ダウンロードURLを出さない。
- `applicationCategory`: サイト上の大分類`learning / communication / utilities`から、それぞれ`EducationalApplication / CommunicationApplication / UtilitiesApplication`へ対応。これはサイトの用途分類であり、App Storeの公式カテゴリを新たに断定したものではない。未知の分類は省略。
- image / screenshot: 現在Productページで使う実アプリアイコンとスクリーンショットのURL。配信地域やアプリ内対応言語をサイト言語から推測しない。
- 価格、offers、aggregateRating、review、reviewCountは追加しない。

[SoftwareApplicationの定義](https://schema.org/SoftwareApplication)では、これらの確認済み情報を記述できる。一方、[GoogleのSoftware Appリッチリザルト](https://developers.google.com/search/docs/appearance/structured-data/software-app)は`offers.price`および評価・レビューを必須としている。本実装はその値を維持する仕組みがなく、ユーザー指示でも推定値は禁止されているため、**schema.orgとしての構造・syntaxの整合と、GoogleのSoftware Appリッチリザルト適格性は区別する**。リッチリザルト適格とは報告しない。Rich Results Testでその不足を指摘されても、ダミー値で埋めない。

## 記事とパンくず

Blogは`BlogPosting`、正式紹介Press ReleaseとInformationは`Article`。記事名、固有description、分類、author / publisher、`mainEntityOfPage`を設定する。公開日と更新日はHugoの`.Date` / `.Lastmod`を使い、build時刻は使わない。既存`relatedProducts`と本文の関連Product導線に対応するアプリだけを`mentions`に指定する。[BlogPosting](https://schema.org/BlogPosting)、[Google Article仕様](https://developers.google.com/search/docs/appearance/structured-data/article)

Article.imageは任意。現状の汎用OGPロゴを、本文を代表する写真と同等に扱って機械的には出力しない。OGPは通常のheadで維持する。Google Articleには必須プロパティの指定はないが、画像を加える場合は実際の記事内容を代表するクロール可能な画像を使用する。今後本文に適切な画像を加えた場合に、画像の意味を確認したうえでschema側へも反映する。

Product詳細の`BreadcrumbList`は、現在画面にある`Products > アプリ名`の2要素と同じ。URLの言語も現在ページに合わせる。新しい可視パンくずや架空の階層は追加しない。Guide / FAQ / Newsのパンくずは現在の目的・分類表示を維持し、SEO目的でProductと同じ階層を無理に付けない。[Google Breadcrumb仕様](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)

## production build後に検証する契約

1. JSON-LDは配信HTMLの`script[type=application/ld+json]`に一つの`@graph`として存在し、JSONとしてparse可能。
2. Home / About / 全Product / 記事でBrand / Person / WebSiteのIDが共通、各ページID・URLはself canonicalと整合。
3. `Organization`、`Corporation`、架空のsameAs / employer / award / alumniOf、offers / review / aggregateRatingが存在しない。
4. 全48 Productで正式名とOS・画像がProductデータに一致。公開済み7アプリ×6言語はdownloadUrlあり、開発中Nocca×6言語はなし。審査中すわなびにwatchOSなし。
5. Productのcreator / publisher参照先がPersonで、そのPerson.brand参照先がBrand。Brandをcreator / publisherへ直接入れない。
6. AboutのPerson名・肩書きとHTML本文が一致し、漢字氏名や非公開個人情報はない。
7. 記事のtypeがカテゴリに対応し、headlineと日付が本文表示・front matterに一致。汎用OGPをArticle.imageへ複製しない。
8. ProductのBreadcrumbListは2要素、positionは1と2、Productsは現言語URL、最終itemは当該ProductのURL。
9. noindexの旧互換ハブや404では、caller側のindex対象判定に従い、この検索向けgraphを省略。
10. build後と本番取得後のJSON-LDを比較。Googleによる実際の再クロール・検索表示は別の確認段階として扱う。

情報はユーザーが閲覧できるページと一致させ、構造化データにだけ検索用キーワードを隠さない。[Googleの一般的な構造化データガイドライン](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
