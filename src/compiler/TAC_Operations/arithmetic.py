from typing import List, Optional, Tuple
from dataclasses import dataclass
from .tac_ops import *
from ..ast_nodes import *
from ..symbol_table import *

class ArithmeticGenerator:
    """
    Handles generation of optimized arithmetic operations for the virtual machine.
    All operations are implemented using the basic instruction set:
    ADD, SUB, HALF, and bit shifts via multiplication by 2 (ADD p0, p0)
    """
    
    def __init__(self, temp_generator):
        self.temp_gen = temp_generator
        
    def generate_multiplication(self, result: str, a: str, b: str) -> List[TACOp]:
        """
        Implements multiplication using Russian Peasant algorithm.
        Time complexity: O(log n) where n is the value of b
        """
        ops = []
        
        # Get temporary variables
        temp_a = self.temp_gen.get_temp()  # Will hold the doubling number
        temp_b = self.temp_gen.get_temp()  # Will hold the halving number
        temp_result = self.temp_gen.get_temp()  # Accumulates result
        
        # Labels for our loops
        loop_label = self.temp_gen.get_label("mult_loop")
        end_label = self.temp_gen.get_label("mult_end")
        
        # Initialize variables
        ops.extend([
            # Load initial values
            LoadOp(int(a)), 
            StoreOp(int(temp_a)),  # temp_a = a
            LoadOp(int(b)),
            StoreOp(int(temp_b)),  # temp_b = b
            SetOp(0),
            StoreOp(int(temp_result))  # temp_result = 0
        ])
        
        # Main multiplication loop
        ops.extend([
            Label(loop_label),
            
            # Check if temp_b is odd
            LoadOp(int(temp_b)),
            HalfOp(),
            StoreOp(int(temp_b) + 1),  # Store half for later
            
            # Double it to check remainder
            AddOp(int(temp_b) + 1),
            SubOp(int(temp_b)),
            
            # If remainder is 1 (odd), add temp_a to result
            JZEROOp(3),  # Skip add if even
            LoadOp(int(temp_result)),
            AddOp(int(temp_a)),
            StoreOp(int(temp_result)),
            
            # Double temp_a
            LoadOp(int(temp_a)),
            AddOp(int(temp_a)),
            StoreOp(int(temp_a)),
            
            # Load halved temp_b back
            LoadOp(int(temp_b) + 1),
            StoreOp(int(temp_b)),
            
            # Check if temp_b is zero
            LoadOp(int(temp_b)),
            JZEROOp(2),  # Jump to end if zero
            JumpOp(loop_label),
            
            Label(end_label)
        ])
        
        # Store final result
        ops.extend([
            LoadOp(int(temp_result)),
            StoreOp(int(result))
        ])
        
        return ops

    def generate_division(self, result: str, a: str, b: str) -> List[TACOp]:
        """
        Implements division using binary long division algorithm.
        Time complexity: O(log n) where n is the larger of a or b
        Handles division by zero according to spec (returns 0)
        """
        ops = []
        
        # Temporary variables
        temp_divisor = self.temp_gen.get_temp()       # Current divisor
        temp_dividend = self.temp_gen.get_temp()      # Current dividend
        temp_quotient = self.temp_gen.get_temp()      # Building quotient
        temp_power = self.temp_gen.get_temp()         # Power of 2 tracker
        
        # Labels
        div_by_zero_label = self.temp_gen.get_label("div_zero")
        normalize_label = self.temp_gen.get_label("div_norm")
        main_loop_label = self.temp_gen.get_label("div_loop")
        end_label = self.temp_gen.get_label("div_end")
        
        ops.extend([
            # Store initial values
            LoadOp(int(b)),
            JZEROOp(div_by_zero_label),  # Check for division by zero
            
            StoreOp(int(temp_divisor)),
            LoadOp(int(a)),
            StoreOp(int(temp_dividend)),
            SetOp(0),
            StoreOp(int(temp_quotient)),
            SetOp(1),
            StoreOp(int(temp_power)),
            
            # Normalize divisor (shift left until larger than dividend)
            Label(normalize_label),
            LoadOp(int(temp_divisor)),
            SubOp(int(temp_dividend)),
            JPOSOp(main_loop_label),  # If divisor > dividend, start main loop
            
            # Double divisor and power
            LoadOp(int(temp_divisor)),
            AddOp(int(temp_divisor)),
            StoreOp(int(temp_divisor)),
            LoadOp(int(temp_power)),
            AddOp(int(temp_power)),
            StoreOp(int(temp_power)),
            JumpOp(normalize_label),
            
            # Main division loop
            Label(main_loop_label),
            LoadOp(int(temp_dividend)),
            SubOp(int(temp_divisor)),
            JNEGOp(3),  # Skip if dividend < divisor
            
            # Dividend >= divisor, update quotient and dividend
            StoreOp(int(temp_dividend)),
            LoadOp(int(temp_quotient)),
            AddOp(int(temp_power)),
            StoreOp(int(temp_quotient)),
            
            # Halve divisor and power
            LoadOp(int(temp_divisor)),
            HalfOp(),
            StoreOp(int(temp_divisor)),
            LoadOp(int(temp_power)),
            HalfOp(),
            StoreOp(int(temp_power)),
            JZEROOp(2),  # If power is 0, we're done
            JumpOp(main_loop_label),
            JumpOp(end_label),
            
            # Division by zero handler
            Label(div_by_zero_label),
            SetOp(0),
            StoreOp(int(result)),
            JumpOp(end_label),
            
            # Store final result
            Label(end_label),
            LoadOp(int(temp_quotient)),
            StoreOp(int(result))
        ])
        
        return ops

    def generate_modulo(self, result: str, a: str, b: str) -> List[TACOp]:
        """
        Implements modulo using the division algorithm.
        According to spec: result should have same sign as divisor
        and x mod 0 should return 0
        """
        ops = []
        
        # Temporary variables
        temp_quotient = self.temp_gen.get_temp()
        temp_product = self.temp_gen.get_temp()
        
        # First compute division
        ops.extend(self.generate_division(temp_quotient, a, b))
        
        # Then multiply quotient by divisor
        ops.extend(self.generate_multiplication(temp_product, temp_quotient, b))
        
        # Finally subtract: a - (quotient * b) to get remainder
        ops.extend([
            LoadOp(int(a)),
            SubOp(int(temp_product)),
            StoreOp(int(result))
        ])
        
        # Handle division by zero case
        zero_label = self.temp_gen.get_label("mod_zero")
        end_label = self.temp_gen.get_label("mod_end")
        
        ops.extend([
            LoadOp(int(b)),
            JZEROOp(3),
            JumpOp(end_label),
            Label(zero_label),
            SetOp(0),
            StoreOp(int(result)),
            Label(end_label)
        ])
        
        return ops

    def optimize_multiply_by_constant(self, result: str, a: str, constant: int) -> List[TACOp]:
        """
        Optimizes multiplication when one operand is a constant.
        Uses additions and shifts based on binary representation.
        """
        ops = []
        
        if constant == 0:
            ops.extend([
                SetOp(0),
                StoreOp(int(result))
            ])
            return ops
            
        # Convert constant to binary and find 1 bits
        bin_str = bin(abs(constant))[2:]  # Remove '0b' prefix
        one_positions = [i for i, bit in enumerate(reversed(bin_str)) if bit == '1']
        
        # Initialize result with 0
        ops.extend([
            SetOp(0),
            StoreOp(int(result))
        ])
        
        temp = self.temp_gen.get_temp()
        # Load and store initial value
        ops.extend([
            LoadOp(int(a)),
            StoreOp(int(temp))
        ])
        
        # Add shifted values based on 1 bits
        for pos in one_positions:
            if pos > 0:
                # Shift left pos times by repeated addition
                for _ in range(pos):
                    ops.extend([
                        LoadOp(int(temp)),
                        AddOp(int(temp)),
                        StoreOp(int(temp))
                    ])
            
            # Add to result
            ops.extend([
                LoadOp(int(result)),
                AddOp(int(temp)),
                StoreOp(int(result))
            ])
            
        # Handle negative constant
        if constant < 0:
            ops.extend([
                LoadOp(int(result)),
                SetOp(0),
                SubOp(int(result)),
                StoreOp(int(result))
            ])
        
        return ops