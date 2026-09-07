# 最終独立クロスレビュー

確認日: 2026-09-08。対象は `main` / `3ab462d3d03247df33420f0657cda305470d8e0b` 上の未コミット変更を含む最新ローカルソース。開始時に `git status --short` を確認し、本文・共通データは編集していない。

対象は8製品の74本文（Privacy 22、Terms 8、FAQ 22、Guide 22）と、`data/document_ui.json` の全6言語、`document-copy` / `document-contact` / `document-help`、Apple Watchの共通Guide。各言語の本文を読み合わせ、FAQ/Guide内の参照ラベル、明示的ID・旧IDと遷移先の節の内容も照合した。実装上の保持・課金条件は各Phase 1の一次根拠と比較した。公開ページや検索結果は使用していない。

この最終クロスレビューで追加のP1/P2は検出していない。Uni:Noteの年齢制限対応は、運営者によるApp Store Connectの指定変更済みの確認と[確定したプロジェクト判断](AGE_RATING_DECISION.md)に基づき対応完了へ更新した。Googleによる18+指定のみでの適合保証が確認できていない点は、既知の規約解釈上の留保事項として残し、リリース／公開ブロッカーとしない。追加の指摘は次のP3のみ。

## CF-01: Noccaの旧「つながり」アンカーの意味ずれ（修正確認済み）

- 検出時: `content/htu/nocca.md:47` の `guide-anchor "つながり"` が「送った意思表示と返信を確認する」の前にあった。同節の操作は `意思表示` タブであり、接続管理の `つながり` ではない。
- 意味が対応する操作は同ファイル `:26–36` の「家族と接続する」。`:32` に `つながり > 接続を確認する` がある。
- 最小修正: IDを削除せず、「家族と接続する」h3の直前へ移す。画像・本文・現行の `#signal-status` は維持する。
- 再確認: rootによる修正後、`content/htu/nocca.md:26` が `guide-anchor "未接続のとき" "つながり"` となり、同IDが接続節へ対応した。修正済み。

## CF-02: 共通定義と残存本文の呼称・大文字の表記差（修正確認済み）

意味やデータフローの矛盾ではないが、共通化後の残存表記としてrootへ報告した。行番号は検出時のソース。

| 対象 | 根拠 | 最小修正案 |
|---|---|---|
| Uni:Note / Pocket Privacy英語 | `content/privacy/uni-note.en.md` と `content/privacy/uni-note-pocket.en.md` に `The App` / `the App`。共通定義は `data/document_ui.json:53` の `the app` | `The app` / `the app` に統一。rootが別途検出し修正済み |
| Pocket Privacyフランス語 | `content/privacy/uni-note-pocket.fr.md:25,29,43` の `L’App`、`:27` の文中 `l’App`。共通定義は `data/document_ui.json:103` の `l’app` | `L’app` / `l’app` に統一 |
| Smokeless Privacy韓国語 | `content/privacy/smokeless.ko.md:27,41,45,53` に `당사`。共通冒頭 `data/document_ui.json:128` は `운영자` を定義 | `당사가` → `운영자가`、`당사는` → `운영자는` 等、既存文法を保って定義名に統一 |
| Uni:Note Privacy韓国語 | `content/privacy/uni-note.ko.md:23,69,79` の `이 앱`。共通定義は `본 앱` | 当該3箇所を `본 앱` へ |
| Uni:Note / Pocket Privacy繁体字中国語 | `content/privacy/uni-note.zh-hant.md:17,23,25,69,71,79`、`content/privacy/uni-note-pocket.zh-hant.md:25,29,43` の `本 App`。共通定義は `本App` | 定義語だけ空白をそろえる。製品名・App Store等は変更しない |

## CF-03: Uni:Note Privacy広告節の不要な時制前置き（修正確認済み）

日本語 `content/privacy/uni-note.md:69` は「本アプリは、広告配信SDKを利用していません」。翻訳側だけ次の前置きが残る。現状の広告機能の説明であり、期限を導入する必要はない。

| 対象 | 検出時の表記 | 最小修正案 |
|---|---|---|
| `content/privacy/uni-note.en.md:69` | `At this time, the App ...` | 前置きを削除し、`The app ...` |
| `content/privacy/uni-note.de.md:69` | `Derzeit verwendet die App ...` | `Die App verwendet ...` |
| `content/privacy/uni-note.fr.md:69` | `À ce jour, l'application ...` | 前置きを削除。呼称をそろえる場合は `L’app ...` |
| `content/privacy/uni-note.ko.md:69` | `현재 이 앱은 ...` | `본 앱은 ...` |
| `content/privacy/uni-note.zh-hant.md:69` | `目前本 App ...` | `本App ...` |

2026-09-08の再確認で、CF-02とCF-03の全修正を確認した。Pocketフランス語の文中 `:27` も `dans l’app` となった。rootが追加した `data/document_ui.json` の `privacyHeadings` 全6言語も読み合わせ、Smokelessフランス語・韓国語・繁体字中国語の削除節、韓国語の改定節が他製品の共通見出しへそろい、旧IDを保持していることを確認した。本レビューの追加指摘に未解消のものはなく、レビューを完了する。

## 今回追加の問題としなかった事項

- Guide末尾の `document-help` は `layouts/shortcodes/document-help.html:4–7` で当該製品・言語のFAQ `#help` を参照する。具体的操作リンクは対応する節へつながり、汎用的なヘルプ文言が限定的な問題節へ飛ぶ以前の問題は残っていない。
- `layouts/shortcodes/document-contact.html:16` はPrivacy/Termsで `legalContactNote` を使う。法務文書の問い合わせに、障害の再現操作を一律要求する共通文は出ない。法務本文にある手動送信・サポート情報の説明は、取得情報を説明する文脈として適切。
- Uni:Noteの録音権限の範囲は6言語とも録音時に限定され、再生にマイク許可を要求する前回の意味差は解消。ズームのFAQとGuide `#write`、Pocketの再開位置とGuide `#read` の参照も対応している。
- OtoMiruの字幕の一時閲覧は、Privacy/FAQ/Termsで上限前の手動停止に限定され、無料時間終了時等の消去条件と矛盾しない。Noccaの独自7日おためしとAppleの14日トライアル、Nocca内の家族利用とAppleのファミリー共有の区別も保持されている。
- Noccaの手動バックアップ削除や問い合わせ保持等の運用確認、App Store公開状態等の未確認事項はPhase 1のままであり、この文書レビューを根拠に確認済みへ変更しない。全生成HTMLと公開物の照合はrootの最終検証に委ねる。
