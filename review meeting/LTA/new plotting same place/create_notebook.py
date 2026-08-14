import nbformat as nbf

nb = nbf.v4.new_notebook()

# Cell 1: Imports
cell_setup = nbf.v4.new_code_cell("""\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import savgol_filter, find_peaks
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.5

# Setup custom logging to save all cell outputs to a text file
report_file = open('LTA_Raman_Analysis_Report.txt', 'w', encoding='utf-8')

def log_print(*args, **kwargs):
    print(*args, **kwargs)
    print(*args, file=report_file, **kwargs)
    report_file.flush()

log_print("============================================================")
log_print("SECTION 1: Notebook Initialization & Environment Setup")
log_print("============================================================")
log_print("Libraries loaded (pandas, numpy, scipy, matplotlib).")
log_print("Logging stream ready.")
log_print("")
""")

# Cell 2: ALS Function
cell_als = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 2: Defining Baseline Correction Algorithm (ALS)")
log_print("============================================================")
def baseline_als(y, lam=1e5, p=0.01, niter=10):
    '''
    Asymmetric Least Squares Smoothing for Baseline Correction
    '''
    L = len(y)
    D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
    return z

log_print("Asymmetric Least Squares (ALS) function successfully loaded into memory.")
log_print("")
""")

# Cell 3: Data Loading
cell_load = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 3: Data Extraction & Cleaning")
log_print("============================================================")

# List of individual Excel files for each power level
file_paths = {
    40: 'sec-10_power-40_i-10.xlsx',
    50: 'sec-10_power-50_i-10.xlsx',
    60: 'sec-10_power-60_i-10.xlsx',
    70: 'sec-10_power-70_i-10.xlsx'
}
log_print(f"Targeting dataset: Individual power files (40, 50, 60, 70 mW)")

# List of laser power levels
powers = [40, 50, 60, 70]
raw_data = {}

for power, file_path in file_paths.items():
    # Load columns C and D (indices 2 and 3)
    df = pd.read_excel(file_path, usecols=[2, 3], header=None)
    
    # Extract numeric data, forcing non-numeric to NaN to handle metadata seamlessly
    df[2] = pd.to_numeric(df[2], errors='coerce')
    df[3] = pd.to_numeric(df[3], errors='coerce')
    
    # Drop rows where either Raman Shift or Intensity is NaN
    df_clean = df.dropna(subset=[2, 3]).copy()
    
    # Rename columns for clarity
    df_clean.columns = ['Raman_Shift', 'Dark_Subtracted_Intensity']
    
    # Sort x-axis and reset index
    df_clean = df_clean.sort_values(by='Raman_Shift').reset_index(drop=True)
    
    raw_data[power] = df_clean
    log_print(f"  -> Power {power}mW loaded from {file_path}. Total valid points: {len(df_clean)}")

log_print("Data Cleaning Complete. All invalid string metadata isolated & removed.")
log_print("")
""")

# Cell 4: Plot COMBINED RAW SPECTRA
cell_plot_raw = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 4: Plotting Overlay of Raw Spectra")
log_print("============================================================")
log_print("Initiating graph for baseline standard Raw Data comparison (500-2000 cm⁻¹)...")

plt.figure(figsize=(10, 6))
for power in powers:
    x = raw_data[power]['Raman_Shift']
    y = raw_data[power]['Dark_Subtracted_Intensity']
    plt.plot(x, y, label=f'{power} mW', linewidth=1.5)

plt.title('COMBINED RAW SPECTRA - Different Laser Power Levels')
plt.xlabel('Raman Shift (cm⁻¹)')
plt.ylabel('Dark Subtracted Intensity (a.u.)')
plt.xlim(500, 2000)
plt.legend()
plt.tight_layout()
plt.show()

log_print("Graph generated: 'COMBINED RAW SPECTRA'")
log_print("")
""")

# Cell 5: Apply BASELINE CORRECTION
cell_apply_als = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 5: Mathematical Baseline Modeling (ALS Algorithm)")
log_print("============================================================")

corrected_data = {}
baselines = {}

for power in powers:
    df = raw_data[power].copy()
    y = df['Dark_Subtracted_Intensity'].values
    
    log_print(f"  -> Constructing baseline matrix and running 10 ALS iterations for {power}mW data...")
    y_baseline = baseline_als(y, lam=1e5, p=0.01, niter=10)
    y_corrected = y - y_baseline
    
    df['Baseline'] = y_baseline
    df['Corrected_Intensity'] = y_corrected
    
    baselines[power] = y_baseline
    corrected_data[power] = df

log_print("Baseline mapping and signal subtraction successfully computed for all 4 profiles.")
log_print("")
""")

