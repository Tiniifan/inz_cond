from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class AddItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Item")
        self.setModal(True)
        layout = QFormLayout(self)
        
        self.item_input = QLineEdit()
        layout.addRow("Item:", self.item_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_value(self):
        return self.item_input.text()