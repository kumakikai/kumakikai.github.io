# Cross-status — 公開状態・時間依存表記・リンクの意味

監査日: 2026-09-08（JST）。サイト `main` / `3ab462d3d03247df33420f0657cda305470d8e0b` に対する統合中の作業ツリーを確認した。最初に `git status --short` を確認し、並行変更を保護した。初めは読取専用として監査し、結果を親担当へ報告後、明示された追加指示により Smokeless の `platformPending` 6言語だけを変更した。他のアプリ・本文・生成ページを編集していない。

公開バイナリ、App Store Connect の現在の提出状態、実購入・公開URLはこの作業では再確認していない。サイトに記録された公開情報、ローカル実装についての今回のPhase 1監査、記事の履歴を区別する。以下のサイト内パスは `/Users/yuya/Projects/homepage/` が基準。行番号はこの監査時点の作業ツリーを指す。

## 1. 対象と結果

74文書（Privacy 22、Terms 8、FAQ 22、Guide 22）を対象に、公開状態・版番号・時点表現を抽出し、文脈を確認した。併せて全8製品の `data/apps.json`、`data/product_details/*.json`、Home/SEO各6言語、生成Product 48ページ、共通問い合わせ・Support・Watch表示の出力条件を確認した。日付付き記事15本も、現在仕様と取り違えやすい記述の分類に限って参照した。

| 製品 | Privacy | Terms | FAQ | Guide | 合計 | Product |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Uni:Note | 6 | 1 | 6 | 6 | 19 | 6 |
| Uni:Note Pocket | 6 | 1 | 6 | 6 | 19 | 6 |
| すわなび / Smokeless | 5 | 1 | 5 | 5 | 16 | 6 |
| オトミル | 1 | 1 | 1 | 1 | 4 | 6 |
| ギガポケ | 1 | 1 | 1 | 1 | 4 | 6 |
| Nocca | 1 | 1 | 1 | 1 | 4 | 6 |
| ギャンカレ | 1 | 1 | 1 | 1 | 4 | 6 |
| SIGNAL | 1 | 1 | 1 | 1 | 4 | 6 |
| **計** | **22** | **8** | **22** | **22** | **74** | **48** |

新設Terms 5本も対象に含む。`content/terms/{uni-note,uni-note-pocket}.md:5`、`{smokeless,balance-calendar,signal}.md:4` は制定日 `2026-09-08`。この日付は文書制定の履歴であり、アプリや追加機能の公開日を意味しない。全8製品の `support.termsURL` は実在する各日本語Termsを指す（`data/apps.json:56,105,152,197,255,304,357,404`）。

**この横断確認で、ローカル実装を新たに一般公開済みと断定した記述は検出しなかった。** ただし、既存の「審査中」「公開中3.4.0」等を今日の公開実績として再証明したものではない。残る提出・公開状態の証拠不足は第4節に記録する。

## 2. 仕様境界として意図的に保持

