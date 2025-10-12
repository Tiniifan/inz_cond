from enum import Enum

class Level5VariableType(Enum):
    SubPhase = "SubPhase"
    BitFlag = "BitFlag"
    Boolean = "Boolean"
    Integer = "Integer"
    Unknown = "Unknown"

class Level5VariableValue(Enum):
    currentSubPhase = "currentSubPhase"
    currentBitFlag = "currentBitFlag"
    Unknown = "Unknown"

class Level5Comparator(Enum):
    Equal = "=="
    EqualSuperior = ">="
    EqualLower = "<="
    EqualInferior = "<"
    
class Level5Variable:
    def __init__(self, vname, vtype=Level5VariableType.Unknown, vvalue=None):
        self.vname = vname
        self.vtype = vtype
        self.vvalue = vvalue if vvalue is not None else Level5VariableValue.Unknown

    def __repr__(self):
        return f"Level5Variable(name={self.vname}, type={self.vtype.value}, value={self.vvalue})"    
        
class Level5Condition:
    def __init__(self, left_operator=None, right_operator=None, compare_operator=None):
        self.left_operator = left_operator
        self.right_operator = right_operator
        self.compare_operator = compare_operator

    def __repr__(self):
        return (
            f"Level5Condition(left={self.left_operator}, "
            f"right={self.right_operator}, "
            f"compare={self.compare_operator})"
        )        