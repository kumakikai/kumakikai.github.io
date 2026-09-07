# SEO変更前監査

監査対象は main `3d0f034` の生成済み `public/` と、2026-09-07 15:00〜15:05 JST 時点の `https://kumakikai.github.io/`。実装変更前のデータは `before-generated.json`、HTTP比較は `before-live.json`、横断集計は `before-analysis.json` に保存した。

## クロール・インデックス

- 生成HTMLは277件。本文を持つ通常ページ210件、互換redirect文書67件。
- `robots.txt` は `User-agent: *` / `Allow: /`。本番sitemap indexへの参照があり、全体のクロール拒否はない。主要取得レスポンスに `X-Robots-Tag` の拒否設定はない。
- sitemap indexと日本語・英語・韓国語・ドイツ語・繁体字・フランス語の6言語sitemapは本番HTTP 200。掲載URLは重複除外194件。
- Home、Products、About（`/company/`）、News、全48 Product、Guide/FAQ/Privacy/Terms本文、既存15記事は発見可能。各アプリのPrivacy本文はnoindexにしていない。
- **修正候補：noindexの互換ハブ25件がsitemapに混在**。`/support/`、`/privacy/`、`/htu/`、`/faq/` の各言語版と `/terms/`。HTTP成功を維持したまま、sitemapから除外するのが整合的。
- **修正候補：旧 `/notes/` はNewsと役割が重複したindex対象の一覧**。`/notes/page/2/`〜`/notes/page/5/` もnoindexなし、canonicalは全て `/notes/`、sitemap外。これらの互換一覧を検索対象として増やす必要はない。個別記事の `/notes/<slug>/` はそのまま保持する。
- 通常210ページすべてにtitle/descriptionとH1が存在し、H1は各1件。H2/H3等の見出し階層飛びは0件。
- index対象の通常ページでは旧Notesのページネーション4件を除き自己参照canonical。localhost・preview・別ドメインcanonicalはない。
- 翻訳先は全て実在。主要翻訳ページのhreflangは相互に対応。旧ページネーション10URLには親一覧のhreflangが継承され、相互性がない。検索対象外の互換ページでは不要なalternateを出さない整理が適切。
- 現行hreflangは `ja-JP`、`en-US`、`ko-KR`、`de-DE`、`zh-Hant`、`fr-FR`。各Productの翻訳canonicalを日本語へ統合していない。`x-default` は未設定。
- sitemap lastmodは116件未設定、78件は実際のfront matterに基づく日付。全ページをbuild時刻に更新している状態ではない。

## ブランド・人物・Productの関係

| 項目 | 変更前 | 対応候補 |
| --- | --- | --- |
| Home title | KUMAKIKAI — iPhone & iPad Apps | 日本語Homeの事業内容を日本語で明示 |
| Home description | iPhone・iPad向けのアプリを企画・開発・運営しています。 | ブランド・Yuya Nakamura・代表Productとの関係を自然に含める |
| About title | About \| KUMAKIKAI | 現行URL/表示名を維持し、人物との関係をmetadataで明示 |
| Product title | 各正式アプリ名 \| KUMAKIKAI | 既に固有。正式名を維持 |
| Product description | 個別の機能紹介。ただしHomeの紹介文と同じ | Productごとの固有説明と開発ブランドの関連を整備 |
| 構造化データ | Organization 147ページ、SoftwareApplication 48ページ、Article 15記事 | 法人と誤認させないBrand/Person、共通 `@id`、Productとの意味的な接続 |

現在のSoftwareApplicationは正式名称、OS、固有説明、アイコン、製品URLを含む。一方、識別用 `@id`、`downloadUrl`、`applicationCategory` は未設定。`creator` は名前だけのOrganizationで、サイト側entityとの明示的な接続がない。架空の価格・レビュー・評価はない。

Aboutの人物情報はOrganization内のfounderにのみ含まれ、独立したPerson識別子がない。全News記事はArticleになっており、BlogPostingの区別、author、mainEntityOfPage等の改善余地がある。

