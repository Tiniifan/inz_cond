import re

from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor

class SquirrelSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Squirrel language"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "function", "local", "if", "else", "return", "true", "false",
            "while", "for", "foreach", "in", "switch", "case", "break",
            "continue", "class", "extends", "constructor", "this", "base",
            "null", "typeof", "clone", "delete"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlighting_rules.append((re.compile(pattern), keyword_format))
        
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA"))
        self.highlighting_rules.append((re.compile(r'\b[A-Z_][A-Z0-9_]*(?=\()'), function_format))
        self.highlighting_rules.append((re.compile(r'\b[a-z_][A-Za-z0-9_]*(?=\()'), function_format))
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\b'), number_format))
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.highlighting_rules.append((re.compile(r'//[^\n]*'), comment_format))
        
        variable_format = QTextCharFormat()
        variable_format.setForeground(QColor("#9CDCFE"))
        self.highlighting_rules.append((re.compile(r'\bvariable[0-9]+\b'), variable_format))
        self.highlighting_rules.append((re.compile(r'\bflag_variable[0-9]+\b'), variable_format))
        self.highlighting_rules.append((re.compile(r'\bresult\b'), variable_format))
    
    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)