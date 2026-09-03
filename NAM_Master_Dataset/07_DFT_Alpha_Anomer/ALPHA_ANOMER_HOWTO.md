# Running the α-Anomer Calculation

**The input file is ready: `NAM_alpha.gjf`.** You do not need to find a structure
or build anything — just submit it to Gaussian.

---

## 1. Why this is easy

The α and β anomers differ at **one** stereocentre: the anomeric carbon, C-1.
Everything else in the molecule — all four other stereocentres, the acetamido
group, the lactyl ether, the ring conformation — is identical.

So rather than downloading a new structure and re-optimising from scratch, I took
your **already-optimised β geometry** and exchanged the positions of the hydroxyl
and hydrogen on C-1.

Verified after the swap:

| Check | Result |
|---|---|
| Chirality at C-1 | Signed volume flipped +1.691 → −1.691 — **inverted** |
| C1–O bond length | 1.384 Å (unchanged) |
| C1–H bond length | 1.104 Å (unchanged) |
| O–H bond length | 0.963 Å |
| Closest atomic contact | 0.961 Å — no clashes |

See `alpha_vs_beta_structure.png` for the two structures side by side, with the
exchanged bonds highlighted.

Starting from the optimised β geometry means the α optimisation begins close to
its own minimum and should converge quickly.

---

## 1b. Alternative starting geometry — PubChem CID 6323218, VERIFIED

An independent α structure was taken from PubChem CID 6323218
(*alpha-Muramic acid, N-acetyl-*) and checked against the optimised β geometry.

Method: bonds assigned from covalent radii, atoms matched between the two
molecules by Morgan connectivity invariant (so the comparison does not depend on
atom ordering), then the signed volume computed at every stereocentre with
substituents ranked by that invariant.

| Stereocentre (by environment) | β | PubChem α | |
|---|---|---|---|
| 43a6d22e | S− | S− | same |
| 5ffc04c4 | R+ | R+ | same |
| 814ad126 | S− | S− | same |
| 9131cc04 | R+ | R+ | same |
| f70a8300 | R+ | R+ | same |
| **f86292b0 — anomeric C** | **S−** | **R+** | **inverted, as required** |

**All six stereocentres matched by environment; five are identical to β and only
the anomeric carbon is inverted.** The structure is a true anomer of the β
calculation, not a different diastereomer, and it agrees with the inverted-β
geometry in `NAM_alpha.gjf` at every centre.

Geometry sanity: C–C 1.505–1.538 Å, C–H 1.092–1.100 Å, C–O 1.224–1.433 Å,
O–H 0.972–0.981 Å, N–H 1.016 Å. No bond outside 0.85–1.8 Å, no close contacts.

Either starting geometry is therefore valid.

---

## 2. Files

| File | What |
|---|---|
| **`NAM_alpha.gjf`** | **Gaussian input — ready to submit** |
| `NAM_alpha.xyz` | Same coordinates, XYZ format, for viewing |
| `alpha_vs_beta_structure.png` | Visual comparison |

---

## 3. The settings

**Everything is already in `NAM_alpha.gjf`. If you submit the file as-is, you do
not need to set anything.** This section explains what those settings mean, and
gives the GaussView equivalents in case you prefer the GUI.

### The file, in full

```
%chk=NAM_alpha.chk
%nprocshared=16
%mem=48GB
# opt=(calcfc,tight) freq=raman b3lyp/6-311++g(d,p)
  empiricaldispersion=gd3bj int=ultrafine scf=(tight,xqc)

alpha-N-acetylmuramic acid  --  anomeric centre inverted from the optimised beta geometry

0 1
 [39 atoms]
                      ← blank line must be here
```

### What each keyword does

| Keyword | Meaning | Why |
|---|---|---|
| `opt=(calcfc,tight)` | Optimise geometry; compute force constants analytically at the first step; tight convergence | `calcfc` makes convergence far more reliable for a flexible sugar. `tight` is **required** before a frequency calculation |
| `freq=raman` | Harmonic frequencies **and Raman activities** | Without `raman` you get frequencies but no intensities, and the spectrum cannot be plotted |
| `b3lyp` | The functional | Same as β |
| `6-311++g(d,p)` | Basis set — triple-zeta, diffuse on all atoms, polarisation on all atoms | Diffuse functions matter for the carboxyl and hydroxyl groups |
| `empiricaldispersion=gd3bj` | Grimme D3 dispersion, Becke–Johnson damping | Intramolecular hydrogen bonding in the sugar |
| `int=ultrafine` | Dense integration grid | The G16 default, and needed for reliable low-frequency modes |
| `scf=(tight,xqc)` | Tight SCF; fall back to quadratic convergence if it stalls | `xqc` rescues the run instead of crashing it |
| `0 1` | Neutral, singlet | NAM is a closed-shell neutral molecule |

