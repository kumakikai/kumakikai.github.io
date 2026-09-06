# 素材・App Store CTA・サポート・NewsのUX整理

実装・監査日: 2026-09-07。

現在のHugoplateによる情報設計と主要コピーを維持し、正式ストア素材、公式バッジ、確認済み配信地域、直接サポート導線を統一した。Newsは記事の性質に合わせて3分類へ整理した。既存のApp Store Connect関連URLとアプリ別Privacy本文を保持している。

**検証状態:** production build・静的検証・ブラウザ54ケース・GitHub Actions / Pages公開が成功。公開277 HTML URLすべてHTTP 200で今回の生成内容と一致し、新しい画像・公式バッジ・CSS・JSの18ファイルも一致した。

## 1. スクリーンショットの採用と鮮度

### SIGNAL

開発画面だけのキャプチャを、訴求コピー入りの正式App Store制作素材へ差し替えた。

- 制作フォルダ: `/Users/yuya/Projects/signal/artifacts/app_store_screenshots_2026-09-03/final/1284x2778/`
- `05_creators.png`: 「個人の発信を、静かに追う」。CREATORSの記事一覧。
- `06_choose_sources.png`: 「読みたい配信源だけ」。配信源を選択する設定画面。
- 2026-09-07のApple公開Lookupで、公開版1.1.1の画像に両ファイルを確認。公式サムネイルとローカル完成原本のコピー・UIを目視照合した。
- 画像内の小さな「無料・広告なし」は完成原本のまま保持。Lookupの価格0 JPYと公開概要の「広告はなく」に整合することを確認した。新たな価格コピーを本文へ追加していない。
- 出力: `static/images/apps/signal/store-{creators,sources}-{420,840}.webp`。420×909 / 840×1817、WebP quality 86。縦横比を維持し、画面内容の描き換え・生成・切り抜きはない。

出典・SHA-256・目視範囲は [screenshot-freshness.json](screenshot-freshness.json) を参照。

### オトミル

公開版1.0.1由来の古い画像から、**1.1.0「審査待ち」**の提出素材へ更新した。App Store Connectのログイン済みChrome画面を読取確認し、iPhone 6.5インチ / iPad 13インチ欄の4ファイル名を確認した。

`01_simple.png` / `02_standard_mode.png` / `03_plus_family.png` / `04_daily_offline.png`

iPhone欄のサムネイルのレイアウト・文字とローカル原本を目視照合している。提出ファイルのバイナリをダウンロードしてのチェックサム比較は実施していない。

| 用途 | 採用原本 | Web配信用 |
|---|---|---|
| Featured / Product 1枚目 | `tmp_appstore_screenshots/refresh_2026_09_05/final/iphone_1284x2778_candidates/01_simple.png` | `review-20260906-simple-{420,840}.webp` |
| Featured / Product 2枚目 | 同フォルダ `04_daily_offline.png` | `review-20260906-daily-offline-{420,840}.webp` |
| Hero | `tmp_appstore_screenshots/refresh_2026_09_05/raw/iphone/01_senior_home_free.png` | `review-20260906-home-{320,640}.webp` |

原本のプロジェクトルートは `/Users/yuya/Projects/oto_miru/`。1枚目は大きな用途選択ボタン、2枚目は会話の大きな字幕を示す。Heroも同じ新セットの制作に使用した実ホーム画面へ更新した。品質88のWebPへ比例縮小し、AI画像生成や画面内の文字変更は行っていない。`oto-assets.json` の全6出力SHAを現ファイルと照合し、01_simpleの420px版をquality 88 / effort 6で再生成すると同じSHAになることも確認した。quality 86では一致しない。

`docs/APP_STORE_METADATA.md`、制作README、CHANGELOGの更新日より、App Store Connectの実際の提出欄を優先した。ローカル文書に残る「未提出」は今回観測した状態と異なるため、提出の根拠には使わない。過去のAI素材や旧7枚セットは採用していない。サイトでは画像下に「審査提出中のバージョンの画面」と明記し、一般公開済みの画像と混同させない。

