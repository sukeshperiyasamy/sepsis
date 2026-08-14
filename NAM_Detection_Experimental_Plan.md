# Experimental Plan — SERS Detection of N-Acetylmuramic Acid

**Project:** SERS nanobiosensor for rapid bacterial identification in sepsis
**Prepared:** August 2026

---

## 1. Objective

To detect N-acetylmuramic acid at clinically relevant concentrations on a
boronic-acid-functionalised Ag/Si SERS substrate, using the reference spectrum
and band assignments already established for the pure powder.

The completed Raman–DFT study gives us something most SERS detection work lacks:
we know exactly which bands belong to NAM, which are strongest, and what
molecular motions produce them. That knowledge determines the experimental
design set out below.

---

## 2. Where we stand

**Completed**

- Reference Raman spectrum of NAM powder from 22 independent measurements
- 41 bands identified, 32 at high confidence
- 30 bands assigned to calculated normal modes (MAE 9.3 cm⁻¹, r = 0.9996)
- Laser-damage threshold established for the powder
- Manuscript written and ready for submission

**Blocking**

- Ag/Si substrate fabrication is not currently reproducible. The July repeat
  produced contaminated substrates and no usable R6G enhancement. Nothing
  downstream can proceed until this is resolved.

**Not yet started**

- Boronic acid surface functionalisation
- NAM detection on substrate
- Concentration series and limit of detection

---

## 3. Detection strategy — which bands to target

Not all NAM bands are equally useful for detection. Selection criteria: high
intensity, high confidence, secure assignment, and freedom from interference.

### 3.1 Primary detection window: 800–1000 cm⁻¹

The four strongest NAM bands fall in this region:

| Band (cm⁻¹) | Rel. intensity | Assignment | Confidence |
|---|---|---|---|
| **930** | 1.00 | Ring breathing (calc. 927) | high |
| **956** | 0.94 | unassigned — see §3.3 | high |
| **871** | 0.94 | Hydroxymethyl wagging (calc. 873) | high |
| **830** | 0.68 | Ring deformation | high |

This window carries the most signal and, critically, is free of interference
from the capture chemistry (§3.2). **It should be the primary detection window.**

### 3.2 Critical finding — the reporter bands overlap NAM features

4-Mercaptophenylboronic acid has SERS bands at **1072 cm⁻¹** (ring breathing)
and **1585 cm⁻¹** (aromatic C=C). Checking these against our measured NAM
spectrum:

| 4-MPBA band | Nearest NAM bands | Separation |
|---|---|---|
| 1585 cm⁻¹ | **NAM 1589 cm⁻¹** | **+4 cm⁻¹ — unresolvable** |
| 1072 cm⁻¹ | NAM 1058 / 1085 cm⁻¹ | −14 / +13 cm⁻¹ — crowded |

At the ~10 cm⁻¹ linewidths we measure, the 1585/1589 pair cannot be separated,
and the 1072 region is congested on both sides.

**Consequences for the experiment:**

1. Do **not** attempt NAM quantification from the 1000–1600 cm⁻¹ region on a
   4-MPBA-functionalised surface. The reporter will dominate and the overlap is
   unresolvable.
2. Use 800–1000 cm⁻¹ for NAM, where the reporter contributes nothing.
3. The overlap is not entirely a liability — the 1072 and 1585 cm⁻¹ reporter
   bands can serve as an **internal intensity reference**, since they are present
   regardless of whether analyte binds. A ratiometric measurement such as
   I(930)/I(1072) is far more robust than absolute intensity, which varies with
   hotspot density between substrates and between spots.

This is the kind of problem that is cheap to design around now and expensive to
discover after three months of measurements.

### 3.3 The 956 cm⁻¹ band

This is the second-strongest band in the spectrum, detected in every one of the
22 reference measurements, and it has **no calculated counterpart**. It is
attributed provisionally to the anomeric mixture in the sample or to crystal
packing.

For detection purposes this does not matter — an unassigned band is still a
reliable marker if it is reproducible, and this one is. But it should be watched:
if it behaves differently from the assigned bands on the substrate, that would be
informative about adsorption geometry.

### 3.4 What we expect SERS to change

