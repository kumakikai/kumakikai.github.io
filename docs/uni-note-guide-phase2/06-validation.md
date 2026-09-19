# ローカル検証結果

2026-09-19。公開・配信・実機動作を検証した記録ではない。

| 検証 | 結果 |
|---|---|
| Node.js | 22.22.0。既存の作業用ランタイムをPATHで選択。システムNodeは変更なし |
| Hugo | Extended 0.158.0。プロジェクト指定版 |
| production build | PASS。prebuildの生成入口72ページに差分なし、日本語整形・検証PASS |
| `npm run verify` | PASS。サイト全体356 HTML、13,904内部参照、既存74文書、旧URL・アンカー等にエラー0 |
| `npm run verify:seo` | PASS。235索引対象ページ、エラー0・警告0 |
| `verify-uninote-guide.py` | PASS。73ページ、196操作、旧25アンカー、3,166内部参照、180スロット／110原本、エラー0 |
| `git diff --check` | PASS |
| 実ブラウザの導線 | トップ → 活用例カテゴリ → 縦ノート記事をクリックして到達 |
| 表示幅1280px | トップの画像読込・内部ID非表示・横はみ出しなし |
| 表示幅390px | トップ、縦ノート活用、ペン、PDF出力、プランの5ページ。横はみ出し・空figure・内部ラベルなし |
| 旧アンカー実表示 | `#pdf`が存在し、対応する写真・PDFの説明位置へ移動 |
| ブラウザconsole | error 0 |
| 画像 | 追跡済み224画像ファイルのhash不変。7素材を8か所に表示、172スロットはHTML非表示 |
| 翻訳・FAQ・他製品 | ソース未変更。サイト全体の既存チェックで確認 |
| 旧監査カタログ | `/htu/uni-note/`だけ更新。残り73 entry不変 |
| Phase 1 / 1.5 | 元資料未変更。継承hashを記録 |
| アプリ本体 | 本作業は読み取りのみ。並行作業でアプリrepoのdiff hashは変化したため、repo全体の不変とは報告しない |
| commit / push / deploy / 公開 | 実施していない |

初回buildは画像shortcodeの呼び出し方法と、Hugo既定cache先へのsandbox書込で失敗した。shortcodeを既存guide-imageと同じ画像処理方式にし、cacheを一時ディレクトリへ指定して解消。成功した最終buildをもって上表へ記録している。

旧本文のexact hashと画像配置を固定する前回監査は、今回の正当な再構成により初回には失敗した。immutable baselineは変えず、本文レビュー後に日本語Uni:Note 1ルートだけのhash・画像配置記録を更新して再検証した。新記事の画像未入手は専用検証器でチェックし、存在しない画像で既存検査を満たすことはしていない。

## 再実行

```sh
PATH=/private/tmp/kumakikai-build-tools/node-v22.22.0-darwin-arm64/bin:$PATH \
HUGO_BINARY=/private/tmp/kumakikai-build-tools/hugo-pkg/Payload/hugo \
HUGO_CACHEDIR=/private/tmp/uninote-phase2-hugo-cache npm run build

PATH=/private/tmp/kumakikai-build-tools/node-v22.22.0-darwin-arm64/bin:$PATH npm run verify
PATH=/private/tmp/kumakikai-build-tools/node-v22.22.0-darwin-arm64/bin:$PATH npm run verify:seo
python3 scripts/verify-uninote-guide.py
git diff --check
```

一時ランタイムが消えた場合は、`.node-version`と`.hugo-version`に合う既存の安全な環境を選び直す。本文や画像の改訂後は、確認済み出力の限定レビューを更新してからmigration検証を行う。

機械可読結果：`guide-verification.json`、`migration-verification.json`、`seo-verification.json`。画像の公開前確認と実配布アプリでの実操作確認は、このローカルサイト検証とは別工程。
