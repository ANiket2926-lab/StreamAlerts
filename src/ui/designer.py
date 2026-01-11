"""
Overlay Designer Page
Customizable alert theme editor with real-time preview
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QGridLayout, QComboBox, QSpinBox,
    QDoubleSpinBox, QSlider, QCheckBox, QLineEdit, QColorDialog,
    QFileDialog, QGroupBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from ..core.models import AlertTheme, AnimationType, PRESET_THEMES
from .styles import get_color_button_style


class ColorPickerButton(QPushButton):
    """Color picker button that shows current color"""
    
    color_changed = Signal(str)
    
    def __init__(self, initial_color: str = "#ffffff", parent=None):
        super().__init__(parent)
        self._color = initial_color
        self.setFixedSize(44, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()
        self.clicked.connect(self._pick_color)
    
    def _update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background: {self._color};
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }}
            QPushButton:hover {{
                border-color: rgba(255, 255, 255, 0.5);
            }}
        """)
    
    def _pick_color(self):
        color = QColorDialog.getColor(QColor(self._color), self, "Select Color")
        if color.isValid():
            self._color = color.name()
            self._update_style()
            self.color_changed.emit(self._color)
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value: str):
        self._color = value
        self._update_style()


class SettingRow(QWidget):
    """A single setting row with label and control"""
    
    def __init__(self, label: str, widget: QWidget, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #e8e8f0; font-size: 13px;")
        lbl.setMinimumWidth(140)
        layout.addWidget(lbl)
        
        layout.addStretch()
        layout.addWidget(widget)


class OverlayDesignerPage(QWidget):
    """Overlay designer page for theme customization"""
    
    # Signals
    theme_changed = Signal(AlertTheme)
    preview_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_theme = AlertTheme()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)
        
        # Left panel - Settings
        settings_panel = QWidget()
        settings_panel.setMinimumWidth(380)
        settings_panel.setMaximumWidth(450)
        settings_layout = QVBoxLayout(settings_panel)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(12)
        
        # Header
        header = QLabel("Overlay Designer")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        """)
        settings_layout.addWidget(header)
        
        # Scroll area for ALL settings including preset
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: transparent; 
            }
            QScrollBar:vertical {
                background: #1e1e2d;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3a3a50;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5865f2;
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(2, 0, 8, 20)
        scroll_layout.setSpacing(16)
        
        # Preset themes - NOW INSIDE SCROLL
        preset_group = self._create_preset_section()
        scroll_layout.addWidget(preset_group)
        
        # Colors section
        colors_group = self._create_colors_section()
        scroll_layout.addWidget(colors_group)
        
        # Typography section
        typography_group = self._create_typography_section()
        scroll_layout.addWidget(typography_group)
        
        # Animation section
        animation_group = self._create_animation_section()
        scroll_layout.addWidget(animation_group)
        
        # Effects section
        effects_group = self._create_effects_section()
        scroll_layout.addWidget(effects_group)
        
        # Sound section
        sound_group = self._create_sound_section()
        scroll_layout.addWidget(sound_group)
        
        # Add more bottom padding for scroll to ensure all content visible
        scroll_layout.addSpacing(80)
        
        scroll.setWidget(scroll_content)
        settings_layout.addWidget(scroll, 1)
        
        layout.addWidget(settings_panel)
        
        # Right panel - Compact Preview
        preview_panel = QWidget()
        preview_panel.setMaximumWidth(420)
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(12)
        
        # Header with button
        preview_header = QHBoxLayout()
        preview_title = QLabel("Live Preview")
        preview_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
        """)
        preview_header.addWidget(preview_title)
        preview_header.addStretch()
        
        self.preview_btn = QPushButton("🎬 Test")
        self.preview_btn.setObjectName("primaryButton")
        self.preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preview_btn.setFixedWidth(80)
        self.preview_btn.clicked.connect(self.preview_requested.emit)
        preview_header.addWidget(self.preview_btn)
        
        preview_layout.addLayout(preview_header)
        
        # Simple preview container - just the alert
        preview_container = QWidget()
        preview_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 0, 0, 0.3), stop:1 rgba(15, 20, 30, 0.4));
                border-radius: 16px;
                border: 1px dashed rgba(168, 237, 234, 0.3);
            }
        """)
        container_layout = QVBoxLayout(preview_container)
        container_layout.setContentsMargins(20, 30, 20, 30)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Mini alert preview - this is the only visual element
        self.alert_preview = self._create_mini_preview()
        container_layout.addWidget(self.alert_preview)
        
        preview_layout.addWidget(preview_container)
        preview_layout.addStretch()
        
        # Action buttons row
        action_layout = QHBoxLayout()
        
        self.save_theme_btn = QPushButton("💾 Save Theme")
        self.save_theme_btn.setObjectName("successButton")
        self.save_theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        action_layout.addWidget(self.save_theme_btn)
        
        self.reset_btn = QPushButton("↺ Reset")
        self.reset_btn.setObjectName("secondaryButton")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self._reset_theme)
        action_layout.addWidget(self.reset_btn)
        
        preview_layout.addLayout(action_layout)
        
        layout.addWidget(preview_panel)
        
        # Initial update
        self._update_preview()
    
    def _create_preset_section(self) -> QGroupBox:
        group = QGroupBox("Preset Themes")
        layout = QHBoxLayout(group)
        layout.setSpacing(8)
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("Default")
        for name in PRESET_THEMES.keys():
            self.preset_combo.addItem(name)
        self.preset_combo.setMinimumWidth(200)
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)
        layout.addWidget(self.preset_combo)
        
        layout.addStretch()
        
        return group
    
    def _create_colors_section(self) -> QGroupBox:
        group = QGroupBox("Colors")
        layout = QGridLayout(group)
        layout.setSpacing(12)
        
        # Background color
        self.bg_color_btn = ColorPickerButton(self._current_theme.background_color)
        self.bg_color_btn.color_changed.connect(lambda c: self._update_theme("background_color", c))
        layout.addWidget(QLabel("Background"), 0, 0)
        layout.addWidget(self.bg_color_btn, 0, 1)
        
        # Primary color
        self.primary_color_btn = ColorPickerButton(self._current_theme.primary_color)
        self.primary_color_btn.color_changed.connect(lambda c: self._update_theme("primary_color", c))
        layout.addWidget(QLabel("Primary"), 0, 2)
        layout.addWidget(self.primary_color_btn, 0, 3)
        
        # Secondary color
        self.secondary_color_btn = ColorPickerButton(self._current_theme.secondary_color)
        self.secondary_color_btn.color_changed.connect(lambda c: self._update_theme("secondary_color", c))
        layout.addWidget(QLabel("Secondary"), 1, 0)
        layout.addWidget(self.secondary_color_btn, 1, 1)
        
        # Accent color
        self.accent_color_btn = ColorPickerButton(self._current_theme.accent_color)
        self.accent_color_btn.color_changed.connect(lambda c: self._update_theme("accent_color", c))
        layout.addWidget(QLabel("Accent"), 1, 2)
        layout.addWidget(self.accent_color_btn, 1, 3)
        
        # Text color
        self.text_color_btn = ColorPickerButton(self._current_theme.text_color)
        self.text_color_btn.color_changed.connect(lambda c: self._update_theme("text_color", c))
        layout.addWidget(QLabel("Text"), 2, 0)
        layout.addWidget(self.text_color_btn, 2, 1)
        
        return group
    
    def _create_typography_section(self) -> QGroupBox:
        group = QGroupBox("Typography")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Font family
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Family"))
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Segoe UI", "Arial", "Roboto", "Open Sans", "Poppins",
            "Montserrat", "Inter", "Outfit", "Nunito", "Lato"
        ])
        self.font_combo.setMinimumWidth(150)
        self.font_combo.currentTextChanged.connect(lambda t: self._update_theme("font_family", t))
        font_layout.addWidget(self.font_combo)
        layout.addLayout(font_layout)
        
        # Font sizes
        size_layout = QGridLayout()
        
        size_layout.addWidget(QLabel("Sender Size"), 0, 0)
        self.sender_size_spin = QSpinBox()
        self.sender_size_spin.setRange(12, 48)
        self.sender_size_spin.setValue(self._current_theme.font_size_sender)
        self.sender_size_spin.valueChanged.connect(lambda v: self._update_theme("font_size_sender", v))
        size_layout.addWidget(self.sender_size_spin, 0, 1)
        
        size_layout.addWidget(QLabel("Amount Size"), 0, 2)
        self.amount_size_spin = QSpinBox()
        self.amount_size_spin.setRange(16, 72)
        self.amount_size_spin.setValue(self._current_theme.font_size_amount)
        self.amount_size_spin.valueChanged.connect(lambda v: self._update_theme("font_size_amount", v))
        size_layout.addWidget(self.amount_size_spin, 0, 3)
        
        size_layout.addWidget(QLabel("Message Size"), 1, 0)
        self.message_size_spin = QSpinBox()
        self.message_size_spin.setRange(10, 36)
        self.message_size_spin.setValue(self._current_theme.font_size_message)
        self.message_size_spin.valueChanged.connect(lambda v: self._update_theme("font_size_message", v))
        size_layout.addWidget(self.message_size_spin, 1, 1)
        
        layout.addLayout(size_layout)
        
        # Border radius
        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Border Radius"))
        self.radius_slider = QSlider(Qt.Orientation.Horizontal)
        self.radius_slider.setRange(0, 32)
        self.radius_slider.setValue(self._current_theme.border_radius)
        self.radius_slider.valueChanged.connect(lambda v: self._update_theme("border_radius", v))
        radius_layout.addWidget(self.radius_slider)
        self.radius_value = QLabel(f"{self._current_theme.border_radius}px")
        self.radius_slider.valueChanged.connect(lambda v: self.radius_value.setText(f"{v}px"))
        radius_layout.addWidget(self.radius_value)
        layout.addLayout(radius_layout)
        
        return group
    
    def _create_animation_section(self) -> QGroupBox:
        group = QGroupBox("Animation")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Animation type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Animation Style"))
        self.animation_combo = QComboBox()
        for anim in AnimationType:
            nice_name = anim.value.replace("_", " ").title()
            self.animation_combo.addItem(nice_name, anim)
        self.animation_combo.currentIndexChanged.connect(self._on_animation_changed)
        type_layout.addWidget(self.animation_combo)
        layout.addLayout(type_layout)
        
        # Animation duration
        anim_dur_layout = QHBoxLayout()
        anim_dur_layout.addWidget(QLabel("Animation Duration"))
        self.anim_duration_spin = QDoubleSpinBox()
        self.anim_duration_spin.setRange(0.1, 2.0)
        self.anim_duration_spin.setSingleStep(0.1)
        self.anim_duration_spin.setValue(self._current_theme.animation_duration)
        self.anim_duration_spin.setSuffix("s")
        self.anim_duration_spin.valueChanged.connect(lambda v: self._update_theme("animation_duration", v))
        anim_dur_layout.addWidget(self.anim_duration_spin)
        layout.addLayout(anim_dur_layout)
        
        # Display duration
        display_dur_layout = QHBoxLayout()
        display_dur_layout.addWidget(QLabel("Display Duration"))
        self.display_duration_spin = QDoubleSpinBox()
        self.display_duration_spin.setRange(1.0, 30.0)
        self.display_duration_spin.setSingleStep(0.5)
        self.display_duration_spin.setValue(self._current_theme.display_duration)
        self.display_duration_spin.setSuffix("s")
        self.display_duration_spin.valueChanged.connect(lambda v: self._update_theme("display_duration", v))
        display_dur_layout.addWidget(self.display_duration_spin)
        layout.addLayout(display_dur_layout)
        
        return group
    
    def _create_effects_section(self) -> QGroupBox:
        group = QGroupBox("Effects")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Glow enabled
        glow_layout = QHBoxLayout()
        self.glow_check = QCheckBox("Enable Glow Effect")
        self.glow_check.setChecked(self._current_theme.glow_enabled)
        self.glow_check.stateChanged.connect(lambda s: self._update_theme("glow_enabled", s == 2))
        glow_layout.addWidget(self.glow_check)
        layout.addLayout(glow_layout)
        
        # Glow color and intensity
        glow_settings = QHBoxLayout()
        glow_settings.addWidget(QLabel("Glow Color"))
        self.glow_color_btn = ColorPickerButton(self._current_theme.glow_color)
        self.glow_color_btn.color_changed.connect(lambda c: self._update_theme("glow_color", c))
        glow_settings.addWidget(self.glow_color_btn)
        
        glow_settings.addWidget(QLabel("Intensity"))
        self.glow_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.glow_intensity_slider.setRange(0, 50)
        self.glow_intensity_slider.setValue(self._current_theme.glow_intensity)
        self.glow_intensity_slider.valueChanged.connect(lambda v: self._update_theme("glow_intensity", v))
        glow_settings.addWidget(self.glow_intensity_slider)
        layout.addLayout(glow_settings)
        
        return group
    
    def _create_sound_section(self) -> QGroupBox:
        group = QGroupBox("Sound")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Sound enabled
        self.sound_check = QCheckBox("Enable Alert Sound")
        self.sound_check.setChecked(self._current_theme.sound_enabled)
        self.sound_check.stateChanged.connect(lambda s: self._update_theme("sound_enabled", s == 2))
        layout.addWidget(self.sound_check)
        
        # Custom sound file
        sound_layout = QHBoxLayout()
        self.sound_path_edit = QLineEdit()
        self.sound_path_edit.setPlaceholderText("Default sound")
        self.sound_path_edit.textChanged.connect(lambda t: self._update_theme("sound_file", t))
        sound_layout.addWidget(self.sound_path_edit)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondaryButton")
        browse_btn.clicked.connect(self._browse_sound)
        sound_layout.addWidget(browse_btn)
        layout.addLayout(sound_layout)
        
        return group
    
    def _create_mini_preview(self) -> QFrame:
        """Create a mini alert preview for the designer"""
        frame = QFrame()
        frame.setFixedWidth(380)
        frame.setStyleSheet(f"""
            QFrame {{
                background: {self._current_theme.background_color};
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Accent bar
        self.preview_accent = QFrame()
        self.preview_accent.setFixedHeight(4)
        self.preview_accent.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {self._current_theme.primary_color}, 
                stop:0.5 {self._current_theme.secondary_color}, 
                stop:1 {self._current_theme.primary_color});
            border-radius: 2px;
        """)
        layout.addWidget(self.preview_accent)
        
        # Sender
        self.preview_sender = QLabel("Sample Donor")
        self.preview_sender.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_sender.setStyleSheet(f"""
            font-size: {self._current_theme.font_size_sender}px;
            font-weight: 600;
            color: {self._current_theme.text_color};
        """)
        layout.addWidget(self.preview_sender)
        
        # Amount
        self.preview_amount = QLabel("₹500")
        self.preview_amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_amount.setStyleSheet(f"""
            font-size: {self._current_theme.font_size_amount}px;
            font-weight: 700;
            color: {self._current_theme.primary_color};
        """)
        layout.addWidget(self.preview_amount)
        
        # Message
        self.preview_message = QLabel("Great stream! Keep it up! 🎮")
        self.preview_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_message.setWordWrap(True)
        self.preview_message.setStyleSheet(f"""
            font-size: {self._current_theme.font_size_message}px;
            color: rgba(255, 255, 255, 0.7);
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
            border-left: 3px solid {self._current_theme.primary_color};
        """)
        layout.addWidget(self.preview_message)
        
        return frame
    
    def _update_theme(self, key: str, value):
        """Update a theme property and refresh preview"""
        setattr(self._current_theme, key, value)
        self._update_preview()
        self.theme_changed.emit(self._current_theme)
    
    def _update_preview(self):
        """Update the mini preview with current theme"""
        theme = self._current_theme
        
        # Update frame
        self.alert_preview.setStyleSheet(f"""
            QFrame {{
                background: {theme.background_color};
                border-radius: {theme.border_radius}px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """)
        
        # Update accent bar
        self.preview_accent.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {theme.primary_color}, 
                stop:0.5 {theme.secondary_color}, 
                stop:1 {theme.primary_color});
            border-radius: 2px;
        """)
        
        # Update sender
        self.preview_sender.setStyleSheet(f"""
            font-size: {theme.font_size_sender}px;
            font-weight: 600;
            color: {theme.text_color};
            font-family: {theme.font_family};
        """)
        
        # Update amount
        self.preview_amount.setStyleSheet(f"""
            font-size: {theme.font_size_amount}px;
            font-weight: 700;
            color: {theme.primary_color};
            font-family: {theme.font_family};
        """)
        
        # Update message
        self.preview_message.setStyleSheet(f"""
            font-size: {theme.font_size_message}px;
            color: rgba(255, 255, 255, 0.7);
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
            border-left: 3px solid {theme.primary_color};
            font-family: {theme.font_family};
        """)
    
    def _on_preset_changed(self, name: str):
        """Load a preset theme"""
        if name == "Default":
            self._current_theme = AlertTheme()
        elif name in PRESET_THEMES:
            self._current_theme = PRESET_THEMES[name]
        
        # Update all controls
        self._refresh_controls()
        self._update_preview()
        self.theme_changed.emit(self._current_theme)
    
    def _on_animation_changed(self, index: int):
        """Handle animation type change"""
        anim_type = self.animation_combo.currentData()
        if anim_type:
            self._update_theme("animation_type", anim_type)
    
    def _refresh_controls(self):
        """Refresh all controls with current theme values"""
        theme = self._current_theme
        
        # Colors
        self.bg_color_btn.color = theme.background_color
        self.primary_color_btn.color = theme.primary_color
        self.secondary_color_btn.color = theme.secondary_color
        self.accent_color_btn.color = theme.accent_color
        self.text_color_btn.color = theme.text_color
        
        # Typography
        idx = self.font_combo.findText(theme.font_family)
        if idx >= 0:
            self.font_combo.setCurrentIndex(idx)
        self.sender_size_spin.setValue(theme.font_size_sender)
        self.amount_size_spin.setValue(theme.font_size_amount)
        self.message_size_spin.setValue(theme.font_size_message)
        self.radius_slider.setValue(theme.border_radius)
        
        # Animation
        for i in range(self.animation_combo.count()):
            if self.animation_combo.itemData(i) == theme.animation_type:
                self.animation_combo.setCurrentIndex(i)
                break
        self.anim_duration_spin.setValue(theme.animation_duration)
        self.display_duration_spin.setValue(theme.display_duration)
        
        # Effects
        self.glow_check.setChecked(theme.glow_enabled)
        self.glow_color_btn.color = theme.glow_color
        self.glow_intensity_slider.setValue(theme.glow_intensity)
        
        # Sound
        self.sound_check.setChecked(theme.sound_enabled)
        self.sound_path_edit.setText(theme.sound_file)
    
    def _reset_theme(self):
        """Reset to default theme"""
        self._current_theme = AlertTheme()
        self._refresh_controls()
        self._update_preview()
        self.theme_changed.emit(self._current_theme)
    
    def _browse_sound(self):
        """Browse for a custom sound file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Sound File", "",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*)"
        )
        if file_path:
            self.sound_path_edit.setText(file_path)
    
    def get_current_theme(self) -> AlertTheme:
        """Get the current theme"""
        return self._current_theme
    
    def set_theme(self, theme: AlertTheme):
        """Set the current theme"""
        self._current_theme = theme
        self._refresh_controls()
        self._update_preview()
