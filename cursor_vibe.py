
import sys
import random
import time
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QSlider, QSystemTrayIcon, 
                            QMenu, QAction, QWidget, QCheckBox)
from PyQt5.QtCore import Qt, QSettings, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QPalette, QFont, QFontDatabase
import pyautogui
import winreg as reg
import os
import resources  # Import the resources file

# Define color scheme
COLORS = {
    "primary": "#0ACDFF",
    "primary_dark": "#0095C2",
    "background": "#F8F9FA",
    "card": "#FFFFFF",
    "text": "#212529",
    "text_secondary": "#6C757D",
    "success": "#28A745",
    "danger": "#DC3545",
    "warning": "#FFC107",
    "border": "#DEE2E6",
}

class ModernSlider(QSlider):
    """Custom slider with modern appearance"""
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 6px;
                background: {COLORS["border"]};
                border-radius: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background: {COLORS["primary"]};
                border: none;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            
            QSlider::handle:horizontal:hover {{
                background: {COLORS["primary_dark"]};
            }}
        """)

class ModernButton(QPushButton):
    """Custom button with modern appearance"""
    
    def __init__(self, text, parent=None, primary=True):
        super().__init__(text, parent)
        self.primary = primary
        self.update_style()
        
    def update_style(self):
        if self.primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS["primary"]};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {COLORS["primary_dark"]};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS["primary_dark"]};
                }}
                QPushButton:disabled {{
                    background-color: {COLORS["border"]};
                    color: {COLORS["text_secondary"]};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS["card"]};
                    color: {COLORS["primary"]};
                    border: 1px solid {COLORS["primary"]};
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {COLORS["background"]};
                }}
                QPushButton:pressed {{
                    background-color: {COLORS["background"]};
                }}
                QPushButton:disabled {{
                    background-color: {COLORS["card"]};
                    color: {COLORS["border"]};
                    border: 1px solid {COLORS["border"]};
                }}
            """)

class ModernCheckBox(QCheckBox):
    """Custom checkbox with modern appearance"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QCheckBox {{
                spacing: 8px;
                color: {COLORS["text"]};
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 3px;
                border: 1px solid {COLORS["border"]};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {COLORS["primary"]};
                border: 1px solid {COLORS["primary"]};
                image: url(:/icons/check.svg);
            }}
            
            QCheckBox::indicator:unchecked:hover {{
                border: 1px solid {COLORS["primary"]};
            }}
        """)

class CardWidget(QWidget):
    """Widget with card-like appearance"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            CardWidget {{
                background-color: {COLORS["card"]};
                border-radius: 8px;
                border: 1px solid {COLORS["border"]};
            }}
        """)

