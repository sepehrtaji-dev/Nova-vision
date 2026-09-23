# Nova Vision

<p align="center">
  <img src="assets/image_20260923_210432_382565694.png" alt="Nova Vision" width="850">
</p>

<p align="center">
  Local AI Text-to-Image Generation
</p>

<p align="center">
  <strong>Python • PyTorch • Stable Diffusion 1.5 • CUDA • PySide6</strong>
</p>

---

## About

**Nova Vision** is an experimental local Text-to-Image AI application built with Python and PyTorch.

It allows users to generate images locally using natural-language prompts without relying on an external image-generation API.

The project is designed as an experimental AI platform with a focus on:

- Local inference
- GPU acceleration
- Prompt-based image generation
- Generation controls
- Clean desktop UI
- Future image editing capabilities

---

## Model Backbone

Nova Vision currently uses **Stable Diffusion v1.5** as its image-generation backbone.

Stable Diffusion is based on a **Latent Diffusion Model (LDM)** architecture.

### Architecture

**Text Prompt**  
↓  
**CLIP Text Encoder**  
↓  
**Text Embeddings**  
↓  
**U-Net Diffusion Denoiser**  
↓  
**Latent Representation**  
↓  
**VAE Decoder**  
↓  
**Generated Image**

### Core Components

| Component | Technology |
|---|---|
| Model | Stable Diffusion v1.5 |
| Architecture | Latent Diffusion |
| Denoiser | U-Net |
| Text Encoder | CLIP |
| Decoder | VAE |
| Framework | PyTorch |
| Inference | Hugging Face Diffusers |
| GPU Acceleration | NVIDIA CUDA |

---

## Features

- 🖼️ Text-to-Image generation
- 🧠 Stable Diffusion 1.5
- ⚡ NVIDIA CUDA acceleration
- ✍️ Prompt support
- 🚫 Negative prompts
- 🎚️ Guidance / CFG control
- 🔢 Seed control
- 🔄 Inference step control
- 📐 Custom image resolution
- 🎨 Style presets
- 💾 PNG / JPEG export
- 💻 Local model loading
- 🖥️ PySide6 desktop interface
- 🐳 Docker support

---

## Generation Controls

### Prompt

Describe the image you want to generate.

Example:

> a futuristic AI laboratory with a humanoid robot, cinematic lighting, highly detailed, realistic

### Negative Prompt

Describe elements that should be avoided.

Example:

> blurry, low quality, distorted, watermark, text, duplicate objects

### Guidance / CFG

Controls how strongly the generation follows the text prompt.

Nova Vision currently uses **7.0** as the default guidance scale.

### Steps

Controls the number of diffusion denoising steps.

A typical starting range for Stable Diffusion 1.5 is **25–35 steps**.

### Seed

A fixed seed can be used to reproduce similar generations with the same settings.

---

## Hardware

Nova Vision is designed to run on consumer NVIDIA GPUs.

Tested configuration:

- **GPU:** NVIDIA RTX 3060
- **VRAM:** 12 GB

The project is optimized around common Stable Diffusion 1.5 resolutions such as **512×512**.

---

## Local Model

The Stable Diffusion 1.5 model is loaded locally.

Example model location:

**D:\Ai_models\SD15**

Keeping the model locally avoids downloading the model every time the application starts.

---

## Project Structure

Nova-Vision/
├── app.py
├── generator.py
├── workers.py
├── theme.py
├── main.py
├── assets/
│   └── image_20260923_210432_382565694.png
├── outputs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

---

## Installation

Clone the repository:

**git clone https://github.com/YOUR_USERNAME/Nova-Vision.git**

Then enter the project directory:

**cd Nova-Vision**

Install the required dependencies:

**pip install -r requirements.txt**

Make sure the Stable Diffusion 1.5 model is available locally.

Then run the application:

**python app.py**

---

## Docker

Nova Vision also includes Docker support.

Build the Docker image:

**docker compose build**

Run the container:

**docker compose up**

The Stable Diffusion model can be mounted from the host instead of being copied into the Docker image.

This keeps the Docker image smaller and avoids storing multiple copies of the model.

---

## Example

Example prompt:

> a futuristic neural network laboratory, glowing artificial intelligence systems, complex electronic circuits, cinematic lighting, highly detailed, professional scientific visualization

Nova Vision generates the resulting image locally using Stable Diffusion 1.5.

---

## Limitations

Because Nova Vision currently uses Stable Diffusion 1.5, some limitations remain:

- Exact object counts are not guaranteed.
- Complex spatial relationships may be inconsistent.
- Text inside generated images can be inaccurate.
- Highly structured diagrams may contain inconsistencies.
- Small details may sometimes be distorted.
- Prompt interpretation depends on the underlying model.

These limitations are part of the current experimental stage.

---

## Roadmap

- [ ] ControlNet
- [ ] Image-to-Image
- [ ] Inpainting
- [ ] LoRA support
- [ ] Image upscaling
- [ ] Improved prompt processing
- [ ] Prompt safety filtering
- [ ] Image safety checking
- [ ] More generation presets
- [ ] Multiple model support
- [ ] API mode
- [ ] Improved Docker deployment

---

## Tech Stack

- **Python**
- **PyTorch**
- **Hugging Face Diffusers**
- **Transformers**
- **Accelerate**
- **Safetensors**
- **Pillow**
- **PySide6**
- **CUDA**
- **Docker**

---

## Project Status

**Experimental — Active Development**

Nova Vision is currently focused on building a solid local image-generation foundation.

Future versions will expand the project toward more controllable generation, image editing, safety mechanisms, and additional AI capabilities.

---

## License

This project is intended for educational and experimental purposes.

Third-party models, model weights, datasets, and dependencies may have their own licenses. Please follow the applicable license terms for each component.

---

<p align="center">
  Built with Python, PyTorch & Stable Diffusion.
</p>