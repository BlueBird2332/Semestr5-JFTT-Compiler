#!/usr/bin/env python3
import argparse
import sys

from compiler.ast_builder import ASTBuilder
from compiler.intermediate_rep.IR_generator import IRGenerator
from compiler.parser import CompilerParser
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.utils import *
from compiler.pre_assembler.memory_map import MemoryMap
from compiler.vm_compiler.vm_code_generator import VMCodeGenerator


from compiler.pre_assembler.memory_map import *

def format_error(message: str, line: int, column: int, source_lines: list[str]) -> str:
    source_line = source_lines[line - 1] if line <= len(source_lines) else ""
    pointer = " " * column + "^"
    return f"""
Error at line {line}, column {column}:
{message}
{source_line}
{pointer}
"""


def main():
    parser = argparse.ArgumentParser(description="Compile a source file")
    parser.add_argument("file", help="Source file to compile")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print parse tree")
    parser.add_argument(
        "--semantic-only", action="store_true", help="Only perform semantic analysis"
    )
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()
    

    # Initialize compiler components
    compiler = CompilerParser()
    ast_builder = ASTBuilder()
    semantic_analyzer = SemanticAnalyzer()
    # vm_compiler = VMCompiler()

    try:
        # Read source file
        with open(args.file) as f:
            source = f.read()
            source_lines = source.splitlines()
    except FileNotFoundError:
        print(f"Error: File {args.file} not found")
        sys.exit(1)

    # Parse source code
    tree, syntax_errors = compiler.parse(source)
    # debug_parse_tree(tree.root_node)
    if syntax_errors:
        print("Compilation failed due to syntax errors!")
        for error in syntax_errors:
            print(compiler.format_error(error))
        sys.exit(1)


    # Build AST
    try:
        ast = ast_builder.build(tree.root_node)
    except ValueError as e:
        print(f"Error building AST: {e}")
        sys.exit(1)


    # Perform semantic analysis
    success, semantic_errors, symbol_table = semantic_analyzer.analyze(ast)
    if not success:
        print("\nCompilation failed due to semantic errors!")
        for message in semantic_errors:
            print(format_error(message, message.line, message.column, source_lines))
        sys.exit(1)

    if args.semantic_only:
        print("Semantic analysis completed successfully!")
        sys.exit(0)

    # print_ast(ast)

    # At this point we have:
    # - Valid AST in 'ast'
    # - Symbol table in 'symbol_table'
    # - No syntax or semantic errors

    # print("Compilation successful!")
    tac_gen = IRGenerator(symbol_table)
    ir, vars, proc_info = tac_gen.generate(ast)

            
    mem_manager = MemoryMap(vars)
    

    
    code_gen = VMCodeGenerator(mem_manager, vars, proc_info, costly_ops=symbol_table.costly_operations)
    code = code_gen.generate(ir)
        
        
    with open(args.output_file, 'w+') as f:
        for item in code:
            f.write(item)
            f.write("\n")

if __name__ == "__main__":
    main()