**Do not change any of these.** Using the identical level of theory is the entire
point — any difference between the α and β spectra must come from the molecule,
not from the method.

### ⚠ Do NOT add solvation

**Your β calculation was gas phase.** Verified directly from the log: the route
line contains no `scrf` keyword, and the only two mentions of SCRF anywhere in
25,000 lines are the auto-generated `SCRF=Check` in the frequency step, which
merely reads the checkpoint and finds nothing set.

If you add `scrf=(smd,solvent=water)` to the α job, the two calculations are no
longer comparable and the whole test is void — any difference in the 830 or
956 cm⁻¹ region could be solvation rather than anomerism, and there would be no
way to tell them apart.

The energies show how large the effect is:

| Calculation | First SCF energy (Hartree) |
|---|---|
| β, gas phase, PubChem starting geometry | −1087.54802 |
| α, **SMD water**, starting geometry | −1087.60679 |
| **Difference** | **−0.0588 Ha = −36.9 kcal/mol** |

Anomers differ in energy by roughly **1 kcal/mol**. A 37 kcal/mol gap is the
solvation free energy, not the anomeric effect. It would swamp the signal being
looked for.

**There is also a physical reason to stay in the gas phase:** the sample measured
was a **dry powder on a glass slide**, not an aqueous solution. Water (ε = 78) is
a poor model for a molecular crystal (ε ≈ 3–4). Gas phase is imperfect but it is
the closer model, and it is what the experimental comparison in the manuscript
already rests on.

*(If a "SMD / water" setting was carried over from an earlier description of this
project — an early draft did wrongly describe the β run as SMD-solvated before the
actual log was checked — that description was corrected. The completed β run is
gas phase.)*

### Settings you *may* need to change

| Line | Change it if | Note |
|---|---|---|
| `%nprocshared=16` | Your machine has fewer cores | Your β run used 16 and completed, so 16 is safe on the same machine |
| `%mem=48GB` | Your machine has less RAM | Leave several GB for the OS. Your β run used 48 GB successfully |
| `%chk=NAM_alpha.chk` | Running from GaussView on Windows | Give a **full path**, e.g. `%chk=C:\Users\COMPUTER\Downloads\NAM\NAM_alpha.chk`, so you can find the file afterwards |

### GaussView equivalents

If you build the job through **Calculate → Gaussian Calculation Setup**:

| Tab | Field | Set to |
|---|---|---|
| Job Type | Job type | **Opt+Freq** |
| Job Type | Optimize to a | Minimum |
| Job Type | Calculate force constants | **Once** (= `calcfc`) |
| Job Type | Compute Raman | **Yes** (= `freq=raman`) |
| Method | Method | Ground State · DFT · **Restricted** · B3LYP |
| Method | Basis set | **6-311++G (d,p)** |
| Method | Charge / Spin | **0 / Singlet** |
| Method | Empirical Dispersion | **GD3BJ** |
| Title | — | anything |
| Link 0 | Memory / Processors | 48GB / 16 |
| General | Use Integral Grid | **UltraFine** |
| SCF | — | Tight, and tick quadratic convergence |
| Solvation | — | **None** — gas phase |

`opt=tight` is not exposed as a checkbox in older GaussView dialogs. If you cannot
find it, type it into the **Additional Keywords** box, or simply edit the route
line by hand — which is why submitting the supplied `.gjf` directly is easier.

### One difference from the β input, deliberate

Your β file used `geom=connectivity` with an explicit bond list. The α file omits
it, so Gaussian works out connectivity from interatomic distances instead.
**This does not change the result** — connectivity only affects the initial
internal-coordinate setup, not the DFT energy or the frequencies. Do not add it
back; the bond list from the β file would no longer be correct after the swap.

