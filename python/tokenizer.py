# tokenizer.py
#
# LilyPond のソース文字列を読み取り、
# tokens.py で定義した Token 列へ変換する。
#
# 例:
#
#     c'8 d e
#
# を
#
#     NoteToken("c", "'", "8")
#     RawToken(" ")
#     NoteToken("d", "", "")
#     ...
#
# のような構造に分解する。

# まず Token 定義
from tokens import *

# 音名定義
#
# LilyPond の音名を長い順に並べる。
# 例:
#
#     beses
#     bes
#     b
#
# のような音名では、短い b を先に読むと誤認識するため、
# 必ず長い音名から判定する。
NOTE_NAMES = [
    "beses", "ases", "ees", "eis",
    "ces", "fes",
    "cis", "des", "dis",
    "es",
    "fis", "ges", "gis",
    "as", "ais", "bes",
    "c", "d", "e", "f", "g", "a", "b"
]

NOTE_NAMES.sort(
    key=len,
    reverse=True
)

# 音符読取用の正規表現
#
# 読み取るもの:
#
#     音名
#     オクターブ記号 , '
#
# 例:
#
#     c
#     c'
#     fis,
#     bes''
#
# 前後が英数字や _ の一部である場合は、
# 変数名やコマンド名の一部と見なして音符として読まない。
import re

NOTE_RE = re.compile(
    r'(?<![A-Za-z0-9_])'
    r'(' +
    '|'.join(NOTE_NAMES) +
    r')'
    r"([,']*)"
    r'(?![A-Za-z])'
)


