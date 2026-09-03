# NAM_Master_Dataset — Consolidated Archive

**N-Acetylmuramic Acid: Powder Raman, DFT Simulation (α/β anomers), and SERS — everything in one place**

Compiled 28 August 2026 · Sukesh P, Department of Electrical Engineering, IIT Jodhpur

This folder consolidates every NAM-related dataset that was previously scattered
across four separate folders (`NAM_Raman_Archive`, `13-08-2026-raw-si`,
`12-08-26`, `14-08-2026-sers-r6g-nam-2m-1700g-8.6-etched-si`), plus the two DFT
anomer calculations and the full analysis history. 750 files, ~168 MB.
Nothing was deleted from the original folders — everything here is a copy.

---

## 1. Sample

| | |
|---|---|
| Compound | N-Acetylmuramic acid (NAM, MurNAc, NAMA) |
| Supplier | Sigma-Aldrich (Merck), catalogue **A3007-100MG**, CAS 10597-89-4, lot **BCCK5768** |
| Formula / MW | C₁₁H₁₉NO₈ / 293.27 g/mol (anhydrous) |
| Purity | ≥98% (TLC), synthetic, made in Switzerland |
| Form | White powder, used as received, no purification |
| **Anomeric configuration** | **NOT specified by the supplier — α/β mixture**, normal for a reducing sugar |

## 2. Machine specs — Raman instrument

| | |
|---|---|
| System | B&W Tek i-Raman Plus, model BWS465-785H |
| Spectrometer / microscope | BTC665N-785H-SYS / BAC102-785E, 20× Plan objective |
| Laser | 785 nm (784.92 nm actual), Class 3B, 0–100% in 1% steps |
| Laser power budget | 495 mW safety label max → 455 mW at laser port → **340 mW exiting probe** → power at sample **unmeasured** (needs a power-meter check) |
| Detector | 2048-pixel TE-cooled CCD (−2 °C) |
| Spectral range | −46 to 2842 cm⁻¹ specified; usable analysis window 400–1800 cm⁻¹ |
| Resolution | < 3.5 cm⁻¹ (manufacturer spec, atomic emission lines at 912 nm) |
| Dark correction | instrument software, `Dark Subtracted #1` column |

## 3. Machine specs — DFT compute

| | |
|---|---|
| Software | Gaussian 16, Revision C.01 (EM64W-G16RevC.01, Windows 64-bit) |
| Method / basis | B3LYP-D3BJ (Grimme D3 dispersion, Becke-Johnson damping) / 6-311++G(d,p) |
| Route | `opt=(calcfc,tight) freq=raman b3lyp/6-311++g(d,p) empiricaldispersion=gd3bj geom=connectivity int=ultrafine scf=(tight,xqc)` |
| Phase | Gas phase, isolated molecule, no solvation |
| Resources | 16 shared-memory processors, 48 GB RAM |
| β-anomer runtime | 3 h 42 min optimisation + 58 min frequencies ≈ 4 h 41 min |
| α-anomer runtime | 2 h 39 min optimisation (27 steps) + 1 h 03 min frequencies = 3 h 42 min |
| Basis functions | 573 (593 Cartesian) for both anomers |
| Imaginary frequencies | 0 for both — both are confirmed true minima |
| Frequency scaling | 0.980 below 1800 cm⁻¹, 0.967 above |

---

## 4. Folder guide

