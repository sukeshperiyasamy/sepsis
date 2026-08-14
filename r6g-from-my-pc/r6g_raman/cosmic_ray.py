"""Cosmic-ray spike detection/removal, compared objectively.

Three despiking methods are implemented and scored on the same real
spectrum so the notebook can pick the best one instead of assuming it:

- Modified Z-score on the first derivative (Whitaker & Hayes, 2018,
  "A simple algorithm for despiking Raman spectra", Chemometrics and
  Intelligent Laboratory Systems, 179, 82-89).
- Hampel filter (rolling median + MAD outlier rejection).
- Median filter thresholding (rolling median, flag large deviations).

All flagged points are replaced by linear interpolation from their
non-flagged neighbours (never by a fabricated constant).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.ndimage import median_filter as _median_filter

MAD_SCALE = 0.6745  # converts MAD to a normal-equivalent sigma


def _interpolate_flagged(y: np.ndarray, flagged: np.ndarray) -> np.ndarray:
    y_out = y.copy()
    idx = np.arange(len(y))
    good = ~flagged
    if good.sum() < 2 or not flagged.any():
        return y_out
    y_out[flagged] = np.interp(idx[flagged], idx[good], y[good])
    return y_out


def modified_zscore_despike(y: np.ndarray, threshold: float = 3.5) -> tuple[np.ndarray, np.ndarray]:
    dy = np.diff(y, prepend=y[0])
    median_dy = np.median(dy)
    mad = np.median(np.abs(dy - median_dy))
    if mad == 0:
        mad = 1e-9
    z = MAD_SCALE * (dy - median_dy) / mad
    flagged = np.abs(z) > threshold
    return _interpolate_flagged(y, flagged), flagged


def hampel_filter(y: np.ndarray, window_size: int = 7, n_sigmas: float = 3.5) -> tuple[np.ndarray, np.ndarray]:
    n = len(y)
    k = window_size // 2
    flagged = np.zeros(n, dtype=bool)
    y_med = np.empty(n)
    for i in range(n):
        lo, hi = max(0, i - k), min(n, i + k + 1)
        window = y[lo:hi]
        med = np.median(window)
        mad = np.median(np.abs(window - med))
        sigma = MAD_SCALE * mad if mad > 0 else 1e-9
        y_med[i] = med
        flagged[i] = np.abs(y[i] - med) > n_sigmas * sigma
    return _interpolate_flagged(y, flagged), flagged


def median_filter_despike(y: np.ndarray, kernel_size: int = 5, threshold_sigma: float = 3.5) -> tuple[np.ndarray, np.ndarray]:
    y_med = _median_filter(y, size=kernel_size, mode="nearest")
    resid = y - y_med
    mad = np.median(np.abs(resid - np.median(resid)))
    sigma = MAD_SCALE * mad if mad > 0 else 1e-9
    flagged = np.abs(resid) > threshold_sigma * sigma
    return _interpolate_flagged(y, flagged), flagged


def wavelet_despike(y: np.ndarray, wavelet: str = "db4", level: int = 1,
                     threshold_sigma: float = 3.5) -> tuple[np.ndarray, np.ndarray]:
    """Cosmic rays deposit essentially all their energy in the finest
    (highest-frequency) wavelet detail coefficients; flag pixels whose
    finest-scale detail coefficient magnitude is a robust outlier, then
    reconstruct with those coefficients soft-thresholded to zero."""
    import pywt

    coeffs = pywt.wavedec(y, wavelet, level=level)
    detail = coeffs[-1]
    mad = np.median(np.abs(detail - np.median(detail)))
    sigma = MAD_SCALE * mad if mad > 0 else 1e-9
    flagged_coef = np.abs(detail) > threshold_sigma * sigma
    coeffs[-1] = np.where(flagged_coef, 0.0, detail)
    y_clean = pywt.waverec(coeffs, wavelet)[: len(y)]

    # map flagged detail coefficients back to approximate pixel positions
    scale = len(y) / len(detail)
    flagged = np.zeros(len(y), dtype=bool)
    for idx in np.where(flagged_coef)[0]:
        lo, hi = int(idx * scale), int((idx + 1) * scale) + 1
        flagged[lo:min(hi, len(y))] = True
    return y_clean, flagged


def _spike_narrowness_score(y: np.ndarray, flagged: np.ndarray) -> float:
    """Fraction of flagged points that are isolated (1-2 px wide), the
    physical signature of a cosmic ray hit vs. a real (broader) Raman band."""
    if not flagged.any():
        return 1.0
    labelled = np.cumsum(np.diff(np.r_[0, flagged.astype(int)]) == 1)
    labelled[~flagged] = 0
    if flagged.sum() == 0:
        return 1.0
    widths = pd.Series(labelled[flagged]).value_counts().values
    return float(np.mean(widths <= 2))


def _broad_signal_preservation(y: np.ndarray, y_clean: np.ndarray, heavy_smooth_window: int = 25) -> float:
    """Correlation between despiked spectrum and a heavily smoothed version
    of the ORIGINAL spectrum -- a despiking method that also erodes broad
    Raman bands will diverge from this reference."""
    ref = _median_filter(y, size=heavy_smooth_window, mode="nearest")
    return float(np.corrcoef(ref, y_clean)[0, 1])


def compare_methods(x: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    methods = {
        "modified_zscore": modified_zscore_despike(y),
        "hampel": hampel_filter(y),
        "median_filter": median_filter_despike(y),
        "wavelet": wavelet_despike(y),
    }
    rows = []
    for name, (y_clean, flagged) in methods.items():
        rows.append(dict(
            method=name,
            n_flagged=int(flagged.sum()),
            spike_narrowness_score=_spike_narrowness_score(y, flagged),
            broad_signal_preservation=_broad_signal_preservation(y, y_clean),
        ))
    df = pd.DataFrame(rows)
    df["composite_score"] = df["spike_narrowness_score"] * df["broad_signal_preservation"]
    return df.sort_values("composite_score", ascending=False).reset_index(drop=True)


def despike(y: np.ndarray, method: str) -> np.ndarray:
    fn = {
        "modified_zscore": modified_zscore_despike,
        "hampel": hampel_filter,
        "median_filter": median_filter_despike,
        "wavelet": wavelet_despike,
    }[method]
    y_clean, _ = fn(y)
    return y_clean
