# Monthly Progress Report

## SERS Substrate Reproducibility Trials and Completion of the N-Acetylmuramic Acid Raman–DFT Study

**Reporting Period:** July 2026

**Student:** Sukesh P · Department of Electrical Engineering, IIT Jodhpur

---

## 1. Introduction

Work during this period followed two parallel tracks. The first was an attempt to
reproduce the silver-coated silicon SERS substrate fabricated in June, using
Rhodamine 6G (R6G) at several concentrations as the standard probe molecule. The
second was completion of the experimental and computational Raman study of
N-acetylmuramic acid (NAM), which has now reached full manuscript stage.

The substrate reproduction trials did not succeed. The fabricated substrates
became contaminated and did not give usable R6G enhancement. The fabrication was
repeated and a second set of measurements was collected; processing and analysis
of that data is in progress. The NAM study, by contrast, is essentially complete
and ready for submission pending a small number of documentation items.

---

## 2. SERS Substrate Fabrication — Reproducibility Trials

### 2.1 Work carried out

The June fabrication procedure was repeated: chemical etching of n-type silicon
using HF with AgNO₃, producing simultaneous silver nanoparticle deposition and
formation of a porous nanostructured surface.

The fabricated substrates were tested with Rhodamine 6G at several different
concentrations in order to establish the working detection range and to confirm
that the June enhancement could be reproduced.

### 2.2 Outcome

The trials were not successful. The substrates showed evidence of contamination,
and the characteristic R6G Raman bands could not be recovered with the signal
quality obtained in June. The enhancement was neither reproducible across
substrates nor consistent between concentrations.

Possible contributing factors identified so far:

- contamination introduced during etching, rinsing or drying
- variation in silver deposition time or solution freshness between batches
- storage or handling of the substrates between fabrication and measurement
- residue from the R6G solutions themselves at higher concentrations

### 2.3 Repeat measurements

Fabrication and measurement were repeated and a second dataset has been
collected. Spectral processing and plotting of this dataset are currently in
progress, using the same preprocessing pipeline established earlier (ALS baseline
correction, Savitzky–Golay smoothing, normalisation). Results will be reported
once the analysis is complete.

**Figure 1.** *Substrate fabrication workflow and representative R6G spectra from
the repeat trials.* (to be added once plotting is complete)

### 2.4 Planned corrective actions

- Prepare fresh HF/AgNO₃ solution for each fabrication batch
- Introduce a documented cleaning and rinsing protocol between steps
- Record a blank substrate spectrum immediately after fabrication, before R6G
  application, to identify contamination at the point it occurs
- Reduce the number of variables per batch so that any failure can be traced
- Measure substrates immediately after fabrication rather than after storage

---

## 3. N-Acetylmuramic Acid Raman–DFT Study — Completed

This study is now complete and written up as a full manuscript.

### 3.1 Experimental dataset

A total of **227 Raman spectra** of NAM powder were acquired at 785 nm using the
i-Raman Plus system with a 20× objective, organised as follows:

| Dataset | Spectra | Purpose |
|---|---|---|
| Acquisition-parameter survey | 98 | 5 integration times × 16 laser powers |
| Replicate sets (9 sets) | 104 | fixed conditions, fresh spot per measurement |
| Photostability series | 10 | same spot, consecutive scans |
| Laser-damage series | 10 | conditions causing sample degradation |
| Substrate blanks | 5 | empty glass slide |

A reference Raman spectrum was constructed from **22 independent measurements on
fresh sample**, with a mean pairwise correlation of 0.986 between contributing
spectra.

### 3.2 Photostability and laser-damage threshold

A working envelope for the material under 785 nm excitation was established:

| Condition | Outcome |
|---|---|
| ≤80% power, ≤25 s | stable |
| 70% power, 30 s and 60 s | stable |
| 90% power, 30 s | stable over 10 consecutive scans |
| **90% power, 60 s** | **sample destroyed** |

At the damaging condition the strongest Raman band at 930 cm⁻¹ decays from 0.44
to 0.23 in normalised intensity over five consecutive scans. This threshold is
reported in the manuscript, as carbohydrate powders are generally assumed to
tolerate near-infrared excitation without limit.

### 3.3 Computational work

DFT calculations were completed in **Gaussian 16** at the
**B3LYP-D3BJ/6-311++G(d,p)** level with tight optimisation, ultrafine integration
grid and Grimme D3BJ dispersion correction. The optimisation converged to a
stationary point with **111 normal modes and no imaginary frequencies**,
confirming a true energy minimum.

