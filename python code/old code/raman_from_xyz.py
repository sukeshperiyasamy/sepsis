import numpy as np
import matplotlib.pyplot as plt
import random

def generate_fake_raman():
    # Random peak positions (simulate vibrational modes)
    peak_positions = sorted(random.sample(range(200, 3300), 10))
    
    # Random intensities
    intensities = [random.uniform(0.3, 1.0) for _ in peak_positions]

    # Build spectral curve
    x = np.linspace(100, 3500, 4000)
    y = np.zeros_like(x)

    for peak, inten in zip(peak_positions, intensities):
        y += inten * np.exp(-0.5 * ((x - peak) / 25)**2)

    return x, y

def plot_raman(molecule_name, outfile):
    x, y = generate_fake_raman()
    plt.figure(figsize=(10,4))
    plt.plot(x, y, linewidth=1.5)
    plt.title(f"Simulated Raman Spectrum: {molecule_name}")
    plt.xlabel("Raman Shift (cm⁻¹)")
    plt.ylabel("Intensity")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    plt.show()

molecules = [
    "Glucose","Lactate","Pyruvate","Urea","Creatinine",
    "Alanine","Phenylalanine","Cholesterol","Ascorbic Acid","Fructose"
]

for mol in molecules:
    print(f"Generating: {mol}")
    plot_raman(mol, f"{mol}_raman.png")
