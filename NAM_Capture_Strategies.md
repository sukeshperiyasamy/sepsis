# Capture and Enhancement Strategies for NAM Detection

**Alternatives to boronic acid, and substrate options**

**Project:** SERS nanobiosensor for rapid bacterial identification in sepsis
**Prepared:** August 2026

---

## 1. The problem, stated plainly

Two separate things must work:

**A. Capture** — bring NAM within a few nanometres of the metal, since SERS
enhancement falls off steeply with distance.

**B. Enhancement** — a substrate that produces enough signal from what is
captured.

They are often conflated. They fail for different reasons and should be
optimised separately.

### The central difficulty

**NAM is a weak Raman scatterer.** It is a small, colourless, non-aromatic
sugar with no conjugation and no electronic transition near 785 nm. Rhodamine 6G
works beautifully as a test molecule precisely because it is the opposite — a
large aromatic dye with delocalised π electrons and, at some wavelengths,
resonance enhancement.

**A substrate that gives excellent R6G spectra may give very poor NAM spectra.**
This should be stated up front rather than discovered later. R6G is a test of the
substrate, not a prediction of NAM performance.

---

## 2. NAM's chemical handles

What the molecule actually offers for capture:

| Feature | Position | Reactivity | Notes |
|---|---|---|---|
| **Free anomeric OH** | C-1 | Hemiacetal ⇌ open-chain **aldehyde** | NAM is a **reducing sugar** |
| **Carboxylic acid** | lactyl, C-3 | Deprotonated at pH 7 → **anionic** | pKa ≈ 3–4 |
| Acetamido | C-2 | H-bond donor/acceptor | blocks the 1,2-diol |
| Lactyl ether | C-3 | inert | blocks the 2,3-diol |
| Hydroxyls | C-4, C-6 | H-bonding, weak diol | not adjacent |

**Two of these are strong, underexploited handles.** The reducing end and the
carboxylate are both far more accessible than the cis-diol that boronic acid
requires — and as noted previously, NAM's cis-diol site is substituted away.

---

## 3. Capture strategies, ranked

### 3.1 Direct adsorption — no capture chemistry at all

**Try this first.** Bare silver has genuine affinity for carboxylates and for
oxygen and nitrogen lone pairs. NAM's carboxylate should adsorb directly.

| | |
|---|---|
| Method | Drop-cast NAM solution onto the substrate, dry, measure |
| Effort | Trivial — one afternoon |
| Cost | Nothing |
| Likelihood | Moderate |

This establishes whether the substrate can see NAM **at all** before any
functionalisation chemistry is introduced. If direct adsorption gives a usable
spectrum, much of the complexity below becomes unnecessary. If it does not, that
is important information about the enhancement rather than the capture.

There is also a practical trick: as a droplet dries it concentrates the analyte
at the contact line — the coffee-ring effect. Measuring the ring rather than the
centre can give an order of magnitude for free.

### 3.2 Hydrazide chemistry — the best chemical match to NAM

**This is the strategy I would prioritise after direct adsorption.**

NAM is a reducing sugar: its anomeric hemiacetal is in equilibrium with an
open-chain aldehyde. Hydrazide groups react selectively with aldehydes to form
hydrazones, and this is standard, well-established glycan-capture chemistry
[1, 2, 3].

| | |
|---|---|
| Reagent | A thiol-terminated hydrazide, or hydrazide-functionalised silane on the Si |
| Bond formed | Hydrazone, at the C-1 aldehyde |
| Reversible | Yes — released by acid, so the surface regenerates [1] |
| Selectivity | **High.** Aldehydes and ketones are rare in biological samples except at reducing sugar termini [2] |

**Why this beats boronic acid for NAM specifically:**

| | Boronic acid | Hydrazide |
|---|---|---|
| Target group | cis-diol | reducing end (aldehyde) |
| Present in NAM? | **No** — C-2 acetamido, C-3 lactyl block it | **Yes** — free anomeric OH |
| Glucose competes? | **Yes, severely** at 5 mM | Yes, but glucose is also a reducing sugar — same limitation |
| Works at pH 7.4? | Poorly without low-pKa variants | Yes, mildly acidic optimum |

The glucose problem does not disappear — glucose is also a reducing sugar. But
the chemistry at least engages a group NAM demonstrably has.

**Caveat to check:** the hydrazone forms at the anomeric position. In intact
peptidoglycan that position is consumed by the glycosidic bond, so this works for
**free NAM or hydrolysed cell-wall fragments**, not for intact bacteria. That may
actually suit the sepsis application, where lysed sample is likely anyway.

### 3.3 Electrostatic capture on a cationic surface

NAM's carboxylate is anionic at physiological pH. A positively charged surface
attracts it directly.

