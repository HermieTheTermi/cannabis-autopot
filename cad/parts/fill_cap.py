# ============================================================================
#  Kappe fuer den Einfuellstutzen - Druckteil (Port von case/modules.scad,
#  Modul fill_cap()).
#  Drucklage +Z, offene Seite nach oben; an der Stutzenmundebene montiert.
# ============================================================================

from build123d import (
    Align,
    Box,
    Cylinder,
    Pos,
    RigidJoint,
)
from params import *
from lib import restmaterial

NAME = "fill_cap"


def build():
    body = Cylinder(
        cap_od / 2, cap_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Zwei gegenueberliegende Greifrippen (greifen in den Mantel ein)
    for rx in (cap_od / 2 - cap_rib_t, -cap_od / 2 - cap_rib_t):
        body += Pos(rx, -cap_rib_w / 2, 0) * Box(
            2 * cap_rib_t, cap_rib_w, cap_h, align=(Align.MIN, Align.MIN, Align.MIN)
        )

    # Sackloch (Klemmsitz auf dem Stutzen), von oben bis 3 mm ueber den Boden
    body -= Pos(0, 0, cap_h - cap_depth) * Cylinder(
        cap_id / 2, cap_depth + 1, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Durchgaengiges Lueftungsloch im Deckel
    body -= Pos(0, 0, -1) * Cylinder(
        cap_vent_d / 2, cap_h + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # Schnittstelle zum Stutzenmund: Ebene des Sacklochgrunds (z = cap_h - cap_depth).
    # Die Kappe wird spaeter so auf die Mundebene gesetzt, dass die offene Seite
    # (+Z) zum Stutzen zeigt.
    RigidJoint("mouth", body, Pos(0, 0, cap_h - cap_depth))
    return body


def check(part):
    bb = part.bounding_box()
    vol = part.volume
    x_soll = cap_od + 2 * cap_rib_t
    y_soll = cap_od

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    assert abs(bb.min.X + x_soll / 2) < 0.01, "X-min falsch (Rippen aussen?)"
    assert abs(bb.max.X - x_soll / 2) < 0.01, "X-max falsch (Rippen aussen?)"
    assert abs(bb.min.Y + y_soll / 2) < 0.01, "Y-min falsch"
    assert abs(bb.max.Y - y_soll / 2) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z) < 0.01, "Z-min falsch"
    assert abs(bb.max.Z - cap_h) < 0.01, "Z-max falsch"

    # Sackloch offen (Sonde im Hohlraum, oberhalb des Deckels)
    sack = restmaterial(
        part,
        Pos(0, 0, cap_h - cap_depth + 0.2)
        * Cylinder(
            cap_id / 2 - 0.5,
            cap_depth - 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ),
    )
    print(f"[{NAME}] Sonde Sackloch: Restmaterial = {sack:.6f} mm^3")
    assert sack < 1e-6, "Sackloch nicht offen"

    # Deckel darunter massiv (Sonde abseits des Lueftungslochs)
    deckel = restmaterial(
        part,
        Pos(0, 0, 0.25)
        * Cylinder(5, 2.5, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(f"[{NAME}] Sonde Deckel: Restmaterial = {deckel:.1f} mm^3")
    assert deckel > 0, "Deckel nicht massiv"

    # Lueftungsloch durchgaengig offen
    vent = restmaterial(
        part,
        Pos(0, 0, -1)
        * Cylinder(
            cap_vent_d / 2 - 0.3,
            cap_h + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ),
    )
    print(f"[{NAME}] Sonde Lueftungsloch: Restmaterial = {vent:.6f} mm^3")
    assert vent < 1e-6, "Lueftungsloch nicht durchgaengig"

    return True
