# SIGNAL ガイド監査（2026-09-07）

## 現行確認

- プロジェクト: `/Users/yuya/Projects/signal`、HEAD `3cee564`、ローカル`pubspec.yaml` 1.1.1+1。
- 日本App Store公開版1.1.1と一致。`store-snapshot.json` を参照。
- AGENTS.mdとREADME全文を確認。アプリ側のソース・作業中差分は変更していない。
- `lib/presentation/home/home_screen.dart`: 初期TODAY、3タブ、右上Settings、15件ずつの追加表示、75/45件上限、refresh時に既存記事をfallbackへ渡す、同じfeedbackで取り消し。
- `lib/common/widgets/article_card.dart`: UIはGOOD/BAD文字ボタンではなくthumb-up/downアイコン、tooltipは「グッド」「バッド」。
- `lib/presentation/settings/settings_screen.dart`: テーマ、文字サイズ（記事）、記事取得サイト設定、チュートリアル、要望・お問い合わせ、学習データリセット（確認ダイアログ）。
- `lib/presentation/web/widgets/article_web_view_controls.dart`: 左上×、右上⋮に外部ブラウザ・共有・再読み込み。
- `lib/data/repositories/feed_repository_impl.dart`: 応答がない配信源は既存表示／メモリを維持。記事本文のオフライン保存ではない。

## 使用画像

`artifacts/app_store_screenshots_2026-09-03/source/ui_captures/` の raw 実画面を使用。マーケティング版・加工済みclean版は使っていない。元画像を目視し、コードの現行UIと一致する領域だけcropした。上部ステータスバーにある他アプリへの戻りリンク、他社記事の本文など操作に不要な領域は除外。UIの描画変更・生成・文字置換なし。

| 出力 | 元画面 | 採用範囲・用途 |
|---|---|---|
| tabs-and-article.png | today.png | 3タブ、設定入口、記事カード、反応ボタンを一度に説明 |
| article-menu.png | article.png | 閉じる／メニューボタン。記事本文は含めない |
| source-switches.png | settings.png | 記事取得サイト設定と2つの実スイッチ |
| text-and-theme.png | settings.png | テーマとSmall／Normal／Large |

画素座標・source/destination SHA-256は `signal-assets.json`。4枚ともcrop。全画面の縦長画像がなくても操作の位置関係が伝わるためFull Screenは使わなかった。今回の新規Simulator撮影は0枚。既存実画面が現行UIと一致したので再撮影は不要だった。

## 本文改訂

- 使い方の入口を初回チュートリアルの長い説明から、タブ→記事→配信源という通常操作へ変更。
- 旧GOOD/BAD表記だけでは画面のアイコンと対応しにくいため「カード右上のグッド／バッド」と画像で説明。
- 反応の再タップで取消、再読込後に表示傾向へ反映することを追加。直後の並び替えは約束しない。
- 文字サイズは記事ブラウザに適用されることを明記。
- FAQへ通信失敗時の表示維持、記事本文の非保存、段階表示の上限を追加。
- 「広告なし」はSIGNALの記事一覧とリンク先サイトを区別。
- テーマ、配信源、共有、リセットの操作をFAQへ重複掲載せず、使い方の該当アンカーへ直接リンク。
- 使い方の旧5アンカーを関連する新しい説明の直前に維持。FAQの旧見出し・IDも維持。正式URLは変更していない。
- 本文末尾のFAQ/Privacy重複リンクは削除。同じ正式URLへ共通の直下Supportリストから到達できる。
- 最終更新日は実際の改訂日2026-09-07。

## 限界

使い方の主要操作は画像で示した。チュートリアル再表示と学習履歴リセットは短い設定パスと注意書きに留める。現行ソースで確認済みだが、今回その2操作のSimulator画面は新規取得していない。