SERS is not simply amplified Raman. Surface selection rules mean modes with
polarisability change perpendicular to the metal surface are enhanced most, so
**relative intensities will differ from the powder spectrum** even though band
positions are largely preserved.

This is scientifically useful rather than a nuisance. Comparing enhanced with
non-enhanced spectra is how adsorption geometry is inferred — and our
non-enhanced reference spectrum is exactly the baseline that comparison requires.
Most SERS studies cannot do this because they lack a properly characterised
reference.

---

## 4. Staged experimental plan

Each stage has a go/no-go criterion. Do not proceed past a failed stage.

### Stage 1 — Restore substrate reproducibility

*Prerequisite for everything else.*

| | |
|---|---|
| Approach | Fresh HF/AgNO₃ per batch; documented cleaning protocol; blank spectrum recorded after each fabrication step |
| Key change | Record a bare-substrate spectrum **before** any probe molecule, to identify where contamination enters |
| Test molecule | Rhodamine 6G, single concentration only |
| **Go criterion** | R6G enhancement reproducible across ≥3 substrates and ≥5 spots each, with the June band positions recovered |

Reducing to a single R6G concentration is deliberate. The July trials varied
concentration and fabrication simultaneously, so a failure could not be traced.
Fix one variable at a time.

### Stage 2 — Boronic acid monolayer

| | |
|---|---|
| Approach | 4-MPBA self-assembly on the Ag surface via the thiol group |
| Verification | Confirm the 1072 and 1585 cm⁻¹ reporter bands |
| **Go criterion** | Reporter bands present, stable over ≥1 h, and reproducible across substrates (CV < 15%) |

This stage doubles as a substrate quality-control metric. A well-formed monolayer
gives a consistent reporter signal; an inconsistent one indicates the underlying
substrate is still variable. **This is a better QC test than R6G** because it
probes the actual working surface.

### Stage 3 — Confirm diol binding

| | |
|---|---|
| Approach | Expose the functionalised surface to a simple sugar (fructose binds most strongly among common sugars) |
| Readout | Change in the 1072 and 1585 cm⁻¹ reporter bands on boronate ester formation |
| **Go criterion** | Reproducible, reversible spectral change on binding and on acid washing |

This proves the capture chemistry works before introducing the complexity of NAM
or bacteria.

### Stage 4 — NAM detection in buffer

| | |
|---|---|
| Concentrations | Decade series, 1 mg/mL down to 1 µg/mL initially |
| Detection window | **800–1000 cm⁻¹** |
| Target bands | 930, 956, 871, 830 cm⁻¹ |
| Reference bands | 1072 or 1585 cm⁻¹ (4-MPBA) |
| Metric | I(930)/I(1072) versus concentration |
| Replication | ≥5 spots per concentration, fresh substrate per concentration |
| **Go criterion** | Monotonic dose–response over ≥2 decades; band positions matching the reference spectrum within ±10 cm⁻¹ |

Also record the full 400–1800 cm⁻¹ range even though only part is used for
quantification — the relative intensity changes across the whole spectrum carry
the adsorption-geometry information described in §3.4.

### Stage 5 — Limit of detection

Extend the concentration series downward until the 930 cm⁻¹ band falls below
three times the local noise, using the same two-criterion validation developed
for the powder work.

**Go criterion:** LOD established with stated confidence, ideally below 1 µg/mL.

### Stage 6 — Selectivity

| Test | Purpose |
|---|---|
| N-acetylglucosamine | The closest structural analogue; discrimination here is the real test |
| Glucose | The principal interferent in blood, at 5 mM |
| NAM + glucose mixture | Quantify competitive displacement |

**Go criterion:** NAM detectable in the presence of physiological glucose, or a
documented sample-preparation requirement to remove it.

The GlcNAc comparison is where the DFT work pays off directly. The lactyl group
is what chemically distinguishes NAM, and bands carrying lactyl character —
1337–1385 cm⁻¹ and the carboxyl stretch above 1750 cm⁻¹ — are in principle the
discriminating features. Note, however, that these fall in the region congested
by the reporter, so this measurement may need a different reporter or a
label-free surface.

### Stage 7 — Complex matrix

Serum, then whole blood, then spiked bacterial samples. Not yet planned in
detail; scope depends on the outcome of Stage 6.

