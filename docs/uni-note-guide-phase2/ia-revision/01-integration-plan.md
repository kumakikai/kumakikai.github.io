# 実装前の統合対応表

基準: 6787e1c。変更前に44個別URLすべてHTTP 200を確認。当初は互換導線を予定したが、後続の明示指示によりこのチャットで増えた44ページは公開済みでも削除可。リダイレクトを作らない。仕様・HOLDの再解釈なし。

## 大項目と統合後のアンカー

| 大項目 | URL | セクション |
|---|---|---|
| はじめに | /htu/uni-note/start/ | #screens, #first-note |
| 教科・フォルダ | /htu/uni-note/library/ | #subjects, #folders, #search |
| ノート・ページ | /htu/uni-note/notebooks/ | #manage, #pages, #vertical |
| 手書き | /htu/uni-note/writing/ | #pen, #eraser, #palette, #ruler, #selection |
| 写真・PDF | /htu/uni-note/materials/ | #photos, #pdf, #arrange, #vertical, #export |
| 録音・文字起こし | /htu/uni-note/recording/ | #capture, #play, #transcribe, #summary, #paste |
| 暗記・集中 | /htu/uni-note/study/ | #sticky, #pomodoro, #laser |
| AI | /htu/uni-note/ai/ | #answer, #settings |
| 問題集 | /htu/uni-note/problem-sets/ | #generate, #review, #edit, #home |
| カスタマイズ | /htu/uni-note/customize/ | #settings, #paper, #display, #toolbar |
| 保護・データ管理 | /htu/uni-note/data/ | #protect, #trash |
| バックアップ | /htu/uni-note/backup/ | #save, #restore |
| プラン・AI残量 | /htu/uni-note/plans/ | #usage |
| 便利な使い方 | /htu/uni-note/workflows/ | 12レシピへの入口を維持 |
| iPadOSとの組み合わせ | /htu/uni-note/ipados/ | #windows, #files |
| 困ったとき | /htu/uni-note/troubleshooting/ | #help |

## 既存個別ページ → 統合先

