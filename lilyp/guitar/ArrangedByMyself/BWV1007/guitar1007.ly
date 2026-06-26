celloPrelude = \relative g {

    \key d \major
    \time 4/4
%1
    d16( a' fis') e fis( a, fis' a,) d,( a' fis') e fis( a, fis' a,)
    d,( b' g')  fis g( b, g' b,) d,( b' g') fis g( b, g' b,)
    d,( cis' g') fis g( cis, g' cis,) d,( cis' g') fis g( cis, g' cis,)
    d,( d' fis) e fis( d fis d) d,( d' fis) e fis( d fis cis)
%5
    \phrasingSlurDown
    d,( b' fis') e fis( d\( cis\) d b) d(\( cis\) d fis, a\( gis fis\))
    gis( d' e) d e( d e d) gis,( d' e) d e( d e d)
    cis( e a) gis a( e\( d\) e cis) e(\( d\) e a,) cis^( b\( a\)^)
    b,( fis' d') cis d( fis, d' fis,) b,( fis' d') cis d( fis, d' fis,)
    b,( gis' a) b a( gis fis e) d'( cis b) a' gis( fis e d)
    cis( b a) a' e a cis, e a,(\( b cis\) e) d( cis\( b a\))
%11
    \once \override TextScript.extra-offset = #'(0 . -1)dis--_\markup \italic "espr." a( c) b c( a) dis( a) fis' a,( c) b c( a) dis( a)
    g( b e) fis g e( b a) g( b e fis g) e( cis b)
    ais( cis ais) cis e( cis e cis) ais( cis ais) cis e( cis e cis)
    d( cis b) d cis d( e) cis d cis( b) a g fis e d
%15
    cis( g' a) g a( g a g) cis,( g' a) g a( g a g)
    d( fis c') b c( fis, c' fis,) d( fis c') b c( fis, c' fis,)
    d( g b) a b( g b g) d( g b) a b( g b g)
    d( cis' g') fis g( cis, g' cis,) d,( cis' g') fis g( cis, g' cis,)
    d,( a' fis') e fis d( cis) b a g fis e d cis b( a)
    gis( e' b'\( cis d\)) b( cis d) gis,,( e' b'\( cis d\)) b( cis d)
%21
    g,,^( e' a\( b cis\)^) g( b cis) g,( e' a\( b cis\)) a( b cis)
    g,^(\( e' a\) cis^) e( gis) a8\fermata r16 e,(\( fis g a b cis d)
    e\)( cis\( a) b( cis  d e fis) g\)( e\( cis) d( e fis g a)\)
    \once \override TextScript.extra-offset = #'(0 . -1)bes(--_\markup \italic "espr."
    a gis a) a( g fis g) g( e cis b a) e( fis g)
%25
    a,( e' a) cis e( fis g e) fis( d a g fis) d e( fis)
    a,(\( d fis a\) d)\( e( fis d)\) g ( fis e f) f( e dis e)
    e( d cis d) d( b gis fis) e( gis b d e) gis( a gis)
    a( e cis) b cis e( a,) cis e, a( gis) fis e d cis b
    a8 g''16( fis e d cis b a) g'( fis e d cis b a
    g) fis'( e d cis b a g fis) e'( d cis b a g fis
%31
    e) d'( cis b cis e) a,( e') b( e) cis( e) d( e) b( e)
    cis( e) a,( e') d( e) b( e) cis( e) a,( e') d( e) b( e)
    cis( e) a,( e') b( e) cis( e) <<{\voiceOne \slurDown r16 e[ r e] r e[ r e]}{\new Voice{\voiceTwo d16[ r e] r fis[ r fis16.] r32}}>>\oneVoice
    <<{\voiceOne \slurDown r16 e[ r e] r e[ r e] r e[ r e] r e[ r e]}{\new Voice{\voiceTwo e16.[ r32 fis16.] r32 g16.[ r32 a,16] r16 fis'[ r g] r a[ r fis] r}}>>\oneVoice
    <<{\voiceOne \slurDown r16 e[ r e] r e[ r e] r e[ r e] r e[ r e]}{\new Voice{\voiceTwo g16[ r fis16] r g16[ r e16.] r32 fis16.[ r32 e16.] r32 fis16.[ r32 d16] r}}>>\oneVoice
    <<{\voiceOne \slurDown r16 e[ r e] r e[ r e] }{\new Voice{\voiceTwo e16[ r d] r e[ r cis] r}}>>\oneVoice d16( e) cis( e) d( e) b( e)
%37
    cis16 e a,( b c a) cis( a) d( a) dis( a) e'( a,) f'( a,)
    fis'16( a,) g'16.( a,32) gis'16.( a,32) a'16.( a,32)
    <<{\voiceOne \slurDown bes'16. r32 b8[ c cis]}{\new Voice{\voiceTwo r16 a,[ r a] r a[ r a]}}>>\oneVoice \break
%39
    d'16( fis, a,) fis' d'( fis,) d'( fis,) d'( fis, a,) fis' d'( fis,) d'( fis,)
    d'16( e, a,) e' d'( e,) d'( e,) d'( e, a,) e' d'( e,) d'( e,) \break
    cis'16( g a,) g' cis( g) cis( g) cis( g a,) g' cis16.( g32) cis16.( g32)
    \acciaccatura<a, d,>8(\( <d' fis, d,>1\)) \bar "|."
  
}
