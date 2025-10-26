from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal

class FileExplorer(QWidget):
    # Signal emitted when a file is selected
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #252526;")
        self.setMaximumWidth(250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Label
        explorer_label = QLabel("FILE EXPLORER")
        explorer_label.setStyleSheet("color: #CCCCCC; font-size: 11px; font-weight: bold; padding: 5px;")
        layout.addWidget(explorer_label)
        
        # Tree widget
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #1E1E1E;
                color: #CCCCCC;
                border: none;
            }
            QTreeWidget::item:hover { background-color: #2A2D2E; }
            QTreeWidget::item:selected { background-color: #37373D; }
        """)
        self.file_tree.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.file_tree)
    
    def _on_item_clicked(self, item, column):
        """Manages clicking on an item"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        
        # If it is a folder, do nothing
        if file_path is None:
            return
            
        if Path(file_path).is_file() or file_path.endswith("playground.inzcond"):
            self.file_selected.emit(file_path)
    
    def load_tree(self, templates):
        """Loads the file tree"""
        self.file_tree.clear()
        root_path = Path.cwd()
        
        # Add playground.inzcond
        playground_item = QTreeWidgetItem(self.file_tree)
        playground_item.setText(0, "playground.inzcond")
        playground_item.setData(0, Qt.ItemDataRole.UserRole, str(root_path / "playground.inzcond"))
        
        # Add the templates folder if it exists
        templates_dir = root_path / "templates"
        if templates_dir.exists() and templates_dir.is_dir() and templates:
            templates_item = QTreeWidgetItem(self.file_tree)
            templates_item.setText(0, "templates")
            templates_item.setData(0, Qt.ItemDataRole.UserRole, None)
            
            # Add each template
            for template_name, template_data in sorted(templates.items()):
                template_item = QTreeWidgetItem(templates_item)
                template_item.setText(0, template_name)
                template_item.setData(0, Qt.ItemDataRole.UserRole, template_data['path'])
            
            templates_item.setExpanded(True)