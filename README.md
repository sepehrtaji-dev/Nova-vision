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

```text
                     Text Prompt
                          │
                          ▼
                   CLIP Text Encoder
                          │
                          ▼
                    Text Embeddings
                          │
                          ▼
              ┌─────────────────────┐
              │       U-Net         │
              │  Diffusion Denoiser │
              └─────────────────────┘
                          │
                          ▼
                    Latent Space
                          │
                          ▼
                         VAE
                          │
                          ▼
                    Generated Image