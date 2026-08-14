"""Spectral normalization methods.

max:    I' = I / max(I)
vector: I' = I / ||I||_2                       (unit L2 norm)
area:   I' = I / integral(I dx)                (unit total area, trapezoidal)
SNV:    I' = (I - mean(I)) / std(I)            (standard normal variate)
TIC:    I' = I / sum(I)                        (total-intensity-count normalization,
                                                 the discrete-sum analogue of area
                                                 normalization -- resolution-independent
                                                 since it does not weight by the
                                                 (possibly non-uniform) x-axis spacing)
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def max_normalize(y: np.ndarray) -> np.ndarray:
    return y / np.max(y)


def vector_normalize(y: np.ndarray) -> np.ndarray:
    return y / np.linalg.norm(y)


def area_normalize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    area = np.trapz(y, x)
    return y / area


def snv_normalize(y: np.ndarray) -> np.ndarray:
    return (y - np.mean(y)) / np.std(y)


def tic_normalize(y: np.ndarray) -> np.ndarray:
    total = np.sum(np.clip(y, 0, None))
    return y / total if total > 0 else y


NORMALIZATION_METHODS = {
    "max": lambda x, y: max_normalize(y),
    "vector": lambda x, y: vector_normalize(y),
    "area": lambda x, y: area_normalize(y, x),
    "SNV": lambda x, y: snv_normalize(y),
    "TIC": lambda x, y: tic_normalize(y),
}


def compare_methods(x: np.ndarray, y: np.ndarray) -> tuple[pd.DataFrame, dict]:
    """Report scale-invariance diagnostics; the appropriate choice for
    matching an intensity-arbitrary DFT stick spectrum is justified in the
    notebook text (max-normalization preserves relative peak-height ratios,
    which is what is compared to DFT band intensities)."""
    normalized = {name: fn(x, y) for name, fn in NORMALIZATION_METHODS.items()}
    rows = []
    for name, y_n in normalized.items():
        rows.append(dict(
            method=name,
            range_min=float(np.min(y_n)),
            range_max=float(np.max(y_n)),
            mean=float(np.mean(y_n)),
            std=float(np.std(y_n)),
        ))
    return pd.DataFrame(rows), normalized
