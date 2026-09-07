# Uni:Note / Uni:Note Pocket — Phase 1 文書統一前監査

監査日: 2026-09-08。アプリ・サイト本文は読取専用。検索エンジン、ChatGPT の公開ページ取得、旧監査の結論を現状の証拠として用いていない。以下のアプリパスは `/Users/yuya/Projects/uni_note/`、Pocket パスは `/Users/yuya/Projects/uni_memo/` からの相対パス。行番号は今回読んだ未コミット変更を含む作業ツリーに対応する。実装があることは公開版で利用できる証拠ではない。

## 1. 現在の調査範囲

| Repository | Branch / HEAD | 開始時の作業ツリー |
|---|---|---|
| homepage | main / `3ab462d3d03247df33420f0657cda305470d8e0b` | `.DS_Store` のみ untracked |
| uni_note | main / `b6aa55ab5213991147e90e4b20feeb56c0699455` | AppSessionStore、問題集、ReviewPrompt、UI、DB、各言語、project、tests、docs、artifacts 等の既存変更あり。すべて保持 |
| uni_memo | main / `1f856cfcf3805a529df5fa39dfd03d69b3a66501` | CHANGELOG_AI、APP_STORE_METADATA、RELEASE_CHECKLIST、TRANSLATION_MATRIX と artifacts の既存変更あり。すべて保持 |

`docs/WEBSITE_MAINTENANCE.md` を正本として適用。2製品それぞれ `content/{privacy,faq,htu}/uni-note*.md` の実在する ja/en/de/fr/ko/zh-hant を確認した。各製品18文書、計36文書。Privacy12、Guide12、FAQ12。両製品の独自Termsは未設置（0）。`data/apps.json` の両製品 support に termsURL はなく、共通 Apple Standard EULA が現行 fallback。

全8製品のうち独自Termsがない5製品は Uni:Note、Uni:Note Pocket、Balance Calendar、Smokeless、Signal。現在 `content/terms/` の正式本文は Nocca / GigaPoke / OtoMiru の日本語3件のみ。独自Terms新設は現行説明の修正と区別して扱う。

## 2. Uni:Note の実装で確認した情報フロー

