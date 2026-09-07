# 文書統一 Phase 1 — Nocca / オトミル

監査日: 2026-09-08。公開ページ、検索結果、ChatGPT のキャッシュは参照していない。現行ローカルソースを読み、アプリの実装、宣言的設定、運用文書、Web 文書を区別した。アプリ・サイト本文は変更していない。

## 1. 対象と作業状態

| リポジトリ | 開始時のブランチ / HEAD | 開始時の状態 |
| --- | --- | --- |
| `/Users/yuya/Projects/homepage` | `main` / `3ab462d` | `.DS_Store` のみ未追跡。監査中に親担当の監査ディレクトリ・スクリプトが追加された |
| `/Users/yuya/Projects/oto_miru` | `main` / `cf7f50b` | AppModel、Speech、表示、課金、文書等に多数の未コミット変更。旧 HighAccuracy サービス・AWS 実装の削除を含む |
| `/Users/yuya/Projects/Nocca` | `main` / `46a58d7` | アプリ、AWS、文書等に多数の未コミット変更。App Attest、課金、認証、Privacy manifest 等の未追跡ファイルを含む |

コミットされた状態だけではなく、現在存在する未コミット・未追跡ファイルも読んだ。アプリ側の status を変更する操作、実行環境の変更、課金・本番 AWS へのアクセスは行っていない。

実在する対象は `content/{privacy,terms,faq,htu}/{nocca,oto-miru}.md` の **8 文書、日本語のみ**。この 4 文書に英語等の翻訳ファイルは存在しない。Product の多言語表示と、支援文書の実在言語は別扱いにする。

サイト運用の正本 `docs/WEBSITE_MAINTENANCE.md` に従い、Guide は実操作、FAQ は問題・例外、Privacy は情報取扱い、Terms は利用条件という役割を維持する。本報告は実装・文面整合の監査であり、法令適合や公開中アプリの実挙動を証明するものではない。

## 2. 優先して直せる事実差分

| ID | 判定 | 現行文書と根拠 | 推奨 |
| --- | --- | --- | --- |
| OM-01 | 確認済みの実装差分 | `content/privacy/oto-miru.md:34` は「会話内容をあとから見返す機能は提供していません」。現在の `OtoMiru/App/AppModel.swift:631` は停止後に `.reviewing` とし、同 `:642` のホーム復帰でバッファを消す。`OtoMiru/Views/RootView.swift:313` はレビュー中に全履歴を表示し、`:793` は「ホームに戻る」 | 「録音ファイル・永続的な字幕履歴は保存しない」と「字幕停止後、その回の字幕を一時的に見返せる」を分ける。ホーム復帰・非アクティブ化等で消える範囲を説明する |
| OM-02 | 確認済みの古い API 説明 | `content/privacy/oto-miru.md:38` は Apple Intelligence / Foundation Models の利用可否判定を実施すると記載。現在の `OtoMiru/Services/DeviceSupportPolicy.swift:68` は SpeechTranscriber と日本語対応のみ判定。現行アプリ Swift に FoundationModels の参照なし | Apple Speech と必要モデルの準備を説明する。Apple Intelligence / Foundation Models を現在利用しているという記載を削除する |
| OM-03 | 確認済みの操作差分 | `content/htu/oto-miru.md:39` は停止まで、`:53` は「字幕を止めてから」設定へ進む。現在は停止→一時レビュー→「ホームに戻る」の段階がある | 停止後レビューとホームへ戻る手順を追加。設定へ進む起点をホームとする。既存画像は保持し、画像が未撮影の状態を創作しない |
| OM-04 | 確認済みの選択肢差分 | `content/htu/oto-miru.md:56` は文字サイズ「小・中・大」。`OtoMiru/Models/CaptionModels.swift:50` は小・やや小・中・やや大・大。`OtoMiru/Views/SettingsView.swift:107` は段階スライダー | 「プレビューを見ながら文字サイズを調整する」等、実操作に合う文にする |
| OM-05 | 現行表示と旧表示の区別が必要 | `content/faq/oto-miru.md:193` は「この端末では高精度字幕を利用できません」を現在の表示のように質問見出し化。現行標準認識の端末判定は `DeviceSupportPolicy.swift:68`。旧表示に対する案内は既存利用者には意味がある | 「端末が対応していないと表示される」等に一般化し、旧見出し ID は対応する質問の直前に残す。旧エラーそのものを現行仕様の証拠にしない |
| NC-01 | 分類の混在 | `content/faq/nocca.md:103` の広告回答に独自 7 日間のおためし・その後のプラン利用が混在 | 広告の有無と料金・おためしを別質問にする。7 日間と Apple の対象者向け 14 日間を混同しない |
| NC-02 | 正確さを補う余地 | `content/faq/nocca.md:133` は通知が「種類だけ」。実際の `aws/lambda/handler.py:6234` は一般的な表示文と familyId/eventId/kind/route を送る。Privacy `:37` は識別情報も説明済み | 「通知画面には本文・家族名を表示せず、通知に必要な識別情報を送る」等にそろえる。可視通知と push payload を分ける |
| NC-03 | 意味上のアンカー配置問題 | `content/privacy/nocca.md:7` / `content/terms/nocca.md:7` に旧節 ID がすべて集約されている。リンク切れではないが、課金・削除・お問い合わせの旧リンクから文書先頭に着地する | 旧 ID を新しい意味対応節の直前へ移す。すべてを先頭に残す方式は採らない |

