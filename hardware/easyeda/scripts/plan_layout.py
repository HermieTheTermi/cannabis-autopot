#!/usr/bin/env python3
"""S3-Planung: Modulbloecke auf A1 anhand GEMESSENER Bauteil-Volumen.

Liest die kanonische IR (raw/ir_numbered.json) und die live gemessenen Volumen
(raw/measured_volumes_2026-09-15.json; je Bauteil vol_w/vol_h = Koerper PLUS
eigene Marker/Stiche) und rechnet daraus

  * raw/placement.json  — Modulbloecke, Bauteilpositionen (Ganzzahl)
  * raw/place_all.sh    — die `easyeda sch place`-Befehle in Modulreihenfolge
  * raw/frames.json (+ frames_<docId>.json, frames_P1.json) — Rahmen je Modul

Verfahren: Jedes Bauteil reserviert ein Volumen (vol_w x vol_h). Innerhalb eines
Moduls packt ein Regal-Packer (Shelf) die Volumen mit >= GAP Abstand; die
Modulbloecke verteilt ein Skyline-Bottom-Left-Packer auf dem A1-Blatt. Ein Block
umschliesst seinen Inhalt mit >= MARGIN; Bloecke ueberlappen nicht, Nutzbereich
und Titelblock-Freihaltezone bleiben frei.

Fehlt ein Bauteil in der Messdatei, wird aus der Koerper-Box eine Fallback-
Schaetzung gebildet (und im Bericht ausgewiesen).

Loetpads aus raw/no_place.json werden nicht platziert.
"""
import json
import math
import os

import build_ir

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')
MEASURED = os.path.join(RAW, 'measured_volumes_2026-09-15.json')

SHEET = (0, 0, 3304, 2338)          # A1 quer (3304 x 2338 raw)
USABLE = (12, 12, 3292, 2326)       # Nutzbereich aus measured_volumes (Fallback)
KEEPOUT = (2602, 12, 3292, 198)     # Titelblock-Ecke (x >= 2602 und y <= 198) bleibt frei
MARGIN = 150                        # Blockrand um den Inhalt (gefordert: >= 150, hart >= 20)
GAP = 25                            # Mindestabstand zweier Volumen (gefordert: >= 25)
PACK_GAP = GAP + 1                  # Regal-Abstand: +1 faengt die Ganzzahl-Rundung der
                                    #   Zentren ab, damit der echte Abstand >= GAP bleibt
GRID = 5

TITLES = {
    'USB':         'USB-C Eingang & ESD',
    'LADER':       'Laden (MCP73831)',
    'DEBUG':       'UART-Debug-Pads (DNP)',
    'MCU':         'ESP32-C6-MCU + Beschaltung',
    'WAEChTER':    'Unterspannungswaechter (MAX809)',
    'LDO':         '3V3-LDO (ME6211)',
    'AKKU':        'Akku & Puffer',
    'SENSOR':      'Sensor-Eingang',
    'PUMPE':       'Pumpentreiber Dosier- + Sauerstoffpumpe',
    'TASTER':      'Taster & LEDs',
    'ERWEITERUNG': 'Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch',
    'BOOST':       '5-V-Boost (MT3608)',
    'LICHT':       'Lichtsensor-Eingang',
}
MODULE_ORDER = ['USB', 'LADER', 'DEBUG', 'MCU', 'WAEChTER', 'LDO',
                'AKKU', 'SENSOR', 'PUMPE', 'BOOST', 'TASTER', 'ERWEITERUNG', 'LICHT']

