"""Preprocessing utilities for tabular scikit-learn pipelines."""

from typing import List, Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def make_one_hot_encoder(verbose: bool = False) -> OneHotEncoder:
    """
    Create a OneHotEncoder compatible with older and newer scikit-learn versions.

    Parameters
    ----------
    verbose : bool, default=False
        If True, print which keyword argument is used for dense output.

    Returns
    -------
    OneHotEncoder
        Configured encoder with unknown-category protection.
    """
    try:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        if verbose:
            print("Using OneHotEncoder with sparse_output=False.")
    except TypeError:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse=False)
        if verbose:
            print("Using OneHotEncoder with sparse=False.")

    return encoder


def infer_feature_types(
    X: pd.DataFrame,
    verbose: bool = False,
) -> Tuple[List[str], List[str]]:
    """
    Infer numeric and categorical feature columns from pandas dtypes.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    verbose : bool, default=False
        If True, print the number and names of inferred feature types.

    Returns
    -------
    Tuple[List[str], List[str]]
        Numeric feature names and categorical feature names.

    Raises
    ------
    TypeError
        If X is not a pandas DataFrame.
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    if verbose:
        print(f"Numeric features    : {len(numeric_features)}")
        print(f"Categorical features: {len(categorical_features)}")
        print("Categorical columns :", categorical_features)

    return numeric_features, categorical_features

def build_preprocessor(
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
    verbose: bool = False,
) -> ColumnTransformer:
    """
    Build a preprocessing transformer for numerical and categorical features.

    Parameters
    ----------
    numeric_features : Sequence[str]
        Numerical feature names.
    categorical_features : Sequence[str]
        Categorical feature names.
    verbose : bool, default=False
        If True, print preprocessing details.

    Returns
    -------
    ColumnTransformer
        Preprocessing transformer.
    """
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", make_one_hot_encoder(verbose=verbose)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(numeric_features)),
            ("categorical", categorical_pipeline, list(categorical_features)),
        ],
        remainder="drop",
    )

    if verbose:
        print("Preprocessor created.")

    return preprocessor

# build_tabular_preprocessor and get_feature_type_lists are now defined in this file, so they can be imported and used in the notebook without needing to redefine them there.
# it is a different approach then build_preprocessor, but it is more modular and allows for more flexibility in the future.
def build_tabular_preprocessor(
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
    verbose: bool = False,
) -> ColumnTransformer:
    """
    Build a ColumnTransformer for numeric and categorical tabular features.

    Parameters
    ----------
    numeric_features : Sequence[str]
        Numerical feature names.
    categorical_features : Sequence[str]
        Categorical feature names.
    verbose : bool, default=False
        If True, print preprocessing details.

    Returns
    -------
    ColumnTransformer
        Preprocessing transformer for use inside a scikit-learn Pipeline.
    """
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", make_one_hot_encoder(verbose=verbose)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(numeric_features)),
            ("categorical", categorical_pipeline, list(categorical_features)),
        ],
        remainder="drop",
    )

    if verbose:
        print("Tabular preprocessor created.")
        print(f"Numeric columns    : {len(numeric_features)}")
        print(f"Categorical columns: {len(categorical_features)}")

    return preprocessor

def get_feature_type_lists(
    X: pd.DataFrame,
    verbose: bool = False,
) -> Tuple[List[str], List[str]]:
    """
    Identify numeric and categorical feature columns.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix.
    verbose : bool, default=False
        If True, print the identified feature types.

    Returns
    -------
    Tuple[List[str], List[str]]
        Numeric feature names and categorical feature names.

    Raises
    ------
    TypeError
        If X is not a pandas DataFrame.
    """
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")

    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    if verbose:
        print(f"Numeric features    : {len(numeric_features)}")
        print(f"Categorical features: {len(categorical_features)}")
        print("Categorical columns :", categorical_features)

    return numeric_features, categorical_features