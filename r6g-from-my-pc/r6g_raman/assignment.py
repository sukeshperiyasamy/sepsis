"""Literature vibrational-mode assignment lookup for Rhodamine 6G.

This module supplies the *literature* half of the assignment; the
*computed* half (bond-projection pseudo-PED from this calculation's own
normal-mode displacement vectors) is in `ped.py`. Every reference cited
below was individually verified in this session (title/authors/journal/
volume/pages/year/DOI checked against the publisher) -- see
`literature.py`. A previously used "Canamares et al. 2008, J. Phys. Chem.
C" citation was removed after verification showed that paper is about
crystal violet SERS, not rhodamine 6G.

This table is explicitly a literature comparison, not a result derived
from the present calculation.
"""
from __future__ import annotations

import pandas as pd

from .literature import REFERENCES

_REF_BY_KEY = {r["key"]: r for r in REFERENCES}


def _cite(key: str) -> str:
    r = _REF_BY_KEY[key]
    return f"{r['authors'].split(';')[0].strip()} {r['year']} (DOI {r['doi']})"


LITERATURE_ASSIGNMENTS = [
    # (low_cm1, high_cm1, assignment, reference_key)
    (600, 630, "Xanthene ring C-C-C in-plane bending", "Hildebrandt1984"),
    (760, 790, "Xanthene ring C-H out-of-plane bending", "Watanabe2005"),
    (1150, 1220, "C-H in-plane bending / C-N stretching (xanthene)", "Jensen2006"),
    (1250, 1340, "Aromatic C-C stretching + N-H in-plane bending", "Watanabe2005"),
    (1340, 1400, "Xanthene ring C-C stretching", "Hildebrandt1984"),
    (1480, 1540, "Aromatic C-C stretching (xanthene)", "Jensen2006"),
    (1540, 1600, "Phenyl/xanthene ring C-C stretching", "Liu2008"),
    (1600, 1680, "Xanthene C=C / C=O stretching", "Watanabe2005"),
    (2800, 3100, "Aliphatic/aromatic C-H stretching", "Hildebrandt1984"),
]


def assign_literature_label(freq_cm1: float) -> tuple[str, str]:
    for lo, hi, label, ref_key in LITERATURE_ASSIGNMENTS:
        if lo <= freq_cm1 <= hi:
            return label, _cite(ref_key)
    return "Unassigned (outside curated literature ranges)", "-"


def build_assignment_table(matched: pd.DataFrame) -> pd.DataFrame:
    out = matched.copy()
    labels, refs = zip(*[assign_literature_label(f) for f in out["exp_position_cm1"]])
    out["literature_assignment"] = labels
    out["literature_reference"] = refs
    return out