Harmonic frequencies were scaled (0.980 below 1800 cm⁻¹, 0.967 above), converted
to Raman intensities using the Placzek expression at 785 nm, and broadened with
Lorentzian line shapes for comparison with experiment.

### 3.4 Results

| Quantity | Value |
|---|---|
| Reproducible bands identified (400–1800 cm⁻¹) | **41** (32 high confidence, 9 tentative) |
| Bands matched to calculated modes | **30** |
| Mean absolute deviation | **9.3 cm⁻¹** |
| Root-mean-square deviation | **10.3 cm⁻¹** |
| Correlation coefficient | **0.9996** |

Two vibrational assignments were obtained that could not have been reached from
the experimental spectrum alone:

**The 872 cm⁻¹ band** is one of the strongest features of the spectrum and would
conventionally be grouped with ring-breathing modes on frequency alone.
Normal-mode decomposition shows it is dominated by hydroxymethyl hydrogen motion
(45.9% of the mass-weighted displacement from a single hydrogen), with only 5.0%
pyranose ring character. It is therefore assigned to hydroxymethyl wagging.

**The 730 cm⁻¹ region** is a long-standing open question in bacterial SERS: this
band is one of the strongest features of bacterial spectra and is widely used for
discrimination, but its molecular origin is disputed. Our calculation places a
mode of appreciable Raman activity at 731 cm⁻¹, which would appear to support a
peptidoglycan origin. Decomposition shows otherwise — 47.9% of the displacement
belongs to the carboxylic acid hydroxyl proton, with only **0.5%** ring
character. Since that proton is absent in intact peptidoglycan, where the muramic
acid carboxyl is amide-linked to the peptide stem, this mode cannot contribute to
bacterial spectra. This constitutes direct evidence against attributing the
bacterial 730 cm⁻¹ band to muramic acid.

**Figure 2.** *Reference Raman spectrum of NAM powder (mean of 22 independent
measurements, ± 1 SD).*

**Figure 3.** *Photostability and laser-damage threshold.*

**Figure 4.** *Experimental versus DFT-simulated Raman spectrum with residuals.*

### 3.5 Manuscript status

A complete manuscript has been prepared:

- 14 pages, seven figures, one main table of 41 assigned bands
- Supplementary material with optimised coordinates and all 111 calculated modes
- Formatted for **Spectrochimica Acta Part A** (Elsevier); alternative target
  **Vibrational Spectroscopy**, where the most closely related recent paper
  (Ma et al., 2024) was published
- LaTeX and Word versions prepared, both compiling without error

All data, calculations, figures and the analysis pipeline have been organised
into a single archive with a documented processing protocol and an executable
analysis notebook, so that every reported number is reproducible from the raw
files.

### 3.6 Remaining items before submission

None of these affect the scientific content:

- reagent lot number
- laser power at the sample in mW (to be measured with a power meter)
- instrument spectral resolution from the specification sheet
- three glass blank spectra recorded at the measurement conditions
- co-author details and acknowledgements
- expansion of the reference list from 14 to approximately 30–45

---

## 4. Summary of Work Completed in July

- Repeated the Ag/Si SERS substrate fabrication by chemical etching and tested it
  with Rhodamine 6G at several concentrations
- Identified substrate contamination as the reason for failure; documented likely
  causes and corrective actions
- Repeated the fabrication and collected a second dataset, currently under
  analysis
- Completed the full experimental Raman study of N-acetylmuramic acid: 227
  spectra, reference spectrum from 22 independent replicates
- Established a photostability and laser-damage threshold for NAM powder
- Completed dispersion-corrected DFT calculations in Gaussian 16 and matched 30
  observed bands to calculated normal modes (MAE 9.3 cm⁻¹, r = 0.9996)
- Obtained two new vibrational assignments, one of which addresses an open
  question in the bacterial SERS literature
- Prepared a complete manuscript with supplementary material, ready for
  submission pending documentation items

---

## 5. Planned Work for August

1. Complete processing and plotting of the repeat SERS substrate dataset
2. Re-fabricate substrates using the revised cleaning protocol, with a blank
   spectrum recorded after each fabrication step to isolate the contamination
   source
3. Re-establish reproducible R6G enhancement before proceeding to NAM detection
   on the substrate
4. Collect the remaining documentation items and submit the NAM manuscript
5. Optionally extend the DFT work to the α anomer and to N-acetylglucosamine, to
   support discrimination between the two peptidoglycan sugars

---

*Prepared July 2026*
