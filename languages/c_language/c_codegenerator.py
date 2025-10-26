import os
import sys

# Add root path to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from level_5.condition.logic import *

class CCodeGenerator:
    def __init__(self, conditions):
        self.conditions = conditions
        
    def generate(self):
        code_lines = []
        
        # Function declaration (C syntax)
        code_lines.append("bool condition()")
        code_lines.append("{")
        
        # Result variable initialization
        code_lines.append("    bool result = false;")
        
        # If there are no conditions, return true immediately
        if not self.conditions:
            code_lines.append("    result = true;")
            code_lines.append("    return result;")
            code_lines.append("}")
            return "\n".join(code_lines)
        
        # Generate condition blocks (separate if statements)
        self._generate_condition_blocks(code_lines)
        
        # Return statement
        code_lines.append("    return result;")
        code_lines.append("}")
        
        return "\n".join(code_lines)
    
    def _generate_condition_blocks(self, code_lines):
        """Generates nested if blocks for each condition list"""
        indent_level = 1
        
        for i, condition_block in enumerate(self.conditions):
            self._generate_single_if_block(condition_block, code_lines, indent_level)
            indent_level += 1
        
        # Set result = true in the innermost block
        indent = "    " * indent_level
        code_lines.append(f"{indent}result = true;")
        
        # Close all if blocks
        for i in range(len(self.conditions) - 1, -1, -1):
            indent = "    " * (i + 1)
            code_lines.append(f"{indent}}}")
    
    def _flatten_logical_and(self, operation):
        """
        Flatten nested LOGICAL_AND operations and lists into a single list of conditions.
        """
        # If it is a list, process each element
        if isinstance(operation, list):
            result = []
            for op in operation:
                result.extend(self._flatten_logical_and(op))
            return result
        
        # If it is not a Level5Operation, return it as it was
        if not isinstance(operation, Level5Operation):
            return [operation]
        
        # If it is a LOGICAL_AND, recursively flatten both sides
        if operation.operator_middle == OperatorEnum.LOGICAL_AND:
            left_parts = self._flatten_logical_and(operation.operator_left)
            right_parts = self._flatten_logical_and(operation.operator_right)
            return left_parts + right_parts
        
        # Otherwise, it's an simple operation.
        return [operation]

    def _generate_single_if_block(self, operation_list, code_lines, indent_level):
        """Generates a single if block with && conditions"""
        if not operation_list:
            return
        
        indent = "    " * indent_level
        
        # Flatten all operations (handle nested LOGICAL_AND and lists)
        flattened_operations = []
        for operation in operation_list:
            flattened_operations.extend(self._flatten_logical_and(operation))
        
        # Build the condition expression
        condition_parts = []
        for operation in flattened_operations:
            condition_str = self._format_operation(operation)
            condition_parts.append(condition_str)
        
        # Combine with &&
        full_condition = " && ".join(condition_parts)
        
        # Generate if statement (without closing brace)
        code_lines.append(f"{indent}if ({full_condition}) {{")
    
    def _format_operation(self, operation):
        """Formats an operation with boolean simplification"""
        left = self._format_operand(operation.operator_left)
        right = self._format_operand(operation.operator_right)
        operator = OperatorEnum.to_string(operation.operator_middle.value)
        
        # Simplification for boolean comparisons
        if operation.operator_type == "bool" and operation.operator_middle == OperatorEnum.EQUAL:
            # Check if right operand is a variable with value 1 or 0
            if isinstance(operation.operator_right, Level5Variable):
                if operation.operator_right.value == 1:
                    # Simplify "== 1" to just the left operand
                    return left
                elif operation.operator_right.value == 0:
                    # Simplify "== 0" to "!" + left operand
                    return f"!{left}"
            
            # Check if left operand is a variable with value 1 or 0
            if isinstance(operation.operator_left, Level5Variable):
                if operation.operator_left.value == 1:
                    # Simplify "1 ==" to just the right operand
                    return right
                elif operation.operator_left.value == 0:
                    # Simplify "0 ==" to "!" + right operand
                    return f"!{right}"
        
        # Default format: left operator right
        return f"{left} {operator} {right}"
    
    def _format_operand(self, operand):
        """Formats an operand for C code, recursively if it's a Level5Operation"""
        if isinstance(operand, Level5Variable):
            return str(operand.value)
        elif isinstance(operand, Level5Function):
            return self._format_function(operand)
        elif isinstance(operand, Level5Operation):
            # If the operand is a nested operation, format it as an expression in parentheses.
            return f"({self._format_operation(operand)})"
        else:
            return str(operand)
    
    def _format_function(self, function):
        """Formats a function call for C code"""
        # Get function name directly (it's already a string from FunctionRegistry)
        func_name_str = function.name
        
        # Format arguments
        args = []
        for arg in function.args:
            if isinstance(arg, Level5Variable):
                # Use the value directly instead of the variable name
                args.append(str(arg.value))
            else:
                args.append(str(arg))
        
        args_str = ", ".join(args)
        
        return f"{func_name_str}({args_str})"