"""Convert a DFT stick spectrum (frequency, intensity) into a continuous
line-shape spectrum via Gaussian, Lorentzian, Voigt, or pseudo-Voigt
broadening, with FWHM (and Voigt sigma/gamma, pseudo-Voigt eta) grid
search optimized against the processed experimental spectrum using
multiple criteria (RMSE, cosine similarity, cross-correlation, AIC, BIC)
so the "optimum" is not just a single-metric artifact.

    Gaussian(v; v0, FWHM)     = exp(-4 ln2 (v-v0)^2 / FWHM^2)
    Lorentzian(v; v0, FWHM)   = (FWHM/2)^2 / [(v-v0)^2 + (FWHM/2)^2]
    Voigt                     = Gaussian (*) Lorentzian convolution
                                (scipy.special.voigt_profile)
    pseudo-Voigt(v; v0,FWHM,eta) = eta*Lorentzian + (1-eta)*Gaussian
                                (same FWHM for both terms -- distinct,
                                cheaper approximation to the true Voigt
                                convolution, common in spectral fitting)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import voigt_profile
from scipy.interpolate import interp1d


def gaussian_profile(v: np.ndarray, v0: float, fwhm: float) -> np.ndarray:
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    return np.exp(-0.5 * ((v - v0) / sigma) ** 2)


def lorentzian_profile(v: np.ndarray, v0: float, fwhm: float) -> np.ndarray:
    gamma = fwhm / 2
    return gamma ** 2 / ((v - v0) ** 2 + gamma ** 2)


def voigt_profile_norm(v: np.ndarray, v0: float, sigma: float, gamma: float) -> np.ndarray:
    peak = voigt_profile(0.0, sigma, gamma)
    return voigt_profile(v - v0, sigma, gamma) / peak


def pseudo_voigt_profile(v: np.ndarray, v0: float, fwhm: float, eta: float) -> np.ndarray:
    return eta * lorentzian_profile(v, v0, fwhm) + (1 - eta) * gaussian_profile(v, v0, fwhm)


def build_stick_spectrum(freqs: np.ndarray, intensities: np.ndarray,
                          grid: np.ndarray, shape: str = "gaussian",
                          fwhm: float = 10.0, sigma: float | None = None,
                          gamma: float | None = None, eta: float = 0.5) -> np.ndarray:
    spectrum = np.zeros_like(grid, dtype=float)
    for v0, inten in zip(freqs, intensities):
        if inten <= 0:
            continue
        if shape == "gaussian":
            spectrum += inten * gaussian_profile(grid, v0, fwhm)
        elif shape == "lorentzian":
            spectrum += inten * lorentzian_profile(grid, v0, fwhm)
        elif shape == "voigt":
            spectrum += inten * voigt_profile_norm(grid, v0, sigma, gamma)
        elif shape == "pseudo_voigt":
            spectrum += inten * pseudo_voigt_profile(grid, v0, fwhm, eta)
        else:
            raise ValueError(f"Unknown line shape: {shape}")
    return spectrum


def _resample_exp_to_grid(exp_x: np.ndarray, exp_y: np.ndarray, grid: np.ndarray) -> np.ndarray:
    f = interp1d(exp_x, exp_y, bounds_error=False, fill_value=0.0)
    return f(grid)


def _score_fit(sim_norm: np.ndarray, exp_norm: np.ndarray, n_params: int) -> dict:
    n = len(exp_norm)
    resid = sim_norm - exp_norm
    rss = float(np.sum(resid ** 2))
    rmse = float(np.sqrt(rss / n))
    cos_sim = float(np.dot(sim_norm, exp_norm) / (np.linalg.norm(sim_norm) * np.linalg.norm(exp_norm)))
    corr = float(np.corrcoef(sim_norm, exp_norm)[0, 1])
    rss_safe = max(rss, 1e-12)
    aic = n * np.log(rss_safe / n) + 2 * n_params
    bic = n * np.log(rss_safe / n) + n_params * np.log(n)
    return dict(rmse=rmse, cosine_similarity=cos_sim, correlation=corr, aic=float(aic), bic=float(bic))


def optimize_fwhm(freqs: np.ndarray, intensities: np.ndarray, grid: np.ndarray,
                   exp_x: np.ndarray, exp_y: np.ndarray, shape: str = "gaussian",
                   fwhm_range: tuple[float, float] = (1.0, 60.0), n_steps: int = 60) -> pd.DataFrame:
    exp_on_grid = _resample_exp_to_grid(exp_x, exp_y, grid)
    exp_norm = exp_on_grid / (np.max(exp_on_grid) if np.max(exp_on_grid) > 0 else 1.0)

    fwhms = np.linspace(fwhm_range[0], fwhm_range[1], n_steps)
    rows = []
    for fwhm in fwhms:
        sim = build_stick_spectrum(freqs, intensities, grid, shape=shape, fwhm=fwhm)
        sim_norm = sim / (np.max(sim) if np.max(sim) > 0 else 1.0)
        row = dict(fwhm_cm1=float(fwhm))
        row.update(_score_fit(sim_norm, exp_norm, n_params=1))
        rows.append(row)
    return pd.DataFrame(rows)


def optimize_voigt(freqs: np.ndarray, intensities: np.ndarray, grid: np.ndarray,
                    exp_x: np.ndarray, exp_y: np.ndarray,
                    sigma_range: tuple[float, float] = (1.0, 15.0),
                    gamma_range: tuple[float, float] = (1.0, 15.0),
                    n_steps: int = 12) -> pd.DataFrame:
    exp_on_grid = _resample_exp_to_grid(exp_x, exp_y, grid)
    exp_norm = exp_on_grid / (np.max(exp_on_grid) if np.max(exp_on_grid) > 0 else 1.0)

    sigmas = np.linspace(*sigma_range, n_steps)
    gammas = np.linspace(*gamma_range, n_steps)
    rows = []
    for sigma in sigmas:
        for gamma in gammas:
            sim = build_stick_spectrum(freqs, intensities, grid, shape="voigt", sigma=sigma, gamma=gamma)
            sim_norm = sim / (np.max(sim) if np.max(sim) > 0 else 1.0)
            row = dict(sigma=float(sigma), gamma=float(gamma))
            row.update(_score_fit(sim_norm, exp_norm, n_params=2))
            rows.append(row)
    return pd.DataFrame(rows)


def optimize_pseudo_voigt(freqs: np.ndarray, intensities: np.ndarray, grid: np.ndarray,
                           exp_x: np.ndarray, exp_y: np.ndarray,
                           fwhm_range: tuple[float, float] = (1.0, 40.0),
                           eta_range: tuple[float, float] = (0.0, 1.0),
                           n_steps: int = 15) -> pd.DataFrame:
    exp_on_grid = _resample_exp_to_grid(exp_x, exp_y, grid)
    exp_norm = exp_on_grid / (np.max(exp_on_grid) if np.max(exp_on_grid) > 0 else 1.0)

    fwhms = np.linspace(*fwhm_range, n_steps)
    etas = np.linspace(*eta_range, n_steps)
    rows = []
    for fwhm in fwhms:
        for eta in etas:
            sim = build_stick_spectrum(freqs, intensities, grid, shape="pseudo_voigt", fwhm=fwhm, eta=eta)
            sim_norm = sim / (np.max(sim) if np.max(sim) > 0 else 1.0)
            row = dict(fwhm_cm1=float(fwhm), eta=float(eta))
            row.update(_score_fit(sim_norm, exp_norm, n_params=2))
            rows.append(row)
    return pd.DataFrame(rows)


def compare_line_shapes(freqs: np.ndarray, intensities: np.ndarray, grid: np.ndarray,
                         exp_x: np.ndarray, exp_y: np.ndarray) -> pd.DataFrame:
    """Best-of-grid summary for every line shape, all scored by the same
    RMSE/cosine/correlation/AIC/BIC criteria for a fair comparison."""
    gauss = optimize_fwhm(freqs, intensities, grid, exp_x, exp_y, shape="gaussian")
    lorentz = optimize_fwhm(freqs, intensities, grid, exp_x, exp_y, shape="lorentzian")
    voigt = optimize_voigt(freqs, intensities, grid, exp_x, exp_y, n_steps=10)
    pv = optimize_pseudo_voigt(freqs, intensities, grid, exp_x, exp_y, n_steps=10)

    rows = []
    for name, scan, param_cols in [
        ("Gaussian", gauss, ["fwhm_cm1"]),
        ("Lorentzian", lorentz, ["fwhm_cm1"]),
        ("Voigt", voigt, ["sigma", "gamma"]),
        ("PseudoVoigt", pv, ["fwhm_cm1", "eta"]),
    ]:
        best = scan.loc[scan["rmse"].idxmin()]
        row = dict(shape=name, **{c: best[c] for c in param_cols})
        row.update(rmse=best["rmse"], cosine_similarity=best["cosine_similarity"],
                   correlation=best["correlation"], aic=best["aic"], bic=best["bic"])
        rows.append(row)
    return pd.DataFrame(rows).sort_values("aic").reset_index(drop=True)
