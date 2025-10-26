from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class CodeEditorWidget(QWidget):
    decode_requested = pyqtSignal()
    encode_requested = pyqtSignal()
    try_requested = pyqtSignal()
    language_changed = pyqtSignal(str)
    code_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1E1E1E;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Base64 bar
        self._create_base64_bar()
        layout.addWidget(self.base64_bar)
        
        # Text editor
        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Courier New", 11))
        self.code_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding: 10px;
            }
        """)
        self.code_editor.setPlaceholderText("The generated code will appear here or write code here...")
        self.code_editor.textChanged.connect(lambda: self.code_changed.emit(self.code_editor.toPlainText()))
        layout.addWidget(self.code_editor)
    
    def _create_base64_bar(self):
        """Creates the bar with the Base64 and Language controls"""
        self.base64_bar = QWidget()
        self.base64_bar.setFixedHeight(75)
        self.base64_bar.setStyleSheet("background-color: #2D2D30;")
        base64_bar_layout = QVBoxLayout(self.base64_bar)
        base64_bar_layout.setContentsMargins(8, 5, 8, 5)
        base64_bar_layout.setSpacing(5)
        
        # First line: Base64 input and buttons
        first_line = QHBoxLayout()
        first_line.setSpacing(8)
        
        base64_label = QLabel("Base64:")
        base64_label.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        first_line.addWidget(base64_label)
        
        self.base64_input = QLineEdit()
        self.base64_input.setPlaceholderText("Paste Base64 encoded condition here...")
        self.base64_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                color: #CCCCCC;
                border: 1px solid #3E3E3E;
                padding: 5px;
                font-family: 'Courier New';
                font-size: 11px;
            }
        """)
        first_line.addWidget(self.base64_input)
        
        self.decode_button = QPushButton("Base64 → Code")
        self.decode_button.setStyleSheet("""
            QPushButton {
                background-color: #0E639C;
                color: white;
                border: none;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1177BB; }
        """)
        self.decode_button.clicked.connect(self.decode_requested.emit)
        first_line.addWidget(self.decode_button)
        
        self.encode_button = QPushButton("Code → Base64")
        self.encode_button.setStyleSheet("""
            QPushButton {
                background-color: #0E639C;
                color: white;
                border: none;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #1177BB; }
        """)
        self.encode_button.clicked.connect(self.encode_requested.emit)
        first_line.addWidget(self.encode_button)
        
        self.try_button = QPushButton("Try")
        self.try_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #32C252; }
        """)
        self.try_button.clicked.connect(self.try_requested.emit)
        first_line.addWidget(self.try_button)
        
        base64_bar_layout.addLayout(first_line)
        
        # Second line: Language selector
        second_line = QHBoxLayout()
        second_line.setSpacing(8)
        
        language_label = QLabel("Language:")
        language_label.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        language_label.setFixedWidth(base64_label.sizeHint().width())
        second_line.addWidget(language_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["C", "Squirrel"])
        self.language_combo.setStyleSheet("""
            QComboBox {
                background-color: #3C3C3C;
                color: #CCCCCC;
                border: 1px solid #3E3E3E;
                padding: 5px;
                font-size: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #1E1E1E;
                color: white;
                selection-background-color: #4DD0E1;
            }
        """)
        self.language_combo.setFixedWidth(150)
        self.language_combo.currentTextChanged.connect(self.language_changed.emit)
        second_line.addWidget(self.language_combo)
        
        second_line.addStretch()
        base64_bar_layout.addLayout(second_line)
    
    def get_code(self):
        """Returns the current code"""
        return self.code_editor.toPlainText()
    
    def set_code(self, code, block_signals=False):
        """Defines the code"""
        if block_signals:
            self.code_editor.blockSignals(True)

        self.code_editor.setPlainText(code)

        if block_signals:
            self.code_editor.blockSignals(False)
    
    def get_base64(self):
        """Returns the current base64"""
        return self.base64_input.text().strip()
    
    def set_base64(self, base64_data):
        """Defines base64"""
        self.base64_input.setText(base64_data)
    
    def get_language(self):
        """Returns the current language"""
        return self.language_combo.currentText()
    
    def clear(self):
        """Delete content"""
        self.code_editor.clear()
        self.base64_input.clear()