Nocca では、現在の Privacy/Terms に重大なデータフローの逆転は確認していない。特に「端末のみ」「運営者にも内容が見えない」「全データが即時完全削除」「登録不要だから認証情報を作らない」へ短縮すると、実装と矛盾する。

## 3. オトミル — 情報取扱いの一次根拠

この節のアプリパスは `/Users/yuya/Projects/oto_miru/` を基準とする。

| 項目 | 現在の実装 | 一次根拠 |
| --- | --- | --- |
| マイク・音声・文字 | マイク入力を Apple Speech の日本語認識へ渡し、端末内で字幕化。必要なモデルの取得・準備を行う。開発者の文字起こし API に音声を送信する経路は現行 Swift にない | `OtoMiru/Services/SpeechRecognitionService.swift:295`, `:316`, `:353`, `:363`; 権限は `:458` |
| 字幕の保存 | 現在の回の字幕はメモリに保持。停止後に一時レビュー可能。録音ファイルや永続字幕履歴の保存実装なし。ホーム復帰・非アクティブ化等で消去 | `OtoMiru/Models/CaptionBuffer.swift:3`, `:35`; `OtoMiru/App/AppModel.swift:381`, `:631`, `:642`; `OtoMiru/Views/RootView.swift:302` |
| 画像・カメラ・写真等 | 現行アプリに撮影・画像投稿・写真ライブラリ読取の製品機能を確認していない。音声字幕と無関係な AI 画像データフローを追加しない | 現行 `OtoMiru/` Swift 一覧と `OtoMiru/Info.plist` の権限キーを確認 |
| 設定・利用量 | 表示モード、テーマ、文字サイズ、聞き取り環境等と無料利用時間・広告追加回数を UserDefaults に保持 | `OtoMiru/Services/DisplaySettingsStore.swift:12`, `:58`; `OtoMiru/Services/FreeUsageLimiter.swift:18` |
| 無料利用 | 1 日 900 秒、広告追加 300 秒、1 日 3 回 | `OtoMiru/Services/FreeUsageLimiter.swift:18` |
| 広告 | 無料利用者に Google Mobile Ads / AdMob。バナー・リワード・インタースティシャルの実装。広告リクエストに字幕本文を渡していない。課金状態読取後、Plus では広告サービスの起動を省く | `OtoMiru/App/AppModel.swift:189`; `OtoMiru/Services/AdPolicyStore.swift:35`; `OtoMiru/Services/RewardedAdService.swift:85`, `:144`; `OtoMiru/Services/InterstitialAdService.swift:66`, `:119`; `OtoMiru/Views/RootView.swift:997` |
| 解析・クラッシュ | 現行アプリソースとプロジェクト依存に Firebase Analytics / Crashlytics / 独自解析送信を確認していない。Google Mobile Ads は存在するため「外部サービスへの情報送信が一切ない」とは書けない | `OtoMiru.xcodeproj/project.pbxproj:744` の GoogleMobileAds 依存、現行 Swift の SDK/API 参照検索 |
| アカウント・Family | 独自ログイン・家族アカウントサーバーはない。StoreKit currentEntitlements で購入者と Family Shared を判定する | `OtoMiru/Services/SubscriptionManager.swift:263` |
| 課金 | 月額 / 年額 Plus。StoreKit Product の価格、購入・復元・更新状態を利用。Plus の主差分は時間制限解除と広告非表示。Web で固定価格・固定トライアルの一律保証を戻さない | `OtoMiru/Services/SubscriptionManager.swift:73`, `:96`, `:157`, `:190`, `:210`, `:263`; `OtoMiru/Views/PaywallView.swift:26` に固定 2 週間文言はあるが、実 Store の適格性・表示の証明ではない |
| 削除 | 字幕は上述の一時データ。アプリ削除で端末上の設定・利用記録を削除する説明と整合。App Store 契約をアプリ削除で解除する実装はない | `content/privacy/oto-miru.md:58`, `:64`; `DisplaySettingsStore.swift:58`; `SubscriptionManager.swift:210`, `:263` |
| 問い合わせ | サイトはメール窓口。返信・品質対応等の必要範囲で保持する記載。Nocca の 1 年保持ルールをこのアプリに適用する一次根拠はない | `content/privacy/oto-miru.md:72`, `:76`, `:92` |
| 対応環境 | iOS / iPadOS 26、Apple Speech 日本語対応。Apple Intelligence の設定は利用条件ではない | `OtoMiru/Services/DeviceSupportPolicy.swift:68`; `OtoMiru.xcodeproj/project.pbxproj:620`, `:632` |

