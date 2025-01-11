# src/compiler/symbol_table.py
from dataclasses import dataclass
from typing import Dict, Optional, List
from .ast_nodes import Location

@dataclass
class Symbol:
    name: str
    symbol_type: str  # 'variable', 'array', 'procedure'
    scope: str
    array_bounds: Optional[tuple[int, int]] = None
    is_param: bool = False
    is_array_param: bool = False
    procedure_params: Optional[List[tuple[str, bool]]] = None  # [(name, is_array)]
    defined_at: Optional[Location] = None

class SymbolTable:
    def __init__(self):
        self.scopes: Dict[str, Dict[str, Symbol]] = {'global': {}}
        self.current_scope = 'global'
        self.scope_stack = ['global']
        
    def enter_scope(self, scope_name: str):
        """Enter a new scope."""
        if scope_name not in self.scopes:
            self.scopes[scope_name] = {}
        self.scope_stack.append(scope_name)
        self.current_scope = scope_name
        
    def exit_scope(self):
        """Exit current scope."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
            
    def add_symbol(self, symbol: Symbol) -> bool:
        """Add a symbol to current scope."""
        if symbol.name in self.scopes[self.current_scope]:
            return False
        self.scopes[self.current_scope][symbol.name] = symbol
        return True
        
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in current and global scope."""
        # Check current scope
        if name in self.scopes[self.current_scope]:
            return self.scopes[self.current_scope][name]
            
        # Check global scope if we're not already in it
        if self.current_scope != 'global' and name in self.scopes['global']:
            return self.scopes['global'][name]
            
        return None
        
    def lookup_current_scope(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in current scope only."""
        return self.scopes[self.current_scope].get(name)

    def add_procedure(self, name: str, params: List[tuple[str, bool]], location: Location) -> bool:
        """Add a procedure to global scope."""
        if name in self.scopes['global']:
            return False
            
        self.scopes['global'][name] = Symbol(
            name=name,
            symbol_type='procedure',
            scope='global',
            procedure_params=params,
            defined_at=location
        )
        return True
    
    
class ASTPrinter:
    def __init__(self, indent_size=2):
        self.indent_size = indent_size

    def print_ast(self, node, indent=0):
        """Print an AST node and its children in a readable format."""
        if node is None:
            return
            
        # Get the node type name
        node_type = type(node).__name__
        
        # Print the current node with indentation
        indent_str = ' ' * (indent * self.indent_size)
        
        # Start with the node type
        print(f"{indent_str}{node_type}:", end=" ")
        
        # Print relevant attributes based on node type
        if hasattr(node, 'location'):
            print(f"(line {node.location.line}, col {node.location.column})")
        else:
            print()

        # Print specific attributes based on node type
        self._print_node_attributes(node, indent + 1)
        
        # Recursively print children
        self._print_children(node, indent + 1)

    def _print_node_attributes(self, node, indent):
        """Print the relevant attributes of a node."""
        indent_str = ' ' * (indent * self.indent_size)
        
        if hasattr(node, 'name'):
            print(f"{indent_str}name: {node.name}")
            
        if hasattr(node, 'value') and isinstance(node.value, (int, str, float)):
            print(f"{indent_str}value: {node.value}")
            
        if hasattr(node, 'operator'):
            print(f"{indent_str}operator: {node.operator}")
            
        if hasattr(node, 'array_bounds') and node.array_bounds is not None:
            start, end = node.array_bounds
            print(f"{indent_str}array_bounds: [{start}:{end}]")
            
        if hasattr(node, 'parameters'):
            params = [f"{'T ' if is_array else ''}{name}" for name, is_array in node.parameters]
            if params:
                print(f"{indent_str}parameters: {', '.join(params)}")

    def _print_children(self, node, indent):
        """Print all child nodes recursively."""
        # Lists of commands, declarations, procedures
        if hasattr(node, 'procedures') and node.procedures:
            self._print_list("procedures", node.procedures, indent)
            
        if hasattr(node, 'declarations') and node.declarations:
            self._print_list("declarations", node.declarations, indent)
            
        if hasattr(node, 'commands') and node.commands:
            self._print_list("commands", node.commands, indent)
            
        # Binary operations
        if hasattr(node, 'left'):
            print(f"{' ' * (indent * self.indent_size)}left:")
            self.print_ast(node.left, indent + 1)
            
        if hasattr(node, 'right'):
            print(f"{' ' * (indent * self.indent_size)}right:")
            self.print_ast(node.right, indent + 1)
            
        # Conditional statements
        if hasattr(node, 'condition'):
            print(f"{' ' * (indent * self.indent_size)}condition:")
            self.print_ast(node.condition, indent + 1)
            
        if hasattr(node, 'then_block'):
            self._print_list("then_block", node.then_block, indent)
            
        if hasattr(node, 'else_block') and node.else_block:
            self._print_list("else_block", node.else_block, indent)
            
        # For loops
        if hasattr(node, 'iterator'):
            print(f"{' ' * (indent * self.indent_size)}iterator: {node.iterator}")
            print(f"{' ' * (indent * self.indent_size)}start:")
            self.print_ast(node.start, indent + 1)
            print(f"{' ' * (indent * self.indent_size)}end:")
            self.print_ast(node.end, indent + 1)
            
        if hasattr(node, 'body'):
            self._print_list("body", node.body, indent)
            
        # Array indices
        if hasattr(node, 'array_index') and node.array_index is not None:
            print(f"{' ' * (indent * self.indent_size)}array_index:")
            self.print_ast(node.array_index, indent + 1)
            
        # Procedure calls
        if hasattr(node, 'arguments') and node.arguments:
            self._print_list("arguments", node.arguments, indent)

    def _print_list(self, name, items, indent):
        """Print a list of nodes with a header."""
        indent_str = ' ' * (indent * self.indent_size)
        if items:
            print(f"{indent_str}{name}:")
            for item in items:
                self.print_ast(item, indent + 1)

# Usage example:
def print_ast(ast_node):
    printer = ASTPrinter(indent_size=2)
    printer.print_ast(ast_node)
    
def debug_parse_tree(node, indent=0):
    if node is None:
        return
    
    prefix = '  ' * indent
    if len(node.children) == 0:
        # For leaf nodes, show the text
        text = node.text.decode('utf8') if hasattr(node, 'text') else ''
        print(f"{prefix}{node.type}: '{text}'")
    else:
        # For non-leaf nodes, just show the type
        print(f"{prefix}{node.type}")
        
    # Print all children recursively
    for child in node.children:
        debug_parse_tree(child, indent + 1)