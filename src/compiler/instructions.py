# src/compiler/vm/instructions.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, List, Union, Set

class InstructionType(Enum):
    GET = "GET"
    PUT = "PUT"
    LOAD = "LOAD"
    STORE = "STORE"
    LOADI = "LOADI"
    STOREI = "STOREI"
    ADD = "ADD"
    SUB = "SUB"
    ADDI = "ADDI"
    SUBI = "SUBI"
    SET = "SET"
    HALF = "HALF"
    JUMP = "JUMP"
    JPOS = "JPOS"
    JZERO = "JZERO"
    JNEG = "JNEG"
    RTRN = "RTRN"
    HALT = "HALT"

@dataclass
class VMInstruction:
    type: InstructionType
    arg: Optional[int] = None
    comment: Optional[str] = None

    def __str__(self) -> str:
        if self.arg is not None:
            base = f"{self.type.value} {self.arg}"
        else:
            base = self.type.value
        
        if self.comment:
            return f"{base:20} # {self.comment}"
        return base

INSTRUCTION_COSTS: Dict[InstructionType, int] = {
    InstructionType.GET: 100,
    InstructionType.PUT: 100,
    InstructionType.LOAD: 10,
    InstructionType.STORE: 10,
    InstructionType.LOADI: 20,
    InstructionType.STOREI: 20,
    InstructionType.ADD: 10,
    InstructionType.SUB: 10,
    InstructionType.ADDI: 20,
    InstructionType.SUBI: 20,
    InstructionType.SET: 50,
    InstructionType.HALF: 5,
    InstructionType.JUMP: 1,
    InstructionType.JPOS: 1,
    InstructionType.JZERO: 1,
    InstructionType.JNEG: 1,
    InstructionType.RTRN: 10,
    InstructionType.HALT: 0
}

@dataclass
class Label:
    """Represents a jump target in the code."""
    name: str
    position: Optional[int] = None

@dataclass
class MemoryLocation:
    """Represents a memory location for a variable."""
    address: int
    size: int = 1  # For arrays, size > 1
    is_array: bool = False
    array_start: Optional[int] = None  # For arrays, the starting index
    array_end: Optional[int] = None    # For arrays, the ending index

class MemoryManager:
    """Manages memory allocation for variables and temporaries."""
    def __init__(self):
        self.next_address: int = 1  # p0 is accumulator
        self.memory_map: Dict[str, MemoryLocation] = {}
        self.temp_counter: int = 0
        
    def allocate(self, name: str, size: int = 1, is_array: bool = False,
                 array_start: Optional[int] = None, array_end: Optional[int] = None) -> MemoryLocation:
        if name in self.memory_map:
            return self.memory_map[name]
            
        location = MemoryLocation(
            address=self.next_address,
            size=size,
            is_array=is_array,
            array_start=array_start,
            array_end=array_end
        )
        self.memory_map[name] = location
        self.next_address += size
        return location
        
    def get_temp(self) -> str:
        """Get a new temporary variable name."""
        self.temp_counter += 1
        return f"_t{self.temp_counter}"
        
    def get_location(self, name: str) -> Optional[MemoryLocation]:
        return self.memory_map.get(name)
        
    def clear_temps(self):
        """Clear all temporary variables."""
        self.memory_map = {k: v for k, v in self.memory_map.items() 
                          if not k.startswith('_t')}
        
    def reset(self):
        """Reset the memory manager."""
        self.next_address = 1
        self.memory_map.clear()
        self.temp_counter = 0