| Folder | Contents | Files |
|---|---|---|
| `00_README_AND_INDEX` | this file + file-level indexes | — |
| `01_Powder_Raman_OLD_April_Optimisation_Grid` | **OLD** powder data — 20–24 April session. Systematic grid: 5 integration times × 16 power levels. One spectrum per condition, *not* replicates. Used to find the safe/optimal acquisition setting, not to build the reference spectrum. | 98 |
| `02_Powder_Raman_NEW_May_Replicates` | **NEW** powder data — 29–30 May session. Nine replicate sets at fixed conditions, fresh spot per measurement. **The reference spectrum used in every downstream comparison is built from this set (sets R2+R4, n=22).** | 104 |
| `03_Powder_Raman_Photostability_Test` | 10 consecutive scans, same spot, 90%/30s, no stage movement — proves the sample doesn't degrade under prolonged illumination at that setting. | 10 |
| `04_Powder_Raman_Glass_Blanks` | Empty-slide blanks, but only at 5%/5s/1 accumulation — **does not match the sample condition**; blanks at 70%/25s/5acc are still needed. | 5 |
| `05_Powder_Raman_EXCLUDED_Laser_Damage` | 90%/60s destroys the sample (r drops to 0.01–0.40 across repeats). Kept deliberately to document the damage threshold — **do not use as NAM spectra.** | 10 |
| `06_Powder_Processed_Results` | Reference spectrum, peak list, DFT-simulated spectrum, and the exp-vs-DFT comparison table. **See the data-quality caveat in §6 below before trusting the comparison CSV.** | 4 |
| `07_DFT_Alpha_Anomer` | Full Gaussian 16 run for the α-anomer: input, geometry, log, all 111 calculated modes, plus the write-up of why this run was performed and what it found. | 6 |
| `08_DFT_Beta_Anomer` | Full Gaussian 16 run for the β-anomer — **the model used throughout the manuscript.** | 4 |
| `09_DFT_Alpha_vs_Beta_Comparison` | The rigorous statistical test of whether the α-anomer explains bands the β-anomer misses (it doesn't — see §6). Structure comparison image, analysis/control scripts, 5-panel summary figure. | 4 |
| `10_SERS_R6G_Calibration` | Rhodamine 6G reference measurements used to pick the best-performing etched substrate, from both the 12 Aug screening session and the 14 Aug session on the substrate that was ultimately used for NAM. | 45 |
| `11_SERS_NAM_Measurements_2min_Etched_14Aug` | The actual NAM SERS measurements (43 usable spectra) on the R6G-selected 2-minute-etched Ag/Si substrate, 14 August. **Note:** the source subfolder was named `1m-etcheddata-` on disk even though the parent folder and every other file in this dataset describe it as the 2-minute etch — flagged here so the mislabel doesn't get carried forward silently. | 56 |
| `12_SERS_Matched_Blank_2min_Etched_NoSample` | **The true matched blank**: bare Si, same AgNO₃/HF recipe and 2-minute etch time as the NAM substrate, no NAM present — from two separate substrate pieces (`substrate_A`, `substrate_B`). This is the control that the final peak-validation conclusions in the report rest on. | 80 |
| `13_SERS_Substrate_Screening_5min_10min_12Aug` | The original 12 Aug substrate-selection experiment: NAM and R6G measured on 2-min, 5-min, and 10-min-etched substrates side by side, which is how the 2-minute etch was chosen. | 121 |
| `14_SERS_Blank_Substrates_Mismatched_Etch_5min_10min` | Blank (no-sample) spectra on the 5-min and 10-min-etched substrates — **not** the exact 2-min condition used for NAM, so treat these as a secondary, less direct check than folder 12. | 45 |
| `15_SERS_Bare_Si_Reference_13Aug` | Bare-silicon reference spectra (organized-by-condition set + a raw substrate-1 set) used to confirm the ~517 cm⁻¹ line seen in every SERS spectrum is the silicon phonon line, not a NAM band. | 91 + 1 report |
| `16_Analysis_Figures` | Every figure generated across the full analysis: powder-vs-DFT overlay and peak-matching table, literature comparison, α-vs-β test figure, all SERS overlays and validation figures. | 20 |
| `17_Analysis_Reports` | The consolidated written report (this analysis, in full). | see report |
| `18_Manuscript` | The existing LaTeX/Word/PDF manuscript and supplementary material (multiple drafts, `v2_final` is the latest). | 38 |
| `19_Original_Analysis_Notebook` | The original Jupyter notebook and protocol document (`ANALYSIS_PROTOCOL.md`) that defines the exact preprocessing pipeline replicated throughout this analysis. | 8 |

---

## 5. Processing pipeline (applied identically to every spectrum in this archive)

1. Extract `Raman Shift` and `Dark Subtracted #1` from the instrument CSV.
2. Interpolate to a uniform 1 cm⁻¹ grid, 400–1800 cm⁻¹.
3. Asymmetric Least Squares baseline correction (λ = 1×10⁵, p = 0.001, 10 iterations).
4. Savitzky–Golay smoothing (window 11, polynomial order 3).
5. Min–max normalisation (display spectra only).
6. Peak detection validated against local noise on two independent criteria (≥3σ prominence and height, ≥50% of replicate spectra).

## 6. Data-quality caveats — read before reusing any file here

- **Two disagreeing exp-vs-DFT comparison tables exist in the source archive.** `19_Original_Analysis_Notebook/tables/Table1_experiment_vs_DFT.csv` reports 30/41 bands matched (11 unmatched) and is what the manuscript actually uses. `06_Powder_Processed_Results/Experimental_vs_DFT_comparison.csv` reports 33/41 matched (8 unmatched) and is **stale** — peak positions differ by 1–2 cm⁻¹ in at least 12 rows. The manuscript is internally consistent (it uses Table1); the processed-results CSV should be regenerated from the notebook or deleted, not treated as current.
- **The α-anomer hypothesis was tested and rejected** as an explanation for the DFT-unmatched bands. A shifted-β decoy control matched just as many bands as the real α calculation (p = 0.46) — the apparent improvement is statistical noise, not chemistry. β remains the correct reference model, both because it is more thermodynamically stable (+3.10 kcal/mol Gibbs free energy over α) and because it fits the experimental spectrum marginally better on its own. Full reasoning in `07_DFT_Alpha_Anomer/ALPHA_ANOMER_RESULT.md`.
- **The DFT calculation is gas-phase, isolated-molecule** — it cannot reproduce the four experimental bands between ~1535–1720 cm⁻¹ (1589, 1637, 1652, 1702 cm⁻¹), which most likely arise from solid-state intermolecular hydrogen bonding to the amide/carboxyl carbonyls. This gap is present in both anomers and is a better-supported explanation than any anomeric effect.
- **The sample is an α/β anomeric mixture**; both DFT models are single anomers, and the literature comparison source is a pure crystalline α-anomer. Residual peak offsets against DFT and literature should be read with this in mind, not treated as calculation error.
- **No blank exists for the exact 2-minute-etched substrate at the exact same physical spot** used for the NAM SERS measurement — folder 12 is the closest available control (same recipe, same etch time, different substrate pieces), and folder 14 is a secondary, mismatched-etch-time control. Both are documented in the report; neither is a perfect same-spot before/after blank.
- **Glass blanks for the powder measurement (folder 04)** were only recorded at 5%/5s/1acc, not at the 70%/25s/5acc condition actually used for the sample — a substrate control at matching conditions is still outstanding.

See `17_Analysis_Reports/NAM_Complete_Analysis_Report.docx` for the full write-up, including the powder old-vs-new comparison, the α-vs-β DFT test, literature cross-check, and the complete SERS validation chain.
