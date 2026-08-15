# Engineering SERS substrates for N-acetylmuramic acid (NAM)

## Scope and evidence boundary

This is an in-session evidence synthesis, not a registered systematic review. The discovery search returned 80 candidate papers spanning direct sialic-acid analogues, bacterial-wall biomarkers, and silicon/porous-silicon SERS substrates. Direct literature on NAM itself was not identified in the retrieved set; the closest direct molecular evidence concerns N-acetylneuraminic acid (Neu5Ac), a different N-acetylated bacterial/host-associated sugar acid. Recommendations below therefore distinguish direct evidence from transfer-based inference.

## What makes NAM difficult relative to R6G

Rhodamine 6G is a strongly absorbing chromophore with large resonance-enhanced Raman cross-section under visible excitation, whereas NAM is a small, nonchromophoric, highly polar sugar acid. The practical consequence is that NAM requires both efficient electromagnetic enhancement and favorable surface localization; a substrate that performs well with R6G is not automatically optimized for NAM. This is an inference from the molecular contrast, not a direct head-to-head NAM/R6G study in the retrieved set.

The closest direct analogue demonstrates feasibility: Neu5Ac adsorbed on silver nanoparticles produced strongly enhanced Raman signals from a small aqueous amount, and the study explicitly combined Raman, SERS, and DFT to interpret adsorption [^1]. A later study detected Neu5Ac bands near 1002 and 1237 cm−1 down to 1 mg/dL on citrate-covered Ag, but also reported frequency shifts and substantial intensity changes upon adsorption, complicating identification in mixed overlayers [^2]. For NAM, this means that peak assignment should be based on spectra of NAM on the actual Ag/Si surface rather than on the neat solid spectrum alone.

## Chemical design implications

NAM presents hydroxyl, carboxylate, ether/hemiacetal, and acetamide functionality. These groups can support electrostatic, hydrogen-bonding, and coordination interactions, but the molecule lacks the strong aromatic π-system that often gives dyes high SERS response. The most defensible design objective is therefore to increase the probability that NAM occupies Ag hot spots without burying its diagnostic vibrational modes under a passivating layer or competing buffer ions.

The Neu5Ac studies support a mixed adsorption picture rather than a simple physisorption model: citrate-covered Ag changes both intensities and frequencies, and the authors interpret the spectra with citrate–Neu5Ac/Ag cluster calculations [^2]. For NAM, the transferable hypothesis is that Ag surface ligand identity and coverage will control both adsorption efficiency and spectral reproducibility. It should be tested by comparing citrate, minimally capped Ag, and deliberately introduced capture chemistries while monitoring Ag colloid stability and background.

## Substrate engineering: relevance to the existing Ag/Si platform

The strongest near-term route is to retain the HF-assisted silicon architecture and optimize Ag morphology, rather than immediately switching to a chemically unrelated platform. Silver/porous-silicon hybrids prepared by immersion plating in AgNO3 formed Ag on both the porous surface and nanopillars, creating a quasi-three-dimensional, high-area substrate; the report measured a model analyte at 10−9 M and attributed the improvement to increased adsorption area and three-dimensional structure [^3]. This directly supports comparing planar etched Si, porous Si, and nanowire/pillar Si under otherwise matched Ag deposition.

Silver-assisted electroless etching is especially compatible with the user's process. A silicon-nanowire study used this approach, characterized Ag-coated morphology by SEM, and found a process window for R6G optimization with a reported aqueous R6G detection limit of 10−8 M [^4]. That result validates the platform for a reporter dye, but it does not establish NAM performance; for NAM, morphology must be optimized using NAM response and spatial reproducibility as primary endpoints, with R6G retained only as a fabrication/QC control.

### Evidence-weighted comparison

