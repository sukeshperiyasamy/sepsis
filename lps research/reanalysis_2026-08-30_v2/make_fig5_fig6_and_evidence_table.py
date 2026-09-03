import numpy as np, json, csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.expanduser('~/mnt')
SRC_DIR = os.path.join(BASE, 'mtp', 'lps research', 'reanalysis_2026-08-30_v2')
OUT_DIR = os.path.join(BASE, 'mtp', 'lps research', 'reanalysis_2026-08-30_v3_final')
os.makedirs(OUT_DIR, exist_ok=True)

d = np.load(os.path.join(SRC_DIR, 'arrays_v2.npz'))
grid = d['grid']; exp_norm = d['exp_norm']

with open(os.path.join(SRC_DIR, 'summary_v2.json')) as f:
    S = json.load(f)
summary = S['summary']; matches = S['matches']; unmatched = S['unmatched']

def yval(x):
    return exp_norm[np.searchsorted(grid, x)]

# ============================================================
# Literature bands actually found in the project's own files
# Source: output/tables/peak_literature_validation.xlsx (mtp/lps--main/lps--main)
# "main reference paper" = cited in thesis report.txt as
# "Highly Sensitive Detection and Differentiation of Endotoxins Derived from
#  Bacterial Pathogens by Surface-Enhanced Raman Scattering" (mdpi.com/2079-6374/11/7/234)
# -- NOTE: no local PDF of this exact paper was found in the project files; it is
# cited by URL/title only in thesis report.txt, and the SAME four numbers are
# ALSO attributed elsewhere in the same document to "Wu 2021", a whole-bacterium
# PCA differentiation study explicitly flagged in-document as NOT purified LPS.
# This citation conflict is preserved here, not resolved.
lit_bands = [
    dict(lit=989, assignment='Carbohydrate (KDO) ring/C-O', sample_type_claimed='Purified LPS (claimed) / Wu2021 whole-bacterium (conflicting attribution)'),
    dict(lit=1131, assignment='Lipid acyl chain (C-C stretch)', sample_type_claimed='Purified LPS (claimed) / Wu2021 whole-bacterium (conflicting attribution)'),
    dict(lit=1330, assignment='Phospholipid (CH2 wagging / P-related)', sample_type_claimed='Purified LPS (claimed) / Wu2021 whole-bacterium (conflicting attribution)'),
    dict(lit=850, assignment='Glycosidic linkage (C-O-C)', sample_type_claimed='Purified LPS (claimed) / Wu2021 whole-bacterium (conflicting attribution)'),
]

peak_rows = list(csv.DictReader(open(os.path.join(SRC_DIR, 'peak_table_v2.csv'))))
exp_peaks_all = sorted([float(r['Experimental_peak_cm-1']) for r in peak_rows])

def nearest_exp(lit_val):
    arr = np.array(exp_peaks_all)
    i = int(np.argmin(np.abs(arr - lit_val)))
    return arr[i], arr[i] - lit_val

for b in lit_bands:
    ep, delta = nearest_exp(b['lit'])
    b['nearest_exp'] = ep
    b['delta'] = delta

# ============================================================
# FIGURE 5 -- Experimental LPS vs literature (literature-supported bands only)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5.8))
ax.plot(grid, exp_norm, color='#333333', lw=1.1, label='Experimental LPS powder spectrum')
lit_bands_sorted = sorted(lit_bands, key=lambda b: b['lit'])
offsets = [(-10, 20), (10, 70), (-10, 20), (10, 70)]
for i, b in enumerate(lit_bands_sorted):
    within = abs(b['delta']) <= 25
    col = '#1a9850' if within else '#d73027'
    y = yval(b['nearest_exp'])
    ax.axvline(b['lit'], color='#4575b4', ls=':', lw=1.0, alpha=0.7)
    ax.plot(b['nearest_exp'], y, marker='o', ms=9, color=col, mec='black', zorder=5)
    ox, oy = offsets[i % len(offsets)]
    ax.annotate(f"lit {b['lit']}\nexp {b['nearest_exp']:.0f} (Δ={b['delta']:+.0f})",
                (b['nearest_exp'], y), textcoords='offset points', xytext=(ox, oy),
                ha='center', fontsize=7.5,
                arrowprops=dict(arrowstyle='-', color='#888888', lw=0.6))
from matplotlib.lines import Line2D
legend_elems = [
    Line2D([0],[0], color='#333333', lw=1.1, label='Experimental LPS powder spectrum'),
    Line2D([0],[0], color='#4575b4', ls=':', lw=1.0, label='Literature band position (project-cited)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#1a9850', markeredgecolor='black', markersize=9, label='Within ±25 cm⁻¹ (project tolerance)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#d73027', markeredgecolor='black', markersize=9, label='Outside ±25 cm⁻¹'),
]
ax.legend(handles=legend_elems, loc='upper right', fontsize=8)
ax.set_xlabel('Raman shift (cm$^{-1}$)')
ax.set_ylabel('Normalized intensity (a.u.)')
ax.set_xlim(200, 2000)
ax.set_ylim(0, 1.45)
ax.set_title('Figure 5. Experimental LPS Powder Spectrum vs. Literature-Cited Bands\n'
             'All 4 bands are the only literature LPS Raman peak positions found in the project\'s own files (thesis report.txt / peak_literature_validation.xlsx).\n'
             'Sample-type attribution of this 4-band table is INTERNALLY CONFLICTING in the project documentation (see report Section 5) -- shown as-is, not resolved.',
             fontsize=10.5)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'Figure5_experimental_vs_literature.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 6 -- Evidence summary workflow
