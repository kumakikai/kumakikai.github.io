# Repository guidance

## KUMAKIKAI Website

公式サイトの変更では、実装前に必ず [docs/WEBSITE_MAINTENANCE.md](docs/WEBSITE_MAINTENANCE.md) を読むこと。Web保守の詳細仕様は同書を正本とする。通常のProduct追加・更新は現在のサイトへの情報反映であり、再設計ではない。明示された設計変更は実装と同時に同書へ反映する。

- 最初に `git status --short` を確認し、並行作業・未コミット変更を保護する。無関係なページ、素材、生成物を変更・stageしない。
- 既存公開URL、特にApp Store ConnectのSupport／Marketing／Privacy／Press Release／Guide／FAQ／Termsを維持する。正式本文をredirectへ置換しない。
- Home＝知る、Products＝全アプリ唯一の総合ハブ、Product＝理解する、Guide＝実操作、FAQ＝問題・例外、News＝発信、About＝ブランド・人物の役割を維持する。
- Headerは **Products / News / About**、FooterはContact中心。Support／Privacy総合ハブ、HomeのOther Appsを復活させない。
- HomeはUni:Note先頭固定＋ランダム3件。Desktopの画像位置は表示順で右→左→右→左、Mobileは説明→画像。Aboutの代表Productは同じ大分類内だけでランダム選出する。
- Hugoplate、既存Typography・余白・カード・CTA・共通partialを維持する。通常更新でテーマ、Framework、ナビゲーション、CMSを変えない。
- Product仕様は現在のアプリ実装・実UIを最優先で確認する。審査提出と一般公開を分け、名称・最低OS・配信地域・URL・利用条件を推測しない。アプリ内用語を使う。
- Product紹介画像は最新の正式App Store提出／公開素材、Guideは最新の実画面を優先する。不足時はSimulator撮影可。個人情報・本番課金・ダミーUI・AI生成UIを使わない。自分が使用したSimulatorだけ終了する。
- App Store CTAは公式ローカライズバッジを無改変で使う。サイト言語と配信地域は別管理。未公開アプリのStore CTAを出さない。
- Product固有Supportの既存URLと5項目の共通UIを維持する。独自Terms未設定時だけ共通Apple Standard EULAへfallbackする。Product／Guide／FAQから同内容のPress Releaseへ誘導しない。
- 基本情報は **対応端末 → 対応OS → 公開状況**。最低OSは必須。「開発元」を戻さず、Uni:Noteは「iPad」「AI残量」とする。
- KUMAKIKAIはYuya Nakamuraが運営するアプリ開発ブランド。法人扱い、漢字氏名、名刺の電話番号、架空実績、抽象的な企業コピーを追加しない。通常Product更新でFounderを書き換えない。
- 固有title／description、canonical、schema、静的リンク、sitemap、実在翻訳間のhreflangを整合させる。SEO目的のURL変更、keyword stuffing、架空ratingは禁止。
- 完了前にproduction buildと対象に応じた検証を行う。公開を伴う更新はcommit/push、Actions・Pages成功、同一成果物と本番URLの再取得まで確認する。ローカル成功と公開確認を混同しない。

実ファイル、3種類のチェックリスト、画像・法務・SEO・検証手順は [運用ガイド](docs/WEBSITE_MAINTENANCE.md) を参照する。リポジトリと関連アプリで調べ、確認できない事実だけをユーザーへ尋ねる。
