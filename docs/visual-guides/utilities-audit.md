# すわなび・ギャンカレ Visual Guide 監査

監査日: 2026-09-07。SIGNAL は root 担当 `signal-audit.md` / `signal-assets.json` を参照。

## 対象

- `content/htu/balance-calendar.md` / `content/faq/balance-calendar.md`
- `content/htu/smokeless{,.en,.fr,.ko,.zh-hant}.md` と対応する5 FAQ
- 計6使い方・6FAQ。既存URL・aliases・h2/h3見出しを保持。

## 仕様の根拠

### ギャンカレ

Repo: `/Users/yuya/Projects/gamble_pnl`, HEAD `8db02fc73957bcaec3fb31215f5d3f2f10ee9d61` と既存ローカル変更。Store 1.4.0はrootの `store-snapshot.json` で確認。

- `lib/features/register/register_page.dart`: タグ、日付選択、履歴。`action_button.dart` の矢印アイコン。テンキーの確定が登録操作。
- `lib/features/graph/graph_page.dart`: 日別/月別/カテゴリ別、全期間累計、詳細内編集・削除。
- `lib/features/settings/settings_page.dart`: タグとウィジェット既定タグ、全般、その他、購入。
- `lib/features/settings/purchase/in_app_purchase_service.dart`: remove_ads_v3 / add_tag_pack / add_app_lock。公開商品の価格・取得状態は端末App Storeに依存するためWebへ固定価格や購入可否を追加しない。
- `docs/FEATURE_REGISTER.md`, `FEATURE_GRAPH.md`, `FEATURE_SETTINGS_TAGS.md` と照合。

変更:
- 実画面の主要ボタンは文字「+収入」「−支出」ではなく「↑」「↓」。ガイドをアイコンに合わせた。
- タグ選択 → 矢印 → テンキー → 確定をStep化。履歴のレシート型アイコンと左スワイプを明記。
- Widgetは単に「そのまま記録」とせず、アプリの金額入力が開くことを明記。
- 収支詳細内の編集/削除、空日表示、設定の階層を追加。
- FAQの登録・タグ・Widget操作はガイド内の該当見出しへ直接リンク。
- 初期タグ設定は短い文章で説明、購入は実際のストア表示へ案内。これらにスクリーンショットを無理に追加しない。
- `root_page.dart:2520-2560` の実装に従い、週次広告は案内から1週間以降・最大週1回・配信状況に依存する説明へ修正。必ず毎週表示されるとは記載しない。

素材:
- 全6画像は `artifacts/app_store_screenshots_2026-09-03/raw/iphone_17_pro_max/` の実Simulator画面から正確なピクセルcrop。
- `income-expense-buttons`、`date-history-controls`、`tag-settings`、`widget-entry` は操作対象のみ。
- `amount-keypad` は入力欄・数字・確定の位置関係を保つ。`daily-records` は切替タブ・一覧・累計・下部ナビを保つ。2枚を screen 幅で配信。
- マーケティング画像、AI画像、模造UIを使用していない。

### すわなび

Repo: `/Users/yuya/Projects/smokeless`, HEAD `3e9e7f38a67f233c1bc4a18c6e56bb50693355d6` と既存ローカル変更。公開1.1.1、審査中1.2.0はroot snapshotと既存Watch監査を参照。

- `lib/features/register/register_page.dart`: 左緑/右赤の1タップ記録、履歴アイコン、`DismissDirection.endToStart`で履歴左スワイプ。過去日入力のUIはない。
- `lib/app/tobacco_brands.dart:12-13`: 通常1銘柄/パック購入後4銘柄。
- `lib/features/settings/settings_page.dart`: 全般の銘柄設定、通貨/言語、喫煙本数アラート。初期設定の本数と価格は銘柄ごとに管理。
- `lib/features/graph/graph_page.dart`: day/month/allTime内部区分だが、ユーザーの表示ラベルは日別・月別・年別。内部名を使い方へ露出しない。
- `lib/features/chart/chart_page.dart`: 週/月/3か月と期間矢印。
- `lib/l10n/app_{ja,en,fr,ko,zh}.arb`: 正式ボタン名称、Undo はja「取消し」/en「Undo」/fr「Annuler」/ko「실행 취소」/zh「復原」。
- `docs/FEATURE_RECORDING.md`, `FEATURE_INSIGHTS.md`, `FEATURE_TOBACCO_BRANDS.md`, `FEATURE_SETTINGS_SUPPORT.md`, `FEATURE_WIDGET.md` と照合。