---

## 5. Parallel computational work

These require no instrument time and can proceed while substrate work continues.

**α anomer calculation.** The sample is an anomeric mixture but only the β anomer
was computed. This would test whether the unassigned 830 and 956 cm⁻¹ bands have
an anomeric origin, closing the last gap in the assignment.

**N-acetylglucosamine at matched level of theory.** A GlcNAc calculation exists
in the project files but at unknown settings. Recomputing at
B3LYP-D3BJ/6-311++G(d,p) would identify which bands discriminate the two
peptidoglycan sugars — directly supporting Stage 6, and a strong addition to the
manuscript in its own right.

**Boronate ester model.** Computing NAM or a model diol bound to phenylboronic
acid would predict which bands shift on binding, giving an expected signature to
look for rather than an empirical search.

---

## 6. Principal risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Substrate reproducibility not restored | Medium | Systematic contamination isolation; consider commercial SERS substrate as a control to separate substrate problems from chemistry problems |
| Boronic acid binds NAM weakly | **Medium–high** | NAM's C-2 acetamido and C-3 lactyl block the usual 1,2-diol site — see §7 |
| Reporter bands swamp analyte bands | Medium | Use the 800–1000 cm⁻¹ window; ratiometric readout |
| Glucose outcompetes NAM | High in blood | Sample preparation; lower-pKa ligand; multivalent avidity |
| Laser damage on plasmonic substrate | Medium | Field concentration lowers the damage threshold below the powder values; re-establish limits on the actual substrate |

---

## 7. An honest concern that should be tested early

Boronate ester formation requires a suitable cis-diol. In NAM, **C-2 carries the
acetamido group and C-3 the lactyl ether**, so the 1,2-diol site normally used
for boronic acid binding is not available. Free NAM may therefore bind boronic
acid only weakly, through the C-4 and C-6 hydroxyls, which are not adjacent.

This does not undermine the sensor concept — on **intact bacteria**, capture is
thought to occur mainly through LPS and teichoic acids, which are diol-rich, not
through the peptidoglycan backbone. But it does mean that **free NAM in solution
may be a poor test analyte for boronic acid capture**, even though it is the
biomarker of interest.

**Recommended test, early and cheap:** before committing to the full
concentration series, run a simple binding check — expose the functionalised
surface to NAM solution and to fructose solution at comparable concentration and
compare the reporter-band response. If NAM gives little or no response while
fructose does, the capture chemistry is working but NAM is not a suitable target
for it, and the strategy needs rethinking at that point rather than after Stage 5.

Possible responses if that turns out to be the case:

- detect NAM by direct SERS adsorption without boronic acid capture
- target intact bacteria or cell-wall fragments rather than free NAM
- use boronic acid for bacterial capture and the Raman fingerprint for
  identification, treating NAM as a spectral marker rather than a binding target

The third option is the architecture already proposed, and it does not require
NAM to bind boronic acid at all. Worth stating clearly so the strategy is not
mistakenly judged on the wrong criterion.

---

## 8. Indicative timeline

| Period | Work |
|---|---|
| Weeks 1–3 | Stage 1 — substrate reproducibility |
| Weeks 3–4 | Stage 2 — monolayer; Stage 3 — diol binding check |
| Week 4 | **Early NAM binding test (§7)** — decision point |
| Weeks 5–7 | Stage 4 — concentration series |
| Weeks 7–8 | Stage 5 — limit of detection |
| Weeks 9–11 | Stage 6 — selectivity |
| Throughout | Parallel computational work; NAM manuscript submission |

---

## 9. Summary

The detection strategy rests on three decisions, each grounded in work already
completed:

1. **Monitor 800–1000 cm⁻¹**, where NAM's four strongest bands lie and the
   capture reporter does not interfere.
2. **Measure ratiometrically** against the 4-MPBA reporter bands, removing
   dependence on absolute intensity.
3. **Test NAM binding to boronic acid early**, because the molecule's substitution
   pattern gives real reason to doubt it, and finding out at week 4 costs far
   less than finding out at week 12.

The immediate blocker remains substrate reproducibility. Until that is fixed,
the computational work in §5 is the most productive use of time.
