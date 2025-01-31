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
    """Enhanced variable representation for IR"""
    name: str
    proc_name: Optional[str] = None
    # Variable type flags
    is_temp: bool = False
    is_const: bool = False
    const_value: Optional[int] = None
    is_array: bool = False
    is_pointer: bool = False
    
    # Array info
    array_start: Optional[int] = None
    array_size: Optional[int] = None  # end - start + 1
    
    
    def __str__(self) -> str:
        """String representation for IR code generation"""

        return self.name
    
    def print_full(self) -> str:
        """Detailed string representation for debugging"""
        parts = []
        if self.is_const:
            parts.append("const")
        if self.const_value is not None:
            parts.append(f"value={self.const_value}")
        if self.is_temp:
            parts.append("temp")
        if self.is_array:
            if self.is_pointer:
                parts.append(f"array[{self.name}]")
            else:
                parts.append(f"array[{self.array_start}:{self.array_start + self.array_size - 1}]")
        if self.is_pointer:
            parts.append("pointer")
            
        return f"{str(self)} ({', '.join(parts)})"
    
    @staticmethod
    def create_temp(temp_name: str, proc_name: Optional[str] = None, is_pointer: Optional[bool] = False) -> 'Variable':
        return Variable(
            name=temp_name,
            proc_name=proc_name,
            is_temp=True,
            is_pointer=is_pointer
        )
    
    @staticmethod
    def create_array(name: str, start: int, size: int, proc_name: Optional[str] = None) -> 'Variable':
        return Variable(
            name=name,
            proc_name=proc_name,
            is_array=True,
            array_start=start,
            array_size=size,
            # is_pointer=True
        )
        
    @staticmethod
    def create_param(name: str, proc_name: str) -> 'Variable':
        return Variable(name=name, proc_name=proc_name, is_pointer=True)
    
    @staticmethod
    def from_number(value: str) -> 'Variable':
        """Create constant variable"""
        name = str(value)
        return Variable(name=name, is_const=True, const_value=int(value))
    
    
    
def wrap_by_value(var: Variable) -> Variable:
    if isinstance(var, BY_VALUE):
        return var
    # elif isinstance(var, BY_REFERENCE):
    #     raise ValueError(f"Variable {var} is already a reference")
    else:
        return BY_VALUE(var)
    
def wrap_by_reference(var: Variable) -> Variable:
    if isinstance(var, BY_REFERENCE):
        return var
    # elif isinstance(var, BY_VALUE):
        # raise ValueError(f"Variable {var} is already a value")
    else:
        return BY_REFERENCE(var)
    
@dataclass
class BY_VALUE(Variable):
    """Enhanced variable representation for IR"""
    
    def __init__(self, var: Variable):
        # Copy all attributes from the wrapped variable
        super().__init__(
            name=var.name,
            proc_name=var.proc_name,
            is_temp=var.is_temp,
            is_const=var.is_const,
            const_value=var.const_value,
            is_array=var.is_array,
            is_pointer=var.is_pointer,
            array_start=var.array_start,
            array_size=var.array_size
        )
    
    def __str__(self):
        return f"BY_VALUE {super().__str__()}"
    
    def print_full(self):
        return f"BY_VALUE {super().print_full()}"
    
@dataclass
class BY_REFERENCE(Variable):
    def __init__(self, var: Variable):
        # Copy all attributes from the wrapped variable
        super().__init__(
            name=var.name,
            proc_name=var.proc_name,
            is_temp=var.is_temp,
            is_const=var.is_const,
            const_value=var.const_value,
            is_array=var.is_array,
            is_pointer=var.is_pointer,
            array_start=var.array_start,
            array_size=var.array_size
        )
    
    def __str__(self):
        return f"BY REFERENCE{super().__str__()}"
    
    def print_full(self):
        return f"BY REFERENCE{super().print_full()}"



    
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
    value: Variable
    
    def __str__(self) -> str:
        return f"{self.target} := {self.value}"
    
    def print_full(self) -> str:
        return f"{self.target.print_full()} := {self.value.print_full()} {f'# {self.comment}' if self.comment else ''}"

