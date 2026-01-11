"""
Dashboard Page
Main overview with live alert preview and statistics
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor

from ..core.models import DonationEvent, AlertTheme


class StatCard(QFrame):
    """Statistics display card"""
    
    def __init__(self, title: str, value: str = "0", color: str = "#5865f2", parent=None):
        super().__init__(parent)
        self._value = value
        self._color = color
        self._setup_ui(title)
    
    def _setup_ui(self, title: str):
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(30, 30, 45, 0.9), stop:1 rgba(25, 25, 40, 0.9));
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Value
        self.value_label = QLabel(self._value)
        self.value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {self._color};
        """)
        layout.addWidget(self.value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 12px;
            color: #8888a0;
            text-transform: uppercase;
            letter-spacing: 1px;
        """)
        layout.addWidget(title_label)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)
    
    def set_value(self, value: str):
        self._value = value
        self.value_label.setText(value)


class AlertPreviewWidget(QFrame):
    """Live alert preview widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_event: DonationEvent = None
        self._current_theme: AlertTheme = AlertTheme()
        self._setup_ui()
    
    def _setup_ui(self):
        self.setMinimumHeight(280)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a28, stop:1 #16161f);
                border-radius: 20px;
                border: 1px solid #2a2a3c;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Preview container with transparent background pattern
        self.preview_container = QFrame()
        self.preview_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(0, 0, 0, 0.2), stop:1 rgba(0, 0, 0, 0.4));
            border-radius: 20px;
        """)
        
        container_layout = QVBoxLayout(self.preview_container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Alert card
        self.alert_card = QFrame()
        self.alert_card.setFixedWidth(400)
        self.alert_card.setStyleSheet("""
            background: #1a1a2e;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        """)
        
        alert_layout = QVBoxLayout(self.alert_card)
        alert_layout.setContentsMargins(24, 24, 24, 24)
        alert_layout.setSpacing(12)
        
        # Top accent bar
        self.accent_bar = QFrame()
        self.accent_bar.setFixedHeight(4)
        self.accent_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00d9ff, stop:0.5 #ff6b6b, stop:1 #00d9ff);
            border-radius: 2px;
        """)
        alert_layout.addWidget(self.accent_bar)
        
        # Icon
        icon_container = QWidget()
        icon_layout = QHBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 8, 0, 8)
        
        self.icon_label = QLabel("💰")
        self.icon_label.setStyleSheet("""
            font-size: 42px;
            padding: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(0, 217, 255, 0.2), stop:1 rgba(255, 107, 107, 0.2));
            border-radius: 30px;
        """)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedSize(80, 80)
        icon_layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignCenter)
        alert_layout.addWidget(icon_container)
        
        # Sender name
        self.sender_label = QLabel("Waiting for donation...")
        self.sender_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
        """)
        self.sender_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alert_layout.addWidget(self.sender_label)
        
        # Amount
        self.amount_label = QLabel("₹0")
        self.amount_label.setStyleSheet("""
            font-size: 38px;
            font-weight: 700;
            color: #00d9ff;
        """)
        self.amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alert_layout.addWidget(self.amount_label)
        
        # Message
        self.message_label = QLabel("Your alert will appear here")
        self.message_label.setStyleSheet("""
            font-size: 15px;
            color: rgba(255, 255, 255, 0.7);
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px 16px;
            border-left: 3px solid #00d9ff;
        """)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alert_layout.addWidget(self.message_label)
        
        container_layout.addWidget(self.alert_card)
        
        # Placeholder text when no event
        self.placeholder = QLabel("No active alert")
        self.placeholder.setStyleSheet("""
            color: #5a5a70;
            font-size: 14px;
        """)
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.placeholder)
        self.placeholder.hide()
        
        main_layout.addWidget(self.preview_container)
        
        # Add glow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 217, 255, 60))
        shadow.setOffset(0, 0)
        self.alert_card.setGraphicsEffect(shadow)
    
    def show_event(self, event: DonationEvent, theme: AlertTheme = None):
        """Display a donation event in the preview"""
        self._current_event = event
        if theme:
            self._current_theme = theme
        
        self.sender_label.setText(event.sender)
        self.amount_label.setText(event.get_formatted_amount())
        self.message_label.setText(event.message if event.message else "Thank you for your support!")
        
        # Apply theme colors
        self.amount_label.setStyleSheet(f"""
            font-size: 38px;
            font-weight: 700;
            color: {self._current_theme.primary_color};
        """)
        
        self.message_label.setStyleSheet(f"""
            font-size: 15px;
            color: rgba(255, 255, 255, 0.7);
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px 16px;
            border-left: 3px solid {self._current_theme.primary_color};
        """)
        
        # Update accent bar
        self.accent_bar.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self._current_theme.primary_color}, 
                stop:0.5 {self._current_theme.secondary_color}, 
                stop:1 {self._current_theme.primary_color});
            border-radius: 2px;
        """)
        
        # Update glow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(self._current_theme.glow_color))
        shadow.setOffset(0, 0)
        self.alert_card.setGraphicsEffect(shadow)
        
        self.alert_card.show()
        self.placeholder.hide()
    
    def update_theme(self, theme: AlertTheme):
        """Update the current theme"""
        self._current_theme = theme
        if self._current_event:
            self.show_event(self._current_event, theme)
    
    def clear_preview(self):
        """Clear the preview"""
        self.sender_label.setText("Waiting for donation...")
        self.amount_label.setText("₹0")
        self.message_label.setText("Your alert will appear here")


class DashboardPage(QWidget):
    """Main dashboard page"""
    
    # Signals
    test_alert_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Test alert button
        self.test_btn = QPushButton("🎉  Send Test Alert")
        self.test_btn.setObjectName("primaryButton")
        self.test_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5865f2, stop:1 #4752c4);
                border: none;
                border-radius: 12px;
                padding: 14px 28px;
                color: white;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6875f5, stop:1 #5865f2);
            }
        """)
        self.test_btn.clicked.connect(self.test_alert_requested.emit)
        header_layout.addWidget(self.test_btn)
        
        layout.addLayout(header_layout)
        
        # Stats row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.total_donations_card = StatCard("Total Donations", "0", "#5865f2")
        self.total_amount_card = StatCard("Total Amount", "₹0", "#43b581")
        self.queue_size_card = StatCard("Queue Size", "0", "#faa61a")
        self.uptime_card = StatCard("Uptime", "00:00:00", "#00d9ff")
        
        stats_layout.addWidget(self.total_donations_card)
        stats_layout.addWidget(self.total_amount_card)
        stats_layout.addWidget(self.queue_size_card)
        stats_layout.addWidget(self.uptime_card)
        
        layout.addLayout(stats_layout)
        
        # Preview section
        preview_header = QHBoxLayout()
        
        preview_title = QLabel("Live Alert Preview")
        preview_title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
        """)
        preview_header.addWidget(preview_title)
        
        preview_header.addStretch()
        
        # OBS URL info
        self.obs_url_label = QLabel("📺 OBS URL: http://127.0.0.1:8080")
        self.obs_url_label.setStyleSheet("""
            color: #8888a0;
            font-size: 13px;
            background: rgba(88, 101, 242, 0.1);
            padding: 8px 16px;
            border-radius: 8px;
        """)
        preview_header.addWidget(self.obs_url_label)
        
        layout.addLayout(preview_header)
        
        # Preview widget
        self.preview_widget = AlertPreviewWidget()
        layout.addWidget(self.preview_widget, 1)
        
        # Connection info
        info_layout = QHBoxLayout()
        
        info_text = QLabel("💡 Add the OBS URL as a Browser Source in OBS Studio for live overlay integration")
        info_text.setStyleSheet("""
            color: #8888a0;
            font-size: 12px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
        """)
        info_layout.addWidget(info_text)
        
        layout.addLayout(info_layout)
    
    def update_stats(self, total_donations: int, total_amount: float, queue_size: int, uptime: str):
        """Update dashboard statistics"""
        self.total_donations_card.set_value(str(total_donations))
        self.total_amount_card.set_value(f"₹{total_amount:,.0f}")
        self.queue_size_card.set_value(str(queue_size))
        self.uptime_card.set_value(uptime)
    
    def show_alert(self, event: DonationEvent, theme: AlertTheme):
        """Show an alert in the preview"""
        self.preview_widget.show_event(event, theme)
    
    def update_obs_url(self, url: str):
        """Update the OBS URL display"""
        self.obs_url_label.setText(f"📺 OBS URL: {url}")
