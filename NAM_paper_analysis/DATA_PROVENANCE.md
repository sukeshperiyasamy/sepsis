# Data Provenance — Exactly What I Used

All paths relative to your `mtp` folder.

---

## USED — experimental Raman

**`20-04/sukesh NAM Raman data/`**

| Subfolder | Files read | Unique | Used |
|---|---|---|---|
| `5sec-power5-80 and 2set/` | 16 | 16 | yes |
| `10sec-power5-80-2set/` | 17 | 17 | yes |
| `15sec-power5-80andset2/` | 16 | 16 | yes |
| `20sec-power5-80and set2/` | 16 | 16 | yes |
| `25sec-power5-80 and set2/` | 16 | 16 | yes |
| `NAM-15secs and power15-75-2sets/` | 17 | 17 | yes |
| `data from pc raw powder/` (5 subfolders) | 80 | 0 | **no — byte-identical duplicates** |
| `data of Dry powder/` (5 subfolders) | 81 | 0 | **no — byte-identical duplicates** |
| `MB 1ugml/` | 2 | 2 | **no — methylene blue, not NAM** |

**261 CSV files read → 100 unique → 98 NAM spectra used.**

Of the 98, the **40 with SNR ≥ 100** were averaged into the reference spectrum.
All 98 were used for the acquisition-optimisation figure.

Duplicate detection was by MD5 hash of the intensity array, so "duplicate" here
means byte-identical data, not merely similar.

---

## USED — DFT

**`review meeting/namfinal laptop simulation/`**

- `CONFORMER3D_COMPOUND_CID_5462244.LOG` — the Gaussian 09 output. Everything
  computational came from this single file: 111 frequencies, Raman activities,
  IR intensities, reduced masses, Cartesian displacement vectors, optimised
  geometry.
- `Conformer3D_COMPOUND_CID_5462244.gjf` — read only to confirm the route line
  and starting coordinates.

I did **not** use `CONFORMER3D_COMPOUND_CID_5462244_raman_act.txt` — I parsed the
`.LOG` directly instead, because the displacement vectors needed for mode
assignment are only in the log.

---

## NOT USED — and why

### Other NAM Raman files

| Path | Why not |
|---|---|
| `20-04/plottingNAM/namdata20secpower40.xlsx` | Single condition (20 s, 40%). Already covered by the 20 s series. |
| `20-04/plottingNAM/powder5per20sec.xlsx` | Single condition (5%, 20 s). Already covered. |
| `20-04/sukesh NAM Raman data/5sec.xlsx`, `20sec.xlsx`, `Combined_Raman.xlsx`, `Copy of 5sec.xlsx` | Appear to be earlier consolidations of the same CSVs. I worked from the raw CSVs to keep the preprocessing under my control. |

**If any of these are independent measurements rather than re-exports of the
same spectra, tell me — they would add replicates, which is exactly what the
paper is short of.**

### Simulated-spectrum files

`20-04/plottingNAM/simulated-NAM.xlsx`, `review meeting/NAM/simdata.xlsx`,
`review meeting/NAM/simulated-NAM.xlsx`

Not used. I regenerated the simulated spectrum from the `.LOG` so that scaling,
Placzek intensity conversion and Lorentzian broadening were all done under known,
documented parameters. If your existing files used different settings, the
numbers won't match mine — mine are the ones described in the Methods.

### Prior write-up

`review meeting/NAM/Comparative Study of DFT Simulated and Experimental Powder
Raman Spectra of N (1).docx`

I have not opened this. If it contains analysis or conclusions you want carried
into the manuscript, point me at it.

### Available but not used

`review meeting/N-ACETYL-D-GLUCOSAMINE-OPT_raman_act.xlsx` — a GlcNAc
calculation. This is the NAM/NAG comparison I suggested earlier. Still worth
doing.

`review meeting/LTA-/`, `20-04/molecules/LTA Final/`, `molecule building/*LipidA*`
— different molecules, irrelevant to this paper.

### Not present

`nam-new/` — the folder your notes describe (70% / 60 s / 5 accumulations,
10 spots). It is not in `mtp`. That is the fixed-condition replicate set the
paper would benefit from most.

---

## Reproducing what I did

Scripts are in my working directory, not your folder. The pipeline was:

1. Parse B&W Tek CSVs — header metadata plus `Raman Shift` and `Dark Subtracted #1`
2. MD5-deduplicate
3. Interpolate to a 1 cm⁻¹ grid, 400–1800
4. ALS baseline (λ = 1e5, p = 0.001, 10 iterations)
5. Savitzky–Golay (window 11, order 3)
6. Min–max normalise
7. Select SNR ≥ 100, average, compute SD
8. Peak detection with two-criterion noise validation
9. Parse Gaussian `.LOG`; scale 0.980 / 0.967; Placzek intensities; Lorentzian FWHM 10
10. Match within ±18 cm⁻¹, preferring highest Raman activity
11. Assign modes from displacement-vector decomposition

Say the word and I will copy the scripts into your folder so the analysis is
reproducible and archivable alongside the paper.
