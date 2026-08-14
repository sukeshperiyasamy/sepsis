# Capture and Enhancement Strategies for LPS Detection

**Reagent now in hand: Sigma-Aldrich L2630-10MG**

**Project:** SERS nanobiosensor for rapid bacterial identification in sepsis
**Prepared:** August 2026

---

## 1. The reagent, and why it matters for strategy

| Property | Value |
|---|---|
| Source | *Escherichia coli* O111:B4 |
| Supplier / catalogue | Sigma-Aldrich, L2630-10MG |
| CAS / EC | 93572-42-0 / 297-473-0 |
| Purification | Phenol extraction (Westphal method) |
| Protein impurity | ≤3% |
| Form | Lyophilised powder, water-soluble |
| Storage | 2–8 °C |

Two things about this specific reagent shape everything below.

**First, phenol extraction preserves the O-antigen.** Unlike TCA-extracted or
deep-rough preparations, Westphal phenol extraction yields predominantly
**smooth LPS** — intact Lipid A, core oligosaccharide, and the full O111
O-antigen repeat. This matters directly for capture chemistry: any strategy
that targets the core sugars (boronic acid) has to reach past the O-antigen to
get there, while any strategy that targets Lipid A's phosphates (cationic
capture, antibody) is targeting a group that sits at the base of the molecule,
also somewhat shielded by the polysaccharide above it.

**Second, this is functionally the same reagent used in the closest published
precedent.** Rusciano et al. (2023) — the most directly comparable SERS-LPS
study, and already the anchor reference in this project's prior literature
review — used Sigma-Aldrich LPS from *E. coli* O111:B4 (catalogue L6529, a
different purification/purity grade of the same serotype). This project's
L2630 is close enough in identity that their reported figures function as a
real benchmark, not just a qualitative comparison: same organism, same
serotype, same supplier family. **This is worth stating early because it
changes the value of the very first experiment** — a bare-substrate LPS
measurement here is directly comparable to their Cmin ≈ 3 ng/mL result, not
just "in the right ballpark."

---

## 2. LPS's chemical handles — a genuinely different situation from NAM

The NAM capture document (previous strategy note) treated NAM as a hard case:
small, non-aromatic, no chromophore, weak intrinsic affinity for bare silver.
**LPS is a different molecule in almost every relevant respect.**

| Feature | Location | Relevance to capture |
|---|---|---|
| **Phosphate groups (×2)** | Lipid A, 1 and 4′ positions | Strongly anionic at pH 7; genuine electrostatic handle |
| **Acyl chains (4–6, hydrophobic)** | Lipid A | Amphiphilic — can physisorb to a bare metal surface via hydrophobic/van der Waals contact, not just charge |
| **KDO carboxylate + vicinal diol** | Core, innermost sugar (3-deoxy-D-*manno*-oct-2-ulosonic acid) | **A genuine cis-diol** — unlike NAM, this is a real boronic-acid target |
| **Heptose diols** | Core | Additional diol sites, same caveat on accessibility |
| **Core phosphates** | Core oligosaccharide | Further anionic character, reinforcing the electrostatic case |
| **O-antigen repeat units** | Distal, O111-specific | Hydrophilic, serotype-defining; likely shields the core and Lipid A from a functionalised surface in smooth LPS |

**The practical consequence:** LPS is amphiphilic and multiply anionic, with a
combination of hydrophobic and electrostatic character that gives it real
intrinsic affinity for a bare metal surface. This is precisely the property
NAM lacked. It is also large and structurally heterogeneous (batch-to-batch
and even molecule-to-molecule micellar aggregation state varies), which cuts
the other way — spectra are broader and less easily assigned than a small
molecule's.

---

## 3. Capture strategies, ranked

### 3.1 Direct adsorption — no capture chemistry at all

**Try this first, and expect it to actually work.** This is the single
biggest strategic difference from NAM.

| | |
|---|---|
| Method | Drop-cast LPS solution onto the existing substrate, dry, measure the 2850–2950 cm⁻¹ region (Lipid A acyl C–H stretches) |
| Precedent | Rusciano et al. (2023) measured **bare, unfunctionalised** silver substrates dosed directly with *E. coli* O111:B4 LPS and extrapolated a Cmin of **≈3 ng/mL** from the 2900 cm⁻¹ band — before any antibody was added. Verde et al. (2021, *Front. Immunol.*) independently demonstrated label-free LPS SERS on bare 50 nm AuNPs. |
| Mechanism | Acyl-chain physisorption plus electrostatic attraction of the phosphate groups to the metal — LPS does not need a designed anchor to reach the surface |
| Effort | Trivial — one afternoon |
| Likelihood | **High**, on existing precedent with the same serotype |