@dataclass
class IRHalf(IRInstruction):
    target: Variable
    
    def __str__(self) -> str:
        return f"Half {self.target}"
    
    def print_full(self) -> str:
        return f"{self.target.print_full()} := {self.target} / 2 {f'# {self.comment}' if self.comment else ''}"

@dataclass
class IRBinaryOp(IRInstruction):
    target: Variable
    left: Variable
    right: Variable
    operator: str
    dereference_target: bool = True
    
    def __post_init__(self):
        if self.operator not in {'+', '-', '*', '/', '%', '[]'}:
            raise ValueError(f"Invalid operator: {self.operator}")
    
    def __str__(self) -> str:
        return f"{self.target} := {self.left} {self.operator} {self.right}"
    
    def print_full(self) -> str:
        comment_part = f"# {self.comment}" if self.comment else ''
        deref_part = f"dereference_target {self.dereference_target}" if self.operator == '[]' else ''
        return (f"{self.target.print_full()} := {self.left.print_full()} "
                f"{self.operator} {self.right.print_full()} {comment_part} {deref_part}")

@dataclass
class IRLabel(IRInstruction):
    label_id: int
    label_type: LabelType
    procedure: Optional[str] = None
    
    def __str__(self) -> str:
        return f"L{self.label_id}: {self.label_type.name} + {self.procedure}"
    
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
    left: Variable
    operator: str
    right: Variable
    label: int
    
    def __post_init__(self):
        if self.operator not in {'=', '!=', '<', '>', '<=', '>='}:
            raise ValueError(f"Invalid comparison operator: {self.operator}")
    
    def __str__(self) -> str:
        return f"if {self.left} {self.operator} {self.right} goto L{self.label}"
    
    def print_full(self) -> str:
        return f"if {self.left.print_full()} {self.operator} {self.right.print_full()} goto L{self.label} {f'# {self.comment}' if self.comment else ''}"

@dataclass
class IRProcCall(IRInstruction):
    name: str
    args: List[Variable] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(str(arg) for arg in self.args)
        return f"call {self.name}({args_str})"
    
    def print_full(self) -> str:
        args_str = ', '.join(arg.print_full() for arg in self.args)
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
    value: Variable
    
    def __str__(self) -> str:
        return f"write {self.value}"
    
    def print_full(self) -> str:
        return f"write {self.value.print_full()} {f'# {self.comment}' if self.comment else ''}"
    
    
@dataclass
class IRReturn(IRInstruction):
    
    return_variable: Variable
    
    def __str__(self) -> str:
        return f"return {self.return_variable}"
    
    def print_full(self) -> str: 
        return f"return {self.return_variable.print_full()} {f'# {self.comment}' if self.comment else ''}"
    

    
@dataclass
class IRArrayRead(IRInstruction):
    """Read value from array at given index"""
    target: Variable  # Where to store the read value
    array: Variable   # Array variable
    index: Variable   # Index to read from
    
    def __str__(self) -> str:
        return f"{self.target} := {self.array}[{self.index}]"
    
    def print_full(self) -> str:
        return f"{self.target.print_full()} := {self.array.print_full()}[{self.index.print_full()}] {f'# {self.comment}' if self.comment else ''}"

@dataclass 
class IRArrayWrite(IRInstruction):
    """Write value to array at given index"""
    array: Variable   # Array variable
    index: Variable   # Index to write to
    value: Variable   # Value to write
    
    def __str__(self) -> str:
        return f"{self.array}[{self.index}] := {self.value}"
    
    def print_full(self) -> str:
        return f"{self.array.print_full()}[{self.index.print_full()}] := {self.value.print_full()} {f'# {self.comment}' if self.comment else ''}"