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