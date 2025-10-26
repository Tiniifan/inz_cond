import os

from level_5.condition.decoder import Level5ConditionDecoder
from level_5.condition.encoder import Level5ConditionEncoder

from languages.c_language.c_codegenerator import CCodeGenerator
from languages.c_language.c_codeserializer import CCodeSerializer

from languages.transformers.code_transformer import CodeTransformer

def test_condition_roundtrip(base64_input):
    """
    Test the roundtrip conversion: base64 -> code1 -> base64 -> code2
    Compare code1 and code2
    Returns (success, message)
    """
    try:
        # Step 1: Decode base64 to conditions
        conditions = Level5ConditionDecoder.from_base64(base64_input)
        
        # Step 2: Generate C code from conditions (code1)
        generator = CCodeGenerator(conditions)
        code1 = CodeTransformer(generator.generate()).beautify()
        
        # Step 3: Parse the generated C code back to conditions
        parser = CCodeSerializer(code1)
        parsed_conditions = parser.parse()
        print('parsed_conditions', parsed_conditions)
        
        # Step 4: Encode back to base64
        base64_output = Level5ConditionEncoder.to_base64(parsed_conditions)
        
        # Step 5: Decode the new base64 to conditions
        conditions2 = Level5ConditionDecoder.from_base64(base64_output)
        
        # Step 6: Generate C code from the new conditions (code2)
        generator2 = CCodeGenerator(conditions2)
        code2 = CodeTransformer(generator2.generate()).beautify()
        
        # Step 7: Compare the two C codes
        if code1 == code2:
            return True, "Success"
        else:
            return False, f"Code mismatch:\nCode1:\n{code1}\n\nCode2:\n{code2}"
            
    except Exception as e:
        return False, f"Error: {type(e).__name__}: {str(e)}"

def main():
    input_file = "test_input.txt"
    output_file = "test_output.txt"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist")
        return
    
    # Read input file
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Process each condition and write results
    with open(output_file, 'w') as f:
        for i, base64_condition in enumerate(lines, 1):
            success, message = test_condition_roundtrip(base64_condition)
            
            # Write to output file
            f.write(f"Test {i}\n")
            f.write(f"Input : {base64_condition}\n")
            f.write(f"Output : {message}\n")
            f.write("\n")
            
            # Also print to console
            print(f"Test {i}: {message}")
    
    print(f"\nResults written to {output_file}")

if __name__ == "__main__":
    main()