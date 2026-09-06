# 恒久URL保護台帳

基準はPaperMod公開ソース `811d9e816f292562b42ba8395ac99683a031ff66` のproduction buildです。旧HTML **191 URL**すべてを保護し、新しいProducts／Support／News／Companyは追加の入口として扱います。旧サポート・プライバシー・規約・Notes本文を新URLへの転送ページへ置き換えません。

確認日: 2026-09-07。確認対象は現在のローカル `public/` と隣接8リポジトリの公開用docs／README／Store metadataです。**現在のApp Store Connect登録値をライブ取得した一覧ではありません。** 公開HTTP到達性もこの台帳作成時点では未検証で、デプロイ後の確認が別途必要です。資格情報・秘密設定は参照していません。

機械可読データ: [permanent-urls.json](permanent-urls.json)。検証基準: [baseline.json](baseline.json)。`npm run verify`は旧非redirectページのredirect化、元canonicalの変更、旧alias転送先の変更、URL／本文／アンカー／リンクの消失を失敗として検出します。

## 1. 維持する旧URL — 138件の直接表示HTML

通常ページ132件と404画面6件です。404画面もURL・canonicalを保持します。明示的な `/404.html` は存在する静的ファイルとしてHTTP 200、存在しないURLへの要求はカスタム404画面とHTTP 404を期待します。ページ送り10 URLのcanonicalは移行前から親一覧を指しており、その元設定を維持しています。

