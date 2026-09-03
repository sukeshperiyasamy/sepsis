import numpy as np, json, csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.dirname(os.path.abspath(__file__))
os.chdir(OUT)

# ---------------- load cached arrays + tables ----------------
npz = np.load('arrays_cache.npz')
grid = npz['grid']; exp_norm = npz['exp_norm']; composite_nnls = npz['composite_nnls']
exp_peaks_idx = npz['exp_peaks_idx']; exp_peaks = npz['exp_peaks']; exp_prom = npz['exp_prom']

def read_csv(fn):
    with open(fn, newline='') as f:
        return list(csv.DictReader(f))

exp_all = read_csv('experimental_peaks_all.csv')
matched = read_csv('reference_band_candidates.csv')
threeway = read_csv('threeway_comparison.csv')
summary = json.load(open('summary.json'))['summary']

matched_by_exp = {float(r['exp_peak_cm-1']): r for r in matched}
matched_exp_vals = set(matched_by_exp.keys())
unmatched_rows = [r for r in exp_all if r['has_dft_match_within_tol'] == 'no']

FS = 'DejaVu Sans'
plt.rcParams.update({'font.size': 11, 'font.family': FS, 'axes.spines.top': False, 'axes.spines.right': False})

# ================= FIGURE 1: experimental spectrum only =================
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.plot(grid, exp_norm, color='#1a1a1a', lw=1.1)
ax.plot(exp_peaks, exp_norm[exp_peaks_idx], 'o', ms=3.2, color='#c0392b', mfc='#c0392b', mec='none', zorder=5)
ax.set_xlim(200, 2000)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel('Raman shift (cm$^{-1}$)')
ax.set_ylabel('Normalized intensity')
ax.set_title('LPS powder Raman spectrum (E. coli O111:B4, 60 s / 20% / 30 acc.)', fontsize=11)
plt.tight_layout()
plt.savefig('Figure1_experimental_spectrum.png', dpi=200)
plt.close(fig)

# ================= FIGURE 2: experimental vs DFT composite, matched/unmatched marked =================
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(grid, exp_norm, color='#1a1a1a', lw=1.1, label='Experimental (powder)')
ax.plot(grid, composite_nnls, color='#c0392b', lw=1.1, label='DFT fragment composite (NNLS)')
for r in exp_all:
    x = float(r['exp_peak_cm-1'])
    y = exp_norm[np.argmin(np.abs(grid - x))]
    if r['has_dft_match_within_tol'] == 'yes':
        ax.plot(x, y, 'o', ms=5, mfc='#1e8449', mec='white', mew=0.5, zorder=6)
    else:
        ax.plot(x, y, 'x', ms=5.5, color='#7f8c8d', mew=1.3, zorder=6)
handles = [
    plt.Line2D([], [], color='#1a1a1a', lw=1.1, label='Experimental (powder)'),
    plt.Line2D([], [], color='#c0392b', lw=1.1, label='DFT fragment composite'),
    plt.Line2D([], [], marker='o', ms=6, mfc='#1e8449', mec='white', linestyle='None', label='Matched band (n=26)'),
    plt.Line2D([], [], marker='x', ms=6, color='#7f8c8d', linestyle='None', label='Unmatched band (n=17)'),
]
ax.legend(handles=handles, loc='upper right', fontsize=8.5, frameon=False)
ax.set_xlim(200, 2000); ax.set_ylim(-0.02, 1.05)
ax.set_xlabel('Raman shift (cm$^{-1}$)'); ax.set_ylabel('Normalized intensity')
ax.set_title('Experimental LPS powder Raman vs. DFT fragment composite', fontsize=11)
plt.tight_layout()
plt.savefig('Figure2_experimental_vs_dft.png', dpi=200)
plt.close(fig)