# Gemessene Bounding-Boxen fehlen fuer die neuen Bibliotheksteile der Erweiterung.
# Ersatzgeometrien relativ zum Symbolursprung (nur fuer die Info-Box `bbox`, nicht
# fuer die Volumen-Reservierung): 1x3-Stiftleiste wie JST-XH 3P, 1x4 breiter,
# Q2 = SOT-23 wie Q1/AO3400A.
SYNTH_BBOX = {
    build_ir.NEW_PARTS['C2937625']['deviceUuid']: (-15.5, -20.5, 25.5, 20.5),
    build_ir.NEW_PARTS['C2691448']['deviceUuid']: (-15.5, -20.5, 35.5, 20.5),
    build_ir.NEW_PARTS['C15127']['deviceUuid']: (-10.5, -10.5, 24.5, 10.5),
    '804240ef97df427480be2a5281ccea31': (-7.5, -8.5, 5.5, 8.5),
    '81214969fb224686b54499e2b4f4ad3f': (-15.5, -15.5, 25.5, 15.5),
    '4d018698282b47d4893c87aca1c32f67': (-15.5, -15.5, 25.5, 15.5),
    'f76627383a2f4537b225d848b6249ec0': (-10.5, -20.5, 10.5, 20.5),
    '41353bd188bd41e4b5cff1c3b04e8681': (-17.4, -0.4, 17.2, 4.8),
    'f42b51ab2afc4d9db90725b5f9dacdaa': (-30.5, -22.5, 30.5, 22.5),
    'c464d818a3cc4b9ba1e2b92f982ed62e': (-15.5, -5.5, 15.5, 5.5),   # R18 75k (R0805)
}


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
    out.update(SYNTH_BBOX)
    return out


def shelf_pack(items, width):
    """Volumen per Regal-Packing in Breite `width` legen. Setzt lx/ly je Item."""
    order = sorted(items, key=lambda it: (-it['h'], it['key']))
    x = y = shelf_h = 0
    for it in order:
        if x > 0 and x + it['w'] > width:
            y += shelf_h + PACK_GAP
            x = 0
            shelf_h = 0
        it['lx'], it['ly'] = x, y
        x += it['w'] + PACK_GAP
        shelf_h = max(shelf_h, it['h'])
    cw = max(it['lx'] + it['w'] for it in order)
    ch = max(it['ly'] + it['h'] for it in order)
    return cw, ch


def pack_module(module, parts, usable):
    """Modulblock aus gemessenen Volumen bauen. Gibt Block-Dict mit Inhalt zurueck."""
    items = []
    for p in parts:
        vw, vh = p['vol_w'], p['vol_h']
        items.append({'key': p['ref'], 'p': p,
                      'w': int(math.ceil(vw)), 'h': int(math.ceil(vh))})
    max_target = (usable[2] - usable[0]) - 2 * MARGIN
    wmin = max(it['w'] for it in items)
    wsum = sum(it['w'] for it in items)
    best_w, best_area = wmin, None
    width = wmin
    while width <= min(wsum, max_target):
        cw, ch = shelf_pack(items, width)
        if best_area is None or cw * ch < best_area:
            best_area, best_w = cw * ch, width
        width += GRID
    shelf_pack(items, best_w)

    for it in items:
        it['cx'] = int(round(it['lx'] + it['w'] / 2.0))
        it['cy'] = int(round(it['ly'] + it['h'] / 2.0))
        vw, vh = it['p']['vol_w'], it['p']['vol_h']
        it['rect'] = [it['cx'] - vw / 2.0, it['cy'] - vh / 2.0,
                      it['cx'] + vw / 2.0, it['cy'] + vh / 2.0]

    cmn_x = min(it['rect'][0] for it in items)
    cmn_y = min(it['rect'][1] for it in items)
    cmx_x = max(it['rect'][2] for it in items)
    cmx_y = max(it['rect'][3] for it in items)
    blk_x0 = math.floor(cmn_x - MARGIN)
    blk_y0 = math.floor(cmn_y - MARGIN)
    blk_x1 = math.ceil(cmx_x + MARGIN)
    blk_y1 = math.ceil(cmx_y + MARGIN)
    return {'module': module, 'title': TITLES[module],
            'w': blk_x1 - blk_x0, 'h': blk_y1 - blk_y0,
            'local_x0': blk_x0, 'local_y0': blk_y0,
            'content': (cmn_x, cmn_y, cmx_x, cmx_y), 'items': items}


def skyline_init(usable, keepout):
    segs = [(usable[0], keepout[0], usable[1]),
            (keepout[0], keepout[2], keepout[3])]
    if keepout[2] < usable[2]:
        segs.append((keepout[2], usable[2], usable[1]))
    return [list(s) for s in segs]