- **Electroless deposition / galvanic displacement on etched Si:** lowest barrier to implementation and directly compatible with the current wafer; morphology can vary with local oxide removal, wafer doping, etch history, and Ag nucleation. Best first comparison for NAM.
- **Ag-decorated silicon nanowires or nanopillars:** increases accessible area and can create three-dimensional hot-spot networks; literature supports strong SERS model-analyte response, but deeper structures can worsen analyte transport and measurement heterogeneity. Best evaluated as a controlled morphology series, not assumed superior.
- **Porous Si/Ag hybrids:** provide high area and quasi-3D geometry; potentially useful for a small polar analyte, but pore wetting, capillary drying, and background adsorption become confounders [^3].
- **Evaporation or sputtering:** offers better control of thickness and coverage than wet deposition, but requires vacuum equipment and may produce a less conformal coating on high-aspect-ratio Si. Use as a reproducibility benchmark if available.
- **Colloidal chemical reduction / seed-mediated particles:** useful for decoupling particle size and shape from the Si scaffold; however, citrate or other capping agents compete with NAM and can alter adsorption, as shown for Neu5Ac [^2].
- **Lithographic arrays / nanosphere lithography:** strong control over geometry and spacing, but higher cost and lower flexibility for exploratory chemistry. Appropriate only after a morphology target has been identified.
- **Hydrothermal synthesis and black-Si/nanocone architectures:** potentially high area and broadband light coupling, but the retrieved evidence did not establish a NAM-specific advantage. Treat as later-stage alternatives rather than first-line recommendations.

The literature does not justify claiming a universal optimum Ag size, spacing, roughness, or coverage for NAM. These parameters are coupled: changing deposition time changes particle size, density, coalescence, accessible Si area, and hotspot distribution simultaneously. A defensible study should therefore report SEM/AFM distributions and relate them to NAM signal variance, not only report a single nominal particle diameter.

## Surface chemistry: what is justified for NAM

A bare or lightly capped Ag surface is the most direct starting point because it preserves access to Ag and avoids introducing a thick Raman background. The first chemical comparison should be a small, controlled set: unmodified Ag/Si; a sparse carboxylate- or amine-terminated layer; and a capture layer selected for NAM recognition. The Neu5Ac/citrate result makes passivating-agent identity a mechanistic variable, not a minor formulation detail [^2].

Thiol SAMs bind Ag strongly and can improve chemical organization, but dense SAMs may block NAM from the metal and add their own intense bands. Amine or silane chemistry on Si can improve wetting and electrostatic capture, but the charge state is pH-dependent and the silane layer must remain thin and spatially uniform. Polymers, MIPs, aptamers, and antibodies may improve selectivity, but they add distance from the metal, mass-transport constraints, and background. No retrieved paper directly establishes that any of these is optimal for NAM; they are hypothesis-generating options requiring controls for signal attenuation and nonspecific adsorption.

## Solution and sampling variables

NAM detection should be evaluated across pH because carboxylate charge, Ag surface charge, ligand protonation, and silane/amine charge all change together. Ionic strength can improve aggregation or destabilize colloids and can screen electrostatic attraction; phosphate, chloride, and sulfur-containing buffers are particularly important competitors for Ag and should not be treated as inert. These are mechanistic predictions that should be tested with buffer-only spectra and matched ionic-strength controls.

Drop-casting can concentrate NAM at the drying perimeter and create apparent hotspots unrelated to substrate-average performance. Compare dried-drop spectra with controlled incubation and mapping across the entire dried footprint. Report median, interquartile range, coefficient of variation, number of spatial points, and independent substrate batches. A substrate improvement should be defined as a gain in NAM signal at fixed laser dose together with lower between-spot and between-batch variance—not as a single maximum spectrum.

## Raman acquisition

The retrieved literature includes measurements at 532 and 785 nm for bacterial SERS and demonstrates that excitation wavelength changes which biochemical components dominate the spectrum [^5]. For NAM, 785 nm is a sensible starting point because it reduces fluorescence and photochemical stress, but visible wavelengths may provide greater Raman scattering and possibly stronger plasmon coupling. A fair comparison requires matched incident power at the sample, comparable acquisition dose, replicate spots, and explicit reporting of objective, integration time, accumulations, spot size, and preprocessing. The evidence does not support declaring 532, 633, or 785 nm universally best for NAM without a wavelength-controlled experiment on the same substrate.

## Related bacterial biomarkers

The bacterial SERS literature supports the broader premise that cell-wall and secreted biomolecules can be measured, but it also shows that spectra are mixtures rather than single-analyte readouts. LPS studies obtained distinct spectra from multiple endotoxin structures, identified lipid and saccharide-associated bands, and differentiated samples by principal-component analysis at 10 nmol/mL [^6]. This supports using LPS, peptidoglycan fragments, or related glycoconjugates as selectivity and matrix-challenge controls, not as substitutes for NAM validation.

Single-cell bacterial SERS studies have linked spectral features to biochemical state and drug sensitivity [^7]. Such work supports multivariate analysis for complex bacterial matrices, but it cannot establish that a particular band is NAM unless chemical identity is independently confirmed. LC–MS or chromatographic fractionation is therefore valuable for assigning candidate NAM-related peaks in bacterial extracts.

