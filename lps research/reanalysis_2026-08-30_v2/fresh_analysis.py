import numpy as np, json, csv, os
from scipy.optimize import nnls, linear_sum_assignment
from scipy.signal import savgol_filter, find_peaks
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from scipy.stats import pearsonr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openpyxl

BASE = os.path.expanduser('~/mnt')
FRAG_DIR = os.path.join(BASE, 'mtp', 'lps research', 'lps sim')
EXP_XLSX = os.path.join(BASE, 'mtp', 'lps--main', 'lps--main', 'sec-60_power-20_i-30.xlsx')
OUT_DIR = os.path.join(BASE, 'mtp', 'lps research', 'reanalysis_2026-08-30_v2')

SCALE = 0.9613
GRID_MIN, GRID_MAX, GRID_STEP = 200.0, 2000.0, 1.0
FWHM = 20.0          # for visualization broadening ONLY -- matching uses discrete modes
TOL = 15.0           # max matching distance, cm-1
CONF_DELTA = 5.0     # "matched-confident" delta threshold
ACT_FRAC = 0.05       # DFT candidate activity threshold, fraction of each fragment's own max
PROM = 0.08          # experimental peak prominence threshold
MIN_SPACING = 10      # cm-1, min spacing between experimental peaks

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

# ============================================================
# STEP 1 -- verify and load DFT fragment data; record discrete vs broadened
# ============================================================
frag_report = {}
frag_data = {}
for name, fn in FRAG_FILES.items():
    path = os.path.join(FRAG_DIR, fn)
    exists = os.path.isfile(path)
    pf, pa, cx, cy = parse_gaussian_txt(path)
    has_discrete = len(pf) > 0
    has_broadened_native = len(cx) > 0
    frag_report[name] = dict(file=fn, exists=exists, n_discrete_modes=int(len(pf)),
                              has_native_broadened_curve=bool(has_broadened_native),
                              native_curve_points=int(len(cx)))
    pf_scaled = pf * SCALE
    vis_curve = gaussian_broaden(pf_scaled, pa, grid, FWHM)  # for plotting/overlay ONLY
    frag_data[name] = dict(peak_freq=pf_scaled, peak_act=pa, vis_curve_raw=vis_curve, vis_curve_norm=minmax(vis_curve))

# ============================================================
# STEP 2 -- load and justify the experimental dataset
# ============================================================
wb = openpyxl.load_workbook(EXP_XLSX, read_only=True, data_only=True)
ws = wb['Sheet1']
rows = list(ws.iter_rows(min_row=2, values_only=True))
raman_shift, intensity = [], []
meta = {}
for i, r in enumerate(rows[:5]):
    if r[0] is not None:
        meta[str(r[0])] = r[1]
for r in rows:
    if r[2] is not None and r[3] is not None:
        raman_shift.append(r[2]); intensity.append(r[3])
raman_shift = np.array(raman_shift, dtype=float)
intensity = np.array(intensity, dtype=float)
order = np.argsort(raman_shift)
raman_shift = raman_shift[order]; intensity = intensity[order]
native_min, native_max = float(raman_shift.min()), float(raman_shift.max())

# ============================================================
# STEP 3 -- preprocessing: window -> baseline -> smooth -> normalize (in that order)
# ============================================================
mask = (raman_shift >= GRID_MIN) & (raman_shift <= GRID_MAX)
rs_w = raman_shift[mask]; int_w = intensity[mask]
exp_on_grid_raw = np.interp(grid, rs_w, int_w)
baseline = baseline_als(exp_on_grid_raw)
corrected = exp_on_grid_raw - baseline
corrected[corrected < 0] = 0
smoothed = savgol_filter(corrected, 11, 3)
exp_norm = minmax(smoothed)

# ============================================================
# STEP 4 -- experimental peak detection (major bands only)
# ============================================================
exp_peaks_idx, exp_props = find_peaks(exp_norm, prominence=PROM, distance=MIN_SPACING)
exp_peaks = grid[exp_peaks_idx]
exp_prom = exp_props['prominences']

