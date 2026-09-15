// swift-tools-version: 5.9
import PackageDescription

// PCCI is built as a Swift Package executable and assembled into an .app bundle by
// scripts/build-macos.sh. That keeps the whole build runnable from the command line
// with just the Swift toolchain — no Xcode project file to drift out of sync — while
// still producing an ordinary, double-clickable macOS application.
let package = Package(
    name: "PCCI",
    platforms: [
        .macOS(.v14)
    ],
    targets: [
        .executableTarget(
            name: "PCCI",
            path: "Sources/PCCI"
        )
    ]
)