### 廃止された AI と公開状態

`aws/high_accuracy_transcription/README.md:3` は旧 AI / Pro を廃止した記録であり、再開用 feature flag ではない。現ワークツリーでは HighAccuracyTranscriptionService、Lambda、CloudFormation、deploy/package ファイルが削除され、現行プランは Free / Plus。過去の OpenAI/AWS の設計を現行データフローに混ぜない。

ただし、ローカルからの削除と、AWS 実リソース・OpenAI API key の実廃止は別である。本 Phase 1 では後者を再確認していない。古い文書・履歴の存在だけで現行 API が動いているとも判断しない。

Guide/FAQ の冒頭には「最新提出資料・開発版をもとにしており、公開版と異なる場合がある」という境界がある。ローカルの新しいレビュー操作を説明するときも、一般公開済みと断定しない。

## 4. Nocca — 情報取扱いの一次根拠

この節のアプリパスは `/Users/yuya/Projects/Nocca/` を基準とする。

| 項目 | 現在の実装 | 一次根拠 |
| --- | --- | --- |
| 情報・送信内容 | 表示名、Family/役割/承認関係、招待、ミュート、意思表示・返信・会話本文・プリセット・時刻・進捗/完了/取消等。任意の体調・気分表現を含み得る | `Nocca/NoccaAPIClient.swift:682`, `:887`, `:936`; `aws/lambda/handler.py:4924`, `:5021` |
| 端末内保存 | 非秘密の状態を UserDefaults、端末 credential を Keychain に分離 | `Nocca/NoccaState.swift:4367`; `Nocca/NoccaCredentialStore.swift:213`, `:231` |
| サーバー保存 | HTTPS の API Gateway/Lambda を通じた DynamoDB 保存。同期用 backupJson もサーバーに保持。東京リージョン構成で、暗号化・TTL・PITR 有効 | `Nocca/NoccaAPIClient.swift:601`, `:1073`; `aws/lambda/handler.py:4478`; `aws/cloudformation.yaml:98`; Release URL は `Nocca.xcodeproj/project.pbxproj:501` |
| 認証・アカウント | メール/パスワードの入力登録は不要だが、インストール識別子・ランダム credential・Cognito 内部ユーザーを作る。認証情報が存在しないサービスではない | `Nocca/NoccaCredentialStore.swift:213`; `aws/lambda/handler.py:534`, `:568` |
| App Attest | チャレンジ・鍵 ID・検証済み公開鍵・検証メタデータを扱う。秘密鍵をサーバー保存するものではない | `aws/lambda/app_attest.py:486`, `:499`; `aws/lambda/handler.py:600`; `Nocca/Nocca.entitlements:5` |
| 家族への共有 | 承認済みの家族内で通信内容を共有。家族に Apple Account の識別情報を公開する仕組みではない。アプリ独自 Family と Apple の Family Sharing は別 | `content/privacy/nocca.md:35`; `aws/lambda/subscriptions.py:297`; `content/terms/nocca.md:47` |
| push | 許可後に token 登録、SNS 経由 APNs。画面表示は「新しいお知らせがあります」等の一般文。payload に Family/event/kind/route 識別情報。本文・家族名は含めない | `Nocca/NoccaPushRegistration.swift:91`; `aws/lambda/handler.py:23`, `:6234` |
| 画像・マイク・AI | v1 iPhone のカメラ/マイク/GPS/連絡先読取・AI 送信を確認していない。体調表現は本人が選択・入力するもので健康計測ではない。「Contacts」申告は承認済み家族関係で、アドレス帳アクセスと混同しない | `Nocca/Info.plist`; `Nocca/PrivacyInfo.xcprivacy:16`; `docs/APP_STORE_METADATA.md:156` |
| 広告・解析 | 第三者広告 SDK / Firebase Analytics / Crashlytics は現行 iPhone プロジェクトにない。AWS の技術ログと短期レート制限は存在する | `Nocca.xcodeproj/project.pbxproj`; `aws/cloudformation.yaml:310`, `:352`, `:801`; `aws/lambda/handler.py:7320` |
| IP の取扱い | リクエストの sourceIp をレート制限に用い、source/method/route の短い SHA-256 ハッシュを保存。本文・IP を通常診断ログへ保存する構成ではない。「IP を一切扱わない」とは書かない | `aws/lambda/handler.py:7508`, `:7320`; `aws/cloudformation.yaml:801` |
| 課金 | 月額・年額。StoreKit の Product と導入オファー適格性を確認。AppTransaction/JWS/deviceVerificationID をサーバー検証、安定 ID のハッシュと appAccountToken 等を復元・不正再取得防止に使う | `Nocca/NoccaSubscription.swift:195`, `:220`, `:250`, `:306`; `aws/lambda/subscriptions.py:104`, `:113` |
| 独自おためし | 最初の家族接続承認時にサーバー時刻で 7 日間開始。購入を開始せず、終了後自動課金しない。繰り返し利用を制限。Apple の適格者向け 14 日間の導入オファーとは別 | `aws/lambda/subscriptions.py:14`, `:266`; `Nocca/NoccaSubscription.swift:220`; `content/terms/nocca.md:27` |
| 家族プラン | 同じ Nocca Family の有効な契約のいずれかで利用可能。家族内の複数契約を自動解約しない。再関連付けは 24 時間制約 | `aws/lambda/subscriptions.py:15`, `:297`; `content/terms/nocca.md:47` |
| 削除 | 本人は家族全体、家族側は自分の対象データを削除。サーバーで論理失効した後、非同期 cleanup。サーバー処理成功後にローカル状態と push を解除。失敗を「削除できた」と表示しない | `Nocca/NoccaBackendCoordinator.swift:1521`, `:1583`; `aws/lambda/handler.py:3430`, `:3526`, `:3573`; `Nocca/ContentView.swift:2409`, `:2439` |
| 問い合わせ | 外部 Google Forms と開けない場合の Gmail。安全な 8 行のサポート情報は明示操作で端末へコピーするだけ。自動診断送信ではない。返信メールは任意の運用方針 | `Nocca/NoccaState.swift:47`, `:89`, `:143`; `Nocca/ContentView.swift:4547`; `docs/PRIVACY_OPERATIONS.md:7` |