| 元ページ | 統合先 | 操作ID | 画像スロット |
|---|---|---|---|
| /htu/uni-note/start/screens/ | /htu/uni-note/start/#screens | N01, S39 | 原本・session・slotを全件維持 |
| /htu/uni-note/start/first-note/ | /htu/uni-note/start/#first-note | N02, N03, N05, N69 | 原本・session・slotを全件維持 |
| /htu/uni-note/library/subjects/ | /htu/uni-note/library/#subjects | N04, N10, N56 | 原本・session・slotを全件維持 |
| /htu/uni-note/library/folders/ | /htu/uni-note/library/#folders | N14, N15, N16, N17, N18, N19, N20, N68 | 原本・session・slotを全件維持 |
| /htu/uni-note/library/search/ | /htu/uni-note/library/#search | N12, N13 | 原本・session・slotを全件維持 |
| /htu/uni-note/notebooks/manage/ | /htu/uni-note/notebooks/#manage | N06, N07, N08, N09, N11, N57 | 原本・session・slotを全件維持 |
| /htu/uni-note/notebooks/pages/ | /htu/uni-note/notebooks/#pages | N21, N22, N25, N26, N27, N63 | 原本・session・slotを全件維持 |
| /htu/uni-note/notebooks/vertical/ | /htu/uni-note/notebooks/#vertical | N23, N65 | 原本・session・slotを全件維持 |
| /htu/uni-note/writing/pens/ | /htu/uni-note/writing/#pen | N28, N29, N30, N31, N32, N33 | 原本・session・slotを全件維持 |
| /htu/uni-note/writing/erasing/ | /htu/uni-note/writing/#eraser | N34, N35, N36, N37, N38 | 原本・session・slotを全件維持 |
| /htu/uni-note/writing/palette/ | /htu/uni-note/writing/#palette | N39, N40 | 原本・session・slotを全件維持 |
| /htu/uni-note/writing/ruler/ | /htu/uni-note/writing/#ruler | N41, N42, N43, M50, M51 | 原本・session・slotを全件維持 |
| /htu/uni-note/writing/move/ | /htu/uni-note/writing/#selection | N44, N45 | 原本・session・slotを全件維持 |
| /htu/uni-note/materials/photos/ | /htu/uni-note/materials/#photos | M01, M02, M03 | 原本・session・slotを全件維持 |
| /htu/uni-note/materials/pdf/ | /htu/uni-note/materials/#pdf | M04, M05, M06 | 原本・session・slotを全件維持 |
| /htu/uni-note/materials/arrange/ | /htu/uni-note/materials/#arrange | M07, M08, M09, M10, M11, M12, M13 | 原本・session・slotを全件維持 |
| /htu/uni-note/materials/vertical/ | /htu/uni-note/materials/#vertical | M14, M15 | 原本・session・slotを全件維持 |
| /htu/uni-note/materials/export/ | /htu/uni-note/materials/#export | M17, M18, S17, S42 | 原本・session・slotを全件維持 |
| /htu/uni-note/recording/capture/ | /htu/uni-note/recording/#capture | M20, M21, M22, M23, M24 | 原本・session・slotを全件維持 |
| /htu/uni-note/recording/play/ | /htu/uni-note/recording/#play | M25, M26, M27, M28, M29, M30 | 原本・session・slotを全件維持 |
| /htu/uni-note/recording/transcribe/ | /htu/uni-note/recording/#transcribe | M32, M33, M34, M35, M36 | 原本・session・slotを全件維持 |
| /htu/uni-note/recording/summary/ | /htu/uni-note/recording/#summary | M37, M38, M39, M40, S43 | 原本・session・slotを全件維持 |
| /htu/uni-note/recording/paste/ | /htu/uni-note/recording/#paste | M41 | 原本・session・slotを全件維持 |
| /htu/uni-note/study/sticky/ | /htu/uni-note/study/#sticky | M42, M43, M44, M45, M46, M62 | 原本・session・slotを全件維持 |
| /htu/uni-note/study/pomodoro/ | /htu/uni-note/study/#pomodoro | M52, M53, M54, M55, M56 | 原本・session・slotを全件維持 |
| /htu/uni-note/study/laser/ | /htu/uni-note/study/#laser | M57, M58 | 原本・session・slotを全件維持 |
| /htu/uni-note/ai/answer/ | /htu/uni-note/ai/#answer | A02, A03, A04, A05, A06, A07, A08 | 原本・session・slotを全件維持 |
| /htu/uni-note/ai/settings/ | /htu/uni-note/ai/#settings | A01 | 原本・session・slotを全件維持 |
| /htu/uni-note/problem-sets/generate/ | /htu/uni-note/problem-sets/#generate | Q01, Q02, Q03, Q04, Q05, Q06, Q07 | 原本・session・slotを全件維持 |
| /htu/uni-note/problem-sets/review/ | /htu/uni-note/problem-sets/#review | Q08, Q09, Q10 | 原本・session・slotを全件維持 |
| /htu/uni-note/problem-sets/edit/ | /htu/uni-note/problem-sets/#edit | Q11, Q12, Q13, Q14, Q15, Q16 | 原本・session・slotを全件維持 |
| /htu/uni-note/problem-sets/home/ | /htu/uni-note/problem-sets/#home | Q18 | 原本・session・slotを全件維持 |
| /htu/uni-note/customize/settings/ | /htu/uni-note/customize/#settings | S01 | 原本・session・slotを全件維持 |
| /htu/uni-note/customize/paper/ | /htu/uni-note/customize/#paper | S02, S03, S04, S05, S06, S07, S08, S09 | 原本・session・slotを全件維持 |
| /htu/uni-note/customize/display/ | /htu/uni-note/customize/#display | S10, S11, S12, S13, S14, S15, S16 | 原本・session・slotを全件維持 |
| /htu/uni-note/customize/toolbar/ | /htu/uni-note/customize/#toolbar | N46, N47, N48, N49, N50, N51, N66 | 原本・session・slotを全件維持 |
| /htu/uni-note/data/protect/ | /htu/uni-note/data/#protect | S25, S26 | 原本・session・slotを全件維持 |
| /htu/uni-note/data/trash/ | /htu/uni-note/data/#trash | S27, S28, S29, S30, S31 | 原本・session・slotを全件維持 |
| /htu/uni-note/backup/save/ | /htu/uni-note/backup/#save | S18, S19, S20, S21 | 原本・session・slotを全件維持 |
| /htu/uni-note/backup/restore/ | /htu/uni-note/backup/#restore | S22, S23, S24 | 原本・session・slotを全件維持 |
| /htu/uni-note/plans/usage/ | /htu/uni-note/plans/#usage | P01, P02, P04, P05, P06, P07, P08 | 原本・session・slotを全件維持 |
| /htu/uni-note/troubleshooting/help/ | /htu/uni-note/troubleshooting/#help | S32, S33, S34, S35, S36, S37, S38, S40, S41 | 原本・session・slotを全件維持 |
| /htu/uni-note/ipados/windows/ | /htu/uni-note/ipados/#windows | O01, O03 | 原本・session・slotを全件維持 |
| /htu/uni-note/ipados/files/ | /htu/uni-note/ipados/#files | O06, O07 | 原本・session・slotを全件維持 |

