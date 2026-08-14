# NAM Raman Study — Data Archive

**N-Acetylmuramic Acid: Experimental Raman Spectroscopy and DFT Vibrational Analysis**

Sukesh P · Department of Electrical Engineering, Indian Institute of Technology Jodhpur
Archive compiled 5 August 2026

---

## 1. SAMPLE

| | |
|---|---|
| **Compound** | N-Acetylmuramic acid |
| **Abbreviations** | NAM, MurNAc, NAMA |
| **Supplier** | Sigma-Aldrich (Merck) |
| **Catalogue number** | **A3007-100MG** (100 mg pack) |
| **CAS number** | 10597-89-4 |
| **Lot number** | **BCCK5768** |
| **Formula** | C₁₁H₁₉NO₈ |
| **Molecular weight** | 293.27 g/mol (anhydrous — **not** a hydrate) |
| **Purity** | ≥98% (TLC) |
| **Source** | Synthetic · manufactured in Switzerland |
| **Form** | White powder |
| **Melting point** | 125 °C |
| **Stated impurity** | ≤1 mol/mol methanol |
| **Storage** | 2–8 °C · amber glass bottle |
| **Sample preparation** | Powder placed directly on clean glass microscope slide, used as received, no purification or recrystallisation |

### Structure

**SMILES**
```
CC(O[C@H]1[C@H](O)[C@@H](CO)OC(O)[C@@H]1NC(C)=O)C(O)=O
```

**InChI**
```
1S/C11H19NO8/c1-5(11(18)19)20-10(9(17)8(16)4-14)7(3-13)12-6(2)15/
h3,5,7-10,14,16-17H,4H2,1-2H3,(H,12,15)(H,18,19)/t5-,7+,8-,9-,10-/m1/s1
```

**IMPORTANT — anomeric configuration is NOT specified.** The anomeric carbon in
the SMILES carries no stereo descriptor, and the InChI stereo layer defines only
five centres. The material is an **α/β anomeric mixture**, normal for a reducing
sugar. The DFT calculation models the **β anomer only**.

---

## 2. INSTRUMENT

| | |
|---|---|
| **System** | B&W Tek i-Raman Plus |
| **Model** | BWS465-785H |
| **Spectrometer** | BTC665N-785H-SYS |
| **Microscope** | BAC102-785E Raman microscope |
| **Objective used** | 20× Plan |
| **Other objective available** | 50× LMPlan (NA 0.50, WD 10.5 mm) — not used |
| **Laser wavelength** | 785 nm (784.92 nm reported by software) |
| **Laser power** | Safety label: 495 mW max output · Spec: 455 mW at laser port, **340 mW exiting probe** · 0–100% in 1% steps |
| **Laser class** | Class 3B |
| **Specified range** | 65–2800 cm⁻¹ |
| **Detector** | 2048-pixel TE-cooled CCD, sensor at −2 °C |
| **Spectral range** | −46 to 2842 cm⁻¹ |
| **Spectral sampling** | 1.76 cm⁻¹/pixel at 400 cm⁻¹ → 1.43 cm⁻¹/pixel at 1800 cm⁻¹ |
| **Spectral resolution** | **< 3.5 cm⁻¹** (at 912 nm, atomic emission lines) |
| **Power at sample** | _______________ mW at 70% ← **measure with power meter** (upper bound: 70% × 340 mW = 238 mW at probe, less at sample) |
| **Dark correction** | Applied by instrument software (column `Dark Subtracted #1`) |

### Nominal power reference

**Three different figures apply — do not conflate them:**

| Figure | Value | What it means |
|---|---|---|
| Safety label | 495 mW | Maximum accessible emission, for Class 3B hazard classification |
| Spec, laser port | 455 mW | Manufacturer nominal at the port |
| Spec, exiting probe | **340 mW** | What leaves the fibre-optic probe |
| At sample | **unmeasured** | Lower again — through BAC102 microscope + 20× objective |

Based on 340 mW nominal exiting the probe:

| Setting | Exiting probe |
|---|---|
| 5% | 17 mW |
| 40% | 136 mW |
| 70% | 238 mW |
| 90% | 306 mW |

These are **at the probe**, not at the sample. Further losses occur through the
BAC102 microscope and the 20× objective, so incident power is lower and still
needs direct measurement.

---

## 3. FILE NAMING

```
NAM_P70_T25s_A5_R2_03.csv
│   │   │    │  │  └── sequence number within the set
│   │   │    │  └───── set code (see below)
│   │   │    └──────── accumulations
│   │   └───────────── integration time in seconds
│   └───────────────── laser power, percent of nominal
└───────────────────── sample: NAM powder, or GLASS for blank
```

### Set codes

| Code | Meaning |
|---|---|
| `GRID` | Power × integration optimisation grid (April session) |
| `R1`–`R9` | Replicate sets — fresh spot for each measurement |
| `SS1` | Photostability — same spot, consecutive scans |
| `DMG1`, `DMG2` | Sample destroyed by laser — excluded from analysis |
| `BLANK` | Empty glass slide |

---

## 4. FOLDER CONTENTS

```
NAM_Raman_Archive/
├── 00_READ_ME_FIRST.md          this file
├── FILE_INDEX.csv               every file with its conditions
│
├── 01_Raman_Data/               227 spectra
│   ├── A_Optimisation_Grid_April/     98
│   ├── B_Replicates_May/             104
│   ├── C_Photostability_May/          10
│   ├── D_Glass_Blanks/                 5
│   └── E_EXCLUDED_Laser_Damage/       10
│
├── 02_DFT_Calculation/          Gaussian 16 log, input, geometry, all 111 modes
├── 03_Processed_Results/        reference spectrum, peak list, comparison table
├── 04_Figures/                  publication figures + diagnostics
└── 05_Manuscript/               LaTeX, Word, PDF, supplementary
```

