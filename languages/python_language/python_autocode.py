import zlib
import re

class PythonAutoCode:
    """
    Generates a complete, executable Python file for testing a condition.
    """
    
    def __init__(self, condition_code, playground_data):
        self.condition_code = condition_code
        self.playground_data = playground_data
    
    def generate(self):
        """Generates the complete Python code"""
        code_parts = []
        
        # Generate stub functions
        code_parts.append(self._generate_stubs())
        code_parts.append("")
        
        # Add the condition function (converted from C to Python)
        code_parts.append("# Condition function (converted from C)")
        code_parts.append(self._convert_c_to_python(self.condition_code))
        code_parts.append("")
        
        # Main execution
        code_parts.append("if __name__ == '__main__':")
        code_parts.append("    result = condition()")
        code_parts.append("    print('true' if result else 'false')")
        
        return "\n".join(code_parts)
    
    def _remove_imports(self, code):
        """Removes all C and Python imports"""
        lines = code.split('\n')
        filtered_lines = []
        
        for line in lines:
            stripped = line.strip()

            if stripped.startswith('#include'):
                continue

            if stripped.startswith('import ') or stripped.startswith('from '):
                continue

            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _convert_c_to_python(self, c_code):
        """Converts C code to Python"""
        # Delete imports first
        python_code = self._remove_imports(c_code)
        
        # Replace return types and bool
        python_code = python_code.replace("bool condition()", "def condition():")
        python_code = python_code.replace("bool ", "")
        python_code = python_code.replace("int ", "")
        python_code = python_code.replace("uint32_t ", "")
        python_code = python_code.replace("float ", "")
        
        # Replace true/false
        python_code = python_code.replace("true", "True")
        python_code = python_code.replace("false", "False")
        
        # Replace logical operators
        python_code = python_code.replace("&&", " and ")
        python_code = python_code.replace("||", " or ")
        python_code = python_code.replace("!", "not ")
        
        # Process line by line
        lines = python_code.split('\n')
        converted_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Ignore blank lines
            if not stripped:
                continue
            
            # Remove opening braces only
            if stripped == "{":
                continue
            
            # Remove closing braces only
            if stripped == "}":
                continue
            
            # Process the other lines
            processed = line.replace("{", "").replace("}", "").replace(";", "")
            
            # Add: after the closing parentheses for if/while/for
            processed = re.sub(r'\)\s*$', '):', processed)
            
            if processed.strip():
                converted_lines.append(processed)
        
        return '\n'.join(converted_lines)
    
    def _generate_stubs(self):
        """Generates all stub functions in Python"""
        stubs = []
        
        # GetSubPhase
        stubs.append("def GetSubPhase():")
        stubs.append(f"    return {self.playground_data['SUB_PHASE_VALUE']}")
        stubs.append("")
        
        # GetPhase
        stubs.append("def GetPhase():")
        stubs.append(f"    return {self.playground_data['PHASE_VALUE']}")
        stubs.append("")
        
        # GetChapter
        stubs.append("def GetChapter():")
        stubs.append(f"    return {self.playground_data['CHAPTER_VALUE']}")
        stubs.append("")
        
        # GetFrameChapter
        stubs.append("def GetFrameChapter():")
        stubs.append(f"    return {self.playground_data['FRAME_CHAPTER_VALUE']}")
        stubs.append("")
        
        # CheckShopOpen
        stubs.append("def CheckShopOpen(shop_id):")
        stubs.append(f"    return {self.playground_data['SHOP_OPEN_VALUE']}")
        stubs.append("")
        
        # GetGameVersion
        stubs.append("def GetGameVersion():")
        stubs.append("    return 1")
        stubs.append("")
        
        # GetTempBitFlag
        stubs.append("def GetTempBitFlag(flag_id):")
        if self.playground_data['TEMP_BIT_FLAG']:
            stubs.append(f"    flags = {dict(self.playground_data['TEMP_BIT_FLAG'])}")
            stubs.append("    if flag_id in flags:")
            stubs.append("        return flags[flag_id]")
            stubs.append("    return False")
        else:
            stubs.append("    return False")
        stubs.append("")
        
        # GetTempMapBitFlag
        stubs.append("def GetTempMapBitFlag(flag_id):")
        if self.playground_data['TEMP_MAP_BIT_FLAG']:
            stubs.append(f"    flags = {dict(self.playground_data['TEMP_MAP_BIT_FLAG'])}")
            stubs.append("    if flag_id in flags:")
            stubs.append("        return flags[flag_id]")
            stubs.append("    return False")
        else:
            stubs.append("    return False")
        stubs.append("")
        
        # GetGlobalBitFlag
        stubs.append("def GetGlobalBitFlag(flag_id):")
        if self.playground_data['GLOBAL_BIT_FLAG']:
            stubs.append(f"    flags = {dict(self.playground_data['GLOBAL_BIT_FLAG'])}")
            stubs.append("    if flag_id in flags:")
            stubs.append("        return flags[flag_id]")
            stubs.append("    return False")
        else:
            stubs.append("    return False")
        stubs.append("")
        
        # GetGlobalTBoxFlag
        stubs.append("def GetGlobalTBoxFlag(flag_id):")
        if self.playground_data['GLOBAL_T_BOX_FLAG']:
            stubs.append(f"    flags = {dict(self.playground_data['GLOBAL_T_BOX_FLAG'])}")
            stubs.append("    if flag_id in flags:")
            stubs.append("        return flags[flag_id]")
            stubs.append("    return False")
        else:
            stubs.append("    return False")
        stubs.append("")
        
        # GetTempMapByteFlag
        stubs.append("def GetTempMapByteFlag(flag_id):")
        stubs.append("    return 1")
        stubs.append("")
        
        # GetTempByteFlag
        stubs.append("def GetTempByteFlag(flag_id):")
        stubs.append("    return 1")
        stubs.append("")
        
        # GetTRouteFlag
        stubs.append("def GetTRouteFlag(flag_id):")
        stubs.append("    return True")
        stubs.append("")
        
        # GetGlobalCharaMetFlag
        stubs.append("def GetGlobalCharaMetFlag(flag_id):")
        stubs.append("    return True")
        stubs.append("")
        
        # IsHaveItem
        stubs.append("def IsHaveItem(item_crc):")
        if self.playground_data['HAVE_ITEM']:
            # Calculate CRC32 for each item
            item_crcs = {}
            for item in self.playground_data['HAVE_ITEM']:
                try:
                    crc = int(item)
                except ValueError:
                    # It's a string, calculate CRC32
                    crc = zlib.crc32(item.encode('utf-8')) & 0xFFFFFFFF
                item_crcs[crc] = True
            
            stubs.append(f"    items = {item_crcs}")
            stubs.append("    return items.get(item_crc, False)")
        else:
            stubs.append("    return False")
        stubs.append("")
        
        return "\n".join(stubs)