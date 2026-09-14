#!/usr/bin/env python
# ============================================================================
#  Smart Grow Topf - montierte Baugruppe aus RigidJoints.
#
#  Die Teilmodule aus Teil 1/2 definieren (noch) keine Joints; sie werden
#  daher hier direkt am gebauten Teil nachgetragen. Die Verbindungen folgen
#  1:1 case/assembly.scad: grid auf grid_z0, inner_pot auf pot_z0,
#  shell_upper auf split_z, distribution_ring auf pot_z1, Kappe auf der
#  Mundebene des Einfuellstutzens. Ansichts-Marker (Sensor, Kabel, Schlauch)
#  gehoeren nicht zur Baugruppe.
# ============================================================================

import sys
from pathlib import Path

from build123d import (
    Align,
    Compound,
    Cylinder,
    Pos,
    RigidJoint,
    Rot,
    export_step,
    export_stl,
)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from params import *  # noqa: E402
from lib import fill_axis, fill_mouth_center, restmaterial  # noqa: E402
from parts import (  # noqa: E402
    distribution_ring,
    fill_cap,
    grid,
    inner_pot,
    shell_lower,
    shell_upper,
)

EXPORT_DIR = ROOT / "export"
NAME = "assembly"


def _joint(part, label, location):
    """Traegt einen benannten RigidJoint am gebauten Teil nach."""
    RigidJoint(label, part, location)
    return part


def build():
    lower = shell_lower.build()
    upper = shell_upper.build()
    gitter = grid.build()
    pot = inner_pot.build()
    ring = distribution_ring.build()
    kappe = fill_cap.build()

    for teil, label in (
        (lower, "shell_lower"),
        (upper, "shell_upper"),
        (gitter, "grid"),
        (pot, "inner_pot"),
        (ring, "distribution_ring"),
        (kappe, "fill_cap"),
    ):
        teil.label = label

    # ---- Schnittstellen der Teile (RigidJoints) -----------------------------
    # shell_lower: Trennebene, Rostauflage, Stutzenmundebene
    _joint(lower, "split_top", Pos(0, 0, split_z))
    _joint(lower, "grid_seat", Pos(0, 0, grid_z0))
    _joint(
        lower,
        "fill_mouth",
        Pos(fill_mouth_center()) * Rot(270 - fill_ang, 0, 0),
    )
    # shell_upper liegt in Drucklage (um split_z nach unten verschoben): der
    # Ursprung z = 0 ist die Trennebene.
    _joint(upper, "split_bottom", Pos(0, 0, 0))
    # grid: Unter- und Oberseite
    _joint(gitter, "bottom", Pos(0, 0, 0))
    _joint(gitter, "top", Pos(0, 0, grid_t))
    # inner_pot: Fussboden (unter z = 0) und Oberkante
    _joint(pot, "feet", Pos(0, 0, -foot_h))
    _joint(pot, "top", Pos(0, 0, pot_h))
    # distribution_ring: Auflageflaeche
    _joint(ring, "bottom", Pos(0, 0, 0))

    # ---- Montage ausschliesslich ueber connect_to() -------------------------
    # connect_to verschiebt das jeweils zweite Teil.
    lower.joints["split_top"].connect_to(upper.joints["split_bottom"])
    lower.joints["grid_seat"].connect_to(gitter.joints["bottom"])
    gitter.joints["top"].connect_to(pot.joints["feet"])
    pot.joints["top"].connect_to(ring.joints["bottom"])
    # Kappe: die Joints sind so definiert, dass sich exakt die Lage aus
    # assembly.scad ergibt (Kappe sitzt mit Klemmsitz auf dem Stutzen).
    lower.joints["fill_mouth"].connect_to(kappe.joints["mouth"])

    return Compound(children=[lower, upper, gitter, pot, ring, kappe])


def _intersection_volume(a, b):
    """Volumen der Durchdringung a geschnitten b (0, wenn leer)."""
    return restmaterial(a, b)


def _neck_solid():
    """Massivzylinder des Einfuellstutzens (nur fuer die Klemmsitz-Zahl)."""
    p0, d = fill_axis()
    base = p0 - fill_start * d
    return Pos(base) * Rot(90 - fill_ang, 0, 0) * Cylinder(
        (fill_bore_d + 2 * fill_wall) / 2,
        fill_start + fill_len,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )


