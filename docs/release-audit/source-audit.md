# 最終リリース監査 — ソース・テンプレート

監査対象の基準コミット: `2b4ff1c`。実装ファイルは変更せず、テーマ設定、全content、Productデータ、共通テンプレート、生成・デプロイ経路を確認した。公開HTTP・CDNキャッシュ・ビルド成果物の一致は別の本番監査結果と合わせて判断する。

## 結論

ソースには旧PaperModを使うProductページや、アプリごとに旧Header/Footerへ分岐するテンプレートはない。全8アプリ × 6言語 = **48 Product詳細**が `type: product` と正しい `product_id` を持ち、`layouts/product/single.html` → `layouts/baseof.html` を共通で使う。個別の `layout`・`url` override は0件。

`hugo.toml:7` は `theme = "hugoplate"`。ローカルの `layouts/baseof.html` が上流テーマのbaseをoverrideし、全通常ページへ現在のHeader/Footerを挿入する。`themes/hugoplate/layouts/baseof.html` の上流デモ用構造は選択されない。リポジトリ内のテーマはHugoplateのみ。

## 対象とテンプレート

| 対象 | 件数 | 共通テンプレート |
|---|---:|---|
| Product詳細 | 48 | `layouts/product/single.html` |
| 使い方 | 22 | `layouts/single.html` |
| FAQ | 22 | `layouts/single.html` |
| Privacy本文 | 22 | `layouts/single.html` |
| 独自Terms本文 | 3 | `layouts/single.html` |
| News/Notes記事本文 | 15 | `layouts/single.html` |
| Home | 6 | `layouts/home.html` |
| Products一覧 | 6 | `layouts/products/list.html` |
| About | 6 | `layouts/company/list.html` |
| News一覧 | 6 | `layouts/news/list.html` |
| Support互換入口 | 6 | `layouts/support/list.html` |
| Privacy/Guide/FAQ/Terms/Notes一覧 | 20 source entries | `layouts/list.html` |
| 旧ページ番号URL | 10 static HTML | 正式URLへの最小限の互換redirect |

contentは合計182 Markdown（132 regular page、50 section/home entry）。News分類はPress Release 8件、Blog 7件、Information 0件。全ファイル・Product URL・各言語プロフィール・ソースハッシュは `source-audit.json` に記録した。

## 全Productの確認

各行とも6言語すべてで同じProductテンプレートを使う。

| Product ID | 日本語デバイス表示 | 状態 | 利用規約 |
|---|---|---|---|
| `uni-note` | iPad | published | Apple Standard EULA |
| `oto-miru` | iPhone / iPad | published | `/terms/oto-miru/` |
| `giga-poke` | iPhone | published | `/terms/giga-poke/` |
| `nocca` | iPhone | development | `/terms/nocca/` |
| `uni-note-pocket` | iPhone | published | Apple Standard EULA |
| `balance-calendar` | iPhone | published | Apple Standard EULA |
| `smokeless` | iPhone（Watchは共通platform partialで審査状態付き追記） | published | Apple Standard EULA |
| `signal` | iPhone | published | Apple Standard EULA |

`layouts/_partials/product-platform.html` が現行の `data/home/<lang>.json` を参照する。Uni:Noteは全言語 `iPad`。Noccaの未公開状態とStore URLなしを維持している。

Product Heroの `app-cta.html` は `product: true` により「詳しく見る」を出さず、公式 `app-store-badge.html` を使用する。上部の独立した「サポートを見る」は存在しない。地域は `verifiedStorefronts` と確認済み国別URLから旗を表示し、表示言語から提供国を推定しない。

Product下部は `support-links.html` / `support-data.html` の5項目。Guide/FAQも同じデータを利用し現在のページを除外する。ProductのPress Releaseリンクはない。News記事の関連Product導線、法務本文中の必要なPrivacyリンクは正当な役割として維持する。

## Header / Footer / 旧ハブ

