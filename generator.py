import os
from pathlib import Path

MODEL_DIR = Path(os.environ.get("IMAGE_STUDIO_MODEL_DIR", r"D:\AI_Models"))
CACHE_DIR = MODEL_DIR / "hub"

try:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
except OSError:
    MODEL_DIR = Path.home() / "AI_Models"
    CACHE_DIR = MODEL_DIR / "hub"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ["HF_HOME"] = str(MODEL_DIR)
os.environ["HF_HUB_CACHE"] = str(CACHE_DIR)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import torch
from diffusers import AutoPipelineForText2Image

DEFAULT_MODEL_ID = "stabilityai/sd-turbo"
DEFAULT_STEPS = 2
DEFAULT_GUIDANCE = 0.0


class ImageGenerator:
    def __init__(self, model_id=DEFAULT_MODEL_ID):
        self.model_id = model_id

        if torch.cuda.is_available():
            self.device = "cuda"
            self.dtype = torch.float16
        elif getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            self.device = "mps"
            self.dtype = torch.float32
        else:
            self.device = "cpu"
            self.dtype = torch.float32

        self.pipe = self._load_pipeline()
        self.pipe.to(self.device)

        if self.device in ("cpu", "mps"):
            self.pipe.enable_attention_slicing()

    def _load_pipeline(self):
        common_kwargs = {
            "torch_dtype": self.dtype,
            "cache_dir": str(CACHE_DIR),
            "low_cpu_mem_usage": True,
        }

        try:
            return AutoPipelineForText2Image.from_pretrained(
                self.model_id,
                safety_checker=None,
                requires_safety_checker=False,
                **common_kwargs,
            )
        except TypeError:
            return AutoPipelineForText2Image.from_pretrained(
                self.model_id,
                **common_kwargs,
            )

    def generate(
        self,
        prompt,
        negative_prompt="",
        steps=DEFAULT_STEPS,
        guidance_scale=DEFAULT_GUIDANCE,
        seed=None,
    ):
        if seed is not None:
            torch.manual_seed(int(seed))

        kwargs = {
            "prompt": prompt,
            "num_inference_steps": int(steps),
            "guidance_scale": float(guidance_scale),
        }

        if negative_prompt:
            kwargs["negative_prompt"] = negative_prompt

        result = self.pipe(**kwargs)
        return result.images[0]