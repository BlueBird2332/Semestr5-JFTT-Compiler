from typing import List, Optional
from dataclasses import dataclass
from .IR_ops import *

class IRArithmetic:
    """
    Implements arithmetic operations using IR code generation.
    Operations are implemented to run in logarithmic time.
    Properly handles negative numbers.
    """
    def __init__(self, label_manager: LabelManager, symbol_table: SymbolTable):
        self.label_manager = label_manager
        self.symbol_table = symbol_table
        self._init_arithmetic_vars()
        
    def _init_arithmetic_vars(self):
        """Initialize shared variables for arithmetic operations"""
        # Add shared variables to symbol table
        for var_name in ["arg1", "arg2", "result", "remainder", "sign1", "sign2", "temp"]:
            try:
                self.symbol_table.add_symbol(
                    name=var_name,
                    symbol_type="global",
                    is_array=False
                )
            except ValueError:
                pass  # Variable already exists
                
    def generate_arithmetic_procedures(self) -> List[IRInstruction]:
        """Generate all arithmetic procedures"""
        code = []
        
        # Generate helper procedures first
        # code.extend(self._generate_abs())
        
        # Generate main arithmetic procedures
        # code.extend(self._generate_multiply())
        code.extend(self._generate_divide())
        # code.extend(self._generate_modulo())
        
        return code
        
    def _generate_abs(self) -> List[IRInstruction]:
        """Generate absolute value procedure"""
        code = []
        
        start_label = self.label_manager.new_label(LabelType.PROC_START, "Absolute value procedure")
        if_1_else = self.label_manager.new_label(LabelType.IF_ELSE, "Negate arg1 if negative")
        if_1_end = self.label_manager.new_label(LabelType.IF_END, "End absolute value")

        if_2_else = self.label_manager.new_label(LabelType.IF_ELSE, "Negate arg2 if negative")
        if_2_end = self.label_manager.new_label(LabelType.IF_END, "End absolute value")
        
        end_label = self.label_manager.new_label(LabelType.PROC_END, "End absolute value")
        
        code.append(IRLabel(label_id=start_label, comment="ABSOLUTE VALUE PROCEDURE"))
        
        # If arg1 >= 0, return arg1
        code.append(IRCondJump(
            left="arg1",
            operator="<",
            right="0",
            label=if_1_else,
            comment="Skip negation if positive"
        ))
        code.append(IRAssign(
            target=Variable("sign1"),
            value="1",
        ))
        code.append(IRJump(label=if_1_end, comment="Skip negation"))
        
        code.append(IRLabel(label_id=if_1_else, comment="Negate arg1 if negative"))
        
        # Negate arg1 if negative
        code.append(IRBinaryOp(
            target=Variable("arg1"),
            left="0",
            right="arg1",
            operator="-",
            comment="Negate negative value"
        ))
        
        code.append(IRAssign(
            target=Variable("sign1"),
            value="-1",
            comment="Set sign of arg1 to negative"            
        ))
        
        code.append(IRLabel(label_id=if_1_end, comment="End absolute value for arg1"))
        
        # If arg2 >= 0, return arg2
        code.append(IRCondJump(
            left="arg2",
            operator="<",
            right="0",
            label=if_2_else,
            comment="Skip negation if positive"
        ))        
        code.append(IRAssign(
            target=Variable("sign2"),
            value="1",
        ))
        code.append(IRJump(label=if_2_end, comment="Skip negation"))
        
        code.append(IRLabel(label_id=if_2_else, comment="Negate arg2 if negative"))
        
        # Negate arg2 if negative
        code.append(IRBinaryOp(
            target=Variable("arg2"),
            left="0",
            right="arg2",
            operator="-",
            comment="Negate negative value"
        ))
        
        code.append(IRAssign(
            target=Variable("sign2"),
            value="-1",
            comment="Set sign of arg2 to negative"            
        ))
        
        
        code.append(IRBinaryOp(
            target=Variable("sign1"),
            left="sign1",
            right="sign2",
            operator="-",
            comment="Compute final sign, sign of expression is stored in sign1"
        ))
        
        
        code.append(IRBinaryOp(
            target=Variable("sign1"),
        ))
        
        code.append(IRLabel(label_id=if_2_end, comment="End absolute value for arg2"))
        
        
        code.append(IRLabel(label_id=end_label, comment="End absolute value"))
        code.append(IRAssign(target=Variable("return"), value="", comment="Return from abs"))
        
        return code
    
    
        
    def _generate_multiply(self) -> List[IRInstruction]:
        """Generate multiplication procedure using Russian Peasant Algorithm"""
        code = []
        
        # Create necessary labels
        start_label = self.label_manager.new_label(LabelType.PROC_START, "Multiply procedure start")
        while_label = self.label_manager.new_label(LabelType.WHILE_START, "Main multiplication loop")
        end_while_label = self.label_manager.new_label(LabelType.WHILE_END, "End of main multiplication loop")
        if_help_label = self.label_manager.new_label(LabelType.IF_HELPER, "")
        if_else_label = self.label_manager.new_label(LabelType.IF_ELSE, "")
        if_end_label = self.label_manager.new_label(LabelType.IF_END, "")
        end_label = self.label_manager.new_label(LabelType.PROC_END, "Multiply end")
        
        code.append(IRLabel(label_id=start_label, comment="MULTIPLY PROCEDURE"))
        code.append(IRProcCall(name="abs", args=[], comment="Compute absolute values and store expression sign in sign1"))
        
        # Optional : swap arg1 and arg2 if arg1 < arg2
        code.append(IRAssign(target=Variable("result"), value="0", comment="Initialize result"))
        
        code.append(IRLabel(label_id=while_label, comment="Main multiplication loop"))
        code.append(IRCondJump(
            left="arg2",
            operator=">",
            right="0",
            label=if_help_label,
            comment="Whlie multiplier is greater than 0"
        ))
        code.append(IRJump(label=end_while_label, comment="Exit multiplication loop"))
        code.append(IRLabel(label_id=if_help_label, comment="Helper if statement"))
        
        code.append(IRAssign(target=Variable("temp"), value="arg2", comment="Hold arg2 for halving"))
        code.append(IRHalf(target=Variable("temp"), comment="Halve arg2"))
        code.append(IRBinaryOp(target=Variable("temp"), left="temp", right="temp", operator="+", comment="Add temp to check modularity"))
        code.append(IRBinaryOp(target=Variable("temp"), left="temp", right="arg2", operator="-", comment="Subtract temp from arg2"))
        code.append(IRCondJump(
            left="temp",
            operator="=",
            right="0",
            label=if_end_label,
            comment="Check if arg2 is odd"
        ))
        # temp < 0
        code.append(IRBinaryOp(
            target=Variable("result"),
            left="result",
            right="arg1",
            operator="+",
            comment="Add multiplicand to result"
        ))
        
        code.append(IRLabel(label_id=if_end_label, comment="If end statement"))
        code.append(IRBinaryOp(
            target=Variable("arg1"),
            left="arg1",
            right="arg1",
            operator="+",
            comment="Double the multiplicand"
        ))
        
        code.append(IRHalf(
            target=Variable("arg2"),
            comment="Halve the multiplier"
        ))
        code.append(IRJump(label=while_label, comment="Continue multiplication loop"))
        code.append(IRLabel(label_id=end_while_label, comment="End of main multiplication loop"))
        
        # Apply sign to result
        
        if_sign = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")
        
        code.append(IRCondJump(
            left="sign1",
            operator="=",
            right="1",
            label=end_label,
            comment="Check if sign is negative"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("result"),
            left="0",
            right="result",
            operator="-",
            comment="Negate result"
        ))
        
        code.append(IRLabel(label_id=end_label, comment="End multiplication"))
        code.append(IRAssign(target=Variable("return"), value="", comment="Return from multiply"))
        
        
        
        return code
        
        
        
    def _generate_divide(self) -> List[IRInstruction]:
        """Generate division procedure handling signs"""
        code = []
        
        start_label = self.label_manager.new_label(LabelType.PROC_START, "Division procedure start")
        power_while_label = self.label_manager.new_label(LabelType.WHILE_START, "Divisor power loop")
        end_power_while_label = self.label_manager.new_label(LabelType.WHILE_END, "End of divisor power loop")
        
        divide_while_label = self.label_manager.new_label(LabelType.WHILE_START, "Division loop")
        divide_while_helper_label = self.label_manager.new_label(LabelType.WHILE_HELPER, "Helper for division loop")
        end_divide_while_label = self.label_manager.new_label(LabelType.WHILE_END, "End of division loop")
        
        if_end_divisor_loop_label = self.label_manager.new_label(LabelType.IF_END, "Inner divisor loop condition")
        
        end_label = self.label_manager.new_label(LabelType.PROC_END, "Division procedure end")
        
        code.append(IRLabel(label_id=start_label, comment="DIVISION PROCEDURE"))
        code.append(IRProcCall(name="abs", args=[], comment="Compute absolute values and store expression sign in sign1"))
        
        code.append(IRAssign(target=Variable("result"), value="0", comment="Initialize result")) # result = 0
        code.append(IRAssign(target=Variable("result2"), value="arg1", comment="Initialize remainder")) # remainder = dividend
        code.append(IRAssign(target=Variable("arg1"), value="1", comment="Initialize power of divisor")) #power = 1
        
        code.append(IRLabel(label_id=power_while_label, comment="Divisor power loop"))
        code.append(IRCondJump(
            left="arg2",
            operator=">",
            right="result2",
            label=end_power_while_label,
            comment="Check if divisor is greater than remainder"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("arg2"),
            left="arg2",
            right="arg2",
            operator="+",
            comment="Double the divisor"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("arg1"),
            left="arg1",
            right="arg1",
            operator="+",
            comment="Double the power"
        ))
        
        code.append(IRJump(label=power_while_label, comment="Continue divisor power loop"))
        code.append(IRLabel(label_id=end_power_while_label, comment="End of divisor power loop"))
        
        code.append(IRLabel(label_id=divide_while_label, comment="Division loop"))
        code.append(IRCondJump(
            left="arg1",
            operator=">",
            right="0",
            label=divide_while_helper_label,
            comment="Check if remainder is greater than 0"
        ))
        code.append(IRJump(label=end_divide_while_label, comment="Exit division loop"))
        code.append(IRLabel(label_id=divide_while_helper_label, comment="Helper for division loop"))
        
        code.append(IRCondJump(
            left="result2",
            operator="<",
            right="arg2",
            label=if_end_divisor_loop_label,
            comment="Check if remainder is greater than 0"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("result2"),
            left="result2",
            right="arg2",
            operator="-",
            comment="Subtract divisor from remainder"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("result"),
            left="result",
            right="arg1",
            operator="+",
            comment="Add power to result"
        ))
        
        code.append(IRLabel(label_id=if_end_divisor_loop_label, comment="End of divisor loop"))
        
        code.append(IRHalf(
            target=Variable("arg1"),
            comment="Halve the power"
        ))
        
        code.append(IRHalf(
            target=Variable("arg2"),
            comment="Halve the divisor"
        ))
        
        code.append(IRJump(label=divide_while_label, comment="Continue division loop"))
        code.append(IRLabel(label_id=end_divide_while_label, comment="End of division loop"))
        
        # Apply sign to result
        
        if_sign = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")
        if_remainder = self.label_manager.new_label(LabelType.IF_ELSE, "If remainder is negative")
        
        code.append(IRCondJump(
            left="sign1",
            operator="=",
            right="1",
            label=if_remainder,
            comment="Check if sign is negative"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("result"),
            left="0",
            right="result",
            operator="-",
            comment="Negate result"
        ))
        
        code.append(IRLabel(label_id=if_remainder, comment="Check if remainder is negative"))
        code.append(IRCondJump(
            left="sign2",
            operator="=",
            right="1",
            label=end_label,
            comment="Check if remainder is 0"
        ))
        
        code.append(IRBinaryOp(
            target=Variable("result2"),
            left="0",
            right="resul2",
            operator="-",
            comment="Negate remainder"
        ))
        
        code.append(IRLabel(label_id=end_label, comment="End division"))
        code.append(IRAssign(target=Variable("return"), value="", comment="Return from divide"))
        
        
        return code
        
    