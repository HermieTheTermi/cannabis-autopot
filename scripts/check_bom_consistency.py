#!/usr/bin/env python3
"""Querabgleich Schaltplan <-> JLCPCB-BOM.

Geprüft wird:
 1. Designatoren: Schaltplan ↔ JLC-BOM (beide Richtungen vollständig).
 2. LCSC-Codes: wenn der Schaltplan einen nennt, muss er mit der CSV übereinstimmen.
 3. Werte bei R* und C*: Zahlenwert mit Einheiten-Präfix wird normiert und verglichen
    (100 nF == 100nF, 4,7 kΩ == 4.7k, 499 Ω == 499R). Für U/D/Q/J/SW wird nur das
    Vorhandensein und der LCSC-Code geprüft (dort sind die Bezeichnungen Freitext).

Prüfpunkte (kein BOM-Bauteil) werden über SKIP ignoriert.
Aufruf: python3 scripts/check_bom_consistency.py      Rückgabe 0 = sauber
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "hardware" / "schaltplan_v1.md"
CSV = ROOT / "hardware" / "pcba_bom_jlc.csv"

SKIP = {"TP1", "TP2", "TP3", "TP4", "TP5", "TP6"}  # Testpunkte, keine BOM-Positionen
DESIG = re.compile(r"^(U|C|R|D|Q|J|SW)\d*[a-z]?(_[A-Z0-9]+)*$")
OHM = {"k": 1e3, "m": 1e-3, "M": 1e6, "r": 1.0, "": 1.0}
FARAD = {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "": 1.0}


def canonical(designator: str, value: str) -> float | None:
    """Wert auf eine Basiseinheit normieren (Ohm bzw. Farad). None = nicht vergleichbar."""
    v = value.replace("**", "").replace("`", "").strip()
    v = re.sub(r"^\s*\d+\s*[×x]\s*", "", v)          # "2 × 100 nF" -> "100 nF"
    v = v.split("(")[0]                               # "(DNP)" abschneiden
    v = v.replace(",", ".").replace("µ", "u").replace("μ", "u").replace("Ω", "").replace("ω", "")
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*([a-zA-Z]*)", v)
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2).lower().strip()
    if designator.startswith("R"):
        pref = unit[0] if unit and unit[0] in "km" else ""
        if unit in ("kohm", "k"):  pref = "k"
        if unit in ("mohm", "m"):  pref = "m"
        if unit.startswith("k"):   pref = "k"
        if unit.startswith("m"):   pref = "m"
        if unit in ("", "r", "ohm"): pref = ""
        return num * OHM.get(pref, 1.0)
    if designator.startswith("C"):
        pref = unit[0] if unit else ""
        pref = {"u": "u", "µ": "u", "n": "n", "p": "p", "m": "m"}.get(pref, "")
        return num * FARAD.get(pref, 1.0)
    return None


def main() -> int:
    text = DOC.read_text(encoding="utf-8")
    doc_parts: dict[str, dict[str, str]] = {}
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        row = " | ".join(cells)
        lcsc = re.search(r"C\d{4,}", row)
        for name in (n.strip().strip("*`") for n in cells[0].split(",")):
            if not DESIG.match(name) or name in SKIP:
                continue
            doc_parts[name] = {"value": cells[1], "lcsc": lcsc.group(0) if lcsc else ""}

    csv_parts: dict[str, dict[str, str]] = {}
    for r in csv.DictReader(CSV.open(encoding="utf-8")):
        for d in r["Designator"].split():
            if d in csv_parts:
                print(f"  ✗ DOPPELTES DESIGNATOR in der JLC-BOM: {d}")
                return 1
            csv_parts[d] = {"value": r["Comment"], "lcsc": r.get("LCSC Part #", "")}

    problems: list[str] = []
    for name in sorted(set(doc_parts) - set(csv_parts)):
        problems.append(f"FEHLT IN DER JLC-BOM: {name} (Schaltplan: {doc_parts[name]['value']})")
    for name in sorted(set(csv_parts) - set(doc_parts)):
        problems.append(f"FEHLT IM SCHALTPLAN: {name} (JLC-BOM: {csv_parts[name]['value']})")

    for name in sorted(set(doc_parts) & set(csv_parts)):
        d, c = doc_parts[name], csv_parts[name]
        if d["lcsc"] and c["lcsc"] and d["lcsc"] != c["lcsc"]:
            problems.append(f"LCSC UNTERSCHIEDLICH bei {name}: {d['lcsc']} vs. {c['lcsc']}")
        dv, cv = canonical(name, d["value"]), canonical(name, c["value"])
        if dv is not None and cv is not None and abs(dv - cv) > max(1e-12, 0.001 * dv):
            problems.append(
                f"WERT UNTERSCHIEDLICH bei {name}: Schaltplan '{d['value']}' vs. BOM '{c['value']}'"
            )

    # 3. Richtung: Bauteile der Netzliste, die in Dokument oder BOM fehlen
    netlist = ROOT / "hardware" / "schaltplan_v1_netzliste.csv"
    if netlist.exists():
        net_parts = set()
        for r in csv.DictReader(netlist.open(encoding="utf-8")):
            if r["Netz"].strip().startswith("#"):   # Kommentarzeile
                continue
            for d in r["Bauteil"].split():
                if DESIG.match(d) and d not in SKIP:
                    net_parts.add(d)
        for name in sorted(net_parts - set(doc_parts)):
            problems.append(f"IN DER NETZLISTE, ABER NICHT IM SCHALTPLAN-DOKUMENT: {name}")
        for name in sorted(net_parts - set(csv_parts)):
            problems.append(f"IN DER NETZLISTE, ABER NICHT IN DER JLC-BOM: {name}")

    print(f"Schaltplan: {len(doc_parts)} Bauteile · JLC-BOM: {len(csv_parts)} Bauteile")
    if problems:
        print(f"\n{len(problems)} BEFUND(E):")
        for p in problems:
            print("  ✗", p)
        return 1
    print("\n✓ Schaltplan und JLC-BOM sind konsistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
