# Home / About 最終整理

確認日：2026-09-07。

HomeとAboutの最終整理を実装し、production build・URL互換性・ブラウザ確認を完了しました。公開確認は末尾に記録します。

## 1. 今回の目的と変更範囲

既存のプロダクト紹介・スクリーンショット・デザインを維持し、Homeは主力といくつかのアプリを知る場所、Productsは全アプリを選ぶ場所、Aboutは開発者と取り組みを知る場所として整理します。Hugoplateからの再移行や、既存アプリの機能・価格・提供地域の変更は行っていません。

## 2. Homeの構成

Hero → Featured Apps → Products一覧へのCTA → News → Aboutの順です。Heroの主要コピー、実UIを使うビジュアル、Newsの最新3件、Aboutへの導線を維持しています。全アプリを一度に同じ重要度で並べる構成にはしていません。

## 3. Uni:Noteは先頭に固定

`layouts/home.html`では、`id: uni-note`を指定して最初の`app-showcase`を出力します。この要素はランダム選択のコンテナ外に置き、候補集合からも除外しています。したがって、選定処理によってUni:Noteを削除・後方へ移動する経路はありません。

Uni:Noteの主力としての大きな紹介、既存キャッチコピー、App Storeと詳細への導線を維持します。

## 4. Homeの残り3枠と候補7アプリ

`data/apps.json`の`featured: true`を「Homeの紹介候補」として扱います。現在の8アプリすべてを候補対象とし、先頭固定のUni:Noteを除いた以下の7アプリから、重複なく3つを表示する実装です。

| ID | アプリ | 現在の状態 |
|---|---|---|
| `oto-miru` | オトミル | 公開中 |
| `giga-poke` | ギガポケ | 公開中 |
| `nocca` | Nocca | 開発中 |
| `uni-note-pocket` | Uni:Note Pocket | 公開中 |
| `balance-calendar` | ギャンカレ | 公開中 |
| `smokeless` | すわなび | 公開中 |
| `signal` | SIGNAL | 公開中 |

この表の状態はデータ監査用です。HomeやAboutに固定の公開アプリ数を追加していません。Products一覧の8アプリと表示順は維持します。

## 5. 選定処理と実行タイミング

`assets/js/select-products.js`は、候補配列をFisher–Yatesで並べ替え、Homeでは3つ、Aboutの各領域では1つを選びます。選択済みのグループに`data-selection-ready`を付け、同じページ上で繰り返し切り替えません。

`layouts/_partials/select-products.html`はHugoでminifyしたコードを候補HTMLの直後にinline出力します。外部スクリプトの取得やDOMContentLoadedを待つ処理、タイマーによる再選定、自動カルーセル、追加ライブラリ、選定用cookie・保存領域、Geo-IP判定はありません。選ばれない候補のHTMLは`template`内に置き、選定後は不要な候補とともに取り除きます。

追加コードは圧縮後551bytesです。下記のローカルブラウザ検証で、通常通信とFast 3Gシミュレーションの双方で選定が初回描画時に完了していることを確認しました。CLS62サンプルはいずれも0です。

## 6. JavaScriptが無効な場合

HomeのHTMLには、Uni:Note・オトミル・ギガポケ・Noccaの4アプリが通常のコンテンツとして出力されます。その他の候補は不活性な`template`内にあり、JavaScriptなしで全8アプリが展開される構造ではありません。

Aboutは各領域の既存`product`を既定表示として保持します。学習・ノートはUni:Note、会話の支援はオトミル、日常の記録・管理はギガポケです。各Productへの通常リンクもHTMLに残します。

## 7. Other Appsと一覧CTAの整理

Other Appsの見出し、説明、開閉式の一覧、`app-disclosure.html`を削除しています。Featured直後の一覧案内は「すべてのプロダクトを見る」の1つのCTAにまとめ、同じ言語の`/products/`へ接続します。HeroやHeaderにある既存のProducts導線は維持します。

