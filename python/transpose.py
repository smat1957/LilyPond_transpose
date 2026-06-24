# transpose.py

import copy
from tokens import *
from music_theory import *
from pitch import *


def letter_shift_between(src, dst):
    src_note, _ = split_pitch(src)
    dst_note, _ = split_pitch(dst)

    src_letter = src_note[0]
    dst_letter = dst_note[0]

    return (
            LETTERS.index(dst_letter)
            - LETTERS.index(src_letter)
    ) % 7


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

'''
def parse_absolute_pitch_pos(pitch):
    note, marks = split_pitch(pitch)

    octave = (
            marks.count("'")
            - marks.count(",")
    )

    return make_pos(note, octave)
'''

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

'''
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


def note_letter(note):
    return note[0]
'''

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

'''
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
'''

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
'''

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

        i += 1


def transpose_tokens(tokens, shift, letter_shift):
    walk_tokens(
        tokens,
        None,
        shift,
        letter_shift
    )