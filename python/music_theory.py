# music_theory.py
#
# 音名と半音値の相互変換を担当する。
#
# 主な責務:
#
#     音名 → 半音値
#     半音値 → 音名
#     移調後の綴り決定
#     シャープ・フラット処理
#
# MIDIやLilyPondの相対音高は扱わず、
# 純粋な音楽理論部分のみを担当する。
# 音高テーブル
# 音名 → 半音値変換テーブル
#
# 例:
#
#     c    -> 0
#     fis  -> 6
#     bes  -> 10
#     bis  -> 0
#
# ダブルシャープ・ダブルフラットも対応。
NOTE_TO_SEMITONE = {
    "ces": 11,
    "c": 0,
    "cis": 1,
    "des": 1,
    "d": 2,
    "dis": 3,
    "ees": 3,
    "es": 3,
    "e": 4,
    "eis": 5,
    "fes": 4,
    "f": 5,
    "fis": 6,
    "ges": 6,
    "g": 7,
    "gis": 8,
    "ases": 7,
    "as": 8,
    "a": 9,
    "ais": 10,
    "beses": 8,
    "bes": 10,
    "b": 11,
    "bis": 0,
}
NOTE_TO_SEMITONE.update({
    # "bis": 0,
    "cisis": 2,
    "disis": 5,
    "eisis": 6,
    "fisis": 7,
    "gisis": 9,
    "aisis": 11,

    "ceses": 10,
    "deses": 0,
    "eeses": 2,
    "feses": 3,
    "geses": 5,
    "aseses": 6,
    "beses": 8,
})
# 音名文字(c,d,e...)のインデックス
#
# 文字移調量(letter_shift)計算で使用する。
LETTER_INDEX = {
    "c": 0,
    "d": 1,
    "e": 2,
    "f": 3,
    "g": 4,
    "a": 5,
    "b": 6,
}
# 半音値から代表的なシャープ系表記へ変換する。
#
# 例:
#
#     3 -> dis
#     8 -> gis
COMMON_PC_TO_NOTE = {
    0: "c",
    1: "cis",
    2: "d",
    3: "dis",
    4: "e",
    5: "f",
    6: "fis",
    7: "g",
    8: "gis",
    9: "a",
    10: "ais",
    11: "b",
}
# 半音値から代表的なフラット系表記へ変換する。
#
# 例:
#
#     3 -> es
#     10 -> bes
SEMITONE_TO_NOTE = {
    0: "c",
    1: "cis",
    2: "d",
    3: "es",
    4: "e",
    5: "f",
    6: "fis",
    7: "g",
    8: "as",
    9: "a",
    10: "bes",
    11: "b",
}
# 自然音(c,d,e,f,g,a,b)の半音値。
#
# 臨時記号(accidental)計算の基準として使用する。
LETTER_TO_NATURAL_PC = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}
# 音名の並び順。
#
# 文字移調(letter_shift)の計算で使用する。
LETTERS = ["c", "d", "e", "f", "g", "a", "b"]


def transpose_note_name_by_interval(
        old_note,
        semitone_shift,
        letter_shift
):
    """
    音名を移調する。

    入力:

        old_note
            元の音名

        semitone_shift
            半音移動量

        letter_shift
            音名文字の移動量

    例:

        c -> a

    の場合

        semitone_shift = -3
        letter_shift = 5

    を使い、

        c → a
        d → b
        e → cis

    のような綴りを決定する。
    """
    old_letter = old_note[0]

    new_letter = LETTERS[
        (
                LETTERS.index(old_letter)
                + letter_shift
        ) % 7
        ]

    old_pc = NOTE_TO_SEMITONE[old_note]
    new_pc = (old_pc + semitone_shift) % 12

    natural_pc = LETTER_TO_NATURAL_PC[new_letter]

    acc = (new_pc - natural_pc) % 12

    if acc > 6:
        acc -= 12

    note = note_from_letter_acc(
        new_letter,
        acc
    )

    return simplify_spelling(note)


def transpose_pitch(
        note,
        shift
):
    """
    音名を半音数だけ移調する。

    綴りは考慮せず、
    SEMITONE_TO_NOTE を用いて
    単純変換する。

    主に \\relative 外の処理で使用。
    """
    pc = NOTE_TO_SEMITONE[note]

    return SEMITONE_TO_NOTE[
        (pc + shift) % 12
        ]


def simplify_spelling(note):
    """
    音名を簡略表記へ変換する。

    例:

        disis -> f
        beses -> gis

    ダブルシャープ・ダブルフラットを
    避けるために使用する。
    """
    pc = NOTE_TO_SEMITONE[note]

    # ダブルシャープ・ダブルフラットを避ける
    if "isis" in note or "eses" in note:
        return COMMON_PC_TO_NOTE[pc]

    return note


def note_from_letter_acc(letter, acc):
    """
    音名文字と臨時記号数から
    LilyPond音名を生成する。

    例:

        ("c", 0)  -> c
        ("c", 1)  -> cis
        ("c", 2)  -> cisis
        ("b",-1)  -> bes
        ("a",-2)  -> ases
    """
    if acc == 0:
        return letter

    if acc == 1:
        return letter + "is"

    if acc == 2:
        return letter + "isis"

    if acc == -1:
        if letter == "a":
            return "as"
        if letter == "e":
            return "es"
        if letter == "b":
            return "bes"
        return letter + "es"

    if acc == -2:
        if letter == "a":
            return "ases"
        if letter == "e":
            return "eses"
        if letter == "b":
            return "beses"
        return letter + "eses"

    raise ValueError(
        f"unsupported accidental: {letter}, {acc}"
    )


def split_note_name(note):
    """
    LilyPond音名を

        文字部分
        臨時記号数

    に分解する。

    例:

        fis   -> ("f", 1)
        bes   -> ("b",-1)
        ases  -> ("a",-2)
        c     -> ("c", 0)
    """
    letter = note[0]
    rest = note[1:]

    if rest == "":
        acc = 0

    elif rest == "is":
        acc = 1

    elif rest == "isis":
        acc = 2

    elif note == "as":
        letter = "a"
        acc = -1

    elif note == "ases":
        letter = "a"
        acc = -2

    elif note == "es":
        letter = "e"
        acc = -1

    elif note == "eses":
        letter = "e"
        acc = -2

    elif note == "bes":
        letter = "b"
        acc = -1

    elif note == "beses":
        letter = "b"
        acc = -2

    elif rest == "es":
        acc = -1

    elif rest == "eses":
        acc = -2

    else:
        raise ValueError(
            f"bad accidental: {note}"
        )

    return letter, acc


def note_base_midi(note):
    """
    音名の基準MIDI値を返す。

    c を MIDI 60 として計算する。

    例:

        c    -> 60
        d    -> 62
        fis  -> 66
        bes  -> 70

    オクターブは含まない。
    """
    letter, acc = split_note_name(note)

    return (
            60
            + LETTER_TO_NATURAL_PC[letter]
            + acc
    )