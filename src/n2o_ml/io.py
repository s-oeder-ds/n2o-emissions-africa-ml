"""Input/output helper functions for tabular data projects."""

from pathlib import Path
from typing import Iterable, List, Sequence, Union

import pandas as pd

PathLike = Union[str, Path]

def find_existing_path(
    candidate_paths: Sequence[Path],
    verbose: bool = False,
) -> Path:
    """
    Return the first existing path from a sequence of candidate paths.

    Parameters
    ----------
    candidate_paths : Sequence[Path]
        Candidate file paths that should be checked in order.
    verbose : bool, default=False
        If True, print every checked path and the final selected path.

    Returns
    -------
    Path
        The first path that exists.

    Raises
    ------
    FileNotFoundError
        If none of the candidate paths exists.
    TypeError
        If candidate_paths is not an iterable of Path-like objects.
    """
    if not isinstance(candidate_paths, Iterable):
        raise TypeError("candidate_paths must be an iterable of Path objects.")

    checked_paths: List[Path] = []

    for candidate_path in candidate_paths:
        path = Path(candidate_path)
        checked_paths.append(path)

        if verbose:
            print(f"Checking path: {path.resolve()}")

        if path.exists():
            if verbose:
                print(f"Selected path: {path.resolve()}")
            return path

    checked_text = "\n".join(str(path) for path in checked_paths)
    raise FileNotFoundError(
        "None of the candidate paths exists. Checked paths:\n" + checked_text
    )

def load_dataset(
    csv_path: Path,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Load a CSV dataset into a pandas DataFrame.

    Parameters
    ----------
    csv_path : Path
        Path to the CSV file.
    verbose : bool, default=False
        If True, print information about the loaded dataset.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If the loaded dataset is empty.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)

    if dataframe.empty:
        raise ValueError(f"Loaded dataset is empty: {csv_path}")

    if verbose:
        print(f"Loaded dataset from: {csv_path.resolve()}")
        print(f"Shape: {dataframe.shape[0]:,} rows x {dataframe.shape[1]:,} columns")

    return dataframe


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: Sequence[str],
    verbose: bool = False,
) -> None:
    """
    Validate that all required columns are present in a DataFrame.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataset to validate.
    required_columns : Sequence[str]
        Column names that must exist in the dataset.
    verbose : bool, default=False
        If True, print validation details.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If dataframe is not a pandas DataFrame.
    ValueError
        If at least one required column is missing.
    """
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe must be a pandas DataFrame.")

    missing_columns = [column for column in required_columns if column not in dataframe.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if verbose:
        print("All required columns are available.")