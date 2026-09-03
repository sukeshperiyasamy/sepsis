"""
mcr_peak_validation.py
Extension analysis for LPS Composite Raman project.

1. Reproduces the NNLS fit from output/processed/*.csv (pure-numpy NNLS,
   no scipy available on this machine) as a sanity check against the
   published model_metrics.xlsx / final_summary_report.txt numbers.
2. Runs a regularized, single-spectrum "soft alternating fit" in the spirit
   of MCR-ALS: because there is only ONE experimental spectrum, canonical
   multi-sample MCR-ALS (which resolves C and S jointly across many mixture
   samples) is not well-posed here. Instead this performs one Tikhonov-
   regularized shape-refinement step, anchored to the DFT reference spectra,
   alternated with an NNLS re-fit of the weights, across a sweep of
   regularization strengths (lambda). This is reported honestly as a
   "regularized / soft alternating refinement (MCR-ALS-inspired, anchored to
   DFT reference shapes)" rather than as textbook MCR-ALS.
3. Validates detected peaks (from output/tables/peak_summary.xlsx) against
   the literature diagnostic Raman peak assignments noted in
   "thesis report.txt" (989 carbohydrate/KDO, 1131 lipid chain,
   1330 phospholipid, 850 glycosidic; from the SERS endotoxin paper).

Outputs:
  output/tables/alternative_fit_comparison.xlsx
  output/tables/peak_literature_validation.xlsx
  output/plots/regularized_fit_vs_nnls.png
"""
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path('.')
OUT = BASE / 'output'
PROC = OUT / 'processed'
TABLES = OUT / 'tables'
PLOTS = OUT / 'plots'

FRAGS = {
    'KDO': PROC / '3-Deoxy-D-Manno-Octulosonic_Acid_processed.csv',
    'Glucosamine': PROC / 'D-glucosamine_processed.csv',
    'Heptose': PROC / 'L-Glycero-D-Manno-Heptose_processed.csv',
    'Myristic Acid': PROC / 'Myristic_Acid_processed.csv',
    'Phosphoric Acid': PROC / 'Phosphoric_acid_processed.csv',
}
EXP = PROC / 'sec-60_power-20_i-30_processed.csv'

GRID = np.arange(200.0, 2000.0 + 1.0, 1.0)


