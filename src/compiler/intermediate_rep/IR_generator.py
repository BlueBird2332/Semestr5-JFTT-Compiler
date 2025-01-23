from typing import List, Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from ..ast_nodes import *
from ..symbol_table import SymbolTable, Symbol
from .IR_ops import *
from .arithmetic import IRArithmetic

class IRGenerator:
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
        self.temp_counter = 0
        self.label_manager = LabelManager()
        self.arithmetic = IRArithmetic(self.label_manager, symbol_table)
        self.code: List[IRInstruction] = []
        self.current_proc: Optional[str] = None
        self.costly_ops = {'*', '/', '%'}
    
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
        # self.code.extend(self.arithmetic.generate_arithmetic_procedures())
        
        # Generate code for procedures
        for proc in node.procedures:
            self._generate_procedure(proc)
            
        # Generate code for main program
        main_label = self.label_manager.new_label(LabelType.MAIN_START, "Main program start")
        self.code.append(IRLabel(label_id=main_label, comment=self.label_manager.get_comment(main_label)))
        
        # Process declarations
        for decl in node.declarations:
            if decl.array_bounds:
                start, end = decl.array_bounds
                size = end - start + 1
                var = self.create_variable(decl.name)
                self.code.append(IRAssign(target=var, value=f"array({size})", 
                                      comment=f"Array declaration {decl.name}[{start}:{end}]"))
        
        # Generate main program code
        for cmd in node.commands:
            self._generate_command(cmd)
            
        
            
        return self.code

    def _generate_procedure(self, proc: Procedure) -> None:
        """Generate IR for procedure definition"""
        self.current_proc = proc.name
        proc_label = self.label_manager.new_label(
            LabelType.PROC_START, 
            f"Procedure {proc.name} start"
        )
        self.code.append(IRLabel(
            label_id=proc_label,
            comment=self.label_manager.get_comment(proc_label)
        ))
        
        # Process local declarations
        for decl in proc.declarations:
            if decl.array_bounds:
                start, end = decl.array_bounds
                size = end - start + 1
                var = self.create_variable(decl.name)
                self.code.append(IRAssign(
                    target=var,
                    value=f"array({size})",
                    comment=f"Local array declaration {decl.name}[{start}:{end}]"
                ))
        
        # Generate procedure body
        for cmd in proc.commands:
            self._generate_command(cmd)
        
        self.code.append(IRAssign(
            target=Variable("return"),
            value="",
            comment=f"End of procedure {proc.name}"
        ))
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
        target = self.create_variable(cmd.target.name)
        
        if isinstance(cmd.value, BinaryOp):
            if cmd.value.operator in self.costly_ops:
                self._generate_optimized_op(target, cmd.value)
            else:
                left = self._generate_value(cmd.value.left)
                right = self._generate_value(cmd.value.right)
                self.code.append(IRBinaryOp(
                    target=target,
                    left=str(left),
                    right=str(right),
                    operator=cmd.value.operator,
                    comment=f"Assignment with {cmd.value.operator}"
                ))
        else:
            value = self._generate_value(cmd.value)
            self.code.append(IRAssign(
                target=target,
                value=str(value),
                comment="Simple assignment"
            ))

    def _generate_optimized_op(self, target: Variable, op: BinaryOp) -> None:
        left = self._generate_value(op.left)
        right = self._generate_value(op.right)
        
        if op.operator == '*':
            if isinstance(op.right, Number):
                if op.right.value == 0:
                    self.code.append(IRAssign(target=target, value='0',
                                          comment="Multiplication by 0"))
                    return
                if op.right.value == 1:
                    self.code.append(IRAssign(target=target, value=str(left),
                                          comment="Multiplication by 1"))
                    return
                
        elif op.operator in {'/', '%'}:
            if isinstance(op.right, Number) and op.right.value == 0:
                self.code.append(IRAssign(target=target, value='0',
                                      comment=f"Division/modulo by 0 -> 0"))
                return
            if op.operator == '/' and isinstance(op.right, Number) and op.right.value == 1:
                self.code.append(IRAssign(target=target, value=str(left),
                                      comment="Division by 1"))
                return
        
        self.code.append(IRBinaryOp(
            target=target,
            left=str(left),
            right=str(right),
            operator=op.operator,
            comment=f"Optimized {op.operator} operation"
        ))

    def _generate_if(self, cmd: IfStatement) -> None:
        else_label = self.label_manager.new_label(
            LabelType.IF_ELSE,
            f"else branch in {'proc ' + self.current_proc if self.current_proc else 'main'}"
        )
        end_label = self.label_manager.new_label(
            LabelType.IF_END,
            f"end of if in {'proc ' + self.current_proc if self.current_proc else 'main'}"
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
            
            self.code.append(IRCondJump(
                left=str(left),
                operator=cmd.condition.operator,
                right=str(right),
                label=else_label,
                comment="Jump to else if condition is true"
            ))            
            # Generate then block
            for then_cmd in cmd.then_block:
                self._generate_command(then_cmd)
            self.code.append(IRJump(label=end_label, comment="Skip else block"))
            
            # Generate else block
            self.code.append(IRLabel(
                label_id=else_label,
                comment=self.label_manager.get_comment(else_label)
            ))
            if cmd.else_block:
                for else_cmd in cmd.else_block:
                    self._generate_command(else_cmd)
            
            self.code.append(IRLabel(
                label_id=end_label,
                comment=self.label_manager.get_comment(end_label)
            ))
            
            
        else:
            
            self.code.append(IRCondJump(
                left=str(left),
                operator=cmd.condition.operator,
                right=str(right),
                label=else_label,
                comment="Jump to else if condition is true"
            ))
            
            if cmd.else_block:
                for else_cmd in cmd.else_block:
                    self._generate_command(else_cmd)
            self.code.append(IRJump(label=end_label, comment="Skip else block"))  
   
            self.code.append(IRLabel(
                label_id=else_label,
                comment=self.label_manager.get_comment(else_label)
            ))          
            
            # Generate then block
            for then_cmd in cmd.then_block:
                self._generate_command(then_cmd)
        
            self.code.append(IRLabel(
                label_id=end_label,
                comment=self.label_manager.get_comment(end_label)
            ))

    def _generate_while(self, cmd: WhileLoop) -> None:
        start_label = self.label_manager.new_label(
            LabelType.WHILE_START,
            f"while loop start in {'proc ' + self.current_proc if self.current_proc else 'main'}"
        )
        end_label = self.label_manager.new_label(
            LabelType.WHILE_END,
            f"while loop end in {'proc ' + self.current_proc if self.current_proc else 'main'}"
        )
        
        helper_label = self.label_manager.new_label(
            LabelType.WHILE_HELPER,
            f"while loop helper for condition evaluation"
        )
        
        self.code.append(IRLabel(
            label_id=start_label,
            comment=self.label_manager.get_comment(start_label)
        ))
        
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
            
            self.code.append(IRCondJump(
                left=str(left),
                operator=cmd.condition.operator,
                right=str(right),
                label=end_label,
                comment="Exit loop if condition is false"
            ))
            
            # Generate loop body
            for loop_cmd in cmd.body:
                self._generate_command(loop_cmd)
                
            self.code.append(IRJump(
                label=start_label,
                comment="Jump back to start of while loop"
            ))
            self.code.append(IRLabel(
                label_id=end_label,
                comment=self.label_manager.get_comment(end_label)
            ))
            
        else:
            
            self.code.append(IRCondJump(
                left=str(left),
                operator=cmd.condition.operator,
                right=str(right),
                label=helper_label,
                comment="Exit loop if condition is false"
            ))
            
            self.code.append(IRJump(
                label=end_label,
                comment="Jump to end of while loop"
            ))
                             
            self.code.append(IRLabel(
                label_id=helper_label,
                comment=self.label_manager.get_comment(helper_label)
            ))        
            
            for loop_cmd in cmd.body:
                self._generate_command(loop_cmd)
                
            self.code.append(IRJump(
                label=start_label,
                comment="Jump back to start of while loop"
            ))
            
            self.code.append(IRLabel(
                label_id=end_label,
                comment=self.label_manager.get_comment(end_label)
            ))   


    def _generate_repeat(self, cmd: RepeatLoop) -> None:
        start_label = self.label_manager.new_label(
            LabelType.REPEAT_START,
            f"repeat loop start in {'proc ' + self.current_proc if self.current_proc else 'main'}"
        )
        
        self.code.append(IRLabel(
            label_id=start_label,
            comment=self.label_manager.get_comment(start_label)
        ))
        
        # Generate loop body
        for loop_cmd in cmd.body:
            self._generate_command(loop_cmd)
            
        # Generate condition and jump back if condition is false
        left = self._generate_value(cmd.condition.left)
        right = self._generate_value(cmd.condition.right)
        self.code.append(IRCondJump(
            left=str(left),
            operator=cmd.condition.operator,
            right=str(right),
            label=start_label,
            comment="Jump back to repeat start if condition is true"
        ))

    def _generate_for(self, cmd: ForLoop) -> None:
        start_label = self.label_manager.new_label(
            LabelType.FOR_START,
            f"for loop start in {'proc ' + self.current_proc if self.current_proc else 'main'}"
        )
        end_label = self.label_manager.new_label(
            LabelType.FOR_END,
            f"for loop end in {'proc ' + self.current_proc if self.current_proc else 'main'}"
        )
        
        # Initialize loop variable
        iterator = self.create_variable(cmd.iterator)
        start_val = self._generate_value(cmd.start)
        end_val = self._generate_value(cmd.end)
        
        self.code.append(IRAssign(
            target=iterator,
            value=str(start_val),
            comment=f"Initialize for loop iterator {iterator}"
        ))
        
        self.code.append(IRLabel(
            label_id=start_label,
            comment=self.label_manager.get_comment(start_label)
        ))
        
        # Generate loop condition
        if cmd.downto:
            self.code.append(IRCondJump(
                left=str(iterator),
                operator='<',
                right=str(end_val),
                label=end_label,
                comment="Exit loop if iterator < end value (downto)"
            ))
        else:
            self.code.append(IRCondJump(
                left=str(iterator),
                operator='>',
                right=str(end_val),
                label=end_label,
                comment="Exit loop if iterator > end value"
            ))
        
        # Generate loop body
        for loop_cmd in cmd.body:
            self._generate_command(loop_cmd)
            
        # Increment/decrement iterator
        if cmd.downto:
            self.code.append(IRBinaryOp(
                target=iterator,
                left=str(iterator),
                right='1',
                operator='-',
                comment="Decrement loop iterator"
            ))
        else:
            self.code.append(IRBinaryOp(
                target=iterator,
                left=str(iterator),
                right='1',
                operator='+',
                comment="Increment loop iterator"
            ))
            
        self.code.append(IRJump(
            label=start_label,
            comment="Jump back to for loop start"
        ))
        
        self.code.append(IRLabel(
            label_id=end_label,
            comment=self.label_manager.get_comment(end_label)
        ))

    def _generate_proc_call(self, cmd: ProcedureCall) -> None:
        args = []
        for arg in cmd.arguments:
            value = self._generate_value(arg)
            if isinstance(value, Variable):
                args.append(value)
            else:
                # If it's a constant, create a temporary variable
                temp = self.new_temp()
                self.code.append(IRAssign(
                    target=temp,
                    value=str(value),
                    comment=f"Prepare argument for procedure call"
                ))
                args.append(temp)
                
        self.code.append(IRProcCall(
            name=cmd.name,
            args=args,
            comment=f"Call procedure {cmd.name}"
        ))

    def _generate_read(self, cmd: ReadCommand) -> None:
        target = self.create_variable(cmd.target.name)
        if cmd.target.array_index is not None:
            # Handle array access
            index = self._generate_value(cmd.target.array_index)
            temp = self.new_temp()
            self.code.append(IRRead(
                target=temp,
                comment=f"Read value for array {target}[{index}]"
            ))
            self.code.append(IRBinaryOp(
                target=target,
                left=str(index),
                right=str(temp),
                operator='[]',
                comment=f"Store read value to array {target}"
            ))
        else:
            self.code.append(IRRead(
                target=target,
                comment=f"Read value into {target}"
            ))

    def _generate_write(self, cmd: WriteCommand) -> None:
        value = self._generate_value(cmd.value)
        self.code.append(IRWrite(
            value=str(value),
            comment=f"Write value {value}"
        ))

    def _generate_value(self, value: Value) -> Union[Variable, str]:
        """Generate IR for value, returns either a Variable or a string constant"""
        if isinstance(value, Number):
            return str(value.value)
        elif isinstance(value, Identifier):
            if value.array_index is not None:
                # Handle array access
                index = self._generate_value(value.array_index)
                temp = self.new_temp()
                array_var = self.create_variable(value.name)
                self.code.append(IRBinaryOp(
                    target=temp,
                    left=str(array_var),
                    right=str(index),
                    operator='[]',
                    comment=f"Array access {array_var}[{index}]"
                ))
                return temp
            return self.create_variable(value.name)
        return str(value)