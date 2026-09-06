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
        let normalizedSourcePitch = try Self.normalizePitch(sourcePitch)
        let normalizedDestinationPitch = try Self.normalizePitch(destinationPitch)
        let sourceValue = try MusicTheory.parsePitch(normalizedSourcePitch)
        let destinationValue = try MusicTheory.parsePitch(normalizedDestinationPitch)
        let shift = destinationValue - sourceValue
        let letterShift = try MusicTheory.letterShift(from: normalizedSourcePitch, to: normalizedDestinationPitch)
        var tokenizer = Tokenizer(source)
        let tokens = try tokenizer.tokenize()
        let transposed = try TransposeEngine.transpose(tokens, shift: shift, letterShift: letterShift)
        return LilyPondWriter.write(transposed)
    }

    /// UIでスマート引用符に変換されたアポストロフィーをLilyPond表記へ戻し、検証する。
    public static func normalizePitch(_ pitch: String) throws -> String {
        let normalized = pitch
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .replacingOccurrences(of: "’", with: "'")
            .replacingOccurrences(of: "‘", with: "'")
        _ = try MusicTheory.splitPitch(normalized)
        return normalized
    }
}
