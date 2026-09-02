// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "LilyPondTransposeCore",
    platforms: [.macOS(.v14), .iOS(.v17)],
    products: [.library(name: "LilyPondTransposeCore", targets: ["LilyPondTransposeCore"])],
    targets: [
        .target(name: "LilyPondTransposeCore", path: "LilyPondTranspose/Core"),
        .testTarget(name: "LilyPondTransposeCoreTests", dependencies: ["LilyPondTransposeCore"], path: "LilyPondTransposeTests")
    ]
)
