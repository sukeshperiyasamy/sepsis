# α-Anomer Calculation — Result

**Verdict: the α anomer does NOT explain the unmatched bands. The hypothesis is
tested and rejected.**

Run completed 11 August 2026, Gaussian 16 Rev C.01, 2 h 39 min optimisation
(27 steps) + 1 h 03 min frequencies = 3 h 42 min total.

---

## 1. The calculation is sound

| Check | Result |
|---|---|
| Route | `opt=(calcfc,tight) freq=raman b3lyp/6-311++g(d,p) empiricaldispersion=gd3bj int=ultrafine scf=(tight,xqc)` |
| Solvation | **none — gas phase**, identical to β |
| Basis functions | 573 (593 Cartesian) — identical to β |
| Normal termination | yes, ×2 |
| Stationary point | found, ×2 |
| Imaginary frequencies | **0** — lowest mode 19.38 cm⁻¹ |
| Normal modes | 111, all with Raman activities |

Nothing wrong with the run. The negative result is a real result, not a failure.

---

## 2. What looked like success at first

Of the 11 bands β could not match, α appeared to match five within ±18 cm⁻¹ —
including 830 and 956 cm⁻¹, the two specifically predicted.

**This was misleading, for a reason I should have anticipated.** The 11 bands
were *defined* as the ones β failed to match. β therefore scores 0/11 on its own
leftovers by construction. Any second mode set will score above zero. That
comparison is survivorship bias, not evidence — the same error identified earlier
in the GitHub repository's RMSE figure.

---

## 3. The honest test — and it fails

The correct question is whether α improves the fit **across all 41 bands** more
than any arbitrary extra 111 modes would.

**Control:** the β modes rigidly shifted by a random offset. Same number of
modes, same spacing statistics, chemically meaningless.

| | bands matched / 41 |
|---|---|
| β alone | 30 |
| **β + real α** | **35** (gain +5) |
| β + shifted-β decoy | 34.3 ± 1.95 (gain +4.28) |
| | **p = 0.46** |

**A meaningless decoy does just as well.** Repeated at tighter tolerances:

| Tolerance | axis coverage | β | α | combined | real gain | decoy gain | p |
|---|---|---|---|---|---|---|---|
| ±5 | 48% | 16 | 14 | 23 | +7 | +7.22 ± 2.06 | 0.62 |
| ±8 | 77% | 23 | 19 | 29 | +6 | +4.94 ± 2.17 | 0.41 |
| ±10 | 96% | 25 | 25 | 30 | +5 | +5.02 ± 2.11 | 0.58 |
| ±18 | 172% | 30 | 31 | 35 | +5 | +4.28 ± 1.95 | 0.46 |

At no tolerance is the α improvement distinguishable from chance.

**Note the coverage column.** With 67 modes in a 1400 cm⁻¹ window, ±18 cm⁻¹
covers 172% of the axis — every band matches something regardless of chemistry.
The ±18 tolerance used throughout this project is not a discriminating test.

---

## 4. Two of the five "matches" are unobservable

| Exp (cm⁻¹) | α mode | Δ | Raman activity | Rel. intensity | |
|---|---|---|---|---|---|
| 772 | 777.2 | +5.2 | 6.94 | 3.39% | credible |
| **830** | 823.9 | −6.1 | 0.93 | **0.42%** | **too weak to observe** |
| 956 | 953.1 | −2.9 | 7.68 | 2.84% | credible |
| **1517** | 1514.3 | −2.7 | 2.40 | **0.45%** | **too weak to observe** |
| 1785 | 1768.8 | −16.2 | 8.38 | 1.21% | marginal (Δ large) |

830 cm⁻¹ — one of the two bands the α calculation was run to explain — is
experimentally **strong** (rel. intensity 0.65, high confidence) but the
candidate α mode carries 0.42% of the calculated maximum. That mode could not
produce an observable band. **The α anomer does not explain 830 cm⁻¹.**

---

## 5. What actually explains the unmatched bands

Both anomers have **no calculated modes at all** between ~1535 and ~1720 cm⁻¹ —
a gap of roughly 190 cm⁻¹. Experiment shows four clear bands inside it
(1589, 1637, 1652, 1702 cm⁻¹).

This is not an anomeric effect. It is the gas-phase isolated-molecule
approximation. In the solid, intermolecular hydrogen bonding to the amide and
carboxyl carbonyls lowers those stretching frequencies by tens of cm⁻¹, moving
them down into precisely that gap. No isolated-molecule calculation of either
anomer can reproduce it.

**This is a cleaner and better-supported explanation than the anomeric one, and
it accounts for the majority of the unmatched bands.**

---

## 6. Two results worth keeping

**β is the correct reference model — now justified rather than assumed.**

| | β | α | α − β |
|---|---|---|---|
| Electronic energy | −1087.570645 | −1087.564954 | +3.57 kcal/mol |
| + ZPE | −1087.252763 | −1087.246711 | +3.80 kcal/mol |
| Gibbs free energy (298.15 K) | −1087.304371 | −1087.299425 | **+3.10 kcal/mol** |

β is the more stable anomer in the gas phase, and it also fits experiment
slightly better on its own (30 vs 31 matched but MAE 5.73 vs 6.42 cm⁻¹). The
manuscript's use of β is defensible on both counts.

*Caveat:* these are single conformers, not conformationally averaged, so the
figure is not a rigorous anomeric equilibrium constant. It should be quoted as an
indication, not a thermodynamic result.

**The anomeric-mixture limitation can now be stated as tested.** The manuscript
currently lists it as a possible explanation and a suggested next step. It can
now say the calculation was performed and did not support it.

---

## 7. Separate issue found — two disagreeing tables in the archive

While running this I found the archive contains **two comparison tables that do
not agree**:

| File | Peaks | Matched | Unmatched |
|---|---|---|---|
| `06_Analysis_Notebook/tables/Table1_experiment_vs_DFT.csv` | 41 | **30** | **11** |
| `03_Processed_Results/Experimental_vs_DFT_comparison.csv` | 41 | **33** | **8** |

Peak positions differ by 1–2 cm⁻¹ in at least 12 rows (522 vs 523, 830 vs 831,
1007 vs 1008, …), and the unmatched sets are different.

**The manuscript uses Table1** (30 matched / 11 unmatched), so the manuscript is
internally consistent. But `03_Processed_Results` is stale and would contradict
the paper if a reviewer or reader checked it.

**Action needed:** regenerate `03_Processed_Results/Experimental_vs_DFT_comparison.csv`
from the notebook, or delete it. Leaving both in a public archive is the kind of
discrepancy that damages credibility.

---

## 8. Files

| File | |
|---|---|
| `NAM_alpha_Gaussian16_B3LYP-D3BJ_6-311++Gdp.log` | the completed run |
| `NAM_alpha_calculated_modes_all_111.csv` | all 111 modes, scaled, with intensities |
| `alpha_analysis.py` | parsing and matching |
| `alpha_rigour.py` | decoy control and tolerance sensitivity |
| `../04_Figures/FigS_alpha_anomer_test.png` | 5-panel summary figure |
