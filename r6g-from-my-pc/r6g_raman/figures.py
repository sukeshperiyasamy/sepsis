"""Shared matplotlib style and multi-format (png/pdf/svg @600dpi) saving
helper so every figure in the notebook is produced the same reproducible
way."""
from __future__ import annotations

import os
import matplotlib.pyplot as plt

PUB_RCPARAMS = {
    "figure.dpi": 150,
    "savefig.dpi": 600,
    "font.size": 11,
    "font.family": "sans-serif",
    "axes.linewidth": 1.0,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "legend.frameon": False,
    "svg.fonttype": "none",
}


def apply_style():
    plt.rcParams.update(PUB_RCPARAMS)


def save_all_formats(fig, out_dir: str, name: str):
    os.makedirs(out_dir, exist_ok=True)
    paths = {}
    for ext in ("png", "pdf", "svg"):
        path = os.path.join(out_dir, f"{name}.{ext}")
        fig.savefig(path, dpi=600 if ext == "png" else None, bbox_inches="tight")
        paths[ext] = path
    return paths
