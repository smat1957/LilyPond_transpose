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

\include "guitar1007.ly"

  isCello = ##f

  celloPreludeG = {
    \tempo \markup {
        \concat {
          \note { 4 } #1
           " = ca. 66-104"
        }
    }
    \clef "bass"
    \keepWithTag #'cello \celloPrelude
  }

  guitarPreludeD = {
    \once \override Score.MetronomeMark.padding = #2.8
    \tempo \markup {
        \concat {
          %\italic "Drop D tuning     "
          \note { 4 } #1
           " = ca. 66-104"
        }
    }
    \clef "treble_8"
    %\transpose g d' {
      %\removeWithTag #'cello \celloPrelude
      \celloPrelude
    %}
  }

\header {
  title = "Prelude from BWV1007"
  composer = "Johann Sebastian Bach"
  arranger = #(if isCello "based on Pablo Casals" "arr. by Shusei Matoike")
  %date = "2026年6月25日"
  tagline = "The arranger's name should be mentioned in concert programs.(Arranged on 2026/06/25)"
}

\score {
  \new Staff \with {
    instrumentName = #(if isCello "Cello" "Guitar")
  }
  {
    #(if isCello
      #{ \celloPreludeG #}
      #{ \guitarPreludeD #})
  }
}