### 01_Raman_Data — what each folder is for

**A_Optimisation_Grid_April** (98 spectra, 20–24 April)
Systematic grid: 5 integration times (5, 10, 15, 20, 25 s) × 16 power levels
(5–80% in 5% steps). Produces the acquisition-optimisation figure. One spectrum
per condition — these are *different conditions*, not replicates.

**B_Replicates_May** (104 spectra, 29–30 May)
Nine replicate sets, each at a single fixed condition with a fresh spot per
measurement. This is the dataset the reference spectrum is built from. Set `R9`
was found misfiled inside a folder named "glass slide empty" — those files are
NAM powder, not glass.

**C_Photostability_May** (10 spectra)
Ten consecutive scans at 90% / 30 s **without moving the stage**. Demonstrates
sample stability under prolonged illumination at that condition.

**D_Glass_Blanks** (5 spectra)
Genuine empty-slide blanks. **Caution:** recorded at 5% / 5 s / 1 accumulation
only, which does not match the sample measurement conditions. Blanks at
70% / 25 s / 5 accumulations are still needed for the substrate control.

**E_EXCLUDED_Laser_Damage** (10 spectra) — **DO NOT USE AS NAM SPECTRA**
90% power with 60 s integration destroys the sample. Correlation with the
reference spectrum falls to r = 0.01–0.40, and the 930 cm⁻¹ band decays
0.44 → 0.23 across five consecutive same-spot scans. Retained deliberately: they
establish the damage threshold.

---

## 5. DAMAGE THRESHOLD

| Condition | Outcome |
|---|---|
| ≤80% power, ≤25 s | safe |
| 70% power, 30 s | safe (r = 0.977) |
| 70% power, 60 s | safe (r = 0.970) |
| 90% power, 30 s | safe (r = 0.948) |
| **90% power, 60 s** | **SAMPLE DESTROYED** |

---

## 6. DFT CALCULATION

| | |
|---|---|
| **Software** | Gaussian 16, Revision C.01 (build EM64W-G16RevC.01, Windows 64-bit) |
| **Method** | B3LYP with Grimme D3 dispersion, Becke–Johnson damping (D3BJ) |
| **Basis set** | 6-311++G(d,p) |
| **Route** | `# opt=(calcfc,tight) freq=raman b3lyp/6-311++g(d,p) empiricaldispersion=gd3bj geom=connectivity int=ultrafine scf=(tight,xqc)` |
| **Phase** | Gas phase, isolated molecule (no solvation model) |
| **Starting geometry** | β anomer, PubChem CID 5462244 |
| **Atoms** | 39 (C₁₁H₁₉NO₈) |
| **Normal modes** | 111 |
| **Imaginary frequencies** | 0 — true minimum confirmed |
| **Termination** | Normal |
| **Frequency scaling** | 0.980 below 1800 cm⁻¹, 0.967 above |
| **Resources** | 16 shared-memory processors, 48 GB |
| **Runtime** | 3 h 42 min optimisation + 58 min frequencies ≈ 4 h 41 min |
| **Thermochemistry** | 298.150 K, 1.00000 atm |

---

## 7. PROCESSING PIPELINE

Applied identically to every spectrum:

1. Extract `Raman Shift` and `Dark Subtracted #1`
2. Interpolate to a uniform 1 cm⁻¹ grid, 400–1800 cm⁻¹
3. ALS baseline correction (λ = 1×10⁵, p = 0.001, 10 iterations)
4. Savitzky–Golay smoothing (window 11, polynomial order 3)
5. Min–max normalisation
6. Build reference spectrum from replicate sets R2 + R4 (n = 22); average, compute standard deviation
7. Peak detection, validated against local noise on two independent criteria
8. Match to calculated modes within ±18 cm⁻¹, preferring highest Raman activity

---

## 8. KEY RESULTS

- Reference spectrum from **22 independent replicate measurements** (sets R2 + R4)
- **41** reproducible bands, 400–1800 cm⁻¹ (32 high confidence, 9 tentative)
- **30** matched to calculated normal modes
- **MAE 9.3 cm⁻¹ · RMSE 10.3 cm⁻¹ · r = 0.9996**
- The mode at **731 cm⁻¹** is out-of-plane carboxylic acid O–H deformation
  (47.9% of displacement), with only **0.5%** pyranose ring character — arguing
  against a muramic acid origin for the bacterial 730 cm⁻¹ SERS marker band
- The **872 cm⁻¹** band is assigned to hydroxymethyl wagging (calculated 873 cm⁻¹)

---

## 9. STILL OUTSTANDING

- [x] ~~Lot number from the bottle~~ — **BCCK5768**
- [ ] Power at sample in mW (power meter at objective focal plane)
- [x] ~~Spectral resolution~~ — **< 3.5 cm⁻¹** (manufacturer spec)
- [ ] Glass blanks at 70% / 25 s / 5 accumulations — 3 spots, 10 minutes
- [x] ~~Extend range above 2842 cm⁻¹~~ — **not possible**; BWS465-785H is specified to 2800 cm⁻¹

---

*Note: an earlier partial copy exists at `mtp/NAM_Raman_Study_2026`. It has
filename collisions and is superseded by this archive — safe to delete.*
