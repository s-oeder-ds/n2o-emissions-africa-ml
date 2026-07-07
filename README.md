# N₂O Emissions in Africa — Machine Learning Portfolio Project

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)
![uv](https://img.shields.io/badge/Environment-uv-purple)
![Jupyter](https://img.shields.io/badge/Workflow-Jupyter-orange)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

## Overview

This repository contains a machine learning project for modeling nitrous oxide (`N₂O`) emissions across Sub-Saharan African ecosystems.

The project uses open scientific data from PANGAEA and follows a complete applied data science workflow: data acquisition, raw-data validation, preprocessing, exploratory data analysis, feature documentation, and model preparation. The final modeling target is the prediction of soil-surface N₂O flux from spatial, temporal, meteorological, soil-related, and management-related features.

The project is intentionally structured as a portfolio project. The focus is not only on producing a model score, but also on building a workflow that is readable, reproducible, and suitable for presentation.

---

## Research Context

Nitrous oxide is a highly relevant greenhouse gas in agricultural and ecological systems. Its emissions are influenced by nitrogen availability, soil moisture, soil temperature, precipitation events, land use, and management practices.

The dataset behind this project combines observations from multiple African land-use systems, including croplands, forests, plantations, and grasslands. This makes the project a realistic tabular machine learning task with spatial structure, heterogeneous feature groups, missing values, and potentially non-linear process relationships.

---

## Project Goals

The main goals are:

1. build a reproducible workflow for downloading and preparing the PANGAEA data,
2. inspect and document the dataset structure,
3. analyze N₂O emission patterns across land-use systems and geography,
4. prepare machine-learning-ready features,
5. train an XGBoost regression model,
6. evaluate prediction quality with regression metrics and residual diagnostics,
7. interpret important model drivers in a scientifically plausible way.

---

## Data Source

The data comes from the PANGAEA bundled publication:

**Agredazywczuk, P. et al. (2026): Nitrous oxide emissions across Sub-Saharan Africa: meta-analysis and data-driven modelling. PANGAEA. DOI: 10.1594/PANGAEA.987298**

The bundled publication contains four datasets:

- Nitrous oxide emissions from African Croplands
- Nitrous oxide emissions from African Forests and Plantations
- Nitrous oxide emissions from African Grasslands
- Site information of nitrous oxide emissions across Croplands, Forests and Grasslands

The original data is licensed under **Creative Commons Attribution 4.0 International (CC-BY-4.0)**.

Raw data files are not intended to be stored directly in this repository. They should be downloaded through the project scripts and stored locally under `data/raw/`.

Further details are documented in [`data_sources.md`](data_sources.md).

---

## Repository Structure

```text
n2o-emissions-africa-ml/
│
├── data/
│   ├── external/              # External reference data, ignored by Git except placeholders
│   ├── interim/               # Intermediate processed files, ignored by Git except placeholders
│   ├── processed/             # Final modeling-ready data, ignored by Git except placeholders
│   ├── raw/                   # Original downloaded data, ignored by Git except placeholders
│   └── features.md            # Feature and column documentation
│
├── notebooks/
│   ├── build_landuse_interim_dataset.ipynb
│   ├── first_look.ipynb
│   └── n2o_eda.ipynb
│
├── src/
│   ├── alignment.py
│   ├── convert_pangaea_textfile.py
│   ├── download_pangaea_data.py
│   └── preprocess_interim_data.py
│
├── .gitignore
├── .python-version
├── LICENSE
├── PROJECT_REPORT.md
├── README.md
├── data_sources.md
├── main.py
├── pyproject.toml
└── uv.lock
```

---

## Current Workflow

The current workflow is organized around four practical stages.

### 1. Data Download

The script `src/download_pangaea_data.py` downloads the PANGAEA bundled dataset, validates the downloaded ZIP archive, and extracts readable files into the local raw-data directory.

### 2. Data Conversion and Alignment

The script `src/convert_pangaea_textfile.py` is used to convert PANGAEA text-based source files into a more convenient tabular format.

The script `src/alignment.py` standardizes cropland-specific soil moisture and soil temperature columns so that they match the shorter naming pattern used in the forest and grassland datasets.

### 3. Preprocessing

The script `src/preprocess_interim_data.py` contains reusable preprocessing functionality, including controlled column renaming and optional export of processed data.

### 4. Exploratory Data Analysis

The notebook `notebooks/n2o_eda.ipynb` is used for exploratory analysis, including distribution checks, missing-value inspection, land-use comparisons, and spatial visualizations.

---

## Feature Groups

The project works with several feature groups:

| Feature group | Examples | Relevance |
|---|---|---|
| Spatial features | latitude, longitude | geographic patterns, climate proxies, site context |
| Time features | date, year, month, day of year | seasonality, long-term structure |
| Land use | cropland, forest, plantation, grassland | ecosystem and management context |
| Fertilisation | nitrogen amount, time since application, decay-adjusted nitrogen | management-driven emission dynamics |
| Weather | air temperature, precipitation, cloud cover, VPD, pressure | meteorological drivers |
| Soil conditions | soil moisture, soil temperature | process-near controls for N₂O formation |
| Radiation | shortwave radiation, PPFD | energy balance and vegetation activity |
| Target | N₂O flux | regression target |

The feature documentation is maintained in `data/features.md`.

---

## Modeling Approach

The main planned model is an **XGBoost Regressor**.

XGBoost is suitable for this dataset because it can model non-linear effects and feature interactions in structured tabular data. This is useful for environmental data, where variables such as soil moisture, temperature, land use, and nitrogen input often interact rather than acting independently.

The model-building workflow includes:

- train-test split,
- preprocessing of numerical and categorical variables,
- baseline model comparison,
- XGBoost training,
- prediction and residual analysis,
- evaluation with regression metrics,
- feature importance analysis,
- interpretation of model behavior.

---

## Evaluation Metrics

The model will be evaluated with multiple regression diagnostics:

| Metric | Interpretation |
|---|---|
| MAE | Average absolute prediction error |
| RMSE | Stronger penalty for large errors |
| R² Score | Share of variance explained by the model |
| Residual plots | Visual inspection of systematic model errors |

Because N₂O emissions can be skewed and noisy, results should be interpreted using both metrics and diagnostic plots.

---

## Environment

This project uses `uv` for dependency management.

The required Python version is defined in `pyproject.toml` as:

```text
>=3.11,<3.13
```

Main dependencies include:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- xgboost
- geopandas
- shapely
- contextily
- requests
- ipykernel

---

## Installation

Clone the repository:

```bash
git clone https://github.com/s-oeder-ds/n2o-emissions-africa-ml.git
cd n2o-emissions-africa-ml
```

Switch to the EDA branch:

```bash
git checkout eda
```

Create and synchronize the environment:

```bash
uv sync
```

Start Jupyter:

```bash
uv run jupyter lab
```

---

## Example Usage

Download and extract the PANGAEA data:

```bash
uv run python src/download_pangaea_data.py
```

Open the notebooks:

```bash
uv run jupyter lab notebooks/
```

Recommended notebook order:

1. `notebooks/first_look.ipynb`
2. `notebooks/build_landuse_interim_dataset.ipynb`
3. `notebooks/n2o_eda.ipynb`

---

## Current Status

The project is currently under active development.

Completed or started:

- repository structure,
- `uv` project setup,
- data folders with Git placeholders,
- PANGAEA download script,
- ZIP validation and extraction workflow,
- initial preprocessing utilities,
- feature documentation,
- first notebooks for data inspection and EDA.

Next steps:

- finalize the cleaned modeling dataframe,
- improve feature naming consistency,
- build the XGBoost modeling notebook,
- add baseline models,
- evaluate model performance,
- interpret feature importance,
- export portfolio-ready figures,
- prepare presentation results.

---

## Limitations

Several limitations should be considered:

- Observations are not expected to be spatially balanced across Africa.
- Some land-use classes may contain more observations than others.
- N₂O flux values can be skewed and event-driven.
- Environmental variables may interact non-linearly.
- Some source columns require careful interpretation because similar PANGAEA column names can be shortened or duplicated during import.
- The final model should be interpreted as a data-driven approximation, not as a process-based biogeochemical model.

---

## License

The source code and repository documentation are released under the MIT License.

The original scientific data remains subject to the license and citation requirements of the original PANGAEA datasets. See [`data_sources.md`](data_sources.md) for details.
