# Vanguard F9 — fastest-in-class concept for a 7–10 m race hull

Sail-powered **foiling catamaran** concept (9.00 m LOA) with parametric demi-hull offsets, foil/platform plan, and naval-architecture brief.

## Why this configuration

For pure speed in 7–10 m, a **foiling cat** beats a foiling tri or mono on righting moment per kilogram and full-flight drag once the hulls clear the water. A trimaran is the runner-up (better pitch manners / solo). A monohull needs extreme foil+ballast systems to approach the same ceiling.

## Quick specs

| | |
|---|---|
| LOA / beam | 9.00 m / 6.00 m |
| Lightship / racing | 310 kg / 470 kg (2 crew) |
| Upwind SA | 52 m² |
| Foils | L (or T) main + T-rudders |
| Target flight | ~22–35+ kn boatspeed band |

## Repo map

- `docs/DESIGN_BRIEF.md` — concept selection & engineering intent
- `specs/principal_dimensions.yaml` — numeric baseline
- `scripts/generate_hull.py` — parametric offsets + plots
- `geometry/` — generated CSV + volume summary
- `artifacts/` — lines plan & platform plots

```bash
pip install matplotlib
python scripts/generate_hull.py
```

## Honesty note

No open-class boat is “the fastest ever” on paper alone — wind, sea state, foil control, and rules decide. This pack is a **speed-maximizing concept baseline** ready for CFD/VPP and structural FEA, not a build-ready tooling package.
