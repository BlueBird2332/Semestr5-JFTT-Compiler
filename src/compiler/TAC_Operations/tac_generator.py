from typing import List, Dict, Optional, Union, Tuple
from dataclasses import dataclass
from .tac_ops import *
from .arithmetic import ArithmeticGenerator
from ..ast_nodes import *
from ..symbol_table import SymbolTable

class TempGenerator:
    """Generates unique temporary variables and labels"""
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self._loop_stack = []  # For managing nested loops
        self._condition_counter = 0  # For managing complex conditions
    
    def get_temp(self) -> str:
        temp = f"_t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def get_label(self, prefix: str = "L") -> str:
        label = f"{prefix}_{self.label_counter}"
        self.label_counter += 1
        return label
    
    def get_condition_var(self) -> str:
        var = f"_cond{self._condition_counter}"
        self._condition_counter += 1
        return var
    
    def push_loop(self, start_label: str, end_label: str) -> None:
        self._loop_stack.append((start_label, end_label))
    
    def pop_loop(self) -> Tuple[str, str]:
        return self._loop_stack.pop()
    
    def current_loop(self) -> Tuple[str, str]:
        if not self._loop_stack:
            raise ValueError("No active loop")
        return self._loop_stack[-1]

class TACGenerator:
    """Main TAC code generator that uses the symbol table"""
    
    def __init__(self, symbol_table):
        self.temp_generator = TempGenerator()
        self.arithmetic = ArithmeticGenerator(self.temp_generator)
        self.symbol_table = symbol_table
        self.tac_instructions: List[TACOp] = []
        self.memory_map: Dict[str, int] = {}  # Maps symbol names to memory locations
        self.next_memory_location = 1  # Reserve 0 for accumulator
        self.return_address_location = None  # Will be set during memory allocation
        
    def get_memory_location(self, name: str) -> int:
        """Get memory location for a variable, considering current scope"""
        symbol = self.symbol_table.lookup(name)
        if not symbol:
            raise ValueError(f"Symbol {name} not found in current scope")
            
        scoped_name = self.symbol_table.make_scoped_name(name, symbol.procedure_name)
        return self.memory_map[scoped_name]

    def allocate_memory(self) -> None:
        """Allocate memory for all program variables and procedure parameters"""
        # Reserve space for return address
        self.return_address_location = self.next_memory_location
        self.next_memory_location += 1

        # First allocate global variables
        for symbol in self.symbol_table.symbols.values():
            if symbol.symbol_type == 'global':
                scoped_name = self.symbol_table.make_scoped_name(symbol.name, None)
                if symbol.is_array:
                    # For arrays, we initially just allocate space for the base address
                    # Actual array space will be allocated at runtime
                    self.memory_map[scoped_name] = self.next_memory_location
                    self.next_memory_location += 1  # Just one location for base pointer
                else:
                    self.memory_map[scoped_name] = self.next_memory_location
                    self.next_memory_location += 1

        # Then handle procedure variables
        for proc_name in self.symbol_table.procedures:
            for symbol in self.symbol_table.symbols.values():
                if symbol.procedure_name == proc_name:
                    scoped_name = self.symbol_table.make_scoped_name(symbol.name, proc_name)
                    
                    if symbol.is_parameter:
                        if symbol.is_array_parameter:
                            # For array parameters, just store the reference
                            self.memory_map[scoped_name] = self.next_memory_location
                            self.next_memory_location += 1
                        else:
                            # Regular parameters - store the reference location
                            self.memory_map[scoped_name] = self.next_memory_location
                            self.next_memory_location += 1
                    else:
                        # Local variables
                        if symbol.is_array:
                            # Local arrays also just get a base pointer initially
                            self.memory_map[scoped_name] = self.next_memory_location
                            self.next_memory_location += 1
                        else:
                            # Regular local variables
                            self.memory_map[scoped_name] = self.next_memory_location
                            self.next_memory_location += 1

    def visit_condition(self, node, jump_true: str, jump_false: str) -> None:
        """Generate code for a condition with jumps to appropriate labels"""
        left = self.visit_expression(node.left)
        right = self.visit_expression(node.right)
        result = self.temp_generator.get_temp()

        # Transform condition into equivalent arithmetic operation
        # All conditions are transformed into "left - right" form
        # and then appropriate jump is used based on the operator
        self.tac_instructions.append(BinaryOp(result, BinaryOpType.SUB, left, right))

        if node.operator == '=':
            self.tac_instructions.append(CondJump(result, jump_false, "JZERO"))
            self.tac_instructions.append(Jump(jump_true))
        elif node.operator == '!=':
            self.tac_instructions.append(CondJump(result, jump_true, "JZERO"))
            self.tac_instructions.append(Jump(jump_false))
        elif node.operator == '<':
            self.tac_instructions.append(CondJump(result, jump_true, "JNEG"))
            self.tac_instructions.append(Jump(jump_false))
        elif node.operator == '<=':
            self.tac_instructions.append(CondJump(result, jump_false, "JPOS"))
            self.tac_instructions.append(Jump(jump_true))
        elif node.operator == '>':
            self.tac_instructions.append(CondJump(result, jump_true, "JPOS"))
            self.tac_instructions.append(Jump(jump_false))
        elif node.operator == '>=':
            self.tac_instructions.append(CondJump(result, jump_false, "JNEG"))
            self.tac_instructions.append(Jump(jump_true))

    def visit_if(self, node) -> None:
        """Process if statement"""
        else_label = self.temp_generator.get_label("else")
        end_label = self.temp_generator.get_label("endif")

        # Generate condition code
        if node.else_block:
            self.visit_condition(node.condition, else_label, end_label)
        else:
            self.visit_condition(node.condition, end_label, else_label)

        # Generate then block
        self.visit_commands(node.then_block)
        if node.else_block:
            self.tac_instructions.append(Jump(end_label))
            self.tac_instructions.append(Label(else_label))
            self.visit_commands(node.else_block)

        self.tac_instructions.append(Label(end_label))

    def visit_while(self, node) -> None:
        """Process while loop"""
        start_label = self.temp_generator.get_label("while")
        end_label = self.temp_generator.get_label("endwhile")
        
        self.temp_generator.push_loop(start_label, end_label)
        
        # Generate loop structure
        self.tac_instructions.append(Label(start_label))
        self.visit_condition(node.condition, end_label, None)  # Jump to end if condition false
        
        # Generate loop body
        self.visit_commands(node.body)
        self.tac_instructions.append(Jump(start_label))
        
        self.tac_instructions.append(Label(end_label))
        self.temp_generator.pop_loop()

    def visit_repeat(self, node) -> None:
        """Process repeat-until loop"""
        start_label = self.temp_generator.get_label("repeat")
        condition_label = self.temp_generator.get_label("until")
        
        self.temp_generator.push_loop(start_label, condition_label)
        
        # Generate loop structure
        self.tac_instructions.append(Label(start_label))
        
        # Generate loop body
        self.visit_commands(node.body)
        
        # Generate condition check
        self.tac_instructions.append(Label(condition_label))
        self.visit_condition(node.condition, start_label, None)  # Jump back if condition false
        
        self.temp_generator.pop_loop()

    def visit_for(self, node) -> None:
        """Process for loop"""
        start_label = self.temp_generator.get_label("for")
        end_label = self.temp_generator.get_label("endfor")
        
        # Get iterator location
        iterator_loc = self.get_memory_location(node.iterator)
        
        # Initialize iterator
        start_value = self.visit_expression(node.start)
        end_value = self.visit_expression(node.end)
        self.tac_instructions.append(Copy(f"p{iterator_loc}", start_value))
        
        # Set up loop
        self.temp_generator.push_loop(start_label, end_label)
        self.tac_instructions.append(Label(start_label))
        
        # Check loop condition
        condition = self.temp_generator.get_temp()
        if not node.downto:
            # Normal FOR: check if iterator <= end
            self.tac_instructions.append(
                BinaryOp(condition, BinaryOpType.SUB, f"p{iterator_loc}", end_value)
            )
            self.tac_instructions.append(CondJump(condition, end_label, "JPOS"))
        else:
            # DOWNTO: check if iterator >= end
            self.tac_instructions.append(
                BinaryOp(condition, BinaryOpType.SUB, end_value, f"p{iterator_loc}")
            )
            self.tac_instructions.append(CondJump(condition, end_label, "JPOS"))
        
        # Generate loop body
        self.visit_commands(node.body)
        
        # Increment/decrement iterator
        if not node.downto:
            self.tac_instructions.append(
                BinaryOp(f"p{iterator_loc}", BinaryOpType.ADD, f"p{iterator_loc}", "1")
            )
        else:
            self.tac_instructions.append(
                BinaryOp(f"p{iterator_loc}", BinaryOpType.SUB, f"p{iterator_loc}", "1")
            )
        
        self.tac_instructions.append(Jump(start_label))
        self.tac_instructions.append(Label(end_label))
        
        self.temp_generator.pop_loop()

    def visit_procedure_call(self, node) -> None:
        """Process procedure call"""
        proc_params = self.symbol_table.get_procedure_params(node.name)
        if not proc_params:
            raise ValueError(f"Procedure {node.name} not found")

        # Save return address
        return_label = self.temp_generator.get_label("return")
        self.tac_instructions.append(LoadImmediate(f"p{self.return_address_location}", return_label))

        # Process arguments
        for (param_name, is_array_param), arg in zip(proc_params, node.arguments):
            param_loc = self.get_memory_location(f"{node.name}_{param_name}")
            
            if is_array_param:
                # For array parameters, pass the base address
                arg_base_loc = self.get_memory_location(arg.name)
                self.tac_instructions.append(LoadImmediate(f"p{param_loc}", arg_base_loc))
            else:
                # For value parameters, evaluate and pass the value
                arg_value = self.visit_expression(arg)
                self.tac_instructions.append(Copy(f"p{param_loc}", arg_value))

        # Jump to procedure
        self.tac_instructions.append(Jump(f"proc_{node.name}"))
        self.tac_instructions.append(Label(return_label))

    def visit_read(self, node) -> None:
        """Process read command"""
        if isinstance(node.target, Identifier) and node.target.array_index is not None:
            # Reading into array element
            array_symbol = self.symbol_table.lookup(node.target.name)
            array_base = self.get_memory_location(node.target.name)
            
            if isinstance(node.target.array_index, Number):
                # Static array index
                index_offset = node.target.array_index.value - array_symbol.array_start
                self.tac_instructions.append(Read(f"p{array_base + index_offset}"))
            else:
                # Dynamic array index
                index = self.visit_expression(node.target.array_index)
                offset = self.temp_generator.get_temp()
                if array_symbol.array_start != 0:
                    self.tac_instructions.append(
                        BinaryOp(offset, BinaryOpType.SUB, index, str(array_symbol.array_start))
                    )
                else:
                    self.tac_instructions.append(Copy(offset, index))
                temp = self.temp_generator.get_temp()
                self.tac_instructions.append(Read(temp))
                self.tac_instructions.append(ArrayStore(f"p{array_base}", offset, temp))
        else:
            # Reading into simple variable
            target_loc = self.get_memory_location(node.target.name)
            self.tac_instructions.append(Read(f"p{target_loc}"))

    def visit_write(self, node) -> None:
        """Process write command"""
        value = self.visit_expression(node.value)
        self.tac_instructions.append(Write(value))

    
    def allocate_array(base_ptr: str, size: Union[str, int]) -> List[TACOp]:
        """Generate TAC for array allocation"""
        ops = []
        # Generate allocation
        ops.append(ArrayAlloc(base_ptr, size))
        return ops

    def deallocate_array(array: str) -> List[TACOp]:
        """Generate TAC for array deallocation"""
        ops = []
        ops.append(ArrayDealloc(array))
        return ops
    
    def generate_code(self, ast) -> List[TACOp]:
        """Main entry point for code generation"""
        # First allocate memory for all variables
        self.allocate_memory()
        for key, value in self.memory_map.items():
            print(key, value)
        
        # Generate code starting from the program node
        # self.visit_program(ast)
        
        return self.tac_instructions