"""Multivariate analysis (PCA, hierarchical clustering, correlation matrix)
across all raw spectra, to test whether sample-preparation condition
(concentration/volume) systematically shifts the Raman band pattern.

Each raw spectrum is independently processed with the same fixed
pipeline (dark subtraction, Rayleigh masking, ALS baseline, Savitzky-Golay
smoothing, max normalization) -- the same method choices already
objectively selected in the main single-spectrum pipeline -- then
interpolated onto a common grid to build one feature matrix.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist, squareform
from sklearn.decomposition import PCA

from . import io_raw, baseline, smoothing


def build_feature_matrix(all_specs: list, grid: np.ndarray) -> tuple[np.ndarray, list[str], list[str]]:
    rows = []
    labels, conditions = [], []
    for s in all_specs:
        x_full = s.data["Raman Shift"].to_numpy()
        y_full = io_raw.dark_subtract(s)
        x, y = io_raw.mask_rayleigh_region(x_full, y_full, cutoff_cm1=100.0)
        y_bl = y - baseline.als_baseline(y)
        y_sm = smoothing.savgol_smooth(y_bl, window_length=11, polyorder=3)
        y_norm = y_sm / np.max(y_sm) if np.max(y_sm) > 0 else y_sm
        rows.append(np.interp(grid, x, y_norm))
        labels.append(s.sample_id)
        conditions.append(s.condition)
    return np.vstack(rows), labels, conditions


def run_pca(X: np.ndarray, n_components: int = 5, seed: int = 42) -> tuple[PCA, np.ndarray]:
    pca = PCA(n_components=n_components, random_state=seed)
    scores = pca.fit_transform(X)
    return pca, scores


def run_hierarchical_clustering(X: np.ndarray, method: str = "ward") -> tuple[np.ndarray, np.ndarray]:
    dist = pdist(X, metric="euclidean")
    linkage = hierarchy.linkage(dist, method=method)
    return linkage, squareform(dist)


def spectral_correlation_matrix(X: np.ndarray) -> np.ndarray:
    return np.corrcoef(X)


def condition_trend(X: np.ndarray, conditions: list[str], grid: np.ndarray,
                     target_wavenumber: float, window: float = 10.0) -> pd.DataFrame:
    """Mean +/- SEM band intensity near target_wavenumber, grouped by
    condition -- used to test for a concentration-dependent trend."""
    mask = np.abs(grid - target_wavenumber) <= window
    band_intensity = X[:, mask].max(axis=1)
    df = pd.DataFrame(dict(condition=conditions, band_intensity=band_intensity))
    summary = df.groupby("condition")["band_intensity"].agg(["mean", "std", "count"]).reset_index()
    summary["sem"] = summary["std"] / np.sqrt(summary["count"])
    return summary
