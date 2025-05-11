
# CursorVibe

CursorVibe is a Python desktop application for Windows that prevents the system from going to sleep or locking due to inactivity by simulating small mouse movements.

## Features

- Simulated mouse movement to keep the system active
- Configurable movement frequency (0.1-2.0 seconds)
- Configurable movement distance (1-10 pixels)
- Activity detection (only moves the cursor when user is idle)
- Toggle on/off functionality
- Run on startup option
- System tray integration

## Requirements

- Python 3.6 or higher
- PyQt5
- pyautogui

## Installation

1. Clone or download this repository
2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

Run the application:

```
python cursor_vibe.py
```

The application will open with the main settings window. You can:

- Adjust the frequency of simulated mouse movements
- Adjust the distance of simulated mouse movements
- Set the idle threshold before movements begin
- Enable/disable "Run on startup"
- Click "Go, Mouse, Go!" to start the simulation

When minimized, the application runs in the system tray. Right-click the tray icon to:

- Start/Stop the simulation
- Show the settings window
- Quit the application

## Note

This application uses the Windows registry to manage the "Run on startup" feature, which requires appropriate permissions.

