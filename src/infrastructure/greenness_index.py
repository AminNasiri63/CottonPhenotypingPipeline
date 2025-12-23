from typing import Literal
import numpy as np
import cv2
from domain.ports import GreennessIndexCalculatorPort
from domain.exceptions import PipelineError


class ExcessGreenIndexCalculator(GreennessIndexCalculatorPort):

    def __init__(self, method: Literal["bgr"] = "bgr"):
        self.method = method

    def compute(self, patch: np.ndarray, mask: np.ndarray) -> float:
        """
        # patch assumed in BGR (OpenCV)
        # b = patch[:, :, 0].astype(np.float32)
        # g = patch[:, :, 1].astype(np.float32)
        # r = patch[:, :, 2].astype(np.float32)
        """
        
        green_pixels = self._extract_green_pixels(patch, mask)

        if self.method == "bgr":
            green_inx = self._bgr_method(green_pixels)
        elif self.method == "ngrdi":
            green_inx = self._ngrdi_method(green_pixels)        
        else:
            raise PipelineError(message=f"Unknown method: {self.method}", step='Green Index Calculator')        


        return green_inx
    
    def _extract_green_pixels(self, patch: np.ndarray, mask: np.ndarray) -> np.ndarray:
        h_p, w_p = patch.shape[:2]
        h_m, w_m = mask.shape[:2]

        if h_p != h_m or w_p != w_m:
            raise PipelineError(message=f'SHAPE_MISMATCH] Patch shape {h_p, w_p} != mask shape {h_m, w_m}', step='Green Index Calculator')
        
        green_pixels = cv2.bitwise_and(patch, patch, mask=mask)
        green_pixels = green_pixels.astype(np.float32)

        return green_pixels
    
    def _bgr_method(self, green_pixels: np.ndarray) -> float:
        b, g, r = cv2.split(green_pixels)
        exg = 2 * g - r - b

        mask = ((g + r) > 20) & (np.abs(g - r) > 2)  # remove dark pixels

        return float(np.median(exg[mask]))
    
    def _ngrdi_method(self, green_pixels: np.ndarray) -> float:
        b, g, r = cv2.split(green_pixels)
        ngrdi = (g - r) / (g + r + 1e-6)

        mask = ((g + r) > 20) & (np.abs(g - r) > 2)  # remove dark pixels

        return float(np.median(ngrdi[mask]))