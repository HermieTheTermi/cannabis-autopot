#!/usr/bin/env python3
"""Selbstkonsistenzpruefung: erzeugte IR gegen die Handnetzliste.

Stellt die kanonische, designator-nummerierte IR (raw/ir_numbered.json) Pin fuer Pin
gegen hardware/schaltplan_v1_netzliste.csv und meldet jede Abweichung. Die Pin-Texte
werden mit DEMSELBEN Auflöser wie in build_ir.py aufgeloest (Symbol-Pin-Tabellen
stammen aus der IR selbst), verglichen wird (Bauteil, Pin) -> Netzname in beide
Richtungen.

Aufruf:
  python3 scripts/check_ir_netlist.py     -> Exit 0 bei 0 Abweichungen
"""
import csv
import json
import os
import sys

import build_ir

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, 'raw')
REPO = os.path.dirname(os.path.dirname(ROOT))


def main():
    ir = json.load(open(os.path.join(RAW, 'ir_numbered.json')))
    net_name = {n['id']: n['name'] for n in ir['nets']}
    comps = {c['id'][4:]: c for c in ir['components']}

    ir_map = {}
    for conn in ir['connections']:
        ir_map[(conn['componentId'][4:], conn['pinNumber'])] = net_name[conn['netId']]

    csv_pairs = {}
    problems, notes = [], []
    csv_path = os.path.join(REPO, 'hardware', 'schaltplan_v1_netzliste.csv')
    with open(csv_path, newline='', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            net = row['Netz'].strip()
            comp = row['Bauteil'].strip()
            spec = row['Pin'].strip()
            if row.get('Bemerkung', '').strip().startswith('#'):
                continue          # Kommentarzeile, keine Verbindung (kein Phantompin)
            rec = comps.get(comp)
            if rec is None:
                problems.append(f"{net}: unbekanntes Bauteil {comp!r}")
                continue
            try:
                nums = build_ir.resolve(spec, comp, rec['pins'])
            except KeyError as exc:
                problems.append(str(exc))
                continue
            if not nums:
                notes.append(f"{comp} {spec!r} ohne Pin (Datenblatt-Hinweis)")
                continue
            for num in nums:
                key = (comp, num)
                if key in csv_pairs and csv_pairs[key] != net:
                    problems.append(f"{comp}:{num} doppelt vergeben ({csv_pairs[key]} / {net})")
                csv_pairs[key] = net

    deviations = []
    for key, net in sorted(csv_pairs.items()):
        if key not in ir_map:
            deviations.append(f"{key[0]}:{key[1]} fehlt in IR (Netzliste: {net})")
        elif ir_map[key] != net:
            deviations.append(f"{key[0]}:{key[1]} IR={ir_map[key]} Netzliste={net}")
    for key, net in sorted(ir_map.items()):
        if key not in csv_pairs:
            deviations.append(f"{key[0]}:{key[1]} nur in IR (Netz {net})")

    print(f"IR:        {len(ir['components'])} Bauteile, {len(ir['nets'])} Netze, "
          f"{len(ir['connections'])} Verbindungen")
    print(f"Netzliste: {len(csv_pairs)} (Bauteil,Pin)-Paare aufgeloest")
    print(f"Abweichungen IR <-> Netzliste: {len(deviations)}")
    for d in deviations:
        print("  " + d)
    if problems:
        print(f"Aufloesungsprobleme: {len(problems)}")
        for p in problems:
            print("  " + p)
    for n in notes:
        print("  HINWEIS: " + n)
    if deviations or problems:
        return 1
    print("OK — 0 Abweichungen")
    return 0


if __name__ == '__main__':
    sys.exit(main())
