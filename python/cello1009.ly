celloPrelude = \relative c {
    %\tempo 4 = 72
    \key c \major
    \time 3/4
%1
    \phrasingSlurDown
    c'8 b16 a g f e d c( g) e g c,4\fermata (
    c16) d^(\( e\) f g\( a b c\)^)
    d( c b a g) a(\( b\) c d\( e f d\))
    e( f e d c) d^(\( e\) f g\( a b c\)^)
    d( c b a g) a^(\( b\) c d\( e f d\)^)
    e( f e d c) c b a g f e d
    c b'( c d) e( d c b) a( c) g( c)
%8
    fis, e( fis g) a( g fis e) d( fis) c( fis)
    b, a'( b c) d( c b a) g( b) fis( b)
    e, d( e fis) g( fis e d) c( e) b( e)
    a, g'( a b) c( b a g) fis( a) e( a)
%12
    d, c( d e) fis( e d c) b( d) a( d)
    g, d'( e) fis g a b c d( c b a)
    b( c d c b) a g( a) b( a g f)
    e( g e cis a) b( c) d e( f g e)
%16
    f( d' a f d) e( f) g a( b c a)
    b( d b gis e) fis( gis) a b( c d b)
    c( d c b a) f( e) d c b a( g)
%19
    f\(^( a b cis d e f^) d\)( b'\( gis a d,\))
    e,( b' d) a' gis( b) e, gis b( d c g)
    a dis,( a') b( a) dis,( a') b( a) dis,( a' b)
%22
    c e,( a) b( c) e,( a) b( c) e,( b' c)
    d e,( b') c( d) e,( b') c( d) b( gis fis)
    e c'( a) gis( a) c( a) gis( a) c( a fis)
%25
    dis c'( a) gis( a) c( a) gis( a) c( a f)
    d b'( gis) fis( gis) b( f) e( f) b( e, d)
    c( a) c e c( a) c( e) a( c a e)
%28
    c( a) c e c( a) c( e) a( c a f)
    d( b) d g d( b) d( g) b( d b g)
    f( b,) f' g f( b,) f'( g) f( d' b g)
    e( c) e g e( c) e( g) bes( d bes g)
%32
    e( c) e g e c e g c( bes a g)
    a f( e f g a b c) d( a f d)
    g e( d e f g a b) c( g e c)
    f d f( g f) d f( g f) c f( g
%36
    f) b, f'( g f) a, f'( g f) g,( f' g)
    e g, c,( g' e' g,) c,( g' e' d c b)
    a e' c'( e, a, e') c'( e, a, g' f e)
    f a, d,( a' f' a,) d,( a' f' e d c)
%40
    b fis' d'( fis, b, fis') d'( fis, b, a' g fis)
    g b, e,( b' g' b,) e,( b' g' f e d)
    c g' e'( g, c, g') e'( g, c,) bes' a( g)
    a c, f,( c' a' c,) f,( c' a') g f( e)
%44
    d a' f'( a, d, a') f'( a, d, a' b c)
    g,( b') f'( b,) g,( b') f'( b,) g,( b') f'( b,)
    g,( c') e( c) \once \override TextScript.staff-padding = #2
g,^\markup \italic "sim. sempre"  c' e c g, c' e c
    g, c' d c g, b' d b g, a' d a
%48
    g, b' d b g, b' g' b, g, b' d b
    g, b' c b g, a' c a g, g' c g
    g, a' c a g, a' f' a, g, a' c a
    g, a' b a g, g' b g g, f' b f
%52
    g, g' b g g, g' e' g, g, g' b g
    g, g' a g g, f' a f g, e' a e
    g, f' a f g, f' d' f, g, f' a f
    g, f' b f g, f' d' f, g, f' b f
%56
    g, e' c' e, g, e' e' e, g, e' c' e,
    g, f' b f g, f' d' f, g, f' b f
    g, es' c' es, g, es' es' es, g, es' c' es,
    g, fis' c' fis, g, d' c' d, g, e' c' e,
%60
    g,( fis') c'( fis,) g,( e') c'( e,) g,( fis') c'( fis,)
    g, g' b( a g f e d) g e g( d)
    g cis,( g') a( g) cis,( g') a( g) cis,( g' a)
%63
    f d a'( g f e d c) f d f( c)
    f b,( f') g( f) b,( f') g( f) b,( f' g)
    e c g'( f e d c b) c a c( g)
    c fis,( c') d( c) fis,( c') d( c) fis,( c' d)
%67
    b g( b) d( b) g( b) d( b) f( b d)
    bes e,( bes') c( bes) e,( bes') c( bes) e,( bes' c)
    a f( a) c( a) f( a) c( a) e( a c)
    b d,( b') f'( b,) d,( b') f'( b,) d,( b' f')
%71
    e c,( d) e f g a b c d e( f)
    g( e) c d e f g a bes( a) bes g
    a( f) d e f g a b c( b) c a
    b( g) e f g a b c d( c) d b
%75
    c( a) f g a b c d e( d) e c
    b( a b) g f( e f) d b^(\( a\) b\(^) g\)
    <f g d' b'>4 r r
    e16 c'' b a g f e d c g e g
%79
    \acciaccatura es<es g g' a>4 r r
    \acciaccatura d8<d g f' b>4 r r
    \acciaccatura c8<c g' e' c'>4 <g' d'~ c'(>4 <d' b')>4
    <c, g' e' c'~>4 c''16 e, c' d c e,( c' d)
    <c,, g' e' bes'~>4 bes''16 e, bes' c bes e,( bes' c)
%84
    <c,, a' f' a~>4 a''16 f( e f) a f( e f)
    <c, as' d~ b'~>4 <d' b'>16 <e c'(> <d b'> <e c'> <d b'> <e c'> <d b'> <e c')>
    <d b'(>2\trill s8 \grace { a'16 b) } s8
    c8 b16 a g f e d c( g) e g
    \slashedGrace c,8( <c) g' e' c'>4 r r
    \bar "|."
  }
