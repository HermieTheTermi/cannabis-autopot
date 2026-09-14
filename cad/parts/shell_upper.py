# ============================================================================
#  Aussenschale oben - Wulst + Kragen + Stecksockel (Port von case/modules.scad)
#  Drucklage: die SCAD-Teil-Datei verschiebt um -split_z; daher wird hier in
#  Montagekoordinaten (z 90 ... 278) gebaut und am Ende nach unten geschoben
#  (Ergebnis z 0 ... 188, LST-Bohrungen bei 179,5 / 184,5).
# ============================================================================

import math

from build123d import (
    Align,
    Box,
    Cylinder,
    Pos,
    RectangleRounded,
    RigidJoint,
    Rot,
    Vector,
    extrude,
    loft,
)
from params import *
from lib import restmaterial, wulst_footprint_2d

NAME = "shell_upper"


def _wulst_envelope():
    """Stuetztragfreier Wulstkoerper: 45-Grad-Fase als ruled loft, darueber
    der volle Grundriss (1:1 zur hull()-Konstruktion in modules.scad).

    Der Ansatz an der Wand ist im SCAD ein Rechteck 60 x 2. Damit OCCT die
    Kanten der beiden Querschnitte eindeutig paart, wird er als abgerundetes
    Rechteck mit verschwindendem Radius gezeichnet (loft erzeugt dann exakt
    die konvexe Huelle).
    """
    eps = 1e-3
    s_ansatz = Pos(0, shell_or - 1, wulst_z0) * RectangleRounded(
        wulst_w, 2, eps
    )
    s_grundriss = Pos(0, 0, wulst_z0 + wulst_taper) * wulst_footprint_2d()
    s_oben = Pos(0, 0, wulst_z1) * wulst_footprint_2d()
    return loft([s_ansatz, s_grundriss, s_oben], ruled=True)


def _wulst_cavity():
    """Elektronikkammer (nach vorne offen, fuer den Deckel)."""
    return Pos(-wc_x, wc_y0, wc_z0) * Box(
        2 * wc_x,
        wc_y1 - wc_y0,
        wc_z1 - wc_z0,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )


