import sys
import argparse

from PyQt6.QtWidgets import QApplication
from gui import InzCondGUI

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='INZ Cond GUI Editor')
    parser.add_argument('-o', '--output', action='store_true', 
                        help='Enable output mode (prints base64 on exit)')
    parser.add_argument('base64', nargs='?', default=None,
                        help='Initial base64 string (optional)')
    
    args = parser.parse_args()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = InzCondGUI(initial_base64=args.base64, output_mode=args.output)
    window.show()
    
    sys.exit(app.exec())