| 対象・根拠 | 保持する記述と判断 | 更新の契機 |
| --- | --- | --- |
| Uni:Note Guide ja `content/htu/uni-note.md:9,52,102`、en/de/fr/ko/zh-hant 各 `:10,51,95`。FAQ ja `content/faq/uni-note.md:69,102`、他5言語各 `:70,103` | 公開版3.4.0と公開前3.5.0を区別。ノート一覧ショートカット・ツール配置/パレット変更・問題集手動作成/編集/ホーム表示設定を、公開中の操作と混在させないための注記。英語は `local upcoming version` とも明示。 | 3.5.0の一般公開と対象操作を確認したときに、12文書を同時更新。ローカルの版番号変更やビルド成功だけで削除しない。 |
| Nocca `content/privacy/nocca.md:12`、`content/terms/nocca.md:12`、`content/faq/nocca.md:19,23`、`content/htu/nocca.md:11` | 「公開準備中」「公開前の現在のiPhone実装」。日本向けiPhone / iOS 17 / 日本語という公開予定範囲と、デモ画面が実際の接続先でないことを区別。 | 正式公開と対象地域・OS・画面を確認したとき。Android等のローカルコードがあるだけでは公開範囲を拡大しない。 |
| Nocca Product `data/apps.json:159,181`、`data/product_details/nocca.json:7,32,56`、他5言語の同じ説明・制約。`data/seo/ja.json:25`、Homeの開発中画面alt `data/home/ja.json:82` | Productは `development`、配信確認は空、`coverage: unreleased`。6言語の紹介と開発中画面説明も一致。法務の存在やサーバー実装があることを一般配信の証拠としていない。 | 正式公開確認後、metadata・紹介・4文書を一緒に更新。 |
| オトミル `content/htu/oto-miru.md:12`、`content/faq/oto-miru.md:12`、`data/apps.json:62,99` | アプリ自体は `published`、画面素材は `screenshotsStatus: review`。Guide/FAQは「提出用素材と開発版」「配信中のバージョンとは画面や設定が異なる場合」を明示。未公開の画面を公開版と断定していない。 | 当該画面を含む版の一般公開を確認し、旧画面との差を解消したとき。 |
| すわなび Privacy ja/en/fr/ko/zh-hant 各 `content/privacy/smokeless*.md:29`、Terms `content/terms/smokeless.md:25`、FAQ ja `:99` / 他4言語 `:100` | Watch版の情報は「公開後、利用する場合」の処理・条件として明示。iPhoneアプリ公開とWatch対応版公開を区別。買い切り2商品の購入特典であり、Watchだけの別商品を新設したように書いていない。 | Watch対応版の一般公開確認後。現行の審査状態自体の要確認は第4節。 |
| すわなび Guideの `watch-guide`（ja/en `:73`、fr/zh-hant `:70`、ko `:71`）、`data/product_details/smokeless.json:4,22,47,72,97,122,147` | 共通Watch欄は `status: review` に応じた公開前注記を全実在Guide/全6言語Productへ出力。`layouts/_partials/watch-guide.html:9`、`watch-product.html:15` に条件あり。 | Watchの公開確認後に共通状態と本文を整合させる。 |
| すわなび Product `layouts/product/single.html:6` | `heroPublished` の文字列はデータ内にあるが、`status == published` の場合にだけ表示。現状は `heroReview` 側。文字列の存在だけで公開済み表示と判定しない。 | 状態切替時の表示確認。 |
| すわなび FAQ ja `content/faq/smokeless.md:44`、en/fr/ko/zh-hant 各 `:45`、zh-hant `:77` | 「現時点では当日分」「目前沒有雲端同步…」は、記録対象日・バックアップ非対応という現在実装の境界。当日件数・Watch連携とクラウドバックアップを混同していない。 | 過去日登録・クラウド/ファイルバックアップの実装と提供確認時。 |
| ギャンカレ `content/faq/balance-calendar.md:58,60` | 「バックアップや自動同期、データのエクスポート」の質問に「現時点ではありません」。ローカルにCloudKitの宣言があることを、利用者用同期がある根拠としていない。 | 実際に使える操作と提供を確認したとき。 |
| SIGNAL `content/terms/signal.md:15`、`data/product_details/signal.json:57,113,169,225,281,337` | 「現時点でアプリ内購入はありません」「現在のアプリ表示言語は日本語」。サイト6言語とアプリUI言語を区別。外部コンテンツ取得に通信が必要なことも明示。 | 課金・アプリUI言語の実装と提供が変わるとき。 |
| Uni:Note翻訳Privacy `content/privacy/uni-note.{en,de,fr,ko,zh-hant}.md:69` | `At this time` / `Derzeit` / `À ce jour` / `현재` / `目前` は広告SDK不使用の説明。日本語と意味は一致し、将来の広告導入予定を表さない。 | 実際のSDK・情報取扱い変更時。機械的な時点語削除は不要。 |
| ギガポケ `content/terms/giga-poke.md:81` | 「将来料金体系を変更する場合」は条件付きの事前案内条項。現時点の全機能無料・広告なし（`:28`）と矛盾せず、課金開発の予告ではない。 | 実際に提供条件が変わるとき。 |
| オトミル `content/htu/oto-miru.md:75`、各課金Termsの購入条件 | 「購入画面で現在の価格と適用条件」は、変わり得る価格を購入時に確認する導線。固定金額・全員への無料トライアル保証を追加していない。 | 購入フローや商品種別が変わるとき。 |

時点語に見えるが公開状態ではないものも残す。例: ギガポケFAQ `:51` の「現在日から推測しない」、Guide `:91` の「最新の状態を確認」、Nocca Privacy `:59` の「現在の購入状態」、FAQ `:120` の実UI引用、Pocketの「最新バックアップ」/「最近使ったノート」、すわなびの現在の喫煙量、GigaPoke他言語の「近日に期限切れになる特典」。いずれも利用者データ・実UI・操作の意味であり、公開予定の古さではない。

