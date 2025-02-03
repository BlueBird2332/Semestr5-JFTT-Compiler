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
        self.instruction_counter = 0
        
        
        self.debug = False
        
        if self.debug:
            
            #print memory map
            print("MEMORY MAP")
            self.memory_map.print_map()
            self.memory_map.print_map_to_file()
            
            #print variables
            print("VARIABLESS")
            for k,v in variables.items():
                print(f"{k} -> {v.print_full()}")
                
            #print proc info
            
        
        # for k,v in variables.items():
        #     print(f"{k} -> {v.print_full()}")   
            
        
        
    def generate(self, ir_code: List[IRInstruction]) -> List[base_op]:
        """Generate VM code from IR instructions"""
        self.code = []
        
        if self.debug:
            print("Generating code")
            for instruction in ir_code:
                print(instruction.print_full()) 
        
        for k,v in self.variables.items():
            
            if v.is_array and not v.is_pointer:
                # print(f"Allocating array {v.name} {v.print_full()}")
                _, array_start_adress, _ = self.memory_map.get_array_info(v.name)
                self.code.append(SET(array_start_adress))
                self.code.append(STORE(self.memory_map.get_address(v.name)))
                self.instruction_counter += 2             
            
            
        
        
        self.generate_consts()
        
        for instruction in ir_code:
            self.code.extend(self.compile_ir(instruction))
            
        
        self.code.append(HALT())
        self.instruction_counter += 1
        
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
                self.instruction_counter += 2
            
    
    
    def compile_ir(self, op: IRInstruction) -> List[str]:
        if isinstance(op, IRLabel):
            # self.instruction_counter += 1
            if self.debug:
                print(f"IRLabel {op}")
                print("----"*8)
            
            
            
            return [LABEL(op.label_id)] 
        elif isinstance(op, IRRead):
            return self.compile_read_op(op) 
        elif isinstance(op, IRWrite):            
            return self.compile_write_op(op)

        elif isinstance(op, IRAssign):            
            return self.compile_assign_op(op)
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
        elif isinstance(op, IRReturn):
            return self.compile_return_op(op)
        elif isinstance(op, IRProcCall):
            return self.compile_proc_call_op(op)
        else:
                   
            raise RuntimeError(f"NOT WORKGWIRNG {op.__class__.__name__}")
        
        
    def compile_read_op(self, op: IRRead) -> List[str]:
        
        code = []
        target = op.target
        if isinstance(target, BY_REFERENCE):
            
            code.append(GET(0))
            code.append(STOREI(self.memory_map.get_address(target.name)))
            self.instruction_counter += 2
        else:
            
            code.append(GET(0))
            code.append(STORE(self.memory_map.get_address(target.name)))
            self.instruction_counter += 2
            
        if self.debug:
            print(f"IRRead {op}")
            for c in code:
                print(c)
            print("----"*8)
        
        return code
        
    def compile_write_op(self, op: IRWrite) -> List[str]:
        
        code = []
        value = op.value
        
        if isinstance(value, BY_REFERENCE):
            code.append(LOADI(self.memory_map.get_address(value.name)))
            code.append(PUT(0))
            self.instruction_counter += 2
        else:
            code.append(LOAD(self.memory_map.get_address(value.name)))
            code.append(PUT(0))
            self.instruction_counter += 2
        
        if self.debug:
            print(f"IRWrite {op}")
            for c in code:
                print(c)
            print("----"*8)
        
        return code       

    def compile_assign_op(self, op: IRAssign) -> List[str]:
        
        code = []
        target = op.target
        value = op.value
        
        if isinstance(value, BY_REFERENCE):
            code.append(LOADI(self.memory_map.get_address(value.name)))
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
                
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
                
            self.instruction_counter += 2
    
        else:
            code.append(LOAD(self.memory_map.get_address(value.name)))
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
                
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
                
            self.instruction_counter += 2
            
        
        if self.debug:
            print(f"IRAssign {op}")
            for c in code:
                print(c)
            print("----"*8)
            
        return code
            
        
    def compile_proc_call_op(self, op: IRProcCall) -> List[str]:
        # print(f"CALL {op}")
        # print(f"ARGS {op.args}")
        # print(f"PROC INFO {self.proc_info[op.name ]}")
        procedure_params = self.proc_info[op.name].arguments
        # print(f"DECLARATION PARAMS {procedure_params}")
        
        code = []
        
        for passed_argument, param_signature in zip(op.args, procedure_params):
                    
            if passed_argument.is_array or passed_argument.is_pointer:
                
                code.append(LOAD(self.memory_map.get_address(passed_argument.name)))
                code.append(STORE(self.memory_map.get_address(param_signature.name)))
            else:
                code.append(SET(self.memory_map.get_address(passed_argument.name)))
                code.append(STORE(self.memory_map.get_address(param_signature.name)))
            self.instruction_counter +=2
        proc_label = self.proc_info[op.name].begin_id
        

        # print(f"RETURN ADDRESS {return_address} from line {self.instruction_counter}")
        code.append(SET_HERE(3))
        code.append(STORE(self.memory_map.get_address(self.proc_info[op.name].return_var.name)))
        code.append(JUMPLABEL(proc_label))
        self.instruction_counter += 3  # Coun
            
            
        if self.debug:
            print(f"IRProcCall {op}")
            for c in code:
                print(c)
            print("----"*8)
        return code
         
    def compile_return_op(self, op: IRReturn) -> List[str]:
        
        code = []
        
        return_value = op.return_variable
        self.instruction_counter += 1
        code.append(RETURN(self.memory_map.get_address(return_value.name)))
        
        if self.debug:
            print(f"IRReturn {op}")
            for c in code:
                print(c)
            print("----"*8)
        
        return code
        
    def compile_binary_op(self, op: IRBinaryOp) -> List[str]:
        
        target = op.target
        left = op.left
        right = op.right
        operator = op.operator
        
        code = []
        
        if operator == '+':
            
            if isinstance(left, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
            self.instruction_counter += 1
            
            if isinstance(right, BY_REFERENCE):
                code.append(ADDI(self.memory_map.get_address(right.name)))
            else:
                code.append(ADD(self.memory_map.get_address(right.name)))
            self.instruction_counter += 1
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
            self.instruction_counter += 1
            
        elif operator == '-':
            
            if isinstance(left, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
            self.instruction_counter += 1
            
            if isinstance(right, BY_REFERENCE):
                code.append(SUBI(self.memory_map.get_address(right.name)))
            else:
                code.append(SUB(self.memory_map.get_address(right.name)))
            self.instruction_counter += 1
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
            self.instruction_counter += 1
            
            
        elif operator == '*':
            
            if isinstance(left, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
            self.instruction_counter += 1
            
            code.append(STORE(self.memory_map.get_address("arg1")))
            
            if isinstance(right, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(right.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(right.name)))
            self.instruction_counter += 1
            
            code.append(STORE(self.memory_map.get_address("arg2")))
    
            
            return_address = self.instruction_counter + 3
            # print(f"RETURN ADDRESS {return_address} from line {self.instruction_counter}")
            code.append(SET_HERE(3))
            code.append(STORE(self.memory_map.get_address(self.proc_info["mul"].return_var.name)))
            code.append(JUMPLABEL(self.proc_info["mul"].begin_id))
            self.instruction_counter += 3
            
            code.append(LOAD(self.memory_map.get_address("result")))
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
        
        elif operator == '/':
            
            if isinstance(left, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
            self.instruction_counter += 1
            
            code.append(STORE(self.memory_map.get_address("arg1")))
            
            if isinstance(right, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(right.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(right.name)))
            self.instruction_counter += 1
            
            code.append(STORE(self.memory_map.get_address("arg2")))
            
            return_address = self.instruction_counter + 3
            # print(f"RETURN ADDRESS {return_address} from line {self.instruction_counter}")
            code.append(SET_HERE(3))
            code.append(STORE(self.memory_map.get_address(self.proc_info["div"].return_var.name)))
            code.append(JUMPLABEL(self.proc_info["div"].begin_id))
            self.instruction_counter += 3
            
            code.append(LOAD(self.memory_map.get_address("result")))
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
        
        elif operator == '%':
            
            if isinstance(left, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(left.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(left.name)))
            self.instruction_counter += 1
            
            code.append(STORE(self.memory_map.get_address("arg1")))
            
            if isinstance(right, BY_REFERENCE):
                code.append(LOADI(self.memory_map.get_address(right.name)))
            else:
                code.append(LOAD(self.memory_map.get_address(right.name)))
            self.instruction_counter += 1
            
            code.append(STORE(self.memory_map.get_address("arg2")))
            
            return_address = self.instruction_counter + 3
            # print(f"RETURN ADDRESS {return_address} from line {self.instruction_counter}")
            code.append(SET_HERE(3))
            code.append(STORE(self.memory_map.get_address(self.proc_info["div"].return_var.name)))
            code.append(JUMPLABEL(self.proc_info["div"].begin_id))
            self.instruction_counter += 3
            
            code.append(LOAD(self.memory_map.get_address("result2")))
            
            if isinstance(target, BY_REFERENCE):
                code.append(STOREI(self.memory_map.get_address(target.name)))
            else:
                code.append(STORE(self.memory_map.get_address(target.name)))
            
            
                     
            
                
            
        if self.debug:
            print(f"IRBinaryOp {op}")
            for c in code:
                print(c)
            print("----"*8)
            
                
        return code
            
        
    
    def compile_jump_op(self, op: IRJump) -> List[str]:
        code = []
        self.instruction_counter += 1
        code.append(JUMPLABEL(op.label))
        
        if self.debug:
            print(f"IRJumpLabel {op}")
            for c in code:
                print(c)
            print("----"*8) 
        
        return code
    
    def compile_half_op(self, op: IRHalf) -> List[str]:
        code = []
        target = op.target
        
        if isinstance(target, BY_REFERENCE):
            code.append(LOADI(self.memory_map.get_address(target.name)))
            code.append(HALF())
            code.append(STOREI(self.memory_map.get_address(target.name)))
            self.instruction_counter += 3   
        else:
            code.append(LOAD(self.memory_map.get_address(target.name)))
            code.append(HALF())
            code.append(STORE(self.memory_map.get_address(target.name)))
            self.instruction_counter += 3
        
        if self.debug:
            print(f"IRHalf {op}")
            for c in code:
                print(c)
            print("----"*8)
            
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
        self.instruction_counter += 3
        
        if target.is_param:
            code.append(STOREI(self.memory_map.get_address(target.name)))
            
        else:
            code.append(STORE(self.memory_map.get_address(target.name)))
        self.instruction_counter += 1
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
        self.instruction_counter += 3

        self.instruction_counter += 2
        if value.is_param:
            code.append(LOADI(value_adress))
        else:
            code.append(LOAD(value_adress))
            
        code.append(STOREI(temp_adress))
            
        return code
        
        
        
        
    def compile_cond_jump_op(self, op: IRCondJump) -> List[str]:
        
 
        
        code = []
        
        operator = op.operator
        left = op.left
        right = op.right
        
        if isinstance(left, BY_REFERENCE):
            code.append(LOADI(self.memory_map.get_address(left.name)))
        else:
            code.append(LOAD(self.memory_map.get_address(left.name)))
            
        if isinstance(right, BY_REFERENCE):
            code.append(SUBI(self.memory_map.get_address(right.name)))
        else:
            code.append(SUB(self.memory_map.get_address(right.name)))
            
        self.instruction_counter += 3

        if operator == '=':
            code.append(JZERO_LABEL(op.label))           
        elif operator == '>':
            code.append(JPOS_LABEL(op.label))
        elif operator == '<':
            code.append(JNEG_LABEL(op.label))
            
        else:
            raise RuntimeError(f"Operator {operator} not supported")
        
        if self.debug:
            print(f"IRCondJump {op}")
            for c in code:
                print(c)
            
        return code
    

            
        
            
        
        
        
        
        
        
        
       