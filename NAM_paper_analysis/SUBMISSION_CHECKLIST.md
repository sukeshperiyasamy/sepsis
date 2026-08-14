# Submission Readiness — Honest Assessment

**Status: NOT ready to submit. Roughly 85% complete.**

Everything that can be produced from your existing data is done. What remains
needs information only you have, plus two verification steps.

---

## Fixed since the last version

- Figure 1 (optimised molecular structure) generated from your Gaussian geometry — was missing entirely
- Kouach 1994 was cited in prose with no reference — now has a bibliography entry
- 8 of 12 references were uncited in the text — all 13 now cited at appropriate places
- Supplementary Material created (computational details, 39-atom coordinate table, all 111 modes)
- Both main text and SI compile with **0 LaTeX errors, 0 undefined references**

---

## BLOCKING — cannot submit without these

### 1. Reagent provenance
Supplier, catalogue number, lot number, stated purity, stated anomeric form.
Without this the work is not reproducible and desk rejection is likely.

### 2. Laser power in mW at the sample
The manuscript currently reports "power level 5–80%", which is meaningless on any
other instrument. If you cannot measure it, state the instrument's rated maximum
output and say that percentages refer to it.

Also still needed for the Methods:
- objective magnification and numerical aperture
- grating (grooves/mm)
- spectral resolution in cm⁻¹

### 3. Gaussian 09 revision letter
Check the first ~20 lines of your `.LOG` file. Cite as "Revision X.01" or similar.

### 4. Co-authors
Your supervisor at minimum. Add to the author list, affiliations, and the CRediT
statement. Submitting single-author work done on institutional instruments without
your supervisor is a problem you do not want.

### 5. Funding and acknowledgements
Grant numbers if any.

### 6. References: 13 → 30–45
Thirteen is thin for a full paper. Priority additions:

- **Kouach et al. 1994** — verify the actual authors, volume and page numbers.
  I have placed a plausible entry but **the details are unverified** and must be
  corrected against the real paper.
- Frosch et al. — source of the 0.980/0.967 scaling scheme you are using
- 4–6 recent bacterial SERS detection papers
- 3–4 combined experimental+DFT vibrational papers as methodological precedent
- 2–3 further peptidoglycan structure/biology references
- Additional amino-sugar Raman literature

---

## MUST VERIFY — a scientific claim depends on it

### 7. The 727 cm⁻¹ mode
Open the `.LOG` in GaussView, animate mode 40, and confirm it is the carboxylic
acid O–H out-of-plane wag. My decomposition says 48.3% of the displacement is
that hydrogen and 1.8% is ring — but this is a numerical analysis of displacement
vectors, not a PED calculation, and your Discussion makes a substantive claim
about the bacterial 730 cm⁻¹ band on the basis of it.

If the animation disagrees, Section 3.7 must be rewritten.

### 8. Spot-check the strongest assignments
Same procedure for modes at 823, 910, 1093, 1337, 1469 and 1688 cm⁻¹.
The Methods are explicit that assignments came from displacement-vector analysis
rather than PED, which is defensible — but you should still have looked.

---

## RECOMMENDED — would materially strengthen the paper

### 9. Glass blank comparison
Your notes say you collected glass blanks at three spots. That data is not in the
folder I can see. Adding a substrate-comparison figure would pre-empt an obvious
reviewer question. Currently the manuscript makes no claim about glass subtraction,
which is honest but leaves a gap.

### 10. The `nam-new` dataset
Your notes describe final measurements at 70% / 60 s / 5 accumulations across
10 spots. That is a genuine replicate set at fixed conditions, which is what
Section 3.2 really wants. What I worked from is the optimisation grid — after
deduplication there is one spectrum per condition except at 15 s.

The manuscript is written honestly around this (40 spectra "spanning acquisition
conditions", not "independent replicates"), but a reviewer may still ask.

### 11. PED analysis via VEDA
Would convert the assignments from qualitative to quantitative percentage
contributions. This is what strong vibrational papers do. Not blocking, but it is
the single biggest quality upgrade available.

### 12. N-acetylglucosamine comparison
You already have a GlcNAc Gaussian run in `review meeting/N-ACETYL-D-GLUCOSAMINE-OPT_raman_act/`.
Adding a NAM-vs-NAG comparison would show which bands actually discriminate the two
peptidoglycan sugars — directly useful to anyone doing bacterial Raman, and a
strong addition to Section 3.6.

---

## Realistic timeline

| | |
|---|---|
| Items 1–5 (your information) | 1–2 days |
| Item 6 (references) | 3–5 days |
| Items 7–8 (GaussView verification) | half a day |
| Items 9–10 (if data exists) | 1 day to reprocess |
| Supervisor review | 1–2 weeks |
| **Submission-ready** | **2–4 weeks** |

Add 2–3 weeks if you do the PED analysis or the NAG comparison.

---

## Where to send it

**Spectrochimica Acta Part A** (IF ~4.3) — first choice.

**Vibrational Spectroscopy** — fallback. Ma et al. (2024) published there;
position the cover letter as the direct experimental validation of their work.

Not the J. Photochem. Photobiol. B SERS special issue — this is a vibrational
spectroscopy paper. Send the SERS substrate work there instead.
