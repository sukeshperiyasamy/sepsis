# Analysis Protocol

Complete specification of how the NAM Raman data is processed, from raw
instrument files to publication figures. Everything here is implemented in
`NAM_Analysis.ipynb`, which has already been executed — every figure and table
in `figures/` and `tables/` was produced by running it top to bottom.

---

## 1. Why run the notebook rather than plot ad hoc

Three reasons, all of which matter for a paper:

**Consistency.** Every spectrum passes through the same preprocessing, and every
figure uses the same colours, fonts and sizing. Parameters live in one `CFG`
dictionary, so nothing can drift between figures.

**Reproducibility.** A reviewer or a future student can re-run one file and get
identical numbers. The notebook is also the natural thing to deposit alongside
the data.

**Traceability.** Every number in the manuscript comes from a cell you can point
at. If a parameter changes, re-run and every figure updates together.

---

## 2. Project structure

```
NAM_Raman_Archive/
├── 00_READ_ME_FIRST.md/.docx      sample and instrument details
├── FILE_INDEX.csv                 227 files with conditions   ← notebook input
│
├── 01_Raman_Data/                                             ← notebook input
│   ├── A_Optimisation_Grid_April/     98   acquisition survey
│   ├── B_Replicates_May/             104   fixed-condition replicates
│   ├── C_Photostability_May/          10   same spot, 90% / 30 s
│   ├── D_Glass_Blanks/                 5   empty slide
│   └── E_EXCLUDED_Laser_Damage/       10   90% / 60 s, destroyed
│
├── 02_DFT_Calculation/                                        ← notebook input
│   ├── NAM_beta_Gaussian16_B3LYP-D3BJ_6-311++Gdp.log
│   ├── NAM_beta_Gaussian16_input.gjf
│   ├── NAM_beta_optimised_geometry.xyz
│   └── NAM_calculated_modes_all_111.csv
│
├── 03_Processed_Results/          earlier processed outputs
├── 04_Figures/                    earlier figures
├── 05_Manuscript/v2_final/        the paper
│
└── 06_Analysis_Notebook/          ← this folder
    ├── ANALYSIS_PROTOCOL.md       this file
    ├── NAM_Analysis.ipynb         the pipeline, already executed
    ├── figures/                   9 figures, 300 dpi          ← notebook output
    └── tables/                    5 CSVs + summary JSON       ← notebook output
```

### Which data feeds which result

| Set code | n | Condition | Used for |
|---|---|---|---|
| `GRID` | 98 | 5–80% × 5–25 s | Acquisition survey, Fig 3 |
| `R2` | 11 | 70%, 10 s, 5 acc | **Reference spectrum** |
| `R4` | 11 | 90%, 10 s, 5 acc | **Reference spectrum** |
| `R6` | 3 | 70%, 30 s, 5 acc | Weak-band validation |
| `R7` | 3 | 70%, 60 s, 5 acc | Weak-band validation |
| `R8` | 5 | 90%, 30 s, 5 acc | Weak-band validation |
| `R1`, `R3`, `R9` | 61 | various | Consistency check only |
| `R5` | 10 | 70%, 10 s, 5 acc | **Excluded** — see §7 |
| `SS1` | 10 | 90%, 30 s, same spot | Photostability, Fig 4 |
| `DMG1`, `DMG2` | 10 | 90%, 60 s | Damage threshold, Fig 4 |
| `BLANK` | 5 | 5%, 5 s | Substrate check |

---

## 3. Preprocessing

Applied identically to all 227 spectra. Order matters — do not rearrange.

| Step | Operation | Parameters |
|---|---|---|
| 1 | Read `Raman Shift` and `Dark Subtracted #1` from the B&W Tek CSV | — |
| 2 | Sort by wavenumber, interpolate onto a uniform grid | 400–1800 cm⁻¹, 1 cm⁻¹ step |
| 3 | Asymmetric least-squares baseline removal | λ = 1×10⁵, p = 0.001, 10 iterations |
| 4 | Savitzky–Golay smoothing | window 11, polynomial order 3 |
| 5 | Min–max normalisation | → [0, 1] |

**Baseline.** ALS is used because the substrate and residual fluorescence give a
slowly varying background that a polynomial fit handles poorly near strong bands.
λ = 1×10⁵ is stiff enough not to follow real peaks; p = 0.001 weights points
below the curve heavily, which is correct for emission-type backgrounds.

