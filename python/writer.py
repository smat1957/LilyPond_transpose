from tokens import *


def write_token(t):
    if isinstance(t, RawToken):
        return t.text
    elif isinstance(t, CommandToken):
        return t.text
    elif isinstance(t, KeyToken):
        return (
                "\\key "
                + t.key
                + " \\"
                + t.mode
        )
    elif isinstance(t, CommentToken):
        return t.text
    elif isinstance(t, SymbolToken):
        return t.text
    elif isinstance(t, NoteToken):
        return (
                t.note
                + t.octave
                + t.suffix
        )
    elif isinstance(t, ChordToken):
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
        return (
                "<<"
                + "".join(
            "{"
            + "".join(write_token(x) for x in voice)
            + "}"
            for voice in t.voices
        )
                + ">>"
        )

    raise TypeError(type(t))
