# NAM Raman — Full Run Sheet

**Instrument:** i-Raman Plus BWS465-785H + BAC102-785E · 785 nm · 20× Plan  
**Sample:** Sigma A3007 NAM powder, glass slide  
**60 spectra · about 2 h 15 min**

Tick each row as you go. Filenames matter — use them exactly and I can
reprocess everything automatically.

---

## Before you start

- [ ] Clean slide (lens tissue + IPA, fully dry)
- [ ] Record NAM **lot number** from the bottle
- [ ] Note if label states **α / β / nothing** about the anomer
- [ ] Measure **power at sample (mW)** with meter at objective focal plane:
      5% ____  40% ____  70% ____  80% ____
- [ ] Check if software allows range beyond 2842 cm⁻¹ — if yes, note it
- [ ] Record **spectral resolution** from spec sheet: ____ cm⁻¹

---

## Block A — Glass blank

*3 spectra · 8 min*

Empty clean slide, no powder. Identical settings to Block B — that is the point. Proves no reported band comes from the substrate.

| ✓ | No | Power | Time | Acc | Spot | Filename |
|---|---|---|---|---|---|---|
| ☐ | 1 | 70% | 25 s | 5 | glass 1 | `GLASS_spot1.csv` |
| ☐ | 2 | 70% | 25 s | 5 | glass 2 | `GLASS_spot2.csv` |
| ☐ | 3 | 70% | 25 s | 5 | glass 3 | `GLASS_spot3.csv` |

## Block B — Reference spectrum — **most important**

*10 spectra · 26 min*

Ten independent spots on fresh powder at one fixed condition. This becomes the reference spectrum in the paper and is the replicate set your current data lacks. **Move the stage to genuinely fresh powder between every spot.**

| ✓ | No | Power | Time | Acc | Spot | Filename |
|---|---|---|---|---|---|---|
| ☐ | 4 | 70% | 25 s | 5 | fresh 1 | `NAM_final_spot01.csv` |
| ☐ | 5 | 70% | 25 s | 5 | fresh 2 | `NAM_final_spot02.csv` |
| ☐ | 6 | 70% | 25 s | 5 | fresh 3 | `NAM_final_spot03.csv` |
| ☐ | 7 | 70% | 25 s | 5 | fresh 4 | `NAM_final_spot04.csv` |
| ☐ | 8 | 70% | 25 s | 5 | fresh 5 | `NAM_final_spot05.csv` |
| ☐ | 9 | 70% | 25 s | 5 | fresh 6 | `NAM_final_spot06.csv` |
| ☐ | 10 | 70% | 25 s | 5 | fresh 7 | `NAM_final_spot07.csv` |
| ☐ | 11 | 70% | 25 s | 5 | fresh 8 | `NAM_final_spot08.csv` |
| ☐ | 12 | 70% | 25 s | 5 | fresh 9 | `NAM_final_spot09.csv` |
| ☐ | 13 | 70% | 25 s | 5 | fresh 10 | `NAM_final_spot10.csv` |

## Block C — Comparison grid

*32 spectra · 53 min*

Repeats your old power×integration conditions so new and old can be overlaid directly. **Run in the scrambled order given** — in the old data power ramped 5%→80% in file order, so power and cumulative exposure are confounded (r = −0.93). Fresh spot each row.

