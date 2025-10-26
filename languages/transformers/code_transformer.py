from .transformations.beautifier import CodeBeautifier
from .transformations.simplifier import CodeSimplifier

class CodeTransformer:
    """
    A class responsible for managing and transforming source code.
    It provides methods to beautify and simplify the code.
    """

    def __init__(self, code):
        """
        Initialize the CodeTransformer with the given code.
        """
        self.code = code
        self.beautifier = CodeBeautifier()
        self.simplifier = CodeSimplifier()
    
    def beautify(self):
        """
        Beautify the current code.
        """
        return self.beautifier.beautify(self.code)
    
    def simplify(self):
        """
        Simplify the current code.
        """
        return self.simplifier.simplify(self.code)
    
    def update_code(self, new_code):
        """
        Update the current code with a new version.
        """
        self.code = new_code
