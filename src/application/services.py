from domain.entities import ImageSample, GreennessMeasurement, PatchRegion
from domain.exceptions import PipelineError, PipelineErrorType
from domain.ports import (
    ImageLoaderPort,    
    ColorCheckerDetectorPort,
    LeafSegmentationPort,
    ColorCalibratorPort,
    PatchSelectorPort,
    GreennessIndexCalculatorPort,
    DatasetDiscoveryPort,
    ResultWriterPort,
)
from config.settings import ProjectConfig
import logging
from presentation.cli import clear_screen

logger = logging.getLogger(__name__)

class ImageProcessingPipeline:

    def __init__(
        self,
        loader: ImageLoaderPort,
        checker_detector: ColorCheckerDetectorPort,
        leaf_segmentor: LeafSegmentationPort,
        calibrator: ColorCalibratorPort,
        patch_selector: PatchSelectorPort,
        greenness_calc: GreennessIndexCalculatorPort,
        config: ProjectConfig,
        show_func,
        show: bool = False,
        save_fig: bool = False,
        save_interval: int = 100
    ):
        self.loader = loader
        self.checker_detector = checker_detector
        self.leaf_segmentor = leaf_segmentor
        self.calibrator = calibrator
        self.patch_selector = patch_selector
        self.greenness_calc = greenness_calc
        self.config = config
        self.show_func = show_func
        self.show = show
        self.save_fig = save_fig
        self.save_interval = save_interval

    def process_image(self, sample: ImageSample, num: int) -> list[GreennessMeasurement]:
        img = self.loader.load(sample.path)

        norm_image, swatch_colours, checker_bbox = self.checker_detector.detect(sample.path)
        leaves_mask, leaves_rgb = self.leaf_segmentor.extract(img, checker_bbox)
        calibrated = self.calibrator.calibrate(norm_image, swatch_colours)

        patches: list[PatchRegion] = self.patch_selector.select_patches(calibrated, checker_bbox,
                                                                        self.config.num_patches_per_image)

        measurements: list[GreennessMeasurement] = []
        for patch in patches:
            patch_img = calibrated[patch.y:patch.y + patch.h, patch.x:patch.x + patch.w]
            patch_mask = leaves_mask[patch.y:patch.y + patch.h, patch.x:patch.x + patch.w]
            green_inx = self.greenness_calc.compute(patch_img, patch_mask)

            measurements.append(
                GreennessMeasurement(image_path=sample.path, folder_name=sample.folder_name, lat=sample.lat,
                                     long=sample.long, patch_id=patch.patch_id, patch_region=patch,
                                     greenness_value=green_inx))
        
        path_save_fig = (self.config.output_figure / sample.root_path / sample.path.name
                         if self.save_fig and (num % self.save_interval == 0)
                         else None)
        self.show_func(path_save_fig, self.show, orig_img=img, leaves_RGB=leaves_rgb)

        return measurements


class DatasetProcessingService:

    def __init__(
        self,
        discovery: DatasetDiscoveryPort,
        pipeline: ImageProcessingPipeline,
        writer: ResultWriterPort,
        info_interval: int = 25
    ):
        self.discovery = discovery
        self.pipeline = pipeline
        self.writer = writer
        self.info_interval = info_interval

    def run(self, root) -> None:        
        samples = self.discovery.discover_images(root)

        clear_screen()
        logger.info(f"{len(samples)} samples read; starting analysis.")

        all_measurements: list[GreennessMeasurement] = []
        for num, sample in enumerate(samples[:10]):

            try:
                ms = self.pipeline.process_image(sample, num)
                all_measurements.extend(ms)

                if num % self.info_interval == 0:
                    clear_screen()
                    logger.info(f"{num} of {len(samples)} samples analyzed.")

            except PipelineError as e:
                logger.warning(f"[WARN] at {e.step} step for {sample.path}: {e.message}.")

                if e.error_type == PipelineErrorType.FATAL:
                    logger.error(f"[ERROR] at step {e.step}: {e.message}. Fatal pipeline error encountered. Stopping processing")
                    break

                continue

            except Exception as e:
                logger.exception(f"Unexpected error for {sample.path}: {e}.")
                continue

        if all_measurements:
            clear_screen()
            logger.info("Exporting data/results to a CSV file.")
            self.writer.write_all(all_measurements)
            logger.info("Data export to CSV completed successfully.")
