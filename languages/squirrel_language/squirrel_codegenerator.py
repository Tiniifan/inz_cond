import re
import os
import sys

# Add root path to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
    
from languages.c_language.c_codegenerator import CCodeGenerator

class SquirrelCodeGenerator:
    def __init__(self, conditions):
        self.conditions = conditions
        
        # Mapping of C function names to Squirrel function names
        self.function_mapping = {
            'getGameSubPhase': 'CMND_GET_GAME_SUB_PHASE',
            'getGlobalBitFlag': 'CMND_GET_GLOBAL_BIT_FLAG',
            'getTeamBitFlag': 'CMND_GET_TEAM_BIT_FLAG',
            'isHaveItem': 'CMND_IS_HAVE_ITEM'
        }
    
    def generate(self):
        # Generate C code first
        c_generator = CCodeGenerator(self.conditions)
        c_code = c_generator.generate()
        
        # Convert C code to Squirrel code
        squirrel_code = self._convert_c_to_squirrel(c_code)
        
        return squirrel_code
    
    def _convert_c_to_squirrel(self, c_code):
        """Converts C code to Squirrel code by replacing syntax"""
        squirrel_code = c_code
        
        # Replace function declaration
        squirrel_code = squirrel_code.replace('bool condition()', 'function condition()')
        
        # Replace bool result declaration
        squirrel_code = squirrel_code.replace('bool result = false;', 'local result = false;')
        
        # Replace function names using mapping
        for c_func, squirrel_func in self.function_mapping.items():
            # Use regex to match function calls (function name followed by parenthesis)
            pattern = r'\b' + c_func + r'\('
            replacement = squirrel_func + '('
            squirrel_code = re.sub(pattern, replacement, squirrel_code)
        
        return squirrel_code