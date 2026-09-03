import warnings, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import find_peaks, savgol_filter
from scipy.optimize import nnls
from scipy.stats import pearsonr
import openpyxl

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning, message='.*Glyph.*')

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.dpi': 130,
    'savefig.dpi': 400,
    'figure.figsize': (11.0, 5.5),
    'font.size': 12,
    'axes.titlesize': 13,
    'axes.labelsize': 13,
    'legend.fontsize': 11,
    'axes.linewidth': 1.2,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'lines.linewidth': 2.2,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
PALETTE = ['#E63946','#2A9D8F','#F4A261','#457B9D','#6A0572']
print(f'NumPy {np.__version__} | Pandas {pd.__version__} | Matplotlib {matplotlib.__version__}')
print('All libraries loaded successfully.')

# --- NEXT CELL ---
# ── Workspace paths ───────────────────────────────────────────────────────────
BASE_DIR = Path(r'C:/Users/COMPUTER/Downloads/sukesh/LPS/excelsheet')
OUTPUT_DIR    = BASE_DIR / 'output'
PLOTS_DIR     = OUTPUT_DIR / 'plots'
TABLES_DIR    = OUTPUT_DIR / 'tables'
PROCESSED_DIR = OUTPUT_DIR / 'processed'
SLIDES_DIR    = OUTPUT_DIR / 'slides'
for d in [OUTPUT_DIR, PLOTS_DIR, TABLES_DIR, PROCESSED_DIR, SLIDES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── DFT Frequency Scale Factor ────────────────────────────────────────────────
# Source: NIST CCCBDB (https://cccbdb.nist.gov/), method B3LYP, basis 6-31G(d)
# Ref: Scott & Radom, J. Phys. Chem. 100, 16502 (1996)
# Corrects: anharmonicity, basis-set incompleteness, electron-correlation error
# Change this constant if a different DFT method/basis was used.
SCALE_FACTOR = 0.9613   # B3LYP/6-31G(d)

# ── Gaussian Broadening (simulated spectra only) ───────────────────────────────
# Converts DFT stick spectra to a continuum spectrum.
# 20 cm-1 FWHM is appropriate for powder/solution Raman at typical instrument resolution.
# Decrease to ~10 cm-1 for high-resolution measurements.
BROADENING_FWHM = 20.0   # cm-1

# ── Spectral crop window ───────────────────────────────────────────────────────
RAMAN_MIN = 400.0    # cm-1
RAMAN_MAX = 3200.0   # cm-1

# ── ALS baseline parameters (experimental spectrum ONLY) ──────────────────────
# Ref: Eilers & Boelens, Baseline Correction with Asymmetric Least Squares (2005)
ALS_LAMBDA = 1e5   # smoothness; larger -> smoother baseline
ALS_P      = 0.01  # asymmetry; p << 0.5 places baseline under peaks
ALS_NITER  = 10    # ALS iterations

# ── Savitzky-Golay smoothing (experimental spectrum ONLY) ─────────────────────
SG_WINDOW    = 11
SG_POLYORDER = 3

# ── Input files ───────────────────────────────────────────────────────────────
INPUT_FILES = [
    BASE_DIR / '3-Deoxy-D-Manno-Octulosonic Acid.xlsx',  # KDO
    BASE_DIR / 'D-glucosamine.xlsx',                      # GlcNAc
    BASE_DIR / 'L-Glycero-D-Manno-Heptose.xlsx',         # Heptose
    BASE_DIR / 'Myristic Acid.xlsx',                      # C14:0 fatty acid
    BASE_DIR / 'Phosphoric acid.xlsx',                    # Phosphate
    BASE_DIR / 'sec-60_power-20_i-30.xlsx',              # Experimental LPS
]
EXPERIMENTAL_TOKENS = ('sec-', 'sec_', 'power', 'exp', 'experimental')

print(f'Scale factor  : {SCALE_FACTOR}  (B3LYP/6-31G(d), NIST CCCBDB)')
print(f'Broadening    : {BROADENING_FWHM} cm-1 FWHM')
print(f'Window        : {RAMAN_MIN}-{RAMAN_MAX} cm-1')
print(f'Output folder : {OUTPUT_DIR}')

# --- NEXT CELL ---
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

print('Data-loading helpers defined.')

# --- NEXT CELL ---
datasets = {}
load_report = []

for fp in INPUT_FILES:
    entry = {'file': str(fp), 'name': fp.stem, 'status': 'not_loaded'}
    if not fp.exists():
        entry['status'] = 'missing_file'
        load_report.append(entry)
        print(f'  MISSING : {fp.name}')
        continue
    try:
        xls = pd.ExcelFile(fp, engine='openpyxl')
    except Exception as e:
        entry['status'] = f'open_error: {e}'
        load_report.append(entry)
        print(f'  ERROR   : {fp.name} -> {e}')
        continue

    candidates = []
    for sh in xls.sheet_names:
        try:
            raw = pd.read_excel(fp, sheet_name=sh, header=None, engine='openpyxl', dtype=object)
            parsed = _parse_sheet(raw)
            if parsed is not None:
                candidates.append((sh, parsed))
        except Exception:
            continue

    if not candidates:
        entry['status'] = 'no_raman_data'
        load_report.append(entry)
        print(f'  NO DATA : {fp.name}')
        continue

    best_sheet, best_df = max(candidates, key=lambda x: len(x[1]))
    key = fp.stem
    datasets[key] = {'data': best_df, 'file': str(fp), 'sheet': best_sheet}
    entry.update({'status': 'loaded', 'sheet': best_sheet, 'rows': len(best_df)})
    load_report.append(entry)
    xr = best_df['raman_shift']
    print(f'  OK  {fp.name:50s} sheet={best_sheet:10s} rows={len(best_df):5d}  '
          f'range={xr.min():.0f}-{xr.max():.0f} cm-1')

print(f'\nLoaded {len(datasets)} / {len(INPUT_FILES)} files.')
if len(datasets) < len(INPUT_FILES):
    missing = [e["name"] for e in load_report if e["status"] != "loaded"]
    print(f'WARNING: Could not load: {missing}')

# --- NEXT CELL ---
def baseline_als(y, lam=1e5, p=0.01, niter=10):
    """Asymmetric Least Squares baseline correction (Eilers & Boelens, 2005).
    Applied ONLY to experimental spectra (fluorescence / drift removal)."""
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
    """Savitzky-Golay smoothing with automatic window-size guard.
    Applied ONLY to experimental spectra (CCD shot-noise reduction)."""
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
    """Normalize to [0, 1]. Returns zeros if signal range is zero."""
    y = np.asarray(y, dtype=float)
    lo, hi = np.nanmin(y), np.nanmax(y)
    if not (np.isfinite(lo) and np.isfinite(hi)) or hi <= lo:
        return np.zeros_like(y)
    return (y - lo) / (hi - lo)

def gaussian_broaden(frequencies, activities, grid, fwhm=20.0):
    """Convert DFT stick spectrum to continuous spectrum via Gaussian convolution.
    Applied ONLY to simulated DFT spectra.
    Parameters: frequencies (scaled cm-1), activities (A4/amu), grid (cm-1),
                fwhm (cm-1) controls line width."""
    sigma = fwhm / (2.0*np.sqrt(2.0*np.log(2.0)))
    freqs = np.asarray(frequencies, dtype=float)
    acts  = np.asarray(activities,  dtype=float)
    spec  = np.zeros(len(grid), dtype=float)
    for f, a in zip(freqs, acts):
        if a > 0:
            spec += a * np.exp(-0.5*((grid - f)/sigma)**2)
    return spec

def is_experimental(name: str) -> bool:
    return any(tok in name.lower() for tok in EXPERIMENTAL_TOKENS)

# Fine grid for initial broadening (simulated spectra)
BROAD_GRID = np.arange(RAMAN_MIN, RAMAN_MAX + 1.0, 1.0)

print('Preprocessing functions defined (ALS, SG, Gaussian broadening, normalization).')

# --- NEXT CELL ---
processed_spectra = {}
proc_summary = []

for name, payload in datasets.items():
    df = payload['data'].copy()
    df['raman_shift'] = pd.to_numeric(df['raman_shift'], errors='coerce')
    df['intensity']   = pd.to_numeric(df['intensity'],   errors='coerce')
    df = df.dropna(subset=['raman_shift','intensity'])
    df = df.sort_values('raman_shift').drop_duplicates('raman_shift').reset_index(drop=True)

    try:
        if is_experimental(name):
            # EXPERIMENTAL: crop -> ALS -> SG -> normalize
            df = df[(df['raman_shift']>=RAMAN_MIN)&(df['raman_shift']<=RAMAN_MAX)].copy()
            if df.empty: raise ValueError('Empty after crop')
            x   = df['raman_shift'].to_numpy(dtype=float)
            y   = df['intensity'].to_numpy(dtype=float)
            bsl = baseline_als(y, lam=ALS_LAMBDA, p=ALS_P, niter=ALS_NITER)
            y_bc   = np.clip(y - bsl, 0, None)
            y_sg   = safe_savgol(y_bc, SG_WINDOW, SG_POLYORDER)
            y_norm = minmax_normalize(y_sg)
            processed_spectra[name] = {
                'type':'experimental', 'x':x,
                'y_raw':y, 'y_baseline':bsl, 'y_bc':y_bc,
                'y_sg':y_sg, 'y_norm':y_norm,
            }
            proc_summary.append({'name':name,'type':'exp','status':'ok',
                                 'rows':len(x),'xmin':float(x.min()),'xmax':float(x.max())})
        else:
            # SIMULATED: frequency scale -> Gaussian broaden -> normalize
            x_raw = df['raman_shift'].to_numpy(dtype=float)
            y_act = df['intensity'].to_numpy(dtype=float)
            x_sc  = x_raw * SCALE_FACTOR
            mask  = (x_sc>=RAMAN_MIN)&(x_sc<=RAMAN_MAX)
            if mask.sum() == 0: raise ValueError('No modes in range after scaling')
            y_broad = gaussian_broaden(x_sc[mask], y_act[mask], BROAD_GRID, BROADENING_FWHM)
            y_norm  = minmax_normalize(y_broad)
            # Also compute UNSCALED for comparison plot
            mask_u  = (x_raw>=RAMAN_MIN)&(x_raw<=RAMAN_MAX)
            y_unsc  = gaussian_broaden(x_raw[mask_u], y_act[mask_u], BROAD_GRID, BROADENING_FWHM)
            y_unsc_norm = minmax_normalize(y_unsc)
            processed_spectra[name] = {
                'type':'simulated', 'x':BROAD_GRID.copy(),
                'y_broad':y_broad, 'y_norm':y_norm,
                'y_unscaled_norm': y_unsc_norm,
                'n_modes':int(mask.sum()),
            }
            proc_summary.append({'name':name,'type':'sim','status':'ok',
                                 'rows':len(BROAD_GRID),'xmin':float(BROAD_GRID.min()),
                                 'xmax':float(BROAD_GRID.max()),'n_modes':int(mask.sum())})
        # Save processed CSV
        safe = ''.join(c if c.isalnum() or c in '-_' else '_' for c in name).strip('_')
        v = processed_spectra[name]
        if v['type'] == 'experimental':
            pd.DataFrame({'raman_shift':v['x'],'raw':v['y_raw'],
                          'baseline':v['y_baseline'],'baseline_corrected':v['y_bc'],
                          'smoothed':v['y_sg'],'normalized':v['y_norm']
                         }).to_csv(PROCESSED_DIR/f'{safe}_processed.csv', index=False)
        else:
            pd.DataFrame({'raman_shift':v['x'],'broadened':v['y_broad'],
                          'normalized':v['y_norm'],'unscaled_norm':v['y_unscaled_norm']
                         }).to_csv(PROCESSED_DIR/f'{safe}_processed.csv', index=False)
    except Exception as e:
        proc_summary.append({'name':name,'type':'?','status':f'error:{e}'})
        print(f'  ERROR processing {name}: {e}')
        continue

print('\n-- Preprocessing Summary --')
for s in proc_summary:
    if s['status']=='ok':
        t = s['type'].upper()
        nm = s.get('n_modes','?')
        extra = f'modes={nm}' if s['type']=='sim' else f'pts={s["rows"]}'
        print(f'  [{t:3s}] {s["name"]:45s} {extra:14s} {s["xmin"]:.0f}-{s["xmax"]:.0f} cm-1')
    else:
        print(f'  [ERR] {s["name"]} -> {s["status"]}')
print(f'\n  Processed CSVs saved to: {PROCESSED_DIR}')

# --- NEXT CELL ---
exp_names = [n for n, v in processed_spectra.items() if v['type']=='experimental']
sim_names = [n for n, v in processed_spectra.items() if v['type']=='simulated']
if not exp_names: raise RuntimeError('No experimental spectrum loaded.')
exp_name = exp_names[0]
sv = processed_spectra[exp_name]

fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), facecolor='white')

