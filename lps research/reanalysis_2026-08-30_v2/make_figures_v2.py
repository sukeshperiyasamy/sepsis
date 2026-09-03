import numpy as np, json, csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.expanduser('~/mnt')
OUT_DIR = os.path.join(BASE, 'mtp', 'lps research', 'reanalysis_2026-08-30_v2')

d = np.load(os.path.join(OUT_DIR, 'arrays_v2.npz'))
grid = d['grid']; exp_norm = d['exp_norm']; composite = d['composite']
exp_peaks = d['exp_peaks']; exp_prom = d['exp_prom']

with open(os.path.join(OUT_DIR, 'summary_v2.json')) as f:
    S = json.load(f)
summary = S['summary']; matches = S['matches']; unmatched = S['unmatched']; component_specific = S['component_specific']

frag_names = ['KDO', 'Glucosamine', 'Heptose', 'Myristic_Acid', 'Phosphoric_Acid']
frag_labels = {'KDO': 'KDO', 'Glucosamine': 'D-Glucosamine', 'Heptose': 'Heptose',
               'Myristic_Acid': 'Myristic Acid', 'Phosphoric_Acid': 'Phosphoric Acid'}
frag_colors = {'KDO': '#1b9e77', 'Glucosamine': '#d95f02', 'Heptose': '#7570b3',
               'Myristic_Acid': '#e7298a', 'Phosphoric_Acid': '#66a61e'}

# ============================================================
# FIGURE 1 -- Experimental LPS powder Raman spectrum
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(grid, exp_norm, color='#333333', lw=1.1, label='LPS powder Raman (processed)')
ax.plot(exp_peaks, exp_norm[np.searchsorted(grid, exp_peaks)], 'v', color='crimson', ms=5,
        label=f'Detected major peaks (n={len(exp_peaks)})')
ax.set_xlabel('Raman shift (cm$^{-1}$)')
ax.set_ylabel('Normalized intensity (a.u.)')
ax.set_title('Figure 1. Experimental LPS Powder Raman Spectrum\n(E. coli O111:B4, Sigma L2630 -- windowed, ALS baseline-corrected,\nSavitzky-Golay smoothed, min-max normalized)')
ax.legend(loc='upper right', fontsize=9)
ax.set_xlim(200, 2000)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'FigureV2_1_experimental_spectrum.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 2 -- DFT spectrum / component plots (per-fragment, discrete modes + visualization curve)
# ============================================================
fig, axes = plt.subplots(5, 1, figsize=(10, 13), sharex=True)
for ax, name in zip(axes, frag_names):
    curve = d[f'frag_curve_{name}']
    pf = d[f'frag_peakf_{name}']; pa = d[f'frag_peaka_{name}']
    ax.plot(grid, curve, color=frag_colors[name], lw=1.0)
    # mark only candidate modes actually used (>=5% of own max, within window)
    if len(pa) > 0:
        thr = 0.05 * pa.max()
        m = (pf >= 200) & (pf <= 2000) & (pa >= thr)
        pa_norm = pa[m] / pa.max() if pa.max() > 0 else pa[m]
        ax.vlines(pf[m], 0, pa_norm, color=frag_colors[name], alpha=0.5, lw=0.8)
    rep = summary['fragment_report'][name]
    ax.set_ylabel(frag_labels[name], fontsize=9)
    ax.text(0.99, 0.85, f"{rep['n_discrete_modes']} discrete modes (calc.);\nnative broadened curve: {'yes' if rep['has_native_broadened_curve'] else 'no'} ({rep['native_curve_points']} pts)",
            transform=ax.transAxes, ha='right', va='top', fontsize=7, color='#444444')
