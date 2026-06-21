from dataclasses import dataclass


@dataclass
class Token:
    pass


@dataclass
class RelativeBlock(Token):
    anchor: str
    tokens: list


@dataclass
class RawToken(Token):
    text: str


@dataclass
class CommentToken(Token):
    text: str


@dataclass
class CommandToken(Token):
    text: str


@dataclass
class NoteToken(Token):
    note: str
    octave: str
    suffix: str


@dataclass
class ChordToken(Token):
    items: list
    suffix: str


@dataclass
class SymbolToken(Token):
    text: str


@dataclass
class ParallelBlock(Token):
    voices: list


@dataclass
class KeyToken(Token):
    key: str
    mode: str
