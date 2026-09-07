# アンカー・リンクラベル意味監査（変更前）

根拠は `/private/tmp/kumakikai-final-audit/before/scan/anchor-label-semantics.json` と現在のローカルHTML/テンプレート/Markdown。公開ページ、検索結果、ChatGPTの取得キャッシュは使用していない。サイトは未編集。

## 対象と結論

- JSONの全4,764リンク行を対象。発信元220ページ。同じ表示ラベル＋完全遷移URLの再利用をまとめると1,257組。これはこのJSONの件数であり、サイト全体のページ数や外部リンク込み総数ではない。
- fragmentあり887リンク、ラベル＋完全URL631組、アンカー付き遷移先458 URL。fragmentなし3,877リンクもページの役割・製品・言語・記事タイトルを確認。
- **誤った内容の節へ遷移する確定不一致は0件。** ただし、Smokeless FAQの具体的な回答からGuide先頭へ繰り返し遷移する13件は改善を推奨。
- `/products/<id>/` と `/products/<id>/#support` は、製品紹介とサポート欄という別目的。URL比較でもfragmentを保持し、この2種類を重複として修正する提案はしない。
- 文字列一致のみを判定根拠にしていない。Guide節の本文、本文周辺の質問、UI役割を確認し、同じ生成規則・同じラベル/URLの再利用はまとめて照合した。

## アンカーあり887リンクの全分類

| パターン | 件数 | 意味の確認 |
| --- | ---: | --- |
| 本文へスキップ #main-content | 210 | 当該ページのmain要素。本文開始へ移動。 |
| Contact #contact | 216 | Footer210件＋About CTA6件。企業/ブランド問い合わせ欄へ。 |
| Product Support #support | 165 | 当該製品の5項目共通Support欄。製品先頭とは別目的。 |
| Newsカテゴリ | 36 | Newsフィルタ24件＋AboutからBlog/Press Release12件。categoryに一致。 |
| Guide目次 | 162 | 各表示ラベルが実アンカーの見出しテキストと全件一致。 |
| FAQ・Guide本文の個別参照 | 98 | 対象の設定、登録、録音、復習、バックアップ、Watch等の節と回答文脈が一致。 |

## 全4,764リンクのコンテキスト別確認

| コンテキスト | 件数 | 確認内容 |
| --- | ---: | --- |
| document | 220 | 本文スキップ210件は当該ページのmain-contentへ。旧ページのHome案内10件は同言語Homeへ。 |
| site-header | 210 | ブランド名から同言語Homeへ。Heroのh1がブランド名と異なることは不一致ではない。 |
| desktop-nav | 630 | Products/News/Aboutが同言語/products/、/news/、/company/へ。 |
| language-menu | 1260 | 6言語の表示名と遷移先言語が全1,260件一致。翻訳なしは該当言語Homeへfallbackする現行仕様。 |
| mobile-menu | 630 | Desktopと同じ3役割。非同時表示のメニュー再掲を誤遷移扱いしない。 |
| app-actions | 72 | 404のHome/Products、Home各アプリの詳細、AboutのPress Release/Contactを各目的先へ。 |
| site-footer | 420 | ブランド名→Home、Contact→About末尾#contact。 |
| company-page | 12 | 開発/運営記事→News #blog、全アプリ→Products。 |
| company-area-products | 48 | 各カードの製品名が遷移先製品h1を含み、同じ製品詳細へ。 |
| main | 467 | TOC162件が実見出しと全文一致。製品カードProduct/Support、News記事タイトル、互換ハブ/記事ページャーも役割一致。 |
| breadcrumbs | 132 | Products階層→Products一覧、News階層→News、製品Support配下記事→当該製品#support。 |
| post-content | 135 | 135件/128組。個別アンカー98件のFAQ回答/Guide内参照は対象節と整合。Smokeless先頭13件は下記改善対象。 |
| support-resources | 312 | Guide/FAQ/Privacy/Terms312件は記事と同じ製品ID。本文の言語か「日本語」fallback注記と実URLが一致。 |
| article-related | 87 | 製品名から当該製品先頭へ。Supportパンくず#supportと別目的のリンク。 |
| home-hero | 6 | 全アプリを知るCTA→Products一覧。 |
| portfolio-featured | 6 | 全製品CTA→Products一覧。 |
| home-news | 24 | News一覧CTAと直近記事3件のタイトルが各遷移先に一致。 |
| home-about | 6 | ブランド紹介→About。 |
| news-filters | 24 | 4分類×6言語。href/target/実際のCSS絞込categoryが一致。 |
| product-page | 48 | 製品末尾の全製品CTA→Products一覧。 |
| article-about | 15 | 記事末尾About→About。 |

## 改善推奨 A1: Smokeless FAQの具体的な質問をGuideの対応節へ

日本語 `content/faq/smokeless.md:18,25`、英語・フランス語・韓国語・繁体字 `content/faq/smokeless.<lang>.md:19,26` の10リンクに加え、実装直前の照合でフランス語・韓国語・繁体字の55行にあるウィジェットの3リンクも確認した。改善対象は計13リンク。