| 機能・目的 | 情報 / 処理先 | 一次根拠 |
|---|---|---|
| 通常のノート保存 | 教科・ノート・ページDB、手書き、画像、PDF、付箋、録音、サムネイルを Application Support に保存 | `Persistence/AppSupportDirectory.swift:81–125`、`Persistence/DatabaseManager.swift:374` |
| 音声・文字起こし | 音声と標準文字起こしJSON/差分を recordings 配下に保存 | `Persistence/LectureRecordingFileStore.swift:24–91` |
| 写真・カメラ・PDF | ユーザー選択資料の貼付、書類写真、PDF出力がある。カメラ/マイク/音声認識の目的を permission 文で説明 | `App/Info.plist:31–36`、`content/htu/uni-note.md:49–63` |
| 文字起こし | Apple SpeechTranscriber / SpeechAnalyzer。対応言語/モデルを確認し、必要時に音声モデルをダウンロードする | `App/RealtimeLectureTranscriptionController.swift:772–839`。独自音声アップロード処理とは別 |
| AI画像解析 | 選択部分の imageBase64、画像形式、問題種別等を AWS proxy へ | `App/ProblemAssistOCRService.swift:382–425` |
| AI解答 | OCRテキスト、プロンプト、必要な画像・layoutContext、言語等を AWS proxy へ | `App/ProblemAssistSolverService.swift:1940–1949,1982–2025,2046–2049` |
| 問題集AI | 対象ページからのOCRテキスト等を refinement / question generation のpayloadとして送る | `App/ProblemSetGenerationAI.swift:850–869,928–974` |
| 録音AI要約 | transcriptText に加え recordingSessionId、recordingId、recordingIds、言語、目的、任意title/notebookName/sectionDate等を送る。結合した transcriptText 自体にも録音タイトル・ID・日時を付ける | `App/LectureAISummaryService.swift:721–739,840–847`。音声ファイルをこの要約APIへ送るpayloadはない |
| AIリクエストの識別 | userId、署名済AppTransaction、署名済Premium取引、clientRequestId、feature/operation/payloadを送る | `App/AIProxyClient.swift:113–122,199–207` |
| ユーザーID | `appstore:` + AppTransactionID。appAccountTokenはAppTransactionIDから導出したUUID。直接氏名を入力する会員アカウントとは別の継続識別子 | `App/AIProxyClient.swift:912–930`。匿名・識別不能とは呼べない |
| AI事業者 | AWS Lambda proxy から Google Gemini の `generativelanguage.googleapis.com/...:generateContent` へ POST | `aws/lambda/aiProxy/src/providers/gemini.ts:123–140` |
| AI生成結果のキャッシュ | AWS DynamoDB の aiRequest 行に成功レスポンス（生成結果を含む）を保存。入力そのものはこの行/台帳へ保存しない設計でも、結果中に入力由来情報が入りうる | `aws/lambda/aiProxy/src/index.ts:1366–1370,1405–1443,2097–2100`、同 README:93 |
| キャッシュ保持設定 | expiresAt の既定は24時間後、予約の既定は15分。環境変数で上書き可能。これは削除実行完了時刻の保証ではない | 同 `index.ts:229–230,2028–2029,2057–2067` |
| 購入・残量台帳 | transactionId、productId、数量、付与量、AppStore環境、AppTransactionID、appAccountToken、元取引ID、購入時刻、検証ハッシュ、付与時刻をDynamoDBへ保存。残量/購入/消費/返還等の台帳 | 同 `index.ts:1661–1745,2685–2707`。取引/残量/ledger行に上記キャッシュTTLを適用するコードはない |
| サーバー診断 | requestId、userHash、feature/operation、処理状態、provider/model、token数、見積費用、残量消費等 | 同 `index.ts:3479–3511` |
| サーバー保護 | PITR、削除保護、TTL、CloudWatch alarms、任意バックアップを設定するスクリプトあり | `aws/scripts/ensure-ai-balance-protection.sh:14–16,55–66`、proxy README:121。現在の本番設定値とは断定しない |
| Crashlytics | Firebase Core / Crashlytics をリンクし、診断の固定キー・分類・サニタイズ済NSError等を送る | `UniNote.xcodeproj/project.pbxproj:575–576,1251–1259`、`App/AppDiagnostics.swift:587–664,1799–1809` |
| 広告/Analytics | 現ターゲットのFirebase製品はCore/Crashlytics。Google Analytics events / 広告SDK利用は見つからない | 同projectとApp全文検索。OSやストア側の診断まで「情報を一切取得しない」とは断定しない |
| ファイルバックアップ | zipの任意保存先。録音音声は includeRecordingAudio を明示したとき含む（既定false） | `Backup/BackupManager.swift:625–639` |
| かんたんバックアップ | 共有iCloudコンテナに `Documents/UniNote/SystemBackup/latest.zip` を更新/復元。ノートのリアルタイム同期ではない | `Backup/BackupManager.swift:214–216,657–720`、`App/UniNote.entitlements:7,15` |
| 削除・復元 | 教科/ノートはsoft delete→ゴミ箱。完全削除と、30日経過対象のpurgeがある。起動処理がpurgeを呼ぶ | `Persistence/DatabaseManager.swift:2186,2298,3747–3789,3911–3926`、`App/AppBootstrapper.swift:606` |
| お問い合わせ | フォーム/メール/サポート情報コピー。コピーはユーザー操作でクリップボードへ | `UI/SettingsViewController.swift:3698–3718`。お問い合わせの送信者情報/自由記入はノートの通常保存とは別に説明が必要 |

### 課金・アカウントについての確定範囲

- Premiumは実UIで買い切り表示（`ja.lproj/Localizable.strings:513,638`）、SKU `jp.uninote.app.fullunlock`（`App/PremiumAccessController.swift:713`）。StoreKit購入/検証/復元経路あり（同:965–975、`Transaction.currentEntitlements`:888付近）。
- AI残量4商品は追加購入。SKU定義同:185–190、署名取引とappAccountTokenの付与・サーバー付与確認は:997–1034。ローカルStore提出説明も消費型と記載（`docs/APP_STORE_METADATA.md:703,717,732,747,762`）。価格や現在販売可能かはコードだけでは確定しない。
- legacyの月/年サブスク型やSKUは残るが、現 `purchaseAISubscription` は unavailable を返す（:990–995）、取得商品はfullunlock + AI残量（:1183）。これだけを根拠に「サブスクリプションを提供」と書かない。
- Premium用月次付与残量と購入残量はバックエンドで別管理（`index.ts:1033–1075,2153–2164,2274–2281`）。「すべて月末失効」「すべて無期限」「購入すれば無制限」などの共通化は不可。具体付与量・運用条件は公開表示と照合してから記載する。
- アプリ独自の会員登録は不要。ただしAI/購入はApple由来の継続識別子を扱う。会員登録なし＝サーバーデータなしではない。

