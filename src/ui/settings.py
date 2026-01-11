"""
Settings Page
Application configuration and preferences
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QGroupBox, QLineEdit, QSpinBox,
    QDoubleSpinBox, QCheckBox, QSlider, QComboBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal

from ..core.settings import AppSettings


class SettingsPage(QWidget):
    """Application settings page"""
    
    # Signals
    settings_changed = Signal(AppSettings)
    restart_server = Signal()
    view_instructions = Signal()
    
    def __init__(self, settings: AppSettings = None, parent=None):
        super().__init__(parent)
        self._settings = settings or AppSettings()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Settings")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Save button
        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.setObjectName("successButton")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self._save_settings)
        header_layout.addWidget(self.save_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        
        # Server settings
        server_group = self._create_server_settings()
        scroll_layout.addWidget(server_group)
        
        # Queue settings
        queue_group = self._create_queue_settings()
        scroll_layout.addWidget(queue_group)
        
        # Display settings
        display_group = self._create_display_settings()
        scroll_layout.addWidget(display_group)
        
        # Audio settings
        audio_group = self._create_audio_settings()
        scroll_layout.addWidget(audio_group)
        
        # Advanced settings
        advanced_group = self._create_advanced_settings()
        scroll_layout.addWidget(advanced_group)
        
        # About section
        about_group = self._create_about_section()
        scroll_layout.addWidget(about_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
    
    def _create_server_settings(self) -> QGroupBox:
        group = QGroupBox("Server Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # Host
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_edit = QLineEdit(self._settings.server_host)
        self.host_edit.setPlaceholderText("127.0.0.1")
        host_layout.addWidget(self.host_edit)
        layout.addLayout(host_layout)
        
        # Ports
        port_layout = QHBoxLayout()
        
        port_layout.addWidget(QLabel("Donation Port:"))
        self.donation_port_spin = QSpinBox()
        self.donation_port_spin.setRange(1024, 65535)
        self.donation_port_spin.setValue(self._settings.server_port)
        port_layout.addWidget(self.donation_port_spin)
        
        port_layout.addSpacing(20)
        
        port_layout.addWidget(QLabel("Overlay Port:"))
        self.overlay_port_spin = QSpinBox()
        self.overlay_port_spin.setRange(1024, 65535)
        self.overlay_port_spin.setValue(self._settings.overlay_port)
        port_layout.addWidget(self.overlay_port_spin)
        
        port_layout.addStretch()
        layout.addLayout(port_layout)
        
        # Restart server button
        restart_layout = QHBoxLayout()
        self.restart_btn = QPushButton("🔄 Restart Server")
        self.restart_btn.setObjectName("secondaryButton")
        self.restart_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restart_btn.clicked.connect(self.restart_server.emit)
        restart_layout.addWidget(self.restart_btn)
        restart_layout.addStretch()
        layout.addLayout(restart_layout)
        
        # Info
        info_label = QLabel("💡 Changes to ports require a server restart")
        info_label.setStyleSheet("color: #8888a0; font-size: 12px;")
        layout.addWidget(info_label)
        
        return group
    
    def _create_queue_settings(self) -> QGroupBox:
        group = QGroupBox("Queue Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # Debounce
        debounce_layout = QHBoxLayout()
        debounce_layout.addWidget(QLabel("Debounce Time:"))
        self.debounce_spin = QSpinBox()
        self.debounce_spin.setRange(100, 5000)
        self.debounce_spin.setValue(self._settings.debounce_ms)
        self.debounce_spin.setSuffix(" ms")
        self.debounce_spin.setToolTip("Minimum time between duplicate donations")
        debounce_layout.addWidget(self.debounce_spin)
        debounce_layout.addStretch()
        layout.addLayout(debounce_layout)
        
        # Max queue size
        queue_layout = QHBoxLayout()
        queue_layout.addWidget(QLabel("Max Queue Size:"))
        self.queue_size_spin = QSpinBox()
        self.queue_size_spin.setRange(10, 500)
        self.queue_size_spin.setValue(self._settings.max_queue_size)
        queue_layout.addWidget(self.queue_size_spin)
        queue_layout.addStretch()
        layout.addLayout(queue_layout)
        
        return group
    
    def _create_display_settings(self) -> QGroupBox:
        group = QGroupBox("Display Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # Display duration
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Alert Display Duration:"))
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(1.0, 30.0)
        self.duration_spin.setSingleStep(0.5)
        self.duration_spin.setValue(self._settings.display_duration)
        self.duration_spin.setSuffix(" seconds")
        duration_layout.addWidget(self.duration_spin)
        duration_layout.addStretch()
        layout.addLayout(duration_layout)
        
        return group
    
    def _create_audio_settings(self) -> QGroupBox:
        group = QGroupBox("Audio Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # Sound enabled
        self.sound_enabled_check = QCheckBox("Enable Alert Sounds")
        self.sound_enabled_check.setChecked(self._settings.sound_enabled)
        layout.addWidget(self.sound_enabled_check)
        
        # Volume
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self._settings.sound_volume * 100))
        volume_layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel(f"{int(self._settings.sound_volume * 100)}%")
        self.volume_slider.valueChanged.connect(
            lambda v: self.volume_label.setText(f"{v}%")
        )
        volume_layout.addWidget(self.volume_label)
        
        layout.addLayout(volume_layout)
        
        # Custom sound
        sound_layout = QHBoxLayout()
        sound_layout.addWidget(QLabel("Custom Sound:"))
        self.sound_path_edit = QLineEdit(self._settings.custom_sound_path)
        self.sound_path_edit.setPlaceholderText("Default sound")
        sound_layout.addWidget(self.sound_path_edit)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.clicked.connect(self._browse_sound)
        sound_layout.addWidget(browse_btn)
        layout.addLayout(sound_layout)
        
        return group
    
    def _create_advanced_settings(self) -> QGroupBox:
        group = QGroupBox("Advanced")
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # Auto start server
        self.auto_start_check = QCheckBox("Auto-start server on launch")
        self.auto_start_check.setChecked(self._settings.auto_start_server)
        layout.addWidget(self.auto_start_check)
        
        # Minimize to tray
        self.minimize_tray_check = QCheckBox("Minimize to system tray")
        self.minimize_tray_check.setChecked(self._settings.minimize_to_tray)
        layout.addWidget(self.minimize_tray_check)
        
        # Start minimized
        self.start_minimized_check = QCheckBox("Start minimized")
        self.start_minimized_check.setChecked(self._settings.start_minimized)
        layout.addWidget(self.start_minimized_check)
        
        # Show onboarding checkbox
        self.show_onboarding_check = QCheckBox("Show setup guide on startup")
        self.show_onboarding_check.setChecked(not getattr(self._settings, 'skip_onboarding', False))
        layout.addWidget(self.show_onboarding_check)
        
        # View instructions button
        layout.addSpacing(8)
        instructions_btn = QPushButton("📋 View Setup Guide")
        instructions_btn.setObjectName("secondaryButton")
        instructions_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        instructions_btn.clicked.connect(self.view_instructions.emit)
        instructions_btn.setToolTip("View the setup instructions for connecting your phone")
        layout.addWidget(instructions_btn)
        
        return group
    
    def _create_about_section(self) -> QGroupBox:
        group = QGroupBox("About")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        app_name = QLabel("StreamAlerts")
        app_name.setStyleSheet("font-size: 18px; font-weight: 700; color: #7289da;")
        layout.addWidget(app_name)
        
        version = QLabel("Version 1.0.0")
        version.setStyleSheet("color: #8888a0;")
        layout.addWidget(version)
        
        desc = QLabel("Professional UPI donation alert overlay system for streamers.")
        desc.setStyleSheet("color: #e8e8f0;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Links
        links_layout = QHBoxLayout()
        
        docs_btn = QPushButton("📖 Documentation")
        docs_btn.setObjectName("secondaryButton")
        docs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        links_layout.addWidget(docs_btn)
        
        links_layout.addStretch()
        layout.addLayout(links_layout)
        
        return group
    
    def _browse_sound(self):
        """Browse for a sound file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Sound File", "",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*)"
        )
        if file_path:
            self.sound_path_edit.setText(file_path)
    
    def _save_settings(self):
        """Save all settings"""
        self._settings.server_host = self.host_edit.text()
        self._settings.server_port = self.donation_port_spin.value()
        self._settings.overlay_port = self.overlay_port_spin.value()
        self._settings.debounce_ms = self.debounce_spin.value()
        self._settings.max_queue_size = self.queue_size_spin.value()
        self._settings.display_duration = self.duration_spin.value()
        self._settings.sound_enabled = self.sound_enabled_check.isChecked()
        self._settings.sound_volume = self.volume_slider.value() / 100
        self._settings.custom_sound_path = self.sound_path_edit.text()
        self._settings.auto_start_server = self.auto_start_check.isChecked()
        self._settings.minimize_to_tray = self.minimize_tray_check.isChecked()
        self._settings.start_minimized = self.start_minimized_check.isChecked()
        self._settings.skip_onboarding = not self.show_onboarding_check.isChecked()
        
        self.settings_changed.emit(self._settings)
    
    def set_settings(self, settings: AppSettings):
        """Update the displayed settings"""
        self._settings = settings
        
        self.host_edit.setText(settings.server_host)
        self.donation_port_spin.setValue(settings.server_port)
        self.overlay_port_spin.setValue(settings.overlay_port)
        self.debounce_spin.setValue(settings.debounce_ms)
        self.queue_size_spin.setValue(settings.max_queue_size)
        self.duration_spin.setValue(settings.display_duration)
        self.sound_enabled_check.setChecked(settings.sound_enabled)
        self.volume_slider.setValue(int(settings.sound_volume * 100))
        self.sound_path_edit.setText(settings.custom_sound_path)
        self.auto_start_check.setChecked(settings.auto_start_server)
        self.minimize_tray_check.setChecked(settings.minimize_to_tray)
        self.start_minimized_check.setChecked(settings.start_minimized)
