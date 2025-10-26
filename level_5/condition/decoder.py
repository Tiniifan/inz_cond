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
        self.local_var_count = 0

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

        end_offset = 0x06 + block_length

        while self.reader.offset < end_offset and self.reader.offset < self.reader.length:
            keyword = self.reader.read_byte()

            if SymbolType.is_function(keyword):
                function = self._read_function()
                variables.append(function)

                if len(variables) == 1 and (self.reader.offset >= end_offset or self.reader.offset >= self.reader.length):
                    self._create_implicit_condition(variables, current_block)

            elif SymbolType.is_local(keyword):
                local_variable = self._read_local_variable(f"variable{self.local_var_count}", keyword)
                variables.append(local_variable)

            elif OperatorEnum.is_comparator(keyword):
                operator = OperatorEnum(keyword)

                if len(variables) >= 2:
                    operator_type = self._determine_operator_type(variables[0], variables[1])
                    new_operation = Level5Operation(variables[0], variables[1], operator, operator_type)
                    current_block.append(new_operation)
                    variables.pop(0)
                    variables.pop(0)
                else:
                    print("Warning: not enough variables for operator")

            elif OperatorEnum.is_logical_operator(keyword):
                middle_operator = OperatorEnum(keyword)

                # Fusionner les 2 derniers blocs si possible
                if len(current_block) >= 2:
                    left_block = current_block.pop(-2)
                    right_block = current_block.pop(-1)

                    # Créer un Level5Operation logique avec AND/OR
                    merged_operation = Level5Operation(left_block, right_block, middle_operator)
                    conditions.append([merged_operation])
                else:
                    print("Warning: not enough conditions to apply logical operator")

        # Fin du bloc/fichier
        if variables:
            self._create_implicit_condition(variables, current_block)

        if current_block:
            conditions.append(current_block)

        # Fusion finale si exactement 2 conditions et pas d'AND/OR
        if len(conditions) == 2:
            merged_operation = Level5Operation(conditions[0], conditions[1], OperatorEnum.LOGICAL_AND)
            conditions = [[merged_operation]]

        return conditions


    def _create_implicit_condition(self, variables, current_block):
        """Creates an implicit condition with == 1 for a remaining variable"""
        # Create a local int variable with the value 1
        implicit_var = Level5Variable(f"variable{self.local_var_count}", SymbolType.LOCAL_INT, 1)
        self.local_var_count += 1
        
        # Determine operator type
        operator_type = self._determine_operator_type(variables[0], implicit_var)
        
        # Create the operation with the EQUAL operator
        new_operation = Level5Operation(variables[0], implicit_var, OperatorEnum.EQUAL, operator_type)
        current_block.append(new_operation)
        
        # Consume the variable used
        variables.pop(0)

    def _determine_operator_type(self, left, right):
        """Determine the operator type based on the operands"""
        # Check if left operand is a function
        if isinstance(left, Level5Function):
            return_type = FunctionRegistry.get_by_name(left.name).return_type
            if return_type:
                return return_type
        
        # Check if right operand is a function
        if isinstance(right, Level5Function):
            return_type = FunctionRegistry.get_by_name(right.name).return_type
            if return_type:
                return return_type
        
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
        func_hash = self.reader.read_int32()
        
        # Get function definition from registry
        func_def = FunctionRegistry.get_by_hash(func_hash)
        
        if func_def is None:
            raise ValueError(f"Unknown function hash: 0x{func_hash:08X}")
        
        func_args = []
        
        # Get argument count from function definition
        func_arg_count = func_def.arg_count
        
        # Skip bytes based on argument count
        if func_arg_count == 0:
            self.reader.skip(3)
        else:
            self.reader.skip(7)
        
        # Read function arguments
        for i in range(func_arg_count):
            arg_keyword = self.reader.read_byte()
            arg = self._read_local_variable(f"variable{self.local_var_count}", arg_keyword)
            func_args.append(arg)
        
        # Return function with name as string (from FunctionDefinition)
        return Level5Function(func_def.name, func_args)