詳細は [oto-assets.json](oto-assets.json)。音声認識の精度を測定した証跡ではなく、実UIを使用した掲載素材の確認である。

### 他6アプリ

| アプリ | 公開情報・ローカル素材の照合 | 判断 |
|---|---|---|
| Uni:Note | 公開3.4.0の画像と `final_v7/SS01_handwriting.png` / `SS03_problem_set.png` が整合。既存採用原本と現行ファイルのSHA一致 | 維持 |
| Uni:Note Pocket | 公開3.4.0の画像と `final/SS01_review_now.png` / `SS02_import_backup.png` が整合。SHA一致 | 維持 |
| ギガポケ | 公開0.1.0と9/4審査修正版の01/02を照合。価格文字を修正した原本を採用済み | 維持。旧9/2提出版へ戻さない |
| ギャンカレ | 公開1.4.0の画像と9/3日本語完成版01/04が整合。SHA一致 | 維持 |
| すわなび | 公開1.1.1は7枚。最新ローカル素材はWatch追加の8枚版。Webで選択済みの01/03は既に最新8枚版で、原本SHAも一致 | 追加差し替えなし。Watch素材への置換や公開済みという主張は追加しない |
| Nocca | 公開Lookup0件。完成済みStoreマーケティング素材は見つからない。9/6の役割説明を含む実画面を使用 | 開発中表示と実UIを維持。Storeバッジ・国別リンクなし |

**未確認:** この6アプリについて、現在審査提出中の素材をApp Store Connectから独立して再取得する確認は完了していない。Chromeが「別の拡張機能UIがページ上で開いている」状態で自動操作を遮断し、すわなびの読取試行では読み込み画面以外を取得できなかった。公開ストアとローカルの制作記録の照合結果を、審査提出素材の直接確認結果に読み替えない。[other-submission-check.json](other-submission-check.json) に確認範囲と制約を記録している。

## 2. Apple公式バッジと配信地域

### バッジ

独自の「App Storeで見る」ボタンを、Apple公式マーケティングツール提供の黒背景SVGへ置き換えた。日本語・英語・韓国語・ドイツ語・フランス語・繁体字の6種類を取得し、サイト言語に応じて選ぶ。

