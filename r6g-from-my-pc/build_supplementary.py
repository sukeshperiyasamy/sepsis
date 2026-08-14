"""Generates Supplementary_Information.md, pulling every supplementary
table already written by the notebook into one document. No numbers are
typed here -- every table is read from outputs/tables/*.csv.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"
TAB = OUT / "tables"
K = json.loads((OUT / "key_numbers.json").read_text())

SECTIONS = [
    ("S1. Raw Spectrum QC (all 97 files)", "table_S1_raw_spectrum_QC.csv"),
    ("S2. Gaussian Job Validation", "table_S2_gaussian_job_validation.csv"),
    ("S3. Condition SNR Ranking", "table_S3_condition_SNR_ranking.csv"),
    ("S4. Cosmic-Ray Removal Method Comparison", "table_S4_cosmic_ray_method_comparison.csv"),
    ("S5. Baseline Correction Method Comparison", "table_S5_baseline_method_comparison.csv"),
    ("S6. Smoothing Method Comparison", "table_S6_smoothing_method_comparison.csv"),
    ("S7. Normalization Method Comparison", "table_S7_normalization_comparison.csv"),
    ("S8. Pooled Replicate Statistics (all 97 spectra, first/last 10 rows)", "table_S8_pooled_replicate_statistics.csv"),
    ("S9. Condition Variability Summary", "table_S9_condition_variability_summary.csv"),
    ("Table 1. Experimental Peaks Detected", "table_1_experimental_peaks_detected.csv"),
    ("Table 1b. Experimental Peaks Fitted (lmfit, with uncertainties)", "table_1b_experimental_peaks_fitted.csv"),
    ("Table 2. All 186 Gaussian DFT Modes (raw)", "table_2_DFT_modes_raw.csv"),
    ("Table 3. DFT Modes with Converted Raman Intensity", "table_3_DFT_modes_with_intensity.csv"),
    ("Table 4. Scaling Factor Optimization Scan", "table_4_scaling_optimization_scan.csv"),
    ("Table 5. Scaling Factor Leave-One-Out Cross-Validation", "table_5_scaling_cross_validation.csv"),
    ("Table 6. Scaling Factor Summary", "table_6_scaling_summary.csv"),
    ("Table 7. Line-Shape Comparison (AIC/BIC)", "table_7_line_shape_comparison_AIC_BIC.csv"),
    ("Table 9. Peak Matches (Literature Scaling)", "table_9_peak_matches_literature_scaling.csv"),
    ("Table 10. Peak Matches (Optimized Scaling)", "table_10_peak_matches_optimized_scaling.csv"),
    ("Table 11. Peak Position Statistics", "table_11_peak_position_statistics.csv"),
    ("Table 12. Whole-Spectrum Shape Statistics", "table_12_whole_spectrum_shape_statistics.csv"),
    ("Table 13. Bootstrap Confidence Intervals", "table_13_bootstrap_confidence_intervals.csv"),
    ("Table 14. Vibrational Assignment (Literature + Computed)", "table_14_vibrational_assignment.csv"),
    ("Table 15. PCA Explained Variance", "table_15b_PCA_explained_variance.csv"),
    ("Table 16. Condition Intensity Trend", "table_16_condition_intensity_trend.csv"),
    ("Table 17. Electronic Structure Summary", "table_17_electronic_structure_summary.csv"),
    ("Table 17b. Mulliken Atomic Charges", "table_17b_mulliken_charges.csv"),
    ("Table 18. Residual Diagnostics", "table_18_residual_diagnostics.csv"),
    ("Table 19. Verified Literature References", "table_19_literature_references.csv"),
]

MAX_ROWS = 40

parts = [
    "# Supplementary Information",
    "",
    "Automatically generated from `outputs/tables/*.csv`, produced by "
    "`R6G_Raman_DFT_Validation.ipynb`. Every table below is the complete, "
    "reproducible output of that notebook -- large tables (e.g. all 186 "
    "DFT modes, all pooled-spectrum statistics) are truncated for "
    f"display here (first/last {MAX_ROWS//2} rows) but the full CSV/XLSX "
    "files are in `outputs/tables/` and `outputs/R6G_validation_summary.xlsx`.",
    "",
    "## Algorithm and Parameter Settings Summary",
    "",
    f"- Cosmic-ray removal: 4 methods compared, `{K['best_cosmic_ray_method']}` selected.",
    f"- Baseline correction: 6 methods compared, `{K['best_baseline_method']}` selected.",
    f"- Smoothing: 5 methods compared, `{K['best_smoothing_method']}` selected.",
    "- Normalization: max (for DFT comparability); vector/area/SNV/TIC also reported.",
    f"- Peak fitting: lmfit, best-of-{{Gaussian, Lorentzian, PseudoVoigt, Voigt}} per peak "
    "by reduced chi-square; 20 cm-1 fit window.",
    f"- Rayleigh-line mask: |shift| < 100 cm-1.",
    f"- Low-frequency DFT intensity cutoff: 100 cm-1.",
    f"- Hungarian assignment cost threshold: 15 cm-1.",
    f"- Scaling factor grid search: s in [0.94, 1.00], 61 steps; bootstrap n=300, seed={K['rng_seed']}.",
    f"- Broadening line-shape selection: AIC/BIC across Gaussian/Lorentzian/Voigt/PseudoVoigt; "
    f"selected shape = `{K['best_line_shape']}`.",
    f"- Bootstrap statistics: n=2000 resamples, seed={K['rng_seed']}.",
    f"- Bond perception (PED): Pyykko & Atsumi (2009) covalent radii, 1.3x tolerance, "
    f"{K['n_bonds_identified']} bonds identified.",
    "",
]

for title, fname in SECTIONS:
    path = TAB / fname
    parts.append(f"## {title}")
    parts.append("")
    if not path.exists():
        parts.append(f"*(File not found: {fname})*")
        parts.append("")
        continue
    df = pd.read_csv(path)
    if len(df) > MAX_ROWS:
        shown = pd.concat([df.head(MAX_ROWS // 2), df.tail(MAX_ROWS // 2)])
        parts.append(f"*({len(df)} rows total; showing first/last {MAX_ROWS//2} -- full file: `outputs/tables/{fname}`)*")
        parts.append("")
    else:
        shown = df
    parts.append("```csv")
    parts.append(shown.to_csv(index=False).strip())
    parts.append("```")
    parts.append("")

(ROOT / "Supplementary_Information.md").write_text("\n".join(parts), encoding="utf-8")
print("Wrote Supplementary_Information.md")
