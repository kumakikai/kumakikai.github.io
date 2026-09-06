# すわなび Apple Watch紹介・全サイト日本語組版監査

2026-09-07。Hugoplateと既存の情報設計・URLを維持した追加変更。

## 1. 最新のApple Watch仕様

すわなびプロジェクトの `3e9e7f38a67f233c1bc4a18c6e56bb50693355d6`、1.2.0 build 3の実装・提出素材・リリース文書を確認した。

- 左の緑ボタンで「我慢」、右の赤ボタンで「喫煙」を1件記録。
- 数字はそれぞれ当日の件数。履歴・グラフ・金額などの確認はiPhone側。
- iPhoneで購入権利を確認した後は、未接続でもWatchへ一時保存。再接続後にiPhoneへ同期し、日時はWatchで記録した時刻を保持。
- 既存の「広告削除」または「銘柄追加パック」の購入特典。購入・復元はiPhone側で行う。
- watchOS 9以降とペアリング済みの対応iPhoneが必要。iPhoneアプリの最低iOS 14と、WatchをペアリングできるiPhone／iOSの条件は区別する。

コードの行番号と、実装・文書間の差は [watch-spec-evidence.md](watch-spec-evidence.md) に記録した。アプリのソース、ビルド、Store設定は変更していない。

## 2. Productへ追加した訴求

Home・Products・Product Hero・Aboutの代表アプリ・Product基本情報に、共通partialから **iPhone / Apple Watch（近日対応）** を表示する。

Product Heroには「Apple Watch対応版は審査中です。公開後、手元で『喫煙』『我慢』を記録できるようになります。」を追加。主要機能の直後に **「Apple Watchから1タップで記録。」** の専用セクションを設けた。操作、当日の件数、同期、購入条件をiPhoneとWatchの画面とともに説明する。

既存のiPhone版へ進む公式App StoreバッジはHeroと主要説明後の2箇所を維持。未公開Watch版のダウンロードボタンは作っていない。

## 3. 採用した実画像

元フォルダは `/Users/yuya/Projects/smokeless/design/app-store-screenshots-2026-09-03/`。最新のWatch提出素材は2026-09-06に作成されたもの。

- 日本語：`final/apple-watch/422x514-upload/01-recording.png`
- 繁体字・韓国語・フランス語：`final/apple-watch/{zh-Hant,ko,fr}/422x514-upload/01-recording.png`
- 英語・ドイツ語および使い方：`sources/ui/watch/recording-40mm.png` の数字のみの実画面。
- iPhone側は既存の正式な `static/images/apps/smokeless/01-recording-{420,840}.webp`。

Watch提出用は422×514、実画面は324×394。`assets/images/apps/smokeless/watch/`へ原本を保持し、Hugoで原寸／半幅のWebPを生成。寸法・srcset・lazy・decodingを指定し、原本を拡大生成していない。

2枚目のWatch提出素材も監査したが、記録画面で当日件数まで説明できるため本番素材へ重複採用しなかった。新しいSimulator撮影や画像生成は行っていない。元ファイル・SHA・画像照合は [watch-assets.json](watch-assets.json)。

## 4. 審査中と一般公開の区別

Apple公式Lookupで日本・台湾・フランス・韓国の公開版は **1.1.1**。ユーザーの最新申告に従い、1.2.0は「提出・審査中」として扱った。古いローカル文書の「提出前」は現状の根拠にしていない。

`data/product_details/smokeless.json` の `watch.status: review` が状態の正。将来、1.2.0の一般公開を確認してから `published` に変更すると、近日対応・Hero・Product・使い方の注意書きがまとめて切り替わる。日付や言語、Geo-IPから公開状態を推測しない。公開前のSoftwareApplicationにはwatchOSを追加しない。

## 5. 使い方への追加

既存の `/htu/smokeless/`、`/en/htu/smokeless/`、`/ko/htu/smokeless/`、`/fr/htu/smokeless/`、`/zh-hant/htu/smokeless/` の末尾に、`#apple-watch` と実画面付きの4手順を追加。

1. インストールとiPhone側の購入権利確認・復元。
2. 左緑の我慢／右赤の喫煙を記録。
3. 当日の件数を確認。
4. 未接続時の一時保存、再接続後の同期、反映確認。

旧本文はそのまま保持した。ドイツ語の使い方本文は元からないため、既存の日本語フォールバックを維持。Watchの説明文自体は6言語に用意した。

