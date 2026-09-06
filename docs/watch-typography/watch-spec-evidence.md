# すわなび Apple Watch 仕様の現行実装監査

確認日: 2026-09-07。対象: `/Users/yuya/Projects/smokeless`。この監査ではアプリのファイルを変更していない。

## 確認した版と公開状態

- コードの HEAD は `3e9e7f38a67f233c1bc4a18c6e56bb50693355d6`（2026-09-06、`feat: add Apple Watch recording for 1.2.0`）。`pubspec.yaml:22` は `1.2.0+3`。Watch の Release 設定も `1.2.0 / 3`（`ios/Runner.xcodeproj/project.pbxproj:1026,1036`）。
- 開始時の dirty files はリリース・素材・テストの文書、Watch scheme、未追跡 `design/`。これらを元に最新の素材を確認したが、上書き・コミットしていない。
- ユーザーの最新申告は「Apple Watch対応版を提出・審査中」。一方、ローカル `docs/RELEASE_NOTES_1_2_0.md:3` と `docs/APP_STORE_METADATA.md:182` は提出前の記録のまま。この差は**最新のユーザー申告を優先**する。提出済みであることと一般公開済みであることを分ける。
- このコード監査だけでは App Store 公開済みを確認できない。公開版の確認は別途 Apple の公開情報で行い、1.2.0 の公開が確認できるまでは Web で「審査中」「公開後に利用できる機能」と明示する。
- `build/ios/iphoneos/Runner.app/Info.plist` は古い `1.1.0 / 2`、`build/ios/iphonesimulator/Runner.app/Info.plist` は古い `1.1.1 / 2`。この場所の成果物は現在の提出バイナリの証拠に使用しない。

## 確認済み仕様とコード根拠

以下のパスは `/Users/yuya/Projects/smokeless` からの相対パス。

| 項目 | 現在の実装 | 根拠 |
|---|---|---|
| Watch の主要操作 | 左の緑ボタンが「我慢」、右の赤ボタンが「喫煙」。1タップで1件記録 | `ios/SmokelessWatchApp/WatchRecordingView.swift:34-54`、`WatchRecordingStore.swift:55-85` |
| 我慢の意味 | 吸いたいと思ったが吸わなかった記録。量の符号は我慢 `+1`、喫煙 `-1` | `PROJECT.md:13-20`、`WatchRecordingStore.swift:55-61`、`ios/Shared/WatchSyncModels.swift:25-27` |
| 当日の表示 | 各ボタンの中央に当日の件数を数字で表示。通常画面には「我慢」「喫煙」の文字ラベルや単位は表示しない | `WatchRecordingView.swift:72-102`、`WatchRecordingStore.swift:152-159` |
| 当日の集計 | iPhone から受け取った当日件数に、その日の未同期記録を加えた件数を表示 | `ios/Shared/WatchSyncModels.swift:182-203` |
| 記録日時 | タップ時点の日時を保存し、再接続時刻に置き換えない | `WatchRecordingStore.swift:69-85`、`ios/Shared/WatchSyncModels.swift:20-55` |
| 日付切替 | Watch がアクティブになったときと日付境界で再集計する。日付キーは Gregorian と現在のタイムゾーン | `WatchRecordingStore.swift:63-66,186-202`、`ios/Shared/WatchSyncModels.swift:168-179` |
| 未接続時の記録 | 権利確認済みであれば、iPhone 未接続でも記録を Watch の UserDefaults に一時保存し、件数へ即時反映 | `WatchRecordingStore.swift:24-47,69-85,171-183` |
| 再接続後 | Watch の起動・再接続等で pending を再送。WatchConnectivity の application context と到達可能時の message を使用 | `WatchRecordingStore.swift:63-66,96-115,205-233`、`SmokelessWatchApp.swift:12-15` |
| iPhone への受信 | iPhone の App Group 内 inbox に原子的に保存。UUID で重複排除し、通常の月別記録へ取り込む | `ios/Shared/WatchEntryInbox.swift:14-20,42-81`、`ios/Runner/WatchConnectivityBridge.swift:132-150`、`lib/features/root/root_page.dart:1130-1186` |
| iPhone 側の集計反映 | iPhone 側の当日集計と購入権利を Watch へ送る。遅れた古い revision で新しい表示を上書きしない | `root_page.dart:1036-1074`、`WatchRecordingStore.swift:118-144` |
| 利用条件 | 既存の「広告削除」または「銘柄追加パック」の購入特典。旧広告削除権利も対象 | `lib/features/settings/purchase/in_app_purchase_service.dart:9-49`、`root_page.dart:973-978,2089-2103` |
| 未購入時 | 通常の記録ボタンを表示せず、有料機能の案内を表示 | `WatchRecordingView.swift:6-13,105-117`、`ios/SmokelessWatchApp/ja.lproj/Localizable.strings:1-2` |
| 購入・復元 | iPhone アプリで行う。Watch 内の購入 UI はない | `settings_page.dart:1690-1739`、`WatchRecordingView.swift:3-118` |
| ペアリング | Watch は iPhone アプリの companion。iPhone 側は `isPaired` と `isWatchAppInstalled` を確認して送信 | `ios/Runner.xcodeproj/project.pbxproj:1031`、`WatchConnectivityBridge.swift:178-182` |
| 最低 OS 設定 | Watch target は watchOS 9.0、iPhone アプリ本体は iOS 14.0 | `project.pbxproj:1015,1046,1076`、`626,715,766` |
| 対象外 | Watch 側に履歴、編集・削除、グラフ、金額、累計、設定、文字盤コンプリケーション、Smart Stack Widget を持たない | `WatchRecordingView.swift:3-118`、`docs/FEATURE_APPLE_WATCH.md`「今回の対象外」 |

