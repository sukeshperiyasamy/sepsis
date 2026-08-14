# What the Sigma-Aldrich Datasheet Changed

Product: **Sigma-Aldrich A3007**, CAS 10597-89-4, synthetic, ≥98% (TLC), MW 293.27

Three things in that specification materially affect the paper. One of them
probably solves the biggest open problem in the analysis.

---

## 1. Your sample is not pure β — it is an anomeric mixture

The supplier SMILES is:

```
CC(O[C@H]1[C@H](O)[C@@H](CO)OC(O)[C@@H]1NC(C)=O)C(O)=O
                                  ^^^^
```

Reading the ring in order — C3`[C@H]` – C4`[C@H]` – C5`[C@@H]` – O5 – **C1 `C(O)`** – C2`[C@@H]` —
the anomeric carbon C1 carries **no stereo descriptor**. The InChI confirms it:
the stereo layer `/t5-,7+,8-,9-,10-/m1/s1` defines five centres, and the
anomeric carbon is not among them.

So the material is an α/β mixture, which is normal for a reducing sugar. Your
DFT modelled the β anomer alone (PubChem CID 5462244).

**Changes made:** the title, abstract and all experimental text now say
"N-acetylmuramic acid" rather than "β-N-acetylmuramic acid". The three remaining
β references are the DFT model, which is correct. The Materials section states
the anomeric ambiguity explicitly and cites the SMILES and InChI.

### This probably explains the 872 cm⁻¹ band

In the 820–980 cm⁻¹ window:

| | |
|---|---|
| observed | 831, **872**, 930, 956 |
| calculated (β only) | 823, **899**, 910, 929 |

831/823 and 930/929 pair up. But 872 has no calculated partner, and the
calculated 899 has no observed partner.

That window is exactly where α and β pyranose anomers differ — through the
anomeric C–H bending and associated ring modes. A band from the α component
would appear in your measurement with nothing to match it in a β-only
calculation. Which is what you see.

**New Section 3.7** sets this out and assigns 872 cm⁻¹ tentatively to the
α anomer.

**To confirm it:** optimise the α anomer at the same level and compare a
weighted combination of both spectra to experiment. No instrument time. If 872
is reproduced it becomes a definite assignment, and the paper is considerably
stronger for having explained its own anomaly.

---

## 2. The material is anhydrous

MW 293.27 corresponds exactly to C₁₁H₁₉NO₈ with no water. That retrospectively
confirms rejecting the dehydration hypothesis I had briefly entertained.

It also matters for the comparison with the 1994 study, which examined the
crystalline **monohydrate**. Different solid form, so band-by-band comparison
needs care — hydration and packing both shift the hydroxyl, carbonyl and
ring-deformation regions. This caveat is now in the Discussion.

---

## 3. Up to 1 mol/mol residual methanol

The specification permits one mole of methanol per mole of product — roughly
10% by mass, which is not trivial.

Methanol's strong Raman band is at 1035 cm⁻¹, with C–H stretches at 2835 and
2945 cm⁻¹. Your spectrum has intensity around 1030–1045, but that region also
contains genuine NAM ring modes, so it is not diagnostic on its own.

**The C–H stretch region would settle it — and your data stops at 2842 cm⁻¹.**
This is now a second, independent reason to extend the measured range above
3000 cm⁻¹, alongside the O–H stretch argument.

Note also that ≥98% is a **TLC** assay. TLC cannot distinguish anomers and is
insensitive to residual solvent, so it does not constrain either issue.

---

## Also updated in this pass

**Table 3 has been corrected.** The peaks at 411 and 901 cm⁻¹ were noise and
have been removed, along with 428, 1495 and 1677. Twelve further bands are now
flagged as tentative with a dagger.

**Statistics revised** accordingly:

| | before | now |
|---|---|---|
| bands reported | 41 | 41 (29 high + 12 tentative) |
| matched | 34 | 33 |
| MAE | 9.8 cm⁻¹ | **9.4 cm⁻¹** |
| RMSE | 11.0 cm⁻¹ | **10.7 cm⁻¹** |
| r | 0.9996 | **0.9997** |

High-confidence bands alone: MAE 9.2, RMSE 10.6, r = 0.99967.

**Methods rewritten** to describe the two-criterion peak validation honestly,
including the point that reproducible processing artefacts can masquerade as
reproducible bands.

**Instrument details** added: i-Raman Plus BWS465-785H, BAC102-785E microscope,
785 nm / 495 mW nominal / Class 3B, 20× Plan objective, spectral sampling
derived from your files (1.76 cm⁻¹/pixel at 400, 1.43 at 1800).

Both LaTeX and Word rebuilt, 14 pages, zero errors.

---

## Still outstanding

**From the bottle:** lot number.

**From the instrument:** measured power at sample (protocol already sent),
spectral resolution in cm⁻¹.

**Computational:** the α-anomer calculation — highest value item, no instrument
time.

**Measurement:** extend range above 3000 cm⁻¹ (now justified twice over —
methanol and hydroxyl), and improve SNR in 1550–1800 cm⁻¹.

**Editorial:** co-authors, funding, references 13 → 30–45, and verify the
Kouach 1994 citation details.
