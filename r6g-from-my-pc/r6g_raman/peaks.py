"""Peak detection and characterization for the processed experimental
spectrum.

Position/height/prominence from scipy.signal.find_peaks; FWHM from
scipy.signal.peak_widths at 50% relative height; area by trapezoidal
integration between the peak's half-max bounds; SNR as peak height over
the local noise std (robust MAD-based) in a nearby peak-free window;
position uncertainty estimated from the local spectral sampling step and
the peak's curvature (Cramer-Rao-like estimate: sigma_x ~ resolution / SNR).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import find_peaks, peak_widths, peak_prominences


def detect_peaks(x: np.ndarray, y: np.ndarray, prominence_frac: float = 0.01,
                  distance_cm1: float = 8.0, min_height: float = 0.0) -> pd.DataFrame:
    """min_height defaults to 0: a genuine Raman band must sit above the
    (already baseline-corrected) zero line -- small local maxima inside a
    baseline-overshoot undershoot region are not physical peaks."""
    step = float(np.mean(np.abs(np.diff(x))))
    distance_pts = max(1, int(round(distance_cm1 / step)))
    prominence = np.ptp(y) * prominence_frac

    idx, props = find_peaks(y, prominence=prominence, distance=distance_pts, height=min_height)
    widths, width_heights, left_ips, right_ips = peak_widths(y, idx, rel_height=0.5)
    proms, left_bases, right_bases = peak_prominences(y, idx)

    noise_mad = np.median(np.abs(np.diff(y))) / 0.6745
    noise_mad = max(noise_mad, 1e-9)

    rows = []
    for k, i in enumerate(idx):
        left_i, right_i = int(np.floor(left_ips[k])), int(np.ceil(right_ips[k]))
        left_i, right_i = max(left_i, 0), min(right_i, len(x) - 1)
        area = float(np.trapz(np.clip(y[left_i:right_i + 1] - width_heights[k], 0, None),
                               x[left_i:right_i + 1])) if right_i > left_i else np.nan
        fwhm_cm1 = float(widths[k] * step)
        height = float(y[i])
        snr = height / noise_mad
        pos_uncertainty = step / max(snr, 1e-6)
        rows.append(dict(
            peak_index=int(i),
            position_cm1=float(x[i]),
            position_uncertainty_cm1=pos_uncertainty,
            intensity=height,
            prominence=float(proms[k]),
            fwhm_cm1=fwhm_cm1,
            area=area,
            snr=snr,
        ))
    return pd.DataFrame(rows).sort_values("position_cm1").reset_index(drop=True)
