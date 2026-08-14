# Which Powers Are Actually in Doubt

Short answer: **none of them are wrong. The problem is that none of them were
repeated.**

---

## What is NOT in doubt — do not redo this

I checked for laser damage properly across your whole range at 25 s:

| Power | 930 cm⁻¹ position | 1451 cm⁻¹ position | FWHM(930) |
|---|---|---|---|
| 5% | 930.0 | 1450.0 | 9 |
| 20% | 930.0 | 1452.0 | 11 |
| 40% | 930.0 | 1452.0 | 10 |
| 60% | 930.0 | 1451.0 | 10 |
| 80% | 930.0 | 1451.0 | 10 |

Band positions stable within ±1 cm⁻¹, linewidths constant, no carbonaceous
background, no band loss. **Every power from 5% to 80% gives valid data.**
There is nothing to re-verify about sample damage.

---

## What IS the problem

Here is how your 40 reference spectra are distributed:

| Power | 10 s | 15 s | 20 s | 25 s | total |
|---|---|---|---|---|---|
| 55% | — | 2 | 1 | 1 | 4 |
| 60% | — | 2 | 1 | 1 | 4 |
| 65% | 1 | 2 | 1 | 1 | 5 |
| 70% | 1 | 2 | 1 | 1 | 5 |
| 75% | 1 | 2 | 1 | 1 | 5 |
| 80% | 1 | 1 | 1 | 1 | 4 |

Read across any row: those are **different integration times**, not repeats.

**There is not one single condition in your entire dataset that was measured
twice on fresh powder.**

So when the paper says "mean of 40 spectra", those 40 are 40 *different
acquisition conditions*. That is defensible — I have written it honestly — but a
reviewer will ask why there are no replicates, and the answer will be that there
aren't any.

---

## What to measure

### Priority 1 — one power, repeated. This is the whole point.

| | |
|---|---|
| Power | **70%** |
| Integration | **25 s** |
| Accumulations | **5** |
| Spots | **10, fresh powder each time** |

Why 70% and not 80%: 70% sits comfortably inside the range you have already
shown to be safe, rather than at the edge of it. Its SNR is essentially the same
(268 vs 227 at 80%), so you lose nothing and the "well inside the safe range"
argument is cleaner to write.

**Files:** `NAM_final_spot01.csv` … `spot10.csv`

This single run converts "40 different conditions" into "10 independent
measurements at one defined condition", which is what a reference spectrum
should be.

### Priority 2 — break the power/order confounding

Eight powers, **scrambled order**, fresh spot each, 25 s / 5 accumulations:

**50%, 10%, 80%, 30%, 70%, 20%, 60%, 40%**

In every existing series the power ramped 5% → 80% in file order, so power and
cumulative exposure are perfectly confounded (r = −0.93). I cannot separate them
in the current data. Randomising the order fixes this permanently.

**Files:** `NAM_rand_p50.csv`, `NAM_rand_p10.csv`, …

### Priority 3 — glass blank

70%, 25 s, 5 accumulations, 3 spots on an empty clean slide. Same settings as
Priority 1, which is the point.

**Files:** `GLASS_spot1.csv`, `spot2`, `spot3`

---

## If you want the weak region fixed too

Twelve of your 41 bands are flagged tentative, and eleven of those sit between
1550 and 1800 cm⁻¹ — amide I, amide II, carboxyl C=O. Same power, double the
accumulations:

| | |
|---|---|
| Power | 70% |
| Integration | 25 s |
| Accumulations | **10** |
| Spots | 5 |

**Files:** `NAM_longacq_spot1.csv` … `spot5.csv`

---

## Total

| Priority | Spectra | Time |
|---|---|---|
| 1 — replicates at 70% | 10 | 25 min |
| 2 — randomised power | 8 | 30 min |
| 3 — glass blank | 3 | 10 min |
| optional — long acquisition | 5 | 30 min |

**21 spectra, about an hour** for priorities 1–3. Add half an hour for the
optional run.

---

## One number to write down

Power at the sample in **mW**, measured with a meter at the objective focal
plane, at least at 70%. Everything in the paper currently says "70% of nominal
495 mW output", which means nothing on another instrument.

If you measure 5 / 40 / 70 / 80% I can also plot the transmission curve, but a
single reading at 70% is the minimum.

---

## Summary

Nothing you measured is wrong. What is missing is repetition at a single
condition, and a power series that isn't confounded with acquisition order. One
hour at the instrument closes both.
