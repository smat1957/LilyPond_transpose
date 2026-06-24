
from tokens import *
from pitch import (
    parse_absolute_pitch_pos,
    make_pos,
    note_letter,
)
from music_theory import (
    LETTER_INDEX,
    note_base_midi,
    transpose_note_name_by_interval,
)

class PitchResolver:
    """
    \\relative ブロック内の音高解決を担当する。

    LilyPond の相対音高規則を解釈し、

        元の音高
            ↓
        移調後の絶対音高
            ↓
        LilyPond相対表記

    に変換する。

    PitchResolver
        \relative 内の直前音を覚えながら
        NoteToken / ChordToken を移調する
    """
    def __init__(self, anchor, letter_shift):
        self.prev_old_pos = parse_absolute_pitch_pos(anchor)
        self.prev_new_pos = None
        self.current_key = "c"
        self.letter_shift = letter_shift

    def transpose_note(self, note_token, shift):
        """
        単音(NoteToken)を移調する。

        相対表記から元の絶対音高を求め、
        指定半音数だけ移調し、
        LilyPondの相対表記へ戻す。
        """
        old_pos = resolve_relative_pitch(
            note_token,
            self.prev_old_pos
        )

        new_midi = old_pos.midi + shift

        new_note = transpose_note_name_by_interval(
            old_pos.note,
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
        """
        和音(ChordToken)を移調する。

        和音内の各音を順番に処理し、
        LilyPondの相対表記を維持したまま
        移調結果へ書き換える。
        """
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

            new_midi = old_pos.midi + shift

            new_note = transpose_note_name_by_interval(
                old_pos.note,
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


def resolve_relative_pitch(note_token, prev_pos):
    """
    NoteToken を絶対音高へ展開する。

    LilyPond の \\relative 規則に従い、
    直前音(prev_pos)から最も近い音域を選ぶ。
    """
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


def lilypond_inferred_octave(prev_pos, note):
    """
    LilyPond の相対音高規則を実装する。

    prev_pos に最も近い音域の note を選び、
    推定オクターブ番号を返す。
    """
    prev_step = (
            prev_pos.octave * 7
            + LETTER_INDEX[prev_pos.letter]
    )

    letter = note_letter(note)
    letter_index = LETTER_INDEX[letter]

    candidates = []

    for octave in range(
            prev_pos.octave - 4,
            prev_pos.octave + 5
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
    """
    絶対音高(MIDI)を
    LilyPond相対表記へ変換する。

    戻り値:
        ("''", PitchPos(...))

    のような
        オクターブ記号
        新しいPitchPos
    の組を返す。
    """
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
