import re

class CodeSimplifier:
    """
    Simplifies C/Squirrel code:
    - Removes empty lines
    - Integrates local variables (except result)
    - Removes unnecessary parentheses
    - Removes blocks where result = false
    - Merges all if / else if / || into a single if with logical OR
    """

    def __init__(self):
        self.variable_values = {}

    def simplify(self, code):
        code = self._remove_blank_lines(code)
        code = self._inline_variables(code)
        code = self._remove_useless_parentheses(code)
        code = self._remove_result_false_blocks(code)
        code = self._convert_and_to_nested_if(code)
        code = self._merge_all_conditions(code)
        return code

    def _remove_blank_lines(self, code):
        return '\n'.join(line for line in code.split('\n') if line.strip())

    def _inline_variables(self, code):
        """
        Replaces local variables with their values except result
        """
        lines = code.split('\n')
        result = []
        self.variable_values.clear()

        for line in lines:
            stripped = line.strip()
            if self._is_var_decl(stripped):
                name, value = self._extract_var(stripped)
                if name == 'result':
                    result.append(line)
                    continue
                if name and value:
                    value = self._replace_vars_in_expression(value)
                    self.variable_values[name] = value
                continue
            else:
                result.append(self._replace_vars(line))
        return '\n'.join(result)

    def _replace_vars_in_expression(self, expression):
        """
        Replaces variables in an expression
        """
        for name, val in sorted(self.variable_values.items(), key=lambda x: len(x[0]), reverse=True):
            expression = re.sub(r'\b' + re.escape(name) + r'\b', val, expression)
        return expression

    def _is_var_decl(self, line):
        return bool(re.match(r'^\s*(int|bool|float|double|char|local)\s+\w+\s*=', line))

    def _extract_var(self, line):
        m = re.match(r'^\s*(?:int|bool|float|double|char|local)\s+(\w+)\s*=\s*(.+?);', line)
        if m:
            return m.group(1), m.group(2).strip()
        return None, None

    def _replace_vars(self, line):
        for name, val in sorted(self.variable_values.items(), key=lambda x: len(x[0]), reverse=True):
            line = re.sub(r'\b' + re.escape(name) + r'\b', val, line)
        return line

    def _remove_useless_parentheses(self, code):
        """
        Removes unnecessary double parentheses around conditions
        """
        while re.search(r'\(\(([^()]+)\)\)', code):
            code = re.sub(r'\(\(([^()]+)\)\)', r'(\1)', code)
        return code

    def _remove_result_false_blocks(self, code):
        """
        Delete blocks where result = false;
        """
        pattern = r'if\s*\([^\)]*\)\s*\{\s*result\s*=\s*false;\s*\}'
        return re.sub(pattern, '', code, flags=re.DOTALL)

    def _convert_and_to_nested_if(self, code):
        """
        Converts conditions with && into nested if statements.
        - Example: if (a && b) { result = true; }
        - Becomes: if (a) { if (b) { result = true; } }
        """
        lines = code.split('\n')
        result = []
        
        for line in lines:
            stripped = line.strip()
            
            # Detects an if with &&
            if_match = re.match(r'^if\s*\((.*?)\)\s*\{', stripped)
            if if_match:
                condition = if_match.group(1).strip()
                
                # If the condition contains &&
                if '&&' in condition:
                    # Separates conditions with &&
                    parts = [p.strip() for p in condition.split('&&')]
                    
                    # Calculates the indentation of the current line
                    indent = len(line) - len(line.lstrip())
                    base_indent = ' ' * indent
                    
                    # Creates nested if statements
                    nested_ifs = []
                    for i, part in enumerate(parts):
                        current_indent = base_indent + '    ' * i
                        nested_ifs.append(f"{current_indent}if ({part}) {{")
                    
                    # Adds nested if statements
                    result.extend(nested_ifs)
                    continue
            
            # Closing braces: add as many } as && found previously
            if stripped == '}' and result:
                # Find out how many nested if statements we have created
                count_nested = 0
                for prev_line in reversed(result):
                    if 'if (' in prev_line and prev_line.strip().endswith('{'):
                        count_nested += 1
                    elif prev_line.strip() == 'result = true;':
                        break
                
                # If there are several nested if statements, add the corresponding }
                if count_nested > 1:
                    indent = len(line) - len(line.lstrip())
                    for i in range(count_nested):
                        result.append(' ' * (indent + (count_nested - 1 - i) * 4) + '}')
                    continue
            
            result.append(line)
        
        return '\n'.join(result)

    def _merge_all_conditions(self, code):
        """
        Merges all if/else if/|| statements into a single if statement with logical OR.
        """
        lines = code.split('\n')
        conditions = []
        inside_if = False
        brace_depth = 0

        for line in lines:
            stripped = line.strip()

            # Detects an if/else if condition (but not nested if statements)
            if (stripped.startswith('if') or stripped.startswith('else if')) and brace_depth == 0:
                m = re.search(r'if\s*\((.*?)\)\s*\{', stripped)
                if m:
                    condition = m.group(1).strip()
                    condition = re.sub(r'\s*\|\|\s*', '||', condition)
                    conditions.append(condition)
                inside_if = True
                brace_depth += line.count('{')
                continue

            if inside_if:
                brace_depth += line.count('{') - line.count('}')
                if brace_depth <= 0:
                    inside_if = False
                continue

        # If there is only one condition with &&, do not merge
        if len(conditions) <= 1:
            return code

        # Proper reconstruction
        merged = []
        merged.append("bool condition() {")
        merged.append("    bool result = false;")

        if conditions:
            cleaned_conditions = []
            for c in conditions:
                c = c.strip()
                c = re.sub(r'^\((.*)\)$', r'\1', c)
                if c not in cleaned_conditions:
                    cleaned_conditions.append(c)

            final_condition = " || ".join(cleaned_conditions)
            merged.append(f"    if ({final_condition}) {{")
            merged.append("        result = true;")
            merged.append("    }")

        merged.append("    return result;")
        merged.append("}")
        return '\n'.join(merged)