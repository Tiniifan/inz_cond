import sys

from PyQt6.QtWidgets import QApplication
from gui import InzCondGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Check if a base64 string has been passed as an argument
    initial_base64 = None
    if len(sys.argv) > 1:
        initial_base64 = sys.argv[1]
    
    window = InzCondGUI(initial_base64=initial_base64)
    window.show()
    
    sys.exit(app.exec())