def skyline_place(sky, usable, w, h):
    """Bottom-Left-Platzierung; gibt (x, y) der linken unteren Ecke oder None."""
    x0, y0, x1, y1 = usable
    best = None
    for sx, ex, _sy in sky:
        x = sx
        if x + w > x1 + 1e-9:
            continue
        y = y0
        cx = x
        ok = True
        while cx < x + w - 1e-9:
            seg = None
            for s in sky:
                if s[0] - 1e-9 <= cx < s[1] - 1e-9:
                    seg = s
                    break
            if seg is None:
                ok = False
                break
            y = max(y, seg[2])
            cx = min(seg[1], x + w)
        if ok and y + h <= y1 + 1e-9:
            cand = (y, x)
            if best is None or cand < best:
                best = cand
    if best is None:
        return None
    return best[1], best[0]


def skyline_update(sky, x, y, w, h):
    new = []
    for sx, ex, sy in sky:
        if ex <= x or sx >= x + w:
            new.append([sx, ex, sy])
        else:
            if sx < x:
                new.append([sx, x, sy])
            if ex > x + w:
                new.append([x + w, ex, sy])
    new.append([x, x + w, y + h])
    new.sort()
    merged = []
    for s in new:
        if merged and abs(merged[-1][1] - s[0]) < 1e-9 and abs(merged[-1][2] - s[2]) < 1e-9:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return merged


