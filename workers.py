import random

from PySide6.QtCore import QThread, Signal

from generator import ImageGenerator


class ModelLoader(QThread):
    loaded = Signal(object, str)
    failed = Signal(str)

    def __init__(self, model_id, parent=None):
        super().__init__(parent)
        self.model_id = model_id

    def run(self):
        try:
            engine = ImageGenerator(self.model_id)
            self.loaded.emit(engine, engine.device)
        except Exception as exc:
            self.failed.emit(str(exc))


class GenerationWorker(QThread):
    succeeded = Signal(object, int)
    failed = Signal(str)

    def __init__(
        self,
        engine,
        prompt,
        negative_prompt,
        steps,
        guidance_scale,
        seed,
        parent=None,
    ):
        super().__init__(parent)
        self.engine = engine
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.steps = steps
        self.guidance_scale = guidance_scale
        self.seed = seed

    def run(self):
        try:
            seed = self.seed

            if seed is None:
                seed = random.randint(1, 2147483647)

            image = self.engine.generate(
                prompt=self.prompt,
                negative_prompt=self.negative_prompt,
                steps=self.steps,
                guidance_scale=self.guidance_scale,
                seed=seed,
            )

            self.succeeded.emit(image, seed)

        except Exception as exc:
            self.failed.emit(str(exc))