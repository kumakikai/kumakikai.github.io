# 実画面ガイドの監査記録

対象は既存8アプリの使い方22ページとFAQ22ページ。公開URLを変更せず、操作手順は使い方、条件・問題・例外はFAQへ整理します。

## 根拠の順序

現在の実装・現在のUIを確認し、最新のプロジェクト文書、App Store metadata、既存Web本文の順に照合します。ローカルの新しいUIが公開版に含まれるとは限らないため、`store-snapshot.json` と照合し、公開前の画面はガイド上で明示します。

各担当の監査記録に採用した実画面の出典、SHA-256、crop範囲、照合した実装、変更した旧仕様を記録します。マーケティング画像を操作用と混同せず、画面内のUIを描き変えません。

## 共通表示

`guide-image` shortcodeはHugoの画像処理でWebPを生成します。cropは最大560px、iPhone全画面は320px、iPadは760px。1x/2xのレスポンシブ画像を生成し、元画像以上には拡大しません。本文の画像リンクから大きな画像を開けます。`width`/`height`、`loading="lazy"`、`decoding="async"`、操作対象を示すaltを共通に設定します。Webの実装方法は[Hugoの画像処理](https://gohugo.io/content-management/image-processing/)に従います。

長いガイドの目次はMarkdownのh2から生成します。JavaScriptを追加せず、更新日も既存Markdownの`lastmod`から表示します。日本語の禁則・語句境界処理は既存の共通組版を利用します。

## 既存本文の保護

`docs/migration/baseline.json` は変更しません。今回明示的に改訂する使い方・FAQのみ、`reviewed-content.json` に元本文とレビュー後本文、MarkdownのSHA-256を記録します。`verify-migration.py` は、この44ページ以外の本文変更や、正式URL、canonical、アンカー、画像・リンクの破損を引き続き検出します。

`record-guide-review.py` は内容確認後の記録用で、CIには組み込みません。改訂後に基準を自動追従させる仕組みではありません。

## 検証の区別

アプリ実装の照合、Simulatorでの画面取得、Webのproduction build、実ブラウザ表示、GitHub PagesでのHTTP確認を分けて報告します。ブラウザのviewport検証は実機操作の代わりにはなりません。画像が読めるか、文章と操作対象が対応しているかは、機械チェックに加えてスクリーンショットを目視確認します。