### 説明時の注意

- iPhone 本体の最低 OS `iOS 14` と、Apple Watch をペアリングするための Apple 側の対応 iPhone / iOS 条件は別。Web で「iOS 14 で Watch も利用可」とは書かない。Watch 側は `watchOS 9以降` とし、ペアリング済みの対応 iPhone が必要なことを記す。
- Watch 単独で初期の購入権利確認はできない。iPhone アプリを起動して購入済み権利を確認・同期した後に、未接続時の Watch 記録が利用可能になる。
- 同期はインターネット上のクラウド同期ではなく、ペアとなる iPhone と Watch の端末間同期。即時配送・常時リアルタイムは保証しない。
- コード上、Watch の pending からの削除は iPhone の永続 inbox に受領済み UUID が保存された確認後に行われる。通常の月別 Entry への取り込みはその後も行われるため、`docs/FEATURE_APPLE_WATCH.md` の「iPhoneが永続化済みUUIDを応答」はこの二段階を含む。一般向けには「再接続後、iPhoneへ同期」と短く記せばよい。
- 実機の Bluetooth / バックグラウンド配送、実 Store 購入・復元、提出済みバイナリ自体の再検証は今回行っていない。過去ドキュメントにある Simulator 確認と区別する。

## 最新素材

素材の管理元: `design/app-store-screenshots-2026-09-03/`。`docs/APP_STORE_METADATA.md:75-96,142-178` と `AUDIT_AND_PLAN.md:14,57,93-98` を確認。

| 用途 | 素材 |
|---|---|
| App Store iPhone欄の Watch 訴求（日本語） | `final/1284x2778-upload/07-watch.png` |
| Apple Watch欄の公式提出用に制作した訴求画像（日本語） | `final/apple-watch/422x514-upload/01-recording.png`、`02-counts.png` |
| 説明用の実画面（40mm） | `sources/ui/watch/recording-40mm.png` |
| 別サイズの実画面（Ultra） | `sources/ui/watch/recording-ultra3-422x514.png` |
| 繁体字・フランス語・韓国語 | `final/apple-watch/{zh-Hant,fr,ko}/422x514-upload/{01-recording,02-counts}.png`、各言語の iPhone 用 `07-watch.png` |

40mm の実画面および日本語の Watch 訴求画像を目視した。左緑が `3`、右赤が `2`、画面上部に OS 時刻を持つ現在の数字のみの UI。訴求画像は実画面の外に「我慢」「喫煙」の説明を配置し、有料機能の注記を保持している。

## 公開前の Web コピー案

Product の対応表示:

> iPhone / Apple Watch（審査中）

Hero 近くの補足:

> Apple Watch対応版は審査中です。以下は公開後に利用できる機能の紹介です。

主要 Feature:

> Apple Watchから1タップで記録。
>
> iPhoneを取り出さずに「喫煙」「我慢」を記録。当日の回数を手元で確認できます。
>
> Apple Watch機能は、広告削除または銘柄追加パックの購入特典です。

使い方への追記（「対応版公開後の操作」と明示する）:

1. ペアリング済みのiPhoneとApple Watchに対応版をインストールします。iPhoneのすわなびで購入済み権利を確認し、Watchアプリを開きます。未反映の場合はiPhone側で購入を復元します。
2. 左の緑ボタンをタップすると「我慢」、右の赤ボタンをタップすると「喫煙」を1件記録します。中央の数字はそれぞれ当日の件数です。
3. iPhoneが未接続でも、記録はWatchに一時保存されます。再接続後にiPhoneへ同期します。反映を確認するときは両方のアプリを開いてください。
4. 履歴やグラフの確認、記録の編集・削除はiPhone側で行います。

## このサブタスクの検証範囲

コード・文書・既存素材の読取のみ。アプリのビルド、テスト、Simulator起動、Store提出・変更は行っていない。ホームページ側の表示・URL・画像最適化検証はサイト実装側の記録を参照。
