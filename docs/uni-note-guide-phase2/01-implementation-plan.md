# Uni:Note Phase 2 実装前計画

対象は一般公開3.5.0の日本語版。P0適用済み本文をbefore-hotfixed-htu.mdへ凍結。Web制作前に196操作の一意な主掲載先を検証した。副掲載は12の活用例で再利用する。

構成: トップ1 + カテゴリ16 + 個別記事56。196/196操作を割当済み。A01/S41は未確認の詳細を保留し、確認済み範囲を説明する。

## 作成ページ・操作・画像

| ページ / URL | 主操作ID | 補助操作ID | 原本ID（画像待ちは非表示） |
|---|---|---|---|
| 画面とノートの仕組み /htu/uni-note/start/screens/ | N01, S39 |  | N-M01, N-M05, M-M14 |
| 最初の教科とノートを作る /htu/uni-note/start/first-note/ | N02, N03, N05, N69 |  | N-M01, N-M02, M-M14 |
| 教科を編集・並べ替え・削除する /htu/uni-note/library/subjects/ | N04, N10, N56 |  | N-M01, N-M04, N-M08, N-M20, S-M15 |
| 教科をフォルダで整理する /htu/uni-note/library/folders/ | N14, N15, N16, N17, N18, N19, N20, N68 |  | N-M01, N-M11, N-M12, N-M13, N-M14, N-M15, N-M17, N-M18 |
| ノートをタイトルで探す /htu/uni-note/library/search/ | N12, N13 |  | N-M01, N-M09 |
| ノートを開く・増やす・整理する /htu/uni-note/notebooks/manage/ | N06, N07, N08, N09, N11, N57 |  | N-M01, N-M05, N-M06, N-M07, N-M58, S-M15 |
| ページを送る・並べ替える・削除する /htu/uni-note/notebooks/pages/ | N21, N22, N25, N26, N27, N63 |  | N-M31, N-M33, N-M34, N-M35, N-M36 |
| 縦ノートを作る /htu/uni-note/notebooks/vertical/ | N23, N65 |  | N-M19, N-M31, M-M14, M-M18 |
| ペンと蛍光ペンを使う /htu/uni-note/writing/pens/ | N28, N29, N30, N31, N32, N33 |  | N-M37, N-M39, N-M40, M-M14 |
| 消しゴム・取り消し・やり直し /htu/uni-note/writing/erasing/ | N34, N35, N36, N37, N38 |  | N-M41, N-M42, N-M43, N-M44 |
| パレットを動かす・収納する /htu/uni-note/writing/palette/ | N39, N40 |  | N-M45, N-M47, M-M14 |
| 定規で直線を引く /htu/uni-note/writing/ruler/ | N41, N42, N43, M50, M51 |  | N-M49, M-M14 |
| 手書きを囲んで移動する /htu/uni-note/writing/move/ | N44, N45 |  | N-M50, N-M51, M-M14 |
| 写真・紙の資料を貼り付ける /htu/uni-note/materials/photos/ | M01, M02, M03 |  | M-M02, M-M03, M-M19, R-M05 |
| PDFのページを選んで貼り付ける /htu/uni-note/materials/pdf/ | M04, M05, M06 |  | M-M06, M-M07, M-M08, M-M09, M-M10, M-M09R |
| 写真・PDFを動かして固定する /htu/uni-note/materials/arrange/ | M07, M08, M09, M10, M11, M12, M13 |  | M-M10, M-M11, M-M12, M-M13, M-M14, M-M15 |
| 縦ノートで資料の大きさを整える /htu/uni-note/materials/vertical/ | M14, M15 |  | N-M19, M-M14, M-M18, M-M19, M-M20 |
| ノートをPDFにして保存・共有する /htu/uni-note/materials/export/ | M17, M18, S17, S42 |  | M-M21 |
| 授業を録音して保存する /htu/uni-note/recording/capture/ | M20, M21, M22, M23, M24 |  | M-M23, M-M24, M-M25, M-M26, M-M27 |
| 録音を再生・整理・共有する /htu/uni-note/recording/play/ | M25, M26, M27, M28, M29, M30 |  | M-M26, M-M28 |
| 録音を文字起こしする /htu/uni-note/recording/transcribe/ | M32, M33, M34, M35, M36 |  | M-M23, M-M24, M-M28, M-M29, M-M30 |
| 文字起こしからAI要約を作る /htu/uni-note/recording/summary/ | M37, M38, M39, M40, S43 |  | M-M31, M-M32, M-M33, R-M01 |
| AI要約を現在のノートへ貼る /htu/uni-note/recording/paste/ | M41 |  | M-M32, M-M35 |
| 付箋マーカーで答えを隠す /htu/uni-note/study/sticky/ | M42, M43, M44, M45, M46, M62 |  | N-M56, M-M37, M-M38, M-M39, M-M40 |
| ポモドーロで集中と休憩を区切る /htu/uni-note/study/pomodoro/ | M52, M53, M54, M55, M56 |  | M-M42, M-M43, M-M44, M-M46 |
| レーザーポインターを使う /htu/uni-note/study/laser/ | M57, M58 |  | M-M10, M-M48 |
| 問題を囲って解答を確認する /htu/uni-note/ai/answer/ | A02, A03, A04, A05, A06, A07, A08 |  | R-M02, R-M03, R-M04 |
| 文字起こし言語とAIの設定を確認する /htu/uni-note/ai/settings/ | A01 |  | R-M01 |
| ノートからAI問題集を作る /htu/uni-note/problem-sets/generate/ | Q01, Q02, Q03, Q04, Q05, Q06, Q07 |  | R-M05, R-M06, R-M07, R-M09, R-M10 |
| 保存した問題集で復習する /htu/uni-note/problem-sets/review/ | Q08, Q09, Q10 |  | R-M11, R-M13, R-M14 |
| 問題集を手動作成・編集する /htu/uni-note/problem-sets/edit/ | Q11, Q12, Q13, Q14, Q15, Q16 |  | R-M11, R-M14, R-M15, R-M16, R-M17, R-M18 |
| ホームの問題集表示を変える /htu/uni-note/problem-sets/home/ | Q18 |  | R-M01, R-M11, R-M20 |
| 設定を開いて目的の項目を探す /htu/uni-note/customize/settings/ | S01 |  | N-M01, S-M01 |
| 紙・左右の配置・ページ情報を設定する /htu/uni-note/customize/paper/ | S02, S03, S04, S05, S06, S07, S08, S09 |  | N-M45, M-M14 |
| 起動・表示・言語を設定する /htu/uni-note/customize/display/ | S10, S11, S12, S13, S14, S15, S16 |  | N-M47, M-M14 |
| ボタンとパレットの配置を変える /htu/uni-note/customize/toolbar/ | N46, N47, N48, N49, N50, N51, N66 |  | N-M52, N-M53, N-M54, N-M55, N-M56, M-M14 |
| ノートを書き込みから保護する /htu/uni-note/data/protect/ | S25, S26 |  | N-M06, S-M14 |
| ゴミ箱から教科・ノートを復元する /htu/uni-note/data/trash/ | S27, S28, S29, S30, S31 |  | S-M15, S-M16 |
| バックアップを保存する /htu/uni-note/backup/save/ | S18, S19, S20, S21 |  | S-M08, S-M10 |
| バックアップから復元する /htu/uni-note/backup/restore/ | S22, S23, S24 |  | S-M08, S-M11, S-M12 |
| PremiumとAI残量を確認する /htu/uni-note/plans/usage/ | P01, P02, P04, P05, P06, P07, P08 |  | S-M01, R-M21, R-M23 |
| 困ったときの確認と問い合わせ /htu/uni-note/troubleshooting/help/ | S32, S33, S34, S35, S36, S37, S38, S40, S41 |  | S-M01 |
| iPadのウインドウ操作を使う /htu/uni-note/ipados/windows/ | O01, O03 |  | R-M24, R-M25 |
| ファイルアプリと共有シートを使う /htu/uni-note/ipados/files/ | O06, O07 |  | M-M10 |
| 縦ノートで資料を大きく表示して書き込む /htu/uni-note/workflows/vertical-annotate/ | N60 | N23, M14, M07, M08, M09, M10, M11 | M-M18, N-M19, N-M31, N-M50, N-M51, M-M10, M-M11, M-M12, M-M13, M-M14 |
| 見開きPDFを左右に分割して学習する /htu/uni-note/workflows/split-spread/ |  | M04, M05, M06, N26 | M-M09, M-M09R, N-M33, N-M34, M-M06, M-M07, M-M08, M-M10 |
| 資料の横に手書きスペースを残す /htu/uni-note/workflows/material-margin/ | M16 | M07, M08, M09, M10, M11, S08 | M-M14, M-M10, M-M11, M-M12, M-M13 |
| PDF・写真に付箋を付けて暗記する /htu/uni-note/workflows/sticky-material/ | M47 | M11, M42, M43, M44, M45, M46 | M-M38, N-M56, M-M14, M-M37, M-M39, M-M40 |
| 録音・文字起こし・AI要約で授業を復習する /htu/uni-note/workflows/record-review/ |  | M20, M21, M22, M32, M33, M34, M35, M36, M37, M38, M39 | M-M30, M-M32, M-M23, M-M24, M-M25, M-M26, M-M28, M-M29, M-M31, M-M33 |
| AI要約をノートへ貼って追記する /htu/uni-note/workflows/summary-annotate/ |  | M41, N28 | M-M35, N-M37, M-M14, M-M32 |
| AI問題集を手修正して復習する /htu/uni-note/workflows/quiz-review/ | Q17 | Q01, Q02, Q03, Q05, Q07, Q08, Q09, Q12 | R-M14, R-M05, R-M06, R-M07, R-M09, R-M10, R-M11, R-M13, R-M16, R-M17 |
| ポモドーロを使いながら勉強する /htu/uni-note/workflows/focus/ |  | M52, M53, M54, M55, M56 | M-M43, M-M42, M-M44, M-M46 |
| レーザーポインターで資料を説明する /htu/uni-note/workflows/explain/ |  | M57, M58, M11 | M-M48, M-M10, M-M14 |
| 資料用と筆記用の2つのノートを並べる /htu/uni-note/workflows/two-notes/ | O02 | O01, O03 | R-M25, R-M24, R-M26 |
| SafariやPDF閲覧アプリと並べて書く /htu/uni-note/workflows/external-material/ | O04 | O01 | R-M27, R-M24, R-M25 |
| 動画を小さく表示しながら書く /htu/uni-note/workflows/pip/ | O05 | N28 | R-M28, N-M37, M-M14 |

