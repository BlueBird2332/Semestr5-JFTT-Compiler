from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Symbol:
    name: str
    symbol_type: str  # 'global', 'local', 'parameter'
    is_array: bool = False
    array_start: Optional[int] = None
    array_end: Optional[int] = None
    is_parameter: bool = False
    is_array_parameter: bool = False
    procedure_name: Optional[str] = (
        None  # For tracking which procedure a symbol belongs to # For tracking which procedure a symbol belongs to
    )
    is_used: bool = False  # For tracking if a symbol is used in the program

    def __str__(self) -> str:
        return f"""
        Name: {self.name}
        Type: {self.symbol_type}
        Array: {self.is_array}
        Array Start: {self.array_start}
        Array End: {self.array_end}
        Parameter: {self.is_parameter}
        Array Parameter: {self.is_array_parameter}
        Procedure: {self.procedure_name}
        Is_used: {self.is_used}
        """


class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.procedures: Dict[str, List[Tuple[str, bool]]] = (
            {}
        )  # procedure_name -> [(param_name, is_array)]
        self.current_procedure: Optional[str] = None
        self.costly_operations: Set[str] = set()

    def add_procedure(self, name: str, parameters: List[Tuple[str, bool]]) -> None:
        """Add procedure with its parameters."""
        if name in self.procedures:
            raise ValueError(f"Procedure {name} already defined")

        self.procedures[name] = parameters
        # Add procedure to symbol table as a special type
        self.add_symbol(name=name, symbol_type="procedure", is_array=False)

    def get_procedure_params(self, name: str) -> Optional[List[Tuple[str, bool]]]:
        """Get procedure parameters if procedure exists."""
        return self.procedures.get(name)

    def is_procedure(self, name: str) -> bool:
        """Check if name refers to a procedure."""
        symbol = self.lookup(name)
        return symbol is not None and symbol.symbol_type == "procedure"

    def enter_procedure(self, name: str):
        """Enter a procedure scope."""
        self.current_procedure = name

    def exit_procedure(self):
        """Exit the current procedure scope. Used when leaving a procedure to set a global scope."""
        self.current_procedure = None

    def get_current_scope_name(self) -> str:
        """Get current scope identifier (procedure name or 'global')."""
        return self.current_procedure if self.current_procedure else "global"

    def make_scoped_name(self, name: str, scope: Optional[str] = None) -> str:
        """Create a scoped name based on current or specified scope."""
        if scope and scope != "global":
            return f"{scope}_{name}"
        return name

    def add_symbol(
        self,
        name: str,
        symbol_type: str,
        is_array: bool = False,
        array_start: Optional[int] = None,
        array_end: Optional[int] = None,
        is_parameter: bool = False,
        is_array_parameter: bool = False,
        procedure_name: Optional[str] = None,
        is_used: bool = False,
    ) -> None:
        """Add a symbol to the table."""
        # Use current procedure if procedure_name not specified
        effective_procedure = (
            procedure_name if procedure_name is not None else self.current_procedure
        )
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
            procedure_name=effective_procedure,
            is_used=is_used,
        )

    def add_costly_operation(self, name: str):
        """Add a costly operation to the set."""
        self.costly_operations.add(name)

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
        if (
            symbol
            and symbol.is_array
            and symbol.array_start is not None
            and symbol.array_end is not None
        ):
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

    def mark_used(self, name: str):
        """Mark a symbol as used."""
        symbol = self.lookup(name)
        if symbol:
            symbol.is_used = True
        else:
            raise ValueError(f"Symbol {name} not found")

    def prune_uncalled_procedures(self):
        for symbol in list(self.symbols.values()):
            if symbol.symbol_type == "procedure" and not symbol.is_used:

                for name, _ in list(self.symbols.items()):
                    if name.startswith(symbol.name + "_"):
                        del self.symbols[name]

                del self.symbols[symbol.name]
                del self.procedures[symbol.name]

    def print_table(self):
        """Print the symbol table for debugging."""
        print("Symbol table:")
        for name, symbol in self.symbols.items():
            print(f"  {name}: {symbol}")
        print("Procedure table:")
        for name, params in self.procedures.items():
            print(f"  {name}: {params}")
        print("Costly operations:")
        print(self.costly_operations)
