import os
import sys

level5_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../level5"))
if level5_path not in sys.path:
    sys.path.insert(0, level5_path)

from logic import *

class SquirrelCodeGenerator:
    def __init__(self, conditions):
        self.conditions = conditions
        self.declared_variables = set()
    
    def generate(self):
        code_lines = []
        
        # Function declaration
        code_lines.append("function condition()")
        code_lines.append("{")
        
        # Result variable initialization
        code_lines.append("    local result = false;")
        
        # If there are no conditions, return true immediately
        if not self.conditions:
            code_lines.append("    result = true;")
            code_lines.append("    return result;")
            code_lines.append("}")
            return "\n".join(code_lines)
        
        # Declare all necessary variables
        self._declare_variables(code_lines)
        
        # Generate conditions
        self._generate_recursive(self.conditions, 0, code_lines, indent=1)
        
        # Return statement
        code_lines.append("    return result;")
        code_lines.append("}")
        
        return "\n".join(code_lines)
    
    def _declare_variables(self, code_lines):
        """Declares all variables used in conditions"""
        for condition in self.conditions:
            # Check left operand
            self._declare_if_needed(condition.left_operator, code_lines)
            
            # Check right operand
            if isinstance(condition.right_operator, list):
                # If it's a list of conditions (BitFlag case)
                for sub_condition in condition.right_operator:
                    self._declare_if_needed(sub_condition.left_operator, code_lines)
                    
                    if sub_condition.right_operator:
                        self._declare_if_needed(sub_condition.right_operator, code_lines)
            else:
                self._declare_if_needed(condition.right_operator, code_lines)
    
    def _declare_if_needed(self, operand, code_lines):
        """Declares a variable if necessary"""
        if isinstance(operand, Level5Variable):
            # Don't declare "system" variables like currentSubPhase
            if operand.vname not in self.declared_variables and \
               not operand.vname.startswith('current'):
                
                # Determine value
                value = self._get_variable_value(operand)
                
                # Generate declaration (Squirrel uses 'local' keyword)
                code_lines.append(f"    local {operand.vname} = {value};")
                self.declared_variables.add(operand.vname)
    
    def _get_variable_value(self, variable):
        """Gets the value of a variable"""
        # Special case: Boolean with integer value
        if variable.vtype == Level5VariableType.Boolean:
            if hasattr(variable, 'vvalue'):
                if isinstance(variable.vvalue, bool):
                    return "true" if variable.vvalue else "false"
                elif isinstance(variable.vvalue, int):
                    return "true" if variable.vvalue != 0 else "false"
            return "false"
        
        # Normal case for other types
        if hasattr(variable, 'vvalue') and isinstance(variable.vvalue, int):
            return str(variable.vvalue)
        elif isinstance(variable.vvalue, bool):
            return "true" if variable.vvalue else "false"
        else:
            return "0"
    
    def _generate_recursive(self, conditions, index, code_lines, indent=0):
        current = conditions[index]
        ind = "    " * indent
        
        # Special case: BitFlag with list of conditions
        if isinstance(current.left_operator, Level5Variable) and \
           current.left_operator.vtype == Level5VariableType.BitFlag and \
           isinstance(current.right_operator, list):
            
            self._generate_bitflag_condition(current, code_lines, indent, index)
            return
        
        # Normal case
        left = self._format_operand(current.left_operator)
        right = self._format_operand(current.right_operator)
        op = current.compare_operator.value if current.compare_operator else "=="
        
        code_lines.append(f"{ind}if ({left} {op} {right}) {{")
        
        if index + 1 < len(conditions):
            self._generate_recursive(conditions, index + 1, code_lines, indent + 1)
        else:
            code_lines.append(f"{ind}    result = true;")
        
        code_lines.append(f"{ind}}}")
    
    def _generate_bitflag_condition(self, condition, code_lines, indent, index):
        """Generates specific code for BitFlag conditions"""
        ind = "    " * indent
        bitflag_conditions = condition.right_operator
        
        # First condition: variable0 (the bitflag ID)
        first_cond = bitflag_conditions[0]
        variable_name = first_cond.left_operator.vname  # e.g. variable0
        op = condition.compare_operator.value if condition.compare_operator else ">="
        
        code_lines.append(f"{ind}if (CMND_GET_LAST_GLOBAL_BIT_FLAG() {op} {variable_name}) {{")
        
        # If there's a second condition (bit value verification)
        if len(bitflag_conditions) > 1:
            second_cond = bitflag_conditions[1]
            flag_var_name = f"flag_{variable_name}"
            value_var_name = second_cond.left_operator.vname
            
            # Get bitflag value using Squirrel function
            code_lines.append(f"{ind}    local {flag_var_name} = CMND_GET_GLOBAL_BIT_FLAG({variable_name});")
            
            # Generate comparison
            compare_op = "=="
            code_lines.append(f"{ind}    if ({flag_var_name} {compare_op} {value_var_name}) {{")
            
            # Set result or continue recursion
            if index + 1 < len(self.conditions):
                self._generate_recursive(self.conditions, index + 1, code_lines, indent + 2)
            else:
                code_lines.append(f"{ind}        result = true;")
            
            code_lines.append(f"{ind}    }}")
        else:
            # No value verification, set result or continue
            if index + 1 < len(self.conditions):
                self._generate_recursive(self.conditions, index + 1, code_lines, indent + 1)
            else:
                code_lines.append(f"{ind}    result = true;")
        
        code_lines.append(f"{ind}}}")
    
    def _format_operand(self, operand):
        """Formats an operand for Squirrel code"""
        if isinstance(operand, Level5Variable):
            # Replace system variables with Squirrel function calls
            if operand.vname == "currentSubPhase":
                return "CMND_GET_GAME_SUB_PHASE()"
            elif operand.vname == "currentBitFlag":
                return "CMND_GET_LAST_GLOBAL_BIT_FLAG()"
            else:
                return operand.vname
        elif isinstance(operand, bool):
            return "true" if operand else "false"
        elif isinstance(operand, int):
            return str(operand)
        elif operand is None:
            return "0"
        else:
            return str(operand)