#!/usr/bin/env python3
"""Offline-Pruefer der Modulplatzierung gegen die gemessenen Bauteil-Volumen.

Liest raw/placement.json, raw/measured_volumes_2026-09-16.json und raw/frames.json
und prueft ohne Live-Zugriff:

  (a) jedes Bauteil-Volumen liegt vollstaendig im nutzbaren Blattbereich (A1),
  (b) kein zwei Volumen sind naeher als 25 Einheiten (Planungs-GAP),
  (c) jeder Rahmen umschliesst seinen Inhalt mit >= 20 Einheiten Rand (harte Grenze;
      Planungsziel ist >= 150 und wird mitberichtet),
  (d) die Blockrahmen ueberlappen einander nicht.

Volumen eines Bauteils = vol_w x vol_h aus der Messdatei, zentriert auf (x, y)
der Platzierung. Aufloesung wie in plan_layout.py: parts[ref], sonst
by_device[deviceUuid], sonst Bestands-Repraesentant gleicher Device-UUID. Erst
wenn all das fehlt, wird die Info-Box plus 20 Einheiten Rand als Fallback
genutzt (wird ausgewiesen).

Exit 0 bei Erfuellung, Exit 1 bei mindestens einem Verstoss. Rohzahlen auf stdout.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')

GAP_MIN = 25.0
MARGIN_MIN = 20.0       # harte Grenze
MARGIN_TARGET = 150.0   # Planungsziel aus plan_layout.py
EPS = 1e-6


def rect_gap(a, b):
    """Abstand zweier achsenparalleler Rechtecke (0 bei Ueberlappung)."""
    dx = max(b[0] - a[2], a[0] - b[2])
    dy = max(b[1] - a[3], a[1] - b[3])
    if dx > 0 and dy > 0:
        return math.hypot(dx, dy)
    if dx > 0:
        return dx
    if dy > 0:
        return dy
    return 0.0


def rects_overlap(a, b):
    return (a[0] < b[2] - EPS and b[0] < a[2] - EPS
            and a[1] < b[3] - EPS and b[1] < a[3] - EPS)


def fmt_rect(r):
    return f"x {r[0]:.1f}..{r[2]:.1f} y {r[1]:.1f}..{r[3]:.1f}"


def main():
    placement = json.load(open(os.path.join(RAW, 'placement.json')))
    measured = json.load(open(os.path.join(RAW, 'measured_volumes_2026-09-16.json')))
    frames = json.load(open(os.path.join(RAW, 'frames.json')))
    old_live_path = os.path.join(RAW, 'backup_1s_live_2026-09-16.json')

    usable = measured['nutzbar']
    parts = measured['parts']
    by_device = measured.get('by_device', {})
    device_vol = {}
    if os.path.exists(old_live_path):
        for c in json.load(open(old_live_path))['components']:
            m = parts.get(c['ref'])
            if m:
                device_vol.setdefault(c['device']['deviceUuid'], (m['vol_w'], m['vol_h']))
    for uuid, rec in by_device.items():
        device_vol[uuid] = (rec['vol_w'], rec['vol_h'])

    volumes, fallbacks = [], []
    for p in placement['placements']:
        m = parts.get(p['ref'])
        if m is not None:
            w, h = m['vol_w'], m['vol_h']
        elif p.get('deviceUuid') in device_vol:
            w, h = device_vol[p['deviceUuid']]
        else:
            bb = p['bbox']
            w = (bb[2] - bb[0]) + 2 * MARGIN_MIN
            h = (bb[3] - bb[1]) + 2 * MARGIN_MIN
            fallbacks.append(p['ref'])
        volumes.append({'ref': p['ref'], 'module': p['module'], 'x': p['x'], 'y': p['y'],
                        'rect': (p['x'] - w / 2.0, p['y'] - h / 2.0,
                                 p['x'] + w / 2.0, p['y'] + h / 2.0)})

    violations = []

    # (a) Volumen vollstaendig im Nutzbereich
    min_edge = None
    for v in volumes:
        x0, y0, x1, y1 = v['rect']
        d = min(x0 - usable['minX'], y0 - usable['minY'],
                usable['maxX'] - x1, usable['maxY'] - y1)
        if min_edge is None or d < min_edge[0]:
            min_edge = (d, v['ref'])
        if d < -EPS:
            violations.append(f"(a) {v['ref']} ragt aus dem Nutzbereich ({fmt_rect(v['rect'])}, "
                              f"Rand {d:.1f})")

    # (b) Abstand zweier Volumen
    min_gap, min_gap_pair = None, None
    for i, a in enumerate(volumes):
        for b in volumes[i + 1:]:
            g = rect_gap(a['rect'], b['rect'])
            if min_gap is None or g < min_gap:
                min_gap, min_gap_pair = g, (a['ref'], b['ref'])
            if g < GAP_MIN - EPS:
                kind = "Ueberlappung" if g <= EPS else "zu eng"
                violations.append(f"(b) {a['ref']} <-> {b['ref']} Abstand {g:.2f} "
                                  f"(< {GAP_MIN:g}, {kind})")

    # (c) Rahmen umschliesst seinen Inhalt mit >= MARGIN_MIN
    modules = sorted({v['module'] for v in volumes})
    by_mod = {}
    for v in volumes:
        by_mod.setdefault(v['module'], []).append(v)
    min_margin, min_margin_ref = None, None
    n_below_target = 0
    for fr in frames['frames']:
        mod = fr['id'][len('frame-'):]
        match = next((m for m in modules if m.lower() == mod), None)
        if match is None:
            violations.append(f"(c) {fr['id']} hat kein Modul")
            continue
        content = by_mod.get(match, [])
        if not content:
            violations.append(f"(c) {fr['id']} hat keinen Inhalt")
            continue
        r = fr['rect']
        cmn_x = min(v['rect'][0] for v in content)
        cmn_y = min(v['rect'][1] for v in content)
        cmx_x = max(v['rect'][2] for v in content)
        cmx_y = max(v['rect'][3] for v in content)
        margins = (cmn_x - r['minX'], cmn_y - r['minY'],
                   r['maxX'] - cmx_x, r['maxY'] - cmx_y)
        m = min(margins)
        if min_margin is None or m < min_margin:
            min_margin, min_margin_ref = m, fr['id']
        if m < MARGIN_TARGET - EPS:
            n_below_target += 1
        if m < MARGIN_MIN - EPS:
            violations.append(f"(c) {fr['id']} Rand {m:.2f} < {MARGIN_MIN:g} "
                              f"(Inhalt {fmt_rect((cmn_x, cmn_y, cmx_x, cmx_y))})")

    # (d) Blockrahmen ueberlappen nicht
    n_overlap = 0
    frects = [(f['id'], (f['rect']['minX'], f['rect']['minY'],
                         f['rect']['maxX'], f['rect']['maxY'])) for f in frames['frames']]
    for i, (ida, ra) in enumerate(frects):
        for idb, rb in frects[i + 1:]:
            if rects_overlap(ra, rb):
                n_overlap += 1
                violations.append(f"(d) Rahmen {ida} <-> {idb} ueberlappen")

    print(f"check_plan_fit: {len(volumes)} Volumen, {len(frames['frames'])} Rahmen, "
          f"Nutzbereich x {usable['minX']}..{usable['maxX']} y {usable['minY']}..{usable['maxY']}")
    print(f"  (a) kleinster Rand eines Volumens zum Nutzbereich: "
          f"{min_edge[0]:.2f} ({min_edge[1]})  [>= 0]")
    print(f"  (b) kleinster Volumen-Abstand: {min_gap:.2f} "
          f"({min_gap_pair[0]} <-> {min_gap_pair[1]})  [>= {GAP_MIN:g}]")
    print(f"  (c) kleinster Rahmen-Rand: {min_margin:.2f} ({min_margin_ref})  "
          f"[hart >= {MARGIN_MIN:g}, Ziel >= {MARGIN_TARGET:g}; "
          f"{n_below_target} unter Ziel]")
    print(f"  (d) ueberlappende Blockrahmen: {n_overlap}  [= 0]")
    print(f"  Fallback-Schaetzungen (nicht gemessen): {len(fallbacks)}"
          + ((" -> " + ", ".join(sorted(fallbacks))) if fallbacks else ""))
    if violations:
        print(f"VERSTOESSE: {len(violations)}")
        for v in violations:
            print("  " + v)
        print("ERGEBNIS: FEHLER")
        return 1
    print("ERGEBNIS: OK")
    return 0


if __name__ == '__main__':
    sys.exit(main())
