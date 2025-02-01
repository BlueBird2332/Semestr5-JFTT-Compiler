from dataclasses import dataclass
from typing import List
from ..ast_nodes import *
from .IR_ops import *

@dataclass
class ProcInfo:
    begin_id: int
    arguments: List[str]
    return_var: Variable