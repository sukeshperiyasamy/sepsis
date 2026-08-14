"""Smoothing/denoising methods, compared objectively.

Savitzky-Golay, Gaussian, wavelet (discrete wavelet shrinkage), and moving
average are scored on: (1) noise reduction (std of high-frequency residual
after subtracting a heavy reference smooth) and (2) peak distortion/shift
(change in detected peak height and position vs. the unsmoothed spectrum).

References:
    Savitzky, A. & Golay, M. J. E. (1964) Anal. Chem. 36, 1627.
    Donoho, D. L. (1995) IEEE Trans. Inf. Theory 41, 613 (wavelet shrinkage).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pywt
from scipy.ndimage import gaussian_filter1d, uniform_filter1d, median_filter
from scipy.signal import savgol_filter, find_peaks


def savgol_smooth(y: np.ndarray, window_length: int = 11, polyorder: int = 3) -> np.ndarray:
    return savgol_filter(y, window_length=window_length, polyorder=polyorder)


def gaussian_smooth(y: np.ndarray, sigma: float = 2.0) -> np.ndarray:
    return gaussian_filter1d(y, sigma=sigma)


def moving_average_smooth(y: np.ndarray, window: int = 9) -> np.ndarray:
    return uniform_filter1d(y, size=window)


def median_smooth(y: np.ndarray, kernel_size: int = 7) -> np.ndarray:
    return median_filter(y, size=kernel_size, mode="nearest")


def wavelet_smooth(y: np.ndarray, wavelet: str = "db4", level: int = 3) -> np.ndarray:
    coeffs = pywt.wavedec(y, wavelet, level=level)
    detail = coeffs[-1]
    sigma = np.median(np.abs(detail - np.median(detail))) / 0.6745
    uthresh = sigma * np.sqrt(2 * np.log(len(y)))
    denoised = [coeffs[0]] + [pywt.threshold(c, uthresh, mode="soft") for c in coeffs[1:]]
    y_rec = pywt.waverec(denoised, wavelet)
    return y_rec[: len(y)]


SMOOTHING_METHODS = {
    "Savitzky-Golay": savgol_smooth,
    "Gaussian": gaussian_smooth,
    "Wavelet": wavelet_smooth,
    "Median": median_smooth,
    "Moving average": moving_average_smooth,
}


def score_smoothing(x: np.ndarray, y_raw: np.ndarray, y_smooth: np.ndarray,
                     match_window_cm1: float = 10.0) -> dict:
    heavy_ref = gaussian_filter1d(y_raw, sigma=8.0)
    noise_before = float(np.std(y_raw - heavy_ref))
    noise_after = float(np.std(y_smooth - heavy_ref))
    noise_reduction_pct = 100.0 * (1 - noise_after / noise_before) if noise_before > 0 else np.nan

    prom = np.ptp(y_raw) * 0.02
    peaks_raw, _ = find_peaks(y_raw, prominence=prom)
    peaks_smooth, _ = find_peaks(y_smooth, prominence=prom)

    # nearest-neighbour match each smoothed peak to a raw peak within a
    # physically small window, rather than pairing by array index (which
    # breaks whenever the two methods find different numbers of peaks).
    shifts, height_changes = [], []
    if len(peaks_raw) > 0 and len(peaks_smooth) > 0:
        x_raw_peaks = x[peaks_raw]
        for i_s in peaks_smooth:
            j = int(np.argmin(np.abs(x_raw_peaks - x[i_s])))
            i_r = peaks_raw[j]
            d = abs(x[i_s] - x[i_r])
            if d <= match_window_cm1:
                shifts.append(d)
                height_changes.append(100 * abs(y_raw[i_r] - y_smooth[i_s]) / max(abs(y_raw[i_r]), 1e-9))

    shift = float(np.mean(shifts)) if shifts else np.nan
    height_change_pct = float(np.mean(height_changes)) if height_changes else np.nan

    return dict(
        noise_reduction_pct=noise_reduction_pct,
        n_peaks_raw=len(peaks_raw),
        n_peaks_after=len(peaks_smooth),
        mean_peak_shift_cm1=shift,
        mean_peak_height_change_pct=height_change_pct,
    )


def compare_methods(x: np.ndarray, y: np.ndarray) -> tuple[pd.DataFrame, dict]:
    smoothed = {name: fn(y) for name, fn in SMOOTHING_METHODS.items()}
    rows = []
    for name, y_s in smoothed.items():
        metrics = score_smoothing(x, y, y_s)
        metrics["method"] = name
        rows.append(metrics)
    df = pd.DataFrame(rows).set_index("method")
    df["distortion_rank"] = (df["mean_peak_shift_cm1"].rank() + df["mean_peak_height_change_pct"].rank())
    df["noise_rank"] = df["noise_reduction_pct"].rank(ascending=False)
    df["composite_score"] = df["distortion_rank"] + df["noise_rank"]
    df = df.sort_values("composite_score").reset_index()
    return df, smoothed
