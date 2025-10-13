import os
import sys
import base64

tools_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tools"))
if tools_path not in sys.path:
    sys.path.insert(0, tools_path)

level5_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if level5_path not in sys.path:
    sys.path.insert(0, level5_path)

from binary_reader import BinaryDataReader
from binary_writer import BinaryDataWriter
from logic import Level5Variable, Level5Condition, Level5VariableType, Level5VariableValue, Level5Comparator

class Level5ConditionDecoder:
    def __init__(self, data):
        self.reader = BinaryDataReader(data)
        self.sub_index = 0
        self.has_extended_operator = False
        self.extended_operator_type = None
        self.extended_operator_skip_count = 0
        self.variable_counter = 0

    @staticmethod
    def from_base64(encoded_str):
        decoded = base64.b64decode(encoded_str)
        parser = Level5ConditionDecoder(decoded)
        return parser.read_conditions()

    def read_conditions(self):
        self.reader.to_seek(0x04)
        block_length = self.reader.read_byte()
        sub_count = self.reader.read_byte()
        
        variables = []
        conditions = []
        operators = []

        while self.sub_index < sub_count:
            sub_header = self.reader.read_byte()
                        
            if sub_header == 0x35:
                variables.append(self.read_memory_value())
            elif sub_header == 0x32:
                variables.append(self.read_custom_value())
            elif sub_header == 0x6f:
                operators.append(Level5Comparator.EqualInferior)
                self.sub_index += 1
            elif sub_header == 0x71:
                operators.append(Level5Comparator.EqualInferior)
                self.sub_index += 1

            if len(variables) >= 2:
                if len(operators) > 0:
                    compare_operator = operators.pop(0)
                else:
                    compare_operator = Level5Comparator.EqualSuperior
                
                if self.has_extended_operator:
                    if len(variables) == 3: 
                        left_var = variables.pop(0)
                        right_conditions = []
                        
                        while len(variables) > 0:
                            sub_var = variables.pop(0)
                            sub_condition = Level5Condition(
                                left_operator=sub_var,
                                right_operator=None,
                                compare_operator=compare_operator
                            )
                            right_conditions.append(sub_condition)
                        
                        condition = Level5Condition(
                            left_operator=left_var,
                            right_operator=right_conditions,
                            compare_operator=compare_operator
                        )
                        conditions.append(condition)
                        
                        self.has_extended_operator = False
                        self.extended_operator_type = None
                        self.extended_operator_skip_count = 0
                else:
                    left_var = variables.pop(0)
                    right_var = variables.pop(0)
                    
                    condition = Level5Condition(
                        left_operator=left_var,
                        right_operator=right_var,
                        compare_operator=compare_operator
                    )
                    conditions.append(condition)
        
        return conditions

    @staticmethod
    def get_variable_type_from_raw(memory_type_raw):
        if memory_type_raw == 0x000100:
            return Level5VariableType.SubPhase
        elif memory_type_raw == 0x000A01:
            return Level5VariableType.BitFlag
        elif memory_type_raw == 0x000602:
            return Level5VariableType.Boolean
        else:
            return Level5VariableType.Unknown

    def read_memory_value(self):
        sub_index_add = 3
        
        memory_raw = self.reader.read_int32_as_hex()
        
        if memory_raw == 0x98EE4B47:
            vvalue = Level5VariableValue.currentSubPhase
        elif memory_raw == 0x2A3D4543:
            vvalue = Level5VariableValue.currentBitFlag
        else:
            vvalue = Level5VariableValue.Unknown
    
        memory_type_raw = self.reader.read_hex3()
        
        extend_operator_test = self.reader.read_byte()
        if extend_operator_test == 0x28:
            sub_index_add = 2
            self.has_extended_operator = True
            self.extended_operator_type = self.reader.read_hex3()
            self.extended_operator_skip_count = 0
        else:
            self.reader.to_seek(self.reader.get_position() - 1)
        
        vtype = self.get_variable_type_from_raw(memory_type_raw)
        
        self.sub_index += sub_index_add

        return Level5Variable(vname=vvalue.value, vtype=vtype, vvalue=vvalue.value)

    def read_custom_value(self):
        vvalue = self.reader.read_int32()
        
        if self.extended_operator_type is not None and self.extended_operator_skip_count == 1:
            memory_type_raw = self.extended_operator_type
            vtype = self.get_variable_type_from_raw(memory_type_raw)
            self.extended_operator_type = None
            self.extended_operator_skip_count = 0
        else:
            vtype = Level5VariableType.Integer
            if self.extended_operator_type is not None:
                self.extended_operator_skip_count += 1

        vname = f"variable{self.variable_counter}"
        self.variable_counter += 1
        
        self.sub_index += 2

        return Level5Variable(vname=vname, vtype=vtype, vvalue=vvalue)