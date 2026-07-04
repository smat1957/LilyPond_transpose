# LilyPond_transpose

LilyPond で書かれたバッハ無伴奏チェロ組曲の楽譜を、ギター用に移調・整形するための作業用リポジトリです。

主に Python スクリプトで LilyPond ソースを移調し、その結果を LilyPond で PDF 化します。

## 概要

このリポジトリでは、チェロ用に入力した LilyPond ソースをもとに、ギターで演奏しやすい調へ移調した楽譜を作成します。

現在は主に以下のような用途を想定しています。

* Bach 無伴奏チェロ組曲 Prelude のギター用編曲
* LilyPond の `\relative` 記法を含むソースの移調
* 単音・和音・臨時記号を含む楽譜の変換
* 変換後の LilyPond ソース生成
* LilyPond による PDF 出力

## ディレクトリ構成

```text
.
├── lilyp/        LilyPond ソース
├── pdf/          生成された PDF
├── python/       移調用 Python スクリプト
├── gen1007.sh    BWV1007 用生成スクリプト
├── gen1009A.sh   BWV1009 A-Dur 用生成スクリプト
├── gen1009D.sh   BWV1009 D-Dur 用生成スクリプト
├── gen1010.sh    BWV1010 用生成スクリプト
└── gen1012.sh    BWV1012 用生成スクリプト
```

## 必要なもの

* Python 3
* LilyPond

## 基本的な使い方

例として、BWV1009 を C-Dur から A-Dur に移調する場合は、次のように実行します。

```sh
cd python
python3 main.py c a < ../lilyp/cello/cello1009.ly > ../lilyp/guitar/guitar1009A.ly
```

その後、LilyPond で PDF を生成します。

```sh
cd ../lilyp
lilypond BWV1009PreludeA.ly
mv BWV1009PreludeA.pdf ../pdf/
```

リポジトリ直下の `gen1009A.sh` などを使うと、変換から PDF 生成までをまとめて実行できます。

```sh
sh gen1009A.sh
```

## Python スクリプトの概要

`python/main.py` は次の形式で使います。

```sh
python3 main.py <移調元> <移調先>
```

例:

```sh
python3 main.py c a
python3 main.py c d
python3 main.py es c
```

標準入力から LilyPond ソースを読み込み、標準出力へ変換後の LilyPond ソースを書き出します。

## 対応している主な処理

* LilyPond 音名の解析
* 半音単位の移調
* 音名文字を考慮した綴りの決定
* `cis`, `fis`, `bes`, `es`, `as` などの臨時記号
* 一部のダブルシャープ・ダブルフラット
* `\relative` 内の音高再計算
* 和音 `<...>` の移調
* `\key` の移調

## 注意点

このプログラムは、LilyPond のすべての構文に対応した完全なパーサではありません。

実用上必要な範囲で、バッハ無伴奏チェロ組曲の LilyPond ソースをギター用に移調することを目的にしています。そのため、複雑な LilyPond 構文では手修正が必要になる場合があります。

変換後は必ず LilyPond でコンパイルし、PDF を確認してください。

## 作業方針

このリポジトリは、楽譜作成とプログラム改良を並行して行うためのものです。

変換結果をそのまま完成版とするのではなく、次のような流れで使います。

1. チェロ用 LilyPond ソースを用意する
2. Python スクリプトでギター用の調に移調する
3. LilyPond で PDF を生成する
4. 音・運指・譜面の見やすさを確認する
5. 必要に応じて LilyPond ソースを手修正する

## ライセンス

このリポジトリのライセンスは、必要に応じて `LICENSE` ファイルを追加してください。

MIT License などを採用する場合は、リポジトリ直下に `LICENSE` ファイルを置くのが一般的です。

## Author

smat1957