`data/home/`の不要な`other`・`otherIntro`も6言語から削除しています。Homeの選定に含まれないアプリもProductsから閲覧できます。

## 8. コピーと実画面の保持

最初の4アプリの`taglineLines`と説明は維持しました。従来Other Appsだった4アプリは、Product詳細の既存`overviewTitle`を共通partialで参照します。Home向けの新しいキャッチコピーを作ったり、同じ文章を別データへ重複定義したりしていません。

| アプリ | 使用する既存の日本語コピー | 参照元 |
|---|---|---|
| Uni:Note | 大学のノートを、iPadへ。 | `data/home/ja.json` |
| オトミル | 聞こえにくい会話を、大きな字幕に。 | `data/home/ja.json` |
| ギガポケ | 届いたギガ、期限切れにしない。 | `data/home/ja.json` |
| Nocca | 家族へ伝える。自分のペースで。 | `data/home/ja.json` |
| Uni:Note Pocket | iPadでまとめた学びを、iPhoneで持ち歩く。 | `data/product_details/uni-note-pocket.json` |
| ギャンカレ | その場で残して、日付で振り返る収支記録。 | `data/product_details/balance-calendar.json` |
| すわなび | 吸った回数も、吸わなかった選択も、記録に。 | `data/product_details/smokeless.json` |
| SIGNAL | 個人の発信と、気になる話題をひとつの場所へ。 | `data/product_details/signal.json` |

6言語とも同じ参照方法です。アプリアイコンとスクリーンショットも既存データを共用し、仮画面や新規のAI製アプリ画面は追加していません。

## 9. App Store・開発中表示・提供地域

紹介候補の変更と公開状態を分けています。Noccaは`status: development`のままで、Homeに選ばれた場合も開発中表示と既存の詳細導線を使います。App Storeリンクは追加していません。

公開アプリの公式バッジ、確認済みStore URL、地域リンク、画像、既存Product URLは変更していません。表示言語をApp Store地域とみなす処理や、未確認URLの生成も追加していません。AboutでNoccaが選ばれる場合は開発中と表示します。

## 10. Companyの画面名をAboutへ

6言語の`data/corporate/<lang>.json`で`nav.company`をAboutに変更しています。Header、モバイルナビ、Aboutのラベル、生成ページtitleがこのデータを参照します。サイト内のURL・section・データディレクトリ名は`company`のままです。

`scripts/sync-products.py`は元から`nav.company`をtitleに使うため変更していません。同期による変更は`content/company/_index*.md`の6入口です。

## 11. 氏名をYuya Nakamuraへ統一

`founderName`を全言語で`Yuya Nakamura`とし、重複していた`founderEnglishName`を削除しました。Founderと基本情報の氏名、画像alt、AboutのSEO説明を整理し、Person構造化データもRoman表記だけを使います。

公開許可済みの人物イラスト、Software Engineer / App Developerという肩書き、開発領域、技術経験、既存プロフィールの趣旨は維持しています。新しい経歴や個人情報は追加していません。

## 12. 公開プロダクト数の固定表示をなくす

Aboutの紹介文を、6言語とも「複数のプロダクト」を意味する文章に変更しました。日本語は次のとおりです。

> 複数のプロダクトをApp Storeで公開・運営しています。代表的なアプリから、取り組んでいる領域をご紹介します。

`%d`の差し込みとtemplate側の件数集計を削除しています。実績数を強調する新しい表示は追加していません。

## 13. Aboutの領域別紹介

`data/apps.json`の`area`と、`data/company/<lang>.json`の各`areas`行を対応させます。templateで対象の領域に絞ってから候補を出力するため、クライアント側で全アプリから無条件に選ぶ構造ではありません。

