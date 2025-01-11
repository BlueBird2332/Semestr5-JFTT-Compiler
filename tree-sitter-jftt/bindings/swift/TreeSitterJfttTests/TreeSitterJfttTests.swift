import XCTest
import SwiftTreeSitter
import TreeSitterJftt

final class TreeSitterJfttTests: XCTestCase {
    func testCanLoadGrammar() throws {
        let parser = Parser()
        let language = Language(language: tree_sitter_jftt())
        XCTAssertNoThrow(try parser.setLanguage(language),
                         "Error loading Jftt grammar")
    }
}
