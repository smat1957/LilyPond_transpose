import Foundation

struct Tokenizer {
    private let characters: [Character]
    private var position = 0

    init(_ text: String) { characters = Array(text) }

    mutating func tokenize() throws -> [Token] {
        var result: [Token] = []
        while !isAtEnd {
            if matches("\\relative") { result.append(try readRelative()); continue }
            if matches("<<") { result.append(try readParallel()); continue }
            if matches(">>") { position += 2; result.append(.symbol(">>")); continue }
            if peek == "{" || peek == "}" { result.append(.symbol(String(advance()))); continue }
            if peek == "%" { result.append(.comment(readComment())); continue }
            if matches("\\key") { result.append(try readKey()); continue }
            if peek == "\\" { result.append(.command(readCommand())); continue }
            if peek == "<" && peekAt(1) != "<" { result.append(try readChord()); continue }
            if let note = readNote() { result.append(note); continue }
            result.append(.raw(String(advance())))
        }
        return result
    }

    private var isAtEnd: Bool { position >= characters.count }
    private var peek: Character? { peekAt(0) }
    private func peekAt(_ offset: Int) -> Character? {
        let index = position + offset
        return characters.indices.contains(index) ? characters[index] : nil
    }
    private mutating func advance() -> Character {
        let character = characters[position]
        position += 1
        return character
    }
    private func matches(_ string: String) -> Bool {
        let target = Array(string)
        guard position + target.count <= characters.count else { return false }
        return Array(characters[position..<(position + target.count)]) == target
    }
    private mutating func skipWhitespace() { while peek?.isWhitespace == true { _ = advance() } }

    private mutating func readComment() -> String {
        var value = ""
        while let character = peek, character != "\n" { value.append(advance()) }
        return value
    }

    private mutating func readCommand() -> String {
        var value = String(advance())
        while let character = peek, character.isLetter || character.isNumber || character == "_" { value.append(advance()) }
        return value
    }

    private func isWordCharacter(_ character: Character?) -> Bool {
        guard let character else { return false }
        return character.isLetter || character.isNumber || character == "_"
    }

    private mutating func readPitchLiteral() -> (String, String)? {
        let start = position
        guard !isWordCharacter(peekAt(-1)) else { return nil }
        guard let name = MusicTheory.noteNames.first(where: { matches($0) }) else { return nil }
        position += name.count
        var octave = ""
        while peek == "'" || peek == "," { octave.append(advance()) }
        if peek?.isLetter == true { position = start; return nil }
        return (name, octave)
    }

    private mutating func readNote() -> Token? {
        guard let pitch = readPitchLiteral() else { return nil }
        var suffix = ""
        while let character = peek, !character.isWhitespace && character != "<" && character != ">" { suffix.append(advance()) }
        return .note(note: pitch.0, octave: pitch.1, suffix: suffix)
    }

    private mutating func readChord() throws -> Token {
        _ = advance()
        var items: [Token] = []
        while let character = peek {
            if character == ">" { _ = advance(); break }
            if character.isWhitespace { items.append(.raw(String(advance()))); continue }
            if let note = readNote() { items.append(note); continue }
            items.append(.symbol(String(advance())))
        }
        guard !isAtEnd || characters.last == ">" else { throw TransposeError.malformedSource("和音を閉じる > がありません") }
        var suffix = ""
        while let character = peek, !character.isWhitespace { suffix.append(advance()) }
        return .chord(items: items, suffix: suffix)
    }

    private mutating func readKey() throws -> Token {
        position += "\\key".count
        skipWhitespace()
        guard let pitch = readPitchLiteral() else { throw TransposeError.malformedSource("\\key の音名がありません") }
        skipWhitespace()
        guard peek == "\\" else { throw TransposeError.malformedSource("\\key の major/minor がありません") }
        return .key(note: pitch.0 + pitch.1, mode: String(readCommand().dropFirst()))
    }

    private mutating func readBraceBody() throws -> String {
        var depth = 1
        var body = ""
        while !isAtEnd {
            let character = advance()
            if character == "{" { depth += 1 }
            if character == "}" {
                depth -= 1
                if depth == 0 { return body }
            }
            body.append(character)
        }
        throw TransposeError.malformedSource("閉じる } がありません")
    }

    private mutating func readRelative() throws -> Token {
        position += "\\relative".count
        skipWhitespace()
        guard let pitch = readPitchLiteral() else { throw TransposeError.malformedSource("\\relative の基準音がありません") }
        skipWhitespace()
        guard peek == "{" else { throw TransposeError.malformedSource("\\relative の { がありません") }
        _ = advance()
        let body = try readBraceBody()
        var tokenizer = Tokenizer(body)
        return .relative(anchor: pitch.0 + pitch.1, tokens: try tokenizer.tokenize())
    }

    private mutating func readParallel() throws -> Token {
        position += 2
        var voices: [[Token]] = []
        while !isAtEnd {
            skipWhitespace()
            if matches(">>") { position += 2; return .parallel(voices: voices) }
            if peek == "{" {
                _ = advance()
                var tokenizer = Tokenizer(try readBraceBody())
                voices.append(try tokenizer.tokenize())
                continue
            }
            if matches("\\new") {
                var prefix = ""
                while let character = peek, character != "{" { prefix.append(advance()) }
                guard peek == "{" else { throw TransposeError.malformedSource("\\new Voice の { がありません") }
                _ = advance()
                let body = try readBraceBody()
                var prefixTokenizer = Tokenizer(prefix)
                var bodyTokenizer = Tokenizer(body)
                voices.append(try prefixTokenizer.tokenize() + [.symbol("{")] + bodyTokenizer.tokenize() + [.symbol("}")])
                continue
            }
            _ = advance()
        }
        throw TransposeError.malformedSource("並列ブロックを閉じる >> がありません")
    }
}
