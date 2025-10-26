class FunctionDefinition:
    def __init__(self, hash_value, name, arg_count, return_type):
        self.hash = hash_value
        self.name = name
        self.arg_count = arg_count
        self.return_type = return_type
    
    def __repr__(self):
        return f"<FunctionDef {self.name} hash=0x{self.hash:X} args={self.arg_count} returns={self.return_type}>"

class FunctionRegistry:
    _functions = {
        0x98EE4B47: FunctionDefinition(0x98EE4B47, "GetSubPhase", 0, "int"),
        0xB91936DA: FunctionDefinition(0xB91936DA, "GetPhase", 0, "int"),
        0xFBA3C513: FunctionDefinition(0xFBA3C513, "GetTRouteFlag", 1, "bool"),
        0x815B2EDD: FunctionDefinition(0x815B2EDD, "GetTempMapByteFlag", 1, "int"),
        0xBDF5EBF0: FunctionDefinition(0xBDF5EBF0, "GetTempByteFlag", 1, "int"),
        0x5C12B538: FunctionDefinition(0x5C12B538, "GetGlobalCharaMetFlag", 1, "bool"),
        0x2A3D4543: FunctionDefinition(0x2A3D4543, "GetGlobalBitFlag", 1, "bool"),
        0x32147A90: FunctionDefinition(0x32147A90, "GetTempMapBitFlag", 1, "bool"),
        0x9F3586B4: FunctionDefinition(0x9F3586B4, "GetTempBitFlag", 1, "bool"),
        0x7F48ECE3: FunctionDefinition(0x7F48ECE3, "GetGlobalTBoxFlag", 1, "bool"),
        0x8D7666D8: FunctionDefinition(0x8D7666D8, "IsHaveItem", 1, "bool"),
        0xA28E6300: FunctionDefinition(0xA28E6300, "CheckShopOpen", 1, "bool"),
        0xD8E3691F: FunctionDefinition(0xD8E3691F, "GetGameVersion", 0, "int"),
        0x2D588D5A: FunctionDefinition(0x2D588D5A, "GetFrameChapter", 0, "int"),
        0x0A527CE2: FunctionDefinition(0x0A527CE2, "GetChapter", 0, "int")
        # 0x4975C890: FunctionDefinition(0x4975C890, "DebugPrint", 0, "int") # Unused
    }
    
    _name_to_hash = {func.name: hash_val for hash_val, func in _functions.items()}
    
    @classmethod
    def get_by_hash(cls, hash_value):
        return cls._functions.get(hash_value)
    
    @classmethod
    def get_by_name(cls, name):
        hash_value = cls._name_to_hash.get(name)
        return cls._functions.get(hash_value) if hash_value else None
    
    @classmethod
    def get_name(cls, hash_value):
        func = cls.get_by_hash(hash_value)
        return func.name if func else None
    
    @classmethod
    def get_arg_count(cls, hash_value):
        func = cls.get_by_hash(hash_value)
        return func.arg_count if func else None
    
    @classmethod
    def get_return_type(cls, hash_value):
        func = cls.get_by_hash(hash_value)
        return func.return_type if func else None
    
    @classmethod
    def is_valid(cls, hash_value):
        return hash_value in cls._functions
    
    @classmethod
    def register(cls, hash_value, name, arg_count, return_type):
        func_def = FunctionDefinition(hash_value, name, arg_count, return_type)
        cls._functions[hash_value] = func_def
        cls._name_to_hash[name] = hash_value
        return func_def