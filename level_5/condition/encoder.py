import os
import sys
import base64

# Add root path to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Import from root
from tools.binary_writer import BinaryDataWriter
from level_5.condition.logic import *

class Level5ConditionEncoder:
    def __init__(self, conditions):
        self.conditions = conditions
        self.writer = BinaryDataWriter()

    @staticmethod
    def to_base64(conditions):
        encoder = Level5ConditionEncoder(conditions)
        encoded_data = encoder._write_conditions()
        return base64.b64encode(encoded_data).decode('utf-8')

    def _write_conditions(self):
        # Write header (4 bytes of zeros)
        self.writer.write_int32(0)
        
        # Write block_length placeholder (will be updated later)
        block_length_offset = self.writer.offset
        self.writer.write_byte(0x00)
        
        # If you put 0x63, it's work fine in game
        sub_count = 0x63
        self.writer.write_byte(sub_count)
        
        # Write each condition block
        for i, condition_block in enumerate(self.conditions):
            for operation in condition_block:
                self._write_operation(operation)
            
            # Write block separator (LOGICAL_AND) after each block except the last
            if i < len(self.conditions) - 1:
                self.writer.write_byte(OperatorEnum.LOGICAL_AND.value)
        
        # Calculate actual block_length (file size - 5)
        block_length = len(self.writer.data) - 5
        
        # Go back and write the correct block_length
        current_offset = self.writer.offset
        self.writer.to_seek(block_length_offset)
        self.writer.write_byte(block_length)
        self.writer.to_seek(current_offset)
        
        return self.writer.data

    def _count_operations(self, block):
        """
        Counts the total number of operations recursively.
        Each operation (even nested ones) counts as 3 elements (left, right, operator).
        """
        count = 0
        for operation in block:
            count += self._count_single_operation(operation)
        return count

    def _count_single_operation(self, operation):
        """
        Recursively counts operations in a single Level5Operation.
        Returns the count multiplied by 3 (left, right, operator).
        """
        if not isinstance(operation, Level5Operation):
            return 0
        
        count = 3  # Current operation: left, right, operator
        
        # Count nested operations in left operand
        if isinstance(operation.operator_left, Level5Operation):
            count += self._count_single_operation(operation.operator_left)
        
        # Count nested operations in right operand
        if isinstance(operation.operator_right, Level5Operation):
            count += self._count_single_operation(operation.operator_right)
        
        return count

    def _write_operation(self, operation):
        """
        Writes a single operation recursively.
        Order: write left operand, write right operand, write operator.
        """
        # Write left operand (can be a nested operation)
        self._write_operand(operation.operator_left)
        
        # Write right operand (can be a nested operation)
        self._write_operand(operation.operator_right)
        
        # Write operator at the end
        self.writer.write_byte(operation.operator_middle.value)

    def _write_operand(self, operand):
        """
        Writes an operand (function, variable, or nested operation).
        """
        if isinstance(operand, Level5Operation):
            # Nested operation: write it recursively
            self._write_operation(operand)
        elif isinstance(operand, Level5Function):
            self._write_function(operand)
        elif isinstance(operand, Level5Variable):
            self._write_variable(operand)
        else:
            raise ValueError(f"Unknown operand type: {type(operand)}")

    def _write_function(self, function):
        """Writes a function"""
        # Write function keyword
        self.writer.write_byte(SymbolType.FUNCTION.value)
        
        # Get function definition from registry
        func_def = FunctionRegistry.get_by_name(function.name)
        
        if func_def is None:
            raise ValueError(f"Unknown function name: {function.name}")
        
        # Write function hash
        self.writer.write_int32(func_def.hash)
        
        # Get argument count
        func_arg_count = func_def.arg_count
        
        # Write the 3 bytes after function hash
        if func_arg_count == 0:
            # For functions with 0 arguments: 00 01 00
            self.writer.write_byte(0x00)
            self.writer.write_byte(0x01)
            self.writer.write_byte(0x00)
        else:
            # For functions with arguments: 00 0A 01 28 00 06 02
            self.writer.write_byte(0x00)
            self.writer.write_byte(0x0A)
            self.writer.write_byte(0x01)
            self.writer.write_byte(0x28)
            self.writer.write_byte(0x00)
            self.writer.write_byte(0x06)
            self.writer.write_byte(0x02)
        
        # Write function arguments
        for arg in function.args:
            if isinstance(arg, Level5Variable):
                self._write_variable(arg)
            else:
                raise ValueError(f"Invalid argument type: {type(arg)}")

    def _write_variable(self, variable):
        """Writes a variable"""
        # Write variable keyword based on lifetime
        self.writer.write_byte(variable.lifetime.value)
        
        # Write variable value with appropriate byte order
        if variable.lifetime == SymbolType.LOCAL_INT:
            self.writer.write_int32(variable.value)
        elif variable.lifetime == SymbolType.LOCAL_IDENT:
            self.writer.write_int32(variable.value, order='little')
        else:
            raise ValueError(f"Invalid variable lifetime: {variable.lifetime}")