# Founder・Supportの最終整理

確認日：2026-09-07。変更前のmainは`4e733c6bcdd05bcc377a02a6040f3f2e48581f8a`です。

## Founder

日本語Founderから「Uni:Noteを自分が欲しいノートアプリとして作り始め、現役学生の助言を取り入れた」「すわなびは喫煙している友人の要望がきっかけ」という個別アプリの話を削除しました。他5言語の対応箇所も更新しています。採用した本文は次の2段落です。

> 組み込みシステム、業務システム、モバイルアプリなど、複数領域のソフトウェア開発を経験。現在はKUMAKIKAIで、iPhone・iPad向けアプリの企画・開発・運営を行っています。
>
> 作るものの分野は特に決めていません。自分が使っていて不便に感じたことや、身近な人から聞いた困りごとをきっかけに、必要だと思ったものをアプリにしています。

氏名`Yuya Nakamura`、肩書き、開発領域、`C / C++ / C# / Java / Python / Dart / Swift`は維持しました。漢字氏名はありません。基本情報はすでに名称・開発者・事業内容の3項目だったため、その状態を保持しています。メール・Web欄はなく、問い合わせはContact CTAへ集約されています。日本語Contactの「各プロダクトページ」表記も確認済みです。今回これらを新たに削除・変更したとは扱いません。

## 全アプリのSupport

すべてのアプリに使い方・FAQ・Privacyの既存日本語本文があります。ダミーの本文ページは追加していません。Contactは共通メール窓口へ、対象アプリ名を件名に付けて直接遷移します。

| Product | Guide | FAQ | Contact | Privacy | Terms |
|---|---|---|---|---|---|
| Uni:Note | 維持 | 維持 | アプリ名付きメール | 維持 | Apple Standard EULA |
| オトミル | 維持 | 維持 | アプリ名付きメール | 維持 | `/terms/oto-miru/` |
| ギガポケ | 維持 | 維持 | アプリ名付きメール | 維持 | `/terms/giga-poke/` |
| Nocca | 維持 | 維持 | アプリ名付きメール | 維持 | `/terms/nocca/` |
| Uni:Note Pocket | 維持 | 維持 | アプリ名付きメール | 維持 | Apple Standard EULA |
| ギャンカレ | 維持 | 維持 | アプリ名付きメール | 維持 | Apple Standard EULA |
| すわなび | 維持 | 維持 | アプリ名付きメール | 維持 | Apple Standard EULA |
| SIGNAL | 維持 | 維持 | アプリ名付きメール | 維持 | Apple Standard EULA |

全URL・各言語の存在状況・24件の既存Support aliasesは[URL監査一覧](url-audit-before.md)に記録しています。翻訳が存在しない本文には、従来どおり「日本語」を明示して既存日本語URLへ案内します。独自規約が日本語のみでも、翻訳ページからApple EULAへ切り替えません。

