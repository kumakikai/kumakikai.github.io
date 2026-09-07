# Utilities Phase 1 — 現行ソースと4文書の読取専用監査

監査日: 2026-09-08（JST）。サイト基準: main `3ab462d3d03247df33420f0657cda305470d8e0b`。対象は GigaPoke、Smokeless、ギャンカレ（Balance Calendar）、SIGNAL。対象アプリを編集せず、サイト本文も変更していない。実装の確認は現在のローカルコード・設定・同梱SDK宣言に基づき、App Storeでの公開版、販売可否、フォーム側設定、実端末通信は確認していない。旧監査を根拠に事実を引き継がず、今回対象ソースを読み直した。

## 1. 範囲と保護

25文書を全文確認した（Guide 8、FAQ 8、Privacy 8、独自Terms 1）。GigaPoke / ギャンカレ / SIGNAL は日本語のみ、Smokelessは ja / en / ko / fr / zh-hant の5言語。ドイツ語SmokelessのProductは存在するが、当該4文書のドイツ語実ページはない。翻訳のないURLの日本語fallbackと既存URL・aliasesを保持する。各アプリの初回操作は git status --short、branch、HEAD確認。すべて既存の未コミット変更あり、差分を保護した。

| アプリrepo | branch / HEAD（初回確認） | 既存変更の主な範囲 |
|---|---|---|
| `/Users/yuya/Projects/povo_manager` | main / `141aa9a845fdc5b4096191c6755c4161144ed25d` | SettingsView、UI tests、設計/公開ドキュメント、Store素材 |
| `/Users/yuya/Projects/smokeless` | main / `3e9e7f38a67f233c1bc4a18c6e56bb50693355d6` | 公開/試験ドキュメント、Watch scheme、Store素材 |
| `/Users/yuya/Projects/gamble_pnl` | main / `8db02fc73957bcaec3fb31215f5d3f2f10ee9d61` | 公開/試験ドキュメント、Store素材、pubspec / Pod lock / project、回帰テスト |
| `/Users/yuya/Projects/signal` | main / `3cee564eddfd1d45841b403c47722d64d8da0389` | Store素材、pubspec / Pod lock、問い合わせテスト |

現時点で独自Termsがあるのは対象内ではGigaPokeだけ。`data/apps.json:148-151`にtermsURLあり、ギャンカレ`:298-300`、Smokeless`:350-352`、SIGNAL`:396-398`にはない。`layouts/_partials/support-data.html:22-24`がApple Standard EULAへfallbackする。日本語Termsを新設する方針では、既存Appleライセンスへの参照も残し、対応言語がない場合の日本語fallbackを維持する。

## 2. 優先して反映する相違・不足

| ID / 優先度 | 現文書の根拠と問題 | 実装根拠 / 修正範囲 |
|---|---|---|
| U-P1 / 高 | `content/privacy/balance-calendar.md:13-23`は広告識別子だけ、Google AdMobも「利用する場合」。`:27`の「第三者に提供することはありません」は広告経由を区別しない絶対表現。購入処理・ローカル購入状態の記載なし。 | 広告と3種の買い切り課金は実装済。端末内記録と、広告SDK・Appleによる処理を区別し、Google/Appleの参照先、購入復元、目的を追加。データ項目は後述。 |
| U-P2 / 高 | `content/privacy/smokeless{,.en,.ko,.fr,.zh-hant}.md:14-26`は同一端末widgetと広告削除購入のみ。`:18`の「端末内でのみ」はWatch対応版まで読むと不足。 | Watch版はローカル実装済だが公開確認なし。記録の日時/種別/同期ID、当日件数、利用権のWatch連携を、公開状態を明示して別段落にする。銘柄追加パックも購入処理対象。iCloud/サーバー同期とWatch連携を混同しない。 |
| U-P3 / 高 | 上記2アプリの広告項目はSDKが扱い得る情報の説明が不十分。Smokelessの「同意状態」から、アプリで同意画面を実装済みとは読ませない。 | GoogleMobileAds 12.14.0の同梱manifestには端末ID、概略位置、広告、操作、診断、性能、クラッシュ情報の宣言あり。独自Firebase/Crashlytics未検出でも「解析・クラッシュ情報を一切送信しない」とは書けない。実際の取得は設定・許可等に依存し、同意取得の実端末動作は要確認。 |
| U-P4 / 中 | `content/privacy/signal.md:11`「端末内で動作」、`:15-17`「外部コンテンツを取得」だけではネットワーク処理が伝わらない。`:31-33`は学習の種類と削除方法がない。 | フィード/API、画像解決、記事WebViewアクセスを明記。学習データはローカル、記事側のCookie・広告等は外部サイトの取扱いとして区別。学習リセットは学習用コレクションのみで、全キャッシュや記事側Cookieの一括削除と説明しない。 |
| U-P5 / 中 | GigaPoke以外のPrivacyは問い合わせを受信した後の目的・保管・削除の説明が不足。Smokelessは「送信するまで送らない」のみ。 | 3アプリはメール下書きにアプリ/バージョン/OS/端末情報を組み込む。送信元メールアドレスと利用者が送った本文は開発者が受け取る。自動送信ではない。対応/調査目的、必要期間の保管、削除依頼先を共通形式で示す。具体的保存期間は未確認のため捏造しない。 |
| U-P6 / 中 | `content/privacy/giga-poke.md:113`のPrivacy Manifest、`:131-135`のGitHub Pages/Cookie、`:45`のExtension列挙、`:139`のDeep Link/外部ログはアプリ利用者には技術用語が多い。 | manifestは開発者向け証拠へ。Extension列挙は「アプリ・共有機能・ウィジェットが同じiPhone内の情報を使う」へ。GitHub Pagesは特典情報の送信先ではなく公式サイト閲覧の話なのでアプリの取扱いから分離/省略候補。サイト全般も適用範囲に残す場合は、Webアクセスで提供元が扱う情報を必要な範囲で別記し、根拠未確認のCookie断定をしない。ホスティング自体にアクセス情報がないと断定もしない。 |
| U-P7 / 中 | GigaPoke Privacyのアカウント/サーバー/同期不使用が`:15`,`:47-52`,`:104-111`,`:117`に反復、非公式説明が`:13`と`:162-164`、Termsにもある。 | 保存/外部処理の節にまとめ、収集しないものを延々列挙しない。非公式性はPrivacy冒頭の対象説明とTermsの固有条件へ。コード等の秘密性・メール本文非保存・ユーザー明示共有という実質は保持。 |
| U-P8 / 中・要確認 | SIGNALアプリ内問い合わせ先はサイト正規メールと一致が確認できない。 | `signal/lib/app/config/support_contact_config.dart:4-6`は`SIGNAL_SUPPORT_EMAIL`未指定時`support@example.com`。現ローカル`ios/Flutter/Generated.xcconfig`にもそのoverrideなし。現行サイト`privacy/signal.md:45-46`の正規メールは保持。設定からの連絡を唯一の確実な窓口とせず、サイトの直接メールを案内。公開バイナリは別確認、アプリは編集しない。 |
| U-P9 / 低 | Smokeless FAQ ko / zh-hant の「我慢とは」`:12-13`はja/en/frにある「禁煙時間を自動計測しない」の補足がない。 | 同じ意味へ補完可。翻訳4本文の中核操作・金額計算・当日限定・購入・広告記述に重大な逆転は見当たらない。 |

## 3. アプリ別の確定情報

以下のアプリ内相対パスは、各節冒頭のrepoを基準とする。引用は現行作業ツリー。

