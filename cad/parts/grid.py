# ============================================================================
#  Auflagerost / Trennplatte (Port von case/modules.scad)
#  Drucklage: z 0 ... grid_t, im Tank spater auf z = grid_z0 verschoben.
# ============================================================================

from build123d import Align, Cylinder, Pos
from params import *
from lib import hole_grid, restmaterial

NAME = "grid"


def _grid_holes():
    """Rostbohrungen (Zylinderliste fuer die Subtraktion).

    hole_grid im SCAD liegt um 1 nach unten versetzt; das entspricht
    z0 = -1 mit Hoehe grid_t + 2.
    """
    return hole_grid(
        grid_or - grid_rim, grid_hole_d, grid_pitch, -1, grid_t + 2
    )


def _hose_passage():
    """Durchlass fuer den Saugschlauch bei y = 52."""
    return Pos(0, 52, -1) * Cylinder(
        7.0, grid_t + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def build():
    body = Cylinder(
        grid_or, grid_t, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    body -= _grid_holes()
    body -= _hose_passage()
    return body


def check(part):
    bb = part.bounding_box()
    vol = part.volume
    holes = _grid_holes()

    print(f"[{NAME}] Volumen = {vol:.1f} mm^3 = {vol / 1000:.2f} cm^3")
    print(
        f"[{NAME}] bbox X {bb.min.X:.3f}..{bb.max.X:.3f}"
        f"  Y {bb.min.Y:.3f}..{bb.max.Y:.3f}"
        f"  Z {bb.min.Z:.3f}..{bb.max.Z:.3f}"
    )
    print(f"[{NAME}] Rostbohrungen = {len(holes)}")

    assert part.is_valid is True, "part.is_valid ist nicht True"
    assert vol > 0, "Volumen <= 0"

    assert abs(bb.min.X + grid_or) < 0.01, "X-min falsch"
    assert abs(bb.max.X - grid_or) < 0.01, "X-max falsch"
    assert abs(bb.min.Y + grid_or) < 0.01, "Y-min falsch"
    assert abs(bb.max.Y - grid_or) < 0.01, "Y-max falsch"
    assert abs(bb.min.Z) < 0.01, "Z-min falsch"
    assert abs(bb.max.Z - grid_t) < 0.01, "Z-max falsch"

    # Jede Rostbohrung ist offen
    r_probe = (grid_hole_d - 0.6) / 2
    for hole in holes:
        c = hole.bounding_box().center()
        rest = restmaterial(
            part,
            Pos(c.X, c.Y, -1)
            * Cylinder(
                r_probe,
                grid_t + 2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ),
        )
        assert rest < 1e-6, f"Rostbohrung bei ({c.X:.1f}, {c.Y:.1f}) zu"

    # Der ungelochte Rand ist massiv
    rand = restmaterial(
        part,
        Pos(grid_or - grid_rim / 2, 0, 0)
        * Cylinder(1.0, grid_t, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(f"[{NAME}] Sonde ungelochter Rand: Restmaterial = {rand:.3f} mm^3")
    assert rand > 0, "kein Material im ungelochten Rand"

    # Durchmesser-14-Durchlass fuer den Saugschlauch (y = 52) ist offen
    durchlass = restmaterial(
        part,
        Pos(0, 52, -1)
        * Cylinder(6.7, grid_t + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)),
    )
    print(f"[{NAME}] Sonde Schlauchdurchlass (y=52): Restmaterial = {durchlass:.6f} mm^3")
    assert durchlass < 1e-6, "Schlauchdurchlass nicht offen"

    return True