## 6–8. 実表示で発見した日本語の問題

| 対象 | 修正前の具体例 |
|---|---|
| Home | 「問／題集」「ウィ／ジェット」「ワンタッ／プ」「カレン／ダー」 |
| Product詳細 | Pocket「バックアッ／プ」「答／え」、Nocca「ペー／ス」、SIGNAL「自／分」、Uni:Note「勉／強」、ギャンカレ「貯／金」 |
| Product本文 | 「お問い／合わせ」「相／手」など、Chromeのauto-phraseでも残る分割 |
| 使い方・FAQ | 「ア／イコン」「サー／バー」「インストー／ル」「デー／タ」「ア／ドバイス」 |
| その他 | Privacy互換ページの見出し末尾「いて」「て」、Watchの長い画像説明で句点だけの行、Footer注記の「商／標」 |

共通組版で語中分割を修正した。Homeの「企画・開発・運営」は既存のフレーズ表示partialでまとめ、事業内容の途中で分けない。Watch画像の説明は「審査提出用のWatch画面。」へ短縮し、旧Privacy一覧の見出しは「プライバシーポリシー」へ簡潔化した。各アプリのポリシー本文は変更していない。

## 9. 共通Typography

`npm run build` のpostbuildでBudouXの文節候補を取得し、`Intl.Segmenter`の単語境界と禁則条件で絞って`<wbr>`を挿入する。`.jp-text`の `word-break: keep-all`、`overflow-wrap: anywhere`、`line-break: strict` を見出し・本文・リスト・説明・Footerの商標注記へ共通適用。

文字列を変えず、既存の意味単位の見出しspanや意図した改行を保持する。ランダム候補のtemplateも生成時に処理し、初回描画後の置換はない。コード・他言語の本文・リンク先・ID・構造化データは保持する。

閲覧者へ追加JavaScriptを配信しない。Node.js 22.22.0をローカル／CIで固定し、日本語辞書の違いによる生成差を防ぐ。BudouX・parse5はbuild専用のdevDependencies、lockfileに固定。`npm run preview`は組版後の完成HTMLを配信する。Hugoの高速な`dev`表示と本番組版の違いはREADMEへ明記した。

## 10–11. 実ブラウザの確認範囲

- **1440 / 1280 / 1024 / 768 / 430 / 390 / 375px**。
- ChromeとWebKitで61ルート＋Homeの追加4seedを各7幅、**455条件ずつ、計910条件**。
- Home、Products、全8 Product、About／Contact、News一覧、全15 News記事、全8使い方、全8 FAQ、全8 Privacy、全3 Terms、既存互換入口、404。
- 全7幅・両エンジンで、ランダム対象の8アプリすべてを実際のFeatured表示で確認。Uni:Note先頭固定、4件表示、重複なし。
- 各見出しと本文をDOM Rangeで行ごとに復元して読み、単なるoverflow検査と分けた。全8 Featuredの1024px／375px画像16枚と主要ページの画像も目視した。
- Watchは6言語Product・5言語使い方の1440／390px、Light／Darkおよび日本語JS無効の**48条件**で成功。axe44条件で違反0。

910条件でHTTPエラー・横はみ出し・欠損画像・Featured重複なし。本文の語中分割候補は0。日本語として独立する「確認。」「選ぶ」の短い末尾行は、機械候補をそのまま不具合とせず読んで判定した。Privacy互換見出しの追加修正は別の14条件で再確認し、全幅で1行・問題なし。

大きなブラウザ記録は読みやすいJSON要約と、全条件を無損失で保持した`.json.gz`原本に分けた。要約の`fullEvidence`とSHAで原本を確認できる。

詳細は [EDITORIAL.md](EDITORIAL.md)、[chrome-final.json](chrome-final.json)、[webkit-final.json](webkit-final.json)、[watch-browser.json](watch-browser.json)。実機のiPhone／iPad操作確認とは区別する。

## 12–14. 修正後のスクリーンショット

- [Home Desktop 全体](screenshots/chrome-home-1440-footer-followup.jpg)
- [Home Mobile 全体](screenshots/webkit-home-390-footer-followup.jpg)
- [すわなび Product Hero Desktop](screenshots/smokeless-hero-1440.jpg)
- [すわなび Watch紹介 Desktop](screenshots/watch-product-section-1440.jpg)
- [すわなび Watch紹介 Mobile](screenshots/watch-product-section-390.jpg)
- [すわなび 使い方 Mobile](screenshots/watch-guide-390.jpg)
- [Uni:Note Desktop 全体](screenshots/chrome-products-uni-note-1440-final.jpg)
- [Uni:Note Mobile 全体](screenshots/webkit-products-uni-note-390-final.jpg)