### 3.1 GigaPoke — `/Users/yuya/Projects/povo_manager`

- **情報と保存**: `Shared/PovoCore/Model/PovoCodeRecord.swift:64-74,140-150`は種別、区分、コード/URL、特典名、期限、状態、UUID、日時。Draftには元メール本文を含めない（`:64-67`）。`Shared/PovoBenefitRegistrationPipeline.swift:3`以降の一時テキスト解析→Draft→repositoryの流れで、元メール全文の永続保存はない。App / Shared / ShareExtension / ActionExtension / WidgetExtensionの検索でメールアカウント取得、外部解析、URLSession等の特典送信経路を検出していない。
- **ローカル保存・バックアップ除外**: `Shared/PovoCore/Persistence/PovoCodeRepository.swift:272-299`でstore directoryをバックアップから除外、`:301-309`は通常のNSPersistentContainer、`:742-744`はiOSのファイル保護。NSPersistentStoreRemoteChangeNotificationという名前はローカルCore Data更新通知で、クラウド同期の根拠ではない。利用者向けは「このiPhone内。アプリ独自の同期/復元を提供しない」と説明可能。
- **削除**: `Shared/PovoExpiredBenefitCleanup.swift:36-44`は期限切れ未使用をゴミ箱へ、`PovoUsedBenefitAutoDeletion.swift:36-48`はusedAtを基準に設定された保存期間を過ぎたゴミ箱を完全削除。ゴミ箱への移動は完全削除と異なる。Guideの2週間/30日/60日、デフォルト無効という操作説明は保持する。
- **クリップボードと共有**: `App/AppModel.swift:301-314`は利用者操作でlocalOnlyコピー。`App/PovoCodeDetailView.swift:170-207`に標準ShareLinkあり、特典名とコード/URLを選択先へ渡す。このため「第三者へ一切送らない」にはしない。`App/RootView.swift:178`で明示ペースト、バックグラウンド監視として書かない。
- **通知**: `Shared/PovoNotificationScheduler.swift:261-281`はローカル期限通知。`PovoCodePrivacy.swift:7-31`がコード/URLを含む特典名を一般名へ置換。利用者向けには通知/Widgetでコードを出さない点を保持し、API名は不要。
- **外部リンク**: `App/AppExternalLinks.swift:13-20`に既存Guide/FAQ/Privacy/Termsと正式フォーム。`App/SupportView.swift:109-120`がフォームを開く実導線。フォームURLは `https://forms.gle/Enzmm94LdXRZjP8k9`。Product共通contactURLを同じURLへ揃える根拠あり。`Shared/BenefitUsageSettingsStore.swift:189`のpovo起動URLにはコードを付けない。外部クーポンURLは本人が選んで開く。
- **問い合わせ**: `App/SupportInformation.swift:4-13`は名前、版、ビルド、iOS、端末モデル識別子、言語、地域。`SupportView.swift:194-201`で任意コピー、フォームへの自動入力ではない。フォーム自体の質問/設定/Google側保管は今回未確認。現Privacy`:86-92`に書かれたフォーム項目をコードだけで再保証はできない。
- **広告/課金/AI/クラウド**: 対象コード内に広告SDK、独自解析/Crashlytics、AI、StoreKit課金、アカウント認証、クラウドDBを検出せず。`App/PrivacyInfo.xcprivacy:16-19`も収集なし/Tracking falseを宣言。ただしアプリSDK宣言と本人が行う外部フォーム/標準共有は別。現Terms`:69`の無料/広告なし/アカウント不要と実装は整合する。
- **条件**: `Config/Shared.xcconfig:16` iOS17、`PovoCodeManager.xcodeproj/project.pbxproj:707,734` iPhone family1。非公式性、期限通知/解析結果の非保証、データ消失、利用者によるコード確認は固有Termsに残す。`content/terms/giga-poke.md:15,59`のApple EULA/Privacy参照は必要な文脈リンク。

### 3.2 Smokeless — `/Users/yuya/Projects/smokeless`

- **記録**: `lib/models/entry.dart:1-20`は記録日時、符号付き件数、銘柄キー、任意同期ID。`lib/app/prefs_keys.dart:4-38`は記録、銘柄、通貨/言語、箱本数/価格、アラート、購入権、広告表示タイミング等。`lib/app/tobacco_brands.dart:11-13,47-61`は無料1銘柄/追加後4銘柄と箱本数・価格。
- **保存/削除**: `lib/features/root/root_page.dart:1973-2008`で月ごとの記録をSharedPreferencesへ保存、`:2333-2344`は個別削除とWidget再反映。`_clearAll`自体は存在するが、今回検索ではregister pageに渡されるcallbackの宣言までで、利用者が押せる全件削除UIは確認できていない。Privacyは個別記録削除とアンインストールの範囲を記載し、存在未確認の全データリセット操作を新設したように書かない。
- **Widget**: `lib/main.dart:12-14`と`ios/Runner/Runner.entitlements:5-8`が同じApp Group。`lib/app/shared_daily_counts_bridge.dart:263-277`は当日件数とWatch状態送信。Widgetの記録ボタンは当日分、銘柄はiPhoneの既定設定。医療/HealthKit取得として説明しない。
- **Watch（未公開の可能性を保持）**: `ios/Shared/WatchSyncModels.swift:20-31`はUUID/時刻/±1、`:58-79`は日付・喫煙/我慢件数・利用権・ACK・revision。`ios/SmokelessWatchApp/WatchRecordingStore.swift:24-43,69-85`は端末内未送信キューと状態保存、`ios/Runner/WatchConnectivityBridge.swift:178-182`はペアリング済みWatchへの通信。`InAppPurchaseService.hasAnyPaidEntitlement:42-49`で既存購入権を利用。`ios/Runner.xcodeproj/project.pbxproj:1015`はwatchOS9。Watch専用課金SKU/サーバーアカウントはない。
- **公開状態の留保**: サイト`data/product_details/smokeless.json:4,22,27-28`は審査中・公開後利用。アプリ`docs/RELEASE_NOTES_1_2_0.md:3`は「入稿・公開は未実施」とする下書き。ローカルコードだけで両者の審査状況のどちらが最新か判定不能。Privacy更新は「対応版でApple Watchを利用する場合」という条件と公開前注記を保ち、公開済みへ変えない。
- **広告**: `lib/main.dart:16-18`でMobileAds初期化、`root_page.dart:2483-2498`でInterstitialAd + AdRequest、`:2501-2516`で案内後最大週1回の条件。FAQの記録画面バナー、Calendar/Chartsの全画面広告は実装と整合。GoogleMobileAdsに診断/広告解析があるため単純な「Analyticsなし」は不可（共通SDK節参照）。
- **課金**: `lib/features/settings/purchase/in_app_purchase_service.dart:17-20`は `jp.smokeless.app.removeads` / `jp.smokeless.app.brandpack4`。`:127-133`はbuyNonConsumable / restorePurchases。買い切り2商品で、サブスクリプション/無料試用/自動更新を共通条文として流し込まない。価格・Store販売可否・Family Sharingは今回未確認。設定の購入状態は端末内保存、購入処理はApple。
- **問い合わせ**: `lib/app/support/support_email.dart:6-8,75-95`は正規メール宛に種別/内容/手順/補足＋アプリ名/版/OS/端末モデルを下書き。`email_launcher.dart:8-13`は外部メールアプリを開くだけ。送信するまで問い合わせ内容の送信はない。送信した場合に受信する情報・保管/削除目的をPrivacyに足す。
- **不要機能**: pubspec`:33-52`、lib、iOS本体の範囲でアカウント認証/独自クラウド同期/AI/独自Firebase・Crashlyticsを検出せず。OSバックアップを禁止している証拠はないので「クラウドに絶対出ない」「アプリ削除で全コピー完全消去」は不可。Termsは医療・治療サービスではなく自己記録、金額は設定による計算、効果保証なしという固有条件を残す。

