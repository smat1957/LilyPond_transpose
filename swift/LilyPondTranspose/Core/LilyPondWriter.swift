import Foundation

enum LilyPondWriter {
    static func write(_ tokens: [Token]) -> String { tokens.map(write).joined() }

    static func write(_ token: Token) -> String {
        switch token {
        case .raw(let text), .comment(let text), .command(let text), .symbol(let text): return text
        case .note(let note, let octave, let suffix): return note + octave + suffix
        case .key(let note, let mode): return "\\key \(note) \\" + mode
        case .chord(let items, let suffix): return "<" + write(items) + ">" + suffix
        case .relative(let anchor, let tokens): return "\\relative \(anchor) {\n" + write(tokens) + "\n}"
        case .parallel(let voices): return "<<" + voices.map { "{" + write($0) + "}" }.joined() + ">>"
        }
    }
}
