from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple

from ..ast_nodes import *
from ..symbol_table import Symbol, SymbolTable


class LabelType(Enum):
    IF_ELSE = auto()
    IF_HELPER = auto()
    IF_END = auto()
    WHILE_START = auto()
    WHILE_END = auto()
    WHILE_HELPER = auto()
    FOR_START = auto()
    FOR_END = auto()
    REPEAT_START = auto()
    REPEAT_END = auto()
    PROC_START = auto()
    PROC_END = auto()
    MAIN_START = auto()


@dataclass
class Variable:
    """Represents a variable in intermediate representation"""

    name: str
    proc_name: Optional[str] = None
    is_temp: bool = False

    def __str__(self) -> str:
        if self.proc_name and not self.is_temp:
            return f"{self.proc_name}_{self.name}"
        return self.name

    def print_full(self) -> str:
        if self.proc_name:
            return f"{self.proc_name}_{self.name}"
        return self.name

    @staticmethod
    def create_temp(temp_name: str, proc_name: Optional[str] = None) -> "Variable":
        return Variable(name=temp_name, proc_name=proc_name, is_temp=True)

    @staticmethod
    def from_symbol(name: str, proc_name: Optional[str] = None) -> "Variable":
        return Variable(name=name, proc_name=proc_name)


class LabelManager:
    """Manages label creation and tracking"""

    def __init__(self):
        self.counter = 0
        self.label_types: Dict[int, Tuple[LabelType, str]] = {}

    def new_label(self, label_type: LabelType, comment: str = "") -> int:
        self.counter += 1
        self.label_types[self.counter] = (label_type, comment)
        return self.counter

    def get_label_info(self, label: int) -> Optional[Tuple[LabelType, str]]:
        return self.label_types.get(label)

    def get_comment(self, label: int) -> str:
        if info := self.label_types.get(label):
            return f"{info[0].name}: {info[1]}"
        return ""


@dataclass
class IRInstruction:
    """Base class for IR instructions"""

    comment: str

    # def __init__(self):
    #     self.comment = "


@dataclass
class IRHalt(IRInstruction):
    comment: str = ""

    def __str__(self) -> str:
        return f"halt"

    def print_full(self) -> str:
        return f"halt {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRAssign(IRInstruction):
    target: Variable
    value: str

    def __str__(self) -> str:
        return f"{self.target} := {self.value}"

    def print_full(self) -> str:
        return f"{self.target.print_full()} := {self.value} {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRHalf(IRInstruction):
    target: Variable

    def __str__(self) -> str:
        return f"{self.target} := {self.target} / 2"

    def print_full(self) -> str:
        return f"{self.target.print_full()} := {self.target} / 2 {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRBinaryOp(IRInstruction):
    target: Variable
    left: str
    right: str
    operator: str

    def __post_init__(self):
        if self.operator not in {"+", "-", "*", "/", "%", "[]"}:
            raise ValueError(f"Invalid operator: {self.operator}")

    def __str__(self) -> str:
        return f"{self.target} := {self.left} {self.operator} {self.right}"

    def print_full(self) -> str:
        return f"{self.target.print_full()} := {self.left} {self.operator} {self.right} {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRLabel(IRInstruction):
    label_id: int

    def __str__(self) -> str:
        return f"L{self.label_id}: {f'# {self.comment}' if self.comment else ''}"

    def print_full(self) -> str:
        return f"L{self.label_id}: {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRJump(IRInstruction):
    label: int

    def __str__(self) -> str:
        return f"goto L{self.label}"

    def print_full(self) -> str:
        return f"goto L{self.label} {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRCondJump(IRInstruction):
    left: str
    operator: str
    right: str
    label: int

    def __post_init__(self):
        if self.operator not in {"=", "!=", "<", ">", "<=", ">="}:
            raise ValueError(f"Invalid comparison operator: {self.operator}")

    def __str__(self) -> str:
        return f"if {self.left} {self.operator} {self.right} goto L{self.label}"

    def print_full(self) -> str:
        return f"if {self.left} {self.operator} {self.right} goto L{self.label} {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRProcCall(IRInstruction):
    name: str
    args: List[Variable] = field(default_factory=list)

    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"call {self.name}({args_str})"

    def print_full(self) -> str:
        args_str = ", ".join(arg.print_full() for arg in self.args)
        return f"call {self.name}({args_str}) {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRRead(IRInstruction):
    target: Variable

    def __str__(self) -> str:
        return f"read {self.target}"

    def print_full(self) -> str:
        return f"read {self.target.print_full()} {f'# {self.comment}' if self.comment else ''}"


@dataclass
class IRWrite(IRInstruction):
    value: str

    def __str__(self) -> str:
        return f"write {self.value}"

    def print_full(self) -> str:
        return f"write {self.value} {f'# {self.comment}' if self.comment else ''}"
