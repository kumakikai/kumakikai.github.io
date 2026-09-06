# 日本語Typographyのブラウザ検証

最終版のChrome検証は **63条件すべて成功**。43条件でaxeを実行し、違反はありませんでした。別途、Aboutの6言語それぞれでDesktopとJavaScript無効時を確認し、12条件すべて成功しています。

- [Chromeの全測定値](browser-verification.json)
- [Aboutの6言語・JavaScript無効時](company-compatibility.json)
- [変更前の実改行](typography-before.json)
- [WebKit実エンジンの別検証](webkit-verification.json)

## 確認範囲

Aboutは1440・1280・834・393・320px。HomeとUni:Note詳細も同じ5幅で確認しています。Products一覧、全8Product、News、Support互換ページ、Uni:Noteの使い方・FAQ、ギガポケ発表記事は1440・393pxで確認しました。Newsは320pxも追加し、意味のまとまりを指定した既存記事6件の見出しは393・320pxで確認しています。

About、News一覧、既存記事6件では、`auto-phrase`が適用されている要素だけを一時的に`normal`へ戻し、未対応環境向けの表示も検証しました。ContactやAbout Heroに明示した`keep-all`は維持しています。これはChrome上のfallback確認であり、WebKitの実行結果とは分けて記録しています。

## 改行の変化

`｜`は実ブラウザで折り返した位置を示します。本文中に挿入した文字ではありません。

| 場所 | 変更前 | 変更後 |
| --- | --- | --- |
| About冒頭、1440/1280px | 身近な不便から、使える道｜具へ。 | KUMAKIKAIについて（1行） |
| Contact本文、1440/1280px | …メールでご連絡ください。ア｜プリの使い方や… | 問い合わせ依頼とアプリサポート案内を別段落に整理。各段落とも1行 |
| About Hero、393/320px | 未対応環境では意味の途中で折り返す場合があった | 日常の「こうしたい」を、｜アプリに。 |
| Contact補足、393/320px | 文章変更だけでは「各プ｜ロダクト」「くだ｜さい」が残った | アプリの使い方や不具合のご相談は、｜各プロダクトページのサポートへ。 |
| Newsの長い記事タイトル | 未対応環境では「累｜計収益」などに分かれた | 「累計収益が」などを意味のまとまりとして保持 |

DOM Rangeで文字ごとの描画位置を取得し、見出しとContact本文の実際の行を記録しています。最終版の863見出し観測では、`Intl.Segmenter`で抽出した日本語の単語内部に行境界が入る候補は0件でした。機械判定は万能ではないため、About・Contactの画像と実際の行テキストも確認しています。

最後に旧記事本文のh2で見つかった7件の折り返し観測は、対象4条件だけを再実行して解消を確認しました。記事本文の文字と見出しIDは変更していません。63条件のJSONには、初回検証と変更対象だけの再検証を`verificationPasses`として分けて記録しています。

## スクリーンショット

| 場所 | Desktop | Mobile |
| --- | --- | --- |
| About | [変更後](screenshots/about-desktop.jpg) | [変更後](screenshots/about-mobile.jpg) |
| Contact | [変更後](screenshots/contact-desktop.jpg) | [変更後](screenshots/contact-mobile.jpg) |
| About・変更前 | [変更前](screenshots/about-desktop-before.jpg) | [変更前](screenshots/about-mobile-before.jpg) |
| Contact・変更前 | [変更前](screenshots/contact-desktop-before.jpg) | [変更前](screenshots/contact-mobile-before.jpg) |

実機のiPhone/iPadでの確認ではなく、各画面幅を設定したブラウザ検証です。実際の公開サイトのHTTP確認は、このローカル表示検証とは別に行います。
