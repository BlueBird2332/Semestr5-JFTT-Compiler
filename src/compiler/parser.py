from tree_sitter import Parser, Language # type: ignore
import tree_sitter_jftt as jftt
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple
import os
import subprocess

@dataclass
class SyntaxError:
    message: str
    line: int
    column: int
    source_line: str
    length: int

class CompilerParser:
    def __init__(self):
        self.parser = None
        self._setup_parser()

    def _setup_parser(self):
        try:

            language = Language(jftt.language())
            self.parser = Parser(language)
    
        except Exception as e:
            print(f"Error creating parser: {e}")
            raise

    def parse(self, code: str) -> Tuple[Optional[object], List[SyntaxError]]:
        """Parse code and return the syntax tree along with any errors."""
        if not self.parser:
            raise RuntimeError("Parser not initialized")
        
        tree = self.parser.parse(bytes(code, "utf8"))
        errors = self._collect_errors(tree.root_node, code)
        return tree, errors

    def _collect_errors(self, node, source_code: str) -> List[SyntaxError]:
        errors = []
        source_lines = source_code.splitlines()
        
        def collect_node_errors(node):
            
            if str(node).startswith("(MISSING"):
                line_num = node.start_point[0]
                missing_token = str(node).split('"')[1]
                if line_num < len(source_lines):
                    source_line = source_lines[line_num]
                    error = SyntaxError(
                        message=f"Missing token: {missing_token}",
                        line=line_num + 1,
                        column=node.start_point[1],
                        source_line=source_line,
                        length=1
                    )
                    errors.append(error)
            
            if node.type == 'ERROR':
                line_num = node.start_point[0]
                if line_num < len(source_lines):
                    source_line = source_lines[line_num]
                    error = SyntaxError(
                        message=f"Unexpected syntax: '{node.text.decode('utf8')}'",
                        line=line_num + 1,
                        column=node.start_point[1],
                        source_line=source_line,
                        length=len(node.text.decode('utf8'))
                    )
                    errors.append(error)
            
            for child in node.children:
                collect_node_errors(child)

        collect_node_errors(node)
        return errors

    def format_error(self, error: SyntaxError) -> str:
        pointer = ' ' * error.column + '^' * error.length
        return f"""
Error at line {error.line}, column {error.column}:
{error.message}

{error.source_line}
{pointer}
"""

    def parse_and_check(self, code: str) -> Tuple[bool, str]:
        tree, errors = self.parse(code)
        if errors:
            error_messages = "\n".join(self.format_error(error) for error in errors)
            return False, error_messages
        return True, "No syntax errors found."