from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from ..intermediate_rep.IR_ops import Variable

@dataclass
class MemoryCell:
    address: int
    is_array: bool = False
    array_start_address: Optional[int] = None
    array_size: Optional[int] = None

class MemoryMap:
    def __init__(self, variables: Dict[str, 'Variable']):
        """Initialize memory map and assign addresses for all variables"""
        # Initialize address counters
        self.next_regular_addr = 1     # Start at 1 since p[0] is accumulator
        self.next_temp_addr = 2**30    # Start temps from high address
        
        # Memory mappings
        self.memory: Dict[str, MemoryCell] = {}
        self.const_map: Dict[int, int] = {}  # value -> address mapping
        
        # Allocate all variables
        self._allocate_regular_variables(variables)
        self._allocate_constants(variables)
        self._allocate_temps(variables)
        
    def _allocate_regular_variables(self, variables: Dict[str, 'Variable']):
        """First pass - allocate regular variables and arrays"""
        for var_name, var in variables.items():
            if var.is_const or var.is_temp:
                continue
            
            # print(f"Allocating {var_name} {var.print_full()}")
            # To do always store pointer to 0th element of array
            if var.is_array and not var.is_pointer: #We need to initialize only arrays that are not parameters
                # ptr_addr = self.next_regular_addr
                
                # print(f"Allocating array {var_name} {var.print_full()}")
                
                offset = 0 - var.array_start
                # print(f"Offset: {offset} for {var_name}")
                current_memory = self.next_regular_addr
                
                self.next_regular_addr += var.array_size + 1
                # print(f"Next regular address: {self.next_regular_addr}")
                ptr_offset = current_memory + offset # To check
                # print(f"Ptr offset: {ptr_offset}")
                zero_adress = current_memory + offset

            
                
                
                    
                self.memory[var_name] = MemoryCell(
                    address=self.next_regular_addr +1,
                    is_array=True,
                    array_start_address=zero_adress,
                    array_size=var.array_size
                )

                self.next_regular_addr += var.array_size + 1
                
                
            else:
                self.memory[var_name] = MemoryCell(
                    address=self.next_regular_addr
                )
                self.next_regular_addr += 1
                
    def _allocate_constants(self, variables: Dict[str, 'Variable']):
        """Second pass - allocate constants with value deduplication"""
        for var_name, var in variables.items():
            if not var.is_const:
                continue
                
            # Skip if constant value is None
            if var.const_value is None:
                continue
                
            value = var.const_value
            if value in self.const_map:
                # Reuse existing address for this constant
                self.memory[var_name] = MemoryCell(
                    address=self.const_map[value]
                )
            else:
                # Allocate new address for this constant
                self.memory[var_name] = MemoryCell(
                    address=self.next_regular_addr
                )
                self.const_map[value] = self.next_regular_addr
                self.next_regular_addr += 1
                
    def _allocate_temps(self, variables: Dict[str, 'Variable']):
        """Third pass - allocate temporary variables from back"""
        for var_name, var in variables.items():
            if not var.is_temp:
                continue
                
            if var.is_array:
                # Allocate space for temp array
                self.next_temp_addr -= var.array_size
                self.memory[var_name] = MemoryCell(
                    address=self.next_temp_addr,
                    is_array=True,
                    array_start=var.array_start,
                    array_size=var.array_size
                )
            else:
                self.next_temp_addr -= 1
                self.memory[var_name] = MemoryCell(
                    address=self.next_temp_addr
                )
            
            
    def get_address(self, var_name: str) -> Optional[int]:
        """Get memory address for a variable"""
        # print(f"Getting address for {var_name}")

        if var_name in self.memory:
            # print(f"Returning {self.memory[var_name].address}")
            return self.memory[var_name].address
        
        raise RuntimeError(f'No adress for variable {var_name} found')
        return None
        
    def get_array_info(self, array_name: str) -> Optional[Tuple[int, int, int]]:
        """Get array (address, start_index, size)"""
        if array_name in self.memory:
            cell = self.memory[array_name]
            if cell.is_array:
                return (cell.address, cell.array_start_address, cell.array_size)
        return None
        
    def is_array(self, var_name: str) -> bool:
        """Check if variable is an array"""
        if var_name in self.memory:
            return self.memory[var_name].is_array
        return False
        
    def print_map(self):
        """Print memory map for debugging"""
        print("\nMemory Map:")
        print(f"Regular variables start: 1")
        print(f"Next regular address: {self.next_regular_addr}")
        print(f"Temp variables start: {self.next_temp_addr}")
        
        print("\nRegular Variables:")
        regular_vars = [(n,c) for n,c in self.memory.items() 
                       if c.address < self.next_regular_addr 
                       and not any(c.address == addr for addr in self.const_map.values())]
        for name, cell in sorted(regular_vars, key=lambda x: x[1].address):
            if cell.is_array:
                print(f"{name}: addr={cell.address}, start={cell.array_start_address}, size={cell.array_size}")
            else:
                print(f"{name}: addr={cell.address}")
                
        if self.const_map:
            print("\nConstant Values:")
            for value, addr in sorted(self.const_map.items()):
                const_vars = [name for name, cell in self.memory.items() 
                            if cell.address == addr]
                print(f"Value {value}: addr={addr} (used by: {', '.join(const_vars)})")
                
        print("\nTemporary Variables:")
        temp_vars = [(n,c) for n,c in self.memory.items() 
                    if c.address >= self.next_temp_addr]
        for name, cell in sorted(temp_vars, key=lambda x: x[1].address):
            print(f"{name}: addr={cell.address}")
            
    def print_map_to_file(self, file = 'memory_map'):
        """Print memory map to file"""
        with open(f"{file}.txt", "w") as f:
            f.write("Memory Map:\n")
            f.write(f"Regular variables start: 1\n")
            f.write(f"Next regular address: {self.next_regular_addr}\n")
            f.write(f"Temp variables start: {self.next_temp_addr}\n")
            
            f.write("\nRegular Variables:\n")
            regular_vars = [(n,c) for n,c in self.memory.items() 
                           if c.address < self.next_regular_addr 
                           and not any(c.address == addr for addr in self.const_map.values())]
            for name, cell in sorted(regular_vars, key=lambda x: x[1].address):
                if cell.is_array:
                    f.write(f"{name}: addr={cell.address}, start={cell.array_start_address}, size={cell.array_size}\n")
                else:
                    f.write(f"{name}: addr={cell.address}\n")
                    
            if self.const_map:
                f.write("\nConstant Values:\n")
                for value, addr in sorted(self.const_map.items()):
                    const_vars = [name for name, cell in self.memory.items() 
                                if cell.address == addr]
                    f.write(f"Value {value}: addr={addr} (used by: {', '.join(const_vars)})\n")
                    
            f.write("\nTemporary Variables:\n")
            temp_vars = [(n,c) for n,c in self.memory.items() 
                        if c.address >= self.next_temp_addr]
            for name, cell in sorted(temp_vars, key=lambda x: x[1].address):
                f.write(f"{name}: addr={cell.address}\n")