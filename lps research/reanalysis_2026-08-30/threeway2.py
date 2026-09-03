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
    (1333, 'D (Yang et al. 2022 / Fig P1)', 'LPS band; overlaps LTA per Fig P1 note'),
    (1614, 'D (Yang et al. 2022 / Fig P1)', 'LPS band; overlaps LTA per Fig P1 note'),
    (1316, 'Kundu-text (flagged conflicted, see note)', 'Aliphatic molecules'),
    (1366, 'Kundu-text (flagged conflicted, see note)', 'Lipids'),
    (1579, 'Kundu-text (flagged conflicted, see note)', 'Graphitic carbon -- likely SERS-substrate artifact'),
    (1655, 'Kundu-text (flagged conflicted, see note)', 'Lipids (C=O)'),
]

exp_peaks = []
with open('experimental_peaks_all.csv') as f:
    for row in csv.DictReader(f):
        exp_peaks.append(float(row['exp_peak_cm-1']))

defensible = {}  # exp_value -> (dft, frag, conf)
with open('reference_band_candidates.csv') as f:
    for row in csv.DictReader(f):
        defensible[float(row['exp_peak_cm-1'])] = (float(row['dft_peak_cm-1_scaled']), row['fragment'], row['confidence'])

dft_all = []
with open('dft_candidates_all.csv') as f:
    for row in csv.DictReader(f):
        dft_all.append((float(row['dft_peak_cm-1_scaled']), row['fragment']))

out_rows = []
for lpos, src, assign in lit:
    exp_hit = min(exp_peaks, key=lambda p: abs(p-lpos)) if exp_peaks else None
    exp_ok = exp_hit if exp_hit is not None and abs(exp_hit-lpos) <= TOL else None
    if exp_ok is not None:
        # chained: does THIS exp peak have a defensible DFT match?
        dft_for_this = defensible.get(exp_ok)
        if dft_for_this:
            status = 'Strong (literature -> our powder -> DFT-supported)'
            dft_str = '%.0f (%s, %s)' % (dft_for_this[0], dft_for_this[1], dft_for_this[2])
        else:
            status = 'Experimental/Literature only (no DFT-supported match at this exp peak)'
            dft_str = '-'
        exp_str = '%.0f' % exp_ok
    else:
        exp_str = '-'
        nearest_dft = min(dft_all, key=lambda d: abs(d[0]-lpos)) if dft_all else None
        if nearest_dft is not None and abs(nearest_dft[0]-lpos) <= TOL:
            status = 'Literature/DFT only (theory places a mode here; no major exp peak detected)'
            dft_str = '%.0f (%s)' % (nearest_dft[0], nearest_dft[1])
        else:
            status = 'Literature only (no match in our data)'
            dft_str = '-'
    out_rows.append(dict(lit=lpos, src=src, assign=assign, exp=exp_str, dft=dft_str, status=status))

with open('threeway_comparison.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['literature_cm-1','source','assignment','our_powder_cm-1','dft_supported_cm-1_(fragment,confidence)','status'])
    for r in out_rows:
        w.writerow([r['lit'], r['src'], r['assign'], r['exp'], r['dft'], r['status']])

for r in out_rows:
    print(r['lit'], '|', r['status'], '|', r['exp'], '|', r['dft'])
