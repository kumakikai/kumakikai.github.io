# オトミル・ギガポケ・Nocca 実画面ガイド監査

確認・更新日: 2026-09-07（JST）

## 対象と公開状態

| アプリ | 既存URL（変更なし） | 確認した版・公開境界 |
|---|---|---|
| オトミル | `/htu/oto-miru/`, `/faq/oto-miru/` | 現在のローカル1.1 / Build 1。日本Storeの公開版は1.0.1。ガイド冒頭に「最新の提出用素材と開発版で確認した画面」と明記。 |
| ギガポケ | `/htu/giga-poke/`, `/faq/giga-poke/` | 現在の実装と公開版0.1.0。旧 `/htu/povo-manager/`, `/faq/povo-manager/` aliasesも維持。 |
| Nocca | `/htu/nocca/`, `/faq/nocca/` | 未公開・開発中の現在のiPhone実装（ローカル0.0.1 / Build 1）。公開済みとして案内しない。 |

日本Storeの取得結果は `store-snapshot.json`。ユーザーはオトミルの最新審査提出素材を優先するよう指示しているが、アプリ側 `docs/APP_STORE_METADATA.md:63` は「ローカル更新、App Store Connectの新バージョン作成・提出・公開は未実施」と記載している。今回、提出済み・公開済みを独自に断定しない。現行ローカルUIと公開版の違いをガイド・FAQ冒頭に示した。

ソースの取得時点: オトミル `cf7f50bc90f6007a303acc439fef2b276399d246`、ギガポケ `141aa9a845fdc5b4096191c6755c4161144ed25d`、Nocca `46a58d754b02d0eda21b958c99f893fa344e29cd`。未コミットの実装も含むため、commit hashだけを撮影版の完全な識別子とはしない。原プロジェクトは編集せず、ビルド・追加UIテストは `/private/tmp/homepage-guide-*-source` の一時コピーで行った。

## 現在の実装と照合した内容

### オトミル

主な根拠: `OtoMiru/App/AppModel.swift`, `Views/RootView.swift`, `Views/SettingsView.swift`, `Services/SpeechRecognitionService.swift`, `Services/DeviceSupportPolicy.swift`, `Services/DisplaySettingsStore.swift`, `docs/FEATURE_DEVICE_SUPPORT.md`, `docs/APP_STORE_METADATA.md`。

- iOS / iPadOS 26以降、日本語の `SpeechTranscriber` が利用できる端末。**Apple Intelligenceの有効化は必須ではない**。旧ガイド・FAQの必須表現を訂正。
- 2026-09-06の現行ソースには旧 `gpt-live-transcribe` / OpenAIの音声送信・高精度engineの実装は残っていない。`highAccuracy`の残りは `DisplaySettingsStore.swift` の旧同意キー削除のみ。現行の `SpeechRecognitionService` はApple Speechを使用。単なるfeature flagによる非表示ではなく、廃止された実装を案内から除外している。
- `docs/APP_STORE_METADATA.md:110,124,140` は旧AI画像を `historical/retired_ai_2026_09_06` に隔離し、Free + Plusのみ掲載するよう明記。過去のAI/Pro/追加パックの文書や画像を採用しない。
- シンプルモードはテレビ・会話・グループの3ボタン。通常モードには映画もあり、選択して「字幕をはじめる」。字幕停止・反転の実際のボタンを説明。
- 設定の正規UIは `表示 > 高齢者向け`。字幕サイズ、テーマ、`音声の聞き取り（感度調整） > 周囲の環境`を実画面付きで案内。
- 初回のモデル準備後は端末内の音声認識を使用。音声・字幕本文を保存しない仕様は、現在のソースとmetadata双方に整合。
- Freeは1日15分、広告で5分追加・1日3回まで。Plusは無制限・広告なし・Family Sharing。旧「1ヶ月トライアル」と固定価格の案内を除き、現在の購入画面へ委ねた。認識engineはFree / Plus共通。
- 購入復元は購入画面の操作であるため、設定に直接存在するような説明を修正。

### ギガポケ

主な根拠: `App/RootView.swift`, `App/AppModel.swift`, `App/CodeEditorView.swift`, `App/PovoCodeDetailView.swift`, `App/SettingsView.swift`, `Shared/PovoCodeParser.swift`, `WidgetExtension/PovoCodeWidget.swift`, `WidgetIntents/CopyGigaCodeIntent.swift`、現在のmetadataとUIテスト。

