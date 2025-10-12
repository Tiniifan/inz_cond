import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QTextEdit, QLabel,
                              QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
import re
import base64

level5_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if level5_path not in sys.path:
    sys.path.insert(0, level5_path)

from level_5.condition.decoder import Level5ConditionDecoder
from languages.c_language.c_codegenerator import CCodeGenerator
from languages.squirrel_language.squirrel_codegenerator import SquirrelCodeGenerator


class CSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for C language"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "bool", "int", "void", "if", "else", "return", "true", "false",
            "while", "for", "do", "switch", "case", "break", "continue",
            "struct", "typedef", "enum", "const", "static", "extern"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlighting_rules.append((re.compile(pattern), keyword_format))
        
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA"))
        self.highlighting_rules.append((re.compile(r'\b[A-Za-z_][A-Za-z0-9_]*(?=\()'), function_format))
        
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


class Level5ConditionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = "C"
        self.c_highlighter = None
        self.squirrel_highlighter = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Level5 Condition Code Generator")
        self.setGeometry(100, 100, 1400, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # --- Top bar ---
        top_bar = QHBoxLayout()
        self.language_button = QPushButton("Switch to Squirrel")
        self.language_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
        """)
        self.language_button.clicked.connect(self.toggle_language)
        
        language_label = QLabel(f"Current Language: {self.current_language}")
        language_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.language_label = language_label
        
        top_bar.addWidget(language_label)
        top_bar.addStretch()
        top_bar.addWidget(self.language_button)
        main_layout.addLayout(top_bar)
        
        # --- Content area ---
        content_layout = QHBoxLayout()
        
        left_container = QVBoxLayout()
        code_label = QLabel("Generated Code:")
        code_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        left_container.addWidget(code_label)
        
        self.code_text = QTextEdit()
        self.code_text.setFont(QFont("Courier New", 10))
        self.code_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #3E3E3E;
                border-radius: 4px;
            }
        """)
        self.code_text.setPlaceholderText("Generated code will appear here...")
        left_container.addWidget(self.code_text)
        self.c_highlighter = CSyntaxHighlighter(self.code_text.document())
        
        middle_container = QVBoxLayout()
        middle_container.addStretch()
        
        self.convert_to_code_button = QPushButton("← Convert to Code")
        self.convert_to_code_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.convert_to_code_button.clicked.connect(self.convert_to_code)
        middle_container.addWidget(self.convert_to_code_button)
        middle_container.addSpacing(20)
        
        self.convert_to_base64_button = QPushButton("Convert to Base64 →")
        self.convert_to_base64_button.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                min-width: 180px;
            }
            QPushButton:disabled {
                background-color: #495057;
                color: #ADB5BD;
            }
        """)
        self.convert_to_base64_button.setEnabled(False)
        self.convert_to_base64_button.clicked.connect(self.convert_to_base64)
        middle_container.addWidget(self.convert_to_base64_button)

        middle_container.addSpacing(20)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
        """)
        self.clear_button.clicked.connect(self.clear_texts)
        middle_container.addWidget(self.clear_button)

        middle_container.addStretch()
        
        right_container = QVBoxLayout()
        base64_label = QLabel("Base64 Condition:")
        base64_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_container.addWidget(base64_label)
        
        self.base64_text = QTextEdit()
        self.base64_text.setFont(QFont("Courier New", 10))
        self.base64_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #3E3E3E;
                border-radius: 4px;
            }
        """)
        self.base64_text.setPlaceholderText("Paste Base64 encoded condition here...")
        right_container.addWidget(self.base64_text)
        
        content_layout.addLayout(left_container, 2)
        content_layout.addLayout(middle_container, 0)
        content_layout.addLayout(right_container, 2)
        main_layout.addLayout(content_layout)
    
    def clear_texts(self):
        """Clear both text containers"""
        self.code_text.clear()
        self.base64_text.clear()
    
    def toggle_language(self):
        if self.current_language == "C":
            self.current_language = "Squirrel"
            self.language_button.setText("Switch to C")
            if self.c_highlighter:
                self.c_highlighter.setDocument(None)
            self.squirrel_highlighter = SquirrelSyntaxHighlighter(self.code_text.document())
        else:
            self.current_language = "C"
            self.language_button.setText("Switch to Squirrel")
            if self.squirrel_highlighter:
                self.squirrel_highlighter.setDocument(None)
            self.c_highlighter = CSyntaxHighlighter(self.code_text.document())
        
        self.language_label.setText(f"Current Language: {self.current_language}")
        
        if self.base64_text.toPlainText().strip():
            self.convert_to_code()
    
    def convert_to_code(self):
        base64_data = self.base64_text.toPlainText().strip()
        if not base64_data:
            QMessageBox.warning(self, "No Base64 Data",
                                "Please paste Base64 encoded condition data in the right container.")
            return
        try:
            conditions = Level5ConditionDecoder.from_base64(base64_data)
            generator = CCodeGenerator(conditions) if self.current_language == "C" else SquirrelCodeGenerator(conditions)
            code = generator.generate()
            self.code_text.setPlainText(code)
        except Exception as e:
            QMessageBox.critical(self, "Conversion Failed",
                                 f"Failed to convert Base64 to code:\n{str(e)}")
    
    def convert_to_base64(self):
        QMessageBox.information(self, "Not Implemented",
                                "Code to Base64 conversion is not yet implemented.")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Level5ConditionGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
