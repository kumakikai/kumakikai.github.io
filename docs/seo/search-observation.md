# 公開検索の確認（2026-09-07）

Googleの通常検索UIをログインなしで開き、`site:kumakikai.github.io` を確認した。
初回結果ページに表示された公式ドメインの結果は以下の2件。

| Google上の表示タイトル | 対応する既存正式URL | 現行記事タイトル |
|---|---|---|
| はじめに：自己紹介とこのアプリを作った理由 \| KUMAKIKAI | `/notes/2026-01-23-introduction/` | ギャンカレについて |
| Uni:Note Pocket を作りました | `/notes/2026-04-01-uni-note-pocket/` | Uni:Note Pocketについて |

これはGoogleの公開検索画面で確認した表示であり、サイトの現行HTMLが旧版という意味ではない。SEO対応前の本番監査でも両URLは現在のタイトル・Header/Footerを配信していた。検索結果には過去のタイトル・本文断片が残っている。

この2件をサイト全体のインデックス総数とはみなさない。順位・Googleが選択するcanonical・最終クロール日時・除外理由は、所有権確認後のSearch Consoleで確認する。今回の変更を理由に即時更新や順位上昇を保証しない。

別のWeb検索ツールでは `site:kumakikai.github.io` と `"KUMAKIKAI" "Yuya Nakamura"` に結果を取得できなかった。検索提供元による取得結果の差であり、Googleで未インデックスと断定する根拠には使わない。

Search Consoleの登録状況はユーザー回答で**未登録**と確認。確認コード・所有権・サイトマップ送信・URL検査の実行済み状態を捏造しない。
