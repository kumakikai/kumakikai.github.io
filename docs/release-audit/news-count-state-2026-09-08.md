# News空状態の件数判定

## 確認した状態

2026-09-08、変更前の本番を直接取得し、ブラウザでもAll → Information → Allを操作した。Allは15件、Informationは0件で、今回の取得では報告されたAllの誤表示自体は再現しなかった。

一方、既存実装はビルド時に空と判定した個別カテゴリーのメッセージだけ生成し、CSSで`hidden`を上書きしていた。記事の絞り込み結果と空状態を実行時に共通判定しておらず、全記事0件のAllにも対応していなかった。既存回帰テストもAllを0件判定から除外していた。

## 変更

- `news-items.html`は空状態を1要素に統一。初期Allが0件の場合だけHTML上でも可視にする。JS無効時のため、同じ記事集合から空カテゴリーを算出する。
- `site.js`は初期実行と`hashchange`で選択カテゴリーに一致する記事を数え、記事と空状態の`hidden`を同じ処理で更新する。Allは全件、不明・不正なfragmentはAll。既存ハッシュURLとブラウザの戻る操作を維持する。
- JS初期化後はCSSによる表示上書きを止める。JS無効時は従来の`:target`によるフィルターを維持する。余白・配色・一覧・カテゴリーUI・本文・URLを変更しない。
- 運用ガイドと既存News回帰テストを更新。結果件数だけでなく記事のカテゴリーも待ち合わせ、同件数のカテゴリー間で切り替え完了を正しく検証する。

## 検証結果

production build、`npm run verify`、`npm run verify:seo`、サイト構造検証、`git diff --check`は成功。282 HTMLでエラー・警告、内部切れ、無効アンカー、重複ID、索引対象の孤立ページは0。

Chromeで全6言語の実記事 × PC 1440px / Mobile 390px × JS有効/無効の24条件と、日本語の全記事0件・Information記事ありの8条件を検証した。初期・各カテゴリーへの直接URL・連続切替・同カテゴリー再選択・キーボード・Back・不明/エンコード済みfragment・CSS未取得時・アクセシビリティ・横overflow・JavaScript/consoleエラーを確認した。

実記事はAll 15件、Press Release 8件、Blog 7件で空状態なし、Information 0件で空状態あり。全記事0件ではAllを含む全カテゴリーで空状態あり。Information記事ありでは空状態なし。実行中のフィルターで記事集合・タイトル・URLが変わらないことも確認した。初回32条件中、同件数のカテゴリーを切り替える1条件でテストの待ち合わせ不足を検出し、テストを補強して該当fixtureの4条件を再実行、全条件が成功した。

`verify-company.cjs`のNews日本語PC・Mobile・JS無効の3条件も成功し、既存選択スタイル・キーボード・戻る操作を確認。PC/MobileのAllとInformationを実視し、全6言語の15記事のHTMLが変更前成果物と一致することを別途確認した。WebKitの自動実行は必要なブラウザ実行ファイルが未導入のため未実施。依存は追加していない。

今回の実行ログは`/tmp/news-empty-20260908-combined.json`（32条件の最新結果）、`/tmp/news-empty-20260908-final/`、`/tmp/news-empty-20260908-recheck/`、`/tmp/news-empty-20260908-company/`、`/tmp/news-empty-20260908-structure/`。過去の監査証跡は上書きしていない。ブラウザviewport検証であり、物理端末の検証とは区別する。
