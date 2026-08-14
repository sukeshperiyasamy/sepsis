% LPS SERS Sensor — Experimental Design and Literature-Derived Rationale
% Project: SERS nanobiosensor for rapid bacterial identification in sepsis
% Prepared: 14 August 2026

---

## 1. Objective and target definition

**Goal.** Achieve label-free (or, if necessary, antibody-assisted) SERS detection of lipopolysaccharide from *Escherichia coli* O111:B4 (Sigma-Aldrich L2630) on the project's existing Ag/Si substrate, with a concentration-dependent response, a stated limit of detection, and reproducibility across spots and substrates.

**Explicit claim boundary.** The correct claim is *"label-free SERS detection of LPS derived from E. coli O111:B4,"* not "detection of E. coli bacteria" and not "sepsis diagnosis." LPS is shared across Gram-negative organisms and its presence is not itself confirmatory of sepsis (this qualification is made explicitly by the closest sepsis-biosensor literature reviewed for this project). If a later stage shows the fingerprint is specific enough to distinguish O111:B4 from other endotoxins, that is a *separate, stronger* claim to be earned with data (Section 6, Stage 6), not assumed at the outset.

**What in the molecule we are actually targeting.** LPS is not a single Raman-active group the way a dye is; it is a large, structurally layered molecule, and different capture/detection strategies target different parts of it:

- **Lipid A acyl chains** (4–6 hydrophobic fatty-acid tails) — the strongest and most literature-precedented direct SERS handle, via C–H stretching bands at 2850–2950 cm⁻¹. This is also the region Rusciano et al. (2023) used for their bare-substrate measurement.
- **Lipid A phosphate groups** (1 and 4′ positions) — the primary anionic handle, relevant to any cationic capture strategy (chitosan, cysteamine, polymyxin B) and to P–O stretching bands in the 1090–1250 cm⁻¹ region.
- **Core oligosaccharide** — KDO (3-deoxy-D-*manno*-oct-2-ulosonic acid) and heptose residues carry a genuine, unblocked cis-diol and a carboxylate, the target for boronic-acid capture. Core sugar ring modes fall in the 800–1150 cm⁻¹ fingerprint region.
- **O-antigen** (O111-specific repeat) — the outermost, most hydrophilic layer. Because our reagent is phenol-extracted (Westphal) *smooth* LPS, the O-antigen is intact and may sterically shield the core and Lipid A from a functionalised surface. This is a design constraint, not just a footnote (Section 7).

---

## 2. Literature foundation — what we take from each paper, and why

This project does not need to invent new SERS chemistry. Every element of the design below is traceable to a specific published result. The table states, for each paper: what they actually did, what we are adopting from it, and where we are deliberately deviating.

