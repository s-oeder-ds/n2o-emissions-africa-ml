"""Regression evaluation helpers."""

from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, r2_score


def regression_metrics(
    y_true: Sequence[float],
    y_pred: Sequence[float],
    prefix: str = "",
    verbose: bool = False,
) -> Dict[str, float]:
    """
    Calculate standard regression metrics on the original target scale.

    Parameters
    ----------
    y_true : Sequence[float]
        True target values.
    y_pred : Sequence[float]
        Predicted target values.
    prefix : str, default=""
        Optional prefix for metric names.
    verbose : bool, default=False
        If True, print calculated metric values.

    Returns
    -------
    Dict[str, float]
        MAE, RMSE, R2, median absolute error, and mean residual bias.

    Raises
    ------
    ValueError
        If inputs have different lengths, are empty, or contain non-finite values.
    """
    y_true_array = np.asarray(y_true, dtype=float)
    y_pred_array = np.asarray(y_pred, dtype=float)

    if y_true_array.shape[0] != y_pred_array.shape[0]:
        raise ValueError("y_true and y_pred must have the same length.")

    if y_true_array.size == 0:
        raise ValueError("y_true and y_pred must not be empty.")

    if not np.isfinite(y_true_array).all() or not np.isfinite(y_pred_array).all():
        raise ValueError("y_true and y_pred must contain only finite values.")

    residuals = y_true_array - y_pred_array
    r2 = r2_score(y_true_array, y_pred_array) if y_true_array.size >= 2 else np.nan

    metrics = {
        f"{prefix}mae": float(mean_absolute_error(y_true_array, y_pred_array)),
        f"{prefix}rmse": float(np.sqrt(mean_squared_error(y_true_array, y_pred_array))),
        f"{prefix}r2": float(r2),
        f"{prefix}median_ae": float(median_absolute_error(y_true_array, y_pred_array)),
        f"{prefix}bias_mean_residual": float(np.mean(residuals)),
    }

    if verbose:
        for name, value in metrics.items():
            print(f"{name}: {value:.4f}")

    return metrics

def metrics_by_group(
    dataframe: pd.DataFrame,
    group_column: str,
    y_true_column: str = "y_true",
    y_pred_column: str = "y_pred",
    min_count: int = 1,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Calculate regression metrics separately for each value of a grouping column.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame containing true values, predictions, and group labels.
    group_column : str
        Column used for grouping.
    y_true_column : str, default="y_true"
        Column containing true target values.
    y_pred_column : str, default="y_pred"
        Column containing predicted target values.
    min_count : int, default=1
        Minimum number of observations required per group.
    verbose : bool, default=False
        If True, print diagnostics.

    Returns
    -------
    pd.DataFrame
        Metrics table by group.

    Raises
    ------
    ValueError
        If required columns are missing or min_count is invalid.
    """
    if min_count < 1:
        raise ValueError("min_count must be at least 1.")

    required = [group_column, y_true_column, y_pred_column]
    missing = [column for column in required if column not in dataframe.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    rows: List[Dict[str, Any]] = []

    for group_value, group_df in dataframe.groupby(group_column, dropna=False):
        if len(group_df) < min_count:
            continue

        metrics = regression_metrics(
            group_df[y_true_column],
            group_df[y_pred_column],
            prefix="",
            verbose=False,
        )
        metrics[group_column] = group_value
        metrics["count"] = len(group_df)
        rows.append(metrics)

    result = pd.DataFrame(rows)
    if result.empty:
        if verbose:
            print("No groups reached the required minimum count.")
        return result

    ordered_columns = [
        group_column,
        "count",
        "mae",
        "rmse",
        "r2",
        "median_ae",
        "bias_mean_residual",
    ]
    result = result[ordered_columns].sort_values("mae", ascending=False).reset_index(drop=True)

    if verbose:
        print(f"Calculated metrics for {len(result)} groups from column: {group_column}")

    return result
