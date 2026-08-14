import re
import numpy as np
import matplotlib.pyplot as plt

def parse_gaussian_log(filename):
    """Extract frequencies and Raman activities from Gaussian log file."""
    freqs = []
    activities = []
    with open(filename, 'r', errors='ignore') as f:
        for line in f:
            if "Frequencies --" in line:
                freqs.extend([float(x) for x in line.split()[2:]])
            if "Raman Activ" in line:
                activities.extend([float(x) for x in line.split()[3:]])
    return np.array(freqs), np.array(activities)

def broaden_spectrum(freqs, intensities, fwhm=20, resolution=2):
    """Apply Gaussian broadening to make smooth Raman peaks."""
    min_freq, max_freq = 0, 4000
    x = np.arange(min_freq, max_freq, resolution)
    y = np.zeros_like(x)
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    for f, i in zip(freqs, intensities):
        y += i * np.exp(-(x - f)**2 / (2 * sigma**2))
    return x, y

def plot_raman(freqs, activities, title="Raman Activity Spectrum", outfile="raman_spectrum.png"):
    """Plot and save the Raman spectrum."""
    x, y = broaden_spectrum(freqs, activities)
    plt.figure(figsize=(9,5))
    plt.plot(x, y, color='maroon', linewidth=1.2)
    plt.xlabel("Frequency (cm⁻¹)")
    plt.ylabel("Intensity (a.u.)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 4000)
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    plt.show()

# === MAIN ===
logfile = "D-Glucose.log"  # change filename here
freqs, activities = parse_gaussian_log(logfile)
plot_raman(freqs, activities)
