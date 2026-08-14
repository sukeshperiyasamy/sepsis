# Audit of `mtp/29-05-26`

**Yes — this is NAM powder data, and it is the dataset I have been asking for.**
129 CSV files, recorded 29 May 17:06 → 30 May 09:01 on the same instrument
(BTC665N-785H-SYS, 784.92 nm).

It also matches your chat log: on **Fri 29 May at 4:17 PM** you asked *"Should I
put the powder directly on the microscope glass or do I need to use a glass
slide?"* — the first files here are timestamped **17:06** that same afternoon.

But there are three problems you need to know about.

---

## How I verified it is NAM

Every file was processed through the same pipeline as the published data and
correlated against your established NAM powder reference spectrum:

| Folder | n | mean r | verdict |
|---|---|---|---|
| `70p-5ac-30s-diifrentspot` | 3 | **0.977** | NAM powder |
| `70p-60s-5ac-diifrentpoint` | 3 | **0.970** | NAM powder |
| `90p-30s-5ac-diifrentpoint` | 5 | **0.948** | NAM powder |
| `90p-30s-5acc-samespot` | 10 | **0.943** | NAM powder |
| `NAM-70p-10s-5ac` | 11 | **0.937** | NAM powder |
| `NAM-90p-10s-5ac` | 11 | **0.936** | NAM powder |
| `NAM-90p-10s-3ac` | 12 | **0.928** | NAM powder |
| `NAM-70p-10s-3acc` | 11 | **0.922** | NAM powder |
| `70p-5ac-10s-diifrentpoint` | 10 | 0.624 | weak — low SNR at 10 s |
| `90p-60s-5a-samespot` | 5 | **0.150** | **sample destroyed** |
| `90p-60s-5ac-diffrentspot` | 5 | **0.156** | **sample destroyed** |
| `glass slide empty` | 43 | 0.748 | **mixed — see below** |

---

## Problem 1 — you burned the sample at 90% / 60 s

The two `90p-60s` folders are not usable as NAM spectra. The sample was
destroyed during acquisition.

Same spot, five consecutive scans — intensity of the strongest NAM band:

| Scan | I(930 cm⁻¹) |
|---|---|
| 1 | 0.44 |
| 2 | 0.31 |
| 3 | 0.28 |
| 4 | 0.25 |
| 5 | 0.23 |

The characteristic sharp bands at 872, 930 and 956 cm⁻¹ collapse into noise, and
the 1580 cm⁻¹ region rises. See `DIAGNOSTIC_90p_60s_damage.png` — the contrast
with the reference spectrum is unmistakable.

**This is actually a useful result.** Combined with everything else, you now have
a clean damage threshold:

| Condition | Outcome |
|---|---|
| ≤80% power, ≤25 s | safe (verified in the April dataset) |
| 70% power, 30 s | safe (r = 0.977) |
| 70% power, 60 s | **safe** (r = 0.970) |
| 90% power, 30 s | safe (r = 0.948) |
| **90% power, 60 s** | **sample destroyed** |

That is a publishable photostability limit, and it justifies your final choice of
conditions rather than leaving it as an assertion. I would put this in the paper.

Note this does **not** contradict the earlier no-damage finding — that analysis
covered 5–80% at 25 s and under. Ninety percent combined with 60 s is well
beyond anything in the April grid.

## Problem 2 — the folder called `glass slide empty` is mostly not glass

Of 43 files:

| Contents | n | Detail |
|---|---|---|
| **True glass blanks** | 5 | `glassslide (1)–(5).csv`, 5% power, 5 s, 1 accumulation, r ≈ 0.24 |
| NAM powder, misfiled | 16 | named `NAM-10S_70P_3AC_S1.csv` etc., r = 0.94–0.99 |
| Ambiguous | 16 | same naming, r = 0.5–0.9 |
| Weak / low power | 6 | `NAM_5P_*`, `NAM_10P_*`, r = 0.26–0.49 |

So you do have genuine glass blanks — but only **five**, and they were taken at
**5% power / 5 s / 1 accumulation**, not at your measurement conditions.

For the substrate-control argument the paper needs, the blank must be recorded at
the *same* settings as the sample. These are not. **This is still worth ten
minutes of instrument time**: three blanks at 70% / 25 s / 5 accumulations.

## Problem 3 — the 10 s data is weak

`70p-5ac-10s-diifrentpoint` correlates at only 0.62. Ten seconds is too short at
this power to give a clean spectrum. Not a fault, just not useful for the
reference spectrum.

---

## What is actually usable

**89 good NAM powder spectra** after excluding the burned folders:

| Power | Integration | Accumulations | n |
|---|---|---|---|
| 70% | 10 s | 3 | 15 |
| 70% | 10 s | 5 | 16 |
| 70% | 30 s | 5 | 3 |
| 70% | 60 s | 5 | 3 |
| 80% | 10 s | 3 | 6 |
| 80% | 10 s | 5 | 3 |
| 90% | 10 s | 3 | 15 |
| 90% | 10 s | 5 | 13 |
| 90% | 30 s | 5 | 15 |

**And crucially, these are genuine replicates at fixed conditions** — which is
exactly what the April dataset lacked. `90p-30s-5acc-samespot` (10 scans, same
spot) plus `90p-30s-5ac-diifrentpoint` (5 fresh spots) together give you both a
photostability series and a replicate series at one condition.

---

## What this changes

**Most of the run sheet I wrote is no longer needed.** You already have:

- ✅ replicates at fixed conditions (Block B) — 90%/30 s, and 70%/10 s
- ✅ photostability, same spot (Block E) — two series
- ✅ a damage threshold, which is better than what I asked for
- ✅ long integration data (30 s, 60 s) the April set didn't have

**Still missing, and still worth doing:**

1. **Glass blanks at measurement conditions** — 3 spots, 70% / 25 s / 5 acc.
   Ten minutes. The five you have are at the wrong settings.
2. **Power at the sample in mW.** Unchanged, still the single most-asked number.
3. **Extended range above 2842 cm⁻¹**, if the software allows it.

---

## What I would like to do next

Merge this dataset with the April grid and rebuild the paper around it. That
would give:

- a reference spectrum from **true replicates** rather than 40 different conditions
- a proper photostability figure with a quantified damage threshold
- longer-integration data, which should rescue several of the twelve tentative
  bands in the 1550–1800 cm⁻¹ region

Say the word and I will reprocess everything. It changes the Methods, the
reference spectrum, Table 3 and the statistics — all for the better.

**One question first:** in `90p-60s-5ac-diffrentspot` the signal declines across
supposedly *fresh* spots (r = 0.40 → 0.01). Was the powder layer very thin there,
or were those spots close to previously burned regions? It affects how I write up
the damage threshold.
