from enum import Enum

class SymbolType(Enum):
    FUNCTION = 0x35
    LOCAL_INT = 0x32
    LOCAL_IDENT = 0x34
    
    @classmethod
    def is_valid(cls, value):
        return any(value == item.value for item in cls)
    
    @classmethod
    def is_function(cls, value):
        return value == cls.FUNCTION.value
    
    @classmethod
    def is_local(cls, value):
        return value in (cls.LOCAL_INT.value, cls.LOCAL_IDENT.value)
    
    @classmethod
    def is_local_int(cls, value):
        return value == cls.LOCAL_INT.value
    
    @classmethod
    def is_local_ident(cls, value):
        return value == cls.LOCAL_IDENT.value

class FunctionNameEnum(Enum):
    GET_GAME_SUB_PHASE = 0x98EE4B47
    GET_GLOBAL_BIT_FLAG = 0x2A3D4543
    GET_TEAM_BIT_FLAG = 0xFBA3C513
    IS_HAVE_ITEM = 0x8D7666D8
    
    @classmethod
    def to_string(cls, value):
        mapping = {
            cls.GET_GAME_SUB_PHASE.value: "getGameSubPhase",
            cls.GET_GLOBAL_BIT_FLAG.value: "getGlobalBitFlag",
            cls.GET_TEAM_BIT_FLAG.value: "getTeamBitFlag",
            cls.IS_HAVE_ITEM.value: "isHaveItem"
        }
        
        return mapping.get(value, None)
    
    @classmethod
    def get_return_type(cls, value):
        mapping = {
            cls.GET_GAME_SUB_PHASE.value: "int",
            cls.GET_GLOBAL_BIT_FLAG.value: "bool",
            cls.GET_TEAM_BIT_FLAG.value: "bool",
            cls.IS_HAVE_ITEM.value: "bool"
        }
        
        return mapping.get(value, None)

class FunctionArgEnum(Enum):
    GET_GAME_SUB_PHASE = 0
    GET_GLOBAL_BIT_FLAG = 1
    GET_TEAM_BIT_FLAG = 1
    IS_HAVE_ITEM = 1
    
    @classmethod
    def get_arg_count(cls, function_value):
        mapping = {
            FunctionNameEnum.GET_GAME_SUB_PHASE.value: cls.GET_GAME_SUB_PHASE.value,
            FunctionNameEnum.GET_GLOBAL_BIT_FLAG.value: cls.GET_GLOBAL_BIT_FLAG.value,
            FunctionNameEnum.GET_TEAM_BIT_FLAG.value: cls.GET_TEAM_BIT_FLAG.value,
            FunctionNameEnum.IS_HAVE_ITEM.value: cls.IS_HAVE_ITEM.value
        }
        
        return mapping.get(function_value, None)

class ComparatorEnum(Enum):
    LESS_THAN = 0x6E
    GREATER_THAN = 0x6F
    UNK_COMPARATOR_3 = 0x70
    GREATER_THAN_OR_EQUAL = 0x71
    EQUAL = 0x78
    UNK_COMPARATOR_6 = 0x79
    
    @classmethod
    def is_comparator(cls, value):
        return value in (item.value for item in cls)
    
    @classmethod
    def to_string(cls, value):
        mapping = {
            cls.LESS_THAN.value: "<",
            cls.GREATER_THAN.value: ">",
            cls.UNK_COMPARATOR_3.value: "??",
            cls.GREATER_THAN_OR_EQUAL.value: ">=",
            cls.EQUAL.value: "==",
            cls.UNK_COMPARATOR_6.value: "??",
        }
        
        return mapping.get(value, None)

class Level5Variable:
    def __init__(self, name, lifetime, value):
        self._name = name
        self._lifetime = lifetime
        self._value = value
    
    @property
    def name(self):
        return self._name
    
    @property
    def lifetime(self):
        return self._lifetime
    
    @property
    def value(self):
        return self._value
    
    def __repr__(self):
        return (f"<Level5Variable name={self.name} "
                f"lifetime={self.lifetime.name} "
                f"value={self.value}>")

class Level5Function:
    def __init__(self, name, args):
        self._name = name
        self._args = args
    
    @property
    def name(self):
        return self._name
    
    @property
    def args(self):
        return self._args
    
    def __repr__(self):
        return (f"<Level5Function name={self.name} "
                f"args={self.args}>")

class Level5Condition:
    def __init__(self, operator_left, operator_right, comparator, comparator_type="int"):
        self._operator_left = operator_left
        self._operator_right = operator_right
        self._comparator = comparator
        self._comparator_type = comparator_type
    
    @property
    def operator_left(self):
        return self._operator_left
    
    @property
    def operator_right(self):
        return self._operator_right
    
    @property
    def comparator(self):
        return self._comparator
    
    @property
    def comparator_type(self):
        return self._comparator_type
    
    def __repr__(self):
        return (f"<Level5Condition "
                f"operator_left={self.operator_left} "
                f"operator_right={self.operator_right} "
                f"comparator={self.comparator.name} "
                f"comparator_type={self.comparator_type}>")