This should be the very first LPS experiment run on the current substrate. If
it reproduces even roughly what Rusciano's bare-substrate measurement showed,
that is a strong, fast signal that the existing fabrication is fine for LPS —
resolving, for this biomarker at least, the substrate-vs-chemistry ambiguity
that has been the project's central open question.

### 3.2 Cationic capture layer — exploiting the net negative charge

LPS is anionic at physiological pH (Lipid A phosphates plus KDO/core
carboxylates and phosphates). A cationic surface concentrates it directly,
the same logic used for NAM's carboxylate but with a much stronger charge
handle here.

| Reagent | Support | Notes |
|---|---|---|
| **Cysteamine** (HS–CH₂CH₂–NH₂) | Ag/Au via thiol | Simple, routine overnight self-assembly |
| **Chitosan** | either, via physical/electrostatic anchoring | Well precedented for LPS specifically — Chi-AgNPs used for electrochemical LPS biosensing (Kim et al., *Micromachines* 2020); polysaccharide backbone also gives multivalent binding |
| **Polymyxin B** | Ag/Au, adsorbed or thiolated | **Not a generic cationic layer — a genuine Lipid A-binding ligand.** Polymyxin B is a cyclic cationic lipopeptide that binds Lipid A with high, well-characterised affinity; it is the basis of clinical endotoxin-neutralisation assays. This gives real selectivity for LPS over other anionic serum species, not just charge attraction |

| | |
|---|---|
| Effort | Low (cysteamine/chitosan) to moderate (polymyxin B) |
| Selectivity | Poor (cysteamine, chitosan) to good (polymyxin B) |
| Likelihood | Good in buffer; polymyxin B should hold up better in serum |

**Recommendation within this tier:** skip straight to polymyxin B if resources
allow. Cysteamine/chitosan mainly answer "does concentrating LPS at the
surface help at all," a question direct adsorption (§3.1) may already answer
on its own.

### 3.3 Boronic acid — the strategy already in place, now aimed at its real target

The NAM document's verdict on boronic acid was: *"the right choice for a
different target."* **This reagent is that target.**

| | |
|---|---|
| Site | KDO carboxylate + vicinal diol; heptose diols in the core |
| Bond formed | Boronate ester, reversible |
| Precedent | A CRISPR/Cas12a + boronic-ester + LPS-aptamer dual-recognition assay (*Anal. Chem.* 2022) confirms boronic-acid–LPS binding is real and usable in an assay context |
| **Caveat specific to this reagent** | Because L2630 is phenol-extracted **smooth** LPS, the O-antigen may sterically shield the core diols from a surface-bound boronic acid ligand. This is a *different* failure mode from NAM's (chemical substitution vs steric shielding) but has the same practical consequence — worth testing directly rather than assuming |

**Recommended test, directly analogous to the NAM binding check:** compare
4-MPBA reporter-band response (1072/1585 cm⁻¹) on exposure to this LPS versus
a simple diol (fructose) at matched concentration, and — if resources allow —
versus a **rough or deep-rough LPS / free Lipid A standard**, where the core
is not O-antigen-shielded. A large response to fructose but a small one to
smooth LPS, recovered on the rough form, would confirm shielding rather than
a fundamentally unreactive core.

This is also the step that most directly reuses existing project
infrastructure — the same 4-MPBA monolayer already being developed for NAM.

### 3.4 Anti-Lipid A antibody — highest selectivity, direct benchmark available

| | |
|---|---|
| Reagent | Commercial polyclonal anti-Lipid A / anti-LPS antibody |
| Mechanism | **Not direct LPS detection.** The antibody itself is the Raman reporter; LPS binding perturbs the antibody's own SERS spectrum (frequency shift, band splitting near 1660 cm⁻¹, blue-shift of the 2900 cm⁻¹ envelope) |
| Precedent | Rusciano et al. (2023), same serotype: **LOD 12 ng/mL, LOQ 41 ng/mL**, established via SNR-based extrapolation on real (not extrapolated) binding data |
| Selectivity | High — the antibody-antigen step does the discrimination, not the substrate |
| Cost / effort | Antibody cost; two-stage functionalisation (Ab coating, then blocking solution to suppress non-specific binding); readout requires multivariate analysis (PCA) rather than a single peak, since the spectral changes are broad and distributed |

**This is the most rigorously benchmarkable option in this whole document.**
Because the organism and serotype match Rusciano's study, a result here is a
direct head-to-head comparison, not a "similar system" comparison — a
genuinely rare position to be in.

### 3.5 Molecularly imprinted polymers (MIP)

A polymer cast around LPS (or Lipid A) as template, then the template
removed, leaving shape- and charge-complementary cavities.

| | |
|---|---|
| Precedent | Özsoylu et al. (2026, *Chem. Eng. J.*) — LPS-templated biomimetic MIP surfaces for high-affinity bacterial capture; a related 2024 *Anal. Chem.* MIP targets bacterial outer-membrane vesicles |
| Selectivity | Potentially high, and — unlike an antibody — stable at room temperature, relevant for a point-of-care device |
| Effort | High; polymer optimisation is a project in itself |
| Timescale | Months |