## 独立レシピを維持

- 縦ノートで資料を大きく表示して書き込む: /htu/uni-note/workflows/vertical-annotate/
- 見開きPDFを左右に分割して学習する: /htu/uni-note/workflows/split-spread/
- 資料の横に手書きスペースを残す: /htu/uni-note/workflows/material-margin/
- PDF・写真に付箋を付けて暗記する: /htu/uni-note/workflows/sticky-material/
- 録音・文字起こし・AI要約で授業を復習する: /htu/uni-note/workflows/record-review/
- AI要約をノートへ貼って追記する: /htu/uni-note/workflows/summary-annotate/
- AI問題集を手修正して復習する: /htu/uni-note/workflows/quiz-review/
- ポモドーロを使いながら勉強する: /htu/uni-note/workflows/focus/
- レーザーポインターで資料を説明する: /htu/uni-note/workflows/explain/
- 資料用と筆記用の2つのノートを並べる: /htu/uni-note/workflows/two-notes/
- SafariやPDF閲覧アプリと並べて書く: /htu/uni-note/workflows/external-material/
- 動画を小さく表示しながら書く: /htu/uni-note/workflows/pip/

## 196操作の新掲載先

| 操作ID | 大項目＋アンカー |
|---|---|
| N01 | /htu/uni-note/start/#screens |
| S39 | /htu/uni-note/start/#screens |
| N02 | /htu/uni-note/start/#first-note |
| N03 | /htu/uni-note/start/#first-note |
| N05 | /htu/uni-note/start/#first-note |
| N69 | /htu/uni-note/start/#first-note |
| N04 | /htu/uni-note/library/#subjects |
| N10 | /htu/uni-note/library/#subjects |
| N56 | /htu/uni-note/library/#subjects |
| N14 | /htu/uni-note/library/#folders |
| N15 | /htu/uni-note/library/#folders |
| N16 | /htu/uni-note/library/#folders |
| N17 | /htu/uni-note/library/#folders |
| N18 | /htu/uni-note/library/#folders |
| N19 | /htu/uni-note/library/#folders |
| N20 | /htu/uni-note/library/#folders |
| N68 | /htu/uni-note/library/#folders |
| N12 | /htu/uni-note/library/#search |
| N13 | /htu/uni-note/library/#search |
| N06 | /htu/uni-note/notebooks/#manage |
| N07 | /htu/uni-note/notebooks/#manage |
| N08 | /htu/uni-note/notebooks/#manage |
| N09 | /htu/uni-note/notebooks/#manage |
| N11 | /htu/uni-note/notebooks/#manage |
| N57 | /htu/uni-note/notebooks/#manage |
| N21 | /htu/uni-note/notebooks/#pages |
| N22 | /htu/uni-note/notebooks/#pages |
| N25 | /htu/uni-note/notebooks/#pages |
| N26 | /htu/uni-note/notebooks/#pages |
| N27 | /htu/uni-note/notebooks/#pages |
| N63 | /htu/uni-note/notebooks/#pages |
| N23 | /htu/uni-note/notebooks/#vertical |
| N65 | /htu/uni-note/notebooks/#vertical |
| N28 | /htu/uni-note/writing/#pen |
| N29 | /htu/uni-note/writing/#pen |
| N30 | /htu/uni-note/writing/#pen |
| N31 | /htu/uni-note/writing/#pen |
| N32 | /htu/uni-note/writing/#pen |
| N33 | /htu/uni-note/writing/#pen |
| N34 | /htu/uni-note/writing/#eraser |
| N35 | /htu/uni-note/writing/#eraser |
| N36 | /htu/uni-note/writing/#eraser |
| N37 | /htu/uni-note/writing/#eraser |
| N38 | /htu/uni-note/writing/#eraser |
| N39 | /htu/uni-note/writing/#palette |
| N40 | /htu/uni-note/writing/#palette |
| N41 | /htu/uni-note/writing/#ruler |
| N42 | /htu/uni-note/writing/#ruler |
| N43 | /htu/uni-note/writing/#ruler |
| M50 | /htu/uni-note/writing/#ruler |
| M51 | /htu/uni-note/writing/#ruler |
| N44 | /htu/uni-note/writing/#selection |
| N45 | /htu/uni-note/writing/#selection |
| M01 | /htu/uni-note/materials/#photos |
| M02 | /htu/uni-note/materials/#photos |
| M03 | /htu/uni-note/materials/#photos |
| M04 | /htu/uni-note/materials/#pdf |
| M05 | /htu/uni-note/materials/#pdf |
| M06 | /htu/uni-note/materials/#pdf |
| M07 | /htu/uni-note/materials/#arrange |
| M08 | /htu/uni-note/materials/#arrange |
| M09 | /htu/uni-note/materials/#arrange |
| M10 | /htu/uni-note/materials/#arrange |
| M11 | /htu/uni-note/materials/#arrange |
| M12 | /htu/uni-note/materials/#arrange |
| M13 | /htu/uni-note/materials/#arrange |
| M14 | /htu/uni-note/materials/#vertical |
| M15 | /htu/uni-note/materials/#vertical |
| M17 | /htu/uni-note/materials/#export |
| M18 | /htu/uni-note/materials/#export |
| S17 | /htu/uni-note/materials/#export |
| S42 | /htu/uni-note/materials/#export |
| M20 | /htu/uni-note/recording/#capture |
| M21 | /htu/uni-note/recording/#capture |
| M22 | /htu/uni-note/recording/#capture |
| M23 | /htu/uni-note/recording/#capture |
| M24 | /htu/uni-note/recording/#capture |
| M25 | /htu/uni-note/recording/#play |
| M26 | /htu/uni-note/recording/#play |
| M27 | /htu/uni-note/recording/#play |
| M28 | /htu/uni-note/recording/#play |
| M29 | /htu/uni-note/recording/#play |
| M30 | /htu/uni-note/recording/#play |
| M32 | /htu/uni-note/recording/#transcribe |
| M33 | /htu/uni-note/recording/#transcribe |
| M34 | /htu/uni-note/recording/#transcribe |
| M35 | /htu/uni-note/recording/#transcribe |
| M36 | /htu/uni-note/recording/#transcribe |
| M37 | /htu/uni-note/recording/#summary |
| M38 | /htu/uni-note/recording/#summary |
| M39 | /htu/uni-note/recording/#summary |
| M40 | /htu/uni-note/recording/#summary |
| S43 | /htu/uni-note/recording/#summary |
| M41 | /htu/uni-note/recording/#paste |
| M42 | /htu/uni-note/study/#sticky |
| M43 | /htu/uni-note/study/#sticky |
| M44 | /htu/uni-note/study/#sticky |
| M45 | /htu/uni-note/study/#sticky |
| M46 | /htu/uni-note/study/#sticky |
| M62 | /htu/uni-note/study/#sticky |
| M52 | /htu/uni-note/study/#pomodoro |
| M53 | /htu/uni-note/study/#pomodoro |
| M54 | /htu/uni-note/study/#pomodoro |
| M55 | /htu/uni-note/study/#pomodoro |
| M56 | /htu/uni-note/study/#pomodoro |
| M57 | /htu/uni-note/study/#laser |
| M58 | /htu/uni-note/study/#laser |
| A02 | /htu/uni-note/ai/#answer |
| A03 | /htu/uni-note/ai/#answer |
| A04 | /htu/uni-note/ai/#answer |
| A05 | /htu/uni-note/ai/#answer |
| A06 | /htu/uni-note/ai/#answer |
| A07 | /htu/uni-note/ai/#answer |
| A08 | /htu/uni-note/ai/#answer |
| A01 | /htu/uni-note/ai/#settings |
| Q01 | /htu/uni-note/problem-sets/#generate |
| Q02 | /htu/uni-note/problem-sets/#generate |
| Q03 | /htu/uni-note/problem-sets/#generate |
| Q04 | /htu/uni-note/problem-sets/#generate |
| Q05 | /htu/uni-note/problem-sets/#generate |
| Q06 | /htu/uni-note/problem-sets/#generate |
| Q07 | /htu/uni-note/problem-sets/#generate |
| Q08 | /htu/uni-note/problem-sets/#review |
| Q09 | /htu/uni-note/problem-sets/#review |
| Q10 | /htu/uni-note/problem-sets/#review |
| Q11 | /htu/uni-note/problem-sets/#edit |
| Q12 | /htu/uni-note/problem-sets/#edit |
| Q13 | /htu/uni-note/problem-sets/#edit |
| Q14 | /htu/uni-note/problem-sets/#edit |
| Q15 | /htu/uni-note/problem-sets/#edit |
| Q16 | /htu/uni-note/problem-sets/#edit |
| Q18 | /htu/uni-note/problem-sets/#home |
| S01 | /htu/uni-note/customize/#settings |
| S02 | /htu/uni-note/customize/#paper |
| S03 | /htu/uni-note/customize/#paper |
| S04 | /htu/uni-note/customize/#paper |
| S05 | /htu/uni-note/customize/#paper |
| S06 | /htu/uni-note/customize/#paper |
| S07 | /htu/uni-note/customize/#paper |
| S08 | /htu/uni-note/customize/#paper |
| S09 | /htu/uni-note/customize/#paper |
| S10 | /htu/uni-note/customize/#display |
| S11 | /htu/uni-note/customize/#display |
| S12 | /htu/uni-note/customize/#display |
| S13 | /htu/uni-note/customize/#display |
| S14 | /htu/uni-note/customize/#display |
| S15 | /htu/uni-note/customize/#display |
| S16 | /htu/uni-note/customize/#display |
| N46 | /htu/uni-note/customize/#toolbar |
| N47 | /htu/uni-note/customize/#toolbar |
| N48 | /htu/uni-note/customize/#toolbar |
| N49 | /htu/uni-note/customize/#toolbar |
| N50 | /htu/uni-note/customize/#toolbar |
| N51 | /htu/uni-note/customize/#toolbar |
| N66 | /htu/uni-note/customize/#toolbar |
| S25 | /htu/uni-note/data/#protect |
| S26 | /htu/uni-note/data/#protect |
| S27 | /htu/uni-note/data/#trash |
| S28 | /htu/uni-note/data/#trash |
| S29 | /htu/uni-note/data/#trash |
| S30 | /htu/uni-note/data/#trash |
| S31 | /htu/uni-note/data/#trash |
| S18 | /htu/uni-note/backup/#save |
| S19 | /htu/uni-note/backup/#save |
| S20 | /htu/uni-note/backup/#save |
| S21 | /htu/uni-note/backup/#save |
| S22 | /htu/uni-note/backup/#restore |
| S23 | /htu/uni-note/backup/#restore |
| S24 | /htu/uni-note/backup/#restore |
| P01 | /htu/uni-note/plans/#usage |
| P02 | /htu/uni-note/plans/#usage |
| P04 | /htu/uni-note/plans/#usage |
| P05 | /htu/uni-note/plans/#usage |
| P06 | /htu/uni-note/plans/#usage |
| P07 | /htu/uni-note/plans/#usage |
| P08 | /htu/uni-note/plans/#usage |
| S32 | /htu/uni-note/troubleshooting/#help |
| S33 | /htu/uni-note/troubleshooting/#help |
| S34 | /htu/uni-note/troubleshooting/#help |
| S35 | /htu/uni-note/troubleshooting/#help |
| S36 | /htu/uni-note/troubleshooting/#help |
| S37 | /htu/uni-note/troubleshooting/#help |
| S38 | /htu/uni-note/troubleshooting/#help |
| S40 | /htu/uni-note/troubleshooting/#help |
| S41 | /htu/uni-note/troubleshooting/#help |
| O01 | /htu/uni-note/ipados/#windows |
| O03 | /htu/uni-note/ipados/#windows |
| O06 | /htu/uni-note/ipados/#files |
| O07 | /htu/uni-note/ipados/#files |
| N60 | /htu/uni-note/workflows/vertical-annotate/ |
| M16 | /htu/uni-note/workflows/material-margin/ |
| M47 | /htu/uni-note/workflows/sticky-material/ |
| Q17 | /htu/uni-note/workflows/quiz-review/ |
| O02 | /htu/uni-note/workflows/two-notes/ |
| O04 | /htu/uni-note/workflows/external-material/ |
| O05 | /htu/uni-note/workflows/pip/ |