## ビルド・互換性・限界

Production build成功。既存191 URL（正式ページ138・aliases53）、84記事本文、126の固定コピー、9,758参照、204 SEOページを検証し、エラー・警告0。URL・aliasの新設／削除／移動なし。Privacy Policy、FAQ、Press Release、App Store Connect関連の既存URLを維持した。[静的検証](static-verification.json)

ビルド時組版は全277HTMLについてテキスト、属性、ID、URL、JSON-LD、DOM構造の保持と再実行の安定性を別途検証。[保持検証](formatter-preservation-review.json)

アプリの実機動作、Store購入・復元、提出バイナリの再試験は今回のWeb作業では行っていない。Apple Watch版の公開完了もまだ主張しない。英語・ドイツ語のWatch販促画像がないため、実画面を代替に使っている。

## 主な変更ファイル

- `data/product_details/smokeless.json`：Watch状態・仕様・6言語コピー・画像。
- `layouts/_partials/product-platform.html`、`watch-product.html`、`watch-guide.html`：共通表示。
- `layouts/product/single.html`、`product-details.html`、`app-showcase.html`、`app-card.html`、`company-product.html`：接続。
- `content/htu/smokeless*.md`、`layouts/_shortcodes/watch-guide.html`：既存使い方への追記。
- `assets/css/site.css`：Watchレイアウトと共通日本語Typography。
- `scripts/format-japanese.mjs`、`verify-japanese.mjs`：ビルド時組版と不変条件の検証。
- `scripts/verify-site-typography.cjs`、`verify-watch.cjs`：実ブラウザ確認。
- `.node-version`、`scripts/run-hugo.js`、`package.json`／lockfile、README：再現可能なbuildと保守手順。

## 最終追補と性能

- Privacy：14条件成功。
- Homeの事業内容の意味単位：70条件成功。全7幅で「企画・開発・運営」が同じ行に収まる。
- Footer：14条件成功。日本語商標注記にも共通組版を適用し「商／標」を解消。
- ランダム選出・多言語・テーマ・JS無効等：88条件成功。実際の6回の表示でHome／Aboutとも6通りを確認。全候補とカテゴリ所属を維持。
- 上記ランダムUIのCLS最大0、axe60回で違反0。最終Home追補のCLS2回も0、axe2回で違反0。
- Lighthouse mobile lab：Home **97 / 100 / 100 / 100**、すわなび **99 / 100 / 100 / 100**（Performance / Accessibility / Best Practices / SEO）。両方CLS 0、TBT 0。実ユーザーの回線・実機を測った値ではない。[性能記録](lighthouse.json)
- `npm audit`：既知の脆弱性0。[依存確認](dependency-audit.json)

[Desktop Hero](screenshots/chrome-home-hero-1440-footer-followup.jpg)／[Mobile Hero](screenshots/webkit-home-hero-390-footer-followup.jpg)／[Mobile Footer](screenshots/webkit-footer-390-footer-followup.jpg)

## 公開反映の確認

実装コミット：`97f96b69b16b7b7374df07185fc6319600983c26`（mainへpush済み）。

- [Hugo CI](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34057274279)：成功。
- [GitHub Pages](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34057298085)：成功。配信コミット `de1eda6662694c4ac20dc85a90275644f4de6f0d`。
- 2026-09-07 05:14 JST、**全277 HTML URLでHTTP 200・最終ローカルビルドのSHA256と一致**。404、本文欠損、未反映ページなし。[公開URL検証](public-verification.json)
- 新Watch画像10個と共通CSS、計11ファイルもHTTP 200・バイト一致。[公開素材検証](public-assets.json)

維持したURLの全一覧は公開URL検証の`results`に記録。今回の新規ページURL／alias／redirectは0件。既存の使い方ページ内に`#apple-watch`を追加しただけで、各アプリのSupport・Privacy・FAQ・記事を移動していない。

公開版1.1.1を直前のApple Lookupでも再確認し、Watchは近日対応／審査中として配信した。[公開前Store確認](store-before-publish.json)

`.DS_Store`は変更・コミットしていない。
