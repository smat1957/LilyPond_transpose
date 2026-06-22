# music_theory.py

# 音高テーブル
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
    "bis": 0,
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

LETTER_INDEX = {
    "c": 0,
    "d": 1,
    "e": 2,
    "f": 3,
    "g": 4,
    "a": 5,
    "b": 6,
}

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

LETTER_TO_NATURAL_PC = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}

LETTERS = ["c", "d", "e", "f", "g", "a", "b"]


def transpose_note_name_by_interval(
        old_note,
        semitone_shift,
        letter_shift
):
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
    pc = NOTE_TO_SEMITONE[note]

    return SEMITONE_TO_NOTE[
        (pc + shift) % 12
        ]


def simplify_spelling(note):
    pc = NOTE_TO_SEMITONE[note]

    # ダブルシャープ・ダブルフラットを避ける
    if "isis" in note or "eses" in note:
        return COMMON_PC_TO_NOTE[pc]

    return note


def note_from_letter_acc(letter, acc):
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
    letter, acc = split_note_name(note)

    return (
            60
            + LETTER_TO_NATURAL_PC[letter]
            + acc
    )