**Smoothing.** Window 11 at 1 cm⁻¹ spacing means an 11 cm⁻¹ kernel, comfortably
narrower than the ~10 cm⁻¹ FWHM of the bands, so peak positions and widths are
preserved. Third order avoids flattening peak tops.

**Normalisation.** Min–max rather than vector normalisation, so relative
intensities can be read directly off the plots.

---

## 4. Signal-to-noise

Two different measures, used for different purposes.

**Global SNR** — for ranking whole spectra:

```
SNR = (max intensity − median) / σ_noise
σ_noise = std(diff(spectrum above 1750 cm⁻¹)) / √2
```

The √2 accounts for differencing inflating the variance. Above 1750 cm⁻¹ there
are no strong bands, so this region estimates detector noise.

**Local noise** — for judging individual peaks:

```
σ_local(i) = std(diff(spectrum[i−50 : i+50])) / √2
```

A ±50-point window means noise is estimated near each peak rather than globally.
This matters because noise is not uniform across the spectrum.

---

## 5. Peak identification — the two-criterion test

This is the part most easily got wrong, so it is worth stating carefully.

**The trap:** baseline correction and smoothing generate *reproducible* residual
structure. A wiggle appearing in every spectrum is not evidence that it is a real
band — it may just be the same processing artefact each time. Reproducibility
alone is not a sufficient criterion.

**The test.** Each candidate peak is measured against local noise two ways:

- **prominence / σ_local** — how far the peak rises above its surrounding valleys
- **height above local median / σ_local** — how far it rises above the baseline

Both measure something different. Prominence handles shoulder peaks correctly but
can be inflated by noisy valleys. Height handles isolated peaks correctly but
under-rates shoulders sitting on a strong neighbour. Requiring both to exceed
3× local noise catches genuine bands of either kind while rejecting artefacts.

**Classification:**

| Both ≥ 3σ | One ≥ 3σ | Confirmed in long-integration data | Result |
|---|---|---|---|
| ✓ | — | — | **high confidence** |
| ✗ | ✓ | ✓ (and ≥ 3σ there) | **high confidence** (promoted) |
| ✗ | ✓ | ✗ | **tentative** |
| ✗ | ✗ | — | **rejected** |

The promotion step uses `R6+R7+R8` (30 and 60 s, SNR up to ~800), an
*independent* dataset from the reference. Two bands — 1007 and 1112 cm⁻¹ — were
promoted this way.

Additionally, a band must be independently detected in ≥50% of the 22 reference
spectra to be reported at all.

**Result:** 41 bands — 32 high confidence, 9 tentative. Five candidates rejected
(424, 558, 800, 901, 1629 cm⁻¹).

---

## 6. DFT processing

Parsed directly from the Gaussian log, not from any intermediate file.

| Step | Detail |
|---|---|
| Parse | Frequencies, Raman activities, IR intensities, and Cartesian displacement vectors |
| Scale | ×0.980 below 1800 cm⁻¹, ×0.967 above (Ma et al. scheme) |
| Intensities | Placzek expression at 785 nm, 298.15 K |
| Broaden | Lorentzian, FWHM 10 cm⁻¹ |

**Why parse the log and not a spreadsheet.** The displacement vectors only exist
in the log, and they are what distinguish a ring-breathing mode from a
hydroxymethyl wag at similar frequency. A pre-broadened curve on a coarse grid
cannot support mode assignment, and matching to one produces spuriously small
errors.

**Placzek intensities.** Raman *activity* is not intensity. Converting requires
the excitation frequency and a Boltzmann factor:

```
I ∝ (ν₀ − ν)⁴ · S / { ν · [1 − exp(−hcν/kT)] }
```

Without this the low-frequency region is badly over-weighted.

**Mode character.** For each mode the fraction of mass-weighted displacement
carried by each atom, and by the pyranose ring, is computed from the displacement
vectors. Connectivity comes from interatomic distances against covalent radii.
This is not a full PED analysis and the notebook says so — but it is quantitative,
reproducible, and sufficient to separate ring modes from substituent modes.

---

## 7. Matching and statistics

Each observed band is matched to the calculated mode of **highest Raman
activity** within ±18 cm⁻¹.

