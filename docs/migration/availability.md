# App Store の提供地域と表示言語

確認日: 2026-09-06。サイトの表示言語と、App Store の提供地域を別々に管理する。

## サイトの表示方針

- `data/apps.json` は全言語共通のプロダクト一覧。表示言語やアクセス元によってアプリを除外しない。
- 言語切替はサイトの文章と既存翻訳ページの切替だけに使用する。英語を米国、ドイツ語をドイツなどのストアへ対応付けない。
- GeoIP、IPアドレスによる国判定、国選択、自動ストアリダイレクトは実装しない。
- 公開中7アプリの既存 `appStoreURL` は、明示的な日本ストアの `https://apps.apple.com/jp/app/id…` を維持する。
- CTA本文は既存の「App Storeで見る」を維持し、その近くに各表示言語で「日本のApp Storeで提供中」と補足する。「日本のみ」とは表示しない。
- 未公開のNoccaは全言語に掲載し、「開発中」として扱う。ストアリンクは表示しない。

## データの意味

公開中の例:

```json
{
  "status": "published",
  "appStoreURL": "https://apps.apple.com/jp/app/id6760258084",
  "availability": {
    "storefront": "jp",
    "verifiedStorefronts": ["jp", "us", "tw", "fr", "kr"],
    "coverage": "partial",
    "checkedAt": "2026-09-06"
  }
}
```

- `storefront`: サイトのストアCTAがリンクする国・地域。表示言語ではなく、`appStoreURL` の国コードと一致させる。
- `verifiedStorefronts`: 確認日時点で、Apple公式の公開Lookup APIが対象Apple IDを返したストア。確認済みの部分集合であり、配信地域の完全な一覧ではない。
- `coverage: partial`: 全世界の提供状況は未調査。リストにない地域は未確認であり、配信不可や日本限定を意味しない。
- `checkedAt`: 配信状況を調査した日。表示言語や最新アプリバージョンを表す値ではない。
- `plannedStorefronts`: 未公開アプリの既存メタデータに記録された配信予定地域。公開中の地域とは区別する。
- `coverage: unreleased`: 未公開。`verifiedStorefronts` は空配列とし、`storefront` と `appStoreURL` を持たせない。

CTAは `status == published`、`appStoreURL` が存在すること、`availability.storefront` が `verifiedStorefronts` に含まれることを確認して表示する。`coverage: partial` を世界配信と読み替えない。将来、異なる地域のリンクを追加する際も、表示言語から地域を推測しない。

## 公開配信の確認結果

Apple公式Lookup APIを、各国コードを明示して読み取り専用で照会した。今回は日本・米国を確認し、すわなびの現行メタデータに公開名称の確認記録があった台湾・フランス・韓国を追加確認した。国の選択はサイト言語の対応表ではない。

| アプリ | Apple ID | 今回確認できた公開ストア | 取得した公開版 | 管理上の扱い |
|---|---|---|---|---|
| Uni:Note | 6760258084 | 日本・米国・台湾・フランス・韓国 | 3.4.0 | partial |
| オトミル | 6770774613 | 日本 | 1.0.1 | partial |
| ギガポケ | 6807501268 | 日本 | 0.1.0 | partial |
| Uni:Note Pocket | 6761449487 | 日本・米国・台湾・フランス・韓国 | 3.4.0 | partial |
| ギャンカレ | 6757731648 | 日本・米国 | 1.4.0 | partial |
| すわなび | 6760842941 | 日本・台湾・フランス・韓国 | 1.1.1 | partial |
| SIGNAL | 6759493613 | 日本 | 1.1.1 | partial |
| Nocca | 6809145321 | なし。日本Lookupは0件 | 未公開 | unreleased |

日本Lookupは公開中7件をすべて返した。米国・台湾・フランス・韓国はそれぞれ3件。結果に返らなかったことから他の全地域で配信不可とは判断していない。日本のみ返ったアプリも、この調査では「日本限定」と断定しない。

実際の問い合わせ:

- [日本のLookup結果](https://itunes.apple.com/lookup?id=6760258084,6770774613,6807501268,6761449487,6757731648,6760842941,6759493613&entity=software&country=jp)
- [米国のLookup結果](https://itunes.apple.com/lookup?id=6760258084,6770774613,6807501268,6761449487,6757731648,6760842941,6759493613&entity=software&country=us)
- [台湾のLookup結果](https://itunes.apple.com/lookup?id=6760258084,6770774613,6807501268,6761449487,6757731648,6760842941,6759493613&entity=software&country=tw)
- [フランスのLookup結果](https://itunes.apple.com/lookup?id=6760258084,6770774613,6807501268,6761449487,6757731648,6760842941,6759493613&entity=software&country=fr)
- [韓国のLookup結果](https://itunes.apple.com/lookup?id=6760258084,6770774613,6807501268,6761449487,6757731648,6760842941,6759493613&entity=software&country=kr)
- [Noccaの日本Lookup結果](https://itunes.apple.com/lookup?id=6809145321&entity=software&country=jp)

これらの公開APIは将来のアクセス時に結果が変わる。上表は2026-09-06の確認記録である。App Storeの提供状況は変更されるため、リリースや地域追加時に再確認する。

## ローカルメタデータとの照合

- `Nocca/docs/APP_STORE_METADATA.md` の2026-09-06 App Store Connect登録・追加設定記録は、Apple ID `6809145321`、提出準備中、一般公開未実施、日本のみの配信予定設定を明示する。したがって `plannedStorefronts: ["jp"]` とし、公開配信として扱わない。
- `smokeless/docs/APP_STORE_METADATA.md` の2026-09-06表は、JP/TW/FR/KRの公開名称をApple Lookup APIで確認した記録を持つ。今回も同じ4ストアの公開結果を取得した。
- その他の調査対象は `uni_note`、`uni_memo`、`oto_miru`、`povo_manager`、`gamble_pnl` の `docs/APP_STORE_METADATA.md` / `docs/RELEASE_CHECKLIST.md`、および `signal/README.md`。公開中アプリについて、全配信地域を確定できる設定記録は見つからなかった。
- Google Playの国設定、翻訳ファイルやスクリーンショットの言語、国内向けという企画上の説明は、App Storeの配信地域の証拠として使用しない。

上記パスは隣接するアプリリポジトリの監査元を示す。このサイトをビルドするために、それらのリポジトリへアクセスする必要はない。

## 将来の更新

1. Apple IDと明示した国コードで公開Lookup結果を確認する。
2. 対象の `verifiedStorefronts` と `checkedAt` を更新する。
3. ストアCTAを変更する場合は `appStoreURL` と `storefront` を一致させる。既存のURLを言語コードから自動生成しない。
4. 新規公開の場合は、公開確認後にのみ `status`、`appStoreURL`、`coverage` を更新する。
5. 全言語のProducts一覧が同じアプリ集合を保ち、開発中アプリにストアCTAが出ないことを検証する。
