# Founder人物イラスト追加（2026-09-07）

ユーザーが名刺の人物イラストを自作AI生成素材としてWeb利用許可したため、CompanyのFounderに追加しました。独立元素材は見つからず、名刺から人物のみをbuilt-in imagegenで抽出。編集指示と元ファイル情報は[asset.json](asset.json)に保存しています。名刺全体・電話番号・QRコード・他の文字は配信しません。

- 6言語共通のイラストと各言語のalt。
- 160×160 CSS px。Hugoで192／384px WebPを生成し、srcset・lazy・asyncと寸法指定を使用。
- Retina表示で384px画像が選択されることを確認。
- 既存のプロフィール文面・URL・問い合わせ先は維持。
- [build／URL互換性](build-verification.json)成功、warnings／errors 0。
- [Companyブラウザ検証](browser-verification.json)20条件成功（6言語、320／393／834／1280／1440px、Light／Dark）。画像欠落・横はみ出し・axe違反0。
- [画像表示](portrait-display.json)はDesktop／MobileのLight／Darkで確認。

画像追加後のLighthouseは再計測していません。前回レポートの100点は人物画像追加前の値です。

スクリーンショット：[Desktop](founder-desktop.png) ／ [Mobile](founder-mobile.png) ／ [Desktop Dark](founder-desktop-dark.png) ／ [Mobile Dark](founder-mobile-dark.png)

公開：実装コミット`5f1c06d219742e45dc51523494cb7b237cc7b7bb`をmainへpushし、[Hugo CI](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34052011274)・[Pages](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34052030692)が成功。[公開URL検証](public-verification.json)で277件すべてHTTP 200・ローカルbuildとSHA256一致を確認しました。

[本番アセット](public-assets.json)も人物WebP192px／384pxとCSSの3件すべてHTTP 200・SHA256／byte数一致。人物画像は通常4,700bytes、Retina10,896bytesです。
