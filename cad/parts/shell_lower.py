# ============================================================================
#  Aussenschale unten - Wassertank + Steckzapfen (Port von case/modules.scad)
#  Drucklage: unveraendert, z 0 ... split_z + spigot_h.
# ============================================================================

import math

from build123d import (
    Align,
    Cone,
    Cylinder,
    Pos,
    Rot,
)
from params import *
from lib import fill_axis, restmaterial

NAME = "shell_lower"


def _grid_ledge():
    """Auflagering fuer den Rost (im Tank, unterhalb des Rostes)."""
    outer = Cylinder(
        shell_ir, ledge_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    inner = Pos(0, 0, -1) * Cylinder(
        ledge_ir,
        ledge_h + 2,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return outer - inner


def _fill_neck():
    """Massivkoerper des Einfuellstutzens (von innen in der Wand bis Mundebene)."""
    p0, d = fill_axis()
    radius = (fill_bore_d + 2 * fill_wall) / 2
    base = p0 - fill_start * d
    return Pos(base) * Rot(90 - fill_ang, 0, 0) * Cylinder(
        radius,
        fill_start + fill_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )


def _fill_bore():
    """Bohrung inkl. kegeliger Trichterlippe am Mund (beidseitig ueberstehend)."""
    p0, d = fill_axis()
    rot = Rot(90 - fill_ang, 0, 0)
    straight_base = p0 - (fill_start + 2) * d
    straight = Pos(straight_base) * rot * Cylinder(
        fill_bore_d / 2,
        fill_start + fill_len + 4,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cone_base = p0 + (fill_len - fill_cs_len) * d
    cone = Pos(cone_base) * rot * Cone(
        bottom_radius=fill_bore_d / 2,
        top_radius=fill_mouth_d / 2,
        height=fill_cs_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    return straight + cone


def _axis_probe(radius, lo, hi):
    """Zylindersonde auf der Stutzenachse, in Achskoordinaten lo bis hi."""
    p0, d = fill_axis()
    base = p0 + lo * d
    return Pos(base) * Rot(90 - fill_ang, 0, 0) * Cylinder(
        radius, hi - lo, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def build():
    outer = Cylinder(
        shell_or, split_z, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    outer += Pos(0, 0, split_z) * Cylinder(
        spigot_or, spigot_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    outer += _fill_neck()

    inner = Pos(0, 0, floor_t) * Cylinder(
        shell_ir,
        split_z + spigot_h - floor_t + 1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body = outer - inner
    body += Pos(0, 0, ledge_z0) * _grid_ledge()
    body -= _fill_bore()
    return body


def check(part):
    bb = part.bounding_box()
    vol = part.volume
    neck_r = (fill_bore_d + 2 * fill_wall) / 2
    ang = math.radians(fill_ang)
    y_min = -shell_or - fill_len * math.cos(ang) - neck_r * math.sin(ang)

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    assert abs(bb.min.X + shell_or) < 0.01, "X-min falsch"
    assert abs(bb.max.X - shell_or) < 0.01, "X-max falsch"
    assert abs(bb.min.Y - y_min) < 0.01, f"Y-min falsch (erwartet {y_min:.3f})"
    assert abs(bb.max.Y - shell_or) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z) < 0.01, "Z-min < 0"
    assert abs(bb.max.Z - (split_z + spigot_h)) < 0.01, "Z-max falsch"

    assert bb.min.Z > -0.01, "Material unter z = 0"
    assert bb.max.Z < split_z + spigot_h + 0.01, "Material ueber Bauraum"

    # Bohrung offen (Sonde kleiner als die lichte Bohrung)
    offen = restmaterial(part, _axis_probe(fill_bore_d / 2 - 1, -fill_start - 2, fill_len + 2))
    print(f"[{NAME}] Sonde Bohrung offen: Restmaterial = {offen:.6f} mm^3")
    assert offen < 1e-6, "Bohrung nicht offen"

    # Wand daneben vorhanden (Sonde groesser als die Bohrung)
    wand = restmaterial(part, _axis_probe(fill_bore_d / 2 + 3, -fill_start, fill_len))
    print(f"[{NAME}] Sonde Stutzenwand: Restmaterial = {wand:.1f} mm^3")
    assert wand > 0, "keine Stutzenwand gefunden"

    # Nichts im Tankinneren ausser der Rostauflage
    inner_probe = Pos(0, 0, floor_t) * Cylinder(
        shell_ir - 0.5,
        split_z - floor_t,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    inner_rest = restmaterial(part, inner_probe)
    ledge_teil = math.pi * ((shell_ir - 0.5) ** 2 - ledge_ir**2) * ledge_h
    print(
        f"[{NAME}] Sonde Tankinneres (r={shell_ir - 0.5}): Restmaterial = "
        f"{inner_rest:.1f} mm^3 (Rostauflage-Anteil erwartet {ledge_teil:.1f})"
    )
    assert abs(inner_rest - ledge_teil) < 0.02 * ledge_teil, (
        "Material im Tankinneren ausserhalb der Rostauflage"
    )

    # Rostauflage frei (Ring bleibt stehen, Innenraum-Schnitt hat dort geraeumt)
    ledge_probe = Pos(0, 0, ledge_z0) * Cylinder(
        shell_ir, ledge_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    ledge_vol = restmaterial(part, ledge_probe)
    ledge_soll = math.pi * (shell_ir**2 - ledge_ir**2) * ledge_h
    print(
        f"[{NAME}] Sonde Rostauflage: Restmaterial = {ledge_vol:.1f} mm^3 "
        f"(erwartet {ledge_soll:.1f})"
    )
    assert abs(ledge_vol - ledge_soll) < 0.02 * ledge_soll, "Rostauflage fehlt"

    # Interferenzprobe gegen die (in Montagelage zurueckgeschobene) obere Schale
    from . import shell_upper

    upper_hoch = Pos(0, 0, split_z) * shell_upper.build()
    schnitt = restmaterial(part, upper_hoch)
    print(f"[{NAME}] Interferenz mit shell_upper (montiert): Volumen = {schnitt:.6f} mm^3")
    assert schnitt < 1e-3, "shell_lower und shell_upper durchdringen sich"

    return True