### 3.3 ギャンカレ — `/Users/yuya/Projects/gamble_pnl`

- **記録/保存**: `lib/models/entry.dart:1-6`は日時、収入/支出金額、タグキー。`lib/app/prefs_keys.dart:4-35`はタグ、言語/通貨、購入権、ロック情報等。`lib/features/root/root_page.dart:1576-1593`で月別記録・タグ等をSharedPreferences保存、`:2282-2311`で個別削除/編集。金額/タグはユーザー端末内。開発者へ記録自体を送るAPIを検出せず。
- **ロック/生体認証**: `root_page.dart:2338-2344`でPINとロック状態を端末内保存。`:1750-1760`でOS認証の成否を受ける。顔画像や指紋そのものを収集する説明は不要。PINを開発者が保管するとも、暗号化方式を保証するとも書かない。`PrefsKeys.appLockSkipWidgetLock:19`があるので「必ず全入口でロック」も不可。
- **Widget**: `ios/HiLowWidgetExtension/HiLowWidgetExtension.swift:24-59`は↑/↓のリンクで入力を開く。取引履歴をWatchや外部へ同期する機能ではない。`lib/main.dart:13`のApp Group文字列はentitlementsと相違があるが、このリンク型Widgetを記録共有型と誤記しない。差異のアプリ修正は対象外。
- **広告**: `lib/main.dart:16-18`はMobileAds初期化、`root_page.dart:2506-2509`はInterstitialAd、`:3426-3429`はBannerAd。既存FAQ`:46-48`の表示位置/最大週1回はそのまま残せる。Adsは「使う場合があります」だけでなく、広告ありという機能とGoogleによる情報処理を説明。
- **課金**: `lib/features/settings/purchase/in_app_purchase_service.dart:14-18`は `remove_ads_v3` / `add_tag_pack` / `add_app_lock`。`:95-101`のbuyNonConsumable / restorePurchasesで3種の買い切り。`settings_page.dart:1982-2003`で購入済みIDを端末保存。サブスクSKUなし。`docs/RELEASE_CHECKLIST.md:78-92,155`ではAndroid add_app_lock登録・実課金未確認、Store販売はコードから断定しない。販売中の商品と価格は購入画面で確認する案内が適切。
- **クラウドの区別**: `ios/Runner/Runner.entitlements:5-11`にCloudKit権限があるが、libとRunnerにCKContainer/CKDatabase等の送受信コードはなく、`ios/Runner/AppDelegate.swift:10-27`はOS設定を開くchannelのみ。backup native stringsと未使用翻訳は実装済み機能の証拠にならない。`docs/RELEASE_CHECKLIST.md:102-107`も実装範囲未確認欄。独自の同期/書出しUIは確認できず、既存FAQの「現時点なし」は保持可能。ただしOS側バックアップまで排除しない。
- **問い合わせ**: `lib/app/support/app_support_contact.dart:3-6`は正規メール。`support_contact_service.dart:190-224`は種別/本文/再現手順/補足＋アプリ名/版/OS/端末情報を下書き。`:289-301`付近はiOS端末名とモデルを利用。`:340-365`はmailto起動。送信時は本文/送信元を開発者が受信するため、現Privacy「アプリ入力で氏名等を直接収集しない」とは別に記載。
- **制限/Terms固有**: 記録支援で、投資/勝敗予測/金融取引や助言機能ではない。FAQの数値表による表示、過去日可/未来日不可、タグ、取消し操作は保持。AI・独自Firebase/Crashlytics・アプリ会員アカウントは依存/本体検索で検出せず、広告SDK内の解析は別。

### 3.4 SIGNAL — `/Users/yuya/Projects/signal`

- **ローカル情報**: `lib/data/local/isar/learning_models.dart:5-65`に閲覧記事ID、時刻、タグ、重み、設定、外部を開いた履歴。`isar_learning_repository.dart:47-80`は閲覧/GOOD/BAD、`:101-107`は滞在時間から重みを更新、`:121-138`はfeedback状態保存。生の滞在時間を永久記録するとまでは書かない。`home_screen.dart:773-778`で読了後に滞在時間を渡す。記事表示のための一部キャッシュも端末内Isar。
- **実利用の学習**: 自端末のGOOD/BAD、閲覧傾向で並び順を調整。AIサービスへ学習情報を送るSDK/通信を検出せず、「AIによる解析」を勝手に追加しない。`source_intake_repository`に共有URL/custom site用コードや旧SavedRecord定義が残っていても、現画面の公開機能としては扱わない。FAQ「記事保存機能なし」とモデルの名前だけでは矛盾判定しない。
- **削除**: `lib/data/local/isar/isar_learning_repository.dart:142-167`は閲覧、旧保存、イベント、タグ重み、外部open、feedback/decayを削除。`lib/presentation/settings/settings_screen.dart:195`が設定の学習リセット導線。学習リセットは全設定・RSSキャッシュ・WebView Cookieの一括消去ではない。現Guide`:57-59`の学習履歴リセットを保持。
- **外部取得**: `lib/data/datasources/rss_feed_data_source.dart:55-79`はnote、Zenn、Yahoo、Google News、DevelopersIO、Qiita。`lib/data/remote/hatena_bookmark_remote_data_source.dart:13`にHatena RSS。`lib/app/providers.dart:158-216`が実稼働のscope別DataSourceを組み立てる。無操作でも一覧表示・更新時に取得先へ通信するため、「本人が外部リンクを押すまで一切送信しない」とは書けない。
- **画像/記事通信**: `lib/data/thumbnail/thumbnail_fetch_data_source.dart:67-76,145-163`はHEAD/GET、`rss_feed_data_source.dart:1787`にGoogle favicon URL。記事表示は`lib/presentation/web/article_web_view_page.dart:166-167,223`でJS有効WebView。取得先にIP等の通常アクセス情報が伝わり得る。記事先でCookie/広告/ログインを使うことと、SIGNAL自体に会員登録や広告SDKがあることを分ける。実際に全記事がCookieを設定するとは断定しない。
- **共有**: `lib/data/repositories/share_repository_impl.dart:20`が標準共有。本人が選ぶ外部ブラウザ・共有先は当該サービスの規約/Privacyに従う。記事著作権/提供元、外部サービスの変更で表示できない、正確性/継続提供の保証はしない等は新Termsの固有条件。
- **広告/アカウント/課金**: `pubspec.yaml:30-50`はDio/Isar/WebView/Share等で広告・Analytics/Crashlytics・IAPなし、`ios/Runner/Runner.entitlements:4-5`は空。認証/開発者サーバー同期も対象コードで検出せず。現FAQのログイン不要、記事一覧広告なし/記事先にはあり得るという区別は正しい。広告SDK不使用を記事先広告の全面否定に変えない。
- **問い合わせ**: `BuildSupportContactDraftUseCase`の`:20-41`は手順/補足＋アプリ名/版/OS/端末を下書き、`platform_support_contact_metadata_repository_impl.dart:20-28,47-56,81-95`が情報収集。宛先fallbackの要確認はU-P8。Privacyに自動送信ではない問い合わせ受信・目的・保管/削除を追加。

## 4. 広告SDKの実証範囲