## 3. Pocket の実装で確認した情報フロー

| 機能・目的 | 情報 / 処理先 | 一次根拠 |
|---|---|---|
| zip取り込み | 選んだバックアップを検証・展開しApplication SupportのImportedSnapshots/currentへ保存。ノート・ページ・添付・問題集・録音等はローカル閲覧 | `Sources/UniNotePocketCore/MemoImportedSnapshotStore.swift:108–168,203–263` |
| 原本の保護 | 原本zipへ書き戻さず、展開後DBはREADONLYで開く | `Sources/UniNotePocketCore/MemoSnapshotCatalog.swift:46`、同ImportedSnapshotStore |
| 取り込み失敗/差替え | 成功時は前のsnapshotを置換しpreviousを削除。置換失敗時は前のsnapshotへ戻す経路がある | 同ImportedSnapshotStore:215–246 |
| 共有iCloud | Uni:Noteと同じiCloudコンテナのlatest.zipを取得。ファイル状態再確認時はOSへダウンロード要求 | `Sources/UniNotePocketCore/MemoSystemBackup.swift:30–45,59–86`、`App/UniNotePocket.entitlements:7,15` |
| 任意の自動読込 | 起動時自動読込設定の既定false。初回の共有バックアップ取込は確認UI、手動読込/更新UIあり | `App/MemoReaderPreferences.swift:1211–1221`、`UI/MemoBookshelfViewController.swift:800–844`、`UI/MemoSettingsViewController.swift:519–537` |
| 設定/閲覧位置 | UserDefaultsへ言語、テーマ、再開位置、横ズレ防止、表示呼称、既読案内等を保存 | `App/MemoReaderPreferences.swift:1164–1249,1258–1415` |
| お問い合わせ | システムメールを開き、種別と自由記入テンプレートを渡す。送信操作はユーザー側。開けない場合はコピー | `UI/MemoSettingsViewController.swift:645–686`、`App/MemoReaderPreferences.swift:1007–1015` |
| AI / 診断SDK / 広告 / 課金 | App、UI、Sources、project、Packageを検索し、アプリ自身のAI API、AWS、Firebase/Crashlytics/Analytics、広告SDK、StoreKit purchase実装は見つからない | `Package.swift:5–25`（外部package依存なし）、app target構成。iCloudやユーザーのメールまで通信なしとは呼ばない |
| 対応環境 | iPhone/iOS17以上のターゲット | `UniNotePocket.xcodeproj/project.pbxproj:334,348` |

Pocketにノート作成/編集/録音/文字起こし/AI要約や独自会員登録の実装はない。付箋表示の切替は表示状態の操作で、Uni:Note原本を編集しない。ノートの個別削除UIをPocketにあるように書かない。インポート差替え、端末内データ、元zip/iCloudの保持を分け、アンインストールが外部バックアップやUni:Note側を削除するとは書かない。

## 4. 文書の不足・矛盾・過度の断定