- povo 2.0向けの非公式アプリ。メールの選択範囲からペースト・共有、または手動で登録する3経路を整理。
- ペースト後の実際の確認画面を取得。実在しない `DEMO-0000-0002` と期限を入力し、特典・コード・期限を確認して登録する流れを説明。
- ギガコードは特典内容・コード・期限が必要。外部特典は特典内容とコードまたは受取URLが必要で、期限は任意。不足情報を推測しない。OCR・QR読み取り・自動取得機能を追加しない。
- 一覧はギガコード / 外部特典を分けて期限順。povo 2.0へは通常起動し、コードをコピーするだけで、自動入力や外部での利用完了確認はしない。
- 使用時の自動ゴミ箱移動と、期限翌日以降の起動・再表示時の整理を区別。復元・個別削除・通知日選択・自動削除設定を短い手順にした。
- ウィジェットは小1件・中最大3件のギガコード。コード文字列・外部特典を表示せず、タップしてアプリ側で最新状態を確認してコピーする仕様を維持。
- 旧Webの主要機能はおおむね現行に一致。冗長な登録・通知操作をFAQからガイドへの直接アンカーへ集約。

### Nocca

主な根拠: `Nocca/ContentView.swift`, `Nocca/NoccaState.swift`, `Nocca/NoccaApp.swift`, `Nocca/NoccaBackendCoordinator.swift`, `Nocca/DebugEnvironment.swift`, `docs/FEATURE_FREE_TALK.md`, `docs/FEATURE_SUBSCRIPTION.md`、現在のUIテスト。

- iPhone / iOS 17以降、日本語。公開前であることは維持しつつ、古い「同期・Push・招待管理は未実装」というプロトタイプ時点の説明を更新。
- 本人が招待し、家族が招待コードを入力してリクエスト、本人が承認する流れ。以前の家族側から本人を招待する導線は現在のUIにないため案内しない。
- 家族の返信は「対応」「完了」の2段階。旧一段階の返信スクリーンショットを不採用。
- 本人の「送った意思表示」は **意思表示タブ上部**。返信と取り消し操作をこの位置で案内する。`つながり`は接続・通信状態を見る場所として区別。
- 自由文の会話は本人が開いたときだけ。本人側の閉じるボタン、家族側の前回の会話の読み返し、会話リクエストは初期無効という条件を説明。
- 通信休止、家族管理、会話リクエスト、引き継ぎコード・データ管理の主要操作を追加。
- 同期・Push・データ削除は現在の実装に存在する。実サーバーでの疎通確認とは区別し、今回は画面とコードの確認まで。
- `docs/FEATURE_SUBSCRIPTION.md` の2026-09-07確定仕様を優先。初回の家族承認から7日間、その後は同じNocca Familyの有効契約が必要。Apple Family Sharingとは別の仕組み。FAQには公開前の条件として短く記載し、未確定の価格表を作らない。購入テストは行っていない。

## 画像の選び方と取得

全21点のソース、SHA-256、出力SHA-256、crop矩形は `communication-codes-assets.json` に記録。

| アプリ | 採用画像 | 取得元 |
|---|---|---|
| オトミル | 7点（すべて必要部分のcrop） | 現行9/6 rawから3点、追加Simulator撮影から4点 |
| ギガポケ | 7点（すべて必要部分のcrop） | 現在のアプリをビルドし、新規Simulator撮影 |
| Nocca | 7点（crop 5点、全画面2点） | 現在のアプリをビルドし、新規Simulator撮影 |

- オトミルの既存rawは `tmp_appstore_screenshots/refresh_2026_09_05/raw/iphone/`。訴求文を載せたmarketing完成画像ではなく、その元になった実UIを使用。旧AI切替入り画像は不使用。
- ギガポケは特典一覧・ボタン・ペースト確認・ゴミ箱・設定。確認画面の上部と入力項目を残し、不要な空白を除いた。手入力の編集画面は同じ項目が続くため、ガイドでは重複表示せず、未使用の新規画像を削除した。
- Noccaは役割選択、本人の招待、意思表示、返信と取り消し、家族返信、会話、休止。招待と会話は上部の操作と下部の操作の関係が重要なので全画面を採用。
- Noccaの既存テストfixtureでは送信が未ack状態、会話が空だったため、その画像は採用しない。ユーザーが許可した最小限の架空データとして、一時コピーのDEBUG fixtureに2文の会話と送信済みIDを設定。View・操作・機能の実装は変更しない。実サーバー同期の成功を示す画像ではない。
- 字幕は既存の `captioning.sampleText` で操作説明用の文章を設定。実際の認識精度の実証として扱わない。
- 画像編集はImageMagickによるcropとmetadata除去だけ。UIの描画・文字変更・AI生成・スクリーンショットの合成はしない。
- iPhone 17e / iOS 26.5、1170×2532で撮影。9:41表示、充電状態を固定。今回作成した専用機 `55CD043A-FB15-4F52-B0ED-5E2263FE527E` は撮影完了後shutdown済み。他作業で使われていたSimulatorには触れていない。

