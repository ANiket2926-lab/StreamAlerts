"""
Onboarding / Instructions Page
Shows setup instructions before main dashboard
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QCheckBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap


class StepCard(QFrame):
    """Individual instruction step card"""
    
    def __init__(self, step_num: int, title: str, description: str, icon: str = "", parent=None):
        super().__init__(parent)
        self._setup_ui(step_num, title, description, icon)
    
    def _setup_ui(self, step_num: int, title: str, description: str, icon: str):
        self.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 45, 0.8);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            QFrame:hover {
                border: 1px solid rgba(114, 137, 218, 0.3);
                background: rgba(35, 35, 55, 0.9);
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)
        
        # Step number circle
        step_frame = QFrame()
        step_frame.setFixedSize(56, 56)
        step_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #5865f2, stop:1 #4752c4);
            border-radius: 28px;
            border: none;
        """)
        step_layout = QVBoxLayout(step_frame)
        step_layout.setContentsMargins(0, 0, 0, 0)
        step_label = QLabel(str(step_num))
        step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        step_label.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: white;
            background: transparent;
            border: none;
        """)
        step_layout.addWidget(step_label)
        layout.addWidget(step_frame)
        
        # Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)
        
        # Title with icon
        title_text = f"{icon}  {title}" if icon else title
        title_label = QLabel(title_text)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            font-size: 14px;
            color: #a0a0b8;
            line-height: 1.5;
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(desc_label)
        
        layout.addLayout(content_layout, 1)


class InfoBox(QFrame):
    """Information highlight box"""
    
    def __init__(self, title: str, content: str, color: str = "#5865f2", parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba({self._hex_to_rgb(color)}, 0.1);
                border-radius: 12px;
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {color};
            background: transparent;
            border: none;
        """)
        layout.addWidget(title_label)
        
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            font-size: 13px;
            color: #c0c0d8;
            background: transparent;
            border: none;
        """)
        layout.addWidget(content_label)
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"{r}, {g}, {b}"


class OnboardingPage(QWidget):
    """Onboarding/Instructions page shown before main dashboard"""
    
    # Signals
    continue_clicked = Signal()
    skip_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d0d14, stop:1 #12121a);
                border: none;
            }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(60, 50, 60, 50)
        content_layout.setSpacing(30)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(12)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo/Title
        logo_label = QLabel("🎬 StreamAlerts")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            font-size: 42px;
            font-weight: 800;
            color: #ffffff;
            background: transparent;
        """)
        header_layout.addWidget(logo_label)
        
        subtitle = QLabel("UPI Donation Overlay System")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: #7289da;
            font-weight: 500;
            background: transparent;
        """)
        header_layout.addWidget(subtitle)
        
        tagline = QLabel("Connect your Google Pay donations to your live stream in minutes")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline.setStyleSheet("""
            font-size: 15px;
            color: #8888a0;
            background: transparent;
            margin-top: 8px;
        """)
        header_layout.addWidget(tagline)
        
        content_layout.addLayout(header_layout)
        content_layout.addSpacing(20)
        
        # Section: How It Works
        section_title = QLabel("📋 How It Works")
        section_title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            background: transparent;
            margin-bottom: 8px;
        """)
        content_layout.addWidget(section_title)
        
        # Steps
        steps = [
            ("Install Companion App", 
             "Download and install the StreamAlerts Companion App on your Android phone from the provided APK or Play Store link.",
             "📱"),
            ("Connect to Same Network",
             "Ensure both your PC running StreamAlerts and your Android phone are connected to the same WiFi network for seamless communication.",
             "📶"),
            ("Enable Google Pay Notifications",
             "In the Companion App, grant notification access permission. This allows the app to detect incoming Google Pay payment notifications.",
             "🔔"),
            ("Enter Server IP Address",
             "Open the Companion App and enter your PC's local IP address (shown in StreamAlerts Settings) to establish the connection.",
             "🔗"),
            ("Add Overlay to OBS",
             "In OBS Studio, add a Browser Source with the overlay URL (http://127.0.0.1:8080) to display donation alerts on your stream.",
             "🎥"),
            ("Start Streaming!",
             "When someone sends you money via Google Pay, the notification is captured and displayed as a beautiful alert overlay on your stream.",
             "🚀")
        ]
        
        for i, (title, desc, icon) in enumerate(steps, 1):
            step_card = StepCard(i, title, desc, icon)
            content_layout.addWidget(step_card)
        
        content_layout.addSpacing(20)
        
        # Important Info Section
        info_section = QLabel("ℹ️ Important Information")
        info_section.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            background: transparent;
        """)
        content_layout.addWidget(info_section)
        
        # Info boxes
        info_grid = QHBoxLayout()
        info_grid.setSpacing(16)
        
        privacy_box = InfoBox(
            "🔒 Privacy First",
            "All data stays on your local network. No cloud servers, no data collection. Your payment notifications are processed entirely offline.",
            "#43b581"
        )
        info_grid.addWidget(privacy_box)
        
        network_box = InfoBox(
            "📡 Network Requirements",
            "Both devices must be on the same WiFi. Alternatively, connect your phone via USB for a direct wired connection.",
            "#faa61a"
        )
        info_grid.addWidget(network_box)
        
        content_layout.addLayout(info_grid)
        
        info_grid2 = QHBoxLayout()
        info_grid2.setSpacing(16)
        
        permission_box = InfoBox(
            "⚠️ Notification Permission",
            "The Android app requires notification access to read Google Pay alerts. This permission is essential for the system to work.",
            "#f04747"
        )
        info_grid2.addWidget(permission_box)
        
        support_box = InfoBox(
            "💡 Supported Apps",
            "Currently supports Google Pay (GPay), PhonePe, Paytm, and other UPI apps that show payment notifications.",
            "#5865f2"
        )
        info_grid2.addWidget(support_box)
        
        content_layout.addLayout(info_grid2)
        
        content_layout.addSpacing(20)
        
        # Server Info
        server_section = QLabel("🖥️ Your Server Details")
        server_section.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            background: transparent;
        """)
        content_layout.addWidget(server_section)
        
        server_info = QFrame()
        server_info.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 45, 0.9);
                border-radius: 16px;
                border: 1px solid #2a2a3c;
            }
        """)
        server_layout = QHBoxLayout(server_info)
        server_layout.setContentsMargins(24, 20, 24, 20)
        server_layout.setSpacing(40)
        
        # Donation endpoint
        donation_box = QVBoxLayout()
        donation_label = QLabel("Donation Endpoint")
        donation_label.setStyleSheet("color: #8888a0; font-size: 12px; background: transparent; border: none;")
        donation_box.addWidget(donation_label)
        donation_url = QLabel("http://127.0.0.1:8765/donation")
        donation_url.setStyleSheet("""
            color: #00d9ff;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Consolas', 'Courier New', monospace;
            background: transparent;
            border: none;
        """)
        donation_url.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        donation_box.addWidget(donation_url)
        server_layout.addLayout(donation_box)
        
        # OBS Overlay
        obs_box = QVBoxLayout()
        obs_label = QLabel("OBS Overlay URL")
        obs_label.setStyleSheet("color: #8888a0; font-size: 12px; background: transparent; border: none;")
        obs_box.addWidget(obs_label)
        obs_url = QLabel("http://127.0.0.1:8080")
        obs_url.setStyleSheet("""
            color: #43b581;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Consolas', 'Courier New', monospace;
            background: transparent;
            border: none;
        """)
        obs_url.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        obs_box.addWidget(obs_url)
        server_layout.addLayout(obs_box)
        
        server_layout.addStretch()
        content_layout.addWidget(server_info)
        
        content_layout.addSpacing(30)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)
        
        # Don't show again checkbox
        self.dont_show_check = QCheckBox("Don't show this again")
        self.dont_show_check.setStyleSheet("""
            QCheckBox {
                color: #8888a0;
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #3a3a50;
                background: #1e1e2d;
            }
            QCheckBox::indicator:checked {
                background: #5865f2;
                border-color: #5865f2;
            }
        """)
        button_layout.addWidget(self.dont_show_check)
        
        button_layout.addStretch()
        
        # Skip button
        skip_btn = QPushButton("Skip for now")
        skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        skip_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 2px solid #3a3a50;
                border-radius: 12px;
                padding: 14px 32px;
                color: #8888a0;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                border-color: #5a5a70;
                color: #c0c0d8;
            }
        """)
        skip_btn.clicked.connect(self.skip_clicked.emit)
        button_layout.addWidget(skip_btn)
        
        # Continue button
        continue_btn = QPushButton("🚀  Get Started")
        continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        continue_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5865f2, stop:1 #7289da);
                border: none;
                border-radius: 12px;
                padding: 14px 40px;
                color: white;
                font-weight: 700;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6875f5, stop:1 #8299ea);
            }
        """)
        continue_btn.clicked.connect(self.continue_clicked.emit)
        button_layout.addWidget(continue_btn)
        
        content_layout.addLayout(button_layout)
        content_layout.addSpacing(20)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def should_skip_next_time(self) -> bool:
        """Check if user wants to skip onboarding next time"""
        return self.dont_show_check.isChecked()
