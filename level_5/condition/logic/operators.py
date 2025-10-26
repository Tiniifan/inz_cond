# Thanks to n123 from https://github.com/n123git/yw-cond

from enum import Enum

class OperatorEnum(Enum):
    # Unary
    INCREMENT = 0x46          # ++
    DECREMENT = 0x47          # --
    BITWISE_NOT = 0x50        # ~
    LOGICAL_NOT = 0x51        # !
    
    # Arithmetic
    MULTIPLY = 0x5A           # *
    DIVIDE = 0x5B             # /
    MODULUS = 0x5C            # %
    ADD = 0x5D                # +
    SUBTRACT = 0x5E           # -
    
    # Bitwise shift
    LEFT_SHIFT = 0x64         # <<
    RIGHT_SHIFT = 0x65        # >>
    
    # Comparison
    LESS_THAN = 0x6E          # <
    LESS_OR_EQUAL = 0x6F      # <=
    GREATER_THAN = 0x70       # >
    GREATER_OR_EQUAL = 0x71   # >=
    EQUAL = 0x78              # ==
    NOT_EQUAL = 0x79          # !=
    
    # Bitwise logic
    BITWISE_AND = 0x82        # &
    BITWISE_OR = 0x83         # |
    BITWISE_XOR = 0x84        # ^
    
    LOGICAL_AND = 0x8F        # &&
    LOGICAL_OR = 0x90         # ||

    @classmethod
    def is_comparator(cls, value):
        return value in (
            cls.LESS_THAN.value,
            cls.LESS_OR_EQUAL.value,
            cls.GREATER_THAN.value,
            cls.GREATER_OR_EQUAL.value,
            cls.EQUAL.value,
            cls.NOT_EQUAL.value,
        )
    
    @classmethod
    def to_string(cls, value):
        mapping = {
            cls.INCREMENT.value: "++",
            cls.DECREMENT.value: "--",
            cls.BITWISE_NOT.value: "~",
            cls.LOGICAL_NOT.value: "!",
            cls.MULTIPLY.value: "*",
            cls.DIVIDE.value: "/",
            cls.MODULUS.value: "%",
            cls.ADD.value: "+",
            cls.SUBTRACT.value: "-",
            cls.LEFT_SHIFT.value: "<<",
            cls.RIGHT_SHIFT.value: ">>",
            cls.LESS_THAN.value: "<",
            cls.LESS_OR_EQUAL.value: "<=",
            cls.GREATER_THAN.value: ">",
            cls.GREATER_OR_EQUAL.value: ">=",
            cls.EQUAL.value: "==",
            cls.NOT_EQUAL.value: "!=",
            cls.BITWISE_AND.value: "&",
            cls.BITWISE_OR.value: "|",
            cls.BITWISE_XOR.value: "^",
            cls.LOGICAL_AND.value: "&&",
            cls.LOGICAL_OR.value: "||",
        }
        
        return mapping.get(value, None)
    
    @classmethod
    def from_string(cls, symbol):
        mapping = {
            "++": cls.INCREMENT,
            "--": cls.DECREMENT,
            "~": cls.BITWISE_NOT,
            "!": cls.LOGICAL_NOT,
            "*": cls.MULTIPLY,
            "/": cls.DIVIDE,
            "%": cls.MODULUS,
            "+": cls.ADD,
            "-": cls.SUBTRACT,
            "<<": cls.LEFT_SHIFT,
            ">>": cls.RIGHT_SHIFT,
            "<": cls.LESS_THAN,
            "<=": cls.LESS_OR_EQUAL,
            ">": cls.GREATER_THAN,
            ">=": cls.GREATER_OR_EQUAL,
            "==": cls.EQUAL,
            "!=": cls.NOT_EQUAL,
            "&": cls.BITWISE_AND,
            "|": cls.BITWISE_OR,
            "^": cls.BITWISE_XOR,
            "&&": cls.LOGICAL_AND,
            "||": cls.LOGICAL_OR,
        }
        
        return mapping.get(symbol, None)

    @classmethod
    def is_logical_operator(cls, value):
        return value in (cls.LOGICAL_AND.value, cls.LOGICAL_OR.value)

    @classmethod
    def is_bitwise_operator(cls, value):
        return value in (
            cls.BITWISE_AND.value,
            cls.BITWISE_OR.value,
            cls.BITWISE_XOR.value,
            cls.BITWISE_NOT.value,
        )

    @classmethod
    def is_arithmetic_operator(cls, value):
        return value in (
            cls.ADD.value,
            cls.SUBTRACT.value,
            cls.MULTIPLY.value,
            cls.DIVIDE.value,
            cls.MODULUS.value,
        )

    @classmethod
    def is_unary_operator(cls, value):
        return value in (
            cls.INCREMENT.value,
            cls.DECREMENT.value,
            cls.LOGICAL_NOT.value,
            cls.BITWISE_NOT.value,
        )