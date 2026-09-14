# ============================================================================
#  Verteilerring (Top-Drip) - Port von case/modules.scad
#  Drucklage: z 0 ... ring_h. Der Stutzen zeigt in +Y (Richtung Wulst).
#  Der Aussenring entsteht im SCAD per rotate_extrude; hier als hohler
#  Zylinder (gleiche Geometrie, identische Massen).
# ============================================================================

from build123d import Align, Cylinder, Pos, Rot
from params import *
from lib import restmaterial

NAME = "distribution_ring"

_AXIS = (Align.CENTER, Align.CENTER, Align.MIN)


def _barb_frame():
    """Lokales KOS des Stutzens: Ursprung am Ringmantel, Achse +Y."""
    return Rot(0, 0, ring_barb_dir) * Pos(ring_or - 1, 0, ring_h / 2) * Rot(0, 90, 0)


def _ring_barb():
    """Stutzen mit zwei Halterippen (1:1 zu ring_barb())."""
    frame = _barb_frame()
    barbs = [
        frame
        * Cylinder(ring_barb_od / 2, ring_barb_len + 1, align=_AXIS)
    ]
    for z in (ring_barb_len * 0.40, ring_barb_len * 0.70):
        barbs.append(
            frame
            * Pos(0, 0, z)
            * Cylinder((ring_barb_od + 0.9) / 2, 1.2, align=_AXIS)
        )
    return barbs


def _outlet_holes():
    """Austrittsbohrungen nach unten/innen, gleichmaessig ueber den Umfang."""
    holes = []
    for i in range(ring_holes):
        holes.append(
            Rot(0, 0, i * 360.0 / ring_holes)
            * Pos(0, ring_hole_r, -1)
            * Cylinder(ring_hole_d / 2, ring_wall + 2, align=_AXIS)
        )
    return holes


def _hose_bore():
    """Schlauchbohrung durch den Stutzen (durchgaengig)."""
    return _barb_frame() * Cylinder(
        ring_barb_id / 2,
        (ring_or - ring_ir) + ring_barb_len + 2,
        align=_AXIS,
    )


def _ring_cavity():
    """Innere Ringkammer (Umlaufkanal)."""
    outer = Pos(0, 0, ring_wall) * Cylinder(
        ring_or - ring_wall,
        ring_h - 2 * ring_wall,
        align=_AXIS,
    )
    inner = Pos(0, 0, ring_wall - 1) * Cylinder(
        ring_ir + ring_wall,
        ring_h - 2 * ring_wall + 2,
        align=_AXIS,
    )
    return outer - inner


def build():
    # Aussenring als hohler Zylinder (rotate_extrude der Mantelflaeche)
    body = Cylinder(ring_or, ring_h, align=_AXIS)
    body -= Pos(0, 0, -1) * Cylinder(ring_ir, ring_h + 2, align=_AXIS)

    for barb in _ring_barb():
        body += barb

    body -= _ring_cavity()
    body -= _outlet_holes()
    body -= _hose_bore()
    return body


def check(part):
    bb = part.bounding_box()
    vol = part.volume
    holes = _outlet_holes()

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )
    print(f"[{NAME}] Austrittsbohrungen = {len(holes)}")

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    grenze = ring_or + ring_barb_len + 1
    assert abs(bb.min.X) <= grenze and abs(bb.max.X) <= grenze, "X ausserhalb"
    assert abs(bb.min.Y) <= grenze and abs(bb.max.Y) <= grenze, "Y ausserhalb"
    assert abs(bb.min.Z) < 0.01, "Z-min falsch"
    assert abs(bb.max.Z - ring_h) < 0.01, "Z-max falsch"

    # Alle Austrittsbohrungen sind offen
    r_probe = (ring_hole_d - 0.6) / 2
    for hole in holes:
        c = hole.bounding_box().center()
        rest = restmaterial(
            part,
            Pos(c.X, c.Y, -1)
            * Cylinder(
                r_probe,
                ring_wall + 2,
                align=_AXIS,
            ),
        )
        assert rest < 1e-6, f"Austrittsbohrung bei ({c.X:.1f}, {c.Y:.1f}) zu"

    # Innere Ringkammer ist hohl (Sonde im Kammerquerschnitt)
    kammer = restmaterial(
        part,
        Pos(45, 0, ring_wall + 1)
        * Cylinder(1.5, ring_h - 2 * ring_wall - 2, align=_AXIS),
    )
    print(f"[{NAME}] Sonde Ringkammer: Restmaterial = {kammer:.6f} mm^3")
    assert kammer < 1e-6, "Ringkammer nicht hohl"

    # Wandstaerke ring_wall ist massiv (Sonde in der Aussenwand)
    wand = restmaterial(
        part,
        Pos(-(ring_or - ring_wall / 2), 0, ring_h / 2)
        * Cylinder(0.8, ring_wall, align=_AXIS),
    )
    print(f"[{NAME}] Sonde Wandstaerke: Restmaterial = {wand:.3f} mm^3")
    assert wand > 0, "keine Wandstaerke gefunden"

    # Schlauchbohrung im Stutzen ist durchgaengig offen
    bore = restmaterial(
        part,
        _barb_frame()
        * Pos(0, 0, 1)
        * Cylinder(ring_barb_id / 2 - 0.3, 22, align=_AXIS),
    )
    print(f"[{NAME}] Sonde Schlauchbohrung Stutzen: Restmaterial = {bore:.6f} mm^3")
    assert bore < 1e-6, "Schlauchbohrung im Stutzen nicht offen"

    return True
