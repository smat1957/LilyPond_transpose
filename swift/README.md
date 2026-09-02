# LilyPond Transpose Swift版

LilyPondで記述された楽譜ソースを、指定した音高間で移調するSwift実装です。
共通変換ライブラリ`LilyPondTransposeCore`と、macOS・iPad・iPhone向けの
SwiftUIアプリを提供します。

リポジトリ全体とPython版については
[LilyPond_transpose README](../README.md)を参照してください。

## 主な機能

- LilyPond音名と臨時記号の解析
- 指定した移調元・移調先に基づく音高変換
- `\relative`内の音高とオクターブ記号の再計算
- 単音、和音、調号の移調
- コメントや移調対象外テキストを保持したソース出力
- macOSでのファイル読込み
- iPad・iPhoneでのテキスト入力と変換
- Swift Packageとして他アプリから利用可能

LilyPondの完全な構文解析器ではありません。変換後はLilyPondでコンパイルし、
音高、調号、記譜結果を確認してください。

## 対応環境

`Package.swift`では次の最低バージョンを指定しています。

- macOS 14以降
- iOS・iPadOS 17以降
- Swift tools 6.0

## ディレクトリ構成

```text
swift/
├── Package.swift
├── LilyPondTranspose.xcodeproj
├── LilyPondTranspose/
│   ├── Core/                 共通の字句解析・移調・出力処理
│   ├── macOS/                macOS固有のUIとファイル選択
│   ├── iPad/                 iPad固有のUI
│   └── iPhone/               iPhone固有のUI
└── LilyPondTransposeTests/   Coreの単体テスト
```

プラットフォーム共通の処理は`Core`へ置き、UIとファイル選択などの固有処理は
各プラットフォームのフォルダへ置きます。プラットフォーム切替えのための
`#if os(...)`は使用せず、Xcodeターゲットの所属で分離します。

## Xcodeアプリのターゲット

- `LilyPondTransposeMac`
- `LilyPondTransposePad`
- `LilyPondTransposePhone`

`LilyPondTranspose.xcodeproj`をXcodeで開き、実行するSchemeと端末を選択して
ビルドします。

## アプリの使い方

1. 移調元の音高を入力します（例：`c`）。
2. 移調先の音高を入力します（例：`a`）。
3. LilyPondソースを入力または読み込みます。
4. 変換を実行します。
5. 出力されたLilyPondソースを確認します。

音高にはLilyPond形式の`cis`、`es`、`bes`なども指定できます。

## Swift Packageとして利用する

Swift Packageのプロダクト名は`LilyPondTransposeCore`です。別のXcodeプロジェクトから
`swift/`ディレクトリをローカルPackageとして追加し、利用するソースでimportします。

```swift
import LilyPondTransposeCore

let result = try LilyPondTransposer().transpose(
    lilyPondSource,
    from: "c",
    to: "a"
)
```

実際の公開APIと引数は
[`LilyPondTransposer.swift`](LilyPondTranspose/Core/LilyPondTransposer.swift)を
基準にしてください。

## LilyPondNoteから利用する

LilyPondNoteのXcodeプロジェクトは、次のように2つのリポジトリが同じ親フォルダに
あることを前提に、`LilyPondTransposeCore`をローカルPackageとして参照します。

```text
Git/
├── LilyPondNote/
└── LilyPond_transpose/
    └── swift/
```

## テスト

`swift`ディレクトリで次を実行します。

```sh
swift test
```

テストは`LilyPondTransposeTests/LilyPondTransposerTests.swift`にあります。

## Python版との関係

Python版は標準入力と標準出力を使うコマンドライン実装として残しています。
Swift版は同じ用途をAppleプラットフォームのアプリやSwiftライブラリから利用するための
実装です。両方の実装で対応範囲や出力に差が生じる可能性があるため、変換結果は必ず
LilyPondで確認してください。
