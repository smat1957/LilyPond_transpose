# pitch.py
from dataclasses import dataclass


@dataclass
class PitchPos:
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
    note, marks = split_pitch(pitch)

    octave = (
            marks.count("'")
            - marks.count(",")
    )

    return make_pos(note, octave)

def make_pos(note, octave):

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
    return note[0]


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