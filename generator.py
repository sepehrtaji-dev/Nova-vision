from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image

DEFAULT_MODEL_ID = "runwayml/stable-diffusion-v1-5"
MODEL_DIR = Path(r"D:\Ai_models\stable-diffusion-v1-5")
DEFAULT_STEPS = 30
DEFAULT_GUIDANCE = 7.0


class ImageGenerator:
    def __init__(self, model_id=DEFAULT_MODEL_ID):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id
        self.model_source = self._resolve_model_source(model_id)

        if self.device == "cuda":
            dtype = torch.float16
        else:
            dtype = torch.float32

        load_kwargs = {
            "torch_dtype": dtype,
            "use_safetensors": True,
        }

        if self.model_source == model_id:
            load_kwargs["cache_dir"] = str(MODEL_DIR)
        elif self._has_variant_files(MODEL_DIR):
            load_kwargs["variant"] = "fp16"

        self.pipe = AutoPipelineForText2Image.from_pretrained(
            self.model_source,
            **load_kwargs,
        )

        self._configure_memory()

    @staticmethod
    def _resolve_model_source(model_id):
        local_dir = Path(model_id)
        if local_dir.is_dir():
            return str(local_dir)

        if MODEL_DIR.is_dir() and (MODEL_DIR / "model_index.json").exists():
            return str(MODEL_DIR)

        return model_id

    @staticmethod
    def _has_variant_files(path):
        return any(path.glob("*fp16*"))

    def _configure_memory(self):
        if self.device == "cuda":
            if hasattr(self.pipe, "enable_vae_slicing"):
                self.pipe.enable_vae_slicing()

            if hasattr(self.pipe, "enable_vae_tiling"):
                self.pipe.enable_vae_tiling()

            try:
                self.pipe.enable_model_cpu_offload()
            except Exception:
                self.pipe = self.pipe.to("cuda")
        else:
            self.pipe = self.pipe.to("cpu")

    @torch.inference_mode()
    def generate(
        self,
        prompt,
        negative_prompt=None,
        width=1024,
        height=1024,
        steps=DEFAULT_STEPS,
        guidance_scale=DEFAULT_GUIDANCE,
        seed=None,
    ):
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        width = max(64, int(width))
        height = max(64, int(height))
        steps = max(1, int(steps))
        guidance_scale = max(0.0, float(guidance_scale))

        generator = None
        if seed is not None:
            seed = int(seed)
            generator = torch.Generator(device=self.device).manual_seed(seed)

        result = self.pipe(
            prompt=prompt.strip(),
            negative_prompt=(negative_prompt.strip() if negative_prompt else None),
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        )

        return result.images[0]

    def save(self, image, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)

    def clear_cuda(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
