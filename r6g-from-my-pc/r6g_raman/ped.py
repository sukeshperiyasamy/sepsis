"""Bond-projection 'pseudo-PED' (potential energy distribution) analysis.

A rigorous PED requires a full normal-coordinate transformation (e.g. with
VEDA), which is out of scope here. This module instead computes a
simpler, still genuinely calculation-derived, bond-stretch character for
every vibrational mode directly from this job's own atomic coordinates and
Cartesian displacement vectors:

For every covalent bond (i,j) (determined from interatomic distance vs.
the sum of covalent radii, with a 1.3x tolerance -- standard practice,
e.g. Pyykko & Atsumi 2009 covalent radii), the bond-stretch contribution
of a mode is the squared component of the atoms' *relative* displacement
projected onto the bond axis:

    c_ij = [(d_i - d_j) . u_ij]^2

normalized so that sum_ij c_ij = 1 over all bonds for that mode (a
stretch-only "% contribution", analogous to a real PED stretch term but
without the bending/torsion internal coordinates a full PED would also
include -- so this systematically only ever reports stretching character,
which is stated explicitly wherever it is used).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Pyykko & Atsumi (2009) single-bond covalent radii, Angstrom
COVALENT_RADII = {1: 0.32, 6: 0.75, 7: 0.71, 8: 0.63}
BOND_TOLERANCE = 1.3


def build_bond_list(geometry: pd.DataFrame) -> pd.DataFrame:
    coords = geometry[["x", "y", "z"]].to_numpy()
    z = geometry["atomic_number"].to_numpy()
    n = len(geometry)
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(coords[i] - coords[j])
            r_cov = COVALENT_RADII.get(z[i], 0.75) + COVALENT_RADII.get(z[j], 0.75)
            if dist <= BOND_TOLERANCE * r_cov:
                rows.append(dict(atom_i=i, atom_j=j, distance_A=float(dist)))
    return pd.DataFrame(rows)


_ELEMENT_SYMBOL = {1: "H", 6: "C", 7: "N", 8: "O"}


def mode_bond_character(displacement: np.ndarray, geometry: pd.DataFrame,
                         bonds: pd.DataFrame, top_n: int = 3) -> list[dict]:
    coords = geometry[["x", "y", "z"]].to_numpy()
    z = geometry["atomic_number"].to_numpy()
    contributions = np.empty(len(bonds))
    for k, (i, j) in enumerate(zip(bonds["atom_i"], bonds["atom_j"])):
        bond_vec = coords[j] - coords[i]
        u = bond_vec / np.linalg.norm(bond_vec)
        rel_disp = displacement[i] - displacement[j]
        contributions[k] = np.dot(rel_disp, u) ** 2
    total = contributions.sum()
    fractions = contributions / total if total > 0 else contributions

    order = np.argsort(fractions)[::-1][:top_n]
    out = []
    for k in order:
        i, j = int(bonds["atom_i"].iloc[k]), int(bonds["atom_j"].iloc[k])
        out.append(dict(
            atom_i=i + 1, atom_j=j + 1,  # 1-indexed, matches Gaussian's own atom numbering
            element_i=_ELEMENT_SYMBOL.get(z[i], "?"), element_j=_ELEMENT_SYMBOL.get(z[j], "?"),
            stretch_fraction=float(fractions[k]),
        ))
    return out


def describe_dominant_bond(character: list[dict]) -> str:
    if not character or character[0]["stretch_fraction"] < 0.05:
        return "delocalized / non-stretch-dominated (bending, torsion, or ring-breathing character)"
    top = character[0]
    return (f"{top['element_i']}{top['atom_i']}-{top['element_j']}{top['atom_j']} stretch "
            f"({100*top['stretch_fraction']:.0f}% of stretch character)")


def build_ped_table(mode_indices: list[int], displacements: dict[int, np.ndarray],
                     geometry: pd.DataFrame, bonds: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    rows = []
    for m in mode_indices:
        character = mode_bond_character(displacements[m], geometry, bonds, top_n=top_n)
        rows.append(dict(
            mode_index=m,
            dominant_bond_description=describe_dominant_bond(character),
            top_bonds=character,
        ))
    return pd.DataFrame(rows)