## ビルド・撮影の記録

3アプリは現在のソースでSimulator Debug buildが成功。追加撮影は一時コピーの既存XCUITest targetから行った。

| xcresult（`/private/tmp/`） | 結果 | 用途 |
|---|---|---|
| `homepage-guide-oto-capture.xcresult` | 1 test passed / 19.65s | 表示設定・聞き取り環境・正立字幕 |
| `homepage-guide-oto-home.xcresult` | 1 test passed / 10.876s | 通常モードの開始ボタン全体 |
| `homepage-guide-giga-capture-final.xcresult` | 1 test passed / 54.83s | 一覧・利用・ゴミ箱・設定 |
| `homepage-guide-giga-paste.xcresult` | 1 test passed / 75.007s | 実際のペースト確認画面 |
| `homepage-guide-nocca-capture-final.xcresult` | 1 test passed / 48.886s | 役割・招待・家族返信・休止ほか |
| `homepage-guide-nocca-filled.xcresult` | 1 test passed / 25.445s | 返信状態・会話のデモデータ入り画面 |

撮影前の試行で、ギガポケの画面遷移途中の画像と、Noccaで条件コンパイルにより0件実行だった結果は不採用。上表は、各対象テストが実際に1件走り、画像を目視した最終結果のみ。画面遷移後には短い待機を入れた。Xcodeのdebugger version / Accessibility loader警告は出たが、最終テストと画像取得は成功した。

添付の取り出しは `xcrun xcresulttool export attachments --path <result>.xcresult --output-path <directory>`。これはUI撮影の検証で、実音声認識、外部特典利用、本番サーバー・Push、StoreKit Sandbox / 実課金、実機動作やApp Store審査通過の証明ではない。

## FAQ・URL・本文の整理

- FAQの基本操作は該当ガイドの直接アンカーに集約。問題・条件・例外はFAQ側へ残した。
- 末尾のFAQ / Privacy / Termsの重複リンク一覧は、共通Supportリストと重なるため除去。本文内の必要なFAQリンクと正式本文URLは維持。
- 6ページすべての `lastmod` を実際の更新日へ更新。
- 旧見出しを変更・統合した箇所には `guide-anchor` を設定。baselineの旧IDは6ページとも生成HTML内に存在することを確認（不足0）。
- 法務本文・Press Release・既存App Store Connect関連URLは変更しない。
- 共通 `guide-image` が1x/2x WebP、適切な最大表示幅、lazy / async、width / height、alt、拡大リンクを提供。原PNGをそのまま巨大サイズで通常配信しない。
- Webの全体build、Mobile / Desktop / Light / Dark、broken imageとURL検査はroot側の統合検証結果を参照。

## 残る範囲と別途確認事項

- ギガポケのiOSウィジェット追加操作は短い2段階の文章案内。OSのウィジェット選択画面は今回新規取得していない。アプリの主要操作7点は実画面で案内済み。
- Noccaの引き継ぎ・削除は安全上必要な短い案内を追加したが、それらの個別確認画面は載せていない。役割・接続・通信の通常操作を優先。
- オトミルの最新ローカル1.1素材とApp Store公開1.0.1の境界は上記の通り。実際の提出状態は別途App Store Connectで確認が必要。
- Noccaの **`content/privacy/nocca.md:32–34`** に「正式なアカウント、端末間同期、Push通知、招待リンクの有効期限管理は未実装」、将来提供時の更新という旧説明が残る。**`content/terms/nocca.md:77`** もサーバー同期等を将来条件として記載。**Privacyの課金節**も初期設計の未確定表現があり、現在の`FEATURE_SUBSCRIPTION.md`と版が異なる。今回はガイド・FAQ担当の権限内で法務本文を独自に改定せず、原URLと本文を保持。公開前に現在のサーバー保存・削除・契約条件と法務文書を別途合わせる必要がある。
