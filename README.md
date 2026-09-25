# Nova Vision

A **PyQt6 desktop app** for AI image generation — generate, preview, and manage images from a local or remote model backend.

## Features

- Clean dark-themed UI built with PyQt6
- Background worker threads (no UI freezing)
- Image download and local saving
- Docker support for easy deployment

## Setup

```bash
pip install -r requirements.txt
python app.py
```

### Docker

```bash
docker-compose up
```

## Project Structure

```
Nova-vision/
├── app.py          # Main PyQt6 application
├── generator.py    # Image generation logic
├── workers.py      # QThread background workers
├── theme.py        # UI theme / stylesheet
├── Downloader.py   # Image download utilities
├── debug_qt.py     # Qt debugging helpers
└── docker-compose.yml
```

## Requirements

See `requirements.txt`.
