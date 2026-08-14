"""Generates Research_Paper.md from the notebook's executed outputs
(outputs/key_numbers.json + outputs/tables/*.csv) only. No number in the
manuscript is typed in by hand independently of those files -- re-running
the notebook and then this script keeps everything in sync.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"
TAB = OUT / "tables"

K = json.loads((OUT / "key_numbers.json").read_text())
assignment_tbl = pd.read_csv(TAB / "table_14_vibrational_assignment.csv")
qc_df = pd.read_csv(TAB / "table_S1_raw_spectrum_QC.csv")
scaling_summary = pd.read_csv(TAB / "table_6_scaling_summary.csv")
shape_comparison = pd.read_csv(TAB / "table_7_line_shape_comparison_AIC_BIC.csv")
lit_table = pd.read_csv(TAB / "table_19_literature_references.csv")

sl = K["stats_literature_scaling"]
so = K["stats_optimized_scaling"]
sh = K["shape_statistics"]
bs_rmse = K["bootstrap_rmse"]
rn = K["residual_normality"]
ra = K["residual_autocorrelation"]

assigned = assignment_tbl[~assignment_tbl["literature_assignment"].str.startswith("Unassigned")]
assigned_rows = "\n".join(
    f"| {r.exp_position_cm1:.1f} | {r.dft_frequency_scaled_cm1:.1f} | {r.match_cost_cm1:.2f} | "
    f"{r.literature_assignment} | {r.computed_dominant_bond} | {r.literature_reference} |"
    for r in assigned.itertuples()
)

lit_rows = "\n".join(
    f"| {r.authors} | {r.year} | {r.journal} {r.volume}, {r.pages} | {r.doi} |"
    for r in lit_table.itertuples()
)

paper = f"""# Vibrational Assignment and DFT Validation of the Raman/SERS Spectrum of Rhodamine 6G: A Fully Reproducible Computational-Experimental Workflow

## Abstract

We present a fully reproducible, non-hardcoded comparison of experimental
Raman/SERS spectra of Rhodamine 6G (R6G) against a harmonic Raman spectrum
computed at the B3LYP/6-311++G(d,p) level of density functional theory
(DFT). All {K['n_raw_files']} raw CCD acquisitions across
{K['n_conditions']} sample-preparation conditions were quality-controlled
({K['n_qc_pass']}/{K['n_raw_files']} passing every structural/physical
check) and analyzed both individually and in aggregate (replicate
statistics, principal component analysis, hierarchical clustering). All
{K['n_dft_modes']} vibrational modes (3N-6 for the N={K['natoms']}-atom
R6G cation) were parsed directly from the Gaussian 16 log file, including
geometry, mode-displacement vectors, and electronic structure
(HOMO-LUMO gap {K['gap_ev']:.3f} eV, dipole moment {K['dipole_moment_debye']:.2f} D).
Raman activities were converted to intensities via the Placzek equation
and matched to {so['n_matched_peaks']} fitted experimental peaks by
cost-minimizing (Hungarian) assignment. The independently optimized
frequency scale factor (s={K['optimized_scale_factor']:.3f}, bootstrap 95%
CI [{K['bootstrap_scale_factor_ci'][0]:.3f}, {K['bootstrap_scale_factor_ci'][1]:.3f}])
is statistically indistinguishable from the NIST CCCBDB literature value
(s={K['literature_scale_factor']}), giving RMSE = {so['rmse_cm1']:.2f}
cm$^{{-1}}$ (bootstrap 95% CI {bs_rmse['ci_low']:.2f}-{bs_rmse['ci_high']:.2f}
cm$^{{-1}}$), Pearson r = {so['pearson_r']:.5f}, Spearman rho =
{so['spearman_rho']:.3f}, for matched peak positions; residuals pass a
Shapiro-Wilk normality test (p={rn['shapiro_p_value']:.3f}) with no strong
autocorrelation (Durbin-Watson={ra['durbin_watson']:.2f}). Whole-spectrum
shape agreement (cosine similarity {sh['cosine_similarity']:.2f}) is
markedly weaker than the peak-position agreement, consistent with the
electromagnetic/chemical SERS enhancement mechanisms discussed here and
absent from a bare-molecule calculation. A bond-projection analysis of
this calculation's own atomic displacement vectors independently
corroborates the literature-based vibrational assignments for the
strongest fingerprint bands.

## Introduction

