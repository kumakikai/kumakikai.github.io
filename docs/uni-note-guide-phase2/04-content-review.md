# 日本語本文の限定レビュー

## 改訂の範囲

ユーザーがPhase 2の実制作を明示的に指示。P0適用済みworking treeを起点に、一般公開3.5.0のトップ1・カテゴリ16・目的別記事56を制作した。アプリ・FAQ・翻訳・他製品の変更は含まない。旧URLとアンカーを残し、記事だけへredirectするトップにはしていない。

196操作は全件掲載先を持つ。基本・詳細は目的別の短い記事、複数機能の組み合わせは独立した12の活用例へ分離。操作台帳1件につき1ページとはしていない。対応はimplementation-map.jsonと05-operation-coverage.md。

## P0の維持

| ID | 本文での確認箇所 |
|---|---|
| HF-P0-01 | トップ冒頭が一般公開版3.5.0。3.4.0への巻き戻しなし |
| HF-P0-02 | notebooks/manageの教科カード内ノート一覧、customize/toolbarの通常機能としての配置設定 |
| HF-P0-03 | problem-sets/editの手動作成・保存後編集、homeの表示設定。手動操作はAI残量を使わない |
| HF-P0-04 | study/stickyとworkflows/sticky-materialのパレット表示設定。旧学習支援ON導線なし |
| HF-P0-05 | ai/answerのその他／ナビゲーションバー配置。旧ONスイッチなし |
| HF-P0-06 | トップ・writing/move・materials/arrangeの写真／PDFのみの移動。付箋の透過／削除は維持 |

## P1の反映

| テーマ | 記事（/htu/uni-note/以下） | 確認した説明 |
|---|---|---|
| HF-P1-01 | materials/arrange | 初期固定、解除→選択→移動／素材のピンチ→固定→筆記 |
| HF-P1-02 | notebooks/vertical、materials/vertical、workflows/vertical-annotate | 作成時の縦罫＋モード、横送り、PDF／書類写真と普通の写真の差 |
| HF-P1-03 | materials/pdf、materials/export、workflows/split-spread | 選択・解除・PDF順・左→右・貼付先・出力範囲 |
| HF-P1-04 | recording各記事、ai/settings | 録音／保存／再生位置・速度、文字起こし条件・言語、AI回答言語、用途・消費量 |
| HF-P1-05 | recording/paste、workflows/summary-annotate | 現在のノートへ画像として貼る。新規ノート自動作成ではない |
| HF-P1-06 | study/sticky、workflows/sticky-material | 色・太さ・新規への適用、透過、長押し削除、ホバー条件 |
| HF-P1-07 | writing/move、erasing、ruler | Pencilで選択／移動、線／部分／全消去、取り消し不可と残る素材 |
| HF-P1-08 | problem-sets各記事、workflows/quiz-review | 候補選別・保存、手動作成、編集、復習を分離 |
| HF-P1-09 | backup/save、restore | 両方式への音声設定、容量・日時・置換復元・再起動、自動同期との区別 |
| HF-P1-10 | data/protect、trash | 書き込み保護・解除時認証、教科／ノート復元、期限と不可逆削除 |
| HF-P1-11 | ipados、workflows末尾3記事 | OS／アプリ機能を区別。2つの別ノート。外部アプリ条件 |
| HF-P1-12 | 全カテゴリ、study、customize | 196操作の割当、110原本への画像スロット、ポモドーロ・レーザー・設定 |

## 画像レビュー

既存9素材を目視し、7点だけを説明内容に合わせて再利用した。create-menu、home-search、writing-tools、record-button、sticky-marker、problem-answer、backup-file-actions。画像ファイルの変更なし。

- writing-toolsは道具を選ぶ部分だけを説明し、ペン詳細パネルの完成画像として扱わない。
- sticky-markerは手書きを隠した例であると明示。PDF教材の完成画像として流用しない。
- record-buttonは表示例の文字起こし言語が英語であることを明示。
- problem-answerはコピーと共有の2ボタンだけを説明。
- attachment-menuは3.5.0の全メニューとして不足、pdf-writingは古いナビゲーションがあるため再掲しない。元画像は保持。

合計180掲載スロット、110種の標準原本。既存7素材を8か所に掲載し、172スロットは非表示の撮影待ち。原本数・掲載箇所数・旧428カット枠を混同しない。12活用例の代表画像は14原本で、実画像は今回まだ用意していない。

## 既存監査の継承

全74文書の旧監査には「画像を同じ場所・同じ属性で維持」という前回改訂の条件がある。今回は日本語Uni:Noteの再構成が明示されたため、この1ルートだけreviewed-output.jsonの正確な画像リストと依存ファイルhashで検証する。残り73文書、翻訳、固定baseline、監査前snapshotの条件は変更しない。

reviewed-content.jsonは/htu/uni-note/の1行分だけ更新し、ほかの製品を一括再記録しない。新しい73ページ群はverify-uninote-guide.pyでも独立に検証し、pending画像のHTML非表示・リンク・操作ID・原本対応・画像不変を確認する。

## 大項目への統合（後続改訂）

44本文を15完全ガイドへ統合し、通常の説明はトップから1遷移で到達する。本文の仕様・条件・注意・P0/P1・HOLDはそのまま継承する。掲載先の現状は05-operation-coverage.md、画像は02-image-map.md、移動前後の対応はia-revision/を参照。旧個別URLはユーザーの明示指示で削除し、リダイレクトなし。テスト不要の指示に従い、本改訂では過去のPASSを新しい結果として扱わない。
