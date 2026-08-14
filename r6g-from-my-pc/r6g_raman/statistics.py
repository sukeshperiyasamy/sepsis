"""Statistical validation metrics comparing the experimental and DFT
(broadened, scaled) spectra or matched peak lists.

All metrics are standard textbook definitions (scipy/sklearn where
available); bootstrap confidence intervals use `numpy.random.default_rng`
with a documented fixed seed for reproducibility (a run-configuration
parameter, not a result being hardcoded).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats
from sklearn.metrics import r2_score


def _err(matched: pd.DataFrame) -> np.ndarray:
    return (matched["exp_position_cm1"] - matched["dft_frequency_scaled_cm1"]).to_numpy()


def peak_position_statistics(matched: pd.DataFrame, n_params: int = 1) -> dict:
    """n_params is the number of fitted parameters in the exp~DFT relation
    (1 for the scale factor) used for the adjusted-R^2 degrees-of-freedom
    correction."""
    err = _err(matched)
    exp_pos = matched["exp_position_cm1"].to_numpy()
    dft_pos = matched["dft_frequency_scaled_cm1"].to_numpy()
    n = len(exp_pos)
    r, p_value = sstats.pearsonr(exp_pos, dft_pos)
    rho, rho_p = sstats.spearmanr(exp_pos, dft_pos)
    tau, tau_p = sstats.kendalltau(exp_pos, dft_pos)
    r2 = r2_score(exp_pos, dft_pos)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - n_params - 1) if n > n_params + 1 else np.nan
    return dict(
        n_matched_peaks=n,
        mae_cm1=float(np.mean(np.abs(err))),
        rmse_cm1=float(np.sqrt(np.mean(err ** 2))),
        mean_signed_error_cm1=float(np.mean(err)),
        median_error_cm1=float(np.median(err)),
        max_abs_error_cm1=float(np.max(np.abs(err))),
        pearson_r=float(r),
        pearson_p_value=float(p_value),
        spearman_rho=float(rho),
        spearman_p_value=float(rho_p),
        kendall_tau=float(tau),
        kendall_p_value=float(tau_p),
        r_squared=float(r2),
        adjusted_r_squared=float(adj_r2),
    )


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def spectral_angle_mapper(a: np.ndarray, b: np.ndarray) -> float:
    cos_theta = np.clip(cosine_similarity(a, b), -1.0, 1.0)
    return float(np.arccos(cos_theta))


def cross_correlation_lag(a: np.ndarray, b: np.ndarray, dx: float) -> dict:
    a0 = a - np.mean(a)
    b0 = b - np.mean(b)
    corr = np.correlate(a0, b0, mode="full")
    lags = np.arange(-len(b0) + 1, len(a0))
    best = np.argmax(corr)
    normalized_peak = corr[best] / (np.linalg.norm(a0) * np.linalg.norm(b0))
    return dict(best_lag_points=int(lags[best]), best_lag_cm1=float(lags[best] * dx),
                normalized_peak_correlation=float(normalized_peak))


def dtw_distance(a: np.ndarray, b: np.ndarray, max_points: int = 400) -> float:
    """Simple O(n*m) dynamic time warping distance (optional diagnostic).
    Both series are downsampled to <= max_points for tractability."""
    def downsample(v):
        if len(v) <= max_points:
            return v
        idx = np.linspace(0, len(v) - 1, max_points).astype(int)
        return v[idx]

    a_ds, b_ds = downsample(a), downsample(b)
    n, m = len(a_ds), len(b_ds)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(a_ds[i - 1] - b_ds[j - 1])
            D[i, j] = cost + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    return float(D[n, m])


def _as_probability(v: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    v = np.clip(v, 0, None) + eps
    return v / v.sum()


def earth_movers_distance(a: np.ndarray, b: np.ndarray, x: np.ndarray) -> float:
    """1D Earth Mover's (Wasserstein-1) distance between two spectra
    treated as distributions over the shared wavenumber axis x."""
    pa, pb = _as_probability(a), _as_probability(b)
    return float(sstats.wasserstein_distance(x, x, u_weights=pa, v_weights=pb))


def jensen_shannon_distance(a: np.ndarray, b: np.ndarray) -> float:
    from scipy.spatial.distance import jensenshannon
    pa, pb = _as_probability(a), _as_probability(b)
    return float(jensenshannon(pa, pb, base=2))


def spectral_information_divergence(a: np.ndarray, b: np.ndarray) -> float:
    """Chang, C.-I. (2000) IEEE Trans. Geosci. Remote Sens. 38, 1927 --
    symmetric KL-divergence-based measure of spectral shape dissimilarity,
    commonly used alongside SAM for hyperspectral/spectral matching."""
    pa, pb = _as_probability(a), _as_probability(b)
    d_ab = np.sum(pa * np.log(pa / pb))
    d_ba = np.sum(pb * np.log(pb / pa))
    return float(d_ab + d_ba)


def residual_normality_test(matched: pd.DataFrame) -> dict:
    """Shapiro-Wilk test for normality of the matched-peak residuals --
    the standard assumption behind reporting a mean +/- std error bar."""
    err = _err(matched)
    stat, p_value = sstats.shapiro(err)
    return dict(shapiro_statistic=float(stat), shapiro_p_value=float(p_value),
                residuals_normal_at_0p05=bool(p_value > 0.05))


def residual_autocorrelation(matched: pd.DataFrame) -> dict:
    """Durbin-Watson statistic (~2 = no autocorrelation, <2 = positive
    autocorrelation) and the lag-1 autocorrelation function value for the
    matched-peak residuals, ordered by experimental frequency -- tests
    whether errors are systematic (frequency-dependent) rather than random."""
    from statsmodels.stats.stattools import durbin_watson
    from statsmodels.tsa.stattools import acf

    ordered = matched.sort_values("exp_position_cm1")
    err = _err(ordered)
    dw = durbin_watson(err)
    acf_vals = acf(err, nlags=min(5, len(err) - 2), fft=False)
    return dict(durbin_watson=float(dw), acf_lag1=float(acf_vals[1]) if len(acf_vals) > 1 else np.nan,
                acf_values=acf_vals.tolist())


def bootstrap_ci(matched: pd.DataFrame, statistic: str = "rmse_cm1",
                  n_boot: int = 2000, seed: int = 42, ci: float = 0.95) -> dict:
    rng = np.random.default_rng(seed)
    err = _err(matched)
    n = len(err)
    boot_vals = np.empty(n_boot)
    for i in range(n_boot):
        sample = rng.choice(err, size=n, replace=True)
        if statistic == "rmse_cm1":
            boot_vals[i] = np.sqrt(np.mean(sample ** 2))
        elif statistic == "mae_cm1":
            boot_vals[i] = np.mean(np.abs(sample))
        elif statistic == "mean_signed_error_cm1":
            boot_vals[i] = np.mean(sample)
        else:
            raise ValueError(f"Unknown statistic: {statistic}")
    alpha = 1 - ci
    lo, hi = np.percentile(boot_vals, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return dict(statistic=statistic, point_estimate=float(np.mean(boot_vals)),
                ci_low=float(lo), ci_high=float(hi), n_boot=n_boot, seed=seed)
