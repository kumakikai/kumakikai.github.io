# 日本語コピー・Typography監査

2026-09-07。Home、Products、全8件のProduct詳細、About、News、Support関連の日本語を監査しました。説明文は「誰が、どのアプリを、何のために作っているか」が分かる内容に絞り、ブランドコピー、具体的な製品説明、操作案内、本人の発表当時の記録は区別して扱っています。

変更後の検証結果と公開確認は後段に記録します。

## 1. 不自然な改行

変更前の実ブラウザ測定では、1440pxのAbout見出しが「身近な不便から、使える道」「具へ。」に分かれていました。1440px・1280pxのContact本文も「…ご連絡ください。ア」「プリの使い方…」に分かれていました。[変更前の行位置記録](typography-before.json)にDOM Rangeによる測定結果を保存しています。

About見出しは内容を直接示す「KUMAKIKAIについて」へ変更。Contactは問い合わせに必要な情報とアプリサポート案内を別段落へ分けました。改行位置を合わせるための`<br>`追加は行っていません。

## 2. Typography側の対応

`assets/css/site.css`で次を調整しています。

- 本文全体の`overflow-wrap: anywhere`を`break-word`へ変更しました。長い連続文字列は必要時に折り返しつつ、最小幅の算出には任意位置での分割を使わない設定です。日本語の語中改行はこの変更だけで解決するものではなく、表示幅・禁則処理・文節解析と合わせて調整しています。
- 日本語の基本設定を`word-break: normal`、`line-break: strict`としました。`@supports`で利用可能な場合だけ`word-break: auto-phrase`を追加します。
- 日本語見出しの負の字間を外し、`letter-spacing: 0`と`text-wrap: balance`を指定。本文は`text-wrap: pretty`を指定しました。
- About冒頭・For Mediaの2カラムを`minmax(0,1fr) / minmax(0,1.1fr)`、間隔48pxへ調整しました。
- Contact本文の最大幅を650pxから52emへ広げ、行高を1.9にしました。短い問い合わせ本文と補足のサポート案内に視覚的な間隔を付けました。
- Contactの短い文は`word-break: keep-all`と`text-wrap: balance`で句読点位置の折り返しを優先します。AboutのHeroは`keep-all / wrap`とし、320pxでは`clamp()`で文字サイズを下げて引用部分を語中で切らないようにしました。長い連続文字列への`break-word`は維持します。
- 長い既存Newsタイトル6件と記事本文の見出し5件は、意味のまとまりを`data/heading_phrases.json`に登録しました。Hugoが同一文字列を`inline-block`のspanへ分け、News一覧・記事h1・本文見出しで使います。画面幅に応じて同じ行にも次の行にも配置され、固定改行は挿入しません。元のtitle・本文の文字列・アンカーID・URL・SEO titleは維持します。
- 720px以下では既存の1カラム構成を維持します。Web Font、改行用のJavaScript、外部ライブラリは追加していません。

`auto-phrase`は補助として使用します。[MDNのword-break仕様説明](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/word-break)を確認し、非対応環境でも基本設定と表示幅で読める構成にしています。Chromeで同機能を無効にした試験に加え、WebKitで実際の非対応時の表示も確認しました。

## 3. About基本情報

基本情報から「お問い合わせ／kumakikai.apps@gmail.com」の行を削除しました。Web欄は以前の整理で削除済みで、再追加していません。最終構成は次の3項目です。

| 項目 | 内容 |
|---|---|
| 名称 | KUMAKIKAI |
| 開発者 | Yuya Nakamura |
| 事業内容 | モバイルアプリケーションの企画・開発・運営 |

問い合わせは同ページ下部のContactと「メールで問い合わせる」CTAへ集約しています。既存メールアドレスやContactアンカーは維持しています。

## 4. Founder名

Founder名・プロフィール画像のalt・基本情報はYuya Nakamuraを維持しています。`content/`、`data/`、`layouts/`のソース検索で漢字氏名の残存はありません。生成HTML277件でも漢字氏名と旧端末表記の残存がないことを[表記監査](text-verification.json)で確認しています。電話番号は追加していません。

## 5. 削除した抽象的な文章

