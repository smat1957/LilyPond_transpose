# writer.py
#
# Token オブジェクトを LilyPond ソース文字列へ戻す。
#
# tokenizer.py が
#
#     文字列 → Token
#
# を担当するのに対して、このファイルは
#
#     Token → 文字列
#
# を担当する。

from tokens import *


def write_token(t):
    """
    1つの Token を LilyPond ソース文字列へ変換する。

    RawToken, NoteToken, ChordToken, RelativeBlock など、
    Token の種類ごとに元の LilyPond 表記へ戻す。
    """

    if isinstance(t, RawToken):
        # 空白・改行・その他の生文字列はそのまま出力する。
        return t.text

    elif isinstance(t, CommandToken):
        # \clef, \time などのコマンドはそのまま出力する。
        return t.text

    elif isinstance(t, KeyToken):
        # KeyToken を \key c \major の形へ戻す。
        return (
                "\\key "
                + t.key
                + " \\"
                + t.mode
        )

    elif isinstance(t, CommentToken):
        # コメントはそのまま出力する。
        return t.text

    elif isinstance(t, SymbolToken):
        # { }, <<, >> などの記号はそのまま出力する。
        return t.text

    elif isinstance(t, NoteToken):
        # 単音を note + octave + suffix の形で出力する。
        #
        # 例:
        #     note   = c
        #     octave = '
        #     suffix = 8(
        #
        #     => c'8(
        return (
                t.note
                + t.octave
                + t.suffix
        )

    elif isinstance(t, ChordToken):
        # 和音 < ... > を出力する。
        #
        # 和音内部の NoteToken, RawToken, SymbolToken を
        # 順番に文字列化してから、最後に suffix を付ける。
        s = "<"

        for item in t.items:
            if isinstance(item, NoteToken):
                s += (
                        item.note
                        + item.octave
                        + item.suffix
                )

            elif isinstance(item, SymbolToken):
                s += item.text

            elif isinstance(item, RawToken):
                s += item.text

        s += ">"
        s += t.suffix

        return s

    elif isinstance(t, RelativeBlock):
        # \relative ブロックを出力する。
        #
        # 内部 tokens をすべて文字列化して body を作り、
        # \relative anchor { ... } の形に戻す。
        body = "".join(
            write_token(x)
            for x in t.tokens
        )

        return (
                "\\relative "
                + t.anchor
                + " {\n"
                + body
                + "\n}"
        )

    elif isinstance(t, ParallelBlock):
        # << ... >> 形式の並列ブロックを出力する。
        #
        # 各 voice を { ... } で囲んで書き戻す。
        return (
                "<<"
                + "".join(
                    "{"
                    + "".join(
                        write_token(x)
                        for x in voice
                    )
                    + "}"
                    for voice in t.voices
                )
                + ">>"
        )

    # 未対応の Token が来た場合はエラーにする。
    raise TypeError(type(t))
