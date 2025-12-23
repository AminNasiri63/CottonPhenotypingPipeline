import logging
from presentation.cli import parse_args, visualizer
from config.settings import ProjectConfig, setup_logging, SamLeafSegConfig
from infrastructure.image_io import OpenCVImageLoader
from infrastructure.file_discovery import FolderDatasetDiscovery
from infrastructure.color_checker_detector_deep import DeepColorCheckerDetector
from infrastructure.leaf_segmentation import LeafSegmentor
from infrastructure.color_calibration import SimpleColorCalibrator
from infrastructure.patch_selection import CorrelationBasedPatchSelector
from infrastructure.greenness_index import ExcessGreenIndexCalculator
from infrastructure.csv_writer import CsvResultWriter
from application.services import ImageProcessingPipeline, DatasetProcessingService


def main():
    try:
        config: ProjectConfig = parse_args()
        setup_logging(config.output_csv)

        # Infrastructure instances
        loader = OpenCVImageLoader()
        discovery = FolderDatasetDiscovery()
        checker_detector = DeepColorCheckerDetector()
        segmentor = LeafSegmentor(method=config.segment_method,
                                  sam_config=config.sam_config
                                  if config.segment_method == 'sam' else None)
        calibrator = SimpleColorCalibrator()
        patch_selector = CorrelationBasedPatchSelector(stride_fraction=0.5)
        greenness_calc = ExcessGreenIndexCalculator(method=config.green_indx)
        writer = CsvResultWriter(output_path=config.output_csv)

        # Pipeline & service
        pipeline = ImageProcessingPipeline(
            loader=loader,
            checker_detector=checker_detector,
            leaf_segmentor=segmentor,
            calibrator=calibrator,
            patch_selector=patch_selector,
            greenness_calc=greenness_calc,
            config=config,
            show_func=visualizer
        )

        service = DatasetProcessingService(
            discovery=discovery,
            pipeline=pipeline,
            writer=writer,
        )

        service.run(config.input_root)

    finally:
        logging.shutdown()

if __name__ == "__main__":
    main()
