from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

from ..ast_nodes import *
from ..symbol_table import Symbol, SymbolTable
from .arithmetic import IRArithmetic
from .IR_ops import *
from .procinfo import ProcInfo



class IRGenerator:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.temp_counter = 0
        self.label_manager = LabelManager()
        self.code: List[IRInstruction] = []
        self.current_proc: Optional[str] = None
        self.costly_ops = symbol_table.costly_operations
        # self.numeric_variables = dict()
        self.dummy_loc = Location(0, 0)
        self.variables: dict[str, Variable] = dict()
        self.proc_info: Dict[str, ProcInfo] = dict()
        self.arithmetic = IRArithmetic(self.label_manager, self.variables, self.proc_info)

    
    def create_variable(self, name: Union[str, int],
                        proc_name:str = None,
                        is_temp: bool = False,
                        is_const: bool = False,
                        is_array: bool = False,
                        is_pointer: bool = False,              
                        array_start: Optional[int] = None,
                        array_size: Optional[int] = None) -> Variable:
        
        var_name = str(name)
        if self.current_proc and not var_name.startswith(self.current_proc + "#") and not is_const and not is_temp:
            var_name = f"{self.current_proc}#{name}"
            
        if var_name not in self.variables:
            
            if is_array:
                var = Variable.create_array(
                    name=var_name,
                    start=array_start,
                    size=array_size,
                    proc_name=proc_name
                )
                
            elif is_pointer and not is_temp:
                var = Variable.create_param(name=var_name, proc_name=proc_name)
                
            elif is_const:
                var = Variable.from_number(var_name)
                
            elif is_temp:
                self.temp_counter += 1
                temp_name = f"t{self.temp_counter}"
                var = Variable.create_temp(temp_name, self.current_proc, is_pointer=is_pointer)

                
            else:                
                var = Variable(name=var_name, proc_name=proc_name)
            self.variables[var_name] = var
            return var            
        
        return self.variables[var_name]

    def generate(self, node: Program) -> List[IRInstruction]:
        """Generate IR for entire program"""
        
        glob_temp = self.create_variable("global##temp", is_temp=True)
        
        
        self.code = []
        
        main_label = self.label_manager.new_label(
            LabelType.MAIN_START, "Main program start"
        )
        
        self.proc_info['main'] = ProcInfo(
            begin_id=main_label,
            arguments=[],
            return_var=None
        )
    

        self.code.extend([
            IRJump(label=main_label, comment="Jump to main program start"),
        ])
        
        if self.costly_ops:
            self.code.extend(self.arithmetic.generate_arithmetic_procedures(self.costly_ops))
              
            
        for proc in node.procedures:
            self._generate_procedure(proc)
        
        # zero_var = self.create_variable(0, is_const=True)
        # one_var = self.create_variable(1, is_const=True)
        # neg_one_var = self.create_variable(-1, is_const=True)
        
        
        self.process_declarations(node.declarations)
        
        self.code.append(
            IRLabel(
                label_id=main_label, 
                label_type=LabelType.MAIN_START, 
                comment=self.label_manager.get_comment(main_label),
                procedure="main"
            )
        )
        
        for cmd in node.commands:
            self._generate_command(cmd)
            
            
        return self.code, self.variables, self.proc_info
        
    def _generate_procedure(self, proc: Procedure) -> None:
        """Generate IR for procedure definition"""       
              
        self.current_proc = proc.name       
                
        proc_label = self.label_manager.new_label(
            LabelType.PROC_START, f"{proc.name} procedure"
        )
        self.code.append(
            IRLabel(
                label_id=proc_label, 
                comment=self.label_manager.get_comment(proc_label).upper(),
                procedure=proc.name,
                label_type=LabelType.PROC_START                
            )
        )

        self.process_parameters(proc.name, proc.parameters, start_id=proc_label)
        self.process_declarations(proc.declarations, proc.name)

        # Generate procedure body
        for cmd in proc.commands:
            self._generate_command(cmd)

        ret = self.proc_info[self.current_proc].return_var
        self.code.append(
            IRReturn(return_variable=ret, comment=f"End of procedure {proc.name}")
        )
        
        self.current_proc = None
        
    def process_declarations(self, declarations: List[Declaration], proc_name: Optional[str] = None) -> None:
        """Process declarations and register variables"""
        
        for decl in declarations:
            name = decl.name
            if self.current_proc:
                name = self.current_proc + "#" + decl.name
            if decl.array_bounds:
                # Create array variable
                start, end = decl.array_bounds
                # print(f"ARRAY BOUNDS for {decl.name}: {start}, {end}")
                array_var = self.create_variable(
                    name=name,
                    proc_name=proc_name,
                    is_array=True,
                    array_start=start,
                    array_size=end - start + 1
                )
            else:
                var = self.create_variable(
                    name=name,
                    proc_name=proc_name
                )


    def process_parameters(self, proc_name: str, parameters: List[Tuple[str, bool]], start_id = None) -> None:
        """Process procedure parameters and register parameter variables"""
        vars = []
        
        for param_name, is_array in parameters:
            if self.current_proc:
                param_name = self.current_proc + "#" + param_name

            param_var = self.create_variable(
                name=param_name,
                proc_name=proc_name,
                is_pointer=True,
                # is_array=True
            )
            vars.append(param_var)
                
        self.proc_info[self.current_proc] = ProcInfo(
            begin_id=start_id,
            arguments=vars,
            return_var=self.create_variable(name = f"{proc_name}#return", proc_name=proc_name)
        )
        

    def _generate_command(self, cmd: Command) -> None:
        if isinstance(cmd, Assignment):
            self._generate_assignment(cmd)
        elif isinstance(cmd, IfStatement):
            self._generate_if(cmd)
        elif isinstance(cmd, WhileLoop):
            self._generate_while(cmd)
        elif isinstance(cmd, RepeatLoop):
            self._generate_repeat(cmd)
        elif isinstance(cmd, ForLoop):
            self._generate_for(cmd)
        elif isinstance(cmd, ProcedureCall):
            self._generate_proc_call(cmd)
        elif isinstance(cmd, ReadCommand):
            self._generate_read(cmd)
        elif isinstance(cmd, WriteCommand):
            self._generate_write(cmd)

    def _generate_assignment(self, cmd: Assignment) -> None:
        if isinstance(cmd.target, Identifier) and cmd.target.array_index is not None:
            # Handle array assignment
            array_var = self.create_variable(cmd.target.name, proc_name=self.current_proc)
            index = self._generate_value(cmd.target.array_index)
            
            if index.is_pointer:
                index = wrap_by_reference(index)
            else:
                index = wrap_by_value(index)
            
            offset = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True, is_pointer=True)
            offset_copy = offset
            self.code.append(
                IRBinaryOp(
                    target=wrap_by_value(offset),
                    left=wrap_by_value(self.create_variable(f"{cmd.target.name}", proc_name=self.current_proc)),
                    right=index,
                    operator="+",
                    comment=f"Calculate array offset for assignment"
                )
            )
            
            # Generate the value to assign
            if isinstance(cmd.value, BinaryOp):
                if cmd.value.operator in self.costly_ops:
                    temp = offset_copy# arguments go by reference
                    self._generate_optimized_op(temp, cmd.value)
                    value = wrap_by_reference(temp)
                else:
                    temp = offset_copy
                    left = self._generate_value(cmd.value.left)                    
                    if left.is_pointer:
                        left = wrap_by_reference(left)
                    else:
                        left = wrap_by_value(left)
                        
                    right = self._generate_value(cmd.value.right)
                    if right.is_pointer:
                        right = wrap_by_reference(right)
                    else:
                        right = wrap_by_value(right)
                        
                    temp = wrap_by_reference(temp)
                    
                    self.code.append(
                        IRBinaryOp(
                            target=temp,
                            left=left,
                            right=right,
                            operator=cmd.value.operator,
                            comment=f"Compute value for array assignment"
                        )
                    )
                    value = wrap_by_value(temp)
            else:
                value = self._generate_value(cmd.value)       
                if value.is_pointer:
                    value = wrap_by_reference(value)
                else:
                    value = wrap_by_value(value)
            # Generate array write instruction
                self.code.append(
                    IRAssign(
                        target=wrap_by_reference(offset),
                        value=value,
                        comment=f"Write to array {cmd.target.name}[{index}]"
                    )
            )
        else:

            target = self.create_variable(cmd.target.name, proc_name=self.current_proc)
            
            if target.is_pointer:
                target = wrap_by_reference(target)
            else:
                target = wrap_by_value(target)
                
            if isinstance(cmd.value, BinaryOp):
                if cmd.value.operator in self.costly_ops:
                    self._generate_optimized_op(target, cmd.value)
                else:
                    left = self._generate_value(cmd.value.left)
                    if left.is_pointer:
                        left = wrap_by_reference(left)
                    else:
                        left = wrap_by_value(left)                 
                    
                    right = self._generate_value(cmd.value.right)
                    if right.is_pointer:
                        right = wrap_by_reference(right)
                    else:
                        right = wrap_by_value(right)
                        
                    self.code.append(
                        IRBinaryOp(
                            target=target,
                            left=left,
                            right=right,
                            operator=cmd.value.operator,
                            comment=f"Assignment with {cmd.value.operator}"
                        )
                    )
            else:
                value = self._generate_value(cmd.value)
                print(f"VALUE: {value} for {cmd.value}")
                if value.is_pointer:
                    value = wrap_by_reference(value)
                else:
                    value = wrap_by_value(value)
                                     
                self.code.append(
                    IRAssign(
                        target=target,
                        value=value,
                        comment="Simple assignment"
                    )
                )


    def _generate_optimized_op(self, target: Variable, op: BinaryOp) -> None:
        
        # TO DO
        
        
        left = self._generate_value(op.left)
        if left.is_pointer:
            left = wrap_by_reference(left)
        else:
            left = wrap_by_value(left)
        right = self._generate_value(op.right)
        if right.is_pointer:
            right = wrap_by_reference(right)
        else:
            right = wrap_by_value(right)
            
        if target.is_pointer:
            target = wrap_by_reference(target)
        else:
            target = wrap_by_value(target)
            

        if op.operator == "*":
            if isinstance(op.right, Number) or isinstance(op.left, Number):
                pass # for now
            
            self.code.append(
                IRBinaryOp(
                    target=target,
                    left=left,
                    right=right,
                    operator=op.operator,
                    comment=f"Optimized {op.operator} operation",
            ))
                
            

        elif op.operator in {"/", "%"}:
            if isinstance(op.right, Number) and op.right.value == 0:
                self.code.append(
                    IRAssign(
                        target=target, value=self.create_variable("0", is_const=True), comment=f"Division/modulo by 0 -> 0"
                    )
                )
                return
            if (
                op.operator == "/"
                and isinstance(op.right, Number)
                and op.right.value == 1
            ):
                self.code.append(
                    IRAssign(target=target, value=left, comment="Division by 1")
                )
                return

            self.code.append(
                IRBinaryOp(
                    target=target,
                    left=left,
                    right=right,
                    operator=op.operator,
                    comment=f"Optimized {op.operator} operation",
                )
            )
        
        else:
            raise ValueError(f"Unsupported operator: {op.operator}")
    

    def _generate_if(self, cmd: IfStatement) -> None:
        else_label = self.label_manager.new_label(
            LabelType.IF_ELSE,
            f"else branch in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )
        end_label = self.label_manager.new_label(
            LabelType.IF_END,
            f"end of if in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )

        # Generate condition jump to else
        left = self._generate_value(cmd.condition.left)
        if left.is_pointer:
            left = wrap_by_reference(left)
        else:
            left = wrap_by_value(left)  
        
        right = self._generate_value(cmd.condition.right)
        if right.is_pointer:
            right = wrap_by_reference(right)
        else:
            right = wrap_by_value(right)

        # invert condition for ">=" and "<=" and "=="

        if cmd.condition.operator in [">=", "<=", "!="]:
            if cmd.condition.operator == ">=":
                cmd.condition.operator = "<"
            elif cmd.condition.operator == "<=":
                cmd.condition.operator = ">"
            elif cmd.condition.operator == "!=":
                cmd.condition.operator = "="

            self.code.append(
                IRCondJump(
                    left=left,
                    operator=cmd.condition.operator,
                    right=right,
                    label=else_label,
                    comment="Jump to else if condition is true",
                )
            )
            # Generate then block
            for then_cmd in cmd.then_block:
                self._generate_command(then_cmd)
            self.code.append(IRJump(label=end_label, comment="Skip else block"))

            # Generate else block
            self.code.append(
                IRLabel(
                    label_id=else_label,
                    comment=self.label_manager.get_comment(else_label),
                    label_type=LabelType.IF_ELSE,
                )
            )
            if cmd.else_block:
                for else_cmd in cmd.else_block:
                    self._generate_command(else_cmd)

            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
                    label_type=LabelType.IF_END,
                )
            )

        else:

            self.code.append(
                IRCondJump(
                    left=left,
                    operator=cmd.condition.operator,
                    right=right,
                    label=else_label,
                    comment="Jump to else if condition is true",
                )
            )
        
            if cmd.else_block:
                for else_cmd in cmd.else_block:
                    self._generate_command(else_cmd)
            self.code.append(IRJump(label=end_label, comment="Skip else block"))

            self.code.append(
                IRLabel(
                    label_id=else_label,
                    comment=self.label_manager.get_comment(else_label),
                    label_type=LabelType.IF_ELSE,
                )
            )

            # Generate then block
            for then_cmd in cmd.then_block:
                self._generate_command(then_cmd)

            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
                    label_type=LabelType.IF_END,
                )
            )

    def _generate_while(self, cmd: WhileLoop) -> None:
        start_label = self.label_manager.new_label(
            LabelType.WHILE_START,
            f"while loop start in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )
        end_label = self.label_manager.new_label(
            LabelType.WHILE_END,
            f"while loop end in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )

        helper_label = self.label_manager.new_label(
            LabelType.WHILE_HELPER, f"while loop helper for condition evaluation"
        )

        self.code.append(
            IRLabel(
                label_id=start_label,
                comment=self.label_manager.get_comment(start_label),
                label_type=LabelType.WHILE_START,
            )
        )

        # Generate condition
        left = self._generate_value(cmd.condition.left)
        if left.is_pointer:
            left = wrap_by_reference(left)
        else:
            left = wrap_by_value(left)
            
        right = self._generate_value(cmd.condition.right)
        if right.is_pointer:
            right = wrap_by_reference(right)
        else:
            right = wrap_by_value(right)

        if cmd.condition.operator in [">=", "<=", "!="]:
            if cmd.condition.operator == ">=":
                cmd.condition.operator = "<"
            elif cmd.condition.operator == "<=":
                cmd.condition.operator = ">"
            elif cmd.condition.operator == "!=":
                cmd.condition.operator = "="

            self.code.append(
                IRCondJump(
                    left=left,
                    operator=cmd.condition.operator,
                    right=right,
                    label=end_label,
                    comment="Exit loop if condition is false",
                )
            )

            # Generate loop body
            for loop_cmd in cmd.body:
                self._generate_command(loop_cmd)

            self.code.append(
                IRJump(label=start_label, comment="Jump back to start of while loop")
            )
            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
                    label_type=LabelType.WHILE_END,
                )
            )

        else:

            self.code.append(
                IRCondJump(
                    left=left,
                    operator=cmd.condition.operator,
                    right=right,
                    label=helper_label,
                    comment="Exit loop if condition is false",
                )
            )

            self.code.append(
                IRJump(label=end_label, comment="Jump to end of while loop")
            )

            self.code.append(
                IRLabel(
                    label_id=helper_label,
                    comment=self.label_manager.get_comment(helper_label),
                    label_type=LabelType.WHILE_HELPER,
                )
            )

            for loop_cmd in cmd.body:
                self._generate_command(loop_cmd)

            self.code.append(
                IRJump(label=start_label, comment="Jump back to start of while loop")
            )

            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
                    label_type=LabelType.WHILE_END,
                )
            )

    def _generate_repeat(self, cmd: RepeatLoop) -> None:
        start_label = self.label_manager.new_label(
            LabelType.REPEAT_START,
            f"repeat loop start in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )

        self.code.append(
            IRLabel(
                label_id=start_label,
                comment=self.label_manager.get_comment(start_label),
                label_type=LabelType.REPEAT_START,
            )
        )
        
        end_label = self.label_manager.new_label(
            LabelType.REPEAT_END, comment="End of repeat loop"
        )


        # Generate loop body
        for loop_cmd in cmd.body:
            self._generate_command(loop_cmd)

        # Generate condition and jump back if condition is false
        left = self._generate_value(cmd.condition.left)
        if left.is_pointer:
            left = wrap_by_reference(left)
        else:
            left = wrap_by_value(left)
            
        right = self._generate_value(cmd.condition.right)
        if right.is_pointer:
            right = wrap_by_reference(right)
        else:
            right = wrap_by_value(right)
            
            
        if cmd.condition.operator in [">=", "<=", "!="]:
            if cmd.condition.operator == ">=":
                cmd.condition.operator = "<"
            elif cmd.condition.operator == "<=":
                cmd.condition.operator = ">"
            elif cmd.condition.operator == "!=":
                cmd.condition.operator = "="

            self.code.append(
                IRCondJump(
                    left=left,
                    operator=cmd.condition.operator,
                    right=right,
                    label=start_label,
                    comment="Jump back to repeat start if condition is true",
                )
            )
            # Else we exit the loop
        else:
            # WE NEED TO INVERT THE CONDITION      
            if_else_helepr = self.label_manager.new_label(
                LabelType.IF_HELPER, comment="if helper for repeat loop"
            )   
                
            
            self.code.append(
                IRCondJump(
                    left=left,
                    operator=cmd.condition.operator,
                    right=right,
                    label=end_label,
                    comment="Jump back to repeat start if condition is true",
                )
            )
            self.code.append(
                IRJump(label=start_label, comment="Jump to end of repeat loop")
            )
            
            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
                    label_type=LabelType.REPEAT_END,
            ))
                    

    def _generate_for(self, cmd: ForLoop) -> None:
        start_label = self.label_manager.new_label(
            LabelType.FOR_START,
            f"for loop start in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )
        end_label = self.label_manager.new_label(
            LabelType.FOR_END,
            f"for loop end in {'proc ' + self.current_proc if self.current_proc else 'main'}",
        )

        # Initialize loop variable
        iterator = BY_VALUE(self.create_variable(cmd.iterator))
        start_val = self._generate_value(cmd.start)
        # iterator_low = self.create_variable("iterator_low", is_temp=True)
        if start_val.is_pointer:
            start_val = wrap_by_reference(start_val)
        else:
            start_val = wrap_by_value(start_val)
            
        end_val = self._generate_value(cmd.end)
        if end_val.is_pointer:
            end_val = wrap_by_reference(end_val)
        else:
            end_val = wrap_by_value(end_val)
            
        iterator_end = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
        self.code.append(
            IRAssign(
                target=BY_VALUE(iterator_end),
                value=end_val,
                comment=f"Initialize for loop iterator end {iterator_end}",
            )
        )

        self.code.append(
            IRAssign(
                target=iterator,
                value=start_val,
                comment=f"Initialize for loop iterator {iterator}",
            )
        )

        self.code.append(
            IRLabel(
                label_id=start_label,
                comment=self.label_manager.get_comment(start_label),
                label_type=LabelType.FOR_START,
            )
        )

        # Generate loop condition
        if cmd.downto:
            self.code.append(
                IRCondJump(
                    left=iterator,
                    operator="<",
                    right=iterator_end,
                    label=end_label,
                    comment="Exit loop if iterator < end value (downto)",
                )
            )
        else:
            self.code.append(
                IRCondJump(
                    left=iterator,
                    operator=">",
                    right= iterator_end,
                    label=end_label,
                    comment="Exit loop if iterator > end value",
                )
            )

        # Generate loop body
        for loop_cmd in cmd.body:
            self._generate_command(loop_cmd)

        # Increment/decrement iterator
        if cmd.downto:
            self.code.append(
                IRBinaryOp(
                    target=iterator,
                    left=iterator,
                    right=self._generate_value(Number(self.dummy_loc, 1)),
                    operator="-",
                    comment="Decrement loop iterator",
                )
            )
        else:
            self.code.append(
                IRBinaryOp(
                    target=iterator,
                    left=iterator,
                    right=self._generate_value(Number(self.dummy_loc, 1)),
                    operator="+",
                    comment="Increment loop iterator",
                )
            )

        self.code.append(
            IRJump(label=start_label, comment="Jump back to for loop start")
        )

        self.code.append(
            IRLabel(
                label_id=end_label, 
                label_type=LabelType.FOR_END,
                comment=self.label_manager.get_comment(end_label)
            )
        )

    def _generate_proc_call(self, cmd: ProcedureCall) -> None:
        args = []
        proc_params = self.symbol_table.get_procedure_params(cmd.name)
        
        for param_call, declared_param in zip(cmd.arguments, proc_params):
            
            if declared_param[1]: # is_array
                cp = f"{self.current_proc}#" if self.current_proc else ""
                name = f"{cp}{param_call.name}"
                base = self.create_variable(name = name, is_pointer=True)
                args.append(base)
                
            else:
                cp = f"{self.current_proc}#" if self.current_proc else ""
                name = f"{cp}{param_call.name}"
                base = self.create_variable(name = name, is_pointer=True)
                
                args.append(base)          
            

        self.code.append(
            IRProcCall(name=cmd.name, args=args, comment=f"Call procedure {cmd.name}")
        )
                
        

    def _generate_value(self, value: Value) -> Variable:
        """Generate IR for value"""
        if isinstance(value, Number):
            return wrap_by_value(self.create_variable(value.value, is_const=True))
        elif isinstance(value, Identifier):
            if value.array_index is not None:
                index = self._generate_value(value.array_index)
                return self._handle_array_access(value.name, index)
            return self.create_variable(value.name, proc_name=self.current_proc)
        raise ValueError(f"Unsupported value type: {type(value)}")

    def _handle_array_access(self, array_name: str, index: Variable) -> Variable:
        """Generate code for array access"""
        temp = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True, is_pointer=True)
        # offset = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
        
        #### TO DO ####
        if index.is_pointer:
            right = wrap_by_reference(index)
        else:
            right = wrap_by_value(index)
        # # # Read from array
        # self.code.append(
        #     # IRArrayRead(
        #     #     target=temp,
        #     #     array=self.create_variable(array_name, proc_name=self.current_proc),
        #     #     index=index,
        #     #     comment=f"Read from array {array_name}[{index}]"
        #     # )

        self.code.append(
            IRBinaryOp(
                target=wrap_by_value(temp),
                left= wrap_by_value(self.create_variable(array_name, proc_name=self.current_proc)),
                right=right,
                operator="+",
                comment=f"Calculate array {array_name} offset"
            )
        )
        
        
        return BY_VALUE(temp)

    def _generate_read(self, cmd: ReadCommand) -> None:
        target = self.create_variable(cmd.target.name)
        
        if cmd.target.array_index is not None:
            # Replace current array handling with:
            name = cmd.target.name
            temp = wrap_by_value(self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True, is_pointer=True))
            # offset = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
            index = self._generate_value(cmd.target.array_index)
            if index.is_pointer:
                right = wrap_by_reference(index)
            else:
                right = wrap_by_value(index)
            # Calculate offset
            self.code.append(
                IRBinaryOp(
                    target=wrap_by_reference(temp),
                    left= wrap_by_value(self.create_variable(name, proc_name=self.current_proc)),
                    right=right,
                    operator="+",
                    comment=f"Calculate array {name} offset"
                )
            )
            
            self.code.append(
                IRRead(target=temp, comment=f"Read value for array {target}")
            )

        else:
            if target.is_pointer:
                target = wrap_by_reference(target)
            else:
                target = wrap_by_value(target)
            self.code.append(IRRead(target=target, comment=f"Read value into {target}"))
            
    def _generate_write(self, cmd: WriteCommand) -> None:
        value = self._generate_value(cmd.value)
        if value.is_pointer:
            value = wrap_by_reference(value)
        else:
            value = wrap_by_value(value)
        
        
        self.code.append(IRWrite(value=value, comment=f"Write value {value}"))