## 3. 履歴として保持

| 対象 | 記録された時点・説明 | 判定 |
| --- | --- | --- |
| `data/apps.json:38,90,139,186,237,290,341,391` | availabilityの確認日 `2026-09-07`。全製品 `partial`、Noccaのみ `unreleased`。 | 当日の配信確認範囲の記録。今日の全世界配信確認と読み替えない。更新する場合は再取得の証拠が必要。 |
| 新設Terms 5本の `legal_established: 2026-09-08`、GigaPoke既存Terms `:7` の `2026-09-02`、全法務のlastmod | 文書の制定・改定日。 | アプリ公開日や課金提供開始日ではない。既存不明制定日を推測していない。 |
| `content/notes/2026-01-26-roadmap.md:19,26,47,83,104,119,123,151` | ギャンカレのAndroid・アドオン・サブスク/バックアップ等の2026年1月の計画。 | 履歴。現Terms/FAQへ計画を移植しない。`data/news.json:7` とdescriptionが当時情報と明示。 |
| `content/notes/2026-04-12-uni-note-10000.md:32`〜`:34` | AIのサブスク・お試し・「次の次」の更新予定。 | 履歴。現TermsのPremium買い切り・消費型AI残量と別。`data/news.json:46` の履歴表示対象。 |
| `content/notes/2026-03-12-uni-note.md:52`、`2026-04-01-uni-note-pocket.md`、`2026-05-19-oto-miru.md:72` | 当時の導入説明・今後の機能・保存方針。 | 履歴。`data/news.json:24,41,51` の履歴注記と現在Productへの導線を維持。 |
| `content/notes/2026-02-14-blog.md:4`、`2026-03-25-blog.md:4` | 「当時の改善方針」「2026年3月当時…改善予定」。 | 記事の日付・descriptionで当時の記録と分かる。現FAQに未実装予定を掲載する根拠にはしない。 |
| `content/notes/2026-05-26-android-release.md:13` | Android公開前のクローズドテストに関する当時の運営記事。 | 履歴。現在の各製品の配信可否を保証する文書ではない。今回本文更新の対象外。 |
| `content/notes/2026-09-06-nocca.md:10` | 開発中・プロトタイプを前提とした公開前紹介。 | 日付付き履歴であると同時に、現Productの開発状態とも整合。正式公開時に過去記事を現在形へ上書きしない。 |
| `guide-anchor` 内の「現在」「recent」「aktuelle」等 | 旧FAQ/Guide見出し由来の互換ID。例: Uni:Note FAQ fr/de/ko/zh-hant `:64`、en/de `:99`。 | 表示される現在状態の説明ではない。意味に対応する節の既存アンカーとして保持。 |

履歴注記の共通出力は `layouts/single.html:9` と `data/corporate/*:38`。日付付き記事の本文を今回の文書統一で修正していない。

## 4. 要更新候補・要確認

| ID | 優先度 | 対象・証拠 | 判断・今回の対応 |
| --- | --- | --- | --- |
| CS-1 | 低・対応済み | `data/product_details/smokeless.json:18,43,68,93,118,143` の `platformPending`。変更前は「近日対応」「coming soon」「지원 예정」「demnächst」「bientôt」「即將支援」。 | 近い公開時期を示す根拠がないため、親からの追加指示により、6言語とも公開前という境界だけを示す表現へ変更。ja「公開前」、en「not yet released」、ko「아직 출시되지 않음」、de「noch nicht veröffentlicht」、fr「pas encore disponible」、zh-hant「尚未推出」。状態値、版番号、審査中の文、Watch操作は変更しない。 |
| CS-2 | 要確認 | 同ファイル `:4` の `status: review`、各言語の `statusReview` / `reviewNotice` と、`/Users/yuya/Projects/smokeless/docs/RELEASE_NOTES_1_2_0.md:3` の「App Store Connectへの入稿・公開は未実施」。 | サイトの従来状態とローカル入稿案の記録だけでは、現在の審査状態を確定できない。古い方がどちらかを推測せず、App Store Connect等の正式な提出状態の確認が必要。今回審査値を変更しない。少なくともWatch一般公開済みにはしていない。 |
| CS-3 | 次回公開時 | Uni:Note3.4.0/3.5.0、Nocca公開準備中、オトミルの画面素材境界。対象は第2節。 | 現時点で削除すべき重複ではなく、一般公開後に全対応文書とProductで同時に更新する管理対象。ローカルHEADやStore用素材の完成を公開実績として扱わない。 |
| CS-4 | 別途確認 | `data/apps.json` の配信確認日・地域、各アプリの実販売SKU、Noccaの導入オファー/運用保持期間、SIGNALの実配布版問い合わせ設定。 | Phase 1の要確認を解消したとは扱わない。本横断監査は文書間の区別・整合を確認したもので、現Store・バックエンド運用・公開バイナリの確認ではない。 |

