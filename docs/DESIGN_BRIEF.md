# Vanguard F9 — 9 m Foiling Race Catamaran

Concept design for a **7–10 m** ultra-light **foiling catamaran** optimized for maximum race speed in open class / prototype rules (no box-rule constraints assumed).

## Verdict: configuration

| Option | Speed potential | Why |
|---|---|---|
| **Foiling catamaran (selected)** | Highest | Max beam → max righting moment → more sail power; two slender demi-hulls for takeoff; proven path (A-Class, NACRA F20s, Cup derivatives) |
| Foiling trimaran | Very high | Better pitch damping and singlehanded manners; extra hull mass and aero drag usually costs top-end vs equal-tech cat |
| Foiling monohull | High but lower ceiling | Needs deep foil + ballast or extreme crew hiking; less RM per kg than a wide multi |
| Displacement / planing multi (no foils) | Far lower | Skin friction + wave-making dominate above ~15–18 kn |

**Selected platform:** 9.00 m LOA foiling catamaran, crew 2, full-flying T/L foil package, carbon primary structure.

> “Fastest ever” is not a claim this document makes. Absolute speed depends on wind, sea state, sail inventory, foil control, and class legality. This concept is engineered to **maximize speed potential** inside 7–10 m LOA for a sail-powered race boat.

## Design intent

1. **Fly early** — low takeoff boatspeed via high foil CL, light platform, and demi-hulls that unload quickly.
2. **Fly clean** — once clear, minimize aero + foil induced/parasite drag; hulls become reserve buoyancy only.
3. **Carry power** — wide beam and trampoline/crew stacking for righting moment without heavy ballast.
4. **Survive the mode** — pitch/heave control via rake-able main foils + T-rudders; fail-safe ventilation recovery.

## Principal dimensions

| Parameter | Value | Notes |
|---|---|---|
| LOA | 9.00 m | Mid of requested 7–10 m band |
| LWL (each demi-hull) | 8.60 m | Fine overhangs |
| Beam overall (max) | 6.00 m | Fold/transport option at 2.5 m with beam bolts |
| Beam hull CL to CL | 5.20 m | Foil span / RM trade |
| Demi-hull max beam | 0.48 m | Low wave-making; spray control |
| Demi-hull depth (keel to deck) | 0.72 m | Volume for crew + systems |
| Hull draft (canoe body) | 0.18 m | Boards/rudders add flying draft |
| Lightship mass target | 310 kg | Platform + foils + spars, no crew |
| Racing displacement | 470 kg | + 2 × 80 kg crew |
| Sail area upwind (main+jib) | 52 m² | High SA/D when flying |
| Downwind + gennaker | 95 m² | Apparent-wind machine |
| Design wind (full flight) | 8–12 kn TWS | Stable flight corridor |
| Target boatspeed band | 22–35+ kn | Sea state and skill limited |

## Hull architecture

### Demi-hull form

- **Wave-piercing entry** (fine Cw forward, slight reverse sheer optional) to reduce pitch moments pre-flight.
- **Narrow waterline** with soft bilge amidships → low wavemaking during displacement/semi-planing takeoff.
- **Flattened buttock lines aft** (last ~25% LWL) for dynamic lift and spray release if foils ventilate.
- **Minimal rocker**; LCB slightly aft of amidships (~52% LWL from FP) to bias foil loading aft and help bow-up takeoff attitude.
- **Hard chine optional** only in aft quarters for build simplicity; forward sections stay round-bilge for seakeeping.

### Cross structure

- Forward beam + aft beam (carbon box), netted trampoline, rotating carbon wing mast (~13.5 m).
- Beams set high to keep aero clean and reduce wave slap when skimming.
- Optional curved dagger trunks integrated into inner hull sides for L-foils, or centerline-ish T-foil cases in each hull.

## Foil package (speed-critical)

| Element | Concept | Role |
|---|---|---|
| Main foils | L-foils or T-foils, carbon, ~1.35 m span each | Primary lift + leeway |
| Rudder foils | T-rudders, independent rake | Pitch trim / altitude |
| Control | Manual rake + gearing; optional ride-height wands | Stabilize flight |
| Section | Custom ~12–15% t/c; cavitation-aware tips | High Re, low Cd |

**Flight logic:** lift ≈ displacement at takeoff speed ~11–13 kn BS; above that, reduce AoA/rake to hold altitude ~0.6–1.0 m. Excess RM from beam allows aggressive apparent-wind sail trim.

## Materials & structure

- **Hull skins:** carbon/epoxy sandwich, Corecell/PET foam ~10–15 mm, local solid carbon at trunks/beam beds.
- **Beams / racks:** high-modulus carbon box beams.
- **Foils:** unidirectional carbon with ±45 skins; titanium or Inox fittings.
- **Safety factor:** Ultimate ≈ 2.0 on foil bending at design load case (flight + gust); buckling check on beam compression from tramp / forestay.

## Weight budget (target)

| Group | Mass (kg) |
|---|---|
| Two demi-hulls (structure) | 95 |
| Beams, racks, tramp, fittings | 55 |
| Foils + rudders + cases | 48 |
| Mast, boom, standing/running | 62 |
| Sails (upwind inventory) | 22 |
| Systems / tiller / misc | 28 |
| **Lightship** | **310** |
| Crew (2) | 160 |
| **Racing** | **470** |

## Why not trimaran or mono here

- **Trimaran:** excellent for solo and rough-water flight, but the center hull + amas add wetted/aero area and mass for the same LOA; choose tri if the brief shifts to singlehanded offshore or pitch-critical sea states.
- **Monohull:** competitive only with extreme foil + ballast systems; within 7–10 m and equal technology, the cat’s RM/weight ratio wins outright speed.

## Deliverables in this repo

- `specs/principal_dimensions.yaml` — numeric design baseline
- `geometry/hull_offsets.csv` — generated demi-hull stations
- `scripts/generate_hull.py` — parametric demi-hull generator + plots
- `artifacts/` — section and planform plots

## Next engineering steps (outside this concept pack)

1. CFD / VPP: takeoff polar, foil Cl/Cd, aero of platform + rig.
2. FEA: foil root bending, beam beds, trunk crush.
3. 3D loft (Rhino/FreeCAD) from offsets → CNC male plug or female tooling.
4. Tank or instrumented prototype foil rake schedule.

## Assumptions locked for this revision

- Sail-powered race boat (not powerboat)
- Open / prototype rules (foils allowed, no strict box)
- Crew of two, daysailing race / inshore course
- Transportable: longitudinal split / beam bolts to road width ~2.5 m
