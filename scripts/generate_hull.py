#!/usr/bin/env python3
"""
Parametric demi-hull generator for Vanguard F9 foiling race catamaran.

Generates:
  - station offsets (CSV)
  - body-plan / profile / planform plots (PNG)

Geometry is a design-intent loft suitable for concept CFD seeding and
Rhino/FreeCAD import — not a class-certifiable lines plan.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

# Optional plotting — script still writes CSV if matplotlib is missing.
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:  # pragma: no cover
    HAS_MPL = False


ROOT = Path(__file__).resolve().parents[1]
OUT_GEOM = ROOT / "geometry"
OUT_ART = ROOT / "artifacts"

# --- Principal dimensions (m) -------------------------------------------------
LOA = 9.00
LWL = 8.60
MAX_BEAM = 0.48          # single demi-hull (narrow for low takeoff drag)
DEPTH = 0.72             # keel to deck
DRAFT = 0.18             # canoe-body draft at DWL (lightly immersed)
LCB_FRAC = 0.52          # longitudinal center of buoyancy from FP / LWL
N_STATIONS = 21
N_WATERLINES = 12
FP_OVERHANG = (LOA - LWL) * 0.45
AP_OVERHANG = (LOA - LWL) * 0.55


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def station_x(i: int, n: int = N_STATIONS) -> float:
    """X from FP (bow) toward AP along LOA."""
    return LOA * i / (n - 1)


def waterline_fraction(s: float) -> float:
    """
    Local DWL half-beam fraction along LWL parameter s in [0, 1].
    Fine wave-piercing entry, max beam ~55% LWL, mild tuck aft.
    """
    # Asymmetric pear: peak slightly aft to support LCB aft of midship.
    peak = 0.55
    if s < peak:
        t = s / peak
        shape = 1.0 - (1.0 - t) ** 2.05
    else:
        t = (s - peak) / (1.0 - peak)
        shape = 1.0 - 0.28 * t**1.35
    # sharpen extreme ends
    end_fade = smoothstep(0.0, 0.08, s) * smoothstep(1.0, 0.90, s)
    return max(0.015, shape * end_fade)


def section_half_breadth(s: float, z_frac: float) -> float:
    """
    Half-breadth at station parameter s (0 bow→1 stern on LWL) and
    vertical fraction z_frac (0=keel, 1=deck).
    Round bilge forward; slight flattening aft for dynamic lift.
    """
    b_dwl = 0.5 * MAX_BEAM * waterline_fraction(s)
    # deck wider than DWL slightly for crew/toe-rail volume
    b_deck = b_dwl * 1.08
    b_keel = b_dwl * 0.08

    # U→V shape factor: 0 = very V, 1 = boxy
    aft_flat = smoothstep(0.65, 1.0, s) * 0.45
    p = 1.55 - aft_flat  # exponent on sectional fullness

    if z_frac <= 0.0:
        return b_keel
    if z_frac >= 1.0:
        return b_deck

    # map keel→DWL→deck
    dwl_frac = DRAFT / DEPTH
    if z_frac <= dwl_frac:
        t = z_frac / dwl_frac
        # power curve from keel to DWL
        return b_keel + (b_dwl - b_keel) * (t**p)
    t = (z_frac - dwl_frac) / (1.0 - dwl_frac)
    # soft flare to deck
    return b_dwl + (b_deck - b_dwl) * (t**1.1)


def rocker(s: float) -> float:
    """Keel z above deepest point; positive rises ends (less draft at ends)."""
    # parabolic rocker with LCB bias
    mid = LCB_FRAC
    return 0.045 * ((s - mid) / max(mid, 1.0 - mid)) ** 2 * DEPTH


def generate_offsets() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for i in range(N_STATIONS):
        x = station_x(i)
        # map x to LWL parameter; overhangs taper
        x_fp = FP_OVERHANG
        x_ap = LOA - AP_OVERHANG
        if x < x_fp:
            s = 0.0
            overhang = (x_fp - x) / max(FP_OVERHANG, 1e-6)
            length_scale = 1.0 - 0.85 * overhang
        elif x > x_ap:
            s = 1.0
            overhang = (x - x_ap) / max(AP_OVERHANG, 1e-6)
            length_scale = 1.0 - 0.75 * overhang
        else:
            s = (x - x_fp) / LWL
            length_scale = 1.0

        z_keel = rocker(s)
        for j in range(N_WATERLINES):
            z_frac = j / (N_WATERLINES - 1)
            z = z_keel + z_frac * (DEPTH - z_keel)
            # normalize z_frac against local depth
            local_depth = DEPTH - z_keel
            zf = (z - z_keel) / local_depth if local_depth > 1e-9 else 0.0
            y = section_half_breadth(s, zf) * length_scale
            rows.append(
                {
                    "station": i,
                    "x_m": round(x, 4),
                    "s_lwl": round(s, 4),
                    "z_m": round(z, 4),
                    "y_half_m": round(y, 5),
                    "z_frac": round(zf, 4),
                }
            )
    return rows


def write_csv(rows: list[dict[str, float]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["station", "x_m", "s_lwl", "z_m", "y_half_m", "z_frac"],
        )
        w.writeheader()
        w.writerows(rows)


def estimate_volume(rows: list[dict[str, float]]) -> float:
    """Crude underwater volume of one demi-hull via station areas."""
    by_station: dict[int, list[dict[str, float]]] = {}
    for r in rows:
        by_station.setdefault(int(r["station"]), []).append(r)

    areas = []
    xs = []
    for st in sorted(by_station):
        pts = sorted(by_station[st], key=lambda r: r["z_m"])
        xs.append(pts[0]["x_m"])
        # trapezoid under DWL only
        a = 0.0
        for a_pt, b_pt in zip(pts, pts[1:]):
            z0, z1 = a_pt["z_m"], b_pt["z_m"]
            if z0 >= DRAFT and z1 >= DRAFT:
                continue
            y0 = a_pt["y_half_m"] if z0 < DRAFT else 0.0
            y1 = b_pt["y_half_m"] if z1 < DRAFT else 0.0
            zz0 = min(z0, DRAFT)
            zz1 = min(z1, DRAFT)
            a += (y0 + y1) * (zz1 - zz0)
        areas.append(2.0 * a)  # both sides

    vol = 0.0
    for i in range(len(areas) - 1):
        dx = xs[i + 1] - xs[i]
        vol += 0.5 * (areas[i] + areas[i + 1]) * dx
    return vol


def plot_lines(rows: list[dict[str, float]], path: Path) -> None:
    if not HAS_MPL:
        print("matplotlib not available — skipping plots")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    by_station: dict[int, list[dict[str, float]]] = {}
    for r in rows:
        by_station.setdefault(int(r["station"]), []).append(r)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    fig.suptitle("Vanguard F9 — demi-hull lines (concept)", fontsize=13)

    # Body plan (sections looking forward): y vs z, mirrored
    ax = axes[0]
    for st, pts in by_station.items():
        pts = sorted(pts, key=lambda r: r["z_m"])
        ys = [p["y_half_m"] for p in pts]
        zs = [p["z_m"] for p in pts]
        # alternate sides for readability
        sign = 1 if st % 2 == 0 else -1
        ax.plot([sign * y for y in ys], zs, color="steelblue", lw=0.9)
    ax.axhline(DRAFT, color="crimson", ls="--", lw=0.8, label="DWL")
    ax.set_aspect("equal")
    ax.set_title("Body plan")
    ax.set_xlabel("y (m)")
    ax.set_ylabel("z (m)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Profile: sheer / keel / DWL
    ax = axes[1]
    xs, z_keel, z_deck = [], [], []
    for st in sorted(by_station):
        pts = sorted(by_station[st], key=lambda r: r["z_m"])
        xs.append(pts[0]["x_m"])
        z_keel.append(pts[0]["z_m"])
        z_deck.append(pts[-1]["z_m"])
    ax.plot(xs, z_keel, label="keel", color="black")
    ax.plot(xs, z_deck, label="sheer", color="steelblue")
    ax.axhline(DRAFT, color="crimson", ls="--", lw=0.8, label="DWL")
    ax.set_aspect("equal")
    ax.set_title("Profile")
    ax.set_xlabel("x from FP (m)")
    ax.set_ylabel("z (m)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.invert_xaxis()  # bow left

    # Planform at DWL
    ax = axes[2]
    y_dwl = []
    x_dwl = []
    for st in sorted(by_station):
        pts = sorted(by_station[st], key=lambda r: r["z_m"])
        # interpolate half-breadth at DRAFT
        below = [p for p in pts if p["z_m"] <= DRAFT]
        above = [p for p in pts if p["z_m"] >= DRAFT]
        if not below or not above:
            y = pts[0]["y_half_m"]
        else:
            a, b = below[-1], above[0]
            if b["z_m"] == a["z_m"]:
                y = a["y_half_m"]
            else:
                t = (DRAFT - a["z_m"]) / (b["z_m"] - a["z_m"])
                y = a["y_half_m"] + t * (b["y_half_m"] - a["y_half_m"])
        x_dwl.append(pts[0]["x_m"])
        y_dwl.append(y)
    ax.plot(x_dwl, y_dwl, color="steelblue")
    ax.plot(x_dwl, [-y for y in y_dwl], color="steelblue")
    ax.set_aspect("equal")
    ax.set_title("Plan (DWL)")
    ax.set_xlabel("x from FP (m)")
    ax.set_ylabel("y (m)")
    ax.grid(True, alpha=0.3)
    ax.invert_xaxis()

    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"wrote {path}")


def plot_platform(path: Path) -> None:
    """Simple top-view of catamaran platform + foil spans."""
    if not HAS_MPL:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    beam_cl = 5.20
    foil_span = 1.35
    fig, ax = plt.subplots(figsize=(10, 5))
    # demi-hull centerlines
    for side, y0 in (("port", beam_cl / 2), ("stbd", -beam_cl / 2)):
        ax.add_patch(
            plt.Rectangle(
                (0, y0 - MAX_BEAM / 2),
                LOA,
                MAX_BEAM,
                fill=False,
                ec="steelblue",
                lw=1.2,
                label=side if side == "port" else None,
            )
        )
        # main foil (simplified L lateral arm inboard)
        ax.plot(
            [LOA * 0.42, LOA * 0.42],
            [y0, y0 - math.copysign(foil_span, y0)],
            color="crimson",
            lw=2,
        )
        # rudder
        ax.plot(
            [LOA * 0.92, LOA * 0.92],
            [y0 - 0.15, y0 + 0.15],
            color="darkorange",
            lw=2,
        )

    ax.plot([1.2, LOA - 0.8], [beam_cl / 2, beam_cl / 2], "k--", alpha=0.4)
    ax.plot([1.2, LOA - 0.8], [-beam_cl / 2, -beam_cl / 2], "k--", alpha=0.4)
    # beams
    for xb in (1.6, 6.8):
        ax.plot([xb, xb], [-beam_cl / 2, beam_cl / 2], color="gray", lw=3, alpha=0.7)

    ax.set_aspect("equal")
    ax.set_title("Vanguard F9 — platform & foil plan (concept)")
    ax.set_xlabel("x from FP (m)")
    ax.set_ylabel("y (m)")
    ax.set_xlim(-0.5, LOA + 0.5)
    ax.set_ylim(-beam_cl / 2 - foil_span - 0.3, beam_cl / 2 + foil_span + 0.3)
    ax.invert_xaxis()
    ax.grid(True, alpha=0.3)
    ax.text(LOA * 0.42, 0, "main foils", color="crimson", ha="center", fontsize=8)
    ax.text(LOA * 0.92, 0.5, "T-rudders", color="darkorange", ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"wrote {path}")


def main() -> None:
    rows = generate_offsets()
    csv_path = OUT_GEOM / "hull_offsets.csv"
    write_csv(rows, csv_path)
    vol = estimate_volume(rows)
    disp_kg = vol * 1025  # seawater
    print(f"wrote {csv_path}")
    print(f"approx one demi-hull canoe volume: {vol:.3f} m³ ({disp_kg:.0f} kg SW)")
    print(f"approx both hulls canoe buoyancy: {2 * disp_kg:.0f} kg SW")
    print(
        "note: racing mass ~470 kg flies on foils; hull volume is for takeoff/reserve."
    )

    plot_lines(rows, OUT_ART / "demi_hull_lines.png")
    plot_platform(OUT_ART / "platform_foil_plan.png")

    # summary sidecar
    summary = OUT_GEOM / "hull_summary.txt"
    summary.write_text(
        "\n".join(
            [
                "Vanguard F9 demi-hull summary",
                f"LOA={LOA} m  LWL={LWL} m  max beam={MAX_BEAM} m  draft={DRAFT} m",
                f"stations={N_STATIONS}  waterlines={N_WATERLINES}",
                f"approx canoe volume (one hull)={vol:.4f} m^3",
                f"approx canoe buoyancy (one hull, SW)={disp_kg:.1f} kg",
                f"approx canoe buoyancy (both, SW)={2 * disp_kg:.1f} kg",
                f"racing displacement target=470 kg (foiling)",
                "",
            ]
        )
    )
    print(f"wrote {summary}")


if __name__ == "__main__":
    main()