---

## 4. Running it

**From the command line:**

```
g16 NAM_alpha.gjf
```

which writes `NAM_alpha.log`.

**On Windows with GaussView:** open `NAM_alpha.gjf`, confirm the structure looks
sensible, then Calculate → Gaussian Calculation Setup → **Submit**. Everything is
already filled in from the file.

**On HPC:** submit through your cluster's scheduler with the same resources.

### Expected runtime — correcting what I told you earlier

I said "about an hour". **That was wrong** — I read only the last timing block in
your β log. The β job actually ran in two stages:

| Stage | Elapsed |
|---|---|
| Optimisation | 3 h 42 min |
| Frequencies | 58 min |
| **Total** | **≈ 4 h 41 min** on 16 cores |

The α optimisation starts from a geometry that is already close to its own
minimum, so it should be somewhat faster than the β optimisation — but the
frequency stage will take the same ~1 hour regardless. **Budget 3–5 hours.**
Start it before you leave for the day rather than expecting it over lunch.

---

## 5. Checking it worked

Before doing anything else, three checks on the log file:

**Normal termination**
```
grep "Normal termination" NAM_alpha.log
```
Should appear at least once.

**Stationary point found**
```
grep "Stationary point found" NAM_alpha.log
```

**No imaginary frequencies** — the critical one
```
grep "Frequencies --" NAM_alpha.log | head
```
Every value must be positive. A negative number means the optimisation landed on
a saddle point rather than a minimum, and the frequencies are not usable.

If an imaginary frequency does appear, the usual fix is to displace the structure
slightly along that mode and re-optimise. Send me the log and I will tell you
what to do.

### Warnings you can safely ignore

**`**** Warning!!: The largest alpha MO coefficient is 0.148D+03`**

Harmless here — and this is not a guess. **Your β log contains the identical
warning twice**, at 0.14406×10³ and 0.15048×10³, and that calculation terminated
normally with a stationary point and zero imaginary frequencies.

The warning is characteristic of diffuse functions (the `++` in the basis set) on
a molecule with many oxygen atoms close together: the diffuse shells overlap
heavily and the basis approaches linear dependence. Gaussian flags it; for this
system it is routine.

### Progress checks while it runs

| What to look for | Meaning |
|---|---|
| `SCF Done: E(RB3LYP) = ...` | One SCF converged. This happens once per optimisation step — **not** the end of the job |
| `Step number  N` | Optimisation step N. **β needed 39 steps** |
| `Optimization completed.` / `-- Stationary point found.` | Optimisation finished; frequencies start next |
| `Frequencies --` and `Raman Activ --` | The frequency stage, the part actually needed |
| `Normal termination` | Done |

Counting `Step number` against β's 39 is the best progress gauge you have.

---

## 6. Send me the log

Once it finishes, send `NAM_alpha.log` and I will:

- parse the frequencies, Raman activities and displacement vectors
- apply the same scaling (0.980 / 0.967) and Lorentzian broadening
- compute a Boltzmann-weighted α + β combined spectrum
- re-match against the 41 experimental bands
- test specifically whether **830 and 956 cm⁻¹** — currently unmatched — are
  reproduced by the α component
- regenerate the figures, Table 1 and all statistics

That is roughly an hour of my time and no instrument time at all.

---

## 7. What the outcome would mean

**If α reproduces 830 and/or 956 cm⁻¹** — that is a real result. It would confirm
that the anomeric mixture explains the unmatched bands, turn two open questions
into assignments, and let the paper state that the sample composition is
spectroscopically visible. Worth an additional figure.

**If it does not** — also useful. The unmatched bands would then be attributable
to crystal packing rather than anomeric composition, which is a cleaner
explanation than the current "one of two possibilities". The paper gets more
definite either way.

**Either way it strengthens the paper**, and it is currently the last substantial
gap in the vibrational assignment.

---

## 8. One caveat

The relative proportion of α and β in your actual sample is unknown — the
supplier does not state it, and reducing sugars mutarotate. For the combined
spectrum I would default to an equal-weight average and say so explicitly, or
present the two calculated spectra separately alongside experiment rather than
combining them.

Presenting them separately is arguably more honest and avoids inventing a
composition. I would decide once we see whether α actually reproduces the
missing bands.
