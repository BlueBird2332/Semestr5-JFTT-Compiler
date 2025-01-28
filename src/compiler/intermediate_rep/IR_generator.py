from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

from ..ast_nodes import *
from ..symbol_table import Symbol, SymbolTable
from .arithmetic import IRArithmetic
from .IR_ops import *


@dataclass
class ProcInfo:
    begin_id: int
    arguments: List[str]
    return_var: Variable

class IRGenerator:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.temp_counter = 0
        self.label_manager = LabelManager()
        self.code: List[IRInstruction] = []
        self.current_proc: Optional[str] = None
        self.costly_ops = symbol_table.costly_operations
        self.numeric_variables = dict()
        self.dummy_loc = Location(0, 0)
        self.variables: dict[str, Variable] = dict()
        self.arithmetic = IRArithmetic(self.label_manager, self.variables)
        self.proc_info: Dict[str, ProcInfo] = dict()

    
    def create_variable(self, name: Union[str, int],
                        proc_name:str = None,
                        is_temp: bool = False,
                        is_const: bool = False,
                        is_array: bool = False,
                        is_param: bool = False,
                        is_array_param: bool = False,                       
                        array_start: Optional[int] = None,
                        array_size: Optional[int] = None,
                        array_base_ref: Optional['Variable'] = None,
                        array_start_ref: Optional['Variable'] = None ) -> Variable:
        """Create/get a variable with proper scope"""
        
        # var_name = f"{self.current_proc}_{name}" if self.current_proc and not name.startswith('t') else name
        var_name = str(name)
        if self.current_proc and not var_name.startswith(self.current_proc) and not is_const:
            var_name = f"{self.current_proc}_{name}"
            
        if var_name not in self.variables:
            
            if is_array:
                var = Variable.create_array(
                    name=var_name,
                    start=array_start,
                    size=array_size,
                    proc_name=proc_name
                )
                
            elif is_param and is_array_param:
                var = Variable.create_array_param(
                    name=var_name,
                    proc_name=proc_name,
                    base_ref=array_base_ref,
                    start_ref=array_start_ref
                )
                
            elif is_param:
                var = Variable.create_param(name=var_name, proc_name=proc_name)
                
            elif is_const:
                var = Variable.from_number(var_name)
                
            elif is_temp:
                self.temp_counter += 1
                temp_name = f"t{self.temp_counter}"
                var = Variable.create_temp(temp_name, self.current_proc)

                
            else:                
                var = Variable(name=var_name, proc_name=proc_name)
                
            self.variables[var_name] = var
            return var            
        
        return self.variables[var_name]

    def generate(self, node: Program) -> List[IRInstruction]:
        """Generate IR for entire program"""
        self.code = []

        
        main_label = self.label_manager.new_label(
            LabelType.MAIN_START, "Main program start"
        )
        
        self.proc_info['main'] = ProcInfo(
            begin_id=main_label,
            arguments=[],
            return_var=None
        )

        # Generate arithmetic procedures      
    
        if self.costly_ops:
            self.code.extend(self.arithmetic.generate_arithmetic_procedures(self.costly_ops))
            
  
            
        for proc in node.procedures:
            self._generate_procedure(proc)
        
        # zero_var = self.create_variable(0, is_const=True)
        # one_var = self.create_variable(1, is_const=True)
        # neg_one_var = self.create_variable(-1, is_const=True)
        

        # Generate code for main program
        main_label = self.label_manager.new_label(
            LabelType.MAIN_START, "Main program start"
        )
        
        self.process_declarations(node.declarations)
        
        self.code.append(
            IRLabel(
                label_id=main_label, 
                label_type=LabelType.MAIN_START, 
                comment=self.label_manager.get_comment(main_label),
                procedure="main"
            )
        )

        # # Generate main program code
        for cmd in node.commands:
            self._generate_command(cmd)
            
        # # self.symbol_table.print_table()
        # with open("IR_file_memory", "w+") as f:
        #     for k,v in self.variables.items():
        #         f.write(f"Key: {k}, Value: {v.print_full()}\n")
        
        
        # for item in self.code:
        #     print(item)
            
        # for k,v in self.variables.items():
        #     print(f"Key: {k}, Value: {v.print_full()}")
            
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

        # zero_var = self.create_variable(0, is_const=True)
        # self.code.append(
        #     IRAssign(
        #         target=Variable("return"),
        #         value=zero_var,
        #         comment=f"End of procedure {proc.name}",
        #     )
        # )
        self.code.append(
            IRReturn(procedure=self.current_proc, comment=f"End of procedure {proc.name}")
        )
        self.current_proc = None
        
    def process_declarations(self, declarations: List[Declaration], proc_name: Optional[str] = None) -> None:
        """Process declarations and register variables"""
        
        for decl in declarations:
            if self.current_proc:
                decl.name = self.current_proc + "#" + decl.name
            if decl.array_bounds:
                # Create array variable
                start, end = decl.array_bounds
                array_var = self.create_variable(
                    name=decl.name,
                    proc_name=proc_name,
                    is_array=True,
                    array_start=start,
                    array_size=end - start + 1
                )
                
                # Create array start index constant
                start_var = self.create_variable(
                    name=start,
                    is_const=True
                )
                # Create array start reference variable
                start_ref = self.create_variable(
                    name=f"{decl.name}_start",
                    proc_name=proc_name
                )
                
                # Generate code for array initialization
                self.code.append(
                    IRAssign(
                        target=start_ref,
                        value=start_var,
                        comment=f"Store array {decl.name} start index"
                    )
                )
            else:
                # Create regular variable
                var = self.create_variable(
                    name=decl.name,
                    proc_name=proc_name
                )

            

    def process_parameters(self, proc_name: str, parameters: List[Tuple[str, bool]], start_id = None) -> None:
        """Process procedure parameters and register parameter variables"""
        vars = []
        
        for param_name, is_array in parameters:
            if self.current_proc:
                param_name = self.current_proc + "_" + param_name
            if is_array:
                # Create parameter array placeholder
                param_var = self.create_variable(
                    name=param_name,
                    proc_name=proc_name,
                    is_param=True,
                    is_array_param=True
                )
                vars.append(param_var)
                # Create start index reference for array parameter
                start_ref = self.create_variable(
                    name=f"{param_name}#start",
                    proc_name=proc_name,
                    is_param=True
                )
                vars.append(start_ref)
            else:
                # Create regular parameter variable
                var =  self.create_variable(
                    name=param_name,
                    proc_name=proc_name,
                    is_param=True
                )
                vars.append(var)
                
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
            
            # Calculate offset
            offset = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
            self.code.append(
                IRBinaryOp(
                    target=offset,
                    left=index,
                    right=self.create_variable(f"{cmd.target.name}_start", proc_name=self.current_proc),
                    operator="-",
                    comment=f"Calculate array offset for assignment"
                )
            )
            
            # Generate the value to assign
            if isinstance(cmd.value, BinaryOp):
                if cmd.value.operator in self.costly_ops:
                    temp = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
                    self._generate_optimized_op(temp, cmd.value)
                    value = temp
                else:
                    left = self._generate_value(cmd.value.left)
                    right = self._generate_value(cmd.value.right)
                    temp = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
                    self.code.append(
                        IRBinaryOp(
                            target=temp,
                            left=left,
                            right=right,
                            operator=cmd.value.operator,
                            comment=f"Compute value for array assignment"
                        )
                    )
                    value = temp
            else:
                value = self._generate_value(cmd.value)
            
            # Generate array write instruction
            self.code.append(
                IRArrayWrite(
                    array=array_var,
                    index=offset,
                    value=value,
                    comment=f"Write to array {cmd.target.name}[{index}]"
                )
            )
        else:
            target = self.create_variable(cmd.target.name, proc_name=self.current_proc)
                
            if isinstance(cmd.value, BinaryOp):
                if cmd.value.operator in self.costly_ops:
                    self._generate_optimized_op(target, cmd.value)
                else:
                    left = self._generate_value(cmd.value.left)
                    right = self._generate_value(cmd.value.right)
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
                self.code.append(
                    IRAssign(
                        target=target,
                        value=value,
                        comment="Simple assignment"
                    )
                )


    def _generate_optimized_op(self, target: Variable, op: BinaryOp) -> None:
        left = self._generate_value(op.left)
        right = self._generate_value(op.right)

        if op.operator == "*":
            if isinstance(op.right, Number):
                if op.right.value == 0:
                    self.code.append(
                        IRAssign(
                            target=target, value="0", comment="Multiplication by 0"
                        )
                    )
                    return
                if op.right.value == 1:
                    self.code.append(
                        IRAssign(
                            target=target,
                            value=left,
                            comment="Multiplication by 1",
                        )
                    )
                    return

        elif op.operator in {"/", "%"}:
            if isinstance(op.right, Number) and op.right.value == 0:
                self.code.append(
                    IRAssign(
                        target=target, value="0", comment=f"Division/modulo by 0 -> 0"
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
        right = self._generate_value(cmd.condition.right)

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
        right = self._generate_value(cmd.condition.right)

        if cmd.condition.operator in [">=", "<=", "="]:
            if cmd.condition.operator == ">=":
                cmd.condition.operator = "<"
            elif cmd.condition.operator == "<=":
                cmd.condition.operator = ">"
            elif cmd.condition.operator == "=":
                cmd.condition.operator = "!="

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

        # Generate loop body
        for loop_cmd in cmd.body:
            self._generate_command(loop_cmd)

        # Generate condition and jump back if condition is false
        left = self._generate_value(cmd.condition.left)
        right = self._generate_value(cmd.condition.right)
        self.code.append(
            IRCondJump(
                left=left,
                operator=cmd.condition.operator,
                right=right,
                label=start_label,
                comment="Jump back to repeat start if condition is true",
            )
        )

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
        iterator = self.create_variable(cmd.iterator)
        start_val = self._generate_value(cmd.start)
        end_val = self._generate_value(cmd.end)

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
                    right=end_val,
                    label=end_label,
                    comment="Exit loop if iterator < end value (downto)",
                )
            )
        else:
            self.code.append(
                IRCondJump(
                    left=iterator,
                    operator=">",
                    right= end_val,
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
        
        for i, (arg, (param_name, is_array)) in enumerate(zip(cmd.arguments, proc_params or [])):
            value = self._generate_value(arg)
            if isinstance(value, Variable):
                if is_array:
                    # For array parameters, pass base and start index
                    param_var = self.create_variable(
                        name=param_name,
                        proc_name=cmd.name,
                        is_param=True,
                        is_array_param=True,
                        array_base_ref=value,
                        array_start_ref=self.create_variable(f"{value.name}_start", proc_name=self.current_proc)
                    )
                    args.append(param_var)
                else:
                    args.append(value)
            else:
                # If it's a constant, create a temporary variable
                temp = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
                self.code.append(
                    IRAssign(
                        target=temp,
                        value=value,
                        comment=f"Prepare argument for procedure call",
                    )
                )
                args.append(temp)

        self.code.append(
            IRProcCall(name=cmd.name, args=args, comment=f"Call procedure {cmd.name}")
        )

    def _generate_value(self, value: Value) -> Variable:
        """Generate IR for value"""
        if isinstance(value, Number):
            return self.create_variable(value.value, is_const=True)
        elif isinstance(value, Identifier):
            if value.array_index is not None:
                index = self._generate_value(value.array_index)
                return self._handle_array_access(value.name, index)
            return self.create_variable(value.name, proc_name=self.current_proc)
        raise ValueError(f"Unsupported value type: {type(value)}")

    def _handle_array_access(self, array_name: str, index: Variable) -> Variable:
        """Generate code for array access"""
        temp = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
        offset = self.create_variable(name=f"t{self.temp_counter + 1}", is_temp=True)
        
        # Calculate offset
        self.code.append(
            IRBinaryOp(
                target=offset,
                left=index,
                right=self.create_variable(f"{array_name}_start", proc_name=self.current_proc),
                operator="-",
                comment=f"Calculate array {array_name} offset"
            )
        )
        
        # Read from array
        self.code.append(
            IRArrayRead(
                target=temp,
                array=self.create_variable(array_name, proc_name=self.current_proc),
                index=offset,
                comment=f"Read from array {array_name}[{index}]"
            )
        )
        
        return temp

    def _generate_read(self, cmd: ReadCommand) -> None:
        target = self.create_variable(cmd.target.name)
        if cmd.target.array_index is not None:
            # Replace current array handling with:
            index = self._generate_value(cmd.target.array_index)
            temp = self.new_temp()
            self.code.append(
                IRRead(target=temp, comment=f"Read value for array {target}")
            )
            # Generate array access using temp as value
            offset = self._handle_array_access(cmd.target.name, index)
            self.code.append(
                IRBinaryOp(
                    target=self.create_variable(cmd.target.name),
                    left=offset,
                    right=temp,
                    operator="[]=",
                    comment=f"Store read value to array"
                )
            )
        else:
            self.code.append(IRRead(target=target, comment=f"Read value into {target}"))
            
    def _generate_write(self, cmd: WriteCommand) -> None:
        value = self._generate_value(cmd.value)
        self.code.append(IRWrite(value=value, comment=f"Write value {value}"))

