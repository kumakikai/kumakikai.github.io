# KUMAKIKAI プロダクトポートフォリオ型トップ

実装・ローカル検証日: 2026-09-06。以下はデプロイ前に実施した検証の記録。最新の公開状況は [GitHub Actions](https://github.com/kumakikai/kumakikai.github.io/actions) で確認できる。

## 調査で確認したこと

- Hugo / PaperMod。テーマは `themes/PaperMod` のGit submodule。
- 以前のトップは6言語の `content/_index*.md` をPaperModのlist templateで表示し、日本語ではその下にNotes記事とページ送りを表示していた。
- 全アプリがテキスト説明と多数のサポートリンクで同列に並び、主力や利用場面が視覚的に伝わらなかった。
- サイトリポジトリにアプリアイコン／スクリーンショットや `static/` はなかった。`assets/` はCSS、`layouts/` はheader等の既存overrideのみ。
- `hugo.toml` は日本語をルート、英語・韓国語・ドイツ語・繁体字・フランス語を言語サブディレクトリに設定。既存ルートを維持した。
- `.github/workflows/deploy.yaml` はmain push → Hugo extended **0.154.5**でminify build → `gh-pages` publish。ワークフロー、テーマ本体、各アプリの詳細本文は変更していない。
- 詳細の主なパスは `/htu/`、`/faq/`、`/privacy/`、`/terms/`、`/notes/`。トップから案内を整理した上で全既存URLを維持した。

## デザインと情報設計

Hero → Featured Apps → Other Apps → About KUMAKIKAI → Support & Contact → PaperMod footer。

白を基本に、アプリごとの淡いニュートラルな背景と余白で区切る。大きなコピーと実在するアプリ画像を中心にし、Uni:Noteに最も広い画像領域を割り当てた。オトミルとNoccaはPCで左右を反転。その他4アプリは小さなカードにまとめた。

公開済みFeaturedにはApple公式のApp Storeバッジと既存詳細への2導線。Otherにも詳細とApp Storeの両方を配置。Noccaには「開発中」と詳細のみを表示する。サポートはページ後半のアプリ別detailsに集約し、FAQや規約も辿れる。

PaperModのテーマ切替・保存・自動配色を維持。6言語のコピーとaltを用意し、翻訳のない詳細は日本語ページへ遷移する旨を明記。画像は日本語版であることを日本語以外のトップに表示する。Webフォントと独自JavaScriptは追加していない。

## 採用コピー・公開確認

Hero: **日常の小さな不便を、シンプルなアプリで。**

2026-09-06にApple公式公開Lookup APIで実際の配信状況とバージョンを確認。アプリ側の未公開ローカル変更を公開機能として宣伝しない。

| 区分 | アプリ / 公開版 | トップのコピー | 遷移先 |
|---|---|---|---|
| Featured | Uni:Note / 3.4.0 | 大学のノートを、iPadへ。 | [App Store](https://apps.apple.com/jp/app/id6760258084)、`/htu/uni-note/` |
| Featured | オトミル / 1.0.1 | 聞こえにくい会話を、大きな字幕に。 | [App Store](https://apps.apple.com/jp/app/id6770774613)、`/htu/oto-miru/` |
| Featured | ギガポケ / 0.1.0 | 届いたギガ、期限切れにしない。 | [App Store](https://apps.apple.com/jp/app/id6807501268)、`/notes/2026-09-02-giga-poke/` |
| Featured | Nocca / 開発中 | 家族へ伝える。自分のペースで。 | `/notes/2026-09-06-nocca/`。公開Lookup結果0件、当日仕様書も提出準備中。Storeボタンなし |
| Other | Uni:Note Pocket / 3.4.0 | Uni:Noteで書いたノートを、iPhoneで復習。バックアップを読み込む閲覧専用アプリ。 | [App Store](https://apps.apple.com/jp/app/id6761449487)、`/htu/uni-note-pocket/` |
| Other | ギャンカレ / 1.4.0 | 収入と支出をその場で記録。カレンダーで日々のお金の流れを振り返る。 | [App Store](https://apps.apple.com/jp/app/id6757731648)、`/htu/balance-calendar/` |
| Other | すわなび / 1.1.1 | 「吸った」と「我慢した」をワンタップで記録。本数と金額の変化を確認。 | [App Store](https://apps.apple.com/jp/app/id6760842941)、`/htu/smokeless/` |
| Other | SIGNAL / 1.1.1 | note、Qiita、Zennなどの個人発信を、自分のペースで読むニュースフィード。 | [App Store](https://apps.apple.com/jp/app/id6759493613)、`/htu/signal/` |

Featuredの説明本文:

- **Uni:Note:** Apple Pencilで書く。PDFに書き込む。ノートを教科やフォルダで整理し、AIで問題集づくりや、囲った問題の質問・解答まで。授業の記録から復習へ、ひと続きに。
- **オトミル:** テレビの声も、身近な人との会話も。音声をiPhoneやiPadの大きな文字で表示し、聞き取りづらい場面をサポートします。
- **ギガポケ:** povo 2.0の特典コードを、期限が近い順にまとめて管理。使いたいコードをすぐにコピー。ウィジェットでも、次に使うギガを確認できます。
- **Nocca:** 家族との会話や接触に負担を感じる方が、必要なことだけ意思表示できるアプリ。家族はその意思を受け取り、必要なときに返事をします。

ギガポケにはpovo 2.0の非公式アプリであり、KDDI・povo・auとの提携／協賛／公認等がない旨を既存表現に沿って掲載。Webコピーに価格・無料・未公開機能の訴求は入れていない。Pocketの自動同期や編集機能も示していない。

## 使用した画像

すべて実アプリ・既存制作物。ダミー画像やAI生成画像なし。各原本のパス／公開URL、SHA-256、出力サイズ・容量は `asset-manifest.json` に記録。

| アプリ | 使用素材 | 原本 |
|---|---|---|
| Uni:Note | 手書きノート、AI問題集 | `uni_note/artifacts/app_store_jp_refresh_2026-09-02/final_v7/SS01_handwriting.png`、`SS03_problem_set.png`。2064×2752。現行Store画像と一致する制作済み素材 |
| オトミル | 大きな字幕、シンプルモード | 現在Appleが配信している日本語Store画像の `3.png`、`2.png`。1284×2778。ローカルの完成画像には配信版と異なるものがあり、公式配信元を使用 |
| ギガポケ | 期限順一覧、ウィジェット | `povo_manager/design/app-store-screenshots-2026-09-04-review-fix/1242x2688-upload/01-hero.png`、`02-widget.png`。1242×2688。価格表現を修正済みのセット |
| Nocca | 意思表示のホーム、本人／家族の役割説明 | `Nocca/docs/audit/screenshots/after/child_home_connected.png`（1170×2532）、`docs/audit/assets/2026-09-06-role-copy/onboarding-standard.png`（750×1334）。現行コードと照合した実画面。「開発中の画面」と表示 |

アイコン8本は各アプリの現行Assetsカタログから取得。WebP化した256px版を使用する。

- スクリーンショットは2解像度のWebP。iPad素材560/1120px、iPhone素材420/840px、原本750pxのNoccaは上限750px。
- 画像24ファイル（8アイコン＋8スクリーンショット×2サイズ）で **728,250 bytes**。元画像は変更せず、拡大もしない。`cwebp -q 86 -m 6 -resize WIDTH 0` で変換。
- `srcset` / `sizes`、width / height、説明的なaltを設定。最初のUni:Note画像のみeager/high priority、それ以外はlazy。画像リンクから大きい方を確認できる。
- Apple公式バッジは `https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg` をローカル配信。

## Hugo実装と保守

| ファイル | 役割 |
|---|---|
| `layouts/index.html` | トップのみの独自main。PaperMod base/head/footerを利用 |
| `layouts/partials/app-showcase.html` | Featured、公開状態によるCTA制御、レスポンシブ画像 |
| `layouts/partials/app-card.html` | Other Apps |
| `layouts/partials/app-detail-link.html` | 翻訳存在に応じた既存詳細URL解決 |
| `layouts/partials/portfolio-header.html` | トップ専用ナビ、言語メニュー、既存テーマ切替 |
| `layouts/partials/header.html` | `.IsHome` の場合だけ上記ヘッダーへ分岐 |
| `assets/css/extended/home.css` | トップに限定したスタイル、画面幅・ダーク・reduced-motion対応 |
| `data/apps.json` | アプリ順序・featured/status・URL・画像。将来の昇格／降格はここで変更 |
| `data/home/{ja,en,ko,de,zh-hant,fr}.json` | 6言語のコピーとalt |
| `content/_index*.md` | 各言語トップのtitle/descriptionのみ |
| `static/images/apps/` | 最適化した実画像 |
| `static/page/{1..5}/index.html`、`static/{en,ko,de,zh-hant,fr}/page/1/index.html` | 旧トップのページ送りURLを対応言語トップへ転送 |
| `static/favicon.svg`等、`hugo.toml` | 元サイトで欠落していたfaviconを補い設定。KUMAKIKAIのKによる簡素なサイト識別用マーク |

アプリ追加時は `data/apps.json` に1件追加し、各言語の `apps.<id>` と実画像を用意する。`status: published` と確認済み `appStoreURL` の両方が揃った場合だけStore導線が出る。`featured`、`reverse`、配列順でレイアウトを調整できる。テストの期待アプリ集合も公開確認に合わせて更新する。

旧ページ送りはHugo 0.154.5と0.155.3でhome aliasの解釈が異なるため、固定URLの小さな静的転送HTMLで保持した。日本語の `/ja/` パスや新しいアプリ詳細URLは作っていない。

## レスポンシブ・アクセシビリティ

- PC: 最大1200pxの内容幅。コピー＋スクリーンショット2枚の左右配置。
- 900px以下: コピー→CTA→画像。iPad縦向きは1カラム、1024px幅では2カラム。
- 540px以下: スクリーンショットを1枚ずつ縦に表示。横スクロールやカルーセルに依存せず、本文中で読めるサイズを優先。
- OtherはPC4列、タブレット／通常のスマートフォン2列、小さい画面1列。
- H1を1つにし、セクションH2／アプリH3で構造化。スキップリンク、focus-visible、native details、十分なコントラストを提供。
- CSSの軽いhoverのみ。reduced-motionでは停止。テーマ切替を含む独自JSは追加せず、PaperModの挙動を利用。
- JavaScript無効・OSダークでも配色を維持し、動作しないテーマボタンを非表示にする。

## 検証結果

| 検証 | 結果 |
|---|---|
| `hugo --minify` | CIと同じ0.154.5、ローカル0.155.3とも成功 |
| 原HEADを同じHugo版で生成してURL比較 | **191/191 HTML URL保持**。サポート／Notes 156、旧ページ送り10を含む |
| 内部リンク／画像／fragment | 6言語・646参照、エラー0 |
| SEO | title、description、canonical、OGPのタイトル／説明、hreflang、sitemap7ファイル／122 URLを確認 |
| ブラウザ | Chrome、1440×1000／820×1180／390×844でLight/Darkを撮影・目視確認 |
| 追加幅 | 320、375、768、1024px × 6言語で横はみ出しなし |
| 操作 | テーマ切替と再読込後の維持、6言語メニュー、サポート開閉、キーボードスキップリンク、reduced-motion成功 |
| axe-core 4.10.3 | 6言語×Light/Dark、WCAG 2/2.1/2.2 AA対象ルール、検出0件 |
| JavaScript無効 | Light/Dark、言語メニュー、配色、テーマボタン非表示を確認 |
| Lighthouse 12.8.2 PC | Performance **100**、Accessibility **100**、Best Practices **100**、SEO **100** |
| Lighthouse 12.8.2 モバイル | Performance **96**、Accessibility **100**、Best Practices **100**、SEO **100** |
| Layout shift | PC・モバイルとも **CLS 0**。Total Blocking Time 0ms |
| Git | `git diff --check` 成功。PaperMod submodule差分なし。既存 `.DS_Store` を保持 |

LighthouseはローカルHTTPサーバー上の1回の測定。モバイルはシミュレーション、iPhone/iPad実機・Safariでの検証や公開GitHub Pagesの測定ではない。ローカルサーバーには圧縮／長期キャッシュがなく、その指摘も含む。検証JSONは `verification/` に保存。

## 残る制約

- Noccaに完成済みStore画像はないため、実アプリ画面で紹介。公開が確認できるまでは開発中・Store導線なしを維持する。
- 英語等のトップも日本語スクリーンショットを使用し、その旨を表示している。
- OGPの画像は元サイト同様に未設定。title/description等のOGPメタデータは維持・更新した。
- 既存の各アプリ詳細本文は今回変更していない。調査中、オトミルの既存詳細に古いApple Intelligence / Foundation Models条件が残っていることを確認したが、トップへは転載していない。
- 上記の検証はローカル環境で実施したもの。GitHub Pagesへの反映は、対応するGitHub Actionsの成功と公開HTMLで別途確認する。

## 再検証

```sh
hugo --minify --destination /private/tmp/kumakikai-home-build --cleanDestinationDir
python3 scripts/verify-home.py /private/tmp/kumakikai-home-build
python3 -m http.server 1313 --bind 127.0.0.1 --directory /private/tmp/kumakikai-home-build
```

別ターミナルで、Playwright 1.62.1 / axe-core 4.10.3を解決できるNode環境から実行:

```sh
node scripts/verify-home-browser.cjs
node scripts/verify-home-accessibility.cjs
```

`CHROME_PATH`、`HOME_PREVIEW_URL`、`HOME_SCREENSHOT_DIR`で実行環境を変更可能。テスト用依存はHugoのbuild/deployには不要。URL比較時の `--baseline` は同じHugoバージョンで作った原HEAD出力を渡す。

## 実際のトップページのスクリーンショット

`screenshots/` に最終CI版buildの実ブラウザ撮影を保存。

| 画面 | Light | Dark |
|---|---|---|
| Desktop 1440px | `desktop-light.jpg` | `desktop-dark.jpg` |
| iPad相当 820px | `ipad-light.jpg` | `ipad-dark.jpg` |
| iPhone相当 390px | `iphone-light.jpg` | `iphone-dark.jpg` |

最初の表示範囲: `desktop-light-first-view.png`、`iphone-light-first-view.png`。