Actively published (2023–2026), so this is a credible, not speculative,
future direction — but not appropriate for the current timeframe.

### 3.6 Linear polymer affinity agents + machine learning (2025)

A newer category worth flagging explicitly. A 2025 study (*ACS Appl. Mater.
Interfaces*) used **broad-affinity linear polymer capture agents** (not
antibody, not a single-target small molecule) immobilised on a metal-film-
over-nanosphere substrate, combined with machine learning classification, to
detect and *differentiate* LPS from multiple foodborne pathogens by spectral
fingerprint rather than by a single diagnostic band.

| | |
|---|---|
| Advantage | Captures LPS broadly (serotype-agnostic), then relies on ML to distinguish sources — sidesteps the need for a serotype-specific binder |
| Relevance here | Directly applicable to this project's stated goal of Gram-class (and potentially organism-level) discrimination from a single sensing channel |
| Effort | Moderate — depends on sourcing or synthesising the affinity polymer; ML classification pipeline is a natural extension of work already done for NAM/R6G peak-matching |
| Maturity | New (2025); worth tracking rather than committing to immediately |

### 3.7 Aptamers

SELEX-selected oligonucleotides against LPS exist in the literature (used
directly in the CRISPR/Cas12a boronic-ester assay cited in §3.3) and offer
high selectivity without an antibody's cold-chain fragility. As with the NAM
document's assessment, a full SELEX campaign is 6–12 months and not
appropriate now — but a **commercially available anti-LPS aptamer**, if one
can be sourced off the shelf, would skip that timeline entirely and is worth
a quick supplier check before ruling this out.

---

## 4. Signal strategies

### 4.1 Direct detection

LPS's own bands are, unlike NAM's, reasonably well characterised in the SERS
literature even if broad: Lipid A acyl C–H stretching (2850–2950 cm⁻¹,
diagnostic and used directly by Rusciano for the bare-substrate measurement),
amide/C=O modes near 1650–1660 cm⁻¹, C–N stretching near 1250 cm⁻¹, and
core-sugar ring modes in the 800–1150 cm⁻¹ fingerprint region. Expect broad,
overlapping bands rather than the sharp, well-separated peaks seen for NAM —
this is a large, structurally heterogeneous molecule, and multi-Gaussian
deconvolution (as Rusciano used for the 2900 cm⁻¹ envelope) or full
multivariate analysis (PCA, or ML per §3.6) is the realistic path to a
quantitative readout, not single-peak intensity.

### 4.2 Indirect / reporter-perturbation assay

The antibody strategy (§3.4) is a specific case of this: a strong Raman
reporter's own spectrum shifts or splits when LPS binds nearby, and the
*change* — not an LPS band — carries the concentration information. This
generalises beyond antibodies: a polymyxin B–dye conjugate, following the
logic of clinical endotoxin-neutralisation assays, could serve the same
reporter role at lower cost than a full antibody.

### 4.3 Machine-learning-assisted classification

Increasingly the standard approach for LPS/endotoxin SERS specifically —
Yang et al. (2022, *Nanoscale*) differentiated bacterial endotoxins by SERS
plus ML; "DeepRaman" (2025) extends this; the linear-polymer-affinity study
(§3.6) pairs broad capture with ML discrimination. Given that this project
already has DFT-grounded peak assignments and a working Python/computational
pipeline from the NAM work, extending toward classification (rather than
single-band quantification) is a natural and comparatively low-cost next
step once real LPS spectra exist.

---

## 5. Recommended sequence

Ordered by information gained per unit effort, and updated for the fact that
this reagent is a direct match to the closest published precedent.

| Priority | Action | Effort | Answers |
|---|---|---|---|
| **1** | Drop-cast LPS on bare existing substrate; measure 2850–2950 cm⁻¹ | 1 day | Does the existing substrate reproduce Rusciano's bare-substrate Cmin (~3 ng/mL) for the same serotype? |
| **2** | Same on a commercial SERS substrate | 1 day + purchase | Separates fabrication issues from LPS-specific issues (same logic as the NAM plan) |
| **3** | Polymyxin B capture layer | 1 week | Does a genuine Lipid A ligand outperform bare adsorption, particularly in a serum-like background? |
| **4** | 4-MPBA boronic acid monolayer (existing chemistry) | 1–2 weeks | Does the core diol bind, or is it O-antigen-shielded — test against fructose and, if available, a rough-LPS control |
| **5** | Anti-Lipid A antibody, frequency-shift readout | 2–3 weeks | Direct, same-serotype benchmark against Rusciano's 12/41 ng/mL LOD/LOQ |
| 6 | Cysteamine/chitosan generic cationic layer | 3 days | Lower priority than polymyxin B; mainly useful if polymyxin B is unavailable |
| 7 | Linear polymer affinity agent + ML classification | Weeks–months, sourcing-dependent | Multiplex/serotype-agnostic capture — aligns with the project's Gram-class discrimination goal |
| 8 | MIP | Months | Long-term selectivity, room-temperature-stable alternative to antibody |
| 9 | Aptamer (SELEX campaign) | 6–12 months | Only if no off-the-shelf aptamer can be sourced |

