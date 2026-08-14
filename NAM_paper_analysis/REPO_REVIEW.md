# Review: github.com/Sukesh-Periyasamy/nam-data

Cloned and checked. **The data is sound and most of the plotting is fine. But
the headline result — RMSE 2.12 cm⁻¹ across 51 matched peaks — is an artefact
and should not go into a paper.**

---

## What's in the repo

- The same five acquisition folders I worked from (81 spectra; the repo omits
  `NAM-15secs and power15-75-2sets`, so 81 rather than 98)
- `all_excel_files/` — 82 converted spreadsheets
- `simdata.xlsx` — the simulated spectrum
- Four notebooks and 14 output figures

I verified `simdata.xlsx` really does come from your Gaussian calculation: 20 of
the 25 strongest true normal modes appear in it within 8 cm⁻¹. The underlying
computation is fine.

---

## Problem 1 — the RMSE is a selection effect

`NAM_Raman_Analysis.ipynb` matches experimental peaks to simulated peaks using
a **±10 cm⁻¹ tolerance**, then computes RMSE over the matched pairs only.

That construction guarantees a small number. Any band that disagrees by more
than 10 cm⁻¹ is not counted as a failure — it silently disappears from the
statistic. Running the same procedure on my data:

| Tolerance | Bands matched | Bands dropped | RMSE over matched |
|---|---|---|---|
| ±3 | 9 | 32 | 1.73 cm⁻¹ |
| ±5 | 15 | 26 | 2.83 cm⁻¹ |
| **±10** | **28** | **13** | **5.98 cm⁻¹** |
| ±18 | 33 | 8 | 10.70 cm⁻¹ |
| ±40 | 39 | 2 | 23.66 cm⁻¹ |

The reported RMSE is essentially a readout of the window you chose. Narrow the
window and the agreement "improves" while a third of your spectrum quietly
falls out of the analysis.

See `DIAGNOSTIC_tolerance_effect.png`.

**A referee will spot this.** The report states 51 matches but never states how
many experimental peaks failed to match, which is the number that actually
matters.

## Problem 2 — 2.12 cm⁻¹ is below the resolution of the inputs

- `simdata.xlsx` is sampled on a **uniform 8 cm⁻¹ grid** (7.68 after ×0.96
  scaling) — 500 points from 0 to 3992 cm⁻¹. These are not discrete normal
  modes; it is a pre-broadened curve.
- Your experimental sampling is 1.4–1.8 cm⁻¹ per pixel.

Quoting agreement to 2.12 cm⁻¹ when the simulated data is quantised at 7.68 cm⁻¹
is not defensible. You cannot resolve a difference finer than the grid you are
comparing against.

## Problem 3 — matching to blends, not modes

The broadened curve has ~35 peaks in 400–1800 cm⁻¹. The Gaussian log has **67
modes** in that range. Broadening has merged them.

So a "matched DFT peak" is often several overlapping modes, and quoting a
difference of 0.0 or 0.1 cm⁻¹ against a blend has no physical meaning. Matching
should be done against the discrete frequency list in the `.LOG`, which is what
I did.

## Problem 4 — the overlay figure contradicts the table

In `fig03_experimental_vs_DFT_overlay.png` the agreement is visibly poor:

- strong simulated peaks near 1340 and 1430 cm⁻¹ have no experimental
  counterpart of comparable intensity
- strong experimental bands at 872, 930 and 956 cm⁻¹ do not line up with
  simulated features

A table claiming ±1–3 cm⁻¹ agreement sitting next to a figure that disagrees
this visibly is exactly the kind of internal inconsistency reviewers pick up on.

## Smaller issues

- Report says the best spectrum is `sec-25_power-80`, but fig03 plots
  `sec-25_power-75`.
- Plot range runs to 3000 cm⁻¹ while experimental data ends at 2842 — the last
  ~150 cm⁻¹ is noise, and the simulated curve shoots up there, making the
  comparison look worse than it is.
- A `+0.05` vertical offset is applied to the simulated trace. Fine for display,
  but it must be stated in the caption if the figure is used.
- `README.md` is 10 bytes.

---

## What is genuinely good

- The acquisition-parameter analysis is sensible and agrees with mine: 25 s /
  75–80% comes out best.
- The waterfall plot (`fig04`) is a nice way to show reproducibility.
- The processing order — Savitzky–Golay, ALS, normalise — matches what I used.
- Converting everything to a single `all_excel_files/` directory with encoded
  filenames was a good move.

---

## What I'd do

**Don't use the 51-peak / 2.12 cm⁻¹ result.** Replace it with the analysis in
the manuscript, which matches against the 111 discrete modes in the `.LOG`,
uses a ±18 cm⁻¹ window, and reports the 8 unmatched bands openly:

> MAE 9.4 cm⁻¹, RMSE 10.7 cm⁻¹, r = 0.9997, 33 of 41 bands matched

That number is larger, and it is the honest one. For gas-phase harmonic B3LYP
against a crystalline powder it is also the *expected* magnitude — the 1994
study, using a force field fitted to its own data, reported 4 cm⁻¹. An unfitted
gas-phase calculation beating that by half would not be believed, and rightly so.

**Two things worth keeping from the repo:**

1. The `NAM-15secs and power15-75-2sets` folder is missing from the repo but
   present in `mtp`. Add it — those are your only genuine replicates.
2. If you push the analysis scripts I wrote alongside the paper, the repo
   becomes a proper data-availability deposit. Say the word and I'll copy them
   into your folder.
