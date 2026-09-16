#!/usr/bin/env python3
"""S3-Planung: Modulbloecke auf A1 anhand GEMESSENER Bauteil-Volumen.

Liest die kanonische IR (raw/ir_numbered.json) und die live gemessenen Volumen
(raw/measured_volumes_2026-09-16.json; je Bauteil vol_w/vol_h = Koerper PLUS
eigene Marker/Stiche) und rechnet daraus

  * raw/placement.json  — Modulbloecke, Bauteilpositionen (Ganzzahl)
  * raw/place_all.sh    — die `easyeda sch place`-Befehle in Modulreihenfolge
  * raw/frames.json (+ frames_<docId>.json, frames_P1.json) — Rahmen je Modul

Verfahren: Jedes Bauteil reserviert ein Volumen (vol_w x vol_h). Innerhalb eines
Moduls packt ein Regal-Packer (Shelf) die Volumen mit >= GAP Abstand so, dass der
Block-Umriss inkl. MARGIN minimal wird; die Modulbloecke verteilt ein
MaxRects-Packer (Best-Short-Side-Fit) auf dem A1-Blatt. Ein Block umschliesst
seinen Inhalt mit >= MARGIN; Bloecke ueberlappen nicht, Nutzbereich und
Titelblock-Freihaltezone bleiben frei.

Volumen-Aufloesung je Bauteil (in dieser Reihenfolge):
  1. `parts[ref]` — instanzgenauer Messwert (numerischer Designator bzw. funktionaler
     Name aus der Allokation).
  2. `by_device[deviceUuid]` — neuer Geraete-Messwert aus raw/measured_volumes_2026-09-16.json
     (Schluessel = Device-UUID aus raw/lcsc_map.json), fuer Bauteile ohne instanzgenauen Wert.
  3. Geraete-Repraesentant aus dem 1S-Bestand (gleiche Device-UUID, anderer Designator).
  4. Fallback-Schaetzung (wird im Bericht ausgewiesen; Ziel ist "keine").

Loetpads aus raw/no_place.json werden nicht platziert.
"""
import json
import math
import os
import random