# ================= FIGURE 3: 4 High-confidence bands, zoomed =================
high_pairs = [(721.0, 717.9, 'KDO'), (748.0, 750.4, 'Heptose'), (1659.0, 1659.1, 'KDO'), (1693.0, 1692.1, 'KDO')]
fig, axes = plt.subplots(2, 2, figsize=(9, 6.4))
for ax, (ep, dp, frag) in zip(axes.flat, high_pairs):
    lo, hi = ep - 30, ep + 30
    m = (grid >= lo) & (grid <= hi)
    ax.plot(grid[m], exp_norm[m], color='#1a1a1a', lw=1.3)
    yv = exp_norm[np.argmin(np.abs(grid - ep))]
    ax.axvline(ep, color='#1e8449', lw=1.1, ls='-', alpha=0.85)
    ax.axvline(dp, color='#c0392b', lw=1.1, ls='--', alpha=0.85)
    ax.plot([ep], [yv], 'o', color='#1e8449', ms=5, zorder=6)
    delta = ep - dp
    ax.set_title(f'{ep:.0f} cm$^{{-1}}$ (exp) vs {dp:.1f} cm$^{{-1}}$ (DFT, {frag})\n$\\Delta$ = {delta:+.1f} cm$^{{-1}}$ — High confidence', fontsize=9.5)
    ax.set_xlabel('Raman shift (cm$^{-1}$)', fontsize=9)
    ax.set_ylabel('Norm. intensity', fontsize=9)
    ax.tick_params(labelsize=8)
handles = [plt.Line2D([], [], color='#1e8449', label='Experimental peak'),
           plt.Line2D([], [], color='#c0392b', ls='--', label='DFT-predicted mode')]