## 5. 同一URLの異ラベルと意味

74本文の手書きMarkdownリンクをURL/fragment単位で抽出し、72種類のソース上の参照先を確認した。これは生成HTMLの全リンク数ではない。`relref` の言語解決前の同じ記述でも、実在翻訳への出力先は別URLとなる。共通shortcode/Supportから出力されるリンクはテンプレートと定義を別に確認した。生成HTMLの到達性・重複数は親担当の全リンク走査に委ねる。

**意味が食い違う異ラベルの同一リンク先は検出しなかった。** 次の異ラベルは役割または翻訳として説明できる。

| 参照先と具体例 | 判定 |
| --- | --- |
| `/privacy/nocca/#5-削除と利用者の選択`：FAQ `content/faq/nocca.md:84`「プライバシーポリシーの削除の説明」、Guide `content/htu/nocca.md:92`「データの保存・削除の説明」 | ともに新しい削除節へ保持された旧ID（Privacy `:98`）。同節 `:105` に削除後も残る記録と保存期間への説明があり、削除時の例外という意味が対応。より詳しい保存期間は前方の保存・管理節にあるが、リンクの意味を反転させていない。 |
| Uni:Note FAQの `/htu/uni-note/#find,#write,#pdf,#recording,#review,#backup,#windows` | 言語別の「検索」「手書き」「PDF」「録音」「復習」「バックアップ」「2ウインドウ」というリンクがそれぞれの操作節へ対応。6言語のラベル差は翻訳であり、別内容への同名誘導ではない。 |
| Pocket FAQの `/htu/uni-note-pocket/#import,#recordings,#refresh,#read` と `/privacy/uni-note-pocket/#data-management` | 取り込み・録音再生・再取り込み・閲覧/検索・データ削除の役割に対応。日本語FAQ `:23,35,47,55,66` と他5言語の同じ行。 |
| Smokeless FAQ5言語から `/htu/smokeless/#apple-watch` | すべてWatch利用条件・未接続保存・再接続という同じ手順を指す。翻訳のないドイツ語Guideを架空生成していない。 |
| Apple Privacy、AWS data privacy、Firebase privacy/security、Gemini API terms | 各言語のラベルは同じ提供元・文書種別を表す。TermsへPrivacyというラベルを付ける等の意味違いはない。各URLの現在の応答内容はこのソース監査の対象外。 |
| 新Terms8本の独自URLとApple標準使用許諾契約 | `data/apps.json` のTermsは製品固有利用規約。`data/document_ui.json:25` のAppleリンクは「Appleの標準使用許諾契約」。二つの異なる文書を同じURLに混同していない。 |
| Productの「お問い合わせ」と本文のフォーム/メールラベル | 同じ正式窓口を役割名と操作名で表している。`layouts/_partials/support-data.html:12`、`layouts/shortcodes/document-contact.html:9`。GigaPokeとNoccaは各専用Google Form、他製品は共通メールに製品件名。法務の問い合わせ先とサポートフォームの意味は一致。 |

## 6. 軽量検証と範囲

- 74本文と48Productファイルの実在数をファイル一覧から計数した。各indexページを件数に含めていない。
- 新Terms5本と全8製品の `termsURL` の対応を確認した。
- SmokelessのJSONを読み直し、変更は `watch.locales.{ja,en,ko,de,fr,zh-hant}.platformPending` の6値だけであることをHEADとの構造差分で確認した。
- `watch.status` は `review`、`releaseVersion` は `1.2.0` のまま。Product/Guideの公開前注記の条件分岐も保持されている。
- 個別Hugo再生成・本番確認はここでは行わず、親担当の統合build・生成HTML・公開物確認へ引き継ぐ。

今回のPhase 1根拠: `learning-phase1.md`、`communication-phase1.md`、`utilities-phase1.md`。これらは同じ監査工程で記録したローカル実装の根拠であり、Store公開や実運用の証明ではない。
