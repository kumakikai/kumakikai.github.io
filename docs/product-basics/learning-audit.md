# Uni:Note / Pocket / Nocca 対応環境の確認

確認日: 2026-09-07。アプリの作業ツリーは3件とも未コミット変更があるため、現行ファイルを読み取りのみで確認した。アプリの変更、ビルド、Simulator起動、Store操作は実施していない。

`project.pbxproj` を `plutil` で解析し、アプリ本体の `PBXNativeTarget → XCConfigurationList → Release` をたどって確認した。テストターゲットやSimulator専用 `LiveE2E` の値を製品要件に採用していない。

| Product | 対応端末 | 最低対応OS | 本体Releaseの根拠（各プロジェクト内） | Web変更前 |
|---|---|---|---|---|
| Uni:Note | iPad | iPadOS 17.0 | `uni_note/UniNote.xcodeproj/project.pbxproj:1063` / device family 2: `1081` | 既存値と一致 |
| Uni:Note Pocket | iPhone | iOS 17.0 | `uni_memo/UniNotePocket.xcodeproj/project.pbxproj:334` / device family 1: `348` | 既存値と一致 |
| Nocca | iPhone | iOS 17.0 | `Nocca/Nocca.xcodeproj/project.pbxproj:510` / device family 1: `523` | `minimumOS` 未設定 |

Uni:Noteは本体Releaseの `SUPPORTED_PLATFORMS` が iPhone OS/Simulator SDKでも、device family は2のため表示は iPad / iPadOS。Pocketは1でiPhone。両アプリはMac Catalyst・Mac Designed for iPhone/iPadを無効化している。Release `.xcconfig` にDeployment Targetやdevice familyを上書きする記述はない。Noccaもdevice family 1でiPhone、Mac Designed for iPhone/iPadは無効。

## 公開状態との分離

- Uni:NoteのローカルReleaseは3.5.0 (1)。`uni_note/docs/APP_STORE_METADATA.md:830` は2026-09-07にApple公開APIから3.4.0を確認したと記録しており、ローカル3.5.0を公開済みと扱わない。サイトのアプリ自体の `published` は維持対象。今回この監査から最新バージョン公開を主張しない。
- PocketのローカルReleaseは3.4.0 (1)。リリース候補設定とApp Store公開状態は別。サイトは `published`、利用可能地域の既存確認日は2026-09-07。ライブ公開状態の最終確認はサイト側の独立監査で行う。
- NoccaのローカルReleaseは0.1.0 (2)。`Nocca/docs/APP_STORE_METADATA.md:3–11` の最新記録はTestFlight内部UI検証用で、審査提出・一般公開を意味しない。`development` を維持し、App Store CTAを追加しない。

## Uni:Noteのユーザー向けAI用語

正式キー `premium.settings.card.ai_balance.title` は各 `*.lproj/Localizable.strings:522` にあり、`UI/SettingsViewController.swift:2624,2637` でユーザー向け設定画面に使用している。

| 言語 | アプリ内表記 |
|---|---|
| ja | AI残量 |
| en | AI Balance |
| ko | AI 잔액 |
| de | KI-Guthaben |
| fr | Solde IA |
| zh-Hant | AI 餘額 |

Webの `data/product_details/uni-note.json` 変更前は6言語のnotesでquota相当の表現を使用していた（88 / 159 / 230 / 301 / 372 / 443行）。上記のアプリ内表記へ合わせる。Japanese `ai_balance.current`（589行）や `problem_generation.ai_balance.title`（723行）もAI残量で一致。内部キーに残るquotaをユーザー向け用語として採用しない。

Pocket / NoccaのProduct本文では quota / credit / entitlement 等の内部用語を検出しなかった。実装にある未公開機能・デバッグ用語をサイトへ追加しない。

機械可読なソース位置・作業ツリーSHA・変更前値は [learning-audit.json](learning-audit.json)。
