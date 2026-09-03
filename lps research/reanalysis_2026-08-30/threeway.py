import csv

TOL = 15.0

lit = [
    (550, 'A (Wu 2021, Enteric LPS)', 'beta(CH2) ring'),
    (680, 'A (Wu 2021, Enteric LPS)', 'delta(C-O-C) fatty acid'),
    (850, 'A (Wu 2021, Enteric LPS / thesis)', 'nu(C-O-C) saccharide / glycosidic'),
    (988, 'A (Wu 2021, Enteric LPS / thesis)', 'Carbohydrate (KDO)'),
    (1131, 'A (Wu 2021, both LPS types) + Kundu-text', 'Fatty acid C-C / lipid vibrations'),
    (1330, 'A (Wu 2021, both LPS types)', 'Phospholipid delta(CH)'),
    (1450, 'A (Wu 2021, Enteric LPS)', 'CH3/CH2 deformation'),
    (543, 'A2 (Wu 2021, N. meningitidis LPS)', 'Glycosidic ring'),
    (552, 'A2 (Wu 2021, N. meningitidis LPS)', 'Lipid ring'),
    (715, 'A2 (Wu 2021, N. meningitidis LPS)', 'C-N'),
    (733, 'A2 (Wu 2021, N. meningitidis LPS)', 'Carbohydrate'),
    (981, 'A2 (Wu 2021, N. meningitidis LPS)', 'Lipid beta(CH)'),
    (1066, 'B (Apr-2026 lit. report)', 'P-O-C / C-O (~1058-1075)'),
    (1230, 'B (Apr-2026 lit. report, PRIMARY)', 'P=O asym (~1220-1240)'),
    (1550, 'B (Apr-2026 lit. report)', 'Amide II (~1540-1560)'),
    (1651, 'B (Apr-2026 lit. report)', 'Amide I (~1645-1658)'),
    (1738, 'B (Apr-2026 lit. report)', 'C=O ester (~1735-1742)'),
    (857, 'D (Yang et al. 2022 / Fig P1)', 'LPS band (differentiation set)'),
    (1003, 'D (Yang et al. 2022 / Fig P1)', 'LPS band (differentiation set)'),
    (1333, 'D (Yang et al. 2022 / Fig P1)', 'LPS band (differentiation set); overlaps LTA per Fig P1 note'),
    (1614, 'D (Yang et al. 2022 / Fig P1)', 'LPS band (differentiation set); overlaps LTA per Fig P1 note'),
    (1316, 'Kundu-text (source flagged conflicted, see note)', 'Aliphatic molecules'),
    (1366, 'Kundu-text (source flagged conflicted, see note)', 'Lipids'),
    (1579, 'Kundu-text (source flagged conflicted, see note)', 'Graphitic carbon -- likely SERS-substrate artifact, not intrinsic LPS'),
    (1655, 'Kundu-text (source flagged conflicted, see note)', 'Lipids (C=O)'),
]

exp_peaks = []
with open('experimental_peaks_all.csv') as f:
    for row in csv.DictReader(f):
        exp_peaks.append((float(row['exp_peak_cm-1']), float(row['prominence'])))

dft_matches = []
with open('reference_band_candidates.csv') as f:
    for row in csv.DictReader(f):
        dft_matches.append(dict(exp=float(row['exp_peak_cm-1']), dft=float(row['dft_peak_cm-1_scaled']),
                                 delta=float(row['delta_cm-1']), frag=row['fragment'], conf=row['confidence']))

out_rows = []
for lpos, src, assign in lit:
    exp_hit = min(exp_peaks, key=lambda p: abs(p[0]-lpos)) if exp_peaks else None
    exp_ok = exp_hit if exp_hit and abs(exp_hit[0]-lpos) <= TOL else None
    dft_hit = min(dft_matches, key=lambda m: abs(m['exp']-lpos)) if dft_matches else None
    dft_ok = dft_hit if dft_hit and abs(dft_hit['exp']-lpos) <= TOL else None
    if exp_ok and dft_ok:
        status = 'Strong (lit + powder + DFT)'
    elif exp_ok and not dft_ok:
        status = 'Experimental/Literature only'
    elif dft_ok and not exp_ok:
        status = 'DFT/Literature only (no major exp peak)'
    else:
        status = 'Literature only (no match in our data)'
    out_rows.append(dict(lit=lpos, src=src, assign=assign,
                          exp='%.0f'%exp_ok[0] if exp_ok else '-',
                          dft='%.0f (%s)'%(dft_ok['dft'], dft_ok['frag']) if dft_ok else '-',
                          status=status))

with open('threeway_comparison.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['literature_cm-1','source','assignment','our_powder_cm-1','dft_supported_cm-1_(fragment)','status'])
    for r in out_rows:
        w.writerow([r['lit'], r['src'], r['assign'], r['exp'], r['dft'], r['status']])

for r in out_rows:
    print(r['lit'], '|', r['status'], '|', r['exp'], '|', r['dft'])
