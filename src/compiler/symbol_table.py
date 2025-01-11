from dataclasses import dataclass
from typing import Dict, Set, Optional, List, Tuple

@dataclass
class Symbol:
    name: str
    symbol_type: str  # 'global', 'local', 'parameter'
    is_array: bool = False
    array_start: Optional[int] = None
    array_end: Optional[int] = None
    is_parameter: bool = False
    is_array_parameter: bool = False
    procedure_name: Optional[str] = None  # For tracking which procedure a symbol belongs to # For tracking which procedure a symbol belongs to

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.procedures: Dict[str, List[Tuple[str, bool]]] = {}  # procedure_name -> [(param_name, is_array)]
        self.current_procedure: Optional[str] = None
        
    def enter_procedure(self, name: str):
        """Enter a procedure scope."""
        self.current_procedure = name
        
    def exit_procedure(self):
        """Exit the current procedure scope."""
        self.current_procedure = None
            
    def get_current_scope_name(self) -> str:
        """Get current scope identifier (procedure name or 'global')."""
        return self.current_procedure if self.current_procedure else 'global'

    def make_scoped_name(self, name: str, scope: Optional[str] = None) -> str:
        """Create a scoped name based on current or specified scope."""
        if scope and scope != 'global':
            return f"{scope}_{name}"
        return name

        
    def add_symbol(self, name: str, symbol_type: str, 
                  is_array: bool = False, 
                  array_start: Optional[int] = None, 
                  array_end: Optional[int] = None,
                  is_parameter: bool = False,
                  is_array_parameter: bool = False,
                  procedure_name: Optional[str] = None):
        """Add a symbol to the table."""
        # Use current procedure if procedure_name not specified
        effective_procedure = procedure_name if procedure_name is not None else self.current_procedure
        full_name = self.make_scoped_name(name, effective_procedure)
        
        if full_name in self.symbols:
            raise ValueError(f"Symbol {name} already defined")
            
        self.symbols[full_name] = Symbol(
            name=name,
            symbol_type=symbol_type,
            is_array=is_array,
            array_start=array_start,
            array_end=array_end,
            is_parameter=is_parameter,
            is_array_parameter=is_array_parameter,
            procedure_name=effective_procedure
        )
    
    def add_procedure(self, name: str, parameters: List[Tuple[str, bool]]):
        """Add a procedure definition with its parameters."""
        if name in self.procedures:
            raise ValueError(f"Procedure {name} already defined")
        self.procedures[name] = parameters
        
        # Add parameters to symbol table
        for param_name, is_array in parameters:
            self.add_symbol(
                name=param_name,
                symbol_type='parameter',
                is_array=is_array,
                is_parameter=True,
                is_array_parameter=is_array,
                procedure_name=name
            )
        
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol, checking both current procedure and global scope."""
        # First try procedure-scoped lookup
        if self.current_procedure:
            scoped_name = f"{self.current_procedure}_{name}"
            if scoped_name in self.symbols:
                return self.symbols[scoped_name]
                
        # Then try global scope
        if name in self.symbols:
            return self.symbols[name]
            
        return None
        
    def lookup_current_scope(self, name: str) -> Optional[Symbol]:
        """Look up a symbol only in the current scope."""
        if self.current_procedure:
            # In procedure scope - only look for procedure-scoped symbol
            scoped_name = f"{self.current_procedure}_{name}"
            return self.symbols.get(scoped_name)
        else:
            # In global scope - only look for global symbol
            return self.symbols.get(name)
        
    def is_defined(self, name: str) -> bool:
        """Check if a symbol is defined in current scope."""
        return self.lookup(name) is not None
        
    def is_array(self, name: str) -> bool:
        """Check if a symbol is an array."""
        symbol = self.lookup(name)
        return symbol is not None and symbol.is_array
        
    def is_parameter(self, name: str) -> bool:
        """Check if a symbol is a parameter."""
        symbol = self.lookup(name)
        return symbol is not None and symbol.is_parameter
        
    def is_array_parameter(self, name: str) -> bool:
        """Check if a symbol is an array parameter (prefixed with T)."""
        symbol = self.lookup(name)
        return symbol is not None and symbol.is_array_parameter
        
    def get_array_bounds(self, name: str) -> Optional[Tuple[int, int]]:
        """Get array bounds if symbol is an array."""
        symbol = self.lookup(name)
        if symbol and symbol.is_array and symbol.array_start is not None and symbol.array_end is not None:
            return (symbol.array_start, symbol.array_end)
        return None
        
    def get_procedure_params(self, name: str) -> Optional[List[Tuple[str, bool]]]:
        """Get procedure parameters if procedure exists."""
        return self.procedures.get(name)
        
    def verify_array_index(self, name: str, index: int) -> bool:
        """Verify if an array index is within bounds."""
        bounds = self.get_array_bounds(name)
        if bounds:
            start, end = bounds
            return start <= index <= end
        return False