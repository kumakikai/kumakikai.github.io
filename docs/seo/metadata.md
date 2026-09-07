# SEOメタデータの整理

対象：Home、About、8 Productの6言語。Hero・キャッチコピー・Product本文・H1用title・既存URLは変更していません。Home下部のAbout紹介のみ、氏名がなかった5言語を日本語の既存文に合わせています。

## 根拠と採用方針

- ブランド／人物：`data/company/<lang>.json` の紹介文、Founder名、役割・開発領域と、`data/home/<lang>.json` のAbout本文に基づく。KUMAKIKAIを法人とは表現していない。
- 各Product：`data/home/<lang>.json` の正式表示名と、`data/product_details/<id>.json` の概要・機能・注意事項を要約。料金、評価、ダウンロード数、未確認の機能を追加していない。
- Uni:Note：Apple Pencil、PDF、教科・フォルダ整理、AI問題集／復習。
- オトミル：日本語音声を大きな字幕で表示する用途。現行説明にないAI機能は追加していない。
- ギガポケ：povo 2.0特典コードの登録・期限・コピー・ウィジェット。「非公式」を全言語descriptionに明記。
- Nocca：`data/apps.json` の `status: development` を正とし、全言語descriptionで開発中と明記。利用可能・配信済みとは表現していない。
- Uni:Note Pocket：バックアップを取り込む閲覧専用。自動同期や編集ができるとは表現していない。
- ギャンカレ：自分で入力した収支のタグ管理、日・月・年合計。銀行等の自動連携は追加していない。
- すわなび：公開済みのiPhoneカウンター機能を要約。`data/product_details/smokeless.json` の `watch.status: review` を確認し、検索descriptionでApple Watchを利用可能と誤認させる記述は追加していない。
- SIGNAL：現在の配信源・フィードから元の記事を開く機能。一般的なメッセージアプリ等とは区別する説明。
- 各言語の既存Product名をprimaryとして保持。検索用の別名やキーワード羅列は新設していない。

## 管理方法

`data/seo/<lang>.json` の `home`、`about`、`products.<id>` に `title` と `description` を一元管理。Product titleは既存正式表示名＋` | KUMAKIKAI`。

`scripts/sync-products.py` がAboutとProductの `description` / `seo_title` を生成する。既存の `title` はH1用として保持。HomeはheadからSEO JSONを読む。

CIで使用する `--check` は、SEOデータの全8 ID一致・空のtitle/descriptionを検証する。不足したまま汎用descriptionに黙ってfallbackしない。

全生成72エントリの同期検査PASS。変更した生成エントリはProduct 48件＋About 6件。Products/News/Supportの18件は変更なし。

以下のBeforeは今回の変更前 `public` HTMLから直接抽出した値。Afterは採用済みSEOデータの値であり、配信HTMLの最終確認は統合build／本番検証で別途行う。

## `/`

**title**

- Before: KUMAKIKAI — iPhone & iPad Apps
- After: KUMAKIKAI | iPhone・iPadアプリ

**description**

- Before: iPhone・iPad向けのアプリを企画・開発・運営しています。
- After: KUMAKIKAIは、Yuya Nakamuraが運営するアプリ開発ブランドです。Uni:Note、オトミルなど、iPhone・iPad向けアプリを企画・開発・運営しています。

## `/company/`

**title**

- Before: About | KUMAKIKAI
- After: About | KUMAKIKAI - Yuya Nakamura

**description**

- Before: KUMAKIKAIについて。開発者Yuya Nakamuraのプロフィール、アプリの分野、取材・お問い合わせ先を掲載しています。
- After: KUMAKIKAIを運営するSoftware Engineer / App Developer、Yuya Nakamuraのプロフィール。組み込み・業務システムの開発経験と、現在企画・開発・運営しているiPhone・iPadアプリを紹介します。

## `/products/uni-note/`

**title**

- Before: Uni:Note | KUMAKIKAI
- After: Uni:Note | KUMAKIKAI

**description**

- Before: Apple Pencilで書く。PDFに書き込む。ノートを教科やフォルダで整理し、AIで問題集づくりや、囲った問題の質問・解答まで。授業の記録から復習へ、ひと続きに。
- After: Uni:Noteは、Apple Pencilでの授業ノート、PDFへの書き込み、AIによる問題集生成や復習に対応したiPadアプリです。ノートを教科・フォルダで整理できます。KUMAKIKAIが開発・運営しています。

## `/products/oto-miru/`

