from dataclasses import dataclass
from typing import List, Optional
from .IR_ops import *
from .procinfo import ProcInfo

@dataclass
class ArithmeticVars:
    """Container for arithmetic variables"""
    arg1: Variable = BY_VALUE(Variable("arg1"))
    arg2: Variable = BY_VALUE(Variable("arg2"))
    result: Variable = BY_VALUE(Variable("result"))
    result2: Variable = BY_VALUE(Variable("result2"))  # Used for remainder in division
    sign1: Variable = BY_VALUE(Variable("sign1"))
    sign2: Variable = BY_VALUE(Variable("sign2"))
    temp: Variable = BY_VALUE(Variable("temp"))
    zero: Variable = BY_VALUE(Variable("0", is_const=True, const_value=0))
    one: Variable = BY_VALUE(Variable("1", is_const=True, const_value=1))
    minus_one: Variable = BY_VALUE(Variable("-1", is_const=True, const_value=-1))
    divisor_copy: Variable = BY_VALUE(Variable("divisor_copy"))
    abs_return: Variable = BY_VALUE(Variable("abs#return"))
    mul_return: Variable = BY_VALUE(Variable("mul#return"))
    div_return: Variable = BY_VALUE(Variable("div#return"))
    
    
    #debugVariables
    debug1: Variable = BY_VALUE(Variable("202", is_const=True, const_value=202))
    debug2: Variable = BY_VALUE(Variable("404", is_const=True, const_value=404))
    debug3: Variable = BY_VALUE(Variable("606", is_const=True, const_value=606))

