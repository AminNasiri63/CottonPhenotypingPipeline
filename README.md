# Cotton Phenotyping Pipeline

A Python-based pipeline for **cotton plant phenotyping from RGB field images**, designed to measure **leaf greenness indices** as indicators of plant health, nitrogen status, and growth vigor.

The system integrates **color-checker-based color calibration** and **leaf segmentation** in a modular and research-oriented architecture.

---

## Features

- Automatic **color checker detection** for illumination-robust color calibration  
- **Leaf segmentation** using vegetation indices and deep model (NExG, ExG, HSV, SAM-based methods)  
- **Image-level greenness analysis** using segmented leaf pixels
- Supports multiple **greenness indices** (e.g., ExG, NGRDI)   
- Structured **CSV export** for statistical analysis  

---

## Pipeline Overview

For each image, the pipeline performs the following steps:

1. Load RGB image  
2. Detect the color checker and calibrate image colors  
3. Segment leaf regions  
4. Treat the entire image as a single analysis unit  
5. Compute greenness index on leaf pixels  
6. Aggregate and export results  
7. (Optional) Save visualization figures  

---

## Project Structure

```
.
├── domain/           # Core entities and abstract interfaces
├── application/      # Pipeline orchestration and use cases
├── infrastructure/   # OpenCV, DL models, file I/O, adapters
├── presentation/     # CLI and visualization
├── config/           # Settings and logging
├── main.py           # Entry point (dependency injection)

```

---

## Dataset Structure

```
dataset_root/
├── ImageData/
    ├── sample_001/
    │   ├── sample_001_1/
    │   │   ├── img1.jpg
    │   │   ├── ...
    │   └── sample_001_2/
    │   │   ├── img1.jpg
    │   │   ├── ...
    │
    ├── sample_002/
    │   │   ├── img1.jpg
    │   │   ├── ...

├── GPSData/
    ├── sample_001/
    │   ├── sample_001_1/
    │   │   ├── gps.csv
    |
    │   └── sample_001_2/
    │   │   ├── gps.csv
    │
    ├── sample_002/
    │   │   ├── gps.csv


```
### Notes:
- Each top-level folder (e.g., sample_001) represents a field plot, location, or experimental unit.
- Image files are stored inside the ImageData/subfolder.
- GPS metadata is stored separately in a corresponding GPSData/subfolder.
- The pipeline matches images to GPS information based on their parent folder.
- Folder depth can be extended (e.g., by date or treatment), as long as the relative images/ ↔ gps/ relationship is preserved.

---


## GPS File Format and Image Association

Each GPS file provides geographic coordinates for the images captured within the same folder.

### GPS File Format

The GPS file is a **plain text file** (space- or tab-separated). Each row corresponds to a single GPS record and follows this format:

    longitude   latitude    time
    -88.85086167 35.631695  10:31:42

Header rows are optional. The pipeline assumes a fixed column order:

1. Longitude (decimal degrees)
2. Latitude (decimal degrees)
3. Time (`HH:MM:SS`)

### Image–GPS Association

Image filenames are **timestamp-based**, for example:

    10_42_29_495958.jpg

Only the **`HH:MM:SS`** component of the filename is used for synchronization with GPS records.

### Notes

- The GPS timestamp corresponds to the image capture time.
- Images are associated with GPS records based on **temporal alignment**.
- If an exact timestamp match is not available, the **closest GPS record in time** is used.
- Longitude and latitude are expressed in **decimal degrees**.
- Image filenames must preserve the original timestamp structure to ensure correct matching.
- This design enables reliable synchronization between image data and GPS logs collected during field acquisition.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AminNasiri63/CottonPhenotypingPipeline.git
    cd CottonPhenotypingPipeline
    ```

2. (Recommended) Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # macOS/Linux
    # .venv\Scripts\activate    # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Notes on SAM Installation

This pipeline uses **Segment Anything (SAM)** for optional leaf segmentation.

If installation fails on some systems, SAM can be installed manually using:

```bash
pip install git+https://github.com/facebookresearch/segment-anything.git
pip install torch torchvision
```

---

## Usage
```bash
python main.py \
  --input-root /path/to/dataset_root \
  --output-csv results.csv \
  --output-fig figures/ \
  --num-patches 3
```

---

---

## Output
### CSV Output (Example)
```text
image_path, plot_id, latitude, longitude, patch_id, greenness_value
plot_001/images/img_001.jpg, plot_001, 35.912345, -83.941234, 0, 0.42
```

---





