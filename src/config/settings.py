from dataclasses import dataclass, field
from pathlib import Path
import logging
import torch


@dataclass
class SamLeafSegConfig:
    model_type: str = "vit_h"
    checkpoint_path: str = r"./dlModel/sam_vit_h_4b8939.pth"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    points_per_side: int = 32
    pred_iou_thresh: float = 0.88
    stability_score_thresh: float = 0.92
    crop_n_layers: int = 1
    min_mask_region_area: int = 400

    min_area_frac: float = 0.002
    max_area_frac: float = 0.80
    keep_top_k: int = 12
    green_score_thresh: float = 0.15
    close_kernel: int = 7


@dataclass
class ProjectConfig:
    input_root: Path
    output_csv: Path
    output_figure: Path
    segment_method: str
    green_indx: str
    num_patches_per_image: int = 1

    sam_config: SamLeafSegConfig = field(default_factory=SamLeafSegConfig)


def setup_logging(path: Path, level=logging.INFO):
    path = path.parent / 'run.log'
    path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(path),
            logging.StreamHandler(),
        ],
    )