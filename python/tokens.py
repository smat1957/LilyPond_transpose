# tokens.py
#
# LilyPond ソースを解析した結果を保持する
# Token クラス群を定義する。
#
# tokenizer.py は文字列を Token に変換し、
# transpose.py は Token を移調し、
# writer.py は Token を LilyPond ソースへ戻す。
#
# ここで定義するクラスは、
# LilyPond の構文要素を表現するための
# データ構造である。

from dataclasses import dataclass


@dataclass
class Token:
    """
    全 Token の基底クラス。

    実際には直接生成せず、
    各種 Token クラスの共通親として使う。
    """
    pass


@dataclass
class RelativeBlock(Token):
    """
    \\relative ブロック。

    例:

        \\relative c' {
            c d e
        }

    anchor
        c'

    tokens
        ブロック内部の Token 列
    """
    anchor: str
    tokens: list


@dataclass
class RawToken(Token):
    """
    そのまま出力する文字列。

    主に空白や改行、
    Token 化対象でない文字列を保持する。
    """
    text: str


@dataclass
class CommentToken(Token):
    """
    LilyPond コメント。

    例:

        % Prelude

    % 以降改行直前までを保持する。
    """
    text: str


@dataclass
class CommandToken(Token):
    """
    LilyPond コマンド。

    例:

        \\clef
        \\time
        \\major
        \\tempo

    コマンド名全体を保持する。
    """
    text: str


@dataclass
class NoteToken(Token):
    """
    単音。

    例:

        c'8
        fis,16~
        bes4(

    note
        音名

    octave
        LilyPondオクターブ記号
        (' や ,)

    suffix
        音価やスラー等の後続文字列
    """
    note: str
    octave: str
    suffix: str


@dataclass
class ChordToken(Token):
    """
    和音。

    例:

        <c e g>4

    items
        和音内部の Token 列

    suffix
        > の後ろに続く音価等
    """
    items: list
    suffix: str


@dataclass
class SymbolToken(Token):
    """
    単独の記号。

    例:

        {
        }
        <<
        >>

    構文解析に必要な記号を保持する。
    """
    text: str


@dataclass
class ParallelBlock(Token):
    """
    << ... >> 形式の並列ブロック。

    例:

        <<
            { voice1 }
            { voice2 }
        >>

    voices
        各声部の Token 列のリスト
    """
    voices: list


@dataclass
class KeyToken(Token):
    """
    \\key コマンド。

    例:

        \\key c \\major
        \\key a \\minor

    key
        調名

    mode
        major / minor
    """
    key: str
    mode: str
