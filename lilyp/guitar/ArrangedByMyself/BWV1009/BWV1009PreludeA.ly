\version "2.26.0"

\paper {
  top-margin = 15
}

\header {
  title = "Prelude from BWV1009"
  composer = "Johann Sebastian Bach"
  arranger = "arr. by Shusei Matoike"
  %date = "2026年6月25日"
  tagline = "The arranger's name should be mentioned in concert programs.(Arranged on 2026/06/25)"
}

\include "guitar1009A.ly"

  celloPreludeC = {
    \clef "bass"
    \celloPrelude
  }

  guitarPreludeC =  {
          %\tempo \markup \italic "6th string tuned to D"
          \clef "treble_8"
          \transpose c c' \celloPrelude
  }

  guitarPreludeA =  {
         \once \override Score.MetronomeMark.padding = #2.8
         \tempo \markup {
             \concat {
             %\italic "Drop D tuning     "
             \note { 4 } #1
             " = ca. 72"
           }
         }
          %\tempo \markup \italic "Drop D tuning"
          \clef "treble_8"
          %\transpose c d \celloPrelude
          \celloPrelude
  }
  guitarPreludeD =  {
         \tempo \markup {
             \concat {
             \italic "Drop D tuning     "
             \note { 4 } #1
             " = ca. 72"
           }
         }
          %\tempo \markup \italic "Drop D tuning"
          \clef "treble_8"
          %\transpose c d \celloPrelude
          \celloPrelude
  }
  guitarPreludeG =  {
          \tempo \markup \italic "normal tuning"
          \clef "treble_8"
          \transpose c g \celloPrelude
  }

\score {
  %\new Staff  \with { instrumentName = "Cello" } {
  \new Staff  \with { instrumentName = "Guitar" } {
     \guitarPreludeA
     %\celloPreludeC
  }
}
