# Productsへのアプリ選択ハブ統合

監査日: 2026-09-07。変更前の基準コミット: `9adadb9a47ea38ffb45deba22ac0100bd20f6397`。

Productsを、アプリを選ぶ唯一の通常導線とする。製品を知りたい場合も、使っているアプリで困った場合も、同じProductsカードから目的の場所へ進める構成へ整理する。前回の素材・CTA・News修正は [前回のUX報告](../ux/REPORT.md) に履歴として残し、本報告とは区別する。

**状態:** 実装・production build・静的検証・ブラウザ64画面を確認済み。最終見出し調整後のProducts10画面の再検証も成功。公開後HTTP確認は末尾へ記録する。

## 1. Products一覧の変更

アプリを選ぶ一覧を `/products/` と5翻訳の同一覧へ集約する。8アプリ、公開中／開発中、アイコン・短い説明・プラットフォームを維持し、各カードで「製品を見る」「サポート」の目的を選べるようにする。

- 日本語: `/products/`
- 英語: `/en/products/`
- 韓国語: `/ko/products/`
- ドイツ語: `/de/products/`
- 繁体字: `/zh-hant/products/`
- フランス語: `/fr/products/`

言語とApp Store配信地域は引き続き別管理。どの言語でも同じ8アプリを表示し、配信地域、正式バッジ、Noccaの開発中表示、素材の出典は前回修正を維持する。

## 2. 各カードのSupport導線

| カード | 製品を見る | サポート |
|---|---|---|
| Uni:Note | `/products/uni-note/` | `/products/uni-note/#support` |
| オトミル | `/products/oto-miru/` | `/products/oto-miru/#support` |
| ギガポケ | `/products/giga-poke/` | `/products/giga-poke/#support` |
| Nocca | `/products/nocca/` | `/products/nocca/#support` |
| Uni:Note Pocket | `/products/uni-note-pocket/` | `/products/uni-note-pocket/#support` |
| ギャンカレ | `/products/balance-calendar/` | `/products/balance-calendar/#support` |
| すわなび | `/products/smokeless/` | `/products/smokeless/#support` |
| SIGNAL | `/products/signal/` | `/products/signal/#support` |

5翻訳も同じパスの前に対応言語を付ける。サポートは該当Productの下部へ直接スクロールする。総合Supportページで同じアプリを選び直す操作は挟まない。カードの2リンクは別々の通常の`a`要素とし、アイコンやカード全体をクリックした後に再選択させる構造を作らない。

## 3. HeaderからSupportを削除

DesktopとMobileのグローバルナビを **Products / News / Company** に揃える。総合Supportを常設メニューから外し、Productsを製品紹介とサポートの共通入口にする。

HeaderのKUMAKIKAI、言語切替、Light / Dark、モバイルメニューは維持。FAQ・使い方・Privacy等を閲覧中も、そのアプリがProductsに属することが自然に分かる状態を目指す。

## 4. `/support/` の最終的な扱い

### 公開前監査で確認したこと

変更前の公開サイトで `/support/`、`/en/support/`、`/ko/support/`、`/de/support/`、`/zh-hant/support/`、`/fr/support/` はすべて **HTTP 200・自己canonical**。8アプリのサポートカードと問い合わせセクションを表示していた。

公開済みHTMLには、各アプリの `#<app-id>`、見出し側の `#support-<app-id>`、`#contact` が存在する。外部のブックマークや過去のリンクから到達する可能性があるため、通常ナビから外すこととURLを削除することを区別する。

### 互換ページ

既存6 URLは削除・別URLへの自動転送をせず、**HTTP 200・自己canonical・`noindex, follow`** の簡潔なProducts案内として保持する。全アプリカードを並べる総合Supportハブは表示しない。

既存のアプリ別fragmentが指定された場合は、CSSの`:target`による該当アプリの案内だけを表示し、`/products/<app-id>/#support` へ直接進めるようにする。`#contact` の場合はメール導線を表示する。アプリが特定済みの古いリンクを、Products一覧での再選択へ戻さない。

