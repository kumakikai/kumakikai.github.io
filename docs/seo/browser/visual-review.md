# SEO変更後のブラウザ回帰確認

`verify-browser.cjs` の既存39ケースと、末尾の操作検証はPASS。CSS・JavaScript・デザインの変更は行っていません。

- Home / Products：1440px・393px、Light / Dark。
- 全8 Product / About / News / Uni:Note Guide・FAQ / ギガポケPress Release：1280px Light・393px Dark。
- 英語・韓国語・ドイツ語・繁体字・フランス語Home：393px Light。
- メニューのフォーカス制御・Escape・背景スクロール・各リンク遷移・テーマ保持・Productから直接Support/Guideへ進む導線・旧互換Support/Privacy・JavaScript無効時を既存テストで確認。
- 全39ケースで横overflow・画像切れ・JS/HTTPエラー・axe違反・見出し飛び・重複IDは0。

目視ではHomeのDesktop/モバイルHero、Dark全体のFeatured交互配置、Productsのモバイルカード、Uni:Note Hero、5言語Homeの更新したAbout紹介文、FounderのDesktop/モバイルを確認しました。余白、画像、CTA、ナビゲーションのSEO変更による回帰は見つかりませんでした。

韓国語の新しいHome紹介文のみ、393pxで中点が次行先頭に来る折り返しがありました。同じ意味の接続表現（「기획하고 개발하며 운영합니다」）へ変更し、再build後の393px実画面で読みやすい折り返しと横overflow 0を確認しました。`korean-copy-recheck.json` と `home-about-ko.png` はこの修正後の記録です。39ケースの全体実行は、この韓国語1文の微調整前の記録です。

本記録はローカルproduction生成物のブラウザ確認です。本番配信・Google index・順位の証明ではありません。
