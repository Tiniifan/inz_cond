import re


class Translator:
    """Translates code between C and Squirrel languages"""
    
    def __init__(self):
        # Mapping C functions (PascalCase) to Squirrel (CMND_UPPER_SNAKE_CASE)
        self.c_to_squirrel_mapping = {
            'GetSubPhase': 'CMND_GET_SUB_PHASE',
            'GetPhase': 'CMND_GET_PHASE',
            'GetTRouteFlag': 'CMND_GET_T_ROUTE_FLAG',
            'GetTempMapByteFlag': 'CMND_GET_TEMP_MAP_BYTE_FLAG',
            'GetTempByteFlag': 'CMND_GET_TEMP_BYTE_FLAG',
            'GetGlobalCharaMetFlag': 'CMND_GET_GLOBAL_CHARA_MET_FLAG',
            'GetGlobalBitFlag': 'CMND_GET_GLOBAL_BIT_FLAG',
            'GetTempMapBitFlag': 'CMND_GET_TEMP_MAP_BIT_FLAG',
            'GetTempBitFlag': 'CMND_GET_TEMP_BIT_FLAG',
            'GetGlobalTBoxFlag': 'CMND_GET_GLOBAL_T_BOX_FLAG',
            'IsHaveItem': 'CMND_IS_HAVE_ITEM',
            'CheckShopOpen': 'CMND_CHECK_SHOP_OPEN',
            'GetGameVersion': 'CMND_GET_GAME_VERSION',
            'GetFrameChapter': 'CMND_GET_FRAME_CHAPTER',
            'GetChapter': 'CMND_GET_CHAPTER'
        }
        
        # Reverse mapping for Squirrel to C
        self.squirrel_to_c_mapping = {v: k for k, v in self.c_to_squirrel_mapping.items()}
    
    def c_to_squirrel(self, c_code):
        """Converts C code to Squirrel code"""
        squirrel_code = c_code
        
        # Replace function declaration
        squirrel_code = squirrel_code.replace('bool condition()', 'function condition()')
        
        # Replace bool result declaration
        squirrel_code = squirrel_code.replace('bool result = false;', 'local result = false;')
        squirrel_code = squirrel_code.replace('bool result = true;', 'local result = true;')
        
        # Replace other bool declarations
        squirrel_code = re.sub(r'\bbool\s+(\w+)\s*=', r'local \1 =', squirrel_code)
        
        # Replace function names using mapping
        for c_func, squirrel_func in self.c_to_squirrel_mapping.items():
            # Use regex to match function calls (function name followed by parenthesis)
            pattern = r'\b' + c_func + r'\('
            replacement = squirrel_func + '('
            squirrel_code = re.sub(pattern, replacement, squirrel_code)
        
        # Replace true/false keywords (case sensitive)
        squirrel_code = re.sub(r'\bfalse\b', 'false', squirrel_code)
        squirrel_code = re.sub(r'\btrue\b', 'true', squirrel_code)
        
        return squirrel_code
    
    def squirrel_to_c(self, squirrel_code):
        """Converts Squirrel code to C code"""
        c_code = squirrel_code
        
        # Replace function declaration
        c_code = c_code.replace('function condition()', 'bool condition()')
        
        # Replace local result declaration
        c_code = c_code.replace('local result = false;', 'bool result = false;')
        c_code = c_code.replace('local result = true;', 'bool result = true;')
        
        # Replace other local declarations
        c_code = re.sub(r'\blocal\s+(\w+)\s*=', r'bool \1 =', c_code)
        
        # Replace function names using mapping
        for squirrel_func, c_func in self.squirrel_to_c_mapping.items():
            # Use regex to match function calls (function name followed by parenthesis)
            pattern = r'\b' + squirrel_func + r'\('
            replacement = c_func + '('
            c_code = re.sub(pattern, replacement, c_code)
        
        return c_code
    
    def translate(self, code, from_language, to_language):
        """Generic translation method"""
        if from_language == to_language:
            return code
        
        if from_language == "C" and to_language == "Squirrel":
            return self.c_to_squirrel(code)
        elif from_language == "Squirrel" and to_language == "C":
            return self.squirrel_to_c(code)
        else:
            raise ValueError(f"Unsupported translation: {from_language} to {to_language}")