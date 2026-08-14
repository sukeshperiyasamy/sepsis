# Power Measurement — What to Do at the Instrument

You said you can measure power at the sample. Here is exactly what to record.

---

## Why this matters more than it looks

At 70% the laser outputs ~347 mW nominal. Through a 20× objective that would
focus into roughly a 2–4 µm spot. If anything close to that reached the powder,
an organic carbohydrate would char almost immediately.

Your data shows the opposite: band positions stable within ±1 cm⁻¹ and the
930 cm⁻¹ FWHM constant at 10–11 cm⁻¹ across the entire 5%→80% range. No
carbonisation, no band loss.

So either the transmission losses through the BAC102 microscope are large, or
the percentage setting is not linear in output. Either way, **the number you
measure is the number that goes in the paper** — and it turns a potential
reviewer objection into a strength, because you can then state the power density
the sample tolerated without damage.

---

## What to measure

Put a power meter head at the objective focal plane (where the sample sits),
785 nm wavelength setting, 20× Plan objective in place.

Record the power at each setting you used:

| Setting | Nominal output | Measured at sample |
|---|---|---|
| 5% | 24.8 mW | ______ mW |
| 10% | 49.5 mW | ______ mW |
| 20% | 99.0 mW | ______ mW |
| 30% | 148.5 mW | ______ mW |
| 40% | 198.0 mW | ______ mW |
| 50% | 247.5 mW | ______ mW |
| 60% | 297.0 mW | ______ mW |
| 70% | 346.5 mW | ______ mW |
| 80% | 396.0 mW | ______ mW |

If time is short, **5%, 40% and 80% is enough** — three points establish whether
the response is linear and give you the endpoints.

---

## Also worth writing down while you are there

**Spectral resolution** — from the manufacturer spec sheet or the software's
instrument info panel. Quoted in cm⁻¹. I can derive the *sampling* from your data
(1.76 cm⁻¹/pixel at 400, 1.43 at 1800) but sampling is not resolution, and
reviewers know the difference.

**Spot size** — if the software or manual gives the focal spot diameter for the
20× objective. With that plus the measured power I can compute an actual power
density in mW µm⁻², which is the physically meaningful quantity.

**Reagent bottle** — while you are in the lab: supplier, catalogue number, lot
number, purity, and critically whether it says **anomer (α or β)** and
**hydrate or anhydrous**. This determines whether the DFT model is correct.

---

## What I will do with the numbers

Once you send them:

1. Replace the placeholder in the Methods section
2. Compute power density at the sample for the 20× objective
3. Add a sentence to Section 3.1 stating the power density the sample tolerated
   without spectral change — this makes the photostability result quantitative
   rather than qualitative, which is considerably stronger
4. Rebuild both the LaTeX and Word versions

---

## Note on the objective

You confirmed **20× Plan**. I have set this in the Methods. The 50× LMPlan
(NA 0.50, WD 10.5 mm) is listed in your instrument description but is not
mentioned as used — I have left it out. If any of the NAM spectra were actually
taken with the 50×, tell me which files and I will separate them, because the
spot size and therefore power density differ substantially.