### 保持期間 — 実装と運用を混同しない

| 対象 | 期間・消去 | 根拠と確認限界 |
| --- | --- | --- |
| 通信・プリセット・同期用バックアップ | 対応する削除まで。会話を閉じる、試用終了、アプリをアンインストールするだけではサーバーデータは消えない | `aws/lambda/handler.py:4478`, `:5021`, `:3430`; Privacy `:53`, `:71` |
| 招待 / 引き継ぎ / 復旧コード | 30 日 / 7 日 / 24 時間 | `aws/lambda/handler.py:29` |
| 単回認証 challenge | 用途により 2〜5 分の有効期限、失効後の保管 TTL はさらに 1 時間 | `aws/lambda/handler.py:17`; `aws/lambda/billing_proof.py:81`。TTL 実削除は非同期 |
| おためし・旧認証再利用防止 hash / 購入復元 principal・token | 固定 TTL なし。家族との直接結合を切り、制度・認証方式・購入復元の必要性が続く間の最小台帳 | `aws/lambda/subscriptions.py:113`; `docs/PRIVACY_OPERATIONS.md:31`。ハッシュを「完全匿名」「全消去済み」と扱わない |
| 購入・通知検証台帳 | 取引の期限、契約期限/猶予期限/最終処理日時、通知処理日時など対象ごとの基点から 400 日 | `aws/lambda/subscriptions.py:454`, `:515`, `:531`, `:551` |
| 技術ログ | CloudWatch 30 日 | `aws/cloudformation.yaml:315`, `:357`。本番実設定を今回再取得したわけではない |
| レート制限 | 標準 window では約 2 分 | `aws/lambda/handler.py:7320`。sourceIp のハッシュを利用 |
| DynamoDB PITR | 運用文書で 35 日 | `docs/PRIVACY_OPERATIONS.md:23`。CloudFormation は有効化の根拠。本 Phase 1 では live の実 retention 値未確認 |
| 手動 on-demand backup | 復旧確認完了から 35 日以内に削除する運用 | `docs/PRIVACY_OPERATIONS.md:24`。**AWS 自動 TTL ではない**。実際の全 backup 消去・期限遵守は今回未検証 |
| 問い合わせ | 対応完了から 1 年以内、未解決・法令/紛争等は必要な例外保持 | `docs/PRIVACY_OPERATIONS.md:11`。**運営者の手動方針**であり Google retention 設定・削除実績の証明ではない |

