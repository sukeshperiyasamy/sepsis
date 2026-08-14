"""Full-dataset (all 97 raw spectra) replicate and condition statistics.

Every raw spectrum is dark-subtracted and interpolated onto one common
wavenumber grid (derived from the finest-sampled file) so that files
acquired on different days can be combined even if the calibration
polynomial shifted by a sub-pixel amount. Mean, median, sample standard
deviation, 95% confidence interval (normal approximation,
t-distribution for small n), and coefficient of variation are computed
per-pixel, both pooled across all 97 spectra and per condition.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

from . import io_raw


def common_grid(specs: list, n_points: int | None = None) -> np.ndarray:
    lo = max(s.data["Raman Shift"].min() for s in specs)
    hi = min(s.data["Raman Shift"].max() for s in specs)
    n_points = n_points or max(len(s.data) for s in specs)
    return np.linspace(lo, hi, n_points)


def interpolated_matrix(specs: list, grid: np.ndarray) -> np.ndarray:
    mat = np.empty((len(specs), len(grid)))
    for k, s in enumerate(specs):
        x = s.data["Raman Shift"].to_numpy()
        y = io_raw.dark_subtract(s)
        mat[k, :] = np.interp(grid, x, y)
    return mat


def replicate_statistics(mat: np.ndarray, ci: float = 0.95) -> pd.DataFrame:
    n = mat.shape[0]
    mean = mat.mean(axis=0)
    median = np.median(mat, axis=0)
    std = mat.std(axis=0, ddof=1)
    sem = std / np.sqrt(n)
    tcrit = sstats.t.ppf(0.5 + ci / 2, df=n - 1)
    ci_low = mean - tcrit * sem
    ci_high = mean + tcrit * sem
    cv = np.divide(std, np.abs(mean), out=np.full_like(std, np.nan), where=np.abs(mean) > 1e-9)
    return pd.DataFrame(dict(
        mean=mean, median=median, std=std, sem=sem,
        ci_low=ci_low, ci_high=ci_high, cv=cv,
    ))


def condition_summary(all_specs: list) -> pd.DataFrame:
    grid = common_grid(all_specs)
    rows = []
    for condition in sorted(set(s.condition for s in all_specs)):
        cond_specs = [s for s in all_specs if s.condition == condition]
        mat = interpolated_matrix(cond_specs, grid)
        stat = replicate_statistics(mat)
        rows.append(dict(
            condition=condition, n_replicates=len(cond_specs),
            mean_intensity=float(stat["mean"].mean()),
            mean_cv=float(np.nanmean(stat["cv"])),
            max_intensity=float(mat.max()),
        ))
    return pd.DataFrame(rows)
