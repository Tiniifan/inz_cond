import os
import sys
import re

# Add root path to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from level_5.condition.logic import *
from languages.transformers.code_transformer import CodeTransformer

class CCodeSerializer:
    def __init__(self, code):
        self.code = code
        self.transformer = CodeTransformer(code)
        self.variable_counter = 0
    
    def parse(self):
        """
        Parses C code and returns a list of condition blocks.
        """
        # Simplify code first
        simplified_code = self.transformer.simplify()
        
        # Parse the simplified code
        conditions = self._parse_simplified_code(simplified_code)    
        
        return conditions
    
    def _parse_simplified_code(self, code):
        """
        Parses simplified C code to extract conditions.
        Handles nested if blocks properly.
        """
        lines = code.split('\n')
        conditions = []
        current_block = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Skip function declaration, opening brace, result declaration
            if stripped in ['bool condition()', '{', 'bool result = false;', 'return result;', '}']:
                i += 1
                continue
            
            # Parse if statement
            if stripped.startswith('if'):
                condition_list = self._parse_if_statement(stripped)
                if condition_list:
                    # This is a new condition block
                    conditions.append(condition_list)
                
                i += 1
                continue
            
            i += 1
        
        return conditions
    
    def _parse_if_statement(self, if_line):
        """
        Parses an if statement and returns a list of Level5Operation.
        For || and &&, creates nested Level5Operation structures.
        """
        # Extract condition from if statement
        match = re.search(r'if\s*\((.*)\)\s*\{', if_line)
        if not match:
            return None
        
        condition_str = match.group(1).strip()
        
        # Parse the full condition expression (handles ||, &&, and simple conditions)
        operation = self._parse_logical_expression(condition_str)
        return [operation] if operation else []
    
    def _parse_logical_expression(self, expr):
        """
        Parses a logical expression with ||, &&, or simple conditions.
        Creates nested Level5Operation for logical operators.
        Priority: || (lowest) > && (highest)
        """
        expr = expr.strip()
        
        # First, check for || (lowest precedence)
        if '||' in expr:
            parts = self._smart_split(expr, '||')
            if len(parts) > 1:
                # Build right-to-left tree for multiple ||
                result = self._parse_logical_expression(parts[-1])
                for i in range(len(parts) - 2, -1, -1):
                    left_op = self._parse_logical_expression(parts[i])
                    # Determine operator type (should be bool for logical operations)
                    operator_type = "bool"
                    result = Level5Operation(left_op, result, OperatorEnum.LOGICAL_OR, operator_type)
                return result
        
        # Then check for && (higher precedence than ||)
        if '&&' in expr:
            parts = self._smart_split(expr, '&&')
            if len(parts) > 1:
                # Build right-to-left tree for multiple &&
                result = self._parse_logical_expression(parts[-1])
                for i in range(len(parts) - 2, -1, -1):
                    left_op = self._parse_logical_expression(parts[i])
                    # Determine operator type (should be bool for logical operations)
                    operator_type = "bool"
                    result = Level5Operation(left_op, result, OperatorEnum.LOGICAL_AND, operator_type)
                return result
        
        # No logical operators, parse as simple condition
        return self._parse_condition_expression(expr)
    
    def _smart_split(self, text, delimiter):
        """
        Split text by delimiter, but respecting parentheses.
        Example: "GetGlobalBitFlag(1701) || GetGlobalBitFlag(1702)"
        Will not split inside the parentheses of function calls.
        """
        parts = []
        current = []
        depth = 0
        
        i = 0
        while i < len(text):
            # Check if we're at the delimiter
            if depth == 0 and text[i:i+len(delimiter)] == delimiter:
                parts.append(''.join(current).strip())
                current = []
                i += len(delimiter)
                continue
            
            # Track parenthesis depth
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
            
            current.append(text[i])
            i += 1
        
        # Add the last part
        if current:
            parts.append(''.join(current).strip())
        
        return parts
    
    def _parse_condition_expression(self, expr):
        """
        Parses a condition expression like "GetSubPhase() >= 130010010"
        or "!GetGlobalBitFlag(1365)" or "GetGlobalBitFlag(1365)"
        """
        # Check for negation (!)
        if expr.startswith('!'):
            # Boolean condition with == 0
            inner_expr = expr[1:].strip()
            left_operand = self._parse_operand(inner_expr)
            right_operand = Level5Variable(f"variable{self.variable_counter}", SymbolType.LOCAL_INT, 0)
            self.variable_counter += 1
            
            operator_type = self._determine_operator_type(left_operand, right_operand)
            return Level5Operation(left_operand, right_operand, OperatorEnum.EQUAL, operator_type)
        
        # Check if it's a simple boolean expression (no comparator)
        if not any(op in expr for op in ['<=', '>=', '==', '!=', '<', '>']):
            # Boolean condition with == 1
            left_operand = self._parse_operand(expr)
            right_operand = Level5Variable(f"variable{self.variable_counter}", SymbolType.LOCAL_INT, 1)
            self.variable_counter += 1
            
            operator_type = self._determine_operator_type(left_operand, right_operand)
            return Level5Operation(left_operand, right_operand, OperatorEnum.EQUAL, operator_type)
        
        # Parse normal comparison with operator
        for symbol in ['<=', '>=', '==', '!=', '<', '>']:  # Order matters: <= and >= before < and >
            if symbol in expr:
                operator_enum = OperatorEnum.from_string(symbol)
                if not operator_enum:
                    raise ValueError(f"Unknown operator: {symbol}")
                
                parts = self._smart_split(expr, symbol)
                if len(parts) == 2:
                    left_str = parts[0].strip()
                    right_str = parts[1].strip()
                    
                    left_operand = self._parse_operand(left_str)
                    right_operand = self._parse_operand(right_str)
                    
                    operator_type = self._determine_operator_type(left_operand, right_operand)
                    return Level5Operation(left_operand, right_operand, operator_enum, operator_type)
        
        raise ValueError(f"Could not parse condition expression: {expr}")
    
    def _parse_operand(self, operand_str):
        """
        Parses an operand (can be a function call or a literal value).
        """
        operand_str = operand_str.strip()
        
        # Check if it's a function call
        if '(' in operand_str and ')' in operand_str:
            return self._parse_function_call(operand_str)
        
        # Otherwise, it's a literal value
        try:
            value = int(operand_str)
            var = Level5Variable(f"variable{self.variable_counter}", SymbolType.LOCAL_INT, value)
            self.variable_counter += 1
            return var
        except ValueError:
            raise ValueError(f"Could not parse operand: {operand_str}")
    
    def _parse_function_call(self, func_str):
        """
        Parses a function call like "GetSubPhase()" or "GetGlobalBitFlag(1365)".
        """
        match = re.match(r'(\w+)\((.*)\)', func_str)
        if not match:
            raise ValueError(f"Invalid function call: {func_str}")
        
        func_name_str = match.group(1)
        args_str = match.group(2).strip()
        
        # Get function definition from registry
        func_def = FunctionRegistry.get_by_name(func_name_str)
        if not func_def:
            raise ValueError(f"Unknown function: {func_name_str}")
        
        # Get expected argument count
        expected_arg_count = func_def.arg_count
        
        # Parse arguments
        func_args = []
        if args_str:
            arg_values = self._smart_split(args_str, ',')
            for arg_value in arg_values:
                arg_value = arg_value.strip()
                try:
                    value = int(arg_value)
                    arg = Level5Variable(f"variable{self.variable_counter}", SymbolType.LOCAL_INT, value)
                    self.variable_counter += 1
                    func_args.append(arg)
                except ValueError:
                    raise ValueError(f"Invalid argument value: {arg_value}")
        
        # Verify argument count matches
        if expected_arg_count != len(func_args):
            raise ValueError(f"Function {func_name_str} expects {expected_arg_count} argument(s), got {len(func_args)}")
        
        # Return function with name as string (from FunctionDefinition)
        return Level5Function(func_def.name, func_args)
    
    def _determine_operator_type(self, left, right):
        """Determine the operator type based on the operands"""
        # Check if left operand is a function
        if isinstance(left, Level5Function):
            func_def = FunctionRegistry.get_by_name(left.name)
            if func_def:
                return func_def.return_type
        
        # Check if right operand is a function
        if isinstance(right, Level5Function):
            func_def = FunctionRegistry.get_by_name(right.name)
            if func_def:
                return func_def.return_type
        
        # Default to int if both are variables
        return "int"