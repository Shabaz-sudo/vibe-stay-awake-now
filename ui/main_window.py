
import sys
from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, 
                            QWidget, QApplication, QTimer)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

from ui.custom_widgets import (ModernSlider, ModernButton, ModernCheckBox, 
                              CardWidget, StatusIndicator, COLORS)
from services.cursor_service import CursorService
from services.settings_service import SettingsService
from services.system_tray import SystemTrayService

class CursorVibe(QMainWindow):
    """Main window class for the CursorVibe application."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize services
        self.settings_service = SettingsService()
        self.cursor_service = CursorService()
        
        # Initialize UI
        self.init_ui()
        
        # Initialize system tray
        self.system_tray = SystemTrayService(self)
        self.system_tray.connect_signals(
            toggle_callback=self.toggle_simulation,
            show_callback=self.show,
            quit_callback=self.close_app
        )
        
        # Apply settings to cursor service
        settings = self.settings_service.get_all_settings()
        self.cursor_service.update_settings(
            frequency=settings["movement_frequency"],
            distance=settings["movement_distance"],
            idle_threshold=settings["idle_threshold"]
        )
        
        # Set up mouse position monitoring
        self.mouse_monitor_timer = QTimer(self)
        self.mouse_monitor_timer.timeout.connect(self.cursor_service.check_mouse_activity)
        self.mouse_monitor_timer.start(500)  # Check every 500ms
    
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
        self.freq_value = QLabel(f"{self.settings_service.movement_frequency:.1f}s")
        self.freq_value.setStyleSheet(f"color: {COLORS['primary']}")
        
        freq_header.addWidget(freq_label)
        freq_header.addStretch()
        freq_header.addWidget(self.freq_value)
        
        self.freq_slider = ModernSlider(Qt.Horizontal)
        self.freq_slider.setRange(1, 30)  # 0.1 to 3.0 seconds (multiplied by 10)
        self.freq_slider.setValue(int(self.settings_service.movement_frequency * 10))
        
        self.freq_slider.valueChanged.connect(self.update_frequency)
        
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
        self.dist_value = QLabel(f"{self.settings_service.movement_distance}px")
        self.dist_value.setStyleSheet(f"color: {COLORS['primary']}")
        
        dist_header.addWidget(dist_label)
        dist_header.addStretch()
        dist_header.addWidget(self.dist_value)
        
        self.dist_slider = ModernSlider(Qt.Horizontal)
        self.dist_slider.setRange(1, 10)  # 1 to 10 pixels
        self.dist_slider.setValue(self.settings_service.movement_distance)
        
        self.dist_slider.valueChanged.connect(self.update_distance)
        
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
        self.idle_value = QLabel(f"{self.settings_service.idle_threshold}s")
        self.idle_value.setStyleSheet(f"color: {COLORS['primary']}")
        
        idle_header.addWidget(idle_label)
        idle_header.addStretch()
        idle_header.addWidget(self.idle_value)
        
        self.idle_slider = ModernSlider(Qt.Horizontal)
        self.idle_slider.setRange(1, 10)  # 1 to 10 seconds
        self.idle_slider.setValue(self.settings_service.idle_threshold)
        
        self.idle_slider.valueChanged.connect(self.update_idle_threshold)
        
        idle_desc = QLabel("Seconds of inactivity before cursor movement begins")
        idle_desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px")
        
        idle_layout.addLayout(idle_header)
        idle_layout.addWidget(self.idle_slider)
        idle_layout.addWidget(idle_desc)
        settings_layout.addLayout(idle_layout)
        
        # Run on startup checkbox
        startup_layout = QHBoxLayout()
        self.startup_checkbox = ModernCheckBox("Run on startup")
        self.startup_checkbox.setChecked(self.settings_service.run_on_startup)
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
    
    def center(self):
        """Center the window on the screen."""
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def update_frequency(self, value):
        """Update the movement frequency setting."""
        frequency = value / 10
        self.freq_value.setText(f"{frequency:.1f}s")
        self.settings_service.save_frequency(frequency)
        self.cursor_service.update_settings(frequency=frequency)
    
    def update_distance(self, value):
        """Update the movement distance setting."""
        self.dist_value.setText(f"{value}px")
        self.settings_service.save_distance(value)
        self.cursor_service.update_settings(distance=value)
    
    def update_idle_threshold(self, value):
        """Update the idle threshold setting."""
        self.idle_value.setText(f"{value}s")
        self.settings_service.save_idle_threshold(value)
        self.cursor_service.update_settings(idle_threshold=value)
    
    def toggle_run_on_startup(self, state):
        """Toggle the run on startup setting."""
        self.settings_service.save_run_on_startup(state == Qt.Checked)
    
    def toggle_simulation(self):
        """Toggle the cursor movement simulation on/off."""
        if not self.cursor_service.is_active:
            # Start simulation
            self.cursor_service.start_simulation()
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
            self.system_tray.update_status(True)
        else:
            # Stop simulation
            self.cursor_service.stop_simulation()
            self.status_text.setText("Inactive")
            self.status_indicator.setActive(False)
            self.toggle_button.setText("Go, Mouse, Go!")
            self.toggle_button.setStyleSheet("")
            self.toggle_button.update_style()  # Reset button style
            self.system_tray.update_status(False)
    
    def closeEvent(self, event):
        """Handle window close event."""
        event.ignore()
        self.hide()
    
    def close_app(self):
        """Close the application completely."""
        self.cursor_service.stop_simulation()
        self.system_tray.tray_icon.hide()
        QApplication.quit()
