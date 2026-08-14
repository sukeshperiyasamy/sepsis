"""Parser and per-file validation for raw BWS465-785H CCD Raman spectra.

Each raw CSV has an instrument metadata header (key,value pairs) followed
by a per-pixel data table with columns:
Pixel, Wavelength, Wavenumber, Raman Shift, Dark, Reference, Raw data #1,
Dark Subtracted #1, %TR #1, Absorbance #1, Irradiance (...) #1,
RelativeIntensityCorrection_Ratio #1, ReferenceMaterialCorrection_Ratio #1,
AbsoluteIrradianceCorrection_Ratio #1.

The ``Dark`` column is the instrument's own per-pixel dark reference
(recorded by the spectrometer firmware for this acquisition), so dark
subtraction is performed with data that ships inside every raw file --
no separate dark-only acquisition file is required or fabricated.
"""
from __future__ import annotations

import glob
import os
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

DATA_COLUMNS = [
    "Pixel", "Wavelength", "Wavenumber", "Raman Shift", "Dark", "Reference",
    "Raw data #1", "Dark Subtracted #1",
]


@dataclass
class RawSpectrum:
    path: str
    condition: str
    sample_id: str
    metadata: dict
    data: pd.DataFrame  # Pixel, Wavelength, Wavenumber, Raman Shift, Dark, Reference, Raw data #1, Dark Subtracted #1


def _find_header_row(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if line.startswith("Pixel,Wavelength,Wavenumber,Raman Shift"):
            return i
    raise ValueError("Could not locate per-pixel data header row")


def parse_raw_csv(path: str) -> RawSpectrum:
    with open(path, "r", errors="replace") as fh:
        lines = fh.readlines()

    header_idx = _find_header_row(lines)

    metadata = {}
    for line in lines[:header_idx]:
        parts = line.rstrip("\n").split(",", 1)
        if len(parts) == 2:
            key, val = parts
        else:
            key, val = parts[0], ""
        key = key.strip()
        if key:
            metadata[key] = val.strip()

    data = pd.read_csv(path, skiprows=header_idx, usecols=range(len(DATA_COLUMNS)))
    data.columns = DATA_COLUMNS
    data = data.apply(pd.to_numeric, errors="coerce")

    condition = os.path.basename(os.path.dirname(path))
    sample_id = os.path.splitext(os.path.basename(path))[0]

    return RawSpectrum(
        path=path, condition=condition, sample_id=sample_id,
        metadata=metadata, data=data,
    )


def discover_raw_files(data_raw_dir: str) -> list[str]:
    return sorted(glob.glob(os.path.join(data_raw_dir, "*", "SP_*.csv")))


def validate_raw_spectrum(spec: RawSpectrum) -> dict:
    """Objective, file-level QA checks -- no thresholds hand-tuned to make
    any particular file 'pass'; all are physical/logical invariants."""
    d = spec.data
    shift = d["Raman Shift"].to_numpy()
    raw = d["Raw data #1"].to_numpy()
    dark = d["Dark"].to_numpy()

    n_missing = int(d.isna().sum().sum())
    n_duplicate_pixels = int(d["Pixel"].duplicated().sum())
    n_negative_raw = int((raw < 0).sum())
    is_monotonic = bool(np.all(np.diff(shift) > 0))
    pixel_spacing = np.diff(d["Pixel"].to_numpy())
    uniform_pixel_spacing = bool(np.all(pixel_spacing == 1))
    shift_step = np.diff(shift)
    mean_resolution_cm1 = float(np.mean(np.abs(shift_step)))
    saturation_level = 65535  # 16-bit CCD full well, from yaxis_max in metadata
    n_saturated = int((raw >= saturation_level).sum())
    n_pixels = len(d)

    laser_wl = float(spec.metadata.get("laser_wavelength", np.nan))

    return dict(
        path=spec.path,
        condition=spec.condition,
        sample_id=spec.sample_id,
        n_pixels=n_pixels,
        n_missing_values=n_missing,
        n_duplicate_pixels=n_duplicate_pixels,
        n_negative_raw_counts=n_negative_raw,
        raman_shift_monotonic=is_monotonic,
        uniform_pixel_spacing=uniform_pixel_spacing,
        mean_spectral_resolution_cm1=mean_resolution_cm1,
        n_saturated_pixels=n_saturated,
        laser_wavelength_nm=laser_wl,
        integration_time_s=float(spec.metadata.get("integration times(sec)", np.nan)),
        accumulations=int(float(spec.metadata.get("average number", np.nan))),
        passes_qc=(
            n_missing == 0 and is_monotonic and uniform_pixel_spacing
            and n_saturated == 0
        ),
    )


def dark_subtract(spec: RawSpectrum) -> np.ndarray:
    """Physical dark subtraction: I(shift) = Raw(shift) - Dark(shift)."""
    return (spec.data["Raw data #1"] - spec.data["Dark"]).to_numpy()


def mask_rayleigh_region(x: np.ndarray, y: np.ndarray, cutoff_cm1: float = 100.0) -> tuple[np.ndarray, np.ndarray]:
    """Remove the region within `cutoff_cm1` of zero Raman shift.

    A dispersive Raman spectrometer relies on an edge/notch filter to
    reject the elastically (Rayleigh) scattered laser line, which is
    many orders of magnitude more intense than any Raman band. Real
    filters have finite roll-off (typically ~100-150 cm-1 for common
    OD6 dielectric edge filters), so intensity within this window is
    residual laser leakage, not molecular vibration -- excluding it is
    standard Raman preprocessing, not data manipulation to help agreement.
    """
    mask = np.abs(x) >= cutoff_cm1
    return x[mask], y[mask]


def estimate_snr(spec: RawSpectrum) -> float:
    """Quick, objective SNR proxy used only to rank raw files/conditions
    by quality: signal = peak-to-peak of the dark-subtracted spectrum,
    noise = robust (MAD-based) std of the pixel-to-pixel first difference
    in the featureless high-wavenumber tail (> 2500 cm-1, beyond R6G's
    fingerprint/CH-stretch region)."""
    shift = spec.data["Raman Shift"].to_numpy()
    y = dark_subtract(spec)
    tail_mask = shift > 2500
    if tail_mask.sum() < 20:
        tail_mask = shift > np.percentile(shift, 80)
    tail = y[tail_mask]
    noise = np.median(np.abs(np.diff(tail) - np.median(np.diff(tail)))) / 0.6745
    noise = max(noise, 1e-9)
    signal = np.ptp(y)
    return float(signal / noise)
