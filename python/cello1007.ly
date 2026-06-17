celloPrelude = \relative c {
    \key g \major
    \time 4/4
%1
    g16( d' b') a b( d, b' d,) g,( d' b') a b( d, b' d,)
    g,( e' c')  b c( e, c' e,) g,( e' c') b c( e, c' e,)
    g,( fis' c') b c( fis, c' fis,) g,( fis' c') b c( fis, c' fis,)
    g,( g' b) a b( g b g) g,( g' b) a b( g b fis)
%5
    \phrasingSlurDown
    g,( e' b') a b( g\( fis\) g e) g(\( fis\) g b, d\( cis b\))
    cis( g' a) g a( g a g) cis,( g' a) g a( g a g)
    fis( a d) cis d( a\( g\) a fis) a(\( g\) a d,) fis^( e\( d\)^)
    e,( b' g') fis g( b, g' b,) e,( b' g') fis g( b, g' b,)
    e,( cis' d) e d( cis b a) g'( fis e) d' cis( b a g)
    fis( e d) d' a d fis, a d,(\( e fis\) a) g( fis\( e d\))
%11
    \once \override TextScript.extra-offset = #'(0 . -1)gis--_\markup \italic "espr." d( f) e f( d) gis( d) b' d,( f) e f( d) gis( d)
    c( e a) b c a( e d) c( e a b c) a( fis e)
    dis( fis dis) fis a( fis a fis) dis( fis dis) fis a( fis a fis)
    g( fis e) g fis g( a) fis g fis( e) d c b a g
%15
    fis( c' d) c d( c d c) fis,( c' d) c d( c d c)
    g( b f') e f( b, f' b,) g( b f') e f( b, f' b,)
    g( c e) d e( c e c) g( c e) d e( c e c)
    g( fis' c') b c( fis, c' fis,) g,( fis' c') b c( fis, c' fis,)
    g,( d' b') a b g( fis) e d c b a g fis e( d)
    cis( a' e'\( fis g\)) e( fis g) cis,,( a' e'\( fis g\)) e( fis g)
%21
    c,,^( a' d\( e fis\)^) c( e fis) c,( a' d\( e fis\)) d( e fis)
    c,^(\( a' d\) fis^) a( cis) d8\fermata r16 a,(\( b c d e fis g)
    a\)( fis\( d) e( fis  g a b) c\)( a\( fis) g( a b c d)\)
    \once \override TextScript.extra-offset = #'(0 . -1)es(--_\markup \italic "espr."
    d cis d) d( c b c) c( a fis e d) a( b c)
%25
    d,( a' d) fis a( b c a) b( g d c b) g a( b)
    d,(\( g b d\) g)\( a( b g)\) c ( b a bes) bes( a gis a)
    a( g fis g) g( e cis b) a( cis e g a) cis( d cis)
    d( a fis) e fis a( d,) fis a, d( cis) b a g fis e
    d8 c''16( b a g fis e d) c'( b a g fis e d
    c) b'( a g fis e d c b) a'( g fis e d c b
%31
    a) g'( fis e fis a) d,( a') e( a) fis( a) g( a) e( a)
    fis( a) d,( a') g( a) e( a) fis( a) d,( a') g( a) e( a)
    fis( a) d,( a') e( a) fis( a) <<{\voiceOne \slurDown r16 a[ r a] r a[ r a]}
        \new Voice{\voiceTwo g16[ r a] r b[ r b16.] r32}>>\oneVoice
    <<{\voiceOne \slurDown r16 a[ r a] r a[ r a] r a[ r a] r a[ r a]}
        \new Voice{\voiceTwo a16.[ r32 b16.] r32 c16.[ r32 d,16] r16 b'[ r c] r d[ r b] r}>>\oneVoice
    <<{\voiceOne \slurDown r16 a[ r a] r a[ r a] r a[ r a] r a[ r a]}
        \new Voice{\voiceTwo c16[ r b16] r c16[ r a16.] r32 b16.[ r32 a16.] r32 b16.[ r32 g16] r}>>\oneVoice
    <<{\voiceOne \slurDown r16 a[ r a] r a[ r a] }
      \new Voice{\voiceTwo a16[ r g] r a[ r fis] r}>>\oneVoice g16( a) fis( a) g( a) e( a)
%37
    fis16 a d,( e f d) fis( d) g( d) gis( d) a'( d,) bes'( d,)
    b'16( d,) c'16.( d,32) cis'16.( d,32) d'16.( d,32)
    <<{\voiceOne \slurDown es'16. r32 e8[ f fis]}
      \new Voice{\voiceTwo r16 d,[ r d] r d[ r d]}>>\oneVoice \break
%39
    g'16( b, d,) b' g'( b,) g'( b,) g'( b, d,) b' g'( b,) g'( b,)
    g'16( a, d,) a' g'( a,) g'( a,) g'( a, d,) a' g'( a,) g'( a,) \break
    fis'16( c d,) c' fis( c) fis( c) fis( c d,) c' fis16.( c32) fis16.( c32)
    \acciaccatura<d, g,>8(\( <g' b, g,>1\)) \bar "|."
  }
