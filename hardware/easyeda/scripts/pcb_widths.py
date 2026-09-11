#!/usr/bin/env python3
"""Leiterbahnbreiten der Platine pruefen und anwenden (P-Phase, SmartGrowTopf V1).

Die Sollbreiten stehen als Definition in ../netclass_spec.json (erzeugt von
netclass_spec.py nach IPC-2221A). Dieses Skript setzt sie auf der echten Platine
durch:

  --route-plan   zeigt die Verdrahtungsbefehle fuer die P-Phase (nichts wird geaendert)
  --check        liest die vorhandenen Leiterbahnen und meldet jede, die duenner als
                 ihre Sollbreite ist (Rueckgabewert 1 = Verstoss, gate-faehig)
  --apply        zieht zu duenne Bahnen auf Sollbreite nach (loeschen + neu zeichnen,
                 gleiche Lage/Netz/Endpunkte; gesperrte Bahnen werden nie angefasst)
  --selftest     prueft die Vergleichslogik ohne Platine (erfundene Bahnenliste)

Hintergrund: EasyEDA Pro kennt im Regelsatz nur EINE Standardbreite
(Physics.Track.copperThickness1oz defaultValue 0,254 mm / minValue 0,127 mm) —
keine Netzklassen. Die Rolle->Breite-Zuordnung stammt daher aus der Spezifikation
hier im Projekt; zusaetzlich leitet easyeda-agent aus dem Netznamen eine Rolle ab,
die aber zwei unserer Netze zu duenn einstuft (+3V3 und PUMP_N, siehe --route-plan).
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.abspath(os.path.join(HERE, "..", "netclass_spec.json"))
MIL = 0.0254


def load_spec():
    with open(SPEC) as f:
        return json.load(f)


def easyeda(args, timeout=180):
    env = dict(os.environ)
    env["PATH"] = os.path.expanduser("~/.local/bin") + os.pathsep + env.get("PATH", "")
    r = subprocess.run(["easyeda"] + args, capture_output=True, text=True, env=env, timeout=timeout)
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError(f"easyeda {' '.join(args)} fehlgeschlagen: {r.stderr.strip()[:300]}")
    return r.stdout


def read_json(out):
    """Erstes JSON-Dokument aus der CLI-Ausgabe (vorangestellte Warnzeilen ignorieren)."""
    return json.JSONDecoder().raw_decode(out.lstrip())[0]


def live_tracks(project, pcb_doc):
    res = read_json(easyeda(["--project", project, "--doc", pcb_doc, "pcb", "track-list"]))["result"]
    return res.get("lines") or []


def width_mm(track):
    w = track.get("lineWidth")
    return None if w is None else float(w) * MIL


def evaluate(tracks, spec):
    """Je Bahn: Sollbreite aus der Definition, Ist-Breite, Bewertung."""
    nets = spec["nets"]
    rows = []
    for t in tracks:
        net = t.get("net") or ""
        entry = nets.get(net)
        ist = width_mm(t)
        if entry is None:
            rows.append({"track": t, "net": net, "ist_mm": ist, "soll_mm": None,
                         "status": "unbekannt", "hinweis": "Netz nicht in der Spezifikation"})
            continue
        soll, minimum = entry.get("width_mm"), entry.get("min_width_mm")
        if not soll:                       # GND: Flaeche, keine Bahn
            status = "hinweis" if (ist or 0) >= 0.4 else "zu_duenn"
            rows.append({"track": t, "net": net, "ist_mm": ist, "soll_mm": None,
                         "status": status, "hinweis": "GND gehoert als Flaeche gelegt"})
            continue
        if ist is None:
            status, hinweis = "unlesbar", "keine Breite gelesen"
        elif ist + 1e-9 >= soll:
            status, hinweis = "ok", ""
        elif ist + 1e-9 >= minimum:
            status, hinweis = "warnung", f"unter Soll {soll} mm, aber ueber Minimum {minimum} mm"
        else:
            status, hinweis = "verstoss", f"unter Minimum {minimum} mm (Soll {soll} mm)"
        rows.append({"track": t, "net": net, "ist_mm": ist, "soll_mm": soll,
                     "min_mm": minimum, "status": status, "hinweis": hinweis})
    return rows


def selftest():
    spec = load_spec()
    fake = [
        {"primitiveId": "a", "net": "VBAT", "layer": 1, "startX": 0, "startY": 0, "endX": 100, "endY": 0,
         "lineWidth": 20, "locked": False},
        {"primitiveId": "b", "net": "PUMP_N", "layer": 1, "startX": 0, "startY": 0, "endX": 100, "endY": 0,
         "lineWidth": 10, "locked": False},          # zu duenn -> Verstoss
        {"primitiveId": "c", "net": "USB_DP", "layer": 1, "startX": 0, "startY": 0, "endX": 50, "endY": 0,
         "lineWidth": 10, "locked": False},          # ok (Signal 0,25 mm = 9,84 mil)
        {"primitiveId": "d", "net": "+3V3", "layer": 1, "startX": 0, "startY": 0, "endX": 50, "endY": 0,
         "lineWidth": 12, "locked": False},          # 0,30 mm -> ueber Minimum 0,25 -> Warnung
        {"primitiveId": "e", "net": "GND", "layer": 2, "startX": 0, "startY": 0, "endX": 50, "endY": 0,
         "lineWidth": 8, "locked": False},           # Flaeche erwartet -> zu_duenn
        {"primitiveId": "f", "net": "LED_STAT", "layer": 1, "startX": 0, "startY": 0, "endX": 30, "endY": 0,
         "lineWidth": 10, "locked": False},
        {"primitiveId": "g", "net": "UNBEKANNT", "layer": 1, "startX": 0, "startY": 0, "endX": 10, "endY": 0,
         "lineWidth": 10, "locked": False},
    ]
    rows = evaluate(fake, spec)
    got = {r["track"]["primitiveId"]: r["status"] for r in rows}
    want = {"a": "ok", "b": "verstoss", "c": "ok", "d": "warnung", "e": "zu_duenn",
            "f": "ok", "g": "unbekannt"}
    ok = got == want
    print("Selbsttest der Vergleichslogik:", "OK" if ok else "FEHLGESCHLAGEN")
    for pid in want:
        mark = "✓" if got[pid] == want[pid] else "✗"
        print(f"  {mark} {pid}: {got[pid]} (erwartet {want[pid]})")
    return 0 if ok else 1


def check(project, pcb_doc, spec, apply_fix, as_json):
    tracks = live_tracks(project, pcb_doc)
    rows = evaluate(tracks, spec)
    bad = [r for r in rows if r["status"] in ("verstoss", "zu_duenn")]
    warn = [r for r in rows if r["status"] in ("warnung", "unbekannt", "unlesbar")]
    if as_json:
        print(json.dumps({"tracks": len(tracks), "verstoesse": bad, "warnungen": warn},
                         indent=2, ensure_ascii=False))
    else:
        print(f"Leiterbahnen auf der Platine: {len(tracks)}")
        for r in rows:
            if r["status"] in ("ok",):
                continue
            ist = "?" if r["ist_mm"] is None else f"{r['ist_mm']:.2f} mm"
            soll = "Flaeche" if not r["soll_mm"] else f"{r['soll_mm']:.2f} mm"
            print(f"  [{r['status']:10}] {r['net']:12} ist {ist:>9} · soll {soll:>8} · {r['hinweis']}")
        print(f"  -> {len(bad)} Verstoss/Verstoesse, {len(warn)} Warnung(en)")
    if apply_fix and bad:
        for r in bad:
            t = r["track"]
            if t.get("locked"):
                print(f"  {r['net']}: gesperrt, uebersprungen")
                continue
            net = t["net"]
            width_mil = round(spec["nets"][net]["width_mm"] / MIL, 1)
            easyeda(["--project", project, "--doc", pcb_doc, "pcb", "track-delete",
                     "--ids", t["primitiveId"]])
            easyeda(["--project", project, "--doc", pcb_doc, "pcb", "track",
                     "--x1", str(t["startX"]), "--y1", str(t["startY"]),
                     "--x2", str(t["endX"]), "--y2", str(t["endY"]),
                     "--layer", str(t.get("layer", 1)), "--width", str(width_mil), "--net", net])
            print(f"  {net}: auf {width_mil} mil ({spec['nets'][net]['width_mm']} mm) neu gelegt")
    return 1 if bad else 0


def route_plan(spec):
    print("Verdrahtungsplan P-Phase (Sollbreiten aus netclass_spec.json):")
    print()
    print("  1) Masse/Schienen als Flaeche, nicht als duenne Bahnen:")
    print("       easyeda pcb power-pour                       # GND beidseitig + lokale Schienen")
    print("       easyeda pcb diff-pair create --name USB --positive USB_DP --negative USB_DM")
    print("       easyeda pcb route-critical                   # Flaechen + USB-Paar + Lock")
    print()
    print("  2) Netze, die easyeda-agent aus dem Namen RICHTIG einstuft (nichts zu tun):")
    for net in ("VBAT", "VBUS"):
        e = spec["nets"][net]
        print(f"       {net:8} -> {e['role']:13} {e['width_mm']} mm (high-current-Stufe)")
    print()
    print("  3) Netze, die EXPLIZIT breiter gelegt werden muessen (Namensheuristik zu duenn):")
    for net, auto in (("+3V3", "power-branch 0,25 mm"), ("PUMP_N", "signal 0,254 mm (Standardregel)")):
        e = spec["nets"][net]
        mil = round(e["width_mm"] / MIL, 1)
        print(f"       {net:8} automatisch {auto:32} -> Soll {e['width_mm']} mm = {mil} mil")
        print(f"                easyeda pcb track --x1 .. --y1 .. --x2 .. --y2 .. --net {net} --width {mil}")
    print()
    print("  4) Rest (Signale) routen — Standardbreite der Platine ist 0,254 mm, das passt:")
    print("       easyeda pcb route-short --width-power 20 --width-signal 10")
    print()
    print("  5) Pruefen:")
    print("       python3 scripts/pcb_widths.py --check      # Rueckgabewert 1 bei Verstoss")
    print("       easyeda pcb check && easyeda pcb drc")


def main():
    ap = argparse.ArgumentParser(description="Leiterbahnbreiten pruefen/anwenden (IPC-2221A-Spezifikation)")
    ap.add_argument("--project", default="SmartGrowTopf_V1")
    ap.add_argument("--pcb-doc", default="PCB1", help="PCB-Dokument (uuid oder Name)")
    ap.add_argument("--check", action="store_true", help="Ist-Breiten gegen die Spezifikation pruefen")
    ap.add_argument("--apply", action="store_true", help="zu duenne Bahnen auf Sollbreite nachziehen")
    ap.add_argument("--route-plan", action="store_true", help="Verdrahtungsbefehle der P-Phase ausgeben")
    ap.add_argument("--selftest", action="store_true", help="Vergleichslogik ohne Platine pruefen")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    spec = load_spec()
    if a.route_plan:
        route_plan(spec)
        return 0
    return check(a.project, a.pcb_doc, spec, a.apply, a.json)   # --check ist der Standard


if __name__ == "__main__":
    sys.exit(main())
