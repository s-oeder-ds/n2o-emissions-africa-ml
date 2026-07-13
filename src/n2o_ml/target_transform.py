"""Target transformation utilities."""

from typing import Optional, Sequence

import numpy as np


class ShiftedLogTargetTransformer:
    """
    Shifted log1p target transformer for targets that may contain negative values.

    The learned shift is based only on the training target. This avoids using holdout
    information when transforming the target variable.
    """

    def __init__(self, margin: float = 1e-6, verbose: bool = False) -> None:
        """
        Initialize the transformer.

        Parameters
        ----------
        
        margin : float, default=1e-6
            Small positive margin added when negative target values require shifting.
        verbose : bool, default=False
            If True, print initialization details.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If margin is negative.
        """
        if margin < 0:
            raise ValueError("margin must be non-negative.")

        self.margin = float(margin)
        self.shift_: Optional[float] = None

        if verbose:
            print(f"Initialized ShiftedLogTargetTransformer with margin={self.margin}.")

    def fit(self, y: Sequence[float], verbose: bool = False) -> "ShiftedLogTargetTransformer":
        """
        Learn the shift from training target values.

        Parameters
        ----------
        y : Sequence[float]
            Training target values on the original scale.
        verbose : bool, default=False
            If True, print the learned shift.

        Returns
        -------
        ShiftedLogTargetTransformer
            Fitted transformer instance.

        Raises
        ------
        ValueError
            If y is empty or contains non-finite values.
        """
        y_array = np.asarray(y, dtype=float)

        if y_array.size == 0:
            raise ValueError("y must not be empty.")

        if not np.isfinite(y_array).all():
            raise ValueError("y contains non-finite values.")

        min_value = float(np.min(y_array))
        self.shift_ = max(0.0, -min_value + self.margin)

        if verbose:
            print(f"Training target minimum: {min_value:.6f}")
            print(f"Learned log shift      : {self.shift_:.6f}")

        return self

    def transform(self, y: Sequence[float], verbose: bool = False) -> np.ndarray:
        """
        Apply the learned shifted log1p transformation.

        Parameters
        ----------
        y : Sequence[float]
            Target values on the original scale.
        verbose : bool, default=False
            If True, print transformation diagnostics.

        Returns
        -------
        np.ndarray
            Transformed target values.

        Raises
        ------
        RuntimeError
            If the transformer has not been fitted.
        ValueError
            If transformed input would be invalid for log1p.
        """
        if self.shift_ is None:
            raise RuntimeError("Transformer must be fitted before transform is called.")

        y_array = np.asarray(y, dtype=float)
        shifted = y_array + self.shift_

        if np.any(shifted <= -1):
            raise ValueError("Shifted target contains values <= -1, which is invalid for log1p.")

        transformed = np.log1p(shifted)

        if verbose:
            print(f"Original target range   : {y_array.min():.4f} to {y_array.max():.4f}")
            print(f"Transformed target range: {transformed.min():.4f} to {transformed.max():.4f}")

        return transformed

    def fit_transform(self, y: Sequence[float], verbose: bool = False) -> np.ndarray:
        """
        Fit the transformer and transform the same target values.

        Parameters
        ----------
        y : Sequence[float]
            Training target values on the original scale.
        verbose : bool, default=False
            If True, print fitting and transformation diagnostics.

        Returns
        -------
        np.ndarray
            Transformed target values.
        """
        self.fit(y, verbose=verbose)
        return self.transform(y, verbose=verbose)

    def inverse_transform(self, y_transformed: Sequence[float], verbose: bool = False) -> np.ndarray:
        """
        Transform shifted log1p values back to the original target scale.

        Parameters
        ----------
        y_transformed : Sequence[float]
            Target values on the transformed scale.
        verbose : bool, default=False
            If True, print inverse transformation diagnostics.

        Returns
        -------
        np.ndarray
            Target values on the original scale.

        Raises
        ------
        RuntimeError
            If the transformer has not been fitted.
        """
        if self.shift_ is None:
            raise RuntimeError("Transformer must be fitted before inverse_transform is called.")

        transformed_array = np.asarray(y_transformed, dtype=float)
        original_scale = np.expm1(transformed_array) - self.shift_

        if verbose:
            print(f"Inverse-transformed range: {original_scale.min():.4f} to {original_scale.max():.4f}")

        return original_scale