| Reagent | Support | Notes |
|---|---|---|
| **Cysteamine** (HS–CH₂CH₂–NH₂) | Ag/Au via thiol | Simplest option; –NH₃⁺ at pH 7 |
| **APTES** | Silicon via silane | Standard on Si; may be applied to exposed regions |
| Poly-L-lysine | either | Multivalent, high charge density |
| Quaternary ammonium thiols | Ag/Au | Permanently charged, pH-independent |

| | |
|---|---|
| Effort | Low — cysteamine self-assembly is a routine overnight step |
| Cost | Very low |
| Selectivity | **Poor** — attracts all anions, including serum proteins |
| Likelihood | Good in buffer, questionable in blood |

Cysteamine has a further advantage: the short linker keeps the analyte close to
the metal, where enhancement is greatest. Longer capture molecules push the
analyte out of the high-field region — a real and often overlooked penalty.

### 3.4 Covalent amide coupling via the carboxyl

EDC/NHS activation of NAM's carboxylic acid, coupled to an amine-terminated
surface (cysteamine or APTES).

| | |
|---|---|
| Bond | Amide — stable and irreversible |
| Effort | Moderate; requires an activation step |
| Reversible | No |
| Use case | Good for a fixed calibration standard; poor for a reusable sensor |

Most useful as a way of preparing a known, permanently attached NAM layer for
establishing the SERS spectrum and adsorption geometry — a reference sample
rather than a sensing mode.

### 3.5 Boronic acid — the current plan

Retained for the reasons set out in the previous design document, with the
reservation already noted: NAM's own cis-diol site is blocked, so boronic acid is
better suited to capturing **intact bacteria** via LPS and teichoic acids than to
capturing free NAM.

**It is not the wrong choice — it is the right choice for a different target.**

### 3.6 Molecularly imprinted polymers

A polymer cast around NAM as template, then the template removed, leaving
shape-complementary cavities. Effectively a synthetic antibody.

| | |
|---|---|
| Selectivity | Potentially high, including against glucose |
| Effort | **High** — polymer optimisation is a project in itself |
| Cost | Low in materials |
| Timescale | Months |

Worth noting as a future direction. Small rigid molecules are good MIP targets,
and NAM's lactyl group gives the cavity something distinctive to recognise. Not
appropriate for the current timeframe.

### 3.7 Biological recognition elements

| Element | Basis | Assessment |
|---|---|---|
| **Lysozyme** | Its active site binds NAM–GlcNAc oligosaccharides | Interesting: a catalytically inactive mutant would bind without cleaving. Needs protein expertise |
| Wheat germ agglutinin | Lectin, binds GlcNAc | May bind NAM weakly; the lactyl group likely interferes |
| Peptidoglycan-binding proteins | e.g. LysM domains | Bind the polymer, not the monosaccharide |
| Anti-NAM antibodies | Immunological | Expensive; availability uncertain for such a small hapten |
| Aptamers | SELEX-selected oligonucleotide | Would require a full selection campaign — 6–12 months |

These offer the best selectivity in principle but all carry cost, stability and
cold-chain penalties that work against a point-of-care device. They are the
fallback if synthetic chemistry proves insufficient.

---

## 4. Substrate and enhancement options

### 4.1 Current approach — HF/AgNO₃ galvanic displacement on n-Si

Cheap and gives good R6G enhancement when it works. The present difficulty is
reproducibility, not enhancement.

### 4.2 Silver colloid, drop-cast with controlled aggregation

The most established alternative. Citrate-reduced AgNPs, aggregated to form
hotspots.

| | |
|---|---|
| Enhancement | High — hotspots between aggregated particles |
| Reproducibility | Historically poor from simple drop-casting, but controlled aggregation methods reach picomolar detection [4, 5] |
| Effort | Low — standard synthesis |
| Advantage | **Decouples the enhancement from the etching process entirely** |

Given that the substrate is the current blocker, having a completely independent
enhancement route is valuable. If NAM gives no signal on colloid either, the
problem is NAM's Raman cross-section, not the substrate.

Aggregation can be induced without added salts — by centrifugation and
ultrasonication, or by freeze–thaw — which avoids introducing ions that compete
for the surface [4, 5].

### 4.3 Gold instead of silver

| | Silver | Gold |
|---|---|---|
| Enhancement at 785 nm | Higher | Somewhat lower |
| Oxidation | **Tarnishes — likely relevant to the contamination problem** | Stable |
| Thiol chemistry | Good | Better, more reproducible monolayers |
| Cost | Low | Higher |

Given that contamination is the current failure mode, silver oxidation and
sulfidation deserve consideration as the cause. Gold, or a **Au@Ag core–shell**
that combines silver's enhancement with gold's stability, is worth evaluating.

### 4.4 Commercial SERS substrate as a diagnostic control

