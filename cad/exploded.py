#!/usr/bin/env python
# ============================================================================
#  Smart Grow Topf - Explosionsansicht aller 8 Druckteile.
#
#  Die Teile werden ueber die vorhandenen Module (parts/*.py) gebaut und wie in
#  assembly.py ueber die benannten RigidJoints in Montagelage gebracht
#  (connect_to verschiebt jeweils das zweite Teil). Danach wird jedes Teil um
#  seinen Explosionsvektor verschoben. Ergebnis: Compound nach
#  cad/export/exploded.step und cad/export/exploded.stl.
#
#  Render:
#  f3d --output=/tmp/exploded.png --resolution=1500,1100 \
#      --camera-position=-850,-1130,1150 --camera-focal-point=0,0,380 \
#      --camera-view-up=0,0,1 cad/export/exploded.stl
# ============================================================================

import sys
from pathlib import Path

from build123d import Compound, Pos, Rot, export_step, export_stl

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from params import *  # noqa: E402
from lib import fill_axis, restmaterial  # noqa: E402
from parts import (  # noqa: E402
    cover,
    distribution_ring,
    fill_cap,
    grid,
    inner_pot,
    shell_lower,
    shell_upper,
    wulst_lid,
)

EXPORT_DIR = ROOT / "export"
NAME = "exploded"

# Explosionsabstaende (mm), benannte Konstanten - keine Magic Numbers im Code.
# Der senkrechte Stapel wird je Schritt um EXPLODE_Z gestaffelt. Die Huelle
# (shell_upper) muss so weit hoch, dass sie die Abdeckung (cover_od 136 >
# Innenradius der Huelle 134) nicht durchdringt: 4*EXPLODE_Z + 188 + Reserve.
EXPLODE_Z = 60.0
EXPLODE_SHELL = 450.0
EXPLODE_LID = 45.0
EXPLODE_CAP = 40.0
MINDESTABSTAND = 5.0


def build():
    lower = shell_lower.build()
    upper = shell_upper.build()
    gitter = grid.build()
    pot = inner_pot.build()
    ring = distribution_ring.build()
    kappe = fill_cap.build()
    lid = wulst_lid.build()
    abdeckung = cover.build()

    # ---- Montagelage ausschliesslich ueber connect_to() ---------------------
    # connect_to verschiebt das jeweils zweite Teil, exakt wie in assembly.py.
    # shell_upper liegt in Drucklage und wandert durch den deckflaeche-Joint
    # zurueck in die Montagelage (z = split_z).
    lower.joints["deckflaeche"].connect_to(upper.joints["deckflaeche"])
    lower.joints["rostauflage"].connect_to(gitter.joints["rostauflage"])
    gitter.joints["rostoberseite"].connect_to(pot.joints["fussboden"])
    pot.joints["oberkante"].connect_to(ring.joints["auflage"])
    lower.joints["mundebene"].connect_to(kappe.joints["mouth"])
    # Abdeckung auf der Kragenoberkante (nicht Teil der Ansicht in assembly.py).
    upper.joints["kragen"].connect_to(abdeckung.joints["seat"])

    # Wulstdeckel liegt flach gedruckt; in Montagelage steht seine Dicke in +Y,
    # die Dichtflaeche schliesst die Wulstoeffnung an wulst_y_outer.
    lid = Pos(0, wulst_y_outer + lid_t, wulst_z0 + wulst_h / 2) * Rot(90, 0, 0) * lid

    # ---- Explosionsvektoren -------------------------------------------------
    _, d = fill_axis()
    teile = [
        (lower, "shell_lower", (0.0, 0.0, 0.0)),
        (gitter, "grid", (0.0, 0.0, EXPLODE_Z)),
        (pot, "inner_pot", (0.0, 0.0, 2 * EXPLODE_Z)),
        (ring, "distribution_ring", (0.0, 0.0, 3 * EXPLODE_Z)),
        (abdeckung, "cover", (0.0, 0.0, 4 * EXPLODE_Z)),
        (upper, "shell_upper", (0.0, 0.0, EXPLODE_SHELL)),
        # Der Wulstdeckel gehoert zur Wulst der oberen Schale: er bekommt
        # zusaetzlich deren Z-Versatz, damit er neben der Wulstoeffnung oben
        # sitzt und nicht allein mitten im Stapel haengt.
        (lid, "wulst_lid", (0.0, EXPLODE_LID, EXPLODE_SHELL)),
        (kappe, "fill_cap", (EXPLODE_CAP * d.X, EXPLODE_CAP * d.Y, EXPLODE_CAP * d.Z)),
    ]

    kinder = []
    for teil, label, vektor in teile:
        teil = Pos(*vektor) * teil
        teil.label = label
        kinder.append(teil)
    return Compound(children=kinder)


def _intersection_volume(a, b):
    """Volumen der Durchdringung a geschnitten b (0, wenn leer)."""
    return restmaterial(a, b)


def check(exploded):
    kinder = list(exploded.children)
    print(f"[{NAME}] Teile = {len(kinder)}")
    print(f"[{NAME}] Volumen = {exploded.volume / 1000:.2f} cm^3")

    bb = exploded.bounding_box()
    print(
        f"[{NAME}] bbox X {bb.min.X:.1f}..{bb.max.X:.1f}"
        f"  Y {bb.min.Y:.1f}..{bb.max.Y:.1f}"
        f"  Z {bb.min.Z:.1f}..{bb.max.Z:.1f}"
    )

    for teil in kinder:
        assert teil.is_valid is True, f"Teil ungueltig: {teil.label}"

    assert len(kinder) == 8, f"erwartet 8 Druckteile, gefunden {len(kinder)}"

    # ---- Interferenz- und Abstandspruefung ----------------------------------
    kleinster = float("inf")
    print(f"[{NAME}] Interferenz-/Abstandspruefung ({len(kinder)} Teile):")
    for i in range(len(kinder)):
        for j in range(i + 1, len(kinder)):
            a, b = kinder[i], kinder[j]
            vol = _intersection_volume(a, b)
            assert vol < 1e-3, f"Interferenz {a.label}/{b.label}: {vol} mm^3"
            dist = a.distance(b)
            kleinster = min(kleinster, dist)
            print(f"[{NAME}]   {a.label} <-> {b.label}: Abstand {dist:.3f} mm")
    print(
        f"[{NAME}] kleinster Abstand = {kleinster:.3f} mm"
        f" (muss > {MINDESTABSTAND:.1f} sein)"
    )
    assert kleinster > MINDESTABSTAND, "Teile liegen zu dicht beieinander"
    return True


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    exploded = build()
    check(exploded)
    export_step(exploded, EXPORT_DIR / f"{NAME}.step")
    export_stl(
        exploded,
        EXPORT_DIR / f"{NAME}.stl",
        tolerance=0.001,
        angular_tolerance=0.1,
    )
    print(
        f"[{NAME}] exportiert: {EXPORT_DIR / (NAME + '.step')}, "
        f"{EXPORT_DIR / (NAME + '.stl')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
