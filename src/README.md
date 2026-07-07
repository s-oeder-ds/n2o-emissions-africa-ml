# Source Code

This folder contains reusable Python scripts for data acquisition and preprocessing.

## `download_pangaea_data.py`

Downloads the PANGAEA bundled dataset, validates the ZIP archive, and extracts
the raw files into the local data directory.

Main responsibilities:

- download dataset bundle,
- avoid unnecessary re-downloads,
- validate ZIP readability,
- extract raw files.

## `convert_pangaea_textfile.py`

Converts PANGAEA text-based source files into a more convenient tabular format.

Main responsibilities:

- read source text files,
- parse dataset content,
- prepare files for later pandas-based processing.

## `alignment.py`

Aligns land-use-specific column names.

This is especially useful for cropland columns where some ERA5 soil moisture
and soil temperature variables use more explicit depth descriptions than in
other land-use datasets.

## `preprocess_interim_data.py`

Contains reusable preprocessing utilities.

Current responsibilities:

- controlled column renaming,
- duplicate-column checks,
- optional saving of renamed dataframes to disk.
