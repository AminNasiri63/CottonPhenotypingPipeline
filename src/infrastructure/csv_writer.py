import csv
from pathlib import Path
from typing import List
from domain.ports import ResultWriterPort
from domain.entities import GreennessMeasurement


class CsvResultWriter(ResultWriterPort):
    def __init__(self, output_path: Path):
        self.output_path = output_path

    def write_all(self, measurements: list[GreennessMeasurement]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "folder_name",
                "image_path",
                "lat",
                "long",
                "patch_id",
                "x",
                "y",
                "w",
                "h",
                "greenness_value",
            ])
            for m in measurements:
                writer.writerow([
                    m.folder_name,
                    str(m.image_path),
                    m.lat,
                    m.long,
                    m.patch_id,
                    m.patch_region.x,
                    m.patch_region.y,
                    m.patch_region.w,
                    m.patch_region.h,
                    m.greenness_value,
                ])