# ============================================================
# STEP 5 -- DFT candidate discrete modes per fragment (NOT a dense grid)
# ============================================================
dft_candidates = []  # (freq, fragment, activity)
for name, d in frag_data.items():
    pf = d['peak_freq']; pa = d['peak_act']
    m = (pf >= GRID_MIN) & (pf <= GRID_MAX)
    pf_w = pf[m]; pa_w = pa[m]
    if len(pa_w) == 0:
        continue
    thresh = ACT_FRAC * pa_w.max()
    keep = pa_w >= thresh
    for f, a in zip(pf_w[keep], pa_w[keep]):
        dft_candidates.append((float(f), name, float(a)))

# ============================================================
# STEP 6 -- one-to-one Hungarian matching, exp peaks <-> DISCRETE DFT modes
# ============================================================
n_exp = len(exp_peaks); n_dft = len(dft_candidates)
BIG = 1e6
cost = np.full((n_exp, n_dft), BIG)
for i, ep in enumerate(exp_peaks):
    for j, (df, frag, act) in enumerate(dft_candidates):
        dd = abs(ep - df)
        if dd <= TOL:
            cost[i, j] = dd

matches = []
matched_dft_idx = set()
if n_exp > 0 and n_dft > 0:
    row_ind, col_ind = linear_sum_assignment(cost)
    for i, j in zip(row_ind, col_ind):
        if cost[i, j] < BIG:
            ep = exp_peaks[i]; df, frag, act = dft_candidates[j]
            delta = float(ep - df)  # signed, Experimental - DFT
            frags_within = sorted(set(fr for (f2, fr, a2) in dft_candidates if abs(ep - f2) <= TOL))
            unique = len(frags_within) == 1
            if abs(delta) <= CONF_DELTA and unique:
                cls = 'Matched - confident'
            else:
                cls = 'Matched - uncertain'
            matches.append(dict(exp=float(ep), dft=float(df), delta=delta, frag=frag,
                                 exp_prominence=float(exp_prom[i]), frags_within=frags_within,
                                 unique=unique, classification=cls))
            matched_dft_idx.add(j)

matched_exp_vals = set(round(m['exp'], 1) for m in matches)
unmatched_exp = [(float(ep), float(pr)) for ep, pr in zip(exp_peaks, exp_prom) if round(float(ep), 1) not in matched_exp_vals]

# component-specific: DFT modes that were candidates but not claimed by any experimental match
component_specific = []
for j, (df, frag, act) in enumerate(dft_candidates):
    if j not in matched_dft_idx:
        component_specific.append(dict(dft=df, frag=frag, activity=act))

# ============================================================
# STEP 7 -- quantitative summary
# ============================================================
confident = [m for m in matches if m['classification'] == 'Matched - confident']
uncertain = [m for m in matches if m['classification'] == 'Matched - uncertain']
all_matched = confident + uncertain
deltas_all = np.array([m['delta'] for m in all_matched]) if all_matched else np.array([])
deltas_conf = np.array([m['delta'] for m in confident]) if confident else np.array([])

def mae_rmse(d):
    if len(d) == 0:
        return None, None
    return float(np.mean(np.abs(d))), float(np.sqrt(np.mean(d ** 2)))

mae_all, rmse_all = mae_rmse(deltas_all)
mae_conf, rmse_conf = mae_rmse(deltas_conf)

# whole-curve comparison -- secondary/exploratory only, using discrete-mode-derived visualization curves
frag_names = list(FRAG_FILES.keys())
B = np.column_stack([frag_data[n]['vis_curve_norm'] for n in frag_names])
w_opt, _ = nnls(B, exp_norm)
composite = minmax(B @ w_opt) if w_opt.sum() > 0 else B @ w_opt
rmse_curve, r2_curve, r_curve = metrics(exp_norm, composite)
w_frac = (w_opt / w_opt.sum()).tolist() if w_opt.sum() > 0 else w_opt.tolist()

