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

    def _add_error(self, message: str, location: Location) -> None:
        """Add a semantic error with location information."""
        self.errors.append(SemanticError(
            message=message,
            line=location.line,
            column=location.column
        ))

    def analyze(self, program: Program) -> Tuple[bool, List[SemanticError], SymbolTable]:
        """Analyze program for semantic correctness."""
        self.errors = []
        self.symbol_table = SymbolTable()
        self.declared_procedures.clear()
        self.initialized_variables.clear()
        
        # First just register procedures
        for proc in program.procedures:
            print(proc.name)
            if proc.name in self.declared_procedures:
                self._add_error(f"Procedure {proc.name} already defined", proc.location)
                continue
            self.declared_procedures.add(proc.name)
            print(f"Adding procedure {proc.name} with parameters {proc.parameters}")
            try:
                self.symbol_table.add_procedure(proc.name, proc.parameters)
            except ValueError as e:
                self._add_error(str(e), proc.location)

            try:
                self._check_procedure(proc)
            except Exception as e:
                self._add_error(str(e), proc.location)
        

        
        # Finally analyze main program
        self._check_main_program(program.declarations, program.commands)
        
        return len(self.errors) == 0, self.errors, self.symbol_table

    def _check_main_program(self, declarations: List[Declaration], commands: List[Command]) -> None:
        """Check main program declarations and commands."""
        # Clear initialized variables for main program
        self.initialized_variables.clear()
        self.current_procedure = None
        self.symbol_table.exit_procedure()  # Ensure we're in global scope
        
        # Check declarations
        for decl in declarations:
            self._check_declaration(decl, 'global')
        
        # Process commands
        for cmd in commands:
            self._check_command(cmd)

    def _check_procedure(self, proc: Procedure) -> None:
        """Check procedure body."""
        # Save current procedure and enter new scope
        prev_procedure = self.current_procedure
        self.current_procedure = proc.name
        
        # Enter procedure scope
        self.symbol_table.enter_procedure(proc.name)
        
        # Save current initialized variables
        prev_initialized = self.initialized_variables.copy()
        print(f"procedure {proc.name} initialized variables: {self.initialized_variables}")
        print(f"prev_initialized: {prev_initialized}")
        self.initialized_variables.clear()
        
        print(f"procedure parameters: {proc.parameters}") 
        # Add parameters to initialized variables and declare them
        for param_name, is_array in proc.parameters:
            # Add parameter to symbol table
            try:
                self.symbol_table.add_symbol(
                    name=param_name,
                    symbol_type='parameter',
                    is_array=is_array,
                    is_parameter=True
                )
                # Mark only the parameter as initialized, not local variables
                self.initialized_variables.add(param_name)
            except ValueError as e:
                self._add_error(str(e), proc.location)
        
        # Check local declarations but DON'T mark tshem as initialized
        for decl in proc.declarations:
            self._check_declaration(decl, 'local')
            # Remove this line - local variables aren't automatically initialized
            # self.initialized_variables.add(decl.name)
        
        # Check commands
        for cmd in proc.commands:
            self._check_command(cmd)
        
        # Restore state
        self.initialized_variables = prev_initialized
        self.current_procedure = prev_procedure
        self.symbol_table.exit_procedure()

    def _check_argument(self, arg: Expression, is_array: bool, location: Location) -> None:
        """Check if procedure call argument is valid."""
        if isinstance(arg, Identifier):
            symbol = self.symbol_table.lookup(arg.name)
            if not symbol:
                self._add_error(f"Undefined variable '{arg.name}'", arg.location)
                return
                
            # Check array vs non-array match
            if is_array != symbol.is_array:
                expected = "array (T parameter)" if is_array else "non-array"
                got = "array" if symbol.is_array else "non-array"
                self._add_error(
                    f"Type mismatch: expected {expected} but got {got} for '{arg.name}'",
                    arg.location
                )
                return
                
            # For non-array arguments, check initialization
            if not is_array and arg.name not in self.initialized_variables:
                self._add_error(
                    f"Vaaariable '{arg.name}' used before initialization",
                    arg.location
                )

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
        print(f"Checking assignment {cmd}")  # Debug
        if not self._check_variable(cmd.target):
            return

        # Check if trying to modify FOR loop iterator
        if cmd.target.name in self.for_loop_iterators:
            self._add_error(
                f"Cannot modify FOR loop iterator '{cmd.target.name}'",
                cmd.location
            )
            return

        self._check_expression(cmd.value)
        self.initialized_variables.add(cmd.target.name)


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
                    symbol_type=scope_type,
                    is_array=True,
                    array_start=start,
                    array_end=end
                )
                # Mark array as initialized upon declaration
                self.initialized_variables.add(decl.name)
            else:
                # Add simple variable to symbol table
                self.symbol_table.add_symbol(
                    name=decl.name,
                    symbol_type=scope_type,
                    is_array=False
                )
        except ValueError as e:
            self._add_error(str(e), decl.location)

    def _check_for_loop(self, cmd: ForLoop) -> None:
        """Check for loop."""
        # Check start and end expressions
        self._check_value(cmd.start)
        self._check_value(cmd.end)
        
        # Add iterator to symbol table as a local variable
        try:
            self.symbol_table.add_symbol(
                name=cmd.iterator,
                symbol_type='local',
                is_array=False
            )
        except ValueError:
            # If iterator already exists in symbol table, that's okay
            pass
        
        # Save current initialized variables
        prev_initialized = self.initialized_variables.copy()
        
        # Add iterator to initialized variables and trackers
        self.initialized_variables.add(cmd.iterator)
        self.for_loop_iterators.add(cmd.iterator)
        
        # Process loop body
        for command in cmd.body:
            self._check_command(command)
            
        # Remove iterator from trackers and symbol table
        self.for_loop_iterators.remove(cmd.iterator)
        
        # Restore initialized variables from before loop
        self.initialized_variables = prev_initialized

    def _check_procedure_call(self, cmd: ProcedureCall) -> None:
        """Check if a procedure call is semantically valid."""
        
        local_vars = set()
        if self.current_procedure:
            for name, symbol in self.symbol_table.symbols.items():
                if (symbol.procedure_name == self.current_procedure and 
                    symbol.symbol_type == 'local'):
                    local_vars.add(symbol.name)
        
        if cmd.name == self.current_procedure:
            self._add_error(f"Recursive procedure call to '{cmd.name}' is not allowed", cmd.location)
            return
                
        if cmd.name not in self.declared_procedures:
            self._add_error(f"Undefined procedure '{cmd.name}'", cmd.location)
            return

        proc_params = self.symbol_table.get_procedure_params(cmd.name)
        print(f"Procedure {cmd.name} parameters: {proc_params}")
        if proc_params is None:
            self._add_error(f"Cannot find parameters for procedure '{cmd.name}'", cmd.location)
            return

        if len(cmd.arguments) != len(proc_params):
            self._add_error(
                f"Wrong number of arguments in procedure '{cmd.name}' call",
                cmd.location
            )
            return

        # # First, check all arguments for existence and type matching
        # for i, (arg, (param_name, is_array)) in enumerate(zip(cmd.arguments, proc_params)):
        #     if isinstance(arg, Identifier):
        #         symbol = self.symbol_table.lookup(arg.name)
        #         if not symbol:
        #             self._add_error(f"Undefined variable '{arg.name}'", arg.location)
        #             continue
                
        #         # Check array vs non-array match
        #         if is_array != symbol.is_array:
        #             self._add_error(
        #                 f"Type mismatch for argument '{arg.name}'",
        #                 arg.location
        #             )
        #             continue
        # print(f"Checking {cmd.arguments}")
        # for i, arg in enumerate(cmd.arguments):
            
        #     if isinstance(arg, Identifier):
        #         print(f"Checking {arg.name}, local vars: {local_vars}")
        #         # Don't check initialization for:
        #         # 1. Local variables of current procedure
        #         # 2. Parameters of current procedure
        #         if (arg.name not in local_vars and 
        #             not self.symbol_table.is_parameter(arg.name) and 
        #             arg.name not in self.initialized_variables):
        #             self._add_error(
        #                 f"Variable '{arg.name}' used before initialization",
        #                 arg.location
        #             )
        
        for i, (arg, (param_name, is_array)) in enumerate(zip(cmd.arguments, proc_params)):
            if isinstance(arg, Identifier):
                symbol = self.symbol_table.lookup(arg.name)
                if not symbol:
                    self._add_error(f"Undefined variable '{arg.name}'", arg.location)
                    continue
                
                # Check array vs non-array match
                if is_array != symbol.is_array:
                    self._add_error(
                        f"Type mismatch for argument '{arg.name}'",
                        arg.location
                    )
                    continue

                # Since parameters are IN-OUT, mark the variable as initialized 
                # after the procedure call
                self.initialized_variables.add(arg.name)

    def _check_variable(self, var: Identifier) -> bool:
        """Check if a variable reference is valid."""
        symbol = self.symbol_table.lookup(var.name)
        print(f"Checking in _check_variable variable {var.name}")  # Debug
        print(f"Symbol: {symbol}")  # Debug
        print(var.array_index)
        if not symbol:
            self._add_error(f"Undefined variable '{var.name}'", var.location)
            return False

        # Check array access
        if var.array_index is not None:
            if not symbol.is_array:
                self._add_error(f"Variable '{var.name}' is not an array", var.location)
                return False
            # Check array index
            self._check_value(var.array_index)

            if var.name not in self.initialized_variables:
                if not symbol.is_parameter:
                    self._add_error(f"Array '{var.name}' used before initialization", var.location)
                    return False
        elif symbol.is_array:
            self._add_error(f"Array '{var.name}' must be accessed with an index", var.location)
            return False

        return True


    def _check_expression(self, expr: Expression) -> None:
        if isinstance(expr, BinaryOp):
            self._check_value(expr.left)
            self._check_value(expr.right)
            
            # Check division by zero for constants
            if expr.operator in ['/', '%'] and isinstance(expr.right, Number):
                if expr.right.value == 0:
                    self._add_error(
                        "Division by zero",
                        expr.location
                    )
        else:
            self._check_value(expr)

    def _check_value(self, value: Value) -> None:
        if isinstance(value, Number):
            return
        elif isinstance(value, Identifier):
            if self._check_variable(value):
                # Check if variable was initialized
                print(f"Checking if {value.name} is initialized")  # Debug
                if (value.name not in self.initialized_variables and 
                    not self.symbol_table.is_parameter(value.name)):
                    self._add_error(
                        f"Vaaariable '{value.name}' used before initialization",
                        value.location
                    )
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
        
        # Track variables that are guaranteed to be initialized in the first iteration
        first_iter_vars = set()
        
        # First pass - collect variables initialized in first iteration
        for command in cmd.body:
            if isinstance(command, Assignment):
                first_iter_vars.add(command.target.name)
            elif isinstance(command, IfStatement):
                # For if statements, only count variables initialized in both branches
                then_vars = set()
                else_vars = set()
                # ... collect vars from both branches
                common_vars = then_vars & else_vars
                first_iter_vars.update(common_vars)
        
        # Add first iteration variables to initialized set
        self.initialized_variables.update(first_iter_vars)
        
        # Second pass - actual command checking with updated initialization info
        for command in cmd.body:
            self._check_command(command)
        
        # Keep variables that were initialized in all paths through the loop
        self.initialized_variables.update(first_iter_vars)

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
        """Check if a read command is semantically valid."""
        # Check if target exists and is a valid l-value
        if self._check_variable(cmd.target):
            # For array elements, mark the whole array as initialized
            if cmd.target.array_index is not None:
                self.initialized_variables.add(cmd.target.name)
            else:
                # For regular variables
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
            self._add_error(
                f"Invalid comparison operator: {condition.operator}",
                condition.location
            )