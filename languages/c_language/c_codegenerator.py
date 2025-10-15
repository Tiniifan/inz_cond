import os
import sys

# Add root path to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from level_5.condition.logic import *

class CCodeGenerator:
    def __init__(self, conditions):
        """
        conditions: List of lists of Level5Condition
        Each inner list represents an if block
        Multiple conditions in same list = && combination
        """
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
        """Generates separate if blocks for each condition list"""
        for condition_block in self.conditions:
            self._generate_single_if_block(condition_block, code_lines)
    
    def _generate_single_if_block(self, condition_list, code_lines):
        """Generates a single if block with && conditions"""
        if not condition_list:
            return
        
        indent = "    "
        
        # Build the condition expression
        condition_parts = []
        for condition in condition_list:
            condition_str = self._format_condition(condition)
            condition_parts.append(condition_str)
        
        # Combine with &&
        full_condition = " && ".join(condition_parts)
        
        # Generate if statement
        code_lines.append(f"{indent}if ({full_condition}) {{")
        code_lines.append(f"{indent}    result = true;")
        code_lines.append(f"{indent}}}")
    
    def _format_condition(self, condition):
        """Formats a condition with boolean simplification"""
        left = self._format_operand(condition.operator_left)
        right = self._format_operand(condition.operator_right)
        comparator = ComparatorEnum.to_string(condition.comparator.value)
        
        # Simplification for boolean comparisons
        if condition.comparator_type == "bool" and condition.comparator == ComparatorEnum.EQUAL:
            # Check if right operand is a variable with value 1 or 0
            if isinstance(condition.operator_right, Level5Variable):
                if condition.operator_right.value == 1:
                    # Simplify "== 1" to just the left operand
                    return left
                elif condition.operator_right.value == 0:
                    # Simplify "== 0" to "!" + left operand
                    return f"!{left}"
            
            # Check if left operand is a variable with value 1 or 0
            if isinstance(condition.operator_left, Level5Variable):
                if condition.operator_left.value == 1:
                    # Simplify "1 ==" to just the right operand
                    return right
                elif condition.operator_left.value == 0:
                    # Simplify "0 ==" to "!" + right operand
                    return f"!{right}"
        
        # Default format: left comparator right
        return f"{left} {comparator} {right}"
    
    def _format_operand(self, operand):
        """Formats an operand for C code"""
        if isinstance(operand, Level5Variable):
            # Return the value directly instead of the variable name
            return str(operand.value)
        elif isinstance(operand, Level5Function):
            return self._format_function(operand)
        else:
            return str(operand)
    
    def _format_function(self, function):
        """Formats a function call for C code"""
        func_name_str = FunctionNameEnum.to_string(function.name.value)
        
        if not func_name_str:
            func_name_str = function.name.name
        
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