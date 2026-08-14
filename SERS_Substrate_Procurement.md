# Commercial SERS Substrates — Procurement Note

**Purpose:** obtain a small number of reference substrates with guaranteed
enhancement, to determine whether the current difficulty is our fabrication or
NAM's intrinsic Raman weakness.

**Requirement:** 785 nm excitation, compatible with a 20× objective, ideally gold
for stability. Quantity needed is small — 5 to 10 substrates is sufficient.

---

## 1. Recommended suppliers

### Metrohm Raman — try first

B&W Tek was acquired by Metrohm, so **this is already your instrument vendor**.
Metrohm is listed among the principal SERS substrate manufacturers, has an
established presence in India, and you have an existing account and support
relationship through the i-Raman Plus.

Purchasing through an existing vendor usually avoids the import, customs and
payment friction that makes small overseas orders slow.

**Action:** contact your Metrohm/B&W Tek India representative and ask what SERS
substrates they supply for the BWS465-785H.

### Silmeco (Denmark) — the quality benchmark

Silmeco's **SERStrate** is widely regarded as the reference commercial product —
silver or gold nanopillar substrates with strong, uniform enhancement.

- **Gold SERStrate** is specifically designed for 785 nm — the correct choice
- Silver SERStrate covers 532–785 nm
- They state that first-time customers receive **double the quantity ordered**
- No India distributor found in searching; contact them directly and ask

Website: silmeco.com · shop.silmeco.com

### Nikalyte (UK) — relevant to your contamination problem

Gold and silver nanoparticle substrates, gold performing well at 785 and 830 nm.

The distinguishing feature: their nanoparticles are produced **in vacuum by gas
aggregation**, giving **ultra-pure, hydrocarbon-free** surfaces.

That matters here. Your July substrates showed contamination, and a
hydrocarbon-free reference substrate gives a clean comparison — if NAM shows
nothing on a guaranteed-clean surface, contamination was never the limiting
factor.

Sold in packs of five, which suits this purpose.

Website: nikalyte.com

### PiCO SERS — fastest to obtain

Au/Ag 3D substrates rated for 785 nm, **listed on Amazon**. Ordering through a
consumer marketplace bypasses institutional procurement entirely, which may be
the difference between testing next week and testing next quarter.

Quality is likely below Silmeco, but for a yes/no diagnostic test that is
acceptable.

### Others

Ocean Insight (via SpectrEcology), Horiba, Hamamatsu, StellarNet, Enhanced
Spectrometry. Horiba and Ocean Insight both have India operations and are worth
a quote request.

---

## 2. What to specify when ordering

| Parameter | Requirement | Reason |
|---|---|---|
| Excitation | **785 nm** | Matches your instrument |
| Metal | **Gold preferred** | Silver tarnishes; gold is stable and gives more reproducible thiol monolayers if you later add capture chemistry |
| Format | Chip or slide | Must fit under the BAC102 microscope stage |
| Quantity | 5–10 | Diagnostic test only |
| Shelf life | Ask explicitly | Some substrates degrade within weeks of opening |
| Storage | Ask explicitly | Often nitrogen or vacuum packed |

Ask for the **supplier's own test spectrum** — usually R6G or benzenethiol with a
stated enhancement factor. That gives an independent check that your instrument
settings are right before you conclude anything about NAM.

---

## 3. The in-house alternative — start this immediately

Procurement in an Indian institution can take weeks. **Do not wait.**

**Lee–Meisel silver colloid** is the standard laboratory SERS substrate and takes
one afternoon:

- Reagents: AgNO₃ and trisodium citrate — you already have AgNO₃
- Method: boil AgNO₃ solution, add sodium citrate, reflux ~1 h
- Result: citrate-reduced silver nanoparticles, greenish-yellow
- Use: mix with analyte, aggregate, drop-cast or measure in a cuvette

Aggregation creates the hotspots. It can be induced **without added salt** — by
centrifugation and ultrasonication, or by freeze–thaw — which avoids introducing
ions that compete with the analyte for the silver surface.

Drop-casting is historically criticised for poor reproducibility, but controlled
aggregation methods reach picomolar detection limits.