取得元URL、原寸、SHA-256は [`data/app-store-badges.json`](../../data/app-store-badges.json)。SVG内部のロゴ、色、文字、比率は変更していない。表示高48px、幅auto、周囲12pxの余白とし、独自の角丸や着色を重ねない。[Apple公式マーケティングガイドライン](https://developer.apple.com/app-store/marketing/guidelines/)に従い、商標表記をFooterに掲載した。

適用範囲は、公開中7アプリのHome紹介とProduct詳細。Homeではアプリごとに1個、Product詳細では上部に1個とし、下部に同じバッジを繰り返さない。Noccaは公開が確認できないため非表示。

### 配信地域UI

「日本のApp Storeで提供中」を廃止し、「配信地域」と小さな国旗リンクに置き換えた。旗は44×44pxのタップ領域を持ち、`aria-label` / `title` とhover・focusの説明で国・地域名と遷移先を確認できる。

- `data/apps.json` の `availability.verifiedStorefronts` / `storefrontURLs` が配信地域とURLの正。
- 表示ラベル・国名は `data/ux/<language>.json`、バッジ言語は `data/app-store-badges.json` で別管理。
- 言語によるアプリの非表示やGeo-IP判定は実装していない。全言語に同じ8プロダクトを掲載する。
- 公式バッジのリンクは従来の確認済み日本Store URLを維持し、リンクのアクセシブルな説明で日本Storeであることを示す。他地域への入口は国旗で明示する。
- 国別URLはApple Lookupが返した `trackViewUrl` をそのまま採用。国コード置換によるURL推測はしていない。
- `coverage: partial` を維持。「確認できた配信地域」であり、世界の完全な配信地域一覧ではない。未確認地域を未配信と断定しない。

2026-09-07に日本・米国・台湾・フランス・韓国・ドイツを照合し、**21 URL**でHTTP 200、対象アプリID、地域、canonical/OG URLを確認した。根拠は [storefront-verification.json](storefront-verification.json)。

| アプリ | 確認地域 | 採用した公式URL | 確認 |
|---|---|---|---|
| Uni:Note | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/uni-note-%E6%9B%B8%E3%81%84%E3%81%A6%E5%AD%A6%E3%81%B6-%E5%BA%83%E5%91%8A%E7%84%A1%E3%81%97%E3%81%AE%E5%A4%A7%E5%AD%A6%E3%83%8E%E3%83%BC%E3%83%88/id6760258084?uo=4) | 200・同一アプリ/地域 |
| Uni:Note | 🇺🇸 米国 (`us`) | [App Store](https://apps.apple.com/us/app/uni-note-study-notes/id6760258084?uo=4) | 200・同一アプリ/地域 |
| Uni:Note | 🇹🇼 台湾 (`tw`) | [App Store](https://apps.apple.com/tw/app/uni-note-%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98/id6760258084?uo=4) | 200・同一アプリ/地域 |
| Uni:Note | 🇫🇷 フランス (`fr`) | [App Store](https://apps.apple.com/fr/app/uni-note-notes-de-r%C3%A9vision/id6760258084?uo=4) | 200・同一アプリ/地域 |
| Uni:Note | 🇰🇷 韓国 (`kr`) | [App Store](https://apps.apple.com/kr/app/uni-note-%EA%B3%B5%EB%B6%80-%EB%85%B8%ED%8A%B8/id6760258084?uo=4) | 200・同一アプリ/地域 |
| Uni:Note | 🇩🇪 ドイツ (`de`) | [App Store](https://apps.apple.com/de/app/uni-note-lernnotizen/id6760258084?uo=4) | 200・同一アプリ/地域 |
| オトミル | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/%E3%82%AA%E3%83%88%E3%83%9F%E3%83%AB-%E8%81%9E%E3%81%93%E3%81%88%E3%82%92%E5%AD%97%E5%B9%95%E3%81%A7%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88/id6770774613?uo=4) | 200・同一アプリ/地域 |
| ギガポケ | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/%E3%82%AE%E3%82%AC%E3%83%9D%E3%82%B1-povo%E7%89%B9%E5%85%B8%E3%82%B3%E3%83%BC%E3%83%89%E7%AE%A1%E7%90%86/id6807501268?uo=4) | 200・同一アプリ/地域 |
| Uni:Note Pocket | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/uni-note-pocket/id6761449487?uo=4) | 200・同一アプリ/地域 |
| Uni:Note Pocket | 🇺🇸 米国 (`us`) | [App Store](https://apps.apple.com/us/app/uni-note-pocket/id6761449487?uo=4) | 200・同一アプリ/地域 |
| Uni:Note Pocket | 🇹🇼 台湾 (`tw`) | [App Store](https://apps.apple.com/tw/app/uni-note-pocket/id6761449487?uo=4) | 200・同一アプリ/地域 |
| Uni:Note Pocket | 🇫🇷 フランス (`fr`) | [App Store](https://apps.apple.com/fr/app/uni-note-pocket/id6761449487?uo=4) | 200・同一アプリ/地域 |
| Uni:Note Pocket | 🇰🇷 韓国 (`kr`) | [App Store](https://apps.apple.com/kr/app/uni-note-pocket/id6761449487?uo=4) | 200・同一アプリ/地域 |
| Uni:Note Pocket | 🇩🇪 ドイツ (`de`) | [App Store](https://apps.apple.com/de/app/uni-note-pocket/id6761449487?uo=4) | 200・同一アプリ/地域 |
| ギャンカレ | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/%E3%82%AE%E3%83%A3%E3%83%B3%E3%82%AB%E3%83%AC-3%E7%A7%92%E3%81%A7%E8%A8%98%E9%8C%B2%E3%81%A7%E3%81%8D%E3%82%8B%E5%8F%8E%E6%94%AF%E7%AE%A1%E7%90%86/id6757731648?uo=4) | 200・同一アプリ/地域 |
| ギャンカレ | 🇺🇸 米国 (`us`) | [App Store](https://apps.apple.com/us/app/balance-calendar/id6757731648?uo=4) | 200・同一アプリ/地域 |
| すわなび | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/%E3%81%99%E3%82%8F%E3%81%AA%E3%81%B3-%E3%81%9F%E3%81%B0%E3%81%93%E3%82%AB%E3%82%A6%E3%83%B3%E3%82%BF%E3%83%BC/id6760842941?uo=4) | 200・同一アプリ/地域 |
| すわなび | 🇹🇼 台湾 (`tw`) | [App Store](https://apps.apple.com/tw/app/smokeless-%E6%88%92%E8%8F%B8%E8%A8%88%E6%95%B8%E5%99%A8/id6760842941?uo=4) | 200・同一アプリ/地域 |
| すわなび | 🇫🇷 フランス (`fr`) | [App Store](https://apps.apple.com/fr/app/smokeless-compteur-tabac/id6760842941?uo=4) | 200・同一アプリ/地域 |
| すわなび | 🇰🇷 韓国 (`kr`) | [App Store](https://apps.apple.com/kr/app/smokeless-%EA%B8%88%EC%97%B0-%EC%B9%B4%EC%9A%B4%ED%84%B0/id6760842941?uo=4) | 200・同一アプリ/地域 |
| SIGNAL | 🇯🇵 日本 (`jp`) | [App Store](https://apps.apple.com/jp/app/signal-%E5%80%8B%E4%BA%BA%E7%99%BA%E4%BF%A1%E3%82%92%E8%BF%BD%E3%81%86%E3%83%8B%E3%83%A5%E3%83%BC%E3%82%B9%E3%82%A2%E3%83%97%E3%83%AA/id6759493613?uo=4) | 200・同一アプリ/地域 |

Noccaは0地域・リンクなし。日本語表示だから日本専用、英語表示だから米国向けとは扱わない。

## 3. CTAとサポート遷移の整理

| 発見した冗長性 | 変更後 |
|---|---|
| Product上部の「サポートを見る」と同ページ下部のSupportが重複 | 上部Support CTAを削除。上部は公式Storeバッジと配信地域に絞る |
| 特定アプリからSupport一覧へ進み、アプリを再選択する | Product下部から既存の使い方・FAQ・Privacyへ直接リンク。お問い合わせはアプリ名入り件名のメールを直接開く |
| Product詳細に「詳しく見る」を表示しうる共通CTA | `.product` では表示しない。Home側だけ詳細リンクを残す |
| Homeの特定アプリSupportショートカットがSupport一覧内へ遷移 | `/products/<id>/#support` に変更。対象ProductのSupportへ直接到達 |
| 既存の使い方・FAQ・Privacy・Termsから別情報を探すため一覧へ戻る | 上部パンくずは対象Productの `#support`。下部に同一アプリの関連情報とProductリンクを配置 |
| 現在開いているPrivacy等へ下部リストから再リンク | `currentPage` のURLと照合し、自ページの項目を省略 |
| FooterにHeaderと同じナビやPrivacy一覧が並ぶ | ブランド表記、Contact、Copyright、必要なApple商標表記に整理 |
| Companyの問い合わせ操作が分かれやすい | ContactのPrimaryはメール。Support一覧は補助テキストリンク |

Product下部の `id="support"` 内は、使い方／よくある質問／お問い合わせ／プライバシーポリシーの小さなリスト。使い方・FAQ・お問い合わせには短い説明を添えた。利用規約は独立した補助リンクとし、PrivacyをPrimary CTAにしない。翻訳のない既存ページは日本語への直接リンクと注記を維持する。

**上部Supportボタンを別のページ内ボタンへ置換して増やしてはいない。** 上部から削除したうえで、Homeのアプリ別Support入口と既存サポート記事のパンくずに `#support` を使用した。Products一覧・Headerから入る共通Supportトップは維持している。

実装: `layouts/_partials/app-cta.html`、`support-links.html`、`layouts/product/single.html`、`layouts/single.html`、`layouts/home.html`、`layouts/company/list.html`、`assets/css/site.css`。

## 4. Newsの3分類

日付・カテゴリ・タイトルの一覧性と降順表示を維持し、絞り込み用の追加画面やJSは増やしていない。Homeの最新3件、News一覧、既存Notes一覧、個別記事の見出し・パンくず、Article構造化データで同じ分類を使う。

| raw category | 表示名 | 対象 | 件数 |
|---|---|---|---:|
| `press-release` | Press Release | 正式な製品紹介・発表 | 8 |
| `blog` | Blog | 開発・運営の記録、考え方、振り返り | 7 |
| `information` | Information | 利用者向けのお知らせ | 0 |

Informationに該当する記事を作るためのダミー告知は追加していない。ギャンカレの初回紹介とNocca紹介はInformationからPress Releaseへ変更。Noccaの「開発中」という本文とStore非表示は維持し、カテゴリ変更で公開済みと誤認させない。

タイトルはアプリの正式名＋「について」へ統一し、必要だった次の3本だけを変更した。

| 旧タイトル | 新タイトル |
|---|---|
| はじめに：自己紹介とこのアプリを作った理由 | ギャンカレについて |
| Uni:Note Pocket を作りました | Uni:Note Pocketについて |
| オトミルを作りました | オトミルについて |

ほかの正式アプリ紹介5本は既に希望の形式だったため維持。**全15記事の本文、日付、URL、title以外のfront matterは変更していない。** 各本文のSHAと分類理由は [news-audit.json](news-audit.json) に記録した。

| 公開日（front matter） | 分類 | 記事と維持したURL |
|---|---|---|
| 2026-09-06 | Press Release | [Noccaについて](https://kumakikai.github.io/notes/2026-09-06-nocca/) |
| 2026-09-02 | Press Release | [ギガポケについて](https://kumakikai.github.io/notes/2026-09-02-giga-poke/) |
| 2026-05-26 | Blog | [Android版アプリ公開の壁が思った以上に高かった](https://kumakikai.github.io/notes/2026-05-26-android-release/) |
| 2026-05-19 | Press Release | [オトミルについて](https://kumakikai.github.io/notes/2026-05-19-oto-miru/) |
| 2026-04-12 | Blog | [アプリ開発を始めてからの累計収益が1万円を超えました](https://kumakikai.github.io/notes/2026-04-12-uni-note-10000/) |
| 2026-04-01 | Press Release | [Uni:Note Pocketについて](https://kumakikai.github.io/notes/2026-04-01-uni-note-pocket/) |
| 2026-03-25 | Blog | [最近、友人にアプリ開発の悩みを相談しました](https://kumakikai.github.io/notes/2026-03-25-blog/) |
| 2026-03-21 | Press Release | [すわなびについて](https://kumakikai.github.io/notes/2026-03-21-smokeless/) |
| 2026-03-13 | Blog | [赤字でも、まだ作り続けている](https://kumakikai.github.io/notes/2026-03-13-blog/) |
| 2026-03-12 | Press Release | [Uni:Noteについて](https://kumakikai.github.io/notes/2026-03-12-uni-note/) |
| 2026-02-22 | Press Release | [SIGNALについて](https://kumakikai.github.io/notes/2026-02-22-signal/) |
| 2026-02-14 | Blog | [リリースから1ヶ月。DLが伸びない中で考えたこと](https://kumakikai.github.io/notes/2026-02-14-blog/) |
| 2026-01-27 | Blog | [思想](https://kumakikai.github.io/notes/2026-01-27-philosophy/) |
| 2026-01-23 | Blog | [ギャンカレの今後について（ロードマップ）](https://kumakikai.github.io/notes/2026-01-26-roadmap/) |
| 2026-01-23 | Press Release | [ギャンカレについて](https://kumakikai.github.io/notes/2026-01-23-introduction/) |

`2026-01-26-roadmap` のfront matterは従来どおり2026-01-23。ファイル名に合わせた日付の修正はしていない。

分類の一元管理は `data/news.json`。新しい記事ではfront matterの `news_category` / `related_products` を優先できる。`layouts/_partials/news-category.html` が `id` と `label` を返し、6言語でPress Release / Blog / Informationという表記を統一する。Newsのintroとmeta descriptionには開発・運営のブログを含めた。

## 5. Privacy・Footer・既存URLの維持

Privacyの全件一覧を通常のサイト導線から外した。アプリ別のPrivacy本文やURLを統合したわけではない。Product／Support／既存サポート記事から、そのアプリ固有のPrivacyへ直接到達できる。

互換用に次の6 URLをそのまま生成し、簡潔な「アプリ別サポートから確認できる」案内とSupportリンクを残している。

- `/privacy/`
- `/en/privacy/`
- `/ko/privacy/`
- `/de/privacy/`
- `/zh-hant/privacy/`
- `/fr/privacy/`

旧ページ送りの `/privacy/page/1/`、`/privacy/page/2/`、`/privacy/page/3/` と、5翻訳の `/LANG/privacy/page/1/` も出力を保持。ページ1の既存aliasを含め、404へ落ちない構成を維持する。Privacy一覧・ページ送りは `noindex, follow` とし、Header／Footerの一覧リンクや不要な再一覧を出さない。

FooterではKUMAKIKAIのブランド表記に加え、Contact、Copyright、公式バッジ利用に伴うAppleの商標表記だけを残した。HeaderのProducts / Support / News / Companyは従来どおり利用できる。

App Store Connect登録済み、または登録されている可能性のあるSupport／Marketing／Privacy／Press Releaseの既存正式URLは移動していない。今回新設した公開ページURLやredirectはない。既存の53 aliasと138直接URLの対応は移行前の監査基準を維持する。全一覧は [恒久URL監査](../migration/permanent-urls.md) と [baseline](../migration/baseline.json) を参照。

### 個別Privacy Policyの公開確認

以下の30 URL（本文22件・既存alias 8件）は同じURLでHTTP 200、現行ビルドのHTMLとSHA-256が一致した。既存aliasは従来の正式Privacyへ到達することも静的検証済み。Privacy本文の変更・削除、新たなalias/redirectはない。

| 維持したURL | HTTP | 内容一致 |
|---|---:|---|
| [/de/privacy/uni-memo/](https://kumakikai.github.io/de/privacy/uni-memo/) | 200 | 既存alias・SHA-256一致 |
| [/de/privacy/uni-note/](https://kumakikai.github.io/de/privacy/uni-note/) | 200 | SHA-256一致 |
| [/de/privacy/uni-note-pocket/](https://kumakikai.github.io/de/privacy/uni-note-pocket/) | 200 | SHA-256一致 |
| [/en/privacy/smokeless/](https://kumakikai.github.io/en/privacy/smokeless/) | 200 | SHA-256一致 |
| [/en/privacy/uni-memo/](https://kumakikai.github.io/en/privacy/uni-memo/) | 200 | 既存alias・SHA-256一致 |
| [/en/privacy/uni-note/](https://kumakikai.github.io/en/privacy/uni-note/) | 200 | SHA-256一致 |
| [/en/privacy/uni-note-pocket/](https://kumakikai.github.io/en/privacy/uni-note-pocket/) | 200 | SHA-256一致 |
| [/fr/privacy/smokeless/](https://kumakikai.github.io/fr/privacy/smokeless/) | 200 | SHA-256一致 |
| [/fr/privacy/uni-memo/](https://kumakikai.github.io/fr/privacy/uni-memo/) | 200 | 既存alias・SHA-256一致 |
| [/fr/privacy/uni-note/](https://kumakikai.github.io/fr/privacy/uni-note/) | 200 | SHA-256一致 |
| [/fr/privacy/uni-note-pocket/](https://kumakikai.github.io/fr/privacy/uni-note-pocket/) | 200 | SHA-256一致 |
| [/ko/privacy/smokeless/](https://kumakikai.github.io/ko/privacy/smokeless/) | 200 | SHA-256一致 |
| [/ko/privacy/uni-memo/](https://kumakikai.github.io/ko/privacy/uni-memo/) | 200 | 既存alias・SHA-256一致 |
| [/ko/privacy/uni-note/](https://kumakikai.github.io/ko/privacy/uni-note/) | 200 | SHA-256一致 |
| [/ko/privacy/uni-note-pocket/](https://kumakikai.github.io/ko/privacy/uni-note-pocket/) | 200 | SHA-256一致 |
| [/privacy/balance-calendar/](https://kumakikai.github.io/privacy/balance-calendar/) | 200 | SHA-256一致 |
| [/privacy/giga-poke/](https://kumakikai.github.io/privacy/giga-poke/) | 200 | SHA-256一致 |
| [/privacy/nocca/](https://kumakikai.github.io/privacy/nocca/) | 200 | SHA-256一致 |
| [/privacy/oto-miru/](https://kumakikai.github.io/privacy/oto-miru/) | 200 | SHA-256一致 |
| [/privacy/povo-manager/](https://kumakikai.github.io/privacy/povo-manager/) | 200 | 既存alias・SHA-256一致 |
| [/privacy/signal/](https://kumakikai.github.io/privacy/signal/) | 200 | SHA-256一致 |
| [/privacy/smoke-less/](https://kumakikai.github.io/privacy/smoke-less/) | 200 | 既存alias・SHA-256一致 |
| [/privacy/smokeless/](https://kumakikai.github.io/privacy/smokeless/) | 200 | SHA-256一致 |
| [/privacy/uni-memo/](https://kumakikai.github.io/privacy/uni-memo/) | 200 | 既存alias・SHA-256一致 |
| [/privacy/uni-note/](https://kumakikai.github.io/privacy/uni-note/) | 200 | SHA-256一致 |
| [/privacy/uni-note-pocket/](https://kumakikai.github.io/privacy/uni-note-pocket/) | 200 | SHA-256一致 |
| [/zh-hant/privacy/smokeless/](https://kumakikai.github.io/zh-hant/privacy/smokeless/) | 200 | SHA-256一致 |
| [/zh-hant/privacy/uni-memo/](https://kumakikai.github.io/zh-hant/privacy/uni-memo/) | 200 | 既存alias・SHA-256一致 |
| [/zh-hant/privacy/uni-note/](https://kumakikai.github.io/zh-hant/privacy/uni-note/) | 200 | SHA-256一致 |
| [/zh-hant/privacy/uni-note-pocket/](https://kumakikai.github.io/zh-hant/privacy/uni-note-pocket/) | 200 | SHA-256一致 |

## 6. 検証結果

### 確認済みの静的検証

`/private/tmp/cta-migration-verification.json` のproduction生成物に対する結果は `ok: true`、warnings 0、errors 0。

| 項目 | 結果 |
|---|---:|
| 移行前HTML URL | 191保持 |
| 恒久直接URL / 既存alias | 138 / 53保持 |
| 既存記事の本文・アンカー・リンク | 84記事保持 |
| 内部リンク・画像・アンカー参照 | 9,783参照成功 |
| 公式バッジ / 配信地域URL | 6素材 / 21 URL |
| 公開アプリの公式バッジ | Home・Product合計84箇所 |
| 国別Storeリンク | 252箇所 |
| 固定プロダクトコピー | 126項目保持 |
| Product詳細 | 8アプリ×6言語＝48ページ |
| アプリが特定済みの直接Supportリンク | 162件 |
| Privacy互換案内 / News分類 | 各6言語 |
| HTML / SEO・構造化データ | 277 / 204ページ |
| sitemap | 200項目 |

ローカルの生成・リンク検証と、公開環境のHTTP確認を別工程で実施した。ローカル詳細は [verification.json](verification.json)、公開URL別の結果は [public-verification.json](public-verification.json)。

### 最終確認

- Production build: Hugo 0.158.0 Extendedで `npm run build` 成功、警告なし。`npm run verify` も errors 0 / warnings 0。実行時に `HUGO_CACHEDIR=/private/tmp/kumakikai-hugoplate-cache` と `HUGO_BINARY=/private/tmp/kumakikai-hugo-0.158.0/Payload/hugo` を指定した。
- Desktop / iPad / Mobile、Light / Dark: **54ケース成功**。`artifacts/ux/browser/results.json` は `ok: true`、`cases: 54`、`interactions: passed`、`failures: []`。1440 / 1280 / 834 / 393 / 320px、8 Product、6言語、Home / News / Support / Privacy等を含む。
- キーボード、折りたたみ、国旗リンク、no-JS、横はみ出し: 追加操作検証成功。各画面の画像・見出し階層・重複ID・コンソールエラー・axe違反も検査し、失敗なし。
- 公開GitHub Pages: 実装修正 `eaffb5d` をmainへpushし、[Hugo CI](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34046941737) と [Pages公開](https://github.com/kumakikai/kumakikai.github.io/actions/runs/34046954589) が成功。2026-09-07 01:56 JST、277 HTML URLすべてがHTTP 200でローカル生成物のSHA-256と一致。画像・公式バッジ・CSS・JSの18ファイルもHTTP 200・SHA一致。全URLと結果は [public-verification.json](public-verification.json)。
- Lighthouse 12.8.2: 今回のproduction生成物をローカルChromeのモバイル模擬条件で測定。Home 99 / 100 / 100 / 100、Uni:Note 100 / 100 / 100 / 100（Performance / Accessibility / Best Practices / SEO）。LCPはHome 2.3 s、Uni:Note 1.5 s、CLSは双方0、run warningsなし。実利用者やモバイル回線のフィールド測定とは区別する。

## 7. 実ページのスクリーンショット

最終production buildをChromeで開き、Desktop 1440px / Mobile 393pxの実画面を保存・目視確認した。Newsの日付・分類・タイトル、FooterのContact単独ナビ、Productの公式バッジと国旗、モバイルの自然な縦積みを確認済み。画像はWebPへ圧縮している。

| 画面 | Desktop | Mobile |
|---|---|---|
| Home | [home-desktop.webp](screenshots/home-desktop.webp) | [home-mobile.webp](screenshots/home-mobile.webp) |
| Uni:Note Product | [uninote-desktop.webp](screenshots/uninote-desktop.webp) | [uninote-mobile.webp](screenshots/uninote-mobile.webp) |
| News | [news-desktop.webp](screenshots/news-desktop.webp) | [news-mobile.webp](screenshots/news-mobile.webp) |
| Footer | [footer-desktop.webp](screenshots/footer-desktop.webp) | [footer-mobile.webp](screenshots/footer-mobile.webp) |

## 8. 残る制約

- オトミルの審査提出欄は直接確認済みだが、公開版は確認時点で1.0.1。1.1.0を公開済みとは表示していない。
- 他6アプリの審査提出素材の直接再確認はChromeの拡張機能UIによる遮断で未完了。現在公開・ローカル制作の照合結果と区別する。
- Noccaには正式なStoreマーケティング画像がない。開発画面と開発中の注記を継続する。
- 配信地域は確認済みサンプルの21 URLであり、全世界の配信設定を網羅する監査ではない。
- 日本語の実スクリーンショットを6言語共通で使用し、日本語以外ではその旨の注記を維持する。
- 既存記事・Privacy本文の歴史的記述を書き換える作業は行っていない。News分類や素材刷新を理由に既存App Store関連ページを別URLへ移していない。

## 9. 主な変更ファイル

- データ: `data/apps.json`、`data/hero.json`、`data/app-store-badges.json`、`data/ux/*.json`、`data/home/*.json`、`data/corporate/*.json`、`data/news.json`
- CTA / Support: `layouts/_partials/app-cta.html`、`app-screenshots.html`、`support-links.html`、`layouts/product/single.html`、`layouts/single.html`、`layouts/home.html`
- News / Privacy / Footer / SEO: `layouts/_partials/news-category.html`、`news-items.html`、`layouts/list.html`、`layouts/_partials/essentials/{head,footer}.html`、`layouts/company/list.html`
- 記事: タイトルだけ変更した `content/notes/2026-01-23-introduction.md`、`2026-04-01-uni-note-pocket.md`、`2026-05-19-oto-miru.md`
- News一覧meta: `content/news/_index*.md`（共有データから生成）
- 表示 / 検証: `assets/css/site.css`、`scripts/verify-migration.py`、`scripts/verify-browser.cjs`
- 素材: `static/images/apps/{oto-miru,signal}/`、`static/images/badges/`
- 根拠: 本ディレクトリのJSON監査記録とスクリーンショット
