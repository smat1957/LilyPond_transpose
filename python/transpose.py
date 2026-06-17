import sys
import copy

from tokenizer import (
    NoteToken,
    ChordToken
)
from tokens import (
    NoteToken,
    ChordToken,
    RelativeBlock
)

#音高テーブル
NOTE_TO_SEMITONE = {
    "ces":11,
    "c":0,
    "cis":1,
    "des":1,
    "d":2,
    "dis":3,
    "ees":2,
    "es":3,
    "e":4,
    "eis":5,
    "fes":4,
    "f":5,
    "fis":6,
    "ges":6,
    "g":7,
    "gis":8,
    "ases":7,
    "as":8,
    "a":9,
    "ais":10,
    "beses":8,
    "bes":10,
    "b":11,
}

#
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

#
LETTER_INDEX = {
    "c": 0,
    "d": 1,
    "e": 2,
    "f": 3,
    "g": 4,
    "a": 5,
    "b": 6,
}

#
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
    0:"c",
    1:"cis",
    2:"d",
    3:"es",
    4:"e",
    5:"f",
    6:"fis",
    7:"g",
    8:"as",
    9:"a",
    10:"bes",
    11:"b"
}

#
LETTER_TO_NATURAL_PC = {
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7,
    "a": 9,
    "b": 11,
}
#
SHARP_KEYS = {
    "c": 0,
    "g": 1,
    "d": 2,
    "a": 3,
    "e": 4,
    "b": 5,
    "fis": 6,
    "cis": 7,
}

FLAT_KEYS = {
    "f": 1,
    "bes": 2,
    "es": 3,
    "as": 4,
    "des": 5,
    "ges": 6,
    "ces": 7,
}

SHARP_ORDER = ["f", "c", "g", "d", "a", "e", "b"]
FLAT_ORDER  = ["b", "e", "a", "d", "g", "c", "f"]

MAJOR_STEPS = [0, 2, 4, 5, 7, 9, 11]
LETTERS = ["c", "d", "e", "f", "g", "a", "b"]

#
def note_letter(note):
    return note[0]

def parse_absolute_pitch_pos(pitch):
    note, octave_marks = split_pitch(pitch)

    octave = (
        octave_marks.count("'")
        - octave_marks.count(",")
    )

    letter = note_letter(note)

    return {
        "note": note,
        "letter": letter,
        "octave": octave,
        "midi": parse_pitch(pitch),
    }

def pitch_pos_to_midi(pos):
    return (
        60
        + pos["octave"] * 12
        + NOTE_TO_SEMITONE[pos["note"]]
    )

#
def letter_shift_between(src, dst):
    src_note, _ = split_pitch(src)
    dst_note, _ = split_pitch(dst)

    src_letter = src_note[0]
    dst_letter = dst_note[0]

    return (
        LETTERS.index(dst_letter)
        - LETTERS.index(src_letter)
    ) % 7

#
def simplify_spelling(note):

    pc = NOTE_TO_SEMITONE[note]

    # ダブルシャープ・ダブルフラットを避ける
    if "isis" in note or "eses" in note:
        return COMMON_PC_TO_NOTE[pc]

    return note

#
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

#
NOTE_NAMES = sorted(
    NOTE_TO_SEMITONE.keys(),
    key=len,
    reverse=True
)

def split_pitch(pitch):

    for name in NOTE_NAMES:

        if pitch.startswith(name):

            return (
                name,
                pitch[len(name):]
            )

    raise ValueError(
        f"bad pitch: {pitch}"
    )

#
def major_scale_spelling(key):
    key_note, _ = split_pitch(key)

    tonic_pc = NOTE_TO_SEMITONE[key_note]
    tonic_letter = key_note[0]

    start = LETTERS.index(tonic_letter)

    scale = []

    for i, step in enumerate(MAJOR_STEPS):
        letter = LETTERS[(start + i) % 7]
        pc = (tonic_pc + step) % 12
        scale.append(spell_note(letter, pc))

    return scale

