# 日本語改行の実表示監査

この記録では、DOM上のはみ出し検査と、日本語の改行位置の読み取りを分ける。`mechanicalPass` はHTTP・画像・横幅・Featured重複の機械検査結果であり、日本語が自然だという判定ではない。DOM Rangeの文字ごとの矩形から行を復元し、Intl.Segmenterの語境界と照合した候補を本文として読み、実スクリーンショットでも確認する。

## 修正前に確認した問題

Chromeは `word-break: auto-phrase` に対応し、主要ページ64条件で見出しの語中分割は検出しなかった。一方、WebKitは同プロパティに依存できず、同64条件で以下が発生した。

| ページ・幅 | 実際の改行 | 問題 |
|---|---|---|
| Pocket / 1024・768・390・375 | 使い始めは、バックアッ／プを取り込むだけ。 | バックアップの語中分割 |
| Pocket / 768・390・375 | 空き時間に、答／えを確かめる。 | 答えの語中分割 |
| Nocca / 768・375 | 伝える側のペー／スを、大切に。 | ペースの語中分割 |
| ギャンカレ / 1024・768・390・375 | 記録の入口は、大き／なふたつのボタン | 大きなの語中分割 |
| SIGNAL / 768・390・375 | フィードを、自／分の読む範囲に | 自分の語中分割 |
| Uni:Note 対象ユーザー / 768 | ノートを試験勉／強にも使いたい | 勉強の語中分割 |
| Home Uni:Note本文 / 768・390・375 | AIで問／題集づくり | 問題集の語中分割 |
| Home ギガポケ本文 / 1024・390 | ウィ／ジェット | ウィジェットの語中分割 |
| Home すわなび本文 / 390・375 | ワンタッ／プ | タップの語中分割 |
| Home ギャンカレ本文 / 375 | カレン／ダー | カレンダーの語中分割 |

記事・使い方・FAQ等もWebKitで70条件確認。Newsの長い見出しは既存の意味単位のspanが効いている一方、共通記事見出しには以下の不足があった。

- Pocket使い方 375px：読み込みア／イコン。
- オトミルFAQ 375px：サー／バー。
- ギガポケFAQ 375px：特／典、画／面、インストー／ル、デー／タ。
- ギャンカレFAQ 375px：ア／ドバイス。
- Privacy 375px：ポ／リシー、ウィ／ジェット。

スクリーンショット：`screenshots/before-pocket-story-390.jpg`、`before-nocca-overview-768.jpg`、`before-home-375.jpg`。

本文の全候補は `webkit-initial.json`・`webkit-initial-content.json` の `bodyCandidates` に記録。日本語では通常の本文改行が語境界に一致しない場合もあるため、候補数をそのまま不具合数として数えない。特に長い複合語やインライン装飾は目視確認する。

## 修正後

7幅（375 / 390 / 430 / 768 / 1024 / 1280 / 1440px）で、61ルートとHome追加4seedをChrome・WebKitそれぞれ455条件、計910条件で再取得した。

- Home、Products一覧、全8Product、About、News、News全15記事、全8アプリ使い方、全8FAQ、全8Privacy、全3Terms、既存の各一覧入口、404を実表示。
- すべての幅でHomeの8アプリ全候補を、実際に選出されたFeatured状態で確認。Uni:Note先頭・4件表示・重複なしを維持。
- 910条件すべてでHTTP・画像読込・横overflow検査が成功。本文の語中分割候補は0。
- 機械的な短行候補は、Watch画像注釈末尾「確認。」とFAQ操作手順末尾「選ぶ」。いずれも独立した意味のまとまりとして読めるため許容。
- 旧 `/privacy/` 互換ページの見出しだけ、Chrome 390/430px・WebKit 375/390pxで「いて」「て」の短い末尾を検出。見出しを「プライバシーポリシー」へ短くし、当該URLを7幅×2エンジンで局所再検証した。14条件すべて成功し、見出し末尾の短い行・語中分割候補も0。各アプリのPrivacy Policy本文は変更しない。

### スクリーンショットの目視

WebKitで全8アプリのFeaturedを1024px・375pxで表示し、アイコン・見出し・説明・CTAを切り出した16枚を目視した。以前の「問／題集」「ウィ／ジェット」「コー／ド」「ワンタッ／プ」「カレン／ダー」は解消。キャッチコピーの意味の区切りは保ち、説明文も語中で切らずに読める。ギガポケの非公式表記・Noccaの開発中表示・すわなびのApple Watch近日対応表示を保っている。

