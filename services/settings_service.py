
import os
import sys
import winreg as reg
from PyQt5.QtCore import QSettings

class SettingsService:
    """Service for managing application settings"""
    
    def __init__(self):
        self.settings = QSettings("CursorVibe", "CursorVibe")
        
        # Load settings with defaults
        self.movement_frequency = self.settings.value("frequency", 1.0, type=float)
        self.movement_distance = self.settings.value("distance", 2, type=int)
        self.idle_threshold = self.settings.value("idle_threshold", 3, type=int)
        self.run_on_startup = self.settings.value("run_on_startup", False, type=bool)
    
    def save_frequency(self, value):
        """Save the movement frequency setting"""
        self.movement_frequency = value
        self.settings.setValue("frequency", value)
    
    def save_distance(self, value):
        """Save the movement distance setting"""
        self.movement_distance = value
        self.settings.setValue("distance", value)
    
    def save_idle_threshold(self, value):
        """Save the idle threshold setting"""
        self.idle_threshold = value
        self.settings.setValue("idle_threshold", value)
    
    def save_run_on_startup(self, value):
        """Save the run on startup setting and update the registry"""
        self.run_on_startup = value
        self.settings.setValue("run_on_startup", value)
        self.update_startup_registry()
    
    def update_startup_registry(self):
        """Update the Windows registry for startup"""
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
    
    def get_all_settings(self):
        """Get all settings as a dictionary"""
        return {
            "movement_frequency": self.movement_frequency,
            "movement_distance": self.movement_distance,
            "idle_threshold": self.idle_threshold,
            "run_on_startup": self.run_on_startup
        }
