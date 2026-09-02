import SwiftUI
import UniformTypeIdentifiers
import LilyPondTransposeCore

struct PhoneContentView: View {
    private enum PreviewTab: String, CaseIterable { case source = "変換前"; case result = "変換後" }
    @State private var source = ""
    @State private var result = ""
    @State private var sourcePitch = "c"
    @State private var destinationPitch = "a"
    @State private var importsFile = false
    @State private var tab = PreviewTab.source
    @State private var errorMessage: String?

    var body: some View {
        NavigationStack {
            VStack(spacing: 10) {
                HStack {
                    Button("ファイルを選択") { importsFile = true }
                    Spacer()
                    TextField("元", text: $sourcePitch).textFieldStyle(.roundedBorder).frame(width: 55)
                    Image(systemName: "arrow.right")
                    TextField("先", text: $destinationPitch).textFieldStyle(.roundedBorder).frame(width: 55)
                }
                Button("変換", action: convert).buttonStyle(.borderedProminent).frame(maxWidth: .infinity, alignment: .trailing).disabled(source.isEmpty)
                if let errorMessage { Text(errorMessage).font(.caption).foregroundStyle(.red).frame(maxWidth: .infinity, alignment: .leading) }
                Picker("プレビュー", selection: $tab) { ForEach(PreviewTab.allCases, id: \.self) { Text($0.rawValue) } }.pickerStyle(.segmented)
                TextEditor(text: tab == .source ? $source : $result).font(.system(.body, design: .monospaced)).border(.separator)
            }
            .padding().navigationTitle("LilyPond Transpose").navigationBarTitleDisplayMode(.inline)
        }
        .fileImporter(isPresented: $importsFile, allowedContentTypes: [UTType(filenameExtension: "ly") ?? .plainText, .plainText]) { selection in
            do {
                let url = try selection.get(); let access = url.startAccessingSecurityScopedResource()
                defer { if access { url.stopAccessingSecurityScopedResource() } }
                source = try String(contentsOf: url, encoding: .utf8); result = ""; tab = .source; errorMessage = nil
            } catch { errorMessage = error.localizedDescription }
        }
    }

    private func convert() {
        do { result = try LilyPondTransposer().transpose(source, from: sourcePitch, to: destinationPitch); tab = .result; errorMessage = nil }
        catch { errorMessage = error.localizedDescription }
    }
}
