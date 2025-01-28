from typing import List, Dict, Optional, Tuple
from ..intermediate_rep.IR_ops import *
from ..pre_assembler.memory_map import MemoryMap
from .vm_operators import *
from .label_correct import correct_labels

class VMCodeGenerator:
    def __init__(self, memory_map: MemoryMap, variables, proc_info, costly_ops={'*', '/', '%'}):
        self.memory_map = memory_map
        self.code: List[str] = []
        self.variables = variables
        self.costly_ops = costly_ops
        self.proc_info = proc_info
        
        memory_map.print_map()
        
        for k,v in variables.items():
            print(f"{k} -> {v.print_full()}")   
            
        
        
    def generate(self, ir_code: List[IRInstruction]) -> List[base_op]:
        """Generate VM code from IR instructions"""
        self.code = []
        
        for k,v in self.variables.items():
            if v.is_array and not v.is_param:
                print(f"ARRAY {v.name}")
                self.code.append(SET(self.memory_map.get_address(v.name)))
                self.
        
        
        self.generate_consts()
        
        for instruction in ir_code:
            self.code.extend(self.compile_ir(instruction))
            
        
        self.code.append(HALT())
        
        self.code = correct_labels(self.code)
            
        return self.code
    
    def generate_consts(self):
        for k,v in self.variables.items():
            if v.is_const:
                adress = self.memory_map.get_address(v.name)
                self.code.extend([
                    SET(v.const_value),
                    STORE(adress)
                ])
            
    
    
    def compile_ir(self, op: IRInstruction) -> List[str]:
        if isinstance(op, IRLabel):
            return [LABEL(op.label_id)]
        elif isinstance(op, IRRead):
            target = self.memory_map.get_address(op.target.name)
            return[GET(target)]
        elif isinstance(op, IRWrite):
            target = self.memory_map.get_address(op.value.name)
            return[PUT(target)]
        elif isinstance(op, IRAssign):
            target = self.memory_map.get_address(op.target.name)
            src = self.memory_map.get_address(op.value.name)
            code = []
            # print(f"op.assignment {op.value}")
            if op.value.is_param:
                # print(f"op.value {op.value} is param")
                code.append(LOADI(src))
            else:
                code.append(LOAD(src))
            if op.target.is_param:
                code.append(STOREI(target))
            else:
                code.append(STORE(target))
            # print(f"code {code}")
            # print(f"current code {self.code}")  
            return code
        elif isinstance(op, IRCondJump):
            return self.compile_cond_jump_op(op)
        elif isinstance(op, IRArrayRead):
            return self.compile_array_read_op(op)
        elif isinstance(op, IRArrayWrite):
            return self.compile_array_write_op(op)
        elif isinstance(op, IRJump):
            return self.compile_jump_op(op)
        elif isinstance(op, IRHalf):
            return self.compile_half_op(op)
        elif isinstance(op, IRBinaryOp):
            return self.compile_binary_op(op)
        else:
                   
            raise RuntimeError(f"NOT WORKGWIRNG {op.__class__.__name__}")
        
    def compile_binary_op(self, op: IRBinaryOp) -> List[str]:
        
        target = op.target
        left = op.left
        right = op.right
        operator = op.operator
        
        code = []
        
        if operator == '+':
            if left.is_param:
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
                
            if right.is_param:
                code.append(ADDI(self.memory_map.get_address(right.name)))
            else:
                print("RIGHT", right)
                print(f"RIGHT ADRESS {self.memory_map.get_address(right.name)}")
                code.append(ADD(self.memory_map.get_address(right.name)))
            
            if target.is_param:
                code.append(STOREI(self.memory_map.get_address(target.name)))
                
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
                
        elif operator == '-':
            
            if left.is_param:
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
                
            if right.is_param:
                code.append(SUBI(self.memory_map.get_address(right.name)))
            else:
                code.append(SUB(self.memory_map.get_address(right.name)))
            
            if target.is_param:
                code.append(STOREI(self.memory_map.get_address(target.name)))
                
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
                
        return code
        
        
        
    
    def compile_jump_op(self, op: IRJump) -> List[str]:
        code = []
        code.append(JUMPLABEL(op.label))
        return code
    
    def compile_half_op(self, op: IRHalf) -> List[str]:
        code = []
        target = op.target
        
        if target.is_param:
            code.append(LOADI(self.memory_map.get_address(target.name)))
            code.append(HALF())
            code.append(STOREI(self.memory_map.get_address(target.name)))
            
        else:
            code.append(LOAD(self.memory_map.get_address(target.name)))
            code.append(HALF())
            code.append(STORE(self.memory_map.get_address(target.name)))
            
        return code
    
    def compile_array_read_op(self, op: IRArrayRead) -> List[str]:
        
        start = op.array
        index = op.index #always temp
        index_adress = self.memory_map.get_address(index.name)
        target = op.target
        
        code = []
        
        code.append(LOAD(self.memory_map.get_address(start.name)))
        code.append(ADD(self.memory_map.get_address(index.name)))
        code.append(LOADI(0))
        
        if target.is_param:
            code.append(STOREI(self.memory_map.get_address(target.name)))
            
        else:
            code.append(STORE(self.memory_map.get_address(target.name)))
            
        return code
    
    def compile_array_write_op(self, op: IRArrayWrite) -> List[str]:
        
        start = op.array
        index = op.index
        value = op.value
        
        start_adress = self.memory_map.get_address(start.name)
        index_adress = self.memory_map.get_address(index.name)
        value_adress = self.memory_map.get_address(value.name)
        temp_adress = self.memory_map.get_address("temp")
        code = []
        
        code.append(LOAD(start_adress))
        code.append(ADD(index_adress))
        code.append(STORE(temp_adress))
        

        
        if value.is_param:
            code.append(LOADI(value_adress))
        else:
            code.append(LOAD(value_adress))
            
        code.append(STOREI(temp_adress))
            
        return code
        
        
        
        
    def compile_cond_jump_op(self, op: IRCondJump) -> List[str]:
        print("____")
        print(op)
        
        code = []
        
        operator = op.operator
        left = op.left
        right = op.right
        
        if left.is_param:
            code.append(LOADI(self.memory_map.get_address(left.name)))
        else:
            code.append(LOAD(self.memory_map.get_address(left.name)))
            
        if right.is_param:
            code.append(SUBI(self.memory_map.get_address(right.name)))
        else:
            code.append(SUB(self.memory_map.get_address(right.name)))

        if operator == '=':
            code.append(JZERO_LABEL(op.label))           
        elif operator == '>':
            code.append(JPOS_LABEL(op.label))
        elif operator == '<':
            code.append(JNEG_LABEL(op.label))
            
        return code
            
        
            
        
        
        
        
        
        
        
       