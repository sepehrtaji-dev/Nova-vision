from pathlib import Path
import sys
import time
import os

from huggingface_hub import hf_hub_download


REPO_ID = "runwayml/stable-diffusion-v1-5"
MODEL_DIR = Path(r"D:\Ai_models\SD15")

RETRIES = 20
RETRY_DELAY = 15
ETAG_TIMEOUT = 60

FILES = [
    "model_index.json",

    "scheduler/scheduler_config.json",

    "tokenizer/vocab.json",
    "tokenizer/merges.txt",
    "tokenizer/tokenizer_config.json",
    "tokenizer/special_tokens_map.json",

    "text_encoder/config.json",
    "text_encoder/model.safetensors",

    "unet/config.json",
    "unet/diffusion_pytorch_model.safetensors",

    "vae/config.json",
    "vae/diffusion_pytorch_model.safetensors",

    "feature_extractor/preprocessor_config.json",
]


def download_file(filename):
    print()
    print("=" * 70)
    print(f"FILE: {filename}")
    print("=" * 70)

    for attempt in range(1, RETRIES + 1):
        try:
            print(f"Attempt {attempt}/{RETRIES}")

            result = hf_hub_download(
                repo_id=REPO_ID,
                filename=filename,
                local_dir=str(MODEL_DIR),
                etag_timeout=ETAG_TIMEOUT,
            )

            path = Path(result)

            if path.exists() and path.stat().st_size > 0:
                size_gb = path.stat().st_size / (1024 ** 3)

                print()
                print(f"OK: {filename}")
                print(f"Size: {size_gb:.3f} GB")
                return True

            raise RuntimeError("Downloaded file is missing or empty.")

        except KeyboardInterrupt:
            print()
            print("Download interrupted.")
            print("Run the script again to continue.")
            return False

        except Exception as exc:
            print()
            print(f"ERROR: {type(exc).__name__}")
            print(str(exc))

            if attempt == RETRIES:
                print()
                print(f"FAILED: {filename}")
                return False

            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    return False


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("STABLE DIFFUSION 1.5 - RELIABLE DOWNLOADER")
    print("=" * 70)
    print(f"Repository : {REPO_ID}")
    print(f"Destination: {MODEL_DIR}")
    print(f"Files      : {len(FILES)}")
    print("=" * 70)

    for index, filename in enumerate(FILES, start=1):
        print()
        print(f"[{index}/{len(FILES)}]")

        if not download_file(filename):
            print()
            print("=" * 70)
            print("DOWNLOAD STOPPED")
            print("=" * 70)
            print()
            print(f"Failed file: {filename}")
            print()
            print("Run the script again later.")
            print("Already completed files will remain in place.")
            sys.exit(1)

    print()
    print("=" * 70)
    print("ALL FILES DOWNLOADED")
    print("=" * 70)
    print()
    print(f"Model ready at:")
    print(MODEL_DIR)


if __name__ == "__main__":
    main()