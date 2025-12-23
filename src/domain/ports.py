from typing import Protocol
import numpy as np
from pathlib import Path
from .entities import BoundingBox, PatchRegion, GreennessMeasurement, ImageSample


class ImageLoaderPort(Protocol):
    def load(self, path: Path) -> np.ndarray:
        ...


class ColorCheckerDetectorPort(Protocol):
    def detect(self, image_path: str) -> tuple[np.ndarray]:
        ...


class ColorCalibratorPort(Protocol):
    def calibrate(self, image: np.ndarray, swatches: np.ndarray) -> np.ndarray:
        ...


class PatchSelectorPort(Protocol):
    def select_patches(
        self,
        image: np.ndarray,
        checker_bbox: BoundingBox,
        num_patches: int
    ) -> list[PatchRegion]:
        ...


class GreennessIndexCalculatorPort(Protocol):
    def compute(self, patch: np.ndarray, mask: np.ndarray) -> float:
        ...


class ResultWriterPort(Protocol):
    def write_all(self, measurements: list[GreennessMeasurement]) -> None:
        ...


class DatasetDiscoveryPort(Protocol):
    def discover_images(self, root: Path) -> list[ImageSample]:
        ...

class LeafSegmentationPort(Protocol):
    def extract(self, image: np.ndarray, checker_bbox: np.ndarray) -> np.ndarray:
        ...