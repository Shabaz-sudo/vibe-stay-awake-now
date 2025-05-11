
import random
import threading
import time
import pyautogui

class CursorService:
    """Service for simulating cursor movements"""
    
    def __init__(self):
        self.is_active = False
        self.stop_thread = False
        self.thread = None
        self.last_activity_time = time.time()
        self.last_mouse_position = pyautogui.position()
        
        # Default settings
        self.movement_frequency = 1.0  # in seconds
        self.movement_distance = 2     # in pixels
        self.idle_threshold = 3        # in seconds
    
    def start_simulation(self):
        """Start the cursor movement simulation"""
        if not self.is_active:
            self.is_active = True
            self.stop_thread = False
            self.thread = threading.Thread(target=self.simulate_cursor_movement)
            self.thread.daemon = True
            self.thread.start()
            return True
        return False
    
    def stop_simulation(self):
        """Stop the cursor movement simulation"""
        if self.is_active:
            self.is_active = False
            self.stop_thread = True
            if self.thread:
                self.thread.join(timeout=1)
            return True
        return False
    
    def check_mouse_activity(self):
        """Check if the user has moved the mouse"""
        current_position = pyautogui.position()
        if current_position != self.last_mouse_position:
            self.last_activity_time = time.time()
            self.last_mouse_position = current_position
    
    def is_user_idle(self):
        """Check if the user has been idle for longer than the threshold"""
        idle_time = time.time() - self.last_activity_time
        return idle_time >= self.idle_threshold
    
    def simulate_cursor_movement(self):
        """Simulate small random cursor movements"""
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
    
    def update_settings(self, frequency=None, distance=None, idle_threshold=None):
        """Update the simulation settings"""
        if frequency is not None:
            self.movement_frequency = frequency
        if distance is not None:
            self.movement_distance = distance
        if idle_threshold is not None:
            self.idle_threshold = idle_threshold