# Left: experimental preprocessing stages
ax = axes[0]
ax.set_facecolor('white')
ax.plot(sv['x'], sv['y_raw']/sv['y_raw'].max(), color='silver', lw=1.4, label='Raw')
ax.plot(sv['x'], sv['y_baseline']/sv['y_raw'].max(), color='tab:orange', lw=1.3,
        ls='--', label='ALS baseline')
ax.plot(sv['x'], sv['y_norm'], color='#E63946', lw=2.3, label='Processed (normalized)')
ax.set_title(f'Experimental: {exp_name}\n(ALS baseline + SG smoothing + normalization)',
             fontweight='bold', fontsize=11)
ax.set_xlabel('Raman Shift (cm$^{-1}$)'); ax.set_ylabel('Normalized Intensity')
ax.set_xlim(RAMAN_MIN, RAMAN_MAX); ax.legend(fontsize=10, frameon=True)
ax.xaxis.set_major_locator(ticker.MultipleLocator(400))

# Right: one simulated spectrum
sn = sim_names[0]
ss = processed_spectra[sn]
ax2 = axes[1]
ax2.set_facecolor('white')
ax2.plot(ss['x'], ss['y_norm'], color='#2A9D8F', lw=2.3,
         label=f'Scaled + broadened (scale={SCALE_FACTOR})')