# Cell 6: Plot COMBINED BASELINE-CORRECTED SPECTRA
cell_plot_corrected = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 6: Plotting Overlay of Cleaned (Corrected) Spectra")
log_print("============================================================")
log_print("Generating combined overlay of mathematically flattened signals (500-2000 cm⁻¹)...")

plt.figure(figsize=(10, 6))

for power in powers:
    x = corrected_data[power]['Raman_Shift']
    y_corr = corrected_data[power]['Corrected_Intensity']
    plt.plot(x, y_corr, label=f'{power} mW', linewidth=1.5)

plt.title('COMBINED BASELINE-CORRECTED SPECTRA')
plt.xlabel('Raman Shift (cm⁻¹)')
plt.ylabel('Corrected Intensity (a.u.)')
plt.xlim(500, 2000)
plt.legend()
plt.tight_layout()
plt.show()

log_print("Graph generated: 'COMBINED BASELINE-CORRECTED SPECTRA'")
log_print("")
""")

# Cell 7: Plot RAW vs BASELINE comparison in 4 subplots
cell_plot_comparison = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 7: Visualizing Pre/Post Baseline Transformation Matrix")
log_print("============================================================")
log_print("Generating 2x2 subplot matrix (500-2000 cm⁻¹)...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, power in enumerate(powers):
    ax = axes[i]
    x = corrected_data[power]['Raman_Shift']
    y_raw = corrected_data[power]['Dark_Subtracted_Intensity']
    y_base = corrected_data[power]['Baseline']
    y_corr = corrected_data[power]['Corrected_Intensity']
    
    ax.plot(x, y_raw, label='Raw Data', color='gray', alpha=0.7)
    ax.plot(x, y_base, label='ALS Baseline', color='red', linestyle='--')
    ax.plot(x, y_corr, label='Baseline-Corrected', color='blue')
    
    ax.set_title(f'Raw vs Baseline - {power} mW')
    ax.set_xlabel('Raman Shift (cm⁻¹)')
    ax.set_ylabel('Intensity (a.u.)')
    ax.set_xlim(500, 2000)
    ax.legend()

plt.tight_layout()
plt.show()

log_print("Graph matrix generated successfully.")
log_print("")
""")

# Cell 8: Plot INDIVIDUAL BASELINE-CORRECTED SPECTRA
cell_plot_individual = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 8: Detailed Individual Power Profiling")
log_print("============================================================")
log_print("Generating isolated graphs for each independent 40-70 mW trial (500-2000 cm⁻¹)...")

for power in powers:
    plt.figure(figsize=(8, 4))
    x = corrected_data[power]['Raman_Shift']
    y_corr = corrected_data[power]['Corrected_Intensity']
    
    plt.plot(x, y_corr, label=f'{power} mW', color='navy')
    
    plt.title(f'INDIVIDUAL BASELINE-CORRECTED SPECTRUM - {power} mW')
    plt.xlabel('Raman Shift (cm⁻¹)')
    plt.ylabel('Corrected Intensity (a.u.)')
    plt.xlim(500, 2000)
    plt.legend()
    plt.tight_layout()
    plt.show()
    log_print(f"  -> Generated graphic for {power} mW.")

log_print("")
""")

# Cell 9: Advanced Analysis (Smoothing, Peak Finding, SNR)
cell_analysis = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 9: Peak Extrapolation & Advanced Hardware Interpretation")
log_print("============================================================")
smoothed_data = {}
peaks_data = {}
advanced_snr_results = {}

for power in powers:
    df = corrected_data[power].copy()
    
    # 1. Smoothing
    window_length = 11
    polyorder = 3
    y_corr = df['Corrected_Intensity'].values
    y_smooth = savgol_filter(y_corr, window_length, polyorder)
    df['Smoothed_Intensity'] = y_smooth
    smoothed_data[power] = df
    log_print(f"  -> [Power {power}mW] Applied Savitzky-Golay (WL:11|PO:3) noise smoothing.")
    
    # 2. Find Peaks
    mask = (df['Raman_Shift'] >= 500) & (df['Raman_Shift'] <= 2000)
    x_roi = df.loc[mask, 'Raman_Shift'].values
    y_roi = df.loc[mask, 'Smoothed_Intensity'].values
    
    if len(y_roi) > 0:
        peak_indices, _ = find_peaks(y_roi, prominence=np.std(y_roi)*0.5, height=np.mean(y_roi))
        peak_positions = x_roi[peak_indices]
    else:
        peak_positions = np.array([])
        
    peaks_data[power] = {'positions': peak_positions}
    log_print(f"  -> [Power {power}mW] Extracted {len(peak_positions)} major physical peak positions in ROIs.")
    
    # 3. SNR
    noise_region = df['Smoothed_Intensity'].values[:100]
    noise_std = np.std(noise_region) if len(noise_region) > 0 else 1.0
    signal_strength = np.max(y_roi) if len(y_roi) > 0 else 0
    snr = signal_strength / noise_std if noise_std > 0 else 0
    advanced_snr_results[power] = snr

log_print("Signal Processing engine successfully gathered heuristics.")
log_print("")
""")

