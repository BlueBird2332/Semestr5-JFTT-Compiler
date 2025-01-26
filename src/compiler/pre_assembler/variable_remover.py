from ..symbol_table import SymbolTable
from ..intermediate_rep.IR_ops import *
from ..intermediate_rep.IR_generator import IRGenerator
from collections import deque as stack




class VariableRemover:
    def __init__(self, ir: List[IRInstruction], symbol_table: SymbolTable):
        self.ir = ir
        self.symbol_table = SymbolTable()
        self.free_variables = stack()
        
        
        