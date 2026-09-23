import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QRect, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import theme
from generator import (
    DEFAULT_GUIDANCE,
    DEFAULT_MODEL_ID,
    DEFAULT_STEPS,
    MODEL_DIR,
)
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

    def clear_image(self):
        self._source_pixmap = None
        self.setText("Your generated image will appear here")
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

        x = available.x() + max(
            0,
            (available.width() - scaled.width()) // 2,
        )
        y = available.y() + max(
            0,
            (available.height() - scaled.height()) // 2,
        )

        target = QRect(x, y, scaled.width(), scaled.height())

        path = QPainterPath()
        path.addRoundedRect(
            QRectF(target),
            self._radius,
            self._radius,
        )

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
        self.loader = None
        self.worker = None
        self.current_image = None
        self.current_seed = None

        self.setWindowTitle("Nova Image AI")
        self.setMinimumSize(1180, 760)
        self.resize(1280, 820)

        self._build_ui()
        self._apply_theme()
        self._start_model_loading()

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        main = QVBoxLayout(root)
        main.setContentsMargins(28, 24, 28, 24)
        main.setSpacing(18)

        header = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(3)

        title = QLabel("Nova Image AI")
        title.setObjectName("appTitle")

        subtitle = QLabel(
            "Local text-to-image generation powered by "
            "PyTorch + Diffusers"
        )
        subtitle.setObjectName("appSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        header.addLayout(title_box)
        header.addStretch()

        self.device_label = QLabel("Loading model…")
        self.device_label.setObjectName("statusLabel")
        header.addWidget(self.device_label)

        main.addLayout(header)

        content = QGridLayout()
        content.setHorizontalSpacing(18)
        content.setVerticalSpacing(18)
        content.setColumnStretch(0, 1)
        content.setColumnStretch(1, 1)
        content.setRowStretch(0, 1)

        preview_card = QFrame()
        preview_card.setObjectName("card")

        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(18, 18, 18, 18)
        preview_layout.setSpacing(10)

        preview_label = QLabel("PREVIEW")
        preview_label.setObjectName("sectionLabel")
        preview_layout.addWidget(preview_label)

        self.image_view = ImageView()
        preview_layout.addWidget(self.image_view, 1)

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Save Image")
        self.save_button.setObjectName("secondaryButton")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("secondaryButton")
        self.clear_button.clicked.connect(
            self.image_view.clear_image
        )

        buttons.addWidget(self.save_button)
        buttons.addWidget(self.clear_button)
        buttons.addStretch()

        preview_layout.addLayout(buttons)

        content.addWidget(preview_card, 0, 0)

        controls_card = QFrame()
        controls_card.setObjectName("card")

        controls = QVBoxLayout(controls_card)
        controls.setContentsMargins(22, 22, 22, 22)
        controls.setSpacing(12)

        prompt_label = QLabel("PROMPT")
        prompt_label.setObjectName("sectionLabel")
        controls.addWidget(prompt_label)

        preset_row = QHBoxLayout()

        preset_label = QLabel("Style")
        preset_label.setObjectName("fieldLabel")

        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Custom",
            "Photorealistic",
            "Cinematic",
            "Digital Art",
            "Anime",
        ])
        self.preset_combo.currentTextChanged.connect(
            self._apply_preset
        )

        preset_row.addWidget(preset_label)
        preset_row.addWidget(self.preset_combo, 1)

        controls.addLayout(preset_row)

        self.prompt_edit = QPlainTextEdit()
        self.prompt_edit.setPlaceholderText(
            "Describe the image you want to create…"
        )
        self.prompt_edit.setFixedHeight(130)
        controls.addWidget(self.prompt_edit)

        negative_label = QLabel("NEGATIVE PROMPT")
        negative_label.setObjectName("sectionLabel")
        controls.addWidget(negative_label)

        self.negative_edit = QPlainTextEdit()
        self.negative_edit.setPlaceholderText(
            "Optional: blurry, distorted, low quality…"
        )
        self.negative_edit.setFixedHeight(85)
        controls.addWidget(self.negative_edit)

        settings_label = QLabel("GENERATION SETTINGS")
        settings_label.setObjectName("sectionLabel")
        controls.addWidget(settings_label)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)

        def add_field(row, col, label, widget):
            text = QLabel(label)
            text.setObjectName("fieldLabel")
            grid.addWidget(text, row, col * 2)
            grid.addWidget(widget, row, col * 2 + 1)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(256, 1536)
        self.width_spin.setSingleStep(64)
        self.width_spin.setValue(512)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(256, 1536)
        self.height_spin.setSingleStep(64)
        self.height_spin.setValue(512)

        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(1, 100)
        self.steps_spin.setValue(DEFAULT_STEPS)

        self.guidance_spin = QDoubleSpinBox()
        self.guidance_spin.setRange(0.0, 20.0)
        self.guidance_spin.setSingleStep(0.5)
        self.guidance_spin.setValue(DEFAULT_GUIDANCE)

        self.seed_spin = QSpinBox()
        self.seed_spin.setRange(0, 2_147_483_647)
        self.seed_spin.setSpecialValueText("Random")
        self.seed_spin.setValue(0)

        add_field(0, 0, "Width", self.width_spin)
        add_field(0, 1, "Height", self.height_spin)
        add_field(1, 0, "Steps", self.steps_spin)
        add_field(1, 1, "Guidance", self.guidance_spin)
        add_field(2, 0, "Seed", self.seed_spin)

        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        controls.addLayout(grid)

        settings_hint = QLabel(
            "SD 1.5: 512×512 • 25–35 steps • Guidance 6–8"
        )
        settings_hint.setObjectName("footnoteLabel")
        settings_hint.setWordWrap(True)
        controls.addWidget(settings_hint)

        controls.addStretch()

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 0)
        self.progress.hide()

        controls.addWidget(self.progress)

        self.generate_button = QPushButton("Generate Image")
        self.generate_button.setObjectName("primaryButton")
        self.generate_button.setMinimumHeight(48)
        self.generate_button.clicked.connect(self.generate)
        self.generate_button.setEnabled(False)

        controls.addWidget(self.generate_button)

        self.status_label = QLabel(
            "Preparing the image model…"
        )
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)

        controls.addWidget(self.status_label)

        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)

        controls.addWidget(self.error_label)

        content.addWidget(controls_card, 0, 1)
        main.addLayout(content, 1)

        footnote = QLabel(
            f"Model: Stable Diffusion 1.5  •  Local: {MODEL_DIR}"
        )
        footnote.setObjectName("footnoteLabel")
        main.addWidget(footnote)

    def _apply_preset(self, preset):
        presets = {
            "Custom": "",
            "Photorealistic": (
                "photorealistic, highly detailed, natural lighting, "
                "realistic textures, sharp focus"
            ),
            "Cinematic": (
                "cinematic composition, dramatic lighting, "
                "volumetric light, film still, detailed atmosphere"
            ),
            "Digital Art": (
                "high quality digital art, detailed illustration, "
                "beautiful composition, polished artwork"
            ),
            "Anime": (
                "anime style, detailed illustration, expressive lighting, "
                "clean line art, vibrant colors"
            ),
        }

        selected = presets.get(preset, "")

        if not selected:
            return

        current = self.prompt_edit.toPlainText().strip()

        if selected.lower() in current.lower():
            return

        if current:
            self.prompt_edit.setPlainText(
                f"{current}, {selected}"
            )
        else:
            self.prompt_edit.setPlainText(selected)

    def _apply_theme(self):
        self.setStyleSheet(theme.qss())
        theme.add_shadow(
            self.findChild(QFrame, "card")
        )

        cards = self.findChildren(QFrame, "card")

        for card in cards:
            theme.add_shadow(card)

    def _start_model_loading(self):
        self.loader = ModelLoader(
            DEFAULT_MODEL_ID,
            self,
        )

        self.loader.loaded.connect(
            self._model_loaded
        )

        self.loader.failed.connect(
            self._model_failed
        )

        self.loader.start()

    def _model_loaded(self, engine, device):
        self.engine = engine

        self.device_label.setText(
            f"Ready • {device.upper()}"
        )

        self.status_label.setText(
            "Model loaded. Enter a prompt and generate."
        )

        self.generate_button.setEnabled(True)
        self.loader = None

    def _model_failed(self, message):
        self.device_label.setText(
            "Model failed to load"
        )

        self.status_label.setText(
            "The model could not be loaded. "
            "Check the error below."
        )

        self.error_label.setText(message)
        self.generate_button.setEnabled(False)
        self.loader = None

    def generate(self):
        if self.engine is None:
            return

        prompt = self.prompt_edit.toPlainText().strip()

        if not prompt:
            self.error_label.setText(
                "Please enter a prompt."
            )
            return

        self.error_label.clear()
        self.generate_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.progress.show()

        self.status_label.setText(
            "Generating image…"
        )

        seed_value = self.seed_spin.value()
        seed = None if seed_value == 0 else seed_value

        self.worker = GenerationWorker(
            engine=self.engine,
            prompt=prompt,
            negative_prompt=self.negative_edit.toPlainText(),
            width=self.width_spin.value(),
            height=self.height_spin.value(),
            steps=self.steps_spin.value(),
            guidance_scale=self.guidance_spin.value(),
            seed=seed,
            parent=self,
        )

        self.worker.succeeded.connect(
            self._generation_succeeded
        )

        self.worker.failed.connect(
            self._generation_failed
        )

        self.worker.finished.connect(
            self._worker_finished
        )

        self.worker.start()

    def _generation_succeeded(self, image, seed):
        self.current_image = image
        self.current_seed = seed

        image_path = (
            OUTPUT_DIR
            / f"image_{datetime.now():%Y%m%d_%H%M%S}_{seed}.png"
        )

        self.engine.save(
            image,
            image_path,
        )

        rgba = image.convert("RGBA")
        data = rgba.tobytes("raw", "RGBA")

        qimage = __import__(
            "PySide6.QtGui",
            fromlist=["QImage"],
        ).QImage(
            data,
            rgba.width,
            rgba.height,
            rgba.width * 4,
            __import__(
                "PySide6.QtGui",
                fromlist=["QImage"],
            ).QImage.Format_RGBA8888,
        ).copy()

        pixmap = QPixmap.fromImage(qimage)

        self.image_view.set_source_pixmap(
            pixmap
        )

        self.save_button.setEnabled(True)

        self.status_label.setText(
            f"Generated successfully • seed {seed} "
            f"• saved to {image_path.name}"
        )

    def _generation_failed(self, message):
        self.error_label.setText(message)
        self.status_label.setText(
            "Generation failed."
        )

    def _worker_finished(self):
        self.progress.hide()

        self.generate_button.setEnabled(
            self.engine is not None
        )

        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

    def save_image(self):
        if self.current_image is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save generated image",
            str(OUTPUT_DIR / "generated.png"),
            "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)",
        )

        if path:
            self.current_image.save(path)

            self.status_label.setText(
                f"Saved: {Path(path).name}"
            )

    def closeEvent(self, event):
        if (
            self.worker is not None
            and self.worker.isRunning()
        ):
            self.worker.wait(3000)

        if (
            self.loader is not None
            and self.loader.isRunning()
        ):
            self.loader.wait(3000)

        if self.engine is not None:
            self.engine.clear_cuda()

        event.accept()


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()