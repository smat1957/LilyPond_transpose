import SwiftUI
import UniformTypeIdentifiers
import LilyPondTransposeCore

struct PadContentView: View {
    @State private var source = ""
    @State private var result = ""
    @State private var sourcePitch = "c"
    @State private var destinationPitch = "a"
    @State private var importsFile = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationStack {
            VStack(spacing: 12) {
                HStack {
                    Button("ファイルを選択") { importsFile = true }
                    Spacer()
                    TextField("移調元", text: $sourcePitch).textFieldStyle(.roundedBorder).frame(width: 100)
                    Image(systemName: "arrow.right")
                    TextField("移調先", text: $destinationPitch).textFieldStyle(.roundedBorder).frame(width: 100)
                    Button("変換", action: convert).buttonStyle(.borderedProminent).disabled(source.isEmpty)
                }
                if let errorMessage { Text(errorMessage).foregroundStyle(.red).frame(maxWidth: .infinity, alignment: .leading) }
                HStack(spacing: 12) {
                    editor("変換前", text: $source)
                    editor("変換後プレビュー", text: $result)
                }
            }
            .padding().navigationTitle("LilyPond Transpose")
        }
        .fileImporter(isPresented: $importsFile, allowedContentTypes: [UTType(filenameExtension: "ly") ?? .plainText, .plainText]) { selection in
            do {
                let url = try selection.get(); let access = url.startAccessingSecurityScopedResource()
                defer { if access { url.stopAccessingSecurityScopedResource() } }
                source = try String(contentsOf: url, encoding: .utf8); result = ""; errorMessage = nil
            } catch { errorMessage = error.localizedDescription }
        }
    }

    private func editor(_ title: String, text: Binding<String>) -> some View {
        VStack(alignment: .leading) { Text(title).font(.headline); TextEditor(text: text).font(.system(.body, design: .monospaced)).border(.separator) }
    }
    private func convert() {
        do { result = try LilyPondTransposer().transpose(source, from: sourcePitch, to: destinationPitch); errorMessage = nil }
        catch { errorMessage = error.localizedDescription }
    }
}
