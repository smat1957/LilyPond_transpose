import sys

from tokenizer import *
from transpose import *
from writer import *

src=sys.argv[1]
dst=sys.argv[2]

shift=(
    parse_pitch(dst)
    -
    parse_pitch(src)
)

letter_shift = letter_shift_between(src, dst)

text=sys.stdin.read()

tokens=Tokenizer(
    text
).tokenize()

#for t in tokens:
#    print(type(t), file=sys.stderr)
#    if isinstance(t, RelativeBlock):
#
#        print("anchor=", t.anchor, file=sys.stderr)
#        print("count =", len(t.tokens), file=sys.stderr)

transpose_tokens(
    tokens,
    shift,
    letter_shift
)

for t in tokens:
    sys.stdout.write(
        write_token(t)
    )
