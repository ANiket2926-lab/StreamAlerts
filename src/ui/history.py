"""
Alerts History Page
Shows past donation events in a scrollable list
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QListWidget, QListWidgetItem,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from typing import List
from datetime import datetime

from ..core.models import DonationEvent


class HistoryItem(QFrame):
    """Single history item widget"""
    
    replay_requested = Signal(DonationEvent)
    
    def __init__(self, event: DonationEvent, parent=None):
        super().__init__(parent)
        self._event = event
        self._setup_ui()
    
    def _setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 45, 0.8);
                border-radius: 12px;
                border-left: 4px solid #5865f2;
            }
            QFrame:hover {
                background: rgba(40, 40, 60, 0.9);
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(16)
        
        # Left section - Amount
        amount_frame = QFrame()
        amount_frame.setFixedWidth(100)
        amount_frame.setStyleSheet("border: none; background: transparent;")
        amount_layout = QVBoxLayout(amount_frame)
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        amount_label = QLabel(self._event.get_formatted_amount())
        amount_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #43b581;
            background: transparent;
            border: none;
        """)
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_layout.addWidget(amount_label)
        
        layout.addWidget(amount_frame)
        
        # Middle section - Details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(4)
        
        sender_label = QLabel(self._event.sender)
        sender_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 600;
            color: #ffffff;
            background: transparent;
            border: none;
        """)
        details_layout.addWidget(sender_label)
        
        if self._event.message:
            message_label = QLabel(self._event.message)
            message_label.setStyleSheet("""
                font-size: 13px;
                color: #8888a0;
                background: transparent;
                border: none;
            """)
            message_label.setWordWrap(True)
            details_layout.addWidget(message_label)
        
        # Timestamp
        time_str = self._event.timestamp.strftime("%I:%M %p") if self._event.timestamp else ""
        date_str = self._event.timestamp.strftime("%b %d") if self._event.timestamp else ""
        time_label = QLabel(f"{time_str} · {date_str}")
        time_label.setStyleSheet("""
            font-size: 11px;
            color: #5a5a70;
            background: transparent;
            border: none;
        """)
        details_layout.addWidget(time_label)
        
        layout.addLayout(details_layout, 1)
        
        # Right section - Replay button
        replay_btn = QPushButton("▶")
        replay_btn.setFixedSize(36, 36)
        replay_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        replay_btn.setStyleSheet("""
            QPushButton {
                background: rgba(88, 101, 242, 0.2);
                border: none;
                border-radius: 18px;
                color: #5865f2;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(88, 101, 242, 0.4);
            }
        """)
        replay_btn.setToolTip("Replay this alert")
        replay_btn.clicked.connect(lambda: self.replay_requested.emit(self._event))
        layout.addWidget(replay_btn)


class HistoryPage(QWidget):
    """Alerts history page"""
    
    # Signals
    replay_alert = Signal(DonationEvent)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._history: List[DonationEvent] = []
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Alerts History")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Stats summary
        self.stats_label = QLabel("0 donations · ₹0 total")
        self.stats_label.setStyleSheet("""
            color: #8888a0;
            font-size: 14px;
            background: rgba(88, 101, 242, 0.1);
            padding: 8px 16px;
            border-radius: 8px;
        """)
        header_layout.addWidget(self.stats_label)
        
        # Clear button
        self.clear_btn = QPushButton("🗑 Clear History")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self._clear_history)
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area for history items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)
        
        self.history_container = QWidget()
        self.history_layout = QVBoxLayout(self.history_container)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_layout.setSpacing(12)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Empty state
        self.empty_label = QLabel("No donation history yet")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #5a5a70;
            font-size: 16px;
            padding: 60px;
        """)
        self.history_layout.addWidget(self.empty_label)
        
        scroll.setWidget(self.history_container)
        layout.addWidget(scroll)
    
    def add_event(self, event: DonationEvent):
        """Add a new event to the history"""
        self._history.insert(0, event)
        
        # Hide empty state
        self.empty_label.hide()
        
        # Create item widget
        item = HistoryItem(event)
        item.replay_requested.connect(self.replay_alert.emit)
        
        # Insert at top
        self.history_layout.insertWidget(0, item)
        
        # Limit displayed items
        if self.history_layout.count() > 100:
            old_item = self.history_layout.takeAt(self.history_layout.count() - 1)
            if old_item.widget():
                old_item.widget().deleteLater()
        
        # Update stats
        self._update_stats()
    
    def set_history(self, events: List[DonationEvent]):
        """Set the full history"""
        self._clear_widgets()
        self._history = events
        
        if not events:
            self.empty_label.show()
            return
        
        self.empty_label.hide()
        
        for event in events:
            item = HistoryItem(event)
            item.replay_requested.connect(self.replay_alert.emit)
            self.history_layout.addWidget(item)
        
        self._update_stats()
    
    def _clear_widgets(self):
        """Clear all history widgets"""
        while self.history_layout.count() > 1:  # Keep empty label
            item = self.history_layout.takeAt(0)
            if item.widget() and item.widget() != self.empty_label:
                item.widget().deleteLater()
    
    def _clear_history(self):
        """Clear all history"""
        self._clear_widgets()
        self._history.clear()
        self.empty_label.show()
        self._update_stats()
    
    def _update_stats(self):
        """Update the stats summary"""
        count = len(self._history)
        total = sum(e.amount for e in self._history)
        self.stats_label.setText(f"{count} donations · ₹{total:,.0f} total")