| Paper | What they did | What we take from it | Where we differ |
|---|---|---|---|
| **Rusciano et al., *Int. J. Mol. Sci.* 24(15):12099 (2023)** — the project's primary benchmark | Nanoporous coral-like Ag SERS substrate; measured LPS from *E. coli* O111:B4 (Sigma L6529) directly on bare substrate (Cmin ≈ 3 ng/mL, from the 2900 cm⁻¹ acyl C–H band) and via an anti-Lipid-A antibody frequency-shift assay (LOD 12 ng/mL, LOQ 41 ng/mL); worked strictly **below LPS's critical micellar concentration** | Same organism and serotype as our L2630 reagent — a direct, not approximate, benchmark. Adopt their concentration range (10 ng/mL–10 µg/mL for bare, 1 ng/mL–10 µg/mL for antibody), their SNR-based LOD/LOQ method (SNR = 3 for LOD, 10 for LOQ), their sub-CMC concentration discipline, and their four-way logic (bare substrate vs. antibody-coated, LPS vs. no-LPS) | Our substrate is fabricated by one-step AgNO₃/HF MACE on n-type Si, not their sputtered-Ag/plasma-roughened-glass route — a different fabrication line reaching for the same electromagnetic mechanism |
| **Verde et al., *Front. Immunol.* 12:758410 (2021)** | Label-free LPS SERS directly on bare 50 nm AuNPs (*E. coli*, *K. pneumoniae*) | Independent confirmation that bare-metal, no-capture-chemistry LPS detection is a real, reproducible phenomenon — not unique to Rusciano's substrate | We use Ag/Si, not colloidal Au |
| **Bai, Du, Wang, Wu, Sugioka, *Nanomaterials* 9(11):1531 (2019)** | MACE (HF/AgNO₃ nucleation → HF/H₂O₂ etch) on **n-type Si, 1–10 Ω·cm** — the identical doping/resistivity band as our own wafer — with Ag NPs by UV photonic reduction; EF ≈ 1.4×10⁸ on R6G and dopamine | Confirms our existing wafer stock is not a compromise choice — it matches a published high-performing recipe exactly. Adopt their EF figure as a realistic target ceiling | We use electroless AgNO₃/HF deposition, not a separate UV photonic-reduction step |
| **Kochylas et al., *Nanomaterials* 11(7):1760 (2021)** | One-step MACE Si-nanowire/Ag SERS, EF up to ~10⁸, R6G LOD to 10⁻¹³ M; nanostructure density tunable via AgNO₃ concentration | This is the direct precedent for our current fabrication route (already cited in the project's own DOE strategy). Adopt their finding that a **strip-and-regrow cycle** improves hotspot uniformity over a single as-grown dendritic soak | Not yet implemented in our process — flagged as a Stage 4 refinement, not a Stage 0 requirement |
| **Yang et al., *Nanoscale* 14(24):8806–8817 (2022)** | Ag-nanorod-array (glancing-angle deposition) SERS + ML classification of bacterial endotoxins, including LPS vs. LTA vs. peptidoglycan discrimination | Confirms LPS/LTA SERS fingerprints carry enough information for ML classification — the basis for our Stage 6 extension | No stated quantitative LOD in their work; we treat this as a classification precedent, not a sensitivity benchmark |
| **CRISPR/Cas12a + boronic ester + LPS aptamer, *Anal. Chem.* (2022)** | Dual-recognition assay using a boronic-ester–LPS binding step | Direct confirmation that boronic acid genuinely binds LPS (via the core KDO/heptose diol) in a working assay — this is real, not inferred by analogy the way it was for NAM | Not a SERS assay; we are transferring the binding chemistry, not the readout method |
| **Kim et al., *Micromachines* 11(4):413 (2020)** | Chitosan-stabilised AgNPs for electrochemical LPS biosensing | Precedent for chitosan as an LPS-specific (not just generically cationic) capture layer | Electrochemical, not SERS readout — chemistry transfers, physics does not |
| **Polymyxin B–AgNP, *Analyst* (2018)** | Polymyxin B–silver colloid system for LPS analysis | Polymyxin B is a genuine Lipid-A-binding ligand (clinical endotoxin-neutralisation basis), not a generic cationic coating — our first-choice capture layer if bare detection needs a selectivity boost | — |
| **Özsoylu et al., *Chem. Eng. J.* (2026); MIP–OMV, *Anal. Chem.* (2024)** | LPS-templated molecularly imprinted polymers | Confirms MIP capture for LPS is an active, feasible 2023–2026 research line | Months-scale development; a Stage-5+ option, not part of the near-term plan |
| **"Machine Learning-Enabled SERS Sensor," *ACS Appl. Mater. Interfaces* (2025)** | Broad-affinity linear polymer LPS capture + ML multiplex classification across bacterial serotypes | Shows a path to serotype-level discrimination without a serotype-specific antibody | New (2025), sourcing/synthesis of the affinity polymer not yet established for our lab |
| **IEEE Biosensors 2026 poster (Singh, Sharma, Soni, Agarwal)** — same host lab, cited in a separate note, **not independently verified via literature search** | Citrate-reduced AgNP colloid + wet-etched n-Si, **532 nm** excitation, LPS response reported 1 nM–10 µM | A related in-house architecture, useful as a secondary reference point | Our Raman system (B&W Tek i-Raman Plus, model BWS465-**785H**) is a dedicated 785 nm instrument — the 532 nm line this poster used is very unlikely to be available on our system. We treat this as a *different candidate architecture* to consider later (Section 6, Stage 4b), not a route to adopt by default, and we do not carry over its concentration range as a target since resonance/plasmon-matching conditions differ at 785 nm |

**One correction to a claim that circulated in earlier project discussion:** a frequently-cited "1 nM LOD for LPS" attributed to a 2022 AgNP/black-phosphorus sepsis-biosensor paper (Kundu et al., *Sensors & Diagnostics*, DOI 10.1039/d1sd00057h) does not hold up — the full text of that paper (already in the project's `lps research` folder) was checked directly, and it contains **zero** occurrences of "LPS" or "lipopolysaccharide." That paper detects IL-3 and procalcitonin, not LPS. It should not be used as an LPS benchmark or cited in any manuscript arising from this work.

---

## 3. Substrate target: pore size and hotspot geometry

"Pore size" in this context really means two related, both-necessary things: the **silicon nanostructure geometry** (which the fabrication chemistry controls) and the **interparticle silver gap** (the actual electromagnetic hotspot), which is the parameter that matters most.

| Parameter | Target | Basis |
|---|---|---|
| Si pore/nanowire diameter | ≈ 50–200 nm | Commonly reported MACE nanowire diameter range for black-Si SERS substrates; tunable via AgNO₃ concentration and etch time in our own process |
| Ag particle/aggregate size | ≈ 50–100 nm | Most commonly cited optimum for visible/NIR excitation across the general SERS literature |
| **Interparticle (hotspot) gap** | **Sub-10 nm, ideally 1–5 nm** | SERS intensity scales with the fourth power of local field enhancement (the \|E\|⁴ law) — small changes in gap size in this range produce disproportionately large signal changes. This is the single most important geometric parameter, more important than particle size alone |
| Nanostructure density | Moderate, evenly distributed — **not** maximised | Excessive density risks wire clumping/collapse, a known MACE artefact that degrades reproducibility without proportionally increasing hotspot count |
| Reported enhancement ceiling at this geometry | ~10⁶–10⁸ (up to ~10× higher on a genuinely 3D nanowire scaffold vs. a flatter equivalent) | Bai et al. 2019 (1.4×10⁸), Kochylas et al. 2021 (up to 10⁸) |

**LPS-specific addition to this section — not relevant for R6G or NAM, and worth stating explicitly.** LPS self-assembles into micellar aggregates in aqueous solution above its critical micellar concentration (CMC). If working concentration is not controlled, LPS may present to the substrate as aggregates larger than the 1–5 nm target hotspot gap, physically excluding the relevant Lipid-A/core groups from the highest-field region regardless of how well the substrate itself is engineered. Rusciano et al. explicitly worked "under critical micellar concentration" for exactly this reason. **Design rule: all LPS working solutions in this plan are kept in the same sub-µg/mL-to-low-µg/mL range Rusciano validated, and we do not assume a bare numeric CMC for our specific reagent lot without confirming it — this is flagged as an open verification item, not asserted as known (Section 7).**

**Current status against this target:** our wafer (n-type, phosphorus-doped, ⟨100⟩, 1–10 Ω·cm) already matches the Bai et al. precedent exactly, so no new silicon is needed. The interparticle gap on our *own fabricated* substrate has never been measured (no AFM or high-resolution SEM on file) — this is a genuine open item, not a known deficiency, and is the single most valuable characterisation measurement to obtain before over-interpreting any negative LPS result as a chemistry failure rather than a geometry issue.

---

## 4. Chemical mixing protocols

### 4.1 Ag/Si substrate fabrication bath (unchanged — already validated via R6G)

This bath is not being redesigned for LPS; it is the same one-step electroless AgNO₃/HF MACE process already validated on this project via R6G (DFT-vs-experiment RMSE 4.62 cm⁻¹, r = 0.99995). Reproduced here for completeness and because LPS work should use the best-characterised existing condition as its starting point rather than a fresh, unvalidated batch.

| Reagent | Amount | Notes |
|---|---|---|
| AgNO₃ | 0.170 g in 50 mL DI water (≈20.0 mM baseline) | Formula: mass (g) = target molarity × 0.050 L × 169.87 g/mol. This is the best-characterised condition on file; other AgNO₃ concentrations (5/10/40/80 mM) remain open DOE variables per the project's existing optimisation study, not part of the LPS-specific plan |
| HF | 8.6 mL concentrated stock, added **to** the AgNO₃/DI mixture (not the reverse — order matters for controlled nucleation), topped to 50 mL total | Stock assumed 49% w/w — **not independently confirmed against the reagent bottle; confirm before treating any derived molarity as exact** |
| Etch/MACE time | 2 minutes (baseline) | — |
| Post-process | DI rinse → 110 °C bake, 10 min → vacuum-desiccated storage | Current mitigation against silver oxidation; no formal shelf-life study exists yet, so use freshly fabricated substrates (within days) for LPS work until one does |

**Safety (unchanged from existing project SOP, restated because HF is present in every batch of this protocol):** double gloves with an HF-rated outer layer, face shield, fume hood, calcium gluconate gel accessible at the bench, never work alone at any stage of bath preparation or etching.

### 4.2 LPS stock and concentration series

**Reporting unit: mass concentration (ng/mL, µg/mL), not molarity.** LPS from phenol extraction is a heterogeneous, polydisperse preparation without a single defined molecular weight, and Sigma's own specification for this class of product reports it in mass and potency (EU/mg) terms rather than a molar figure. Converting to molarity would manufacture false precision. This also matches Rusciano et al.'s own reporting convention, which is the direct point of comparison.

| Step | Detail |
|---|---|
| Stock preparation | Dissolve L2630 in DI water (matches the project's established solvent choice for all three biomarkers — PBS is specifically avoided because its phosphate bands overlap the 800–1100 cm⁻¹ region used for biomarker diagnostic bands). Reagent solubility per Sigma spec: ≈5 mg/mL clear-to-hazy at room temperature |
| Primary series | Log-dilution series from 10 µg/mL down to 10 ng/mL, matching Rusciano's tested range exactly for direct comparability |
| Extension series | Continue the log-dilution down toward 1 ng/mL and below, to find where **our own** substrate stops detecting LPS, rather than assuming their 12 ng/mL or 3 ng/mL figures will reproduce exactly on a different fabrication line |
| Deposition | 2–3 µL drop-cast per spot, matching the project's existing biomarker-deposition convention (consistent with the volumes used for NAM) |
| Concentration ceiling | Do not exceed the low-µg/mL range without explicit justification — this is the CMC design constraint from Section 3 |

### 4.3 Optional capture-chemistry reagents (Stage 3+, not required for the first experiment)

These are **not needed to start** — they are held in reserve for the branch of Section 6 where bare detection needs a selectivity or sensitivity boost. None are currently in the lab's chemical inventory; procurement is a prerequisite for this section only.

| Reagent | Working concentration (literature-typical) | Purpose |
|---|---|---|
| Polymyxin B | Low µg/mL range, adsorbed or thiol-anchored onto Ag | Lipid-A-specific capture; first choice if a capture layer is needed, on cost and selectivity grounds |
| Chitosan | Dilute acidic solution (typically 0.1–1% w/v), physically/electrostatically anchored | Generic cationic capture, LPS-precedented (Kim et al. 2020) |
| Cysteamine | ~1–10 mM ethanolic solution, thiol self-assembly, overnight | Simplest cationic layer; lowest selectivity of the options listed |
| Anti-Lipid-A antibody (if replicating Rusciano's assay) | 10 µg/mL in 50 mM Na-phosphate buffer, pH 7.4, 2 h incubation, RT, humid chamber; followed by a blocking solution (1% BSA, 1% sucrose, 0.05% Tween-20 in 50 mM Tris-HCl, pH 7.4) | Highest-selectivity option, and the only one with a direct, same-serotype published LOD/LOQ to benchmark against |

---

## 5. Testing / measurement protocol

### 5.1 Four-way control structure

Every concentration point is measured against this fixed comparison set, not in isolation. This is the single most important methodological safeguard in the whole plan — it is what lets a result be attributed to LPS rather than to the substrate or the fabrication chemistry.

| Control | Purpose |
|---|---|
| Bare Si (no Ag) | Confirms no signal originates from the silicon itself |
| Ag/Si, no analyte (blank) | Establishes the substrate's own background spectrum |
| LPS on bare Si (no Ag) | Confirms any signal seen on Ag/Si is plasmonically enhanced, not just LPS's native (very weak) Raman signal |
| **LPS on Ag/Si** | The measurement of interest |

### 5.2 Acquisition parameters

| Parameter | Value |
|---|---|
| Instrument | B&W Tek i-Raman Plus, BWS465-785H / BTC665N-785H-SYS |
| Excitation | 785 nm (784.92 nm actual) |
| Objective | 20× Plan (existing standard) |
| Target band | 2850–2950 cm⁻¹ (Lipid A acyl C–H stretch) as the primary diagnostic window, following Rusciano's own approach directly |
| Secondary bands to record (even though not primary) | 1090–1250 cm⁻¹ (phosphate/C–N), 800–1150 cm⁻¹ (core sugar ring) — full-range acquisition costs nothing extra and preserves information for later PCA/ML work |
| Integration / accumulations | Hold constant across the whole concentration series (do not vary power or integration time mid-series — this was an explicitly identified past failure mode in this project's NAM work, where varying two variables at once made a negative result uninterpretable) |
| Spots per condition | ≥5, at different points on the substrate, to characterise spot-to-spot variability (not just report a single "best" spectrum) |
| Laser power check | Measure true power at the sample in mW with a power meter before starting, if one is accessible — this has never been done for this instrument and is a five-minute fix that materially improves how comparable any LOD figure is to the literature |

### 5.3 Data processing and LOD/LOQ

- Baseline correction (polynomial or ALS, consistent with the method already used for R6G on this project).
- Track the 2850–2950 cm⁻¹ band intensity (or, if an antibody layer is used, the frequency shift of the antibody's own bands, following Rusciano's Section 2.3 method exactly).
- Compute signal-to-noise ratio at each concentration; fit the low-concentration region linearly; extrapolate the concentration at which SNR = 3 for LOD and SNR = 10 for LOQ — this is a direct reuse of Rusciano's own method, chosen specifically so the resulting number is comparable to theirs, not just superficially similar.
- Report mean ± SD and %RSD across spots at each concentration, and across independently fabricated substrates at one fixed concentration — this project has never yet produced a formal reproducibility figure for any biomarker, and LPS is the best-positioned biomarker in the panel to be the first one that does.

---

## 6. Staged approach — reproduce the benchmark first, then branch

This is the direct answer to "if we can recreate the same sensor, then we try other methods." The plan is a decision tree with explicit go/no-go gates, not a linear list — each stage either confirms the hypothesis and moves forward, or fails informatively and points at a specific next action rather than a vague "try something else."

**Stage 0 — Reproduce the benchmark, no new fabrication or chemistry.**
Drop-cast the LPS concentration series (Section 4.2) directly onto the *existing*, already R6G-validated Ag/Si substrate. No capture chemistry, no new silver route. This is the cheapest possible experiment — a few days — and it is testing the most favourable-case hypothesis in the whole project: that LPS, unlike NAM, has enough intrinsic amphiphilic/anionic affinity for bare Ag to be detected directly (Verde et al. 2021; Rusciano et al.'s own bare-substrate result).
*Go:* a concentration-dependent 2850–2950 cm⁻¹ signal appears, reproducible across ≥5 spots and absent from the bare-Si and blank controls → proceed to Stage 1.
*No-go:* no signal, or signal indistinguishable between LPS and blank → proceed to Stage 2 before concluding anything about LPS chemistry.

**Stage 1 — Quantify.**
Full concentration series, LOD/LOQ by the SNR method (Section 5.3), reproducibility across ≥3 independently fabricated substrates. Compare the resulting LOD against Rusciano's 3 ng/mL bare-substrate figure — not expecting an exact match (different fabrication line), but expecting the same order of magnitude if the underlying physics is the same.

**Stage 2 — Diagnose, if Stage 0 was negative.**
Before assuming a capture layer is required, isolate whether the problem is the substrate or genuinely the analyte: run R6G on the same substrate batch used in Stage 0 (confirms the electromagnetic enhancement itself is intact); if a power meter is accessible, confirm true laser power; if SEM/AFM access can be arranged, image the actual silver morphology and gap distribution against the Section 3 target. Only if R6G is strong on the same batch and the LPS signal is still absent does this become a genuine chemistry problem rather than a fabrication or instrumentation one.

**Stage 3 — Add a capture layer ("other methods"), only if Stage 1's LOD is not good enough for the intended use, or Stage 2 confirms bare detection is genuinely insufficient.**
First choice: **polymyxin B** (cheap, Lipid-A-specific, real literature precedent) over generic chitosan/cysteamine. Re-run the Section 5 protocol with this layer in place.

**Stage 4 — Substrate re-engineering, only if Stage 3 still underperforms.**
(a) Implement Kochylas et al.'s strip-and-regrow cycle on the existing MACE line to improve hotspot uniformity — a process refinement, not a new architecture. (b) Only after (a), consider the citrate-AgNP/wet-etched-Si route (the in-house IEEE-poster architecture) as a genuinely different candidate substrate — but note this requires either confirming 532 nm excitation is available on some accessible instrument, or accepting that results will be read out at 785 nm and may not reproduce that poster's reported range for resonance reasons. This should be a deliberate, stated decision, not a default substitution.

**Stage 5 — Antibody replication, as the rigorous benchmark match.**
Reproduce Rusciano's anti-Lipid-A frequency-shift assay directly (Section 4.3), since this is the one route in this whole plan with a same-serotype published LOD/LOQ to match against directly, not just approximately.

**Stage 6 — Advanced/optional: PCA / ML classification.**
Only after a working, quantified, reproducible detection method exists. Use the full-range spectra already being collected (Section 5.2) to test whether O111:B4's fingerprint is distinguishable from other LPS or LTA — following Yang et al. (2022) and the 2025 broad-affinity-polymer study. This is where the "detect O111:B4 specifically" claim would actually get earned, not assumed.

---

## 7. Challenges

**Fabrication and instrumentation gaps common to the whole project, inherited here:**
- HF handling risk at every fabrication step (standard PPE protocol applies without exception).
- Silver oxidation / undocumented shelf life — use freshly fabricated substrates until a stability study exists.
- Substrate reproducibility (RSD) has never been formally quantified for this project's own fabrication line.
- No SEM/AFM/EDS/UV-Vis characterisation exists yet for the actual fabricated substrate, so the Section 3 gap-size target cannot currently be confirmed as met — a real diagnostic blind spot if Stage 0 comes back negative.
- True laser power at the sample has never been measured in mW.

**Challenges specific to LPS:**
- **Lot-to-lot potency variation.** Sigma's own documentation for phenol-extracted (rather than chromatographically purified) LPS notes this can be significant — record the lot/CoA for this exact bottle before starting, since quantitative comparisons across future re-orders will need it.
- **Aggregation state.** Working above the CMC risks excluding LPS from the target 1–5 nm hotspot gaps regardless of substrate quality (Section 3) — the exact CMC for this specific reagent lot is not currently confirmed and should be treated as an open item, not assumed from general LPS literature values.
- **O-antigen shielding.** Because L2630 is smooth (S-type) LPS, the intact O-antigen may sterically block access to the core diols (relevant only if/when boronic-acid capture is explored) and to Lipid A itself (relevant to any cationic or antibody capture layer) — a plausible, testable reason a capture-chemistry stage could underperform even if the chemistry is fundamentally sound.
- **Residual protein.** ≤3% protein impurity (Lowry-TCA) is low but not zero, and protein amide bands can fall near the 1650 cm⁻¹ region sometimes used in antibody-based readouts — worth a protein-free blank check if that region is relied upon quantitatively.
- **GHS06 / Acute Tox. 2 (H300) classification.** Handle at the small analytical quantities this plan specifies, under the institution's approved SOP and SDS, with appropriate PPE — this is a real hazard classification, not a formality.
- **Wavelength mismatch with some literature.** Our instrument is 785 nm-only; results should not be expected to numerically match studies run at 532 nm (including the in-house IEEE poster) even where the underlying chemistry is the same, because plasmon resonance and resonance-Raman contributions differ by excitation wavelength.

---

## 8. Expected results and success criteria

| Stage | Expected result if the underlying hypothesis is correct | Minimum bar for "success" |
|---|---|---|
| Stage 0 (bare detection) | A 2850–2950 cm⁻¹ band appears, growing with LPS concentration, absent on bare-Si and blank controls | Signal distinguishable from blank at ≥3 of the tested concentrations, reproducible across ≥5 spots |
| Stage 1 (quantification) | A monotonic dose–response over at least 2 decades of concentration; LOD in the same order of magnitude as Rusciano's 3 ng/mL bare-substrate figure | A calculated LOD and LOQ with a stated confidence method (SNR-based), plus a reproducibility (%RSD) figure — both currently absent for every biomarker in this project |
| Stage 3 (capture layer, if reached) | Lower LOD and/or improved selectivity relative to Stage 1, closing toward Rusciano's antibody-based 12 ng/mL / 41 ng/mL LOD/LOQ | Measurable improvement over the bare-substrate baseline, not just a different number |
| Stage 5 (antibody replication, if reached) | LOD/LOQ in the same range as Rusciano et al. (12 / 41 ng/mL), since the reagent, organism, and serotype are matched | A same-serotype, directly comparable published benchmark met or approached — a genuinely strong, citable result for this project regardless of what precedes it |
| Stage 6 (ML, if reached) | O111:B4's spectral fingerprint separable from other LPS/LTA by PCA or a simple classifier | Not required for a first publication; a differentiator for a stronger one |

**Overall assessment:** LPS is the most tractable of the project's three biomarkers for exactly the reasons this design leans on — it is amphiphilic and multiply anionic (unlike NAM), it has a direct, same-serotype published benchmark to compare against (unlike LTA, where no quantitative SERS LOD exists in the literature at all), and the existing substrate and wafer stock already match a high-performing published fabrication recipe without modification. The realistic, defensible target for a first result is Stage 0/1 — bare-substrate detection and quantification on the substrate already in hand — with Stages 3–6 as a genuine, literature-grounded path to a stronger sensor rather than a required starting point.
