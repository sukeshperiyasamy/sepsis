#!/usr/bin/env python3
"""
Extract and plot Raman spectrum from Gaussian output
Applies Gaussian/Lorentzian broadening to stick spectrum

Usage:
  1. Extract frequencies and Raman activities from .log file
  2. Update the freq and raman_activ arrays below
  3. Run: python plot_raman_spectrum.py
"""

import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# STEP 1: Extract data from Gaussian .log file
# ==============================================================================
# Search for lines like:
#   Frequencies --   1045.2  1082.7  1120.4
#   Raman Activ --   215.4   190.2   88.9
#
# Paste your frequencies and Raman activities here:

# Example data (REPLACE WITH YOUR ACTUAL VALUES)
freq = np.array([
    500, 580, 720, 850, 920,  # Example low frequency
    1050, 1080, 1110, 1150,   # PO2- stretch region
    1250, 1300, 1350,         # C-C stretch
    1440, 1460,               # CH2 scissoring
    1560, 1580,               # Amide II
    1650, 1680                # Amide I
])

raman_activ = np.array([
    10, 15, 25, 30, 20,       # Low intensity
    180, 220, 190, 150,       # Strong phosphate peaks
    80, 90, 70,               # Medium C-C
    120, 100,                 # CH2
    140, 160,                 # Amide II
    200, 180                  # Amide I
])

# ==============================================================================
# STEP 2: Apply broadening
# ==============================================================================

def gaussian_broadening(x, freq, intensity, fwhm=10.0):
    """
    Apply Gaussian broadening to stick spectrum
    
    Parameters:
    -----------
    x : array
        Wavenumber grid (cm^-1)
    freq : array
        Peak frequencies (cm^-1)
    intensity : array
        Peak intensities (Raman activities)
    fwhm : float
        Full width at half maximum (cm^-1)
    """
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    y = np.zeros_like(x)
    
    for f, i in zip(freq, intensity):
        y += i * np.exp(-(x - f)**2 / (2 * sigma**2))
    
    return y

def lorentzian_broadening(x, freq, intensity, fwhm=10.0):
    """
    Apply Lorentzian broadening to stick spectrum
    
    Parameters:
    -----------
    x : array
        Wavenumber grid (cm^-1)
    freq : array
        Peak frequencies (cm^-1)
    intensity : array
        Peak intensities (Raman activities)
    fwhm : float
        Full width at half maximum (cm^-1)
    """
    gamma = fwhm / 2
    y = np.zeros_like(x)
    
    for f, i in zip(freq, intensity):
        y += i * (gamma**2) / ((x - f)**2 + gamma**2)
    
    return y

# ==============================================================================
# STEP 3: Generate spectrum
# ==============================================================================

# Wavenumber range (cm^-1)
x = np.linspace(400, 1800, 5000)

# Apply broadening (choose one)
y_gaussian = gaussian_broadening(x, freq, raman_activ, fwhm=10)
y_lorentzian = lorentzian_broadening(x, freq, raman_activ, fwhm=10)

# Normalize to max intensity = 1
y_gaussian = y_gaussian / np.max(y_gaussian)
y_lorentzian = y_lorentzian / np.max(y_lorentzian)

# ==============================================================================
# STEP 4: Plot spectrum
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Panel A: Gaussian broadening
ax1.plot(x, y_gaussian, 'b-', linewidth=2)
ax1.set_xlabel('Raman shift (cm$^{-1}$)', fontsize=14)
ax1.set_ylabel('Normalized Intensity (a.u.)', fontsize=14)
ax1.set_title('Lipid A Proxy - Raman Spectrum (Gaussian Broadening)', fontsize=16, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(400, 1800)

# Add region labels
ax1.axvspan(980, 1100, alpha=0.1, color='red', label='PO$_2^-$ stretch')
ax1.axvspan(1060, 1130, alpha=0.1, color='orange', label='C-C lipid')
ax1.axvspan(1420, 1460, alpha=0.1, color='yellow', label='CH$_2$ scissor')
ax1.axvspan(1540, 1580, alpha=0.1, color='green', label='Amide II')
ax1.axvspan(1640, 1680, alpha=0.1, color='blue', label='Amide I')
ax1.legend(loc='upper right', fontsize=10)

# Panel B: Lorentzian broadening
ax2.plot(x, y_lorentzian, 'r-', linewidth=2)
ax2.set_xlabel('Raman shift (cm$^{-1}$)', fontsize=14)
ax2.set_ylabel('Normalized Intensity (a.u.)', fontsize=14)
ax2.set_title('Lipid A Proxy - Raman Spectrum (Lorentzian Broadening)', fontsize=16, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(400, 1800)

# Add region labels
ax2.axvspan(980, 1100, alpha=0.1, color='red')
ax2.axvspan(1060, 1130, alpha=0.1, color='orange')
ax2.axvspan(1420, 1460, alpha=0.1, color='yellow')
ax2.axvspan(1540, 1580, alpha=0.1, color='green')
ax2.axvspan(1640, 1680, alpha=0.1, color='blue')

plt.tight_layout()
plt.savefig('lipidA_raman_spectrum.png', dpi=300, bbox_inches='tight')
print("✓ Saved: lipidA_raman_spectrum.png")

plt.show()

# ==============================================================================
# STEP 5: Export data for publication
# ==============================================================================

# Save broadened spectrum as CSV
output_data = np.column_stack((x, y_gaussian, y_lorentzian))
np.savetxt('lipidA_raman_spectrum.csv', output_data, 
           delimiter=',', 
           header='Wavenumber(cm-1),Intensity_Gaussian,Intensity_Lorentzian',
           comments='')

print("✓ Saved: lipidA_raman_spectrum.csv")
print("\n" + "=" * 78)
print("SPECTRUM GENERATION COMPLETE")
print("=" * 78)
print("\n📊 FILES CREATED:")
print("  • lipidA_raman_spectrum.png - Publication-quality figure")
print("  • lipidA_raman_spectrum.csv - Raw data for further analysis")
print("\n📝 INSTRUCTIONS:")
print("  1. Open lipidA_freq.log in a text editor")
print("  2. Search for 'Frequencies --' and 'Raman Activ --'")
print("  3. Copy all frequencies and Raman activities")
print("  4. Update the freq and raman_activ arrays in this script")
print("  5. Re-run to generate actual spectrum")
print("=" * 78)
