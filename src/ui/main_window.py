"""
Main Application Window
Central hub connecting all components
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QSystemTrayIcon, QMenu, QApplication
)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QObject

from datetime import datetime
from typing import Optional

from .sidebar import Sidebar
from .dashboard import DashboardPage
from .designer import OverlayDesignerPage
from .history import HistoryPage, TestingPage
from .settings import SettingsPage
from .onboarding import OnboardingPage
from .styles import MAIN_STYLESHEET

from ..core.models import DonationEvent, AlertTheme
from ..core.event_queue import EventQueue
from ..core.settings import SettingsManager
from ..server.donation_server import DonationServer
from ..server.mock_generator import MockDonationGenerator


class DonationBridge(QObject):
    """Thread-safe bridge for donation events"""
    donation_received = Signal(dict)
    event_ready = Signal(object)  # DonationEvent


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("StreamAlerts - UPI Donation Overlay System")
        self.setMinimumSize(1280, 800)
        self.resize(1400, 900)
        
        # Create signal bridge first
        self._bridge = DonationBridge()
        self._bridge.donation_received.connect(self._handle_donation_in_main_thread)
        self._bridge.event_ready.connect(self._handle_event_ready_in_main_thread)
        
        # Initialize components
        self._settings_manager = SettingsManager()
        self._current_theme = AlertTheme()
        self._start_time = datetime.now()
        self._total_donations = 0
        self._total_amount = 0.0
        
        # Initialize event queue (callbacks will use bridge)
        self._event_queue = EventQueue(
            debounce_ms=self._settings_manager.settings.debounce_ms,
            max_queue_size=self._settings_manager.settings.max_queue_size,
            on_event_ready=self._on_event_ready_from_thread
        )
        self._event_queue.set_display_duration(self._settings_manager.settings.display_duration)
        
        # Initialize server (callback will use bridge)
        self._server = DonationServer(
            host=self._settings_manager.settings.server_host,
            port=self._settings_manager.settings.server_port,
            overlay_port=self._settings_manager.settings.overlay_port,
            on_donation=self._on_donation_from_thread
        )
        
        # Initialize mock generator
        self._mock_generator = MockDonationGenerator(
            on_donation=self._on_donation_from_thread
        )
        
        # Apply stylesheet
        self.setStyleSheet(MAIN_STYLESHEET)
        
        # Setup UI with onboarding
        self._setup_ui()
        self._setup_timers()
        self._setup_connections()
        
        # Check if should show onboarding
        if self._should_show_onboarding():
            self._show_onboarding()
        else:
            self._show_main_app()
        
        # Delay server start until event loop is running
        if self._settings_manager.settings.auto_start_server:
            QTimer.singleShot(200, self._start_server)
    
    def _should_show_onboarding(self) -> bool:
        """Check if onboarding should be shown"""
        # Check settings for skip flag
        settings = self._settings_manager.settings
        return not getattr(settings, 'skip_onboarding', False)
    
    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout for the entire app
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Root stacked widget (onboarding vs main app)
        self.root_stack = QStackedWidget()
        
        # Onboarding page
        self.onboarding_page = OnboardingPage()
        self.onboarding_page.continue_clicked.connect(self._on_onboarding_complete)
        self.onboarding_page.skip_clicked.connect(self._on_onboarding_complete)
        self.root_stack.addWidget(self.onboarding_page)  # Index 0
        
        # Main app container
        self.app_container = QWidget()
        self._setup_main_app_ui()
        self.root_stack.addWidget(self.app_container)  # Index 1
        
        self.main_layout.addWidget(self.root_stack)
    
    def _setup_main_app_ui(self):
        """Setup the main application UI"""
        app_layout = QHBoxLayout(self.app_container)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_changed.connect(self._on_navigation_changed)
        app_layout.addWidget(self.sidebar)
        
        # Content area
        content_widget = QWidget()
        content_widget.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stacked widget for pages
        self.page_stack = QStackedWidget()
        
        # Create pages
        self.dashboard_page = DashboardPage()
        self.designer_page = OverlayDesignerPage()
        self.history_page = HistoryPage()
        self.testing_page = TestingPage()
        self.settings_page = SettingsPage(self._settings_manager.settings)
        
        # Add pages to stack
        self.page_stack.addWidget(self.dashboard_page)    # 0
        self.page_stack.addWidget(self.designer_page)     # 1
        self.page_stack.addWidget(self.history_page)      # 2
        self.page_stack.addWidget(self.testing_page)      # 3
        self.page_stack.addWidget(self.settings_page)     # 4
        
        content_layout.addWidget(self.page_stack)
        app_layout.addWidget(content_widget, 1)
        
        # Update OBS URL on dashboard
        self.dashboard_page.update_obs_url(self._server.overlay_url)
    
    def _show_onboarding(self):
        """Show the onboarding page"""
        self.root_stack.setCurrentIndex(0)
    
    def _show_main_app(self):
        """Show the main application"""
        self.root_stack.setCurrentIndex(1)
    
    def _on_onboarding_complete(self):
        """Handle onboarding completion"""
        # Check if user wants to skip next time
        if self.onboarding_page.should_skip_next_time():
            self._settings_manager.update_setting('skip_onboarding', True)
        
        # Transition to main app
        self._show_main_app()
    
    def _setup_timers(self):
        """Setup update timers"""
        # Stats update timer
        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._update_stats)
        self._stats_timer.start(1000)  # Update every second
    
    def _setup_connections(self):
        """Setup signal connections"""
        # Dashboard
        self.dashboard_page.test_alert_requested.connect(self._send_test_alert)
        
        # Designer
        self.designer_page.theme_changed.connect(self._on_theme_changed)
        self.designer_page.preview_requested.connect(self._send_test_alert)
        
        # History
        self.history_page.replay_alert.connect(self._replay_alert)
        
        # Testing
        self.testing_page.send_test_donation.connect(self._on_test_donation)
        self.testing_page.start_continuous.connect(self._start_continuous_generation)
        self.testing_page.stop_continuous.connect(self._stop_continuous_generation)
        self.testing_page.start_stress_test.connect(self._run_stress_test)
        self.testing_page.stop_stress_test.connect(self._stop_stress_test)
        
        # Settings
        self.settings_page.settings_changed.connect(self._on_settings_changed)
        self.settings_page.restart_server.connect(self._restart_server)
        self.settings_page.view_instructions.connect(self._show_onboarding)
    
    def _on_navigation_changed(self, page_id: str):
        """Handle navigation changes"""
        page_map = {
            "dashboard": 0,
            "designer": 1,
            "history": 2,
            "testing": 3,
            "settings": 4
        }
        
        if page_id in page_map:
            self.page_stack.setCurrentIndex(page_map[page_id])
    
    def _start_server(self):
        """Start the donation server"""
        try:
            self._server.start()
            self._event_queue.start_processing()
            self.sidebar.update_connection_status(True, "Servers running")
        except Exception as e:
            print(f"Error starting server: {e}")
            self.sidebar.update_connection_status(False, str(e))
    
    def _stop_server(self):
        """Stop the donation server"""
        self._server.stop()
        self._event_queue.stop_processing()
        self.sidebar.update_connection_status(False, "Servers stopped")
    
    def _restart_server(self):
        """Restart the donation server"""
        self._stop_server()
        
        # Update server with new settings
        settings = self._settings_manager.settings
        self._server = DonationServer(
            host=settings.server_host,
            port=settings.server_port,
            overlay_port=settings.overlay_port,
            on_donation=self._on_donation_from_thread
        )
        
        self._start_server()
        self.dashboard_page.update_obs_url(self._server.overlay_url)
    
    def _on_donation_from_thread(self, data: dict):
        """Called from server thread - emit signal to main thread"""
        self._bridge.donation_received.emit(data)
    
    def _on_event_ready_from_thread(self, event: DonationEvent):
        """Called from queue thread - emit signal to main thread"""
        self._bridge.event_ready.emit(event)
    
    @Slot(dict)
    def _handle_donation_in_main_thread(self, data: dict):
        """Handle donation in main Qt thread"""
        event = DonationEvent.from_dict(data)
        added = self._event_queue.add_event(event)
        
        if added:
            self._total_donations += 1
            self._total_amount += event.amount
    
    @Slot(object)
    def _handle_event_ready_in_main_thread(self, event):
        """Handle event ready in main Qt thread"""
        if not isinstance(event, DonationEvent):
            return
            
        # Update dashboard preview
        self.dashboard_page.show_alert(event, self._current_theme)
        
        # Add to history
        self.history_page.add_event(event)
        
        # Broadcast to overlay
        self._server.broadcast_donation(event.to_dict(), self._current_theme.to_dict())
    
    def _on_theme_changed(self, theme: AlertTheme):
        """Handle theme changes"""
        self._current_theme = theme
        self._server.update_theme(theme.to_dict())
        self._event_queue.set_display_duration(theme.display_duration)
    
    def _on_settings_changed(self, settings):
        """Handle settings changes"""
        self._settings_manager.settings = settings
        self._settings_manager.save()
        
        # Update queue settings
        self._event_queue.set_debounce(settings.debounce_ms)
        self._event_queue.set_display_duration(settings.display_duration)
    
    def _send_test_alert(self):
        """Send a test alert"""
        self._mock_generator.generate_single()
    
    def _on_test_donation(self, data: dict):
        """Handle test donation request"""
        if data:
            data["timestamp"] = datetime.now().isoformat()
            self._on_donation_from_thread(data)
        else:
            self._mock_generator.generate_single()
    
    def _replay_alert(self, event: DonationEvent):
        """Replay an alert from history"""
        self._handle_event_ready_in_main_thread(event)
    
    def _start_continuous_generation(self, min_interval: float, max_interval: float):
        """Start continuous mock generation"""
        self._mock_generator.start_continuous(min_interval, max_interval)
    
    def _stop_continuous_generation(self):
        """Stop continuous mock generation"""
        self._mock_generator.stop_continuous()
    
    def _run_stress_test(self, count: int, interval: float):
        """Run a stress test"""
        self._mock_generator.stress_test(count, interval)
    
    def _stop_stress_test(self):
        """Stop ongoing stress test"""
        self._mock_generator.stop_stress_test()
        self.testing_page.set_stress_running(False)
    
    def _update_stats(self):
        """Update dashboard statistics"""
        # Calculate uptime
        uptime = datetime.now() - self._start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Get queue stats
        queue_stats = self._event_queue.get_stats()
        
        # Update dashboard
        self.dashboard_page.update_stats(
            total_donations=self._total_donations,
            total_amount=self._total_amount,
            queue_size=queue_stats.queue_size,
            uptime=uptime_str
        )
        
        # Update sidebar status
        if self._server.is_running:
            self.sidebar.update_connection_status(True, f"Queue: {queue_stats.queue_size}")
        else:
            self.sidebar.update_connection_status(False, "Server stopped")
    
    def show_instructions(self):
        """Show the onboarding/instructions page"""
        self._show_onboarding()
    
    def closeEvent(self, event):
        """Handle window close"""
        # Stop all running processes
        self._mock_generator.stop_continuous()
        self._event_queue.stop_processing()
        self._server.stop()
        
        # Save settings
        self._settings_manager.save()
        
        event.accept()