import build_ir

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')
MEASURED = os.path.join(RAW, 'measured_volumes_2026-09-16.json')
OLD_LIVE = os.path.join(RAW, 'backup_1s_live_2026-09-16.json')

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
    'LADER':       'Laden (IP2326, 2S)',
    'DEBUG':       'UART-Debug-Pads (DNP)',
    'MCU':         'ESP32-C6-MCU + Beschaltung',
    'WAEChTER':    'Unterspannungswaechter (TPS3839)',
    'LDO':         '3V3-Buck (AP63203)',
    'AKKU':        'Akku & Puffer',
    'SENSOR':      'Sensor-Eingang',
    'PUMPE':       'Pumpentreiber Dosier- + Sauerstoffpumpe',
    'TASTER':      'Taster & LEDs',
    'ERWEITERUNG': 'Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch',
    'BOOST':       '5-V-Buck (SY8113B)',
    'LICHT':       'Lichtsensor-Eingang',
    'SCHUTZ':      'Akku-Schutz (HY2120-CB + PSMN4R2)',
}
MODULE_ORDER = ['USB', 'LADER', 'DEBUG', 'MCU', 'WAEChTER', 'SCHUTZ', 'LDO',
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
        # Der Block traegt den Rand MARGIN an allen vier Seiten. Deshalb den
        # Blockflaechen-Umriss (cw+2M)(ch+2M) minimieren, nicht die reine
        # Inhaltsflaeche: breite Flachbloecke (z. B. LADER) verschwendeten
        # sonst Rand und liessen sich nicht dicht kacheln.
        block_area = (cw + 2 * MARGIN) * (ch + 2 * MARGIN)
        if best_area is None or block_area < best_area:
            best_area, best_w = block_area, width
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


def rects_intersect(a, b):
    return (a[0] < b[2] - 1e-9 and b[0] < a[2] - 1e-9
            and a[1] < b[3] - 1e-9 and b[1] < a[3] - 1e-9)


def rect_contains(a, b):
    return (a[0] <= b[0] + 1e-9 and a[1] <= b[1] + 1e-9
            and a[2] >= b[2] - 1e-9 and a[3] >= b[3] - 1e-9)


def free_rects(usable, keepout):
    """Nutzbereich minus Titelblock-Keepout als disjunkte Rechtecke."""
    x0, y0, x1, y1 = usable
    kx0, ky0, kx1, ky1 = keepout
    cand = [(x0, y0, kx0, y1), (kx1, y0, x1, y1),
            (kx0, y0, kx1, ky0), (kx0, ky1, kx1, y1)]
    return [r for r in cand if r[2] - r[0] > 1e-9 and r[3] - r[1] > 1e-9]


def mr_prune(free):
    """Von zwei freien Rechtecken das enthaltene verwerfen."""
    out = []
    for i, f in enumerate(free):
        if any(i != j and rect_contains(g, f) for j, g in enumerate(free)):
            continue
        out.append(f)
    return out


def mr_split(free, used):
    """Freie Rechtecke am belegten Rechteck aufteilen, enthaltene entfernen."""
    ux0, uy0, ux1, uy1 = used
    new = []
    for fx0, fy0, fx1, fy1 in free:
        if not rects_intersect((fx0, fy0, fx1, fy1), used):
            new.append((fx0, fy0, fx1, fy1))
            continue
        if ux0 > fx0:
            new.append((fx0, fy0, ux0, fy1))
        if ux1 < fx1:
            new.append((ux1, fy0, fx1, fy1))
        if uy0 > fy0:
            new.append((fx0, fy0, fx1, uy0))
        if uy1 < fy1:
            new.append((fx0, uy1, fx1, fy1))
    return mr_prune(new)


def _try_order(blocks, usable, keepout, rng):
    """Eine Blockreihenfolge per Best-Short-Side-Fit setzen; sonst None.

    `rng=None` waehlt unter gleich guten freien Rechtecken deterministisch das
    erste, sonst zufaellig (fuer die Random-Restarts in `distribute`).
    """
    free = free_rects(usable, keepout)
    pos = {}
    for b in blocks:
        cands = []
        for f in free:
            fw, fh = f[2] - f[0], f[3] - f[1]
            if b['w'] <= fw + 1e-9 and b['h'] <= fh + 1e-9:
                cands.append((min(fw - b['w'], fh - b['h']),
                              max(fw - b['w'], fh - b['h']), f))
        if not cands:
            return None
        cands.sort(key=lambda c: (c[0], c[1]))
        if rng is None:
            f = cands[0][2]
        else:
            best_ss = cands[0][0]
            f = rng.choice([c for c in cands if c[0] == best_ss])[2]
        pos[b['module']] = (f[0], f[1])
        free = mr_split(free, (f[0], f[1], f[0] + b['w'], f[1] + b['h']))
    return pos


def distribute(blocks, usable, keepout):
    """Bloecke mit MaxRects aufs Blatt verteilen; gibt {module: (x0, y0)} oder None.

    Der Skyline-Packer liess bei ~92 % Fuellung Luecken, die breite Bloecke
    ausschlossen. MaxRects (Best-Short-Side-Fit) schliesst diese Luecken.
    Erst werden mehrere feste Sortierungen probiert; scheitert die gierige
    Wahl, suchen deterministische Random-Restarts (fester Seed) die dichte
    Packung reproduzierbar.
    """
    keys = [lambda b: (-b['w'] * b['h'], b['module']),
            lambda b: (-b['h'], -b['w'], b['module']),
            lambda b: (-b['w'], -b['h'], b['module']),
            lambda b: (-max(b['w'], b['h']), -min(b['w'], b['h']), b['module']),
            lambda b: (-(b['w'] + b['h']), b['module'])]
    for key in keys:
        pos = _try_order(sorted(blocks, key=key), usable, keepout, None)
        if pos is not None:
            return pos
    for seed in range(16):
        rng = random.Random(seed)
        for _ in range(20000):
            order = list(blocks)
            rng.shuffle(order)
            pos = _try_order(order, usable, keepout, rng)
            if pos is not None:
                return pos
    return None


def main():
    ir = json.load(open(os.path.join(RAW, 'ir_numbered.json')))
    modules = json.load(open(os.path.join(RAW, 'modules.json')))   # Originalname -> Modul
    no_place = set(json.load(open(os.path.join(RAW, 'no_place.json'))))
    measured = json.load(open(MEASURED))
    volumes = measured['parts']
    by_device = measured.get('by_device', {})
    usable = tuple(measured.get('nutzbar', {}).get(k, USABLE[i])
                   for i, k in enumerate(('minX', 'minY', 'maxX', 'maxY')))
    rel = rel_bboxes()

    # Geraete-Repraesentanten aus dem 1S-Bestand: gleiche Device-UUID -> gemessenes
    # Instanzvolumen. Das deckt die neuen Bauteile ab, deren Geraet im Bestand schon
    # einmal gemessen wurde (z. B. 100-nF-Kondensator, 10-k-Widerstand). Die neuen
    # Geraete aus `by_device` haben Vorrang.
    device_vol = {}
    old_live = json.load(open(OLD_LIVE))
    for c in old_live['components']:
        p = volumes.get(c['ref'])
        if p:
            device_vol.setdefault(c['device']['deviceUuid'], (p['vol_w'], p['vol_h']))
    for uuid, rec in by_device.items():
        device_vol[uuid] = (rec['vol_w'], rec['vol_h'])

    fallbacks, from_device = [], []
    comps = []
    for c in ir['components']:
        orig = c['id'][4:]
        if orig in no_place:            # Loetpads ohne Bestueckungsplatz
            continue
        mod = modules.get(orig)
        if mod is None:
            raise SystemExit(f"kein Modul fuer {orig}")
        uuid = c['device']['deviceUuid']
        vol = volumes.get(c['ref'])
        if vol is not None:
            vw, vh = vol['vol_w'], vol['vol_h']
        elif uuid in by_device:
            vw, vh = by_device[uuid]['vol_w'], by_device[uuid]['vol_h']
            from_device.append(f"{c['ref']} (by_device)")
        elif uuid in device_vol:
            vw, vh = device_vol[uuid]
            from_device.append(f"{c['ref']} (Bestand gleiche Device-UUID)")
        else:
            # Letzter Ausweg: Koerper-Box + zweimal GAP (grob, wird im Bericht genannt)
            vw = (rel[uuid][2] - rel[uuid][0]) + 2 * GAP if uuid in rel else 40
            vh = (rel[uuid][3] - rel[uuid][1]) + 2 * GAP if uuid in rel else 20
            fallbacks.append(c['ref'])
        # Info-Box: gemessene relative bbox, sonst aus dem Volumen zentriert abgeleitet.
        rb = rel.get(uuid) or (-vw / 2.0, -vh / 2.0, vw / 2.0, vh / 2.0)
        comps.append({'ref': c['ref'], 'role': orig, 'module': mod, 'id': c['id'],
                      'deviceUuid': uuid, 'vol_w': vw, 'vol_h': vh,
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

    # Bloecke per MaxRects auf dem Blatt verteilen.
    problems = []
    pos = distribute(blocks, usable, KEEPOUT)
    if pos is None:
        widest = max(blocks, key=lambda b: b['w'] * b['h'])
        raise SystemExit(f"Block {widest['module']} ({widest['w']}x{widest['h']}) "
                         f"passt nicht aufs Blatt "
                         f"({usable[2] - usable[0]}x{usable[3] - usable[1]})")
    for b in blocks:
        b['x0'], b['y0'] = pos[b['module']]
        b['x1'], b['y1'] = b['x0'] + b['w'], b['y0'] + b['h']
        b['content_bottom'] = b['y0'] + (b['content'][1] - b['local_y0'])
        if b['x0'] < usable[0] or b['x1'] > usable[2] or b['y0'] < usable[1] or b['y1'] > usable[3]:
            problems.append(f"Block {b['module']} verlaesst den Nutzbereich")
        if (b['x0'] < KEEPOUT[2] and KEEPOUT[0] < b['x1']
                and b['y0'] < KEEPOUT[3] and KEEPOUT[1] < b['y1']):
            problems.append(f"Block {b['module']} in der Titelblock-Freihaltezone")

    placements = []
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

    # Kontrolle: der Plan enthaelt jedes IR-Bauteil (Refdes-Menge identisch).
    ir_refs = {c['ref'] for c in ir['components']}
    pl_refs = {p['ref'] for p in placements}
    if ir_refs != pl_refs:
        problems.append("Refdes-Menge placement != IR: fehlend="
                        + str(sorted(ir_refs - pl_refs))
                        + " ueberzaehlig=" + str(sorted(pl_refs - ir_refs)))

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
             'G=(--project "SmartGrowTopf_V1" --doc 4f6771a27edec75b)',
             'LIB=0819f05c4eef4c71ace90d822a990e87',
             'FAIL=0']
    for p in placements:
        lines.append(f'easyeda "${{G[@]}}" sch place --lib $LIB --uuid {p["deviceUuid"]} '
                     f'--x {p["x"]} --y {p["y"]} --designator {p["ref"]} >/dev/null || '
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
    if from_device:
        print(f"Geraete-Messwert (by_device/Bestand) fuer {len(from_device)} Bauteil(e): "
              + ", ".join(sorted(from_device)))
    if fallbacks:
        print(f"Fallback-Schätzung fuer {len(fallbacks)} Bauteil(e) ohne Messwert: "
              + ", ".join(sorted(fallbacks)))
    else:
        print("Fallback-Schätzung: keine (alle Bauteile gemessen)")
    for b in sorted(blocks, key=lambda b: -b['y1']):
        print(f"  {b['module']:<11} x {b['x0']:>4}..{b['x1']:<4} y {b['y0']:>4}..{b['y1']:<4} "
              f"({b['w']}x{b['h']})")
    print("PROBLEME:" if problems else "kein Planungsproblem")
    for p in problems:
        print("  " + p)
    return 0 if not problems else 1


if __name__ == '__main__':
    raise SystemExit(main())