| ID / 種別 | 現行ソースの問題 | 根拠・改稿時の扱い |
|---|---|---|
| L01 / 優先・対象不明確な断定 | Uni:Note Privacy ja:19「開発者が内容を取得することはありません」。同節の画像/PDFは別AI機能では自社AWSを通り得る | 通常の貼付を端末内処理に限定し、AI時のAWS/Gemini処理を別記。開発者による人的閲覧の有無をコードから推定しない |
| L02 / 優先・保存先の不足 | Uni:Note Privacy ja:11,23の端末内保存とAI節ja:31–37だけでは、自社AWSの処理・生成レスポンスcache・購入/残量台帳が読者に分からない | 第2節に記したコードと照合。端末/外部保存/サーバーを情報種類ごとに記載。TTL保証を作らない |
| L03 / 優先・送信項目の不足 | Uni:Note Privacy ja:33は要約の「文字起こしテキスト」だけを説明 | 録音タイトル/ID/日時、条件によりノート名等を含むpayloadが実在。ノート名を「絶対に送信しない」と一般化しない |
| L04 / 対象限定が必要 | Uni:Note Privacy ja:53はノート名等「送信しません」、FAQ ja:65は「診断ログには含めません」 | Privacy診断節の否定をCrashlytics向け診断に明確に限定。AIや問い合わせ送信の説明と矛盾させない |
| L05 / 優先・削除条件不足 | Uni:Note Privacyにユーザー操作による削除・バックアップ削除・サーバー台帳の扱いなし。Guide ja:115、FAQ ja:25はゴミ箱から復元できるとだけ説明 | ゴミ箱30日purgeと完全削除、外部backupが別管理であることを追記。削除の絶対保証や購入台帳即時消去は不可 |
| L06 / 説明不足 | Uni:Note Privacy ja:43の「識別ID」だけでは購入取引情報・サーバー保存目的が不足 | AppTransactionID等の一般向け表現、残量管理/二重付与防止/復元・問い合わせ目的を明示。氏名を入力しないことは維持 |
| L07 / 優先・機能経路の欠落 | Pocket Privacy 全6言語の:18–28は明示選択したzipと選択した外部ストレージだけを説明 | 現Guide ja:77–83と実装にかんたんバックアップのiCloud読込、設定時起動読込がある。これもPrivacyへ説明 |
| L08 / 用語・網羅不足 | Pocket Privacy 全6言語:14の「暗記レイヤー」相当は旧称。問題集/録音/閲覧位置等の説明も薄い | 現Guide/FAQおよび実UIの付箋マーカー/表示状態へ統一。機能追加とは扱わない |
| L09 / 共通項目不足 | 両Privacyに独立した利用目的、保存・削除、問い合わせで任意提供される情報の項目がない。適用範囲には公式サイトも含む | アプリから自動で送らないデータと、利用者が問い合わせ時に送る連絡先/本文/添付を分ける。サイトの配信基盤情報は共通監査側で確認 |
| L10 / 構成差 | Uni:Note Privacy10節、Pocket7節。Guide冒頭に最低OSがなく、FAQにある。FAQは疑問文Q&Aでなく7/4の集約したトラブル項目 | 共通h2順に再配置。機能章数まで同一にせず実装差を残す。Guideの基本手順と画像を維持し、FAQへ長い手順を複製しない |
| L11 / Terms新設 | 両Termsは元々ない。既存Apple EULAへのリンクはリンク切れではない | 日本語独自Termsの新設時に実装通りの利用範囲/購入方式/AI結果の確認/バックアップを記述。Appleとの購入契約や法定権利を独自ルールで変更しない |
| L12 / 時点依存 | Uni:Note Guide各言語:45,89相当、FAQ:74相当は3.4.0公開/3.5.0公開前。version_context_dateは2026-09-07 | 日付付きの区別を維持するか恒久ガイドから公開前説明を外す。現在のdirty3.5.0の実装だけで一般公開に変更しない |

L01〜L06は Uni:Note Privacy 全6言語に同等の説明がある。日本語の行からen/de/fr/zh-hantは概ね+1、koは旧anchor・lastmod追加により+2〜+5のずれがある。L07〜L08はPocket全6言語で同じ段落位置。12Privacyは取得/保存/外部AI/第三者提供/変更/問い合わせを実際に読んで照合し、翻訳によりAIやアカウントの有無が反転するような独立した矛盾は見つけていない。

## 5. Guide / FAQ の意味、役割、保持対象

- 現FAQ→Guideの固有リンクは Uni:Note 7パターン×6言語=42本、Pocket4パターン×6言語=24本。write/find/pdf/recording/review/backup/windows および import/refresh/recordings/read は実在節と文脈が一致する。現在の同一URLへ異なる目的名を付けたリンクの新たな意味不一致は見つからない。
- Uni:Note FAQ help-7の最後はwindows。問全体は言語/ボタン差/更新情報も含むため、共通FAQへ分割するなら「2つのウインドウ」の質問と一緒に移す。Pocket help-4→read は再開/拡大/スクロール説明として妥当。表示設定の質問を独立させるならsettingsへ意味対応させる。見かけの重複削減目的でアンカーを付け替えない。
- 共通の製品先頭リンクと `#support` は異なる目的として保持する。古いFAQ/Guide anchor群は同じ意味の新見出し直前へ残す。ページ冒頭へ一括移動しない。
- Uni:Noteの手順は作成、Pencil/指の役割、範囲移動、検索範囲、PDF挿入/出力、録音、付箋、AI解答のコピー/共有、問題集、保護/削除、backup、multiwindowを保持。Freeの10教科/6冊、150ページ、Premium録音と30分分割/5件、文字起こしiPadOS26は前提として維持し、公開版との区別を継続する。
- Pocketのzipを展開しない手順、原本不変/失敗時保持、read-only、検索範囲、付箋の表示だけを切替、取り込み済録音の再生、読みやすさ、iCloud更新アイコンと手動読込/任意自動読込の違いは保持する。
- 「はじめに→基本的な使い方（最初の操作h3）→既存固有章→困ったとき→お問い合わせ」の案は適用できる。FAQも共通の概要/環境→固有Q&A→保存/購入→困ったときに統一可能。ただしPocketに存在しない購入・アカウント削除・AIを操作機能として追加しない。
- 各画像shortcodeのsrc/alt/caption/mode、明示ID、旧guide-anchor、見出し、操作全文とSHA256を **learning-preservation-inventory.json** に記録する。現在のbefore-build HTMLのarticle内ID/画像/リンクも同ファイルへ記録。後の差分比較で画像・操作・旧リンク到達先を確認するための基準である。