Privacy `content/privacy/nocca.md:49` の保持表、`:65` の TTL 非同期、`:67` の backup、`:69` の問い合わせ・最小台帳例外は、利用者の判断に影響する。形式統一で丸ごと「必要な期間」へ縮めない。

### 実装済み・非公開・未確認

- Release の東京 API URL・APNs/App Attest production 構成はある。これはストア一般公開の証明ではない。`docs/APP_STORE_METADATA.md:34` は NOT SUBMITTED、`:48` はアップロード済み build とその後のソースの差を記録している。
- Android / FCM のコード・プロトタイプが存在しても、v1 iPhone の公開機能としない。`docs/APP_STORE_METADATA.md:156` と `:279` で切り分けられている。
- Google Forms の最新項目・任意設定、AWS 実設定、削除 worker の現場完了、実購入/復元/Family 共有は本監査で操作していない。構成・実装・運用方針をそれぞれの根拠として扱う。

## 5. 文書の役割と共通構成への適用

### Privacy

共通順序「はじめに → 取得する情報 → 利用目的 → 保存・管理 → 外部サービス・第三者提供 → 固有機能 → データ管理・削除 → 未成年者 → 変更 → お問い合わせ」は両アプリに適用可能。

- Nocca は取得情報と目的が現在一節に混在。別節へ整理するが、家族共有、Apple 安定 ID、認証・復元の最小台帳、AWS 保存、通信本文、任意の体調表現を保持する。課金の Privacy 節は金額宣伝でなく、購入証明・識別情報と用途に集中する。
- オトミルの固有節はマイク・Apple Speech・字幕の一時保持と広告。独自生成 AI がないことと Apple Speech の機械学習処理は別であり、「AI は一切使用しない」といった広い断定に置き換えない。
- サイト・メール窓口の情報はアプリ内処理と区別する。Nocca の Forms、オトミルの AdMob を他製品へコピーしない。
- 「第三者提供なし」だけの絶対文にせず、ユーザーが使う外部サービスと家族共有を具体的に示す。
- Nocca の問い合わせ/変更が一つの節、オトミルは独立しているため分離して順序をそろえられる。
- 保存期間や開示等の共通項目が他製品にない場合、Nocca の期間や本人確認の処理を勝手に移植しない。確認できる範囲を記載し、未確認を親監査へ残す。

### Terms

- Nocca は独自 7 日間、Apple 14 日間、Nocca Family の共有と複数契約・24 時間再関連付けが必要。オトミルは無料利用 15 分・広告延長・Plus と Apple Family Sharing が必要。共通の課金見出し内で固有小節を維持する。
- 医療/治療の代替ではないこと、字幕精度の限界、監視・緊急用途ではないこと等、両製品の理由の異なる制限を一律文に潰さない。
- Apple による購入/解約/返金と、アプリ削除では契約解除されない点、購入画面条件優先は共通化可能。固定価格・全員無料期間を新規に追加しない。
- 現在のオトミル Terms には独立した知的財産・準拠法節がない。Nocca の法的条件を、そのまま既存契約条件だったかのように複製しない。追加する場合は構成整理ではなく利用条件の追加として記録する。

### Guide / FAQ

- Guide 冒頭に概要・対応環境、初回操作を置く共通構成は可能。既存機能 h2 を保ち、初心者が実際に押す画面語と順序を残す。
- オトミルは「字幕を止める → 一時レビュー → ホームに戻る」と、設定の実操作を更新する。映画モードの警告、簡易モードとの違い、反転、聞き取り環境、利用時間・復元の手順は保持する。
- Nocca は招待コード入力だけで接続成立とはしない。本人側での承認、本人が会話を開く/閉じる、家族側リクエスト制約、取消/対応/完了の違い、通信休止、機種変更、削除範囲を残す。
- Guide の末尾はトラブルへの入口と問い合わせ。個々の原因・例外を FAQ に残し、操作の本文を FAQ に再掲しない。FAQ の「最初に何をすれば」等は対応 Guide 節への短い案内にできる。
- Nocca FAQ は既読と対応状況の区別、家族から勝手に会話を開けないこと、閉じた会話の参照、request 初期 OFF/間隔、GPS/行動監視なしを保持する。
- オトミル FAQ は音声モデル/オフライン条件、録音と一時表示の区別、話者識別誤り、同一の標準認識と料金差、音声未検出/非対応/広告・復元の問題を保持する。
- 共通の「不具合」「お問い合わせ先」には連絡に必要な最小情報を置く。Nocca に存在する安全なサポート情報コピーをオトミルにも存在する機能として書かない。