summary = dict(
    experimental_file='sec-60_power-20_i-30.xlsx',
    experimental_metadata=meta,
    native_exp_range_cm1=[native_min, native_max],
    fragment_report=frag_report,
    preprocessing_order=['window 200-2000 cm-1', 'ALS baseline correction', 'Savitzky-Golay smoothing (11,3)', 'min-max normalization (last)'],
    scale_factor=SCALE,
    matching_tolerance_cm1=TOL,
    confident_delta_threshold_cm1=CONF_DELTA,
    dft_activity_threshold_fraction=ACT_FRAC,
    peak_detection=dict(prominence=PROM, min_spacing_cm1=MIN_SPACING),
    n_experimental_peaks=int(n_exp),
    n_dft_candidate_modes=int(n_dft),
    n_matched_confident=len(confident),
    n_matched_uncertain=len(uncertain),
    n_unmatched_experimental=len(unmatched_exp),
    n_component_specific_dft_only=len(component_specific),
    mae_all_matched_cm1=mae_all,
    rmse_all_matched_cm1=rmse_all,
    mae_confident_cm1=mae_conf,
    rmse_confident_cm1=rmse_conf,
    whole_curve_fit_SECONDARY_ONLY=dict(rmse=rmse_curve, r2=r2_curve, pearson_r=r_curve, nnls_weights_fraction=dict(zip(frag_names, w_frac)),
                                          caveat='Whole-curve fit is reported only as a secondary/exploratory diagnostic. It compares the experimental spectrum to a linear composite of 5 independently-broadened fragment curves (visualization broadening, FWHM=20 cm-1) -- it does NOT represent an intact-LPS calculation, ignores inter-fragment coupling, and its R^2 should not be read as a validation metric. Peak-level MAE/RMSE above are the primary, more defensible quantitative result.'),
)

with open(os.path.join(OUT_DIR, 'summary_v2.json'), 'w') as f:
    json.dump(dict(summary=summary, matches=matches, unmatched=unmatched_exp, component_specific=component_specific), f, indent=2)

with open(os.path.join(OUT_DIR, 'peak_table_v2.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Experimental_peak_cm-1', 'DFT_mode_cm-1', 'Delta_cm-1_(Exp-DFT)', 'Component_fragment', 'Other_fragments_within_tol', 'Classification'])
    seen = set()
    for m in sorted(matches, key=lambda x: x['exp']):
        w.writerow([round(m['exp'],1), round(m['dft'],1), round(m['delta'],1), m['frag'].replace('_',' '),
                    ';'.join([f for f in m['frags_within'] if f != m['frag']]), m['classification']])
        seen.add(round(m['exp'],1))
    for ep, pr in sorted(unmatched_exp):
        w.writerow([round(ep,1), '-', '-', '-', '-', 'Unmatched'])

with open(os.path.join(OUT_DIR, 'component_specific_v2.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['DFT_mode_cm-1', 'Fragment', 'Activity'])
    for c in sorted(component_specific, key=lambda x: x['dft']):
        w.writerow([round(c['dft'],1), c['frag'].replace('_',' '), round(c['activity'],4)])

np.savez(os.path.join(OUT_DIR, 'arrays_v2.npz'), grid=grid, exp_norm=exp_norm, composite=composite,
         exp_peaks_idx=exp_peaks_idx, exp_peaks=exp_peaks, exp_prom=exp_prom,
         **{f'frag_curve_{n}': frag_data[n]['vis_curve_norm'] for n in frag_names},
         **{f'frag_peakf_{n}': frag_data[n]['peak_freq'] for n in frag_names},
         **{f'frag_peaka_{n}': frag_data[n]['peak_act'] for n in frag_names})

print(json.dumps(summary, indent=2, default=str))
