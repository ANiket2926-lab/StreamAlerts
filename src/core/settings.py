"""
Settings Manager
Handles application settings persistence
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass

from .models import AlertTheme


@dataclass
class AppSettings:
    """Application settings"""
    # Server settings
    server_host: str = "127.0.0.1"
    server_port: int = 8765
    overlay_port: int = 8080
    
    # Queue settings
    debounce_ms: int = 500
    max_queue_size: int = 100
    
    # Display settings
    display_duration: float = 5.0
    
    # Theme settings
    current_theme_name: str = "Default"
    custom_theme: Optional[Dict] = None
    
    # Sound settings
    sound_enabled: bool = True
    sound_volume: float = 0.8
    custom_sound_path: str = ""
    
    # Advanced settings
    auto_start_server: bool = True
    minimize_to_tray: bool = True
    start_minimized: bool = False
    skip_onboarding: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "server_host": self.server_host,
            "server_port": self.server_port,
            "overlay_port": self.overlay_port,
            "debounce_ms": self.debounce_ms,
            "max_queue_size": self.max_queue_size,
            "display_duration": self.display_duration,
            "current_theme_name": self.current_theme_name,
            "custom_theme": self.custom_theme,
            "sound_enabled": self.sound_enabled,
            "sound_volume": self.sound_volume,
            "custom_sound_path": self.custom_sound_path,
            "auto_start_server": self.auto_start_server,
            "minimize_to_tray": self.minimize_to_tray,
            "start_minimized": self.start_minimized,
            "skip_onboarding": self.skip_onboarding
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AppSettings':
        return cls(
            server_host=data.get("server_host", "127.0.0.1"),
            server_port=data.get("server_port", 8765),
            overlay_port=data.get("overlay_port", 8080),
            debounce_ms=data.get("debounce_ms", 500),
            max_queue_size=data.get("max_queue_size", 100),
            display_duration=data.get("display_duration", 5.0),
            current_theme_name=data.get("current_theme_name", "Default"),
            custom_theme=data.get("custom_theme"),
            sound_enabled=data.get("sound_enabled", True),
            sound_volume=data.get("sound_volume", 0.8),
            custom_sound_path=data.get("custom_sound_path", ""),
            auto_start_server=data.get("auto_start_server", True),
            minimize_to_tray=data.get("minimize_to_tray", True),
            start_minimized=data.get("start_minimized", False),
            skip_onboarding=data.get("skip_onboarding", False)
        )


class SettingsManager:
    """Manages application settings persistence"""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir:
            self._config_dir = Path(config_dir)
        else:
            # Use AppData directory on Windows
            app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
            self._config_dir = Path(app_data) / "StreamAlerts"
        
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._settings_file = self._config_dir / "settings.json"
        self._themes_file = self._config_dir / "themes.json"
        
        self._settings = AppSettings()
        self._custom_themes: Dict[str, AlertTheme] = {}
        
        self.load()
    
    def load(self):
        """Load settings from disk"""
        # Load main settings
        if self._settings_file.exists():
            try:
                with open(self._settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._settings = AppSettings.from_dict(data)
            except Exception as e:
                print(f"Error loading settings: {e}")
                self._settings = AppSettings()
        
        # Load custom themes
        if self._themes_file.exists():
            try:
                with open(self._themes_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, theme_data in data.items():
                        self._custom_themes[name] = AlertTheme.from_dict(theme_data)
            except Exception as e:
                print(f"Error loading themes: {e}")
    
    def save(self):
        """Save settings to disk"""
        try:
            with open(self._settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings.to_dict(), f, indent=2)
            
            # Save custom themes
            themes_data = {name: theme.to_dict() for name, theme in self._custom_themes.items()}
            with open(self._themes_file, 'w', encoding='utf-8') as f:
                json.dump(themes_data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    @property
    def settings(self) -> AppSettings:
        return self._settings
    
    @settings.setter
    def settings(self, value: AppSettings):
        self._settings = value
        self.save()
    
    def update_setting(self, key: str, value: Any):
        """Update a single setting"""
        if hasattr(self._settings, key):
            setattr(self._settings, key, value)
            self.save()
    
    def get_custom_themes(self) -> Dict[str, AlertTheme]:
        return self._custom_themes
    
    def add_custom_theme(self, theme: AlertTheme):
        """Add or update a custom theme"""
        self._custom_themes[theme.name] = theme
        self.save()
    
    def remove_custom_theme(self, name: str):
        """Remove a custom theme"""
        if name in self._custom_themes:
            del self._custom_themes[name]
            self.save()
    
    @property
    def config_dir(self) -> Path:
        return self._config_dir
