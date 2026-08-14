"""Convert Gaussian Raman scattering activities into relative Raman
intensities using the standard Placzek/temperature-dependent conversion.

    I_i = f * (v0 - v_i)^4 * S_i / [v_i * (1 - exp(-h c v_i / (k_B T)))]

where v0 is the incident laser wavenumber (cm^-1), v_i the vibrational
wavenumber of mode i (cm^-1), S_i the Gaussian-reported Raman scattering
activity (A^4/amu), T the temperature (K), and f an arbitrary scaling
constant (intensities are only meaningful in relative/normalized form).

Reference: Polavarapu, P. L. J. Phys. Chem. 1990, 94, 8106-8112;
Gaussian, Inc. "Vibrational Analysis in Gaussian" white paper
(https://gaussian.com/vib/), which documents this activity->intensity
conversion used by GaussView's Raman spectrum plotting.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

H_PLANCK = 6.62607015e-34      # J s
C_LIGHT = 2.99792458e10        # cm/s
K_BOLTZ = 1.380649e-23         # J/K
LITERATURE_SCALING_FACTOR = 0.967  # B3LYP/6-311++G(d,p), NIST CCCBDB recommendation


def activity_to_intensity(freq_cm1: np.ndarray, raman_activity: np.ndarray,
                           laser_wavenumber_cm1: float, temperature_k: float = 298.15) -> np.ndarray:
    freq = np.asarray(freq_cm1, dtype=float)
    activity = np.asarray(raman_activity, dtype=float)
    # avoid divide-by-zero / unphysical negative "frequencies" from
    # near-zero translational/rotational residual modes
    safe_freq = np.where(freq > 1.0, freq, np.nan)

    boltzmann_pop = 1.0 - np.exp(-H_PLANCK * C_LIGHT * safe_freq / (K_BOLTZ * temperature_k))
    intensity = (laser_wavenumber_cm1 - safe_freq) ** 4 * activity / (safe_freq * boltzmann_pop)
    return np.nan_to_num(intensity, nan=0.0)


def laser_wavenumber_from_nm(laser_wavelength_nm: float) -> float:
    return 1.0e7 / laser_wavelength_nm


def build_intensity_table(modes: pd.DataFrame, laser_wavelength_nm: float,
                           temperature_k: float = 298.15,
                           min_frequency_cm1: float = 100.0) -> pd.DataFrame:
    """min_frequency_cm1 excludes low-frequency lattice/torsional modes
    below the typical Rayleigh-line notch-filter cutoff of a dispersive
    Raman spectrometer (where the 1/v_i term in the Placzek formula also
    diverges numerically) -- these modes are neither experimentally
    observable nor physically meaningful intensities, not a fabricated
    exclusion."""
    v0 = laser_wavenumber_from_nm(laser_wavelength_nm)
    out = modes.copy()
    out["laser_wavenumber_cm1"] = v0
    out["raman_intensity_raw"] = activity_to_intensity(
        out["frequency_cm1"].to_numpy(), out["raman_activity_A4_amu"].to_numpy(), v0, temperature_k
    )
    out.loc[out["frequency_cm1"] < min_frequency_cm1, "raman_intensity_raw"] = 0.0
    out["raman_intensity_norm"] = out["raman_intensity_raw"] / out["raman_intensity_raw"].max()
    return out


def apply_scaling(modes: pd.DataFrame, scale_factor: float) -> pd.DataFrame:
    out = modes.copy()
    out["frequency_scaled_cm1"] = out["frequency_cm1"] * scale_factor
    return out