class IRArithmetic:
    """
    Implements arithmetic operations using IR code generation.
    Operations are implemented to run in logarithmic time.
    Properly handles negative numbers.
    """

    def __init__(self, label_manager: LabelManager, variables: dict[str, Variable], procinfo: dict[str, ProcInfo]):
        self.label_manager = label_manager
        self.variables = variables
        self.vars = ArithmeticVars()
        self.procinfo = procinfo
        self._init_arithmetic_vars()
        

                

    def _init_arithmetic_vars(self):
        for var in self.vars.__dict__.values():
            self.variables[var.name] = BY_VALUE(var)

    def generate_arithmetic_procedures(self, costly_operations: set) -> List[IRInstruction]:
        """Generate all arithmetic procedures"""
        code = []
        
        code.extend(self._generate_abs())
        if "*" in costly_operations:
            code.extend(self._generate_multiply())
                
            
        if "/" in costly_operations or "%" in costly_operations:
            code.extend(self._generate_divide())
        return code

    def _generate_abs(self) -> List[IRInstruction]:
        """Generate absolute value procedure"""
        code = []
        vars = self.vars
        
        
        start_label = self.label_manager.new_label(
            LabelType.PROC_START, "Absolute value procedure"
        )
        
        self.procinfo["abs"] = ProcInfo(start_label, [], vars.abs_return)
        
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

        code.append(IRLabel(label_id=start_label,
                            label_type=LabelType.PROC_START,
                            procedure="abs",                            
                            comment="ABSOLUTE VALUE PROCEDURE"))
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

        code.append(IRLabel(label_id=if_1_else,
                            label_type=LabelType.IF_ELSE,
                            comment="Negate arg1 if negative"))

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

        code.append(IRLabel(label_id=if_1_end, 
                            label_type=LabelType.IF_END,
                            comment="End absolute value for arg1"))

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

        code.append(IRLabel(label_id=if_2_else, 
                            label_type=LabelType.IF_ELSE,
                            comment="Negate arg2 if negative"))

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


        code.append(IRLabel(label_id=if_2_end, 
                            label_type=LabelType.IF_END,
                            comment="End absolute value for arg2"))

        code.append(IRLabel(label_id=end_label, 
                            label_type=LabelType.PROC_END,
                            procedure="abs",
                            comment="End absolute value"))


        code.append(
            IRReturn(return_variable=vars.abs_return, comment="Return from abs")
        )
        
        
        

        return code

    def _generate_multiply(self) -> List[IRInstruction]:
        """Generate multiplication procedure using Russian Peasant Algorithm"""
        code = []
        vars = self.vars


        start_label = self.label_manager.new_label(
            LabelType.PROC_START, "Multiply procedure start"
        )
        
        self.procinfo["mul"] = ProcInfo(start_label, [], vars.mul_return)
        
        
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

        code.append(IRLabel(label_id=start_label, 
                            label_type=LabelType.PROC_START,
                            procedure="multiply",                            
                            comment="MULTIPLY PROCEDURE"))
        code.append(
            IRProcCall(
                name="abs",
                args=[],
                comment="",
            )
        )
        
        code.append(
            IRAssign(
                target=vars.result, value=vars.zero, comment="Initialize result"
            )
        )

        # Optional : swap arg1 and arg2 if arg1 < arg2

        code.append(IRLabel(label_id=while_label,
                            label_type=LabelType.WHILE_START,
                            comment="Main multiplication loop"))
        
        
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
        code.append(IRLabel(label_id=if_help_label, 
                            label_type=LabelType.IF_HELPER,
                            comment="Helper if statement"))
        

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
                right=vars.arg2,
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

        code.append(IRLabel(label_id=if_end_label,
                            label_type=LabelType.IF_END,
                            comment="If end statement"))
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
            IRLabel(label_id=end_while_label, 
                    label_type=LabelType.WHILE_END,
                    comment="End of main multiplication loop")
        )

        # Apply sign to result

        if_sign = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")
        code.append(
            IRCondJump(
                left=vars.sign1,
                operator="=",
                right=vars.sign2,
                label=end_label,
                comment="Check if signs match",
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
        
        code.append(IRLabel(label_id=end_label,
                            procedure="multiply",
                            label_type=LabelType.PROC_END,                            
                            comment="End multiplication"))
        
        code.append(
            IRReturn(
                return_variable=vars.mul_return, comment="Return from multiply"
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
    
        
        self.procinfo["div"] = ProcInfo(start_label, [], vars.div_return)
        
        if_end = self.label_manager.new_label(LabelType.IF_END, "End of sign check")
        
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

        code.append(IRLabel(label_id=start_label, 
                            label_type=LabelType.PROC_START,
                            procedure="divide",
                            comment="DIVISION PROCEDURE"))
        
        if_else_local = self.label_manager.new_label(LabelType.IF_ELSE, "If divisor is 0")
        if_end_local = self.label_manager.new_label(LabelType.IF_END, "If divisor is not 0")
        
        
        
        code.append(
            IRCondJump(
                left=vars.arg2,
                operator="=",
                right=vars.zero,
                label=if_else_local,
                comment="Check if divisor is zero",
            ))
        
        code.append(IRJump(label=if_end_local, comment="Skip division"))
        
        
        code.append(IRLabel(label_id=if_else_local, 
                            label_type=LabelType.IF_ELSE,
                            comment="If divisor is 0"))
        
        code.append(IRAssign(
            target=vars.result,
            value=vars.zero,
            comment="Return 0 if divisor is 0",
        ))
        
        code.append(IRAssign(
            target=vars.result2,
            value=vars.zero,
            comment="Return 0 if divisor is 0",
        ))
        
        code.append(
            IRJump(label=if_end, comment="Skip division")
        )
        
        
        code.append(IRLabel(label_id=if_end_local, 
                            label_type=LabelType.IF_ELSE,
                            comment="If divisor is not zero"))
        
        code.append(
            IRProcCall(
                name="abs",
                args=[],
                comment="Compute absolute values and store expression sign in sign1",
            )
        )
        
        code.append(
            IRAssign(
                target=vars.divisor_copy,
                value=vars.arg2,
                comment="Copy dividend for sign comparison",
            )
        )

        code.append(
            IRAssign(target=vars.result, value=vars.zero, comment="Initialize result")
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

        code.append(IRLabel(label_id=power_while_label, 
                            label_type=LabelType.WHILE_START,
                            comment="Divisor power loop"))
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
            IRLabel(label_id=end_power_while_label, 
                    label_type=LabelType.WHILE_END,
                    comment="End of divisor power loop")
        )

        code.append(IRLabel(label_id=divide_while_label, 
                            label_type=LabelType.WHILE_START,
                            comment="Division loop"))
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
                label_id=divide_while_helper_label, 
                label_type=LabelType.WHILE_HELPER,
                comment="Helper for division loop"
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
            IRLabel(label_id=if_end_divisor_loop_label, 
                    label_type=LabelType.IF_END,
                    comment="End of divisor loop")
        )

        code.append(IRHalf(target=vars.arg1, comment="Halve the power"))

        code.append(IRHalf(target=vars.arg2, comment="Halve the divisor"))

        code.append(IRJump(label=divide_while_label, comment="Continue division loop"))
        code.append(
            IRLabel(label_id=end_divide_while_label, 
                    label_type=LabelType.WHILE_END,
                    comment="End of division loop")
        )

        ######## SIGNS ########

        # if_sign = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")
        # if_remainder_outer = self.label_manager.new_label(
        #     LabelType.IF_ELSE, "If remainder is negative"
        # )

        # code.append(
        #     IRCondJump(
        #         left=vars.sign1,
        #         operator="=",
        #         right=vars.sign2,
        #         label=if_remainder_outer,
        #         comment="Check if sign is negative",
        #     )
        # )
        
        # if_remainder = self.label_manager.new_label(
        #     LabelType.IF_ELSE, "If remainder is negative"
        # )
        
        # if_else_remainder = self.label_manager.new_label(
        #     LabelType.IF_ELSE, "If remainder is negative"
        # )
        
        # if_remainder_end = self.label_manager.new_label(
        #     LabelType.IF_END, "End of remainder sign check"
        # )
        
        # code.append(
        #     IRCondJump(
        #         left=vars.result2,
        #         operator="=",
        #         right=vars.zero,
        #         label=if_else_remainder,
        #         comment="Check if remainder is negative", # if zero we dont need to negate only negate result
        #     ))
        
        # # code.append(IRLabel(label_id=if_else_remainder,
        # #             label_type=LabelType.IF_ELSE,
        # #             comment="If remainfer not 0"))
        
        # # code.append(IRJump(label=if_remainder_end, comment="Skip negation"))

        # code.append(
        #     IRBinaryOp(
        #         target=vars.result,
        #         left=vars.result,
        #         right=vars.one,
        #         operator="+",
        #         comment="Add 1 to result",
        #     )
        # )
    

        # code.append(
        #     IRBinaryOp(
        #         target=vars.result2,
        #         left=vars.result2,
        #         right=vars.divisor_copy,
        #         operator="-",
        #         comment="Negate remainder",
        #     )        
        # )

        # code.append(IRLabel(label_id=if_else_remainder,
        #                     label_type=LabelType.IF_ELSE,
        #                     comment="If remainder is zero"))
        
        # code.append(
        #     IRBinaryOp(
        #         target=vars.result,
        #         left=vars.zero,
        #         right=vars.result,
        #         operator="-",
        #         comment="Negate result",
        # ))

        
        
        # code.append(IRLabel(label_id=if_remainder_end,
        #                     label_type=LabelType.IF_END,
        #                     comment="End of remainder sign check"))
        
        
        
        
        # #No need for sign change
        
        # code.append(
        #     IRLabel(label_id=if_remainder_outer, 
        #             label_type=LabelType.IF_ELSE,
        #             comment="Check if remainder is negative")
        # )

        # code.append(IRLabel(label_id=end_label,
        #                     label_type=LabelType.PROC_END,
        #                     procedure="divide",
        #                     comment="End division"))
        # code.append(
        #     IRReturn(return_variable=vars.div_return, comment="Return from divide")
        # )
        
        # checks1 = self.label_manager.new_label(LabelType.IF_ELSE, "If sign is negative")

        a_neg_b_pos = self.label_manager.new_label(LabelType.IF_ELSE, "If a is negative and b is positive")
        a_pos_check_s2 = self.label_manager.new_label(LabelType.IF_ELSE, "Check if sign2 is negative")
        carry_on = self.label_manager.new_label(LabelType.IF_ELSE, "Carry on with division")
        if_helper = self.label_manager.new_label(LabelType.IF_HELPER, "Helper for division")
        
        
        
        code.append(
            IRCondJump(
                left=vars.result2,
                operator="=",
                right=vars.zero,
                label=if_helper,
                comment="Check if signs match",
            )
        )
        code.append(
            IRJump(label=carry_on, comment="Skip negation")
        )
        code.append(
            IRLabel(label_id=if_helper, 
                     label_type=LabelType.IF_HELPER,
                     comment="Helper for division"))
        
        code.append(
            IRCondJump(
                left=vars.sign1,
                operator="=",
                right=vars.sign2,
                label=if_end,
                comment="Check if signs match",
            ))
        
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
            IRJump(label=if_end, comment="Skip negation"))
        
        code.append(IRLabel(label_id=carry_on, 
                            label_type=LabelType.IF_ELSE,
                            comment="Carry on with division"))
        
        
        
        
        
        
        # IF sign1 > 0
        code.append(
            IRCondJump(
                left=vars.sign1,
                operator=">",
                right=vars.zero,
                label=a_pos_check_s2,
                comment="Check if signs match",
            )
        )
        
        # HERE sign1 < 0
        
        code.append(
            IRCondJump(
                left=vars.sign2,
                operator=">",
                right=vars.zero,
                label=a_neg_b_pos,
                comment="Check if signs match",
            )
        )
        
        # HERE sign1 < 0, sign2 < 0 -> result > 0 and remainder < 0
        code.append(
            IRBinaryOp(
                target=vars.result2,
                left=vars.zero,
                right=vars.result2,
                operator="-",
                comment="Negate result",
            )
        )
        
        code.append(IRJump(label=if_end, comment="Skip negation"))
        
        # HERE sign1 < 0, sign2 > 0 -> result < 0 and remainder > 0
        code.append(IRLabel(label_id=a_neg_b_pos, 
                                 label_type=LabelType.IF_ELSE,
                                 comment="If a is negative and b is positive"))
        
        # a:a +1 then negate a; b:-b then b:=b+copy_divisor
        
        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.result,
                right=vars.one,
                operator="+",
                comment="Add 1 to result",
            )
        )
        
        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.zero,
                right=vars.result,
                operator="-",
                comment="Negate remainder",
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
        
        code.append(
            IRBinaryOp(
                target=vars.result2,
                left=vars.result2,
                right=vars.divisor_copy,
                operator="+",
                comment="Negate remainder",
            )
        )
        
        code.append(IRJump(label=if_end, comment="Skip negation"))
        
        code.append(IRLabel(label_id=a_pos_check_s2, 
                                 label_type=LabelType.IF_ELSE,
                                 comment="Check if sign2 is negative"))
        
        # HERE sign1 > 0
        
        a_pos_b_pos = self.label_manager.new_label(LabelType.IF_ELSE, "If a is positive and b is negative")
        
        code.append(
            IRCondJump(
                left=vars.sign2,
                operator=">",
                right=vars.zero,
                label=if_end,
                comment="Check if signs match",
            )
        )
        
        # HERE sign1 > 0, sign2 < 0
        # a:a +1 then negate a; b:b- copy_divisor
        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.result,
                right=vars.one,
                operator="+",
                comment="Add 1 to result",
            ))
        
        code.append(
            IRBinaryOp(
                target=vars.result,
                left=vars.zero,
                right=vars.result,
                operator="-",
                comment="Negate remainder",
            )
        )
        
        code.append(
            IRBinaryOp(
                target=vars.result2,
                left=vars.result2,
                right=vars.divisor_copy,
                operator="-",
                comment="Negate remainder",
            )
        )
        
        code.append(IRLabel(label_id=if_end, 
                                 label_type=LabelType.IF_END,
                                 comment="End of sign check"))        

        code.append(
            IRReturn(return_variable=vars.div_return, comment="Return from divide")
        )
        

        return code