class StatusIndicator(QLabel):
    """Custom status indicator"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = False
        self.setFixedSize(12, 12)
        
    def setActive(self, active):
        self.active = active
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.active:
            color = QColor(COLORS["success"])
        else:
            color = QColor(COLORS["danger"])
            
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 12, 12)
        painter.end()

class CursorVibe(QMainWindow):
    """Main window class for the CursorVibe application."""
    
    def __init__(self):
        super().__init__()
        
        # Load custom fonts
        self.load_fonts()
        
        # Initialize settings
        self.settings = QSettings("CursorVibe", "CursorVibe")
        
        # Set up variables
        self.is_active = False
        self.last_activity_time = time.time()
        self.thread = None
        self.stop_thread = False
        
        # Default settings
        self.movement_frequency = self.settings.value("frequency", 1.0, type=float)  # in seconds
        self.movement_distance = self.settings.value("distance", 2, type=int)  # in pixels
        self.idle_threshold = self.settings.value("idle_threshold", 3, type=int)  # in seconds
        self.run_on_startup = self.settings.value("run_on_startup", False, type=bool)
        
        # Set up UI
        self.init_ui()
        self.setup_system_tray()
        
        # Set up mouse position monitoring
        self.last_mouse_position = pyautogui.position()
        self.mouse_monitor_timer = QTimer(self)
        self.mouse_monitor_timer.timeout.connect(self.check_mouse_activity)
        self.mouse_monitor_timer.start(500)  # Check every 500ms
        
        # Apply run on startup setting
        self.update_startup_registry()
    
    def load_fonts(self):
        """Load custom fonts for the application."""
        # Note: In a real application, you would include font files in your resources
        pass
    
    def init_ui(self):
        """Initialize the user interface components."""
        self.setWindowTitle("CursorVibe")
        self.setFixedSize(420, 500)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS["background"]};
                color: {COLORS["text"]};
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel {{
                color: {COLORS["text"]};
            }}
        """)
        
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # Header with logo and title
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap(":/icons/cursor.png")
        logo_label.setPixmap(logo_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        title_layout = QVBoxLayout()
        title_label = QLabel("CursorVibe")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        subtitle_label = QLabel("Keep your workflow alive")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setStyleSheet(f"color: {COLORS['text_secondary']}")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        header_layout.addWidget(logo_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Status card
        status_card = CardWidget()
        status_layout = QVBoxLayout(status_card)
        
        # Status header
        status_header = QHBoxLayout()
        status_title = QLabel("Status")
        status_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        self.status_indicator = StatusIndicator()
        self.status_text = QLabel("Inactive")
        self.status_text.setStyleSheet(f"color: {COLORS['text_secondary']}")
        
        status_header.addWidget(status_title)
        status_header.addStretch()
        status_header.addWidget(self.status_indicator)
        status_header.addWidget(self.status_text)
        
        # Toggle button
        self.toggle_button = ModernButton("Go, Mouse, Go!")
        self.toggle_button.clicked.connect(self.toggle_simulation)
        
        status_layout.addLayout(status_header)
        status_layout.addWidget(self.toggle_button)
        status_layout.setContentsMargins(16, 16, 16, 16)
        
        # Settings card
        settings_card = CardWidget()
        settings_layout = QVBoxLayout(settings_card)
        settings_layout.setContentsMargins(16, 16, 16, 16)
        settings_layout.setSpacing(20)
        
        settings_title = QLabel("Settings")
        settings_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        settings_layout.addWidget(settings_title)
        
        # Frequency slider
        freq_layout = QVBoxLayout()
        freq_header = QHBoxLayout()
        freq_label = QLabel("Check Frequency")
        self.freq_value = QLabel(f"{self.movement_frequency:.1f}s")
        self.freq_value.setStyleSheet(f"color: {COLORS['primary']}")
        
        freq_header.addWidget(freq_label)
        freq_header.addStretch()
        freq_header.addWidget(self.freq_value)
        
        self.freq_slider = ModernSlider(Qt.Horizontal)
        self.freq_slider.setRange(1, 30)  # 0.1 to 3.0 seconds (multiplied by 10)
        self.freq_slider.setValue(int(self.movement_frequency * 10))
        
        self.freq_slider.valueChanged.connect(
            lambda value: self.update_frequency(value/10)
        )
        self.freq_slider.valueChanged.connect(
            lambda value: self.freq_value.setText(f"{value/10:.1f}s")
        )
        
        freq_desc = QLabel("How often CursorVibe checks if movement is needed")
        freq_desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px")
        
        freq_layout.addLayout(freq_header)
        freq_layout.addWidget(self.freq_slider)
        freq_layout.addWidget(freq_desc)
        settings_layout.addLayout(freq_layout)
        
        # Distance slider
        dist_layout = QVBoxLayout()
        dist_header = QHBoxLayout()
        dist_label = QLabel("Movement Distance")
        self.dist_value = QLabel(f"{self.movement_distance}px")
        self.dist_value.setStyleSheet(f"color: {COLORS['primary']}")
        
        dist_header.addWidget(dist_label)
        dist_header.addStretch()
        dist_header.addWidget(self.dist_value)
        
        self.dist_slider = ModernSlider(Qt.Horizontal)
        self.dist_slider.setRange(1, 10)  # 1 to 10 pixels
        self.dist_slider.setValue(self.movement_distance)
        
        self.dist_slider.valueChanged.connect(
            lambda value: self.update_distance(value)
        )
        self.dist_slider.valueChanged.connect(
            lambda value: self.dist_value.setText(f"{value}px")
        )
        
        dist_desc = QLabel("How far the cursor moves each time")
        dist_desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px")
        
        dist_layout.addLayout(dist_header)
        dist_layout.addWidget(self.dist_slider)
        dist_layout.addWidget(dist_desc)
        settings_layout.addLayout(dist_layout)
        
        # Idle threshold slider
        idle_layout = QVBoxLayout()
        idle_header = QHBoxLayout()
        idle_label = QLabel("Idle Threshold")
        self.idle_value = QLabel(f"{self.idle_threshold}s")
        self.idle_value.setStyleSheet(f"color: {COLORS['primary']}")
        
        idle_header.addWidget(idle_label)
        idle_header.addStretch()
        idle_header.addWidget(self.idle_value)
        
        self.idle_slider = ModernSlider(Qt.Horizontal)
        self.idle_slider.setRange(1, 10)  # 1 to 10 seconds
        self.idle_slider.setValue(self.idle_threshold)
        
        self.idle_slider.valueChanged.connect(
            lambda value: self.update_idle_threshold(value)
        )
        self.idle_slider.valueChanged.connect(
            lambda value: self.idle_value.setText(f"{value}s")
        )
        
        idle_desc = QLabel("Seconds of inactivity before cursor movement begins")
        idle_desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px")
        
        idle_layout.addLayout(idle_header)
        idle_layout.addWidget(self.idle_slider)
        idle_layout.addWidget(idle_desc)
        settings_layout.addLayout(idle_layout)
        
        # Run on startup checkbox
        startup_layout = QHBoxLayout()
        self.startup_checkbox = ModernCheckBox("Run on startup")
        self.startup_checkbox.setChecked(self.run_on_startup)
        self.startup_checkbox.stateChanged.connect(self.toggle_run_on_startup)
        
        startup_layout.addWidget(self.startup_checkbox)
        startup_layout.addStretch()
        settings_layout.addLayout(startup_layout)
        
        # Add all components to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(status_card)
        main_layout.addWidget(settings_card)
        main_layout.addStretch()
        
        # Add a footer
        footer_label = QLabel("© 2025 CursorVibe")
        footer_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px")
        footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer_label)
        
        # Show the window
        self.center()
        self.show()
    
    def setup_system_tray(self):
        """Set up the system tray icon and menu."""
        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set icon
        icon = QIcon(":/icons/cursor.png")
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("CursorVibe")
        
        # Create the tray menu
        tray_menu = QMenu()
        tray_menu.setStyleSheet(f"""
            QMenu {{
                background-color: {COLORS["card"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 4px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 25px 6px 20px;
                border-radius: 3px;
                margin: 2px;
            }}
            QMenu::item:selected {{
                background-color: {COLORS["primary"]};
                color: white;
            }}
        """)
        
        # Add actions to the menu
        status_action = QAction("Status: Inactive", self)
        status_action.setEnabled(False)
        tray_menu.addAction(status_action)
        
        tray_menu.addSeparator()
        
        self.toggle_action = QAction("Start", self)
        self.toggle_action.triggered.connect(self.toggle_simulation)
        tray_menu.addAction(self.toggle_action)
        
        show_action = QAction("Show Settings", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close_app)
        tray_menu.addAction(quit_action)
        
        # Set the menu for the tray icon
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Connect the activated signal
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Save status action for later updates
        self.status_action = status_action
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
    
    def center(self):
        """Center the window on the screen."""
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def update_frequency(self, value):
        """Update the movement frequency setting."""
        self.movement_frequency = value
        self.settings.setValue("frequency", value)
    
    def update_distance(self, value):
        """Update the movement distance setting."""
        self.movement_distance = value
        self.settings.setValue("distance", value)
    
    def update_idle_threshold(self, value):
        """Update the idle threshold setting."""
        self.idle_threshold = value
        self.settings.setValue("idle_threshold", value)
    
    def toggle_run_on_startup(self, state):
        """Toggle the run on startup setting."""
        self.run_on_startup = (state == Qt.Checked)
        self.settings.setValue("run_on_startup", self.run_on_startup)
        self.update_startup_registry()
    
    def update_startup_registry(self):
        """Update the Windows registry for startup."""
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
            
            if self.run_on_startup:
                # Get the path of the current script
                app_path = os.path.abspath(sys.argv[0])
                reg.SetValueEx(key, "CursorVibe", 0, reg.REG_SZ, app_path)
            else:
                try:
                    reg.DeleteValue(key, "CursorVibe")
                except FileNotFoundError:
                    pass  # Key doesn't exist, which is fine
            
            reg.CloseKey(key)
        except Exception as e:
            print(f"Error updating registry: {e}")
    
    def check_mouse_activity(self):
        """Check if the user has moved the mouse."""
        current_position = pyautogui.position()
        if current_position != self.last_mouse_position:
            self.last_activity_time = time.time()
            self.last_mouse_position = current_position
    
    def is_user_idle(self):
        """Check if the user has been idle for longer than the threshold."""
        idle_time = time.time() - self.last_activity_time
        return idle_time >= self.idle_threshold
    
    def simulate_cursor_movement(self):
        """Simulate small random cursor movements."""
        while not self.stop_thread:
            if self.is_user_idle():
                # Get current cursor position
                current_x, current_y = pyautogui.position()
                
                # Calculate small random movement
                random_x = random.randint(-self.movement_distance, self.movement_distance)
                random_y = random.randint(-self.movement_distance, self.movement_distance)
                
                # Move cursor
                pyautogui.moveTo(current_x + random_x, current_y + random_y)
                print(f"Moved cursor by ({random_x}, {random_y}) pixels")
            
            # Wait for the next movement
            time.sleep(self.movement_frequency)
    
    def toggle_simulation(self):
        """Toggle the cursor movement simulation on/off."""
        if not self.is_active:
            # Start simulation
            self.is_active = True
            self.status_text.setText("Active")
            self.status_indicator.setActive(True)
            self.toggle_button.setText("Hold the Mouse Back")
            self.toggle_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS["danger"]};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #C82333;
                }}
                QPushButton:pressed {{
                    background-color: #BD2130;
                }}
            """)
            self.toggle_action.setText("Stop")
            self.status_action.setText("Status: Active")
            
            # Start the simulation thread
            self.stop_thread = False
            self.thread = threading.Thread(target=self.simulate_cursor_movement)
            self.thread.daemon = True
            self.thread.start()
        else:
            # Stop simulation
            self.is_active = False
            self.status_text.setText("Inactive")
            self.status_indicator.setActive(False)
            self.toggle_button.setText("Go, Mouse, Go!")
            self.toggle_button.setStyleSheet("")
            self.toggle_button.update_style()  # Reset button style
            self.toggle_action.setText("Start")
            self.status_action.setText("Status: Inactive")
            
            # Stop the simulation thread
            self.stop_thread = True
            if self.thread:
                self.thread.join(timeout=1)
    
    def closeEvent(self, event):
        """Handle window close event."""
        event.ignore()
        self.hide()
    
    def close_app(self):
        """Close the application completely."""
        if self.thread and self.thread.is_alive():
            self.stop_thread = True
            self.thread.join(timeout=1)
        
        self.tray_icon.hide()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    cursor_vibe = CursorVibe()
    sys.exit(app.exec_())

