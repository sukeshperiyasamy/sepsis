"""Peak fitting (as opposed to plain detection) for major Raman bands
using lmfit, with Gaussian, Lorentzian, pseudo-Voigt, and Voigt line-shape
models compared per band and the best model (by reduced chi-square)
kept.

For every fitted band: position, height, area, FWHM (all with parameter
standard errors from the least-squares covariance matrix), and a
goodness-of-fit summary (reduced chi-square, R^2).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from lmfit.models import GaussianModel, LorentzianModel, PseudoVoigtModel, VoigtModel

MODELS = {
    "Gaussian": GaussianModel,
    "Lorentzian": LorentzianModel,
    "PseudoVoigt": PseudoVoigtModel,
    "Voigt": VoigtModel,
}


def _r_squared(y: np.ndarray, y_fit: np.ndarray) -> float:
    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else np.nan


def fit_single_peak(x: np.ndarray, y: np.ndarray, center_guess: float,
                     window_cm1: float = 20.0) -> dict | None:
    mask = np.abs(x - center_guess) <= window_cm1
    if mask.sum() < 6:
        return None
    xw, yw = x[mask], y[mask]
    if yw.max() <= 0:
        return None

    best = None
    for shape, ModelCls in MODELS.items():
        model = ModelCls()
        params = model.guess(yw, x=xw)
        try:
            result = model.fit(yw, params, x=xw, nan_policy="omit")
        except Exception:
            continue
        if not result.success:
            continue
        redchi = result.redchi if np.isfinite(result.redchi) else np.inf
        if best is None or redchi < best["_redchi"]:
            p = result.params
            fwhm = p["fwhm"].value if "fwhm" in p else np.nan
            fwhm_err = p["fwhm"].stderr if "fwhm" in p and p["fwhm"].stderr else np.nan
            center = p["center"].value
            center_err = p["center"].stderr if p["center"].stderr else np.nan
            amplitude = p["amplitude"].value
            amplitude_err = p["amplitude"].stderr if p["amplitude"].stderr else np.nan
            height = result.eval(x=np.array([center]))[0]
            best = dict(
                shape=shape, position_cm1=center, position_stderr_cm1=center_err,
                height=height, area=amplitude, area_stderr=amplitude_err,
                fwhm_cm1=fwhm, fwhm_stderr_cm1=fwhm_err,
                reduced_chi_square=redchi, r_squared=_r_squared(yw, result.best_fit),
                n_points=int(mask.sum()), _redchi=redchi,
            )
    if best is not None:
        del best["_redchi"]
    return best


def fit_peak_table(x: np.ndarray, y: np.ndarray, peak_positions: np.ndarray,
                    window_cm1: float = 20.0) -> pd.DataFrame:
    rows = []
    for p0 in peak_positions:
        fit = fit_single_peak(x, y, p0, window_cm1=window_cm1)
        if fit is not None:
            fit["seed_position_cm1"] = float(p0)
            rows.append(fit)
    return pd.DataFrame(rows).sort_values("position_cm1").reset_index(drop=True)