ax2.set_title(f'Simulated: {sn}\n'
              f'(B3LYP/6-31G(d), scale={SCALE_FACTOR}, FWHM={BROADENING_FWHM} cm$^{{-1}}$)',
              fontweight='bold', fontsize=11)
ax2.set_xlabel('Raman Shift (cm$^{-1}$)'); ax2.set_ylabel('Normalized Intensity')
ax2.set_xlim(RAMAN_MIN, RAMAN_MAX); ax2.legend(fontsize=10, frameon=True)
ax2.xaxis.set_major_locator(ticker.MultipleLocator(400))

fig.suptitle('Step 3: Preprocessing Pipeline Comparison', fontsize=13, fontweight='bold', y=1.01)
fig.tight_layout()
fig.savefig(PLOTS_DIR/'step3_preprocessing_stages.png', dpi=400, bbox_inches='tight')
plt.show(); plt.close(fig)
print(f'Saved -> {PLOTS_DIR}/step3_preprocessing_stages.png')

# --- NEXT CELL ---
# Scientific validation: compare scaled vs unscaled DFT frequencies
# This plot justifies the 0.9613 scale factor by showing peak position alignment
fig2, axes2 = plt.subplots(len(sim_names), 1, figsize=(13, 3.5*len(sim_names)),
                             facecolor='white', sharex=False)
if len(sim_names) == 1: axes2 = [axes2]

for ax_i, sn in zip(axes2, sim_names):
    ss = processed_spectra[sn]
    ax_i.set_facecolor('white')
    ax_i.plot(BROAD_GRID, ss['y_unscaled_norm'], color='#E63946', lw=1.8, alpha=0.7,
              ls='--', label=f'Unscaled (raw DFT)')
    ax_i.plot(BROAD_GRID, ss['y_norm'], color='#2A9D8F', lw=2.2,
              label=f'Scaled x{SCALE_FACTOR} (NIST CCCBDB)')
    ax_i.set_xlim(400, 2000); ax_i.set_ylim(-0.05, 1.15)
    ax_i.set_ylabel('Norm. Intensity', fontsize=11)
    ax_i.set_title(f'{sn} — Effect of B3LYP/6-31G(d) Scale Factor ({SCALE_FACTOR})',
                   fontsize=11, fontweight='bold')
    ax_i.legend(fontsize=10, frameon=True)
    ax_i.xaxis.set_major_locator(ticker.MultipleLocator(200))
    ax_i.xaxis.set_minor_locator(ticker.MultipleLocator(50))
axes2[-1].set_xlabel('Raman Shift (cm$^{-1}$)', fontsize=12)

fig2.suptitle(f'Scaled vs. Unscaled DFT Spectra\n'
              f'Scale factor {SCALE_FACTOR} corrects ~4% overestimation of harmonic frequencies',
              fontsize=12, fontweight='bold', y=1.01)
fig2.tight_layout()
fig2.savefig(PLOTS_DIR/'step3_scaled_vs_unscaled.png', dpi=400, bbox_inches='tight')
plt.show(); plt.close(fig2)
print(f'Saved -> {PLOTS_DIR}/step3_scaled_vs_unscaled.png')