## Computational evidence

The direct Neu5Ac papers used DFT to interpret adsorption-induced shifts and intensity changes [^1][^2]. A NAM study should similarly compare isolated NAM, NAM–Ag clusters, and NAM with plausible surface ligands, and should report the functional, basis set, cluster model, dispersion treatment, and frequency scaling factor. Calculated modes should be treated as assignments with uncertainty, not as proof of adsorption geometry. Experimental spectra on Ag/Si at multiple pH values and with isotopic or orthogonal chemical confirmation would be stronger evidence than matching one calculated peak.

## Recommended roadmap from the current substrate

1. **Establish a morphology–signal baseline.** Use SEM, AFM, EDS, XRD, and, where useful, UV–Vis/reflectance to quantify Ag coverage, particle-size distribution, coalescence, roughness, crystallinity, and optical response. Record wafer lot, Si resistivity/doping, etch history, and Ag deposition batch.
2. **Separate dye QC from NAM performance.** Use R6G to verify that the fabrication process remains SERS-active, but rank substrates using NAM peak area or integrated spectral windows, limit of detection, blank response, and spatial/batch CV.
3. **Run a morphology comparison.** Compare at least the current surface with a lower-coverage, intermediate-coverage, and near-coalesced Ag condition, plus a porous/nanowire or nanopillar variant if fabrication is available. Keep analyte preparation and acquisition fixed.
4. **Test adsorption chemistry without overcoating.** Compare bare/lightly capped Ag with one thin charged or capture-oriented modification. Include ligand-only and no-Ag controls, and quantify whether the modification increases NAM signal enough to offset added Raman background and increased metal–molecule distance.
5. **Map solution effects.** Use a pH and ionic-strength matrix with buffer blanks. Avoid interpreting a higher signal as improved affinity until colloid/substrate morphology and Ag stability are shown unchanged.
6. **Validate specificity.** Test NAM against structurally related sugars, muramic-acid/peptidoglycan fragments, LPS/LTA or glycopeptide controls, and matrix components. Confirm candidate peaks with an orthogonal method where possible.
7. **Use statistics appropriate to substrates.** Treat substrate batch as a random effect; use independent batches, multiple positions per substrate, blank spectra, and prespecified spectral features. Report calibration uncertainty, recovery, selectivity, and robustness to drying position and acquisition wavelength.

## Research gaps and thesis-level opportunity

The central gap is not a lack of SERS substrates in general; it is the lack of a validated, reproducible NAM-specific substrate and spectral assignment workflow. The most defensible novelty is a controlled comparison of Ag morphology and surface ligand state on an etched-silicon scaffold, coupled to DFT/experimental peak assignment and batch-level statistics. The key conclusion is an inference: the current Ag/Si platform is a rational starting point because the fabrication is compatible with silicon and related Neu5Ac work shows that Ag adsorption can make an N-acetylated sugar acid measurable, but optimization must be driven by NAM itself rather than by R6G alone.


[^1]: Vinogradova et al., 2014. Surface‐enhanced Raman scattering of N‐acetylneuraminic acid on silver nanoparticle surface. Journal of Raman Spectroscopy.

[^2]: Hernández-Arteaga et al., 2017. Surface-Enhanced Raman Spectroscopy of Acetil-neuraminic Acid on Silver Nanoparticles: Role of the Passivating Agent on the Adsorption Efficiency and Amplification of the Raman Signal. Journal of Physical Chemistry C.

[^3]: Nguyen et al., 2021. Quasi-three-dimension Structured Surface-enhanced Raman Scattering Substrates Based on Silver Nanoparticles/ Porous Silicon Hybrid.

[^4]: Gebavi et al., 2017. Silicon Nanowires Substrates Fabrication for Ultra-Sensitive Surface Enhanced Raman Spectroscopy Sensors. Croatica Chemica Acta.

[^5]: Durovich et al., 2018. Molecular origin of surface-enhanced Raman spectra of E. coli suspensions excited at 532 and 785 nm using silver nanoparticle sols as sers substrates. Nanomedicine.

[^6]: Wu et al., 2021. Highly Sensitive Detection and Differentiation of Endotoxins Derived from Bacterial Pathogens by Surface-Enhanced Raman Scattering. Biosensors.

[^7]: Zyubin et al., 2025. Single-cell analysis of Mycobacterium tuberculosis with diverse drug resistance using surface-enhanced Raman spectroscopy (SERS). PeerJ.