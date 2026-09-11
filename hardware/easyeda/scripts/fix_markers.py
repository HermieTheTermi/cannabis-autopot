#!/usr/bin/env python3
"""S5-Nacharbeit: Marker-Ueberlappungen und Leitungsquerungen gezielt aufloesen.

Vorgehen je Befund:
  1. beteiligte Marker (netflag/netport) bestimmen,
  2. ihren Host-Pin ueber die Stichleitung finden (ein Segmentende am Marker,
     das andere exakt auf einem Pin),
  3. Stichleitung trennen (`sch disconnect --pin`) und mit einer anderen
     Richtung/Laenge neu verbinden (`sch connect`),
  4. `sch check` messen — nur behalten, wenn die Gesamtzahl der Befunde sinkt,
     sonst zurueckdrehen.

Aufruf: python3 scripts/fix_markers.py [--budget-min 12]
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENV = dict(os.environ, PATH=os.path.expanduser('~/.local/bin') + ':' + os.environ['PATH'])
G = ['--project', 'SmartGrowTopf_V1', '--doc', 'P1']
KINDS = {'GND': 'ground', '+3V3': 'power', 'VBAT': 'power', 'VBUS': 'power'}


def run(args, timeout=180):
    return subprocess.run(['easyeda'] + G + args, capture_output=True, text=True,
                          env=ENV, cwd=ROOT, timeout=timeout)


def load_page():
    r = run(['sch', 'list', '--include-pins', '--include-bbox', '--include-wires'])
    return json.loads(r.stdout)['result']


def findings():
    r = run(['sch', 'check', '--json'])
    return json.loads(r.stdout)['result']


def check_total(res):
    return res['summary']['total']


def marker_host_pin(page, marker):
    """Marker -> (designator, pinNumber, direction, offset, net) ueber die Stichleitung.

    `sch list --include-wires` liefert achsenparallele Segmente {net,x0,y0,x1,y1};
    der Marker hat seinen Anschlusspunkt in pins[0]."""
    pin = None
    if marker.get('pins'):
        pin = (marker['pins'][0]['x'], marker['pins'][0]['y'])
    else:
        pin = (marker['x'], marker['y'])
    for w in page.get('wires') or []:
        ends = [(w['x0'], w['y0']), (w['x1'], w['y1'])]
        near = [e for e in ends if abs(e[0] - pin[0]) <= 2 and abs(e[1] - pin[1]) <= 2]
        if not near:
            continue
        far = ends[1] if near[0] == ends[0] else ends[0]
        for c in page['components']:
            if c.get('componentType') != 'part':
                continue
            for pp in c.get('pins') or []:
                if abs(pp['x'] - far[0]) <= 1 and abs(pp['y'] - far[1]) <= 1:
                    dx, dy = pin[0] - far[0], pin[1] - far[1]
                    if abs(dx) > abs(dy):
                        direction = 'right' if dx > 0 else 'left'
                    else:
                        direction = 'up' if dy > 0 else 'down'
                    return (c['designator'], pp['pinNumber'], direction,
                            max(abs(dx), abs(dy)), marker.get('net') or pp.get('net'))
    return None


def main():
    budget = 12 * 60
    start = time.time()
    page = load_page()
    res = findings()
    base = check_total(res)
    print(f"Start: {base} Befunde", flush=True)

    markers = {c['primitiveId']: c for c in page['components']
               if c.get('componentType') in ('netflag', 'netport') and c.get('primitiveId')}

    def problems(res):
        out = []
        for f in res['findings']:
            if f['type'] == 'marker-overlap':
                out += [f.get('primitiveId'), (f.get('other') or {}).get('primitiveId')]
            elif f['type'] in ('reversed-net-flag', 'duplicate-net-marker', 'redundant-net-marker'):
                out.append(f.get('primitiveId'))
        return [i for i in out if i in markers]

    tried = set()
    while time.time() - start < budget:
        res = findings()
        before = check_total(res)
        todo = [i for i in problems(res) if i not in tried]
        if not todo:
            print("keine weiteren behebbaren Marker-Befunde", flush=True)
            break
        pid = todo[0]
        tried.add(pid)
        m = markers.get(pid)
        if not m:
            continue
        info = marker_host_pin(page, m)
        if not info:
            print(f"  {pid}: Host-Pin nicht aufloesbar (net={m.get('net')})", flush=True)
            continue
        ref, pin, cur_dir, cur_off, net = info
        kind = KINDS.get(net, 'netport')
        print(f"  {pid} net={net} pin={ref}:{pin} dir={cur_dir} off={cur_off:.0f} (Befunde {before})", flush=True)
        best = None
        for direction in [d for d in ('up', 'down', 'left', 'right') if d != cur_dir]:
            for offset in (30, 60, 100):
                run(['sch', 'disconnect', '--pin', f"{ref}:{pin}"])
                cr = run(['sch', 'connect', '--pin', f"{ref}:{pin}", '--kind', kind,
                          '--net', net, '--direction', direction, '--offset', str(offset)])
                if '"ok": true' not in cr.stdout:
                    continue
                after = check_total(findings())
                if after < before:
                    best = (after, direction, offset)
                    break
                # zuruecksetzen für den naechsten Versuch
                run(['sch', 'disconnect', '--pin', f"{ref}:{pin}"])
            if best:
                break
        if best:
            print(f"    -> behalten: {best[1]} @{best[2]} (Befunde {before} -> {best[0]})", flush=True)
        else:
            print("    -> keine Verbesserung, zuruecksetzen", flush=True)
            run(['sch', 'disconnect', '--pin', f"{ref}:{pin}"])
            run(['sch', 'connect', '--pin', f"{ref}:{pin}", '--kind', kind, '--net', net,
                 '--direction', cur_dir, '--offset', str(int(cur_off))])
    print("fertig, verstrichen: %.0f s" % (time.time() - start), flush=True)
    final = findings()
    print("Endstand:", json.dumps(final['summary'], ensure_ascii=False), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
