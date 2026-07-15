from __future__ import annotations

from collections import Counter
from typing import Mapping

import pandas as pd


# Canonical column names used throughout the complete modeling pipeline.
EVENT_COLUMN = "event_id"
# LATITUDE_COLUMN = "latitude_deg"
# LONGITUDE_COLUMN = "longitude_deg"
DATE_COLUMN = "observation_date"
LAND_USE_COLUMN = "land_use"
TARGET_COLUMN = "n2o_flux_ug_m2_h"


N2O_COLUMN_RENAME_MAP: dict[str, str] = {
    # Identification and spatial information
    "Event": EVENT_COLUMN,
    # "Latitude": LATITUDE_COLUMN,
    # "Longitude": LONGITUDE_COLUMN,
    "Date/Time": DATE_COLUMN,
    "Land use": LAND_USE_COLUMN,

    # Fertilizer management
    "Fert N [kg/ha] (Recorded at time of application)": (
        "fertilizer_n_applied_kg_ha"
    ),

    # ERA5 air-temperature variables
    "TTT day m [°C] (ERA5 reanalyses)": (
        "era5_air_temperature_mean_c"
    ),
    "TxTxTx day max [°C] (ERA5 reanalyses)": (
        "era5_air_temperature_max_c"
    ),
    "TnTnTn day min [°C] (ERA5 reanalyses)": (
        "era5_air_temperature_min_c"
    ),

    # ERA5 precipitation
    "Precip day total [mm/day] (ERA5 reanalyses)": (
        "era5_precipitation_daily_total_mm"
    ),

    # ERA5 volumetric soil-moisture layers
    "Soil moisture [m**3/m**3] (Content at 0-7 cm depth, ERA5...)": (
        "era5_soil_moisture_0_7cm_m3_m3"
    ),
    "Soil moisture [m**3/m**3] (ERA5 reanalyses)": (
        "era5_soil_moisture_7_28cm_m3_m3"
    ),
    "Soil moisture [m**3/m**3] (ERA5 reanalyses).1": (
        "era5_soil_moisture_28_100cm_m3_m3"
    ),

    # ERA5 soil-temperature layers
    "T soil day m [°C] (ERA5 reanalyses)": (
        "era5_soil_temperature_0_7cm_mean_c"
    ),
    "T soil day m [°C] (ERA5 reanalyses).1": (
        "era5_soil_temperature_7_28cm_mean_c"
    ),
    "T soil day m [°C] (ERA5 reanalyses).2": (
        "era5_soil_temperature_28_100cm_mean_c"
    ),

    # Additional ERA5 meteorological variables
    "Cloud cov [%] (ERA5 reanalyses)": (
        "era5_cloud_cover_pct"
    ),
    "VPD day m [kPa] (ERA5 reanalyses)": (
        "era5_vapor_pressure_deficit_mean_kpa"
    ),
    "PPPP day m [hPa] (ERA5 reanalyses)": (
        "era5_atmospheric_pressure_mean_hpa"
    ),
    "SWD day m [W/m**2] (ERA5 reanalyses)": (
        "era5_shortwave_radiation_mean_w_m2"
    ),
    "PPFD day m [µmol/m**2/s] (ERA5 reanalyses)": (
        "era5_ppfd_mean_umol_m2_s"
    ),

    # Event recency variables
    "Duration [days] (Since last precipitation even...)": (
        "days_since_precipitation_gt_1mm"
    ),
    "Duration [days] (Since last fertiliser applica...)": (
        "days_since_fertilizer_application"
    ),

    # Decay-adjusted nitrogen availability
    "Fert N dec adj exp [kg/ha] (Exponential decay model (k=0.05))": (
        "fertilizer_n_decay_adjusted_kg_ha"
    ),

    # Cyclic transformations supplied by the source dataset
    "Transformation S (Modeled)": (
        "source_time_cycle_sin"
    ),
    "Transformation C (Modeled)": (
        "source_time_cycle_cos"
    ),

    # Regression target
    "N2O flux [µg/m**2/h] (From soil surface, Modeled)": TARGET_COLUMN,
}