Smokeless・ギャンカレ両方の `ios/Podfile.lock:5-11` に Google-Mobile-Ads-SDK 12.14.0 / GoogleUserMessagingPlatform 3.1.0。各repoの `ios/Pods/Google-Mobile-Ads-SDK/Frameworks/GoogleMobileAdsFramework/GoogleMobileAds.xcframework/ios-arm64/GoogleMobileAds.framework/PrivacyInfo.xcprivacy` を直接読んだ。

| 行 | SDK宣言 | 利用者向け記載での注意 |
|---|---|---|
| 9 / 37 / 51 | その他診断 / 性能 / クラッシュ情報 | Crashlytics不使用と診断送信なしは同義ではない |
| 23 | 概略位置情報 | OS位置情報をアプリが取得すること、正確なGPS座標取得と同義ではない |
| 63 / 77 | 広告情報 / 製品操作 | 広告効果測定や広告SDKの解析と、自社の行動分析を区別 |
| 91-100 | 端末ID、tracking true、広告/Analytics目的 | SDKの宣言が実端末で許可済みIDFAを毎回取得する証拠ではない |

app lib / Runner内のConsent/ATT呼出は今回検出なし。SDKにUMPが同梱されるだけで同意画面表示済みとは保証できない。サイト法務の説明更新と、許可/同意を含むアプリ実機監査を混同しない。SDKの正確な現行ポリシーとStore Privacy申告は別確認。個々のSDKフィールド名をそのまま利用者向け本文へ大量列挙する必要はなく、情報の種類・目的・提供先を平易に記す。

## 5. Guide / FAQ 統一への適用

親担当の共通形式（冒頭はじめに/環境、Guide基本操作→固有機能→困ったとき→問い合わせ、FAQ固有質問→該当data/購入→困ったとき→共通2問）を適用できる。次を保護する。

- **GigaPoke**: Guideの「設定と困ったとき」には実画面/設定手順がある（`:86-92`）。機械的に全部を共通「困ったとき」へ置換せず、設定説明を固有機能として残す。FAQ「Widget表示更新が遅い」`:89-91`は困ったときへ移動可。「登録方法」「使用ボタン」「通知時間」からGuideへの短い参照は役割分離として適切。Privacy/Termsのメール非保存、ローカル保存、コード秘密性の一文は文書の目的に必要で、FAQとの表面上一致だけで削らない。
- **Smokeless（5言語）**: 初回セットアップ、1タップ記録、履歴スワイプ/Undo、Calendar3区分、Chart期間/矢印、Widget既定銘柄、1→4銘柄を保持。FAQは手順をGuideリンクへ委ねており、不要な長文二重掲載は見当たらない。Watch未反映FAQは「困ったとき」に寄せるが、現GuideのWatch説明には対応版の公開前注記/要件/操作があるので共通shortcodeだけで失わせない。
- **ギャンカレ**: Guide「追加購入」`:60-62`は購入/復元の一般操作、FAQは広告位置/無効化と保存制限。Guideに必要な購入復元手順とFAQの制限回答は役割が異なる。FAQの「間違って削除」`:17-18`等は困ったときへ移動可。未来日不可、数値表で予測なし、タグ上限、↑/↓を変更しない。
- **SIGNAL**: Guide「案内を見直す・学習をリセット」`:53-61`には再チュートリアルと消去の操作があり、問い合わせ共通文への置換で消さない。FAQ「記事表示できない」「offline」「feed-limit」は困ったときへ移動可。TODAY最大75 / 他45、本文未保存、更新失敗時は直前記事保持を保持。
- **意味ずれリンク**: 今回対象の本文内Guide/FAQ相互リンクを全件読んだ範囲で、明白な節違いリンクは見当たらない。既存リンクは必要な対象節を指す。見出し順変更・連番除去で自動IDが変わるので、下記既存IDを明示アンカーとして残す必要がある。韓国語Smokeless旧Calendar別名とSIGNAL旧番号アンカーも保護。
- **共通項目不足**: Giga以外のFAQは対応環境/末尾の不具合・問い合わせ2問なし。Guide8ページとも明示的な共通「はじめに」「困ったとき」「お問い合わせ」の揃った形ではない。PrivacyではGigaだけ15節/制定日まであり、他は6–7節、運営者名、情報別目的、保管/削除を欠く。形式を揃えても、存在しないクラウド/課金/AI節を各製品に機能として追加しない。

## 6. 残る要確認

1. 各Storeの公開版/販売中SKU/地域/Family Sharing/価格と、Smokeless Watch審査状況。今回は現在のソースの実装を証明したものでリリース証明ではない。
2. Google広告の現端末での許可・同意・実際に送信したフィールド。SDK同梱宣言から取得有無を一律確定しない。
3. Gigaフォームの現質問・収集設定、全製品の問い合わせ保管期間/削除運用。新しい固定保存日数を捏造しない。
4. SIGNAL公開ビルドの実際の連絡先define。現ローカル既定値はplaceholderであり、公式メールをサイトに残す。
5. ギャンカレCloudKit entitlement/backup文字列は実働サービス証明ではない。OSバックアップまで含めた絶対的非送信/消去保証はしない。
6. 既存個人向け表現を法人、漢字氏名、公開されていない住所/電話へ拡張しない。統一後のTermsの法的妥当性/各国の法要件の保証は本コード監査の範囲外。

## 7. 保存する操作画像・既存アンカー一覧

以下は今回の現行ソースと、同じ基準のローカルbefore-buildから採取。素材を変更せず、見出しだけ整理する場合も画像、alt、既存IDとaliasesを保持する。FAQは画像なし。共通navigation IDは除外した。

### content/htu/giga-poke.md

- 公開パス: `/htu/giga-poke/`
- 現行ソースSHA256: `364f6ee1295425129b1135b2729d320dfcaf5b8ef4de46e33a5f9b9fe4811d2a`
- 画像（引用元行、src、altを保持）:
  - `content/htu/giga-poke.md:19` {{< guide-image src="images/guides/giga-poke/home-add-controls.png" alt="ギガポケのホーム右上の追加ボタンと、一覧下のペーストして追加ボタン" mode="crop" >}}
  - `content/htu/giga-poke.md:21` {{< guide-image src="images/guides/giga-poke/paste-review.png" alt="コピーしたデモ特典の確認画面。3GB、コード、有効期限を確認して右上の登録を押す" mode="screen" >}}
  - `content/htu/giga-poke.md:41` {{< guide-image src="images/guides/giga-poke/benefit-row.png" alt="デモ用ギガコードの特典名、本日までの期限表示、povo 2.0ボタン" mode="crop" >}}
  - `content/htu/giga-poke.md:53` {{< guide-image src="images/guides/giga-poke/benefit-actions.png" alt="特典詳細のpovo 2.0で使う、ゴミ箱に移動、コードをAirDrop等で共有するボタン" mode="crop" >}}
  - `content/htu/giga-poke.md:65` {{< guide-image src="images/guides/giga-poke/trash-list.png" alt="ゴミ箱内のデモ特典と、特典ごとの削除ボタン、右上のゴミ箱を空にするボタン" mode="crop" >}}
  - `content/htu/giga-poke.md:75` {{< guide-image src="images/guides/giga-poke/notification-settings.png" alt="ギガポケ設定の通知タイミングの選択項目" mode="crop" >}}
  - `content/htu/giga-poke.md:90` {{< guide-image src="images/guides/giga-poke/benefit-management-settings.png" alt="使用時にpovo 2.0を開く、自動でゴミ箱へ移動、自動削除の設定" mode="crop" >}}