## 6. リンク・画像・操作・アンカーの保持方針

FAQ→Guide、Guide→FAQ の現行アンカー付きリンクを読み、Nocca の旧法務 ID の先頭集約以外に明確な別意味節への遷移は確認していない。静的リンクの網羅検査・生成物の前後照合は親担当の全サイト検査で行う。

親担当が保存した `/private/tmp/kumakikai-document-unification/before-build` の HTML を、生成済みの実 ID の比較元とする。以下の source inventory には明示 ID と旧 ID と見出しを残す。自動生成 ID は見出し表記から推測せず、before-build の実 ID を使う。

- **画像 14 件（各 7 件）を保持**。画像にまだ存在しない新 UI を生成しない。オトミル `mode-and-settings.png` の `single-source=true` も保持する。
- 旧 ID はそれぞれ対応する新しい意味の節/質問の直前に置く。Nocca 法務の全旧 ID を先頭へ集約した状態は解消する。お問い合わせ ID は問い合わせへ、課金 ID は課金へ、削除 ID は削除へ着地させる。
- Guide の操作/画像と FAQ の問題/例外を移す場合は、リンク名の意味と到着節の意味を合わせる。存在するだけの ID を合格条件にしない。

## 7. 要確認として残す事項

1. 一般公開 App Store 版とローカル変更の対応、実 StoreKit の価格・導入オファー適格性・Family 共有・復元の現場結果。
2. オトミル旧 AI の AWS/OpenAI 実廃止状態。現行アプリの通信経路はないが、ローカル削除だけで外部消去は断定できない。
3. Nocca PITR 実保持期間、手動 backup の棚卸し/消去実績、Google Forms の最新設定、問い合わせの手動削除実績。
4. オトミルの問い合わせの厳密な保存期限。現サイトは目的上必要な範囲という記載で、固定 1 年の根拠はない。
5. Google Mobile Ads 側が実際の同意・端末・地域条件ごとに取得するデータ/保持期間。SDK 依存の存在と広告 Request は確認したが、ネットワーク計測や provider の現行設定は確認していない。

これらは文書統一を止める理由ではなく、未確認の事実を共通テンプレートに埋め込まないための境界である。確認済みの内容差分と構成・重複整理は進められる。

## 8. 保持対象のソース inventory

以下は Phase 1 の現行文書から抽出した行番号付き見出し・アンカー・画像である。

### content/privacy/nocca.md

```text
7: {{< guide-anchor "1-基本方針" "2-本アプリが扱う情報" "3-保存と同期について" "4-取得しない情報" "5-通信内容について" "6-第三者サービスについて" "7-広告について" "8-課金について" "9-お問い合わせについて" "10-未成年の利用について" "11-プライバシーポリシーの変更" "12-お問い合わせ" >}}
15: ## 1. 取得する情報と目的
31: ## 2. 保存先と家族への共有
39: ## 3. おためしとサブスクリプション
49: ## 4. 保存期間
71: ## 5. 削除と利用者の選択
83: ## 6. 外部サービスと安全管理
91: ## 7. 年齢について
95: ## 8. お問い合わせと改定
```

### content/terms/nocca.md

```text
7: {{< guide-anchor "1-適用範囲" "2-本アプリの内容" "3-医療治療監視目的ではないこと" "4-利用上の前提" "5-招待と接続" "6-会話と返信" "7-通信休止とミュート" "8-禁止事項" "9-料金について" "10-データとプライバシー" "11-免責事項" "12-仕様変更提供停止" "13-本利用規約の変更" "14-お問い合わせ" >}}
15: ## 1. Noccaについて
21: ## 2. 利用条件
27: ## 3. Nocca独自の7日間のおためし
37: ## 4. 月額・年額プランとAppleの無料トライアル
47: ## 5. 家族でのプラン利用
57: ## 6. 禁止する行為
66: ## 7. データの削除
74: ## 8. サービスの変更・停止と責任
80: ## 9. 知的財産と規約の変更
86: ## 10. お問い合わせ・準拠法
```

### content/faq/nocca.md

