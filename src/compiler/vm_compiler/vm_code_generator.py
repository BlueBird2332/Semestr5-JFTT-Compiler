from typing import List, Dict, Optional, Tuple
from ..intermediate_rep.IR_ops import *

class VMCodeGenerator:
    def __init__(self, memory_map, costly_ops={'*', '/', '%'}):
        self.memory_map = memory_map
        self.code: List[str] = []
        self.costly_ops = costly_ops
        
    def generate(self, ir_code: List[IRInstruction]) -> List[str]:
        """Generate VM code from IR instructions"""
        self.code = []
        
        for instr in ir_code:
            if isinstance(instr, IRLabel):
                # Keep label as placeholder for now
                self.code.append(f"LABEL_{instr.label_id}")
            elif isinstance(instr, IRJump):
                # Keep jump as placeholder for now
                self.code.append(f"JUMP_{instr.label}")
            elif isinstance(instr, IRCondJump):
                self._generate_cond_jump(instr)
            else:
                self._generate_instruction(instr)
                
        return self.code
        
    def _generate_instruction(self, instr: IRInstruction):
        """Generate code for a single IR instruction"""
        if isinstance(instr, IRAssign):
            self._generate_assign(instr)
        elif isinstance(instr, IRBinaryOp):
            self._generate_binary_op(instr)
        elif isinstance(instr, IRArrayRead):
            self._generate_array_read(instr)
        elif isinstance(instr, IRArrayWrite):
            self._generate_array_write(instr)
        elif isinstance(instr, IRProcCall):
            self._generate_proc_call(instr)
        elif isinstance(instr, IRRead):
            self._generate_read(instr)
        elif isinstance(instr, IRWrite):
            self._generate_write(instr)
            
    def _generate_assign(self, instr: IRAssign):
        """Generate code for assignment"""
        target_addr = self.memory_map.get_address(instr.target.name)
        value_addr = self.memory_map.get_address(instr.value.name)
        
        if instr.value.is_const:
            self.code.append(f"SET {instr.value.const_value}")
            self.code.append(f"STORE {target_addr}")
        else:
            self.code.append(f"LOAD {value_addr}")
            self.code.append(f"STORE {target_addr}")
            
    def _generate_binary_op(self, instr: IRBinaryOp):
        """Generate code for binary operation"""
        target_addr = self.memory_map.get_address(instr.target.name)
        left_addr = self.memory_map.get_address(instr.left.name)
        right_addr = self.memory_map.get_address(instr.right.name)
        
        # Load left operand to accumulator
        if instr.left.is_const:
            self.code.append(f"SET {instr.left.const_value}")
        else:
            self.code.append(f"LOAD {left_addr}")
            
        # Apply operation
        if instr.operator == '+':
            if instr.right.is_const:
                if instr.right.const_value != 0:  # Skip adding 0
                    self.code.append(f"SET {instr.right.const_value}")
                    self.code.append(f"ADD 0")
            else:
                self.code.append(f"ADD {right_addr}")
                
        elif instr.operator == '-':
            if instr.right.is_const:
                if instr.right.const_value != 0:  # Skip subtracting 0
                    self.code.append(f"SET {instr.right.const_value}")
                    self.code.append(f"SUB 0")
            else:
                self.code.append(f"SUB {right_addr}")
                
        elif instr.operator in {'*', '/', '%'}:
            # These operations should be handled by specialized routines
            self._generate_costly_op(instr)
            
        # Store result
        self.code.append(f"STORE {target_addr}")
        
    def _generate_costly_op(self, instr: IRBinaryOp):
        """Generate optimized code for multiplication, division, and modulo"""
        # This would contain the optimized implementations
        # For division and modulo: repeated subtraction with powers of 2
        # For multiplication: repeated addition with powers of 2
        # TODO: Implement optimized algorithms
        pass
            
    def _generate_array_read(self, instr: IRArrayRead):
        """Generate code for array read"""
        target_addr = self.memory_map.get_address(instr.target.name)
        array_info = self.memory_map.get_array_info(instr.array.name)
        
        if not array_info:
            raise ValueError(f"Array {instr.array.name} not found")
            
        base_addr, start_idx, _ = array_info
        
        # Calculate effective address: base + (index - start_idx)
        if instr.array.is_array_param:
            # For array parameters, load base address indirectly
            self.code.append(f"LOAD {base_addr}")  # Load base address
            self.code.append(f"STORE {target_addr}")  # Store temporarily
            
            # Load index
            if instr.index.is_const:
                self.code.append(f"SET {instr.index.const_value}")
            else:
                self.code.append(f"LOAD {self.memory_map.get_address(instr.index.name)}")
                
            # Subtract start index
            start_addr = base_addr + 1  # Address storing start index
            self.code.append(f"SUB {start_addr}")
            
            # Add to base address
            self.code.append(f"ADD {target_addr}")
            
            # Load value indirectly
            self.code.append("LOADI 0")
        else:
            # For regular arrays
            # Load index
            if instr.index.is_const:
                self.code.append(f"SET {instr.index.const_value}")
            else:
                self.code.append(f"LOAD {self.memory_map.get_address(instr.index.name)}")
                
            # Add base address
            self.code.append(f"SET {base_addr}")
            self.code.append("ADD 0")
            
            # Load value indirectly
            self.code.append("LOADI 0")
            
        # Store result
        self.code.append(f"STORE {target_addr}")
            
    def _generate_array_write(self, instr: IRArrayWrite):
        """Generate code for array write"""
        array_info = self.memory_map.get_array_info(instr.array.name)
        
        if not array_info:
            if not instr.array.is_temp:
                raise ValueError(f"Array {instr.array.name} not found")
            # For temporary arrays, get info directly from variable
            array_info = (self.memory_map.get_address(instr.array.name), 0, instr.array.array_size)
            
        base_addr, start_idx, _ = array_info
        
        # First load value to write
        if instr.value.is_const:
            self.code.append(f"SET {instr.value.const_value}")
        else:
            self.code.append(f"LOAD {self.memory_map.get_address(instr.value.name)}")
            
        # Store value temporarily
        temp_addr = self.memory_map.next_temp_addr - 1
        self.code.append(f"STORE {temp_addr}")
        
        # Calculate effective address
        if instr.array.is_array_param:
            # For array parameters, load base address indirectly
            self.code.append(f"LOAD {base_addr}")  # Load base address
            self.code.append(f"STORE {temp_addr + 1}")  # Store temporarily
            
            # Load index
            if instr.index.is_const:
                self.code.append(f"SET {instr.index.const_value}")
            else:
                self.code.append(f"LOAD {self.memory_map.get_address(instr.index.name)}")
                
            # Subtract start index
            start_addr = base_addr + 1
            self.code.append(f"SUB {start_addr}")
            
            # Add to base address
            self.code.append(f"ADD {temp_addr + 1}")
            
            # Load value and store indirectly
            self.code.append(f"LOAD {temp_addr}")
            self.code.append("STOREI 0")
        else:
            # For regular arrays
            # Load index
            if instr.index.is_const:
                self.code.append(f"SET {instr.index.const_value}")
            else:
                self.code.append(f"LOAD {self.memory_map.get_address(instr.index.name)}")
                
            # Add base address
            self.code.append(f"SET {base_addr}")
            self.code.append("ADD 0")
            
            # Store address temporarily
            self.code.append(f"STORE {temp_addr + 1}")
            
            # Load value and store indirectly
            self.code.append(f"LOAD {temp_addr}")
            self.code.append("STOREI 0")
            
    def _generate_proc_call(self, instr: IRProcCall):
        """Generate code for procedure call"""
        # Save return address first
        return_addr = self.memory_map.next_temp_addr - 1
        self.code.append(f"SET {return_addr}")
        self.code.append("STORE 1")  # Store return address
        
        # Handle parameters
        for i, arg in enumerate(instr.args):
            if arg.is_array_param or arg.is_array:
                # Pass array by reference
                if arg.is_array_param:
                    # If it's already a parameter, pass the stored reference
                    array_base = self.memory_map.get_address(arg.name)
                    self.code.append(f"LOAD {array_base}")  # Load base address
                    self.code.append(f"STORE {2 + i*2}")  # Store base address
                    self.code.append(f"LOAD {array_base + 1}")  # Load start index
                    self.code.append(f"STORE {2 + i*2 + 1}")  # Store start index
                else:
                    # Pass new array reference
                    array_info = self.memory_map.get_array_info(arg.name)
                    if not array_info:
                        raise ValueError(f"Array {arg.name} not found")
                    base_addr, start_idx, _ = array_info
                    
                    self.code.append(f"SET {base_addr}")
                    self.code.append(f"STORE {2 + i*2}")  # Store base address
                    self.code.append(f"SET {start_idx}")
                    self.code.append(f"STORE {2 + i*2 + 1}")  # Store start index
            else:
                # Pass value
                param_addr = 2 + i
                if arg.is_const:
                    self.code.append(f"SET {arg.const_value}")
                else:
                    self.code.append(f"LOAD {self.memory_map.get_address(arg.name)}")
                self.code.append(f"STORE {param_addr}")
                
        # Jump to procedure (will be replaced in final pass)
        self.code.append(f"CALL_{instr.name}")
        
    def _generate_read(self, instr: IRRead):
        """Generate code for read instruction"""
        target_addr = self.memory_map.get_address(instr.target.name)
        self.code.append(f"GET {target_addr}")
        
    def _generate_write(self, instr: IRWrite):
        """Generate code for write instruction"""
        if instr.value.is_const:
            self.code.append(f"SET {instr.value.const_value}")
            self.code.append("PUT 0")
        else:
            value_addr = self.memory_map.get_address(instr.value.name)
            self.code.append(f"PUT {value_addr}")
            
    def _generate_cond_jump(self, instr: IRCondJump):
        """Generate code for conditional jump"""
        # Load first value
        if instr.left.is_const:
            self.code.append(f"SET {instr.left.const_value}")
        else:
            self.code.append(f"LOAD {self.memory_map.get_address(instr.left.name)}")
            
        # Subtract second value
        if instr.right.is_const:
            self.code.append(f"SET {instr.right.const_value}")
            self.code.append("SUB 0")
        else:
            self.code.append(f"SUB {self.memory_map.get_address(instr.right.name)}")
            
        # Add jump placeholder - will be replaced in final pass
        self.code.append(f"CONDJUMP_{instr.operator}_{instr.label}")