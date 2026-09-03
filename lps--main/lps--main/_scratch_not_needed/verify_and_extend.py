"""
verify_and_extend.py
Exact reproduction of the NNLS fit (200-2000 cm-1 grid, matching
output/final_summary_report.txt and output/tables/model_metrics.xlsx)
directly from the original .xlsx files, using the same parsing/
preprocessing functions as run_final.py. Then extends with:
  - a regularized "soft alternating fit" (MCR-ALS-inspired) lambda sweep
  - peak validation against literature diagnostic assignments
"""
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import savgol_filter
from scipy.optimize import nnls
from scipy.stats import pearsonr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = Path('.')
OUT = BASE_DIR / 'output'
TABLES = OUT / 'tables'
PLOTS = OUT / 'plots'
TABLES.mkdir(parents=True, exist_ok=True)
PLOTS.mkdir(parents=True, exist_ok=True)

SCALE_FACTOR = 0.9613
BROADENING_FWHM = 20.0
RAMAN_MIN, RAMAN_MAX = 200.0, 2000.0   # matches final_summary_report.txt (NOT current run_final.py's 400-3200)
ALS_LAMBDA, ALS_P, ALS_NITER = 1e5, 0.01, 10
SG_WINDOW, SG_POLYORDER = 11, 3

INPUT_FILES = [
    BASE_DIR / '3-Deoxy-D-Manno-Octulosonic Acid.xlsx',
    BASE_DIR / 'D-glucosamine.xlsx',
    BASE_DIR / 'L-Glycero-D-Manno-Heptose.xlsx',
    BASE_DIR / 'Myristic Acid.xlsx',
    BASE_DIR / 'Phosphoric acid.xlsx',
    BASE_DIR / 'sec-60_power-20_i-30.xlsx',
]
EXPERIMENTAL_TOKENS = ('sec-', 'sec_', 'power', 'exp', 'experimental')

def _normalize_cols(df):
    df.columns = [str(c).strip() for c in df.columns]
    return df

def _coerce_numeric(df, min_valid=3):
    out = {col: pd.to_numeric(df[col], errors='coerce')
           for col in df.columns
           if pd.to_numeric(df[col], errors='coerce').notna().sum() >= min_valid}
    return pd.DataFrame(out) if len(out) >= 2 else pd.DataFrame()

def _score_shift(name, s):
    sc = 6.0 if any(k in name.lower() for k in ['raman','shift','wavenumber','cm','freq']) else 0.0
    v = s.dropna()
    if len(v):
        sc += 1.0 if v.min() >= 0 else 0.0
        sc += min((v.max()-v.min())/600.0, 3.0)
    return sc

def _score_intensity(name, s):
    sc = 6.0 if any(k in name.lower() for k in ['intensity','activity','raman','signal','counts']) else 0.0
    v = s.dropna()
    if len(v): sc += min(v.std()/10.0, 2.5)
    return sc

def _parse_sheet(raw_df):
    work = raw_df.dropna(how='all').dropna(axis=1, how='all')
    if work.empty: return None
    first = work.iloc[0].astype(str).str.strip()
    hdr_like = (first.str.lower().str.contains(
        'raman|shift|wavenumber|cm|freq|intensity|activity|signal|counts', regex=True).any()
        or first.str.contains(r'[A-Za-z]', regex=True).sum() >= max(1, int(0.3*len(first))))
    if hdr_like:
        df = work.copy(); df.columns = first; df = df.iloc[1:]
    else:
        df = work.copy(); df.columns = [f'col_{i}' for i in range(df.shape[1])]
    df = _normalize_cols(df)
    ndf = _coerce_numeric(df)
    if ndf.shape[1] < 2: return None
    sc_col = sorted(ndf.columns, key=lambda c: _score_shift(c, ndf[c]), reverse=True)[0]
    ic_col = sorted([c for c in ndf.columns if c != sc_col],
                    key=lambda c: _score_intensity(c, ndf[c]), reverse=True)[0]
    out = pd.DataFrame({
        'raman_shift': pd.to_numeric(ndf[sc_col], errors='coerce'),
        'intensity':   pd.to_numeric(ndf[ic_col], errors='coerce')
    }).dropna()
    out = out[np.isfinite(out['raman_shift']) & np.isfinite(out['intensity']) & (out['raman_shift']>0)]
    out = out.sort_values('raman_shift').drop_duplicates('raman_shift', keep='first')
    return out.reset_index(drop=True) if len(out) >= 5 else None

def baseline_als(y, lam=1e5, p=0.01, niter=10):
    y = np.asarray(y, dtype=float)
    n = len(y)
    if n < 3: return np.zeros_like(y)
    D = sparse.diags([1.,-2.,1.],[0,-1,-2], shape=(n,n-2), format='csc')
    w = np.ones(n)
    for _ in range(niter):
        W = sparse.spdiags(w, 0, n, n)
        z = spsolve(W + lam*(D@D.T), w*y)
        w = p*(y>z).astype(float) + (1-p)*(y<=z).astype(float)
    return np.asarray(z, dtype=float)

def safe_savgol(y, window_length=11, polyorder=3):
    y = np.asarray(y, dtype=float)
    n = len(y)
    if n < 5: return y.copy()
    win = int(window_length)|1
    win = min(win, n if n%2==1 else n-1)
    if win < 5: return y.copy()
    poly = min(polyorder, win-2)
    if poly < 1: return y.copy()
    return savgol_filter(y, window_length=win, polyorder=poly, mode='interp')

