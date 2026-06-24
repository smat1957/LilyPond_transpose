# pitch.py
#
# LilyPond の音高表記と内部音高(MIDI)との
# 相互変換を担当するモジュール。
#
# 例:
#
#     c      -> MIDI 60
#     c'     -> MIDI 72
#     fis,   -> MIDI 54
#
# Relative 解決のための PitchPos クラスも定義する。

from dataclasses import dataclass


@dataclass
class PitchPos:
    """
    絶対音高を保持する内部データ。

    note
        LilyPond音名
        例: c, fis, bes

    octave
        c を基準としたオクターブ番号

    letter
        音名の文字部分
        例: c,d,e,f,g,a,b

    midi
        MIDI音高番号
    """
    note: str
    octave: int
    letter: str
    midi: int


from tokenizer import NOTE_NAMES
from music_theory import (
    NOTE_TO_SEMITONE,
    SEMITONE_TO_NOTE,
    note_base_midi,
)


def split_pitch(pitch):
    """
    LilyPond音高文字列を

        音名
        オクターブ記号

    に分解する。

    例:

        c''   -> ("c", "''")
        fis,  -> ("fis", ",")
        bes   -> ("bes", "")
    """
    for name in NOTE_NAMES:

        if pitch.startswith(name):
            return (
                name,
                pitch[len(name):]
            )

    raise ValueError(
        f"bad pitch: {pitch}"
    )


def parse_pitch(pitch):
    """
    LilyPond音高文字列を
    MIDI音高へ変換する。

    例:

        c     -> 60
        c'    -> 72
        fis,  -> 54
    """
    note, octave = split_pitch(
        pitch
    )

    midi = 60 + NOTE_TO_SEMITONE[
        note
    ]

    midi += (
                    octave.count("'")
                    - octave.count(",")
            ) * 12

    return midi


def parse_absolute_pitch_pos(pitch):
    """
    LilyPond音高文字列から
    PitchPos を生成する。

    例:

        c'
            ↓

        PitchPos(
            note='c',
            octave=1,
            ...
        )
    """
    note, marks = split_pitch(pitch)

    octave = (
            marks.count("'")
            - marks.count(",")
    )

    return make_pos(note, octave)

def make_pos(note, octave):
    # 以前は dict を返していたが、
    # 現在は PitchPos を返す。
    """
    音名とオクターブ番号から
    PitchPos を生成する。

    Relative 解決処理の
    基本データ生成関数。
    """
    midi = (
        note_base_midi(note)
        + octave * 12
    )

    return PitchPos(
        note=note,
        octave=octave,
        letter=note_letter(note),
        midi=midi,
    )


def note_letter(note):
    """
    音名から文字部分だけを取り出す。

    例:

        fis -> f
        bes -> b
        c   -> c
    """
    return note[0]


def midi_to_absolute_lily(midi):
    """
    MIDI音高を
    LilyPond絶対表記へ変換する。

    例:

        60 -> c
        72 -> c'
        54 -> fis,

    戻り値は
    \\relative を使わない
    絶対表記である。
    """
    pc = midi % 12
    note = SEMITONE_TO_NOTE[pc]

    octave_count = (midi - (60 + pc)) // 12

    if octave_count > 0:
        octave = "'" * octave_count
    elif octave_count < 0:
        octave = "," * (-octave_count)
    else:
        octave = ""

    return note + octave