# Version 2 — Rebuilt on the Full Archive

The paper has been rewritten from scratch using all 227 spectra. Every number in
it now traces to the archive.

---

## What changed

### The reference spectrum is now built from real replicates

**Before:** mean of 40 spectra taken at 40 *different* acquisition conditions.
Defensible, but not a replicate set — and a reviewer would have asked.

**Now:** mean of **22 independent measurements on fresh sample** at a single
integration time (10 s, 5 accumulations), across two laser powers (70% and 90%).

- Mean pairwise correlation among contributing spectra: **0.986**
- The two contributing sets agree with each other at **r = 0.992**, which
  demonstrates the spectrum is independent of laser power within the stable
  regime

### New section: photostability and laser-damage threshold

This is the biggest addition, and it came out of your May data.

- At 90% power / 30 s the spectrum is unchanged over **ten consecutive scans**
  on the same spot — the 930 cm⁻¹ band varies by under 2%
- At 90% power / **60 s** the sample is destroyed: I(930) falls 0.44 → 0.23 over
  five scans, correlation with the reference drops to r = 0.06–0.31

Figure 3 shows both series side by side plus the quantitative decay curve. The
working envelope is stated as a table.

Carbohydrate powders are usually assumed to tolerate near-infrared excitation
indefinitely. Showing an abrupt threshold is a genuine contribution, and it also
justifies your choice of conditions instead of leaving it as an assertion.

### Weak bands now cross-validated

Bands passing only one of the two noise criteria are tested against an
**independent** long-integration dataset (30 and 60 s, SNR up to 796) and
promoted if confirmed there. Two bands — 1007 and 1112 cm⁻¹ — were promoted this
way.

Result: **32 high confidence + 9 tentative**, versus 29 + 12 before.

### Honest note about the power series

The Methods now state plainly that in the April survey power was stepped in
ascending order, so power and cumulative exposure are not statistically
separable — and that the photostability measurements were designed to address
that directly. Better to say it than have a referee find it.

---

## Final numbers

| | |
|---|---|
| Spectra in archive | 227 |
| Reference spectrum | 22 independent measurements |
| Bands reported | 41 (32 high confidence, 9 tentative) |
| Matched to calculated modes | 30 |
| MAE | **9.3 cm⁻¹** |
| RMSE | **10.3 cm⁻¹** |
| Correlation | **0.9996** |
| Mean signed deviation | +1.6 cm⁻¹ |
| High-confidence bands only | MAE 9.2, RMSE 10.2 |

Unmatched: 772, 830, 956, 1517, 1589, 1637, 1652, 1663, 1702, 1785, 1797 cm⁻¹ —
nine of the eleven above 1500 cm⁻¹, where the isolated-molecule model is least
applicable. Discussed openly in Section 3.8.

---

## Files

| File | What |
|---|---|
| `manuscript.tex` | **Submit this.** Elsevier `elsarticle` format for Overleaf |
| `manuscript_preview.pdf` | Compiled preview, 14 pages |
| `manuscript_WORD.docx` | Word version |
| `supplementary.tex` / `.pdf` / `.docx` | Sample, instrument, inventory, coordinates, all 111 modes |
| `figures/` | Seven figures at 300 dpi |
| `table3.tex` | Table 1 rows (already inlined) |

Both documents compile with **zero errors and zero undefined references**.

### Figures

1. DFT-optimised structure, two views, groups labelled
2. Reference spectrum, mean ± SD from 22 measurements
3. Acquisition survey — SNR heat map and power curves
4. **Photostability and damage threshold** — new
5. Simulated spectrum, sticks and broadened
6. Experimental vs simulated overlay with residual panel
7. The 730 cm⁻¹ region

---

## Still needed from you

Marked in **red** in the PDF:

1. Lot number from the bottle
2. Power at sample in mW — then the damage threshold can be quoted as a power
   density, which is far more useful to other groups than "90%"
3. Spectral resolution in cm⁻¹
4. Glass blanks at the reference condition (the five you have are at 5% / 5 s)
5. Co-authors and CRediT contributions
6. Funding and acknowledgements
7. Gaussian 16 revision letter
8. References: 14 → 30–45
9. Verify the Kouach 1994 citation — I inserted plausible values, the volume and
   pages are **unverified**

And one verification: open the `.LOG` in GaussView and confirm mode 41
(731 cm⁻¹) is the carboxylic acid O–H wag. The central claim rests on it.

---

## Things I would still like to check with you

**The damage mechanism.** In the fresh-spot series at 90% / 60 s the signal also
declines across spots (r = 0.40 → 0.01). If those spots were genuinely fresh
powder, that's odd — it would suggest thermal damage spreading beyond the
illuminated spot, which is worth saying explicitly. If they were near
already-burned regions, the write-up should say so instead. Currently the text
just reports that the behaviour is the same on fresh spots.

**Set R5** (70%, 10 s, 5 acc, 10 spectra) correlates at only 0.70–0.79 with the
other sets, whereas every other set sits at 0.94–0.99. It is excluded from the
reference spectrum. Do you recall anything different about that run — different
sample loading, a different day, focus problems?
