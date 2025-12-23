import argparse
from pathlib import Path
from config.settings import ProjectConfig
import matplotlib.pyplot as plt
import os


def parse_args() -> ProjectConfig:
    parser = argparse.ArgumentParser(description="Cotton greenness pipeline")
    parser.add_argument("--input-root", type=str, required=True)
    parser.add_argument("--output-csv", type=str, required=True)
    parser.add_argument("--output-fig", type=str, default=None)
    parser.add_argument("--num-patches", type=int, default=1)
    parser.add_argument("--segment-method", type=str, default="nexg")
    parser.add_argument("--green-indx", type=str, default="ngrdi")
    args = parser.parse_args()

    return ProjectConfig(
        input_root=Path(args.input_root),
        output_csv=Path(args.output_csv),
        output_figure=Path(args.output_fig) if args.output_fig else Path(args.output_csv).parent,
        num_patches_per_image=args.num_patches,
        segment_method=args.segment_method,
        green_indx=args.green_indx,
    )

def visualizer(path: Path, show: bool ,**images) -> None:
    """PLot images in one row."""
    n = len(images)
    plt.figure(num='Results', figsize=(16, 5))
    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image, cmap='viridis')

    plt.tight_layout()

    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, bbox_inches="tight", dpi=300)

    if show:
        plt.show()

    plt.close()

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')