- `layouts/_partials/essentials/header.html:6,19` は `products, news, company` だけを列挙。`data/corporate/*:6` の表示名はすべて `About`。DesktopとMobile共通の3項目。
- Footerは `layouts/_partials/essentials/footer.html` に1つだけ。KUMAKIKAI、`/company/#contact` へのContact、copyright、Apple商標の補足。
- `data/corporate/*` にある `nav.support` は互換 `/support/` のfront matter生成用に残っているが、Headerの反復対象には入らない。
- Header / Footer / Home / Product / Guide / FAQの共通導線に `/support/` や `/privacy/` 総合ハブへの直接リンクはない。各アプリのPrivacy本文URLは必要なため残す。
- `layouts/list.html` のresource branchは旧Privacy indexのMarkdown一覧本文を描画しない。Productsへの短い案内だけを表示する。`layouts/_partials/essentials/head.html:6,34` によって一覧互換ページを `noindex, follow` とする。
- `/support/#<app>`、`#support-<app>`、`#contact` はCSS targetで既存fragmentの到達性だけを維持。旧Support全アプリ一覧を主要入口として表示しない。
- `static/*/page/1/index.html` と `static/page/{1..5}/index.html` の10ファイルは旧テーマページではなく、canonical・meta refresh・リンクだけの互換HTML。URL保護のため削除しない。

## Founder

`data/company/{ja,en,de,fr,ko,zh-hant}.json` の6プロフィールすべてでProduct固有名は0件、氏名は `Yuya Nakamura`。旧Uni:Note/すわなびの小話はない。経験領域、肩書き、技術経験は残る。

現在の日本語本文:

> 組み込みシステム、業務システム、モバイルアプリなど、複数領域のソフトウェア開発を経験。現在はKUMAKIKAIで、iPhone・iPad向けアプリの企画・開発・運営を行っています。
>
> 作るものの分野は特に決めていません。自分が使っていて不便に感じたことや、身近な人から聞いた困りごとをきっかけに、必要だと思ったものをアプリにしています。

About基本情報は名称・開発者・事業内容の3項目。Web・メール欄なし。メールはContact CTAへ集約され、`contactSupportText` は「各プロダクトページ」の表記。

## 修正対象として共有した2点

1. **Aboutの説明metaだけ旧強調が残る** — `data/corporate/ja.json:54` と生成済み `content/company/_index.md:4` に「Uni:Noteなどの開発背景、」が残っていた。Founder本文は現行だが、meta description/OGPが削除済みエピソードの強調を引き継いでいた。rootが当該句だけを削除してsyncする方針。他言語に同種の個別エピソードmetaはない。
2. **News empty stateの初期HTML** — `layouts/_partials/news-items.html:11` はInformation 0件を表す段落を初期HTMLへ出力し、`assets/css/site.css:221-222` だけで表示状態を制御していた。CSSを評価しない外部取得では初期「すべて」でも文章を拾い得る。修正担当がnative `hidden` を追加する方針。通常ブラウザでの表示状態は別途実測し、旧テンプレートと混同しない。

## 検索ヒットの区別

`layouts/`、`data/`、`content/` を対象にした正確な文字列検索で、`iPad専用`、`日本のApp Storeで提供中`、`サポートを見る`、漢字Founder名、`各Productページ`、旧Founderの2つのエピソード全文は0件。

`App Storeで見る` は `data/home/ja.json:28` の未使用翻訳キー `store` に1件のみ。現行CTAはこのキーを参照せず公式バッジを出すため、旧ボタンの表示とは区別する。source上の未使用キーを理由にProductページを旧仕様と判定しない。

記事本文にある「Uni:Noteは」「すわなびは」は製品そのものの説明であり、Founderの旧個別エピソードではない。過去記事・法務本文への機械的な削除やコピー再創作は行っていない。

## 生成経路

`python3 scripts/sync-products.py --check` は **72ページ、差分0、成功**。全Product front matterが現在の共有JSONと一致し、旧metadataへ戻す別生成器はない。`themeGenerator.js` はCSS生成のみ。

Nodeは `.node-version` の22.22.0、Hugo Extendedは `.hugo-version` の0.158.0へ固定。`npm run build` は `--cleanDestinationDir` を付け、`public/` はGit管理対象外。GitHub Actionsは同じnpm build後に検証し、`./public` を `gh-pages` へ発行する。`keep_files` を有効化するoverrideはない。ローカルpublicが古い場合やデプロイ/CDNの状態はソースだけで断定せず、rootの成果物・HTTP比較で結論を出す。