**Why ±18 and not ±10.** A narrow window guarantees a small RMSE by construction:
bands that disagree are silently dropped rather than counted as failures. The
notebook prints a tolerance sensitivity table showing exactly this. At ±5 cm⁻¹
the RMSE looks excellent but most bands vanish from the statistic. Reporting
unmatched bands openly is the honest approach, and ±18 is wide enough to admit
genuine assignments while remaining physically meaningful.

**Reported:** MAE, RMSE, maximum absolute deviation, correlation coefficient,
mean signed deviation, and the list of unmatched bands.

**Current values:** 41 bands, 30 matched, MAE 9.3 cm⁻¹, RMSE 10.3 cm⁻¹,
r = 0.9996, mean signed +1.6 cm⁻¹.

---

## 8. Figure naming

Manuscript figures are `figN_shortname.png`; supplementary are `figSN_...`.
All are 300 dpi PNG with tight bounding boxes.

| File | Figure | Content |
|---|---|---|
| `fig1_structure.png` | 1 | DFT-optimised geometry, two views (generated separately) |
| `fig2_reference.png` | 2 | Reference spectrum, mean ± SD, n = 22 |
| `fig3_optimisation.png` | 3 | Acquisition survey — SNR heat map and power curves |
| `fig4_photostability.png` | 4 | Photostability, damage, and band decay |
| `fig5_simulated.png` | 5 | Simulated spectrum, sticks and broadened |
| `fig6_overlay.png` | 6 | Experiment vs theory with residual panel |
| `fig7_region730.png` | 7 | The 730 cm⁻¹ region |
| `figS1_qc_overview.png` | S1 | Signal quality and spectra count by set |
| `figS2_correlation.png` | S2 | Correlation matrix between set-mean spectra |
| `figS3_peak_validation.png` | S3 | Peak confidence and SNR criteria |

### Style, applied globally

| | |
|---|---|
| Font | DejaVu Sans, 9 pt |
| Experimental | `#1f3864` (dark blue) |
| Simulated | `#c0392b` (red) |
| Stable / pass | `#2ecc71` |
| Warning / tentative | `#e67e22` |
| Grid | alpha 0.15, linewidth 0.5 |
| Resolution | 300 dpi, `bbox_inches="tight"` |

Single-column figures are ~4.6 in wide, double-column ~7.4 in. These match
Elsevier's column widths, so figures are not rescaled at typesetting.

---

## 9. Outputs

| File | Contents |
|---|---|
| `tables/Table1_experiment_vs_DFT.csv` | Table 1 — observed, calculated, Δ, activity, assignment |
| `tables/Experimental_peak_list.csv` | 41 bands with all confidence metrics |
| `tables/Experimental_reference_spectrum.csv` | Mean ± SD on the 1 cm⁻¹ grid |
| `tables/DFT_simulated_spectrum.csv` | Broadened simulated spectrum |
| `tables/DFT_all_modes.csv` | All 111 modes, scaled and unscaled |
| `tables/analysis_summary.json` | Config and headline statistics, machine-readable |

---

## 10. Known issues in the data

Documented so they are not rediscovered later.

**Set R5 is excluded.** It correlates at only 0.70–0.79 with the other sets,
which all sit at 0.94–0.99, despite nominally identical conditions to R2 (70%,
10 s, 5 acc). Cause unknown — possibly sample loading or focus. Visible in
`figS2_correlation.png`. Flagged for the author to check against lab notes.

**Power confounded with acquisition order in the April grid.** Power was stepped
5% → 80% in file order, so the two cannot be separated statistically. The
photostability measurements address this directly and the manuscript says so.

**Glass blanks are at the wrong settings.** 5% / 5 s / 1 accumulation, not the
reference condition. Three blanks at 70% / 25 s / 5 acc are still needed.

**Range stops at 2842 cm⁻¹.** No C–H or O–H stretch region, so the residual
methanol declared by the supplier (≤1 mol/mol) cannot be tested.

**Two sets destroyed by the laser.** 90% / 60 s, kept in
`E_EXCLUDED_Laser_Damage` and excluded from all vibrational analysis.

---

## 11. Running it

```bash
cd NAM_Raman_Archive/06_Analysis_Notebook
jupyter notebook NAM_Analysis.ipynb
```

Then Run All. Takes a few minutes, mostly the ALS baseline on 227 spectra.

Requires: numpy, pandas, scipy, matplotlib. Paths are relative, so the archive
folder can be moved or shared as-is.

**To change a parameter**, edit `CFG` in cell 1 and re-run. Everything downstream
updates consistently — that is the point of keeping it in one place.
