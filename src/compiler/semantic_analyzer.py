# src/compiler/semantic_analyzer.py
from typing import List, Set, Optional, Dict, Tuple
from .ast_nodes import *
from .symbol_table import SymbolTable, Symbol
from .semantic_error import SemanticError

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[Tuple[str, Location]] = []  # (message, location)
        self.current_procedure: Optional[str] = None
        self.for_loop_iterators: Set[str] = set()
        self.declared_procedures: Set[str] = set()
        self.initialized_variables: Set[str] = set()

    def analyze(self, program: Program) -> Tuple[bool, List[SemanticError], SymbolTable]:
        """Analyze program for semantic correctness."""
        self.errors = []
        self.symbol_table = SymbolTable()
        
        # First process all procedure definitions
        for proc in program.procedures:
            self._check_procedure(proc)
        
        # Then process global declarations
        for decl in program.declarations:
            self._check_declaration(decl, 'global')  # Using 'global' as symbol_type
        
        # Finally process main program commands
        for cmd in program.commands:
            self._check_command(cmd)
        
        return len(self.errors) == 0, self.errors, self.symbol_table

    def _collect_procedures(self, program: Program) -> None:
        for proc in program.procedures:
            if proc.name in self.declared_procedures:
                self.errors.append((
                    f"Procedure '{proc.name}' already defined",
                    proc.location
                ))
            else:
                self.declared_procedures.add(proc.name)
                self.symbol_table.add_procedure(
                    name=proc.name,
                    parameters=proc.parameters,
                    location=proc.location
                )

    def _check_declaration(self, decl: Declaration, scope_type: str) -> None:
        """
        Check if a declaration is semantically valid.
        scope_type can be 'global', 'local', or 'parameter'
        """
        # Check for redeclaration in current scope
        if self.symbol_table.lookup_current_scope(decl.name):
            self._add_error(f"Redeclaration of '{decl.name}' in current scope", decl.location)
            return

        try:
            # Check array bounds if it's an array
            if decl.array_bounds is not None:
                start, end = decl.array_bounds
                if start > end:
                    self._add_error(
                        f"Invalid array bounds [{start}:{end}] - start index greater than end index",
                        decl.location
                    )
                    return

                # Add array to symbol table
                self.symbol_table.add_symbol(
                    name=decl.name,
                    symbol_type=scope_type,  # Using scope_type instead of scope
                    is_array=True,
                    array_start=start,
                    array_end=end
                )
            else:
                # Add simple variable to symbol table
                self.symbol_table.add_symbol(
                    name=decl.name,
                    symbol_type=scope_type,  # Using scope_type instead of scope
                    is_array=False
                )
        except ValueError as e:
            self._add_error(str(e), decl.location)


    def _check_procedure(self, proc: Procedure) -> None:
        """Check if a procedure definition is semantically valid."""
        # Add procedure to symbol table
        try:
            self.symbol_table.add_procedure(proc.name, proc.parameters)
        except ValueError as e:
            self._add_error(str(e), proc.location)
            return

        # Enter procedure scope
        self.symbol_table.enter_procedure(proc.name)
        
        # Check procedure declarations
        for decl in proc.declarations:
            self._check_declaration(decl, 'local')  # Using 'local' as symbol_type
        
        # Check procedure commands
        for cmd in proc.commands:
            self._check_command(cmd)
        
        # Exit procedure scope
        self.symbol_table.exit_procedure()

    # src/compiler/semantic_analyzer.py (continued)
    def _check_command(self, cmd: Command) -> None:
        if isinstance(cmd, Assignment):
            self._check_assignment(cmd)
        elif isinstance(cmd, IfStatement):
            self._check_if_statement(cmd)
        elif isinstance(cmd, WhileLoop):
            self._check_while_loop(cmd)
        elif isinstance(cmd, RepeatLoop):
            self._check_repeat_loop(cmd)
        elif isinstance(cmd, ForLoop):
            self._check_for_loop(cmd)
        elif isinstance(cmd, ProcedureCall):
            self._check_procedure_call(cmd)
        elif isinstance(cmd, ReadCommand):
            self._check_read(cmd)
        elif isinstance(cmd, WriteCommand):
            self._check_write(cmd)

    def _check_assignment(self, cmd: Assignment) -> None:
        # Check if target exists
        if not self._check_variable(cmd.target):
            return

        # Check if trying to modify FOR loop iterator
        if cmd.target.name in self.for_loop_iterators:
            self.errors.append((
                f"Cannot modify FOR loop iterator '{cmd.target.name}'",
                cmd.location
            ))
            return

        self._check_expression(cmd.value)
        self.initialized_variables.add(cmd.target.name)

    def _check_for_loop(self, cmd: ForLoop) -> None:
        if cmd.iterator in self.for_loop_iterators:
            self.errors.append((
                f"Nested FOR loop with same iterator '{cmd.iterator}'",
                cmd.location
            ))
            return

        self.for_loop_iterators.add(cmd.iterator)
        self._check_value(cmd.start)
        self._check_value(cmd.end)
        
        # Process loop body
        for command in cmd.body:
            self._check_command(command)
            
        self.for_loop_iterators.remove(cmd.iterator)

    def _check_procedure_call(self, cmd: ProcedureCall) -> None:
        # Check if procedure exists
        proc_symbol = self.symbol_table.lookup(cmd.name)
        if not proc_symbol or proc_symbol.symbol_type != 'procedure':
            self.errors.append((
                f"Undefined procedure '{cmd.name}'",
                cmd.location
            ))
            return

        # Check recursive call
        if cmd.name == self.current_procedure:
            self.errors.append((
                f"Recursive procedure calls are not allowed",
                cmd.location
            ))
            return

        # Check if called procedure was defined earlier
        if cmd.name not in self.declared_procedures:
            self.errors.append((
                f"Cannot call procedure '{cmd.name}' before its definition",
                cmd.location
            ))
            return

        # Check arguments
        if len(cmd.arguments) != len(proc_symbol.procedure_params):
            self.errors.append((
                f"Wrong number of arguments in procedure '{cmd.name}' call",
                cmd.location
            ))
            return

        # Check each argument
        for arg, (param_name, is_array) in zip(cmd.arguments, proc_symbol.procedure_params):
            if not self._check_variable(arg):
                continue
            
            # Check parameter type match
            arg_symbol = self.symbol_table.lookup(arg.name)
            if is_array != (arg_symbol.symbol_type == 'array'):
                self.errors.append((
                    f"Type mismatch in procedure call: parameter requires {'array' if is_array else 'variable'} but got {'array' if arg_symbol.symbol_type == 'array' else 'variable'}",
                    arg.location
                ))

    def _check_variable(self, var: Identifier) -> bool:
        symbol = self.symbol_table.lookup(var.name)
        if not symbol:
            self.errors.append((
                f"Undefined variable '{var.name}'",
                var.location
            ))
            return False

        if var.array_index is not None:
            if symbol.symbol_type != 'array':
                self.errors.append((
                    f"Variable '{var.name}' is not an array",
                    var.location
                ))
                return False
            self._check_value(var.array_index)

        return True

    def _check_expression(self, expr: Expression) -> None:
        if isinstance(expr, BinaryOp):
            self._check_value(expr.left)
            self._check_value(expr.right)
            
            # Check division by zero for constants
            if expr.operator in ['/', '%'] and isinstance(expr.right, Number):
                if expr.right.value == 0:
                    self.errors.append((
                        "Division by zero",
                        expr.location
                    ))
        else:
            self._check_value(expr)

    def _check_value(self, value: Value) -> None:
        if isinstance(value, Number):
            return
        elif isinstance(value, Identifier):
            if self._check_variable(value):
                # Check if variable was initialized
                if (value.name not in self.initialized_variables and 
                    not self.symbol_table.is_parameter(value.name)):
                    self.errors.append((
                        f"Variable '{value.name}' used before initialization",
                        value.location
                    ))
    # Add these methods to the SemanticAnalyzer class

    def _check_if_statement(self, cmd: IfStatement) -> None:
        # Check condition
        self._check_condition(cmd.condition)
        
        # Create sets to track variables initialized in each branch
        pre_then_vars = set(self.initialized_variables)
        
        # Check then block
        for command in cmd.then_block:
            self._check_command(command)
        
        # Store variables initialized in then block
        then_vars = set(self.initialized_variables)
        self.initialized_variables = pre_then_vars
        
        # Check else block if it exists
        if cmd.else_block:
            for command in cmd.else_block:
                self._check_command(command)
            
            # Only keep variables initialized in both branches
            self.initialized_variables.intersection_update(then_vars)
        else:
            # If no else block, only keep previously initialized variables
            self.initialized_variables = pre_then_vars

    def _check_while_loop(self, cmd: WhileLoop) -> None:
        # Check condition first
        self._check_condition(cmd.condition)
        
        # Save set of initialized variables before loop
        pre_loop_vars = set(self.initialized_variables)
        
        # Check loop body
        for command in cmd.body:
            self._check_command(command)
        
        # After loop, only variables that were initialized before loop are guaranteed to be initialized
        self.initialized_variables = pre_loop_vars

    def _check_repeat_loop(self, cmd: RepeatLoop) -> None:
        # Save set of initialized variables before loop
        pre_loop_vars = set(self.initialized_variables)
        
        # Check loop body
        for command in cmd.body:
            self._check_command(command)
        
        # Check condition
        self._check_condition(cmd.condition)
        
        # After loop, only variables that were initialized before loop are guaranteed to be initialized
        self.initialized_variables = pre_loop_vars

    def _check_read(self, cmd: ReadCommand) -> None:
        # Check if target exists and is a valid l-value
        if self._check_variable(cmd.target):
            # Mark variable as initialized
            self.initialized_variables.add(cmd.target.name)

    def _check_write(self, cmd: WriteCommand) -> None:
        # Check if value is valid
        self._check_value(cmd.value)

    def _check_condition(self, condition: Condition) -> None:
        # Check both sides of the condition
        self._check_expression(condition.left)
        self._check_expression(condition.right)
        
        # Validate condition operator
        valid_operators = ['=', '!=', '<', '>', '<=', '>=']
        if condition.operator not in valid_operators:
            self.errors.append((
                f"Invalid comparison operator: {condition.operator}",
                condition.location
            ))