- 保持ID: `1-特典を登録する`, `コピーペーストする`, `メールから共有する`, `手動で入力する`, `登録に必要な情報`, `2-期限の近い特典を確認する`, `3-特典を使う`, `4-ゴミ箱を管理する`, `5-期限通知を設定する`, `6-widgetを追加する`, `7-設定とサポート`

### content/faq/giga-poke.md

- 公開パス: `/faq/giga-poke/`
- 現行ソースSHA256: `8fb977c3ee9242c13837088c4dcf8d20b91a82517bef520b0553d4882292c4b1`
- 画像: なし。
- 保持ID: `基本`, `ギガポケはどんなアプリですか`, `kddipovoauの公式アプリですか`, `対応端末は`, `料金広告アカウント登録は`, `登録`, `メールを自動で読み取りますか`, `登録方法は`, `何を含めて共有すればよいですか`, `期限が書かれていない特典も登録できますか`, `urlを開いて期限を自動取得しますか`, `複数のコードをまとめて登録できますか`, `同じ特典をもう一度登録するとどうなりますか`, `画像qrコードpdfから読み取れますか`, `使用と管理`, `povo-20コピー開くの違いは`, `povo-20のコード入力画面へ直接移動しますか`, `操作するとすぐ削除されますか`, `期限が切れた特典はどうなりますか`, `ゴミ箱から自動で削除されますか`, `widgetと通知`, `widgetには何が表示されますか`, `widgetの表示がすぐに更新されません`, `通知はいつ届きますか`, `通知にコードやurlは表示されますか`, `データとプライバシー`, `特典データはどこに保存されますか`, `共有したメール本文は保存されますか`, `機種変更や再インストールで復元できますか`, `広告アクセス解析ai解析はありますか`, `お問い合わせ時に登録データは送信されますか`, `困ったとき`, `共有シートにギガポケが表示されません`, `特典を解析できません`, `povo-20アプリを開けません`, `通知が届きません`, `問い合わせ先は`

### content/htu/balance-calendar.md

- 公開パス: `/htu/balance-calendar/`
- 現行ソースSHA256: `b8727065d50e393108ef42e1c9a96428bc740b6894be28335f4cb5ee471469c5`
- 画像（引用元行、src、altを保持）:
  - `content/htu/balance-calendar.md:18` {{< guide-image src="images/guides/balance-calendar/income-expense-buttons.png" alt="ギャンカレの登録画面。緑の上矢印と赤の下矢印、その下にタグの選択ボタン" mode="crop" >}}
  - `content/htu/balance-calendar.md:22` {{< guide-image src="images/guides/balance-calendar/amount-keypad.png" alt="収入金額を入力するテンキーと、下部の緑の確定ボタン" mode="screen" >}}
  - `content/htu/balance-calendar.md:30` {{< guide-image src="images/guides/balance-calendar/date-history-controls.png" alt="ギャンカレの画面上部。中央に日付、右上に履歴を開くレシート型アイコン" mode="crop" >}}
  - `content/htu/balance-calendar.md:40` {{< guide-image src="images/guides/balance-calendar/daily-records.png" alt="収支画面の切替タブと日別一覧。各行に日付と収支、下部に全期間累計を表示" mode="screen" >}}
  - `content/htu/balance-calendar.md:48` {{< guide-image src="images/guides/balance-calendar/widget-entry.png" alt="ホーム画面のギャンカレウィジェット。収入用の緑の上矢印と支出用の赤の下矢印" mode="screen" >}}
  - `content/htu/balance-calendar.md:56` {{< guide-image src="images/guides/balance-calendar/tag-settings.png" alt="タグ設定の編集対象一覧とウィジェット用デフォルトタグの項目" mode="crop" >}}
- 保持ID: `1-最初に用途に合うタグを選ぶ`, `2-登録-画面で収入--支出を記録する`, `3-履歴-を見直して削除や取消しをする`, `4-収支-画面で振り返る`, `5-ホームウィジェットを使う`, `6-設定-を調整する`, `7-追加購入を使う`

### content/faq/balance-calendar.md

- 公開パス: `/faq/balance-calendar/`
- 現行ソースSHA256: `a5dc3dc5ebfe30a7a6fe7c1547b6bc6a996a416a54d714114ec5ed0e4f8b8f54`
- 画像: なし。
- 保持ID: `基本`, `ギャンカレはどんなアプリですか`, `ギャンブル以外の用途でも使えますか`, `過去日の記録はできますか`, `間違って削除した記録は戻せますか`, `振り返りと設定`, `何を確認できますか`, `折れ線グラフや予測アドバイスはありますか`, `タグはいくつまで使えますか`, `アプリロックはありますか`, `ホームウィジェットは使えますか`, `言語や通貨は変更できますか`, `課金と保存`, `広告はどこに表示されますか`, `広告を消せますか`, `バックアップや自動同期データのエクスポートはありますか`

### content/htu/smokeless.en.md

- 公開パス: `/en/htu/smokeless/`
- 現行ソースSHA256: `aede900f555f97de1788184fe759f9d836140c84c5e538555aa581cbd56b526c`
- 画像（引用元行、src、altを保持）:
  - `content/htu/smokeless.en.md:19` {{< guide-image src="images/guides/smokeless/en/record-buttons.png" alt="Smokeless logging controls: green Avoided on the left and red Smoked on the right, with today’s counts" mode="crop" >}}
  - `content/htu/smokeless.en.md:29` {{< guide-image src="images/guides/smokeless/en/history.png" alt="Smokeless history showing today’s record times and smoked or avoided icons" mode="crop" >}}
  - `content/htu/smokeless.en.md:37` {{< guide-image src="images/guides/smokeless/en/calendar.png" alt="Smokeless Calendar tabs and daily counts with money totals" mode="screen" >}}
  - `content/htu/smokeless.en.md:43` {{< guide-image src="images/guides/smokeless/en/chart.png" alt="Smokeless chart with period controls and smoked, avoided and average lines" mode="screen" >}}
  - `content/htu/smokeless.en.md:56` {{< guide-image src="images/guides/smokeless/en/settings.png" alt="Smokeless brand settings for pack size, pack price and the widget default brand" mode="crop" >}}
- 保持ID: `1-check-the-first-tutorial-and-pack-settings`, `2-record-from-log`, `3-review-todays-records-in-history`, `4-review-by-day-month-and-year-in-calendar`, `5-check-recent-changes-in-charts`, `6-use-the-home-widget`, `7-adjust-settings`, `apple-watch`, `watch-guide-title`
- 共通Watch図: `data/product_details/smokeless.json:8` の `images/apps/smokeless/watch/recording-ui.png`。`layouts/_partials/watch-guide.html:7-14` の `apple-watch` / `watch-guide-title`、要件・公開前注記・手順・altを保持。

### content/htu/smokeless.fr.md

- 公開パス: `/fr/htu/smokeless/`
- 現行ソースSHA256: `71f4a6dac450a610f4bc7d4ba4da07bf3485d9d39f38525f107d27089cbd1a3a`
- 画像（引用元行、src、altを保持）:
  - `content/htu/smokeless.fr.md:19` {{< guide-image src="images/guides/smokeless/fr/record-buttons.png" alt="Boutons de saisie Smokeless : cigarette évitée en vert à gauche, fumée en rouge à droite" mode="crop" >}}
  - `content/htu/smokeless.fr.md:29` {{< guide-image src="images/guides/smokeless/fr/history-controls.png" alt="En haut de Saisie, icône de ticket à droite pour ouvrir l’historique" mode="crop" >}}
  - `content/htu/smokeless.fr.md:37` {{< guide-image src="images/guides/smokeless/fr/calendar.png" alt="Calendrier Smokeless avec onglets Jour, Mois et Année et totaux quotidiens" mode="screen" >}}
  - `content/htu/smokeless.fr.md:43` {{< guide-image src="images/guides/smokeless/fr/chart.png" alt="Graphiques Smokeless et commandes de période, avec courbes des cigarettes fumées et évitées" mode="screen" >}}