# Cell 10: Interpretation and Recommendations
cell_interpretation = nbf.v4.new_code_cell("""\
log_print("============================================================")
log_print("SECTION 10: Final Interpretation Matrix")
log_print("============================================================")

# Signal Strength Analysis
avg_snr = np.mean(list(advanced_snr_results.values()))
if avg_snr < 5:
    signal_strength = "WEAK"
elif avg_snr < 15:
    signal_strength = "MODERATE"
else:
    signal_strength = "STRONG"

log_print(f"\\n1. Signal Strength: {signal_strength}")
log_print(f"   - Average SNR: {avg_snr:.2f}")
log_print(f"   - SNR Classification: {'Acceptable for weak LTA signals' if avg_snr >= 5 else 'Low - consider longer integration or higher power'}")

# LTA Peak Analysis
lta_peaks_found = False
for power in powers:
    peak_positions = peaks_data[power]['positions']
    for pos in peak_positions:
        if 1050 <= pos <= 1100:
            lta_peaks_found = True
            break

log_print(f"\\n2. LTA Peaks (Phosphate region ~1080 cm⁻¹):")
if lta_peaks_found:
    log_print("   - phosphate/LTA peaks DETECTED")
else:
    log_print("   - No clear LTA phosphate peaks detected")
    log_print("   - Try: adjusting baseline or increasing integration time")

# Laser Power Effect
log_print(f"\\n3. Laser Power Effect:")
snr_values = list(advanced_snr_results.values())
if snr_values[0] < snr_values[-1]:
    log_print("   - SNR increases with laser power")
    log_print("   - Recommendation: Use highest practical power (70mW)")
else:
    log_print("   - SNR relatively constant across power levels")
    log_print("   - Consider optimizing other parameters")

# Noise Analysis
log_print(f"\\n4. Noise Behavior:")
for power in powers:
    df = smoothed_data[power]
    noise_region = df['Smoothed_Intensity'].values[:100]
    noise_std = np.std(noise_region)
    log_print(f"   - Power {power}mW: noise std = {noise_std:.3f}")

# Recommendations
log_print(f"\\n5. Recommendations:")
log_print("   a. For weak LTA signals, consider:")
log_print("      - Longer integration time")
log_print("      - Higher laser power (if samples allow)")
log_print("      - Multiple scans and averaging")
log_print("   b. For better baseline correction:")
log_print("      - Adjust ALS parameters (lambda, p)")
log_print("   c. For peak detection:")
log_print("      - Adjust height/distance parameters")
log_print("      - Consider 2nd derivative analysis")

log_print("\\n" + "=" * 60)
log_print("PROCESS EXECUTION COMPLETED")
log_print("=" * 60)

report_file.close()
""")

# Assemble notebook
nb.cells = [
    nbf.v4.new_markdown_cell('# Raman Spectroscopy Analysis - Baseline Correction\nThis notebook processes 4 sheets of Raman spectra (powers: 40, 50, 60, 70), removing metadata rows, and extracting Raman Shift (col C) vs Intensity (col D).\n\nRequires: `pandas`, `numpy`, `scipy`, `matplotlib`'),
    cell_setup,
    nbf.v4.new_markdown_cell('### 1. Function for Baseline Correction (ALS)'),
    cell_als,
    nbf.v4.new_markdown_cell('### 2. Load and Clean Data from Excel Sheets'),
    cell_load,
    nbf.v4.new_markdown_cell('### 3. Plot Combined Raw Spectra'),
    cell_plot_raw,
    nbf.v4.new_markdown_cell('### 4. Apply Baseline Correction using ALS'),
    cell_apply_als,
    nbf.v4.new_markdown_cell('### 5. Plot Combined Baseline-Corrected Spectra'),
    cell_plot_corrected,
    nbf.v4.new_markdown_cell('### 6. Plot Raw vs Baseline Comparison (Subplots)'),
    cell_plot_comparison,
    nbf.v4.new_markdown_cell('### 7. Plot Individual Baseline-Corrected Spectra'),
    cell_plot_individual,
    nbf.v4.new_markdown_cell('### 8. Advanced Data Analysis (Smoothing & ROI Metrics)'),
    cell_analysis,
    nbf.v4.new_markdown_cell('### 9. Signal Quality Interpretation & Recommendations'),
    cell_interpretation
]

with open('LTA_Raman_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print("Notebook 'LTA_Raman_Analysis.ipynb' updated fully with detailed logging.")
