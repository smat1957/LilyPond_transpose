import Foundation

private struct PitchPosition {
    var note: String
    var octave: Int
    var midi: Int
    var letter: String { String(note.prefix(1)) }
}

private struct RelativeResolver {
    var previousOld: PitchPosition
    var previousNew: PitchPosition
    let letterShift: Int

    init(anchor: String, newAnchor: String, letterShift: Int) throws {
        previousOld = try Self.absolutePosition(anchor)
        previousNew = try Self.absolutePosition(newAnchor)
        self.letterShift = letterShift
    }

    mutating func transpose(note: String, octave: String, shift: Int) throws -> (String, String) {
        let old = try resolve(note: note, marks: octave, relativeTo: previousOld)
        let newNote = try MusicTheory.transposeNote(old.note, semitones: shift, letterShift: letterShift)
        let converted = try relativeMarks(previous: previousNew, midi: old.midi + shift, note: newNote)
        previousOld = old
        previousNew = converted.position
        return (newNote, converted.marks)
    }

    mutating func transposeChord(_ items: [Token], shift: Int) throws -> [Token] {
        var oldPrevious = previousOld
        var newPrevious = previousNew
        var firstOld: PitchPosition?
        var firstNew: PitchPosition?
        let converted = try items.map { item -> Token in
            guard case .note(let note, let octave, let suffix) = item else { return item }
            let old = try resolve(note: note, marks: octave, relativeTo: oldPrevious)
            let newNote = try MusicTheory.transposeNote(old.note, semitones: shift, letterShift: letterShift)
            let new = try relativeMarks(previous: newPrevious, midi: old.midi + shift, note: newNote)
            oldPrevious = old; newPrevious = new.position
            if firstOld == nil { firstOld = old; firstNew = new.position }
            return .note(note: newNote, octave: new.marks, suffix: suffix)
        }
        if let firstOld, let firstNew { previousOld = firstOld; previousNew = firstNew }
        return converted
    }

    private func resolve(note: String, marks: String, relativeTo previous: PitchPosition) throws -> PitchPosition {
        let inferred = inferredOctave(previous: previous, note: note)
        let octave = inferred + marks.filter { $0 == "'" }.count - marks.filter { $0 == "," }.count
        return try Self.position(note: note, octave: octave)
    }

    private func relativeMarks(previous: PitchPosition, midi: Int, note: String) throws -> (marks: String, position: PitchPosition) {
        let absoluteOctave = (midi - (try MusicTheory.noteBaseMIDI(note))) / 12
        let difference = absoluteOctave - inferredOctave(previous: previous, note: note)
        let marks = difference > 0 ? String(repeating: "'", count: difference) : String(repeating: ",", count: -difference)
        return (marks, try Self.position(note: note, octave: absoluteOctave))
    }

    private func inferredOctave(previous: PitchPosition, note: String) -> Int {
        let previousStep = previous.octave * 7 + MusicTheory.letters.firstIndex(of: previous.letter)!
        let letterIndex = MusicTheory.letters.firstIndex(of: String(note.prefix(1)))!
        return ((previous.octave - 4)...(previous.octave + 4)).min {
            let left = $0 * 7 + letterIndex - previousStep
            let right = $1 * 7 + letterIndex - previousStep
            return (abs(left), left) < (abs(right), right)
        }!
    }

    private static func absolutePosition(_ pitch: String) throws -> PitchPosition {
        let value = try MusicTheory.splitPitch(pitch)
        let octave = value.marks.filter { $0 == "'" }.count - value.marks.filter { $0 == "," }.count
        return try position(note: value.note, octave: octave)
    }

    private static func position(note: String, octave: Int) throws -> PitchPosition {
        PitchPosition(note: note, octave: octave, midi: try MusicTheory.noteBaseMIDI(note) + octave * 12)
    }
}

enum TransposeEngine {
    static func transpose(_ tokens: [Token], shift: Int, letterShift: Int) throws -> [Token] {
        var resolver: RelativeResolver?
        return try walk(tokens, resolver: &resolver, shift: shift, letterShift: letterShift)
    }

    private static func walk(_ tokens: [Token], resolver: inout RelativeResolver?, shift: Int, letterShift: Int) throws -> [Token] {
        try tokens.map { token in
            switch token {
            case .note(let note, let octave, let suffix):
                if resolver != nil {
                    let converted = try resolver!.transpose(note: note, octave: octave, shift: shift)
                    return .note(note: converted.0, octave: converted.1, suffix: suffix)
                }
                return .note(note: try MusicTheory.transposeSimple(note, semitones: shift), octave: octave, suffix: suffix)
            case .chord(let items, let suffix):
                if resolver != nil { return .chord(items: try resolver!.transposeChord(items, shift: shift), suffix: suffix) }
                let converted = try items.map { item -> Token in
                    guard case .note(let note, let octave, let noteSuffix) = item else { return item }
                    return .note(note: try MusicTheory.transposeSimple(note, semitones: shift), octave: octave, suffix: noteSuffix)
                }
                return .chord(items: converted, suffix: suffix)
            case .key(let note, let mode):
                return .key(note: try MusicTheory.transposeSimple(note, semitones: shift), mode: mode)
            case .relative(let anchor, let children):
                let newAnchor = try absoluteLily(fromMIDI: MusicTheory.parsePitch(anchor) + shift)
                var childResolver: RelativeResolver? = try RelativeResolver(anchor: anchor, newAnchor: newAnchor, letterShift: letterShift)
                return .relative(anchor: newAnchor, tokens: try walk(children, resolver: &childResolver, shift: shift, letterShift: letterShift))
            case .parallel(let voices):
                let converted = try voices.map { voice in
                    var voiceResolver = resolver
                    return try walk(voice, resolver: &voiceResolver, shift: shift, letterShift: letterShift)
                }
                return .parallel(voices: converted)
            default: return token
            }
        }
    }

    private static func absoluteLily(fromMIDI midi: Int) throws -> String {
        let pc = MusicTheory.modulo(midi, 12)
        let note = MusicTheory.flatSpelling[pc]
        let octave = (midi - (60 + pc)) / 12
        return note + (octave > 0 ? String(repeating: "'", count: octave) : String(repeating: ",", count: -octave))
    }
}
