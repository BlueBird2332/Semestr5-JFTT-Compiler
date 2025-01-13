# src/compiler/vm/memory_manager.py
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

@dataclass
class MemoryCell:
    """Represents a single memory cell allocation."""
    address: int
    size: int = 1
    is_array: bool = False
    array_start: Optional[int] = None
    array_end: Optional[int] = None
    is_parameter: bool = False
    scope: str = 'global'

class MemoryManager:
    def __init__(self):
        self.memory_map: Dict[str, MemoryCell] = {}
        self.next_address: int = 1  # p0 is accumulator
        self.scope_stack: List[str] = ['global']
        self.temp_counter: int = 0
        
    def get_current_scope(self) -> str:
        """Get current scope name."""
        return self.scope_stack[-1]
    
    def enter_scope(self, scope_name: str):
        """Enter a new scope."""
        self.scope_stack.append(scope_name)
        
    def exit_scope(self):
        """Exit current scope."""
        if len(self.scope_stack) > 1:  # Keep at least global scope
            self.scope_stack.pop()
            
    def get_scoped_name(self, name: str) -> str:
        """Get fully qualified name for variable in current scope."""
        if self.get_current_scope() == 'global':
            return name
        return f"{self.get_current_scope()}_{name}"
        
    def allocate(self, name: str, size: int = 1, is_array: bool = False,
                array_start: Optional[int] = None, array_end: Optional[int] = None,
                is_parameter: bool = False) -> MemoryCell:
        """Allocate memory for a variable."""
        scoped_name = self.get_scoped_name(name)
        
        # Check if already allocated in current scope
        if scoped_name in self.memory_map:
            return self.memory_map[scoped_name]
            
        cell = MemoryCell(
            address=self.next_address,
            size=size,
            is_array=is_array,
            array_start=array_start,
            array_end=array_end,
            is_parameter=is_parameter,
            scope=self.get_current_scope()
        )
        
        self.memory_map[scoped_name] = cell
        self.next_address += size
        return cell
    
    def allocate_temp(self) -> MemoryCell:
        """Allocate temporary variable."""
        self.temp_counter += 1
        return self.allocate(f"_t{self.temp_counter}")
    
    def get_location(self, name: str) -> Optional[MemoryCell]:
        """Get memory location for a variable, checking all accessible scopes."""
        # Try current scope
        scoped_name = self.get_scoped_name(name)
        if scoped_name in self.memory_map:
            return self.memory_map[scoped_name]
            
        # Try global scope
        if name in self.memory_map:
            return self.memory_map[name]
            
        return None
        
    def clear_temps(self):
        """Clear temporary variables."""
        self.memory_map = {k: v for k, v in self.memory_map.items() 
                          if not k.startswith('_t')}
        
    def reset(self):
        """Reset memory manager state."""
        self.memory_map.clear()
        self.next_address = 1
        self.scope_stack = ['global']
        self.temp_counter = 0