独立した「開発で大切にしていること」セクションを削除しました。削除対象は次の3組です。

| 見出し | 削除した説明 |
|---|---|
| 必要なことを、分かりやすく | 機能を増やすことだけを目的にせず、使いたいことへ迷わず進める表示と操作を考えます。 |
| 使う場面から考える | 授業中、会話中、移動中など、実際にアプリを開く状況を踏まえて必要な機能を選びます。 |
| 公開後も手をかける | 不具合への対応や使い勝手の見直しを重ね、公開したアプリを継続して改善します。 |

これらは方向性の表明に留まり、KUMAKIKAI固有の経緯を増やしていませんでした。日本語以外の5言語でも同セクションのデータと表示を削除しています。

また、Aboutの「ひとつの分野に限らずプロダクトを展開」「日々の具体的な場面を起点に、役立つ道具をつくっています」といった説明を削減しました。分野はWhat we build、開発の経緯はFounderで説明します。

## 6. 具体化した文章

| 対象 | 変更前 | 変更後 |
|---|---|---|
| HomeのAbout説明 | KUMAKIKAIは、学びや暮らしの中で感じる小さな不便を、使いやすいアプリに変えていきます。 | Yuya Nakamuraが、Uni:Noteやオトミルなどのアプリを企画・開発・運営しています。 |
| About冒頭 | iPhone・iPad向けの企画・開発・運営をHero直後に再説明 | KUMAKIKAIは、Yuya Nakamuraが運営するアプリ開発ブランドです。手書きノートのUni:Note、字幕アプリのオトミルなどをApp Storeで公開しています。 |
| Founder後半 | 必要な人が使いやすい形を考え、公開後の改善にも取り組んでいます。 | Uni:Noteは、自分が欲しいと思ったノートアプリを作るところから始まりました。現役学生の助言も取り入れています。すわなびは、喫煙している友人からの要望がきっかけです。 |
| オトミル・最初の画面 | 使い始めの操作を確認できます。 | テレビ・会話・グループから、使いたい場面をひとつ選んで字幕を開始できます。 |
| オトミル・会話の画面 | 病院でのやり取りを例に、大きな字幕と停止ボタンを紹介。 | 病院の受付など、相手の声が聞き取りづらい場面で、iPhoneやiPadに表示された字幕を読みながら会話できます。 |

Noccaの「Noccaは…アプリを開発しています」は主語と述語が合っていないため、「Noccaは…開発中のアプリです」へ修正しました。公開状況や機能は変えていません。

## 7. 開発方針の最終的な扱いと出典

理念の3項目を別の抽象的な3項目へ置き換えることはせず、実際の開発背景をFounderへまとめました。開発・運営のBlogへのリンクもFounder直下へ移しています。

| 公開情報 | 根拠 |
|---|---|
| Yuya Nakamura、Software Engineer / App Developer、組み込みシステム・業務システム・モバイルアプリの経験、技術経験 | ユーザーが本タスクで公開プロフィールとして明示した情報、および提示した名刺素材。勤務先、年数、職歴、学歴は推測していません。 |
| 自分が欲しいノートアプリ、現役学生の助言 | [Uni:Noteについて](../../content/notes/2026-03-12-uni-note.md)の「そういうアプリが欲しくて」「現役の学生にも実際にアドバイスをもらいながら」という記録。 |
| すわなびを作ったきっかけ | [すわなびについて](../../content/notes/2026-03-21-smokeless.md)の「喫煙している友人からの要望をきっかけに作ったアプリ」という記録。 |

既存の人物イラストはユーザーがサイト使用を許可した素材を継続利用しています。名刺全体、電話番号、QRコードは追加していません。

## 8. Contactの整理

見出しを「取材・掲載・お問い合わせ」、本文を次の一文へ短縮しました。

> 媒体名、ご相談内容、対象のプロダクト、希望時期を添えてご連絡ください。

「メールで問い合わせる」CTAの後に、補足として次の一文を分けて表示します。

> アプリの使い方や不具合のご相談は、各プロダクトページのサポートへ。

日本語本文の「各Productページ」を「各プロダクトページ」へ変更。Support・Privacy互換ページの案内も「Productsで」から「プロダクト一覧で」へ変更しました。HeaderのProducts / News / About、Contact、Press Releaseなどのナビゲーション名は維持しています。

