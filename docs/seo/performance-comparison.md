# 公開後Lighthouse確認と変更前比較

対象：`https://kumakikai.github.io/`。公開ソース `106f7d9`、公開成果物 `14e8efc84d61858c86e23986ea7409c3e3d1cb3c`。2026-09-07にPages公開成功後、既存Chrome / Lighthouse 12.8.2で確認した。

## 結果

| ページ | 条件 | Performance 前 → 後 | LCP 前 → 後 | CLS 前 → 後 | TBT 前 → 後 |
| --- | --- | ---: | ---: | ---: | ---: |
| `/` | mobile | 98 → 100 | 1.53秒 → 1.53秒 | 0 → 0 | 0 → 0ms |
| `/products/uni-note/` | mobile | 100 → 100 | 1.36秒 → 1.36秒 | 0 → 0 | 0 → 0ms |
| `/htu/uni-note/` | mobile | 100 → 100 | 1.24秒 → 1.23秒 | 0 → 0 | 0 → 0ms |
| `/` | desktop | 未計測 → 100 | 未計測 → 0.34秒 | 未計測 → 0 | 未計測 → 0ms |
| `/products/uni-note/` | desktop | 未計測 → 100 | 未計測 → 0.33秒 | 未計測 → 0 | 未計測 → 0ms |
| `/htu/uni-note/` | desktop | 未計測 → 100 | 未計測 → 0.28秒 | 未計測 → 0 | 未計測 → 0ms |

公開後は6条件すべてPerformance / Accessibility / Best Practices / SEOが100。エラー・run warningなし。MobileのLCPは約1.23〜1.53秒、Desktopは約0.28〜0.34秒、CLSとTBTはいずれも0だった。測定範囲で重大な性能劣化は検出していない。

## 測定条件の訂正

変更前監査でDesktopと報告した3件は、Lighthouse Node APIに渡した `preset: desktop` が設定へ反映されず、実際はMobile条件だった。原本の `configSettings.formFactor=mobile`、412×823のscreenEmulation、CPU 4倍のthrottlingから確認した。変更前Desktop値として扱った旧報告を訂正する。

`before-performance.json.gz` の原本は書き換えていない。`before-performance.json` summaryと `baseline.md` に訂正を追記し、上表では変更前Desktopを未計測としている。変更前との同条件比較は最初のMobile3件に限る。

公開後の初回測定にも旧スクリプトが使われたため、その結果は `after-performance-invalid-desktop-label.json.gz` に退避した。確定値は公式 `lighthouse/core/config/desktop-config.js` をAPI第3引数に指定し、結果のformFactorが要求と一致することをassertしたうえで、6条件を再取得したもの。サイトのHTML/CSS/画像/JSには性能測定を理由とする変更を加えていない。

## 条件と限界

- Mobile：412×823、deviceScaleFactor 1.75、CPU slowdown 4、simulated mobile network。
- Desktop：1350×940、deviceScaleFactor 1、CPU slowdown 1、公式desktopDense4G設定。
- 同一マシンのChromeで1条件1回のLighthouseラボ測定。ランダムFeatured、ネットワーク、ホスト負荷によって値は変動する。MobileのHomeスコア98→100をSEO変更による速度向上と断定しない。
- TBTはラボ指標でありINPではない。CrUX、Search Consoleの実ユーザーCore Web Vitals、実測INPはこの検査では取得していない。
- Lighthouse SEO 100はチェック項目に対する結果。Googleインデックス、検索順位、すべてのschema.org意味検証やリッチリザルト適格性を保証しない。
- Pagesのキャッシュ寿命、画像の追加圧縮余地、Guide先頭画像のlazy loading等は診断に残るが、今回の測定では重大なLCP/CLS/TBT問題になっていない。

## 証拠

- `before-performance.json` / `before-performance.json.gz`：変更前と訂正注記。
- `after-performance.json` / `after-performance.json.gz`：訂正した条件での公開後確定値。
- `scripts/audit-seo-performance.mjs`：再実行スクリプト。既存一時QA依存のみ利用。

```sh
AUDIT_RUN=after TEST_BASE_URL=https://kumakikai.github.io \
  /private/tmp/kumakikai-node22/node_modules/node/bin/node scripts/audit-seo-performance.mjs
```
