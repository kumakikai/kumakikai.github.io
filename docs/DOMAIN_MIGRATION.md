# kumakikai.top 独自ドメイン運用

2026-09-24の移行対象は `https://kumakikai.github.io/` → `https://kumakikai.top/` のoriginのみ。本文・デザイン・ナビゲーション・path・query・fragmentは維持する。

## 公開設定

- ソースrepoは引き続き `kumakikai/kumakikai.github.io`。repo名を変更しない。
- `main` → `.github/workflows/deploy.yaml` → Hugo / 検証 → `gh-pages` → GitHub Pages。Pagesは **Deploy from a branch / gh-pages / root** を維持する。
- Hugo `baseURL = "https://kumakikai.top/"`、`static/CNAME` は `kumakikai.top` 1行。HugoがCNAMEをpublicへコピーし、通常の再デプロイでも消えない。CIがsource/output両方のCNAMEを検査する。
- PagesのCustom domainは **kumakikai.top**。DNS検証と証明書発行後に **Enforce HTTPS** を有効化する。発行中は完了扱いにしない。
- `.Permalink` / `absURL` / `absLangURL` がcanonical、hreflang、OGP / Twitter画像、JSON-LD、sitemap、robotsとHugo組み込みRSSを生成する。Atom単独feed・Web app manifest・service workerは現行構成にない。

## DNS

Spaceshipの `launch1.spaceship.net` / `launch2.spaceship.net` を維持し、高度なDNSで以下を登録する。TTL 300秒は移行時の運用値で、GitHub必須値ではない。

| Type | Host | Value | TTL |
| --- | --- | --- | --- |
| A | @ | 185.199.108.153 | 300 |
| A | @ | 185.199.109.153 | 300 |
| A | @ | 185.199.110.153 | 300 |
| A | @ | 185.199.111.153 | 300 |
| AAAA | @ | 2606:50c0:8000::153 | 300 |
| AAAA | @ | 2606:50c0:8001::153 | 300 |
| AAAA | @ | 2606:50c0:8002::153 | 300 |
| AAAA | @ | 2606:50c0:8003::153 | 300 |
| CNAME | www | kumakikai.github.io | 300 |

調査時、apexはSpaceship既定の駐車ページIP `34.216.117.25` / `54.149.79.189` を返し、カスタムDNS一覧は0件だった。上記を保存した後、権威DNSと公開リゾルバーに旧IPが残らないことを確認する。独自に設定された同名の異なるA / AAAA / ALIAS / ANAME、wwwのA / AAAA / CNAME、URL転送があれば競合を解消する。MX・無関係なTXT・NSは削除しない。ワイルドカードは作らない。

wwwのCNAME値はGitHubのホスト名なので旧ドメインを維持する。apexをCustom domainとすることで、wwwはapexへ転送される。GitHubアカウントのPagesでドメイン検証を行う場合は、GitHubが発行したTXT名・値をそのまま登録し、検証後も残す。

値と挙動の根拠: [GitHub公式・Custom domain管理](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)、[HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)、[ドメイン検証](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)。

## 公開前後の検証

1. 固定Node / Hugoで `npm run build`。`npm run verify`、`npm run verify:seo`、`python3 scripts/verify-domain.py --build public` とworkflowの既存チェックを実行する。
2. 全HTMLのpath、既存noindex対象、本文・画像・CSS・JSを移行前と比較する。旧paginationの既存HTML aliasは転送先originだけを更新する。画像に描画済みの旧ドメイン文字は画像維持の要件に従って変更せず、OGP URL自体は新originにする。今後のOGP生成器は新domainを出力する。
3. source commitのActions、対応するgh-pages commit、Pagesジョブ成功を確認する。成果物のCNAMEとSEO出力を読む。
4. apex / wwwのHTTPS、旧github.ioからの同一pathへの301、HTTP→HTTPS、主要Product / Support / Guide / FAQ / News / Privacy / Termsを確認する。存在しないURLは404を維持する。
5. 公開成果物と本番GET本文のSHA256を照合し、画像・CSS・JSのHTTP成功、mixed contentなしを確認する。ローカルPASS、DNS保存、DNS反映、TLS発行、実HTTP成功は別の証拠とする。
6. Search Consoleはユーザーアカウントで [SEO運用メモ](seo/OPERATIONS.md) に従う。旧→新の転送と既存repoは継続維持する。

## 旧ドメインを残す箇所

- `docs/migration/` の固定baseline・恒久URL一覧、過去の公開・SEO・素材・法務監査は当時の証拠。書き換えない。
- `scripts/verify-migration.py` の歴史的な本文リンク比較、`document_review.py` / `legal_navigation_review.py` / `nocca_legal_review.py` / `record-document-review.py` と対応する旧テストは、その固定baselineを参照する。現行canonicalには新originを要求する。
- 旧Home構成専用の `verify-home.py` は履歴用であり、現行CIには使わない。
- `verify-domain.py` の旧domainは再混入を検出する禁止値。移行記録・旧URL確認・Search Console旧プロパティ、GitHub repo名、DNSのwww CNAMEも意図した参照。
- `docs/uni-note-guide-phase2/reviewed-output.json` は今回変更した2つの検証依存のSHAのみ更新する。画像・本文・過去baselineのhashは維持する。

## 復旧

設定後に到達性の重大な問題が出た場合、まずDNSとPagesのcname/TLS状態、Actionsとgh-pagesのSHAを確認する。旧originへ戻す必要がある場合は、PagesのCustom domainを解除するだけでなく、baseURL・static/CNAME・検証期待値も同じ復旧commitで整合させて公開する。新旧canonicalが混在する成果物を出さない。DNSやCustom domainを切り替えた後は必ず実HTTPを再取得する。
