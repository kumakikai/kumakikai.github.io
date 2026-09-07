# スクリーンショット更新 — 2026-09-07

依頼に基づき、App Store Connectへ未アップロードの完成素材も公式サイトへ反映。アプリの公開状況・Store URL・地域・利用条件は変更していない。

## 採用素材

| 対象 | 最新セットと掲載内容 |
| --- | --- |
| すわなび | `design/app-store-screenshots-2026-09-03/final/1284x2778-upload/` の `01-value.png`、`03-counts.png`。9月7日のDynamic Islandフレーム統一版 |
| Uni:Note Pocket | `artifacts/app_store_screenshots_2026-09-02/final/` の `SS01_review_now.png`、`SS02_import_backup.png`、Product詳細用 `SS03_practice_set.png`。9月7日の再書き出し版 |
| SIGNAL | `artifacts/app_store_screenshots_2026-09-03/final/1284x2778/` の `05_creators.png`、`06_choose_sources.png`。9月7日の再書き出し版 |
| Nocca | `docs/store-assets/iphone-2026-09-07/final/` の採用済み6枚から `01-quiet-person.png`、`02-family-replies.png`。旧7枚の不採用案は使用しない |

完成PNG全体を等比で420／840pxへ縮小し、WebP quality 86／effort 6で保存。Noccaは実画面単体から正式紹介素材へ切り替え、家族の受信・定型文返信を示す2枚目に合わせて説明・altを6言語更新。その他の画像テーマと本文は維持。Home Featured・Product・Aboutの共通参照先を更新し、PocketのProduct専用画像も更新した。Guideの実操作画像は今回の対象外。OGPはアプリアイコンだけを使用するため再生成不要。

## Home Heroの修正

- オトミルは最新の `01_simple.png` に含まれるDynamic Island付きシンプルモードの端末内画面を使用。制作コードの画面領域に沿って `(227,738,830,1796)` を抽出した。
- ギガポケの旧画像は宣伝画像の下端で切れた画面（974×1794）を使っていたため、同じ幅でも短く太く見えていた。制作元のモザイク済み全画面（1206×2622）をアプリのGit履歴から回収し、採用済みv3の端末構成を全画面で再現した。元の文字・一覧・コードのモザイクは保持。
- ギガポケは幅1040へ等比縮小後、共通比率に合わせて下端の無地10行だけ除外。除外領域は全ピクセルRGB `(245,246,241)` で、操作・文字・ホームバーを含まない。Dynamic Islandは採用済みv3と同じ位置・寸法・色。元の宣伝canvasを縦に延長して全画面を抽出した結果とピクセル一致を確認した。
- 両画像とも320×693／640×1386へ等比の `contain` で書き出し。整数丸めによる最大1pxの余白のみ。端末の幅・枠・配置は既存CSSを使用し、画面を引き伸ばさない。

絶対出典、Git参照、原本／出力SHA-256、寸法、容量、加工範囲は [assets.json](assets.json)。配信画像は日付付きの新URLへ切り替え、旧画像URLは互換性のため保持した。

## 検証

- 指定Node 22.22.0／Hugo Extended 0.158.0でproduction build PASS、同期ずれなし。
- `npm run verify`／`npm run verify:seo` PASS。277 HTML、既存URL・Support・静的参照・画像・SEOを確認。
- 基本情報48ページ＋負例17件、Nocca法務25 tests PASS（並行作業の最新サポート・法務更新を取り込み後に再検証）。
- Hero: 375〜1440pxの9幅×light/dark、他5言語を合わせた23ケースPASS。同じフレーム幅・高さ、無歪み、はみ出しなし。1440／390px画像を目視確認。
- Home Featured: 33ケースPASS。10回reload、全候補の左右、901／900px境界、light/dark、no-JSを確認。CLSはいずれも0.1以下。
- Product: 4アプリ×1440／768／390pxの12ケースPASS。15枚を目視確認し、Dynamic Island、画像・本文・公開状態の整合を確認。
- WebP22ファイル計807,664bytes、最大110,504bytes。新規依存・CSS・JS変更なし。

ローカルの検証結果・画面は `artifacts/screenshot-refresh-20260907/`。要約は [verification.json](verification.json)。公開確認はソースcommitのActions／Pages成功と、gh-pages成果物・本番の対象ページ／画像のSHA一致で行う。