独自規約がない5アプリのリンク先は、指定された[Apple Standard EULA](https://www.apple.com/legal/internet-services/itunes/dev/stdeula/)です。公式ページの到達を確認しました。既存サイトの外部リンクと同じタブで開き、外部矢印、title、読み上げ用補足でAppleの外部ページであることを示しています。

Productでは次の5行を、同じタイトル・説明・区切り線・矢印のUIで表示します。

| 項目 | 説明 |
|---|---|
| 使い方 | 基本操作や機能の使い方 |
| よくある質問 | よくあるお問い合わせ |
| お問い合わせ | 解決しない場合はこちら |
| プライバシーポリシー | プライバシーに関する情報 |
| 利用規約 | アプリの利用条件 |

使い方の末尾はFAQ・Contact・Privacy・Terms、FAQの末尾は使い方・Contact・Privacy・Termsです。各4行と、対象Productへ戻る小さなリンクを表示します。閲覧中のページへの行は出しません。Support総合ハブを経由する導線はありません。

## 共通化と冗長リンクの除去

- `data/apps.json`の`support`に既存の`guideURL`・`faqURL`・`privacyURL`・独自`termsURL`を登録しました。個別`contactURL`がなければ共通窓口を使用します。
- `data/support.json`で共通メールとApple EULA URLを一元管理します。
- `support-data.html`がURL・翻訳・閲覧中ページの除外・EULA fallbackを解決し、`support-links.html`が全行を表示します。Product・使い方・FAQ・既存記事レイアウトで同じpartialを使用します。
- 明示された独自Termsの本文が見つからなければbuildエラーにします。誤ったURLをEULAへ黙って置換しません。
- Privacyにも説明を追加し、リスト外の小さな「利用規約」リンクと、その専用CSSを削除しました。
- Productの「関連ニュース」はギガポケ・Noccaの6言語、計12リンクを削除しました。他Productには元からありませんでした。
- Guide・FAQのPress Releaseリンクは変更前から0件です。全ページで0件を再確認し、存在しなかったリンクを削除済みとは報告していません。
- 全8件のPress Release本文・URLとNewsからのリンクは維持しています。

## 本文・URL保持

今回の本文URLの新設・移動・削除、新しいaliases・redirectはありません。独自規約3件、Privacy22件、Guide22件、FAQ22件、Product48件、Press Release8件の計125ソースファイルが変更前のSHA256と完全一致しました。[比較結果](source-preservation.json)

Hugo移行前の191 URL、84記事本文、現在レビュー済みの44 Guide/FAQ本文も既存検査に通っています。検査を通すためのbaseline更新はしていません。公開HTTP結果はデプロイ後の検証記録に分離します。

## build・ブラウザ確認

- Hugo Extended 0.158.0／Node 22.22.0によるproduction build成功。277 HTMLを生成。
- [移行・リンク検証](build-verification.json)：エラー0、警告0、内部参照10,505件、Support416行を検査。
- [Chrome](chrome-browser.json)：全48 Product＋22 Guide＋22 FAQ、計92ページ／232ケースPASS。
- [WebKit](webkit-browser.json)：日本語の全8 Product＋8 Guide＋8 FAQ、計24ページ／96ケースPASS。
- 日本語は1440・768・390pxと390px Dark、他5言語は1440・390px。リンク先・同じ行スタイル・44px以上のタップ領域・キーボードfocus・横overflow・PRリンクの混在を検査しました。
- 日本語24ページのDesktopでaxeのWCAG A/AA検査をChrome・WebKit両方で実行し、違反0件でした。
- [About](about-browser.json)：6言語Desktop／Mobileと日本語Light／Dark、14ケースPASS。Founder・Contactの日本語画像10枚を目視確認しました。
- Product Support、Guide末尾、FAQ末尾の通常viewport画像を別途目視し、利用規約を含む行の階層・可読性・Light／Dark表示を確認しました。
- [負例8ケース](negative-regressions.json)で、Terms欠落・独自規約の誤置換・説明や矢印の欠落・PR混在・自己リンク・Founder小話の復活を検査が検出することも確認しました。

ブラウザのviewport検証であり、iPhone実機での確認ではありません。今回の変更に素材不足・未対応ページはありません。既存の日本語のみの本文を新たに翻訳する作業は含めていません。

## スクリーンショット

- [Product Support／Desktop](screenshots/chrome-products-uni-note-1440-light.jpg)
- [Product Support／Mobile・Dark](screenshots/webkit-products-uni-note-390-dark.jpg)
- [Guide末尾／Mobile](screenshots/chrome-htu-giga-poke-390-light.jpg)
- [Guide末尾／Desktop](screenshots/chrome-htu-giga-poke-1440-light.jpg)
- [FAQ末尾／Desktop](screenshots/chrome-faq-giga-poke-1440-light.jpg)
- [FAQ末尾／Mobile](screenshots/chrome-faq-uni-note-390-light.jpg)
- [Founder／Desktop](screenshots/about-founder-1440-light.jpg)
- [Contact／Mobile](screenshots/about-contact-390-light.jpg)

## 主な変更ファイル

`data/company/*.json`、`data/apps.json`、`data/support.json`、`data/ux/*.json`、`layouts/_partials/support-data.html`、`layouts/_partials/support-links.html`、`layouts/product/single.html`、`assets/css/site.css`、`scripts/verify-migration.py`、`scripts/verify-support.cjs`、`README.md`。

アプリ本体・既存本文Markdown・Hugoplate vendor・デプロイ設定は変更していません。新しい閲覧用JavaScriptや外部ライブラリも追加していません。
