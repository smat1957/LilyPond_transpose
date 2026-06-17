\version "2.26.0"

\paper {
  top-margin = 15
}

useTenorClef = ##t
tenorClef =
#(define-music-function () ()
   (if useTenorClef
       #{ \clef tenor #}
       #{ s1*0 #}))
bassClef =
#(define-music-function () ()
   (if useTenorClef
       #{ \clef bass #}
       #{ s1*0 #}))

\include "guitar/guitar1010.ly"

  isCello = ##f

  celloPreludeEs = {
    \tempo \markup {
        \concat {
          \note { 2 } #1
           " = ca. 40-50"
        }
    }
    \clef "bass"
    \keepWithTag #'cello \celloPrelude
  }

  guitarPreludeC = {
    \tempo \markup {
        \concat {
          %\italic "Drop D tuning     "
          \note { 2 } #1
           " = ca. 40-50"
        }
    }
    \clef "treble_8"
    %\transpose es c' {
      %\removeWithTag #'cello \celloPrelude
      \celloPrelude
    %}
  }

\header {
  title = "Prelude (BWV1010)"
  composer = "Johann Sebastian Bach"
  arranger = #(if isCello "based on Pablo Casals" "edt. by Shusei Matoike")
}

\score {
  \new Staff \with {
    instrumentName = #(if isCello "Cello" "Guitar")
  }
  {
    #(if isCello
      #{ \celloPreludeEs #}
      #{ \guitarPreludeC #})
  }
}