# --- NEXT CELL ---
exp_x = processed_spectra[exp_name]['x']
GRID_MIN = float(max(RAMAN_MIN, np.ceil(exp_x.min())))
GRID_MAX = float(min(RAMAN_MAX, np.floor(exp_x.max())))
COMMON_GRID = np.arange(GRID_MIN, GRID_MAX + 1.0, 1.0)

print(f'Experimental extent  : {exp_x.min():.1f} - {exp_x.max():.1f} cm-1')
print(f'Common grid (shared) : {GRID_MIN:.0f} - {GRID_MAX:.0f} cm-1  '
      f'({len(COMMON_GRID)} pts, step=1 cm-1)')
print('No zero-padding: grid capped at experimental measurement limits.\n')

# Fragment mapping
FRAGMENT_MAP = {
    'KDO'           : ['kdo','3-deoxy-d-manno-octulosonic'],
    'Glucosamine'   : ['glucosamine'],
    'Heptose'       : ['heptose','l-glycero-d-manno-heptose'],
    'Myristic Acid' : ['myristic'],
    'Phosphoric Acid': ['phosphoric'],
}
fragment_keys = {}
for label, pats in FRAGMENT_MAP.items():
    for dname, dval in processed_spectra.items():
        if dval['type']=='simulated' and any(p in dname.lower() for p in pats):
            fragment_keys[label] = dname; break
missing = [k for k in FRAGMENT_MAP if k not in fragment_keys]
if missing: raise ValueError(f'Missing simulated spectra for: {missing}')
print('Fragment -> dataset mapping:')
for lbl, dn in fragment_keys.items():
    print(f'  {lbl:18s} <- {dn}')

# Interpolate all onto common grid
interp = {}
for name, val in processed_spectra.items():
    x, y = val['x'], val['y_norm']
    order = np.argsort(x)
    interp[name] = np.interp(COMMON_GRID, x[order], y[order], left=0.0, right=0.0)

exp_on_grid = interp[exp_name]
frag_labels  = list(fragment_keys.keys())
frag_spectra = [interp[fragment_keys[l]] for l in frag_labels]
n_frags      = len(frag_spectra)
print(f'\nInterpolated {len(interp)} spectra onto common grid.')

# --- NEXT CELL ---
# Combined overlay
fig, ax = plt.subplots(figsize=(13, 6), facecolor='white')
ax.set_facecolor('white')
for i, (lbl, ys) in enumerate(zip(frag_labels, frag_spectra)):
    ax.plot(COMMON_GRID, ys, color=PALETTE[i], lw=2.5, label=lbl)
ax.set_xlim(GRID_MIN, GRID_MAX); ax.set_ylim(-0.02, 1.15)
ax.set_xlabel('Raman Shift (cm$^{-1}$)'); ax.set_ylabel('Normalized Intensity')
ax.set_title('Slide 1 - Individual LPS Fragment Raman Spectra\n'
             f'(B3LYP/6-31G(d), scale={SCALE_FACTOR}, '
             f'Gaussian FWHM={BROADENING_FWHM} cm$^{{-1}}$, '
             f'grid={GRID_MIN:.0f}-{GRID_MAX:.0f} cm$^{{-1}}$)',
             fontweight='bold')
ax.legend(loc='upper right', frameon=True, framealpha=0.9)
ax.xaxis.set_major_locator(ticker.MultipleLocator(400))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
fig.tight_layout()
p = SLIDES_DIR/'slide1_individual_fragment_spectra.png'
fig.savefig(p, dpi=400, bbox_inches='tight'); plt.show(); plt.close(fig)
print(f'Saved -> {p}')

# Per-molecule
for i,(lbl,ys) in enumerate(zip(frag_labels, frag_spectra)):
    fig2,ax2 = plt.subplots(figsize=(10,5), facecolor='white')
    ax2.set_facecolor('white')
    ax2.plot(COMMON_GRID, ys, color=PALETTE[i], lw=2.8, label=lbl)
    ax2.fill_between(COMMON_GRID, 0, ys, alpha=0.12, color=PALETTE[i])
    ax2.set_xlim(GRID_MIN, GRID_MAX); ax2.set_ylim(-0.02, 1.15)
    ax2.set_xlabel('Raman Shift (cm$^{-1}$)'); ax2.set_ylabel('Normalized Intensity')
    ax2.set_title(f'Slide 1 - {lbl} (DFT Simulated Raman)', fontweight='bold')
    ax2.legend(loc='upper right', frameon=True)
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(400))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(100))
    fig2.tight_layout()
    safe = lbl.lower().replace(' ','_')
    fig2.savefig(SLIDES_DIR/f'slide1_{safe}.png', dpi=400, bbox_inches='tight')
    plt.show(); plt.close(fig2)
    print(f'  Saved -> slide1_{safe}.png')

# --- NEXT CELL ---
I_equal      = np.mean(np.vstack(frag_spectra), axis=0)
I_equal_norm = minmax_normalize(I_equal)

fig3, axes3 = plt.subplots(1, 2, figsize=(16, 5.5), facecolor='white')
for ax_j in axes3: ax_j.set_facecolor('white')

axes3[0].plot(COMMON_GRID, I_equal_norm, color='#1D3557', lw=2.8, label='Equal-weight composite')
axes3[0].fill_between(COMMON_GRID, 0, I_equal_norm, alpha=0.1, color='#1D3557')
axes3[0].set_title('Equal-Weight Composite (Null Model)', fontweight='bold')
axes3[0].set_xlabel('Raman Shift (cm$^{-1}$)'); axes3[0].set_ylabel('Normalized Intensity')
axes3[0].set_xlim(GRID_MIN,GRID_MAX); axes3[0].set_ylim(-0.02,1.15)
axes3[0].legend(frameon=True)
axes3[0].xaxis.set_major_locator(ticker.MultipleLocator(400))

