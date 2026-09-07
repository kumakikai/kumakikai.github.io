# News記事のdescription整備

2026-09-07に全15記事の本文を読み、front matterのdescriptionを追加・更新した。従来は13記事が未指定（Hugo Summaryへのfallback）、2記事が「紹介とサポート情報」という汎用説明だった。変更前の公開HTMLのdescriptionと、採用した全文は[news-metadata.json](news-metadata.json)に記録。

- Press Release 8件: 発表の対象、開発のきっかけ、本文で説明している用途を短く記述。過去のOS条件・価格・AI機能の記載を、現在利用可能な機能として検索結果へ押し出さない。ギガポケは非公式アプリ、Noccaは開発中であることをdescriptionにも維持。
- Blog 7件: 記事固有の相談、運営結果、公開準備、開発計画を説明。過去の計画・収益は「当時」「2026年○月の記録」などで時点を明確にした。
- Information 0件: 分類を埋めるための記事追加・再分類は行っていない。

descriptionは15件すべて異なる内容。記事本文・タイトル・公開日・ファイル名・URL・関連リンクは変更せず、本文のSHA-256一致を確認した。変更したfront matter項目は`description`と`lastmod`だけ。`lastmod: 2026-09-07`は実際にSEOメタデータを更新した日であり、記事本文を最新仕様へ書き換えたという意味ではない。以後のbuildで日付を自動更新しない。

新しい記事は`title`、固有の`description`、公開日の`date`を指定し、実際の変更時だけ`lastmod`を更新する。過去の発表記事を最新Product紹介として扱わず、現在の仕様は既存のProductページへの導線で確認できる状態を維持する。
