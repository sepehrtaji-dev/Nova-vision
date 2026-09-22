from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

WINDOW_BG = "#F5F5F7"
CARD_BG = "#FFFFFF"
BORDER = "#E4E4E9"
TEXT = "#1D1D1F"
SUBTLE = "#86868B"
ACCENT = "#0071E3"
ACCENT_HOVER = "#0077ED"
ACCENT_PRESSED = "#0062C4"
ACCENT_DISABLED = "#B4D5FA"
DANGER = "#FF3B30"


def add_shadow(widget):
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(54)
    effect.setOffset(0, 12)
    effect.setColor(QColor(10, 10, 20, 24))
    widget.setGraphicsEffect(effect)


def qss():
    return """
* {
    font-family: "SF Pro Text", "SF Pro Display", -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    color: #1D1D1F;
    outline: none;
}

QMainWindow,
QWidget#root {
    background-color: #F5F5F7;
}

QLabel#appTitle {
    font-size: 30px;
    font-weight: 700;
}

QLabel#appSubtitle {
    color: #86868B;
    font-size: 14px;
}

QLabel#sectionLabel {
    color: #86868B;
    font-size: 11px;
    font-weight: 700;
}

QLabel#fieldLabel {
    color: #515154;
    font-size: 13px;
}

QLabel#statusLabel,
QLabel#footnoteLabel {
    color: #86868B;
    font-size: 12px;
}

QLabel#errorLabel {
    color: #FF3B30;
    font-size: 12px;
}

QLabel#imagePlaceholder {
    color: #A1A1A6;
    font-size: 15px;
    background: transparent;
}

QFrame#card {
    background-color: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 22px;
}

QPlainTextEdit,
QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #E4E4E9;
    border-radius: 12px;
    padding: 10px 12px;
    font-size: 13px;
    selection-background-color: #0071E3;
    selection-color: #FFFFFF;
}

QPlainTextEdit {
    padding: 12px;
    border-radius: 14px;
    font-size: 14px;
}

QPlainTextEdit:focus,
QLineEdit:focus {
    border: 1px solid #0071E3;
}

QLineEdit:read-only,
QPlainTextEdit:read-only {
    background-color: #FAFAFA;
    color: #A1A1A6;
    border-color: #EDEDF2;
}

QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #E4E4E9;
    border-radius: 12px;
    padding: 11px 18px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #F5F5F7;
}

QPushButton:pressed {
    background-color: #E8E8ED;
}

QPushButton:disabled {
    background-color: #FAFAFA;
    border-color: #EDEDF2;
    color: #C7C7CC;
}

QPushButton#primaryButton {
    background-color: #0071E3;
    border: none;
    border-radius: 14px;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
    padding: 13px 20px;
}

QPushButton#primaryButton:hover {
    background-color: #0077ED;
}

QPushButton#primaryButton:pressed {
    background-color: #0062C4;
}

QPushButton#primaryButton:disabled {
    background-color: #B4D5FA;
    color: #FFFFFF;
}

QPushButton#secondaryButton {
    background-color: #F5F5F7;
    border: none;
    color: #1D1D1F;
}

QPushButton#secondaryButton:hover {
    background-color: #EDEDF2;
}

QPushButton#secondaryButton:pressed {
    background-color: #E4E4E9;
}

QPushButton#secondaryButton:disabled {
    background-color: #F5F5F7;
    color: #C7C7CC;
}

QProgressBar {
    background-color: #E8E8ED;
    border: none;
    border-radius: 2px;
    height: 4px;
}

QProgressBar::chunk {
    background-color: #0071E3;
    border-radius: 2px;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: #C7C7CC;
    border-radius: 5px;
    min-height: 34px;
}

QScrollBar::handle:vertical:hover {
    background: #A1A1A6;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background: #C7C7CC;
    border-radius: 5px;
    min-width: 34px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}

QToolTip {
    background-color: #FFFFFF;
    color: #1D1D1F;
    border: 1px solid #E4E4E9;
    border-radius: 8px;
    padding: 6px 8px;
}
"""