OGPはページごとのtitle/description/URL/imageと共通 `og:site_name=KUMAKIKAI` を出力。Twitter Cardはsummary_large_image。Product画像と共通フォールバック画像へのリンクは存在し、faviconのサイト表記は統一されている。

## 内部リンク・画像・既存URL

- 各言語のProducts一覧から全8 Productへ、JavaScript実行前から通常のHTMLリンクが存在する。HomeのランダムFeaturedは唯一の発見経路ではない。
- HomeからProducts/News/About、AboutからProducts、Productから固有Guide/FAQ/Privacy/Termsへ直接到達可能。
- 全8 Press Releaseに対象Productへのリンクが既にある。既存Blogは7件中6件に言及するProductへのリンクがある。Android版公開についての記事は対象アプリ名を特定したリンクを持たない。リンク数を増やすだけの追加は不要。
- 全通常ページで画像alt属性の欠落0件、画像width/height欠落0件。装飾画像は意図的な空alt。操作画像等の説明altをSEOキーワードに置き換える必要はない。
- 主要URLとrobots/sitemapの28件を本番再取得。変更前生成物と照合可能な25件はすべてHTTP 200かつSHA-256一致。
- `/products/uni-note` はHTTP 301で `/products/uni-note/` へ正規化。`/products/uni-note/index.html` はHTTP 200だが、canonicalは末尾スラッシュの正式URL。
- `/seo-audit-nonexistent-20260907/` はHTTP 404。200のSoft 404ではない。

## 変更前性能（本番Chrome / Lighthouse）

既存の一時QA環境のLighthouse 12系を使用し、リポジトリに依存追加は行っていない。各URLでMobileナビゲーションを測定。Desktop指定として実行した追加3件も、後日の設定点検により実際はMobile設定だったことが判明した（下記注記）。結果全文の主要指標・diagnosticsは `before-performance.json`。再実行用スクリプトは `scripts/audit-seo-performance.mjs`。

| ページ | 条件 | Performance | LCP | CLS | TBT |
| --- | --- | ---: | ---: | ---: | ---: |
| Home | Mobile | 98 | 1.53秒 | 0 | 0ms |
| Uni:Note Product | Mobile | 100 | 1.36秒 | 0 | 0ms |
| Uni:Note Guide | Mobile | 100 | 1.24秒 | 0 | 0ms |
| Home | 追加Mobile（旧ラベルDesktop） | 100 | 1.36秒 | 0 | 0ms |
| Uni:Note Product | 追加Mobile（旧ラベルDesktop） | 100 | 1.36秒 | 0 | 0ms |
| Uni:Note Guide | 追加Mobile（旧ラベルDesktop） | 100 | 1.05秒 | 0 | 0ms |

**測定条件の訂正：** 監査スクリプトがNode APIへ `preset: desktop` をflagとして渡したが、この引数はDesktop設定に変換されなかった。原本の `configSettings.formFactor` と `screenEmulation` を再点検し、6件とも412×823のMobile設定であることを確認した。変更前Desktopは未計測として扱い、前後比較には最初のMobile3件だけを使う。原本 `before-performance.json.gz` は改変せず保持し、スクリプトは公式desktop configをAPI第3引数へ渡す方式へ修正した。公開後は実際のformFactorをassertして測定している。

Accessibility / Best Practices / SEOは6件とも100。これはLighthouseが検査する範囲の結果であり、検索順位、Googleインデックス状況、structured dataの全意味検証を保証しない。

ラボ測定であり、実ユーザーのCrUXやINPは未計測。TBTをINPの実測値として扱わない。Homeはランダム選出・ネットワーク・ホスト負荷で値が変動する。

診断にはGitHub Pagesの10分キャッシュ、画像のさらなる縮小余地、最初のGuide画像のlazy loading等があるが、測定したLCP/CLS/TBTに重大な問題はない。SEO作業を理由にデザインや画像の構成を変更する必要はない。
