# ============================================================================
#  Wulstdeckel mit Dichtungsnut, USB-C und LED - Druckteil (Port von
#  case/modules.scad, Modul wulst_lid()).
#  Drucklage lokal: X = Breite, Y = Hoehe, Z = Dicke (flach gedruckt).
# ============================================================================

from build123d import (
    Align,
    Box,
    Cylinder,
    Pos,
    RectangleRounded,
    RigidJoint,
    extrude,
)
from params import *
from lib import restmaterial, rrect

NAME = "wulst_lid"


def _dichtungsnut():
    """Umlaufende Dichtungsnut auf der oberen Dichtflaeche.

    Das SCAD schneidet offset(-4) minus offset(-6) des Grundrisses aus; das
    entspricht zwei abgerundeten Rechtecken, die um 4 bzw. 6 mm eingerueckt
    sind (Eckradius reduziert sich mit dem Offset).
    """
    aussen = RectangleRounded(wulst_w - 8, wulst_h - 8, wulst_cr - 4)
    innen = RectangleRounded(wulst_w - 12, wulst_h - 12, wulst_cr - 6)
    return Pos(0, 0, lid_t - 1.3) * extrude(aussen - innen, amount=1.4)


def build():
    body = rrect(wulst_w, wulst_h, lid_t, wulst_cr)

    body -= _dichtungsnut()

    # Verschraubung (4 x M2,5)
    for x in (-boss_x, boss_x):
        for y in lid_screw_y:
            body -= Pos(x, y, -1) * Cylinder(
                boss_hole_d / 2,
                lid_t + 2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )

    # USB-C-Durchbruch (Langloch)
    body -= Pos(0, usb_y, -1) * extrude(
        RectangleRounded(usb_w, usb_h, 1.5), amount=lid_t + 2
    )

    # LED-Fenster
    body -= Pos(0, led_y, -1) * Cylinder(
        led_d / 2, lid_t + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    # Schnittstelle zur Wulst: Dichtflaeche auf der Unterseite (z = 0)
    RigidJoint("seal", body, Pos(0, 0, 0))
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

    assert abs(bb.min.X + wulst_w / 2) < 0.01, "X-min falsch"
    assert abs(bb.max.X - wulst_w / 2) < 0.01, "X-max falsch"
    assert abs(bb.min.Y + wulst_h / 2) < 0.01, "Y-min falsch"
    assert abs(bb.max.Y - wulst_h / 2) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z) < 0.01, "Z-min falsch"
    assert abs(bb.max.Z - lid_t) < 0.01, "Z-max falsch"

    # 4 Verschraubungsbohrungen offen (Sonde kleiner als die Bohrung)
    for x in (-boss_x, boss_x):
        for y in lid_screw_y:
            rest = restmaterial(
                part,
                Pos(x, y, -1)
                * Cylinder(
                    boss_hole_d / 2 - 0.2,
                    lid_t + 2,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                ),
            )
            print(f"[{NAME}] Sonde Schraubkanal ({x:+.0f},{y:+.0f}): Rest = {rest:.6f}")
            assert rest < 1e-6, f"Schraubbohrung zu ({x},{y})"

    # USB-C-Durchbruch offen
    usb_rest = restmaterial(
        part,
        Pos(0, usb_y, -1)
        * extrude(RectangleRounded(usb_w - 0.6, usb_h - 0.6, 1.0), amount=lid_t + 2),
    )
    print(f"[{NAME}] Sonde USB-C: Restmaterial = {usb_rest:.6f} mm^3")
    assert usb_rest < 1e-6, "USB-C-Durchbruch nicht offen"

    # LED-Fenster offen
    led_rest = restmaterial(
        part,
        Pos(0, led_y, -1)
        * Cylinder(
            led_d / 2 - 0.2,
            lid_t + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ),
    )
    print(f"[{NAME}] Sonde LED-Fenster: Restmaterial = {led_rest:.6f} mm^3")
    assert led_rest < 1e-6, "LED-Fenster nicht offen"

    # Dichtungsnut: im Nutgrund leer, daneben Material. Der Grundriss ist an
    # X = 0 am oberen Rand geradlinig; die Nut liegt dort zwischen Y = 74 und 76.
    nut_rest = restmaterial(
        part,
        Pos(0, 75, 2.9)
        * Cylinder(0.5, 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    neben = restmaterial(
        part,
        Pos(0, 73, 2.9)
        * Cylinder(0.5, 0.4, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(
        f"[{NAME}] Sonde Dichtungsnut (Y=75): Rest = {nut_rest:.6f} mm^3,"
        f" daneben (Y=73): Rest = {neben:.1f} mm^3"
    )
    assert nut_rest < 1e-6, "Dichtungsnut nicht offen"
    assert neben > 0, "kein Material neben der Dichtungsnut"

    return True
