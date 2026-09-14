# ============================================================================
#  Innentopf mit Giessfuessen und Drainageloechern (Port von case/modules.scad)
#  Geometrie 1:1 im Lokalkoordinatensystem des SCAD-Moduls: Boden bei z = 0,
#  die sechs Giessfuesse reichen bis z = -foot_h unter null. Die Montage
#  setzt den Topf spaeter per Offset/Joint auf den Rost.
# ============================================================================

import math

from build123d import (
    Align,
    Box,
    Cylinder,
    Pos,
    RigidJoint,
    Rot,
)
from params import *
from lib import hole_grid, restmaterial

NAME = "inner_pot"


def _drain_holes():
    """Drainagebohrungen im Boden (Zylinderliste fuer die Subtraktion).

    hole_grid im SCAD liegt um 1 nach unten versetzt; das entspricht
    z0 = -1 mit Hoehe pot_floor_t + 2.
    """
    return hole_grid(
        pot_ir - 6, drain_hole_d, drain_pitch, -1, pot_floor_t + 2
    )


def _hose_passage():
    """Schlauchdurchlass am Rand oben (+Y, Richtung Wulst).

    Im SCAD ein achsenparalleler Cube; hier als Box mit MIN-Ausrichtung.
    """
    return Pos(-pot_hose_w / 2, pot_ir - 1, pot_h - pot_hose_h) * Box(
        pot_hose_w,
        (pot_or - pot_ir) + 2,
        pot_hose_h + 1,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )


def _feet():
    """Sechs Giessfuesse, gleichmaessig ueber den Umfang verteilt."""
    feet = []
    for i in range(n_feet):
        foot = Pos(foot_r - foot_d / 2, 0, -foot_h) * Box(
            foot_d,
            foot_w,
            foot_h + 1,
            align=(Align.MIN, Align.MIN, Align.MIN),
        )
        feet.append(Rot(0, 0, i * 360.0 / n_feet) * foot)
    return feet


def build():
    body = Cylinder(
        pot_or, pot_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    body -= Pos(0, 0, pot_floor_t) * Cylinder(
        pot_ir,
        pot_h - pot_floor_t + 1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body -= _drain_holes()
    body -= _hose_passage()

    for foot in _feet():
        body += foot

    # Schnittstellen (RigidJoints): Fussboden (Unterkante der Giessfuesse, lokal
    # z = -foot_h) auf dem Rost, Oberkante als Auflage des Verteilerrings.
    RigidJoint("fussboden", body, Pos(0, 0, -foot_h))
    RigidJoint("oberkante", body, Pos(0, 0, pot_h))
    return body


def check(part):
    bb = part.bounding_box()
    vol = part.volume
    drains = _drain_holes()

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )
    print(f"[{NAME}] Drainagebohrungen = {len(drains)}")

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    assert abs(bb.min.X + pot_or) < 0.01, "X-min falsch"
    assert abs(bb.max.X - pot_or) < 0.01, "X-max falsch"
    assert abs(bb.min.Y + pot_or) < 0.01, "Y-min falsch"
    assert abs(bb.max.Y - pot_or) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z + foot_h) < 0.01, "Z-min falsch (Fuesse)"
    assert abs(bb.max.Z - pot_h) < 0.01, "Z-max falsch"

    # Jede Drainagebohrung ist offen (Sonde: Durchmesser drain_hole_d - 0,6).
    # Das SCAD vereinigt die Giessfuesse NACH dem Bohren; die Fuesse ragen
    # 1 mm (foot_h + 1) in den Boden und ueberdecken dort einzelne Bohrungen
    # im untersten Millimeter. Fuer diese wird der freie Kanal oberhalb der
    # Fusssohle geprueft.
    r_probe = (drain_hole_d - 0.6) / 2
    fuss_oben = foot_h + 1 - foot_h  # = 1.0 mm, Oberkante der Fuesse
    z_frei = fuss_oben + 0.05
    ueberdeckt = 0
    for hole in drains:
        c = hole.bounding_box().center()
        rest = restmaterial(
            part,
            Pos(c.X, c.Y, -1)
            * Cylinder(
                r_probe,
                pot_floor_t + 2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ),
        )
        if rest < 1e-6:
            continue
        offen = restmaterial(
            part,
            Pos(c.X, c.Y, z_frei)
            * Cylinder(
                r_probe,
                pot_floor_t + 2 - z_frei,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ),
        )
        assert offen < 1e-6, f"Drainagebohrung bei ({c.X:.1f}, {c.Y:.1f}) zu"
        ueberdeckt += 1
    print(
        f"[{NAME}] davon von Giessfuessen ueberdeckt (nur unterste 1 mm) = "
        f"{ueberdeckt}, oberhalb davon frei = {len(drains) - ueberdeckt}"
    )

    # Zwischen zwei benachbarten Bohrungen (x = 0 und x = drain_pitch) ist
    # Material (Boden).
    zwischen = restmaterial(
        part,
        Pos(drain_pitch / 2, 0, 0)
        * Cylinder(1.0, pot_floor_t, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(f"[{NAME}] Sonde zwischen zwei Bohrungen: Restmaterial = {zwischen:.3f} mm^3")
    assert zwischen > 0, "kein Material zwischen zwei Drainagebohrungen"

    # Schlauchdurchlass am Rand oben (+Y) ist offen
    durchlass = restmaterial(
        part,
        Pos(-pot_hose_w / 2 + 1, pot_ir + 0.5, pot_h - pot_hose_h + 1)
        * Box(
            pot_hose_w - 2,
            (pot_or - pot_ir) - 1,
            pot_hose_h - 1,
            align=(Align.MIN, Align.MIN, Align.MIN),
        ),
    )
    print(f"[{NAME}] Sonde Schlauchdurchlass (+Y): Restmaterial = {durchlass:.6f} mm^3")
    assert durchlass < 1e-6, "Schlauchdurchlass nicht offen"

    # Fuss vorhanden (Sonde im Fuss, in dessen tangentialer Mitte) ...
    fuss = restmaterial(
        part,
        Pos(foot_r, foot_w / 2, -foot_h + foot_h / 2)
        * Cylinder(1.5, 5, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(f"[{NAME}] Sonde im Giessfuss: Restmaterial = {fuss:.3f} mm^3")
    assert fuss > 0, "kein Material im Giessfuss"

    # ... und zwischen zwei Fuessen unterhalb des Topfbodens leer
    a = math.radians(360.0 / n_feet / 2)
    leer = restmaterial(
        part,
        Pos(foot_r * math.cos(a), foot_r * math.sin(a), -foot_h + foot_h / 2)
        * Cylinder(1.5, 5, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(f"[{NAME}] Sonde zwischen zwei Fuessen: Restmaterial = {leer:.6f} mm^3")
    assert leer < 1e-6, "Material zwischen zwei Fuessen"

    return True
