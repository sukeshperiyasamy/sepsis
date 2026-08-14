import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import savgol_filter
import os

file_path = 'sec-10_power-70_i-10.xlsx'
df_raw = pd.read_excel(file_path, header=None)

# From inspection:
# column 2 is Raman Shift, column 3 is Intensity
# Row 0 contains headers (e.g. "Raman Shift", "Dark Subtracted #1")
# Data starts at Row 1
x_data = df_raw.iloc[1:, 2].astype(float).values
y_data = df_raw.iloc[1:, 3].astype(float).values

# Sort the data just in case it's not sorted
sort_idx = np.argsort(x_data)
x_data = x_data[sort_idx]
y_data = y_data[sort_idx]

# Filter 500 to 2000 cm-1
mask = (x_data >= 500) & (x_data <= 2000)
x_filtered = x_data[mask]
y_filtered = y_data[mask]

# ALS baseline correction
def als_baseline(y, lam=1e5, p=0.01, niter=10):
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    D = lam * D.dot(D.transpose())
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + D
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z

baseline = als_baseline(y_filtered)
y_corrected = y_filtered - baseline

# Smoothing (Savitzky-Golay)
# We will smooth the baseline corrected data as requested in similar tasks
# We'll use a slightly larger window if possible to make it smooth but keep peaks
window_length = min(21, len(y_corrected) if len(y_corrected) % 2 != 0 else len(y_corrected) - 1)
if window_length < 3:
    window_length = 3
polyorder = 3
if window_length > polyorder:
    y_smoothed = savgol_filter(y_corrected, window_length, polyorder)
else:
    y_smoothed = y_corrected

# Plot 1: Raw spectra
plt.figure(figsize=(10, 6))
plt.plot(x_filtered, y_filtered, color='blue', linewidth=1.5)
plt.title('Raman Spectra (500 - 2000 cm⁻¹) - Raw\n(10sec-power70-acc10)', fontsize=14, fontweight='bold')
plt.xlabel('Raman Shift (cm⁻¹)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(500, 2000)
plt.tight_layout()
plt.savefig('raw_spectra.png', dpi=300)
plt.close()

# Plot 2: Baseline Corrected
plt.figure(figsize=(10, 6))
plt.plot(x_filtered, y_corrected, color='green', linewidth=1.5)
plt.title('Raman Spectra (500 - 2000 cm⁻¹) - Baseline Corrected\n(10sec-power70-acc10)', fontsize=14, fontweight='bold')
plt.xlabel('Raman Shift (cm⁻¹)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(500, 2000)
plt.tight_layout()
plt.savefig('baseline_corrected.png', dpi=300)
plt.close()

# Plot 3: Smoothed (Baseline Corrected)
plt.figure(figsize=(10, 6))
plt.plot(x_filtered, y_smoothed, color='red', linewidth=1.5)
plt.title('Raman Spectra (500 - 2000 cm⁻¹) - Smoothed\n(10sec-power70-acc10)', fontsize=14, fontweight='bold')
plt.xlabel('Raman Shift (cm⁻¹)', fontsize=12)
plt.ylabel('Intensity (a.u.)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlim(500, 2000)
plt.tight_layout()
plt.savefig('smoothed.png', dpi=300)
plt.close()

print(f"Plots generated successfully! Found {len(x_filtered)} points in range 500-2000.")