axes3[1].plot(COMMON_GRID, I_equal_norm, color='#E63946', lw=2.5,
              label='Equal-weight composite')
axes3[1].plot(COMMON_GRID, exp_on_grid, color='#1D3557', lw=2.0, alpha=0.80,
              label='Experimental LPS')
axes3[1].set_title('Equal-Weight Composite vs. Experimental', fontweight='bold')
axes3[1].set_xlabel('Raman Shift (cm$^{-1}$)'); axes3[1].set_ylabel('Normalized Intensity')
axes3[1].set_xlim(GRID_MIN,GRID_MAX); axes3[1].set_ylim(-0.02,1.15)
axes3[1].legend(frameon=True)
axes3[1].xaxis.set_major_locator(ticker.MultipleLocator(400))

fig3.suptitle('Slide 2 - Equal-Weight LPS Composite  '
              r'($I_{LPS} = \frac{1}{5}\sum_{i=1}^{5} I_i$)',
              fontsize=13, fontweight='bold')
fig3.tight_layout()
p2 = SLIDES_DIR/'slide2_equal_weight_composite.png'
fig3.savefig(p2, dpi=400, bbox_inches='tight'); plt.show(); plt.close(fig3)
print(f'Saved -> {p2}')

# --- NEXT CELL ---
B = np.column_stack(frag_spectra)   # (n_grid, n_frags)

# NNLS: minimize ||exp_on_grid - B*w||^2  s.t. w >= 0
raw_w, nnls_res = nnls(B, exp_on_grid)

# Rescale to sum=1 for compositional interpretation
w_sum = raw_w.sum()
opt_weights = raw_w / w_sum if w_sum > 1e-12 else np.ones(n_frags)/n_frags

# Optimized composite
I_opt_raw  = B @ opt_weights
I_opt_norm = minmax_normalize(I_opt_raw)

# Metrics on normalized arrays [0,1] on COMMON_GRID
residuals  = exp_on_grid - I_opt_norm
rmse       = float(np.sqrt(np.mean(residuals**2)))
ss_res     = float(np.sum(residuals**2))
ss_tot     = float(np.sum((exp_on_grid - exp_on_grid.mean())**2))
r_squared  = float(1.0 - ss_res/ss_tot) if ss_tot > 1e-12 else 0.0
corr_r, _  = pearsonr(exp_on_grid, I_opt_norm)

# Region-wise RMSE
REGIONS = [
    ('Sugar/phosphate C-O (900-1200)', 900, 1200),
    ('CH2/CH3 scissors (1200-1500)',  1200, 1500),
    ('C=O / C=C (1500-1700)',         1500, 1700),
    ('C-H alkyl (2700-2841)',         2700, GRID_MAX),
]
region_rmse = {}
for rname, rlo, rhi in REGIONS:
    m = (COMMON_GRID>=rlo)&(COMMON_GRID<=rhi)
    if m.any():
        region_rmse[rname] = float(np.sqrt(np.mean((exp_on_grid[m]-I_opt_norm[m])**2)))

print('='*65)
print('  NNLS Optimization Results')
print(f'  DFT: B3LYP/6-31G(d), scale={SCALE_FACTOR}, FWHM={BROADENING_FWHM} cm-1')
print('='*65)
print('\nOptimized Weights (sum=1 rescaled):')
for lbl, w in zip(frag_labels, opt_weights):
    bar = '#' * int(round(w*35))
    print(f'  {lbl:18s} : {w*100:6.2f}%  {bar}')
print(f'\nGlobal Metrics (normalized arrays, {GRID_MIN:.0f}-{GRID_MAX:.0f} cm-1):')
print(f'  RMSE      : {rmse:.4f}  (lower=better; scale [0,1])')
print(f'  R^2       : {r_squared:.4f}  (1.0=perfect)')
print(f'  Pearson r : {corr_r:.4f}  (1.0=perfect linear correlation)')
print('\nRegion-wise RMSE:')
for rn, rv in region_rmse.items(): print(f'  {rn}: {rv:.4f}')
print('='*65)

# --- NEXT CELL ---
# Slide 3(a): Optimized alone
fig5, ax5 = plt.subplots(figsize=(12, 6), facecolor='white'); ax5.set_facecolor('white')
ax5.plot(COMMON_GRID, I_opt_norm, color='#6A0572', lw=2.8, label='Optimized composite (NNLS)')
ax5.fill_between(COMMON_GRID, 0, I_opt_norm, alpha=0.1, color='#6A0572')
ax5.set_xlim(GRID_MIN,GRID_MAX); ax5.set_ylim(-0.02,1.15)
ax5.set_xlabel('Raman Shift (cm$^{-1}$)'); ax5.set_ylabel('Normalized Intensity')
ax5.set_title(f'Slide 3 - Optimized Weighted LPS Composite (NNLS)\n'
              f'R$^2$={r_squared:.4f} | RMSE={rmse:.4f} | Pearson r={corr_r:.4f}', fontweight='bold')
ax5.legend(loc='upper right', frameon=True)
ax5.xaxis.set_major_locator(ticker.MultipleLocator(400))
ax5.xaxis.set_minor_locator(ticker.MultipleLocator(100))
fig5.tight_layout()
p3 = SLIDES_DIR/'slide3_optimized_weighted_composite.png'
fig5.savefig(p3, dpi=400, bbox_inches='tight'); plt.show(); plt.close(fig5)
print(f'Saved -> {p3}')

# Slide 3(b): vs experimental
fig6, ax6 = plt.subplots(figsize=(12, 6), facecolor='white'); ax6.set_facecolor('white')
ax6.plot(COMMON_GRID, I_opt_norm, color='#6A0572', lw=2.5,
         label=f'Optimized composite (R$^2$={r_squared:.3f})')
