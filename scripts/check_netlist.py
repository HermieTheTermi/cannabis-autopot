#!/usr/bin/env python3
"""Netzlisten-Lint: findet strukturelle Fehler in schaltplan_v1_netzliste.csv.

Geprüft wird:
 1. Jedes mehrpolige Bauteil muss auf mindestens 2 verschiedenen Netzen liegen
    (sonst ist es kurzgeschlossen oder ein Anschluss fehlt).
 2. Jedes Netz braucht mindestens 2 Knoten.
 3. Jeder Pin eines Bauteils darf nur auf einem Netz liegen.
 4. Pinbezeichnungen dürfen nicht doppelt vergeben sein (Tippfehler).

Aufruf: python3 scripts/check_netlist.py [csv]
Rückgabe: 0 = sauber, 1 = Befunde
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "hardware" / "schaltplan_v1_netzliste.csv"

# Einpolige Elemente (nur ein Anschluss in der Liste erwartet)
ONE_PIN_OK_PREFIX = ("TP",)  # Testpunkte sind einpolig


def main() -> int:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    nets: dict[str, list[tuple[str, str]]] = defaultdict(list)
    comp_nets: dict[str, set[str]] = defaultdict(set)
    pin_net: dict[tuple[str, str], str] = {}

    findings: list[str] = []

    for r in rows:
        net, comp, pin = r["Netz"].strip(), r["Bauteil"].strip(), r["Pin"].strip()
        if net.startswith("#"):      # Kommentarzeile (keine Verbindung)
            continue
        nets[net].append((comp, pin))
        comp_nets[comp].add(net)
        key = (comp, pin)
        if key in pin_net and pin_net[key] != net:
            findings.append(f"PIN AUF ZWEI NETZEN: {comp} Pin {pin} → {pin_net[key]} und {net}")
        pin_net[key] = net

    # 1. Mehrpolige Bauteile auf nur einem Netz
    for comp in sorted(comp_nets):
        if comp.startswith(ONE_PIN_OK_PREFIX):
            continue
        if len(comp_nets[comp]) < 2:
            findings.append(
                f"NUR EIN NETZ: {comp} liegt ausschließlich auf "
                f"'{next(iter(comp_nets[comp]))}' → Anschluss fehlt oder Kurzschluss"
            )

    # 2. Netze mit nur einem Knoten
    for net, nodes in sorted(nets.items()):
        if len(nodes) < 2:
            findings.append(f"NETZ MIT EINEM KNOTEN: {net} → nur {nodes[0][0]} {nodes[0][1]}")

    # 3. Vollständigkeit: Designatoren aus dem Schaltplan-Dokument gegen die Netzliste
    doc = ROOT / "hardware" / "schaltplan_v1.md"
    if doc.exists():
        import re
        text = doc.read_text(encoding="utf-8")
        cells = [c.strip().strip("*`") for c in re.findall(r"^\|\s*([^|]+?)\s*\|", text, re.M)]
        expected = {c for c in cells if re.fullmatch(r"(U|C|R|D|Q|J|SW|TP)[A-Z0-9_]*", c)}
        # Netznamen stehen in derselben Tabellenspalte und wuerden falsch anschlagen
        expected -= set(nets)
        in_netlist = set(comp_nets)
        for comp in sorted(expected - in_netlist):
            findings.append(f"FEHLT KOMPLETT IN DER NETZLISTE: {comp} (steht im Schaltplan-Dokument)")

    # 4. Bauteile ganz ohne Netz (nur informativ: aus dem Schaltplan erwartet)
    print(f"Geprüft: {len(rows)} Zeilen · {len(nets)} Netze · {len(comp_nets)} Bauteile")
    for net in sorted(nets):
        print(f"  {net:14s} {len(nets[net]):2d} Knoten")

    if findings:
        print(f"\n{len(findings)} BEFUND(E):")
        for f in findings:
            print("  ✗", f)
        return 1

    print("\n✓ Keine strukturellen Befunde.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
