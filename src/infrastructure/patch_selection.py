import numpy as np
from domain.ports import PatchSelectorPort
from domain.entities import PatchRegion


def _extract_feature(patch: np.ndarray) -> np.ndarray:
    pass


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    pass


class CorrelationBasedPatchSelector(PatchSelectorPort):
    def __init__(self, stride_fraction: float = 0.5):
        self.stride_fraction = stride_fraction

    def select_patches(self, image: np.ndarray, checker_bbox: np.ndarray, num_patches: int) -> list[PatchRegion]:
        h_img, w_img, _ = image.shape
        # x1, y1 = np.min(checker_bbox, axis=0)
        # x2, y2 = np.max(checker_bbox, axis=0)

        selected: list[PatchRegion] = []
        selected.append(PatchRegion(x=0, y=0, w=w_img-1, h=h_img-1, patch_id=0))

        return selected