def _wulst_bosses():
    """Deckel-Verschraubungsposten (innen an der Rueckwand)."""
    height = (wulst_y_outer - 8) - wc_y0
    bosses = []
    for x in (-boss_x, boss_x):
        for z in boss_z:
            bosses.append(
                Pos(x, wc_y0, z)
                * Rot(-90, 0, 0)
                * Cylinder(
                    boss_d / 2,
                    height,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
            )
    return bosses


def _wulst_drip_lip():
    """Tropfkante am Wulstboden (unterbricht den Wasserfilm an der Aussenwand)."""
    outer = Pos(0, 0, drip_z) * extrude(
        wulst_footprint_2d(drip_band), amount=drip_h
    )
    inner = Pos(0, 0, drip_z - 1) * extrude(
        wulst_footprint_2d(), amount=drip_h + 2
    )
    return outer - inner


def _collar_ring():
    """Kragen / Auflagering."""
    outer = Pos(0, 0, collar_z0) * Cylinder(
        collar_r, collar_h, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    inner = Pos(0, 0, collar_z0 - 1) * Cylinder(
        shell_ir, collar_h + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return outer - inner


def _lst_layout():
    """(row, world_winkel_grad, z_montage) aller LST-Bohrungen.

    Korrigierte Orientierung: world = 0 Grad liegt auf +X, der Kragenausschnitt
    (+Y) liegt bei 90 Grad. Eine Bohrung entfaellt, wenn ihr world-Winkel naeher
    als lst_gap_deg an 90 Grad liegt.
    """
    layout = []
    for row in range(lst_rows):
        z = lst_row_z[row]
        off = (row % 2) * (180.0 / lst_holes)
        for i in range(lst_holes):
            world = off + i * 360.0 / lst_holes
            da = min(abs(world - 90.0), 360.0 - abs(world - 90.0))
            if da >= lst_gap_deg:
                layout.append((row, world, z))
    return layout


def _lst_holes():
    """Radiale Bohrungen durch den Kragen (aussen beginnend an r = shell_ir - 1)."""
    holes = []
    for _row, world, z in _lst_layout():
        a = math.radians(world)
        start = Vector((shell_ir - 1) * math.cos(a), (shell_ir - 1) * math.sin(a), z)
        holes.append(
            Pos(start)
            * Rot(0, 0, world)
            * Rot(0, 90, 0)
            * Cylinder(
                lst_hole_d / 2,
                lst_drill_len,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        )
    return holes


def build():
    body = Pos(0, 0, split_z) * Cylinder(
        shell_or, total_h - split_z, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    body += _wulst_envelope()
    body += _collar_ring()

    # Stecksockel (groesserer Freistich am unteren Rand)
    body -= Pos(0, 0, split_z) * Cylinder(
        socket_ir, spigot_h + 0.01, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    # Hauptkavitaet
    body -= Pos(0, 0, split_z + spigot_h) * Cylinder(
        shell_ir,
        total_h - split_z - spigot_h + 1,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    body -= _wulst_cavity()
    body += _wulst_bosses()
    body += _wulst_drip_lip()

    cuts = []
    # Schlauchkanal (Saug- und Druckschlauch) durch Mantel + Wulst
    cuts.append(
        Pos(-hose_w / 2, shell_or - 10, hose_z - hose_w / 2)
        * Box(hose_w, 16, hose_w, align=(Align.MIN, Align.MIN, Align.MIN))
    )
    # Sensorkabelkanal
    cuts.append(
        Pos(0, shell_or - 10, cable_z)
        * Rot(-90, 0, 0)
        * Cylinder(cable_d / 2, 16, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )
    # Druckschlauch-Austritt nach oben
    cuts.append(
        Pos(pressure_x, pressure_y, wulst_z1 - 8)
        * Cylinder(
            pressure_hole_d / 2,
            14,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    )
    # Kragenausschnitt fuer den Sensorkabelaustritt
    cuts.append(
        Pos(-3.5, shell_or - 10, collar_z0 + 2)
        * Box(7, 16, collar_h + 4, align=(Align.MIN, Align.MIN, Align.MIN))
    )
    # LST-Ankerloecher im Kragen
    cuts += _lst_holes()
    # Deckelgewinde (Pilotbohrungen)
    for x in (-boss_x, boss_x):
        for z in boss_z:
            cuts.append(
                Pos(x, shell_or, z)
                * Rot(-90, 0, 0)
                * Cylinder(
                    boss_hole_d / 2,
                    wulst_y_outer - shell_or + 2,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )
            )
    body -= cuts

    # Drucklage: um split_z nach unten geschoben, der Ursprung z = 0 ist die
    # Trennebene. Die Joints stellen daher die Montagelage her:
    # deckflaeche - Trennebene zur unteren Schale (Montage z = split_z)
    # kragen      - Kragenoberkante als Auflage der Abdeckung (Montage z = total_h)
    body = Pos(0, 0, -split_z) * body
    RigidJoint("deckflaeche", body, Pos(0, 0, 0))
    RigidJoint("kragen", body, Pos(0, 0, total_h - split_z))
    return body


def _hole_probe(world, z_montage, radius, length):
    """Radiale Sonde durch den Kragen (Druckkoordinaten)."""
    a = math.radians(world)
    start = Vector((shell_ir - 1) * math.cos(a), (shell_ir - 1) * math.sin(a), z_montage - split_z)
    return (
        Pos(start)
        * Rot(0, 0, world)
        * Rot(0, 90, 0)
        * Cylinder(radius, length, align=(Align.CENTER, Align.CENTER, Align.MIN))
    )


def check(part):
    bb = part.bounding_box()
    vol = part.volume
    layout = _lst_layout()
    je_reihe = [sum(1 for row, _w, _z in layout if row == r) for r in range(lst_rows)]

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )
    print(f"[{NAME}] LST-Bohrungen je Reihe = {je_reihe}  (Summe {len(layout)})")

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    assert abs(bb.min.X + collar_r) < 0.01, "X-min falsch"
    assert abs(bb.max.X - collar_r) < 0.01, "X-max falsch"
    assert abs(bb.min.Y + collar_r) < 0.01, "Y-min falsch"
    assert abs(bb.max.Y - (wulst_y_outer + drip_band)) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z) < 0.01, "Z-min falsch (Drucklage)"
    assert abs(bb.max.Z - (total_h - split_z)) < 0.01, "Z-max falsch (Drucklage)"

    # 47 LST-Bohrungen: je erwarteter Bohrung eine Sonde, dazwischen Material
    r_probe = lst_hole_d / 2 - 0.2
    for row, world, z in layout:
        rest = restmaterial(part, _hole_probe(world, z, r_probe, lst_drill_len))
        assert rest < 1e-6, f"LST-Bohrung zu (Reihe {row}, {world:.1f} Grad)"
    # Zwischen zwei Bohrungen der ersten Reihe (halbe Teilung) ist Material
    zwischen = restmaterial(
        part,
        _hole_probe(360.0 / lst_holes / 2, lst_row_z[0], r_probe, lst_drill_len),
    )
    print(f"[{NAME}] Sonde zwischen zwei LST-Bohrungen: Restmaterial = {zwischen:.1f} mm^3")
    assert zwischen > 0, "kein Material zwischen den LST-Bohrungen"

    # Kragenausschnitt (+Y = 90 Grad) ist frei
    ausschnitt = restmaterial(
        part,
        _hole_probe(90.0, collar_z0 + collar_h / 2, 1.5, (collar_r - shell_ir) + 2),
    )
    print(f"[{NAME}] Sonde Kragenausschnitt (+Y): Restmaterial = {ausschnitt:.6f} mm^3")
    assert ausschnitt < 1e-6, "Kragenausschnitt nicht frei"

    return True