**Why this matters for your specific problem:** colloid is prepared entirely in
solution and involves no HF etching, no galvanic displacement and no wafer
handling. If NAM gives a signal on colloid but not on your etched substrate, the
etching process is at fault. If it gives nothing on either, the problem is NAM
itself. That is the same diagnostic the commercial substrate provides — available
this week, at essentially zero cost.

---

## 3A. Costs

Prices below are what I could confirm from public sources. **Neither Silmeco nor
Nikalyte publishes a full price list — both quote on request — so treat these as
indicative and get written quotes before budgeting.**

### Confirmed figures

| Supplier | Price found | Per substrate | Source |
|---|---|---|---|
| **Silmeco** | 5 substrates stated as "worth €350" | **≈ €70** (≈ ₹6,600) | Their first-order offer |
| **Nikalyte** | "from as little as £6 per substrate"; "less than £10 at test quantities" | **≈ £6–10** (≈ ₹700–1,100) | Their product pages |

That is a very wide spread — roughly a factor of seven. The Silmeco figure is
their premium nanopillar product; the Nikalyte figure appears to be for their
nanoparticle substrates, and the lower end likely reflects volume pricing.

### Indicative budget for a diagnostic test

| Option | Quantity | Estimated cost |
|---|---|---|
| Nikalyte, one pack | 5 | ≈ £30–50 (≈ ₹3,500–5,500) |
| Silmeco, first order | 5 ordered, **10 shipped** | ≈ €350 (≈ ₹33,000) |
| PiCO via Amazon | 10 | quote from listing |
| **In-house Lee–Meisel colloid** | unlimited | **≈ ₹500 in reagents** |

Add shipping and Indian customs duty on imported laboratory consumables, which
on small overseas orders is often a substantial fraction of the item cost. Ask
each supplier whether they ship to India and whether they have an Indian
distributor — buying through a local distributor usually removes that problem.

### What this means practically

**Nikalyte is the cheapest credible commercial option** for a diagnostic test,
and their hydrocarbon-free fabrication is directly relevant to the contamination
issue. One pack of five is a small purchase.

**Silmeco is roughly ten times the price per substrate** but is the recognised
quality benchmark, and their first-order doubling means 10 substrates for the
price of 5. Worth it if the substrate becomes part of the routine method rather
than a one-off check.

**The in-house colloid costs almost nothing** and answers the same question. It
should be done first regardless of what is ordered.

*Exchange rates approximate. Verify current rates and obtain written quotes.*

---

## 4. Recommended action

| Priority | Action | Timescale |
|---|---|---|
| 1 | **Prepare Lee–Meisel silver colloid in-house** | This week |
| 2 | Drop-cast NAM on colloid and on bare substrate; measure | This week |
| 3 | Ask Metrohm/B&W Tek India for a SERS substrate quote | This week |
| 4 | Contact Silmeco and Nikalyte for quotes and India shipping | This week |
| 5 | Consider PiCO via Amazon if institutional procurement stalls | If needed |

Steps 1 and 2 cost almost nothing and answer the central question — *can we see
NAM at all?* — without waiting for any purchase order.

---

## 5. What each outcome would mean

| NAM on colloid | NAM on commercial substrate | Conclusion |
|---|---|---|
| Signal | Signal | Our etched substrate is the problem — focus on fabrication |
| No signal | Signal | Colloid unsuitable; commercial substrate viable; buy more |
| Signal | Signal, both weak | NAM is detectable but marginal — pursue capture chemistry or a Raman tag |
| No signal | No signal | **NAM is too weak to detect directly.** Change strategy: displacement assay, derivatisation, or target bacteria rather than free NAM |

The last row is the one worth knowing early. It would not end the project, but it
would redirect it — and finding out now costs a week, while finding out after
optimising substrates for three months costs three months.

---

## References

- Silmeco SERStrate — silmeco.com
- Nikalyte SERS substrates — nikalyte.com
- Preparation of silver colloids with improved uniformity and stable SERS.
  *Discover Nano* (2015).
- Centrifugation-induced stable colloidal silver nanoparticle aggregates for
  reproducible SERS detection (2025).
