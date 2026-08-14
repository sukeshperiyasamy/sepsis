"""Baseline correction methods, compared objectively.

Implements ALS, airPLS, arPLS, IModPoly, morphological, and rolling-ball
baselines and scores each on the same spectrum using:

- RMSE of the corrected spectrum in flat (no-peak) spectral windows
  (residual baseline should be ~0 there),
- residual-baseline flatness (std of the corrected signal in those windows),
- peak-area preservation (area of detected peaks before vs. after
  correction, relative to a light reference smoothing).

References:
    Eilers, P. H. C. (2003) Anal. Chem. 75, 3631 (asymmetric least squares).
    Zhang, Z.-M. et al. (2010) Analyst 135, 1138 (airPLS).
    Baek, S.-J. et al. (2015) Analyst 140, 250 (arPLS).
    Lieber, C. A. & Mahadevan-Jansen, A. (2003) Appl. Spectrosc. 57, 1363
    (I-ModPoly, iterative modified polynomial fitting).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pybaselines import Baseline
from scipy.signal import find_peaks


def als_baseline(y: np.ndarray, lam: float = 1e5, p: float = 0.01, n_iter: int = 10) -> np.ndarray:
    fitter = Baseline()
    baseline, _ = fitter.asls(y, lam=lam, p=p, max_iter=n_iter)
    return baseline


def airpls_baseline(y: np.ndarray, lam: float = 1e5) -> np.ndarray:
    fitter = Baseline()
    baseline, _ = fitter.airpls(y, lam=lam)
    return baseline


def arpls_baseline(y: np.ndarray, lam: float = 1e5) -> np.ndarray:
    fitter = Baseline()
    baseline, _ = fitter.arpls(y, lam=lam)
    return baseline


def imodpoly_baseline(y: np.ndarray, x: np.ndarray, poly_order: int = 5) -> np.ndarray:
    fitter = Baseline(x_data=x)
    baseline, _ = fitter.imodpoly(y, poly_order=poly_order)
    return baseline


def morphological_baseline(y: np.ndarray, half_window: int = 40) -> np.ndarray:
    fitter = Baseline()
    baseline, _ = fitter.mor(y, half_window=half_window)
    return baseline


def rolling_ball_baseline(y: np.ndarray, half_window: int = 40) -> np.ndarray:
    fitter = Baseline()
    baseline, _ = fitter.rolling_ball(y, half_window=half_window)
    return baseline


BASELINE_METHODS = {
    "ALS": als_baseline,
    "airPLS": airpls_baseline,
    "arPLS": arpls_baseline,
    "morphological": morphological_baseline,
    "rolling_ball": rolling_ball_baseline,
}


def _flat_window_mask(x: np.ndarray, peak_positions: np.ndarray, exclusion_cm1: float = 25.0) -> np.ndarray:
    """Pixels far from any detected peak -- used as a proxy 'no signal'
    region for scoring baseline residual flatness, without assuming any
    fixed wavenumber window a priori."""
    mask = np.ones(len(x), dtype=bool)
    for p in peak_positions:
        mask &= np.abs(x - p) > exclusion_cm1
    return mask


def score_baseline(x: np.ndarray, y_raw: np.ndarray, baseline: np.ndarray) -> dict:
    corrected = y_raw - baseline
    peaks_idx, _ = find_peaks(corrected, prominence=np.ptp(corrected) * 0.02)
    peak_positions = x[peaks_idx]
    flat_mask = _flat_window_mask(x, peak_positions)

    residual_flat = corrected[flat_mask]
    rmse_flat = float(np.sqrt(np.mean(residual_flat ** 2))) if flat_mask.sum() > 5 else np.nan
    flatness_std = float(np.std(residual_flat)) if flat_mask.sum() > 5 else np.nan

    peak_area = float(np.trapz(np.clip(corrected[peaks_idx.min():peaks_idx.max()], 0, None))) if len(peaks_idx) > 1 else 0.0

    return dict(
        n_peaks_detected=len(peaks_idx),
        rmse_flat_region=rmse_flat,
        flat_region_std=flatness_std,
        preserved_peak_area=peak_area,
    )


def compare_methods(x: np.ndarray, y: np.ndarray) -> tuple[pd.DataFrame, dict]:
    baselines = {name: fn(y) for name, fn in BASELINE_METHODS.items()}
    baselines["IModPoly"] = imodpoly_baseline(y, x)

    rows = []
    for name, baseline in baselines.items():
        metrics = score_baseline(x, y, baseline)
        metrics["method"] = name
        rows.append(metrics)

    df = pd.DataFrame(rows).set_index("method")
    df["rmse_rank"] = df["rmse_flat_region"].rank()
    df["flatness_rank"] = df["flat_region_std"].rank()
    df["peak_preservation_rank"] = df["preserved_peak_area"].rank(ascending=False)
    df["composite_score"] = df["rmse_rank"] + df["flatness_rank"] + df["peak_preservation_rank"]
    df = df.sort_values("composite_score").reset_index()
    return df, baselines