fig.legend(handles=handles, loc='lower center', ncol=2, fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.suptitle('High-confidence LPS DFT-supported reference bands', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig('Figure3_high_confidence_bands.png', dpi=200)
plt.close(fig)

# ================= FIGURE 4: literature vs experimental vs DFT, convergence points =================
convergence_exp = [542, 674, 721, 972, 1124, 1354, 1659]
# gather literature/DFT values that map to each of these experimental positions from threeway_comparison.csv
groups = {v: {'lit': [], 'dft': None} for v in convergence_exp}
for r in threeway:
    ov = r['our_powder_cm-1']
    if ov == '-':
        continue
    ov = float(ov)
    nearest = min(convergence_exp, key=lambda v: abs(v - ov))
    if abs(nearest - ov) <= 2:
        groups[nearest]['lit'].append(float(r['literature_cm-1']))
        dstr = r['dft_supported_cm-1_(fragment,confidence)']
        if dstr != '-':
            groups[nearest]['dft'] = dstr

fig, ax = plt.subplots(figsize=(10, 5.0))
lanes = {'Literature': 2, 'Experimental powder': 1, 'DFT-supported': 0}
colors = plt.cm.tab10(np.linspace(0, 1, len(convergence_exp)))
for ci, ev in enumerate(convergence_exp):
    col = colors[ci]
    dstr = groups[ev]['dft']
    dval = float(dstr.split(' ')[0]) if dstr else None
    for lv in groups[ev]['lit']:
        ax.plot(lv, lanes['Literature'], '^', ms=8, color=col, mec='black', mew=0.4, zorder=5)
        ax.plot([lv, ev], [2, 1], color=col, lw=0.6, alpha=0.3, zorder=1)
    ax.plot(ev, lanes['Experimental powder'], 'o', ms=8, color=col, mec='black', mew=0.4, zorder=5)
    if dval is not None:
        ax.plot(dval, lanes['DFT-supported'], 's', ms=8, color=col, mec='black', mew=0.4, zorder=5)
        ax.plot([ev, dval], [1, 0], color=col, lw=0.6, alpha=0.3, zorder=1)
    ax.annotate(f'{ev:.0f}', (ev, lanes['Experimental powder']), textcoords='offset points', xytext=(0, -16), fontsize=8, ha='center', color='#333333')

ax.set_yticks([0, 1, 2]); ax.set_yticklabels(['DFT-supported', 'Experimental\npowder', 'Literature'])
ax.set_ylim(-0.7, 2.9)
ax.set_xlabel('Raman shift (cm$^{-1}$)')
handles = [plt.Line2D([], [], marker='^', color='gray', linestyle='None', label='Literature (4 project sources)'),
           plt.Line2D([], [], marker='o', color='gray', linestyle='None', label='Our experimental powder peak'),
           plt.Line2D([], [], marker='s', color='gray', linestyle='None', label='DFT-supported band')]
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=3, fontsize=8.5, frameon=False)
fig.suptitle('Literature vs. experimental powder vs. DFT -- strongest convergence points', fontsize=11, y=1.02)
plt.tight_layout()
plt.savefig('Figure4_literature_vs_exp_vs_dft.png', dpi=200, bbox_inches='tight')
plt.close(fig)

# ================= FIGURE 5: matched vs unmatched =================
fig, ax = plt.subplots(figsize=(10, 3.6))
for r in exp_all:
    x = float(r['exp_peak_cm-1']); p = float(r['prominence'])
    if r['has_dft_match_within_tol'] == 'yes':
        ax.plot(x, p, 'o', ms=6, mfc='#1e8449', mec='white', mew=0.5, zorder=5)
    else:
        ax.plot(x, p, 'x', ms=7, color='#7f8c8d', mew=1.4, zorder=5)
handles = [plt.Line2D([], [], marker='o', ms=7, mfc='#1e8449', mec='white', linestyle='None', label=f'Matched (n={len(matched_exp_vals)})'),
           plt.Line2D([], [], marker='x', ms=7, color='#7f8c8d', linestyle='None', label=f'No DFT match within ±15 cm$^{{-1}}$ (n={len(unmatched_rows)})')]
ax.legend(handles=handles, loc='upper right', fontsize=9, frameon=False)
ax.set_xlim(200, 2000)
ax.set_xlabel('Raman shift (cm$^{-1}$)'); ax.set_ylabel('Peak prominence')
ax.set_title('Matched vs. unmatched major experimental LPS bands', fontsize=11)
plt.tight_layout()
plt.savefig('Figure5_matched_vs_unmatched.png', dpi=200)
plt.close(fig)

# ================= FIGURE 6: workflow diagram =================
fig, ax = plt.subplots(figsize=(4.4, 10.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 22); ax.axis('off')

steps = [
    ('Literature\n(LPS Raman/SERS band reports)', 'done'),
    ('Experimental LPS powder Raman\n(E. coli O111:B4, 785 nm, optimized condition)', 'done'),
    ('DFT fragment calculations\n(KDO, Glucosamine, Heptose,\nMyristic Acid, Phosphoric Acid)', 'done'),
    ('One-to-one peak matching\n(Hungarian assignment, ±15 cm$^{-1}$)', 'done'),
    ('DFT-supported reference bands\n(26 matches; 4 High confidence)', 'done'),
    ('LPS SERS testing\non fabricated Ag/Si substrate', 'pending'),
    ('Blank-substrate validation', 'pending'),
]
n = len(steps)
y0, dy = 20.5, 3.15
box_w, box_h = 8.6, 2.35
for i, (text, state) in enumerate(steps):
    y = y0 - i * dy
    if state == 'done':
        fc, ec, tc = '#EAF6EF', '#1e8449', '#1e8449'
    else:
        fc, ec, tc = '#FDEDEC', '#c0392b', '#c0392b'
    box = FancyBboxPatch((0.7, y - box_h/2), box_w, box_h, boxstyle='round,pad=0.12,rounding_size=0.18',
                          linewidth=1.6, edgecolor=ec, facecolor=fc)
    ax.add_patch(box)
    ax.text(5.0, y + 0.32, text, ha='center', va='center', fontsize=9.3, color='#1a1a1a')
    label = 'Established in project data' if state == 'done' else 'Not yet validated'
    ax.text(5.0, y - 0.75, label, ha='center', va='center', fontsize=8.3, color=tc, style='italic')
    if i < n - 1:
        ax.annotate('', xy=(5.0, y - box_h/2 - 0.15), xytext=(5.0, y - dy + box_h/2 + 0.15),
                    arrowprops=dict(arrowstyle='-|>', color='#555555', lw=1.3))

plt.tight_layout()
plt.savefig('Figure6_evidence_workflow.png', dpi=200)
plt.close(fig)

# ================= Table 1: all 43 peaks merged =================
with open('Table1_all_experimental_peaks.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Experimental_Raman_cm-1', 'DFT_Raman_cm-1', 'Delta_cm-1', 'Fragment', 'Confidence'])
    for r in sorted(exp_all, key=lambda x: float(x['exp_peak_cm-1'])):
        ev = float(r['exp_peak_cm-1'])
        m = matched_by_exp.get(ev)
        if m:
            w.writerow([f"{ev:.0f}", m['dft_peak_cm-1_scaled'], m['delta_cm-1'], m['fragment'].replace('_',' '), m['confidence']])
        else:
            w.writerow([f"{ev:.0f}", '-', '-', '-', 'Unmatched'])

print('figures and Table1 written')
print('unmatched count', len(unmatched_rows), 'matched count', len(matched_exp_vals))
