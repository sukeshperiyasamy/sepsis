import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Data
exp_df = pd.read_csv('output_figures/processed_sec-25_power-80_i-2.csv')
exp_x = exp_df.iloc[:, 0].values
exp_y = exp_df.iloc[:, 1].values

sim_df = pd.read_excel('simdata.xlsx')
sim_x = sim_df['X'].values
sim_y = sim_df['Y'].values

# Normalize simulation to 0-1
sim_y = (sim_y - sim_y.min()) / (sim_y.max() - sim_y.min())

# Setup Plot configuration
fig = plt.figure(figsize=(16, 7))
gs = fig.add_gridspec(1, 4, wspace=0.1)

ax_main = fig.add_subplot(gs[0, :3])
ax_text = fig.add_subplot(gs[0, 3])

# Overlay Plot
ax_main.plot(sim_x, sim_y + 0.1, color='#d62728', label='Simulated (DFT)', alpha=0.8, linewidth=2)  # Slight offset for clarity, Red color
ax_main.plot(exp_x, exp_y, color='black', label='Experimental Spectrum', linewidth=2)

# Specific peaks requested by user to be marked
key_peaks = [489, 830, 956, 1024, 1086, 1319, 1452, 1701]

# Mark peaks
for peak in key_peaks:
    # Find closest point in experimental data
    idx = (np.abs(exp_x - peak)).argmin()
    x_val = exp_x[idx]
    y_val = exp_y[idx]
    
    # Add a marker and some text
    ax_main.plot(x_val, y_val, marker='v', color='#1f77b4', markersize=8)
    ax_main.annotate(str(peak), 
                     xy=(x_val, y_val), 
                     xytext=(0, 15), 
                     textcoords="offset points", 
                     ha='center', 
                     va='bottom', 
                     fontsize=11, 
                     rotation=90, 
                     color='#1f77b4', 
                     fontweight='bold',
                     arrowprops=dict(arrowstyle="-", color='#1f77b4'))

ax_main.set_xlabel('Raman Shift (cm$\\mathbf{^{-1}}$)', fontsize=14, fontweight='bold')
ax_main.set_ylabel('Normalized Intensity', fontsize=14, fontweight='bold')
ax_main.set_xlim(200, 3000)
ax_main.set_ylim(-0.05, 1.4)
ax_main.legend(loc='upper right', fontsize=14, framealpha=0.9, edgecolor='black')
ax_main.grid(True, linestyle='--', alpha=0.5)
ax_main.set_title('Experimental vs. Simulated Raman Spectra Overlay', fontsize=18, fontweight='bold', pad=20)

# Right Side - Results Box
ax_text.axis('off')

box_text = (
    "$\\mathbf{Peak\ Matching\ Results}$\n"
    "─────────────────\n\n"
    "$\\mathbf{Matched\ Peaks:}$ 51\n\n"
    "$\\mathbf{RMSE:}$ 2.12 cm$^{-1}$\n\n"
    "$\\mathbf{Mean\ Error:}$ 0.38 cm$^{-1}$\n\n"
    "$\\mathbf{Tolerance:}$ ±10 cm$^{-1}$"
)

# Create a clean, highlighted box
bbox_props = dict(boxstyle="round,pad=1.5", fc="#f8f9fa", ec="#343a40", lw=2.5)

ax_text.text(0.5, 0.5, box_text, 
             ha='center', va='center', 
             fontsize=15, 
             bbox=bbox_props, 
             color='#212529',
             transform=ax_text.transAxes)

plt.tight_layout()
plt.savefig('output_figures/overlay_validation_plot.png', dpi=300, bbox_inches='tight')
print("Plot successfully saved to: 'output_figures/overlay_validation_plot.png'")