**title**

- Before: オトミル | KUMAKIKAI
- After: オトミル | KUMAKIKAI

**description**

- Before: テレビの声も、身近な人との会話も。音声をiPhoneやiPadの大きな文字で表示し、聞き取りづらい場面をサポートします。
- After: オトミルは、テレビの声や目の前の会話をiPhone・iPadの大きな字幕で表示する、KUMAKIKAIの聴覚支援アプリです。聞き取りづらい日本語の音声を、その場で文字として確認できます。

## `/products/giga-poke/`

**title**

- Before: ギガポケ | KUMAKIKAI
- After: ギガポケ | KUMAKIKAI

**description**

- Before: povo 2.0の特典コードを、期限が近い順にまとめて管理。使いたいコードをすぐにコピー。ウィジェットでも、次に使うギガを確認できます。
- After: ギガポケは、povo 2.0の特典コードと有効期限を管理するKUMAKIKAIの非公式iPhoneアプリです。メールからの登録、期限順の確認、コードのコピー、ウィジェットに対応しています。

## `/products/nocca/`

**title**

- Before: Nocca | KUMAKIKAI
- After: Nocca | KUMAKIKAI

**description**

- Before: 家族との会話や接触に負担を感じる方が、必要なことだけ意思表示できるアプリ。家族はその意思を受け取り、必要なときに返事をします。
- After: Noccaは、KUMAKIKAIが開発中のiPhone向けアプリです。家族との会話や接触に負担を感じる方が短い言葉とアイコンで意思を伝え、家族が必要なときに返事をする仕組みを紹介します。

## `/products/uni-note-pocket/`

**title**

- Before: Uni:Note Pocket | KUMAKIKAI
- After: Uni:Note Pocket | KUMAKIKAI

**description**

- Before: Uni:Noteで書いたノートを、iPhoneで復習。バックアップを読み込む閲覧専用アプリ。
- After: Uni:Note Pocketは、Uni:Noteのバックアップを読み込み、手書きノートや問題集をiPhoneで復習する閲覧専用アプリです。ノート名の検索や付箋マーカーにも対応。KUMAKIKAIが開発・運営しています。

## `/products/balance-calendar/`

**title**

- Before: ギャンカレ | KUMAKIKAI
- After: ギャンカレ | KUMAKIKAI

**description**

- Before: 収入と支出をその場で記録。カレンダーで日々のお金の流れを振り返る。
- After: ギャンカレは、収入・支出やギャンブルの収支を記録するKUMAKIKAIのiPhoneアプリです。プラス・マイナスの金額をタグで分け、日別・月別・年合計で振り返れます。

## `/products/smokeless/`

**title**

- Before: すわなび | KUMAKIKAI
- After: すわなび | KUMAKIKAI

**description**

- Before: 「吸った」と「我慢した」をワンタップで記録。本数と金額の変化を確認。
- After: すわなびは、喫煙した回数と我慢した回数をワンタップで記録するKUMAKIKAIのiPhoneアプリです。日別・月別・年別の履歴やグラフで、本数と金額の目安を確認できます。

## `/products/signal/`

**title**

- Before: SIGNAL | KUMAKIKAI
- After: SIGNAL | KUMAKIKAI

**description**

- Before: note、Qiita、Zennなどの個人発信を、自分のペースで読むニュースフィード。
- After: SIGNALは、note・Qiita・Zennなどの個人発信や記事をまとめて読むKUMAKIKAIのiPhoneニュースアプリです。配信源を選び、フィードの見出しから元の記事へ進めます。

## Home本文の人物・Product関係

日本語Homeの既存About文は維持。他5言語にはYuya Nakamuraが本文中に存在しなかったため、同じ事実を忠実に翻訳して `data/home/<lang>.json` の `aboutText` だけを更新。氏名をmeta/JSON-LDにのみ置く状態を避けるための変更で、HeroやランダムFeaturedは変更していません。

- en: Yuya Nakamura designs, develops and maintains apps including Uni:Note and OtoMiru.
- ko: Yuya Nakamura가 Uni:Note, OtoMiru 등의 앱을 기획·개발·운영합니다.
- de: Yuya Nakamura konzipiert, entwickelt und betreut Apps wie Uni:Note und OtoMiru.
- fr: Yuya Nakamura conçoit, développe et maintient des apps comme Uni:Note et OtoMiru.
- zh-hant: Yuya Nakamura 企劃、開發及維護 Uni:Note、OtoMiru 等 App。
