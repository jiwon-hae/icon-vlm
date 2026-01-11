"""Icon dataset for diffusion model training."""
from pathlib import Path
from typing import Dict
import json
import logging

import torch
import numpy as np
from torch.utils.data import Dataset
from PIL import Image

logger = logging.getLogger(__name__)


class IconDataset(Dataset):
    """Dataset for loading icon images with text captions for diffusion training.

    Args:
        meta_path: Path to JSONL metadata file with 'image' and 'caption' fields
        img_dir: Directory containing the icon images
        tokenizer: HuggingFace tokenizer for text encoding
        size: Target image size (default: 256)
        max_caption_length: Maximum caption length in tokens (default: 77 for SD1.5)
    """

    def __init__(
        self,
        meta_path: Path,
        img_dir: Path,
        tokenizer,
        size: int = 256,
        max_caption_length: int = 77,
    ):
        self.img_dir = Path(img_dir)
        self.size = size
        self.tokenizer = tokenizer
        self.max_caption_length = max_caption_length

        # Load metadata
        self.samples = []
        missing_count = 0

        logger.info(f"Loading dataset from {meta_path}")
        with open(meta_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    ex = json.loads(line)
                    img_name = ex.get("image")
                    caption = ex.get("caption", "")

                    if not img_name:
                        logger.warning(f"Line {line_num}: Missing 'image' field")
                        continue

                    img_path = self.img_dir / img_name
                    if img_path.exists():
                        self.samples.append((str(img_path), caption))
                    else:
                        missing_count += 1

                except json.JSONDecodeError as e:
                    logger.warning(f"Line {line_num}: Invalid JSON - {e}")
                    continue

        if missing_count > 0:
            logger.warning(f"Skipped {missing_count} samples with missing images")

        if len(self.samples) == 0:
            raise ValueError(f"No valid samples found in {meta_path}")

        logger.info(f"Loaded {len(self.samples)} samples successfully")

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """Load and preprocess a single sample.

        Returns:
            Dictionary with 'pixel_values' (tensor) and 'input_ids' (tensor)
        """
        img_path, caption = self.samples[idx]

        # Load and transform image
        try:
            image = Image.open(img_path).convert("RGB")
            # Resize and center crop
            image = image.resize((self.size, self.size), Image.Resampling.LANCZOS)
            # Convert to tensor [0, 1] in CHW format
            pixel_values = torch.from_numpy(np.array(image)).permute(2, 0, 1).float() / 255.0
        except Exception as e:
            logger.error(f"Error loading image {img_path}: {e}")
            # Return a blank image on error
            pixel_values = torch.zeros(3, self.size, self.size)

        # Tokenize caption
        text_inputs = self.tokenizer(
            caption,
            truncation=True,
            padding="max_length",
            max_length=self.max_caption_length,
            return_tensors="pt",
        )
        input_ids = text_inputs.input_ids[0]

        return {
            "pixel_values": pixel_values,
            "input_ids": input_ids,
        }
