import Foundation

public enum TransposeError: LocalizedError, Equatable {
    case invalidPitch(String)
    case malformedSource(String)
    case unsupportedAccidental(String)

    public var errorDescription: String? {
        switch self {
        case .invalidPitch(let pitch): "音名を解釈できません: \(pitch)"
        case .malformedSource(let message): "LilyPondソースを解釈できません: \(message)"
        case .unsupportedAccidental(let note): "未対応の臨時記号です: \(note)"
        }
    }
}

public struct LilyPondTransposer: Sendable {
    public init() {}

    public func transpose(_ source: String, from sourcePitch: String, to destinationPitch: String) throws -> String {
        let sourceValue = try MusicTheory.parsePitch(sourcePitch)
        let destinationValue = try MusicTheory.parsePitch(destinationPitch)
        let shift = destinationValue - sourceValue
        let letterShift = try MusicTheory.letterShift(from: sourcePitch, to: destinationPitch)
        var tokenizer = Tokenizer(source)
        let tokens = try tokenizer.tokenize()
        let transposed = try TransposeEngine.transpose(tokens, shift: shift, letterShift: letterShift)
        return LilyPondWriter.write(transposed)
    }
}