#
'''
def build_key_note_names(key):
    scale = major_scale_spelling(key)

    result = {}

    # まずダイアトニック音を登録
    for note in scale:
        pc = NOTE_TO_SEMITONE[note]
        result[pc] = note

    # 派生音を登録
    #
    # 方針：
    # その調の音階音を半音上げた綴りを優先する
    # 例 A-Dur:
    #   d -> dis
    #   e -> eis
    #   a -> ais
    #
    for note in scale:
        pc = NOTE_TO_SEMITONE[note]

        sharp_note = raise_note_spelling(note)
        sharp_pc = (pc + 1) % 12

        if sharp_pc not in result:
            result[sharp_pc] = sharp_note

        flat_note = lower_note_spelling(note)
        flat_pc = (pc - 1) % 12

        if flat_pc not in result:
            result[flat_pc] = flat_note

    return result
'''
#
def build_key_note_names(key):

    scale = major_scale_spelling(key)

    result = dict(COMMON_PC_TO_NOTE)

    # 音階音だけは、その調の正しい綴りで上書きする
    for note in scale:
        pc = NOTE_TO_SEMITONE[note]
        result[pc] = note

    return result
#
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

#
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

def spell_note(letter, target_pc):
    natural_pc = LETTER_TO_NATURAL_PC[letter]

    delta = (target_pc - natural_pc) % 12

    if delta > 6:
        delta -= 12

    return note_from_letter_acc(
        letter,
        delta
    )

def raise_note_spelling(note):
    letter, acc = split_note_name(note)

    return note_from_letter_acc(
        letter,
        acc + 1
    )


def lower_note_spelling(note):
    letter, acc = split_note_name(note)

    return note_from_letter_acc(
        letter,
        acc - 1
    )

#
KEY_NOTE_NAMES = {
    key: build_key_note_names(key)
    for key in [
        "c", "g", "d", "a", "e", "b", "fis", "cis",
        "f", "bes", "es", "as", "des", "ges", "ces",
    ]
}

#
#KEY_NOTE_NAMES["a"][0] = "bis"
KEY_NOTE_NAMES["a"][0] = "c"
KEY_NOTE_NAMES["e"][0] = "bis"
KEY_NOTE_NAMES["b"][0] = "bis"

#KEY_NOTE_NAMES["d"][5] = "eis"
KEY_NOTE_NAMES["a"][5] = "eis"
KEY_NOTE_NAMES["e"][5] = "eis"
KEY_NOTE_NAMES["b"][5] = "eis"

#KEY_NOTE_NAMES["a"][7] = "fisis"
KEY_NOTE_NAMES["a"][7] = "g"
KEY_NOTE_NAMES["e"][7] = "fisis"
KEY_NOTE_NAMES["b"][7] = "fisis"

#
def note_base_midi(note):
    letter, acc = split_note_name(note)

    return (
        60
        + LETTER_TO_NATURAL_PC[letter]
        + acc
    )

#
def note_letter(note):
    return note[0]

def make_pos(note, octave):

    midi = (
        note_base_midi(note)
        + octave * 12
    )

    return {
        "note": note,
        "letter": note_letter(note),
        "octave": octave,
        "midi": midi,
    }
'''
def make_pos(note, octave):
    midi = (
        60
        + octave * 12
        + NOTE_TO_SEMITONE[note]
    )

    return {
        "note": note,
        "letter": note_letter(note),
        "octave": octave,
        "midi": midi,
    }
'''
def parse_absolute_pitch_pos(pitch):
    note, marks = split_pitch(pitch)

    octave = (
        marks.count("'")
        - marks.count(",")
    )

    return make_pos(note, octave)

#
def semitone_to_note(pc, key=None):

    if key in KEY_NOTE_NAMES:
        return KEY_NOTE_NAMES[key][pc]

    return SEMITONE_TO_NOTE[pc]

#
def transpose_pitch(
    note,
    shift
):

    pc=NOTE_TO_SEMITONE[note]

    return SEMITONE_TO_NOTE[
        (pc+shift)%12
    ]

