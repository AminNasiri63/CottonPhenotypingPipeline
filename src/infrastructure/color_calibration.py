import numpy as np
import cv2
import colour
from domain.ports import ColorCalibratorPort


class SimpleColorCalibrator(ColorCalibratorPort):

    def __init__(self):
        self.D65 = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D65"]
        self.REFERENCE_COLOUR_CHECKER = colour.CCS_COLOURCHECKERS["ColorChecker24 - After November 2014"]
        self.colour_checker_rows = self.REFERENCE_COLOUR_CHECKER.rows
        self.colour_checker_columns = self.REFERENCE_COLOUR_CHECKER.columns
        self.REFERENCE_SWATCHES = colour.XYZ_to_RGB(colour.xyY_to_XYZ(list(self.REFERENCE_COLOUR_CHECKER.data.values())),
                                               "sRGB",self.REFERENCE_COLOUR_CHECKER.illuminant)  

    
    def calibrate(self, image: np.ndarray, swatches: np.ndarray) -> np.ndarray:

        corrected_image = colour.colour_correction(image, swatches, self.REFERENCE_SWATCHES)
        corrected_image = colour.cctf_encoding(corrected_image)
        corrected_image = (corrected_image * 255).clip(0, 255).astype("uint8")
        corrected_image = cv2.cvtColor(corrected_image, cv2.COLOR_RGB2BGR) 
        
        return corrected_image