## カテゴリ

- はじめに: /htu/uni-note/start/
- 教科・フォルダ: /htu/uni-note/library/
- ノート・ページ: /htu/uni-note/notebooks/
- 手書き: /htu/uni-note/writing/
- 写真・PDF: /htu/uni-note/materials/
- 録音・文字起こし: /htu/uni-note/recording/
- 暗記・集中: /htu/uni-note/study/
- AI: /htu/uni-note/ai/
- 問題集: /htu/uni-note/problem-sets/
- カスタマイズ: /htu/uni-note/customize/
- 保護・データ管理: /htu/uni-note/data/
- バックアップ: /htu/uni-note/backup/
- プラン・AI残量: /htu/uni-note/plans/
- 便利な使い方: /htu/uni-note/workflows/
- iPadOSとの組み合わせ: /htu/uni-note/ipados/
- 困ったとき: /htu/uni-note/troubleshooting/

## 旧アンカーの案内先

| 既存トップ内ID | 新しい説明 |
|---|---|
| 1-ホームで教科とフォルダを整理する | /htu/uni-note/start/first-note/ |
| 2-最初のノートを開く | /htu/uni-note/start/first-note/ |
| create | /htu/uni-note/start/first-note/ |
| 3-apple-pencilで書く | /htu/uni-note/writing/pens/ |
| 4-2本指でズームする | /htu/uni-note/writing/pens/ |
| 5-ツールを切り替える | /htu/uni-note/writing/pens/ |
| 9-定規-を使う | /htu/uni-note/writing/ruler/ |
| write | /htu/uni-note/writing/pens/ |
| 6-ノート一覧-と-ページ一覧-を使う | /htu/uni-note/notebooks/manage/ |
| find | /htu/uni-note/notebooks/manage/ |
| 7-その他-メニューを使う | /htu/uni-note/materials/pdf/ |
| 8-写真とpdfを使う | /htu/uni-note/materials/pdf/ |
| pdf | /htu/uni-note/materials/pdf/ |
| 10-録音文字起こしai要約を使う | /htu/uni-note/recording/capture/ |
| recording | /htu/uni-note/recording/capture/ |
| 11-暗記を使う | /htu/uni-note/study/sticky/ |
| 12-囲って解答アシスタント-を使う | /htu/uni-note/ai/answer/ |
| 13-問題集を作る | /htu/uni-note/problem-sets/generate/ |
| review | /htu/uni-note/study/sticky/ |
| 14-保護ゴミ箱 | /htu/uni-note/data/protect/ |
| protect | /htu/uni-note/data/protect/ |
| 15-設定バックアップ | /htu/uni-note/backup/save/ |
| backup | /htu/uni-note/backup/save/ |
| split-view--slide-over--2ペインで使う | /htu/uni-note/ipados/windows/ |
| windows | /htu/uni-note/ipados/windows/ |

