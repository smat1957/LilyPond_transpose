import sys

from tokenizer import Tokenizer
from transpose import (
    parse_pitch,
    letter_shift_between,
    transpose_tokens,
)
from writer import write_token


def main():
    if len(sys.argv) != 3:
        print(
            "usage: python main.py SRC DST",
            file=sys.stderr
        )
        print(
            "example: python main.py c a",
            file=sys.stderr
        )
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]

    shift = (
            parse_pitch(dst)
            -
            parse_pitch(src)
    )

    letter_shift = letter_shift_between(src, dst)

    text = sys.stdin.read()

    tokens = Tokenizer(
        text
    ).tokenize()

    transpose_tokens(
        tokens,
        shift,
        letter_shift
    )

    for t in tokens:
        sys.stdout.write(
            write_token(t)
        )


if __name__ == "__main__":
    main()