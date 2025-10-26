from PyQt6.QtWidgets import QDialog, QFormLayout, QSpinBox, QCheckBox, QDialogButtonBox

class AddFlagDialog(QDialog):
    def __init__(self, parent=None, title="Add Flag"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        layout = QFormLayout(self)
        
        self.key_input = QSpinBox()
        self.key_input.setRange(0, 999999)
        layout.addRow("Key:", self.key_input)
        
        self.value_input = QCheckBox()
        self.value_input.setChecked(True)
        layout.addRow("Value:", self.value_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_values(self):
        return self.key_input.value(), self.value_input.isChecked()