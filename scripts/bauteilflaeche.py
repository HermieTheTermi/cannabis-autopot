#!/usr/bin/env python3
"""Bauteilflaeche und Platinengroesse fuer den SmartGrowTopf (cannabis-autopot).

Rechnet aus der Stueckliste (hardware/pcba_bom_jlc.csv) den Flaechenbedarf der
Bauteile und daraus die noetige Platinengroesse.

Datenquellen
------------
1. BOM: hardware/pcba_bom_jlc.csv  (Bauteil -> Designatoren -> Footprint -> LCSC)
2. Footprint-Bounding-Box je LCSC-Code aus der EasyEDA-Produkt-API
     https://easyeda.com/api/products/<LCSC>/svgs     (docType 4 = Footprint)
   Die "-bbox" darin ist in 0.01 inch -> mm = Wert * 0.254.
   Ergebnis wird in hardware/pcb/footprint_bbox.json zwischengespeichert.
3. Gegenprobe: live-`pcb dump` des alten Boards
     hardware/easyeda/s5/archiv/pcb_vor_neuaufbau_2026-09-14.json  (40 Roheinheiten = 1 mm)

Aufruf
------
    python3 scripts/bauteilflaeche.py            # rechnet + schreibt Tabellen
    python3 scripts/bauteilflaeche.py --nofetch  # nur aus dem Cache rechnen
"""
from __future__ import annotations

import csv
import json
import math
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOM = os.path.join(ROOT, "hardware/pcba_bom_jlc.csv")
CACHE = os.path.join(ROOT, "hardware/pcb/footprint_bbox.json")

MM_PER_UNIT = 0.254          # API-bbox-Einheit (0.01 inch)
RAW_PER_MM = 40.0            # Einheiten des live-`pcb dump` je mm
EDGE = 2.5                   # Randaufschlag je Platinenkante [mm]


# ---------------------------------------------------------------- Footprints --
def fetch_footprints(codes: list[str]) -> dict:
    out = {}
    for c in codes:
        r = subprocess.run([
            "curl", "-s", "-m", "30",
            f"https://easyeda.com/api/products/{c}/svgs",
            "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
            "-H", "Referer: https://easyeda.com/",
            "-H", "Accept: application/json",
        ], capture_output=True, text=True)
        try:
            res = json.loads(r.stdout).get("result") or []
        except Exception:
            res = []
        fp = [x for x in res if x.get("docType") == 4]
        if fp:
            b = fp[0].get("bbox") or {}
            out[c] = [round(b.get("width", 0) * MM_PER_UNIT, 3),
                      round(b.get("height", 0) * MM_PER_UNIT, 3)]
        else:
            out[c] = None
        time.sleep(0.4)
    return out


def load_footprints(codes: list[str], nofetch: bool) -> dict:
    cached = {}
    if os.path.exists(CACHE):
        cached = json.load(open(CACHE))
    todo = [c for c in codes if c not in cached or cached[c] is None]
    if todo and not nofetch:
        print(f"[i] {len(todo)} Footprints von der EasyEDA-API holen ...")
        cached.update(fetch_footprints(todo))
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        json.dump(cached, open(CACHE, "w"), indent=1, sort_keys=True)
    return cached


# ---------------------------------------------------------------------- BOM --
def bom_lines(fpb: dict) -> list[dict]:
    lines = []
    for r in csv.DictReader(open(BOM)):
        refs = r["Designator"].split()
        lcsc = (r["LCSC Part #"] or "").strip()
        dim = fpb.get(lcsc)
        w = max(dim) if dim else None
        h = min(dim) if dim else None
        lines.append(dict(comment=r["Comment"], fp=r["Footprint"], lcsc=lcsc,
                          refs=refs, n=len(refs), w=w, h=h,
                          area=(w * h) if w else None))
    return lines


