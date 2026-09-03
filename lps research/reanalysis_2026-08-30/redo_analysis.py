import numpy as np, json, csv, os
from scipy.optimize import nnls, linear_sum_assignment
from scipy.signal import savgol_filter, find_peaks
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openpyxl

BASE = os.path.expanduser('~/mnt')
FRAG_DIR = os.path.join(BASE, 'mtp', 'lps research', 'lps sim')
EXP_XLSX = os.path.join(BASE, 'mtp', 'lps--main', 'lps--main', 'sec-60_power-20_i-30.xlsx')
OUT_DIR = os.path.join(BASE, 'mtp', 'lps research', 'reanalysis_2026-08-30')

SCALE = 0.9613
GRID_MIN, GRID_MAX, GRID_STEP = 200.0, 2000.0, 1.0
FWHM = 20.0
TOL = 15.0
grid = np.arange(GRID_MIN, GRID_MAX + GRID_STEP, GRID_STEP)

FRAG_FILES = {
    'KDO': '3-Deoxy-D-Manno-Octulosonic Acid_raman_act.txt',
    'Glucosamine': 'D-glucosamine-opt_raman_act.txt',
    'Heptose': 'L-Glycero-D-Manno-Heptose-opt_raman_act.txt',
    'Myristic_Acid': 'Myristic Acid-opt_raman_act.txt',
    'Phosphoric_Acid': 'Phosphoric acid-opt_raman_act.txt',
}

def parse_gaussian_txt(path):
    with open(path) as f:
        lines = f.readlines()
    peak_freqs, peak_acts = [], []
    curve_x, curve_y = [], []
    section = None
    for line in lines:
        if 'Peak information' in line:
            section = 'peak'; continue
        if 'Plot Curve' in line:
            section = 'curve'; continue
        s = line.strip().lstrip('#').strip()
        if not s:
            continue
        parts = s.split()
        try:
            vals = [float(p) for p in parts]
        except ValueError:
            continue
        if section == 'peak' and len(vals) >= 2:
            peak_freqs.append(vals[0]); peak_acts.append(vals[1])
        elif section == 'curve' and len(vals) >= 2:
            curve_x.append(vals[0]); curve_y.append(vals[1])
    return np.array(peak_freqs), np.array(peak_acts), np.array(curve_x), np.array(curve_y)

def gaussian_broaden(freqs, acts, grid_, fwhm):
    sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    out = np.zeros_like(grid_)
    for f, a in zip(freqs, acts):
        out += a * np.exp(-0.5 * ((grid_ - f) / sigma) ** 2)
    return out

def minmax(y):
    lo, hi = float(np.min(y)), float(np.max(y))
    if hi - lo < 1e-12:
        return np.zeros_like(y)
    return (y - lo) / (hi - lo)

