import glob
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.signal import find_peaks, savgol_filter
from scipy.sparse.linalg import spsolve


# Notebook-friendly config
ROOT_DIR = r"C:\Users\sukes\Downloads\LTA"
FILE_PATTERN = os.path.join(ROOT_DIR, "**", "sec-*.xlsx")


def baseline_als(y, lam=1e5, p=0.01, niter=10):
    """Asymmetric least-squares baseline correction."""
    length = len(y)
    d = sparse.diags([1, -2, 1], [0, -1, -2], shape=(length, length - 2))
    w = np.ones(length)

    for _ in range(niter):
        w_mat = sparse.spdiags(w, 0, length, length)
        z = w_mat + lam * d.dot(d.T)
        baseline = spsolve(z, w * y)
        w = p * (y > baseline) + (1 - p) * (y < baseline)

    return baseline


def smooth_signal(y, preferred_window=11, polyorder=3):
    """Use a valid odd Savitzky-Golay window for the current signal length."""
    window = min(preferred_window, len(y) if len(y) % 2 == 1 else len(y) - 1)
    min_window = polyorder + 2 if (polyorder + 2) % 2 == 1 else polyorder + 3
    window = max(window, min_window)

    if window >= len(y):
        window = len(y) - 1 if len(y) % 2 == 0 else len(y)
    if window < polyorder + 2:
        return y

    return savgol_filter(y, window, polyorder)


def parse_metadata(df):
    metadata = {}
    for row_idx in range(3):
        key = df.iloc[row_idx, 0]
        value = df.iloc[row_idx, 1]
        metadata[str(key)] = value
    return metadata


def load_dataset(path):
    df = pd.read_excel(path, header=None)
    metadata = parse_metadata(df)

    x = pd.to_numeric(df.iloc[1:, 2], errors="coerce").to_numpy()
    y = pd.to_numeric(df.iloc[1:, 3], errors="coerce").to_numpy()

    valid = np.isfinite(x) & np.isfinite(y)
    x = x[valid]
    y = y[valid]

    # Filter out Rayleigh peak and high-frequency noise
    mask = (x >= 400) & (x <= 1500)
    x = x[mask]
    y = y[mask]

    return {
        "name": os.path.basename(path),
        "path": path,
        "metadata": metadata,
        "x": x,
        "y": y,
    }


def build_peak_table(processed_data):
    rows = []

    for item in processed_data:
        x = item["x"]
        y = item["y_smooth"]
        peak_threshold = np.max(y) * 0.1
        prominence = max(np.max(y) * 0.05, 1)

        peaks, props = find_peaks(y, height=peak_threshold, distance=20, prominence=prominence)
        item["peaks"] = peaks
        item["peak_heights"] = props.get("peak_heights", np.array([]))

        for peak_idx, height in zip(peaks, item["peak_heights"]):
            rows.append(
                {
                    "file": item["name"],
                    "raman_shift": float(x[peak_idx]),
                    "intensity": float(height),
                }
            )

    return pd.DataFrame(rows)


files = sorted(glob.glob(FILE_PATTERN, recursive=True))
datasets = [d for d in (load_dataset(path) for path in files) if len(d["x"]) > 10]

print(f"Loaded {len(datasets)} cleaned Raman datasets")
for item in datasets:
    meta = item["metadata"]
    print(
        f"- {item['name']}: "
        f"sec={meta.get('integration times(sec)')}, "
        f"set={meta.get('average number')}, "
        f"power={meta.get('laser_powerlevel')}"
    )


# STEP 1: Plot raw spectra
plt.figure(figsize=(12, 7))
for item in datasets:
    plt.plot(item["x"], item["y"], label=item["name"], alpha=0.7)

plt.xlabel("Raman Shift (cm^-1)")
plt.ylabel("Intensity (Raw Counts)")
plt.title("Raw Raman Spectra")
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()


# STEP 2: Baseline correction + smoothing
processed_data = []

plt.figure(figsize=(12, 7))
for item in datasets:
    baseline = baseline_als(item["y"])
    y_corrected = item["y"] - baseline
    y_smooth = smooth_signal(y_corrected)

    processed = dict(item)
    processed["baseline"] = baseline
    processed["y_corrected"] = y_corrected
    processed["y_smooth"] = y_smooth
    processed_data.append(processed)

    plt.plot(item["x"], y_smooth, label=item["name"], alpha=0.8)

plt.xlabel("Raman Shift (cm^-1)")
plt.ylabel("Corrected Intensity")
plt.title("Baseline Corrected and Smoothed Raman Spectra")
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()


# STEP 3: Peak detection
peak_table = build_peak_table(processed_data)

plt.figure(figsize=(12, 7))
for item in processed_data:
    x = item["x"]
    y = item["y_smooth"]
    peaks = item["peaks"]

    plt.plot(x, y, label=item["name"], alpha=0.75)
    plt.scatter(x[peaks], y[peaks], color="red", s=12)

plt.xlabel("Raman Shift (cm^-1)")
plt.ylabel("Intensity")
plt.title("Detected Raman Peaks")
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

print("\nPeak summary:")
if peak_table.empty:
    print("No peaks detected with the current threshold.")
else:
    print(peak_table.sort_values(["file", "raman_shift"]).to_string(index=False))


# STEP 4: Average spectrum
common_x = processed_data[0]["x"]
all_y = []

for item in processed_data:
    y_interp = np.interp(common_x, item["x"], item["y_smooth"])
    item["y_interp"] = y_interp
    all_y.append(y_interp)

all_y = np.array(all_y)
mean_spectrum = np.mean(all_y, axis=0)

plt.figure(figsize=(12, 7))
for item in processed_data:
    plt.plot(common_x, item["y_interp"], color="gray", alpha=0.25)
plt.plot(common_x, mean_spectrum, color="black", linewidth=2, label="Average spectrum")
plt.title("Average Raman Spectrum")
plt.xlabel("Raman Shift (cm^-1)")
plt.ylabel("Intensity")
plt.legend()
plt.tight_layout()
plt.show()


# STEP 5: Compare differences from the average
plt.figure(figsize=(12, 7))
for item in processed_data:
    delta = item["y_interp"] - mean_spectrum
    item["difference_from_mean"] = delta
    plt.plot(common_x, delta, label=item["name"], alpha=0.8)

plt.axhline(0, color="black", linewidth=1, linestyle="--")
plt.title("Difference from Average Spectrum")
plt.xlabel("Raman Shift (cm^-1)")
plt.ylabel("Delta Intensity")
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()


# STEP 6: Compact comparison table
comparison_rows = []
for item in processed_data:
    delta = item["difference_from_mean"]
    comparison_rows.append(
        {
            "file": item["name"],
            "sec": item["metadata"].get("integration times(sec)"),
            "set": item["metadata"].get("average number"),
            "power": item["metadata"].get("laser_powerlevel"),
            "max_corrected_intensity": float(np.max(item["y_smooth"])),
            "peak_count": int(len(item["peaks"])),
            "rmse_vs_average": float(np.sqrt(np.mean(delta ** 2))),
        }
    )

comparison_df = pd.DataFrame(comparison_rows).sort_values(["sec", "power", "set", "file"])

print("\nComparison summary:")
print(comparison_df.to_string(index=False))