| ✓ | No | Power | Time | Acc | Spot | Filename |
|---|---|---|---|---|---|---|
| ☐ | 14 | 40% | 25 s | 5 | fresh 1 | `NAM_grid_p40_t25.csv` |
| ☐ | 15 | 40% | 10 s | 5 | fresh 2 | `NAM_grid_p40_t10.csv` |
| ☐ | 16 | 20% | 5 s | 5 | fresh 3 | `NAM_grid_p20_t5.csv` |
| ☐ | 17 | 10% | 25 s | 5 | fresh 4 | `NAM_grid_p10_t25.csv` |
| ☐ | 18 | 80% | 25 s | 5 | fresh 5 | `NAM_grid_p80_t25.csv` |
| ☐ | 19 | 20% | 15 s | 5 | fresh 6 | `NAM_grid_p20_t15.csv` |
| ☐ | 20 | 50% | 25 s | 5 | fresh 7 | `NAM_grid_p50_t25.csv` |
| ☐ | 21 | 20% | 25 s | 5 | fresh 8 | `NAM_grid_p20_t25.csv` |
| ☐ | 22 | 60% | 5 s | 5 | fresh 9 | `NAM_grid_p60_t5.csv` |
| ☐ | 23 | 80% | 15 s | 5 | fresh 10 | `NAM_grid_p80_t15.csv` |
| ☐ | 24 | 50% | 5 s | 5 | fresh 11 | `NAM_grid_p50_t5.csv` |
| ☐ | 25 | 60% | 10 s | 5 | fresh 12 | `NAM_grid_p60_t10.csv` |
| ☐ | 26 | 30% | 15 s | 5 | fresh 13 | `NAM_grid_p30_t15.csv` |
| ☐ | 27 | 80% | 5 s | 5 | fresh 14 | `NAM_grid_p80_t5.csv` |
| ☐ | 28 | 10% | 5 s | 5 | fresh 15 | `NAM_grid_p10_t5.csv` |
| ☐ | 29 | 10% | 10 s | 5 | fresh 16 | `NAM_grid_p10_t10.csv` |
| ☐ | 30 | 40% | 5 s | 5 | fresh 17 | `NAM_grid_p40_t5.csv` |
| ☐ | 31 | 30% | 25 s | 5 | fresh 18 | `NAM_grid_p30_t25.csv` |
| ☐ | 32 | 70% | 10 s | 5 | fresh 19 | `NAM_grid_p70_t10.csv` |
| ☐ | 33 | 50% | 15 s | 5 | fresh 20 | `NAM_grid_p50_t15.csv` |
| ☐ | 34 | 10% | 15 s | 5 | fresh 21 | `NAM_grid_p10_t15.csv` |
| ☐ | 35 | 70% | 25 s | 5 | fresh 22 | `NAM_grid_p70_t25.csv` |
| ☐ | 36 | 60% | 15 s | 5 | fresh 23 | `NAM_grid_p60_t15.csv` |
| ☐ | 37 | 30% | 10 s | 5 | fresh 24 | `NAM_grid_p30_t10.csv` |
| ☐ | 38 | 70% | 5 s | 5 | fresh 25 | `NAM_grid_p70_t5.csv` |
| ☐ | 39 | 40% | 15 s | 5 | fresh 26 | `NAM_grid_p40_t15.csv` |
| ☐ | 40 | 50% | 10 s | 5 | fresh 27 | `NAM_grid_p50_t10.csv` |
| ☐ | 41 | 20% | 10 s | 5 | fresh 28 | `NAM_grid_p20_t10.csv` |
| ☐ | 42 | 60% | 25 s | 5 | fresh 29 | `NAM_grid_p60_t25.csv` |
| ☐ | 43 | 80% | 10 s | 5 | fresh 30 | `NAM_grid_p80_t10.csv` |
| ☐ | 44 | 70% | 15 s | 5 | fresh 31 | `NAM_grid_p70_t15.csv` |
| ☐ | 45 | 30% | 5 s | 5 | fresh 32 | `NAM_grid_p30_t5.csv` |

## Block D — Weak region

*5 spectra · 23 min*

Double accumulations. Eleven of your twelve tentative bands sit between 1550 and 1800 cm⁻¹ — amide I, amide II, carboxyl C=O. This should move most of them to confident.

| ✓ | No | Power | Time | Acc | Spot | Filename |
|---|---|---|---|---|---|---|
| ☐ | 46 | 70% | 25 s | 10 | fresh 1 | `NAM_longacq_spot1.csv` |
| ☐ | 47 | 70% | 25 s | 10 | fresh 2 | `NAM_longacq_spot2.csv` |
| ☐ | 48 | 70% | 25 s | 10 | fresh 3 | `NAM_longacq_spot3.csv` |
| ☐ | 49 | 70% | 25 s | 10 | fresh 4 | `NAM_longacq_spot4.csv` |
| ☐ | 50 | 70% | 25 s | 10 | fresh 5 | `NAM_longacq_spot5.csv` |

## Block E — Photostability

*10 spectra · 23 min*

Ten consecutive scans on the **same spot without moving the stage**. Proves no cumulative change at the final condition. Optional but cheap, and it makes the no-damage claim airtight.

| ✓ | No | Power | Time | Acc | Spot | Filename |
|---|---|---|---|---|---|---|
| ☐ | 51 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run01.csv` |
| ☐ | 52 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run02.csv` |
| ☐ | 53 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run03.csv` |
| ☐ | 54 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run04.csv` |
| ☐ | 55 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run05.csv` |
| ☐ | 56 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run06.csv` |
| ☐ | 57 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run07.csv` |
| ☐ | 58 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run08.csv` |
| ☐ | 59 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run09.csv` |
| ☐ | 60 | 70% | 25 s | 5 | SAME spot | `NAM_stability_run10.csv` |

---

## Summary

| Block | Purpose | Spectra | Time |
|---|---|---|---|
| A | Glass blank | 3 | 8 min |
| B | Reference spectrum — most important | 10 | 26 min |
| C | Comparison grid | 32 | 53 min |
| D | Weak region | 5 | 23 min |
| E | Photostability | 10 | 23 min |
| | **TOTAL** | **60** | **~2 h 15 min** |

---

## If you are short on time

**Blocks A + B only** — 13 spectra, 34 minutes. That gives the substrate control
and the replicate set, which are the two things a reviewer will ask about.

Blocks C, D and E are improvements, not requirements.

---

## Afterwards

Save everything raw, unprocessed, into a folder called **`NAM_new_measurements`**
inside your `mtp` folder. Keep the filenames exactly as listed.

Then tell me and I will:

- rebuild the reference spectrum from the 10 true replicates (Block B)
- add the glass-blank comparison as a new figure (Block A)
- overlay new vs old grid to show consistency (Block C)
- re-run peak validation — tentative bands should become confident (Block D)
- add a photostability figure (Block E)
- insert your measured mW into the Methods
- regenerate Table 3, all statistics, and every figure
