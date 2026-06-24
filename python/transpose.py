# transpose.py
'''
transpose.py
    Token列を歩く
'''
import copy
from tokens import *
from music_theory import *
from pitch import *
from relative import PitchResolver


def letter_shift_between(src, dst):
    """
    音名の文字移動量を求める。

    例:
        c -> a  : 5
        c -> d  : 1
        g -> d' : 4

    半音数ではなく、
    c,d,e,f,g,a,b の文字位置の差を返す。
    """
    src_note, _ = split_pitch(src)
    dst_note, _ = split_pitch(dst)

    src_letter = src_note[0]
    dst_letter = dst_note[0]

    return (
            LETTERS.index(dst_letter)
            - LETTERS.index(src_letter)
    ) % 7



def transpose_relative_block(block, shift, letter_shift):
    """
    RelativeBlock 全体を移調する。

    anchor を移調し、
    新しい PitchResolver を作成して
    ブロック内部を再帰的に処理する。
    """
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


def walk_tokens(tokens, resolver, shift, letter_shift):
    # << ... >> を検出したら
    # resolver をコピーして独立に処理する
    """
    Token列を再帰的に走査する。

    処理対象:

        RelativeBlock
        NoteToken
        ChordToken
        KeyToken
        ParallelBlock
        << >> ブロック

    を見つけると適切な移調処理を行う。
    """
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
                # local_resolver = resolver.clone()
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
                    # local_resolver = resolver.clone()
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
    """
    Token列全体を移調する。

    移調処理のエントリポイント。
    """
    walk_tokens(
        tokens,
        None,
        shift,
        letter_shift
    )