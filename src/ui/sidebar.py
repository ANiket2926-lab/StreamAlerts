"""
Sidebar Navigation Component
Modern dark theme sidebar with navigation buttons
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QIcon


class SidebarButton(QPushButton):
    """Custom sidebar navigation button"""
    
    def __init__(self, text: str, icon_char: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_char}  {text}" if icon_char else text)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(52)  # Increased height for font descenders
        self.setStyleSheet("padding-bottom: 4px;")  # Extra padding for descenders


class StatusIndicator(QFrame):
    """Connection status indicator widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusIndicator")
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        
        # Status dot
        self.dot = QFrame()
        self.dot.setObjectName("statusDot")
        self.dot.setFixedSize(10, 10)
        self.dot.setStyleSheet("""
            background: #43b581;
            border-radius: 5px;
        """)
        layout.addWidget(self.dot)
        
        # Status text and info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.status_label = QLabel("Connected")
        self.status_label.setStyleSheet("color: #43b581; font-weight: 600; font-size: 12px;")
        text_layout.addWidget(self.status_label)
        
        self.info_label = QLabel("Server running")
        self.info_label.setObjectName("statusText")
        self.info_label.setStyleSheet("color: #8888a0; font-size: 11px;")
        text_layout.addWidget(self.info_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
    
    def set_status(self, connected: bool, info: str = ""):
        if connected:
            self.dot.setStyleSheet("background: #43b581; border-radius: 5px;")
            self.status_label.setText("Connected")
            self.status_label.setStyleSheet("color: #43b581; font-weight: 600; font-size: 12px;")
        else:
            self.dot.setStyleSheet("background: #f04747; border-radius: 5px;")
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color: #f04747; font-weight: 600; font-size: 12px;")
        
        if info:
            self.info_label.setText(info)


class Sidebar(QWidget):
    """Main sidebar navigation widget"""
    
    # Signals
    navigation_changed = Signal(str)  # Emits page name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(240)
        self._buttons = {}
        self._current_page = "dashboard"
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo section
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 24, 20, 20)
        
        logo_label = QLabel()
        logo_label.setObjectName("sidebarLogo")
        logo_label.setText("Stream<span style='color: #7289da;'>Alerts</span>")
        logo_label.setTextFormat(Qt.TextFormat.RichText)
        logo_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
        """)
        logo_layout.addWidget(logo_label)
        layout.addWidget(logo_container)
        
        # Navigation buttons
        nav_items = [
            ("dashboard", "📊", "Dashboard"),
            ("designer", "🎨", "Overlay Designer"),
            ("history", "📜", "Alerts History"),
            ("testing", "🧪", "Testing"),
            ("settings", "⚙️", "Settings"),
        ]
        
        for page_id, icon, text in nav_items:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda checked, p=page_id: self._on_nav_click(p))
            self._buttons[page_id] = btn
            layout.addWidget(btn)
        
        # Set dashboard as active
        self._buttons["dashboard"].setChecked(True)
        
        # Spacer to push status to bottom
        layout.addStretch()
        
        # Bottom container for status and version
        bottom_container = QWidget()
        bottom_container.setMinimumHeight(100)
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(12, 8, 12, 16)
        bottom_layout.setSpacing(8)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: #2a2a3c; max-height: 1px;")
        bottom_layout.addWidget(separator)
        
        # Status indicator
        self.status_indicator = StatusIndicator()
        bottom_layout.addWidget(self.status_indicator)
        
        # Version label
        version_label = QLabel("v1.0.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("""
            color: #5a5a70;
            font-size: 11px;
            padding: 8px 0;
        """)
        bottom_layout.addWidget(version_label)
        
        layout.addWidget(bottom_container)
    
    def _on_nav_click(self, page_id: str):
        self._current_page = page_id
        
        # Update button states
        for pid, btn in self._buttons.items():
            btn.setChecked(pid == page_id)
        
        # Emit signal
        self.navigation_changed.emit(page_id)
    
    def set_page(self, page_id: str):
        """Set the current page programmatically"""
        if page_id in self._buttons:
            self._on_nav_click(page_id)
    
    def update_connection_status(self, connected: bool, info: str = ""):
        """Update the connection status indicator"""
        self.status_indicator.set_status(connected, info)
