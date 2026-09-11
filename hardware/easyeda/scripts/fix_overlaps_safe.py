#!/usr/bin/env python3
"""S5-Kosmetik: die verbleibenden marker-overlaps sicher aufloesen.

Sichere Klinge (Lehre aus dem Vorfall vom 11.09.2026):
  * gearbeitet wird auf dem HOST-PIN, nicht auf einer Marker-ID — nach jedem
    disconnect/connect hat die Marke eine neue primitiveId;
  * `sch disconnect --flag-id <id>` trifft nur DIESE Stichleitung + Marke (kein Baum);
    die Antwort wird auf `alsoDisconnectedPins` geprueft (nicht leer => zurueck);
  * `sch connect --pin REF:PIN --direction … --offset …` haengt dieselbe Marke neu;
  * nach JEDEM Versuch: pin->net gegen raw/ir_numbered.json diffen (muss 0 bleiben)
    und marker-overlap-Zahl (muss sinken) — sonst exakt zurueck auf die Ausgangslage.

Aufruf: python3 scripts/fix_overlaps_safe.py
"""
import json
import os
import subprocess
import sys
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENV = dict(os.environ, PATH=os.path.expanduser('~/.local/bin') + ':' + os.environ['PATH'])
PAGE = '4f6771a27edec75b'
KIND = {'GND': 'ground', 'VBAT': 'power', '+3V3': 'power', 'VBUS': 'power'}


def run(args, timeout=240):
    return subprocess.run(['easyeda', '--project', 'SmartGrowTopf_V1', '--doc', PAGE] + args,
                          capture_output=True, text=True, env=ENV, cwd=ROOT, timeout=timeout)


def parse(text):
    return json.JSONDecoder().raw_decode(text.lstrip())[0]


def page():
    return parse(run(['sch', 'list', '--include-pins', '--include-bbox', '--include-wires']).stdout)['result']


def check():
    r = parse(run(['sch', 'check', '--json']).stdout)
    return r.get('result', r)


def overlaps(n):
    return [f for f in check()['findings'] if f['type'] == 'marker-overlap']


def deviations():
    ir = json.load(open(os.path.join(ROOT, 'raw', 'ir_numbered.json')))
    ref_of = {c['id']: c['ref'] for c in ir['components']}
    netname = {n['id']: n['name'] for n in ir['nets']}
    tgt = {(ref_of[c['componentId']], c['pinNumber']): netname[c['netId']]
           for c in ir['connections']}
    st = parse(run(['sch', 'read', '--no-check']).stdout).get('result', {})
    live = {(c['designator'], p['number']): p['net']
            for c in st['components'] if c.get('componentType') == 'part'
            for p in c['pins']}
    return [(k, tgt[k], live.get(k)) for k in tgt if live.get(k) != tgt[k]]


def host_pin(pg, marker):
    """Marker -> (designator, pinNumber, direction, offset) ueber seine Stichleitung."""
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
                    return c['designator'], pp['pinNumber'], d, int(max(abs(dx), abs(dy)))
    return None


def marker_ids_for(ref, pin):
    pg = page()
    out = []
    for c in pg['components']:
        if c.get('componentType') not in ('netflag', 'netport'):
            continue
        info = host_pin(pg, c)
        if info and info[0] == ref and info[1] == pin:
            out.append(c['primitiveId'])
    return out


def main():
    ck = check()
    n0 = len(overlaps(ck))
    print(f"marker-overlaps zu Beginn: {n0} | Netzabweichungen: {len(deviations())}", flush=True)
    # Kandidaten: Host-Pins der beteiligten Marker, Mehrfach-Overlaps zuerst
    pg = page()
    hits = defaultdict(int)
    for f in overlaps(ck):
        for pid in (f['primitiveId'], (f.get('other') or {}).get('primitiveId')):
            if not pid:
                continue
            m = next((c for c in pg['components'] if c.get('primitiveId') == pid), None)
            if not m:
                continue
            info = host_pin(pg, m)
            if info:
                hits[(info[0], info[1], info[2], info[3], m.get('net'))] += 1
    cands = sorted(hits.items(), key=lambda kv: -kv[1])
    for (ref, pin, cur_dir, cur_off, net), cnt in cands:
        kind = KIND.get(net, 'netport')
        base = len(overlaps(check()))
        print(f"  {ref}:{pin} {net} ({cur_dir}/{cur_off}) x{cnt} — {base} overlaps", flush=True)
        improved = False
        for direction in [d for d in ('down', 'up', 'right', 'left') if d != cur_dir]:
            for offset in (30, 55, 90):
                ids = marker_ids_for(ref, pin)
                if not ids:
                    break
                dr = run(['sch', 'disconnect', '--flag-id', ids[0]])
                if '"ok": true' not in dr.stdout:
                    print("    disconnect abgelehnt — Abbruch", flush=True)
                    break
                try:
                    also = parse(dr.stdout)['result'].get('alsoDisconnectedPins') or []
                except Exception:
                    also = []
                if also:
                    print(f"    ⚠ {len(also)} fremde Pins mitgetrennt — zurueck", flush=True)
                    run(['sch', 'connect', '--pin', f"{ref}:{pin}", '--kind', kind, '--net', net,
                         '--direction', cur_dir, '--offset', str(cur_off)])
                    break
                cr = run(['sch', 'connect', '--pin', f"{ref}:{pin}", '--kind', kind, '--net', net,
                          '--direction', direction, '--offset', str(offset)])
                if '"ok": true' not in cr.stdout:
                    continue
                dev = deviations()
                if dev:
                    print(f"    Netzverletzung {dev[:2]} — zurueck", flush=True)
                else:
                    now = len(overlaps(check()))
                    if now < base:
                        print(f"    -> {direction}@{offset}: {base} -> {now}", flush=True)
                        improved = True
                        break
                # zuruecksetzen
                ids = marker_ids_for(ref, pin)
                if ids:
                    run(['sch', 'disconnect', '--flag-id', ids[0]])
                run(['sch', 'connect', '--pin', f"{ref}:{pin}", '--kind', kind, '--net', net,
                     '--direction', cur_dir, '--offset', str(cur_off)])
                time.sleep(0.2)
            if improved:
                break
        if not improved:
            print("    keine Verbesserung moeglich", flush=True)
        time.sleep(0.3)
    fin = check()
    print("marker-overlaps am Ende:", len(overlaps(fin)), "| Netzabweichungen:", len(deviations()), flush=True)
    print(json.dumps(fin['summary'], ensure_ascii=False), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
