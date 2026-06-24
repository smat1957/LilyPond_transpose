'''
main.py
    プログラム全体の流れ
tokenizer.py
    文字列 → Token
tokens.py
    Token定義
music_theory.py
    音楽理論
pitch.py
    PitchPos と MIDI
transpose.py
    移調処理
writer.py
    Token → 文字列
'''
# main.py
#
# LilyPond 移調プログラムのエントリポイント。
#
# 処理の流れ:
#
#     標準入力
#         ↓
#     Tokenize
#         ↓
#     移調
#         ↓
#     LilyPond文字列へ復元
#         ↓
#     標準出力
#
# 使用例:
#
#     python main.py c a \
#         < cello.ly \
#         > guitar.ly
#
# この例では
#
#     c調基準 → a調基準
#
# の移調を行う。

import sys

from tokenizer import Tokenizer
from transpose import (
    parse_pitch,
    letter_shift_between,
    transpose_tokens,
)
from writer import write_token


def main():
    """
    メイン処理。

    コマンドライン引数:

        argv[1]
            移調元音名

        argv[2]
            移調先音名

    例:

        python main.py c a
    """

    # 引数チェック
    if len(sys.argv) != 3:

        print(
            "usage: python main.py SRC DST",
            file=sys.stderr
        )

        print(
            "example: python main.py c a",
            file=sys.stderr
        )

        sys.exit(1)

    # 移調元音名
    src = sys.argv[1]

    # 移調先音名
    dst = sys.argv[2]

    # 半音移動量を計算する。
    #
    # 例:
    #
    #     c → a
    #
    # なら -3
    #
    shift = (
            parse_pitch(dst)
            -
            parse_pitch(src)
    )

    # 音名文字の移動量を計算する。
    #
    # 例:
    #
    #     c → a
    #
    # なら
    #
    #     c d e f g a
    #
    # なので 5
    #
    letter_shift = letter_shift_between(
        src,
        dst
    )

    # LilyPondソースを標準入力から読む。
    text = sys.stdin.read()

    # Token列へ変換する。
    tokens = Tokenizer(
        text
    ).tokenize()

    # Token列を移調する。
    transpose_tokens(
        tokens,
        shift,
        letter_shift
    )

    # LilyPondソースへ戻して標準出力へ書く。
    for t in tokens:
        sys.stdout.write(
            write_token(t)
        )


# スクリプトとして実行された場合のみ main() を呼ぶ。
if __name__ == "__main__":
    main()
