from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

from gui.widgets import FileExplorer, CodeEditorWidget, PlaygroundPanel
from gui.controllers import FileController, CodeController

from languages.c_language.c_syntaxhighlighter import CSyntaxHighlighter
from languages.squirrel_language.squirrel_syntaxhighlighter import SquirrelSyntaxHighlighter

class InzCondGUI(QMainWindow):
    def __init__(self, initial_base64=None):
        super().__init__()
        
        # Controllers
        self.file_controller = FileController()
        self.code_controller = CodeController()
        
        # Status
        self.initial_base64 = initial_base64
        self.current_language = "C"
        self.c_highlighter = None
        self.squirrel_highlighter = None
        
        # Load data
        self.file_controller.load_templates()
        self.file_controller.load_or_create_playground_data()
        
        # Initialize the UI
        self.init_ui()
                
        # If an initial base64 is provided
        if self.initial_base64:
            self.editor_widget.set_base64(self.initial_base64)
            self._on_decode_requested()
    
    def init_ui(self):
        """Initializes the user interface"""
        self.setWindowTitle("inz_cond.py")
        self.setGeometry(100, 100, 1600, 900)
        
        # Dark theme
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(20, 20, 20))
        self.setPalette(palette)
        
        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main area with splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # File Explorer
        self.file_explorer = FileExplorer()
        self.file_explorer.file_selected.connect(self._on_file_selected)
        self.file_explorer.load_tree(self.file_controller.templates)
        content_splitter.addWidget(self.file_explorer)
        
        # Code Editor
        self.editor_widget = CodeEditorWidget()
        self.editor_widget.decode_requested.connect(self._on_decode_requested)
        self.editor_widget.encode_requested.connect(self._on_encode_requested)
        self.editor_widget.try_requested.connect(self._on_try_requested)
        self.editor_widget.language_changed.connect(self._on_language_changed)
        self.editor_widget.code_changed.connect(self._on_code_changed)
        self.c_highlighter = CSyntaxHighlighter(self.editor_widget.code_editor.document())
        content_splitter.addWidget(self.editor_widget)
        
        content_splitter.setStretchFactor(1, 1)
        main_layout.addWidget(content_splitter)
        
        # Playground Panel
        self.playground_panel = PlaygroundPanel()
        self.playground_panel.load_data(self.file_controller.playground_data)
        self.playground_panel.data_changed.connect(self._on_playground_data_changed)
        main_layout.addWidget(self.playground_panel)
        
        # Footer
        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(25)
        bottom_bar.setStyleSheet("""
            background-color: #007ACC;
            border-top: 1px solid #005A99;
        """)
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar_layout.setContentsMargins(10, 0, 10, 0)
        
        version_label = QLabel("v1.0")
        version_label.setStyleSheet("color: white; font-size: 11px;")
        bottom_bar_layout.addStretch()
        bottom_bar_layout.addWidget(version_label)
        main_layout.addWidget(bottom_bar)
        
    def _on_file_selected(self, file_path):
        """Manages file selection"""
        # Change the current file
        self.file_controller.current_file = file_path
        is_playground = self.file_controller.is_playground(file_path)
        
        # If it's playground and there is content in memory
        if is_playground:
            memory_code = self.file_controller.load_from_memory(file_path)
            if memory_code is not None:
                self.editor_widget.set_code(memory_code, block_signals=True)
                return
        
        # Load from disk
        content = self.file_controller.load_file_content(file_path)
        
        if content is None:
            QMessageBox.critical(self, "Error", "Failed to load file")
            return
        
        if not is_playground or content:
            self.editor_widget.set_base64(content)
            if content:
                self._on_decode_requested()
            else:
                self.editor_widget.clear()
        else:
            self.editor_widget.clear()
    
    def _on_code_changed(self, code):
        """Manages code changes"""
        if self.file_controller.current_file:
            self.file_controller.save_to_memory(self.file_controller.current_file, code)
    
    def _on_decode_requested(self):
        """Manages decoding requests"""
        base64_data = self.editor_widget.get_base64()
        if not base64_data:
            QMessageBox.warning(self, "No Base64 Data", "Please enter Base64 encoded condition data.")
            return
        
        code, error = self.code_controller.decode_base64(base64_data, self.current_language)
        if error:
            QMessageBox.critical(self, "Decode Error", f"Failed to decode Base64:\n{error}")
            return
        
        self.editor_widget.set_code(code, block_signals=True)
        
        # Update memory
        if self.file_controller.current_file:
            self.file_controller.save_to_memory(self.file_controller.current_file, code)
    
    def _on_encode_requested(self):
        """Manages encoding requests"""
        code = self.editor_widget.get_code().strip()
        if not code:
            QMessageBox.warning(self, "No Code", "Please enter code in the editor.")
            return
        
        encoded, error = self.code_controller.encode_code(code, self.current_language)
        if error:
            QMessageBox.critical(self, "Encode Error", f"Failed to encode code:\n{error}")
            return
        
        self.editor_widget.set_base64(encoded)
        QMessageBox.information(self, "Success", "Code successfully encoded to Base64.")
    
    def _on_try_requested(self):
        """Manages test requests"""
        code = self.editor_widget.get_code().strip()
        if not code:
            QMessageBox.warning(self, "No Code", "Please enter code in the editor.")
            return
        
        result_str, error = self.code_controller.try_condition(
            code, 
            self.current_language, 
            self.file_controller.playground_data
        )
        
        if error:
            QMessageBox.critical(self, "Error", f"Failed to test condition:\n{error}")
            return
        
        # Display the result
        if result_str.lower() in ("true", "1"):
            QMessageBox.information(self, "Condition Result", "TRUE")
        elif result_str.lower() in ("false", "0"):
            QMessageBox.information(self, "Condition Result", "FALSE")
        elif result_str == "":
            QMessageBox.warning(self, "No Output", "Program executed but produced no visible output.")
        else:
            QMessageBox.information(self, "Program Output", f"Output:\n{result_str}")
    
    def _on_language_changed(self, language):
        """Manages language change"""
        current_code = self.editor_widget.get_code().strip()
        old_language = self.current_language
        self.current_language = language
        
        # Change the syntax highlighter
        if language == "C":
            if self.squirrel_highlighter:
                self.squirrel_highlighter.setDocument(None)
            self.c_highlighter = CSyntaxHighlighter(self.editor_widget.code_editor.document())
        else:
            if self.c_highlighter:
                self.c_highlighter.setDocument(None)
            self.squirrel_highlighter = SquirrelSyntaxHighlighter(self.editor_widget.code_editor.document())
        
        # Convert the code
        if current_code:
            converted_code, error = self.code_controller.translate_code(current_code, old_language, language)
            if error:
                QMessageBox.warning(self, "Conversion Error", 
                                  f"Failed to convert code to {language}:\n{error}\n\n"
                                  f"The code will remain as is.")
                return
            
            self.editor_widget.set_code(converted_code, block_signals=True)
            
            # Update memory
            if self.file_controller.current_file:
                self.file_controller.save_to_memory(self.file_controller.current_file, converted_code)
    
    def _on_playground_data_changed(self, data):
        """Manages changes to playground data"""
        result = self.file_controller.save_playground_data(data)
        if result is not True:
            QMessageBox.critical(self, "Save Error", f"Failed to save playground.json:\n{result[1]}")
    
    def closeEvent(self, event):
        """Manages the closing of the application"""
        try:
            code = self.editor_widget.get_code().strip()
            
            # If launched with an initial base64, we want to get the new base64
            if self.initial_base64 is not None and code:           
                encoded, error = self.code_controller.encode_code(code, self.current_language)

                if encoded:
                    print(encoded)
                else:
                    print(self.initial_base64)

        except Exception:
            pass
        
        event.accept()