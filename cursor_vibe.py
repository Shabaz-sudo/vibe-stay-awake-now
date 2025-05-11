
import sys
import random
import time
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QSlider, QSystemTrayIcon, 
                            QMenu, QAction, QWidget, QCheckBox)
from PyQt5.QtCore import Qt, QSettings, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
import pyautogui
import winreg as reg
import os

class CursorVibe(QMainWindow):
    """Main window class for the CursorVibe application."""
    
    def __init__(self):
        super().__init__()
        
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
    
    def init_ui(self):
        """Initialize the user interface components."""
        self.setWindowTitle("CursorVibe - Prevent System Sleep")
        self.setFixedSize(400, 300)
        
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add tagline
        tagline = QLabel("Keep your workflow alive")
        tagline.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(tagline)
        
        # Frequency slider
        freq_layout = QVBoxLayout()
        freq_label = QLabel(f"Check Frequency: {self.movement_frequency:.1f} seconds")
        self.freq_slider = QSlider(Qt.Horizontal)
        self.freq_slider.setRange(1, 20)  # 0.1 to 2.0 seconds (multiplied by 10)
        self.freq_slider.setValue(int(self.movement_frequency * 10))
        self.freq_slider.valueChanged.connect(
            lambda value: self.update_frequency(value/10)
        )
        self.freq_slider.valueChanged.connect(
            lambda value: freq_label.setText(f"Check Frequency: {value/10:.1f} seconds")
        )
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.freq_slider)
        main_layout.addLayout(freq_layout)
        
        # Distance slider
        dist_layout = QVBoxLayout()
        dist_label = QLabel(f"Movement Distance: {self.movement_distance} pixels")
        self.dist_slider = QSlider(Qt.Horizontal)
        self.dist_slider.setRange(1, 10)  # 1 to 10 pixels
        self.dist_slider.setValue(self.movement_distance)
        self.dist_slider.valueChanged.connect(
            lambda value: self.update_distance(value)
        )
        self.dist_slider.valueChanged.connect(
            lambda value: dist_label.setText(f"Movement Distance: {value} pixels")
        )
        dist_layout.addWidget(dist_label)
        dist_layout.addWidget(self.dist_slider)
        main_layout.addLayout(dist_layout)
        
        # Idle threshold slider
        idle_layout = QVBoxLayout()
        idle_label = QLabel(f"Idle Threshold: {self.idle_threshold} seconds")
        self.idle_slider = QSlider(Qt.Horizontal)
        self.idle_slider.setRange(1, 10)  # 1 to 10 seconds
        self.idle_slider.setValue(self.idle_threshold)
        self.idle_slider.valueChanged.connect(
            lambda value: self.update_idle_threshold(value)
        )
        self.idle_slider.valueChanged.connect(
            lambda value: idle_label.setText(f"Idle Threshold: {value} seconds")
        )
        idle_layout.addWidget(idle_label)
        idle_layout.addWidget(self.idle_slider)
        main_layout.addLayout(idle_layout)
        
        # Run on startup checkbox
        startup_layout = QHBoxLayout()
        self.startup_checkbox = QCheckBox("Run on startup")
        self.startup_checkbox.setChecked(self.run_on_startup)
        self.startup_checkbox.stateChanged.connect(self.toggle_run_on_startup)
        startup_layout.addWidget(self.startup_checkbox)
        main_layout.addLayout(startup_layout)
        
        # Status indicators
        self.status_label = QLabel("Status: Inactive")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Toggle button
        self.toggle_button = QPushButton("Go, Mouse, Go!")
        self.toggle_button.clicked.connect(self.toggle_simulation)
        main_layout.addWidget(self.toggle_button)
        
        # Show the window
        self.center()
        self.show()
    
    def setup_system_tray(self):
        """Set up the system tray icon and menu."""
        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("CursorVibe")
        
        # Create a simple icon (a filled circle)
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        self.tray_icon.setIcon(QIcon(pixmap))
        
        # Create the tray menu
        tray_menu = QMenu()
        
        # Add actions to the menu
        self.toggle_action = QAction("Start", self)
        self.toggle_action.triggered.connect(self.toggle_simulation)
        tray_menu.addAction(self.toggle_action)
        
        show_action = QAction("Show Settings", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close_app)
        tray_menu.addAction(quit_action)
        
        # Set the menu for the tray icon
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Connect the activated signal
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
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
            self.status_label.setText("Status: Active")
            self.toggle_button.setText("Hold the Mouse Back")
            self.toggle_action.setText("Stop")
            
            # Start the simulation thread
            self.stop_thread = False
            self.thread = threading.Thread(target=self.simulate_cursor_movement)
            self.thread.daemon = True
            self.thread.start()
        else:
            # Stop simulation
            self.is_active = False
            self.status_label.setText("Status: Inactive")
            self.toggle_button.setText("Go, Mouse, Go!")
            self.toggle_action.setText("Start")
            
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
    app.setQuitOnLastWindowClosed(False)  # Prevent app from quitting when window is closed
    cursor_vibe = CursorVibe()
    sys.exit(app.exec_())
