"""Experimental <-> DFT peak assignment via cost-minimizing (Hungarian)
matching, and scaling-factor optimization built on top of it.

Nearest-neighbour matching is deliberately NOT used: instead a full cost
matrix (frequency distance, optionally combined with a rank-order
intensity term) is built between every experimental peak and every
DFT mode above an activity threshold, and `scipy.optimize.linear_sum_assignment`
finds the globally cost-minimal one-to-one assignment. Matches whose cost
exceeds `max_cost_cm1` are discarded as genuinely unmatched (never forced).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

from . import dft_intensity


def build_cost_matrix(exp_positions: np.ndarray, dft_positions: np.ndarray,
                       exp_intensity_rank: np.ndarray | None = None,
                       dft_intensity_rank: np.ndarray | None = None,
                       intensity_weight: float = 0.0) -> np.ndarray:
    freq_cost = np.abs(exp_positions[:, None] - dft_positions[None, :])
    if intensity_weight > 0 and exp_intensity_rank is not None and dft_intensity_rank is not None:
        rank_cost = np.abs(exp_intensity_rank[:, None] - dft_intensity_rank[None, :])
        return freq_cost + intensity_weight * rank_cost
    return freq_cost


def hungarian_match(exp_peaks: pd.DataFrame, dft_modes: pd.DataFrame,
                     dft_freq_col: str = "frequency_scaled_cm1",
                     max_cost_cm1: float = 15.0,
                     intensity_weight: float = 0.0) -> pd.DataFrame:
    exp_pos = exp_peaks["position_cm1"].to_numpy()
    dft_pos = dft_modes[dft_freq_col].to_numpy()

    exp_rank = exp_peaks["intensity"].rank().to_numpy() if intensity_weight > 0 else None
    dft_rank = dft_modes["raman_intensity_norm"].rank().to_numpy() if intensity_weight > 0 else None

    cost = build_cost_matrix(exp_pos, dft_pos, exp_rank, dft_rank, intensity_weight)
    row_idx, col_idx = linear_sum_assignment(cost)

    rows = []
    for r, c in zip(row_idx, col_idx):
        matched_cost = cost[r, c]
        row_costs = np.sort(cost[r, :])
        second_best = row_costs[1] if len(row_costs) > 1 else np.inf
        confidence = float(1.0 - matched_cost / second_best) if np.isfinite(second_best) and second_best > 0 else np.nan
        is_matched = bool(matched_cost <= max_cost_cm1)
        if is_matched:
            reason = "matched"
        else:
            reason = (f"nearest DFT mode is {matched_cost:.1f} cm-1 away, "
                      f"exceeding the {max_cost_cm1:.0f} cm-1 assignment threshold "
                      "(no calculated mode close enough in frequency)")
        rows.append(dict(
            exp_index=int(exp_peaks.index[r]),
            exp_position_cm1=float(exp_pos[r]),
            exp_intensity=float(exp_peaks["intensity"].iloc[r]),
            dft_mode_index=int(dft_modes["mode_index"].iloc[c]),
            dft_frequency_scaled_cm1=float(dft_pos[c]),
            dft_frequency_unscaled_cm1=float(dft_modes["frequency_cm1"].iloc[c]),
            dft_raman_intensity_norm=float(dft_modes["raman_intensity_norm"].iloc[c]),
            match_cost_cm1=float(matched_cost),
            matching_confidence=confidence,
            matched=is_matched,
            unmatched_reason=("" if is_matched else reason),
        ))
    df = pd.DataFrame(rows).sort_values("exp_position_cm1").reset_index(drop=True)
    return df


def optimize_scaling_factor(exp_peaks: pd.DataFrame, dft_modes_raw: pd.DataFrame,
                             scale_range: tuple[float, float] = (0.94, 1.00),
                             n_steps: int = 61, max_cost_cm1: float = 15.0) -> pd.DataFrame:
    scales = np.linspace(scale_range[0], scale_range[1], n_steps)
    rows = []
    for s in scales:
        scaled = dft_intensity.apply_scaling(dft_modes_raw, s)
        matches = hungarian_match(exp_peaks, scaled, max_cost_cm1=max_cost_cm1)
        matched = matches[matches["matched"]]
        if len(matched) == 0:
            rows.append(dict(scale_factor=s, n_matched=0, rmse_cm1=np.nan, mae_cm1=np.nan))
            continue
        err = matched["exp_position_cm1"] - matched["dft_frequency_scaled_cm1"]
        rows.append(dict(
            scale_factor=float(s),
            n_matched=int(len(matched)),
            rmse_cm1=float(np.sqrt(np.mean(err ** 2))),
            mae_cm1=float(np.mean(np.abs(err))),
        ))
    return pd.DataFrame(rows)


def cross_validate_scaling(exp_peaks: pd.DataFrame, dft_modes_raw: pd.DataFrame,
                            scale_range: tuple[float, float] = (0.94, 1.00),
                            n_steps: int = 61, max_cost_cm1: float = 15.0) -> pd.DataFrame:
    """Leave-one-peak-out cross-validation of the RMSE-optimal scale factor."""
    scales = np.linspace(scale_range[0], scale_range[1], n_steps)
    rows = []
    for i in exp_peaks.index:
        held_out = exp_peaks.drop(index=i)
        best_scale, best_rmse = np.nan, np.inf
        for s in scales:
            scaled = dft_intensity.apply_scaling(dft_modes_raw, s)
            matches = hungarian_match(held_out, scaled, max_cost_cm1=max_cost_cm1)
            matched = matches[matches["matched"]]
            if len(matched) == 0:
                continue
            err = matched["exp_position_cm1"] - matched["dft_frequency_scaled_cm1"]
            rmse = float(np.sqrt(np.mean(err ** 2)))
            if rmse < best_rmse:
                best_rmse, best_scale = rmse, s
        rows.append(dict(held_out_peak_cm1=float(exp_peaks.loc[i, "position_cm1"]),
                          best_scale_factor=best_scale, rmse_cm1=best_rmse))
    return pd.DataFrame(rows)
