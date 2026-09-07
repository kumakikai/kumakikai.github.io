# News empty state — 最終リリース監査

## 修正前の再現結果

2026-09-07に、本番 `https://kumakikai.github.io/news/` とローカルproduction生成物を実Chromeで比較した。

- 通常のCSS読込後：初期の「すべて」には15記事が表示され、empty stateは見えない。Informationを選択したときだけ0記事となり、empty stateが見える。
- 本番6言語、1440px / 390px、JavaScript有効 / 無効の24ケースでも上記を確認した。カテゴリー選択後の「すべて」への復帰、`#information` の直接アクセスも正常だった。
- 一方、CSSの取得を遮断すると、15記事と「このカテゴリーの記事はまだありません。」が同時に表示された。
- 原因はempty stateの `<p>` がHTML上では非表示指定を持たず、CSSの `display:none` だけに依存していたこと。通常のブラウザ表示での不具合は再現していない。CSSを評価しない外部テキスト抽出には当該テキストが含まれ得る。

証拠：`news-before-live-chrome.json`、`news-before-unstyled.json`。

## 最小修正

`layouts/_partials/news-items.html` のempty stateにHTML標準の `hidden` 属性を追加した。既存のカテゴリー選択用CSSは、該当カテゴリーが選択された場合だけ `display:block !important` にする。Tailwind preflightが `@layer base` 内で `[hidden]` に `display:none !important` を指定するため、選択時のセレクタだけ同じ `base` レイヤー・同じ優先度で上書きする。通常のunlayered CSSに `!important` を付けるだけではCSSレイヤー順位により選択時も隠れたままになることを実ブラウザで確認し、この限定上書きへ修正した。本文・デザイン・分類・記事URL・JavaScriptは変更していない。

これによりCSS未取得でも初期empty stateは非表示になる。CSS読込後は引き続きCSSだけでカテゴリー切替が動作する。HTMLやCSSの意味を無視する外部抽出器が文字列を返すことまで制御する変更ではない。

## 検証方法

`scripts/verify-news-release.cjs` を使用する。各ブラウザで6言語 × 1440px / 390px × JavaScript有効 / 無効 = 24ケース。

各ケースで、初期のfragmentなし、Press Release、Blog、Information、「すべて」へ復帰、Information fragment直接アクセスを検証する。表示記事数とempty stateの可視性に加え、アクセシビリティツリーとの一致、横overflow、ブラウザ実行エラーを確認する。修正後はCSS取得を遮断した初期表示も確認する。

この検証はブラウザviewportによる表示確認であり、実機の検証ではない。

## 修正後ローカル結果

Chrome 24ケース、WebKit 24ケース、計48ケースすべてPASS。6言語とも初期・すべてへの復帰ではempty stateなし、0件のInformation選択時だけ表示される。JavaScript無効時の操作とfragment直接アクセスも一致した。全48ケースでCSS取得を遮断しても初期empty stateが視覚・アクセシビリティツリー両方から隠れることを確認した。

証拠：`news-local-chrome.json`、`news-local-webkit.json`。通常表示と0件カテゴリーのDesktop / Mobile画像は `screenshots/news-local-*.jpg`。
