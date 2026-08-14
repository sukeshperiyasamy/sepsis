# Test script to verify the analysis works
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
from scipy.sparse import csc_matrix, eye, diags
from scipy.sparse.linalg import spsolve
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("Testing NAM Raman Analysis (40% Power)")
print("="*60)

# File paths
simulation_file = r"C:\Users\sukes\Downloads\plottingNAM\simulated-NAM.xlsx"
powder_file = r"C:\Users\sukes\Downloads\plottingNAM\namdata20secpower40.xlsx"

# Test 1: Load simulation data
print("\n1. Loading simulation data...")
try:
    df_simulation = pd.read_excel(simulation_file, header=None, engine='openpyxl')
    df_simulation.columns = ['Raman_shift', 'Intensity']
    print(f"   ✓ Simulation data loaded: {df_simulation.shape}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 2: Load powder data
print("\n2. Loading powder data (40% power)...")
try:
    df_powder = pd.read_excel(powder_file, header=None, engine='openpyxl')
    df_powder.columns = ['Raman_shift', 'Intensity']
    print(f"   ✓ Powder data loaded: {df_powder.shape}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 3: Filter spectral range
print("\n3. Filtering spectral range (200-2000 cm⁻¹)...")
try:
    range_min, range_max = 200, 2000
    df_simulation_filtered = df_simulation[
        (df_simulation['Raman_shift'] >= range_min) & 
        (df_simulation['Raman_shift'] <= range_max)
    ].copy()
    df_powder_filtered = df_powder[
        (df_powder['Raman_shift'] >= range_min) & 
        (df_powder['Raman_shift'] <= range_max)
    ].copy()
    print(f"   ✓ Simulation filtered: {len(df_simulation)} → {len(df_simulation_filtered)} points")
    print(f"   ✓ Powder filtered: {len(df_powder)} → {len(df_powder_filtered)} points")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 4: Normalize simulation
print("\n4. Normalizing simulation spectrum...")
try:
    df_simulation_filtered['Intensity_normalized'] = (
        df_simulation_filtered['Intensity'] / df_simulation_filtered['Intensity'].max()
    )
    print(f"   ✓ Normalized range: [{df_simulation_filtered['Intensity_normalized'].min():.4f}, {df_simulation_filtered['Intensity_normalized'].max():.4f}]")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 5: Preprocess powder data
print("\n5. Preprocessing powder data...")
try:
    # ALS baseline function
    def als_baseline(y, lam=1e5, p=0.01, niter=5):
        from scipy import sparse
        from scipy.sparse.linalg import spsolve
        L = len(y)
        D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
        w = np.ones(L)
        for _ in range(niter):
            W = sparse.spdiags(w, 0, L, L)
            Z = W + lam * D @ D.T
            z = spsolve(Z, w * y)
            w = p * (y > z) + (1 - p) * (y < z)
        return z
    
    df_powder_processed = df_powder_filtered.copy()
    
    # Dark subtraction
    dark_baseline = df_powder_processed['Intensity'].min()
    df_powder_processed['Intensity'] = df_powder_processed['Intensity'] - dark_baseline
    print(f"   ✓ Dark subtraction (baseline = {dark_baseline:.2f})")
    
    # ALS baseline correction
    baseline = als_baseline(df_powder_processed['Intensity'].values, lam=1e5, p=0.01, niter=5)
    df_powder_processed['Intensity'] = df_powder_processed['Intensity'].values - baseline
    df_powder_processed['Intensity'] = np.maximum(df_powder_processed['Intensity'], 0)
    print(f"   ✓ ALS baseline correction completed")
    
    # Savitzky-Golay smoothing
    df_powder_processed['Intensity'] = savgol_filter(
        df_powder_processed['Intensity'].values, 11, 3
    )
    print(f"   ✓ Savitzky-Golay smoothing completed")
    
    # Normalize
    df_powder_processed['Intensity_normalized'] = (
        df_powder_processed['Intensity'] / df_powder_processed['Intensity'].max()
    )
    print(f"   ✓ Normalized range: [{df_powder_processed['Intensity_normalized'].min():.4f}, {df_powder_processed['Intensity_normalized'].max():.4f}]")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 6: Peak detection
print("\n6. Detecting peaks...")
try:
    peaks_sim, _ = find_peaks(
        df_simulation_filtered['Intensity_normalized'].values,
        prominence=0.1,
        height=0.1
    )
    peaks_powder, _ = find_peaks(
        df_powder_processed['Intensity_normalized'].values,
        prominence=0.4,
        height=0.4,
        distance=10
    )
    print(f"   ✓ Simulation peaks: {len(peaks_sim)}")
    print(f"   ✓ Powder peaks: {len(peaks_powder)}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 7: Create output directory
print("\n7. Creating output directory...")
try:
    import os
    output_dir = "figures_40power_normalized"
    os.makedirs(output_dir, exist_ok=True)
    print(f"   ✓ Output directory: {output_dir}/")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

# Test 8: Create a simple test plot
print("\n8. Creating test plot...")
try:
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_simulation_filtered['Raman_shift'], 
            df_simulation_filtered['Intensity_normalized'],
            'b-', linewidth=2, label='Simulation')
    ax.plot(df_powder_processed['Raman_shift'], 
            df_powder_processed['Intensity_normalized'],
            'r-', linewidth=2, label='Powder (40% Power)')
    ax.set_xlabel('Raman Shift (cm⁻¹)')
    ax.set_ylabel('Normalized Intensity (a.u.)')
    ax.set_title('Test Overlay Plot')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/test_plot.png", dpi=150)
    plt.close()
    print(f"   ✓ Test plot saved: {output_dir}/test_plot.png")
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    exit(1)

print("\n" + "="*60)
print("✓ ALL TESTS PASSED - No issues detected!")
print("="*60)
print("\nThe notebook should work correctly.")
print("If the notebook still hangs, try:")
print("  1. Restart VS Code")
print("  2. Clear all outputs and run again")
print("  3. Check if another Python process is using matplotlib")