def load_interp(path, col='normalized'):
    d = pd.read_csv(path)
    x = d['raman_shift'].values.astype(float)
    y = d[col].values.astype(float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    return np.interp(GRID, x, y)


def minmax_normalize(y):
    lo, hi = y.min(), y.max()
    if hi - lo < 1e-12:
        return np.zeros_like(y)
    return (y - lo) / (hi - lo)


def nnls_mu(A, b, n_iter=4000, eps=1e-12):
    """Non-negative least squares via multiplicative update (Lee & Seung
    style). A is (m,n) with A>=0 assumed (true here: all spectra are
    intensities). Converges to the NNLS solution for small well-posed
    problems like this 5-component fit."""
    m, n = A.shape
    x = np.full(n, 1.0 / n)
    AtA = A.T @ A
    Atb = A.T @ b
    for _ in range(n_iter):
        den = AtA @ x + eps
        x = np.clip(x * (Atb / den), 0, None)
    return x


def metrics(exp_y, model_y):
    resid = exp_y - model_y
    rmse = float(np.sqrt(np.mean(resid ** 2)))
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((exp_y - exp_y.mean()) ** 2))
    r2 = float(1 - ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    r = float(np.corrcoef(exp_y, model_y)[0, 1])
    return rmse, r2, r, resid


exp_y = load_interp(EXP)
frag_labels = list(FRAGS.keys())
B = np.column_stack([load_interp(p) for p in FRAGS.values()])

# ---------------------------------------------------------------------
# 1. Reproduce plain NNLS fit (sanity check vs published model_metrics.xlsx)
# ---------------------------------------------------------------------
raw_w = nnls_mu(B, exp_y)
w_sum = raw_w.sum()
w_nnls = raw_w / w_sum if w_sum > 1e-12 else raw_w
I_nnls_raw = B @ raw_w
I_nnls_norm = minmax_normalize(I_nnls_raw)
rmse_n, r2_n, r_n, resid_n = metrics(exp_y, I_nnls_norm)

print('=== Reproduced plain NNLS (sanity check) ===')
for lbl, w in zip(frag_labels, w_nnls):
    print(f'  {lbl:18s}: {w*100:6.2f}%')
print(f'  RMSE={rmse_n:.6f}  R2={r2_n:.6f}  r={r_n:.6f}')
print('  (compare to model_metrics.xlsx: RMSE=0.185045 R2=0.179946 r=0.507839)')

# ---------------------------------------------------------------------
# 2. Regularized / soft alternating refinement (MCR-ALS-inspired), lambda sweep
#    S_new = clip(B + outer(residual, C) / (C.C + lambda), 0, None)
#    then re-fit weights C via NNLS against the refined S.
#    lambda is expressed as a multiple of (C.C) -> lam = k * (C.C)
# ---------------------------------------------------------------------
C0 = raw_w.copy()
CtC0 = float(C0 @ C0)
sweep_rows = []
best = None
for k in [50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05]:
    lam = k * CtC0
    model0 = B @ C0
    resid0 = exp_y - model0
    S = B + np.outer(resid0, C0) / (CtC0 + lam)
    S = np.clip(S, 0, None)
    C1 = nnls_mu(S, exp_y)
    model1 = S @ C1
    model1_norm = minmax_normalize(model1)
    rmse1, r2_1, r_1, _ = metrics(exp_y, model1_norm)
    mask = B > 0.05
    rel_dev = np.abs(S - B)[mask] / B[mask]
    max_dev = float(np.max(rel_dev)) if mask.any() else 0.0
    med_dev = float(np.median(rel_dev)) if mask.any() else 0.0
    sweep_rows.append({
        'lambda_multiplier_k': k, 'lambda': lam,
        'RMSE': rmse1, 'R2': r2_1, 'Pearson_r': r_1,
        'max_relative_shape_deviation': max_dev,
        'median_relative_shape_deviation': med_dev,
    })
    print(f'k={k:6.2f}  RMSE={rmse1:.4f}  R2={r2_1:.4f}  r={r_1:.4f}  '
          f'max_dev={max_dev*100:5.1f}%  med_dev={med_dev*100:4.1f}%')

sweep_df = pd.DataFrame(sweep_rows)

candidates = sweep_df[(sweep_df.median_relative_shape_deviation < 0.10) &
                       (sweep_df.max_relative_shape_deviation < 0.25)]
if len(candidates):
    rec = candidates.sort_values('lambda_multiplier_k', ascending=False).iloc[0]
else:
    rec = sweep_df.sort_values('lambda_multiplier_k', ascending=False).iloc[0]

k_rec = float(rec['lambda_multiplier_k'])
lam_rec = k_rec * CtC0
model0 = B @ C0
resid0 = exp_y - model0
S_rec = np.clip(B + np.outer(resid0, C0) / (CtC0 + lam_rec), 0, None)
C_rec = nnls_mu(S_rec, exp_y)
model_rec = S_rec @ C_rec
model_rec_norm = minmax_normalize(model_rec)
rmse_r, r2_r, r_r, resid_r = metrics(exp_y, model_rec_norm)
w_rec = C_rec / C_rec.sum() if C_rec.sum() > 1e-12 else C_rec

print('\n=== Recommended conservative regularized fit ===')
print(f'k={k_rec}, lambda={lam_rec:.4f}')
for lbl, w in zip(frag_labels, w_rec):
    print(f'  {lbl:18s}: {w*100:6.2f}%')
print(f'  RMSE={rmse_r:.6f}  R2={r2_r:.6f}  r={r_r:.6f}')
print(f'  Improvement over plain NNLS: '
      f'RMSE {"-" if rmse_r<rmse_n else "+"}{abs(rmse_n-rmse_r)/rmse_n*100:.1f}%, '
      f'R2 {"+" if r2_r>r2_n else "-"}{abs(r2_r-r2_n)/max(r2_n,1e-9)*100:.1f}%')

# ---------------------------------------------------------------------
TABLES.mkdir(parents=True, exist_ok=True)
with pd.ExcelWriter(TABLES / 'alternative_fit_comparison.xlsx') as xw:
    pd.DataFrame([
        {'model': 'NNLS (reproduced)', 'rmse': rmse_n, 'r2': r2_n, 'pearson_r': r_n,
         **{f'weight_{l}': w for l, w in zip(frag_labels, w_nnls)}},
        {'model': f'Regularized soft fit (k={k_rec}, MCR-ALS-inspired)',
         'rmse': rmse_r, 'r2': r2_r, 'pearson_r': r_r,
         **{f'weight_{l}': w for l, w in zip(frag_labels, w_rec)}},
    ]).to_excel(xw, sheet_name='summary', index=False)
    sweep_df.to_excel(xw, sheet_name='lambda_sweep', index=False)
print(f'\nSaved -> {TABLES/"alternative_fit_comparison.xlsx"}')

PLOTS.mkdir(parents=True, exist_ok=True)
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
axes[0].plot(GRID, exp_y, color='#1D3557', lw=2.0, label='Experimental LPS')
axes[0].plot(GRID, I_nnls_norm, color='#F4A261', lw=1.8, label=f'Plain NNLS (R2={r2_n:.3f})')
axes[0].plot(GRID, model_rec_norm, color='#2A9D8F', lw=1.8, ls='--',
             label=f'Regularized soft fit (R2={r2_r:.3f}, k={k_rec})')
axes[0].set_ylabel('Normalized Intensity')
axes[0].legend(frameon=True)
axes[0].set_title('NNLS vs. regularized soft alternating fit (MCR-ALS-inspired)')

axes[1].plot(sweep_df.lambda_multiplier_k, sweep_df.R2, marker='o', color='#6A0572')
axes[1].axvline(k_rec, color='gray', ls=':', label=f'recommended k={k_rec}')
axes[1].set_xscale('log')
axes[1].invert_xaxis()
axes[1].set_xlabel('Regularization multiplier k  (larger k = more constrained to DFT reference)')
axes[1].set_ylabel('R2 of refined fit')
axes[1].legend(frameon=True)
axes[1].set_title('Regularization sweep: R2 vs. constraint strength\n'
                   '(R2 -> 1 as k -> 0 is overfitting, not physical signal)')
fig.tight_layout()
fig.savefig(PLOTS / 'regularized_fit_vs_nnls.png', dpi=300, bbox_inches='tight')
print(f'Saved -> {PLOTS/"regularized_fit_vs_nnls.png"}')

# ---------------------------------------------------------------------
# 3. Peak validation against literature diagnostic assignments
# ---------------------------------------------------------------------
peaks_xl = pd.ExcelFile(TABLES / 'peak_summary.xlsx')
exp_peaks = peaks_xl.parse('Experimental')
nnls_peaks = peaks_xl.parse('NNLS_Optimized_Composite')

LIT_PEAKS = [
    {'literature_cm-1': 989, 'assignment': 'Carbohydrate (KDO) ring/C-O',
     'source': 'SERS endotoxin paper (main reference, mdpi.com/2079-6374/11/7/234)'},
    {'literature_cm-1': 1131, 'assignment': 'Lipid acyl chain (C-C stretch)',
     'source': 'SERS endotoxin paper'},
    {'literature_cm-1': 1330, 'assignment': 'Phospholipid (CH2 wagging / P-related)',
     'source': 'SERS endotoxin paper'},
    {'literature_cm-1': 850, 'assignment': 'Glycosidic linkage (C-O-C)',
     'source': 'SERS endotoxin paper'},
]

TOL = 25.0


def nearest_peak(df, target):
    if len(df) == 0:
        return None, None
    d = (df['peak_shift_cm-1'] - target).abs()
    i = d.idxmin()
    return float(df.loc[i, 'peak_shift_cm-1']), float(d.loc[i])


def region_dominant_fragment(lo, hi):
    m = (GRID >= lo) & (GRID <= hi)
    if not m.any():
        return 'n/a'
    scores = [float(np.sum(B[m, j]) * w_nnls[j]) for j in range(len(frag_labels))]
    return frag_labels[int(np.argmax(scores))]


val_rows = []
for lp in LIT_PEAKS:
    tgt = lp['literature_cm-1']
    exp_pos, exp_delta = nearest_peak(exp_peaks, tgt)
    model_pos, model_delta = nearest_peak(nnls_peaks, tgt)
    dom = region_dominant_fragment(tgt - 20, tgt + 20)
    val_rows.append({
        'Literature peak (cm-1)': tgt,
        'Literature assignment': lp['assignment'],
        'Nearest experimental peak (cm-1)': exp_pos,
        'Delta exp vs literature (cm-1)': round(exp_delta, 1) if exp_delta is not None else None,
        'Within tolerance (+/-25 cm-1)?': (exp_delta is not None and exp_delta <= TOL),
        'Nearest NNLS-model peak (cm-1)': model_pos,
        'Delta model vs literature (cm-1)': round(model_delta, 1) if model_delta is not None else None,
        'Dominant fragment in this region (NNLS weights)': dom,
        'Source': lp['source'],
    })

val_df = pd.DataFrame(val_rows)
val_df.to_excel(TABLES / 'peak_literature_validation.xlsx', index=False)
print(f'\nSaved -> {TABLES/"peak_literature_validation.xlsx"}')
print(val_df.to_string(index=False))