| `area` | 領域 | 選定対象 | JavaScript無効時の既定 |
|---|---|---|---|
| `learning` | 学習・ノート | Uni:Note / Uni:Note Pocket | Uni:Note |
| `communication` | 会話の支援 | オトミル / Nocca | オトミル |
| `daily-tools` | 日常の記録・管理 | ギガポケ / ギャンカレ / すわなび / SIGNAL | ギガポケ |

各行で表示するアプリは1つです。既存の`product`キーは、同じ領域内の既定表示用IDとして維持します。名称・端末・アイコン・リンクはProductデータを共用します。

## 14. Aboutの基本情報とContact

基本情報からWeb行と不要になった`webLabel`を削除しました。運営名、開発者、事業内容、既存メールを残します。末尾ContactのメールCTA、For Mediaから`#contact`へ移動する導線、FooterのContactは維持します。

名刺全体、電話番号、QRコード、未確認の会社情報を追加していません。人物画像の利用許可と編集方法の記録は、既存の`docs/company/portrait/`を保持します。

## 15. Uni:NoteのiPad表記とOGP

共通の`platform`を6言語とも`iPad`に統一し、Only・専用等の限定語を外しています。Home、Products、Product詳細、Aboutの端末表示はこの共通データを参照します。

今回明示された既存本文の変更は、次の2件だけです。URLや他の本文は変えていません。

| 既存URL | 変更 |
|---|---|
| `/htu/uni-note/` | 対応環境の`iPad専用`を`iPad`へ |
| `/faq/uni-note/` | 対応端末の`iPad専用です。`を`iPadです。`へ |

`static/images/og/uni-note.png`も既存生成スクリプトで再生成し、焼き込みの端末表記が`iPad`になっていることを画像で確認しました。1200×630の形式と既存キャッチコピーを維持しています。`scripts/generate-og.mjs`に対象ID引数を加え、Uni:Noteだけ再生成できるようにしています。

確認時のUni:Note OGP SHA-256：`8176294f9a108aa0038350b8394da1893dd30761c8a996975a9ec49877fef5b0`。

## 16. URL・既存コンテンツの保護

ソース上では、今回の変更によるHTTPページの移動・削除、新しいaliasやredirectはありません。維持対象は`/company/`と6言語入口、全Product、各アプリのSupport・FAQ・Privacy・Terms、公開済みNotes・Press Release、既存アンカーです。

`/htu/uni-note/`と`/faq/uni-note/`の許可された語句変更は、他の既存本文変更と区別して検証します。App Store Connectから参照される可能性があるURLは同じ場所で読めることを最終buildと公開環境で確認する必要があります。HTTP成功・本文保持・canonical・aliasの最終結果は下記の検証欄へ追記します。

過去の`docs/company/`等に残る漢字氏名、数値、旧Other Appsの記述・画像は、当時の検証証拠です。今回の公開コンテンツに残っているかどうかの検索とは分け、過去証拠を書き換えません。

## 17. 主な変更ファイルと保守方法

| 場所 | 変更内容 |
|---|---|
| `data/apps.json` | Home候補の意味と`area` |
| `data/home/<lang>.json` | Uni:Noteの端末表記、不要なOtherキー削除 |
| `data/company/<lang>.json` | Roman氏名、数値なしの紹介、領域、不要キー削除 |
| `data/corporate/<lang>.json` | About表示、一覧CTA、SEO説明 |
| `content/company/_index*.md` | データ同期によるAbout title等 |
| `layouts/home.html` | Uni:Note固定、3枠の候補、Products CTA |
| `layouts/company/list.html` | 領域内1件、氏名・数値・基本情報の整理 |
| `layouts/_partials/app-showcase.html` | 共通紹介と既存overviewTitle参照 |
| `layouts/_partials/company-product.html` | 領域で選ぶアプリの共通リンク |
| `layouts/_partials/select-products.html` / `assets/js/select-products.js` | 初期表示時だけの選定 |
| `layouts/_partials/app-disclosure.html` | 廃止 |
| `layouts/_partials/essentials/head.html` | Personの氏名を一本化 |
| `assets/css/site.css` | 不要な開閉表示の削除と新構成の調整 |
| `content/htu/uni-note.md` / `content/faq/uni-note.md` | 許可された端末表記変更のみ |
| `scripts/generate-og.mjs` / `static/images/og/uni-note.png` | Uni:Note OGPの限定再生成 |
| `scripts/verify-migration.py` / `scripts/verify-browser.cjs` / `scripts/verify-company.cjs` | 今回の表示契約と既存URLの検証 |
| `README.md` | 候補・領域・About・氏名・件数を固定しない編集手順 |