ax6.plot(COMMON_GRID, exp_on_grid, color='#2A9D8F', lw=2.0, alpha=0.85,
         label='Experimental LPS')
ax6.set_xlim(GRID_MIN,GRID_MAX); ax6.set_ylim(-0.02,1.15)
ax6.set_xlabel('Raman Shift (cm$^{-1}$)'); ax6.set_ylabel('Normalized Intensity')
ax6.set_title('Slide 3 - NNLS Composite vs. Experimental LPS Raman', fontweight='bold')
ax6.legend(loc='upper right', frameon=True)
ax6.xaxis.set_major_locator(ticker.MultipleLocator(400))
ax6.xaxis.set_minor_locator(ticker.MultipleLocator(100))
fig6.tight_layout()
fig6.savefig(SLIDES_DIR/'slide3_optimized_vs_experimental.png', dpi=400, bbox_inches='tight')
plt.show(); plt.close(fig6)
print(f'Saved -> {SLIDES_DIR}/slide3_optimized_vs_experimental.png')

# Slide 4: Three-way overlay
fig7, ax7 = plt.subplots(figsize=(13, 6.5), facecolor='white'); ax7.set_facecolor('white')
ax7.plot(COMMON_GRID, exp_on_grid, color='#1D3557', lw=3.0, alpha=0.90,
         label='Experimental LPS')
ax7.plot(COMMON_GRID, I_equal_norm, color='#E63946', lw=2.1, ls='--', alpha=0.85,
         label='Equal-weight composite (null model)')
ax7.plot(COMMON_GRID, I_opt_norm, color='#F4A261', lw=2.5, alpha=0.90,
         label=f'NNLS composite (R$^2$={r_squared:.3f})')
ax7.set_xlim(GRID_MIN,GRID_MAX); ax7.set_ylim(-0.02,1.18)
ax7.set_xlabel('Raman Shift (cm$^{-1}$)'); ax7.set_ylabel('Normalized Intensity')
ax7.set_title('Slide 4 - Analytical Overlay: Experimental vs. Composite Models', fontweight='bold')
ax7.legend(loc='upper right', frameon=True, framealpha=0.9)
ax7.xaxis.set_major_locator(ticker.MultipleLocator(400))
ax7.xaxis.set_minor_locator(ticker.MultipleLocator(100))
fig7.tight_layout()
p4 = SLIDES_DIR/'slide4_overlay_with_experimental.png'
fig7.savefig(p4, dpi=400, bbox_inches='tight'); plt.show(); plt.close(fig7)
print(f'Saved -> {p4}')

# --- NEXT CELL ---
# Residual analysis: shows WHERE the model succeeds and fails
# Residual > 0: experimental has MORE signal than model (underfit region)
# Residual < 0: model has MORE signal than experimental (overfit region)
fig8, axes8 = plt.subplots(2, 1, figsize=(13, 9), facecolor='white')
fig8.suptitle('Residual Analysis: NNLS Composite vs. Experimental', fontsize=13, fontweight='bold')

# Top: overlay with residual shading
ax_t = axes8[0]; ax_t.set_facecolor('white')
ax_t.plot(COMMON_GRID, exp_on_grid, color='#1D3557', lw=2.2, label='Experimental LPS')
ax_t.plot(COMMON_GRID, I_opt_norm,  color='#F4A261', lw=2.2, label='NNLS composite')
ax_t.fill_between(COMMON_GRID, exp_on_grid, I_opt_norm,
                  where=(exp_on_grid>I_opt_norm), alpha=0.25, color='#E63946',
                  label='Underfit (exp > model)')
ax_t.fill_between(COMMON_GRID, exp_on_grid, I_opt_norm,
                  where=(exp_on_grid<=I_opt_norm), alpha=0.25, color='#2A9D8F',
                  label='Overfit (model > exp)')
ax_t.set_xlim(GRID_MIN,GRID_MAX); ax_t.set_ylim(-0.05,1.20)
ax_t.set_ylabel('Normalized Intensity'); ax_t.legend(fontsize=10, frameon=True)
ax_t.xaxis.set_major_locator(ticker.MultipleLocator(400))
ax_t.xaxis.set_minor_locator(ticker.MultipleLocator(100))

# Bottom: residual spectrum
ax_b = axes8[1]; ax_b.set_facecolor('white')
ax_b.axhline(0, color='black', lw=0.9, ls='--')
ax_b.plot(COMMON_GRID, residuals, color='#457B9D', lw=1.5, label='Residual (exp - model)')
ax_b.fill_between(COMMON_GRID, residuals, 0, where=(residuals>0),
                  alpha=0.35, color='#E63946', label='Positive residual')
ax_b.fill_between(COMMON_GRID, residuals, 0, where=(residuals<=0),
                  alpha=0.35, color='#2A9D8F', label='Negative residual')
ax_b.set_xlim(GRID_MIN, GRID_MAX)
ax_b.set_xlabel('Raman Shift (cm$^{-1}$)')
ax_b.set_ylabel('Residual (exp - model)')
ax_b.legend(fontsize=10, frameon=True)
ax_b.set_title(f'Residuals: RMSE={rmse:.4f}, R$^2$={r_squared:.4f}', fontsize=11)
ax_b.xaxis.set_major_locator(ticker.MultipleLocator(400))
ax_b.xaxis.set_minor_locator(ticker.MultipleLocator(100))

# Annotate mismatch regions
for rname, rlo, rhi in REGIONS:
    rv = region_rmse.get(rname, 0)
    if rv > rmse*1.1:  # highlight regions with above-average RMSE
        ax_b.axvspan(rlo, min(rhi, GRID_MAX), alpha=0.08, color='orange')