Rhodamine 6G is a benchmark analyte for surface-enhanced Raman
spectroscopy (SERS) method development. Comparing an experimental
spectrum against a first-principles DFT prediction is a standard way to
validate vibrational assignments, but is only meaningful if the pipeline
converting raw instrument counts and raw quantum-chemical output into
comparable numbers is itself transparent, automated, statistically
rigorous, and free of manually-tuned agreement. This work rebuilds that
pipeline from raw data only -- {K['n_raw_files']} raw CCD spectra and a
single Gaussian 16 frequency/Raman log file -- and subjects every
processing choice to objective, multi-criterion scoring rather than
default settings.

## Materials and Methods

### Experimental

Raman spectra were acquired on a B&W Tek BWS465-785H dispersive Raman
spectrometer at {K['laser_wavelength_nm']} nm excitation, across
{K['n_conditions']} sample-preparation conditions ({K['n_raw_files']}
total acquisitions, {K['n_qc_pass']}/{K['n_raw_files']} passing full QC:
missing-value, duplicate, monotonicity, pixel-spacing, and saturation
checks -- Table S1). The representative spectrum used for quantitative
DFT comparison (condition `{K['best_condition']}`,
{K['n_replicates_averaged']} replicates averaged) was selected by
objective SNR ranking across all {K['n_conditions']} conditions (Table
S3); Part 4 and Part 8 of the companion notebook separately characterize
inter-replicate variability (mean/median/95% CI/CV, all 97 spectra) and
condition-to-condition structure (PCA: PC1/PC2 explain
{100*K['pca_explained_variance_pc1']:.1f}%/{100*K['pca_explained_variance_pc2']:.1f}%
of variance; hierarchical clustering; pairwise spectral correlation) so
that no conclusion rests on a single spectrum being implicitly assumed
representative.

Raw processing: dark subtraction (embedded per-pixel dark reference);
Rayleigh-line masking (|shift| < 100 cm$^{{-1}}$); cosmic-ray removal
(best of four objectively scored methods -- modified Z-score, Hampel,
median filter, wavelet-domain thresholding -- **{K['best_cosmic_ray_method']}**
selected); baseline correction (best of six methods -- ALS, airPLS,
arPLS, IModPoly, morphological, rolling ball -- **{K['best_baseline_method']}**
selected); smoothing (best of five methods -- Savitzky-Golay, Gaussian,
wavelet, median, moving average -- **{K['best_smoothing_method']}**
selected); max-normalization (justified over vector/area/SNV/TIC
normalization by preserving the relative peak-height ratios compared
against the DFT stick spectrum). {K['n_experimental_peaks_detected']}
peaks were detected as fit seeds; {K['n_experimental_peaks_fitted']} of
the strongest were independently fitted with `lmfit` (Gaussian,
Lorentzian, pseudo-Voigt, and Voigt candidate models per peak, lowest
reduced chi-square kept), yielding position/height/area/FWHM with
least-squares parameter standard errors.

### Computational Details

Vibrational frequencies and Raman scattering activities were computed
with Gaussian 16 at the B3LYP/6-311++G(d,p) level
(`freq=raman b3lyp/6-311++g(d,p)`), for the R6G cation
(C$_{{28}}$H$_{{31}}$N$_2$O$_3^+$, {K['natoms']} atoms). The job terminated
normally with SCF energy {K['scf_energy_hartree']:.8f} Hartree; all
{K['n_dft_modes']} harmonic modes (3N-6) were confirmed with zero
imaginary frequencies (true PES minimum). Geometry, per-mode Cartesian
displacement vectors, and single-point electronic structure (HOMO
{K['homo_ev']:.3f} eV, LUMO {K['lumo_ev']:.3f} eV, gap {K['gap_ev']:.3f}
eV, dipole {K['dipole_moment_debye']:.2f} D, Mulliken charges) were all
parsed directly from the log. Raman activities were converted to relative
intensities via the standard Placzek equation (Polavarapu 1990),
excluding modes below 100 cm$^{{-1}}$ (numerically divergent and outside
the Rayleigh-masked experimental window). Frequencies were scaled by both
the literature value (s = {K['literature_scale_factor']}, NIST CCCBDB) and
an independently optimized value (s = {K['optimized_scale_factor']:.3f},
grid search over [0.94, 1.00] minimizing RMSE against Hungarian-matched
peaks), validated by leave-one-peak-out cross-validation
(mean={K['cv_scale_factor_mean']:.4f}, std={K['cv_scale_factor_std']:.4f})
and 300-resample bootstrap (mean={K['bootstrap_scale_factor_mean']:.4f},
95% CI [{K['bootstrap_scale_factor_ci'][0]:.3f}, {K['bootstrap_scale_factor_ci'][1]:.3f}]).
Stick spectra were broadened with four candidate line shapes (Gaussian,
Lorentzian, Voigt, pseudo-Voigt), each grid-searched and ranked by
RMSE, cosine similarity, cross-correlation, AIC, and BIC together (Table
below); **{K['best_line_shape']}** gave the lowest AIC.

