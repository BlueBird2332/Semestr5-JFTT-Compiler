from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

from ..ast_nodes import *
from ..symbol_table import Symbol, SymbolTable
from .arithmetic import IRArithmetic
from .IR_ops import *


class IRGenerator:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.temp_counter = 0
        self.label_manager = LabelManager()
        self.arithmetic = IRArithmetic(self.label_manager, symbol_table)
        self.code: List[IRInstruction] = []
        self.current_proc: Optional[str] = None
        self.costly_ops = symbol_table.costly_operations
        self.numeric_variables = dict()
        self.dummy_loc = Location(0, 0)

    def new_temp(self) -> Variable:
        """Generate new temporary variable"""
        self.temp_counter += 1
        return Variable.create_temp(f"t{self.temp_counter}", self.current_proc)

    def create_variable(self, name: str) -> Variable:
        """Create a variable with proper scope"""
        
        return Variable.from_symbol(name, self.current_proc)

    def generate(self, node: Program) -> List[IRInstruction]:
        """Generate IR for entire program"""
        self.code = []

        # Generate arithmetic procedures
        
    
        if self.costly_ops:
            self.code.extend(self.arithmetic.generate_arithmetic_procedures(self.costly_ops))
            
        for proc in node.procedures:
            self._generate_procedure(proc)
            self.numeric_variables["0"] = 0
            self.numeric_variables["1"] = 1
            self.numeric_variables["neg_1"] = -1

        # Generate code for main program
        main_label = self.label_manager.new_label(
            LabelType.MAIN_START, "Main program start"
        )
        self.code.append(
            IRLabel(
                label_id=main_label, comment=self.label_manager.get_comment(main_label)
            )
        )

        # Process declarations
        for decl in node.declarations:
            if decl.array_bounds:
                start, end = decl.array_bounds
                # Replace current array handling with:
                self._handle_array_declaration(decl.name, start, end)

        # Generate main program code
        for cmd in node.commands:
            self._generate_command(cmd)

        return self.code
        
    def _generate_procedure(self, proc: Procedure) -> None:
        """Generate IR for procedure definition"""
        self.current_proc = proc.name
        proc_label = self.label_manager.new_label(
            LabelType.PROC_START, f"{proc.name} procedure"
        )
        self.code.append(
            IRLabel(
                label_id=proc_label, comment=self.label_manager.get_comment(proc_label).upper()
            )
        )

        # Process local declarations
        for decl in proc.declarations:
            if decl.array_bounds:
                start, end = decl.array_bounds
                # Replace current array handling with:
                self._handle_array_declaration(decl.name, start, end)

        # Generate procedure body
        for cmd in proc.commands:
            self._generate_command(cmd)

        zero_var = Variable.from_number("0")
        self.code.append(
            IRAssign(
                target=Variable("return"),
                value=zero_var,
                comment=f"End of procedure {proc.name}",
            )
        )
        self.current_proc = None

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
            array_var = self.create_variable(cmd.target.name)
            index = self._generate_value(cmd.target.array_index)
            
            # Calculate offset
            offset = self.new_temp()
            self.code.append(
                IRBinaryOp(
                    target=offset,
                    left=index,
                    right=self.create_variable(f"{cmd.target.name}_start"),
                    operator="-",
                    comment=f"Calculate array offset for assignment"
                )
            )
            
            # Generate the value to assign
            if isinstance(cmd.value, BinaryOp):
                if cmd.value.operator in self.costly_ops:
                    temp = self.new_temp()
                    self._generate_optimized_op(temp, cmd.value)
                    value = temp
                else:
                    left = self._generate_value(cmd.value.left)
                    right = self._generate_value(cmd.value.right)
                    temp = self.new_temp()
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
            # Handle regular assignment (existing code)
            target = self.create_variable(cmd.target.name)
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
                )
            )
            if cmd.else_block:
                for else_cmd in cmd.else_block:
                    self._generate_command(else_cmd)

            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
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
                )
            )

            # Generate then block
            for then_cmd in cmd.then_block:
                self._generate_command(then_cmd)

            self.code.append(
                IRLabel(
                    label_id=end_label,
                    comment=self.label_manager.get_comment(end_label),
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
                label_id=end_label, comment=self.label_manager.get_comment(end_label)
            )
        )

    def _generate_proc_call(self, cmd: ProcedureCall) -> None:
        args = []
        for arg in cmd.arguments:
            value = self._generate_value(arg)
            if isinstance(value, Variable):
                args.append(value)
            else:
                # If it's a constant, create a temporary variable
                temp = self.new_temp()
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

    def _generate_value(self, value: Value) -> Union[Variable, Number, str]:
        """Generate IR for value, returns either a Variable or a string constant"""
        if isinstance(value, Number):
            
            name = str(value.value)
            if value.value < 0:
                name = "neg" + str(abs(value.value))
                
            if name not in self.numeric_variables.keys():
                self.numeric_variables[name] = value.value
                
            return Variable.from_number(name)
        
        elif isinstance(value, Identifier):
            if value.array_index is not None:
                # Replace current array access code with:
                index = self._generate_value(value.array_index)
                return self._handle_array_access(value.name, index)
            return self.create_variable(value.name)
        
        raise ValueError(f"Unsupported value type: {type(value)}")

    def _handle_array_declaration(self, name: str, start: int, end: int) -> None:
        """Generate code for array declaration"""
        # Create array variables
        array_var = self.create_variable(name)
        start_var = Variable.from_number(start)
        size_var = Variable.from_number(end - start + 1)
        
        # Store array metadata
        self.code.append(
            IRAssign(
                target=self.create_variable(f"{name}_start"),
                value=start_var,
                comment=f"Store array {name} start index"
            )
        )
        
        self.code.append(
            IRAssign(
                target=self.create_variable(f"{name}_size"),
                value=size_var,
                comment=f"Store array {name} size"
            )
        )
        
        # Allocate array
        self.code.append(
            IRAssign(
                target=array_var,
                value=size_var,
                comment=f"Array allocation {name}[{start}:{end}]"
            )
        )

    def _handle_array_access(self, array_name: str, index: Variable) -> Variable:
        """Generate code for array access with bounds checking"""
        temp = self.new_temp()
        
        # Calculate actual offset: index - start_index
        offset = self.new_temp()
        self.code.append(
            IRBinaryOp(
                target=offset,
                left=index,
                right=self.create_variable(f"{array_name}_start"),
                operator="-",
                comment=f"Calculate array {array_name} offset"
            )
        )
        
        # Access array at offset using new IRArrayRead instruction
        self.code.append(
            IRArrayRead(
                target=temp,
                array=self.create_variable(array_name),
                index=offset,
                comment=f"Read from array {array_name}[{index}]"
            )
        )
        
        return temp
        
        
