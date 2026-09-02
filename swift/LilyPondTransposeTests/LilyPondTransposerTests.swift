import Testing
@testable import LilyPondTransposeCore

@Test func transposesNotesKeyChordAndRelativeBlock() throws {
    let source = "\\key c \\major\n\\relative c' { c4 d e <c e g> }"
    let result = try LilyPondTransposer().transpose(source, from: "c", to: "d")
    #expect(result.contains("\\key d \\major"))
    #expect(result.contains("\\relative d'"))
    #expect(result.contains("d4 e fis <d fis a>"))
}

@Test func preservesCommentsAndCommands() throws {
    let source = "% title\n\\time 4/4\n\\relative c' { c8( d) }"
    let result = try LilyPondTransposer().transpose(source, from: "c", to: "a")
    #expect(result.contains("% title"))
    #expect(result.contains("\\time 4/4"))
}

@Test func rejectsInvalidPitch() {
    #expect(throws: TransposeError.self) { try LilyPondTransposer().transpose("c", from: "h", to: "a") }
}