## 6. 要確認として残す運用事実

1. Uni:Noteの実運用Lambda環境変数によるAI cache期限、DynamoDB TTL有効値/実削除、CloudWatch保持日数、PITR/オンデマンドbackupの保持期限。ローカル設定処理は確認、live設定は取得していない。
2. Google Gemini契約上の保持期間、学習利用、処理地域、およびAWSの実運用処理地域。コードのエンドポイントだけで契約条件を断定しない。Providerの最新Privacyリンクを載せるなら直接公式URL確認は別段階。
3. サーバー上の取引/残量/キャッシュ/ログについて、問い合わせによる照会/削除運用と法的保存根拠・期間。公開コードに利用者用の一括削除APIは見つからない。存在しない自動削除機能を案内しない。
4. Storeで現在販売可能なSKU/価格/地域/Family Sharing、3.5.0公開状態。今回のローカルコード読みで確定しない。新Termsへ固定価格・Family共有・提供期間の保証を入れない。
5. Firebase SDK/Apple OSが標準で扱う診断識別子・保持条件の網羅は、アプリ独自のsafe metadata検証とは別。独自キーのホワイトリストだけを根拠に「列挙項目以外は一切送信しない」としない。

本Phaseではこれらが未確認でも断定を避けた記述へ改稿できる。製品の実装差を消すテンプレート適用、旧URL/anchor/画像/操作の削除、未公開機能の公開扱いは行わない。

## 7. 保持インベントリの件数

36 source文書と36 before-build HTMLを対応付けた。Guide/FAQ24文書の明示見出しID 156 個、旧guide-anchor ID 654 個、Guide画像 90 配置（64 unique src）を保持基準として採取。

| ソース | 明示ID | 旧ID | 画像 |
|---|---:|---:|---:|
| `content/htu/uni-note-pocket.de.md` | 6 | 11 | 6 |
| `content/htu/uni-note-pocket.en.md` | 6 | 11 | 6 |
| `content/htu/uni-note-pocket.fr.md` | 6 | 11 | 6 |
| `content/htu/uni-note-pocket.ko.md` | 6 | 11 | 6 |
| `content/htu/uni-note-pocket.md` | 6 | 11 | 6 |
| `content/htu/uni-note-pocket.zh-hant.md` | 6 | 11 | 6 |
| `content/htu/uni-note.de.md` | 9 | 16 | 9 |
| `content/htu/uni-note.en.md` | 9 | 16 | 9 |
| `content/htu/uni-note.fr.md` | 9 | 16 | 9 |
| `content/htu/uni-note.ko.md` | 9 | 16 | 9 |
| `content/htu/uni-note.md` | 9 | 16 | 9 |
| `content/htu/uni-note.zh-hant.md` | 9 | 16 | 9 |
| `content/faq/uni-note-pocket.de.md` | 4 | 28 | 0 |
| `content/faq/uni-note-pocket.en.md` | 4 | 28 | 0 |
| `content/faq/uni-note-pocket.fr.md` | 4 | 28 | 0 |
| `content/faq/uni-note-pocket.ko.md` | 4 | 28 | 0 |
| `content/faq/uni-note-pocket.md` | 4 | 28 | 0 |
| `content/faq/uni-note-pocket.zh-hant.md` | 4 | 28 | 0 |
| `content/faq/uni-note.de.md` | 7 | 54 | 0 |
| `content/faq/uni-note.en.md` | 7 | 54 | 0 |
| `content/faq/uni-note.fr.md` | 7 | 54 | 0 |
| `content/faq/uni-note.ko.md` | 7 | 54 | 0 |
| `content/faq/uni-note.md` | 7 | 54 | 0 |
| `content/faq/uni-note.zh-hant.md` | 7 | 54 | 0 |
