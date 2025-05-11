
from PyQt5.QtWidgets import QSlider, QPushButton, QCheckBox, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

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
