"""
StreamAlerts - UPI Donation Overlay System
Main application entry point
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QColor

from src.ui.main_window import MainWindow


def setup_application() -> QApplication:
    """Configure and create the application instance"""
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("StreamAlerts")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("StreamAlerts")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(13, 13, 20))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.Base, QColor(22, 22, 31))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(30, 30, 45))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(30, 30, 45))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.Button, QColor(42, 42, 60))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(232, 232, 240))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(114, 137, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(88, 101, 242))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    return app


def main():
    """Main entry point"""
    print("=" * 50)
    print("  StreamAlerts - UPI Donation Overlay System")
    print("  Version 1.0.0")
    print("=" * 50)
    print()
    
    # Create application
    app = setup_application()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    print("Application started successfully!")
    print()
    print("Server URLs:")
    print(f"  Donation Endpoint: http://127.0.0.1:8765/donation")
    print(f"  OBS Overlay URL:   http://127.0.0.1:8080")
    print()
    print("Add the Overlay URL as a Browser Source in OBS Studio")
    print()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
