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
# Notes:
- Each top-level folder (e.g., sample_001) represents a field plot, location, or experimental unit.
- Image files are stored inside the images/ subfolder.
- GPS metadata is stored separately in a corresponding gps/ subfolder.
- The pipeline matches images to GPS information based on their parent folder.
- Folder depth can be extended (e.g., by date or treatment), as long as the relative images/ ↔ gps/ relationship is preserved.


---




