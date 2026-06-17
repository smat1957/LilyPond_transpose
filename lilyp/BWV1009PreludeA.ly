\version "2.26.0"

\paper {
  top-margin = 15
}

\header {
  title = "Prelude (BWV1009)"
  composer = "Johann Sebastian Bach"
  arranger = "edt. by Shusei Matoike"
}

\include "guitar/guitar1009A.ly"

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
          %\tempo \markup \italic "normal tuning"
          \clef "treble_8"
          \transpose c a \celloPrelude
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
     \guitarPreludeD
     %\celloPreludeC
  }
}
