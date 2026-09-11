#!/usr/bin/env python3
"""S5-Feinschliff: Cluster-Befunde (Marker ragen aus dem Blatt / ueberlappen Fremdbauteile)
durch gezieltes Umhaengen einzelner Marker beheben.

Sicherheitsnetz je Aenderung:
  * `sch disconnect --flag-id` (nur diese Stichleitung + Marke) — Antwort auf
    alsoDisconnectedPins wird geprueft, fremde Pins werden nicht akzeptiert;
  * `sch connect --pin ... --direction ... --offset ...` haengt dieselbe Marke neu;
  * danach Netzliste gegen raw/ir_numbered.json vergleichen (muss exakt bleiben)
    und `sch clusters` zaehlen — nur behalten, wenn Fehlerzahl sinkt, sonst zurueck.

Aufruf: python3 scripts/fix_clusters.py
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENV = dict(os.environ, PATH=os.path.expanduser('~/.local/bin') + ':' + os.environ['PATH'])
G = ['--project', 'SmartGrowTopf_V1', '--doc', 'P1']
KIND = {'GND': 'ground', 'VBAT': 'power', '+3V3': 'power', 'VBUS': 'power'}


def run(args, timeout=180):
    return subprocess.run(['easyeda'] + G + args, capture_output=True, text=True,
                          env=ENV, cwd=ROOT, timeout=timeout)


def parse(text):
    dec = json.JSONDecoder()
    return dec.raw_decode(text.lstrip())[0]


def page():
    return parse(run(['sch', 'list', '--include-pins', '--include-bbox', '--include-wires']).stdout)['result']


def clusters():
    out = run(['sch', 'clusters', '--json'])
    p = parse(out.stdout)
    r = p.get('result', p)
    errs = [f for f in r.get('findings') or [] if f.get('level') == 'ERROR']
    return len(errs), r


def netlist_ok():
    ir = json.load(open(os.path.join(ROOT, 'raw', 'ir_numbered.json')))
    ref_of = {c['id']: c['ref'] for c in ir['components']}
    netname = {n['id']: n['name'] for n in ir['nets']}
    target = {(ref_of[c['componentId']], c['pinNumber']): netname[c['netId']]
              for c in ir['connections']}
    st = parse(run(['sch', 'read', '--no-check']).stdout)['result']
    live = {(c['designator'], p['number']): p['net']
            for c in st['components'] if c.get('componentType') == 'part'
            for p in c['pins']}
    bad = [(k, target[k], live.get(k)) for k in target if live.get(k) != target[k]]
    return bad


def host_pin(pg, marker):
    pin = (marker['pins'][0]['x'], marker['pins'][0]['y']) if marker.get('pins') else (marker['x'], marker['y'])
    for w in pg.get('wires') or []:
        ends = [(w['x0'], w['y0']), (w['x1'], w['y1'])]
        near = [e for e in ends if abs(e[0] - pin[0]) <= 2 and abs(e[1] - pin[1]) <= 2]
        if not near:
            continue
        far = ends[1] if near[0] == ends[0] else ends[0]
        for c in pg['components']:
            if c.get('componentType') != 'part':
                continue
            for pp in c.get('pins') or []:
                if abs(pp['x'] - far[0]) <= 1 and abs(pp['y'] - far[1]) <= 1:
                    dx, dy = pin[0] - far[0], pin[1] - far[1]
                    d = ('right' if dx > 0 else 'left') if abs(dx) > abs(dy) else ('up' if dy > 0 else 'down')
                    return c['designator'], pp['pinNumber'], d, max(abs(dx), abs(dy))
    return None


def main():
    pg = page()
    markers = {c['primitiveId']: c for c in pg['components']
               if c.get('componentType') in ('netflag', 'netport')}
    errs, rep = clusters()
    print(f"Cluster-Fehler zu Beginn: {errs}", flush=True)
    seen = set()
    for f in rep.get('findings') or []:
        if f.get('level') != 'ERROR':
            continue
        ref = f.get('a')
        # zum Bauteil gehoerende Marker mit problematischer Lage suchen
        cands = [m for m in markers.values()
                 if any(p['x'] == m['x'] and p['y'] == m['y']
                        for c in pg['components'] if c.get('designator') == ref
                        for p in (c.get('pins') or []))]
        if not cands:
            # Marker direkt ueber die bbox zuordnen (Marker ragt ueber das Blatt)
            bb = f.get('bbox')
            if bb:
                cands = [m for m in markers.values()
                         if m['bbox']['minX'] <= bb['maxX'] and bb['minX'] <= m['bbox']['maxX']
                         and m['bbox']['minY'] <= bb['maxY'] and bb['minY'] <= m['bbox']['maxY']]
        for m in cands[:1]:
            pid = m['primitiveId']
            if pid in seen:
                continue
            seen.add(pid)
            info = host_pin(pg, m)
            if not info:
                print(f"  {pid}: Host-Pin unbekannt", flush=True)
                continue
            href, hpin, cur_dir, cur_off = info
            net = m.get('net')
            kind = KIND.get(net, 'netport')
            print(f"  {pid} {net} an {href}:{hpin} ({cur_dir}/{cur_off:.0f})", flush=True)
            improved = False
            for direction in [d for d in ('up', 'right', 'down', 'left') if d != cur_dir]:
                for offset in (30, 50, 80):
                    dr = run(['sch', 'disconnect', '--flag-id', pid])
                    if '"ok": true' not in dr.stdout:
                        print("    disconnect abgelehnt", flush=True)
                        break
                    try:
                        also = parse(dr.stdout)['result'].get('alsoDisconnectedPins') or []
                    except Exception:
                        also = []
                    if also:
                        print(f"    ⚠ {len(also)} fremde Pins mitgetrennt -> zurueck", flush=True)
                        run(['sch', 'connect', '--pin', f"{href}:{hpin}", '--kind', kind,
                             '--net', net, '--direction', cur_dir, '--offset', str(int(cur_off))])
                        break
                    cr = run(['sch', 'connect', '--pin', f"{href}:{hpin}", '--kind', kind,
                              '--net', net, '--direction', direction, '--offset', str(offset)])
                    if '"ok": true' not in cr.stdout:
                        continue
                    bad = netlist_ok()
                    if bad:
                        print(f"    Netzliste verletzt ({bad[:2]}) -> zurueck", flush=True)
                        run(['sch', 'disconnect', '--flag-id', pid])
                        run(['sch', 'connect', '--pin', f"{href}:{hpin}", '--kind', kind,
                             '--net', net, '--direction', cur_dir, '--offset', str(int(cur_off))])
                        continue
                    e2, _ = clusters()
                    if e2 < errs:
                        print(f"    -> {direction}@{offset} besser ({errs} -> {e2})", flush=True)
                        errs = e2
                        improved = True
                        pg = page()
                        markers = {c['primitiveId']: c for c in pg['components']
                                   if c.get('componentType') in ('netflag', 'netport')}
                        break
                if improved:
                    break
            if not improved:
                print("    -> keine Verbesserung", flush=True)
    print("Ende. Cluster-Fehler:", errs, flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
