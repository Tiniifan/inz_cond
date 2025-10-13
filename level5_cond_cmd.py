import argparse

from level_5.condition.decoder import Level5ConditionDecoder
from languages.c_language.c_codegenerator import CCodeGenerator
from languages.squirrel_language.squirrel_codegenerator import SquirrelCodeGenerator
from languages.transformers.code_transformer import CodeTransformer

def main():
    parser = argparse.ArgumentParser(description="Level5 Condition Code Generator")
    parser.add_argument("-d", "--data", required=True, help="Base64 encoded condition file")
    parser.add_argument("-sq", "--squirrel", action="store_true", help="Generate Squirrel code instead of C")
    parser.add_argument("-c", "--c", action="store_true", help="Force C code generation (default)")
    args = parser.parse_args()
    
    encoded = args.data
    
    # Decoding the conditions
    conditions = Level5ConditionDecoder.from_base64(encoded)
    print("\nDecoded Conditions:", conditions)
    
    # Generator selection
    if args.squirrel:
        generator = SquirrelCodeGenerator(conditions)
    else:
        generator = CCodeGenerator(conditions)
    
    # Code generation
    code = generator.generate()
    
    # Beautify the generated code
    transformer = CodeTransformer(code)
    code = transformer.beautify()
    
    print("\nGenerated Code:\n")
    print(code)

if __name__ == "__main__":
    main()