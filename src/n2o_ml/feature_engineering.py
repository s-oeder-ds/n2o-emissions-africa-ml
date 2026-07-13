"""Project-specific feature engineering for the N2O emissions dataset."""

from typing import List

import numpy as np
import pandas as pd


def add_n2o_domain_features(
    dataframe: pd.DataFrame,
    date_column: str,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Add N2O-domain features derived from date, weather, soil, and fertilizer columns.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Input dataset.
    date_column : str
        Name of the date column.
    verbose : bool, default=False
        If True, print all generated feature names.

    Returns
    -------
    pd.DataFrame
        Copy of the input dataset with additional engineered features.

    Raises
    ------
    TypeError
        If dataframe is not a pandas DataFrame.
    ValueError
        If date_column is missing.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame.")

    if date_column not in dataframe.columns:
        raise ValueError(f"date_column is missing from dataframe: {date_column}")

    df_features = dataframe.copy()
    created_features: List[str] = []

    # Convert dates once and keep invalid values as NaT instead of crashing silently.
    df_features[date_column] = pd.to_datetime(df_features[date_column], errors="coerce")

    # Basic temporal features.
    df_features["year"] = df_features[date_column].dt.year
    df_features["month"] = df_features[date_column].dt.month
    df_features["day_of_year"] = df_features[date_column].dt.dayofyear
    df_features["week_of_year"] = (
        df_features[date_column].dt.isocalendar().week.astype("float")
    )
    created_features.extend(["year", "month", "day_of_year", "week_of_year"])

    # Cyclic encodings avoid an artificial jump between December and January.
    df_features["month_sin"] = np.sin(2 * np.pi * df_features["month"] / 12)
    df_features["month_cos"] = np.cos(2 * np.pi * df_features["month"] / 12)
    df_features["day_of_year_sin"] = np.sin(
        2 * np.pi * df_features["day_of_year"] / 365.25
    )
    df_features["day_of_year_cos"] = np.cos(
        2 * np.pi * df_features["day_of_year"] / 365.25
    )
    created_features.extend(
        ["month_sin", "month_cos", "day_of_year_sin", "day_of_year_cos"]
    )

    # Interpretable meteorological season labels.
    month_to_season = {
        12: "DJF",
        1: "DJF",
        2: "DJF",
        3: "MAM",
        4: "MAM",
        5: "MAM",
        6: "JJA",
        7: "JJA",
        8: "JJA",
        9: "SON",
        10: "SON",
        11: "SON",
    }
    df_features["season"] = df_features["month"].map(month_to_season)
    created_features.append("season")

    # Temperature range can represent daily thermal variability.
    max_temp_col = "TxTxTx day max [°C] (ERA5 reanalyses)"
    min_temp_col = "TnTnTn day min [°C] (ERA5 reanalyses)"
    if max_temp_col in df_features.columns and min_temp_col in df_features.columns:
        df_features["air_temp_range"] = df_features[max_temp_col] - df_features[min_temp_col]
        created_features.append("air_temp_range")

    # Fertilizer intensity proxy: high recent nitrogen application should matter more.
    fert_col = "Fert N [kg/ha] (Recorded at time of application)"
    fert_duration_col = "Duration [days] (Since last fertiliser applica...)"
    if fert_col in df_features.columns and fert_duration_col in df_features.columns:
        df_features["fert_n_per_day_since_application"] = (
            df_features[fert_col] / (1 + df_features[fert_duration_col].clip(lower=0))
        )
        created_features.append("fert_n_per_day_since_application")

    # Exponential precipitation recency proxy.
    precip_duration_col = "Duration [days] (Since last precipitation even...)"
    if precip_duration_col in df_features.columns:
        df_features["precip_recency_decay"] = np.exp(
            -0.05 * df_features[precip_duration_col].clip(lower=0)
        )
        created_features.append("precip_recency_decay")

    # Process-inspired interaction terms.
    mean_temp_col = "TTT day m [°C] (ERA5 reanalyses)"
    soil_moisture_col = "Soil moisture [m**3/m**3] (Content at 0-7 cm depth, ERA5...)"

    if mean_temp_col in df_features.columns and soil_moisture_col in df_features.columns:
        df_features["air_temp_x_topsoil_moisture"] = (
            df_features[mean_temp_col] * df_features[soil_moisture_col]
        )
        created_features.append("air_temp_x_topsoil_moisture")

    if fert_col in df_features.columns and soil_moisture_col in df_features.columns:
        df_features["fert_n_x_topsoil_moisture"] = (
            df_features[fert_col] * df_features[soil_moisture_col]
        )
        created_features.append("fert_n_x_topsoil_moisture")

    if fert_col in df_features.columns and mean_temp_col in df_features.columns:
        df_features["fert_n_x_air_temp"] = df_features[fert_col] * df_features[mean_temp_col]
        created_features.append("fert_n_x_air_temp")

    if verbose:
        print(f"Created {len(created_features)} engineered features:")
        for feature in created_features:
            print(f"- {feature}")

    return df_features
