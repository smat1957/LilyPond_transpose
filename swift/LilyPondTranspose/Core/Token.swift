import Foundation

indirect enum Token: Equatable {
    case raw(String)
    case comment(String)
    case command(String)
    case symbol(String)
    case note(note: String, octave: String, suffix: String)
    case chord(items: [Token], suffix: String)
    case relative(anchor: String, tokens: [Token])
    case parallel(voices: [[Token]])
    case key(note: String, mode: String)
}
