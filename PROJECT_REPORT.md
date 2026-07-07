# Project Report

## N₂O Emissions in Africa — Machine Learning Portfolio Project

---

## 1. Problem Statement

Nitrous oxide (`N₂O`) emissions are driven by complex interactions between land use, nitrogen input, precipitation, soil moisture, soil temperature, and other environmental conditions. These interactions are often non-linear and difficult to describe with simple linear assumptions.

The goal of this project is to build a data science workflow for predicting N₂O flux values across Sub-Saharan African ecosystems using open scientific data from PANGAEA.

The project is designed as a portfolio project, but it follows a realistic applied machine learning structure: source-data handling, preprocessing, feature documentation, exploratory analysis, model building, and interpretation.

---

## 2. Data Source

The project uses the PANGAEA bundled publication:

**Agredazywczuk, P. et al. (2026): Nitrous oxide emissions across Sub-Saharan Africa: meta-analysis and data-driven modelling. PANGAEA. DOI: 10.1594/PANGAEA.987298**

The bundled publication contains data for croplands, forests and plantations, grasslands, and site-level information.

The original dataset is licensed under **CC-BY-4.0**. The repository code is separately licensed under MIT.

Detailed citation information is maintained in:

```text
data_sources.md
```

---

## 3. Repository Status

The repository currently contains:

```text
data/
├── external/
├── interim/
├── processed/
├── raw/
└── features.md

notebooks/
├── build_landuse_interim_dataset.ipynb
├── first_look.ipynb
└── n2o_eda.ipynb

src/
├── alignment.py
├── convert_pangaea_textfile.py
├── download_pangaea_data.py
└── preprocess_interim_data.py
```

The project environment is managed with `uv`, using `pyproject.toml` and `uv.lock`.

---

## 4. Data Acquisition

The data acquisition step is handled by `src/download_pangaea_data.py`.

The script currently performs three important tasks:

1. download the PANGAEA ZIP bundle,
2. validate whether the downloaded file is a readable ZIP archive,
3. extract the archive into the local raw-data folder.

This is useful because raw scientific data downloads can fail silently or produce incomplete files. ZIP validation reduces the risk of continuing the workflow with corrupted data.

---

## 5. Data Preparation

The preprocessing stage is split across reusable Python scripts and notebooks.

Important preparation tasks include:

- converting PANGAEA text files into tabular data,
- aligning column names across land-use-specific datasets,
- documenting feature semantics,
- combining cropland, forest, plantation, and grassland observations,
- preparing an interim dataset,
- preparing a final model-ready dataset.

The script `alignment.py` is especially relevant because some cropland columns use more explicit depth labels, while other land-use datasets use shorter ERA5-based column names. Aligning these names is necessary before combining the data.

---

## 6. Feature Documentation

The file `data/features.md` documents the expected columns and their interpretation.

The documented feature groups include:

- identification variables,
- spatial coordinates,
- date and derived time features,
- land use,
- fertilizer and management features,
- ERA5 weather variables,
- soil moisture,
- soil temperature,
- radiation variables,
- modeled time transformations,
- target variable.

This documentation is important because many columns are domain-specific and not self-explanatory.

---

## 7. Exploratory Data Analysis

The EDA is developed mainly in:

```text
notebooks/n2o_eda.ipynb
```

The planned and partially implemented EDA focuses on:

- dataset dimensions,
- column consistency,
- missing values,
- target distribution,
- land-use distribution,
- spatial distribution of observations,
- feature-target relationships,
- potential outliers,
- skewness and transformation needs.

Spatial analysis is a key part of the project because the observations are geographically structured and likely unevenly distributed across countries, land-use types, and measurement sites.

---

## 8. Modeling Plan

The main planned model is an **XGBoost Regressor**.

The model-building workflow should include:

1. define the target variable,
2. select feature columns,
3. split data into training and test sets,
4. preprocess categorical and numerical variables,
5. train a simple baseline model,
6. train an XGBoost model,
7. evaluate predictions,
8. inspect residuals,
9. analyze feature importance,
10. document limitations and findings.

The model should not only be evaluated by one metric. Environmental emission data is often noisy and skewed, so numerical metrics and visual diagnostics should be interpreted together.

---

## 9. Evaluation Plan

Planned regression metrics:

| Metric | Reason |
|---|---|
| MAE | Easy-to-interpret average absolute error |
| RMSE | Penalizes large prediction errors |
| R² Score | Measures explained variance |
| Residual plots | Shows systematic under- or overprediction |

Additional useful diagnostics:

- predicted vs. observed plot,
- residuals by land use,
- residuals by emission range,
- feature importance plot,
- optional SHAP analysis if time allows.

---

## 10. Current Strengths

The project already has several strong points:

- real scientific dataset,
- clear environmental relevance,
- reproducible data download script,
- raw-data validation step,
- separated data folders,
- feature documentation,
- notebook-based EDA workflow,
- `uv` environment management,
- XGBoost as a suitable model choice for tabular data.

---

## 11. Current Limitations

The project still needs improvement in several areas:

- the final model-ready dataset is not yet fully fixed,
- the XGBoost model-building notebook still needs to be completed,
- feature naming should be standardized consistently,
- exact preprocessing decisions must be documented,
- final model metrics are not available yet,
- the README and project documentation should be kept synchronized with the actual workflow.

These limitations are normal for the current project phase and can be addressed step by step.

---

## 12. Next Steps

Recommended next steps:

1. finalize the cleaned interim dataset,
2. define a stable target column,
3. build a single modeling dataframe,
4. implement baseline regression,
5. implement XGBoost regression,
6. evaluate with MAE, RMSE, and R²,
7. add residual diagnostics,
8. export final figures,
9. summarize findings for presentation,
10. update this report with final results.

---

## 13. Placeholder for Final Results

| Metric | Value |
|---|---:|
| MAE | TODO |
| RMSE | TODO |
| R² Score | TODO |

Most important features:

1. TODO
2. TODO
3. TODO

Main interpretation:

```text
TODO: Add final model interpretation after training and evaluation.
```

---

## 14. Conclusion

This project demonstrates a realistic machine learning workflow using environmental data. The main value of the project is not only the final model performance, but also the structured handling of scientific data, feature documentation, exploratory analysis, and transparent modeling decisions.

The final version should be suitable as a portfolio project because it combines data engineering, EDA, domain-aware feature interpretation, and machine learning in one coherent workflow.
