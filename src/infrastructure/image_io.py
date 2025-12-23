import cv2
import numpy as np
from pathlib import Path
from domain.ports import ImageLoaderPort
from domain.exceptions import PipelineError


class OpenCVImageLoader(ImageLoaderPort):
    def load(self, path: Path) -> np.ndarray:
        img = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if img is None:
            raise PipelineError(message='Could not load image', step='Image Loader')
        return img
