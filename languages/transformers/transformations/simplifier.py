import re

class CodeSimplifier:
    """
    Simplifies code by:
    - Removing blank lines
    - Converting && conditions to nested if statements
    - Extracting literal values into variables
    """
    
    def __init__(self):
        self.variable_counter = 0
        self.declared_variables = set()
    
    def simplify(self, code):
        """
        Main method to simplify code.
        """
        # Step 1: Remove blank lines
        code = self._remove_blank_lines(code)
        
        # Step 2: Extract literals to variables
        code = self._extract_literals_to_variables(code)
        
        # Step 3: Convert && to nested if statements
        code = self._convert_and_to_nested_if(code)
        
        return code
    
    def _remove_blank_lines(self, code):
        """
        Removes all blank lines from the code.
        """
        lines = code.split('\n')
        non_blank_lines = [line for line in lines if line.strip()]
        return '\n'.join(non_blank_lines)
    
    def _extract_literals_to_variables(self, code):
        """
        Extracts numeric literals from conditions into variables.
        Only extracts literals that are not function calls.
        """
        lines = code.split('\n')
        result = []
        self.variable_counter = 0
        self.declared_variables = set()
        
        # First pass: find where to insert variable declarations
        insert_index = -1
        for i, line in enumerate(lines):
            result.append(line)
            stripped = line.strip()
            
            # Find the position after the opening brace and initial declarations
            if stripped == '{':
                insert_index = i + 1
            elif insert_index != -1 and not self._is_variable_declaration(stripped):
                # Found first non-declaration line
                break
        
        # Second pass: extract literals from if statements
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if stripped.startswith('if'):
                # Extract literals from this if statement
                modified_line, new_declarations = self._extract_literals_from_line(line)
                
                if new_declarations:
                    # Insert variable declarations before this if
                    indent = self._get_indent(line)
                    for var_name, var_value in new_declarations:
                        declaration = f"{indent}int {var_name} = {var_value};"
                        result.insert(i, declaration)
                        i += 1
                    
                    result[i] = modified_line
                else:
                    result[i] = line
            
            i += 1
        
        # Rebuild from result if we modified anything
        if any('variable' in line for line in result):
            return '\n'.join(result)
        
        return code
    
    def _extract_literals_from_line(self, line):
        """
        Extracts numeric literals from a line and replaces them with variables.
        Returns the modified line and a list of (variable_name, value) tuples.
        """
        new_declarations = []
        
        # Pattern to find numeric literals in conditions (not in function calls)
        # Match numbers that are not followed by ) or preceded by (
        pattern = r'(?<=[<>=!]\s)(\d+)(?!\))'
        
        def replace_literal(match):
            value = match.group(1)
            var_name = f"variable{self.variable_counter}"
            self.variable_counter += 1
            new_declarations.append((var_name, value))
            return var_name
        
        modified_line = re.sub(pattern, replace_literal, line)
        
        return modified_line, new_declarations
    
    def _convert_and_to_nested_if(self, code):
        """
        Converts && conditions to nested if statements.
        """
        lines = code.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if stripped.startswith('if') and '&&' in stripped:
                # Split the condition by &&
                indent = self._get_indent(line)
                conditions = self._split_and_conditions(stripped)
                
                # Create nested if statements
                nested_ifs = self._create_nested_ifs(conditions, indent)
                result.extend(nested_ifs)
                
                # Skip lines until we find the closing brace of this if
                i += 1
                brace_count = 1
                inner_lines = []
                
                while i < len(lines) and brace_count > 0:
                    current = lines[i]
                    if '{' in current:
                        brace_count += current.count('{')
                    if '}' in current:
                        brace_count -= current.count('}')
                    
                    if brace_count > 0:
                        inner_lines.append(current)
                    i += 1
                
                # Add the inner content with proper indentation
                for inner_line in inner_lines:
                    result.append(indent + '\t' + inner_line)
                
                # Add closing braces
                for _ in range(len(conditions)):
                    result.append(indent + '\t' * (len(conditions) - _ - 1) + '}')
                
                continue
            
            result.append(line)
            i += 1
        
        return '\n'.join(result)
    
    def _split_and_conditions(self, if_statement):
        """
        Splits an if statement by && operators.
        """
        # Extract condition from if statement
        match = re.search(r'if\s*\((.*)\)', if_statement)
        if not match:
            return [if_statement]
        
        condition = match.group(1)
        
        # Split by && (simple split, doesn't handle nested parentheses)
        conditions = [c.strip() for c in condition.split('&&')]
        
        return conditions
    
    def _create_nested_ifs(self, conditions, base_indent):
        """
        Creates nested if statements from a list of conditions.
        """
        result = []
        
        for i, condition in enumerate(conditions):
            indent = base_indent + '\t' * i
            result.append(f"{indent}if ({condition}) {{")
        
        return result
    
    def _is_variable_declaration(self, line):
        """
        Checks if a line is a variable declaration.
        """
        patterns = [
            r'^\s*(int|bool|float|double|char|local)\s+\w+\s*=',
            r'^\s*(int|bool|float|double|char|local)\s+\w+\s*;'
        ]
        return any(re.match(pattern, line) for pattern in patterns)
    
    def _get_indent(self, line):
        """
        Gets the indentation of a line.
        """
        return line[:len(line) - len(line.lstrip())]