# ---------------------------------------------------------------- Packmass --
def pack(rects, W, H, rot=True):
    """MaxRects (Best-Short-Side-Fit). None, wenn nicht alles passt."""
    free = [(0.0, 0.0, W, H)]
    placed = []
    for (w, h) in sorted(rects, key=lambda r: (max(r), r[0] * r[1]), reverse=True):
        best = None
        for (fx, fy, fw, fh) in free:
            for (ww, hh) in ([(w, h), (h, w)] if rot else [(w, h)]):
                if ww <= fw + 1e-9 and hh <= fh + 1e-9:
                    key = (min(fw - ww, fh - hh), max(fw - ww, fh - hh))
                    if best is None or key < best[0]:
                        best = (key, fx, fy, ww, hh)
        if best is None:
            return None
        _, x, y, ww, hh = best
        placed.append((x, y, ww, hh))
        nf = []
        for (fx, fy, fw, fh) in free:
            if x >= fx + fw or x + ww <= fx or y >= fy + fh or y + hh <= fy:
                nf.append((fx, fy, fw, fh))
                continue
            if x > fx:
                nf.append((fx, fy, x - fx, fh))
            if x + ww < fx + fw:
                nf.append((x + ww, fy, fx + fw - (x + ww), fh))
            if y > fy:
                nf.append((fx, fy, fw, y - fy))
            if y + hh < fy + fh:
                nf.append((fx, y + hh, fw, fy + fh - (y + hh)))
        keep = []
        for i, a in enumerate(nf):
            cont = False
            for j, b in enumerate(nf):
                if i == j:
                    continue
                if (a[0] >= b[0] - 1e-9 and a[1] >= b[1] - 1e-9 and
                        a[0] + a[2] <= b[0] + b[2] + 1e-9 and
                        a[1] + a[3] <= b[1] + b[3] + 1e-9):
                    if (a[2], a[3]) != (b[2], b[3]) or j < i:
                        cont = True
                        break
            if not cont:
                keep.append(a)
        free = keep
    return placed


def min_height(rects, W, gap, hi=400.0):
    infl = [(w + gap, h + gap) for (w, h) in rects]
    if pack(infl, W, hi) is None:
        return None
    lo = 1.0
    while hi - lo > 0.5:
        mid = (lo + hi) / 2
        if pack(infl, W, mid) is not None:
            hi = mid
        else:
            lo = mid
    return hi


# ---------------------------------------------------------------------- Run --
def main() -> None:
    nofetch = "--nofetch" in sys.argv
    codes = sorted({(r["LCSC Part #"] or "").strip()
                    for r in csv.DictReader(open(BOM))} - {""})
    fpb = load_footprints(codes, nofetch)
    lines = bom_lines(fpb)

    total = sum((l["area"] or 0) * l["n"] for l in lines)
    count = sum(l["n"] for l in lines if l["area"])
    rects = [(l["w"], l["h"]) for l in lines if l["w"] for _ in l["refs"]]
    print(f"\n{count} Bauteile mit Flaeche, Summe Bauraum = {total:.1f} mm²\n")

    print("== Einzelposten (absteigend) ==")
    for l in sorted(lines, key=lambda x: -(x["area"] or 0) * x["n"]):
        if not l["area"]:
            continue
        print("  %-30s %-26s %-9s n=%2d  %5.2f x %5.2f mm  %7.1f mm²"
              % (l["comment"][:30], l["fp"][:26], l["lcsc"], l["n"],
                 l["w"], l["h"], l["area"] * l["n"]))

    print("\n== Kleinstes umschliessendes Rechteck (MaxRects-Packmass) ==")
    for gap in (0.2, 0.6, 1.0):
        row = []
        for W in (40, 48, 54, 60, 70, 80):
            H = min_height(rects, W, gap)
            row.append("W=%d -> L>=%s" % (W, ("%.1f" % H) if H else "n/a"))
        print("  Fuge %.1f mm: %s" % (gap, " | ".join(row)))

    print("\n== Boardgroesse aus Belegungsdichte (Flaeche = Summe / Dichte) ==")
    print("  Randaufschlag %.1f mm je Kante\n" % EDGE)
    print("   Dichte | Boardflaeche | L bei W=54 | Quadrat (L=B)")
    for d in (0.25, 0.30, 0.35, 0.40, 0.427, 0.45):
        A = total / d
        print("   %5.1f%% | %8.0f mm² | %8.1f mm | %8.1f mm"
              % (d * 100, A, A / (54 - 2 * EDGE) + 2 * EDGE, math.sqrt(A)))

    A40 = total / 0.40
    print("\n   Formvergleich bei %.0f mm²:" % A40)
    for W in (38.0, 54.0, math.sqrt(A40)):
        print("     W = %5.1f mm -> L = %5.1f mm, Umfang %5.1f mm"
              % (W, A40 / W, 2 * (W + A40 / W)))


if __name__ == "__main__":
    main()