fig8.tight_layout()
fig8.savefig(PLOTS_DIR/'residual_analysis.png', dpi=400, bbox_inches='tight')
plt.show(); plt.close(fig8)
print(f'Saved -> {PLOTS_DIR}/residual_analysis.png')

# --- NEXT CELL ---
# Slide 5: Contribution bar chart
fig9, axes9 = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')

# Bar chart
ax_bar = axes9[0]; ax_bar.set_facecolor('white')
bars = ax_bar.bar(frag_labels, opt_weights*100, color=PALETTE,
                  edgecolor='white', linewidth=1.5, width=0.6)
ax_bar.set_ylabel('Contribution Weight (%)', fontsize=12)
ax_bar.set_title('NNLS Fragment Weight Distribution', fontweight='bold')
ymax_b = max(opt_weights*100)*1.18 if opt_weights.max()>0 else 100
ax_bar.set_ylim(0, ymax_b)
ax_bar.tick_params(axis='x', rotation=20)
for bar, w in zip(bars, opt_weights*100):
    ax_bar.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
                f'{w:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Pie chart (complementary)
ax_pie = axes9[1]; ax_pie.set_facecolor('white')
non_zero = [(l, w) for l, w in zip(frag_labels, opt_weights) if w > 1e-4]
if non_zero:
    ls_nz, ws_nz = zip(*non_zero)
    cols_nz = [PALETTE[frag_labels.index(l)] for l in ls_nz]
    ax_pie.pie(ws_nz, labels=ls_nz, colors=cols_nz, autopct='%1.1f%%',
               startangle=90, pctdistance=0.8,
               wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'})
ax_pie.set_title('Composition (non-zero weights)', fontweight='bold')

fig9.suptitle('Slide 5 - NNLS Optimized LPS Fragment Contributions', fontsize=13, fontweight='bold')
fig9.tight_layout()
p5 = SLIDES_DIR/'slide5_dominant_contributors.png'
fig9.savefig(p5, dpi=400, bbox_inches='tight'); plt.show(); plt.close(fig9)
print(f'Saved -> {p5}')

# Regional dominance
def region_dominant(lo, hi):
    m = (COMMON_GRID>=lo)&(COMMON_GRID<=min(hi,GRID_MAX))
    if not m.any(): return 'n/a'
    sc = [float(np.sum(fs[m])*w) for fs,w in zip(frag_spectra, opt_weights)]
    return frag_labels[int(np.argmax(sc))]

print('\nRegional Dominance Analysis:')
print(f'  Strongest overall             : {frag_labels[int(np.argmax(opt_weights))]} '
      f'({opt_weights.max()*100:.1f}%)')
print(f'  900-1200 cm-1 (C-O/P-O)      : {region_dominant(900, 1200)}')
print(f'  1000-1100 cm-1 (ring/sugar)   : {region_dominant(1000, 1100)}')
print(f'  1200-1500 cm-1 (CH2 scissors) : {region_dominant(1200,1500)}')
print(f'  1500-1700 cm-1 (C=O/C=C)      : {region_dominant(1500,1700)}')
print(f'  2700-2841 cm-1 (C-H alkyl)    : {region_dominant(2700, 2841)}')
sugar_w = sum(opt_weights[i] for i,l in enumerate(frag_labels) if l in ['KDO','Glucosamine','Heptose'])
lipid_w = sum(opt_weights[i] for i,l in enumerate(frag_labels) if l in ['Myristic Acid'])
phos_w  = sum(opt_weights[i] for i,l in enumerate(frag_labels) if l in ['Phosphoric Acid'])
print(f'\n  Sugar/core total  : {sugar_w*100:.1f}%   (KDO + Glucosamine + Heptose)')
print(f'  Lipid tail total  : {lipid_w*100:.1f}%   (Myristic Acid)')
print(f'  Phosphate total   : {phos_w*100:.1f}%   (Phosphoric Acid)')

# --- NEXT CELL ---
def adaptive_find_peaks(x_grid, y, min_height=0.04, distance=12, noise_mult=2.0):
    """Adaptive peak detection.
    Prominence threshold = noise_mult * MAD(y), minimum min_height.
    Avoids global fixed thresholds that miss low-amplitude or catch noise peaks."""
    y = np.asarray(y, dtype=float)
    # Median absolute deviation as robust noise estimator
    mad = float(np.median(np.abs(y - np.median(y))))
    prom_thresh = max(min_height, noise_mult * mad)
    pks, props = find_peaks(y, height=min_height, distance=distance,
                            prominence=prom_thresh)
    return pks, prom_thresh

def assign_region(wn):
    if   wn < 700:   return 'Skeletal deformations (<700 cm-1)'
    elif wn < 900:   return 'Ring deformation / breathing (700-900 cm-1)'
    elif wn < 1200:  return 'C-O, C-C, P-O stretch (sugars/phosphate, 900-1200 cm-1)'
    elif wn < 1500:  return 'CH2/CH3 scissors, C-N stretch (1200-1500 cm-1)'
    elif wn < 1700:  return 'C=O, C=C stretch / Amide I (1500-1700 cm-1)'
    elif wn < 2800:  return 'Silent / combination (1700-2800 cm-1)'
    elif wn < 3050:  return 'C-H stretches, alkyl chains (2800-3050 cm-1)'
    else:            return 'O-H / N-H stretches (>3050 cm-1)'

peak_rows = []
spectra_to_peak = (
    list(zip(frag_labels, frag_spectra)) +
    [('Experimental LPS', exp_on_grid),
     ('NNLS Composite',   I_opt_norm),
     ('Equal-Weight',     I_equal_norm)]
)

for lbl, ys in spectra_to_peak:
    pks, prom_used = adaptive_find_peaks(COMMON_GRID, ys)
    for idx in pks:
        peak_rows.append({
            'Spectrum': lbl,
            'Peak Position (cm-1)': round(float(COMMON_GRID[idx]), 1),
            'Relative Intensity':   round(float(ys[idx]), 4),
            'Region Assignment':    assign_region(COMMON_GRID[idx]),
            'Prominence Threshold': round(prom_used, 4),
        })

peaks_df = pd.DataFrame(peak_rows)
out_peaks = TABLES_DIR / 'peak_summary.xlsx'
peaks_df.to_excel(out_peaks, index=False)
print(f'Detected {len(peaks_df)} total peaks across {len(spectra_to_peak)} spectra (adaptive prominence).')
for lbl, _ in spectra_to_peak:
    n = len(peaks_df[peaks_df['Spectrum']==lbl])
    print(f'  {lbl:25s}: {n} peaks')
print(f'\nSaved -> {out_peaks}')
try:
    from IPython.display import display
    display(peaks_df[peaks_df['Spectrum']=='Experimental LPS'])
except Exception:
    print(peaks_df[peaks_df['Spectrum']=='Experimental LPS'].to_string(index=False))

# --- NEXT CELL ---
metrics_rows = [
    {'Parameter':'DFT method',               'Value':'B3LYP/6-31G(d)'},
    {'Parameter':'DFT keyword',              'Value':'freq=Raman'},
    {'Parameter':'Frequency scale factor',   'Value':SCALE_FACTOR},
    {'Parameter':'Scale factor reference',   'Value':'NIST CCCBDB; Scott & Radom 1996'},
    {'Parameter':'Gaussian broadening FWHM','Value':f'{BROADENING_FWHM} cm-1'},
    {'Parameter':'ALS applied to',           'Value':'Experimental spectrum only'},
    {'Parameter':'ALS lambda',               'Value':ALS_LAMBDA},
    {'Parameter':'ALS p',                    'Value':ALS_P},
    {'Parameter':'ALS iterations',           'Value':ALS_NITER},
    {'Parameter':'SG window',                'Value':SG_WINDOW},
    {'Parameter':'SG polynomial order',      'Value':SG_POLYORDER},
    {'Parameter':'Optimization method',      'Value':'NNLS (Lawson-Hanson, scipy.optimize.nnls)'},
    {'Parameter':'Spectral range',           'Value':f'{GRID_MIN:.0f}-{GRID_MAX:.0f} cm-1'},
    {'Parameter':'Grid points',              'Value':len(COMMON_GRID)},
    {'Parameter':'RMSE (global)',            'Value':round(rmse, 6)},
    {'Parameter':'R^2',                      'Value':round(r_squared, 6)},
    {'Parameter':'Pearson r',                'Value':round(float(corr_r), 6)},
]
for lbl, w in zip(frag_labels, opt_weights):
    metrics_rows.append({'Parameter':f'Weight: {lbl}', 'Value':round(float(w), 6)})
for rname, rv in region_rmse.items():
    metrics_rows.append({'Parameter':f'Region RMSE: {rname}', 'Value':round(rv, 6)})

metrics_df = pd.DataFrame(metrics_rows)
out_m = TABLES_DIR/'model_metrics.xlsx'
metrics_df.to_excel(out_m, index=False)
print(f'Model metrics saved -> {out_m}')
try:
    from IPython.display import display
    display(metrics_df)
except Exception:
    print(metrics_df.to_string(index=False))

# --- NEXT CELL ---
quality = 'STRONG' if r_squared>0.7 else ('MODERATE' if r_squared>0.4 else 'WEAK')
print('='*70)
print('  FINAL SCIENTIFIC SUMMARY: LPS Composite Raman Analysis')
print('='*70)
print(f'\n1. DFT METHOD')
print(f'   Method    : B3LYP/6-31G(d), freq=Raman (Gaussian 16)')
print(f'   Scale     : {SCALE_FACTOR} (NIST CCCBDB; Scott & Radom, 1996)')
print(f'   Broadening: Gaussian FWHM={BROADENING_FWHM} cm-1')
print(f'\n2. PREPROCESSING (asymmetric pipeline)')
print(f'   Simulated : frequency scaling -> Gaussian broadening -> normalization')
print(f'   Experiment: ALS baseline (lambda={ALS_LAMBDA:.0e}, p={ALS_P}) -> SG -> normalization')
print(f'   NOTE: ALS skipped for simulated spectra (no fluorescence background)')
print(f'\n3. OPTIMIZATION (NNLS, Lawson-Hanson)')
for lbl, w in zip(frag_labels, opt_weights):
    bar = '#'*int(round(w*30))
    print(f'   {lbl:18s}: {w*100:5.1f}%  {bar}')
print(f'\n4. MODEL FIT ({GRID_MIN:.0f}-{GRID_MAX:.0f} cm-1, normalized arrays)')
print(f'   RMSE      = {rmse:.4f}')
print(f'   R^2       = {r_squared:.4f}')
print(f'   Pearson r = {corr_r:.4f}')
print(f'   Quality   = {quality}')
print(f'\n5. SCIENTIFIC LIMITATIONS (must state in thesis/paper)')
print('   - Linear superposition ignores intermolecular interactions')
print('   - Covalent coupling and H-bonding in intact LPS not captured')
print('   - Missing outer-core sugars (Glucose, Galactose) likely explains low R^2')
print('   - Single experimental replicate; N>=3 required for publication')
print(f'   - Grid limited to {GRID_MIN:.0f}-{GRID_MAX:.0f} cm-1 (experimental limit)')
print('   - Phosphoric Acid weight=0%: may be confounded with KDO/Heptose P-O modes')
print(f'\n6. OUTPUT FILES')
all_out = list(SLIDES_DIR.glob('*.png')) + list(TABLES_DIR.glob('*.xlsx'))
all_out += list(PLOTS_DIR.glob('*.png'))
for fp in sorted(all_out): print(f'   {fp.parent.name}/{fp.name}')
print('='*70)
