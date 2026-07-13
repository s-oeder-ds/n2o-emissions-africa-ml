"""Group-aware model-selection helpers."""

from typing import Tuple

import pandas as pd
from sklearn.model_selection import GroupKFold, GroupShuffleSplit


def split_by_group(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
    verbose: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Split features and target into train and test sets without group leakage.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    y : pd.Series
        Target vector.
    groups : pd.Series
        Group labels. Samples from the same group stay in the same split.
    test_size : float, default=0.2
        Fraction of groups assigned to the test set.
    random_state : int, default=42
        Random seed for reproducible group sampling.
    verbose : bool, default=False
        If True, print split diagnostics.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series, pd.Series]
        X_train, X_test, y_train, y_test, groups_train, groups_test.

    Raises
    ------
    ValueError
        If input lengths are inconsistent, test_size is invalid, or too few groups exist.
    """
    if not (len(X) == len(y) == len(groups)):
        raise ValueError("X, y, and groups must have the same length.")

    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    if groups.nunique() < 3:
        raise ValueError("At least three unique groups are required for grouped splitting.")

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=test_size,
        random_state=random_state,
    )
    train_idx, test_idx = next(splitter.split(X, y, groups=groups))

    X_train = X.iloc[train_idx].copy()
    X_test = X.iloc[test_idx].copy()
    y_train = y.iloc[train_idx].copy()
    y_test = y.iloc[test_idx].copy()
    groups_train = groups.iloc[train_idx].copy()
    groups_test = groups.iloc[test_idx].copy()

    overlap = set(groups_train.unique()).intersection(set(groups_test.unique()))
    if overlap:
        raise ValueError(f"Group leakage detected. Overlapping groups: {overlap}")

    if verbose:
        print(f"Train rows       : {len(X_train):,}")
        print(f"Test rows        : {len(X_test):,}")
        print(f"Train groups     : {groups_train.nunique():,}")
        print(f"Test groups      : {groups_test.nunique():,}")
        print(f"Group overlap    : {len(overlap)}")
        print(f"Train target mean: {y_train.mean():.4f}")
        print(f"Test target mean : {y_test.mean():.4f}")

    return X_train, X_test, y_train, y_test, groups_train, groups_test


def build_group_kfold(
    groups_train: pd.Series,
    max_splits: int = 5,
    verbose: bool = False,
) -> GroupKFold:
    """
    Build a GroupKFold object with a valid number of splits.

    Parameters
    ----------
    groups_train : pd.Series
        Training group labels.
    max_splits : int, default=5
        Maximum number of splits.
    verbose : bool, default=False
        If True, print the selected number of splits.

    Returns
    -------
    GroupKFold
        Group-aware cross-validation splitter.

    Raises
    ------
    ValueError
        If fewer than two unique groups are available.
    """
    n_groups = groups_train.nunique()

    if n_groups < 2:
        raise ValueError("At least two unique groups are required for GroupKFold.")
    
    # Use the smaller value to avoid requesting more folds than available groups.
    # GroupKFold requires n_splits to be less than or equal to the number of unique groups.
    n_splits = min(max_splits, n_groups)

    if n_splits < max_splits:
            print(f"Warning: Requested max_splits={max_splits} exceeds available unique groups={n_groups}. Using n_splits={n_splits} instead.")
    elif verbose:
        print(f"Using GroupKFold with n_splits={n_splits}.")

    return GroupKFold(n_splits=n_splits)


# EXTRA: For example, functions to summarize train-test distributions or validate splits can be implemented below.
def summarize_split_distribution(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    land_use_column: str,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Create a compact summary of train-test distribution differences.

    Parameters
    ----------
    X_train : pd.DataFrame
        Training features.
    X_test : pd.DataFrame
        Test features.
    y_train : pd.Series
        Training target values.
    y_test : pd.Series
        Test target values.
    land_use_column : str
        Name of the land-use column.
    verbose : bool, default=False
        If True, print summary diagnostics.

    Returns
    -------
    pd.DataFrame
        Summary table with row counts and target statistics by split.

    Raises
    ------
    ValueError
        If the land-use column is missing from one of the feature matrices.
    """
    if land_use_column not in X_train.columns or land_use_column not in X_test.columns:
        raise ValueError(f"Land-use column missing: {land_use_column}")

    train_summary = pd.DataFrame({
        "split": "train",
        "land_use": X_train[land_use_column],
        "target": y_train,
    })
    test_summary = pd.DataFrame({
        "split": "test",
        "land_use": X_test[land_use_column],
        "target": y_test,
    })

    summary = pd.concat([train_summary, test_summary], axis=0)
    result = (
        summary
        .groupby(["split", "land_use"])["target"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
    )

    if verbose:
        print("Created split distribution summary.")

    return result