- 保持ID: `1-vérifiez-le-premier-tutoriel-et-les-réglages-du-paquet`, `2-enregistrez-depuis-saisie`, `3-revoyez-les-enregistrements-du-jour-depuis-historique`, `4-revoyez-par-jour-mois-et-année-dans-calendrier`, `5-vérifiez-les-changements-récents-dans-graphiques`, `6-utilisez-le-widget-daccueil`, `7-ajustez-les-réglages`, `apple-watch`, `watch-guide-title`
- 共通Watch図: `data/product_details/smokeless.json:8` の `images/apps/smokeless/watch/recording-ui.png`。`layouts/_partials/watch-guide.html:7-14` の `apple-watch` / `watch-guide-title`、要件・公開前注記・手順・altを保持。

### content/htu/smokeless.ko.md

- 公開パス: `/ko/htu/smokeless/`
- 現行ソースSHA256: `a67c2843843945070426a4587d919808102aa0e68df75fda94d31bc3814d4970`
- 画像（引用元行、src、altを保持）:
  - `content/htu/smokeless.ko.md:19` {{< guide-image src="images/guides/smokeless/ko/record-buttons.png" alt="왼쪽 초록색 참음 버튼과 오른쪽 빨간색 흡연 버튼, 각 버튼에 표시된 오늘 기록 수" mode="crop" >}}
  - `content/htu/smokeless.ko.md:29` {{< guide-image src="images/guides/smokeless/ko/history-controls.png" alt="기록 화면 오른쪽 위에 있는 당일 기록을 여는 영수증 아이콘" mode="crop" >}}
  - `content/htu/smokeless.ko.md:38` {{< guide-image src="images/guides/smokeless/ko/calendar.png" alt="일별·월별·연별 탭과 날짜별 기록 수 및 금액을 표시하는 캘린더" mode="screen" >}}
  - `content/htu/smokeless.ko.md:44` {{< guide-image src="images/guides/smokeless/ko/chart.png" alt="기간 선택과 흡연·참음·흡연 평균 추이를 보여 주는 차트" mode="screen" >}}
- 保持ID: `1-첫-튜토리얼과-한-갑-설정을-확인합니다`, `2-기록-화면에서-기록합니다`, `3-기록-에서-당일-기록을-확인합니다`, `4-캘린더-에서-일별--월별--연별로-되돌아봅니다`, `4-캘린더로-기록을-확인합니다`, `5-차트-에서-최근-변화를-봅니다`, `6-홈-위젯을-사용합니다`, `7-설정-을-조정합니다`, `apple-watch`, `watch-guide-title`
- 共通Watch図: `data/product_details/smokeless.json:8` の `images/apps/smokeless/watch/recording-ui.png`。`layouts/_partials/watch-guide.html:7-14` の `apple-watch` / `watch-guide-title`、要件・公開前注記・手順・altを保持。

### content/htu/smokeless.md

- 公開パス: `/htu/smokeless/`
- 現行ソースSHA256: `b23238be6ce9251aec1c7bfbfd1d37c77e0c5270ed2db6986368f4071ef9d10f`
- 画像（引用元行、src、altを保持）:
  - `content/htu/smokeless.md:19` {{< guide-image src="images/guides/smokeless/ja/record-buttons.png" alt="すわなびの記録ボタン。左の緑が我慢、右の赤が喫煙で、各ボタン内に当日の回数を表示" mode="crop" >}}
  - `content/htu/smokeless.md:29` {{< guide-image src="images/guides/smokeless/ja/history.png" alt="すわなびの当日履歴。時刻と我慢・喫煙のアイコンが並ぶ記録一覧" mode="crop" >}}
  - `content/htu/smokeless.md:37` {{< guide-image src="images/guides/smokeless/ja/calendar.png" alt="すわなびのカレンダー。日別・月別・年別タブと、日付ごとの喫煙・我慢回数と金額" mode="screen" >}}
  - `content/htu/smokeless.md:43` {{< guide-image src="images/guides/smokeless/ja/chart.png" alt="すわなびのグラフ。週・月・3か月の切替と、我慢・喫煙・喫煙平均の推移" mode="screen" >}}
  - `content/htu/smokeless.md:56` {{< guide-image src="images/guides/smokeless/ja/settings.png" alt="すわなびの銘柄設定。既定銘柄の本数と価格、追加購入が必要な銘柄を追加の項目" mode="crop" >}}
- 保持ID: `1-初回チュートリアルと本数設定を確認する`, `2-記録-画面で喫煙--我慢を記録する`, `3-履歴-から当日の記録を見直す`, `4-カレンダー-で日別--月別--年別に振り返る`, `5-グラフ-で最近の変化を見る`, `6-ホームウィジェットを使う`, `7-設定-を調整する`, `apple-watch`, `watch-guide-title`
- 共通Watch図: `data/product_details/smokeless.json:8` の `images/apps/smokeless/watch/recording-ui.png`。`layouts/_partials/watch-guide.html:7-14` の `apple-watch` / `watch-guide-title`、要件・公開前注記・手順・altを保持。

### content/htu/smokeless.zh-hant.md

- 公開パス: `/zh-hant/htu/smokeless/`
- 現行ソースSHA256: `1ea74722defd122bc5d3d3e52169f21e2d59203d2b45e6ca97e7122cf8759431`
- 画像（引用元行、src、altを保持）:
  - `content/htu/smokeless.zh-hant.md:19` {{< guide-image src="images/guides/smokeless/zh-hant/record-buttons.png" alt="左側綠色忍住按鈕與右側紅色吸菸按鈕，按鈕中顯示今天的次數" mode="crop" >}}
  - `content/htu/smokeless.zh-hant.md:29` {{< guide-image src="images/guides/smokeless/zh-hant/history-controls.png" alt="記錄畫面右上角用來開啟當日履歷的收據圖示" mode="crop" >}}
  - `content/htu/smokeless.zh-hant.md:37` {{< guide-image src="images/guides/smokeless/zh-hant/calendar.png" alt="日曆的日月年切換，以及各日期的吸菸、忍住次數與金額" mode="screen" >}}
  - `content/htu/smokeless.zh-hant.md:43` {{< guide-image src="images/guides/smokeless/zh-hant/chart.png" alt="圖表的期間選擇與吸菸、忍住、吸菸平均趨勢" mode="screen" >}}
- 保持ID: `1-確認首次教學與每包設定`, `2-在-記錄-畫面中記錄`, `3-從-履歷-查看當日記錄`, `4-在-日曆-以日--月--年回顧`, `5-在-圖表-查看近期變化`, `6-使用主畫面小工具`, `7-調整-設定`, `apple-watch`, `watch-guide-title`
- 共通Watch図: `data/product_details/smokeless.json:8` の `images/apps/smokeless/watch/recording-ui.png`。`layouts/_partials/watch-guide.html:7-14` の `apple-watch` / `watch-guide-title`、要件・公開前注記・手順・altを保持。

### content/faq/smokeless.en.md

