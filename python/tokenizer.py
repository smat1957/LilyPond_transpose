# まず Token 定義
from tokens import *

# 音名定義
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

# 音符読取
import re

NOTE_RE = re.compile(
    r'(?<![A-Za-z0-9_])'
    r'(' +
    '|'.join(NOTE_NAMES) +
    r')'
    r"([,']*)"
    r'(?![A-Za-z])'
)


# Tokenizer
class Tokenizer:

    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.len = len(text)

    def peek(self, n=0):

        p = self.pos + n

        if p >= self.len:
            return ""

        return self.text[p]

    def advance(self):

        ch = self.peek()

        self.pos += 1

        return ch

    # コメント
    def read_comment(self):

        buf = ""

        while self.peek() not in ("", "\n"):
            buf += self.advance()

        return CommentToken(buf)

    # コマンド
    def read_command(self):

        buf = self.advance()

        while (
                self.peek().isalnum()
                or self.peek() == "_"
        ):
            buf += self.advance()

        return CommandToken(buf)

    # 音符
    def read_note(self):

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

    # 和音
    def read_chord(self):

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

    # tokenize
    def tokenize(self):

        result = []

        while self.pos < self.len:

            ch = self.peek()

            if self.text.startswith(
                    "\\relative",
                    self.pos
            ):
                result.append(
                    self.read_relative()
                )
                continue

            if self.text.startswith("<<", self.pos):
                result.append(
                    self.read_parallel()
                )
                continue

            if self.text.startswith(">>", self.pos):
                self.pos += 2
                result.append(SymbolToken(">>"))
                continue

            if ch in "{}":
                result.append(
                    SymbolToken(
                        self.advance()
                    )
                )
                continue

            if ch == "%":
                result.append(
                    self.read_comment()
                )

                continue

            if self.text.startswith("\\key", self.pos):
                result.append(self.read_key())
                continue

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

            if ch == "<":

                if self.peek(1) != "<":
                    result.append(
                        self.read_chord()
                    )

                    continue

            n = self.read_note()

            if n:
                result.append(n)

                continue

            result.append(
                RawToken(
                    self.advance()
                )
            )

        return result

    #
    def read_key(self):

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

    #
    def read_pitch_literal(self):

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

    #
    def read_brace_block(self):

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

    #
    def read_relative(self):

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

    #
    def read_parallel(self):

        self.pos += 2  # skip <<

        voices = []

        while self.pos < self.len:

            while self.peek().isspace():
                self.advance()

            if self.text.startswith(">>", self.pos):
                self.pos += 2
                break

            # { ... }
            if self.peek() == "{":
                self.advance()
                body = self.read_brace_block()

                voices.append(
                    Tokenizer(body).tokenize()
                )
                continue

            # \new Voice { ... }
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

            # fallback
            self.advance()

        return ParallelBlock(voices)