```text
9: ## 基本
11: ### Nocca はどんなアプリですか？
17: ### 現在公開されていますか？
23: ### 対応端末や言語は？
29: ### 医療、治療、見守りのアプリですか？
35: ### 誰が管理者になりますか？
43: ## 使い方
45: ### 最初に何をしますか？
49: ### 家族と接続するには？
53: ### 意思表示では何ができますか？
57: ### 家族側は自由にメッセージできますか？
63: ### 会話は常時チャットですか？
69: ### 家族から会話リクエストは送れますか？
75: ### 通信を休止できますか？
83: ## プライバシーと設計
85: ### 既読や未読は表示されますか？
91: ### GPS や行動ログは使いますか？
97: ### AI は使いますか？
101: ### 広告はありますか？
105: ### データはどこに保存されますか？
111: ## トラブルシューティング
113: ### 招待コードを入力しても接続できません。
119: ### 返信や会話リクエストが送れません。
125: ### 本人が「今は閉じたまま」を選んだことは家族側に通知されますか？
131: ### 通知が届かない場合は？
```

### content/htu/nocca.md

```text
11: ## 最初に役割を選ぶ {#1-最初に役割を選ぶ}
18: {{< guide-image src="images/guides/nocca/choose-role.png" alt="Nocca初回画面の本人として使う・家族として使うボタンと役割の説明" mode="crop" >}}
22: {{< guide-anchor "未接続のとき" >}}
23: ## 家族と接続する {#3-家族を招待する}
30: {{< guide-image src="images/guides/nocca/invite-family.png" alt="本人側の家族を招待画面。招待コードのコピーと招待リンクの共有ボタン" mode="screen" caption="画像のコードは説明用です。アプリに表示されたコードを共有してください。" >}}
34: {{< guide-anchor "2-本人として使う" "意思表示" >}}
35: ## 本人から意思表示を送る {#send-signal}
39: {{< guide-image src="images/guides/nocca/send-signal.png" alt="本人側の意思表示画面。ご飯ほしい、飲み物ほしい、片付けお願いのアイコン" mode="crop" >}}
43: {{< guide-anchor "つながり" >}}
44: ## 送った意思表示と返信を確認する {#signal-status}
48: {{< guide-image src="images/guides/nocca/signal-status.png" alt="本人側の送った意思表示。家族からの少し待ってねという返信と取り消すボタン" mode="crop" >}}
50: {{< guide-anchor "5-家族として使う" "受信" >}}
51: ## 家族から短い返信を返す {#reply}
58: {{< guide-image src="images/guides/nocca/reply-options.png" alt="家族側の受信画面。ご飯ほしいへの対応と完了の定型返信ボタン" mode="crop" >}}
62: {{< guide-anchor "会話" "会話-1" >}}
63: ## 話せるときだけ会話を開く {#talk}
69: {{< guide-image src="images/guides/nocca/owner-talk.png" alt="本人側の会話画面。会話を閉じる操作と短いメッセージの入力欄" mode="screen" >}}
73: {{< guide-anchor "設定" "設定-1" >}}
74: ## 通信を休止する {#4-通信を休止する}
78: {{< guide-image src="images/guides/nocca/pause-communication.png" alt="通信を休止する画面の説明と通信を休止するボタン" mode="crop" >}}
82: ## 機種変更とデータ管理 {#data-management}
90: {{< guide-anchor "6-nocca-でしないこと" >}}
91: ## 相手の状況を監視する機能はありません {#privacy-design}
95: {{< guide-anchor "7-うまく使えないとき" "家族と接続できない" "意思表示を送れない" "家族側から会話リクエストを送れない" "通知や同期が期待通りに動かない" >}}
96: ## 接続・返信ができないとき {#troubleshooting}
```

### content/privacy/oto-miru.md

```text
9: ## 1. 基本方針
17: ## 2. 本アプリが扱う情報
28: ## 3. マイクと音声認識について
36: ## 4. Apple のサービスについて
42: ## 5. 広告について
52: ## 6. 課金について
58: ## 7. 端末内保存と削除について
66: ## 8. 第三者提供について
72: ## 9. 本公式サイトについて
78: ## 10. 子どもの利用について
82: ## 11. プライバシーポリシーの変更
88: ## 12. お問い合わせ
```

### content/terms/oto-miru.md

```text
11: ## 1. 適用範囲
17: ## 2. 本アプリの内容
23: ## 3. 医療機器ではないこと
29: ## 4. 字幕精度について
37: ## 5. 利用上の注意
45: ## 6. マイク・音声・字幕データ
53: ## 7. 無料版と広告
63: ## 8. オトミル Plus
71: ## 9. 課金・解約・返金
79: ## 10. 禁止事項
91: ## 11. 免責事項
97: ## 12. 仕様変更・提供停止
103: ## 13. 本利用規約の変更
109: ## 14. お問い合わせ
```

### content/faq/oto-miru.md