- 公開パス: `/en/faq/smokeless/`
- 現行ソースSHA256: `9d969ddb89b5a704d2c9763bbce44b6b368125120e981b3e2fa50d8c7e95364f`
- 画像: なし。
- 保持ID: `basics`, `what-kind-of-app-is-smokeless`, `what-does-avoided-record`, `is-this-a-medical-app`, `is-there-a-first-time-tutorial`, `recording-and-review`, `what-can-i-check`, `how-is-the-money-amount-calculated`, `can-i-restore-a-record-deleted-by-mistake`, `can-i-record-past-dates-too`, `data-and-storage`, `where-is-the-data-stored`, `are-backup-or-cloud-sync-available`, `do-i-need-to-register-an-account`, `features`, `is-there-a-home-widget`, `can-i-add-multiple-brands`, `is-there-an-over-smoking-alert`, `where-are-ads-shown`, `can-i-remove-ads`, `can-i-change-the-language-or-currency`, `why-are-apple-watch-records-not-appearing-on-iphone`

### content/faq/smokeless.fr.md

- 公開パス: `/fr/faq/smokeless/`
- 現行ソースSHA256: `ff118b4127b6a74cad80514a7cb22754593a2b3d0f34ad64484ab3e1e8aa4f49`
- 画像: なし。
- 保持ID: `généralités`, `quel-type-dapplication-est-smokeless-`, `que-signifie-évitée-`, `est-ce-une-application-médicale-`, `y-a-t-il-un-tutoriel-au-premier-lancement-`, `enregistrement-et-relecture`, `que-puis-je-consulter-`, `comment-le-montant-est-il-calculé-`, `puis-je-restaurer-un-enregistrement-supprimé-par-erreur-`, `puis-je-enregistrer-des-jours-passés-`, `données-et-stockage`, `où-les-données-sont-elles-stockées-`, `existe-t-il-une-sauvegarde-ou-une-synchronisation-cloud-`, `dois-je-créer-un-compte-`, `fonctions`, `existe-t-il-un-widget-daccueil-`, `puis-je-ajouter-plusieurs-marques-`, `existe-t-il-une-alerte-de-surconsommation-`, `où-les-publicités-sont-elles-affichées-`, `puis-je-supprimer-les-publicités-`, `puis-je-changer-la-langue-ou-la-devise-`, `pourquoi-les-enregistrements-apple-watch-napparaissent-ils-pas-sur-liphone-`

### content/faq/smokeless.ko.md

- 公開パス: `/ko/faq/smokeless/`
- 現行ソースSHA256: `21b4a48e444d4e37979b8aee49c9f1adb61190598edf4c1ef81f19feacf15c11`
- 画像: なし。
- 保持ID: `기본`, `smokeless는-어떤-앱인가요`, `참음-기록-은-무엇을-기록하나요`, `의료-앱인가요`, `첫-실행-튜토리얼이-있나요`, `기록과-되돌아보기`, `무엇을-확인할-수-있나요`, `금액은-어떻게-계산되나요`, `실수로-삭제한-기록을-되돌릴-수-있나요`, `지난-날짜-기록도-가능한가요`, `데이터와-저장`, `데이터는-어디에-저장되나요`, `백업이나-클라우드-동기화가-있나요`, `계정-등록이-필요한가요`, `기능`, `홈-위젯을-사용할-수-있나요`, `브랜드를-여러-개-등록할-수-있나요`, `흡연-과다-알림이-있나요`, `광고는-어디에-표시되나요`, `광고를-제거할-수-있나요`, `언어나-통화를-변경할-수-있나요`, `apple-watch-기록이-iphone에-표시되지-않아요`

### content/faq/smokeless.md

- 公開パス: `/faq/smokeless/`
- 現行ソースSHA256: `ec04c431d54f3600acc71cedfbe96a1acd0a4f14c5f0255961b563f4586f0ad3`
- 画像: なし。
- 保持ID: `基本`, `すわなびはどんなアプリですか`, `我慢は何を記録しますか`, `医療アプリですか`, `初回チュートリアルはありますか`, `記録と振り返り`, `何を確認できますか`, `金額はどう計算されますか`, `間違って削除した記録は戻せますか`, `過去日の記録もできますか`, `データと保存`, `データはどこに保存されますか`, `バックアップやクラウド同期はありますか`, `アカウント登録は必要ですか`, `機能`, `ホームウィジェットは使えますか`, `銘柄は複数登録できますか`, `吸いすぎアラートはありますか`, `広告はどこに表示されますか`, `広告を消せますか`, `言語や通貨は変更できますか`, `apple-watchの記録がiphoneに反映されません`

### content/faq/smokeless.zh-hant.md

- 公開パス: `/zh-hant/faq/smokeless/`
- 現行ソースSHA256: `dd92e2b4d0c559a341c0e2627e2d4013501403d5d929cfa20bfdd9a299440d11`
- 画像: なし。
- 保持ID: `基本`, `smokeless-是什麼樣的應用程式`, `記錄忍住-記錄的是什麼`, `這是醫療-app-嗎`, `有首次教學嗎`, `記錄與回顧`, `可以查看哪些內容`, `金額是如何計算的`, `誤刪的記錄可以還原嗎`, `可以記錄過去日期嗎`, `資料與儲存`, `資料儲存在哪裡`, `有備份或雲端同步嗎`, `需要註冊帳號嗎`, `功能`, `有主畫面小工具嗎`, `可以新增多個品牌嗎`, `有-吸太多提醒-嗎`, `廣告會顯示在哪裡`, `可以移除廣告嗎`, `可以更改語言或貨幣嗎`, `apple-watch記錄沒有顯示在iphone上`

### content/htu/signal.md

- 公開パス: `/htu/signal/`
- 現行ソースSHA256: `b08dde44f9c3e2f0709d6cc933d31f9e656ca178ee093cd58e7ff6610e2c7a0e`
- 画像（引用元行、src、altを保持）:
  - `content/htu/signal.md:17` {{< guide-image src="images/guides/signal/tabs-and-article.png" alt="SIGNAL上部の3タブと、右上にグッド・バッドのボタンがある記事カード" mode="crop" >}}
  - `content/htu/signal.md:30` {{< guide-image src="images/guides/signal/article-menu.png" alt="SIGNALの記事画面上部にある閉じるボタンと右上のメニューボタン" mode="crop" >}}
  - `content/htu/signal.md:41` {{< guide-image src="images/guides/signal/source-switches.png" alt="設定の「記事取得サイト設定」とnote・Zennの配信スイッチ" mode="crop" >}}
  - `content/htu/signal.md:49` {{< guide-image src="images/guides/signal/text-and-theme.png" alt="設定上部のテーマ選択とSmall・Normal・Largeの文字サイズ選択" mode="crop" >}}
- 保持ID: `2-まずは-today-を見る`, `3-creators-と-news-を使い分ける`, `browse`, `4-記事を開く`, `read`, `5-設定-を調整する`, `sources`, `appearance`, `1-初回はチュートリアルを見る`, `settings-help`

### content/faq/signal.md

- 公開パス: `/faq/signal/`
- 現行ソースSHA256: `1dde4cbd65ac0dd490b8fb283b6c52e566ca62ba0c2109ec457af942d800ab29`
- 画像: なし。
- 保持ID: `基本`, `signalはどんなアプリですか`, `ログインは必要ですか`, `どの配信源に対応していますか`, `配信源は切り替えられますか`, `記事はどこで開きますか`, `記事の保存機能はありますか`, `通知はありますか`, `広告はありますか`, `offline`, `feed-limit`, `学習と保存`, `表示順はどう調整されますか`, `学習データはどこに保存されますか`, `学習データはリセットできますか`, `個人情報やアカウント情報は必要ですか`, `テーマや文字サイズは変えられますか`