切り出しは `artifacts/watch-typography/featured-visual/` に保存。ユーザーに渡す全体画像は `screenshots/*-final.jpg` に保存。root担当でもHome Hero、Watchセクション、全Productの概要・機能紹介画面を別途目視。

初回のWatch画像注釈では句点だけの独立行があり、「審査提出用のWatch画面。」へ短縮後に解消した。画像自体は実App Store提出素材のまま。

### 検証範囲の区別

`chrome-final.json` / `webkit-final.json` は、Privacy見出しの局所修正前まで含めた全幅の記録。Privacy最終追補、ランダム選出・多言語・アクセシビリティを含む既存selection検査は別ファイルで記録する。物理iPhone/iPadの検証や実ユーザーの回線品質の測定ではない。

Privacy最終追補は `chrome-privacy-followup.json` / `webkit-privacy-followup.json` に記録。これを適用した最終状態では全61ルート・7幅・2エンジンの見出しに未解決の語中分割・不自然な短い末尾行はない。

エンジンはGoogle Chrome 152.0.7977.82とPlaywright WebKit 26.5。各エンジンで見出し6,111表示、本文16,891ブロックの行位置を記録した（ルート・幅・Featuredパターン違いの繰り返しを含む）。DOM行数や単語候補の全量を読んだという意味ではなく、不自然な候補の抽出と実表示の目視に利用した。

## ランダム選出・多言語・アクセシビリティの最終追補

`selection-verification.json` は最終の静止ビルドで88条件すべて成功。全候補の決定的seed検証、実際の初回＋5回リロード、6言語、Light/Dark、Desktop/Mobile、JS無効、外部JS遮断、低速回線のシミュレーションを含む。実リロードではHome・Aboutとも6通りの組み合わせを観測した。Uni:Note先頭・重複なし・Aboutのカテゴリ内選出を維持。CLSは62ケース（画像読込前後124測定値）ですべて0、実際にaxeを実行した60ケースで違反0。

最終記録のcheckedAtは `2026-09-06T19:58:09.838Z`。一度目のselection試行は途中の再ビルドと明示中断が重なったため無効とし、`artifacts/watch-typography/selection-interrupted-for-rebuild.json` に分離した。公開用の証拠や成功件数に含めない。

## Home HeroとFooterの追加目視

Home leadは文章を変えずに既存の可変フレーズ表示を適用し、「iPhone・iPad向けのアプリを」「企画・開発・運営しています。」をまとまりとして扱った。`chrome-home-followup.json` / `webkit-home-followup.json` の計70条件で、全7幅・全Featured候補を確認。「企画・開発・運営」が同じ視覚行に属することを明示的に検証し、すべて成功。Chrome 1440/390pxのCLSは0、axeも2条件で違反0。既存455/88条件の記録は上書きしていない。

本文に加えてmain外のFooter商標注記も行位置を記録・目視。WebKit375pxで「商／標です。」が残り、共通フレーズ処理の対象外であることを確認した。`webkit-footer-375-before-fallback.jpg` が修正前証跡。Footerの局所修正・追補を別記録で行う。

Footerへ同じビルド時フレーズ処理を適用後、`chrome-footer-followup.json` / `webkit-footer-followup.json` の14条件で再検証し、すべて成功。WebKit375/390pxでは「Apple、Appleのロゴ、iPhone、iPadはApple Inc.の商標です。」が1行、「App StoreはApple Inc.のサービスマークです。」が次の行となり、語中分割は解消した。Homeの「企画・開発・運営」も再度全幅で維持を確認。

最終添付向け画像は `screenshots/{chrome,webkit}-home-{1440,390}-footer-followup.jpg`（全長）、`{chrome,webkit}-home-hero-{1440,390}-footer-followup.jpg`（Hero）、`{chrome,webkit}-footer-{1440,390}-footer-followup.jpg`（Footer）。実UI画像の読込後に撮影し、Desktop Hero・Mobile Hero・Mobile Footerを目視確認した。旧画像は比較証拠として保持し、最終添付には `footer-followup` を使用する。
