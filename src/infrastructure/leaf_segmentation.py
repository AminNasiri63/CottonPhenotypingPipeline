from typing import Literal
import numpy as np
import cv2
from domain.ports import LeafSegmentationPort
from domain.exceptions import PipelineError, PipelineErrorType
from config.settings import SamLeafSegConfig
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator



class LeafSegmentor(LeafSegmentationPort):

    def __init__(
        self,
        method: Literal["nexg", "exg", "hsv", "sam"] = "nexg",
        nexg_thresh: float = 0.1,
        exg_thresh: float = 0.0,
        hsv_h_range=(35, 85),
        hsv_s_min: int = 40,
        hsv_v_min: int = 40,
        mask_are_min: int = 10_000,
        sam_config: SamLeafSegConfig = None
    ):
        self.method = method
        self.nexg_thresh = nexg_thresh
        self.exg_thresh = exg_thresh
        self.hsv_h_range = hsv_h_range
        self.hsv_s_min = hsv_s_min
        self.hsv_v_min = hsv_v_min
        self.mask_are_min = mask_are_min
        self.sam_config = sam_config

        if self.sam_config is not None:
            self._load_sam()

    def extract(self, image_rgb: np.ndarray, checker_bbox: np.ndarray) -> np.ndarray:
        if self.method == "nexg":
            mask = self._nexg_mask(image_rgb)
        elif self.method == "exg":
            mask = self._exg_mask(image_rgb)
        elif self.method == "hsv":
            mask = self._hsv_mask(image_rgb)
        elif self.method == 'sam':
            if self.sam_config is None:
                raise PipelineError(message="SAM Config can not be None", step='Leaf Segmentor', error_type=PipelineErrorType.FATAL)
            mask = self._hsv_mask(image_rgb)
        else:
            raise PipelineError(message=f"Unknown method: {self.method}", step='Leaf Segmentor', error_type=PipelineErrorType.FATAL)

        mask = (mask * 255).astype(np.uint8)
        cv2.fillPoly(mask, [checker_bbox], (0, 0, 0))
        mask = self._morphology_mask(mask)
        overlay = self._overlay_img_mask(image_rgb, mask)
        
        if np.sum(mask) < self.mask_are_min:
            raise PipelineError(message='No leaf detected', step='Leaf Segmentor')

        return mask, overlay
    
    
    def _nexg_mask(self, image_rgb: np.ndarray) -> np.ndarray:
        img = image_rgb.astype(np.float32)
        R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

        sum_rgb = R + G + B + 1e-6
        r = R / sum_rgb
        g = G / sum_rgb
        b = B / sum_rgb

        nexg = 2 * g - r - b
        mask = nexg > self.nexg_thresh
        
        return mask

    def _exg_mask(self, image_rgb: np.ndarray) -> np.ndarray:
        img = image_rgb.astype(np.float32)
        R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

        exg = 2 * G - R - B
        mask = exg > self.exg_thresh

        return mask

    def _hsv_mask(self, image_rgb: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

        h_min, h_max = self.hsv_h_range
        mask = (
            (h >= h_min) & (h <= h_max) &
            (s >= self.hsv_s_min) &
            (v >= self.hsv_v_min)
        )

        return mask
    
    def _sam_masks(self, image_rgb: np.ndarray) -> np.ndarray:

        hsv_mask = self._hsv_mask(image_rgb)

        H, W = image_rgb.shape[:2]
        img_area = H * W

        masks = self.mask_gen.generate(image_rgb)
        mask = np.zeros((H, W), dtype=bool)

        for m in masks:
            seg = m["segmentation"]
            area_frac = seg.sum() / img_area
            if area_frac < self.sam_config.min_area_frac or area_frac > self.sam_config.max_area_frac:
                continue

            green_ratio = float((hsv_mask & seg).sum() / seg.sum())

            if green_ratio < self.sam_config.green_score_thresh:
                continue

            mask |= seg

        return mask 
    
    
    def _load_sam(self):
        sam = sam_model_registry[self.sam_config.model_type](checkpoint=self.sam_config.checkpoint_path)
        sam.to(device=self.sam_config.device)

        self.mask_gen = SamAutomaticMaskGenerator(
            model=sam,
            points_per_side=self.sam_config.points_per_side,
            pred_iou_thresh=self.sam_config.pred_iou_thresh,
            stability_score_thresh=self.sam_config.stability_score_thresh,
            crop_n_layers=self.sam_config.crop_n_layers,
            min_mask_region_area=self.sam_config.min_mask_region_area,
        )        
    
    
    @staticmethod
    def _morphology_mask(mask: np.ndarray) -> np.ndarray:

        kernel = np.ones((3, 3), np.uint8)
        mask_morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask_morph = cv2.morphologyEx(mask_morph, cv2.MORPH_CLOSE, kernel, iterations=2)

        mask_morph = cv2.erode(mask_morph, kernel, iterations = 1)
        mask_morph = cv2.dilate(mask_morph, kernel, iterations = 2)

        return mask_morph
    
    @staticmethod
    def _overlay_img_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:

        overlay = cv2.bitwise_and(image, image, mask=mask)

        return overlay