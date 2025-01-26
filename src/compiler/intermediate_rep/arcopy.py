from dataclasses import dataclass
from typing import List, Optional

from .IR_ops import *

@dataclass
class ArithmeticVars:
    """Container for arithmetic variables"""
    arg1: Variable = Variable("arg1")
    arg2: Variable = Variable("arg2")
    result: Variable = Variable("result")
    result2: Variable = Variable("result2")  # Used for remainder in division
    sign1: Variable = Variable("sign1")
    sign2: Variable = Variable("sign2")
    temp: Variable = Variable("temp")
    zero: Variable = Variable("0")
    one: Variable = Variable("1")
    minus_one: Variable = Variable("-1")

class IRArithmetic:
    """
    Implements arithmetic operations using IR code generation.
    Operations are implemented to run in logarithmic time.
    Properly handles negative numbers.
    """

    def __init__(self, label_manager: LabelManager, symbol_table: SymbolTable):
        self.label_manager = label_manager
        self.symbol_table = symbol_table
        self.vars = ArithmeticVars()
        self._init_arithmetic_vars()

    def _init_arithmetic_vars(self):
        """Initialize shared variables for arithmetic operations"""
        # Add shared variables to symbol table
        for var_name in [
            self.vars.arg1.name,
            self.vars.arg2.name,
            self.vars.result.name,
            self.vars.result2.name,
            self.vars.sign1.name,
            self.vars.sign2.name,
            self.vars.temp.name,
        ]:
            try:
                self.symbol_table.add_symbol(
                    name=var_name, symbol_type="global", is_array=False
                )
            except ValueError:
                pass  # Variable already exists

    def generate_arithmetic_procedures(self) -> List[IRInstruction]:
        """Generate all arithmetic procedures"""
        code = []
        code.extend(self._generate_abs())
        code.extend(self._generate_multiply())
        code.extend(self._generate_divide())
        return code

    def _generate_abs(self) -> List[IRInstruction]:
        """Generate absolute value procedure"""
        code = []
        vars = self.vars
        
        start_label = self.label_manager.new_label(
            LabelType.PROC_START, "Absolute value procedure"
        )
        if_1_else = self.label_manager.new_label(
            LabelType.IF_ELSE, "Negate arg1 if negative"
        )
        if_1_end = self.label_manager.new_label(LabelType.IF_END, "End absolute value")

        if_2_else = self.label_manager.new_label(
            LabelType.IF_ELSE, "Negate arg2 if negative"
        )
        if_2_end = self.label_manager.new_label(LabelType.IF_END, "End absolute value")

        end_label = self.label_manager.new_label(
            LabelType.PROC_END, "End absolute value"
        )

        code.append(IRLabel(label_id=start_label, comment="ABSOLUTE VALUE PROCEDURE"))

        # If arg1 >= 0, return arg1
        code.append(
            IRCondJump(
                left=vars.arg1,
                operator="<",
                right=vars.zero,    
                label=if_1_else,
                comment="Skip negation if positive",
            )
        )
        code.append(
            IRAssign(
                target=vars.sign1,
                value=vars.one,
                comment=""
            )
        )
        code.append(IRJump(label=if_1_end, comment="Skip negation"))

        code.append(IRLabel(label_id=if_1_else, comment="Negate arg1 if negative"))

        # Negate arg1 if negative
        code.append(
            IRBinaryOp(
                target=vars.arg1,
                left=vars.zero,
                right=vars.arg1,
                operator="-",
                comment="Negate negative value",
            )
        )

        code.append(
            IRAssign(
                target=vars.sign1,
                value=vars.minus_one,
                comment="Set sign of arg1 to negative",
            )
        )

        code.append(IRLabel(label_id=if_1_end, comment="End absolute value for arg1"))

        # If arg2 >= 0, return arg2
        code.append(
            IRCondJump(
                left=vars.arg2,
                operator="<",
                right=vars.zero,
                label=if_2_else,
                comment="Skip negation if positive",
            )
        )
        code.append(
            IRAssign(
                target=vars.sign2,
                value=vars.one,
                comment=""
            )
        )
        code.append(IRJump(label=if_2_end, comment="Skip negation"))

        code.append(IRLabel(label_id=if_2_else, comment="Negate arg2 if negative"))

        # Negate arg2 if negative
        code.append(
            IRBinaryOp(
                target=vars.arg2,
                left=vars.zero,
                right=vars.arg2,
                operator="-",
                comment="Negate negative value",
            )
        )

        code.append(
            IRAssign(
                target=vars.sign2,
                value=vars.minus_one,
                comment="Set sign of arg2 to negative",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.sign1,
                left=vars.sign1,
                right=vars.sign2,
                operator="-",
                comment="Compute final sign, sign of expression is stored in sign1",
            )
        )

        # code.append(
        #     IRBinaryOp(
        #         target=vars.sign1,
        #     )
        # )

        code.append(IRLabel(label_id=if_2_end, comment="End absolute value for arg2"))

        code.append(IRLabel(label_id=end_label, comment="End absolute value"))
        code.append(
            IRAssign(target=Variable("return"), value=vars.zero, comment="Return from abs")
        )

        return code

    def _generate_multiply(self) -> List[IRInstruction]:
        """Generate multiplication procedure using Russian Peasant Algorithm"""
        code = []
        vars = self.vars


        start_label = self.label_manager.new_label(
            LabelType.PROC_START, "Multiply procedure start"
        )
        while_label = self.label_manager.new_label(
            LabelType.WHILE_START, "Main multiplication loop"
        )
        end_while_label = self.label_manager.new_label(
            LabelType.WHILE_END, "End of main multiplication loop"
        )
        if_help_label = self.label_manager.new_label(LabelType.IF_HELPER, "")
        if_else_label = self.label_manager.new_label(LabelType.IF_ELSE, "")
        if_end_label = self.label_manager.new_label(LabelType.IF_END, "")
        end_label = self.label_manager.new_label(LabelType.PROC_END, "Multiply end")

        code.append(IRLabel(label_id=start_label, comment="MULTIPLY PROCEDURE"))
        code.append(
            IRProcCall(
                name="abs",
                args=[],
                comment="Compute absolute values and store expression sign in sign1",
            )
        )

        # Optional : swap arg1 and arg2 if arg1 < arg2
        code.append(
            IRAssign(target=Variable("result"), value=vars.zero, comment="Initialize result")
        )

        code.append(IRLabel(label_id=while_label, comment="Main multiplication loop"))
        code.append(
            IRCondJump(
                left=vars.arg2,
                operator=">",
                right=vars.zero,
                label=if_help_label,
                comment="Whlie multiplier is greater than 0",
            )
        )
        code.append(IRJump(label=end_while_label, comment="Exit multiplication loop"))
        code.append(IRLabel(label_id=if_help_label, comment="Helper if statement"))

        code.append(
            IRAssign(
                target=Variable("temp"), value=vars.arg2, comment="Hold arg2 for halving"
            )
        )
        code.append(IRHalf(target=Variable("temp"), comment="Halve arg2"))
        code.append(
            IRBinaryOp(
                target=vars.temp,
                left=vars.temp,
                right=vars.temp,
                operator="+",
                comment="Add temp to check modularity",
            )
        )
        code.append(
            IRBinaryOp(
                target=vars.temp,
                left=vars.temp,
                right=vars.temp,
                operator="-",
                comment="Subtract temp from arg2",
            )
        )
        code.append(
            IRCondJump(
                left=vars.temp,
                operator="=",
                right=vars.zero,
                label=if_end_label,
                comment="Check if arg2 is odd",
            )
        )
        # temp < 0
        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.result,
                right=vars.arg1,
                operator="+",
                comment="Add multiplicand to result",
            )
        )

        code.append(IRLabel(label_id=if_end_label, comment="If end statement"))
        code.append(
            IRBinaryOp(
                target=vars.arg1,
                left=vars.arg1,
                right=vars.arg1,
                operator="+",
                comment="Double the multiplicand",
            )
        )

        code.append(IRHalf(target=vars.arg2, comment="Halve the multiplier"))
        code.append(IRJump(label=while_label, comment="Continue multiplication loop"))
        code.append(
            IRLabel(label_id=end_while_label, comment="End of main multiplication loop")
        )

        # Apply sign to result

        if_sign = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")

        code.append(
            IRCondJump(
                left=vars.sign1,
                operator="=",
                right=vars.one,
                label=end_label,
                comment="Check if sign is negative",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.zero,
                right=vars.result,  
                operator="-",
                comment="Negate result",
            )
        )

        code.append(IRLabel(label_id=end_label, comment="End multiplication"))
        code.append(
            IRAssign(
                target=Variable("return"), value=vars.zerp, comment="Return from multiply"
            )
        )

        return code

    def _generate_divide(self) -> List[IRInstruction]:
        """Generate division procedure handling signs"""
        code = []
        vars = self.vars

        start_label = self.label_manager.new_label(
            LabelType.PROC_START, "Division procedure start"
        )
        power_while_label = self.label_manager.new_label(
            LabelType.WHILE_START, "Divisor power loop"
        )
        end_power_while_label = self.label_manager.new_label(
            LabelType.WHILE_END, "End of divisor power loop"
        )

        divide_while_label = self.label_manager.new_label(
            LabelType.WHILE_START, "Division loop"
        )
        divide_while_helper_label = self.label_manager.new_label(
            LabelType.WHILE_HELPER, "Helper for division loop"
        )
        end_divide_while_label = self.label_manager.new_label(
            LabelType.WHILE_END, "End of division loop"
        )

        if_end_divisor_loop_label = self.label_manager.new_label(
            LabelType.IF_END, "Inner divisor loop condition"
        )

        end_label = self.label_manager.new_label(
            LabelType.PROC_END, "Division procedure end"
        )

        code.append(IRLabel(label_id=start_label, comment="DIVISION PROCEDURE"))
        code.append(
            IRProcCall(
                name="abs",
                args=[],
                comment="Compute absolute values and store expression sign in sign1",
            )
        )

        code.append(
            IRAssign(target=vars.result, value="0", comment="Initialize result")
        )  # result = 0
        code.append(
            IRAssign(
                target=vars.result2, value=vars.arg1, comment="Initialize remainder"
            )
        )  # remainder = dividend
        code.append(
            IRAssign(
                target=vars.arg1,
                value=vars.one,
                comment="Initialize power of divisor",
            )
        )  # power = 1

        code.append(IRLabel(label_id=power_while_label, comment="Divisor power loop"))
        code.append(
            IRCondJump(
                left=vars.arg2,
                operator=">",
                right=vars.result2,
                label=end_power_while_label,
                comment="Check if divisor is greater than remainder",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.arg2,
                left=vars.arg2,
                right=vars.arg2,
                operator="+",
                comment="Double the divisor",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.arg1,
                left=vars.arg1,
                right=vars.arg1,
                operator="+",
                comment="Double the power",
            )
        )

        code.append(
            IRJump(label=power_while_label, comment="Continue divisor power loop")
        )
        code.append(
            IRLabel(label_id=end_power_while_label, comment="End of divisor power loop")
        )

        code.append(IRLabel(label_id=divide_while_label, comment="Division loop"))
        code.append(
            IRCondJump(
                left=vars.arg1,
                operator=">",
                right=vars.zero,
                label=divide_while_helper_label,
                comment="Check if remainder is greater than 0",
            )
        )
        code.append(IRJump(label=end_divide_while_label, comment="Exit division loop"))
        code.append(
            IRLabel(
                label_id=divide_while_helper_label, comment="Helper for division loop"
            )
        )

        code.append(
            IRCondJump(
                left=vars.result2,
                operator="<",
                right=vars.arg2,
                label=if_end_divisor_loop_label,
                comment="Check if remainder is greater than 0",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.result2,
                left=vars.result2,
                right=vars.arg2,
                operator="-",
                comment="Subtract divisor from remainder",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.result,
                right=vars.arg1,
                operator="+",
                comment="Add power to result",
            )
        )

        code.append(
            IRLabel(label_id=if_end_divisor_loop_label, comment="End of divisor loop")
        )

        code.append(IRHalf(target=vars.arg1, comment="Halve the power"))

        code.append(IRHalf(target=vars.arg2, comment="Halve the divisor"))

        code.append(IRJump(label=divide_while_label, comment="Continue division loop"))
        code.append(
            IRLabel(label_id=end_divide_while_label, comment="End of division loop")
        )

        # Apply sign to result

        if_sign = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")
        if_remainder = self.label_manager.new_label(
            LabelType.IF_ELSE, "If remainder is negative"
        )

        code.append(
            IRCondJump(
                left=vars.sign1,
                operator="=",
                right=vars.one,
                label=if_remainder,
                comment="Check if sign is negative",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.zero,
                right=vars.result,
                operator="-",
                comment="Negate result",
            )
        )

        code.append(
            IRLabel(label_id=if_remainder, comment="Check if remainder is negative")
        )
        code.append(
            IRCondJump(
                left=vars.sign2,
                operator="=",
                right=vars.one,
                label=end_label,
                comment="Check if remainder is 0",
            )
        )

        code.append(
            IRBinaryOp(
                target=vars.result2,
                left=vars.zero,
                right=vars.result2,
                operator="-",
                comment="Negate remainder",
            )
        )

        code.append(IRLabel(label_id=end_label, comment="End division"))
        code.append(
            IRAssign(target=Variable("return"), value=vars.zero, comment="Return from divide")
        )

        return code