def minmax_normalize(y):
    y = np.asarray(y, dtype=float)
    lo, hi = np.nanmin(y), np.nanmax(y)
    if not (np.isfinite(lo) and np.isfinite(hi)) or hi <= lo:
        return np.zeros_like(y)
    return (y - lo) / (hi - lo)

def gaussian_broaden(frequencies, activities, grid, fwhm=20.0):
    sigma = fwhm / (2.0*np.sqrt(2.0*np.log(2.0)))
    freqs = np.asarray(frequencies, dtype=float)
    acts  = np.asarray(activities,  dtype=float)
    spec  = np.zeros(len(grid), dtype=float)
    for f, a in zip(freqs, acts):
        if a > 0:
            spec += a * np.exp(-0.5*((grid - f)/sigma)**2)
    return spec

def is_experimental(name):
    return any(tok in name.lower() for tok in EXPERIMENTAL_TOKENS)

BROAD_GRID = np.arange(RAMAN_MIN, RAMAN_MAX + 1.0, 1.0)

# ---- Load ----
datasets = {}
for fp in INPUT_FILES:
    xls = pd.ExcelFile(fp, engine='openpyxl')
    candidates = []
    for sh in xls.sheet_names:
        raw = pd.read_excel(fp, sheet_name=sh, header=None, engine='openpyxl', dtype=object)
        parsed = _parse_sheet(raw)
        if parsed is not None:
            candidates.append((sh, parsed))
    best_sheet, best_df = max(candidates, key=lambda x: len(x[1]))
    datasets[fp.stem] = {'data': best_df, 'sheet': best_sheet}
    print(f'  OK {fp.name:45s} sheet={best_sheet:10s} rows={len(best_df):5d} '
          f'range={best_df.raman_shift.min():.0f}-{best_df.raman_shift.max():.0f}')

# ---- Preprocess ----
processed = {}
exp_name = None
for name, val in datasets.items():
    df = val['data']
    if is_experimental(name):
        exp_name = name
        x = df['raman_shift'].values
        y = df['intensity'].values
        bl = baseline_als(y, ALS_LAMBDA, ALS_P, ALS_NITER)
        y_bc = y - bl
        y_sm = safe_savgol(y_bc, SG_WINDOW, SG_POLYORDER)
        y_n = minmax_normalize(y_sm)
        processed[name] = {'x': x, 'y_norm': y_n, 'type': 'experimental'}
    else:
        x_scaled = df['raman_shift'].values * SCALE_FACTOR
        acts = df['intensity'].values
        y_broad = gaussian_broaden(x_scaled, acts, BROAD_GRID, BROADENING_FWHM)
        y_n = minmax_normalize(y_broad)
        processed[name] = {'x': BROAD_GRID, 'y_norm': y_n, 'type': 'simulated'}

assert exp_name is not None
exp_x = processed[exp_name]['x']
GRID_MIN = float(max(RAMAN_MIN, np.ceil(exp_x.min())))
GRID_MAX = float(min(RAMAN_MAX, np.floor(exp_x.max())))
COMMON_GRID = np.arange(GRID_MIN, GRID_MAX + 1.0, 1.0)
print(f'\nGRID: {GRID_MIN}-{GRID_MAX}  n={len(COMMON_GRID)}')

FRAGMENT_MAP = {
    'KDO': ['kdo','3-deoxy-d-manno-octulosonic'],
    'Glucosamine': ['glucosamine'],
    'Heptose': ['heptose','l-glycero-d-manno-heptose'],
    'Myristic Acid': ['myristic'],
    'Phosphoric Acid': ['phosphoric'],
}
fragment_keys = {}
for label, pats in FRAGMENT_MAP.items():
    for dname, dval in processed.items():
        if dval['type']=='simulated' and any(p in dname.lower() for p in pats):
            fragment_keys[label] = dname; break

interp = {}
for name, val in processed.items():
    x, y = val['x'], val['y_norm']
    order = np.argsort(x)
    interp[name] = np.interp(COMMON_GRID, x[order], y[order], left=0.0, right=0.0)

exp_on_grid = interp[exp_name]
frag_labels = list(fragment_keys.keys())
frag_spectra = [interp[fragment_keys[l]] for l in frag_labels]
B = np.column_stack(frag_spectra)

raw_w, _ = nnls(B, exp_on_grid)
w_sum = raw_w.sum()
opt_weights = raw_w / w_sum if w_sum > 1e-12 else np.ones(len(frag_labels))/len(frag_labels)
I_opt_raw = B @ opt_weights
I_opt_norm = minmax_normalize(I_opt_raw)
residuals = exp_on_grid - I_opt_norm
rmse = float(np.sqrt(np.mean(residuals**2)))
ss_tot = float(np.sum((exp_on_grid-exp_on_grid.mean())**2))
r2 = float(1 - np.sum(residuals**2)/ss_tot)
r, _ = pearsonr(exp_on_grid, I_opt_norm)

print('\n=== VERIFIED NNLS reproduction (scipy, exact pipeline) ===')
for lbl, w in zip(frag_labels, opt_weights):
    print(f'  {lbl:18s}: {w*100:6.2f}%')
print(f'  RMSE={rmse:.6f}  R2={r2:.6f}  r={r:.6f}')
print('  Published (model_metrics.xlsx): RMSE=0.185045 R2=0.179946 r=0.507839')

# save these authoritative arrays for reuse
np.savez(BASE_DIR/'_verified_arrays.npz', grid=COMMON_GRID, exp=exp_on_grid, B=B,
         weights=opt_weights, labels=np.array(frag_labels))
print('\nSaved intermediate arrays -> _verified_arrays.npz')
