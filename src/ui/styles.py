"""
Liquid Glass Theme Styles for StreamAlerts
Premium glassmorphism streamer-grade UI design
"""

# Main application stylesheet - LIQUID GLASS THEME
MAIN_STYLESHEET = """
/* ============================================
   StreamAlerts - Liquid Glass Theme
   Premium Glassmorphism Design
   ============================================ */

/* Global Styles */
* {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0a0a12, stop:0.5 #0e1420, stop:1 #0a1018);
}

QWidget {
    color: #e8f4ff;
    font-size: 13px;
}

/* Sidebar Navigation - Liquid Glass */
#sidebar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(20, 30, 48, 0.95), stop:1 rgba(15, 25, 40, 0.9));
    border-right: 1px solid rgba(168, 237, 234, 0.15);
    border-radius: 0;
}

#sidebar QPushButton {
    background: transparent;
    border: none;
    border-radius: 14px;
    padding: 16px 20px 18px 20px;
    text-align: left;
    color: rgba(168, 237, 234, 0.7);
    font-size: 14px;
    font-weight: 500;
    margin: 3px 12px;
}

#sidebar QPushButton:hover {
    background: rgba(168, 237, 234, 0.08);
    color: #a8edea;
}

#sidebar QPushButton:checked,
#sidebar QPushButton[active="true"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.2), stop:1 rgba(254, 214, 227, 0.1));
    color: #a8edea;
    border-left: 3px solid #a8edea;
    margin-left: 9px;
}

#sidebarLogo {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    padding: 24px;
    background: transparent;
}

#sidebarLogoAccent {
    color: #a8edea;
}

/* Status Indicator - Glass Card */
#statusIndicator {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.08), stop:1 rgba(254, 214, 227, 0.05));
    border-radius: 16px;
    padding: 12px 16px;
    margin: 12px;
    border: 1px solid rgba(168, 237, 234, 0.2);
}

#statusDot {
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #a8edea, stop:1 #7fdbda);
}

#statusDot[status="offline"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #fed6e3, stop:1 #f8a5c2);
}

#statusDot[status="connecting"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ffeaa7, stop:1 #fdcb6e);
}

#statusText {
    color: rgba(168, 237, 234, 0.6);
    font-size: 12px;
}

/* Content Panels */
#contentArea {
    background: transparent;
    border-radius: 24px 0 0 0;
}

QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QScrollBar:vertical {
    background: rgba(168, 237, 234, 0.05);
    width: 8px;
    border-radius: 4px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.4), stop:1 rgba(254, 214, 227, 0.3));
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.6), stop:1 rgba(254, 214, 227, 0.5));
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* Glass Cards */
.card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(255, 255, 255, 0.08), stop:1 rgba(255, 255, 255, 0.03));
    border-radius: 20px;
    border: 1px solid rgba(168, 237, 234, 0.15);
    padding: 20px;
}

#previewCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.05), stop:1 rgba(254, 214, 227, 0.03));
    border-radius: 24px;
    border: 1px solid rgba(168, 237, 234, 0.2);
    min-height: 300px;
}

#statsCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.12), stop:1 rgba(168, 237, 234, 0.04));
    border-radius: 20px;
    border: 1px solid rgba(168, 237, 234, 0.25);
    padding: 16px;
}

#queueCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(127, 219, 218, 0.12), stop:1 rgba(127, 219, 218, 0.04));
    border-radius: 20px;
    border: 1px solid rgba(127, 219, 218, 0.25);
    padding: 16px;
}

/* Liquid Glass Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.25), stop:1 rgba(254, 214, 227, 0.15));
    border: 1px solid rgba(168, 237, 234, 0.3);
    border-radius: 14px;
    padding: 12px 24px;
    color: #ffffff;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.35), stop:1 rgba(254, 214, 227, 0.25));
    border-color: rgba(168, 237, 234, 0.5);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.4), stop:1 rgba(254, 214, 227, 0.3));
}

QPushButton:disabled {
    background: rgba(100, 100, 120, 0.2);
    color: rgba(255, 255, 255, 0.3);
    border-color: rgba(100, 100, 120, 0.2);
}

#primaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.4), stop:1 rgba(184, 243, 255, 0.3));
    border: 1px solid rgba(168, 237, 234, 0.5);
    min-width: 140px;
}

#primaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.5), stop:1 rgba(184, 243, 255, 0.4));
    border-color: #a8edea;
}

#successButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(127, 219, 218, 0.4), stop:1 rgba(0, 200, 180, 0.3));
    border: 1px solid rgba(127, 219, 218, 0.5);
}

#successButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(127, 219, 218, 0.5), stop:1 rgba(0, 200, 180, 0.4));
}

#dangerButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(254, 214, 227, 0.4), stop:1 rgba(248, 165, 194, 0.3));
    border: 1px solid rgba(254, 214, 227, 0.5);
}

#dangerButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(254, 214, 227, 0.5), stop:1 rgba(248, 165, 194, 0.4));
}

#secondaryButton {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(168, 237, 234, 0.2);
}

#secondaryButton:hover {
    background: rgba(168, 237, 234, 0.1);
    border-color: rgba(168, 237, 234, 0.35);
}

#iconButton {
    background: rgba(168, 237, 234, 0.08);
    border: 1px solid rgba(168, 237, 234, 0.15);
    border-radius: 12px;
    padding: 8px;
    min-width: 36px;
    max-width: 36px;
}

#iconButton:hover {
    background: rgba(168, 237, 234, 0.15);
}

/* Glass Text Inputs */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(168, 237, 234, 0.2);
    border-radius: 12px;
    padding: 10px 14px;
    color: #e8f4ff;
    font-size: 13px;
    selection-background-color: rgba(168, 237, 234, 0.4);
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: rgba(168, 237, 234, 0.5);
    background: rgba(168, 237, 234, 0.08);
}

QLineEdit:hover, QTextEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: rgba(168, 237, 234, 0.35);
}

/* Glass Combo Box */
QComboBox {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(168, 237, 234, 0.2);
    border-radius: 12px;
    padding: 10px 14px;
    color: #e8f4ff;
    min-width: 150px;
}

QComboBox:hover {
    border-color: rgba(168, 237, 234, 0.35);
}

QComboBox:focus {
    border-color: rgba(168, 237, 234, 0.5);
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid rgba(168, 237, 234, 0.7);
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background: rgba(15, 25, 40, 0.95);
    border: 1px solid rgba(168, 237, 234, 0.25);
    border-radius: 12px;
    selection-background-color: rgba(168, 237, 234, 0.25);
    outline: none;
}

/* Glass Sliders */
QSlider::groove:horizontal {
    height: 6px;
    background: rgba(168, 237, 234, 0.15);
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 18px;
    height: 18px;
    margin: -6px 0;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #a8edea, stop:1 #7fdbda);
    border-radius: 9px;
    border: 2px solid rgba(255, 255, 255, 0.3);
}

QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #b8f3ff, stop:1 #a8edea);
    border-color: rgba(255, 255, 255, 0.5);
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.6), stop:1 rgba(254, 214, 227, 0.4));
    border-radius: 3px;
}

/* Labels */
QLabel {
    color: #e8f4ff;
}

#sectionTitle {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 16px;
}

#subtitle {
    font-size: 13px;
    color: rgba(168, 237, 234, 0.6);
}

#statValue {
    font-size: 28px;
    font-weight: 700;
    color: #a8edea;
}

#statLabel {
    font-size: 12px;
    color: rgba(168, 237, 234, 0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Glass Checkboxes */
QCheckBox {
    spacing: 10px;
    color: #e8f4ff;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 8px;
    border: 2px solid rgba(168, 237, 234, 0.3);
    background: rgba(255, 255, 255, 0.05);
}

QCheckBox::indicator:hover {
    border-color: rgba(168, 237, 234, 0.5);
    background: rgba(168, 237, 234, 0.08);
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.6), stop:1 rgba(127, 219, 218, 0.5));
    border-color: #a8edea;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid rgba(168, 237, 234, 0.2);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.03);
    margin-top: -1px;
}

QTabBar::tab {
    background: transparent;
    padding: 12px 24px;
    margin-right: 4px;
    color: rgba(168, 237, 234, 0.6);
    border-bottom: 3px solid transparent;
}

QTabBar::tab:selected {
    color: #a8edea;
    border-bottom-color: #a8edea;
}

QTabBar::tab:hover:!selected {
    color: rgba(168, 237, 234, 0.8);
}

/* Glass Group Box */
QGroupBox {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.06), stop:1 rgba(254, 214, 227, 0.03));
    border: 1px solid rgba(168, 237, 234, 0.15);
    border-radius: 16px;
    margin-top: 20px;
    padding: 20px;
    font-weight: 600;
    color: #e8f4ff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 0 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0e1420, stop:1 #0a1018);
    color: #a8edea;
}

/* Progress Bar */
QProgressBar {
    background: rgba(168, 237, 234, 0.1);
    border-radius: 6px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(168, 237, 234, 0.7), stop:1 rgba(254, 214, 227, 0.5));
    border-radius: 6px;
}

/* Glass List Widget */
QListWidget {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(168, 237, 234, 0.15);
    border-radius: 16px;
    padding: 8px;
    outline: none;
}

QListWidget::item {
    background: transparent;
    border-radius: 12px;
    padding: 12px;
    margin: 4px 0;
}

QListWidget::item:selected {
    background: rgba(168, 237, 234, 0.15);
}

QListWidget::item:hover:!selected {
    background: rgba(168, 237, 234, 0.08);
}

/* Glass Tooltips */
QToolTip {
    background: rgba(15, 25, 40, 0.95);
    border: 1px solid rgba(168, 237, 234, 0.3);
    border-radius: 10px;
    padding: 8px 12px;
    color: #e8f4ff;
}

/* Glass Menu */
QMenu {
    background: rgba(15, 25, 40, 0.95);
    border: 1px solid rgba(168, 237, 234, 0.25);
    border-radius: 12px;
    padding: 8px 0;
}

QMenu::item {
    padding: 8px 24px;
}

QMenu::item:selected {
    background: rgba(168, 237, 234, 0.2);
}

/* Splitter */
QSplitter::handle {
    background: rgba(168, 237, 234, 0.2);
    width: 2px;
}

QSplitter::handle:hover {
    background: #a8edea;
}

/* Frame styles */
QFrame {
    border-radius: 12px;
}
"""


