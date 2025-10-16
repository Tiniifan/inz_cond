import os
import sys
import base64

# Add root path to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Import from root
from tools.binary_reader import BinaryDataReader
from level_5.condition.logic import *

class Level5ConditionDecoder:
    def __init__(self, data):
        self.reader = BinaryDataReader(data)
        self.local_var_count = 0;

    @staticmethod
    def from_base64(encoded_str):
        decoded = base64.b64decode(encoded_str)
        parser = Level5ConditionDecoder(decoded)
        return parser._read_conditions()

    def _read_conditions(self):
        self.reader.to_seek(0x04)
        block_length = self.reader.read_byte()
        sub_count = self.reader.read_byte()
        variables = []
        conditions = []
        current_block = []
        
        while self.reader.offset < self.reader.length:
            keyword = self.reader.read_byte()
            
            if SymbolType.is_function(keyword):
                function = self._read_function()
                variables.append(function)
                
                # Special rule: if we have exactly 1 variable and it's GET_TEAM_BIT_FLAG, consume it immediately
                if len(variables) == 1 and isinstance(variables[0], Level5Function):
                    if variables[0].name == FunctionNameEnum.GET_TEAM_BIT_FLAG:
                        self._create_implicit_condition(variables, current_block)
                        
            elif SymbolType.is_local(keyword):
                local_variable = self._read_local_variable(f"variable{self.local_var_count}", keyword)
                variables.append(local_variable)
            elif ComparatorEnum.is_comparator(keyword):
                comparator = ComparatorEnum(keyword)
                
                if len(variables) >= 2:
                    # Determine comparator type based on variables
                    comparator_type = self._determine_comparator_type(variables[0], variables[1])
                    
                    # Create a new condition using the first two variables
                    new_condition = Level5Condition(variables[0], variables[1], comparator, comparator_type)
                    current_block.append(new_condition)
                    
                    # Consume the two variables used
                    variables.pop(0)
                    variables.pop(0)
                else:
                    print("Warning: not enough variables for comparator")
            elif keyword == 0x8F:
                # close current condition block and start a new one
                
                if current_block:
                    conditions.append(current_block)
                    current_block = []
        
        # If there is one variable left at the end, create a condition with == 1
        if len(variables) == 1:
            self._create_implicit_condition(variables, current_block)
        
        # Append last block if not empty
        if current_block:
            conditions.append(current_block)
        
        return conditions

    def _create_implicit_condition(self, variables, current_block):
        """Creates an implicit condition with == 1 for a remaining variable"""
        # Create a local int variable with the value 1
        implicit_var = Level5Variable(f"variable{self.local_var_count}", SymbolType.LOCAL_INT, 1)
        self.local_var_count += 1
        
        # Determine comparator type
        comparator_type = self._determine_comparator_type(variables[0], implicit_var)
        
        # Create the condition with the EQUAL operator
        new_condition = Level5Condition(variables[0], implicit_var, ComparatorEnum.EQUAL, comparator_type)
        current_block.append(new_condition)
        
        # Consume the variable used
        variables.pop(0)

    def _determine_comparator_type(self, left, right):
        """Determine the comparator type based on the operands"""
        # Check if left operand is a function
        if isinstance(left, Level5Function):
            return FunctionNameEnum.get_return_type(left.name.value)
        
        # Check if right operand is a function
        if isinstance(right, Level5Function):
            return FunctionNameEnum.get_return_type(right.name.value)
        
        # Default to int if both are variables
        return "int"

    def _read_local_variable(self, var_name, keyword):
        if SymbolType.is_local_int(keyword):
            var_value = self.reader.read_int32()
            lifetime = SymbolType.LOCAL_INT
        elif SymbolType.is_local_ident(keyword):
            var_value = self.reader.read_int32(order='little')
            lifetime = SymbolType.LOCAL_IDENT
        else:
            raise ValueError(f"Invalid keyword: {keyword}")
        
        self.local_var_count += 1
        
        return Level5Variable(var_name, lifetime, var_value)

    def _read_function(self):
        func_name_value = self.reader.read_int32()
        
        try:
            func_name = FunctionNameEnum(func_name_value)
        except ValueError:
            raise ValueError(f"Unknown function name: 0x{func_name_value:08X}")
        
        func_args = []
        
        func_arg_count = FunctionArgEnum.get_arg_count(func_name_value)
        
        if func_arg_count is None:
            raise ValueError(f"No argument count found for function: {func_name.name}")
        
        if func_arg_count == 0:
            self.reader.skip(3)
        else:
            self.reader.skip(7)
        
        for i in range(func_arg_count):
            arg_keyword = self.reader.read_byte()
            arg = self._read_local_variable(f"variable{self.local_var_count}", arg_keyword)
            func_args.append(arg)
        
        return Level5Function(func_name, func_args)