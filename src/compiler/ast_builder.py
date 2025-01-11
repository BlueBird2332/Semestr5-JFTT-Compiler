from typing import List, Optional, Tuple, Any
from .ast_nodes import *

class ASTBuilder:
    """
    AST Builder for the compiler.
    Converts tree-sitter parse tree into our AST representation.
    """
    
    def build(self, node: Any) -> Program:
        """Entry point for AST building."""
        if node is None:
            raise ValueError("Cannot build AST from None node")
            
        if node.type != 'program_all':
            raise ValueError(f"Expected program_all node, got {node.type}")
            
        procedures = []
        declarations = []
        commands = []
        
        # Process each child based on type
        for child in node.children:
            if child.type == 'procedures':
                procedures = self.build_procedures(child)
            elif child.type == 'main':
                declarations, commands = self.build_main(child)
                
        return Program(
            location=self.get_location(node),
            procedures=procedures,
            declarations=declarations,
            commands=commands
        )

    def build_procedures(self, node: Any) -> List[Procedure]:
        """
        Build list of procedures.
        procedures -> procedures PROCEDURE proc_head IS declarations BEGIN commands END
                   | procedures PROCEDURE proc_head IS BEGIN commands END
                   | ε
        """
        procedures = []
        
        for child in node.children:
            if child.type == 'procedure_def':
                procedures.append(self.build_procedure_def(child))
                
        return procedures

    def build_procedure_def(self, node: Any) -> Procedure:
        """Build a single procedure definition."""
        proc_head = None
        declarations = []
        commands = []
        
        for child in node.children:
            if child.type == 'proc_head':
                proc_head = self.build_proc_head(child)
            elif child.type == 'declarations':
                declarations = self.build_declarations(child)
            elif child.type == 'commands':
                commands = self.build_commands(child)
                
        if not proc_head:
            raise ValueError("Procedure definition missing procedure head")
            
        return Procedure(
            location=self.get_location(node),
            name=proc_head.name,
            parameters=proc_head.parameters,
            declarations=declarations,
            commands=commands
        )

    def build_proc_head(self, node: Any) -> ProcHead:
        """
        Build procedure head.
        proc_head -> pidentifier ( args_decl )
        """
        name = None
        parameters = []
        
        for child in node.children:
            if child.type == 'pidentifier' and not name:
                name = child.text.decode('utf8')
            elif child.type == 'args_decl':
                parameters = self.build_args_decl(child)
                
        if not name:
            raise ValueError("Procedure head missing name")
            
        return ProcHead(
            location=self.get_location(node),
            name=name,
            parameters=parameters
        )

    def build_args_decl(self, node: Any) -> List[Tuple[str, bool]]:
        """
        Build procedure parameter declarations.
        args_decl -> args_decl , pidentifier
                  | args_decl , T pidentifier
                  | pidentifier
                  | T pidentifier
        """
        params = []
        is_array = False
        
        for child in node.children:
            if child.text == b'T':
                is_array = True
            elif child.type == 'pidentifier':
                params.append((child.text.decode('utf8'), is_array))
                is_array = False
                
        return params

    def build_main(self, node: Any) -> Tuple[List[Declaration], List[Command]]:
        """
        Build main program block.
        main -> PROGRAM IS declarations BEGIN commands END
              | PROGRAM IS BEGIN commands END
        """
        declarations = []
        commands = []
        
        for child in node.children:
            if child.type == 'declarations':
                declarations = self.build_declarations(child)
            elif child.type == 'commands':
                commands = self.build_commands(child)
                
        return declarations, commands

    def build_declarations(self, node: Any) -> List[Declaration]:
        """
        Build variable declarations.
        declarations -> declarations , pidentifier
                    | declarations , pidentifier [ num : num ]
                    | pidentifier
                    | pidentifier [ num : num ]
        """
        declarations = []

        def collect_declarations(node):
            decls = []
            # Handle recursive declaration structure
            if len(node.children) > 0:
                for child in node.children:
                    if child.type == 'declarations':
                        decls.extend(collect_declarations(child))
                    elif child.type == 'pidentifier':
                        # Create declaration for this identifier
                        current_decl = {
                            "name": child.text.decode('utf8'),
                            "start": None,
                            "end": None,
                            "location": self.get_location(child)
                        }
                        
                        # Look ahead for array bounds
                        idx = node.children.index(child)
                        remaining_children = node.children[idx+1:]
                        num_values = []
                        for next_child in remaining_children:
                            if next_child.type == 'num':
                                num_values.append(int(next_child.text.decode('utf8')))
                                if len(num_values) == 2:
                                    break
                        
                        if len(num_values) == 2:
                            current_decl["start"] = num_values[0]
                            current_decl["end"] = num_values[1]
                        
                        decls.append(self.create_declaration(current_decl))
                        
            return decls

        declarations = collect_declarations(node)
        return declarations

    def create_declaration(self, decl: dict) -> Declaration:
        """Helper to create a Declaration from collected info."""
        array_bounds = None
        if decl["start"] is not None and decl["end"] is not None:
            array_bounds = (decl["start"], decl["end"])
                
        return Declaration(
            location=decl["location"],
            name=decl["name"],
            array_bounds=array_bounds
        )


    def build_commands(self, node: Any) -> List[Command]:
        """
        Build command list maintaining source order.
        commands -> commands command
                | command
        """
        commands = []
        
        if node.type != 'commands':
            # Single command case
            commands.append(self.build_command(node))
            return commands

        # Visit command nodes in order of appearance
        def collect_commands(node):
            cmd_nodes = []
            # Find the deepest commands node first
            for child in reversed(node.children):
                if child.type == 'commands':
                    cmd_nodes.extend(collect_commands(child))
                elif child.type == 'command':
                    cmd_nodes.append(child)
            return cmd_nodes

        # Collect command nodes in correct order
        command_nodes = collect_commands(node)
        
        # Build commands in original source order
        for cmd_node in reversed(command_nodes):
            commands.append(self.build_command(cmd_node))
        
        return commands

    def build_command(self, node: Any) -> Command:
        """Build individual command based on its type."""
        first_child = next(child for child in node.children 
                         if child.type not in {';'})

        if first_child.type == 'identifier':
            return self.build_assignment(node)
        elif first_child.text == b'IF':
            return self.build_if_statement(node)
        elif first_child.text == b'WHILE':
            return self.build_while_loop(node)
        elif first_child.text == b'REPEAT':
            return self.build_repeat_loop(node)
        elif first_child.text == b'FOR':
            return self.build_for_loop(node)
        elif first_child.type == 'proc_call':
            return self.build_proc_call(first_child)
        elif first_child.text == b'READ':
            return self.build_read(node)
        elif first_child.text == b'WRITE':
            return self.build_write(node)
            
        raise ValueError(f"Unknown command type: {first_child.type}")

    def build_assignment(self, node: Any) -> Assignment:
        """Build assignment command: identifier := expression ;"""
        target = self.build_identifier(next(child for child in node.children 
                                         if child.type == 'identifier'))
        value = self.build_expression(next(child for child in node.children 
                                        if child.type == 'expression'))
        return Assignment(
            location=self.get_location(node),
            target=target,
            value=value
        )

    def build_if_statement(self, node: Any) -> IfStatement:
        """Build if statement with optional else block."""
        condition = None
        then_block = None
        else_block = None
        in_else = False
        
        for child in node.children:
            if child.type == 'condition':
                condition = self.build_condition(child)
            elif child.type == 'commands':
                if not then_block:
                    then_block = self.build_commands(child)
                else:
                    else_block = self.build_commands(child)
                    
        return IfStatement(
            location=self.get_location(node),
            condition=condition,
            then_block=then_block or [],
            else_block=else_block
        )

    def build_while_loop(self, node: Any) -> WhileLoop:
        """Build while loop: WHILE condition DO commands ENDWHILE"""
        condition = None
        body = None
        
        for child in node.children:
            if child.type == 'condition':
                condition = self.build_condition(child)
            elif child.type == 'commands':
                body = self.build_commands(child)
                
        return WhileLoop(
            location=self.get_location(node),
            condition=condition,
            body=body or []
        )

    def build_repeat_loop(self, node: Any) -> RepeatLoop:
        """Build repeat loop: REPEAT commands UNTIL condition ;"""
        body = None
        condition = None
        
        for child in node.children:
            if child.type == 'commands':
                body = self.build_commands(child)
            elif child.type == 'condition':
                condition = self.build_condition(child)
                
        return RepeatLoop(
            location=self.get_location(node),
            body=body or [],
            condition=condition
        )

    def build_for_loop(self, node: Any) -> ForLoop:
        """Build for loop with direction (TO/DOWNTO)."""
        iterator = None
        start = None
        end = None
        body = None
        downto = False
        
        for child in node.children:
            if child.type == 'pidentifier' and not iterator:
                iterator = child.text.decode('utf8')
            elif child.type == 'value':
                if not start:
                    start = self.build_value(child)
                else:
                    end = self.build_value(child)
            elif child.text == b'DOWNTO':
                downto = True
            elif child.type == 'commands':
                body = self.build_commands(child)
                
        return ForLoop(
            location=self.get_location(node),
            iterator=iterator,
            start=start,
            end=end,
            body=body or [],
            downto=downto
        )

    def build_proc_call(self, node: Any) -> ProcedureCall:
        """Build procedure call: proc_call -> pidentifier ( args )"""
        name = None
        arguments = []
        
        for child in node.children:
            if child.type == 'pidentifier' and not name:
                name = child.text.decode('utf8')
            elif child.type == 'args':
                arguments = self.build_args(child)
                
        return ProcedureCall(
            location=self.get_location(node),
            name=name,
            arguments=arguments
        )

    def build_read(self, node: Any) -> ReadCommand:
        """Build read command: READ identifier ;"""
        target = self.build_identifier(next(child for child in node.children 
                                         if child.type == 'identifier'))
        return ReadCommand(
            location=self.get_location(node),
            target=target
        )

    def build_write(self, node: Any) -> WriteCommand:
        """Build write command: WRITE value ;"""
        value = self.build_value(next(child for child in node.children 
                                    if child.type == 'value'))
        return WriteCommand(
            location=self.get_location(node),
            value=value
        )

    def build_expression(self, node: Any) -> Expression:
        """
        Build expression according to grammar:
        expression -> value
                   | value + value
                   | value - value
                   | value * value
                   | value / value
                   | value % value
        """
        if len(node.children) == 1:
            return self.build_value(node.children[0])
            
        # Binary operation
        left = self.build_value(node.children[0])
        operator = next(child.text.decode('utf8') 
                      for child in node.children 
                      if child.text in {b'+', b'-', b'*', b'/', b'%'})
        right = self.build_value(node.children[-1])
        
        return BinaryOp(
            location=self.get_location(node),
            left=left,
            operator=operator,
            right=right
        )

    def build_condition(self, node: Any) -> Condition:
        """
        Build condition according to grammar:
        condition -> value = value
                  | value != value
                  | value > value
                  | value < value
                  | value >= value
                  | value <= value
        """
        expressions = [self.build_expression(child) 
                      for child in node.children 
                      if child.type == 'expression']
        operator = next(child.text.decode('utf8') 
                      for child in node.children 
                      if child.text in {b'=', b'!=', b'>', b'<', b'>=', b'<='})
        
        return Condition(
            location=self.get_location(node),
            left=expressions[0],
            right=expressions[1],
            operator=operator
        )

    def build_value(self, node: Any) -> Value:
        """
        Build value according to grammar:
        value -> num
              | identifier
        """
        if node.type == 'value':
            node = node.children[0]
            
        if node.type == 'num':
            return Number(
                location=self.get_location(node),
                value=int(node.text.decode('utf8'))
            )
        elif node.type == 'identifier':
            return self.build_identifier(node)
            
        raise ValueError(f"Unknown value type: {node.type}")

            
    def build_identifier(self, node: Any) -> Identifier:
        """
        Build identifier according to grammar:
        identifier -> pidentifier
                   | pidentifier [ pidentifier ]
                   | pidentifier [ num ]
        """
        name = None
        array_index = None
        
        for child in node.children:
            if child.type == 'pidentifier' and not name:
                name = child.text.decode('utf8')
            elif child.type in ['pidentifier', 'num']:
                if child.type == 'num':
                    array_index = Number(
                        location=self.get_location(child),
                        value=int(child.text.decode('utf8'))
                    )
                else:
                    array_index = Identifier(
                        location=self.get_location(child),
                        name=child.text.decode('utf8')
                    )
                
        return Identifier(
            location=self.get_location(node),
            name=name,
            array_index=array_index
        )

    def build_args(self, node: Any) -> List[Expression]:
        """
        Build procedure call arguments according to grammar:
        args -> args , pidentifier
             | pidentifier
        """
        args = []
        for child in node.children:
            if child.type == 'pidentifier':
                args.append(Identifier(
                    location=self.get_location(child),
                    name=child.text.decode('utf8')
                ))
        return args

    def get_location(self, node: Any) -> Location:
        """Extract location information from a node."""
        return Location(
            line=node.start_point[0] + 1,
            column=node.start_point[1]
        )