# Alert preview widget styles - Liquid Glass
ALERT_PREVIEW_STYLE = """
#alertPreview {
    background: transparent;
    border-radius: 20px;
    padding: 20px;
}

#previewContainer {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.05), stop:1 rgba(254, 214, 227, 0.03));
    border-radius: 20px;
    border: 2px dashed rgba(168, 237, 234, 0.3);
    min-height: 250px;
}

#previewLabel {
    color: rgba(168, 237, 234, 0.5);
    font-size: 14px;
}
"""


# Color picker button style
def get_color_button_style(color: str) -> str:
    return f"""
    QPushButton {{
        background: {color};
        border: 2px solid rgba(168, 237, 234, 0.3);
        border-radius: 10px;
        min-width: 40px;
        max-width: 40px;
        min-height: 40px;
        max-height: 40px;
    }}
    QPushButton:hover {{
        border-color: rgba(168, 237, 234, 0.6);
    }}
    """


# History item styles - Liquid Glass
HISTORY_ITEM_STYLE = """
#historyItem {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(168, 237, 234, 0.08), stop:1 rgba(254, 214, 227, 0.04));
    border-radius: 16px;
    padding: 16px;
    border-left: 4px solid #a8edea;
}

#historyItemSender {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
}

#historyItemAmount {
    font-size: 18px;
    font-weight: 700;
    color: #a8edea;
}

#historyItemMessage {
    font-size: 13px;
    color: rgba(168, 237, 234, 0.6);
}

#historyItemTime {
    font-size: 11px;
    color: rgba(168, 237, 234, 0.4);
}
"""