新しいアプリは共通データにID・`featured`・`area`・公開状態・素材を登録し、6言語のコピーを用意します。状態や提供地域を掲載候補と混同せず、Uni:Noteの固定表示を維持します。Aboutの各`product`は同じ`area`内のアプリを指定します。更新後は生成ページ同期、build、静的検証、画面確認を行います。

## 18. 検証・画面・公開結果

- **Hugo production build**：0.158.0 Extendedで成功、warnings 0、errors 0。生成入口72件の同期差分なし。
- **[静的検証](static-verification.json)**：HTML277件、旧URL191件、正式URL138件・既存alias53件、本文84件、固定コピー126項目、内部参照9,690件、SEO204件を検証。旧本文は許可されたUni:Noteの2箇所だけ変更し、それ以外の改変を検出する保護を維持しています。
- **[既存QAとの整合](compat-qa.json)**：Homeの表示と従来のナビ・Support／Privacy導線、AboutのJS有効／無効時を確認。基準となる `docs/migration/baseline.json` は変更していません。
- **[専用ブラウザ検証](browser-verification.json)**：88条件すべて成功。6言語、Desktop1440／iPad834／iPhone393／小型320相当、Light／Dark、no-JS、外部JS遮断、キーボード、重複ID・見出し階層・画像・はみ出しを確認。axe60回で違反0。
- **ランダムの確認**：固定乱数の試験でHomeの全7候補、Aboutの各カテゴリの全候補が表示可能と確認。単一候補と同一DOM再実行時の安定性も確認しました。テスト初回のseed不足による候補網羅失敗は追加seedで検証し、UIを変えず、元試験と補足の経緯をJSONに保持しています。
- **実リロード**：各ページの初回＋5回再読み込みでHome6通り、About5通りを確認。常にHome先頭Uni:Note・同じ表示内の重複なし・Aboutのカテゴリ外選出なし。毎回異なること自体は保証しません。
- **CLS**：通常表示・画像読込・Fast 3Gシミュレーションを含む62サンプルすべて0。Lighthouse総合点は今回再計測していません。実端末や本番のField Core Web Vitalsとは区別します。
- **[表記監査](text-audit.json)**：公開用HTML277件に旧デバイス表記・漢字氏名なし。Aboutの数値差込、Web行、HomeのOther Apps、ナビのCompanyも撤去を確認。過去の検証資料・Git履歴は当時の証拠として残しています。

### スクリーンショット

いずれも今回のproduction buildをChromeで表示して撮影した一回の選出例です。実画面のアプリ・コピーを使用し、ダミーを入れていません。

| ページ | Desktop1440 | Mobile393 |
|---|---|---|
| Home / Light | [画像](screenshots/home-desktop-light.jpg) | [画像](screenshots/home-mobile-light.jpg) |
| Home / Dark | [画像](screenshots/home-desktop-dark.jpg) | [画像](screenshots/home-mobile-dark.jpg) |
| About / Light | [画像](screenshots/about-desktop-light.jpg) | [画像](screenshots/about-mobile-light.jpg) |
| About / Dark | [画像](screenshots/about-desktop-dark.jpg) | [画像](screenshots/about-mobile-dark.jpg) |

### 公開の記録

公開確認は配信後に追記します。
