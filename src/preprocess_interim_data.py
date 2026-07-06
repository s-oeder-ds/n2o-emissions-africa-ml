from pathlib import Path
from typing import Mapping, Optional, Union

import pandas as pd


def rebrand_columns(
    data: pd.DataFrame,
    names: Mapping[str, str],
    save_to_disk: bool = False,
    output_path: Optional[Union[str, Path]] = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Rename selected columns of a pandas DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        Input DataFrame whose columns should be renamed.

    names : Mapping[str, str]
        Dictionary-like mapping where keys are existing column names
        and values are the new column names.

    save_to_disk : bool, default=False
        If True, the renamed DataFrame will be saved to disk.

    output_path : Optional[Union[str, Path]], default=None
        File path where the DataFrame should be saved.
        Supported formats: .csv, .parquet, .pkl, .pickle

    verbose : bool, default=False
        If True, prints detailed information about the renaming process.

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with renamed columns.

    Raises
    ------
    TypeError
        If input arguments have invalid types.

    ValueError
        If column names are missing, duplicated, or output_path is invalid.
    """

    # Validate input DataFrame.
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame.")

    # Validate column mapping.
    if not isinstance(names, Mapping):
        raise TypeError("names must be a dictionary-like mapping.")

    # Validate that all old column names are strings.
    invalid_old_names = [old_name for old_name in names.keys() if not isinstance(old_name, str)]
    if invalid_old_names:
        raise TypeError(f"All keys in names must be strings. Invalid keys: {invalid_old_names}")

    # Validate that all new column names are strings.
    invalid_new_names = [new_name for new_name in names.values() if not isinstance(new_name, str)]
    if invalid_new_names:
        raise TypeError(f"All values in names must be strings. Invalid values: {invalid_new_names}")

    # Check whether all columns to rename exist in the DataFrame.
    missing_columns = [column for column in names.keys() if column not in data.columns]
    if missing_columns:
        raise ValueError(f"The following columns are missing in data: {missing_columns}")

    # Check whether the new column names would create duplicates.
    remaining_columns = [column for column in data.columns if column not in names.keys()]
    renamed_columns = list(names.values())
    final_columns = remaining_columns + renamed_columns

    duplicated_columns = [
        column for column in final_columns if final_columns.count(column) > 1
    ]

    if duplicated_columns:
        raise ValueError(
            f"Renaming would create duplicated column names: {sorted(set(duplicated_columns))}"
        )

    # Print information before renaming if verbose mode is enabled.
    if verbose:
        print("Starting column renaming...")
        print(f"Original columns: {list(data.columns)}")
        print("Column rename mapping:")

        for old_name, new_name in names.items():
            print(f"  {old_name} -> {new_name}")

    # Rename columns on a copy to avoid changing the original DataFrame unexpectedly.
    renamed_data = data.rename(columns=names).copy()

    # Print information after renaming if verbose mode is enabled.
    if verbose:
        print(f"Renamed columns: {list(renamed_data.columns)}")
        print("Column renaming completed.")

    # Save DataFrame to disk if requested.
    if save_to_disk:
        if output_path is None:
            raise ValueError("output_path must be provided when save_to_disk=True.")

        output_path = Path(output_path)

        # Create parent directories if they do not exist.
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the DataFrame depending on the file extension.
        if output_path.suffix == ".csv":
            renamed_data.to_csv(output_path, index=False)

        elif output_path.suffix == ".parquet":
            renamed_data.to_parquet(output_path, index=False)

        elif output_path.suffix in [".pkl", ".pickle"]:
            renamed_data.to_pickle(output_path)

        else:
            raise ValueError(
                "Unsupported file format. Use one of: .csv, .parquet, .pkl, .pickle"
            )

        if verbose:
            print(f"Renamed DataFrame saved to: {output_path}")

    return renamed_data


if __name__ == "__main__":
    # Example usage.
    df = pd.DataFrame(
        {
            "old_name_1": [1, 2, 3],
            "old_name_2": [4, 5, 6],
        }
    )

    column_mapping = {
        "old_name_1": "new_name_1",
        "old_name_2": "new_name_2",
    }

    df_renamed = rebrand_columns(
        data=df,
        names=column_mapping,
        save_to_disk=False,
        output_path=None,
        verbose=True,
    )

    print(df_renamed)