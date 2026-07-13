"""Utilities for saving trained models and related artifacts."""

from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Union

import joblib
import pandas as pd


PathLike = Union[str, Path]


def save_model_artifacts(
    model: Any,
    output_dir: PathLike,
    model_name: str,
    tables: Optional[Mapping[str, pd.DataFrame]] = None,
    metadata: Optional[Mapping[str, Any]] = None,
    feature_groups: Optional[Mapping[str, Sequence[str]]] = None,
    table_index: bool = False,
    overwrite: bool = True,
    verbose: bool = False,
) -> Dict[str, Path]:
    """
    Save a trained model and optional related artifacts.

    Parameters
    ----------
    model : Any
        Fitted model, pipeline, or another serializable estimator.
    output_dir : PathLike
        Directory in which all artifacts are stored.
    model_name : str
        Base name used for generated files.
    tables : Optional[Mapping[str, pd.DataFrame]], default=None
        Named DataFrames that should be stored as CSV files.
        The dictionary keys are used as filename suffixes.
    metadata : Optional[Mapping[str, Any]], default=None
        Additional information stored together with the model.
    feature_groups : Optional[Mapping[str, Sequence[str]]], default=None
        Named feature collections, such as numeric or categorical features.
    table_index : bool, default=False
        If True, include DataFrame indices in saved CSV files.
    overwrite : bool, default=True
        If False, raise an error when an output file already exists.
    verbose : bool, default=False
        If True, print all created artifact paths.

    Returns
    -------
    Dict[str, Path]
        Mapping between artifact names and saved file paths.

    Raises
    ------
    ValueError
        If model_name is empty or contains unsupported path components.
    TypeError
        If tables contains values that are not pandas DataFrames.
    FileExistsError
        If overwrite is False and an output file already exists.
    """
    if not isinstance(model_name, str) or not model_name.strip():
        raise ValueError("model_name must be a non-empty string.")

    cleaned_model_name = model_name.strip()

    # Prevent model_name from unintentionally creating nested paths.
    if Path(cleaned_model_name).name != cleaned_model_name:
        raise ValueError(
            "model_name must be a filename only and must not contain directory components."
        )

    artifact_directory = Path(output_dir)
    artifact_directory.mkdir(parents=True, exist_ok=True)

    normalized_tables: Dict[str, pd.DataFrame] = dict(tables or {})
    normalized_metadata: Dict[str, Any] = dict(metadata or {})
    normalized_feature_groups: Dict[str, list[str]] = {
        group_name: list(columns)
        for group_name, columns in (feature_groups or {}).items()
    }

    for table_name, dataframe in normalized_tables.items():
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("Every table name must be a non-empty string.")

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                f"Artifact '{table_name}' must be a pandas DataFrame, "
                f"not {type(dataframe).__name__}."
            )

    model_path = artifact_directory / f"{cleaned_model_name}_model.joblib"

    table_paths = {
        table_name: artifact_directory / f"{cleaned_model_name}_{table_name}.csv"
        for table_name in normalized_tables
    }

    output_paths = {
        "model": model_path,
        **table_paths,
    }

    if not overwrite:
        existing_paths = [
            path for path in output_paths.values() if path.exists()
        ]

        if existing_paths:
            existing_text = "\n".join(str(path) for path in existing_paths)
            raise FileExistsError(
                "The following artifact files already exist:\n"
                f"{existing_text}"
            )

    # Store the model together with information required for later interpretation.
    model_bundle: Dict[str, Any] = {
        "model": model,
        "metadata": normalized_metadata,
        "feature_groups": normalized_feature_groups,
    }

    joblib.dump(model_bundle, model_path)

    for table_name, dataframe in normalized_tables.items():
        dataframe.to_csv(
            table_paths[table_name],
            index=table_index,
        )

    if verbose:
        print("Saved model artifacts:")

        for artifact_name, artifact_path in output_paths.items():
            print(f"- {artifact_name}: {artifact_path.resolve()}")

    return output_paths