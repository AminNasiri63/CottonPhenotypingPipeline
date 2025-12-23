from pathlib import Path
import pandas as pd
import logging
from domain.ports import DatasetDiscoveryPort
from domain.entities import ImageSample

logger = logging.getLogger(__name__)


class FolderDatasetDiscovery(DatasetDiscoveryPort):
    def __init__(self, valid_exts: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".tif")):
        self.valid_exts = valid_exts
        self.GPS_data = {}
        self.last_time_index = 0

    def discover_images(self, root: Path) -> list[ImageSample]:
        samples: list[ImageSample] = []

        for p in root.rglob("*"):

            try:
                if p.suffix.lower() in self.valid_exts:
                    rel = p.relative_to(Path.cwd().parent)
                    root_path = rel.parent
                    folder_name = p.parent.name

                    if p.parent not in self.GPS_data:
                        gps_path = Path(str(p.parent).replace('ImageData', 'GPSData'))
                        self.GPS_data[p.parent] = self._read_GPS_data(gps_path)
                        self.last_time_index = 0

                    lat, long = self._read_lat_long(p)

                    samples.append(ImageSample(path=p, root_path=root_path, folder_name=folder_name, lat=lat, long=long))

            except Exception as e:
                logger.exception(f"Unexpected error for {p} in Dataset Discovery step: {e}.")
                continue


        return samples

    def _read_GPS_data(self, path: Path) -> dict:
        gps_csv = list(path.glob('*.csv'))[0]
        df = pd.read_csv(gps_csv, header=None)
        df.columns = ['Lat.', 'Long.', 'time']
        gps_data = df.to_dict(orient='list')

        return gps_data

    def _read_lat_long(self, path: Path):

        name = path.name
        time = name[:name.rfind('_')]
        time = time.replace('_', ':')

        if time not in self.GPS_data[path.parent]['time']:
            time_index = self.last_time_index
            logger.warning(f"[WARN] for {path}: {'Image time is not in GPS data. Last time is used.'}")
        else:
            time_index = self.GPS_data[path.parent]['time'].index(time)

        lat = self.GPS_data[path.parent]['Lat.'][time_index]
        long = self.GPS_data[path.parent]['Long.'][time_index]

        self.last_time_index = time_index

        return lat, long




