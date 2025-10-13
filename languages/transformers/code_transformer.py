from transformations.beautifier import CodeBeautifier
from transformations.simplifier import CodeSimplifier

class CodeTransformer:
    def __init__(self, code):
        self.code = code
        self.beautifier = CodeBeautifier()
        self.simplifier = CodeSimplifier()
    
    def beautify(self):
        return self.beautifier.beautify(self.code)
    
    def simplify(self):
        return self.simplifier.simplify(self.code)
    
    def update_code(self, new_code):
        self.code = new_code