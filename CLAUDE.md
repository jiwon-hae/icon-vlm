# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

icon-vlm is an icon generation system using diffusion models with vision-language model (VLM) integration. The project aims to generate high-quality icon images using LoRA fine-tuning on diffusion models, with CLIP encoders for text and image conditioning.

## Architecture

The codebase follows a modular architecture with three main components:

### 1. Data Pipeline (`data/`)
- **Dataset sourcing**: Downloads icon datasets from Bootstrap Icons, Feather Icons, Heroicons, and FontAwesome
- **Format conversion**: Converts SVG icons to PNG using CairoSVG ([svg2png.py](data/svg2png.py))
- **Data organization**: Maintains three directories:
  - `icons_raw/`: Original SVG files from various icon libraries
  - `icons_png/`: Converted PNG files (256x256)
  - `icons_unique/`: Deduplicated icons
- **Dataset preparation**: [download_dataset.ipynb](data/download_dataset.ipynb) orchestrates the download and conversion pipeline

### 2. Encoders (`src/encoders/`)
- **CLIP encoder** ([clip_encoder.py](src/encoders/clip_encoder.py)): Encodes text prompts and reference images using CLIP
- **Image preprocessor** ([image_preprocessor.py](src/encoders/image_preprocessor.py)): Handles image preprocessing for diffusion model input

### 3. Diffusion Model (`src/diffusion/`)
- **LoRA training** ([train_lora.py](src/diffusion/train_lora.py)): Fine-tunes diffusion models using LoRA adapters
- **Inference** ([infer_diffusion.py](src/diffusion/infer_diffusion.py)): Generates icons from text/image prompts
- **Scheduler configuration** ([scheduler_config.py](src/diffusion/scheduler_config.py)): Configures diffusion sampling schedulers

## Configuration

The project uses YAML-based configuration in `configs/`:
- [training.yaml](configs/training.yaml): Training hyperparameters, optimizer settings, batch size
- [model.yaml](configs/model.yaml): Model architecture, pretrained weights, CLIP variant
- [lora.yaml](configs/lora.yaml): LoRA rank, alpha, target modules
- [serving.yaml](configs/serving.yaml): Inference settings, sampling parameters

## Development Environment

### Python Environment
The project uses conda environment `icongen` with Python 3.10. Key dependencies include:
- `pillow`: Image processing
- `cairosvg`: SVG to PNG conversion
- `tqdm`: Progress bars
- `requests`: HTTP requests for dataset downloads
- `python-slugify`: Filename normalization

### Data Collection
To download and prepare the icon dataset:
```bash
jupyter notebook data/download_dataset.ipynb
```

The notebook will:
1. Download icon sets from GitHub repositories (Bootstrap, Feather, Heroicons, FontAwesome)
2. Extract all SVG files into `data/icons_raw/`
3. Convert SVGs to 256x256 PNGs using [svg2png.py](data/svg2png.py)
4. Store converted images in `data/icons_png/`

## Project Structure Notes

- The project is in early development - most Python modules in `src/` are empty placeholders
- Configuration files in `configs/` are empty and need to be populated with actual parameters
- The data pipeline is functional and can download ~4000 icons from major icon libraries
- Git ignores `data/icons_raw/*` to avoid tracking large binary files
