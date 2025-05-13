
# Obukhov Length Calculation and Atmospheric Stability Classification

This repository contains scripts to calculate **Obukhov inverse length (Linv)** and classify atmospheric stability conditions (stable, unstable, neutral) using ERA5 data. Results are saved in NetCDF and CSV formats for further analysis.

---

## Contents
0. [Description](#-description)
1. [Directory Structure](#-directory-structure)
2. [Requirements](#-requirements)
3. [Installation](#installation)
4. [Usage](#-usage)
5. [Methodology](#methodology)
6. [Stability Classification](#-stability-classification)
7. [Key Parameters](#-key-parameters)
8. [Study Location](#-study-location)
9. [Limitations](#-limitations)
10. [References](#-references)

## Description
Obukhov Length Calculation (ERA5-Specific) based on [ERA5: How to calculate Obukhov Length](https://confluence.ecmwf.int/display/CKB/ERA5%3A+How+to+calculate+Obukhov+Length):  

### **Formula for Obukhov Length (L)**  
The Obukhov length is calculated as:  
```  
Linv = vk * g * tvst / (tv2 * ust**2)  #ECMWF ERA5 calc.
``` 
Where: 

- `vk` = 0.4 (Von Kármán).
- `g` = 9.81 m/s² (gravedad).
- `tvst` = -wtv / ust (escala de temperatura turbulenta).
- `tv2` = temperatura virtual a 2 m.
- `ust` = velocidad de fricción (u*).
```  
L = - (T₀ * u*³) / (k * g * H)  #IFS Doc. Cy49r1
```  
Where:  
- `T₀` = Surface temperature `[K]`  
- `u*` = Friction velocity `[m/s]`  (ustar)
- `k` = Von Kármán constant (0.4)  
- `g` = Gravitational acceleration (9.81) `[m/s²]`  
- `H` = Sensible heat flux `[W/m²]`

In this repository, we calculate the **inverse Obukhov length (`Linv = 1/L`)** to avoid division by near-zero values.  

## Directory Structure
```
.
├── data                  # Input ERA5 NetCDF files
├── out_csv              # Output CSV files with classified events (single point)
├── out_fig              # Output figures (e.g., timeseries, histograms)
├── out_nc               # Output NetCDF files with L_inv and u* (same shape as input)
├── PDFs
│   └── IFS_part4_Cy49r1_comentado.pdf  # Annotated reference document from ECMWF
├── src                  # Source code scripts
│   ├── p00_download_ERA5.py      # Optional download script
│   ├── p00_general.sh            # Shell script for automation
│   ├── p01_obukhov_calculate.py  # Calculates L_inv and u*
│   ├── p02_save_events.py        # Classifies stability conditions
│   └── p03_plot_point.py         # Generates plots
└── tex                  # LaTeX files for documentation
```

---

## Requirements
- Python 3.8+
- Required libraries:
  ```bash
  numpy pandas xarray matplotlib netCDF4
  ```

---

## Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### 1. Calculate Obukhov Length
```bash
python src/p01_obukhov_calculate.py data/era5_1990_01.nc
```
**Output**: `out_nc/Lu_1990_01_.nc` (NetCDF with `Linv` and `u*`).

### 2. Classify Stability Conditions
```bash
python src/p02_save_events.py out_nc/Lu_1990_01_.nc
```
**Outputs**: 
- `out_csv/stable_199001.csv`
- `out_csv/unstable_199001.csv`  
- `out_csv/neutral_199001.csv`

### 3. Generate Plots
```bash
python src/p03_plot_point.py
```
**Output**: Figures in `out_fig/`.

---

## Methodology

### Core Scripts
1. **`p01_obukhov_calculate.py`**  
   - Calculates inverse Obukhov length (`Linv`) and friction velocity (`u*`) from ERA5 data.
   - Uses variables: `t2m`, `d2m`, `sp`, `ishf`, `ie`, `iews`, `inss`.

2. **`p02_save_events.py`**  
   - Classifies stability using thresholds:
     - Unstable: `Linv < -0.01 m⁻¹`
     - Stable: `Linv > 0.01 m⁻¹`
     - Neutral: `-0.01 ≤ Linv ≤ 0.01 m⁻¹`

3. **`p03_plot_point.py`**  
   - Generates time-series and climatology plots.

### Key Formulas
1. **Friction velocity**:
   ```python
   ustar = sqrt(iews² + inss²) / sqrt(air_density)
   ```
2. **Inverse Obukhov length**:
   ```python
   Linv = (0.4 * 9.81 * virtual_heat_flux) / (tv2 * ustar³)
   ```

---

## Stability Classification
| Condition | Threshold (`Linv`) | Physical Interpretation |
|-----------|--------------------|-------------------------|
| Unstable  | < -0.01 m⁻¹        | Daytime convection      |
| Stable    | > 0.01 m⁻¹         | Nighttime stability     |
| Neutral   | -0.01 to 0.01 m⁻¹  | Wind-dominated          |

---

## Key Parameters
### Input Variables
| Variable | Description | Unit |
|----------|-------------|------|
| `t2m`    | 2m temperature | K |
| `d2m`    | 2m dewpoint | K |
| `sp`     | Surface pressure | Pa |
| `ishf`   | Sensible heat flux | W/m² |
| `ie`     | Evaporation flux | m/s |
| `iews`   | Eastward turbulent stress | N/m² |
| `inss`   | Northward turbulent stress | N/m² |

---

## Study Location
```python
LAT_PONTO = -21.6389  # Coastal Brazil
LON_PONTO = -40.8693
```

---

## Limitations
- Less reliable in mountainous areas (`sdfor > 50 m`).
- Assumes Monin-Obukhov similarity theory holds.

---

## References
1. [ECMWF IFS Documentation CY49R1 - Part IV](https://www.ecmwf.int/sites/default/files/elibrary/112024/81626-ifs-documentation-cy49r1-part-iv-physical-processes.pdf)  
2. [ERA5: Obukhov Length Calculation Guide](https://confluence.ecmwf.int/display/CKB/ERA5%3A+How+to+calculate+Obukhov+Length)  
3. [ECMWF Parameter Database](https://apps.ecmwf.int/codes/grib/param-db)
