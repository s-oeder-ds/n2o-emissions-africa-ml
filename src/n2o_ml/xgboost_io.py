"""XGBoost-specific inspection helpers."""

from typing import Any, List, Optional, Sequence

import pandas as pd
from sklearn.pipeline import Pipeline


def get_transformed_feature_names(
    fitted_pipeline: Pipeline,
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
    verbose: bool = False,
) -> List[str]:
    """
    Extract transformed feature names from a fitted preprocessing pipeline.

    Parameters
    ----------
    fitted_pipeline : Pipeline
        Fitted pipeline containing a 'preprocess' step.
    numeric_features : Sequence[str]
        Original numeric feature names.
    categorical_features : Sequence[str]
        Original categorical feature names.
    verbose : bool, default=False
        If True, print feature-name extraction details.

    Returns
    -------
    List[str]
        Transformed feature names.

    Raises
    ------
    ValueError
        If the pipeline does not contain the expected preprocessing step.
    """
    if "preprocess" not in fitted_pipeline.named_steps:
        raise ValueError("Pipeline must contain a 'preprocess' step.")

    fitted_preprocessor = fitted_pipeline.named_steps["preprocess"]
    feature_names: List[str] = list(numeric_features)

    if len(categorical_features) > 0:
        categorical_pipeline = fitted_preprocessor.named_transformers_["categorical"]
        onehot = categorical_pipeline.named_steps["onehot"]
        categorical_names = onehot.get_feature_names_out(categorical_features).tolist()
        feature_names.extend(categorical_names)

    if verbose:
        print(f"Extracted {len(feature_names)} transformed feature names.")

    return feature_names


def extract_xgb_importance(
    fitted_pipeline: Pipeline,
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
    importance_type: str = "gain",
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Extract feature importance from a fitted XGBoost pipeline.

    Parameters
    ----------
    fitted_pipeline : Pipeline
        Fitted preprocessing + XGBoost pipeline.
    numeric_features : Sequence[str]
        Original numeric feature names.
    categorical_features : Sequence[str]
        Original categorical feature names.
    importance_type : str, default="gain"
        XGBoost importance type. Common values are 'gain', 'weight', 'cover', 'total_gain'.
    verbose : bool, default=False
        If True, print extraction diagnostics.

    Returns
    -------
    pd.DataFrame
        Feature importance table.

    Raises
    ------
    ValueError
        If the model step is missing.
    """
    if "model" not in fitted_pipeline.named_steps:
        raise ValueError("Pipeline must contain a 'model' step.")

    feature_names = get_transformed_feature_names(
        fitted_pipeline,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        verbose=verbose,
    )

    model = fitted_pipeline.named_steps["model"]
    booster = model.get_booster()
    score_dict = booster.get_score(importance_type=importance_type)

    rows = []
    for index, feature_name in enumerate(feature_names):
        xgb_key = f"f{index}"
        rows.append({
            "feature": feature_name,
            "importance": score_dict.get(xgb_key, 0.0),
        })

    importance_df = (
        pd.DataFrame(rows)
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    if verbose:
        print(f"Extracted importance for {len(importance_df)} features.")

    return importance_df