## 9. 重複削減と保持した内容

AboutのHeroは「iPhone・iPad向けのアプリを企画・開発・運営しています。」に留め、直後の本文は運営者と実際のアプリ名を説明する構成にしました。基本情報のメール、独立した理念セクションも削除しています。

Productsの案内は「アプリを選ぶと、製品情報や使い方・よくある質問を確認できます。」へ整理しました。製品を知りたい人と利用中の人の入口という役割は変えていません。

以下は具体的な情報やページ固有の役割があるため維持しています。

- HomeのHero「日常の小さな不便を、シンプルなアプリで。」と既存Featuredのキャッチコピー。
- 全8Productの機能・利用場面・対応環境。Uni:NoteのApple Pencil・PDF・問題集、オトミルのテレビ・会話・字幕、ギガポケのpovoコード・期限・コピー、Noccaの本人側・家族側の操作、Pocketのバックアップ閲覧、ギャンカレの収支とタグ、すわなびの喫煙・我慢、SIGNALの配信源を維持しています。
- Newsに掲載する既存15記事の本文。発表当時の仕様・計画・本人の経験は、その時点の記録として保持し、現在の企業コピーへ一律に書き換えていません。
- 各アプリの使い方・FAQ・Privacy Policy・利用規約の既存本文。今回の差分ではこれらのファイルを変更していません。URLも移動していません。

未使用データの整備は公開表示の変更と区別しています。`data/home/ja.json`の`intro`は現在のHomeテンプレートでは未使用ですが、「毎日に寄り添う」を実際の事業内容へ更新しました。`data/corporate/ja.json`の`contactText`も現在未使用で、「Productsの各アプリ」を「各プロダクトページ」へ整理しています。

## 10. What we buildの大分類

装飾的な見出し「学びと暮らしの、具体的な場面に。」を「開発しているアプリの分野」へ変更。直下の分類名を繰り返す導入文も削除し、見出しと3分類だけにしました。カテゴリ固有の機能は列挙していません。

| 表示名 | 説明 | Productデータの`area` | 代表表示の候補 |
|---|---|---|---|
| 学習 | 学ぶ・書く・整理するためのアプリ。 | `learning` | Uni:Note、Uni:Note Pocket |
| コミュニケーション | 会話や意思表示を支えるアプリ。 | `communication` | オトミル、Nocca |
| ユーティリティ | 日常のちょっとした手間を減らすアプリ。 | `utilities` | ギガポケ、ギャンカレ、すわなび、SIGNAL |

以前の`daily-tools`は`utilities`へ統一しました。各カテゴリのProduct所属自体は維持し、6言語のカテゴリ名と説明を同じ大分類へ整理しています。「特典コード」「期限の管理」など、特定Productの機能説明はAboutのカテゴリ説明から削除しました。

既存の軽量JavaScriptによる読込時の1件選出を維持しています。候補は`data/apps.json`の`area`から取得し、他カテゴリから補充しません。JS無効時の既存代表Product、HomeのUni:Note先頭固定＋ランダム3件、全アプリへ静的リンクで到達するProducts一覧も維持しています。新しいアプリは該当する`area`へ追加できます。Noccaは開発中の表示とApp Store CTAなしを維持します。

## 11. Build・ブラウザ・URL確認

最終production buildとブラウザで次を確認しました。

| 確認 | 結果 |
|---|---|
| Hugo production build | 0.158.0 Extended、成功。warnings 0 / errors 0。72入口の同期差分なし |
| [静的検証](static-verification.json) | HTML277件、既存URL191件（正式138 / 既存alias53）、既存本文84件、内部参照9,690件、固定Productコピー126項目、SEO204件で成功 |
| [Chrome改行・画面検証](browser-verification.json) | 63条件成功。About1440 / 1280 / 834 / 393 / 320px、auto-phrase無効時、Dark、全8Product、Home、Products、News、Support、FAQ、使い方、記事。axe43回で違反0 |
| [About互換性](company-compatibility.json) | 6言語のDesktopとJS無効時の12条件成功。基本情報3項目・Roman氏名・Contact1CTA・カテゴリ内代表リンクを確認 |
| [WebKit検証](webkit-verification.json) | 30条件成功。About5幅、Home / Products / Uni:Note / News / Support / 使い方、長いBlog6記事を確認。観測した見出しの語中改行候補0、横はみ出し0、画像欠損0 |
| 表記・素材・本文保護 | [表記監査](text-verification.json)で漢字氏名・旧デバイス表記なし。Productデータはarea以外不変。今回の既存記事・Support・Privacy本文ファイルの変更なし |
| 公開サイト | [公開HTML照合](public-verification.json)：277ページすべてHTTP 200、最終buildとのSHA-256一致。既存URLの404なし |