## 8. 文書全件の構造インベントリ

表のH2は現行順序。構造統一時に事実差を保持するためのbaseline。

| ファイル | 言語 | H2（現在の順序） |
|---|---|---|
| `content/htu/giga-poke.md` | ja | 特典を登録する {#1-特典を登録する} → 期限と利用ボタンを確認する {#2-期限の近い特典を確認する} → 特典を使う {#3-特典を使う} → ゴミ箱から戻す・削除する {#4-ゴミ箱を管理する} → 期限の通知を設定する {#5-期限通知を設定する} → ウィジェットを追加する {#6-widgetを追加する} → 設定と困ったときの案内 {#7-設定とサポート} |
| `content/faq/giga-poke.md` | ja | 基本 → 登録 → 使用と管理 → Widgetと通知 → データとプライバシー → 困ったとき |
| `content/privacy/giga-poke.md` | ja | 1. 基本方針 → 2. 本アプリが取り扱う情報 → 3. 共有したメール本文 → 4. 保存場所、同期、バックアップ → 5. クリップボード、通知、Widget → 6. 外部通信と第三者サービス → 7. 収集しない情報と利用しない機能 → 8. データの共有と第三者提供 → 9. ユーザーによる管理と削除 → 10. 本公式サイト → 11. セキュリティ → 12. 子どもの利用 → 13. 本ポリシーの変更 → 14. お問い合わせ → 15. 非公式アプリであること |
| `content/terms/giga-poke.md` | ja | 1. 適用範囲 → 2. 本アプリの内容 → 3. 非公式アプリであること → 4. 利用上の注意 → 5. コードとURLの管理 → 6. データの保存と削除 → 7. 外部サービス → 8. 料金と広告 → 9. 禁止事項 → 10. 知的財産権 → 11. 免責事項 → 12. 仕様変更、提供停止 → 13. 本規約の変更 → 14. 準拠法と管轄 → 15. お問い合わせ |
| `content/htu/balance-calendar.md` | ja | 1. 最初に用途に合うタグを選ぶ → 2. `登録` 画面で収入 / 支出を記録する → 3. `履歴` を見直して削除や取消しをする → 4. `収支` 画面で振り返る → 5. ホームウィジェットを使う → 6. `設定` を調整する → 7. 追加購入を使う |
| `content/faq/balance-calendar.md` | ja | 基本 → 振り返りと設定 → 課金と保存 |
| `content/privacy/balance-calendar.md` | ja | 1. 収集する情報について → 2. 広告について → 3. 個人情報の第三者提供について → 4. データの保存について → 5. プライバシーポリシーの変更 → 6. お問い合わせ |
| `content/htu/smokeless.en.md` | en | 1. Check the first tutorial and pack settings → 2. Record from `Log` → 3. Review today's records in `History` → 4. Review by day, month, and year in `Calendar` → 5. Check recent changes in `Charts` → 6. Use the home widget → 7. Adjust `Settings` |
| `content/htu/smokeless.fr.md` | fr | 1. Vérifiez le premier tutoriel et les réglages du paquet → 2. Enregistrez depuis `Saisie` → 3. Revoyez les enregistrements du jour depuis `Historique` → 4. Revoyez par jour, mois et année dans `Calendrier` → 5. Vérifiez les changements récents dans `Graphiques` → 6. Utilisez le widget d'accueil → 7. Ajustez les `Réglages` |
| `content/htu/smokeless.ko.md` | ko | 1. 첫 튜토리얼과 한 갑 설정을 확인합니다 → 2. `기록` 화면에서 기록합니다 → 3. `기록` 에서 당일 기록을 확인합니다 → 4. 캘린더로 기록을 확인합니다 → 5. `차트` 에서 최근 변화를 봅니다 → 6. 홈 위젯을 사용합니다 → 7. `설정` 을 조정합니다 |
| `content/htu/smokeless.md` | ja | 1. 初回チュートリアルと本数設定を確認する → 2. `記録` 画面で喫煙 / 我慢を記録する → 3. `履歴` から当日の記録を見直す → 4. `カレンダー` で日別 / 月別 / 年別に振り返る → 5. `グラフ` で最近の変化を見る → 6. ホームウィジェットを使う → 7. `設定` を調整する |
| `content/htu/smokeless.zh-hant.md` | zh-hant | 1. 確認首次教學與每包設定 → 2. 在 `記錄` 畫面中記錄 → 3. 從 `履歷` 查看當日記錄 → 4. 在 `日曆` 以日 / 月 / 年回顧 → 5. 在 `圖表` 查看近期變化 → 6. 使用主畫面小工具 → 7. 調整 `設定` |
| `content/faq/smokeless.en.md` | en | Basics → Recording and review → Data and storage → Features |
| `content/faq/smokeless.fr.md` | fr | Généralités → Enregistrement et relecture → Données et stockage → Fonctions |
| `content/faq/smokeless.ko.md` | ko | 기본 → 기록과 되돌아보기 → 데이터와 저장 → 기능 |
| `content/faq/smokeless.md` | ja | 基本 → 記録と振り返り → データと保存 → 機能 |
| `content/faq/smokeless.zh-hant.md` | zh-hant | 基本 → 記錄與回顧 → 資料與儲存 → 功能 |
| `content/privacy/smokeless.en.md` | en | 1. Information collected → 2. On-device storage and widget integration → 3. Advertising and in-app purchases → 4. Contact feature → 5. Provision of personal information to third parties → 6. Changes to this privacy policy → 7. Contact |
| `content/privacy/smokeless.fr.md` | fr | 1. Informations collectées → 2. Stockage sur l'appareil et intégration du widget → 3. Publicité et achats intégrés → 4. Fonction de contact → 5. Communication des données personnelles à des tiers → 6. Modifications de cette politique de confidentialité → 7. Contact |
| `content/privacy/smokeless.ko.md` | ko | 1. 수집하는 정보 → 2. 기기 내 저장과 위젯 연동 → 3. 광고 및 인앱 구매 → 4. 문의 기능 → 5. 개인정보의 제3자 제공 → 6. 개인정보 처리방침의 변경 → 7. 문의 |
| `content/privacy/smokeless.md` | ja | 1. 取得する情報について → 2. 端末内保存とウィジェット連携について → 3. 広告およびアプリ内購入について → 4. お問い合わせについて → 5. 個人情報の第三者提供について → 6. プライバシーポリシーの変更 → 7. お問い合わせ |
| `content/privacy/smokeless.zh-hant.md` | zh-hant | 1. 蒐集的資訊 → 2. 裝置內儲存與小工具整合 → 3. 廣告與 App 內購買 → 4. 聯絡功能 → 5. 向第三方提供個人資訊 → 6. 隱私權政策的變更 → 7. 聯絡方式 |
| `content/htu/signal.md` | ja | 1. タブを選んで記事を探す {#browse} → 2. 記事を読む・共有する {#read} → 3. 配信源を選ぶ {#sources} → 4. 文字サイズと配色を変える {#appearance} → 5. 案内を見直す・学習をリセットする {#settings-help} |
| `content/faq/signal.md` | ja | 基本 → 学習と保存 |
| `content/privacy/signal.md` | ja | 1. 取得する情報について → 2. 外部コンテンツの取得について → 3. 広告・解析ツールについて → 4. 個人情報の第三者提供について → 5. データの保存について → 6. プライバシーポリシーの変更 → 7. お問い合わせ |