def standardize_n2o_column_names(
    dataframe: pd.DataFrame,
    rename_map: Mapping[str, str] | None = None,
    strict: bool = True,
    copy: bool = True,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Convert the original N2O dataset column names to a canonical schema.

    The original source column names contain spaces, units, abbreviations,
    special characters, truncated descriptions, and automatically generated
    pandas suffixes such as ".1" and ".2". This function replaces them with
    consistent snake_case names suitable for feature engineering and modeling.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Input dataframe containing the original dataset columns.
    rename_map : Mapping[str, str] or None, default=None
        Mapping from original column names to canonical names. If None,
        `N2O_COLUMN_RENAME_MAP` is used.
    strict : bool, default=True
        If True, raise an error when one or more expected source columns are
        missing. If False, rename only the columns that are available.
    copy : bool, default=True
        If True, return a renamed copy and leave the input dataframe unchanged.
    verbose : bool, default=False
        If True, print information about detected, missing, and renamed columns.

    Returns
    -------
    pd.DataFrame
        Dataframe with standardized column names.

    Raises
    ------
    TypeError
        If `dataframe` is not a pandas DataFrame or if the rename mapping
        contains non-string keys or values.
    ValueError
        If the mapping contains duplicate destination names, required source
        columns are missing in strict mode, or renaming would create duplicate
        dataframe columns.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(
            "`dataframe` must be a pandas DataFrame, "
            f"but received {type(dataframe).__name__}."
        )

    active_rename_map = dict(
        N2O_COLUMN_RENAME_MAP if rename_map is None else rename_map
    )

    invalid_mapping_entries = [
        (source_column, target_column)
        for source_column, target_column in active_rename_map.items()
        if not isinstance(source_column, str)
        or not isinstance(target_column, str)
    ]

    if invalid_mapping_entries:
        raise TypeError(
            "All rename-map keys and values must be strings. "
            f"Invalid entries: {invalid_mapping_entries}"
        )

    destination_counts = Counter(active_rename_map.values())
    duplicate_destinations = [
        column
        for column, count in destination_counts.items()
        if count > 1
    ]

    if duplicate_destinations:
        raise ValueError(
            "The rename mapping contains duplicate destination names: "
            f"{duplicate_destinations}"
        )

    missing_source_columns = [
        column
        for column in active_rename_map
        if column not in dataframe.columns
    ]

    if strict and missing_source_columns:
        raise ValueError(
            "The dataframe is missing columns required by the canonical "
            f"schema: {missing_source_columns}"
        )

    applicable_rename_map = {
        source_column: target_column
        for source_column, target_column in active_rename_map.items()
        if source_column in dataframe.columns
    }

    resulting_columns = [
        applicable_rename_map.get(column, column)
        for column in dataframe.columns
    ]

    duplicate_result_columns = [
        column
        for column, count in Counter(resulting_columns).items()
        if count > 1
    ]

    if duplicate_result_columns:
        raise ValueError(
            "Renaming would create duplicate dataframe columns: "
            f"{duplicate_result_columns}"
        )

    standardized_dataframe = dataframe.rename(
        columns=applicable_rename_map,
        copy=copy,
    )

    if verbose:
        print("Standardized N2O dataset column names.")
        print(f"Input columns       : {len(dataframe.columns)}")
        print(f"Renamed columns     : {len(applicable_rename_map)}")
        print(
            "Unchanged columns   : "
            f"{len(dataframe.columns) - len(applicable_rename_map)}"
        )

        if missing_source_columns:
            print(
                "Missing source cols : "
                f"{len(missing_source_columns)}"
            )

        print(
            "Duplicate columns    : "
            f"{standardized_dataframe.columns.duplicated().sum()}"
        )

    return standardized_dataframe