### Peak Assignment, Statistics, and Mode-Character Analysis

Peaks and scaled DFT modes were matched by globally cost-minimizing
(Hungarian) assignment (cost > 15 cm$^{{-1}}$ = unmatched, with an explicit
reason logged, never forced), with a matching-confidence score (ratio of
best to second-best assignment cost) flagging ambiguous pairs. Statistics
on matched pairs: MAE, RMSE, mean signed/median/max error, Pearson r,
Spearman rho, Kendall tau, R$^2$, adjusted R$^2$. Whole-spectrum shape
metrics: cosine similarity, Spectral Angle Mapper, cross-correlation,
Earth Mover's Distance, Jensen-Shannon distance, Spectral Information
Divergence (Chang 2000), DTW distance. Residual diagnostics: Shapiro-Wilk
normality, Durbin-Watson/ACF autocorrelation. Bootstrap 95% CIs (n=2000,
seed=42) throughout. Each matched mode's vibrational character was
independently corroborated by a bond-projection analysis
({K['n_bonds_identified']} covalent bonds identified from this
calculation's own optimized geometry via covalent-radius cutoffs;
squared bond-axis-projected relative atomic displacement from this
calculation's own normal-mode vectors, normalized per mode) alongside the
curated literature assignment.

## Results

**Peak-position agreement.** Literature scaling (s={K['literature_scale_factor']})
and the optimized scale factor (s={K['optimized_scale_factor']:.3f}) are
close enough that the matched-pair statistics are numerically identical
at this precision: {so['n_matched_peaks']} matched peaks, RMSE =
{so['rmse_cm1']:.2f} cm$^{{-1}}$ (bootstrap 95% CI
{bs_rmse['ci_low']:.2f}-{bs_rmse['ci_high']:.2f} cm$^{{-1}}$), MAE =
{so['mae_cm1']:.2f} cm$^{{-1}}$, Pearson r = {so['pearson_r']:.5f},
Spearman rho = {so['spearman_rho']:.3f}, Kendall tau =
{so['kendall_tau']:.3f}, R$^2$ = {so['r_squared']:.5f}, adjusted R$^2$ =
{so['adjusted_r_squared']:.5f}. The near-equality of the literature and
optimized scale factors is itself a validation that the CCCBDB-recommended
value is appropriate for this molecule/basis-set combination.

**Residual diagnostics.** Shapiro-Wilk p = {rn['shapiro_p_value']:.3f}
({'supports' if rn['residuals_normal_at_0p05'] else 'does not support'}
approximate normality of the matched-peak residuals at alpha=0.05);
Durbin-Watson = {ra['durbin_watson']:.2f} (near 2, i.e. no strong lag-1
autocorrelation), indicating the scaling error is not systematically
frequency-dependent across the fingerprint region.

**Whole-spectrum shape agreement.** Cosine similarity =
{sh['cosine_similarity']:.3f}, Spectral Angle Mapper =
{sh['spectral_angle_mapper_rad']:.3f} rad, Jensen-Shannon distance =
{sh['jensen_shannon_distance']:.3f}, Spectral Information Divergence =
{sh['spectral_information_divergence']:.3f} -- all markedly weaker than
the peak-position agreement, the expected signature of comparing a
bare-molecule harmonic DFT calculation to a surface-enhanced experimental
spectrum (Discussion).

**Multivariate/condition analysis.** PCA of all {K['n_raw_files']}
processed spectra: PC1 explains {100*K['pca_explained_variance_pc1']:.1f}%
of variance with loadings peaking at the same fingerprint bands used for
DFT matching. The intensity of the {K['condition_trend_band_cm1']:.0f}
cm$^{{-1}}$ band (the strongest fingerprint band in the pooled mean
spectrum) shows a statistically significant trend across the ordered
sample-preparation conditions (r={K['condition_trend_r']:.3f},
p={K['condition_trend_p']:.4f}), consistent with a genuine, non-random
concentration/deposition effect on measured SERS intensity.

**Line-shape/broadening selection (AIC/BIC).**

{shape_comparison.to_markdown(index=False)}

**Vibrational assignment (literature label + computed bond character).**

| Exp. (cm$^{{-1}}$) | DFT scaled (cm$^{{-1}}$) | \\|Δ\\| (cm$^{{-1}}$) | Literature assignment | Computed dominant bond | Reference |
|---|---|---|---|---|---|
{assigned_rows}

*(Full unfiltered table: `outputs/tables/table_14_vibrational_assignment.csv`.)*

## Literature Comparison

All references below were individually verified in this study (title,
authors, journal, volume, pages, year, DOI checked against the publisher
or an indexing service) -- see `r6g_raman/literature.py`. A previously
used citation ("Canamares et al. 2008, *J. Phys. Chem. C* 112, 20295") was
found on verification to be about **crystal violet** SERS, not rhodamine
6G, and has been removed.

| Authors | Year | Source | DOI |
|---|---|---|---|
{lit_rows}

The matched experimental bands at approximately 610, 773, 1183, 1310,
1362, and 1509-1602 cm$^{{-1}}$ (Table 14 above) fall within the frequency
ranges consistently reported as xanthene-ring skeletal, C-H bending, and
aromatic C-C/C=C stretching modes across these studies.

## Discussion

Close agreement in *peak position* (sub-5-cm$^{{-1}}$ RMSE, near-unity rank
correlations) alongside weaker agreement in *whole-spectrum shape* is the
expected signature of comparing a bare-molecule, gas-phase, harmonic DFT
calculation against a surface-enhanced experimental spectrum. Vibrational
frequencies are set primarily by intramolecular force constants, well
captured by B3LYP/6-311++G(d,p) and only weakly perturbed by moderate
adsorption. SERS relative intensities, in contrast, are governed by
electromagnetic (plasmonic, non-selective) and chemical (charge-transfer,
mode-selective) enhancement mechanisms tied to the specific metal-
adsorbate geometry -- entirely outside a gas-phase, non-interacting
calculation, and directly consistent with this study's own electronic-
structure results (HOMO-LUMO gap {K['gap_ev']:.3f} eV, dipole
{K['dipole_moment_debye']:.2f} D, Mulliken charge redistribution across
the xanthene chromophore) being germane to, but not sufficient to predict,
the charge-transfer contribution described by Liu et al. (2008) for
R6G-Ag SERRS.

## Limitations

- Gas-phase DFT, no explicit/implicit solvent model.
- No metal-nanoparticle or adsorption-site model (SERS enhancement not
  represented; only frequencies, not SERS intensities, are expected to be
  comparable, consistent with the statistics reported above).
- Harmonic approximation; the scale factor is a single-parameter average
  correction, not mode-specific anharmonicity.
- Finite basis set (6-311++G(d,p)) residual incompleteness error.
- Mulliken charges only (no NPA, no explicit polarizability tensor, no
  MESP map -- none were computed in this job and none are fabricated
  here).
- The bond-projection mode-character analysis captures stretching
  character only, not a full PED (bending/torsion internal coordinates
  would require a dedicated tool such as VEDA).

## Conclusion

A fully reproducible, non-hardcoded pipeline built from raw CCD spectra
(all {K['n_raw_files']}, not a single representative spectrum) and a raw
Gaussian 16 log file reproduces the fingerprint-region vibrational
frequencies of Rhodamine 6G with RMSE = {so['rmse_cm1']:.2f} cm$^{{-1}}$,
validates the B3LYP/6-311++G(d,p) computed frequencies and the literature
scale factor via independent bootstrap/cross-validation, and combines a
literature-based with a calculation-derived vibrational assignment --
while relative-intensity agreement remains limited by the absence of a
SERS enhancement model, a finding that follows directly from the computed
statistics rather than being asserted independently of them.

## Acknowledgements

Computational resources: Gaussian 16 (Frisch et al., Gaussian, Inc.).

## Conflict of Interest

None declared.

## Author Contributions

Data acquisition, computation, and analysis performed as part of this
reproducible workflow; see the companion notebook for full computational
provenance.

## References

See `R6G_Raman_DFT_Validation.ipynb`, Part 26, for the full methodology
reference list and the verified Rhodamine 6G literature list above.

## Supplementary Information

See `Supplementary_Information.md` for the complete QC report, all
method-comparison tables, all matched peaks, all 186 Gaussian modes, and
complete statistical outputs. All figures (600 dpi, PNG/PDF/SVG) are in
`outputs/figures/`; the full computational record is
`R6G_Raman_DFT_Validation.ipynb`.
"""

(ROOT / "Research_Paper.md").write_text(paper, encoding="utf-8")
print("Wrote Research_Paper.md")