def main():
    ir = json.load(open(os.path.join(RAW, 'ir_numbered.json')))
    modules = json.load(open(os.path.join(RAW, 'modules.json')))   # Originalname -> Modul
    no_place = set(json.load(open(os.path.join(RAW, 'no_place.json'))))
    measured = json.load(open(MEASURED))
    volumes = measured['parts']
    usable = tuple(measured.get('nutzbar', {}).get(k, USABLE[i])
                   for i, k in enumerate(('minX', 'minY', 'maxX', 'maxY')))
    rel = rel_bboxes()

    fallbacks = []
    comps = []
    for c in ir['components']:
        orig = c['id'][4:]
        if orig in no_place:            # Loetpads ohne Bestueckungsplatz
            continue
        mod = modules.get(orig)
        if mod is None:
            raise SystemExit(f"kein Modul fuer {orig}")
        rb = rel.get(c['device']['deviceUuid'])
        if rb is None:
            raise SystemExit(f"keine gemessene bbox fuer {orig} ({c['device']['deviceUuid']})")
        vol = volumes.get(c['ref'])
        if vol is None:
            # Fallback: Koerper-Box + zweimal GAP (grob, wird im Bericht genannt)
            vw = (rb[2] - rb[0]) + 2 * GAP
            vh = (rb[3] - rb[1]) + 2 * GAP
            fallbacks.append(c['ref'])
        else:
            vw, vh = vol['vol_w'], vol['vol_h']
        comps.append({'ref': c['ref'], 'role': orig, 'module': mod, 'id': c['id'],
                      'deviceUuid': c['device']['deviceUuid'], 'vol_w': vw, 'vol_h': vh,
                      'rel': rb})

    by_mod = {}
    for c in comps:
        by_mod.setdefault(c['module'], []).append(c)

    blocks = []
    for mod in MODULE_ORDER:
        parts = by_mod.get(mod, [])
        if not parts:
            raise SystemExit(f"Modul {mod} ohne Bauteile")
        blocks.append(pack_module(mod, parts, usable))

    # Bloecke per Skyline-Bottom-Left auf dem Blatt verteilen.
    sky = skyline_init(usable, KEEPOUT)
    placements, problems = [], []
    for b in sorted(blocks, key=lambda b: (-b['h'], -b['w'], b['module'])):
        pos = skyline_place(sky, usable, b['w'], b['h'])
        if pos is None:
            raise SystemExit(f"Block {b['module']} ({b['w']}x{b['h']}) passt nicht aufs Blatt")
        b['x0'], b['y0'] = pos
        b['x1'], b['y1'] = pos[0] + b['w'], pos[1] + b['h']
        sky = skyline_update(sky, b['x0'], b['y0'], b['w'], b['h'])
        b['content_bottom'] = b['y0'] + (b['content'][1] - b['local_y0'])
        if b['x0'] < usable[0] or b['x1'] > usable[2] or b['y0'] < usable[1] or b['y1'] > usable[3]:
            problems.append(f"Block {b['module']} verlaesst den Nutzbereich")
        if (b['x0'] < KEEPOUT[2] and KEEPOUT[0] < b['x1']
                and b['y0'] < KEEPOUT[3] and KEEPOUT[1] < b['y1']):
            problems.append(f"Block {b['module']} in der Titelblock-Freihaltezone")

    for b in blocks:
        for it in b['items']:
            p = it['p']
            gx = b['x0'] + (it['cx'] - b['local_x0'])
            gy = b['y0'] + (it['cy'] - b['local_y0'])
            placements.append({'ref': p['ref'], 'role': p['role'], 'module': b['module'],
                               'id': p['id'], 'deviceUuid': p['deviceUuid'],
                               'x': gx, 'y': gy, 'rotation': 0, 'mirror': False,
                               'bbox': [snap(gx + p['rel'][0]), snap(gy + p['rel'][1]),
                                        snap(gx + p['rel'][2]), snap(gy + p['rel'][3])]})

    # Kontrolle: Bloecke untereinander und Volumen im Nutzbereich.
    for i, a in enumerate(blocks):
        for b in blocks[i + 1:]:
            if (a['x0'] < b['x1'] and b['x0'] < a['x1']
                    and a['y0'] < b['y1'] and b['y0'] < a['y1']):
                problems.append(f"Blockueberlappung {a['module']} <-> {b['module']}")

    json.dump({'sheet': list(SHEET), 'keepout': list(KEEPOUT), 'usable': list(usable),
               'blocks': [{'module': b['module'], 'title': b['title'], 'x0': b['x0'],
                           'y1': b['y1'], 'x1': b['x1'], 'y0': b['y0'],
                           'content_bottom': b['content_bottom']} for b in blocks],
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

    # Rahmen je Modulblock (S2, `sch frame apply`)
    frames = {'schemaVersion': 1, 'documentId': '4f6771a27edec75b', 'frames': []}
    for b in sorted(blocks, key=lambda b: -b['y1']):
        frames['frames'].append({
            'id': 'frame-' + b['module'].lower(),
            'title': b['title'],
            'rect': {'minX': b['x0'], 'minY': b['y0'], 'maxX': b['x1'], 'maxY': b['y1']},
            'titleX': b['x0'] + 12, 'titleY': b['y1'] - 12,
            'fontSize': 20, 'color': '#AA00AA', 'lineType': 1,
        })
    for fn in ('frames.json', 'frames_4f6771a27edec75b.json', 'frames_P1.json'):
        json.dump(frames, open(os.path.join(RAW, fn), 'w'), ensure_ascii=False, indent=1)

    # Belegungsstatistik
    u_area = (usable[2] - usable[0]) * (usable[3] - usable[1])
    block_area = sum(b['w'] * b['h'] for b in blocks)
    volume_area = sum(c['vol_w'] * c['vol_h'] for c in comps)
    print(f"Bauteile: {len(placements)}  Bloecke: {len(blocks)}  "
          f"Blattnutzung (Bloecke): {100.0 * block_area / u_area:.1f} %  "
          f"(Volumen: {100.0 * volume_area / u_area:.1f} %)")
    if fallbacks:
        print(f"Fallback-Schaetzung fuer {len(fallbacks)} Bauteil(e) ohne Messwert: "
              + ", ".join(sorted(fallbacks)))
    else:
        print("Fallback-Schaetzung: keine (alle Bauteile gemessen)")
    for b in sorted(blocks, key=lambda b: -b['y1']):
        print(f"  {b['module']:<11} x {b['x0']:>4}..{b['x1']:<4} y {b['y0']:>4}..{b['y1']:<4} "
              f"({b['w']}x{b['h']})")
    print("PROBLEME:" if problems else "kein Planungsproblem")
    for p in problems:
        print("  " + p)
    return 0 if not problems else 1


if __name__ == '__main__':
    raise SystemExit(main())