実際の外部からの参照・ブックマーク利用は未確認。リポジトリ内に参照が見つからないことを、App Store Connect等に登録されていない証明として扱わない。今回App Store Connect登録値の変更・削除は行わない。

## 5. アプリ固有URLの維持

Product内の`#support`と、既存の使い方・FAQ・Privacy・Terms・製品発表記事は役割が異なる。入口の統合を理由に個別ページを移動しない。**`content/htu/`、`content/faq/`、`content/privacy/`、`content/terms/`、`content/notes/` の個別84 Markdownについて、変更前のファイルSHAを監査基準として保持する。**

| アプリ | 使い方 | FAQ | Privacy | Terms |
|---|---|---|---|---|
| Uni:Note | [使い方](https://kumakikai.github.io/htu/uni-note/) | [FAQ](https://kumakikai.github.io/faq/uni-note/) | [Privacy](https://kumakikai.github.io/privacy/uni-note/) | 既存の個別Termsなし |
| オトミル | [使い方](https://kumakikai.github.io/htu/oto-miru/) | [FAQ](https://kumakikai.github.io/faq/oto-miru/) | [Privacy](https://kumakikai.github.io/privacy/oto-miru/) | [Terms](https://kumakikai.github.io/terms/oto-miru/) |
| ギガポケ | [使い方](https://kumakikai.github.io/htu/giga-poke/) | [FAQ](https://kumakikai.github.io/faq/giga-poke/) | [Privacy](https://kumakikai.github.io/privacy/giga-poke/) | [Terms](https://kumakikai.github.io/terms/giga-poke/) |
| Nocca | [使い方](https://kumakikai.github.io/htu/nocca/) | [FAQ](https://kumakikai.github.io/faq/nocca/) | [Privacy](https://kumakikai.github.io/privacy/nocca/) | [Terms](https://kumakikai.github.io/terms/nocca/) |
| Uni:Note Pocket | [使い方](https://kumakikai.github.io/htu/uni-note-pocket/) | [FAQ](https://kumakikai.github.io/faq/uni-note-pocket/) | [Privacy](https://kumakikai.github.io/privacy/uni-note-pocket/) | 既存の個別Termsなし |
| ギャンカレ | [使い方](https://kumakikai.github.io/htu/balance-calendar/) | [FAQ](https://kumakikai.github.io/faq/balance-calendar/) | [Privacy](https://kumakikai.github.io/privacy/balance-calendar/) | 既存の個別Termsなし |
| すわなび | [使い方](https://kumakikai.github.io/htu/smokeless/) | [FAQ](https://kumakikai.github.io/faq/smokeless/) | [Privacy](https://kumakikai.github.io/privacy/smokeless/) | 既存の個別Termsなし |
| SIGNAL | [使い方](https://kumakikai.github.io/htu/signal/) | [FAQ](https://kumakikai.github.io/faq/signal/) | [Privacy](https://kumakikai.github.io/privacy/signal/) | 既存の個別Termsなし |

上記は日本語の正式URL。既存翻訳のあるURLもそのまま保持する。翻訳のないページへ新しい架空URLは作らず、日本語への直接リンクを使う。

互換aliasも維持する。例: Pocketの `/htu/uni-memo/`・`/faq/uni-memo/`・`/privacy/uni-memo/`、すわなびの `/htu/smoke-less/`・`/privacy/smoke-less/`、ギガポケの `povo-manager` 名の各旧URL。既存の正式ページをaliasへ置換することはしない。

既存のApp Store関連情報として確認している例:

- オトミルのSupport: `https://kumakikai.github.io/notes/2026-05-19-oto-miru/`。前回のApp Store Connect読取記録で確認済み。MarketingのトップURLも維持。
- NoccaのSupport: `https://kumakikai.github.io/notes/2026-09-06-nocca/`。9/6の登録読戻し記録がある。今回ASCの現在値を再取得したわけではない。
- ギガポケのFAQ・Privacy・使い方・TermsとGoogle Formsには関連リポジトリからの参照がある。FAQ URLとフォームURLのどちらが現在のASC登録値かは未確認のため、両方の既存導線を保持する。
- [お問い合わせフォーム](https://forms.gle/Enzmm94LdXRZjP8k9)は既存のギガポケ/Nocca記事やポリシーから参照される外部サービス。リンクを変更せず、フォーム内容や送信先にも手を加えない。
- `mailto:kumakikai.apps@gmail.com`、全15件の`/notes/.../`記事URL、各アプリのApp Store URLを保持。

恒久URL一覧と過去の取得時点は [permanent-urls.json](../migration/permanent-urls.json)、直前の公開確認は [前回公開検証](../ux/public-verification.json) を参照。過去の登録記録と今回の生確認を混同しない。

## 6. Productから総合Supportを経由していた箇所

前回修正の時点で、Product上部の「サポートを見る」は既に削除済み。Product下部には使い方・FAQ・お問い合わせ・Privacyと任意のTermsがあり、対象アプリの情報へ直接移動できていた。その改善を戻さない。

今回の残存問題は、アプリ選択入口がProductsとSupportに分かれ、Header・Home・Company・404・Privacy互換案内から総合Supportを再度開けた点。共通テンプレートでアプリを識別できない記事のパンくずにも総合Supportへのfallbackが残っていた。

ProductsカードのSupportリンク追加と、残存する総合Supportへの通常リンクの整理で、既にアプリが分かっている利用者が一覧を重ねて辿る必要をなくす。

## 7. 直接導線の修正

- Productsカード → 対象Productの`#support`。
- Productの`#support` → 対象の使い方・FAQ・Privacy・Terms・メール。
- 使い方・FAQ・Privacy・Terms → 同じアプリの関連情報とProduct。
- 古い`/support/#<app-id>` → 対象Productの`#support`への個別案内。
- 旧`/support/#contact` → メール。
- アプリ未特定の一般案内 → Products。

CompanyのContactはメールをPrimaryとし、アプリの情報を探す補助リンクをProductsへ揃える。404もトップまたはProductsへ戻れる構成とし、廃止した総合Supportを復活させない。

## 8. Homeの重複Supportセクションを削除

Home下部の総合Support紹介とFeatured4アプリのSupportショートカットを削除する。Hero、Featured / Other、各アプリの公式Storeバッジと製品詳細、News、Aboutは維持する。

Homeから「使っているアプリのサポートを探す」場合の入口はHeaderのProducts。製品詳細を閲覧した場合は、そのページ下部のSupportを使う。全アプリの再選択用カードをHome下部へ追加しない。

以前公開されていたHomeの`#support`への外部ブックマークの利用は未確認。互換性のため、このIDをHeroのProducts CTAへ移し、同じURLからアプリ選択へ進める状態を保持した。Support専用セクションは追加していない。

## 9. その他の重複ハブ監査

| 対象 | 監査で確認した状態 | 今回の扱い |
|---|---|---|
| `/htu/`・`/faq/` | `_index.md`の手動アプリ一覧とPaginatorの自動一覧が重なり、同じ個別URLが二度出る場合がある | 個別記事を維持し、旧一覧はProducts案内の互換ページへ整理 |
| `/terms/` | 手動一覧と自動一覧の両方に同じ3アプリのTermsが出る | 個別Termsを維持し、旧一覧はProducts案内へ整理 |
| `/privacy/` | 前回から互換案内だが、遷移先がSupport一覧 | Productsへ変更。6言語と旧ページ送りのURLを維持 |
| `/support/` | Productsと同じアプリを選択する全件カード一覧 | 通常ハブとして廃止し、URL・fragment互換のみ保持 |
| Contact | 独立したアプリ選択画面はない。Footer→Company#contact→メール | 維持。追加のContactハブや問い合わせ前の再選択を作らない |
| Newsカテゴリ | Press Release / Blog / Informationは同じNews一覧上のラベル | 維持。分類ごとの選択画面・新しいハブは追加しない |
| 旧`/notes/`とページ送り | News移行前の公開URL。正式な既存記事への導線がある | URL互換のため保持し、HeaderはNewsへ統一 |
| Footer | ブランド、Contact、Copyright、Apple商標表記 | 維持。ProductsやSupportのアプリ一覧を追加しない |
| Home | Featured / Otherに続き別Supportカード群があった | Support群を削除し、製品の紹介としてのFeatured / Otherを維持 |

`/htu/`・`/faq/`・`/privacy/`・`/terms/`の互換案内は自己canonical、`noindex, follow`とし、従来のページ送り出力も保持する。個別ページの本文やリンクを書き換えて一覧を廃止するのではなく、一覧テンプレート側で重複したアプリ選択UIを出さないようにする。

## 10. Desktop版Productsのスクリーンショット

保存先: [products-desktop.webp](screenshots/products-desktop.webp)

Desktop 1440px / 1280pxは3列、iPad 834pxは2列。実画面を撮影して、8カードの製品/Supportリンクの区別と文字の折り返しを確認した。[Dark版](screenshots/products-desktop-dark.webp)も保存済み。

## 11. Mobile版Productsのスクリーンショット

保存先: [products-mobile.webp](screenshots/products-mobile.webp)

Mobile 393px / 320pxは1列。リンクは最小44px高、折り返し可能な2導線に限定。日本語の見出しは既存コピーを維持し、意味のまとまりで折り返して「アプリ」が途中で分断されないようにした。[Mobile先頭画面](screenshots/products-mobile-viewport.webp)と[Dark版](screenshots/products-mobile-dark.webp)も保存済み。

## 12. 最終ナビゲーション

**KUMAKIKAI / Products / News / Company**

- Products: アプリ選択、製品紹介、各アプリのサポート。
- News: 製品発表・開発ブログ・お知らせ。
- Company: KUMAKIKAIと一般のお問い合わせ。
- Footer: Contact。CopyrightとApple商標表記を併記。

総合Supportへの常設メニューは置かない。各Productの`#support`と既存の個別サポート/法務URLは維持する。

### 最終検証・公開結果の追記欄

<!-- HUB_FINAL_VERIFICATION_PENDING: 実装確認・build・ブラウザ・公開HTTPは完了した証拠だけを追記する。 -->

- 変更前の公開読取: Support6言語とHome / Products / Company / 旧各一覧 / News / Notesの計15 URLでHTTP 200。Support全言語の旧アプリ・見出し・Contact fragmentと自己canonicalを記録済み。
- 変更前の内部参照: Header、Home、Company、404、Privacy互換、共通記事fallbackに総合Supportへの導線があることを確認。
- 外部登録・リンク: 既存ドキュメントの記録は確認。今回、App Store Connect全アプリの登録値や外部リンク・ブックマークの利用実態を新たに全件取得したわけではない。
- 個別84 Markdownの不変確認: 変更前9adadb9のSHA-256と全84ファイルが一致。[content-verification.json](content-verification.json)参照。本文・日付・タイトル・既存URL定義は不変。
- Hugo 0.158.0 Extended production build成功。静的検証はerrors 0 / warnings 0、既存191 HTML URL・138直接URL・53既存alias・84本文を保持。6言語×8カード、個別48 Product、25互換案内、公式バッジ6言語・確認済みStore21 URLも検証済み。[verification.json](verification.json)参照。
- Desktop / iPad / Mobile / Light / Dark: 64画面すべて成功。最終見出し調整後にProductsの1440 / 1280 / 834 / 393 / 320px×Light/Darkの10画面を再検証して成功。横はみ出し・画像切れ・axe違反・コンソールエラーは0。カードは44px以上の2導線を確認。
- 旧fragment: 8アプリ×6言語×2形式（`#<id>` / `#support-<id>`）の96通りと6件のContact、JavaScript無効時の直接遷移、キーボード・メニューEscape/focusを確認。結果は [browser-verification.json](browser-verification.json) / [products-final-verification.json](products-final-verification.json)。
- GitHub Actions / Pages / commit: 公開完了後に追記予定。
- 公開HTTP: 旧Support6言語、個別Support / FAQ / Privacy / Terms / Notes、旧一覧・ページ送りを含む公開後の結果を追記予定。

変更前の公開監査は [public-before.json](public-before.json)、個別本文の比較結果は [content-verification.json](content-verification.json)。既存URLに新しいredirectを足したり、JavaScript redirectへ依存したりする変更はない。
