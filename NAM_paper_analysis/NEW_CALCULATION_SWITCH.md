# Switched to the New Gaussian 16 Calculation

**Use `N-ACETYL-BETA-MURAMIC ACID.LOG`. Discard the old one. No new simulation
needed for NAM.**

---

## Why this one

| | Old (used until now) | New (now used) |
|---|---|---|
| File | `CONFORMER3D_COMPOUND_CID_5462244.LOG` | `N-ACETYL-BETA-MURAMIC ACID.LOG` |
| Program | Gaussian 09 | **Gaussian 16** |
| Basis set | 6-311+G(d,p) | **6-311++G(d,p)** (diffuse on H too) |
| Dispersion | none | **D3BJ** |
| Optimisation | default | **`opt=(calcfc,tight)`** |
| Integration grid | default | **ultrafine** |
| SCF | default | **`tight,xqc`** |
| Termination | normal | normal (×2) |
| Imaginary frequencies | 0 | 0 |
| Stationary point | — | **explicitly confirmed** |

The new run is the setup your notes originally planned. It is the one to publish.

Both give 39 atoms and 111 modes, so the molecule and the analysis pipeline are
unchanged — only the quality of the electronic structure differs.

---

## What changed in the results

**Agreement improved slightly:**

| | old | new |
|---|---|---|
| MAE | 9.4 cm⁻¹ | **9.1 cm⁻¹** |
| RMSE | 10.7 cm⁻¹ | **10.2 cm⁻¹** |
| r | 0.99965 | **0.99967** |
| matched | 33 / 41 | 33 / 41 |

Modest, as expected — a better basis set and dispersion correction refine
frequencies but cannot fix the fundamental gas-phase-versus-crystal limitation.

### The 872 cm⁻¹ mystery is solved — and not the way I guessed

The new calculation places a mode at **873.0 cm⁻¹**, matching the observed
872 cm⁻¹ band to within 1 cm⁻¹. The old calculation had nothing there.

Decomposing it: a single hydrogen on the C-6 carbon carries **45.9%** of the
displacement, a second **17.4%**, the pyranose ring only **5.0%**, heavy atoms
**8.9%**. It is **out-of-plane wagging of the hydroxymethyl group**, not a ring
mode and not an anomeric effect.

So my earlier α-anomer explanation for 872 was wrong, and I have removed it. The
band is now a clean, confident assignment — one you could not have reached from
the experimental spectrum alone, which is exactly the kind of result that
justifies a combined experimental/DFT paper.

### Your 730 cm⁻¹ claim survives, and got stronger

The mode moved from 727 to **731.3 cm⁻¹** — closer to the disputed band — with
identical Raman activity (5.29 Å⁴/amu).

| | old | new |
|---|---|---|
| carboxylic acid O–H contribution | 48.3% | **47.9%** |
| pyranose ring contribution | 1.8% | **0.5%** |
| heavy atoms | 24.8% | **24.0%** |

Ring character is now essentially zero. The argument — that this mode cannot
contribute to the bacterial 730 cm⁻¹ band because the proton responsible is
absent in intact peptidoglycan — holds, with better numbers behind it.

### Which bands are now unmatched

Changed from `704, 872, 956, 1590, 1633, 1652, 1726, 1792`
to **`772, 831, 956, 1590, 1633, 1652, 1700, 1792`**.

Two are worth noting:

**831 cm⁻¹** was matched before (to a calculated 823) and now falls between
calculated modes at 793 and 873. Along with 956, it is now discussed as
plausibly anomeric or packing-related.

**1700 cm⁻¹ (amide I)** dropped out. The new calculation puts the amide carbonyl
at 1723 cm⁻¹, 23 cm⁻¹ above the observed band and outside the ±18 window. This
is the right direction and magnitude for a gas-phase model — hydrogen bonding to
the amide carbonyl in the crystal lowers the stretch substantially, and no
isolated-molecule calculation reproduces that. It now reads as a physical
result rather than an unexplained gap.

---

## What was updated

- Methods: full new route section, Gaussian 16, D3BJ, ultrafine, tight SCF
- All statistics in abstract, results and conclusions
- Table 3 regenerated against the new modes
- Figures 1, 4, 5 and 6 regenerated
- Section 3.7 rewritten — 872 is now assigned, and the anomeric discussion is
  reframed around 831 and 956
- Amide I discussion added
- References: Gaussian 16 replaces Gaussian 09, Grimme D3BJ added
- Supplementary Material: new coordinates, all 111 new modes, corrected route
- LaTeX and Word rebuilt, 14 pages, zero errors

---

## Do you need another simulation?

**Not for NAM.** This calculation is publication grade.

Two optional additions, both compute-only:

**α anomer** — would test whether 831 and 956 cm⁻¹ have an anomeric origin.
Same level of theory, then compare a weighted combination of the two spectra.
This is the last real gap in the assignment.

**N-acetylglucosamine** — you already have a GlcNAc calculation in
`review meeting/N-ACETYL-D-GLUCOSAMINE-OPT_raman_act.xlsx`, though at an unknown
level of theory. Re-running it at the same B3LYP-D3BJ/6-311++G(d,p) level would
let you show which bands distinguish the two peptidoglycan sugars — directly
useful to anyone doing bacterial Raman, and a strong addition rather than a
gap-filler.

Neither is required to submit.