```text
9: ## 基本
11: ### オトミルはどんなアプリですか？
17: ### どんな場面で使えますか？
21: ### 医療機器ですか？
27: ### 日本語以外にも対応していますか？
31: ### ログインやアカウント登録は必要ですか？
39: ## 対応端末
41: ### 対応している端末は？
45: ### Apple Intelligence は必要ですか？
49: ### 古い端末でも使えますか？
55: ### オフラインで使えますか？
63: ## 使い方
65: {{< guide-anchor "最初に何をすればいいですか" "シンプルモード高齢者とは何ですか" "通常モードとは何ですか" "反転表示とは何ですか" "映画モードはどこにありますか" >}}
66: ### 字幕の始め方・表示の切り替えは？
70: ### 映画館で使ってもいいですか？
76: ### グループ会話は議事録になりますか？
82: ### 字幕の精度は保証されますか？
88: ### 話者ラベルは必ず正しいですか？
96: ## プライバシー
98: ### 音声や字幕は保存されますか？
104: ### 音声や字幕は開発者のサーバーへ送られますか？
110: ### 広告に字幕内容は使われますか？
116: ### 端末内に保存されるものは何ですか？
122: ### データを削除するにはどうすればいいですか？
130: ## 料金・広告・Plus
132: ### 無料で使えますか？
138: ### 広告を見ると何ができますか？
144: ### 字幕中に広告は出ますか？
150: ### オトミル Plus とは何ですか？
156: ### 無料版と Plus で認識精度は変わりますか？
162: ### 購入を復元できますか？
168: ### 解約はどこでできますか？
176: ## トラブルシューティング
178: ### マイクが使えません。
184: ### 字幕が出ません。
193: ### 「この端末では高精度字幕を利用できません」と表示されます。
199: {{< guide-anchor "apple-intelligence-を有効にしてくださいと表示されます" >}}
200: ### モデル準備が終わりません。
204: ### 広告を見ても時間が追加されません。
212: ## サポート
214: ### 問い合わせ先はどこですか？
```

### content/htu/oto-miru.md

```text
11: ## 利用前に確認すること {#1-利用前に確認すること}
17: {{< guide-anchor "2-表示モードを選ぶ" "シンプルモード高齢者" "3-字幕をはじめる" >}}
18: ## 大きなボタンから字幕を始める {#start}
23: {{< guide-image src="images/guides/oto-miru/simple-mode-buttons.png" alt="オトミルのシンプルモードに並ぶテレビ・会話・グループの開始ボタン" mode="crop" >}}
25: {{< guide-anchor "通常モード" >}}
26: ## 通常モードで場面を選ぶ {#standard-mode}
30: {{< guide-image src="images/guides/oto-miru/mode-and-settings.png" alt="通常モード上部のテレビ・会話・グループ・映画の切り替えと、右上の設定ボタン" mode="crop" single-source=true >}}
32: {{< guide-image src="images/guides/oto-miru/start-caption.png" alt="通常モード下部の字幕をはじめるボタン" mode="crop" >}}
34: {{< guide-anchor "4-テレビで使う" "5-会話で使う" "6-グループ会話で使う" >}}
35: ## 字幕を読む・向きを変える・終了する {#read-captions}
41: {{< guide-image src="images/guides/oto-miru/caption-and-controls.png" alt="会話字幕のサンプルと、字幕を止める・反転ボタン" mode="screen" >}}
43: {{< guide-anchor "7-映画で使う" >}}
44: ## 映画モードを使う {#movie}
50: {{< guide-anchor "9-設定を変更する" >}}
51: ## 文字の大きさと聞き取り環境を変える {#settings}
58: {{< guide-image src="images/guides/oto-miru/display-settings.png" alt="表示設定の字幕の文字サイズ、高齢者向けスイッチ、テーマの切り替え" mode="crop" >}}
62: {{< guide-image src="images/guides/oto-miru/listening-environment.png" alt="音声の聞き取り設定で周囲の環境を選ぶ項目" mode="crop" >}}
64: {{< guide-anchor "8-無料版とオトミル-plus" >}}
65: ## 利用時間とPlusを確認する {#usage}
69: {{< guide-image src="images/guides/oto-miru/free-time-and-plus.png" alt="シンプルモード下部の今日の残り無料時間、広告を見て5分追加、Plusに加入するボタン" mode="crop" >}}
73: {{< guide-anchor "10-うまく字幕が出ないとき" "音声が入らない" "端末非対応と表示される" "apple-intelligence-を有効にしてくださいと表示される" "字幕の精度が低い" >}}
74: ## 字幕が出ないとき {#troubleshooting}
```