変更:
- 全5言語を短い手順へ。文字ラベルではなく緑の斜線入りたばこ/赤いたばこアイコンを操作対象として記載。
- 「我慢」は吸いたいと思ったが吸わずに済んだ1回。自動的な禁煙時間のカウントという誤解を避ける。
- 旧「最大4銘柄」無条件説明を、通常1銘柄/銘柄追加パック購入後合計4に修正。
- 韓国語/繁体字の古い取消し文言を現行ARBの「실행 취소」/「復原」に更新。
- 初回から毎週必ず広告が出ると読める文章を、広告案内から1週間以降・最大週1回・表示される場合ありへ修正。
- FAQの操作概要は画像ガイドへ、課金・保存・過去日不可等の例外はFAQに保持。
- Apple Watchは既存 `watch-guide` の実画面・4手順・審査中表示をそのまま維持。FAQから `#apple-watch` へ直リンク。Watch連携をクラウド同期と混同しない。

撮影・素材:
- 他の起動中Simulatorを触らず、割当 `5455BA32-3B45-4C7B-85CA-8E1CAAB351D3` (Smokeless Sync QA iPhone)のみ起動。
- CUA初回getAppが長時間応答せず中断されたため、System EventsでSimulator自身のAXGroup位置・サイズを読み、実画面座標で操作。`simctl io <UUID> screenshot`で取得。
- JAの初回撮影は公開同等の既存1.1.1(2)QAビルドで行い、3回の実操作で当日の我慢2回・喫煙1回のデモを追加。最終採用画像はJA/ENとも下記の現行1.2.0(3)へインストール更新後に再撮影した10枚。記録、履歴、銘柄設定、カレンダー、グラフを実際に開いた。既存iPhone機能の画面であり、審査中Watch機能を提供済みとは扱わない。
- 現行1.2.0(3)は `flutter build ios --simulator --debug --no-pub -d <UUID>` 成功(195.1s)。最初のdevice未指定はWatch companionのため失敗し、明示指定で解消。
- fr/ko/zh-Hantは2026-09-03 `sources/ui/<locale>/{register,graph,chart}.png` の現行UI原画を再利用。配信言語に合う実画面を使用。
- 履歴・操作ボタン・設定をcrop。グラフは期間選択から凡例まで関係を保ってscreen表示。テスト広告・Debug項目は配信画像に含めない。
- 全28ファイルの元パス・SHA-256・crop座標・取得日・対象版は `utilities-assets.json`。JA/EN10枚の最終cropは `/private/tmp/smokeless-guide-final-crops.jpg` で並べて目視し、ボタン、行、凡例、銘柄項目が切れていないことを確認。
- 撮影後はこの作業で起動した専用Simulatorだけをshutdown。他の起動中デバイスは変更しない。

## アプリ側の変更

アプリコードを編集せず、既存dirtyを保持。新規テスト・本番課金・実機インストール・実ユーザーデータ使用なし。Webの見た目/リンク/画像配信確認はrootの共通buildとブラウザQAで行う。

## 素材数・未対応範囲

- ギャンカレ6枚、すわなびJA5/EN5/fr4/ko4/zh-Hant4枚。計28枚すべて実画面のcrop。新規Simulator10枚、既存raw再利用18枚。
- 長い画像はscreenモードで上部のOSステータスバーだけを除き、操作領域全体・下部ナビ・グラフ凡例を保持。操作ボタン、履歴、設定、Widgetは必要な範囲のみcrop。
- 初回の短い入力説明、購入条件、すわなびのiPhone Widget説明は短文で足りるため専用画像を増やしていない。fr/ko/zh-Hantの銘柄設定も短い経路説明とし、異なる言語の画面は流用していない。全ガイドには4〜6枚の操作画像と、すわなびの場合は既存Watch画像がある。
- 未取得の有料状態を模造せず、課金条件は現行コードの確認できる範囲のみ記載。細かい価格・OS条件を追加推測しない。
- ページURL・front matter aliases・既存h2/h3は変更せず、Privacy本文も未変更。FAQから該当ガイドへ直接リンクし、旧総合ハブを経由しない。

## 最終読み直し (2026-09-07)

- 6ガイド・6FAQの本文を実装・正式ローカライズ・最終画像と再照合。iPhone操作、履歴の取消し名称、購入条件、Widgetの動作を確認。
- 週次広告の起点は両アプリとも `weeklyInterstitialNoticeShownAt` / `lastWeeklyInterstitialAt` で管理。初回利用日と断定せず、広告案内から1週間以降に統一。すわなびは5言語すべて修正。
- ギャンカレの本文末尾に残っていた一般FAQリンクを削除。同ページ直下の共通Supportが同じURLを提供するため。目的が明確なFAQ→操作ガイドのリンクは保持。
- 全28素材の元画像SHA-256・配信元SHA-256・crop後寸法・6ガイドの28画像参照を機械照合してPASS。PNG原画像合計2,016,568 bytesで、配信時は共通Hugo処理によりWebP生成。
- Watchガイドは5言語とも既存の審査中表示を維持。FAQのWatch同期質問にも審査中と記載。新規撮影版1.2.0(3)は撮影の根拠であり、公開済みという宣言ではない。
- 専用Simulator `5455BA32-3B45-4C7B-85CA-8E1CAAB351D3` はShutdown状態を確認。
