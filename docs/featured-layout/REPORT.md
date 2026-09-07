# Home Featuredの表示順と左右配置

更新日：2026-09-07。

## 修正内容

オトミル・NoccaのProductデータに固定されていた`reverse`を削除し、`app-showcase.html`もアプリ固有の反転classを出力しないようにしました。これにより「このアプリは常に左側」という指定はなくなります。

Uni:Noteを先頭に固定し、残り3件を選ぶ既存のランダム処理は変更していません。選出されたDOMの実際の順番へCSSを適用します。Uni:Noteは選出グループ外の1件目、グループ内の奇数番目はページ全体の2・4件目となるため、その2件だけ画像を左に配置します。

| ページ内の表示順 | テキスト | スクリーンショット |
|---|---|---|
| 1：Uni:Note固定 | 左 | 右 |
| 2：ランダム | 右 | 左 |
| 3：ランダム | 左 | 右 |
| 4：ランダム | 右 | 左 |

901px以上はこの2カラム、900px以下は全アプリ共通で説明・CTA・配信地域・補足→スクリーンショットの縦順です。反転のCSS自体をDesktop側のmedia query内へ閉じ込め、Mobileの読み順を変更しません。スクリーンショットの内部順序・重なり・shadow・cropは変更していません。

JavaScript無効時も、静的に出力される4件へ同じCSSが働きます。左右配置のためのJavaScript・遅延実行・追加DOM更新・外部依存はありません。既存の選出処理は候補HTML直後のinline scriptで実行され、選出されたDOMに初めから正しいCSSが適用されます。

## 保持したもの

- Uni:Noteの先頭固定、残り3件の重複なしランダム選出。
- 全8アプリの内容、App Store CTA、配信地域、公開／開発中表示。
- ギガポケの非公式アプリ表記を含む、テキスト側の補足。
- Product詳細・Aboutのレイアウト、本文、既存の公開URL。

## build

Hugo Extended 0.158.0／Node 22.22.0によるproduction buildは成功。[互換性検証](build-verification.json)で既存191 URL、84記事、44 Guide/FAQ本文を保持し、エラー・警告は0件でした。

公開前に並行作業のNocca法務・サポート更新`006e874`を統合しました。その本文やURLを巻き戻さず、統合後のproduction build、追加の法務レビュー検査18件、URL互換性検証もすべて成功しています。今回のFeatured修正に伴う本文・URL変更はありません。

## 主な変更ファイル

- `assets/css/site.css`：表示順に基づくDesktopの左右交互配置。
- `layouts/_partials/app-showcase.html`：アプリ固有の反転classを廃止。
- `data/apps.json`：固定`reverse`属性を削除。
- `README.md`：順番とbreakpointの保守方針を追記。

検証用コード・結果は同じディレクトリの記録と`scripts/verify-featured-layout.cjs`に保存します。

## ブラウザ検証

- [Chrome 33ケース](chrome-browser.json)・[WebKit 32ケース](webkit-browser.json)、すべてPASS。
- 通常の乱数による実際の再読み込み10回で9種類の並びを観測。すべてUni:Note先頭・重複なし・画像は右→左→右→左でした。
- オトミル、ギガポケ、Nocca、Uni:Note Pocket、ギャンカレ、すわなび、SIGNALの7候補を、それぞれ左右両方のFeaturedとして表示しました。検証用seedはブラウザのテスト環境だけで使用し、本番コードには固定選出を入れていません。
- 1440／1280／1024／901pxでは左右交互、900／834／768／430／390／375pxでは全4件が説明→画像の縦順でした。
- Light／Dark、JavaScript無効時も確認しました。検査はclass名だけでなく、実際の表示座標を比較しています。
- 元データとの照合でコピー、画像の内部順序、リンク、配信地域、補足を確認。左右両表示の画像寸法・shadow・crop・重なりのCSSも同一でした。
- Chromeで計測した初期表示と全画像読込後のCLSは最大0。WebKitには同じ計測APIがないため、CLSを測定済みとはしていません。実機・実ユーザー環境での性能測定ではありません。
- Desktopの2組み合わせ、Mobile縦順、1024px Darkの画像を目視しました。ギガポケの注意書きはどちらの配置でも本文側に残り、画像とCTAの欠落・はみ出しはありません。

スクリーンショット：

- [Desktop：Uni:Note → ギガポケ → すわなび → SIGNAL](screenshots/chrome-seed-1-desktop.jpg)
- [Desktop：Uni:Note → オトミル → ギガポケ → ギャンカレ](screenshots/chrome-seed-11-desktop.jpg)
- [Mobile](screenshots/chrome-390-light.jpg)
- [Tablet 1024px・Dark](screenshots/webkit-1024-dark.jpg)

## 公開確認

- 実装コミット：`6d27733`。並行更新統合後の検証記録：`b8c485f`。mainへpush済みです。
- [Hugo CI](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34081222307)・[GitHub Pages配信](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34081255413)ともに成功。公開成果物のgh-pagesは`2e860118451ce5f2c77359ab06dc6d4393bd2104`です。
- 2026-09-07 12:56 JST、[全277 HTML URL](public-verification.json)がHTTP200・ローカルbuildとのSHA256完全一致でした。
- [本番ブラウザ](live-browser.json)でも通常の乱数で10回リロードし、10種類の異なる並びすべてでUni:Note先頭・重複なし・右→左→右→左を確認しました。390pxでは全4件が説明→画像の縦順です。
- [本番Desktop](screenshots/live-desktop.jpg)／[本番Mobile・通常viewport](screenshots/live-mobile.jpg)を撮影し、目視確認しました。
