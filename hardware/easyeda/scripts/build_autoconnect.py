#!/usr/bin/env python3
"""S4: autoconnect-Specs je Modul aus der kanonischen IR bauen.

Jeder Pin mit Netz bekommt genau eine Marke (ground / power / netport). Ausnahme:
U1s durchgehende GND-Pins 36..53 werden als Strombus mit EINEM Massezeichen verdrahtet
(die 18 Pins liegen im 10-raw-Raster direkt hintereinander; 18 einzelne Marker wuerden sich
ueberlagern und die Marker-Overlap-Regel des Caches verletzen).

Ausgang: raw/ac_<modul>.json  + raw/ac_summary.txt
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')

POWER = {'+3V3', 'VBAT', 'VBUS'}
GND_BUS_REF = 'U1'
GND_BUS_PINS = {str(n) for n in range(36, 54)}     # U1: durchgehende Massepins rechts

RULES = {"avoidTitleBlock": True, "avoidPinFanout": True, "staggerLabels": True,
         "offsetRange": [18, 150], "offsetStep": 6}


def main():
    ir = json.load(open(os.path.join(RAW, 'ir_numbered.json')))
    modules = json.load(open(os.path.join(RAW, 'modules.json')))
    net_name = {n['id']: n['name'] for n in ir['nets']}
    ref_of = {c['id']: c['ref'] for c in ir['components']}

    buckets = {}
    skipped = []
    for conn in ir['connections']:
        ref = ref_of[conn['componentId']]
        pin = conn['pinNumber']
        net = net_name[conn['netId']]
        if ref == GND_BUS_REF and net == 'GND' and pin in GND_BUS_PINS:
            skipped.append(f"{ref}:{pin}")
            continue
        if net == 'GND':
            kind = 'ground'
        elif net in POWER:
            kind = 'power'
        else:
            kind = 'netport'
        mod = modules[conn['componentId'][4:]]   # modules.json ist auf Originalnamen geschluesselt
        buckets.setdefault(mod, []).append({'pin': f"{ref}:{pin}", 'kind': kind, 'net': net})

    order = ['USB', 'LADER', 'AKKU', 'WAEChTER', 'LDO', 'MCU',
             'TASTER', 'PUMPE', 'SENSOR', 'DEBUG']
    total = 0
    lines = []
    for mod in order:
        conns = buckets.get(mod, [])
        # erst Masse/Versorgung (grosse Marker), dann Signale
        conns.sort(key=lambda c: (c['kind'] == 'netport', c['pin']))
        doc = {'connections': conns, 'rules': RULES}
        path = os.path.join(RAW, f'ac_{mod}.json')
        json.dump(doc, open(path, 'w'), ensure_ascii=False, indent=1)
        total += len(conns)
        by_kind = {}
        for c in conns:
            by_kind[c['kind']] = by_kind.get(c['kind'], 0) + 1
        lines.append(f"{mod:<9} {len(conns):>3} Verbindungen  {by_kind}")
    lines.insert(0, f"Verbindungen gesamt: {total} (uebersprungen: {len(skipped)} U1-GND-Pins fuer den Bus)")
    out = "\n".join(lines) + "\n"
    open(os.path.join(RAW, 'ac_summary.txt'), 'w').write(out)
    print(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
