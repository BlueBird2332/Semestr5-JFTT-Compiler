from dataclasses import dataclass

@dataclass()
class base_op:
    def __str__(self):
        return self.__class__.__name__

@dataclass
class GET(base_op):
    val: int
    
    def __str__(self):
        return f"GET {self.val}"
    
@dataclass
class HALF(base_op):
    def __str__(self):
        return "HALF"

@dataclass()
class PUT(base_op):
    val: int
    
    def __str__(self):
        return f"PUT {self.val}"
    
@dataclass()
class LOAD(base_op):
    val: int
    
    def __str__(self):
        return f"LOAD {self.val}"
    
@dataclass()
class STORE(base_op):
    val: int
    
    def __str__(self):
        return f"STORE {self.val}"
    
@dataclass()
class LOADI(base_op):
    val: int
    
    def __str__(self):
        return f"LOADI {self.val}"
    
@dataclass()
class STOREI(base_op):
    val: int
    
    def __str__(self):
        return f"STOREI {self.val}"
    
@dataclass()
class ADD(base_op):
    val: int
    
    def __str__(self):
        return f"ADD {self.val}"    

@dataclass()
class ADDI(base_op):
    val: int
    
    def __str__(self):
        return f"ADDI {self.val}"

@dataclass()
class SUB(base_op):
    val: int
    
    def __str__(self):
        return f"SUB {self.val}"
    
@dataclass()
class SUBI(base_op):
    val: int
    
    def __str__(self):
        return f"SUBI {self.val}"
    
@dataclass()
class SET(base_op):
    val: int
    
    def __str__(self):
        return f"SET {self.val}"
    
@dataclass()
class LABEL(base_op):
    label_id: int
    
    def __str__(self):
        return f"L{self.label_id}"
    
@dataclass()
class JUMP(base_op):
    val: int
    
    def __str__(self):
        return f"JUMP {self.val}"
    
@dataclass()   
class JUMPLABEL(base_op):
    label_id: int
        
    def __str__(self):
        return f"JUMP {self.label_id}"
    
@dataclass()
class JZERO(base_op):
    label_id: int
    
    def __str__(self):
        return f"JZERO {self.label_id}"
    
@dataclass()
class JZERO_LABEL(base_op):
    label_id: int
    
    def __str__(self):
        return f"JZERO {self.label_id}"
    
@dataclass()
class JPOS(base_op):
    label_id: int
    
    def __str__(self):
        return f"JPOS {self.label_id}"
    
@dataclass()
class JPOS_LABEL(base_op):
    label_id: int
    
    def __str__(self):
        return f"JPOS {self.label_id}"
    
@dataclass()
class JNEG(base_op):
    label_id: int
    
    def __str__(self):
        return f"JNEG {self.label_id}"

@dataclass()
class JNEG_LABEL(base_op):
    label_id: int
    
    def __str__(self):
        return f"JNEG {self.label_id}"
    
@dataclass()
class RETURN(base_op):
    val: int
    
    def __str__(self):
        return f"RTRN {self.val}"    

    
@dataclass()
class HALT(base_op):
    def __str__(self):
        return "HALT"

@dataclass()
class SET_HERE(base_op):
    offset: int
    def __str__(self):
        return "SET_HERE + " + str(self.offset)