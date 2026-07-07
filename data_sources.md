# Data Sources

This document records the external data sources used in the project  
**N₂O Emissions in Africa — Machine Learning Portfolio Project**.

The original scientific data is provided by PANGAEA. The repository contains
code and documentation for working with the data, but the data itself remains
subject to the original PANGAEA license and citation requirements.

---

## Main Bundled Publication

**Citation**

Agredazywczuk, Phillip; Ouma, Turry; Barthel, Matti; Otinga, Abigael; Njoroge, Ruth; Butterbach-Bahl, Klaus; Daelman, Roxanne; Hickman, Jonathan; Ibrahim, Wanyama; Laub, Moritz; Leitner, Sonja; Shumba, Armwell; Tully, Katherine; Wachiye, Sheila; Zheng, Jinsen; Bauters, Marijn; Kiese, Ralf; Cardinael, Rémi; Balokah, Rita; Christian, Andreas; Kesia, Lourenco; Ouattara, Kakira; Harris, Eliza; Six, Johan (2026):  
*Nitrous oxide emissions across Sub-Saharan Africa: meta-analysis and data-driven modelling* [dataset bundled publication].  
PANGAEA. DOI: `10.1594/PANGAEA.987298`

**Source URL**

```text
https://doi.org/10.1594/PANGAEA.987298
```

**Direct download used in this project**

```text
https://doi.pangaea.de/10.1594/PANGAEA.987298?format=zip
```

**Publication date**

```text
2026-02-20
```

**License**

```text
Creative Commons Attribution 4.0 International (CC-BY-4.0)
```

**Project usage**

This bundled publication is the main source of the raw N₂O emission data used
for preprocessing, exploratory data analysis, and machine learning.

---

## Datasets Included in the Bundled Publication

### 1. Nitrous oxide emissions from African Croplands

| Field | Information |
|---|---|
| DOI | `10.1594/PANGAEA.987299` |
| Source URL | `https://doi.org/10.1594/PANGAEA.987299` |
| Provider | PANGAEA |
| Topic | N₂O emissions from African croplands |
| Used for | Land-use-specific preprocessing, EDA, and model dataset construction |

---

### 2. Nitrous oxide emissions from African Forests and Plantations

| Field | Information |
|---|---|
| DOI | `10.1594/PANGAEA.987301` |
| Source URL | `https://doi.org/10.1594/PANGAEA.987301` |
| Provider | PANGAEA |
| Topic | N₂O emissions from African forests and plantations |
| Used for | Land-use-specific preprocessing, EDA, and model dataset construction |

---

### 3. Nitrous oxide emissions from African Grasslands

| Field | Information |
|---|---|
| DOI | `10.1594/PANGAEA.987305` |
| Source URL | `https://doi.org/10.1594/PANGAEA.987305` |
| Provider | PANGAEA |
| Topic | N₂O emissions from African grasslands |
| Used for | Land-use-specific preprocessing, EDA, and model dataset construction |

---

### 4. Site Information

| Field | Information |
|---|---|
| DOI | `10.1594/PANGAEA.987307` |
| Source URL | `https://doi.org/10.1594/PANGAEA.987307` |
| Provider | PANGAEA |
| Topic | Site information for N₂O observations across croplands, forests, and grasslands |
| Used for | Contextual site information and possible metadata enrichment |

---

## Dataset Summary

According to the PANGAEA bundled publication, the data collection includes:

- N₂O flux measurements from 27 sites,
- six African countries,
- multiple land-use types,
- 5,280 daily observations,
- observation period from 2005 to 2025,
- 26 environmental covariates,
- meteorological, soil, and management-related variables.

The dataset supports greenhouse gas emission research and data-driven modeling
for African environments.

---

## Data Handling in This Repository

The repository uses the following local data layout:

```text
data/
├── external/
├── interim/
├── processed/
└── raw/
```

Large data files are ignored by Git. Only folder placeholders and metadata
documentation should be committed.

The intended workflow is:

```text
download PANGAEA ZIP bundle
        ↓
validate ZIP archive
        ↓
extract raw source files
        ↓
convert PANGAEA text files
        ↓
align land-use-specific columns
        ↓
build interim dataset
        ↓
prepare processed modeling data
        ↓
run EDA and model building
```

---

## Access Date

Access date should be updated whenever the data is freshly downloaded.

```text
Last checked for this documentation draft: 2026-07-08
```

---

## Notes

The project documentation should always cite the PANGAEA bundled publication
when results, figures, or model outputs are based on the dataset.

The MIT License in this repository only applies to the project code and local
documentation. It does not relicense the original PANGAEA data.
