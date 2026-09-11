#!/usr/bin/env python3
"""S3-Planung: Modulblöcke auf A4 + Platzierungsbefehle.

Liest die kanonische IR (raw/ir_numbered.json) und die am lebenden Symbol gemessenen
Bounding-Boxen (raw/probe4.json) und rechnet daraus

  * raw/placement.json  — Modulblöcke, Bauteilpositionen (5-raw-Raster)
  * raw/place_all.sh    — die `easyeda sch place`-Befehle in Modulreihenfolge

Verfahren: je Modul werden die Bauteile auf einem Regal-Raster (Shelf-Packing) gepackt,
die Modulblöcke sitzen auf fest vorgegebenen Ankern (x0, y_top) in Leserichtung.
Regeln: 5-raw-Raster, Ränder 25 raw, Titelblock-Freihaltezone (x>=468, y<=198) bleibt frei,
Mindestabstand zwischen Bauteilen 40 raw (Platz für Stubs + Netport-Marker).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')

SHEET = (0, 0, 2338, 1652)          # A2 quer, seit 11.09.2026 (zwei Groessen groesser als A4)
KEEPOUT = (1636, 0, 2338, 198)      # Titelblock aus sch sheet-geometry (A2)
MARGIN = 50
GAP = 70          # Mindestabstand zwischen zwei Bauteilen im Block (Platz fuer Stubs + Marker)
PAD = 60          # Innenabstand des Blocks zum Rahmen
GRID = 5

# Modul -> (Titel, Anker x0, Anker y_top, Breite, max. Hoehe bis zum naechsten Anker)
MODULES = {
    # (Titel, Anker x0, Anker y_top, Breite, Hoehe, Inhaltsversatz x)
    'USB':      ('USB-C Eingang & ESD',        50, 1590,  700, 340, 130),
    'LADER':    ('Laden (MCP73831)',          830, 1590,  800, 340,  0),
    'DEBUG':    ('UART-Debug-Pads (DNP)',    1690, 1590,  560, 340,  0),
    'MCU':      ('ESP32-C6-MCU + Beschaltung', 50, 1220, 1250, 620, 300),
    'WAEChTER': ('Unterspannungswaechter (MAX809)', 1360, 1220, 470, 300, 0),
    'LDO':      ('3V3-LDO (ME6211)',         1880, 1220,  400, 300,  0),
    'AKKU':     ('Akku & Puffer',            1360,  890,  470, 300,  0),
    'SENSOR':   ('Sensor-Eingang',           1880,  890,  400, 300,  0),
    'PUMPE':    ('Pumpentreiber (Low-Side)', 1310,  560,  560, 330,  0),
    'TASTER':   ('Taster & LEDs',            1960,  560,  320, 330,  0),
}
MODULE_ORDER = ['USB', 'LADER', 'DEBUG', 'MCU', 'WAEChTER', 'LDO',
                'AKKU', 'SENSOR', 'PUMPE', 'TASTER']


def snap(v):
    return int(round(v / GRID) * GRID)


def rel_bboxes():
    """Device-UUID -> (dx_min, dy_min, dx_max, dy_max) relativ zum Symbolursprung."""
    out = {}
    data = json.load(open(os.path.join(RAW, 'probe4.json')))
    for c in data['result']['components']:
        dev = c.get('device') or {}
        uuid = dev.get('libraryUuid')
        bb = c.get('bbox')
        if not uuid or len(uuid) != 32 or not bb:
            continue
        out[uuid] = (bb['minX'] - c['x'], bb['minY'] - c['y'],
                     bb['maxX'] - c['x'], bb['maxY'] - c['y'])
    return out


def main():
    ir = json.load(open(os.path.join(RAW, 'ir_numbered.json')))
    modules = json.load(open(os.path.join(RAW, 'modules.json')))   # Originalname -> Modul
    rel = rel_bboxes()

    comps = []
    for c in ir['components']:
        orig = c['id'][4:]
        mod = modules.get(orig)
        if mod is None:
            raise SystemExit(f"kein Modul fuer {orig}")
        rb = rel.get(c['device']['deviceUuid'])
        if rb is None:
            raise SystemExit(f"keine gemessene bbox fuer {orig} ({c['device']['deviceUuid']})")
        comps.append({'ref': c['ref'], 'role': orig, 'module': mod, 'id': c['id'],
                      'deviceUuid': c['device']['deviceUuid'],
                      'w': rb[2] - rb[0], 'h': rb[3] - rb[1], 'rel': rb})

    by_mod = {}
    for c in comps:
        by_mod.setdefault(c['module'], []).append(c)

    placements, blocks, problems = [], [], []
    for mod in MODULE_ORDER:
        title, ax, ay, aw, ah, dx = MODULES[mod]
        parts = sorted(by_mod.get(mod, []), key=lambda c: (-c['h'], c['ref']))
        if not parts:
            problems.append(f"Modul {mod} ohne Bauteile")
            continue

        # Shelf-Packing innerhalb des Blocks (y abwärts)
        cx, cy = ax + PAD + dx, ay - PAD
        shelf_h = 0
        block_used_w = 0
        for p in parts:
            if cx + p['w'] > ax + aw - PAD:
                cx = ax + PAD + dx
                cy -= shelf_h + GAP
                shelf_h = 0
            center_x, center_y = snap(cx - p['rel'][0]), snap(cy - p['rel'][3])
            bbox = [snap(center_x + p['rel'][0]), snap(center_y + p['rel'][1]),
                    snap(center_x + p['rel'][2]), snap(center_y + p['rel'][3])]
            placements.append({'ref': p['ref'], 'role': p['role'], 'module': mod, 'id': p['id'],
                               'deviceUuid': p['deviceUuid'], 'x': center_x, 'y': center_y,
                               'rotation': 0, 'mirror': False, 'bbox': bbox})
            cx += p['w'] + GAP
            shelf_h = max(shelf_h, p['h'])
            block_used_w = max(block_used_w, cx - ax)
        bottom = cy - shelf_h - PAD
        blocks.append({'module': mod, 'title': title, 'x0': ax, 'y1': ay,
                       'x1': ax + aw, 'y0': ay - ah, 'content_bottom': bottom})
        if bottom < ay - ah:
            problems.append(f"Modul {mod}: Inhalt reicht bis y={bottom:.0f}, Block endet bei {ay-ah}")
        if cx - ax > aw:
            problems.append(f"Modul {mod}: Inhalt {cx-ax:.0f} breiter als Block {aw}")
        if ax + aw > SHEET[2] - MARGIN or ay > SHEET[3] - MARGIN:
            problems.append(f"Modul {mod}: Block verlaesst das Blatt")

    # Kollisionen / Ränder / Freihaltezone
    for i, a in enumerate(placements):
        ax0, ay0, ax1, ay1 = a['bbox']
        if ax0 < MARGIN or ax1 > SHEET[2] - MARGIN or ay0 < MARGIN or ay1 > SHEET[3] - MARGIN:
            problems.append(f"{a['ref']} ausserhalb des Blattrands ({a['bbox']})")
        if ax1 > KEEPOUT[0] and ay0 < KEEPOUT[3]:
            problems.append(f"{a['ref']} in der Titelblock-Freihaltezone")
        for b in placements[i + 1:]:
            bx0, by0, bx1, by1 = b['bbox']
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                problems.append(f"Ueberlappung {a['ref']} <-> {b['ref']}")

    json.dump({'sheet': SHEET, 'keepout': KEEPOUT, 'blocks': blocks,
               'placements': placements, 'problems': problems},
              open(os.path.join(RAW, 'placement.json'), 'w'), ensure_ascii=False, indent=1)

    lines = ['#!/bin/bash',
             '# generiert von scripts/plan_layout.py — S3-Platzierung SmartGrowTopf_V1',
             'set -u',
             'export PATH="$HOME/.local/bin:$PATH"',
             'G=(--project "SmartGrowTopf_V1" --doc P1)',
             'LIB=0819f05c4eef4c71ace90d822a990e87',
             'FAIL=0']
    for p in placements:
        lines.append(f'easyeda "${{G[@]}}" sch place --lib $LIB --uuid {p["deviceUuid"]} '
                     f'--x {p["x"]} --y {p["y"]} --designator {p["ref"]} >/dev/null 2>&1 || '
                     f'{{ echo "FAIL {p["ref"]}"; FAIL=1; }}')
    lines.append('echo "place-done FAIL=$FAIL"')
    path = os.path.join(RAW, 'place_all.sh')
    open(path, 'w').write("\n".join(lines) + "\n")
    os.chmod(path, 0o755)

    print(f"Bauteile: {len(placements)}  Bloecke: {len(blocks)}")
    for b in sorted(blocks, key=lambda b: -b['y1']):
        print(f"  {b['module']:<10} x {b['x0']:>4}..{b['x1']:<4} y {b['y0']:>4}..{b['y1']:<4} "
              f"Inhalt bis y={b['content_bottom']:>5.0f}")
    print("PROBLEME:" if problems else "kein Planungsproblem")
    for p in problems:
        print("  " + p)
    return 0 if not problems else 1


if __name__ == '__main__':
    raise SystemExit(main())
