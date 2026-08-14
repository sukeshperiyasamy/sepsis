# Measuring Laser Power at the Sample

> **Update — you do not need this to submit the paper.**
>
> The manuscript has been rewritten to report power settings as percentages of
> the instrument maximum, together with the manufacturer's nominal figures and an
> explicitly-labelled estimated range for the power density. That is honest,
> publishable, and common practice in the Raman literature.
>
> This protocol is kept for if a meter becomes available later, or if a reviewer
> asks. Section 3 lists free routes that need no equipment.


**Instrument:** i-Raman Plus BWS465-785H + BAC102-785E microscope, 20× Plan, 785 nm

**Why:** the paper reports a laser-damage threshold. Stated as "90% power" it is
unreproducible on any other instrument. Stated as a power density in mW µm⁻² it
is a physical quantity anyone can check.

---

## 1. What you need

An **optical power meter** with a sensor rated for 785 nm and at least ~500 mW.

| Type | Suitable? | Note |
|---|---|---|
| **Thermal (thermopile)** | **Best** | Handles high power, wavelength-flat, won't be damaged |
| Photodiode | Usable | Must set wavelength to 785 nm; **can be damaged by a focused beam** |

Common models: Thorlabs PM100D/PM16 series, Ophir Nova/Vega, Coherent LabMax,
Gentec. Any photonics, laser or optics lab at IIT Jodhpur will have one — this is
standard equipment, worth asking around before buying.

---

## 2. Procedure

1. **Set the meter to 785 nm.** Photodiode sensors are strongly wavelength
   dependent; a wrong setting gives a wrong answer with no warning.

2. **Zero the meter** with the laser off or shuttered.

3. **Position the sensor at the sample plane** — where the powder normally sits,
   at the objective's working distance. This is the measurement that matters.
   Measuring anywhere else gives the wrong number.

4. **Defocus slightly if using a photodiode.** Move the sensor 1–2 mm below the
   focal plane so the beam has expanded. All the light is still collected, but the
   intensity on the detector element is far lower. A focused 785 nm beam at
   >100 mW can permanently damage a photodiode sensor. Thermal sensors are safe
   at focus.

5. **Record at several settings** — 5%, 40%, 70%, 90%. Four points confirm the
   response is linear and give you the whole curve rather than one point.

6. **Let each reading settle**, especially with a thermal sensor, which takes
   several seconds to equilibrate.

Wear the laser safety goggles supplied with the instrument. This is a Class 3B
laser and you will have the beam path open.

### Record this

| Setting | Reading (mW) |
|---|---|
| 5% | ______ |
| 40% | ______ |
| 70% | ______ |
| 90% | ______ |

---

## 3. If no power meter is available — free routes

**In order of effort. None requires buying anything.**

### a. Ask Metrohm — do this first

One email to your Metrohm/B&W Tek India representative:

> "For the BWS465-785H with the BAC102-785E microscope and a 20× Plan objective,
> what is the approximate optical transmission from probe output to sample, or
> the typical power at the sample at a given percentage setting?"

They may have the figure already. Costs nothing, and an answer from the
manufacturer is citable.

### b. Central Instrumentation Facility

IIT Jodhpur's CIF, and the physics and materials departments, will almost
certainly have an optical power meter. Photonics and laser groups use them
routinely. A twenty-minute loan is all that is needed.

### c. Any group running a laser

Ask around. Power meters are common shared equipment and people generally lend
them without ceremony.

### d. Estimate from component specifications — what the paper now does

A 20× Plan achromat transmits roughly 70–85% at 785 nm; microscope optics
(beamsplitter, filters, mirrors) perhaps 50–80%. Combined, about 40–65%.

This is what the manuscript now reports, **clearly labelled as an estimate
derived from component specifications rather than a measurement**. That
distinction is what makes it acceptable.

### e. Low-cost meter, if you ever want one

Basic laser power meters covering 785 nm at a few hundred mW are available for
roughly ₹5,000–15,000. Accuracy is modest but adequate for an order-of-magnitude
figure. Not necessary for this paper.

---

## 4. Converting to power density

### Spot size

For a diffraction-limited focus:

```
d = 1.22 λ / NA
```

With λ = 0.785 µm and a 20× Plan objective (NA ≈ 0.40):

| NA | Spot diameter | Area |
|---|---|---|
| 0.35 | 2.74 µm | 5.88 µm² |
| **0.40** | **2.39 µm** | **4.50 µm²** |
| 0.45 | 2.13 µm | 3.56 µm² |

**Check the NA marked on your objective barrel** — it is printed on the side.

Note the real spot is often **larger** than the diffraction limit, because the
probe delivers an image of the fibre core rather than a perfect point. If your
BAC102 has a video microscope, you may be able to see the spot and estimate its
diameter against a stage micrometer. That is a better number than the theoretical
one.

### The calculation

```
power density = P_sample / spot area
```

### Expected range for your system

Taking 238 mW at the probe for the 70% setting:

| Transmission | P at sample | Power density | |
|---|---|---|---|
| 30% | 71 mW | 15.9 mW µm⁻² | 1.6 MW cm⁻² |
| 40% | 95 mW | 21.1 mW µm⁻² | 2.1 MW cm⁻² |
| **50%** | **119 mW** | **26.4 mW µm⁻²** | **2.6 MW cm⁻²** |
| 60% | 143 mW | 31.7 mW µm⁻² | 3.2 MW cm⁻² |
| 70% | 167 mW | 37.0 mW µm⁻² | 3.7 MW cm⁻² |

*(1 mW µm⁻² = 0.1 MW cm⁻²)*

**These numbers make your damage result physically sensible.** Power densities of
a few MW cm⁻² will readily char an organic powder over 60 seconds, which is
exactly what you observed at 90% / 60 s. Percentages conceal that; power density
explains it.

---

## 5. What to report in the paper

Once measured, the Methods section should state:

> "Laser power at the sample was measured with a [meter model] at the objective
> focal plane and was **X mW** at the [Y]% setting used for the final
> measurements. With a 20× objective (NA Z), this corresponds to a spot diameter
> of approximately **D µm** and a power density of approximately **P mW µm⁻²**."

And Section 3.3 should restate the damage threshold in those terms:

> "Sample degradation occurred at a power density of approximately **P mW µm⁻²**
> with 60 s exposure, while **P′ mW µm⁻²** for 30 s produced no detectable
> change over ten consecutive scans."

That is the version another laboratory can act on.

---

## 6. Send me

- The four meter readings
- The NA printed on your objective
- Spot diameter, if you can measure it

I will compute the power densities, update the Methods and Section 3.3, and
rebuild both output formats.
