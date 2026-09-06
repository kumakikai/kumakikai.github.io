# KUMAKIKAI Hugoplate移行・検証報告

実装・検証: 2026-09-06〜07。移行前基準は `811d9e816f292562b42ba8395ac99683a031ff66`。この文書は実装とローカル検証の記録です。公開の実行履歴は[GitHub Actions](https://github.com/kumakikai/kumakikai.github.io/actions)で確認できます。

## 実装結果

1. **旧テーマと構成** — PaperMod（固定commit `6c5a8f6`）、Hugo Extended 0.154.5によるGitHub Pages公開。トップのみ独自portfolio、その他はテーマの一覧／記事。6言語、既存Markdown110件、Notes15記事。トップの分類・コピーは既に完成していたため維持対象とした。企業サイトとして不足していた共通ナビ、Products、News、Company、Hero実UI、記事とトップの一貫性を改善した。
2. **移行方法** — [Hugoplate公式commit `2f5a454`](https://github.com/zeon-studio/hugoplate/tree/2f5a454ee708f5f2666414af9ef48df65570752a)のruntimeを`themes/hugoplate/`へ固定。上流CSS／コンポーネント12ファイルはSHA-256一致、MIT LICENSE・出典を同梱。Tailwind v4のbase、content typography、container、section、buttonsと派生base shellを使用。KUMAKIKAIのレイアウトとCSSはrootで上書きする。PaperMod submodule・旧専用CSS／partialsは除去。デモcontent、作者、イラスト、価格表、推薦文、slider、不要なGo Modulesは導入していない。
3. **保持したトップ要素** — Hero → Featured → Other → About → Supportの流れ、Featured/Other分類、Featured順序、全6言語のアプリ名・キャッチコピー・説明の趣旨、非公式表記、About方向性、Support導線を保持。旧記事本文・公開日・タイトルをテーマ都合で書き換えていない。
4. **改善したトップ** — 実UIを組み合わせたHero、明確なApp Store Primary CTA、余白とスクリーンショットの階層、最新News3件、Company導線、簡潔なSupport、共通Footer。過剰な装飾・アニメーション・実績の創作なし。
5. **ナビゲーション** — 全言語でProducts / Support / News / Company。既存サポートやNotesを開いても関連する項目を選択状態にする。言語切替とテーマ切替を維持。モバイルはnative dialogのメニュー、JavaScript無効時は通常のリンクを表示。
6. **Featured Apps** — Uni:Note → オトミル → ギガポケ → Nocca。既存コピーは下表のとおり固定。Noccaは開発中、Storeリンクなし。
7. **Other Apps** — Uni:Note Pocket、ギャンカレ、すわなび、SIGNAL。小さなカードで紹介し、Featuredの視覚的な優先度を維持。
8. **Heroの変更** — 主見出し「日常の小さな不便を、シンプルなアプリで。」は維持。補足を「iPhone・iPad向けのアプリを企画・開発・運営しています。」に変更した。理由は事業内容を初見で明確にするため。6言語へ同じ趣旨を反映。アプリのキャッチコピーは変更していない。
9. **スクリーンショット** — Featuredは既存の各2枚、計8枚を継続使用。Uni:Noteの手書き／問題集、オトミルの字幕／入力選択、ギガポケのコード一覧／ウィジェット、Noccaの意思表示／役割説明。HeroはUni:Note、オトミル、ギガポケの実UI原本・公開済み素材から用意した3点。各2解像度のWebP、large3枚合計187,964bytes。出典・切り抜き・寸法は[Hero素材記録](hero-assets.md)、従来Featuredは[前回の素材一覧](../homepage/README.md)を参照。
10. **App Store CTA** — 公開7アプリは確認済み日本ストアへ直接リンクする独自テキストボタン。FeaturedはStoreをPrimary、製品詳細をSecondaryにした。Appleロゴは新作・改変していない。表示言語とStore地域は分離し、全言語で「日本のApp Storeで提供中」を明記。`availability.storefront`が確認済み地域に含まれる場合のみCTAを出す。Geo-IPや言語→国の変換なし。確認済み地域は部分集合であり、「日本のみ」「世界配信」と推測しない。[地域調査](availability.md)
11. **Products一覧** — `/products/`と5翻訳ルートに同じ全8アプリ。アイコン・名称・説明・プラットフォーム・公開状況・製品詳細を表示。アプリの地域別非表示は行わない。
12. **Product詳細** — `/products/{id}/`を8アプリ×6言語で作成。名称、端末、現在の説明、Store／Support、利用可能な実画像、使い方・FAQ・Privacy・Terms・関連記事を接続。既存詳細ページのURLを製品ページへ強制変更していない。
13. **Support** — `/support/`に全アプリを集約。アプリごとに既存の使い方、FAQ（トラブル対応を含む）、Privacy、存在するTerms、問い合わせへ進める。翻訳がない資料は日本語と明記。Uni:Noteの使い方への導線をブラウザで確認した。トップは主要4アプリへの入口と一覧CTAだけに圧縮。
14. **News** — `/news/`で既存15記事を日付・区分・タイトルの一覧へ整理。6件Press Release、9件Information。トップは最新3件。日本語のみの記事は翻訳ページでもその旨を示して既存日本語記事へ接続。翻訳追加時は同じ記事を重複表示しない。
15. **Press Release** — `/notes/.../`を維持し、区分、元の公開日、タイトル、本文、関連プロダクト、KUMAKIKAI紹介・問い合わせを共通デザインで表示。更新日が別に設定されている記事は更新日も表示。本文H1はrender hookでH2へ変換し、旧アンカーを保持。
16. **Company** — `/company/`に「運営名 KUMAKIKAI」「モバイルアプリケーションの企画・開発・運営」と既存メールを掲載。既存公開記事は個人事業主と記載しており、法人名・所在地・代表者等の裏付けがないため追加していない。
17. **Footer** — Products / Support / News / Company / Contact / Privacy とcopyright。ContactはCompany、Privacyは既存のアプリ別ポリシー一覧へ接続。不要なSNSや架空の企業情報はなし。
18. **URL互換性** — 基準buildの191 HTML URLをすべて保持。84記事の本文、1,285アンカー、161本文リンクを比較した。Hugo更新で翻訳aliasの言語prefixが二重になる問題を15件のfront matter正規化で修正。既存のすわなび誤記リンク`/htu/smoke-less/`、`/privacy/smoke-less/`にaliasesを追加。既存content17件の変更はfront matterだけで、本文は完全一致。プライバシー／利用規約はアプリごとに維持。旧正規138 URLの非redirectと元canonical、旧alias53件の元転送先・canonicalも固定検査する。[恒久URLの全一覧](permanent-urls.md)
19. **SEO** — 各ページのtitle、description、production canonical、hreflang、lang、favicon、OGP、Twitter card、sitemap、robotsを確認。生成204ページのSEO検査成功。Organization／SoftwareApplication／ArticleのJSON-LDを内容に応じて出力。価格・評価・レビュー数・利用者数は追加していない。404はnoindex。
20. **OGP** — 共通1枚＋アプリ別8枚を実際のアイコンと既存コピーで生成。1200×630 PNG、合計180,263bytes。Product／サポート／関連記事へ適切なアプリ画像を選択し、未指定は共通画像へfallback。front matterの`images`でも指定可能。既存の日本語ブランド画像を共通使用。[OGP素材記録](og-assets.md)
21. **GitHub Actions / Pages** — Node22、Hugo0.158.0 Extended、`npm ci`、lockfile、npm cache、production build、移行検証を導入。検証成功後だけ既存`gh-pages`へ公開。rootの`app-ads.txt`コピーを維持。
22. **Build** — `npm ci`、Hugo0.158.0 Extendedの`npm run build`、72生成ページの同期検査、`git diff --check`成功。build警告なし。ローカルNodeは25.6.1、CIの指定はNode22。旧Hugoを誤使用した場合は起動時に拒否する。
23. **Broken links** — 内部参照10,635件、旧191 URL、alias／ページ送り、全Product／Support、SEO画像、sitemapを検証しエラー0。7公開App StoreリンクはApple公式Lookupで日本配信を確認。外部サイト全体の網羅crawlやメール配送試験は実施していない。
24. **Responsive** — Desktop1440、Desktop1280、iPad834、iPhone Pro393、小型iPhone320の各幅で実ブラウザ確認。横はみ出し0。広い画面はHero／Featured左右配置、834以下は自然に1カラム。Otherは4→2列、Productsは3→2→1列。小型画面ではコピー→CTA→実画像の順、横スクロール不要。
25. **Light / Dark・操作** — トップと主要ページ、6言語を含む46画面でaxe・画像読み込み・heading・幅検査成功。追加の3画面で言語ラベルと画像sizesを再検証。メニューのTab循環、Escape、フォーカス復帰、背景スクロール停止、4主要リンク、テーマ保存、Support→使い方を確認。JavaScript無効時のナビ・ダーク背景を確認。外部フォントなし、追加JSは約1.6KB、motionは軽いhoverのみでreduced-motion対応。
26. **Lighthouse** — 最終値は下表と[検証JSON](verification.json)。Chromeでローカルproduction出力を計測。実回線・実機・公開サーバーの値ではない。ローカルHTTPサーバーの圧縮・cache headerに関する助言はホスティング条件による。
27. **未解決事項・検証範囲** — 実機iPhone／iPadのSafari確認は未実施。ブラウザのviewportとChromeによる検証である。App Store地域情報は確認日時点の部分集合であり、追加地域は公開時に再確認する。法人情報は根拠のある追加資料が公開された場合にのみ拡張する。
28. **素材不足** — Other4アプリは従来のアイコン・説明で構成し、新規スクリーンショットを捏造していない。Noccaは現在ある開発中2画面だけを使う。価格／無料表現を新たに追加していない。
29. **主な変更ファイル** — 下記一覧。アプリ追加は共通JSONとローカライズを編集し`npm run sync:products`。News追加はMarkdownだけでよい。運用手順は[README](../../README.md)。
30. **Desktopスクリーンショット** — [トップ](screenshots/desktop-top.webp)／[全体](screenshots/desktop-full.webp)／[Dark](screenshots/desktop-dark.webp)／[iPad](screenshots/ipad.webp)。
31. **Mobileスクリーンショット** — [トップ](screenshots/mobile-top.webp)／[全体](screenshots/mobile-full.webp)／[Dark](screenshots/mobile-dark.webp)／[小型iPhone](screenshots/small-iphone.webp)。

## 固定したFeaturedコピー

| 順 | アプリ | 現在のキャッチコピー | 公開状態 |
|---|---|---|---|
| 1 | Uni:Note | 大学のノートを、iPadへ。 | 公開中 |
| 2 | オトミル | 聞こえにくい会話を、大きな字幕に。 | 公開中 |
| 3 | ギガポケ | 届いたギガ、期限切れにしない。 | 公開中・非公式 |
| 4 | Nocca | 家族へ伝える。自分のペースで。 | 開発中 |

## Lighthouse

| 計測 | Performance | Accessibility | Best Practices | SEO | LCP | CLS |
|---|---|---|---|---|---|---|
| Mobile | 99 | 100 | 100 | 100 | 2.3 s | 0 |
| Desktop | 100 | 100 | 100 | 100 | 0.5 s | 0 |

## 主な変更ファイル

- `hugo.toml`、`.github/workflows/deploy.yaml`、`.hugo-version`、`.node-version`
- `package.json`、`package-lock.json`、`themes/hugoplate/`
- `layouts/baseof.html`、`home.html`、`single.html`、`list.html`、`404.html`、`robots.txt`
- `layouts/{products,product,support,news,company}/`、`layouts/_partials/`、`layouts/_markup/`
- `assets/css/main.css`、`assets/css/site.css`、`assets/js/site.js`
- `data/apps.json`、`data/corporate/`、`data/news.json`、`data/hero.json`、`data/theme.json`
- `content/{products,support,news,company}/`（72生成入口）と既存aliasのfront matter17件
- `static/images/hero/`、`static/images/og/`
- `scripts/{run-hugo.js,themeGenerator.js,sync-products.py,verify-migration.py,verify-browser.cjs,generate-og.mjs}`
- `README.md`、`docs/migration/`

## App Store関連URLの恒久維持

旧直接表示138 URLは同じURLの正式HTMLとして維持し、既存alias53 URLも元の転送先を維持する。新規ページ72 URLとは分けて扱う。追加aliasは誤記互換2件とHugoのtaxonomyページ送り12件。Hugo aliasはcanonical＋0秒meta refreshの静的HTMLで、JavaScriptに依存せず、HTTP301を返すものではない。既存Support／Marketing／Privacy／Press Releaseの正規本文ページをaliasへ置き換えていない。

[維持URL・新設URL・redirect・登録候補の全一覧](permanent-urls.md)と[機械可読一覧](permanent-urls.json)を保存。`verify-live.py`で公開後の全277 HTMLについてHTTP200・候補buildと同じ内容を検証する。App Store Connectの登録設定自体は変更していない。