class Tokenizer:
    """
    LilyPond ソース文字列を Token 列へ変換するクラス。

    self.text
        入力文字列

    self.pos
        現在の読み取り位置

    self.len
        入力文字列の長さ
    """

    def __init__(self, text):
        """
        Tokenizer を初期化する。
        """

        self.text = text
        self.pos = 0
        self.len = len(text)

    def peek(self, n=0):
        """
        現在位置から n 文字先を見る。

        文字を読むだけで、self.pos は進めない。
        範囲外なら空文字を返す。
        """

        p = self.pos + n

        if p >= self.len:
            return ""

        return self.text[p]

    def advance(self):
        """
        現在位置の1文字を読み取り、
        self.pos を1文字進める。
        """

        ch = self.peek()

        self.pos += 1

        return ch

    def read_comment(self):
        """
        コメントを読み取る。

        % から行末直前までを
        CommentToken として返す。
        改行文字自体はここでは読まない。
        """

        buf = ""

        while self.peek() not in ("", "\n"):
            buf += self.advance()

        return CommentToken(buf)

    def read_command(self):
        """
        LilyPond コマンドを読み取る。

        例:
            \\clef
            \\time
            \\major

        バックスラッシュから始まり、
        英数字または _ が続く部分を読む。
        """

        buf = self.advance()

        while (
                self.peek().isalnum()
                or self.peek() == "_"
        ):
            buf += self.advance()

        return CommandToken(buf)

    def read_note(self):
        """
        音符を読み取る。

        読み取る内容:

            音名
            オクターブ記号
            後続の suffix

        suffix には、音価・スラー・タイ・装飾などを含める。

        例:
            c'8(
            fis,16~
            bes4\\trill
        """

        m = NOTE_RE.match(
            self.text,
            self.pos
        )

        if not m:
            return None

        self.pos = m.end()

        note = m.group(1)

        octave = m.group(2)

        suffix = ""

        while (
                self.peek()
                and self.peek() not in
                " \t\r\n<>"
        ):
            suffix += self.advance()

        return NoteToken(
            note,
            octave,
            suffix
        )

    def read_chord(self):
        """
        和音 < ... > を読み取る。

        和音内の音符は NoteToken として、
        空白は RawToken として、
        その他の記号は SymbolToken として保持する。

        和音閉じ記号 > の後に続く音価や記号は
        chord の suffix として保持する。
        """

        self.advance()  # '<'

        items = []

        while True:

            if self.peek() == ">":
                self.advance()
                break

            if self.peek().isspace():
                items.append(
                    RawToken(
                        self.advance()
                    )
                )
                continue

            n = self.read_note()

            if n:
                items.append(n)
                continue

            items.append(
                SymbolToken(
                    self.advance()
                )
            )

        suffix = ""

        while (
                self.peek()
                and self.peek() not in
                " \t\r\n"
        ):
            suffix += self.advance()

        return ChordToken(
            items,
            suffix
        )

    def tokenize(self):
        """
        入力文字列全体を Token 列へ変換する。

        処理する主な構文:

            \\relative { ... }
            \\key c \\major
            << ... >>
            < ... >
            コメント
            コマンド
            音符
            その他の生文字列
        """

        result = []

        while self.pos < self.len:

            ch = self.peek()

            # \\relative ブロック
            if self.text.startswith(
                    "\\relative",
                    self.pos
            ):
                result.append(
                    self.read_relative()
                )
                continue

            # 並列ブロック開始
            if self.text.startswith("<<", self.pos):
                result.append(
                    self.read_parallel()
                )
                continue

            # 並列ブロック終了
            if self.text.startswith(">>", self.pos):
                self.pos += 2
                result.append(SymbolToken(">>"))
                continue

            # 波括弧
            if ch in "{}":
                result.append(
                    SymbolToken(
                        self.advance()
                    )
                )
                continue

            # コメント
            if ch == "%":
                result.append(
                    self.read_comment()
                )

                continue

            # 調指定
            if self.text.startswith("\\key", self.pos):
                result.append(self.read_key())
                continue

            # 一般コマンド
            if ch == "\\":

                if self.text.startswith(
                        "\\relative",
                        self.pos
                ):
                    result.append(
                        self.read_relative()
                    )
                    continue

                result.append(
                    self.read_command()
                )
                continue

            # 和音
            if ch == "<":

                if self.peek(1) != "<":
                    result.append(
                        self.read_chord()
                    )

                    continue

            # 単音
            n = self.read_note()

            if n:
                result.append(n)

                continue

            # どの構文にも該当しない文字はそのまま保持する
            result.append(
                RawToken(
                    self.advance()
                )
            )

        return result

    def read_key(self):
        """
        \\key コマンドを読み取る。

        例:
            \\key c \\major
            \\key a \\minor

        戻り値:
            KeyToken(key, mode)
        """

        self.pos += len("\\key")

        while self.peek().isspace():
            self.advance()

        pitch = self.read_pitch_literal()

        if not pitch:
            raise SyntaxError("key pitch expected")

        key = pitch[0] + pitch[1]

        while self.peek().isspace():
            self.advance()

        if self.peek() != "\\":
            raise SyntaxError("key mode expected")

        mode = self.read_command().text[1:]

        return KeyToken(key, mode)

    def read_pitch_literal(self):
        """
        音高リテラルを読み取る。

        NoteToken は作らず、

            (音名, オクターブ記号)

        のタプルを返す。

        \\relative の anchor や
        \\key の調名読み取りに使う。
        """

        m = NOTE_RE.match(
            self.text,
            self.pos
        )

        if not m:
            return None

        self.pos = m.end()

        return (
            m.group(1),
            m.group(2)
        )

    def read_brace_block(self):
        """
        { ... } の中身を文字列として読み取る。

        入れ子の { ... } にも対応する。

        呼び出し時点では、
        開き波括弧 { はすでに読み取り済みであることを前提にする。

        戻り値には、外側の { } は含めない。
        """

        depth = 1

        start = self.pos

        while self.pos < self.len:

            ch = self.advance()

            if ch == "{":
                depth += 1

            elif ch == "}":
                depth -= 1

                if depth == 0:
                    return self.text[start:self.pos - 1]

        raise SyntaxError("missing }")

    def read_relative(self):
        """
        \\relative ブロックを読み取る。

        例:
            \\relative c' { c d e }

        処理内容:

            anchor を読む
            { ... } の中身を読む
            中身を再度 Tokenizer にかける

        戻り値:
            RelativeBlock(anchor, child_tokens)
        """

        self.pos += len("\\relative")

        while self.peek().isspace():
            self.advance()

        pitch = self.read_pitch_literal()

        if not pitch:
            raise SyntaxError(
                "relative anchor expected"
            )

        anchor = pitch[0] + pitch[1]

        while self.peek().isspace():
            self.advance()

        if self.peek() != "{":
            raise SyntaxError(
                "{ expected"
            )

        self.advance()

        body = self.read_brace_block()

        child_tokens = Tokenizer(
            body
        ).tokenize()

        return RelativeBlock(
            anchor,
            child_tokens
        )

    def read_parallel(self):
        """
        並列ブロック << ... >> を読み取る。

        対応する主な形:

            <<
              { voice1 }
              { voice2 }
            >>

        および

            <<
              \\new Voice { voice1 }
              \\new Voice { voice2 }
            >>

        各 voice を個別に tokenize し、
        ParallelBlock として返す。
        """

        self.pos += 2  # skip <<

        voices = []

        while self.pos < self.len:

            while self.peek().isspace():
                self.advance()

            if self.text.startswith(">>", self.pos):
                self.pos += 2
                break

            # { ... } 形式の voice
            if self.peek() == "{":
                self.advance()
                body = self.read_brace_block()

                voices.append(
                    Tokenizer(body).tokenize()
                )
                continue

            # \\new Voice { ... } 形式の voice
            start = self.pos

            if self.text.startswith("\\new", self.pos):

                prefix = ""

                while (
                        self.pos < self.len
                        and self.peek() != "{"
                ):
                    prefix += self.advance()

                if self.peek() != "{":
                    raise SyntaxError(
                        "missing { after \\new Voice"
                    )

                self.advance()
                body = self.read_brace_block()

                voice_tokens = (
                        Tokenizer(prefix).tokenize()
                        + [SymbolToken("{")]
                        + Tokenizer(body).tokenize()
                        + [SymbolToken("}")]
                )

                voices.append(voice_tokens)
                continue

            # 想定外の文字は読み飛ばす
            self.advance()

        return ParallelBlock(voices)