class TestingPage(QWidget):
    """Testing and mock donation page"""
    
    # Signals
    send_test_donation = Signal(dict)
    start_continuous = Signal(float, float)
    stop_continuous = Signal()
    start_stress_test = Signal(int, float)
    stop_stress_test = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._continuous_running = False
        self._stress_running = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)
        
        # Header
        title = QLabel("Testing & Mock Generator")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
        """)
        layout.addWidget(title)
        
        # Quick test section
        quick_group = QFrame()
        quick_group.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 45, 0.8);
                border-radius: 16px;
                border: 1px solid #2a2a3c;
            }
        """)
        quick_layout = QVBoxLayout(quick_group)
        quick_layout.setContentsMargins(24, 24, 24, 24)
        quick_layout.setSpacing(16)
        
        quick_title = QLabel("Quick Test")
        quick_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #ffffff;")
        quick_layout.addWidget(quick_title)
        
        quick_btn_layout = QHBoxLayout()
        
        self.test_small_btn = QPushButton("₹50 Donation")
        self.test_small_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_small_btn.clicked.connect(lambda: self._send_test(50))
        quick_btn_layout.addWidget(self.test_small_btn)
        
        self.test_medium_btn = QPushButton("₹500 Donation")
        self.test_medium_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_medium_btn.clicked.connect(lambda: self._send_test(500))
        quick_btn_layout.addWidget(self.test_medium_btn)
        
        self.test_large_btn = QPushButton("₹5000 Donation")
        self.test_large_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_large_btn.clicked.connect(lambda: self._send_test(5000))
        quick_btn_layout.addWidget(self.test_large_btn)
        
        self.test_random_btn = QPushButton("🎲 Random")
        self.test_random_btn.setObjectName("primaryButton")
        self.test_random_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_random_btn.clicked.connect(lambda: self.send_test_donation.emit({}))
        quick_btn_layout.addWidget(self.test_random_btn)
        
        quick_layout.addLayout(quick_btn_layout)
        layout.addWidget(quick_group)
        
        # Continuous generation section
        continuous_group = QFrame()
        continuous_group.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 45, 0.8);
                border-radius: 16px;
                border: 1px solid #2a2a3c;
            }
        """)
        continuous_layout = QVBoxLayout(continuous_group)
        continuous_layout.setContentsMargins(24, 24, 24, 24)
        continuous_layout.setSpacing(16)
        
        continuous_title = QLabel("Continuous Mock Generation")
        continuous_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #ffffff;")
        continuous_layout.addWidget(continuous_title)
        
        continuous_desc = QLabel("Simulate a realistic stream of donations at random intervals")
        continuous_desc.setStyleSheet("color: #8888a0; font-size: 13px;")
        continuous_layout.addWidget(continuous_desc)
        
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Interval Range:"))
        
        from PySide6.QtWidgets import QDoubleSpinBox
        self.min_interval_spin = QDoubleSpinBox()
        self.min_interval_spin.setRange(0.5, 60)
        self.min_interval_spin.setValue(3)
        self.min_interval_spin.setSuffix("s")
        interval_layout.addWidget(self.min_interval_spin)
        
        interval_layout.addWidget(QLabel("to"))
        
        self.max_interval_spin = QDoubleSpinBox()
        self.max_interval_spin.setRange(1, 120)
        self.max_interval_spin.setValue(10)
        self.max_interval_spin.setSuffix("s")
        interval_layout.addWidget(self.max_interval_spin)
        
        interval_layout.addStretch()
        continuous_layout.addLayout(interval_layout)
        
        continuous_btn_layout = QHBoxLayout()
        
        self.start_continuous_btn = QPushButton("▶ Start Continuous")
        self.start_continuous_btn.setObjectName("successButton")
        self.start_continuous_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_continuous_btn.clicked.connect(self._toggle_continuous)
        continuous_btn_layout.addWidget(self.start_continuous_btn)
        
        continuous_btn_layout.addStretch()
        continuous_layout.addLayout(continuous_btn_layout)
        
        layout.addWidget(continuous_group)
        
        # Stress test section
        stress_group = QFrame()
        stress_group.setStyleSheet("""
            QFrame {
                background: rgba(240, 71, 71, 0.1);
                border-radius: 16px;
                border: 1px solid rgba(240, 71, 71, 0.3);
            }
        """)
        stress_layout = QVBoxLayout(stress_group)
        stress_layout.setContentsMargins(24, 24, 24, 24)
        stress_layout.setSpacing(16)
        
        stress_title = QLabel("⚠️ Stress Test")
        stress_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #f04747;")
        stress_layout.addWidget(stress_title)
        
        stress_desc = QLabel("Send rapid bursts of donations to test system stability")
        stress_desc.setStyleSheet("color: #8888a0; font-size: 13px;")
        stress_layout.addWidget(stress_desc)
        
        stress_settings = QHBoxLayout()
        
        from PySide6.QtWidgets import QSpinBox
        stress_settings.addWidget(QLabel("Count:"))
        self.stress_count_spin = QSpinBox()
        self.stress_count_spin.setRange(1, 100)
        self.stress_count_spin.setValue(20)
        stress_settings.addWidget(self.stress_count_spin)
        
        stress_settings.addWidget(QLabel("Interval:"))
        self.stress_interval_spin = QDoubleSpinBox()
        self.stress_interval_spin.setRange(0.05, 1)
        self.stress_interval_spin.setValue(0.2)
        self.stress_interval_spin.setSuffix("s")
        stress_settings.addWidget(self.stress_interval_spin)
        
        stress_settings.addStretch()
        stress_layout.addLayout(stress_settings)
        
        # Stress test buttons
        stress_btn_layout = QHBoxLayout()
        
        self.stress_btn = QPushButton("🔥 Run Stress Test")
        self.stress_btn.setObjectName("dangerButton")
        self.stress_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stress_btn.clicked.connect(self._toggle_stress_test)
        stress_btn_layout.addWidget(self.stress_btn)
        
        stress_btn_layout.addStretch()
        stress_layout.addLayout(stress_btn_layout)
        
        layout.addWidget(stress_group)
        
        layout.addStretch()
    
    def _send_test(self, amount: int):
        """Send a test donation with specific amount"""
        self.send_test_donation.emit({
            "sender": "Test User",
            "amount": amount,
            "currency": "INR",
            "message": f"Test donation of ₹{amount}!"
        })
    
    def _toggle_continuous(self):
        """Toggle continuous generation"""
        if self._continuous_running:
            self._continuous_running = False
            self.start_continuous_btn.setText("▶ Start Continuous")
            self.start_continuous_btn.setObjectName("successButton")
            self.stop_continuous.emit()
        else:
            self._continuous_running = True
            self.start_continuous_btn.setText("⏹ Stop")
            self.start_continuous_btn.setObjectName("dangerButton")
            self.start_continuous.emit(
                self.min_interval_spin.value(),
                self.max_interval_spin.value()
            )
        
        self.start_continuous_btn.style().unpolish(self.start_continuous_btn)
        self.start_continuous_btn.style().polish(self.start_continuous_btn)
    
    def _toggle_stress_test(self):
        """Toggle stress test"""
        if self._stress_running:
            self._stress_running = False
            self.stress_btn.setText("🔥 Run Stress Test")
            self.stress_count_spin.setEnabled(True)
            self.stress_interval_spin.setEnabled(True)
            self.stop_stress_test.emit()
        else:
            self._stress_running = True
            self.stress_btn.setText("⏹ Stop Stress Test")
            self.stress_count_spin.setEnabled(False)
            self.stress_interval_spin.setEnabled(False)
            self.start_stress_test.emit(
                self.stress_count_spin.value(),
                self.stress_interval_spin.value()
            )
        
        self.stress_btn.style().unpolish(self.stress_btn)
        self.stress_btn.style().polish(self.stress_btn)
    
    def set_continuous_running(self, running: bool):
        """Update the continuous running state"""
        self._continuous_running = running
        if running:
            self.start_continuous_btn.setText("⏹ Stop")
        else:
            self.start_continuous_btn.setText("▶ Start Continuous")
    
    def set_stress_running(self, running: bool):
        """Update the stress test running state"""
        self._stress_running = running
        self.stress_count_spin.setEnabled(not running)
        self.stress_interval_spin.setEnabled(not running)
        if running:
            self.stress_btn.setText("⏹ Stop Stress Test")
        else:
            self.stress_btn.setText("🔥 Run Stress Test")

