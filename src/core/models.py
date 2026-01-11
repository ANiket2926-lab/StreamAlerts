"""
Donation Event Models
Defines the data structures for donation events
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum
import json
import uuid


class AnimationType(Enum):
    """Available animation types for alerts"""
    FADE_SLIDE = "fade_slide"
    SCALE_POP = "scale_pop"
    GLOW_PULSE = "glow_pulse"
    BOUNCE_IN = "bounce_in"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_ROTATE = "zoom_rotate"


@dataclass
class DonationEvent:
    """Represents a single donation event"""
    sender: str
    amount: float
    currency: str = "INR"
    message: str = ""
    timestamp: Optional[datetime] = None
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    processed: bool = False
    displayed: bool = False
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        elif isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "event_id": self.event_id,
            "sender": self.sender,
            "amount": self.amount,
            "currency": self.currency,
            "message": self.message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "processed": self.processed,
            "displayed": self.displayed
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DonationEvent':
        """Create from dictionary"""
        return cls(
            sender=data.get("sender", "Anonymous"),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", "INR"),
            message=data.get("message", ""),
            timestamp=data.get("timestamp"),
            event_id=data.get("event_id", str(uuid.uuid4())),
            processed=data.get("processed", False),
            displayed=data.get("displayed", False)
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'DonationEvent':
        """Create from JSON string"""
        return cls.from_dict(json.loads(json_str))
    
    def get_formatted_amount(self) -> str:
        """Get formatted amount with currency symbol"""
        symbols = {
            "INR": "₹",
            "USD": "$",
            "EUR": "€",
            "GBP": "£"
        }
        symbol = symbols.get(self.currency, self.currency)
        return f"{symbol}{self.amount:,.0f}"


@dataclass
class AlertTheme:
    """Customizable alert theme settings"""
    name: str = "Default"
    background_color: str = "#1a1a2e"
    primary_color: str = "#00d9ff"
    secondary_color: str = "#ff6b6b"
    text_color: str = "#ffffff"
    accent_color: str = "#ffd93d"
    font_family: str = "Segoe UI"
    font_size_sender: int = 28
    font_size_amount: int = 48
    font_size_message: int = 20
    border_radius: int = 16
    animation_type: AnimationType = AnimationType.FADE_SLIDE
    animation_duration: float = 0.5
    display_duration: float = 5.0
    sound_enabled: bool = True
    sound_file: str = ""
    glow_enabled: bool = True
    glow_color: str = "#00d9ff"
    glow_intensity: int = 20
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "background_color": self.background_color,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "text_color": self.text_color,
            "accent_color": self.accent_color,
            "font_family": self.font_family,
            "font_size_sender": self.font_size_sender,
            "font_size_amount": self.font_size_amount,
            "font_size_message": self.font_size_message,
            "border_radius": self.border_radius,
            "animation_type": self.animation_type.value,
            "animation_duration": self.animation_duration,
            "display_duration": self.display_duration,
            "sound_enabled": self.sound_enabled,
            "sound_file": self.sound_file,
            "glow_enabled": self.glow_enabled,
            "glow_color": self.glow_color,
            "glow_intensity": self.glow_intensity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AlertTheme':
        """Create from dictionary"""
        anim_type = data.get("animation_type", "fade_slide")
        if isinstance(anim_type, str):
            anim_type = AnimationType(anim_type)
        
        return cls(
            name=data.get("name", "Default"),
            background_color=data.get("background_color", "#1a1a2e"),
            primary_color=data.get("primary_color", "#00d9ff"),
            secondary_color=data.get("secondary_color", "#ff6b6b"),
            text_color=data.get("text_color", "#ffffff"),
            accent_color=data.get("accent_color", "#ffd93d"),
            font_family=data.get("font_family", "Segoe UI"),
            font_size_sender=data.get("font_size_sender", 28),
            font_size_amount=data.get("font_size_amount", 48),
            font_size_message=data.get("font_size_message", 20),
            border_radius=data.get("border_radius", 16),
            animation_type=anim_type,
            animation_duration=data.get("animation_duration", 0.5),
            display_duration=data.get("display_duration", 5.0),
            sound_enabled=data.get("sound_enabled", True),
            sound_file=data.get("sound_file", ""),
            glow_enabled=data.get("glow_enabled", True),
            glow_color=data.get("glow_color", "#00d9ff"),
            glow_intensity=data.get("glow_intensity", 20)
        )


# Preset themes
PRESET_THEMES = {
    "Neon Cyber": AlertTheme(
        name="Neon Cyber",
        background_color="#0a0a1a",
        primary_color="#00ff88",
        secondary_color="#ff0088",
        text_color="#ffffff",
        accent_color="#00d4ff",
        glow_color="#00ff88"
    ),
    "Sunset Glow": AlertTheme(
        name="Sunset Glow",
        background_color="#1a0a1a",
        primary_color="#ff6b35",
        secondary_color="#f7931e",
        text_color="#ffffff",
        accent_color="#ffcc00",
        glow_color="#ff6b35"
    ),
    "Ocean Wave": AlertTheme(
        name="Ocean Wave",
        background_color="#0a1a2a",
        primary_color="#00b4d8",
        secondary_color="#0077b6",
        text_color="#ffffff",
        accent_color="#90e0ef",
        glow_color="#00b4d8"
    ),
    "Royal Purple": AlertTheme(
        name="Royal Purple",
        background_color="#1a0a2a",
        primary_color="#9d4edd",
        secondary_color="#7b2cbf",
        text_color="#ffffff",
        accent_color="#e0aaff",
        glow_color="#9d4edd"
    ),
    "Mint Fresh": AlertTheme(
        name="Mint Fresh",
        background_color="#0a2a1a",
        primary_color="#2ec4b6",
        secondary_color="#20a4f3",
        text_color="#ffffff",
        accent_color="#cbf3f0",
        glow_color="#2ec4b6"
    ),
    "Liquid Glass": AlertTheme(
        name="Liquid Glass",
        background_color="rgba(255, 255, 255, 0.08)",
        primary_color="#a8edea",
        secondary_color="#fed6e3",
        text_color="#ffffff",
        accent_color="#b8f3ff",
        font_family="Segoe UI",
        border_radius=24,
        animation_type=AnimationType.SCALE_POP,
        glow_enabled=True,
        glow_color="#a8edea",
        glow_intensity=30
    ),
    "Aurora Borealis": AlertTheme(
        name="Aurora Borealis",
        background_color="#0d1b2a",
        primary_color="#00f5d4",
        secondary_color="#9b5de5",
        text_color="#ffffff",
        accent_color="#00bbf9",
        glow_enabled=True,
        glow_color="#00f5d4",
        glow_intensity=25
    ),
    "Cherry Blossom": AlertTheme(
        name="Cherry Blossom",
        background_color="#1a1a2e",
        primary_color="#ff6b9d",
        secondary_color="#c44569",
        text_color="#ffffff",
        accent_color="#ffc8dd",
        glow_color="#ff6b9d",
        glow_intensity=20
    )
}
