from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Union


class TACOpType(Enum):
    """TAC operation types matching virtual machine instructions"""

    GET = auto()  # Read input to memory
    PUT = auto()  # Write from memory to output
    LOAD = auto()  # p[0] ← p[i]
    STORE = auto()  # p[i] ← p[0]
    LOADI = auto()  # p[0] ← p[p[i]]
    STOREI = auto()  # p[p[i]] ← p[0]
    ADD = auto()  # p[0] ← p[0] + p[i]
    SUB = auto()  # p[0] ← p[0] - p[i]
    HALF = auto()  # p[0] ← ⌊p[0]/2⌋
    JUMP = auto()  # Unconditional jump
    JPOS = auto()  # Jump if p[0] > 0
    JZERO = auto()  # Jump if p[0] = 0
    JNEG = auto()  # Jump if p[0] < 0
    SET = auto()  # p[0] ← x
    RTRN = auto()  # Return from procedure
    HALT = auto()  # End program


@dataclass
class TACOp:
    """Base class for all TAC operations"""

    op_type: TACOpType
    target: Optional[int] = None  # Memory location for operations (p[i])
    jump_offset: Optional[int] = None  # For jump instructions
    value: Optional[Union[int, str]] = None  # For immediate values or labels


@dataclass
class MemoryOp(TACOp):
    """Base class for memory operations (LOAD, STORE, GET, PUT)"""

    def __post_init__(self):
        if self.target is None:
            raise ValueError(
                f"Memory operation {self.op_type} requires a target address"
            )


@dataclass
class LoadOp(MemoryOp):
    """LOAD i: p[0] ← p[i]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.LOAD, target=address)


@dataclass
class StoreOp(MemoryOp):
    """STORE i: p[i] ← p[0]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.STORE, target=address)


@dataclass
class IndirectLoadOp(MemoryOp):
    """LOADI i: p[0] ← p[p[i]]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.LOADI, target=address)


@dataclass
class IndirectStoreOp(MemoryOp):
    """STOREI i: p[p[i]] ← p[0]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.STOREI, target=address)


@dataclass
class ArithmeticOp(TACOp):
    """Base class for arithmetic operations (ADD, SUB, HALF)"""

    def __post_init__(self):
        if self.op_type not in [TACOpType.ADD, TACOpType.SUB, TACOpType.HALF]:
            raise ValueError(f"Invalid arithmetic operation: {self.op_type}")


@dataclass
class AddOp(ArithmeticOp):
    """ADD i: p[0] ← p[0] + p[i]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.ADD, target=address)


@dataclass
class SubOp(ArithmeticOp):
    """SUB i: p[0] ← p[0] - p[i]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.SUB, target=address)


@dataclass
class HalfOp(ArithmeticOp):
    """HALF: p[0] ← ⌊p[0]/2⌋"""

    def __init__(self):
        super().__init__(TACOpType.HALF)


@dataclass
class Label(TACOp):
    """Represents a jump target label"""

    def __init__(self, name: str):
        super().__init__(TACOpType.LABEL)
        self.name = name
        self.position: Optional[int] = None  # Will be filled during code generation


@dataclass
class JumpOp(TACOp):
    """Base class for jump operations"""

    def __post_init__(self):
        if self.jump_offset is None:
            raise ValueError(f"Jump operation {self.op_type} requires an offset")


@dataclass
class UnconditionalJump(JumpOp):
    """JUMP j: k ← k + j"""

    def __init__(self, offset: int):
        super().__init__(TACOpType.JUMP, jump_offset=offset)


@dataclass
class ConditionalJump(JumpOp):
    """JPOS/JZERO/JNEG j: Conditional jumps based on p[0]"""

    def __init__(self, op_type: TACOpType, offset: int):
        if op_type not in [TACOpType.JPOS, TACOpType.JZERO, TACOpType.JNEG]:
            raise ValueError(f"Invalid conditional jump type: {op_type}")
        super().__init__(op_type, jump_offset=offset)


@dataclass
class IOOp(MemoryOp):
    """Base class for input/output operations"""

    pass


@dataclass
class ReadOp(IOOp):
    """GET i: Read input to p[i]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.GET, target=address)


@dataclass
class WriteOp(IOOp):
    """PUT i: Write p[i] to output"""

    def __init__(self, address: int):
        super().__init__(TACOpType.PUT, target=address)


@dataclass
class SetOp(TACOp):
    """SET x: p[0] ← x"""

    def __init__(self, value: int):
        super().__init__(TACOpType.SET, value=value)


@dataclass
class ReturnOp(TACOp):
    """RTRN i: k ← p[i]"""

    def __init__(self, address: int):
        super().__init__(TACOpType.RTRN, target=address)


@dataclass
class HaltOp(TACOp):
    """HALT: End program"""

    def __init__(self):
        super().__init__(TACOpType.HALT)


class ArrayManager:
    """Handles array operations using basic VM instructions"""

    def __init__(self):
        self.arrays: Dict[str, int] = {}  # Maps array names to base addresses

    def access_array(
        self, base_addr: int, index: Union[int, str], offset: int = 0
    ) -> List[TACOp]:
        """Generate instructions for array access p[base + index - offset]"""
        ops = []

        if isinstance(index, int):
            # Static index
            actual_addr = base_addr + index - offset
            ops.append(LoadOp(actual_addr))
        else:
            # Dynamic index, need to compute address
            ops.extend(
                [
                    LoadOp(index),  # Load index to p[0]
                    SetOp(offset),  # Load offset
                    SubOp(0),  # Subtract offset from index
                    SetOp(base_addr),  # Load base address
                    AddOp(0),  # Add base to (index - offset)
                    IndirectLoadOp(0),  # Load from computed address
                ]
            )

        return ops

    def store_array(
        self, base_addr: int, index: Union[int, str], value: int, offset: int = 0
    ) -> List[TACOp]:
        """Generate instructions for array store p[base + index - offset] ← value"""
        ops = []

        # First load value to accumulator
        ops.append(SetOp(value))

        if isinstance(index, int):
            # Static index
            actual_addr = base_addr + index - offset
            ops.append(StoreOp(actual_addr))
        else:
            # Dynamic index
            ops.extend(
                [
                    StoreOp(1),  # Temporarily store value
                    LoadOp(index),  # Load index to p[0]
                    SetOp(offset),  # Load offset
                    SubOp(0),  # Subtract offset from index
                    SetOp(base_addr),  # Load base address
                    AddOp(0),  # Add base to (index - offset)
                    StoreOp(2),  # Store computed address
                    LoadOp(1),  # Reload value
                    IndirectStoreOp(2),  # Store at computed address
                ]
            )

        return ops