axes[-1].set_xlabel('Raman shift (cm$^{-1}$, scaled x0.9613)')
axes[0].set_title('Figure 2. DFT Raman Spectra of the Five LPS Structural Fragments\n(scaled harmonic frequencies, activity-weighted stick modes overlaid on a\nGaussian-broadened visualization curve, FWHM=20 cm$^{-1}$, for display only)', fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'FigureV2_2_dft_component_plots.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 3 -- Experimental vs DFT (whole-curve composite) overlay
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(grid, exp_norm, color='#333333', lw=1.1, label='Experimental LPS powder (normalized)')
ax.plot(grid, composite, color='#1f78b4', lw=1.1, ls='--',
        label='NNLS-weighted composite of 5 DFT fragment curves\n(secondary/exploratory -- see caveat in report)')
ax.set_xlabel('Raman shift (cm$^{-1}$)')
ax.set_ylabel('Normalized intensity (a.u.)')
wc = summary['whole_curve_fit_SECONDARY_ONLY']
ax.set_title(f"Figure 3. Experimental vs. DFT Composite Overlay\nRMSE={wc['rmse']:.3f}, R$^2$={wc['r2']:.3f}, r={wc['pearson_r']:.3f} (whole-curve; secondary diagnostic only)")
ax.legend(loc='upper right', fontsize=8)
ax.set_xlim(200, 2000)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'FigureV2_3_experimental_vs_dft_overlay.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 4 -- Peak-matching plot, 4-way classification
# ============================================================
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(grid, exp_norm, color='#cccccc', lw=1.0, zorder=1, label='Experimental spectrum')

conf = [m for m in matches if m['classification'] == 'Matched - confident']
unc = [m for m in matches if m['classification'] == 'Matched - uncertain']

def yval(x):
    return exp_norm[np.searchsorted(grid, x)]

if unc:
    xs = [m['exp'] for m in unc]; ys = [yval(x) for x in xs]
    ax.scatter(xs, ys, marker='o', s=35, facecolor='#fdae61', edgecolor='#a35a00', zorder=3, label=f'Matched - uncertain (n={len(unc)})')
if conf:
    xs = [m['exp'] for m in conf]; ys = [yval(x) for x in xs]
    ax.scatter(xs, ys, marker='*', s=180, facecolor='#1a9850', edgecolor='black', zorder=4, label=f'Matched - confident (n={len(conf)})')
if unmatched:
    xs = [u[0] for u in unmatched]; ys = [yval(x) for x in xs]
    ax.scatter(xs, ys, marker='x', s=45, color='#d73027', zorder=3, label=f'Unmatched experimental (n={len(unmatched)})')

# component-specific DFT-only modes: show as faint ticks near baseline
cs_x = [c['dft'] for c in component_specific]
ax.vlines(cs_x, -0.05, -0.01, color='#4575b4', alpha=0.35, lw=0.6)

ax.set_ylim(-0.12, 1.08)
ax.set_xlim(200, 2000)
ax.set_xlabel('Raman shift (cm$^{-1}$)')
ax.set_ylabel('Normalized intensity (a.u.)')
ax.set_title('Figure 4. Experimental-DFT Peak Matching (Hungarian assignment, one-to-one, tolerance = 15 cm$^{-1}$)')
ax.legend(loc='upper right', fontsize=8)
fig.tight_layout(rect=[0, 0.08, 1, 1])
fig.text(0.5, 0.015, f'Blue ticks: DFT-only (component-specific) modes not claimed by any experimental peak, n={len(component_specific)}',
         ha='center', fontsize=8, color='#4575b4')
fig.savefig(os.path.join(OUT_DIR, 'FigureV2_4_peak_matching.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 5 -- Final LPS reference-band figure (confident tier only)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(grid, exp_norm, color='#333333', lw=1.1)
conf_sorted = sorted(conf, key=lambda m: m['exp'])
# stagger annotation offsets so nearby bands (e.g. 721/748, 1659/1693) don't overlap
offsets = [(-25, 55), (25, 95), (-25, 55), (25, 95)]
for i, m in enumerate(conf_sorted):
    x = m['exp']; y = yval(x)
    ax.plot([x, x], [0, y], color='#1a9850', lw=1.3, alpha=0.8)
    ax.plot(x, y, marker='*', ms=14, color='#1a9850', mec='black')
    ox, oy = offsets[i % len(offsets)]
    ax.annotate(f"{x:.0f} cm$^{{-1}}$\n(DFT {m['dft']:.1f}, {m['frag'].replace('_',' ')})", (x, y),
                textcoords='offset points', xytext=(ox, oy), ha='center', fontsize=8,
                arrowprops=dict(arrowstyle='-', color='#666666', lw=0.6))
ax.set_xlabel('Raman shift (cm$^{-1}$)')
ax.set_ylabel('Normalized intensity (a.u.)')
ax.set_title(f'Figure 5. DFT-Supported LPS Reference Bands (n={len(conf)})\nCriteria: unique fragment assignment within 15 cm$^{{-1}}$ AND |exp - DFT| <= 5 cm$^{{-1}}$\n(These are DFT-supported reference bands, NOT validated LPS-specific biomarkers)')
ax.set_xlim(200, 2000)
ax.set_ylim(0, 1.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'FigureV2_5_reference_bands.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

print('Figures written:')
for fn in ['FigureV2_1_experimental_spectrum.png','FigureV2_2_dft_component_plots.png',
           'FigureV2_3_experimental_vs_dft_overlay.png','FigureV2_4_peak_matching.png',
           'FigureV2_5_reference_bands.png']:
    p = os.path.join(OUT_DIR, fn)
    print(fn, os.path.getsize(p) if os.path.exists(p) else 'MISSING')