# ============================================================
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.axis('off')
stages = [
    ('LPS Powder\nRaman\n(measured)', 'available', '43 major peaks\ndetected, 200-2000 cm⁻¹'),
    ('DFT Fragment\nSupport', 'available', f"{summary['n_matched_confident']} confident +\n{summary['n_matched_uncertain']} uncertain matches"),
    ('Literature', 'partial', '2/4 cited peaks\nmatch within tol.;\ncitation conflict found'),
    ('LPS SERS', 'not available', 'Not yet performed\n(planned next step)'),
    ('Blank-substrate\nControl', 'not available', 'No LPS-matched\nblank exists'),
    ('Final\nInterpretation', 'conservative', 'DFT-supported\ncandidate bands only\n(not biomarkers)'),
]
colors_map = {'available': '#1a9850', 'partial': '#e9a227', 'not available': '#d73027', 'conservative': '#4575b4'}
n = len(stages)
xs = np.linspace(0.06, 0.94, n)
y = 0.55
box_w, box_h = 0.12, 0.32
for i, (label, status, note) in enumerate(stages):
    x = xs[i]
    color = colors_map[status]
    rect = plt.Rectangle((x-box_w/2, y-box_h/2), box_w, box_h, facecolor=color, edgecolor='black', alpha=0.85, zorder=3, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=4, transform=ax.transAxes)
    ax.text(x, y-box_h/2-0.10, note, ha='center', va='top', fontsize=7.5, color='#333333', transform=ax.transAxes)
    ax.text(x, y+box_h/2+0.09, status.upper(), ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=color, transform=ax.transAxes)
    if i < n-1:
        ax.annotate('', xy=(xs[i+1]-box_w/2-0.005, y), xytext=(x+box_w/2+0.005, y),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle='->', color='#555555', lw=1.4))
ax.set_title('Figure 6. LPS Evidence Workflow -- Current Status\n'
             'Green = data exists and was analyzed. Amber = partial/conflicting. Red = not currently available in the project dataset.',
             fontsize=11)
ax.set_xlim(0,1); ax.set_ylim(0,1)
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, 'Figure6_evidence_workflow.png'), dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FINAL EVIDENCE TABLE
# ============================================================
confident = [m for m in matches if m['classification'] == 'Matched - confident']

evidence_rows = []
# Rows from confident DFT-matched bands (no literature/SERS support)
for m in sorted(confident, key=lambda x: x['exp']):
    evidence_rows.append(dict(
        exp_band=round(m['exp'],1),
        dft_band=f"{m['dft']:.1f} ({m['frag'].replace('_',' ')})",
        delta=round(m['delta'],1),
        lit_band='Not available',
        lit_assignment='No literature band found within a reasonable tolerance of this position',
        sers_band='Not available',
        blank_status='Not available (no LPS-specific blank-substrate control exists)',
        classification='Candidate',
    ))
# Rows from literature-cited bands (cross-referenced to nearest experimental + whether DFT supports that region)
for b in lit_bands:
    ep = b['nearest_exp']
    # is this exp peak DFT-matched (any tier)?
    row = next((r for r in peak_rows if abs(float(r['Experimental_peak_cm-1']) - ep) < 0.5), None)
    dft_band = 'Not available'
    if row and row['Classification'] != 'Unmatched':
        dft_band = f"{row['DFT_mode_cm-1']} ({row['Component_fragment']})"
    within_tol = abs(b['delta']) <= 25
    if within_tol and dft_band != 'Not available':
        cls = 'Strong candidate'
    elif within_tol:
        cls = 'Candidate'
    else:
        cls = 'Unconfirmed'
    evidence_rows.append(dict(
        exp_band=round(ep,1),
        dft_band=dft_band,
        delta=round(float(row['Delta_cm-1_(Exp-DFT)']),1) if row and row['Classification']!='Unmatched' else 'N/A',
        lit_band=b['lit'],
        lit_assignment=b['assignment'] + ' [sample-type attribution conflicting -- see Section 5]',
        sers_band='Not available',
        blank_status='Not available (no LPS-specific blank-substrate control exists)',
        classification=cls,
    ))

with open(os.path.join(OUT_DIR, 'final_evidence_table.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['LPS_experimental_band_cm-1','DFT_band_fragment','Delta_Exp_minus_DFT_cm-1',
                'Literature_band_cm-1','Literature_assignment','SERS_band','Blank_substrate_status','Final_evidence_classification'])
    for r in evidence_rows:
        w.writerow([r['exp_band'], r['dft_band'], r['delta'], r['lit_band'], r['lit_assignment'], r['sers_band'], r['blank_status'], r['classification']])

print('Figures + evidence table written to', OUT_DIR)
print(json.dumps(lit_bands, indent=2, default=str))
for r in evidence_rows:
    print(r)
