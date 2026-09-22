import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QRect, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QImage,
    QKeySequence,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import theme
from generator import DEFAULT_GUIDANCE, DEFAULT_MODEL_ID, DEFAULT_STEPS, MODEL_DIR
from workers import GenerationWorker, ModelLoader

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class ImageView(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("imagePlaceholder")
        self.setAlignment(Qt.AlignCenter)
        self.setText("Your generated image will appear here")
        self.setMinimumSize(460, 460)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._source_pixmap = None
        self._padding = 22
        self._radius = 18

    def set_source_pixmap(self, pixmap):
        self._source_pixmap = pixmap
        self.setText("")
        self.update()

    def paintEvent(self, event):
        if self._source_pixmap is None:
            super().paintEvent(event)
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        available = QRect(
            self.rect().x() + self._padding,
            self.rect().y() + self._padding,
            max(1, self.rect().width() - self._padding * 2),
            max(1, self.rect().height() - self._padding * 2),
        )

        scaled = self._source_pixmap.scaled(
            available.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        x = available.x() + max(0, (available.width() - scaled.width()) // 2)
        y = available.y() + max(0, (available.height() - scaled.height()) // 2)
        target = QRect(x, y, scaled.width(), scaled.height())

        path = QPainterPath()
        path.addRoundedRect(QRectF(target), self._radius, self._radius)

        painter.setClipPath(path)
        painter.drawPixmap(target, scaled)

        painter.setClipping(False)
        painter.setPen(QPen(QColor(0, 0, 0, 16), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.engine = None
       