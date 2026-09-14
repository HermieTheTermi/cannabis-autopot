#!/usr/bin/env python
# ============================================================================
#  Export aller Bauteile aus cad/parts/*.py (Autodiscovery).
#  Je Modul: build() -> check(part) -> STL + STEP nach cad/export/.
#  Exit-Code 1, sobald ein Asserts oder der Build fehlschlaegt.
# ============================================================================

import importlib
import sys
from pathlib import Path

from build123d import export_step, export_stl

ROOT = Path(__file__).resolve().parent
PARTS_DIR = ROOT / "parts"
EXPORT_DIR = ROOT / "export"
PLA_DICHTE = 1.24  # g/cm^3


def discover():
    return sorted(
        p.stem for p in PARTS_DIR.glob("*.py") if p.name != "__init__.py"
    )


def _bbox_text(bb):
    return (
        f"X {bb.min.X:.1f}..{bb.max.X:.1f}  "
        f"Y {bb.min.Y:.1f}..{bb.max.Y:.1f}  "
        f"Z {bb.min.Z:.1f}..{bb.max.Z:.1f}"
    )


def main():
    sys.path.insert(0, str(ROOT))
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    alle_ok = True
    zeilen = []

    for name in discover():
        try:
            modul = importlib.import_module(f"parts.{name}")
            assert getattr(modul, "NAME", None) == name, f"NAME != {name}"
            part = modul.build()
            modul.check(part)
        except Exception as fehler:
            print(f"[FEHLER] {name}: {fehler}")
            alle_ok = False
            zeilen.append((name, None, None, None))
            continue

        vol_cm3 = part.volume / 1000.0
        masse_g = vol_cm3 * PLA_DICHTE
        bb = part.bounding_box()

        stl_pfad = EXPORT_DIR / f"{name}.stl"
        step_pfad = EXPORT_DIR / f"{name}.step"
        export_stl(
            part, stl_pfad, tolerance=0.001, angular_tolerance=0.1
        )
        export_step(part, step_pfad)

        zeilen.append((name, vol_cm3, masse_g, bb))

    print()
    print(f"{'Name':<20}{'Volumen cm^3':>14}{'Masse g':>10}   Bounding-Box")
    print("-" * 100)
    for name, vol, masse, bb in zeilen:
        if vol is None:
            print(f"{name:<20}{'FEHLER':>14}{'-':>10}   -")
        else:
            print(f"{name:<20}{vol:>14.2f}{masse:>10.2f}   {_bbox_text(bb)}")

    if alle_ok:
        print("\nGesamt: alle Teile ok")
        return 0
    print("\nGesamt: FEHLER (siehe oben)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
