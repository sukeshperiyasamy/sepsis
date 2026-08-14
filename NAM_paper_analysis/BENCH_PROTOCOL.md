# Bench Protocol — NAM Raman Re-measurement

**Instrument:** i-Raman Plus BWS465-785H + BAC102-785E, 785 nm, 20× Plan
**Sample:** Sigma A3007 NAM powder on clean glass slide
**Total time:** about 2.5 hours
**Runs:** six, in this order

Your final condition throughout is **25 s, 70% power, 5 accumulations** — this
came out best in your existing data (SNR 268 at 25 s / 70%, and no sign of
damage anywhere between 5% and 80%).

---

## Before you start

- [ ] Clean glass slide, lens tissue + IPA, let dry fully
- [ ] Write down the **lot number** from the NAM bottle
- [ ] Note whether the label says **α, β, or nothing** about the anomer
- [ ] Check in the software: is there a **spectral range setting**? Your data
      stops at 2842 cm⁻¹ — find out whether that's a hardware limit or a setting
- [ ] Note the **spectral resolution** from the spec sheet or instrument info panel

---

## RUN 1 — Power at the sample  ·  15 min

Power meter head at the objective focal plane, 785 nm setting, 20× in place.

| Setting | Nominal | Measured (mW) |
|---|---|---|
| 5% | 25 mW | ________ |
| 40% | 198 mW | ________ |
| 70% | 347 mW | ________ |
| 80% | 396 mW | ________ |

Four points is enough. **This is the single most-requested number reviewers ask
for and you currently cannot answer it.**

If the software already displays mW, just record what it says at each setting
and note that it is software-reported rather than meter-measured.

---

## RUN 2 — Glass blank  ·  10 min

Empty clean slide, no powder.

| Setting | Value |
|---|---|
| Power | 70% |
| Integration | 25 s |
| Accumulations | 5 |
| Spots | **3**, well separated |

**Files:** `GLASS_spot1.csv`, `GLASS_spot2.csv`, `GLASS_spot3.csv`

Identical settings to Run 3 — that is the whole point. This proves no reported
band comes from the substrate.

---

## RUN 3 — Main replicate set  ·  25 min  ·  **most important run**

Fresh NAM powder on the slide. This becomes the reference spectrum in the paper.

| Setting | Value |
|---|---|
| Power | 70% |
| Integration | 25 s |
| Accumulations | 5 |
| Spots | **10**, move the stage between each |

**Files:** `NAM_final_spot01.csv` … `NAM_final_spot10.csv`

Move to genuinely fresh powder for each spot — do not re-measure the same grain.
Ten independent spots at one fixed condition is what the paper is missing; right
now you have one spectrum per condition and no true replicates.

---

## RUN 4 — Extended range  ·  20 min

**Only if Run 0 showed the range is adjustable.** Target 3600 cm⁻¹.

| Setting | Value |
|---|---|
| Power | 70% |
| Integration | 25 s |
| Accumulations | 5 |
| Range | up to 3600 cm⁻¹ if possible |
| Spots | **5** |

**Files:** `NAM_extended_spot1.csv` … `spot5.csv`

This gives the C–H (2800–3000) and O–H (3000–3600) stretch regions, which the
paper currently lacks. It also settles whether the residual methanol the supplier
declares (up to 1 mol/mol) is actually present — methanol's diagnostic C–H
stretches sit at 2835 and 2945 cm⁻¹.

If 2842 cm⁻¹ turns out to be a hardware limit, skip this run and tell me — I'll
write it up as a stated limitation instead.

---

## RUN 5 — Long acquisition for the weak region  ·  30 min

Same sample, but doubled accumulations to beat down noise above 1500 cm⁻¹.

| Setting | Value |
|---|---|
| Power | 70% |
| Integration | 25 s |
| Accumulations | **10** |
| Spots | **5** |

**Files:** `NAM_longacq_spot1.csv` … `spot5.csv`

Twelve of your 41 bands are currently flagged tentative, and eleven of those sit
between 1550 and 1800 cm⁻¹ — the amide I, amide II and carboxyl C=O region. That
is the chemically most interesting part of the spectrum and the weakest part of
your data. Doubling accumulations should move most of those to confident.

---

## RUN 6 — Randomised power series  ·  30 min

Fresh powder. **Run the powers in the scrambled order below, not ascending.**

| Order | Power | Spot |
|---|---|---|
| 1 | 50% | fresh |
| 2 | 10% | fresh |
| 3 | 80% | fresh |
| 4 | 30% | fresh |
| 5 | 70% | fresh |
| 6 | 20% | fresh |
| 7 | 60% | fresh |
| 8 | 40% | fresh |

Fixed: **25 s, 5 accumulations**, new spot every time.

**Files:** `NAM_rand_p50.csv`, `NAM_rand_p10.csv`, `NAM_rand_p80.csv`, …

In your existing data every series ramped 5% → 80% in file order, so power and
cumulative exposure are perfectly confounded (r = −0.93). Scrambling the order
and using a fresh spot each time breaks that, and makes the optimisation figure
unarguable.

---

## Summary

| Run | What | Power | Time | Acc. | Spots | Files |
|---|---|---|---|---|---|---|
| 1 | Power meter | 5/40/70/80% | — | — | — | write down mW |
| 2 | Glass blank | 70% | 25 s | 5 | 3 | 3 |
| 3 | **Main replicates** | 70% | 25 s | 5 | **10** | 10 |
| 4 | Extended range | 70% | 25 s | 5 | 5 | 5 |
| 5 | Long acquisition | 70% | 25 s | **10** | 5 | 5 |
| 6 | Randomised power | 8 levels | 25 s | 5 | 8 | 8 |

**31 spectra, about 2.5 hours.**

---

## If you only have one hour

Do **Run 1, Run 2 and Run 3**. Those three fix the gaps that matter most: the
missing power value, the missing substrate control, and the missing replicates.
Runs 4–6 are improvements; 1–3 are things a reviewer will ask about.

---

## Afterwards

Put everything in one folder called `NAM_new_measurements` inside your `mtp`
folder, keeping the filenames above. Then tell me and I will:

- reprocess the reference spectrum from the 10 true replicates
- add the glass-blank comparison as a new figure
- re-run peak validation — most tentative bands should become confident
- add the C–H / O–H region if Run 4 worked
- rebuild the optimisation figure from the randomised series
- insert your measured mW into the Methods
- regenerate Table 3 and all statistics

Keep the raw files exactly as the instrument writes them. Don't pre-process
anything — the pipeline in the paper needs to start from raw.
