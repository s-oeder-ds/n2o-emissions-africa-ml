from pathlib import Path
from typing import Optional, Union, Dict


import pandas as pd


def align_cropland_columns(
    df: pd.DataFrame,
    verbose: bool = False
) -> pd.DataFrame:
    """
    Rename cropland-specific soil moisture and soil temperature columns to match
    the shorter column names used in the forest and grassland datasets.

    Parameters
    ----------
    df : pd.DataFrame
        Cropland dataframe whose column names should be standardized.
    verbose : bool, default=False
        If True, prints all renamed columns.

    Returns
    -------
    pd.DataFrame
        Copy of the input dataframe with renamed cropland columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input 'df' must be a pandas DataFrame.")

    rename_map: Dict[str, str] = {
        "Soil moisture [m**3/m**3] (Content at 7-28 cm depth, ERA...)": 
            "Soil moisture [m**3/m**3] (ERA5 reanalyses)",
        "Soil moisture [m**3/m**3] (Content at 28-100 cm depth, E...)": 
            "Soil moisture [m**3/m**3] (ERA5 reanalyses).1",
        "T soil day m [°C] (At 0-7 cm depth, ERA5 reanalyses)":
            "T soil day m [°C] (ERA5 reanalyses)",
        "T soil day m [°C] (At 7-28 cm depth, ERA5 reanal...)": 
            "T soil day m [°C] (ERA5 reanalyses).1",
        "T soil day m [°C] (At 28-100 cm depth, ERA5 rean...)": 
            "T soil day m [°C] (ERA5 reanalyses).2",
    }

    existing_rename_map = {
        old_name: new_name
        for old_name, new_name in rename_map.items()
        if old_name in df.columns
    }

    missing_columns = set(rename_map) - set(existing_rename_map)

    if verbose:
        print(f"Found {len(existing_rename_map)} cropland-specific columns to rename.")

        for old_name, new_name in existing_rename_map.items():
            print(f"Renaming: {old_name} -> {new_name}")

        if missing_columns:
            print("Columns not found and therefore not renamed:")
            for col in sorted(missing_columns):
                print(f"  - {col}")

    return df.rename(columns=existing_rename_map).copy()



if __name__ == "__main__":
    main(verbose=True)