- 「初回チュートリアルはありますか？」の回答は初期設定・基本操作と書いて、Guide先頭への「画像付きの使い方」を表示している。対象Guideには初回チュートリアル/1箱の本数と金額設定の専用第1節がある。質問に対応する「初回チュートリアルと本数設定」等のラベル・周辺文に限定し、第1節へ直リンクする。第1節に載っていない日常操作までこのリンクで説明できるとは書かない。
- 「何を確認できますか？」の回答は本数・金額・期間別推移を説明して「使い方」でGuide先頭へ戻る。Guide第4節に日別/月別/年別カレンダー、第5節にグラフがある。「カレンダーで日別・月別・年別に振り返る」等の具体ラベルで第4節へ接続すると、既存の短い回答と自然につながる。推移の操作まで必要なら第5節を別の具体参照として扱うが、単なる重複回避のために別アンカーを付けない。
- 共通Support欄のGuide先頭リンクは全操作の入口として維持する。質問ごとの特定節リンクと入口リンクは意味が異なる。

| 言語 | 該当linkId | 第1節の実fragment | 第4節の実fragment |
| --- | --- | --- | --- |
| ja | 1807, 1808 | `1-初回チュートリアルと本数設定を確認する` | `4-カレンダー-で日別--月別--年別に振り返る` |
| en | 890, 891 | `1-check-the-first-tutorial-and-pack-settings` | `4-review-by-day-month-and-year-in-calendar` |
| fr | 1969, 1970 | `1-vérifiez-le-premier-tutoriel-et-les-réglages-du-paquet` | `4-revoyez-par-jour-mois-et-année-dans-calendrier` |
| ko | 3199, 3200 | `1-첫-튜토리얼과-한-갑-설정을-확인합니다` | `4-캘린더로-기록을-확인합니다` |
| zh-hant | 5168, 5169 | `1-確認首次教學與每包設定` | `4-在-日曆-以日--月--年回顧` |

ウィジェットの追加3件：fr linkId 1971 → `#6-utilisez-le-widget-daccueil`、ko linkId 3201 → `#6-홈-위젯을-사용합니다`、zh-hant linkId 5170 → `#6-使用主畫面小工具`。質問もラベルもホームウィジェットの操作に限定し、各言語の実在第6節へ接続する。ja/enの同じ回答はすでにウィジェット節へ直リンクしている。

## 文字列だけでは疑わしく見えるが、意味を確認して適合とした例

- ギャンカレFAQ「タグの使い方」→Guide `#6-設定-を調整する`。見出しは一般的な設定だが、本文 `content/htu/balance-calendar.md:54` にタグ名/アイコン編集、58行に初期タグの選び直しがあるため適合。FAQの「追加後の操作とデフォルトタグの設定」→第5節も49–50行のウィジェット操作/既定タグ説明と一致。
- Uni:Note「録音の操作」→ `#recording`、Pocket「取り込んだ録音の再生」→ `#recordings`。文字列や単複ではなく機能と対象アプリが一致。両アプリ×6言語のFAQ→Guide66件を、書く/探す/PDF/録音/復習/backup/windowsとimport/refresh/recordings/readの意味で確認。
- Noccaの互換アンカー `#3-家族を招待する` は見出し「家族と接続する」に接続する。操作手順が招待と接続を含むため不一致ではない。
- オトミル `#settings` は「文字の大きさと聞き取り環境を変える」に接続し、FAQの表示/聞き取り設定の質問に対応。SIGNAL `#settings-help` は案内再表示・学習リセット節に接続。
- Newsの `#press-release` / `#blog` 等は同じ名前のフィルタリンク自体がtargetになるが、`layouts/_partials/news-items.html:10` と `assets/css/site.css:211-216` で該当記事分類のみ表示する。別の本文見出しへスクロールしないこと自体は意味不一致ではない。
- 製品名だけのSupportパンくずは、Guide/FAQ/Privacy/Termsを束ねる製品サポート階層への戻り先として `#support` を使う (`layouts/single.html:4`)。末尾の製品名リンクは同製品の紹介先頭であり、削除対象の同一目的リンクではない。
- AboutとProductsのh1はコピーになっていてラベル文字列と同一でないが、/company/はブランド・人物、/products/は全アプリ一覧として正しい。
- 同言語翻訳がないページの言語メニューは選んだ言語Homeへ移動する現行仕様 (`layouts/_partials/essentials/header.html:10`)。全1,260件で言語名と到着先言語が一致。Homeへの246件には本来のHome切替も含むため、この数をすべて翻訳欠落とは扱わない。
- `linkId 4112, 4113` は過去記事の `/htu/smoke-less/` / `/privacy/smoke-less/`。targetTextは空だが、ローカル生成alias HTMLのcanonicalとmeta refreshはそれぞれ正しい現行Smokeless本文URLを指す。意味不一致・リンク切れとは判定しない。旧URL互換性として保持し、入口を直接URLにするかは履歴本文保護方針に従う。

## 検証の範囲

アンカーの存在だけでなく、目次ラベルと見出し、FAQの質問と節本文、共通Supportの製品ID/URL種別、日本語fallback表示、News分類CSSを確認した。物理ブラウザで全クリックした監査や、外部URL・mailtoの意味/到達性の検証をしたとする報告ではない。外部リンクと公開物の検証はroot監査の担当。
