from .vm_operators import *
from typing import List

def correct_labels(code: List[base_op]) -> List[str]:
    
    label_map = {} #id: line
    counter = 0
    new_code = []
    
    for item in code:
        print(f"{counter}: {item}")
        if isinstance(item, LABEL):
            label_map[item.label_id] = counter
        else:
            counter += 1
            new_code.append(item)
            
    print
    
    corrected_code = []
    
    for curr, item in enumerate(new_code):
        if isinstance(item, JUMPLABEL):
            offset = label_map[item.label_id] - curr
            corrected_code.append(str(JUMP(offset)))
            
        elif isinstance(item, JZERO_LABEL):
            offset = label_map[item.label_id] - curr
            corrected_code.append(str(JZERO(offset)))
        
        elif isinstance(item, JPOS_LABEL):
            offset = label_map[item.label_id] - curr
            corrected_code.append(str(JPOS(offset)))
            
        elif isinstance(item, JNEG_LABEL):
            offset = label_map[item.label_id] - curr
            corrected_code.append(str(JNEG(offset)))
        
        elif isinstance(item, LABEL):
            continue
        
        else:
            corrected_code.append(str(item))
            
    return corrected_code


# def test_label_correct():
#     code = [LABEL(1), 
#             JUMPLABEL(1),
#             JZERO_LABEL(1), 
#             JPOS_LABEL(1), 
#             JNEG_LABEL(1), 
#             LABEL(2), 
#             ADD(1), 
#             SUB(1),
#             JUMPLABEL(2),
#             LABEL(3),
#             JUMPLABEL(3)]
#     corrected = correct_labels(code)
    
#     assert corrected == [
#         JUMP(0),
#         JZERO(0),
#         JPOS(0),
#         JNEG(0),
#         ADD(1),
#         SUB(1),
#         JUMP(4),
#         JUMP(7)
#     ]
    
#     print("All tests passed!")
    
# if __name__ == "__main__":
#     test_label_correct()
            