# Zulaessige Durchdringungen. Der eigentliche Auftrags-Fall ist der Klemmsitz
# der Kappe auf dem Stutzen (0,2 mm Uebermass). Tankwand, Wulst-Tropfkante und
# Rostrand ueberlappen in der SCAD-Vorlage ebenso; die Zahlen wurden am
# gerenderten SCAD gegengeprueft (siehe Kommentar, SCAD-Messwerte).
AUSNAHMEN = {
    frozenset(("shell_lower", "fill_cap")): (
        260.0,
        "Klemmsitz Kappe/Stutzen (0,2 mm Uebermass); zusaetzlich Anlage des "
        "Kappenrands an der Tankwand (SCAD-Messwert 224,4 mm^3)",
    ),
    frozenset(("shell_upper", "inner_pot")): (
        20.0,
        "Wulst-Tropfkante (1,6-mm-Band) trifft Innentopfwand "
        "(SCAD-Messwert 14,5 mm^3)",
    ),
    frozenset(("grid", "fill_cap")): (
        1.0,
        "Kappenrand am Rostrand (SCAD-Messwert 0,13 mm^3)",
    ),
}


def check(assembly):
    print(f"[{NAME}] Volumen = {assembly.volume / 1000:.2f} cm^3")
    bb = assembly.bounding_box()
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )
    print(
        f"[{NAME}] erwartet: X/Y innerhalb +/-{wulst_y_outer:.1f}"
        f" (+ Tropfkante), z 0..{total_h:.0f}"
    )

    # Einzelteile gueltig
    for teil in assembly.children:
        assert teil.is_valid is True, f"Teil ungueltig: {teil.label}"

    assert abs(bb.min.Z) < 0.01, "Z-min != 0"
    # Der Verteilerring liegt bei pot_z1 auf; sein Oberrand ist pot_z1 + ring_h
    # und ragt damit 4 mm ueber die Kragenoberkante (total_h) hinaus (in der
    # SCAD-Vorlage genauso).
    z_max = pot_z1 + ring_h
    print(
        f"[{NAME}] Z-max = {bb.max.Z:.3f} (Ringoberkante pot_z1+ring_h = {z_max:.1f},"
        f" total_h = {total_h:.1f})"
    )
    assert abs(bb.max.Z - z_max) < 0.01, "Z-max falsch"
    # X wird vom Kragen (collar_r) begrenzt, +Y von der Wulst (wulst_y_outer
    # plus Tropfkante), -Y vom Einfuellstutzen mit aufgesetzter Kappe.
    assert abs(bb.min.X + collar_r) < 0.01, "X-min falsch"
    assert abs(bb.max.X - collar_r) < 0.01, "X-max falsch"
    assert abs(bb.max.Y - (wulst_y_outer + drip_band)) < 0.01, "Y-max falsch"
    assert bb.min.X >= -wulst_y_outer - 0.01, "X-min ausserhalb +/-wulst_y_outer"
    assert bb.max.X <= wulst_y_outer + 0.01, "X-max ausserhalb +/-wulst_y_outer"
    grenze = wulst_y_outer + drip_band
    assert bb.min.Y >= -grenze - 0.01, "Y-min ausserhalb"
    assert bb.max.Y <= grenze + 0.01, "Y-max ausserhalb"
    # Einfuellstutzen liegt in -Y
    assert bb.min.Y < -shell_or, "kein Stutzen in -Y"
    print(
        f"[{NAME}] X = +/-{collar_r:.0f} (Kragen), Y {bb.min.Y:.1f}..{bb.max.Y:.1f}"
        f" (Stutzen/Kappe in -Y, Wulst in +Y)"
    )

    # ---- Interferenzpruefung ------------------------------------------------
    kinder = list(assembly.children)
    print(f"[{NAME}] Interferenzpruefung ({len(kinder)} Teile):")
    summe = 0.0
    for i in range(len(kinder)):
        for j in range(i + 1, len(kinder)):
            a, b = kinder[i], kinder[j]
            vol = _intersection_volume(a, b)
            paar = frozenset((a.label, b.label))
            if paar in AUSNAHMEN:
                grenzvol, begruendung = AUSNAHMEN[paar]
                print(
                    f"[{NAME}]   {a.label} <-> {b.label}: {vol:.3f} mm^3"
                    f" (Ausnahme: {begruendung})"
                )
                assert vol <= grenzvol, f"{a.label}/{b.label}: {vol} mm^3 zu gross"
                continue
            print(f"[{NAME}]   {a.label} <-> {b.label}: {vol:.6f} mm^3")
            assert vol < 1e-3, f"Interferenz {a.label}/{b.label}: {vol} mm^3"
            summe += vol
    print(f"[{NAME}] Summe ungeplanter Interferenzen = {summe:.6f} mm^3")

    # Klemmsitz gesondert ausweisen: Kappe gegen den reinen Stutzenzylinder.
    kappe = next(t for t in kinder if t.label == "fill_cap")
    klemmsitz = restmaterial(kappe, _neck_solid())
    print(
        f"[{NAME}] Klemmsitz Kappe/Stutzen (nur Stutzenzylinder):"
        f" {klemmsitz:.3f} mm^3"
    )
    assert klemmsitz > 0, "kein Klemmsitz zwischen Kappe und Stutzen"

    return True


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    assembly = build()
    check(assembly)
    export_step(assembly, EXPORT_DIR / f"{NAME}.step")
    export_stl(
        assembly,
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
