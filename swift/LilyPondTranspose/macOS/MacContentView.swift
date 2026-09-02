import AppKit
import SwiftUI
import UniformTypeIdentifiers
import LilyPondTransposeCore

struct MacContentView: View {
    @State private var source = ""
    @State private var result = ""
    @State private var sourcePitch = "c"
    @State private var destinationPitch = "a"
    @State private var fileName = "ファイル未選択"
    @State private var errorMessage: String?

    var body: some View {
        VStack(spacing: 12) {
            HStack {
                Button("LilyPondファイルを選択", action: chooseFile)
                Text(fileName).foregroundStyle(.secondary).lineLimit(1)
                Spacer()
                pitchField("移調元", text: $sourcePitch)
                Image(systemName: "arrow.right")
                pitchField("移調先", text: $destinationPitch)
                Button("変換", action: convert).buttonStyle(.borderedProminent).disabled(source.isEmpty)
            }
            if let errorMessage { Text(errorMessage).foregroundStyle(.red).frame(maxWidth: .infinity, alignment: .leading) }
            HSplitView {
                editor(title: "変換前", text: $source)
                editor(title: "変換後プレビュー", text: $result)
            }
        }
        .padding()
        .navigationTitle("LilyPond Transpose")
    }

    private func pitchField(_ title: String, text: Binding<String>) -> some View {
        HStack(spacing: 5) { Text(title); TextField("c", text: text).frame(width: 55).textFieldStyle(.roundedBorder) }
    }

    private func editor(title: String, text: Binding<String>) -> some View {
        VStack(alignment: .leading) {
            Text(title).font(.headline)
            TextEditor(text: text).font(.system(.body, design: .monospaced)).border(.separator)
        }.frame(minWidth: 360)
    }

    private func chooseFile() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [UTType(filenameExtension: "ly") ?? .plainText, .plainText]
        panel.allowsMultipleSelection = false
        guard panel.runModal() == .OK, let url = panel.url else { return }
        do { source = try String(contentsOf: url, encoding: .utf8); fileName = url.lastPathComponent; result = ""; errorMessage = nil }
        catch { errorMessage = error.localizedDescription }
    }

    private func convert() {
        do { result = try LilyPondTransposer().transpose(source, from: sourcePitch, to: destinationPitch); errorMessage = nil }
        catch { errorMessage = error.localizedDescription }
    }
}