## 画像・内容の移動方針

180スロットをID・master・capture session・状態ごと保持。本文の語句、手順、条件、注意は変更せず、見出しレベル・重複ID・リンク先だけを統合先に合わせる。既存カテゴリ本文の案内とリンクも同一ページ内へ移す。本文内の旧個別ページ見出しへのリンクはfragment_mapで新しい節へ書き換える。旧URL自体の互換補完は行わない。トップの旧アンカーは各カテゴリ行の位置に保持する。

## 公開・テスト方針

ユーザー指示によりテストは実行しない。production build、差分確認、対応表による内容移動の照合を行う。既存CIのゲートは変更せず、push後の通常パイプラインに任せる。

## 追加指示による削除対象

44個別URLは、このチャットで増えたページのため削除を許可された。本文移動後に削除し、互換ページを作らない。

- content/uni-note-guide/start-screens.md
- content/uni-note-guide/start-first-note.md
- content/uni-note-guide/library-subjects.md
- content/uni-note-guide/library-folders.md
- content/uni-note-guide/library-search.md
- content/uni-note-guide/notebooks-manage.md
- content/uni-note-guide/notebooks-pages.md
- content/uni-note-guide/notebooks-vertical.md
- content/uni-note-guide/writing-pens.md
- content/uni-note-guide/writing-erasing.md
- content/uni-note-guide/writing-palette.md
- content/uni-note-guide/writing-ruler.md
- content/uni-note-guide/writing-move.md
- content/uni-note-guide/materials-photos.md
- content/uni-note-guide/materials-pdf.md
- content/uni-note-guide/materials-arrange.md
- content/uni-note-guide/materials-vertical.md
- content/uni-note-guide/materials-export.md
- content/uni-note-guide/recording-capture.md
- content/uni-note-guide/recording-play.md
- content/uni-note-guide/recording-transcribe.md
- content/uni-note-guide/recording-summary.md
- content/uni-note-guide/recording-paste.md
- content/uni-note-guide/study-sticky.md
- content/uni-note-guide/study-pomodoro.md
- content/uni-note-guide/study-laser.md
- content/uni-note-guide/ai-answer.md
- content/uni-note-guide/ai-settings.md
- content/uni-note-guide/problem-sets-generate.md
- content/uni-note-guide/problem-sets-review.md
- content/uni-note-guide/problem-sets-edit.md
- content/uni-note-guide/problem-sets-home.md
- content/uni-note-guide/customize-settings.md
- content/uni-note-guide/customize-paper.md
- content/uni-note-guide/customize-display.md
- content/uni-note-guide/customize-toolbar.md
- content/uni-note-guide/data-protect.md
- content/uni-note-guide/data-trash.md
- content/uni-note-guide/backup-save.md
- content/uni-note-guide/backup-restore.md
- content/uni-note-guide/plans-usage.md
- content/uni-note-guide/troubleshooting-help.md
- content/uni-note-guide/ipados-windows.md
- content/uni-note-guide/ipados-files.md