def baseline_als(y, lam=1e5, p=0.01, niter=10):
    L = len(y)
    D = diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    D = lam * D.dot(D.transpose())
    w = np.ones(L)
    W = diags(w, 0, shape=(L, L))
    z = y.copy()
    for i in range(niter):
        W.setdiag(w)
        Z = W + D
        z = spsolve(Z.tocsc(), w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z

def metrics(a, b):
    rmse = float(np.sqrt(np.mean((a - b) ** 2)))
    ss_res = float(np.sum((a - b) ** 2)); ss_tot = float(np.sum((a - a.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    r = float(np.corrcoef(a, b)[0, 1])
    return rmse, r2, r

# ---------------- fragments ----------------
frag_data = {}
for name, fn in FRAG_FILES.items():
    path = os.path.join(FRAG_DIR, fn)
    pf, pa, cx, cy = parse_gaussian_txt(path)
    pf_scaled = pf * SCALE
    curve_raw = gaussian_broaden(pf_scaled, pa, grid, FWHM)
    frag_data[name] = dict(peak_freq=pf_scaled, peak_act=pa,
                            curve_raw=curve_raw, curve_norm=minmax(curve_raw),
                            n_raw_peaks=int(len(pf)))

# ---------------- experimental ----------------
wb = openpyxl.load_workbook(EXP_XLSX, read_only=True, data_only=True)
ws = wb['Sheet1']
rows = list(ws.iter_rows(min_row=2, values_only=True))
raman_shift, intensity = [], []
for r in rows:
    if r[2] is not None and r[3] is not None:
        raman_shift.append(r[2]); intensity.append(r[3])
raman_shift = np.array(raman_shift, dtype=float)
intensity = np.array(intensity, dtype=float)
order = np.argsort(raman_shift)
raman_shift = raman_shift[order]; intensity = intensity[order]

native_min, native_max = float(raman_shift.min()), float(raman_shift.max())

mask = (raman_shift >= GRID_MIN) & (raman_shift <= GRID_MAX)
rs_w = raman_shift[mask]; int_w = intensity[mask]
exp_on_grid_raw = np.interp(grid, rs_w, int_w)

baseline = baseline_als(exp_on_grid_raw)
corrected = exp_on_grid_raw - baseline
corrected[corrected < 0] = 0
smoothed = savgol_filter(corrected, 11, 3)
exp_norm = minmax(smoothed)

# also compute the OLD (buggy) pipeline for side-by-side comparison:
# normalize over native full range BEFORE windowing
old_norm_full = minmax(intensity)
old_exp_on_grid = np.interp(grid, raman_shift, old_norm_full)

# ---------------- NNLS refit (corrected pipeline) ----------------
frag_names = list(FRAG_FILES.keys())
B = np.column_stack([frag_data[n]['curve_norm'] for n in frag_names])
w_opt, nnls_res = nnls(B, exp_norm)
w_sum = w_opt.sum()
w_opt_frac = (w_opt / w_sum) if w_sum > 0 else w_opt
composite_nnls_raw = B @ w_opt
composite_nnls = minmax(composite_nnls_raw)

B_eq_raw = np.mean(B, axis=1)
composite_eq = minmax(B_eq_raw)

rmse_n, r2_n, r_n = metrics(exp_norm, composite_nnls)
rmse_e, r2_e, r_e = metrics(exp_norm, composite_eq)

# also fit NNLS on the OLD (buggy) exp normalization, to show how much the metric swings
w_opt_old, _ = nnls(B, old_exp_on_grid)
composite_nnls_old = minmax(B @ w_opt_old) if w_opt_old.sum() > 0 else B @ w_opt_old
rmse_old, r2_old, r_old = metrics(old_exp_on_grid, composite_nnls_old)

# ---------------- peak detection on corrected experimental ----------------
exp_peaks_idx, exp_props = find_peaks(exp_norm, prominence=0.08, distance=10)
exp_peaks = grid[exp_peaks_idx]
exp_prom = exp_props['prominences']

# ---------------- DFT candidate discrete peaks per fragment ----------------
dft_candidates = []
for name, d in frag_data.items():
    pf = d['peak_freq']; pa = d['peak_act']
    m = (pf >= GRID_MIN) & (pf <= GRID_MAX)
    pf_w = pf[m]; pa_w = pa[m]
    if len(pa_w) == 0:
        continue
    thresh = 0.05 * pa_w.max()
    keep = pa_w >= thresh
    for f, a in zip(pf_w[keep], pa_w[keep]):
        dft_candidates.append((float(f), name, float(a)))

# ---------------- one-to-one Hungarian matching within tolerance ----------------
n_exp = len(exp_peaks); n_dft = len(dft_candidates)
BIG = 1e6
cost = np.full((n_exp, n_dft), BIG)
for i, ep in enumerate(exp_peaks):
    for j, (df, frag, act) in enumerate(dft_candidates):
        dd = abs(ep - df)
        if dd <= TOL:
            cost[i, j] = dd
matches = []
if n_exp > 0 and n_dft > 0:
    row_ind, col_ind = linear_sum_assignment(cost)
    for i, j in zip(row_ind, col_ind):
        if cost[i, j] < BIG:
            ep = exp_peaks[i]; df, frag, act = dft_candidates[j]
            delta = float(ep - df)
            frags_within = sorted(set(fr for (f2, fr, a2) in dft_candidates if abs(ep - f2) <= TOL))
            m = dict(exp=float(ep), dft=float(df), delta=delta, frag=frag,
                     exp_prominence=float(exp_prom[i]), n_frag_within_tol=len(frags_within),
                     frags_within=frags_within)
            ad = abs(delta)
            unique = m['n_frag_within_tol'] == 1
            if ad <= 5 and unique:
                m['confidence'] = 'High'
            elif ad <= 10:
                m['confidence'] = 'Moderate'
            elif ad <= 15:
                m['confidence'] = 'Low'
            else:
                m['confidence'] = 'Reject'
            matches.append(m)

matched_ok = [m for m in matches if m['confidence'] != 'Reject']
deltas = np.array([m['delta'] for m in matched_ok]) if matched_ok else np.array([])
mae = float(np.mean(np.abs(deltas))) if len(deltas) else None
rmse_peaks = float(np.sqrt(np.mean(deltas ** 2))) if len(deltas) else None

summary = dict(
    n_exp_peaks_detected=int(n_exp),
    n_dft_candidates=int(n_dft),
    n_matches_within_tol=int(len(matches)),
    n_defensible_matches=int(len(matched_ok)),
    n_high=int(sum(1 for m in matched_ok if m['confidence']=='High')),
    n_moderate=int(sum(1 for m in matched_ok if m['confidence']=='Moderate')),
    n_low=int(sum(1 for m in matched_ok if m['confidence']=='Low')),
    mae_matched=mae,
    rmse_matched=rmse_peaks,
    tolerance_cm1=TOL,
    fit_corrected=dict(rmse=rmse_n, r2=r2_n, r=r_n, weights_frac=dict(zip(frag_names, w_opt_frac.tolist()))),
    fit_equal_weight_corrected=dict(rmse=rmse_e, r2=r2_e, r=r_e),
    fit_old_buggy_pipeline=dict(rmse=rmse_old, r2=r2_old, r=r_old, published_rmse=0.185045, published_r2=0.179946, published_r=0.507839),
    native_exp_range=[native_min, native_max],
    fragment_raw_peak_counts={n: frag_data[n]['n_raw_peaks'] for n in frag_names},
)

with open(os.path.join(OUT_DIR, 'summary.json'), 'w') as f:
    json.dump(dict(summary=summary, matches=matches), f, indent=2)

with open(os.path.join(OUT_DIR, 'reference_band_candidates.csv'), 'w', newline='') as f:
    wcsv = csv.writer(f)
    wcsv.writerow(['exp_peak_cm-1', 'dft_peak_cm-1_scaled', 'delta_cm-1', 'fragment', 'other_fragments_within_tol', 'exp_prominence', 'confidence'])
    for m in sorted(matches, key=lambda x: x['exp']):
        others = [fr for fr in m['frags_within'] if fr != m['frag']]
        wcsv.writerow([round(m['exp'],1), round(m['dft'],1), round(m['delta'],1), m['frag'], ';'.join(others), round(m['exp_prominence'],4), m['confidence']])

with open(os.path.join(OUT_DIR, 'experimental_peaks_all.csv'), 'w', newline='') as f:
    wcsv = csv.writer(f)
    wcsv.writerow(['exp_peak_cm-1', 'prominence', 'has_dft_match_within_tol'])
    matched_exp_positions = set(round(m['exp'],1) for m in matches)
    for ep, pr in zip(exp_peaks, exp_prom):
        wcsv.writerow([round(float(ep),1), round(float(pr),4), 'yes' if round(float(ep),1) in matched_exp_positions else 'no'])

# ---------------- plot ----------------
fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={'height_ratios':[3,1]})
ax = axes[0]
ax.plot(grid, exp_norm, label='Experimental (corrected pipeline)', color='black', lw=1.3)
ax.plot(grid, composite_nnls, label=f'DFT NNLS composite (R2={r2_n:.3f})', color='crimson', lw=1.3)
for m in matched_ok:
    ax.axvline(m['exp'], color='gray', alpha=0.15, lw=0.8)
ax.scatter(exp_peaks, exp_norm[exp_peaks_idx], color='black', s=14, zorder=5)
ax.set_ylabel('Normalized intensity')
ax.legend(loc='upper right', fontsize=9)
ax.set_title('LPS: experimental powder Raman vs DFT fragment-composite (corrected pipeline)')
axr = axes[1]
axr.plot(grid, exp_norm - composite_nnls, color='steelblue', lw=0.9)
axr.axhline(0, color='k', lw=0.6)
axr.set_ylabel('Residual')
axr.set_xlabel('Raman shift (cm$^{-1}$)')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'experimental_vs_dft_composite.png'), dpi=160)

print('DONE')

np.savez(os.path.join(OUT_DIR, 'arrays_cache.npz'),
         grid=grid, exp_norm=exp_norm, composite_nnls=composite_nnls, composite_eq=composite_eq,
         exp_peaks_idx=exp_peaks_idx, exp_peaks=exp_peaks, exp_prom=exp_prom)

print(json.dumps(summary, indent=2))
