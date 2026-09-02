import Foundation

enum MusicTheory {
    static let letters = ["c", "d", "e", "f", "g", "a", "b"]
    static let noteNames = [
        "beses", "ases", "ees", "eis", "ces", "fes", "cis", "des", "dis",
        "es", "fis", "ges", "gis", "as", "ais", "bes", "c", "d", "e", "f", "g", "a", "b"
    ].sorted { $0.count > $1.count }

    static let noteToSemitone: [String: Int] = [
        "ces": 11, "c": 0, "cis": 1, "des": 1, "d": 2, "dis": 3, "ees": 3,
        "es": 3, "e": 4, "eis": 5, "fes": 4, "f": 5, "fis": 6, "ges": 6,
        "g": 7, "gis": 8, "ases": 7, "as": 8, "a": 9, "ais": 10, "beses": 8,
        "bes": 10, "b": 11, "bis": 0, "cisis": 2, "disis": 5, "eisis": 6,
        "fisis": 7, "gisis": 9, "aisis": 11, "ceses": 10, "deses": 0,
        "eeses": 2, "feses": 3, "geses": 5, "aseses": 6
    ]
    static let naturalPC = ["c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11]
    static let flatSpelling = ["c", "cis", "d", "es", "e", "f", "fis", "g", "as", "a", "bes", "b"]
    static let sharpSpelling = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]

    static func splitPitch(_ pitch: String) throws -> (note: String, marks: String) {
        guard let name = noteNames.first(where: { pitch.hasPrefix($0) }) else { throw TransposeError.invalidPitch(pitch) }
        let marks = String(pitch.dropFirst(name.count))
        guard marks.allSatisfy({ $0 == "'" || $0 == "," }) else { throw TransposeError.invalidPitch(pitch) }
        return (name, marks)
    }

    static func parsePitch(_ pitch: String) throws -> Int {
        let value = try splitPitch(pitch)
        guard let pc = noteToSemitone[value.note] else { throw TransposeError.invalidPitch(pitch) }
        return 60 + pc + (value.marks.filter { $0 == "'" }.count - value.marks.filter { $0 == "," }.count) * 12
    }

    static func letterShift(from source: String, to destination: String) throws -> Int {
        let sourceNote = try splitPitch(source).note
        let destinationNote = try splitPitch(destination).note
        guard let sourceIndex = letters.firstIndex(of: String(sourceNote.prefix(1))),
              let destinationIndex = letters.firstIndex(of: String(destinationNote.prefix(1))) else {
            throw TransposeError.invalidPitch("\(source) → \(destination)")
        }
        return (destinationIndex - sourceIndex + 7) % 7
    }

    static func transposeNote(_ note: String, semitones: Int, letterShift: Int) throws -> String {
        guard let oldPC = noteToSemitone[note], let oldIndex = letters.firstIndex(of: String(note.prefix(1))) else {
            throw TransposeError.invalidPitch(note)
        }
        let letter = letters[(oldIndex + letterShift) % 7]
        let pc = modulo(oldPC + semitones, 12)
        var accidental = modulo(pc - naturalPC[letter]!, 12)
        if accidental > 6 { accidental -= 12 }
        let result = try noteName(letter: letter, accidental: accidental)
        return result.contains("isis") || result.contains("eses") ? sharpSpelling[pc] : result
    }

    static func transposeSimple(_ note: String, semitones: Int) throws -> String {
        guard let pc = noteToSemitone[note] else { throw TransposeError.invalidPitch(note) }
        return flatSpelling[modulo(pc + semitones, 12)]
    }

    static func noteName(letter: String, accidental: Int) throws -> String {
        switch accidental {
        case 0: return letter
        case 1: return letter + "is"
        case 2: return letter + "isis"
        case -1:
            if letter == "a" { return "as" }; if letter == "e" { return "es" }; if letter == "b" { return "bes" }
            return letter + "es"
        case -2:
            if letter == "a" { return "ases" }; if letter == "e" { return "eses" }; if letter == "b" { return "beses" }
            return letter + "eses"
        default: throw TransposeError.unsupportedAccidental("\(letter), \(accidental)")
        }
    }

    static func noteBaseMIDI(_ note: String) throws -> Int {
        let letter = String(note.prefix(1))
        guard let natural = naturalPC[letter], let pc = noteToSemitone[note] else { throw TransposeError.invalidPitch(note) }
        var accidental = pc - natural
        if accidental > 6 { accidental -= 12 }
        return 60 + natural + accidental
    }

    static func modulo(_ value: Int, _ divisor: Int) -> Int { (value % divisor + divisor) % divisor }
}
