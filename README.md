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

The GPS file is a **CSV file** (space- or tab-separated). Each row corresponds to a single GPS record and follows this format:

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
Run the pipeline from the command line as follows:
```bash
python main.py \
  --input-root /path/to/dataset_root \
  --output-csv results.csv \
  --output-fig figures/ \
  --num-patches 1 \
  --segment-method nexg \
  --green-indx ngrdi
```

### Command-Line Arguments

| Argument | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--input-root` | `str` | ✅ Yes | — | Root directory of the dataset containing nested image and GPS folders |
| `--output-csv` | `str` | ✅ Yes | — | Path to the output CSV file for greenness measurements |
| `--output-fig` | `str` | ❌ No | `None` | Directory to save visualization figures (if not provided, figures are not saved) |
| `--num-patches` | `int` | ❌ No | `1` | Number of analysis units per image (currently image-level; kept for future extensibility) |
| `--segment-method` | `str` | ❌ No | `"nexg"` | Leaf segmentation method (`nexg`, `exg`, `hsv`, `sam`) |
| `--green-indx` | `str` | ❌ No | `"ngrdi"` | Greenness index used for phenotyping (`ngrdi`, `exg`) |

---

## Output

The pipeline generates two primary outputs:

1. A **CSV file** containing image-level greenness measurements  
2. A **log file** (`run.log`) capturing execution details, warnings, and errors  

---

### CSV Output

The CSV file contains one row per processed image (currently one patch per image).

#### Columns

| Column | Description |
|------|-------------|
| `folder_name` | Identifier of the plot or parent folder |
| `image_path` | Absolute path to the processed image |
| `lat` | Latitude in decimal degrees |
| `long` | Longitude in decimal degrees |
| `patch_id` | Patch identifier (currently always `0`, image-level analysis) |
| `x` | Top-left x-coordinate of the analysis region (pixels) |
| `y` | Top-left y-coordinate of the analysis region (pixels) |
| `w` | Width of the analysis region (pixels) |
| `h` | Height of the analysis region (pixels) |
| `greenness_value` | Computed greenness index value |

Since the current implementation performs **image-level analysis**, the analysis region (`x`, `y`, `w`, `h`) corresponds to the full image extent.

---

## Sample Data and Example Results

To facilitate quick testing and reproducibility, the repository includes a small set of **sample images** and corresponding **example outputs**.

### Sample Data (`samples/`)

The `samples/` directory contains a minimal dataset illustrating the expected input structure:

```
samples/
├── ImageData/
│   ├── 10_42_29_495958.png
│   ├── 10_43_43_985830.png
│   └── 10_42_15_744794.png
└── GPSData/
    └── gps.csv
```

### Example Outputs (`results/`)
```
results/
├── sample_results.csv
├── run.log
└── figures/
    ├── 10_42_29_495958.png
    └── 10_43_43_985830.png
    └── 10_42_15_744794.png
```

# License
MIT License.

---

# Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

