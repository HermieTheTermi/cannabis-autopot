#!/usr/bin/env python3
"""S5-Reparatur: Pins, deren Netz nach der Marker-Nacharbeit abweicht, sauber neu verbinden.

Je Pin: `sch disconnect --pin` (alte Stichleitung + Marke weg), dann
`sch autoconnect --pin` (Marke auf dem jetzt freien Pin neu setzen).
Am Ende Gegenprobe gegen raw/ir_numbered.json.

Aufruf: python3 scripts/repair_pins.py
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


def live_state():
    r = run(['sch', 'read', '--no-check'])
    return json.loads(r.stdout)['result']


def deviations():
    ir = json.load(open(os.path.join(ROOT, 'raw', 'ir_numbered.json')))
    ref_of = {c['id']: c['ref'] for c in ir['components']}
    netname = {n['id']: n['name'] for n in ir['nets']}
    target = {(ref_of[c['componentId']], c['pinNumber']): netname[c['netId']]
              for c in ir['connections']}
    st = live_state()
    live = {(c['designator'], p['number']): p['net']
            for c in st['components'] if c.get('componentType') == 'part'
            for p in c['pins']}
    return [(k, target[k], live.get(k)) for k in sorted(target) if live.get(k) != target[k]], st


def main():
    todo, st = deviations()
    print(f"Abweichungen vor der Reparatur: {len(todo)}", flush=True)
    fixed = 0
    for (ref, pin), want, have in todo:
        kind = KIND.get(want, 'netport')
        dr = run(['sch', 'disconnect', '--pin', f"{ref}:{pin}"])
        time.sleep(0.4)
        ar = run(['sch', 'autoconnect', '--pin', f"{ref}:{pin}", '--kind', kind,
                  '--net', want, '--json'])
        ok = '"ok": true' in ar.stdout or '"succeeded"' in ar.stdout
        print(f"  {ref}:{pin} {have} -> {want}  disconnect={dr.returncode} connect={ok}", flush=True)
        fixed += 1 if ok else 0
        time.sleep(0.3)
    todo2, st = deviations()
    print(f"verbunden: {fixed}; Abweichungen danach: {len(todo2)}", flush=True)
    for t in todo2:
        print("   REST", t, flush=True)
    print("netCount", st['netCount'], "floatingPins", st['floatingPinCount'], flush=True)
    return 0 if not todo2 else 1


if __name__ == '__main__':
    sys.exit(main())