**Steps 1 and 2 together cost two days and, unusually for this project,
compare directly against a published number rather than an unknown.** They
should be run before anything else involving this reagent.

---

## 6. What I would tell the professor

Three points:

**This reagent is a near-exact match to the strongest published precedent
this project has.** Rusciano et al. (2023) used the same organism and
serotype (*E. coli* O111:B4) from the same supplier family. Every experiment
run with this LPS can be benchmarked against a real, published LOD/LOQ
(12/41 ng/mL, or Cmin ≈3 ng/mL for bare-substrate detection) rather than
compared only qualitatively to "similar" work.

**LPS is intrinsically far more SERS-favourable than NAM.** It is amphiphilic
and multiply anionic — properties that give it real affinity for a bare
metal surface without any capture chemistry — where NAM had essentially
none. The first experiment should be the cheapest one: direct adsorption on
the existing substrate.

**Boronic acid, already the project's working chemistry, is aimed at the
wrong analyte if used for free NAM, but is aimed at the right one here.**
LPS's core KDO and heptose residues carry genuine, unblocked cis-diols. The
open question for *this* reagent specifically is not whether the chemistry
exists, but whether the intact O111 O-antigen (a consequence of choosing the
phenol-extraction / smooth-LPS product) sterically shields those diols — a
one-week experiment, not a redesign.

---

## References

1. Rusciano, G.; Capaccio, A.; Sasso, A.; Capo, A.; Almuzara, C.M.; Staiano,
   M.; D'Auria, S.; Varriale, A. "A Surface-Enhanced Raman Spectroscopy-Based
   Biosensor for the Detection of Biological Macromolecules: The Case of the
   Lipopolysaccharide Endotoxin Molecules." *Int. J. Mol. Sci.* 24(15):12099
   (2023). DOI:10.3390/ijms241512099. [Uses *E. coli* O111:B4 LPS,
   Sigma-Aldrich L6529 — same serotype/supplier family as this project's
   L2630.]
2. Verde, A.; Mangini, M.; Managò, S.; Tramontano, C.; Rea, I.; Boraschi, D.;
   Italiani, P.; De Luca, A.C. "SERS sensing of bacterial endotoxin on gold
   nanoparticles." *Front. Immunol.* 12:758410 (2021).
3. Yang, D.; Xu, S.; Haverstick, J.; Ibtehaz, N.; Muszyński, A.; Chen, X.;
   Chowdhury, R.; Zughaier, S.M.; Zhao, Y. "Differentiation and
   classification of bacterial endotoxins based on surface enhanced Raman
   scattering and advanced machine learning." *Nanoscale* 14(24):8806–8817
   (2022). DOI:10.1039/d2nr01277d.
4. "DeepRaman: Implementing SERS with cutting-edge machine learning for
   differentiation/classification of bacterial endotoxins." (2025).
5. CRISPR/Cas12a + boronic ester + LPS aptamer dual-recognition assay.
   *Anal. Chem.* (2022). PubMed 36040369.
6. Kim, H. et al. "Chitosan Stabilized Silver Nanoparticles for the
   Electrochemical Detection of Lipopolysaccharide: A Facile Biosensing
   Approach for Gram-Negative Bacteria." *Micromachines* 11(4):413 (2020).
   PMC7231338.
7. Özsoylu, D.; Börmann-El Kholy, E.; Wagner, P.; Schöning, M.J.
   "Lipopolysaccharide-templated biomimetic MIP surfaces for high-affinity
   bacterial capture." *Chem. Eng. J.* (2026).
8. "Lipopolysaccharide Imprinted Polymers for Specific Recognition of
   Bacterial Outer Membrane Vesicles." *Anal. Chem.* (2024).
   DOI:10.1021/acs.analchem.4c05288.
9. "A Machine Learning-Enabled SERS Sensor: Multiplex Detection of
   Lipopolysaccharides from Foodborne Pathogenic Bacteria." *ACS Appl.
   Mater. Interfaces* (2025). DOI:10.1021/acsami.5c08361.
10. Sigma-Aldrich product page, Lipopolysaccharides from *E. coli* O111:B4,
    L2630 (CAS 93572-42-0, EC 297-473-0).

*Citation details to be independently verified against the primary sources
before use in a formal report, consistent with the practice followed for the
NAM capture-strategy document.*
