# NAM Raman + DFT Manuscript — Deliverables

Generated 4 August 2026 from your Gaussian log and 98 experimental Raman spectra.

---

## The manuscript

| File | What it is |
|---|---|
| `latex/manuscript.tex` | **Primary deliverable.** Elsevier `elsarticle` format, ready for Overleaf. |
| `latex/manuscript_article.tex` | Fallback using standard `article` class — compiles anywhere. |
| `latex/manuscript_article.pdf` | Compiled preview, 12 pages. |
| `manuscript_WORD.docx` | Word version if you prefer to edit there. |
| `latex/figures/` | All five figures at 300 dpi. |
| `latex/table3.tex` | Table 3 rows (already inlined into the .tex files). |

**To use on Overleaf:** upload `manuscript.tex` and the `figures/` folder. `elsarticle.cls` is
available there by default. Compile with pdfLaTeX.

---

## Data files

| File | Contents |
|---|---|
| `Table_DFT_all_modes.csv` | All 111 calculated modes: frequency, scaled frequency, Raman activity, IR intensity, reduced mass, assignment |
| `Table_DFT_fingerprint_region.csv` | The 67 modes in 400–1800 cm⁻¹ |
| `DFT_simulated_spectrum.csv` | Broadened simulated spectrum (x, y) |

---

## What the analysis found

**DFT** — Gaussian 09, B3LYP/6-311+G(d,p), gas phase. Normal termination, 111 modes,
zero imaginary frequencies. Formula confirmed C₁₁H₁₉NO₈, 39 atoms.

**Experimental** — 261 CSV files reduced to **98 unique** spectra (see caveat below).
40 spectra with SNR ≥ 100 used to build the reference spectrum. Mean pairwise
correlation 0.957. **41 bands** identified at ≥50% detection confidence; 33 of these
appear in all 40 spectra.

**Agreement** — 34 of 41 bands matched to calculated modes:

- MAE = 9.8 cm⁻¹
- RMSE = 11.0 cm⁻¹
- max |Δ| = 17.1 cm⁻¹
- r = 0.9996
- mean signed Δ = +2.2 cm⁻¹

**The 730 cm⁻¹ result** — the calculated mode at 727 cm⁻¹ is 48.3% displacement of a
single hydrogen, which connectivity identifies as the carboxylic acid hydroxyl proton
(O–H 0.97 Å → C 1.35 Å → C=O 1.21 Å). Pyranose ring contributes 1.8%. Since that proton
is absent in intact peptidoglycan (the carboxyl is amide-linked to L-alanine), this mode
cannot contribute to the bacterial 730 cm⁻¹ band.

---

## Before you submit — must fix

Items marked in **red** in the PDF (`\authorcheck{...}` in the source):

1. **Reagent details** — supplier, catalogue number, lot, stated purity.
2. **Laser power in mW** — "70% of maximum" is instrument-specific and reviewers will ask.
   Also add objective magnification/NA, grating, and spectral resolution in cm⁻¹.
3. **Gaussian 09 revision number** — check the header of your `.log`.
4. **Co-authors** — supervisor and anyone else, plus CRediT contributions.
5. **Funding and acknowledgements.**
6. **References** — currently 12; expand to 30–45. Priority additions listed as comments
   at the end of the `.tex` file. The most important is the 1994 Kouach harmonic-dynamics
   paper on crystalline NAM — you cite its 4 cm⁻¹ agreement in the Introduction but the
   reference is not yet in the list.

---

## Three things you should know

**1. Your Methods were wrong in the old draft.** The chat notes plan
B3LYP-D3BJ/6-311++G(d,p) with SMD water in Gaussian 16. Your actual completed run was:

```
# opt freq=raman b3lyp/6-311+g(d,p) geom=connectivity
```

Gaussian **09**, **no** dispersion correction, **single**-plus basis, **gas phase**.
The manuscript describes what you actually did. That level is publishable, but it makes
the gas-phase-vs-crystalline-solid argument central to your Discussion — which is how
I have written it.

**2. Most of your files are triplicates.** Of 261 CSVs, only 100 are unique — 80 spectra
appear three times across `10sec-power5-80-2set/`, `data from pc raw powder/` and
`data of Dry powder/`. The folder names say "2set" but after deduplication there is
**one spectrum per (integration, power) condition**, except at 15 s where 2–3 replicates
exist. Two files in `MB 1ugml/` are methylene blue, not NAM, and were excluded.

The manuscript therefore describes the 40 spectra as spanning acquisition conditions
rather than claiming independent replicate measurements at a fixed condition. That is
honest and defensible, but if you have the `nam-new` dataset (10 spots at final settings,
per your notes) it would strengthen Section 3.2 considerably. Send it and I will rerun.

**3. Assignments need your eyes.** The mode characters were derived programmatically from
Cartesian displacement vectors — atom contributions, ring fraction, bond-stretch
projections. The Methods section says so explicitly. This is reproducible and defensible,
but it is not a potential energy distribution analysis. Open the `.log` in GaussView and
check the animations for at least the strongest bands before submission — particularly
the 727 cm⁻¹ mode, since a scientific claim rests on it.

---

## Suggested target

**Spectrochimica Acta Part A** (IF ~4.3) — best fit and impact for a combined
experimental+DFT vibrational study.

Fallback: **Vibrational Spectroscopy**, where Ma et al. (2024) published. Position the
cover letter as the direct experimental validation of their computational NAM work.

Not the J. Photochem. Photobiol. B SERS special issue — this is a vibrational
spectroscopy paper, not a SERS paper. Send your substrate work there instead.

---

*Housekeeping: `latex/` contains LaTeX build artefacts (`.aux`, `.log`, `.out`) and
preview images (`p-*.jpg`, `q-*.jpg`, `pv-*.jpg`). Safe to delete.*
