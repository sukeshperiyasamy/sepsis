# Doubts in the Data — and What Would Actually Fix Them

I ran diagnostics rather than guessing. Below is what I found, what I got wrong,
and the specific measurements worth repeating.

---

## First, a correction to my own analysis

I initially thought I had found laser-induced dehydration — the band near
1640 cm⁻¹ drops ~70% across every power ramp, in all six runs. It looked like a
real, reportable effect.

**It isn't.** I tested it against the simpler explanation and the band tracks
*noise level* (r = +0.87) far better than it tracks *power* (r = −0.51). What
was falling was noise amplitude as SNR improved, not a water band.

That matters because it exposed a flaw in **my** peak detection. My original
criterion was prominence plus reproducibility across the 40 spectra. But baseline
correction and Savitzky–Golay smoothing produce *reproducible* wiggles — the same
noise bumps appear in every spectrum and scored 80–100% "confidence."

**Revised peak classification** (peak height and prominence both measured against
local noise):

| | count |
|---|---|
| High confidence (both criteria ≥3× noise) | **29** |
| Tentative (one criterion only) | **12** |
| Rejected as noise | **5** |

Dropped entirely: 411, 428, 901, 1495, 1677 cm⁻¹.
Of these, **411 and 901 cm⁻¹ are currently in Table 3 of the manuscript and must
be removed.** Several others must be downgraded to tentative.

The MAE/RMSE will shift slightly once the table is corrected. I have not yet
propagated this into the manuscript — say the word and I will.

---

## What is genuinely fine — no need to redo

**No laser damage.** I checked this properly. From 5% to 80% power at 25 s:

- 930 cm⁻¹ band position: stable within ±1 cm⁻¹
- 1451 cm⁻¹ band position: stable within ±1 cm⁻¹
- FWHM of the 930 cm⁻¹ band: 10–11 cm⁻¹ throughout
- no carbonaceous background, no band loss

This is a solid, defensible result and the manuscript reports it correctly.
Your instinct to run the full power range was right.

**Spectral reproducibility is good.** Mean pairwise correlation 0.957 across
40 spectra spanning very different acquisition conditions.

---

## Real doubts — ranked by how much they matter

### 1. The 1550–1800 cm⁻¹ region is under-measured — **most important**

Eleven of the twelve tentative peaks fall here. This is not a coincidence: the
spectrum is weak in this window and the noise floor is comparable to the bands.

It is also the chemically most interesting region — amide I, amide II, and the
carboxyl C=O. These are the bands that distinguish muramic acid from
N-acetylglucosamine, and the ones your Discussion leans on.

**Suggested measurement:** dedicated long acquisition on this window only.
Something like 70% power, 60 s, 10 accumulations, 5 fresh spots. If the
instrument allows restricting the readout range, do that. The goal is to get
1590, 1633, 1652, 1700, 1751 and 1792 cm⁻¹ unambiguously above noise, or to
establish that they are not real.

Roughly an hour of instrument time, and it would move ~12 peaks from tentative
to confirmed.

### 2. The O–H and C–H stretch regions were never measured

Your data stops at **2842 cm⁻¹**. The C–H stretch region (2800–3000) and O–H
stretch region (3000–3600) are absent.

Most reviewers of a "reference spectrum" paper will expect them. They would also
settle the hydration question directly — a broad O–H feature near 3400 would tell
you immediately whether the powder carries water.

**Suggested measurement:** extend the range to 3600 cm⁻¹ if the grating allows,
at your optimised settings, 3–5 spots.

### 3. No glass blank in the data I can see

Your notes say you collected blanks at three spots, but they are not in the
folder. Without them I cannot demonstrate that no reported band comes from the
substrate. The manuscript currently makes no claim about this, which is honest
but leaves an obvious reviewer question open.

**If the files exist, send them.** If not, it is ten minutes of instrument time:
clean slide, identical settings, three spots.

### 4. Power and acquisition order are perfectly confounded

Every run ramped 5% → 80% sequentially (SP_86 → SP_101 maps exactly onto
5% → 80%). Power correlates with file order at r = −0.93.

So strictly, "SNR increases with laser power" cannot be separated from "SNR
increases with cumulative exposure." Nothing in the data suggests the sample
changed — see the no-damage result above — but a careful reviewer may notice.

**Suggested fix:** repeat the power series in randomised order, or on a fresh
spot for each condition. Half an hour, and it makes Figure 3 airtight.

### 5. No genuine replicates at a single fixed condition

After removing triplicated files, there is one spectrum per (integration, power)
combination, except at 15 s. The manuscript is written honestly around this, but
a proper replicate set would be better.

**This is what your `nam-new` dataset was meant to be** — 70% / 60 s / 5
accumulations across 10 spots, per your notes. If it exists, send it; that alone
fixes this. Otherwise it is about 30 minutes to collect.

### 6. Spectral resolution is not documented

Not an experiment — just a number from the instrument manual or software. Needed
in Methods, and it also sets a floor on how precisely you can quote band positions.

---

## Computational doubts — no new experiments needed

### 7. The 872 and 956 cm⁻¹ bands are unassigned — **highest-value fix**

These are the second and third strongest bands in the entire spectrum, both
detected in 40/40 spectra, and neither has a calculated counterpart within
±18 cm⁻¹.

In the 840–1010 cm⁻¹ window:

- observed: 872, 930, 956 (plus weak 1008)
- calculated: 899, 910, 929, 980, 995, 1006

Only 930 lines up. A paper claiming vibrational assignment cannot leave its two
strongest bands unexplained.

**Most likely cause:** you optimised a single PubChem conformer. Carbohydrates
have many low-energy conformers differing in hydroxyl orientation and
hydroxymethyl rotation, and ring/exocyclic modes in the 850–1000 cm⁻¹ region are
sensitive to exactly that.

**Suggested fix:** conformer search — generate 5–10 low-energy conformers, optimise
each, Boltzmann-weight the spectra. This is very likely to fill the gaps, and it
is the single biggest improvement available to the paper. Compute time only.

### 8. Hydration state of the sample

The 1994 reference study you cite worked on the **monohydrate**. If your powder is
also hydrated, an anhydrous gas-phase calculation is the wrong model, and it could
contribute to the 850–1000 cm⁻¹ mismatch.

**Just check the bottle.** If it says monohydrate, we should discuss adding an
explicit water molecule to the calculation.

### 9. Anomeric form

The calculation assumed **β**. If the reagent is the α anomer or an anomeric
mixture, ring-mode frequencies shift. Again — check the label.

### 10. Consider adding solvation or dispersion

Your run was gas-phase B3LYP with no dispersion correction. Adding D3BJ, or an
implicit solvation model, typically improves agreement for hydrogen-bonded
molecules. Worth testing once the conformer question is settled — but do the
conformer search first, it will matter more.

---

## If you only do three things

1. **Check the reagent bottle** — anomer and hydrate state. Five minutes, and it
   may change the computational model.
2. **Run the conformer search.** No instrument time, and it is the most likely
   route to explaining 872 and 956 cm⁻¹.
3. **Re-measure 1550–1800 cm⁻¹ properly, and extend to 3600 cm⁻¹.** About two
   hours total, and it converts a third of your peak list from tentative to solid
   while adding a region reviewers will expect.

Everything else is optional polish.

---

*Diagnostic evidence: `DIAGNOSTIC_water_band_loss.png` — this shows what I first
mistook for dehydration. Kept as a record of why it was rejected.*
