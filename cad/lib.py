# ============================================================================
#  Smart Grow Topf - gemeinsame Helfer (Port von case/modules.scad)
#  1:1-Uebersetzung der dortigen 2D/3D-Hilfsformen und Achsen.
# ============================================================================

import math

from build123d import (
    Align,
    Cylinder,
    Plane,
    Pos,
    RectangleRounded,
    ShapeList,
    Vector,
    extrude,
)
from params import *


def rrect(w, d, h, r):
    """Abgerundeter Quader, in XY zentriert, von z=0 bis z=h (mm)."""
    return extrude(RectangleRounded(w, d, r), amount=h)


def hole_grid(radius, d, pitch, z0, h):
    """Lochraster (versetzte Reihen), gefiltert auf einen Kreis.

    Liefert eine Liste einzelner Zylinder (fuer `part - holes`).
    """
    dy = pitch * math.sqrt(3) / 2
    rows = int(math.floor(radius / dy))
    cols = int(math.floor(radius / pitch))
    holes = []
    for row in range(-rows, rows + 1):
        y = row * dy
        xoff = 0.0 if (abs(row) % 2 == 0) else pitch / 2
        for c in range(-cols, cols + 1):
            x = c * pitch + xoff
            if x * x + y * y <= radius * radius + 1e-9:
                holes.append(
                    Pos(x, y, z0)
                    * Cylinder(
                        d / 2,
                        h,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                )
    return holes


def wulst_footprint_2d(off=0.0):
    """Grundriss der Wulst (X tangential, Y radial von 0 bis wulst_y_outer)."""
    return Pos(0, wulst_y_outer / 2, 0) * RectangleRounded(
        wulst_w + 2 * off,
        wulst_y_outer + 2 * off,
        wulst_cr + off,
    )


def fill_axis():
    """Achse des Einfuellstutzens: (P0 an der Aussenwand, Einheitsrichtung)."""
    ang = math.radians(fill_ang)
    d = Vector(0, -math.cos(ang), math.sin(ang))
    p0 = Vector(0, -shell_or, fill_z_wall)
    return p0, d


def fill_mouth_center():
    """Mittelpunkt der Mundebene des Einfuellstutzens."""
    p0, d = fill_axis()
    return p0 + fill_len * d


def cylinder_between(a, b, d):
    """Zylinder Durchmesser d zwischen den Wegpunkten a und b."""
    a = Vector(*a)
    b = Vector(*b)
    v = b - a
    length = v.length
    if length < 1e-6:
        return None
    plane = Plane(origin=a, z_dir=v)
    return plane * Cylinder(
        d / 2, length, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )


def chain(points, d):
    """Zylinderkette zwischen Wegpunkten (Liste von 3D-Punkten)."""
    segments = []
    for a, b in zip(points[:-1], points[1:]):
        seg = cylinder_between(a, b, d)
        if seg is not None:
            segments.append(seg)
    return segments


def restmaterial(part, probe):
    """Volumen des Materials von `part`, das in der Sonde `probe` liegt.

    `intersect()` kann `None` (leer) oder eine `ShapeList` liefern.
    """
    inter = part.intersect(probe)
    if inter is None:
        return 0.0
    if isinstance(inter, ShapeList):
        return sum(shape.volume for shape in inter)
    try:
        return inter.volume
    except AttributeError:
        return sum(shape.volume for shape in inter)