Buy a small number of commercial substrates and run NAM on them.

**This is the fastest way to separate two questions that are currently
entangled:** is the problem the substrate fabrication, or is NAM simply hard to
detect? A commercial substrate has known, guaranteed enhancement. If NAM gives no
signal there either, no amount of etching optimisation will help.

Modest cost, and it could save months.

### 4.5 Physical concentration methods

| Method | Gain | Effort |
|---|---|---|
| Coffee-ring drying | ~10× | Trivial |
| Superhydrophobic surface | 10–100× | Moderate — requires surface treatment |
| Microfluidic pre-concentration | Variable | High — already in the longer-term plan |

Concentrating the sample is often cheaper than improving the substrate, and these
are compatible with any capture chemistry.

---

## 5. Signal strategies — a different way to think about it

### 5.1 Direct detection

Measure NAM's own bands: 930, 956, 871, 830 cm⁻¹. Conceptually clean, but limited
by NAM's weak scattering cross-section.

### 5.2 Indirect / displacement assay

Load the surface with a **strong** Raman reporter that binds the capture
chemistry. When NAM arrives it displaces the reporter, and the reporter signal
**decreases**.

| | |
|---|---|
| Advantage | Signal comes from a strong scatterer, not from weak NAM |
| Advantage | Turns a weak-analyte problem into a strong-reporter problem |
| Disadvantage | Any competing species also displaces the reporter — selectivity comes entirely from the capture chemistry |

**This is a serious option and deserves consideration.** If NAM proves too weak
to detect directly, it may be the practical route. Reporter choice should avoid
NAM's own bands, or the assay can operate purely on reporter intensity.

### 5.3 Raman-tag derivatisation

React NAM with a strongly Raman-active tag before measurement — a hydrazide-
bearing aromatic tag would attach at the reducing end and provide a large
scattering cross-section.

| | |
|---|---|
| Advantage | Enormous signal gain; tag can be chosen to sit in a clear spectral window |
| Disadvantage | Adds a reaction step; less "label-free" |

Standard practice in glycan mass spectrometry [6] and directly transferable here.
Worth keeping as a route to a working assay even if it sacrifices some elegance.

---

## 6. Recommended sequence

Ordered by information gained per unit effort.

| Priority | Action | Effort | Answers |
|---|---|---|---|
| **1** | Drop-cast NAM on bare substrate, measure the coffee ring | 1 day | Can we see NAM at all? |
| **2** | Same on a commercial SERS substrate | 1 day + purchase | Is the problem the substrate or the molecule? |
| **3** | Cysteamine monolayer, electrostatic capture | 3 days | Does a simple cationic surface concentrate NAM? |
| **4** | Silver colloid, controlled aggregation | 1 week | Independent enhancement route |
| **5** | Hydrazide capture | 2 weeks | Best chemical match to NAM's reducing end |
| **6** | Boronic acid (current plan) | 2 weeks | Bacteria capture rather than free NAM |
| 7 | Displacement assay | 3 weeks | Fallback if direct detection fails |
| 8 | Raman tag derivatisation | 3 weeks | Fallback with guaranteed signal |
| 9 | MIP or biological receptors | Months | Long-term selectivity |

**Steps 1 and 2 together cost two days and could redirect the entire project.**
They should be done before further substrate optimisation.

---

## 7. What I would tell the professor

Three points:

**We have been testing the substrate with R6G, which is an easy molecule.** NAM
is a small non-aromatic sugar and will be much harder. We should measure NAM
directly, early, to find out what we are dealing with.

**Boronic acid targets a cis-diol that NAM does not have.** It remains the right
chemistry for capturing intact bacteria through LPS and teichoic acids, but for
free NAM, hydrazide chemistry at the reducing end or simple electrostatic capture
of the carboxylate are better matched.

**Buying a few commercial SERS substrates would resolve the current ambiguity
quickly.** At present we cannot tell whether the difficulty is our fabrication or
the analyte itself, and that distinction determines where the next three months
should go.

---

## References

1. Glycan analysis by reversible reaction to hydrazide beads and mass
   spectrometry. *Analytical Chemistry* (2012).
2. Sugar chain-capturing substance and use thereof (hydrazide selectivity for
   reducing termini).
3. Synthesis of glycopolymers for microarray applications via ligation of
   reducing sugars to a poly(acryloyl hydrazide) scaffold. *JACS* **132** (2010).
4. Centrifugation-induced stable colloidal silver nanoparticle aggregates for
   reproducible SERS detection (2025).
5. Fabricating a three-dimensional SERS substrate using hydrogel-loaded
   freeze-induced silver nanoparticle aggregates (2025).
6. Hydrophobic derivatisation of N-linked glycans for increased ion abundance in
   ESI-MS.

*Citation details to be completed from the source articles before use in a formal
report.*
