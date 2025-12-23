# Cotton Phenotyping Pipeline

A Python-based pipeline for **cotton plant phenotyping from RGB field images**, designed to measure **leaf greenness indices** as indicators of plant health, nitrogen status, and growth vigor.

The system integrates **color-checker-based color calibration**, **leaf segmentation**, and **patch-level analysis** in a modular and research-oriented architecture.

---

## Features

- Automatic **color checker detection** for illumination-robust color calibration  
- **Leaf segmentation** using vegetation indices (NExG, ExG, HSV-based methods)  
- **Patch-based greenness analysis** for localized phenotyping  
- Supports multiple **greenness indices** (e.g., ExG, NGRDI)  
- Batch processing of large field datasets  
- Optional **visual diagnostics** for quality control  
- Structured **CSV export** for statistical analysis  

---

## Pipeline Overview

For each image, the pipeline performs the following steps:

1. Load RGB image  
2. Detect color checker and calibrate image colors  
3. Segment leaf regions  
4. Select analysis patches  
5. Compute greenness index on leaf pixels  
6. Aggregate and export results  
7. (Optional) Save visualization figures  

---

## Project Structure

```text
.
├── domain/           # Core entities and abstract interfaces
├── application/      # Pipeline orchestration and use cases
├── infrastructure/   # OpenCV, DL models, file I/O, adapters
├── presentation/     # CLI and visualization
├── config/           # Settings and logging
├── main.py           # Entry point (dependency injection)