旧アンカーはトップに実体を残し、新記事への説明付きリンクと対応させる。redirectだけのトップにしない。

## 暫定画像

- N-M02: ja/create-menu.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。
- N-M09: ja/home-search.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。
- N-M37: common/writing-tools.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。
- M-M23: common/record-button.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。
- M-M38: common/sticky-marker.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。
- R-M04: ja/problem-answer.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。
- S-M08: common/backup-file-actions.png → 将来同IDの原本へ置換。既存cropが説明できる部分だけに使う。

既存attachment-menu.pngは項目不足、pdf-writing.pngは古いナビゲーションを含むため再掲しない。元ファイルは削除しない。

## 保留と版の境界

- HF-H-01: 作成後の向き変更は可否とも記載しない。作成時だけ説明。
- HF-H-02: 付箋移動・拡縮は掲載しない。写真・PDFの操作と分離。
- HF-H-03: 付箋＋定規補正を掲載しない。
- HF-H-04: 任意1ページPDF出力を掲載しない。
- HF-H-05: 同一ノートの同時編集を推奨しない。別ノートの例だけ。
- HF-H-06: 録音ロックを掲載しない。
- HF-H-07: Premium Plus固有の購入・付与を掲載しない。
- HF-H-08: 指描画F01〜F09と未確認UIを公開しない。CoreHandwriting内部説明も不要。
- HF-H-09: OS固有操作はApple公式へのリンクと条件付き説明。画像は採用OS実機確認後。
- A01: AI回答言語の独立設定は5b6c641と800c0c3で差分あり。掲載先を確保し、公開確認までは文字起こし言語との区別だけ。
- S41: クラッシュ後の具体的な復帰ダイアログは公開build照合待ち。通常の再起動・サポート案内だけ。
- Q18: ホーム表示切替は公開済み。設定内の所在がコミット間で異なるためカテゴリ名は断定しない。

## 画像待ちの再評価

134候補すべてをplan.jsonで再評価。機能の説明と画面そのものの確認を分離する。標準110のうち、指描画によらない筆記・素材・録音等は3.5.0で制作。次期配置画面・レーザーON・通知復帰等は特定の見た目を断定しない。

## 検証方針

Node22.22.0と既存Hugoを一時ランタイムから使用。production build、既存migration/SEO、全記事リンク・旧アンカー・画像ID/原本/操作の対応・P0/P1/HOLD・画像不変を検証する。既存の不変baselineは更新せず、日本語Uni:Noteの明示的な再構成だけを限定レビューとして記録する。
