import re

class CodeBeautifier:
    """
    Beautifies code by adding blank lines according to specific rules.
    """
    
    def beautify(self, code):
        """
        Formats code by adding blank lines according to specific rules.
        """
        lines = code.split('\n')
        result = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Add current line
            result.append(line)
            
            # Rules for adding a blank line after
            if i < len(lines) - 1:
                next_line = lines[i + 1].strip()
                
                # Rule 0: After "bool result = false;" or "local result = false;", add blank line
                if self._is_result_declaration(stripped) and self._is_variable_declaration(next_line):
                    result.append('')
                
                # Rule 1: After a block of variable declarations, before if/while/for
                elif self._is_variable_declaration(stripped) and self._starts_with_control_structure(next_line):
                    result.append('')
                
                # Rule 2: After a variable assignment (inside an if), before an if
                elif self._is_assignment(stripped) and next_line.startswith('if'):
                    result.append('')
                
                # Rule 3: After a closing brace of an if block, before another if
                elif stripped == '}' and next_line.startswith('if'):
                    result.append('')
                
                # Rule 4: Before a return (except right after an opening brace)
                elif next_line.startswith('return') and not stripped.endswith('{'):
                    # Check that we're not right after the function opening
                    if i > 0 and not lines[i - 1].strip().endswith('{'):
                        result.append('')
            
            i += 1
        
        return '\n'.join(result)
    
    def _is_result_declaration(self, line):
        """Detects the result variable declaration (bool result = false or local result = false)."""
        patterns = [
            r'^\s*(bool|local)\s+result\s*=\s*false\s*;',
        ]
        return any(re.match(pattern, line) for pattern in patterns)
    
    def _is_variable_declaration(self, line):
        """Detects a variable declaration."""
        patterns = [
            r'^\s*(int|bool|float|double|char|local)\s+\w+\s*=',
            r'^\s*(int|bool|float|double|char|local)\s+\w+\s*;'
        ]
        
        return any(re.match(pattern, line) for pattern in patterns)
    
    def _is_assignment(self, line):
        """Detects a variable assignment."""
        return '=' in line and not line.strip().startswith('if') and not line.strip().startswith('return')
    
    def _starts_with_control_structure(self, line):
        """Detects the start of a control structure."""
        return line.startswith(('if', 'while', 'for', 'switch'))