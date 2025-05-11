
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import CursorVibe
import resources  # Import the resources file

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    cursor_vibe = CursorVibe()
    sys.exit(app.exec_())
