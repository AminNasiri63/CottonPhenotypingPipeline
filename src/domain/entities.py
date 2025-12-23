from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImageSample:
    path: Path
    root_path: Path
    folder_name: str
    lat: float
    long: float


@dataclass(frozen=True)
class BoundingBox:
    x: int
    y: int
    w: int
    h: int


@dataclass(frozen=True)
class PatchRegion:
    x: int
    y: int
    w: int
    h: int
    patch_id: int


@dataclass(frozen=True)
class GreennessMeasurement:
    image_path: Path
    folder_name: str
    lat: float
    long: float
    patch_id: int
    patch_region: PatchRegion
    greenness_value: float