#
def parse_pitch(pitch):

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

#
def midi_to_relative(
    prev_midi,
    midi,
    current_key
):
    pc = midi % 12

    note = semitone_to_note(
        pc,
        current_key
    )
    
    base = (
        prev_midi // 12
    ) * 12 + pc

    candidates = []

    for k in range(-6, 7):
        candidates.append(
            base + k * 12
        )

    nearest = min(
        candidates,
        key=lambda x: abs(
            x - prev_midi
        )
    )

    diff = midi - nearest

    if diff > 0:
        octave = "'" * (diff // 12)
    elif diff < 0:
        octave = "," * ((-diff) // 12)
    else:
        octave = ""

    #print( "REL",prev_midi,midi,"=>",note,octave,file=sys.stderr)

    return note, octave

#
class PitchResolver:

    def __init__(self, anchor, letter_shift):
        self.prev_old_pos = parse_absolute_pitch_pos(anchor)
        self.prev_new_pos = None
        self.current_key = "c"
        self.letter_shift = letter_shift

    def transpose_note(self, note_token, shift):

        old_pos = resolve_relative_pitch(
            note_token,
            self.prev_old_pos
        )

        new_midi = old_pos["midi"] + shift
                
        new_note = transpose_note_name_by_interval(
            old_pos["note"],
            shift,
            self.letter_shift
        )

        marks, new_pos = midi_to_lilypond_relative_with_note(
            self.prev_new_pos,
            new_midi,
            new_note
        )

        note_token.note = new_note
        note_token.octave = marks

        self.prev_old_pos = old_pos
        self.prev_new_pos = new_pos

    def transpose_chord(self, chord, shift):

        first_old_pos = None
        first_new_pos = None

        chord_old_prev = self.prev_old_pos
        chord_new_prev = self.prev_new_pos

        for item in chord.items:

            if not isinstance(item, NoteToken):
                continue

            old_pos = resolve_relative_pitch(
                item,
                chord_old_prev
            )

            new_midi = old_pos["midi"] + shift
                        
            new_note = transpose_note_name_by_interval(
                old_pos["note"],
                shift,
                self.letter_shift
            )

            marks, new_pos = midi_to_lilypond_relative_with_note(
                chord_new_prev,
                new_midi,
                new_note
            )

            item.note = new_note
            item.octave = marks

            chord_old_prev = old_pos
            chord_new_prev = new_pos

            if first_old_pos is None:
                first_old_pos = old_pos
                first_new_pos = new_pos

        if first_old_pos is not None:
            self.prev_old_pos = first_old_pos
            self.prev_new_pos = first_new_pos
                    
#
def walk_tokens(tokens, resolver, shift, letter_shift):
    i = 0

    while i < len(tokens):

        t = tokens[i]

        if (
            isinstance(t, SymbolToken)
            and t.text == "<<"
        ):
            depth = 1
            j = i + 1

            while j < len(tokens):

                x = tokens[j]

                if (
                    isinstance(x, SymbolToken)
                    and x.text == "<<"
                ):
                    depth += 1

                elif (
                    isinstance(x, SymbolToken)
                    and x.text == ">>"
                ):
                    depth -= 1

                    if depth == 0:
                        break

                j += 1

            inner = tokens[i + 1:j]

            if resolver:
                local_resolver = copy.deepcopy(
                    resolver
                )
            else:
                local_resolver = None
                
            walk_tokens(
                inner,
                local_resolver,
                shift,
                letter_shift
            )

            i = j + 1
            continue

        if isinstance(t, RelativeBlock):

            transpose_relative_block(
                t,
                shift,
                letter_shift
            )

        elif isinstance(t, NoteToken):

            if resolver:
                resolver.transpose_note(
                    t,
                    shift
                )
            else:
                t.note = transpose_pitch(
                    t.note,
                    shift
                )

        elif isinstance(t, ChordToken):

            if resolver:
                resolver.transpose_chord(
                    t,
                    shift
                )
            else:
                for item in t.items:
                    if isinstance(item, NoteToken):
                        item.note = transpose_pitch(
                            item.note,
                            shift
                        )

        elif isinstance(t, KeyToken):

            old_key = t.key

            new_key = transpose_pitch(
                old_key,
                shift
            )

            t.key = new_key

            if resolver:
                resolver.current_key = new_key
                                    
        elif isinstance(t, ParallelBlock):

            for voice in t.voices:

                if resolver:
                    local_resolver = copy.deepcopy(
                        resolver
                    )
                else:
                    local_resolver = None

                walk_tokens(
                    voice,
                    local_resolver,
                    shift,
                    letter_shift
                )
        
        elif isinstance(t, ParallelBlock):

            for voice in t.voices:
                local = copy.deepcopy(resolver)
                walk_tokens(voice, local, shift)
        
        i += 1

#
def transpose_relative_block(block, shift, letter_shift):

    old_anchor = block.anchor

    resolver = PitchResolver(
        old_anchor,
        letter_shift
    )

    block.anchor = midi_to_absolute_lily(
        parse_pitch(old_anchor) + shift
    )

    resolver.prev_new_pos = parse_absolute_pitch_pos(
        block.anchor
    )

    walk_tokens(
        block.tokens,
        resolver,
        shift,
        letter_shift
    )
    
#
from tokens import *
def transpose_tokens(tokens, shift, letter_shift):

    walk_tokens(
        tokens,
        None,
        shift,
        letter_shift
    )

#
def lilypond_inferred_octave(prev_pos, note):
    prev_step = (
        prev_pos["octave"] * 7
        + LETTER_INDEX[prev_pos["letter"]]
    )

    letter = note_letter(note)
    letter_index = LETTER_INDEX[letter]

    candidates = []

    for octave in range(
        prev_pos["octave"] - 4,
        prev_pos["octave"] + 5
    ):
        step = octave * 7 + letter_index
        diff = step - prev_step

        candidates.append(
            (octave, diff)
        )

    octave, diff = min(
        candidates,
        key=lambda x: (
            abs(x[1]),
            x[1]
        )
    )

    return octave

#
def resolve_relative_pitch(note_token, prev_pos):
    note = note_token.note

    octave = lilypond_inferred_octave(
        prev_pos,
        note
    )

    octave += (
        note_token.octave.count("'")
        - note_token.octave.count(",")
    )

    return make_pos(note, octave)

#
def midi_to_absolute_lily(midi):

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

#
def midi_to_lilypond_relative(prev_pos, midi, current_key):
    pc = midi % 12

    note = semitone_to_note(
        pc,
        current_key
    )

    abs_octave = (
        midi
        - (60 + NOTE_TO_SEMITONE[note])
    ) // 12

    inferred_octave = lilypond_inferred_octave(
        prev_pos,
        note
    )

    diff = abs_octave - inferred_octave

    if diff > 0:
        marks = "'" * diff
    elif diff < 0:
        marks = "," * (-diff)
    else:
        marks = ""

    return note, marks, make_pos(note, abs_octave)

#
def midi_to_lilypond_relative_with_note(
    prev_pos,
    midi,
    note
):
    abs_octave = (
        midi
        - note_base_midi(note)
    ) // 12

    inferred_octave = lilypond_inferred_octave(
        prev_pos,
        note
    )

    diff = abs_octave - inferred_octave

    if diff > 0:
        marks = "'" * diff
    elif diff < 0:
        marks = "," * (-diff)
    else:
        marks = ""

    return marks, make_pos(note, abs_octave)
'''
def midi_to_lilypond_relative_with_note(
    prev_pos,
    midi,
    note
):
    abs_octave = (
        midi
        - (60 + NOTE_TO_SEMITONE[note])
    ) // 12

    inferred_octave = lilypond_inferred_octave(
        prev_pos,
        note
    )

    diff = abs_octave - inferred_octave

    if diff > 0:
        marks = "'" * diff
    elif diff < 0:
        marks = "," * (-diff)
    else:
        marks = ""

    return marks, make_pos(note, abs_octave)
'''
