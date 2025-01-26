# src/compiler/ast_nodes.py
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Location:
    line: int
    column: int


@dataclass
class ASTNode:
    location: Location


@dataclass
class Value(ASTNode):
    pass


@dataclass
class Number(Value):
    value: int


@dataclass
class Identifier(Value):
    name: str
    array_index: Optional["Expression"] = None


@dataclass
class Expression(ASTNode):
    pass


@dataclass
class BinaryOp(Expression):
    left: Value
    operator: str
    right: Value


@dataclass
class Condition(ASTNode):
    left: Expression
    operator: str
    right: Expression


@dataclass
class Command(ASTNode):
    pass


@dataclass
class Assignment(Command):
    target: Identifier
    value: Expression


@dataclass
class IfStatement(Command):
    condition: Condition
    then_block: List[Command]
    else_block: Optional[List[Command]]


@dataclass
class WhileLoop(Command):
    condition: Condition
    body: List[Command]


@dataclass
class RepeatLoop(Command):
    body: List[Command]
    condition: Condition


@dataclass
class ForLoop(Command):
    iterator: str
    start: Value
    end: Value
    body: List[Command]
    downto: bool


@dataclass
class ProcedureCall(Command):
    name: str
    arguments: List[Expression]


@dataclass
class ReadCommand(Command):
    target: Identifier


@dataclass
class WriteCommand(Command):
    value: Value


@dataclass
class Declaration(ASTNode):
    name: str
    array_bounds: Optional[tuple[int, int]] = None


@dataclass
class ProcHead(ASTNode):
    name: str
    parameters: List[tuple[str, bool]]  # (name, is_array)


@dataclass
class Procedure(ASTNode):
    name: str
    parameters: List[tuple[str, bool]]
    declarations: List[Declaration]
    commands: List[Command]


@dataclass
class Program(ASTNode):
    procedures: List[Procedure]
    declarations: List[Declaration]
    commands: List[Command]