| 旧URL（直接表示を維持） | 元canonicalが異なる場合 |
|---|---|
| [/](https://kumakikai.github.io/) | 同じURL |
| [/404.html](https://kumakikai.github.io/404.html) | 404画面 |
| [/categories/](https://kumakikai.github.io/categories/) | 同じURL |
| [/de/](https://kumakikai.github.io/de/) | 同じURL |
| [/de/404.html](https://kumakikai.github.io/de/404.html) | 404画面 |
| [/de/categories/](https://kumakikai.github.io/de/categories/) | 同じURL |
| [/de/faq/](https://kumakikai.github.io/de/faq/) | 同じURL |
| [/de/faq/uni-note-pocket/](https://kumakikai.github.io/de/faq/uni-note-pocket/) | 同じURL |
| [/de/faq/uni-note/](https://kumakikai.github.io/de/faq/uni-note/) | 同じURL |
| [/de/htu/](https://kumakikai.github.io/de/htu/) | 同じURL |
| [/de/htu/uni-note-pocket/](https://kumakikai.github.io/de/htu/uni-note-pocket/) | 同じURL |
| [/de/htu/uni-note/](https://kumakikai.github.io/de/htu/uni-note/) | 同じURL |
| [/de/privacy/](https://kumakikai.github.io/de/privacy/) | 同じURL |
| [/de/privacy/uni-note-pocket/](https://kumakikai.github.io/de/privacy/uni-note-pocket/) | 同じURL |
| [/de/privacy/uni-note/](https://kumakikai.github.io/de/privacy/uni-note/) | 同じURL |
| [/de/tags/](https://kumakikai.github.io/de/tags/) | 同じURL |
| [/en/](https://kumakikai.github.io/en/) | 同じURL |
| [/en/404.html](https://kumakikai.github.io/en/404.html) | 404画面 |
| [/en/categories/](https://kumakikai.github.io/en/categories/) | 同じURL |
| [/en/faq/](https://kumakikai.github.io/en/faq/) | 同じURL |
| [/en/faq/smokeless/](https://kumakikai.github.io/en/faq/smokeless/) | 同じURL |
| [/en/faq/uni-note-pocket/](https://kumakikai.github.io/en/faq/uni-note-pocket/) | 同じURL |
| [/en/faq/uni-note/](https://kumakikai.github.io/en/faq/uni-note/) | 同じURL |
| [/en/htu/](https://kumakikai.github.io/en/htu/) | 同じURL |
| [/en/htu/smokeless/](https://kumakikai.github.io/en/htu/smokeless/) | 同じURL |
| [/en/htu/uni-note-pocket/](https://kumakikai.github.io/en/htu/uni-note-pocket/) | 同じURL |
| [/en/htu/uni-note/](https://kumakikai.github.io/en/htu/uni-note/) | 同じURL |
| [/en/privacy/](https://kumakikai.github.io/en/privacy/) | 同じURL |
| [/en/privacy/smokeless/](https://kumakikai.github.io/en/privacy/smokeless/) | 同じURL |
| [/en/privacy/uni-note-pocket/](https://kumakikai.github.io/en/privacy/uni-note-pocket/) | 同じURL |
| [/en/privacy/uni-note/](https://kumakikai.github.io/en/privacy/uni-note/) | 同じURL |
| [/en/tags/](https://kumakikai.github.io/en/tags/) | 同じURL |
| [/faq/](https://kumakikai.github.io/faq/) | 同じURL |
| [/faq/balance-calendar/](https://kumakikai.github.io/faq/balance-calendar/) | 同じURL |
| [/faq/giga-poke/](https://kumakikai.github.io/faq/giga-poke/) | 同じURL |
| [/faq/nocca/](https://kumakikai.github.io/faq/nocca/) | 同じURL |
| [/faq/oto-miru/](https://kumakikai.github.io/faq/oto-miru/) | 同じURL |
| [/faq/page/2/](https://kumakikai.github.io/faq/page/2/) | https://kumakikai.github.io/faq/ |
| [/faq/page/3/](https://kumakikai.github.io/faq/page/3/) | https://kumakikai.github.io/faq/ |
| [/faq/signal/](https://kumakikai.github.io/faq/signal/) | 同じURL |
| [/faq/smokeless/](https://kumakikai.github.io/faq/smokeless/) | 同じURL |
| [/faq/uni-note-pocket/](https://kumakikai.github.io/faq/uni-note-pocket/) | 同じURL |
| [/faq/uni-note/](https://kumakikai.github.io/faq/uni-note/) | 同じURL |
| [/fr/](https://kumakikai.github.io/fr/) | 同じURL |
| [/fr/404.html](https://kumakikai.github.io/fr/404.html) | 404画面 |
| [/fr/categories/](https://kumakikai.github.io/fr/categories/) | 同じURL |
| [/fr/faq/](https://kumakikai.github.io/fr/faq/) | 同じURL |
| [/fr/faq/smokeless/](https://kumakikai.github.io/fr/faq/smokeless/) | 同じURL |
| [/fr/faq/uni-note-pocket/](https://kumakikai.github.io/fr/faq/uni-note-pocket/) | 同じURL |
| [/fr/faq/uni-note/](https://kumakikai.github.io/fr/faq/uni-note/) | 同じURL |
| [/fr/htu/](https://kumakikai.github.io/fr/htu/) | 同じURL |
| [/fr/htu/smokeless/](https://kumakikai.github.io/fr/htu/smokeless/) | 同じURL |
| [/fr/htu/uni-note-pocket/](https://kumakikai.github.io/fr/htu/uni-note-pocket/) | 同じURL |
| [/fr/htu/uni-note/](https://kumakikai.github.io/fr/htu/uni-note/) | 同じURL |
| [/fr/privacy/](https://kumakikai.github.io/fr/privacy/) | 同じURL |
| [/fr/privacy/smokeless/](https://kumakikai.github.io/fr/privacy/smokeless/) | 同じURL |
| [/fr/privacy/uni-note-pocket/](https://kumakikai.github.io/fr/privacy/uni-note-pocket/) | 同じURL |
| [/fr/privacy/uni-note/](https://kumakikai.github.io/fr/privacy/uni-note/) | 同じURL |
| [/fr/tags/](https://kumakikai.github.io/fr/tags/) | 同じURL |
| [/htu/](https://kumakikai.github.io/htu/) | 同じURL |
| [/htu/balance-calendar/](https://kumakikai.github.io/htu/balance-calendar/) | 同じURL |
| [/htu/giga-poke/](https://kumakikai.github.io/htu/giga-poke/) | 同じURL |
| [/htu/nocca/](https://kumakikai.github.io/htu/nocca/) | 同じURL |
| [/htu/oto-miru/](https://kumakikai.github.io/htu/oto-miru/) | 同じURL |
| [/htu/page/2/](https://kumakikai.github.io/htu/page/2/) | https://kumakikai.github.io/htu/ |
| [/htu/page/3/](https://kumakikai.github.io/htu/page/3/) | https://kumakikai.github.io/htu/ |
| [/htu/signal/](https://kumakikai.github.io/htu/signal/) | 同じURL |
| [/htu/smokeless/](https://kumakikai.github.io/htu/smokeless/) | 同じURL |
| [/htu/uni-note-pocket/](https://kumakikai.github.io/htu/uni-note-pocket/) | 同じURL |
| [/htu/uni-note/](https://kumakikai.github.io/htu/uni-note/) | 同じURL |
| [/ko/](https://kumakikai.github.io/ko/) | 同じURL |
| [/ko/404.html](https://kumakikai.github.io/ko/404.html) | 404画面 |
| [/ko/categories/](https://kumakikai.github.io/ko/categories/) | 同じURL |
| [/ko/faq/](https://kumakikai.github.io/ko/faq/) | 同じURL |
| [/ko/faq/smokeless/](https://kumakikai.github.io/ko/faq/smokeless/) | 同じURL |
| [/ko/faq/uni-note-pocket/](https://kumakikai.github.io/ko/faq/uni-note-pocket/) | 同じURL |
| [/ko/faq/uni-note/](https://kumakikai.github.io/ko/faq/uni-note/) | 同じURL |
| [/ko/htu/](https://kumakikai.github.io/ko/htu/) | 同じURL |
| [/ko/htu/smokeless/](https://kumakikai.github.io/ko/htu/smokeless/) | 同じURL |
| [/ko/htu/uni-note-pocket/](https://kumakikai.github.io/ko/htu/uni-note-pocket/) | 同じURL |
| [/ko/htu/uni-note/](https://kumakikai.github.io/ko/htu/uni-note/) | 同じURL |
| [/ko/privacy/](https://kumakikai.github.io/ko/privacy/) | 同じURL |
| [/ko/privacy/smokeless/](https://kumakikai.github.io/ko/privacy/smokeless/) | 同じURL |
| [/ko/privacy/uni-note-pocket/](https://kumakikai.github.io/ko/privacy/uni-note-pocket/) | 同じURL |
| [/ko/privacy/uni-note/](https://kumakikai.github.io/ko/privacy/uni-note/) | 同じURL |
| [/ko/tags/](https://kumakikai.github.io/ko/tags/) | 同じURL |
| [/notes/](https://kumakikai.github.io/notes/) | 同じURL |
| [/notes/2026-01-23-introduction/](https://kumakikai.github.io/notes/2026-01-23-introduction/) | 同じURL |
| [/notes/2026-01-26-roadmap/](https://kumakikai.github.io/notes/2026-01-26-roadmap/) | 同じURL |
| [/notes/2026-01-27-philosophy/](https://kumakikai.github.io/notes/2026-01-27-philosophy/) | 同じURL |
| [/notes/2026-02-14-blog/](https://kumakikai.github.io/notes/2026-02-14-blog/) | 同じURL |
| [/notes/2026-02-22-signal/](https://kumakikai.github.io/notes/2026-02-22-signal/) | 同じURL |
| [/notes/2026-03-12-uni-note/](https://kumakikai.github.io/notes/2026-03-12-uni-note/) | 同じURL |
| [/notes/2026-03-13-blog/](https://kumakikai.github.io/notes/2026-03-13-blog/) | 同じURL |
| [/notes/2026-03-21-smokeless/](https://kumakikai.github.io/notes/2026-03-21-smokeless/) | 同じURL |
| [/notes/2026-03-25-blog/](https://kumakikai.github.io/notes/2026-03-25-blog/) | 同じURL |
| [/notes/2026-04-01-uni-note-pocket/](https://kumakikai.github.io/notes/2026-04-01-uni-note-pocket/) | 同じURL |
| [/notes/2026-04-12-uni-note-10000/](https://kumakikai.github.io/notes/2026-04-12-uni-note-10000/) | 同じURL |
| [/notes/2026-05-19-oto-miru/](https://kumakikai.github.io/notes/2026-05-19-oto-miru/) | 同じURL |
| [/notes/2026-05-26-android-release/](https://kumakikai.github.io/notes/2026-05-26-android-release/) | 同じURL |
| [/notes/2026-09-02-giga-poke/](https://kumakikai.github.io/notes/2026-09-02-giga-poke/) | 同じURL |
| [/notes/2026-09-06-nocca/](https://kumakikai.github.io/notes/2026-09-06-nocca/) | 同じURL |
| [/notes/page/2/](https://kumakikai.github.io/notes/page/2/) | https://kumakikai.github.io/notes/ |
| [/notes/page/3/](https://kumakikai.github.io/notes/page/3/) | https://kumakikai.github.io/notes/ |
| [/notes/page/4/](https://kumakikai.github.io/notes/page/4/) | https://kumakikai.github.io/notes/ |
| [/notes/page/5/](https://kumakikai.github.io/notes/page/5/) | https://kumakikai.github.io/notes/ |
| [/privacy/](https://kumakikai.github.io/privacy/) | 同じURL |
| [/privacy/balance-calendar/](https://kumakikai.github.io/privacy/balance-calendar/) | 同じURL |
| [/privacy/giga-poke/](https://kumakikai.github.io/privacy/giga-poke/) | 同じURL |
| [/privacy/nocca/](https://kumakikai.github.io/privacy/nocca/) | 同じURL |
| [/privacy/oto-miru/](https://kumakikai.github.io/privacy/oto-miru/) | 同じURL |
| [/privacy/page/2/](https://kumakikai.github.io/privacy/page/2/) | https://kumakikai.github.io/privacy/ |
| [/privacy/page/3/](https://kumakikai.github.io/privacy/page/3/) | https://kumakikai.github.io/privacy/ |
| [/privacy/signal/](https://kumakikai.github.io/privacy/signal/) | 同じURL |
| [/privacy/smokeless/](https://kumakikai.github.io/privacy/smokeless/) | 同じURL |
| [/privacy/uni-note-pocket/](https://kumakikai.github.io/privacy/uni-note-pocket/) | 同じURL |
| [/privacy/uni-note/](https://kumakikai.github.io/privacy/uni-note/) | 同じURL |
| [/tags/](https://kumakikai.github.io/tags/) | 同じURL |
| [/terms/](https://kumakikai.github.io/terms/) | 同じURL |
| [/terms/giga-poke/](https://kumakikai.github.io/terms/giga-poke/) | 同じURL |
| [/terms/nocca/](https://kumakikai.github.io/terms/nocca/) | 同じURL |
| [/terms/oto-miru/](https://kumakikai.github.io/terms/oto-miru/) | 同じURL |
| [/zh-hant/](https://kumakikai.github.io/zh-hant/) | 同じURL |
| [/zh-hant/404.html](https://kumakikai.github.io/zh-hant/404.html) | 404画面 |
| [/zh-hant/categories/](https://kumakikai.github.io/zh-hant/categories/) | 同じURL |
| [/zh-hant/faq/](https://kumakikai.github.io/zh-hant/faq/) | 同じURL |
| [/zh-hant/faq/smokeless/](https://kumakikai.github.io/zh-hant/faq/smokeless/) | 同じURL |
| [/zh-hant/faq/uni-note-pocket/](https://kumakikai.github.io/zh-hant/faq/uni-note-pocket/) | 同じURL |
| [/zh-hant/faq/uni-note/](https://kumakikai.github.io/zh-hant/faq/uni-note/) | 同じURL |
| [/zh-hant/htu/](https://kumakikai.github.io/zh-hant/htu/) | 同じURL |
| [/zh-hant/htu/smokeless/](https://kumakikai.github.io/zh-hant/htu/smokeless/) | 同じURL |
| [/zh-hant/htu/uni-note-pocket/](https://kumakikai.github.io/zh-hant/htu/uni-note-pocket/) | 同じURL |
| [/zh-hant/htu/uni-note/](https://kumakikai.github.io/zh-hant/htu/uni-note/) | 同じURL |
| [/zh-hant/privacy/](https://kumakikai.github.io/zh-hant/privacy/) | 同じURL |
| [/zh-hant/privacy/smokeless/](https://kumakikai.github.io/zh-hant/privacy/smokeless/) | 同じURL |
| [/zh-hant/privacy/uni-note-pocket/](https://kumakikai.github.io/zh-hant/privacy/uni-note-pocket/) | 同じURL |
| [/zh-hant/privacy/uni-note/](https://kumakikai.github.io/zh-hant/privacy/uni-note/) | 同じURL |
| [/zh-hant/tags/](https://kumakikai.github.io/zh-hant/tags/) | 同じURL |

## 2. 新規URL — 72件

4セクション×6言語の24一覧と、8製品×6言語の48詳細です。旧URLを置き換えず追加します。日本語トップ `/` と他言語トップは既存URLなので、この新規72件には含めません。

| 新規URL | 種別 |
|---|---|
| [/products/](https://kumakikai.github.io/products/) | 一覧 |
| [/support/](https://kumakikai.github.io/support/) | 一覧 |
| [/news/](https://kumakikai.github.io/news/) | 一覧 |
| [/company/](https://kumakikai.github.io/company/) | 一覧 |
| [/products/uni-note/](https://kumakikai.github.io/products/uni-note/) | 製品詳細 |
| [/products/oto-miru/](https://kumakikai.github.io/products/oto-miru/) | 製品詳細 |
| [/products/giga-poke/](https://kumakikai.github.io/products/giga-poke/) | 製品詳細 |
| [/products/nocca/](https://kumakikai.github.io/products/nocca/) | 製品詳細 |
| [/products/uni-note-pocket/](https://kumakikai.github.io/products/uni-note-pocket/) | 製品詳細 |
| [/products/balance-calendar/](https://kumakikai.github.io/products/balance-calendar/) | 製品詳細 |
| [/products/smokeless/](https://kumakikai.github.io/products/smokeless/) | 製品詳細 |
| [/products/signal/](https://kumakikai.github.io/products/signal/) | 製品詳細 |
| [/en/products/](https://kumakikai.github.io/en/products/) | 一覧 |
| [/en/support/](https://kumakikai.github.io/en/support/) | 一覧 |
| [/en/news/](https://kumakikai.github.io/en/news/) | 一覧 |
| [/en/company/](https://kumakikai.github.io/en/company/) | 一覧 |
| [/en/products/uni-note/](https://kumakikai.github.io/en/products/uni-note/) | 製品詳細 |
| [/en/products/oto-miru/](https://kumakikai.github.io/en/products/oto-miru/) | 製品詳細 |
| [/en/products/giga-poke/](https://kumakikai.github.io/en/products/giga-poke/) | 製品詳細 |
| [/en/products/nocca/](https://kumakikai.github.io/en/products/nocca/) | 製品詳細 |
| [/en/products/uni-note-pocket/](https://kumakikai.github.io/en/products/uni-note-pocket/) | 製品詳細 |
| [/en/products/balance-calendar/](https://kumakikai.github.io/en/products/balance-calendar/) | 製品詳細 |
| [/en/products/smokeless/](https://kumakikai.github.io/en/products/smokeless/) | 製品詳細 |
| [/en/products/signal/](https://kumakikai.github.io/en/products/signal/) | 製品詳細 |
| [/ko/products/](https://kumakikai.github.io/ko/products/) | 一覧 |
| [/ko/support/](https://kumakikai.github.io/ko/support/) | 一覧 |
| [/ko/news/](https://kumakikai.github.io/ko/news/) | 一覧 |
| [/ko/company/](https://kumakikai.github.io/ko/company/) | 一覧 |
| [/ko/products/uni-note/](https://kumakikai.github.io/ko/products/uni-note/) | 製品詳細 |
| [/ko/products/oto-miru/](https://kumakikai.github.io/ko/products/oto-miru/) | 製品詳細 |
| [/ko/products/giga-poke/](https://kumakikai.github.io/ko/products/giga-poke/) | 製品詳細 |
| [/ko/products/nocca/](https://kumakikai.github.io/ko/products/nocca/) | 製品詳細 |
| [/ko/products/uni-note-pocket/](https://kumakikai.github.io/ko/products/uni-note-pocket/) | 製品詳細 |
| [/ko/products/balance-calendar/](https://kumakikai.github.io/ko/products/balance-calendar/) | 製品詳細 |
| [/ko/products/smokeless/](https://kumakikai.github.io/ko/products/smokeless/) | 製品詳細 |
| [/ko/products/signal/](https://kumakikai.github.io/ko/products/signal/) | 製品詳細 |
| [/de/products/](https://kumakikai.github.io/de/products/) | 一覧 |
| [/de/support/](https://kumakikai.github.io/de/support/) | 一覧 |
| [/de/news/](https://kumakikai.github.io/de/news/) | 一覧 |
| [/de/company/](https://kumakikai.github.io/de/company/) | 一覧 |
| [/de/products/uni-note/](https://kumakikai.github.io/de/products/uni-note/) | 製品詳細 |
| [/de/products/oto-miru/](https://kumakikai.github.io/de/products/oto-miru/) | 製品詳細 |
| [/de/products/giga-poke/](https://kumakikai.github.io/de/products/giga-poke/) | 製品詳細 |
| [/de/products/nocca/](https://kumakikai.github.io/de/products/nocca/) | 製品詳細 |
| [/de/products/uni-note-pocket/](https://kumakikai.github.io/de/products/uni-note-pocket/) | 製品詳細 |
| [/de/products/balance-calendar/](https://kumakikai.github.io/de/products/balance-calendar/) | 製品詳細 |
| [/de/products/smokeless/](https://kumakikai.github.io/de/products/smokeless/) | 製品詳細 |
| [/de/products/signal/](https://kumakikai.github.io/de/products/signal/) | 製品詳細 |
| [/zh-hant/products/](https://kumakikai.github.io/zh-hant/products/) | 一覧 |
| [/zh-hant/support/](https://kumakikai.github.io/zh-hant/support/) | 一覧 |
| [/zh-hant/news/](https://kumakikai.github.io/zh-hant/news/) | 一覧 |
| [/zh-hant/company/](https://kumakikai.github.io/zh-hant/company/) | 一覧 |
| [/zh-hant/products/uni-note/](https://kumakikai.github.io/zh-hant/products/uni-note/) | 製品詳細 |
| [/zh-hant/products/oto-miru/](https://kumakikai.github.io/zh-hant/products/oto-miru/) | 製品詳細 |
| [/zh-hant/products/giga-poke/](https://kumakikai.github.io/zh-hant/products/giga-poke/) | 製品詳細 |
| [/zh-hant/products/nocca/](https://kumakikai.github.io/zh-hant/products/nocca/) | 製品詳細 |
| [/zh-hant/products/uni-note-pocket/](https://kumakikai.github.io/zh-hant/products/uni-note-pocket/) | 製品詳細 |
| [/zh-hant/products/balance-calendar/](https://kumakikai.github.io/zh-hant/products/balance-calendar/) | 製品詳細 |
| [/zh-hant/products/smokeless/](https://kumakikai.github.io/zh-hant/products/smokeless/) | 製品詳細 |
| [/zh-hant/products/signal/](https://kumakikai.github.io/zh-hant/products/signal/) | 製品詳細 |
| [/fr/products/](https://kumakikai.github.io/fr/products/) | 一覧 |
| [/fr/support/](https://kumakikai.github.io/fr/support/) | 一覧 |
| [/fr/news/](https://kumakikai.github.io/fr/news/) | 一覧 |
| [/fr/company/](https://kumakikai.github.io/fr/company/) | 一覧 |
| [/fr/products/uni-note/](https://kumakikai.github.io/fr/products/uni-note/) | 製品詳細 |
| [/fr/products/oto-miru/](https://kumakikai.github.io/fr/products/oto-miru/) | 製品詳細 |
| [/fr/products/giga-poke/](https://kumakikai.github.io/fr/products/giga-poke/) | 製品詳細 |
| [/fr/products/nocca/](https://kumakikai.github.io/fr/products/nocca/) | 製品詳細 |
| [/fr/products/uni-note-pocket/](https://kumakikai.github.io/fr/products/uni-note-pocket/) | 製品詳細 |
| [/fr/products/balance-calendar/](https://kumakikai.github.io/fr/products/balance-calendar/) | 製品詳細 |
| [/fr/products/smokeless/](https://kumakikai.github.io/fr/products/smokeless/) | 製品詳細 |
| [/fr/products/signal/](https://kumakikai.github.io/fr/products/signal/) | 製品詳細 |

## 3. 互換aliasと追加alias

**既存53件は元の転送先を維持します。** これはGitHub Pagesに置くHTML内のcanonicalと即時meta refreshによる案内です。HTTP 301／302リダイレクトではなく、JavaScriptにも依存しません。リンクによる手動移動も可能です。

| 既存alias | 維持する転送先 |
|---|---|
| [/de/faq/page/1/](https://kumakikai.github.io/de/faq/page/1/) | [/de/faq/](https://kumakikai.github.io/de/faq/) |
| [/de/faq/uni-memo/](https://kumakikai.github.io/de/faq/uni-memo/) | [/de/faq/uni-note-pocket/](https://kumakikai.github.io/de/faq/uni-note-pocket/) |
| [/de/htu/page/1/](https://kumakikai.github.io/de/htu/page/1/) | [/de/htu/](https://kumakikai.github.io/de/htu/) |
| [/de/htu/uni-memo/](https://kumakikai.github.io/de/htu/uni-memo/) | [/de/htu/uni-note-pocket/](https://kumakikai.github.io/de/htu/uni-note-pocket/) |
| [/de/page/1/](https://kumakikai.github.io/de/page/1/) | [/de/](https://kumakikai.github.io/de/) |
| [/de/privacy/page/1/](https://kumakikai.github.io/de/privacy/page/1/) | [/de/privacy/](https://kumakikai.github.io/de/privacy/) |
| [/de/privacy/uni-memo/](https://kumakikai.github.io/de/privacy/uni-memo/) | [/de/privacy/uni-note-pocket/](https://kumakikai.github.io/de/privacy/uni-note-pocket/) |
| [/en/faq/page/1/](https://kumakikai.github.io/en/faq/page/1/) | [/en/faq/](https://kumakikai.github.io/en/faq/) |
| [/en/faq/uni-memo/](https://kumakikai.github.io/en/faq/uni-memo/) | [/en/faq/uni-note-pocket/](https://kumakikai.github.io/en/faq/uni-note-pocket/) |
| [/en/htu/page/1/](https://kumakikai.github.io/en/htu/page/1/) | [/en/htu/](https://kumakikai.github.io/en/htu/) |
| [/en/htu/uni-memo/](https://kumakikai.github.io/en/htu/uni-memo/) | [/en/htu/uni-note-pocket/](https://kumakikai.github.io/en/htu/uni-note-pocket/) |
| [/en/page/1/](https://kumakikai.github.io/en/page/1/) | [/en/](https://kumakikai.github.io/en/) |
| [/en/privacy/page/1/](https://kumakikai.github.io/en/privacy/page/1/) | [/en/privacy/](https://kumakikai.github.io/en/privacy/) |
| [/en/privacy/uni-memo/](https://kumakikai.github.io/en/privacy/uni-memo/) | [/en/privacy/uni-note-pocket/](https://kumakikai.github.io/en/privacy/uni-note-pocket/) |
| [/faq/page/1/](https://kumakikai.github.io/faq/page/1/) | [/faq/](https://kumakikai.github.io/faq/) |
| [/faq/povo-manager/](https://kumakikai.github.io/faq/povo-manager/) | [/faq/giga-poke/](https://kumakikai.github.io/faq/giga-poke/) |
| [/faq/uni-memo/](https://kumakikai.github.io/faq/uni-memo/) | [/faq/uni-note-pocket/](https://kumakikai.github.io/faq/uni-note-pocket/) |
| [/fr/faq/page/1/](https://kumakikai.github.io/fr/faq/page/1/) | [/fr/faq/](https://kumakikai.github.io/fr/faq/) |
| [/fr/faq/uni-memo/](https://kumakikai.github.io/fr/faq/uni-memo/) | [/fr/faq/uni-note-pocket/](https://kumakikai.github.io/fr/faq/uni-note-pocket/) |
| [/fr/htu/page/1/](https://kumakikai.github.io/fr/htu/page/1/) | [/fr/htu/](https://kumakikai.github.io/fr/htu/) |
| [/fr/htu/uni-memo/](https://kumakikai.github.io/fr/htu/uni-memo/) | [/fr/htu/uni-note-pocket/](https://kumakikai.github.io/fr/htu/uni-note-pocket/) |
| [/fr/page/1/](https://kumakikai.github.io/fr/page/1/) | [/fr/](https://kumakikai.github.io/fr/) |
| [/fr/privacy/page/1/](https://kumakikai.github.io/fr/privacy/page/1/) | [/fr/privacy/](https://kumakikai.github.io/fr/privacy/) |
| [/fr/privacy/uni-memo/](https://kumakikai.github.io/fr/privacy/uni-memo/) | [/fr/privacy/uni-note-pocket/](https://kumakikai.github.io/fr/privacy/uni-note-pocket/) |
| [/htu/page/1/](https://kumakikai.github.io/htu/page/1/) | [/htu/](https://kumakikai.github.io/htu/) |
| [/htu/povo-manager/](https://kumakikai.github.io/htu/povo-manager/) | [/htu/giga-poke/](https://kumakikai.github.io/htu/giga-poke/) |
| [/htu/uni-memo/](https://kumakikai.github.io/htu/uni-memo/) | [/htu/uni-note-pocket/](https://kumakikai.github.io/htu/uni-note-pocket/) |
| [/ja/](https://kumakikai.github.io/ja/) | [/](https://kumakikai.github.io/) |
| [/ko/faq/page/1/](https://kumakikai.github.io/ko/faq/page/1/) | [/ko/faq/](https://kumakikai.github.io/ko/faq/) |
| [/ko/faq/uni-memo/](https://kumakikai.github.io/ko/faq/uni-memo/) | [/ko/faq/uni-note-pocket/](https://kumakikai.github.io/ko/faq/uni-note-pocket/) |
| [/ko/htu/page/1/](https://kumakikai.github.io/ko/htu/page/1/) | [/ko/htu/](https://kumakikai.github.io/ko/htu/) |
| [/ko/htu/uni-memo/](https://kumakikai.github.io/ko/htu/uni-memo/) | [/ko/htu/uni-note-pocket/](https://kumakikai.github.io/ko/htu/uni-note-pocket/) |
| [/ko/page/1/](https://kumakikai.github.io/ko/page/1/) | [/ko/](https://kumakikai.github.io/ko/) |
| [/ko/privacy/page/1/](https://kumakikai.github.io/ko/privacy/page/1/) | [/ko/privacy/](https://kumakikai.github.io/ko/privacy/) |
| [/ko/privacy/uni-memo/](https://kumakikai.github.io/ko/privacy/uni-memo/) | [/ko/privacy/uni-note-pocket/](https://kumakikai.github.io/ko/privacy/uni-note-pocket/) |
| [/notes/page/1/](https://kumakikai.github.io/notes/page/1/) | [/notes/](https://kumakikai.github.io/notes/) |
| [/page/1/](https://kumakikai.github.io/page/1/) | [/](https://kumakikai.github.io/) |
| [/page/2/](https://kumakikai.github.io/page/2/) | [/](https://kumakikai.github.io/) |
| [/page/3/](https://kumakikai.github.io/page/3/) | [/](https://kumakikai.github.io/) |
| [/page/4/](https://kumakikai.github.io/page/4/) | [/](https://kumakikai.github.io/) |
| [/page/5/](https://kumakikai.github.io/page/5/) | [/](https://kumakikai.github.io/) |
| [/privacy/page/1/](https://kumakikai.github.io/privacy/page/1/) | [/privacy/](https://kumakikai.github.io/privacy/) |
| [/privacy/povo-manager/](https://kumakikai.github.io/privacy/povo-manager/) | [/privacy/giga-poke/](https://kumakikai.github.io/privacy/giga-poke/) |
| [/privacy/uni-memo/](https://kumakikai.github.io/privacy/uni-memo/) | [/privacy/uni-note-pocket/](https://kumakikai.github.io/privacy/uni-note-pocket/) |
| [/terms/page/1/](https://kumakikai.github.io/terms/page/1/) | [/terms/](https://kumakikai.github.io/terms/) |
| [/terms/povo-manager/](https://kumakikai.github.io/terms/povo-manager/) | [/terms/giga-poke/](https://kumakikai.github.io/terms/giga-poke/) |
| [/zh-hant/faq/page/1/](https://kumakikai.github.io/zh-hant/faq/page/1/) | [/zh-hant/faq/](https://kumakikai.github.io/zh-hant/faq/) |
| [/zh-hant/faq/uni-memo/](https://kumakikai.github.io/zh-hant/faq/uni-memo/) | [/zh-hant/faq/uni-note-pocket/](https://kumakikai.github.io/zh-hant/faq/uni-note-pocket/) |
| [/zh-hant/htu/page/1/](https://kumakikai.github.io/zh-hant/htu/page/1/) | [/zh-hant/htu/](https://kumakikai.github.io/zh-hant/htu/) |
| [/zh-hant/htu/uni-memo/](https://kumakikai.github.io/zh-hant/htu/uni-memo/) | [/zh-hant/htu/uni-note-pocket/](https://kumakikai.github.io/zh-hant/htu/uni-note-pocket/) |
| [/zh-hant/page/1/](https://kumakikai.github.io/zh-hant/page/1/) | [/zh-hant/](https://kumakikai.github.io/zh-hant/) |
| [/zh-hant/privacy/page/1/](https://kumakikai.github.io/zh-hant/privacy/page/1/) | [/zh-hant/privacy/](https://kumakikai.github.io/zh-hant/privacy/) |
| [/zh-hant/privacy/uni-memo/](https://kumakikai.github.io/zh-hant/privacy/uni-memo/) | [/zh-hant/privacy/uni-note-pocket/](https://kumakikai.github.io/zh-hant/privacy/uni-note-pocket/) |

追加は14件です。すわなび旧記事の誤記2 URLを正しいページへ案内し、残り12件はHugoが生成する各言語taxonomy一覧の第1ページaliasです。

| 新規alias | 転送先 | 理由 |
|---|---|
| [/categories/page/1/](https://kumakikai.github.io/categories/page/1/) | [/categories/](https://kumakikai.github.io/categories/) | Hugo taxonomy第1ページ |
| [/de/categories/page/1/](https://kumakikai.github.io/de/categories/page/1/) | [/de/categories/](https://kumakikai.github.io/de/categories/) | Hugo taxonomy第1ページ |
| [/de/tags/page/1/](https://kumakikai.github.io/de/tags/page/1/) | [/de/tags/](https://kumakikai.github.io/de/tags/) | Hugo taxonomy第1ページ |
| [/en/categories/page/1/](https://kumakikai.github.io/en/categories/page/1/) | [/en/categories/](https://kumakikai.github.io/en/categories/) | Hugo taxonomy第1ページ |
| [/en/tags/page/1/](https://kumakikai.github.io/en/tags/page/1/) | [/en/tags/](https://kumakikai.github.io/en/tags/) | Hugo taxonomy第1ページ |
| [/fr/categories/page/1/](https://kumakikai.github.io/fr/categories/page/1/) | [/fr/categories/](https://kumakikai.github.io/fr/categories/) | Hugo taxonomy第1ページ |
| [/fr/tags/page/1/](https://kumakikai.github.io/fr/tags/page/1/) | [/fr/tags/](https://kumakikai.github.io/fr/tags/) | Hugo taxonomy第1ページ |
| [/htu/smoke-less/](https://kumakikai.github.io/htu/smoke-less/) | [/htu/smokeless/](https://kumakikai.github.io/htu/smokeless/) | 旧記事の誤記修復 |
| [/ko/categories/page/1/](https://kumakikai.github.io/ko/categories/page/1/) | [/ko/categories/](https://kumakikai.github.io/ko/categories/) | Hugo taxonomy第1ページ |
| [/ko/tags/page/1/](https://kumakikai.github.io/ko/tags/page/1/) | [/ko/tags/](https://kumakikai.github.io/ko/tags/) | Hugo taxonomy第1ページ |
| [/privacy/smoke-less/](https://kumakikai.github.io/privacy/smoke-less/) | [/privacy/smokeless/](https://kumakikai.github.io/privacy/smokeless/) | 旧記事の誤記修復 |
| [/tags/page/1/](https://kumakikai.github.io/tags/page/1/) | [/tags/](https://kumakikai.github.io/tags/) | Hugo taxonomy第1ページ |
| [/zh-hant/categories/page/1/](https://kumakikai.github.io/zh-hant/categories/page/1/) | [/zh-hant/categories/](https://kumakikai.github.io/zh-hant/categories/) | Hugo taxonomy第1ページ |
| [/zh-hant/tags/page/1/](https://kumakikai.github.io/zh-hant/tags/page/1/) | [/zh-hant/tags/](https://kumakikai.github.io/zh-hant/tags/) | Hugo taxonomy第1ページ |

Hugo 0.158.0ではaliasに言語prefixが自動付与されるため、Pocketの5翻訳×3セクション、計15 front matterを言語サイト内の相対指定へ正規化しました。例: `/en/faq/uni-memo/` → `/faq/uni-memo/`。**生成URLは従来どおり `/en/faq/uni-memo/`** です。対象の全15ファイルと前後値はJSONの `compatibility.source_normalizations` にあります。旧記事本文は変更していません。

## 4. App Store Connect関連の可能性があるURLと根拠

下表はリポジトリ資料で具体的なURLを確認できた10件の証拠です。同一URLの別用途を含み、サイト内8種類と外部Google Forms 1種類にまとまります。サイト内URLはすべて旧191 URLに含まれ、候補buildでも直接表示と元canonicalを保持しています。**「候補」「設定指示」「過去取得記録」を現在の登録済み値として扱いません。** App Review固有の追加サイトURLは、このdocs範囲では見つかりませんでした。

| アプリrepo | 用途・URL | 証拠の強さ／制約 | 資料 |
|---|---|---|
| Nocca | Support URL: [/notes/2026-09-06-nocca/](https://kumakikai.github.io/notes/2026-09-06-nocca/) | 0.1.0提出準備中の過去取得記録。現在ASCをライブ確認した証拠ではない。 | `Nocca/docs/APP_STORE_METADATA.md:15`; `Nocca/docs/audit/2026-09-06_nocca_store_role_copy.md:130` |
| Nocca | Marketing URL: [/](https://kumakikai.github.io/) | 同日の保存後再読込でも維持したという記録。現在ASCは未照合。 | `Nocca/docs/APP_STORE_METADATA.md:15` |
| povo_manager | Support URL candidate: [/faq/giga-poke/](https://kumakikai.github.io/faq/giga-poke/) | 候補と明記。Release ChecklistにはGoogle FormsをSupport URLとする別記載もあり、登録済み値は断定しない。 | `povo_manager/docs/APP_STORE_METADATA.md:343`; `povo_manager/docs/FEATURE_SETTINGS_SUPPORT.md:87`; `povo_manager/docs/RELEASE_CHECKLIST.md:434` |
| povo_manager | Privacy Policy URL: [/privacy/giga-poke/](https://kumakikai.github.io/privacy/giga-poke/) | 公開済み・アプリ反映済み、アプリとASCで同一にする文書記載。現在ASCは未照合。 | `povo_manager/docs/APP_STORE_METADATA.md:243,344`; `povo_manager/docs/FEATURE_SETTINGS_SUPPORT.md:238,239`; `povo_manager/docs/RELEASE_CHECKLIST.md:464` |
| povo_manager | Marketing URL candidate: [/](https://kumakikai.github.io/) | 候補と明記。現在ASCの設定値ではない。 | `povo_manager/docs/APP_STORE_METADATA.md:346` |
| povo_manager | How-to/support resource: [/htu/giga-poke/](https://kumakikai.github.io/htu/giga-poke/) | 公式サポート素材として使用。ASCの特定fieldへ登録済みという証拠ではない。 | `povo_manager/docs/APP_STORE_METADATA.md:226`; `povo_manager/docs/FEATURE_SETTINGS_SUPPORT.md:81`; `povo_manager/docs/RELEASE_CHECKLIST.md:433` |
| povo_manager | Terms/support resource: [/terms/giga-poke/](https://kumakikai.github.io/terms/giga-poke/) | 公式規約への参照。ASCの特定fieldへ登録済みという証拠ではない。 | `povo_manager/docs/APP_STORE_METADATA.md:229`; `povo_manager/docs/FEATURE_SETTINGS_SUPPORT.md:242`; `povo_manager/docs/RELEASE_CHECKLIST.md:446` |
| povo_manager | Support URL candidate: [/Enzmm94LdXRZjP8k9](https://forms.gle/Enzmm94LdXRZjP8k9) | FAQ候補との矛盾が残る外部Forms URL。Hugo管理外であり、本移行では変更しない。 | `povo_manager/docs/RELEASE_CHECKLIST.md:465,533` |
| oto_miru | Description/EULA Terms URL: [/terms/oto-miru/](https://kumakikai.github.io/terms/oto-miru/) | ASC説明文またはEULA欄への設定指示。実際の現在登録値は未照合。 | `oto_miru/docs/APP_STORE_METADATA.md:88,93`; `oto_miru/docs/RELEASE_CHECKLIST.md:83` |
| oto_miru | Privacy Policy URL: [/privacy/oto-miru/](https://kumakikai.github.io/privacy/oto-miru/) | Store metadataと実装仕様文書の参照。現在ASCは未照合。 | `oto_miru/docs/APP_STORE_METADATA.md:89`; `oto_miru/docs/FEATURE_SUBSCRIPTION.md:99`; `oto_miru/docs/TRANSLATION_MATRIX.md:143` |

ギガポケのSupportについては、FAQを候補にするmetadataと、Google Formsを確認対象にするrelease checklistが併存しています。現在の公開トップが使うNotesの詳細／サポート入口も維持します。資料だけで一つをASC実登録値と断定せず、FAQ、Notes、Privacy、規約をすべて残します。

隣接8リポジトリの調査範囲と未確認事項:

| repo | 結果 | 主な確認資料 |
|---|---|
| uni_note | 現行docsはASC実登録値を未確認と明記。docs・公開用metadata/report Markdownの範囲で具体的サイトURLは見つからない。 | `docs/APP_STORE_METADATA.md`; `docs/RELEASE_CHECKLIST.md` |
| uni_memo | Support/Privacy確認項目はあるが具体値なし。権威あるASC metadataを保持していないと明記。 | `docs/APP_STORE_METADATA.md`; `docs/RELEASE_CHECKLIST.md` |
| oto_miru | Terms/Privacyの具体URLあり。Support/Marketingの特定field値は未確認。 | `docs/APP_STORE_METADATA.md` |
| povo_manager | Privacyとサポート資源の具体URLあり。SupportはFAQ候補とFormsの記載が混在。 | `docs/APP_STORE_METADATA.md`; `docs/RELEASE_CHECKLIST.md` |
| Nocca | Support/Marketingの2026-09-06 ASC取得記録あり。現時点のライブ照合ではない。 | `docs/APP_STORE_METADATA.md` |
| signal | 確認範囲に具体サイトURL／ASC field証拠なし。docs/fastlane metadataは探索で見つからない。 | `README.md`; `artifacts/app_store_screenshots_2026-09-03/SCREENSHOT_REPORT_JA.md` |
| smokeless | Store確定値を未確認扱いと明記。公開用docs/metadata/reportに具体サイトURLは見つからない。 | `docs/APP_STORE_METADATA.md`; `docs/FEATURE_SETTINGS_SUPPORT.md` |
| gamble_pnl | 確認範囲に具体サイトURL／ASC field証拠なし。FEATURE_SUPPORTはメール問い合わせ仕様。 | `docs/APP_STORE_METADATA.md`; `docs/FEATURE_SUPPORT.md` |

さらに、現在の公開サイト・共通アプリデータに存在する各アプリの詳細／サポート資源は下記です。これらも外部登録されている可能性を排除せず恒久保持しますが、**サイトにあることだけでASC登録済みとは主張しません。** 翻訳URLは第1一覧ですべて保持しています。

| アプリ | 既存入口・サポート資源 |
|---|---|
| uni-note | [/htu/uni-note/](https://kumakikai.github.io/htu/uni-note/) / [/faq/uni-note/](https://kumakikai.github.io/faq/uni-note/) / [/privacy/uni-note/](https://kumakikai.github.io/privacy/uni-note/) |
| oto-miru | [/htu/oto-miru/](https://kumakikai.github.io/htu/oto-miru/) / [/faq/oto-miru/](https://kumakikai.github.io/faq/oto-miru/) / [/privacy/oto-miru/](https://kumakikai.github.io/privacy/oto-miru/) / [/terms/oto-miru/](https://kumakikai.github.io/terms/oto-miru/) |
| giga-poke | [/notes/2026-09-02-giga-poke/](https://kumakikai.github.io/notes/2026-09-02-giga-poke/) / [/htu/giga-poke/](https://kumakikai.github.io/htu/giga-poke/) / [/faq/giga-poke/](https://kumakikai.github.io/faq/giga-poke/) / [/privacy/giga-poke/](https://kumakikai.github.io/privacy/giga-poke/) / [/terms/giga-poke/](https://kumakikai.github.io/terms/giga-poke/) |
| nocca | [/notes/2026-09-06-nocca/](https://kumakikai.github.io/notes/2026-09-06-nocca/) / [/htu/nocca/](https://kumakikai.github.io/htu/nocca/) / [/faq/nocca/](https://kumakikai.github.io/faq/nocca/) / [/privacy/nocca/](https://kumakikai.github.io/privacy/nocca/) / [/terms/nocca/](https://kumakikai.github.io/terms/nocca/) |
| uni-note-pocket | [/htu/uni-note-pocket/](https://kumakikai.github.io/htu/uni-note-pocket/) / [/faq/uni-note-pocket/](https://kumakikai.github.io/faq/uni-note-pocket/) / [/privacy/uni-note-pocket/](https://kumakikai.github.io/privacy/uni-note-pocket/) |
| balance-calendar | [/htu/balance-calendar/](https://kumakikai.github.io/htu/balance-calendar/) / [/faq/balance-calendar/](https://kumakikai.github.io/faq/balance-calendar/) / [/privacy/balance-calendar/](https://kumakikai.github.io/privacy/balance-calendar/) |
| smokeless | [/htu/smokeless/](https://kumakikai.github.io/htu/smokeless/) / [/faq/smokeless/](https://kumakikai.github.io/faq/smokeless/) / [/privacy/smokeless/](https://kumakikai.github.io/privacy/smokeless/) |
| signal | [/htu/signal/](https://kumakikai.github.io/htu/signal/) / [/faq/signal/](https://kumakikai.github.io/faq/signal/) / [/privacy/signal/](https://kumakikai.github.io/privacy/signal/) |

現在のASC登録URLと全localeを最終確定するには、各アプリのSupport、Marketing、Privacy、EULA／説明文、App Review欄を認証済みでライブ取得して照合する必要があります。その照合結果が未取得でも、今回確認した旧191 URLは削除・新URLへの置換を行いません。
