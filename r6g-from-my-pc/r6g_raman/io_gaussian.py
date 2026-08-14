"""Parser for Gaussian 16 frequency/Raman (.LOG) output.

Reads harmonic vibrational modes directly from the fixed-width
``Frequencies --`` / ``Raman Activ --`` / ``Depolar (P/U) --`` blocks that
Gaussian writes for a ``freq=raman`` job. No values are hardcoded; every
number returned here is parsed from the log file text.

Reference: Gaussian 16 User's Reference, "Frequency Job", and
Frisch, M. J. et al. Gaussian 16 Output Description (frequency/Raman section).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
import pandas as pd

_FREQ_RE = re.compile(r"^\s*Frequencies\s*--\s*(.*)$")
_REDMASS_RE = re.compile(r"^\s*Red\. masses\s*--\s*(.*)$")
_FRCCONST_RE = re.compile(r"^\s*Frc consts\s*--\s*(.*)$")
_IRINTEN_RE = re.compile(r"^\s*IR Inten\s*--\s*(.*)$")
_RAMANACT_RE = re.compile(r"^\s*Raman Activ\s*--\s*(.*)$")
_DEPOL_P_RE = re.compile(r"^\s*Depolar \(P\)\s*--\s*(.*)$")
_DEPOL_U_RE = re.compile(r"^\s*Depolar \(U\)\s*--\s*(.*)$")


def _floats(line: str) -> list[float]:
    return [float(x) for x in line.split()]


@dataclass
class GaussianJobMeta:
    natoms: int
    route: str
    method: str
    basis: str
    scf_energy_hartree: float
    normal_termination: bool
    n_imaginary_low_freq: int
    low_frequencies: list[float]


def parse_job_metadata(log_path: str) -> GaussianJobMeta:
    """Extract job-level metadata used to validate the calculation."""
    with open(log_path, "r", errors="replace") as fh:
        lines = fh.readlines()

    route = ""
    natoms = None
    scf_energy = None
    normal_term = False
    low_freqs: list[float] = []

    route_re = re.compile(r"^\s*#\s*(.*freq.*)$", re.IGNORECASE)
    natoms_re = re.compile(r"NAtoms=\s*(\d+)")
    scf_re = re.compile(r"SCF Done:\s*E\([^)]*\)\s*=\s*(-?\d+\.\d+)")
    low_re = re.compile(r"^\s*Low frequencies\s*---\s*(.*)$")

    for line in lines:
        m = route_re.match(line)
        if m and not route:
            route = m.group(1).strip()
        m = natoms_re.search(line)
        if m and natoms is None:
            natoms = int(m.group(1))
        m = scf_re.search(line)
        if m:
            scf_energy = float(m.group(1))  # keep last (final geometry) SCF energy
        m = low_re.match(line)
        if m:
            low_freqs.extend(_floats(m.group(1)))
        if "Normal termination of Gaussian" in line:
            normal_term = True

    if not route:
        raise ValueError(f"No frequency route section found in {log_path}")
    if natoms is None:
        raise ValueError(f"NAtoms not found in {log_path}")
    if scf_energy is None:
        raise ValueError(f"SCF Done energy not found in {log_path}")

    route_lower = route.lower()
    method_match = re.search(r"(b3lyp|m062x|pbe0|wb97xd|hf|mp2)", route_lower)
    basis_match = re.search(r"\b(6-311\+\+g\(d,p\)|6-31g\(d\)|[a-z0-9\-\+\(\),*]+g\([a-z,]*\))", route_lower)
    method = method_match.group(1) if method_match else "unknown"
    basis = basis_match.group(1) if basis_match else "unknown"

    # first 6 "low frequencies" are the translational/rotational near-zero
    # modes; anything beyond those that is negative indicates a real
    # imaginary vibrational frequency (transition state / non-minimum).
    n_imaginary = sum(1 for f in low_freqs[6:] if f < 0)

    return GaussianJobMeta(
        natoms=natoms,
        route=route,
        method=method,
        basis=basis,
        scf_energy_hartree=scf_energy,
        normal_termination=normal_term,
        n_imaginary_low_freq=n_imaginary,
        low_frequencies=low_freqs,
    )


def parse_vibrational_modes(log_path: str) -> pd.DataFrame:
    """Parse every vibrational mode's frequency, Raman activity and
    depolarization ratios from the log file.

    Returns
    -------
    DataFrame with columns:
        mode_index, frequency_cm1, reduced_mass_amu, force_constant_mdyne_A,
        ir_intensity_km_mol, raman_activity_A4_amu, depolar_ratio_p,
        depolar_ratio_u
    """
    with open(log_path, "r", errors="replace") as fh:
        lines = fh.readlines()

    records = []
    mode_counter = 0
    i = 0
    n = len(lines)
    while i < n:
        m = _FREQ_RE.match(lines[i])
        if m:
            freqs = _floats(m.group(1))
            k = len(freqs)
            # Fixed Gaussian ordering for a freq=raman job:
            # Frequencies, Red. masses, Frc consts, IR Inten, Raman Activ,
            # Depolar (P), Depolar (U)
            redmass = _floats(_REDMASS_RE.match(lines[i + 1]).group(1))
            frcconst = _floats(_FRCCONST_RE.match(lines[i + 2]).group(1))
            irinten = _floats(_IRINTEN_RE.match(lines[i + 3]).group(1))
            ramanact = _floats(_RAMANACT_RE.match(lines[i + 4]).group(1))
            depol_p = _floats(_DEPOL_P_RE.match(lines[i + 5]).group(1))
            depol_u = _floats(_DEPOL_U_RE.match(lines[i + 6]).group(1))

            for j in range(k):
                mode_counter += 1
                records.append(
                    dict(
                        mode_index=mode_counter,
                        frequency_cm1=freqs[j],
                        reduced_mass_amu=redmass[j],
                        force_constant_mdyne_A=frcconst[j],
                        ir_intensity_km_mol=irinten[j],
                        raman_activity_A4_amu=ramanact[j],
                        depolar_ratio_p=depol_p[j],
                        depolar_ratio_u=depol_u[j],
                    )
                )
            i += 7
        else:
            i += 1

    df = pd.DataFrame.from_records(records)
    if df.empty:
        raise ValueError(f"No vibrational modes parsed from {log_path}")
    return df


def parse_geometry(log_path: str) -> pd.DataFrame:
    """Parse the first 'Standard orientation' block (the geometry used for
    the frequency calculation, since the job used geom=allcheck to read
    the optimized structure from the checkpoint file).

    Returns DataFrame: atom_index, atomic_number, x, y, z (Angstrom).
    """
    with open(log_path, "r", errors="replace") as fh:
        lines = fh.readlines()

    start = None
    for i, line in enumerate(lines):
        if "Standard orientation:" in line:
            start = i
            break
    if start is None:
        raise ValueError(f"No 'Standard orientation' block found in {log_path}")

    # header is 5 lines (title, 2 dashed rules, column labels, dashed rule),
    # then one row per atom until the closing dashed rule.
    row_start = start + 5
    records = []
    for line in lines[row_start:]:
        if line.strip().startswith("---"):
            break
        parts = line.split()
        if len(parts) != 6:
            break
        center, atomic_num, atomic_type, x, y, z = parts
        records.append(dict(
            atom_index=int(center), atomic_number=int(atomic_num),
            x=float(x), y=float(y), z=float(z),
        ))
    df = pd.DataFrame.from_records(records)
    if df.empty:
        raise ValueError(f"Failed to parse atom coordinates from {log_path}")
    return df


_ATOM_ROW_RE = re.compile(r"^\s*\d+\s+\d+(\s+-?\d+\.\d+){9}\s*$")


def parse_mode_displacements(log_path: str, natoms: int) -> dict[int, "np.ndarray"]:
    """Parse the per-atom Cartesian displacement vectors for every mode.

    Returns {mode_index: ndarray of shape (natoms, 3)} (dimensionless
    mass-weighted-normal-mode displacement components, as printed by
    Gaussian directly beneath each Frequencies/Raman Activ block).
    """
    with open(log_path, "r", errors="replace") as fh:
        lines = fh.readlines()

    displacements: dict[int, np.ndarray] = {}
    mode_counter = 0
    i = 0
    n = len(lines)
    while i < n:
        m = _FREQ_RE.match(lines[i])
        if m:
            k = len(_floats(m.group(1)))
            atom_header_idx = i + 7
            if atom_header_idx < n and lines[atom_header_idx].strip().startswith("Atom"):
                data_start = atom_header_idx + 1
                mats = [np.zeros((natoms, 3)) for _ in range(k)]
                for row in range(natoms):
                    parts = lines[data_start + row].split()
                    vals = [float(v) for v in parts[2:]]
                    for j in range(k):
                        mats[j][row, :] = vals[3 * j:3 * j + 3]
                for j in range(k):
                    mode_counter += 1
                    displacements[mode_counter] = mats[j]
                i = data_start + natoms
            else:
                i += 7
        else:
            i += 1
    return displacements


def parse_electronic_structure(log_path: str) -> dict:
    """Parse HOMO/LUMO orbital eigenvalues, dipole moment, and Mulliken
    atomic charges from the single-point electronic structure printed for
    the (checkpoint-read) geometry."""
    with open(log_path, "r", errors="replace") as fh:
        lines = fh.readlines()

    occ_vals: list[float] = []
    virt_vals: list[float] = []
    dipole = None
    mulliken_rows = []
    in_mulliken = False

    occ_re = re.compile(r"Alpha\s+occ\.\s+eigenvalues\s+--\s+(.*)")
    virt_re = re.compile(r"Alpha\s+virt\.\s+eigenvalues\s+--\s+(.*)")
    dipole_re = re.compile(
        r"X=\s*(-?\d+\.\d+)\s+Y=\s*(-?\d+\.\d+)\s+Z=\s*(-?\d+\.\d+)\s+Tot=\s*(-?\d+\.\d+)")

    for idx, line in enumerate(lines):
        m = occ_re.search(line)
        if m:
            occ_vals.extend(_floats(m.group(1)))
            continue
        m = virt_re.search(line)
        if m:
            virt_vals.extend(_floats(m.group(1)))
            continue
        if line.strip() == "Mulliken charges:":
            in_mulliken = True
            continue
        if in_mulliken:
            parts = line.split()
            if len(parts) == 3 and parts[0].isdigit():
                mulliken_rows.append(dict(atom_index=int(parts[0]), element=parts[1], charge=float(parts[2])))
            elif line.strip().startswith("Sum of Mulliken"):
                in_mulliken = False
        m = dipole_re.search(line)
        if m and dipole is None and idx > 0 and "Dipole moment" in lines[idx - 1]:
            dipole = dict(x=float(m.group(1)), y=float(m.group(2)), z=float(m.group(3)), total_debye=float(m.group(4)))

    if not occ_vals or not virt_vals:
        raise ValueError(f"HOMO/LUMO eigenvalues not found in {log_path}")

    homo_hartree = occ_vals[-1]
    lumo_hartree = virt_vals[0]
    hartree_to_ev = 27.211386245988

    return dict(
        homo_hartree=homo_hartree,
        lumo_hartree=lumo_hartree,
        gap_hartree=lumo_hartree - homo_hartree,
        homo_ev=homo_hartree * hartree_to_ev,
        lumo_ev=lumo_hartree * hartree_to_ev,
        gap_ev=(lumo_hartree - homo_hartree) * hartree_to_ev,
        dipole_moment_debye=dipole,
        mulliken_charges=pd.DataFrame.from_records(mulliken_rows),
    )


def validate_modes(df: pd.DataFrame, meta: GaussianJobMeta) -> dict:
    """Cross-check the number of parsed modes against 3N-6 (or 3N-5)."""
    expected_nonlinear = 3 * meta.natoms - 6
    expected_linear = 3 * meta.natoms - 5
    n_modes = len(df)
    return dict(
        natoms=meta.natoms,
        n_modes_parsed=n_modes,
        expected_modes_nonlinear=expected_nonlinear,
        expected_modes_linear=expected_linear,
        matches_nonlinear=(n_modes == expected_nonlinear),
        normal_termination=meta.normal_termination,
        n_imaginary_frequencies=meta.n_imaginary_low_freq,
        is_true_minimum=(meta.n_imaginary_low_freq == 0),
    )
