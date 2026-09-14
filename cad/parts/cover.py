# ============================================================================
#  Optionale Substrat-Abdeckung - Druckteil (Port von case/modules.scad,
#  Modul cover()).
# ============================================================================

import math

from build123d import (
    Align,
    Box,
    Cylinder,
    Pos,
    RigidJoint,
)
from params import *
from lib import restmaterial

NAME = "cover"


def build():
    body = Cylinder(
        cover_od / 2, cover_t, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Mittelloch fuer die Pflanze
    body -= Pos(0, 0, -1) * Cylinder(
        cover_hole / 2,
        cover_t + 2,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    # Kragenausschnitt (+Y) fuer Kabel-/Schlauchaustritt
    body -= Pos(-4, shell_or - 14, -1) * Box(
        8, 16, cover_t + 2, align=(Align.MIN, Align.MIN, Align.MIN)
    )

    # Schnittstelle zum Kragen: Auflageflaeche auf der Unterseite (z = 0)
    RigidJoint("seat", body, Pos(0, 0, 0))
    return body


def check(part):
    bb = part.bounding_box()
    vol = part.volume

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    assert abs(bb.min.X + cover_od / 2) < 0.01, "X-min falsch"
    assert abs(bb.max.X - cover_od / 2) < 0.01, "X-max falsch"
    assert abs(bb.min.Y + cover_od / 2) < 0.01, "Y-min falsch"
    # Der Kragenausschnitt (x -4..4) nimmt am +Y-Rand die breiteste Stelle weg;
    # der hoechste verbleibende Punkt liegt bei x = 4 auf dem Kreis.
    y_max_soll = math.sqrt((cover_od / 2) ** 2 - 4.0**2)
    assert abs(bb.max.Y - y_max_soll) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z) < 0.01, "Z-min falsch"
    assert abs(bb.max.Z - cover_t) < 0.01, "Z-max falsch"

    # Mittelloch offen
    mitte = restmaterial(
        part,
        Pos(0, 0, -1)
        * Cylinder(
            cover_hole / 2 - 0.5,
            cover_t + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ),
    )
    print(f"[{NAME}] Sonde Mittelloch: Restmaterial = {mitte:.6f} mm^3")
    assert mitte < 1e-6, "Mittelloch nicht offen"

    # Kragenausschnitt offen (Kanal x -4..4, y 56..72)
    ausschnitt = restmaterial(
        part,
        Pos(-3, 57, -1) * Box(6, 8, cover_t + 2, align=(Align.MIN, Align.MIN, Align.MIN)),
    )
    print(f"[{NAME}] Sonde Kragenausschnitt: Restmaterial = {ausschnitt:.6f} mm^3")
    assert ausschnitt < 1e-6, "Kragenausschnitt nicht offen"

    # Sonst massiv: Material zwischen Mittelloch und Rand
    massiv = restmaterial(
        part,
        Pos(35, 0, -1) * Box(10, 10, cover_t + 2, align=(Align.MIN, Align.MIN, Align.MIN)),
    )
    print(f"[{NAME}] Sonde massiver Ring: Restmaterial = {massiv:.1f} mm^3")
    assert massiv > 0, "Abdeckung nicht massiv"

    return True