Chrome・WebKitとも、最終の見出し調整が影響したRoadmap／友人Blogの4条件だけ再検証し、それ以外の不変な画面の成功結果を保持しています。再検証の範囲と実行順は各JSONの`verificationPasses`に記録しました。

ご指摘の「道／具」「ア／プリ」に加え、非対応ブラウザで見つかった「こうした／い」「希／望」「プロ／ダクト」、Newsの「累／計」、本文見出しの「アップ／デート」等も解消しました。About Heroは393 / 320pxで「日常の「こうしたい」を、／アプリに。」、Contactの補足は「アプリの使い方や不具合のご相談は、／各プロダクトページのサポートへ。」と意味のまとまりで表示されます。

WebKitはPlaywrightのWebKit 26.5実エンジンです。iPhone / iPadの実機SafariやFirefox全バージョンの確認ではありません。Chromeではauto-phrase非適用時も別途確認しました。任意の画面幅・すべての日本語本文について語境界の完全な保証をするものではありません。今回Lighthouse総合点の再計測は行っていません。

## 12. スクリーンショットと主な変更ファイル

最終production buildを表示した確認画像です。ランダムProductは撮影時の選出例です。

| ページ | Desktop | Mobile |
|---|---|---|
| About | [Chrome](screenshots/about-desktop.jpg) / [WebKit](screenshots/webkit-about-desktop.jpg) | [Chrome](screenshots/about-mobile.jpg) / [WebKit](screenshots/webkit-about-mobile.jpg) |
| Contact周辺 | [Chrome](screenshots/contact-desktop.jpg) / [WebKit](screenshots/webkit-contact-desktop.jpg) | [Chrome](screenshots/contact-mobile.jpg) / [WebKit](screenshots/webkit-contact-mobile.jpg) |

主な変更ファイルは、`assets/css/site.css`、`layouts/company/list.html`、`data/company/*.json`、`data/apps.json`、`data/home/ja.json`、`data/corporate/ja.json`、`data/ux/ja.json`、`data/product_details/nocca.json`、`data/product_details/oto-miru.json`です。会社紹介・Supportの日本語metadataはデータ同期で更新しています。見出しのまとまりは`data/heading_phrases.json`と`layouts/_partials/heading-text.html`、News一覧と記事の描画で管理しています。保守手順と分類はREADMEへ反映しています。

## 公開確認

- 実装コミット：[`c814881d6f67d5a7c37e09cbca0f1295770f28a7`](https://github.com/kumakikai/kumakikai.github.io/commit/c814881d6f67d5a7c37e09cbca0f1295770f28a7)、`main`へpush済み。
- [Hugo build / deploy](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34054883186)：成功。
- [GitHub Pages公開](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34054906566)：成功。配信コミット`4015853ef07b01d4a31a793c5fe63f9387b2f6d0`。
- 公開ページ：[About](https://kumakikai.github.io/company/) / [Contact](https://kumakikai.github.io/company/#contact) / [Home](https://kumakikai.github.io/) / [News](https://kumakikai.github.io/news/)。

- [公開HTML照合](public-verification.json)：277ページすべてHTTP 200、最終buildとSHA-256一致。旧URL191件を含み、新規URL・alias・redirectは追加していません。
- [公開アセット照合](public-assets.json)：公開Home・Aboutの参照から取得したCSS・主要JS・Founder画像192/384の4件がHTTP 200、byte数・SHA-256一致。公開HTML自体も一致しています。
