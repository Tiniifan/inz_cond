import io

from contextlib import redirect_stdout

from PyQt6.QtWidgets import QMessageBox

from level_5.condition.decoder import Level5ConditionDecoder
from level_5.condition.encoder import Level5ConditionEncoder

from languages.c_language.c_codegenerator import CCodeGenerator
from languages.c_language.c_codeserializer import CCodeSerializer
from languages.squirrel_language.squirrel_codegenerator import SquirrelCodeGenerator
from languages.transformers.code_transformer import CodeTransformer
from languages.python_language.python_autocode import PythonAutoCode
from languages.translator import Translator

class CodeController:
    """Controller for code management (encode/decode/try)"""
    
    def __init__(self):
        self.translator = Translator()
    
    def decode_base64(self, base64_data, language):
        """Decode a base64 string into code"""
        try:
            conditions = Level5ConditionDecoder.from_base64(base64_data)
            if language == "C":
                generator = CCodeGenerator(conditions)
            else:
                generator = SquirrelCodeGenerator(conditions)
            code = CodeTransformer(generator.generate()).beautify()
            return code, None
        except Exception as e:
            return None, str(e)
    
    def encode_code(self, code, language):
        """Encode the code in base64"""
        if language != "C":
            code = self.translator.translate(code, language, 'C')
        
        try:
            parser = CCodeSerializer(code)
            conditions = parser.parse()
            encoded = Level5ConditionEncoder.to_base64(conditions)
            return encoded, None
        except Exception as e:
            return None, str(e)
    
    def try_condition(self, code, language, playground_data):
        """Test the condition"""
        if language != "C":
            code = self.translator.translate(code, language, 'C')
        
        try:
            # We convert the C code into Python code
            auto_code = PythonAutoCode(code, playground_data)
            full_python_code = auto_code.generate()

            # Capture stdout
            output_buffer = io.StringIO()
            
            try:
                # Create a namespace for execution
                exec_namespace = {}
                
                with redirect_stdout(output_buffer):
                    # Run the generated Python code
                    exec(full_python_code, exec_namespace)
                    
                    # Call the condition function
                    if 'condition' in exec_namespace:
                        result = exec_namespace['condition']()
                        print('true' if result else 'false')
                
                # Retrieve the output
                result_str = output_buffer.getvalue().strip()
                return result_str, None
                
            except Exception as e:
                return None, f"Execution error: {str(e)}"
        
        except Exception as e:
            return None, str(e)

    def translate_code(self, code, from_language, to_language):
        """Translates code from one language to another"""
        try:
            converted = self.translator.translate(code, from_language, to_language)
            return converted, None
        except Exception as e:
            return None, str(e)            