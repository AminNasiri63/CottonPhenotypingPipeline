import numpy as np
from typing import Optional, Tuple
from domain.ports import ColorCheckerDetectorPort
from domain.exceptions import PipelineError
import colour
from colour_checker_detection import (
    detect_colour_checkers_segmentation,
    SETTINGS_SEGMENTATION_COLORCHECKER_CLASSIC
    )


class DeepColorCheckerDetector(ColorCheckerDetectorPort):
    def __init__(self, model_path: str = '', device: str = "cpu"):
        self.model_path = model_path
        self.device = device
        self.model = self._load_model()

    def _load_model(self):
        return None

    def detect(self, image_path: str) -> Tuple[np.ndarray]:

        image = colour.cctf_decoding(colour.io.read_image(image_path))
        colour_checkers = detect_colour_checkers_segmentation(image=image, additional_data=True, show=False,
                                                    setting=SETTINGS_SEGMENTATION_COLORCHECKER_CLASSIC)

        if len(colour_checkers) == 0:
            raise PipelineError(message='No ColorChecker detected', step='Checker Detector')       

        quad_orig = self._get_colourchecker_quad_on_original(colour_checkers[0], image,
                                                            SETTINGS_SEGMENTATION_COLORCHECKER_CLASSIC['working_width'])

        return image, colour_checkers[0].swatch_colours, quad_orig

    
    def _get_colourchecker_quad_on_original(self, colour_checker: np.ndarray, image: np.ndarray, working_width) -> np.ndarray:
        quad_work = np.asarray(colour_checker.quadrilateral, dtype=np.float32)  # (4,2)
        H0, W0 = image.shape[:2]

        rotated = W0 < H0

        if not rotated:
            scale = W0 / float(working_width)
            quad_orig = quad_work * scale
            quad_orig = np.rint(quad_orig).astype(np.int32)
            return quad_orig

        scale = H0 / float(working_width)

        quad_rot = quad_work * scale

        quad_orig = np.zeros_like(quad_rot)
        quad_orig[:, 0] = quad_rot[:, 1]
        quad_orig[:, 1] = (H0 - 1) - quad_rot[:, 0]
        quad_orig = np.rint(quad_orig).astype(np.int32)

        return quad_orig # (4,2)

