# KUMAKIKAI公式サイト 運用ガイド

**Webサイト保守の正本。** 入口はルートの [AGENTS.md](../AGENTS.md)。実装前に本書を読み、現在の情報設計・デザイン・URL互換性・SEOを維持する。通常のProduct追加・更新は現在のサイトへ情報を追加・更新する作業であり、サイトを再設計する作業ではない。

2026-09-07の実装を照合して記録。公開状況・OS・素材は更新の都度確認する。本書とコードに差がある場合は、ユーザーが意図した仕様変更か確認し、古い資料だけでコードを巻き戻さない。明示された設計変更は実装と本書を同時更新する。READMEは環境構築の入口、過去の監査レポートは当時の証拠として扱う。Web保守方針は本書を優先する。

**Product更新と記事作成は独立した作業。** 新規アプリ追加・リリース・大幅アップデートを含む通常のサイト更新では、Press Release／Information／Blogを自動作成しない。記事追加はユーザーが明示的に記事作成を依頼した場合のみ。以下の新規追加・既存更新・公開状態変更チェックリストに記事作成は含めない。

## 1. 短い指示を受けたら

1. `git status --short` とbranchを確認し、未コミット変更・並行作業を保護する。本書と対象アプリ側の作業規則を読む。
2. 下表から対象アプリを特定し、最新実装・実UI・提出／公開素材とWebの差分を調べる。サイト構成を毎回聞き直さない。
3. [既存更新](#existing-product)、[新規追加](#new-product)、[公開状態変更](#release-state) のチェックリストを選ぶ。
4. 対象の必要なデータ・本文・素材・SEOだけを更新する。通常更新でHome構成、Founder、他アプリのコピーを再生成しない。
5. production buildと検証を行う。公開を伴う依頼は、セッションの承認済み範囲でcommit/push → Actions／Pages → 本番再取得まで進める。「草案」「ローカルのみ」等の明示指示は優先する。

| 日本語名 | 固定 `id` / Product URLのslug | この環境の関連プロジェクト |
| --- | --- | --- |
| Uni:Note | `uni-note` | `/Users/yuya/Projects/uni_note` |
| オトミル | `oto-miru` | `/Users/yuya/Projects/oto_miru` |
| ギガポケ | `giga-poke` | `/Users/yuya/Projects/povo_manager` |
| Nocca | `nocca` | `/Users/yuya/Projects/Nocca` |
| Uni:Note Pocket | `uni-note-pocket` | `/Users/yuya/Projects/uni_memo` |
| ギャンカレ | `balance-calendar` | `/Users/yuya/Projects/gamble_pnl` |
| すわなび | `smokeless` | `/Users/yuya/Projects/smokeless` |
| SIGNAL | `signal` | `/Users/yuya/Projects/signal` |

上表は探索の開始点。移転・新規プロジェクトは実際の場所を確認する。Web更新のためにアプリ本体の仕様・リリース設定を勝手に変更しない。最初は読み取り監査とし、必要な画面撮影だけ開発環境で行う。

**情報の優先順位**は、現在のアプリ実装・実UI → 最新App Store提出／公開metadata → 最新プロジェクトdocs → 既存Web。機能がコードに存在すること、ローカルversion、TestFlight、審査提出は一般公開の証拠ではない。公開可否は現在のStore状態とユーザーの最新情報を別途確認する。正式名称・配信地域・URL・仕様が調査しても不明な場合だけ質問し、推測しない。

## 2. 情報設計・ナビゲーション

| ページ | 正式な役割・現在のURL |
| --- | --- |
| Home | 代表Productを知る。`/`。Hero → Featured → Productsリンク → News最新3件 → About紹介 |
| Products | 全アプリ唯一の総合ハブ。`/products/`。アイコン・名称・端末・説明・公開状況・「Product」「Support」 |
| Product | アプリを理解する。`/products/<id>/`。概要・特徴・画像・利用シーン・基本情報・Store・Support |
| Guide | 実画面で操作を説明。既存 `/htu/<id>/`。短いStepと操作画像 |
| FAQ | 困りごと・例外・よくある質問。既存 `/faq/<id>/`。操作はGuideの見出しへ |
| News | 発表・読み物・実務告知。`/news/`。旧 `/notes/<slug>/` と新 `/news/<slug>/` 記事を集約 |
| About | ブランド、Yuya Nakamura、開発領域、For Media、基本情報。表示名About、URLは **`/company/`** |
| Contact | 取材・掲載・その他問い合わせ。現在は **`/company/#contact`**。独立した `/contact/` を仮定しない |
| Privacy / Terms | 各アプリの既存本文URL。総合一覧を主要入口にしない |

Headerは **Products / News / About** と言語切替。Footerはブランド名、**Contact**、copyright、既存のApple商標表記。HeaderのサイトマップをFooterへ繰り返さず、通常追加で項目を増やさない。

**KUMAKIKAI公式サイトはライトテーマ固定。** 現在のライト配色を正式なブランドデザインとし、通常更新でDark modeやテーマ切替を再導入しない。OSの `prefers-color-scheme: dark` や旧theme保存値に反応してサイトを暗くしない。テーマ判定・保存・切替用の独自JS、Dark専用の独自CSSを追加しない。Hugoplate本体や依存を破壊的に変更する必要はない。実際のアプリにあるDark UI・スクリーンショットの配色はサイトのテーマ方針とは別で、画像を書き換えたりアプリ仕様を削除したりしない。

Productsカードの「Support」は **`/products/<id>/#support`**。対象が決まったらGuide／FAQ／Contact／Privacy／Termsへ直接進める。全アプリSupportで再選択させない。旧 `/support/` 等は互換用に残すがHeader・Footer・Homeから積極的に案内しない。

### UIラベルの言語方針

サイト構造を示すNavigation／Section Label／List CTAは英語を基本とする。日本語ページの一覧導線は **Products → / News →**、Aboutへの導線は **About →**。単一アプリの製品情報へのCTAは **Product**、同アプリのサポートへのCTAは **Support**。Contact、What we build、Press Release／Blog／Information／Allも既存の英語UI体系として使い、冗長な「すべて見る」「〜を見る」を付けない。

日本語ページの本文・説明・機能名・操作説明は自然な日本語を使用する。UI表記を理由に本文中の「アプリ」「プロダクト」「お問い合わせ」を英語化せず、「各Productページ」「下記のContact」のような不自然な混在も避ける。内容見出しの「使い方とサポート」「対応環境・基本情報」、Support行の「お問い合わせ」、What we buildの「学習／コミュニケーション／ユーティリティ」は日本語のまま。メール作成などの具体的な操作は「メールで問い合わせる」でよい。BreadcrumbはProducts等の階層名と「よくある質問」等の実際のページ名を区別する。

共通の一覧・About導線は `data/corporate/ja.json`、Home CTAは `data/home/ja.json`、Productカードは `data/ux/ja.json`、About内CTAとNewsフィルタは `data/company/ja.json` で管理する。対象をUI／Navigation／CTA／本文／内容見出しに分けて判断し、単純置換しない。aria-labelは日本語で目的を補足できるが、音声操作のため表示ラベルも含める。`detailsLabel`／`productViewLabel`／`appSupportLabel`は任意の読み上げ用文言で、未設定の言語は既存ラベルへfallbackする。他言語本文には日本語ページの変更を機械的に適用しない。URL・SEO metadata・アプリ内の正式用語・既存のライトデザインは維持する。

### Home Featured

- **Uni:Note先頭固定＋ほかの `featured: true` から重複なしのランダム3件**。現行候補は公開済みアプリと紹介可能な開発中Nocca。未公開候補にStore CTAを出さない。
- `layouts/home.html` が静的fallbackと候補 `template` を出力し、`select-products.html` / `assets/js/select-products.js` がページロード中に一度選ぶ。外部ライブラリ、Cookie、Geo-IP、自動カルーセルを追加しない。
- **表示順確定後**に `assets/css/site.css` がindex相当の `nth-of-type` で画像を **右→左→右→左** へ。固定先頭と別のランダムgroup内の奇数番目が全体2・4件目。Productデータに左右属性を持たせない。
- 901px以上は交互2カラム、900px以下は説明→CTA／地域／補足→画像の縦順。非公式表記等はテキスト側に残す。
- JS無効でもUni:Note＋静的候補で成立。主要本文・ProductsリンクをJS依存にせず、初期選出時のCLSを抑える既存構造を維持。
- **Other Appsを戻さない**。末尾の「Products →」1導線でProductsへ。

### Productの情報量・CTA

Homeは短い紹介、Productは何ができるか・誰向けか・条件まで説明する。Homeと同じ文章／同じ3枚＋Supportだけに戻さない。共通デザインの中でアプリごとに自然な機能数・画像・シーンを選び、巨大マニュアルや全アプリへの同一6カードの機械適用を避ける。

Heroはアイコン・正式名称・端末・キャッチコピー・短文・公式Storeバッジ・配信地域。上部へ「詳しく見る」「サポートを見る」「FAQ」「Privacy」を大量に並べない。長い説明後のStoreバッジ1回は可。Supportは下部。価格は固定値を増やさず公開済みだけ共通のApp Store確認文へ案内。

## 3. 実ファイルと編集責任

言語キーは **ja / en / ko / de / zh-hant / fr**。日本語Markdownはsuffixなし、他は `<basename>.<lang>.md`。日本語URLに `/ja/` は付かない。Product一覧は全言語共通の集合。Guide等の翻訳がなければ実在する日本語ページへ案内し、架空の翻訳URLを作らない。

| 実パス | 編集する内容 |
| --- | --- |
| `hugo.toml` | 正式baseURL、6言語、Hugoplate、Git lastmod、verification、Tailwind設定 |
| `data/apps.json` | アプリ共通属性・配列順・Store・画像・地域・Support。単一のアプリ集合 |
| `data/home/<lang>.json` | `apps.<id>` の正式名称・既存コピー・短文・端末・alt。Homeコピーもここ |
| `data/product_details/<id>.json` | 必須minimumOS、各言語の詳細紹介・素材・補足、任意Watch情報 |
| `data/product_ui/<lang>.json` | Product共通の見出し・基本情報ラベル・料金案内 |
| `data/support.json` / `data/ux/<lang>.json` | 共通Contact・EULA URL／Support行・地域UI等の文言 |
| `data/seo/<lang>.json` | `home` / `about` / `products.<id>` の固有title・description |
| `data/company/<lang>.json` | About・Founder・大分類・For Media・Contact文 |
| `data/corporate/<lang>.json` | nav、一覧・Heroの説明、共通CTA。`nav.company` はAbout |
| `data/news.json` | 既存記事のcategory・relatedProducts。新記事はfront matter優先 |
| `data/hero.json` / `data/app-store-badges.json` | Hero実UI画像／Apple公式バッジの出典・寸法・hash |
| `content/products/` | 生成Product入口。**直接編集しない** |
| `content/{support,news,company}/_index*.md` | 生成主要入口。**直接編集しない** |
| `content/_index*.md` | Home入口・実際の更新日。表示コピーはdata側 |
| `content/{htu,faq,privacy,terms}/` | アプリ固有の既存本文。URL・アンカー保護対象 |
| `content/notes/` / `content/news/` | 旧URLの本文／新しい編集記事 |
| `static/images/apps/<id>/` | 最適化済みProductアイコン・Store画像 |
| `assets/images/guides/<id>/` | 操作説明のcrop／画面素材。HugoがWebPへ処理 |
| `static/images/{hero,og,badges}/` | Hero・OGP・公式バッジ。OGPは通常buildでは再生成しない |
| `assets/images/company/yuya-nakamura.png` | 利用許可済み人物イラスト。名刺全体は掲載しない |
| `data/theme.json` / `scripts/themeGenerator.js` | ライト専用token定義・生成。Dark用tokenを再追加しない |
| `assets/css/{main,site}.css` | Hugoplate読込／共通Typography・レイアウト |
| `assets/css/{base,components,buttons}.css` | サイト側のライト専用スタイルでHugoplate同名CSSをoverride |
| `assets/js/site.js` / `assets/js/select-products.js` | ナビ・言語切替／Home・Aboutランダム選出 |
| `scripts/sync-products.py` | 共通JSONから入口同期。編集記事は上書きしない |
| `.github/workflows/deploy.yaml` | main push → build・検証 → gh-pages → Pages |

### 共通template / partial

| 実パス | 用途 |
| --- | --- |
| `layouts/baseof.html` / `layouts/_partials/essentials/{head,header,footer,style}.html` | 全ページshell、SEO head、ナビ、Footer、CSS |
| `layouts/home.html` | Home順序・固定Uni:Note・候補 |
| `layouts/_partials/{app-showcase,app-screenshots,app-cta,app-store-badge,hero-visual}.html` | Featuredコピー・画像・CTA・バッジ・Hero |
| `layouts/_partials/select-products.html` | ランダム処理の出力入口 |
| `layouts/products/list.html` / `layouts/_partials/app-card.html` | Products総合ハブ・カード |
| `layouts/product/single.html` / `layouts/_partials/product-details.html` | Product Hero・概要・特徴・画像・シーン・Support |
| `layouts/_partials/{product-facts,minimum-os,product-platform}.html` | 基本情報3行・OS改行・端末とWatch近日表示 |
| `layouts/_partials/{support-data,support-links}.html` | 共通URL解決・5項目行UI |
| `layouts/single.html` / `layouts/_partials/guide-toc.html` | Guide・FAQ・News等の本文・目次・末尾導線 |
| `layouts/_shortcodes/{guide-image,guide-anchor,watch-guide}.html` | 操作画像・旧アンカー・Watch操作の埋込 |
| `layouts/_partials/{watch-product,watch-guide}.html` | Watch製品紹介／Guide・公開前表示 |
| `layouts/news/list.html` / `layouts/_partials/{news-items,news-category}.html` | News一覧・分類 |
| `layouts/company/list.html` / `layouts/_partials/company-product.html` | About・カテゴリ内代表Product |
| `layouts/support/list.html` / `layouts/list.html` / `layouts/404.html` | 旧互換ハブ・一覧・404 |
| `layouts/_partials/seo/{indexable,language,alternates,schema,sitemap-url}.html` | index判定・hreflang・entity graph・sitemap要素 |
| `layouts/{sitemapindex,sitemap}.xml` / `layouts/robots.txt` | root全言語sitemap・既存言語sitemap・robots |
| `layouts/_partials/heading-text.html` / `data/heading_phrases.json` | 意味のまとまりを保つ見出し |

通常追加でテンプレートをアプリごとに複製しない。`themes/hugoplate/` は固定vendor runtime。内部改造やデモsetup/updateコマンド実行は通常保守に含めない。

## 4. Product metadataの契約

### data/apps.jsonの1要素

| フィールド | 意味・制約 |
| --- | --- |
| `id` | 一意の固定slug。正式Productは `/products/<id>/` として生成。表示名変更でidを変えない |
| 配列順 | Products一覧・静的fallback順。通常更新で既存アプリを並べ替えない |
| `featured` | Home候補か。常時表示・公開済みの意味ではない |
| `area` | learning / communication / utilities。About・schemaも使用 |
| `status` | **published / development の2種**。available / upcoming等を未対応のまま入れない |
| `appStoreURL` | 一般公開とリンク先を確認して登録。未公開には設定しない |
| `detailURL` | 旧Guide／紹介記事等の互換情報。**新ProductページのURLフィールドではない**。既存値を一括置換しない |
| `icon` | 実在するWeb配信用アイコンURL |
| `screenshots[]` | small / large / width / height / largeWidth / raw。実寸と一致。rawは実画面、falseはStore訴求素材。未入手なら不足を報告し、下記のstories参照・表示契約も確認 |
| `screenshotsStatus` | 任意review。提出中素材を公開版と区別。アプリ本体statusとは独立 |
| `operatingSystems` | schema用OS名配列（例iPadOS）。最低バージョンは別minimumOS |
| `availability` | 配信地域。表示言語でアプリを消さない |
| `support` | guideURL / faqURL / privacyURL / 任意termsURL / 任意contactURL。既存本文URL |

`availability.storefront` はPrimaryバッジの確認済み地域、`verifiedStorefronts` は確認した地域、`storefrontURLs` はその地域の実URL、`checkedAt` は確認日。`coverage: partial` は全世界確認済みを意味しない。未公開は `coverage: unreleased`、確認済み地域は空。任意 `plannedStorefronts` は配信済み国旗へ混ぜない。

地域UIは国旗・地域別リンク・国名aria-label/titleを小さく表示。言語で `/jp/` を置換してURLを作らない。Apple返却URL・HTTP証拠を `docs/ux/storefront-verification.json` と整合させる。新地域コードは `data/ux/<lang>.json.countries` に国名・flagを6言語追加する。公式バッジは `static/images/badges/` と `data/app-store-badges.json` を共用し、色・比率・内部文字・ロゴを加工しない。

### コピー・詳細・SEOの分離

- `data/home/<lang>.json.apps.<id>`: name、platform、description、任意taglineLines、imageAlts、任意note。imageAltsは共通screenshotsの順序・枚数と対応。taglineLinesがない場合、Home Featuredは既存 `product_details.locales.<lang>.overviewTitle` を参照、Product Heroはキャッチコピーを省略、Productsカードはdescriptionを表示する。全6言語を整合。
- `data/product_details/<id>.json`: 必須minimumOS、任意media・watch、locales。各言語は overviewTitle / overview / features / stories / audienceTitle / audience / notes。詳細な構造は既存ファイルに合わせ、機能・素材・利用条件を実装確認する。
- `data/seo/<lang>.json.products.<id>`: 固有title・description。表示コピーとSEO説明を個別HTMLへ重複定義しない。
- `npm run sync:products` が `content/products/<id>[.<lang>].md` の title / description / seo_title / type: product / product_idを生成。マーカー付き入口Markdownは直接編集しない。
- prebuildの `--check` はずれの検出だけ。同期後のMarkdownもコミットする。削除idの旧生成ページは自動削除せずURL保全が必要として失敗する。

素材不足時はscreenshotsを空配列にするだけで完成としない。詳細のstoriesがその画像indexを参照するとbuildが失敗し、現行検証は2〜3件の画像付きstoriesを要求する。最新実画面の取得を先に検討し、なお不足ならmedia・stories・featuredの扱いと検証契約を合わせて確認・報告する。ダミー画像や空の機能紹介を作って条件を埋めない。

### 対応環境・基本情報

全Product・全言語で **対応端末 → 対応OS → 公開状況**。「開発元」を追加しない。`product-facts.html` が同じdefinition list、notes箇条書き、公開済みだけ料金案内を生成する。

- 端末は本体ReleaseのTARGETED_DEVICE_FAMILY、最低OSは本体Release Deployment Targetと継承xcconfigから確認。テスト・Widget・Flutter AppFramework.plistやProject設定を、アプリターゲットの上書きより優先しない。互換動作だけでiPad/Mac対応を追加しない。
- minimumOSは必須。`iPadOS 17.0`、`iOS 26.0 / iPadOS 26.0` 等のOS名＋最低値。「以降」は共通翻訳で各OSへ付ける。未確認なら省略・推測せず確認。syncとHugoは欠落を検出するが、値の正しさは実装照合が必要。
- Uni:Noteは **iPad**。「iPad専用」に戻さない。
- watchはminimumOS・status・locales・素材等を別管理。review中は端末・OS・本文に近日対応を示し、一般公開後だけpublishedへ。iPhone単体最低OSとWatchペアリング互換性を同一視せず、互換性のあるペアリング済みiPhoneという補足を維持。
- ユーザー向け用語は実UIを正とする。Uni:Noteは **AI残量**（AI Balance / AI 잔액 / KI-Guthaben / Solde IA / AI 餘額）。内部のquota / credit / entitlementへ言い換えない。オトミルは設定名「高齢者向け」を使用し、Store訴求名を設定ラベルとして案内しない。
- notesはProduct固有の重要条件だけを共通箇条書きにする。変動する料金を増やさず、公開済みは「料金・App内課金の詳細はApp Storeをご確認ください。」を共通表示。

## 5. Product / Guide / FAQ / 法務の導線

`support-data.html` が共通Productデータを読み、`support-links.html` が **使い方 → よくある質問 → お問い合わせ → プライバシーポリシー → 利用規約** を同じtitle・description・divider・arrowで表示。Termsだけ小さなリンクにしない。

- Productは5項目、Guideは自分の使い方を省き4項目、FAQは自分のFAQを省く。再選択や不要な中間画面を作らない。
- termsURL未設定時だけ `data/support.json.standardEULAURL` の [Apple Standard EULA](https://www.apple.com/legal/internet-services/itunes/dev/stdeula/) へfallback。独自Terms URLを設定したのに本文がない場合はbuildエラー。黙って別規約へ切り替えない。
- contactURL未指定は `data/support.json.contactURL`。共通メールにアプリ名を件名として補う。会社全体ContactはAbout末尾。
- 外部リンクは現行の同じタブを維持。EULAは外部矢印・title・読み上げ補足。一部だけ新規タブにしない。
- 翻訳がなければ日本語実ページをその旨付きで案内。`layouts/single.html` はFile.ContentBaseNameでProductを特定するため、新Guide／FAQ等のbasenameはidに合わせる。既存例外URLは変更せず必要なら紐付け処理を限定対応。
- **現在の検証は全ProductにGuide／FAQ／Privacy実ページを要求する**。本当に不要なGuide／FAQはダミーを作らず理由を報告。必要性が判断された省略はUI・検証の該当契約だけを意図的に対応し、無条件に検証を外さない。
- アプリ別Privacy・Termsは統合せず、実データ処理・公開条件に合わせる。未公開機能を公開済みとして法務へ記載しない。
- 法務ページの汎用導線は末尾の共通「使い方とサポート」へまとめ、本文に同じ「関連ページ」一覧や単独のProductリンクを重ねない。法務上の説明に必要な参照先や問い合わせメールは本文に残す。NoccaのPrivacy／Termsはこの構成とし、フォームは共通欄の「お問い合わせ」から案内する。旧本文リンクを移す場合も、同一ページの共通欄に既存のリンク先が残ることを検証する。
- Product／Guide／FAQ末尾に同ProductのPress Releaseを重ねない。記事本文・URLは維持しNewsから案内する。

## 6. 最新画像・Guide・Simulator

Productは最新正式App Store提出／公開画像 → アプリ内fastlane / metadata / screenshots / marketing / docs / release素材 → 既存Webの順で探索する。提出中画像は状態を区別し、古い仕様・ダミーで補わない。

Guideは「見出し → 短い説明／Step → 実UI画像 → 必要な補足」。通常は対象部分をcrop、初期画面・完成状態・位置関係のみ全画面。画像で分かる操作を長文で繰り返さず、FAQは問題・例外へ分ける。

現画面がなければSimulator撮影は許可されている。最新ビルドを起動し、明らかなデモデータで正常状態へ操作。実ユーザー情報・連絡先・Debug表示・エラー・開発バナーを写さない。有料機能は既存StoreKit／開発テスト環境のみで、本番購入しない。撮影用コードが必要ならアプリ側規則を確認し、本体仕様を変えない。他作業中のSimulatorは終了せず、自分が起動・使用した端末だけ撮影後に終了する。

```go-html-template
{{< guide-image src="images/guides/<id>/add-item.png"
    alt="記録画面右上の追加ボタン" mode="crop" >}}
```

書式例のパスは実ファイルへ置換する。modeは **crop / screen / tablet**。最大表示幅560 / 320 / 760px、HugoでWebP q92・1x/2x srcset・width/height・lazy・decoding・拡大リンクを生成し、元画像以上に拡大しない。**cropモード自体は切り抜かない**ので、入力素材を適切にcropして用意する。

- 内容が分かるファイル名・alt、必要なcaptionを付ける。UIを書き換えず、補助枠・矢印は必要時だけ。
- 原本は可能ならアプリ側。サイトrepoは制作・再生成に必要なcrop素材とWeb成果物だけ。raw動画、大量原寸PNG、一時撮影物を蓄積しない。
- Home Heroのオトミルとギガポケは同じiPhone縦横比で表示する。Dynamic Islandを含む採用済み素材を使い、全画面の原本から等比で書き出す。宣伝画像の下端で切れた端末を全画面として扱わず、CSSで画面を縦に引き伸ばさない。現在の共通書き出し寸法は320×693／640×1386。
- 取得元・版・hash・crop範囲・実装の照合を `docs/visual-guides/` 等へ記録。未使用画像は全参照確認後にだけ整理。
- Guide見出し変更時は `{{< guide-anchor "旧ID" >}}` で対応箇所へ旧アンカーを残す。URLと実際のlastmodを維持。
- 既存Guide／FAQ改訂は **本文・素材監査 → npm run buildで最新public生成 → scripts/record-guide-review.py → 対象entryのsource／rendered hashと理由の差分確認 → npm run verify** の順。同scriptはpublicを読むため、古いHTMLで記録しない。`docs/visual-guides/reviewed-content.json` は既存対象一括処理・監査ファイル固定表に基づくので、対象以外のhashが変わっていないか読む。新ページは旧本文baseline対象ではなく、無条件にmanifestへ足さない。通すためだけにhashを更新しない。
- Nocca法務は `docs/legal/README.md` / `scripts/nocca_legal_review.py` / `docs/legal/reviewed-nocca-content.json` の限定保護も確認。Guide改訂と法務変更を混同しない。

## 7. News / About / 文章

### News（明示的な記事作成依頼がある場合のみ）

「プレスリリースを作って」「正式発表の記事を書いて」「お知らせを書いて」「この内容でブログを書きたい」等の依頼がある場合にだけ記事を追加する。「新しいアプリをHPに追加して」「リリースしたのでサイトも更新して」「アプリを更新したのでHPも合わせて」は記事作成の指示ではない。Informationも通常更新に付随して作らず、BlogもProductリリースとは独立して扱う。

実際に発信したい内容がある場合だけ作成し、更新しているように見せるための記事、分類を埋める記事、SEO用の薄い記事を生成しない。既存Press Releaseの本文・URLはこの運用変更では編集・削除・移動しない。Newsからの既存導線も維持する。

以下およびREADME・SEO運用メモのNews追加手順は、明示的な記事作成依頼がある場合だけ適用する。新規は `content/news/YYYY-MM-DD-slug.md`、既存は `content/notes/` のまま。HTMLを編集せずMarkdownだけで追加する。下例は明示依頼されたProduct紹介Press Releaseの例であり、Support URLを用意するためには作成しない。値・日付・idは実際のものへ置換。

```yaml
---
title: "正式アプリ名について"
description: "実際に発表する用途・内容を説明する固有の文。"
date: 2026-09-07T10:00:00+09:00
lastmod: 2026-09-07T10:00:00+09:00
news_category: "press-release"
related_products: ["対象の既存id"]
draft: true
---
```

news_categoryは **press-release / blog / information**、UIは **Press Release / Blog / Information**。明示依頼された正式Product紹介Press Releaseは「正式アプリ名＋について」。開発・運営の読み物はBlog、利用者への実務告知はInformation。未分類は実装上informationへfallbackするため必ず明示する。

旧記事は `data/news.json` のcategory / relatedProductsで補助、新記事のfront matterが優先。related_productsは実際に扱うアプリのみ指定し、Press Release → Productの静的リンクを保つ。全Blogに全Productを自動列挙しない。公開時は本文・日付・draftを確認（未来日は通常build対象外）。翻訳は同basenameのsuffix。現行Newsは日本語記事を他言語一覧にも日本語と明示して案内する。

カテゴリは `/news/#press-release` / `#blog` / `#information` / `#all-news`。CSSで同じ一覧を絞り込み、重複カテゴリページ・追加JSを作らない。初期「All」でempty stateを出さず、本当に0件のカテゴリ選択時だけ表示。

### About・Founder

KUMAKIKAIは **Yuya Nakamuraが個人事業として運営するアプリ開発ブランド**。法人・架空の社員やオフィス・数値実績を作らない。表示名About・URL `/company/` を維持。Founderは **Yuya Nakamura** のみ、**Software Engineer / App Developer**、組み込み／業務／モバイル経験と `C / C++ / C# / Java / Python / Dart / Swift` を維持。勤務先・経験年数・学歴を推測しない。

**Home／AboutのKUMAKIKAI紹介文では、特定Productを代表例として恣意的に列挙しない。** About冒頭は運営者・個人事業・アプリ開発ブランドであること、Home下部は運営者とブランドの関係を簡潔に伝える。具体的なProduct紹介はProductsおよびWhat we buildへ任せ、ブランド紹介の本文へ一部アプリの名称や固有機能を戻さない。編集元は `data/company/<lang>.json.about` と `data/home/<lang>.json.aboutText`。Home／AboutのSEO descriptionでも特定Productを恣意的に列挙しない。既存のProduct紹介・カテゴリ内代表Product・静的クロール導線は維持する。

`data/company/ja.json.founderBio` は複数領域のソフトウェア開発経験と、自分の不便や身近な人の困りごとから必要なものを作る、という本人のスタンス。ブランド全体の事業説明を再度加えない。通常Product更新で再生成せず、特定アプリだけの小話を追加しない。使用許可済み人物イラストは維持可。漢字氏名・電話番号・名刺全体を追加しない。

基本情報は **名称／開発者／事業形態（個人事業）／事業内容／適格請求書発行事業者（登録済み）**。登録確認は国税庁公表サイトの本人情報へリンクし、番号・税務上の屋号・漢字氏名・住所等を転載しない。紹介文・ラベルは `data/company/<lang>.json`、確認リンクは `layouts/company/list.html` で管理する。Web欄・メール欄を戻さず末尾Contact CTAへ集約。For MediaはPress Release一覧と同ページ#contactへ。アプリSupportと一般問い合わせを混同しない。

What we buildは **学習（learning）／コミュニケーション（communication）／ユーティリティ（utilities）**。カテゴリそのものを短く説明し、PDF・字幕・特典コード・期限等の個別機能に細分化しない。

- learning＝Uni:Note／Pocket、communication＝オトミル／Nocca、utilities＝ギガポケ／ギャンカレ／すわなび／SIGNAL。
- areas[].areaごとにdata/apps.json.areaからランダム1件。Homeのfeaturedとは独立し、statusで除外しない現仕様を維持。
- areas[].productはJS無効時fallback。**同じarea内の実在idが必須**。1候補なら固定、他領域から補充しない。
- 同areaの新Product追加だけならAbout本文変更不要。自然に入らない場合だけ新分類を検討する。
- 本文の固定アプリ数は禁止。代表ProductとProducts一覧の静的リンクを維持する。

### コピー・Typography

**KUMAKIKAI全体の事業説明はHome Heroを主な説明箇所とする。** 「iPhone・iPad向けのアプリを企画・開発・運営しています。」はHome Hero（`data/corporate/<lang>.json.heroLead`）で維持し、各セクションで同じ説明を繰り返さない。単語だけを変えた「App Storeで公開・運営」「iPhone・iPadアプリを開発」等も同じ意味なら追加しない。各ページはそのページ固有の情報を伝える。

Home Aboutは運営者とブランド、About冒頭はブランド・個人事業、Founderは経験・開発スタイル、Productsは実際のアプリ、Contactは問い合わせ方法を伝える。About Heroと記事末尾には事業説明の定型段落を置かず、空の段落や代わりの抽象コピーも作らない。About基本情報の事業内容は事実確認用の項目として維持する。SEO用meta description／structured dataは画面上の反復と区別し、検索エンジンへの事業説明を維持できる。多言語も同じ役割分担とし、既存の翻訳・アプリ固有の説明・記事本文を機械的に書き換えない。

具体的な機能・用途・条件を書く。会社名を他社へ置換しても成立し、固有情報がない説明は削除・具体化。「ユーザーに寄り添う」「より良い体験」「革新的」「シームレス」等を雰囲気のために足さない。Hero・採用済みキャッチコピーは役割が違うため通常更新で再創作しない。日本語本文は「各プロダクトページ」等自然な表記にする。

既存の幅・余白・フォント・コントラスト・CTA階層を使う。日本語組版は `scripts/format-japanese.mjs` が **build時** にBudouXとIntl.Segmenterでwbrを挿入し、共通 `.jp-text` と合わせて語中分割を抑える。`verify-japanese.mjs` が本文・URL・metadata保存を確認。手動br・画像内文字・個別CSSで帳尻合わせしない。コピーとして意図した改行のみ許容。Hugo dev serverだけではpostbuild組版がないため最終確認はproduction出力で行う。

## 8. 恒久URL・SEO

**通常更新で既存公開URLを変更しない。** Support、Marketing、Privacy、Press Release、Guide、FAQ、Terms、Contact、翻訳URL・アンカーを保護。App Store Connectで利用の可能性がある本文は同URLの正式ページとして維持しredirectへ置換しない。

基準は `docs/migration/baseline.json` と `docs/migration/permanent-urls.json` / `permanent-urls.md`。旧正式本文と過去aliasを区別し、検証を通すためにbaselineを作り直さない。既存alias維持は新たな本文移動の推奨ではない。明示的な移行時だけ影響を調べ、HugoのHTML aliasがHTTP 301そのものではない点を区別。JS redirect、404経由、一括slug変更を避ける。

旧support / privacy / htu / faq / terms / notes集約、旧pagination、空taxonomy、404は検索対象外。互換用ページのHTTP・リンク・自己canonicalを保ち、robotsでクロールを拒否せずnoindex, followで整理。アプリ固有本文・Privacy・Terms・正式紹介記事を一緒にnoindexにしない。既存Supportのアプリ別fragmentも維持。

### App Store Connect Support URL

新規アプリのSupport URLは原則として、そのアプリの正式Product詳細ページ **`https://kumakikai.github.io/products/<id>/`** を使用する。例: `https://kumakikai.github.io/products/uni-note/`。Product概要・機能・対応環境と、使い方／FAQ／お問い合わせ／Privacy／Termsへの直接導線を備える正式入口として扱う。Support URLのために「アプリ名について」の記事を作成しない。

App Store Connect登録用はProductページ自体の正式URL。サイト内カードから同ページ下部へ進む `/products/<id>/#support` とは用途を分ける。旧互換情報の `data/apps.json.detailURL` を新規登録先として機械的に採用しない。

既存アプリがPress Release URLをSupport URLとして登録していても、Web更新の都合だけでは変更しない。次回、そのアプリのApp Store Connectメタデータを更新する機会に、必要に応じて正式Product URLへの変更を検討する。通常のHP更新だけでApp Store Connect設定まで変更しない。登録先を変更した後も、既存Press Releaseの本文・旧URLは外部参照・検索・過去コンテンツの互換性のため維持し、HTTP成功を確認する。

### SEO更新

- Product名で検索する人向けの正式ランディングページは **`/products/<id>/`**。固有metadata・schema・静的リンクを中心に整備し、Press Releaseを作らない代わりの検索用記事を追加しない。
- titleは正式Product名＋KUMAKIKAI等の固有値、descriptionは用途。Product H1には正式名をHTMLで含める。KUMAKIKAI／Yuya Nakamura表記を統一。
- Home・About・Productは `data/seo/<lang>.json`、記事はfront matter。Heroや本文へ検索語を詰め込まず、別表記は確認できる必要な範囲だけ。
- canonicalは正式 `https://kumakikai.github.io/` の各ページ自身。翻訳を日本語へ統合せずlocalhost／previewを出さない。
- `seo/alternates.html` は実在・index可能な翻訳間のみ相互hreflang、日本語があればx-default。言語正規化は `seo/language.html` の ja / en / ko / de / zh-Hant / frに従う。
- OGP／Twitter Card／og:site_nameを維持。ページimages指定・該当Product OGP・共通画像のfallbackを確認。`scripts/generate-og.mjs <id>` で対象だけ再生成できる（既存sharp QA環境使用）。無指定は全画像と共通OGPを再生成するので通常更新では使わない。共通OGPは固定配置のためアプリ増加時に無条件再生成しない。
- root **`/sitemap.xml`** は `sitemapindex.xml` から全言語index対象を列挙するurlsetを生成。Home／Products／Product／About／News記事／Guide／FAQ／個別Privacy／Termsを確認。既存言語sitemapも維持。
- robotsは通常検索を許可しroot sitemapを示す。明示noindex: trueと `seo/indexable.html` がrobots meta・sitemap・hreflang・schemaの対象を揃える。
- lastmodは **lastmod → modified → Git → date → publishdate**。実質更新ページのみ記録。全ページへbuild日を入れずCIのfetch-depth: 0を維持。dataだけの変更は生成入口・Git日付の反映範囲を確認し、生成Markdownへ消えるlastmodを手入力しない。Home実質更新は `content/_index*.md` も確認。
- 静的リンクはHome → Products / About / News、Products → 全Product、Product → 固有Support、Press Release → Product、About → Products。ランダムで選ばれないアプリもクロール可能。逆向きProduct → 同内容Press Releaseは追加しない。

### 構造化データ

`seo/schema.html` の共通entityを維持する。

| Entity | ID・関係 |
| --- | --- |
| Brand | `https://kumakikai.github.io/#brand`、KUMAKIKAI |
| Person | `https://kumakikai.github.io/company/#person`、Yuya Nakamura、brandでBrand参照 |
| WebSite | `https://kumakikai.github.io/#website`、publisherはPerson、aboutはBrand |
| SoftwareApplication | `/products/<id>/#software`。creator／publisherは同じPerson。名称・説明・画像・OS・area由来category |
| Article / BlogPosting | Press Release等はArticle、BlogはBlogPosting。実date／lastmod・Person著者・関連Productのみmentions |
| WebPage / AboutPage / BreadcrumbList | 各正式URLと可視のページ階層に一致 |

Corporation扱いをせず、Brandを型の異なるcreator/publisherへ直接代入しない。価格・aggregateRating・review・award・架空sameAsを追加しない。未公開ProductはdownloadUrlなし、Watchはwatch.status: publishedになって初めてwatchOSをschemaへ加える。Rich Result適格性や検索順位を保証しない。

Search Consoleは2026-09-07時点の回答では未登録。今後は接続状態を確認する。`hugo.toml` のparams.verification.google / bingに発行済みcontent値だけを設定できる。未登録はサイト更新のブロッカーにせずtokenを生成しない。登録・sitemap送信・優先URLは [SEO運用メモ](seo/OPERATIONS.md)。通常更新ごとにindex requestせず、新規重要Product等で必要性を判断。反映待ちでURL・titleを毎日変えない。

<a id="new-product"></a>

## 9. 新規Product追加チェックリスト

- [ ] 最新プロジェクト・実UI・正式名称・既存URLを確認し作業ツリーを保護。
- [ ] 本体Releaseの端末・最低OS、一般公開、Store URL・実配信地域を確認。未公開は区別。
- [ ] data/apps.jsonへ固定id・順序・icon・status・operatingSystems・availability・supportを追加。
- [ ] 既存3分類からareaを選び、紹介可能ならfeatured: true。Home／About候補への反映を確認。
- [ ] 全6言語homeへ名称・端末・短文・alt。product_detailsへ必須minimumOS、具体的概要・特徴・画像・シーン・補足。
- [ ] 最新正式Store素材を最適化。必要なGuide実画面を取得／crop。寸法・alt・srcset・lazy・出典確認。
- [ ] 実装に即したGuide／FAQ、実態に即したPrivacy、必要な独自Termsを作成。未設定Termsは共通EULA。Contactは確認済み先。
- [ ] 下部の共通Support5種類を確認。不要なGuide／FAQはダミーを作らず必要性と検証契約を判断。
- [ ] 正式Product詳細ページを確認し、新規App Store Connect Support URLの登録先として案内する。概要・機能・対応環境と固有Supportへの到達を確認。
- [ ] 全6言語SEOへ固有title・description、Product OGPまたはfallbackを確認。
- [ ] npm run sync:products後の生成Markdownを確認。Products静的リンク、H1、schema、canonical、hreflang、sitemap。
- [ ] 新idの素材・地域証拠を登録。固定アプリ集合に依存するQA期待値を根拠付き拡張。baselineは緩めない。
- [ ] production build、既存URL・Support・基本情報・SEO・画像検証。
- [ ] Desktop／Tablet／Mobileでライト表示・keyboardを確認。OSのダーク設定や旧theme保存値でもライト固定。Home10回reload＋全候補両側、Aboutカテゴリを確認。
- [ ] 対象差分だけcommit/push。Actions／Pages後、Product・Products・Home等と画像を本番再取得。

<a id="existing-product"></a>

## 10. 既存Product更新チェックリスト

- [ ] 最新実装・実UI・提出／公開metadataとWeb差分を特定。削除機能・新機能・課金条件・設定名。
- [ ] 変更仕様のproduct_detailsと必要なHome短文だけ更新。既存キャッチコピー再創作・他Product変更をしない。
- [ ] 最新正式素材へ必要箇所を置換。詳細stories・共通screenshots・alt・使用するHero／OGPを照合。
- [ ] Guideは現操作と実画面へ、FAQは問題・例外へ。旧アンカー・本文URL・実lastmod・監査記録を保護。
- [ ] platform／minimumOS／status／地域／Store URLの変更有無を確認。変更がなければ触らない。
- [ ] Product／Guide／FAQのSupportとTerms fallbackが同一データを参照することを確認。
- [ ] SEO description、schema OS・画像・downloadUrl、静的リンクを整合。削除機能をmetadataにも残さない。
- [ ] 全言語の関連コピー・alt・公開前表示を確認。未翻訳を別言語の内容として誤表示しない。
- [ ] 必要なsync、production build、リンク・画像・基本情報・SEO、対象と表示先の実ブラウザ確認。
- [ ] 公開後、変更ページと必要なHome候補を本番再取得。変更対象・根拠・未確認を短く報告。

<a id="release-state"></a>

## 11. 審査中から公開へのチェックリスト

- [ ] 対象バージョン・地域の一般公開を確認。公開連絡とStore情報を照合し、手動公開待ち／TestFlightと区別。
- [ ] アプリ本体はdata/apps.json.status、Watchはproduct_detailsのwatch.statusを更新。未知statusは表示・CTA・schema・検証を同時対応。
- [ ] Store URL・availability・国別HTTP証拠・checkedAtを整合。更新なら既存Store IDを保つ。
- [ ] 公開機能の近日／審査中表示を全言語から外す。screenshotsStatusも公開素材一致後だけ解除。
- [ ] platform・minimumOS・Home／Product・画像・Guide／FAQ・必要な法務を確認。
- [ ] Watchは端末表示・OS行・feature・Guide notice・schema watchOSを一括確認。ペアリング条件は残す。
- [ ] SEO、バッジ、国旗、sitemap、更新日、検証のreview前提を意図した範囲で更新。
- [ ] build → 対象画面 → commit/push → Actions／Pages → 本番。

## 12. build・検証・公開

環境の正本は `.hugo-version`（現在Extended 0.158.0）、`.node-version` / `package.json`（Node 22.22.0）、`package-lock.json`。Python 3使用。[README](../README.md)の環境手順を参照し、npmを維持する。

```sh
npm ci
# 共通dataから生成入口の同期が必要な場合
npm run sync:products
npm run build
cp app-ads.txt public/app-ads.txt
python3 scripts/test_nocca_legal_review.py
npm run verify
python3 scripts/test_product_basics.py --build public
npm run verify:seo
```

依存がlockfileと一致済みならnpm ciの繰り返しは不要。HUGO_BINARYで固定実行ファイル、必要ならHUGO_CACHEDIRでcacheを指定可能。**Hugo単体だけで公開しない**。npm run buildはcleanDestinationDir、同期検査、theme生成、日本語組版と検証を含む。dev serverだけで完了にせず、publicを手修正しない。

| 対象 | 実行・確認 |
| --- | --- |
| 全変更 | production build、warnings、git diff --check、npm run verify、npm run verify:seo |
| 基本情報・Support | test_product_basics.py、verify-support.cjs。3行・5項目・status・EULA |
| Home候補・画像・platform | verify-featured-layout.cjs、必要ならverify-selection.cjs。10回reload・全候補両側・固定先頭・no-JS |
| Aboutカテゴリ | verify-company.cjs / verify-selection.cjs。同area限定・fallback・静的導線 |
| Guide／FAQ | verify-guides.cjs、audit-guide-assets.py。実読・crop・alt・画像404・アンカー |
| 共通Typography | verify-site-typography.cjs等を現条件に合わせ使用。全主要ページを実読 |
| SEO | verify-seo.py。初期HTML・schema構文・H1・メタ・canonical・hreflang・sitemap・リンク |
| 全公開・混在疑い | audit-release-http.py、必要ならaudit-release-browser.cjs。全HTML・リソース・現在shell |

上表のscriptはすべて `scripts/` 配下。ブラウザはproduction出力をHTTP配信し、既存QA環境のPlaywright／axe-coreを使用。サイトbuild依存へ追加しない。

```sh
python3 -m http.server 1314 --directory public --bind 127.0.0.1
# 別ターミナル。QA依存・Chromeの場所は実環境に合わせる
TEST_BASE_URL=http://127.0.0.1:1314 NODE_PATH=/path/to/qa/node_modules node scripts/verify-browser.cjs
```

各script冒頭の対応環境変数を読む。CHROME_PATH、一部のTEST_ENGINE=webkit、GuideのTEST_APP / TEST_LOCALES / TEST_WIDTHS等を使用可能。previewの既定1313と多くのQAの既定1314を混同しない。TEST_REPORT等で新しい保存先を指定し、対応しない変数を推測しない。保存先固定scriptは生成差分を読み、過去証跡を無自覚に上書きしない。

基本幅は **1440 / 1280 / 1024 / 768 / 430 / 390 / 375px**。Home変更時は901/900px境界も確認。共通CSS変更は全主要ページ、データ限定変更は対象と表示先へ範囲を合わせる。語中分割、末尾1〜2文字落ち、助詞・句読点、PCの細すぎる本文、MobileのCTA・国旗・画像・Supportを実読し、overflowだけで日本語PASSにしない。OSのlight／dark両設定と旧theme保存値がある状態でも、サイトが同じライト表示になることを確認。テーマ切替UIを出さず、focus、menu Escape・背景スクロールも影響範囲で確認する。

画像が増えた場合はLCP・CLS・総容量・実操作を確認し、必要ならaudit-seo-performance.mjsでLighthouse測定。Hero主要画像だけeager／fetchpriorityを検討し他はlazy。ラボTBT等を実ユーザーINPと呼ばず、Search Console field dataは得られる場合に確認する。

### 保護対象とテスト期待値

verify-migration.pyはdataから新Productを検査する一方、既存アプリの相対順・area・コピーを保護する。verify-selection.cjsは当時のarea別候補が固定、Home候補もfeatured filterなしの前提がある。新規・featured・カテゴリ変更では実際の意図へ期待値を拡張。verify-browser.cjsのルート一覧、verify-featured-layout.cjsの固定seedと両側coverageも確認する。検証削除・baseline再生成で通さない。

古いverify-home.py / verify-home-browser.cjsは旧固定Featured／Other構成用で、現行CIゲートへ復活させない。現在のworkflowと本書を基準にする。Guide本文hash、地域証拠、Nocca法務等は対象改訂の根拠付きで更新。失敗を「旧テスト」と決めつけず保護内容を読む。test_product_basics.pyのWatch近日負例は公開後自動skipするため、過去の件数17を恒久要件にしない。

### GitHub Pages・本番確認

`.github/workflows/deploy.yaml`: main push → 全履歴checkout → 固定Hugo／Node → npm ci → build → app-adsコピー → 法務・URL・基本情報・SEO検証 → gh-pages。続くPages公開ジョブも確認。

1. 対象差分だけstage・commit/push。.DS_Store、public、resources、node_modules、cache、raw動画、一時撮影物を含めない。
2. 該当ソースcommitのActionsとPages成功を確認。mainが進んだだけでは完了ではない。
3. origin/gh-pages成果物と同じcommitのローカルHTMLを比較。Git lastmodが影響する場合はcommit後に再build。Mac／CIの画像圧縮差はCI公開成果物を基準にする。
4. 変更ページ・関連Products／Home・新画像・SEOの影響範囲を本番再取得。全体監査は下記を使用。

```sh
python3 scripts/verify-live.py --build public --output artifacts/current-update/live.json
# 公開成果物を取得済みの場合の全ファイル・cache条件比較
python3 scripts/audit-release-http.py --build /path/to/deployed-artifact --output artifacts/current-update/release-http.json
```

macOSでCA参照が必要ならSSL_CERT_FILE=/etc/ssl/cert.pemを指定し、TLS検証を無効化しない。例のパスは実フォルダへ置換。本番差異はsource SHA → Actions対象SHA → Pages → gh-pages → public鮮度 → HTTP本文／CSS fingerprint → browser/CDN cacheの順で調べる。旧public継ぎ足し・旧テーマ出力の公開をしない。第三者検索キャッシュと実HTTPの古さを区別する。

## 13. ドキュメントと変更範囲

- 本書: Navigation、Home、Product、Support、News、About、SEO、metadata、URL方針の意図的変更時に同時更新。細かなアプリ仕様や一時statusを全部複写し続けない。
- AGENTS.md: 絶対ルール・詳細ガイドの場所が変わった場合だけ更新。全仕様・監査ログを詰め込まない。
- README: build・development・deploy手順が変わった場合に更新。通常Product更新で無関係な編集を増やさず、詳細方針は本書へ。
- 証拠: 素材出典・確認日・公開版・テスト・本番結果を対象別に簡潔に記録。過去証跡を上書きしない。大きな完了結果はscripts/archive-verification.pyで要約＋圧縮可能。

通常保守で行わないこと: テーマ・Framework・URL全面移行、Header増設、Footer再設計、CMS／Analytics新設、AI生成Product UI、架空レビュー・ユーザー数・実績。明示的な設計変更依頼なら影響確認 → 実装 → 本書更新 → 検証まで対応する。現在のスタイル維持自体が要件。

## 14. 短い指示の自己レビュー

| 指示 | 本書から決まる作業 | 完了確認 |
| --- | --- | --- |
| Nocca更新したからHPも更新して | Projects/Nocca、nocca共通data・詳細・該当Guide／FAQ／法務・画像・6言語SEOを差分更新。公開は別確認 | 機能・status・固有Support、旧 `/notes/2026-09-06-nocca/` 等のURL、build・本番 |
| 新しいアプリを作ったのでサイトに追加して | 新規チェックリストでid・6言語data・Product・実画面・Support・Store地域・area・SEOを追加しsync | Products静的掲載、Home／About候補、必要な実ページ、status、sitemap・本番 |
| すわなびのWatch版が公開された | 公開版照合後、smokelessのwatch.status・素材状態・Watch Product／Guide／OS・schemaを関連更新 | 審査中表示の残り、iOSペアリング条件、公開版との画像差。iPhone版Store IDは維持 |
| Uni:Noteのスクショ変えたからHPも変えて | 最新正式素材を特定し、共通screenshots・詳細stories・alt、使用するHero／OGPを照合。Guideは操作画面変更時だけ | 最新素材、表示先、寸法・容量・alt、Featured、不要な本文変更なし、build・本番 |
| 新アプリについてプレスリリースも作って | 明示された記事作成としてNews手順を適用し、依頼内容・正式Productへのリンク・分類・記事SEOを確認 | 既存記事・URLの維持、依頼された記事だけを追加、build・本番 |

最初の4例ではPress Release／Information／Blogを作らない。新規アプリのSupport URLは正式Product詳細ページとし、既存アプリの登録URLと過去記事は維持する。最後の例は明示依頼があるため記事を作成できる。いずれも対象data・テンプレート・検証・公開確認を特定できる。未確認の新アプリ名・配信国等だけは調査後に確認する。短い指示で完結することは、未確認事実を作ることではない。

通常報告は **更新内容（Product／画像／Guide・FAQ／Support／SEO）→ 確認（build／リンク／Desktop・Mobile／本番）→ 未対応があれば理由**。全項目の長大な再掲や検索順位保証は不要。
