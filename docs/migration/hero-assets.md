# Hero実UI素材の出典と加工

作成日: 2026-09-06。既存トップページで使用済みのアプリ画面、またはその制作原本のみを採用。AI画像生成、画面の描き直し、文字の置換、合成は行っていない。

## 選定

- **Uni:Note**: 現在のトップで使っている `SS01_handwriting.png` の実UI原本。`uni_note/artifacts/app_store_jp_refresh_2026-09-02/source_v7/generate_v7.mjs` の SS01 定義が `raw_v5/memorization_after_actual.png` を参照していることを確認。手書きノートとPDF講義資料が見える1640×2360のiPad縦画面を切り抜かず使用。Safariとローカルアドレスが画面半分に見える `split_view_actual.png` は採用しなかった。
- **オトミル**: `tmp_appstore_screenshots/export/3.png` の字幕画面。現在のトップ `static/images/apps/oto-miru/screen-1-840.webp` に掲載している字幕・話者ラベル・停止ボタンと同一表示内容であることを目視照合。画面の外側に付いた白余白を除去。字幕内容・反転中のステータス表示は原本を維持。ローカルの新しい未公開AI画面は使用していない。
- **ギガポケ**: 現在のトップにも使用している2026-09-04審査修正版 `01-hero.png` の端末内UIのみを切り抜いた。元のプロモーション文・背景は含めず、一覧・有効期限・利用ボタン・追加操作を保持。未修正の価格表現を含む初回提出版は使用していない。非公式アプリの表示は引き続きProduct/Featuredの本文で維持する。

既存公開トップ素材の調査記録は [前回の素材一覧](../homepage/README.md) を参照。

## 出力

データ契約は `data/hero.json` の `images` 配列。`width`/`height` はsmallの実寸、`largeWidth`/`largeHeight` はlargeの実寸。6言語の内容を説明するaltを含む。すべてRGB WebP、Lanczosリサイズ、quality=82、method=6。拡大処理・端末フレーム追加・回転・色調変更はない。

| ID | small | bytes | large | bytes |
|---|---:|---:|---:|---:|
| uni-note | 560×806 | 42,534 | 1120×1612 | 104,990 |
| oto-miru | 320×692 | 25,278 | 640×1385 | 57,274 |
| giga-poke | 320×589 | 11,830 | 640×1179 | 25,700 |

最大104,990bytes、3点のlarge合計187,964bytes。各ファイル150KB以下。画像間の配置・枠・影はWebのCSS側で設定し、画像への加工は増やさない。

## 原本と再生成情報

cropはPillowの `(left, top, right, bottom)`。nullは原寸領域。原本は各アプリのローカル制作ディレクトリに保持し、Web配信用の6ファイルだけをサイトへ追加した。

```json
[
  {
    "id": "uni-note",
    "source": "/Users/yuya/Projects/uni_note/artifacts/app_store_jp_refresh_2026-09-02/raw_v5/memorization_after_actual.png",
    "originalDimensions": [
      1640,
      2360
    ],
    "sourceSHA256": "9d40fa164af4ef38c5200e7ca29099d29f8a247ee9e0f03649460e92282a6a03",
    "crop": null,
    "croppedDimensions": [
      1640,
      2360
    ],
    "exports": [
      {
        "path": "/images/hero/uni-note-560.webp",
        "width": 560,
        "height": 806,
        "bytes": 42534,
        "sha256": "e5e38d4444796296c3ae9cc0e2371fe8b4a0b0b4b43105ab4b1a92e92ea05036"
      },
      {
        "path": "/images/hero/uni-note-1120.webp",
        "width": 1120,
        "height": 1612,
        "bytes": 104990,
        "sha256": "92a8968e66a4ff6f79571ac14baa5cb1ee651659d6d9a5313c5f640a33941349"
      }
    ]
  },
  {
    "id": "oto-miru",
    "source": "/Users/yuya/Projects/oto_miru/tmp_appstore_screenshots/export/3.png",
    "originalDimensions": [
      1284,
      2778
    ],
    "sourceSHA256": "49e63283ca15176ae7807c1e14789f0b85f1874ffd9185288c37470360c7492d",
    "crop": [
      244,
      824,
      1040,
      2546
    ],
    "croppedDimensions": [
      796,
      1722
    ],
    "exports": [
      {
        "path": "/images/hero/oto-miru-320.webp",
        "width": 320,
        "height": 692,
        "bytes": 25278,
        "sha256": "140599c156cee0802351c3b4d16c551cf81e3fa09ca679c4237a7331e2823111"
      },
      {
        "path": "/images/hero/oto-miru-640.webp",
        "width": 640,
        "height": 1385,
        "bytes": 57274,
        "sha256": "4012656a8bf19756c9f2aa857ba73594ceaa77cf4131e6607e164a74778b96ce"
      }
    ]
  },
  {
    "id": "giga-poke",
    "source": "/Users/yuya/Projects/povo_manager/design/app-store-screenshots-2026-09-04-review-fix/1242x2688-upload/01-hero.png",
    "originalDimensions": [
      1242,
      2688
    ],
    "sourceSHA256": "45e75bc71cc27dab44bc1660054889f458dc4c59ffb6515ff0ec6c30d06a7a71",
    "crop": [
      134,
      894,
      1108,
      2688
    ],
    "croppedDimensions": [
      974,
      1794
    ],
    "exports": [
      {
        "path": "/images/hero/giga-poke-320.webp",
        "width": 320,
        "height": 589,
        "bytes": 11830,
        "sha256": "75d988c3d56166eb941506144e33c209123966dddb49ded76235ec7ab7db9a8a"
      },
      {
        "path": "/images/hero/giga-poke-640.webp",
        "width": 640,
        "height": 1179,
        "bytes": 25700,
        "sha256": "332976bb5c68bfc7be09c1257ccaa3e086203db4084ed913fcf26aff8fd5cfaf"
      }
    ]
  }
]
```

再生成時は原本のSHA-256を確認し、次の処理を同じcropと幅で適用する。

```python
from PIL import Image
image = Image.open(source).convert("RGB")
if crop:
    image = image.crop(crop)
height = round(image.height * width / image.width)
image = image.resize((width, height), Image.Resampling.LANCZOS)
image.save(destination, "WEBP", quality=82, method=6)
```

## 目視確認

smallの3ファイルを画像ビューアで開き、文字・操作ボタンの欠け、トリミング境界、ノートおよび有効期限表示を確認済み。元画面を維持した縮小画像であり、Hero掲載サイズでの最終可読性はサイトのresponsive目視検証で確認する。
