
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class SystemTrayService:
    """Service for managing the system tray icon and menu"""
    
    def __init__(self, parent=None):
        self.parent = parent
        
        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(parent)
        
        # Set icon
        icon = QIcon(":/icons/cursor.png")
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("CursorVibe")
        
        # Create the tray menu
        self.tray_menu = QMenu()
        self.setup_menu()
        
        # Set the menu for the tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
    
    def setup_menu(self):
        """Set up the system tray menu"""
        # Define colors for menu styling
        colors = {
            "card": "#FFFFFF",
            "border": "#DEE2E6",
            "primary": "#0ACDFF",
        }
        
        self.tray_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {colors["card"]};
                border: 1px solid {colors["border"]};
                border-radius: 4px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 25px 6px 20px;
                border-radius: 3px;
                margin: 2px;
            }}
            QMenu::item:selected {{
                background-color: {colors["primary"]};
                color: white;
            }}
        """)
        
        # Add actions to the menu
        self.status_action = QAction("Status: Inactive", self.parent)
        self.status_action.setEnabled(False)
        self.tray_menu.addAction(self.status_action)
        
        self.tray_menu.addSeparator()
        
        self.toggle_action = QAction("Start", self.parent)
        self.tray_menu.addAction(self.toggle_action)
        
        self.show_action = QAction("Show Settings", self.parent)
        self.tray_menu.addAction(self.show_action)
        
        self.tray_menu.addSeparator()
        
        self.quit_action = QAction("Quit", self.parent)
        self.tray_menu.addAction(self.quit_action)
    
    def update_status(self, is_active):
        """Update the status text in the menu"""
        if is_active:
            self.status_action.setText("Status: Active")
            self.toggle_action.setText("Stop")
        else:
            self.status_action.setText("Status: Inactive")
            self.toggle_action.setText("Start")
    
    def connect_signals(self, toggle_callback, show_callback, quit_callback):
        """Connect menu actions to callbacks"""
        self.toggle_action.triggered.connect(toggle_callback)
        self.show_action.triggered.connect(show_callback)
        self.quit_action.triggered.connect(quit_callback)
        self.tray_icon.activated.connect(self.icon_activated)
    
    def icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            # Show the main window when the tray icon is double-clicked
            if self.parent and hasattr(self.parent, 'show'):
                self.parent.show()
