"""CLI-Bericht fuer den Schaltplan V1.

Aufruf:
    python3 -m design.report        (aus hardware/ heraus)
    python3 hardware/design/report.py

Gibt erst alle Design-Regelpruefungen mit Ist/Soll, danach die Simulationen
aus.  Exit-Code 1, sobald eine Pruefung fehlschlaegt.
"""
from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from design import checks, circuit, sim
else:
    from . import checks, circuit, sim


def _f(value, decimals, unit=""):
    text = ("%%.%df" % decimals) % value
    return text.replace(".", ",") + ((" " + unit) if unit else "")


def print_checks(results):
    print("Pruefungen: %d" % len(results))
    print("-" * 96)
    print("%-2s %-28s %-8s %-30s %s" % ("#", "Pruefung", "Ergebnis", "Ist", "Soll"))
    print("-" * 96)
    for nr, r in enumerate(results, 1):
        status = "OK" if r.bestanden else "FEHLER"
        print("%-2d %-28s %-8s %-30s %s" % (nr, r.name, status, r.ist, r.soll))
        print("   Begruendung: %s" % r.begruendung)
    print("-" * 96)


def print_sims(data):
    gate = data["gate"]
    inrush = data["inrush"]
    runtime = data["runtime"]
    print("Simulationen")
    print("-" * 96)
    print("Gate-Treiber @ %s PWM (R1 %s, R2 %s, Ciss %s):"
          % (_f(circuit.load_system()["pwm_hz"] / 1000.0, 0, "kHz"),
             _f(data["rb"]["R1"] / 1000.0, 1, "kΩ"),
             _f(data["rb"]["R2"] / 1000.0, 0, "kΩ"),
             _f(data["rb"]["Ciss"] * 1e12, 0, "pF")))
    print("   Zeitkonstante tau = %s, VGS-Endwert = %s"
          % (_f(gate["tau_us"], 2, "µs"), _f(gate["v_ziel"], 2, "V")))
    print("   Zeit bis VGS 2,5 V = %s (Periode %s, Ein/Aus-Anteil %s)"
          % (_f(gate["t_ein_us"], 2, "µs"), _f(gate["periode_us"], 1, "µs"),
             _f(gate["anteil_prozent"], 1, "%")))
    print("   GPIO-Strom: Peak %s, Mittel %s"
          % (_f(gate["i_peak_ma"], 3, "mA"), _f(gate["i_mittel_ma"], 3, "mA")))
    print("Pumpen-Einschaltstrom (%s Puffer, 1 A Lastsprung fuer 1 ms, "
          "R_BAT %s):"
          % (_f(data["rb"]["C3"] * 1e6, 0, "µF"), _f(inrush["r_bat"], 2, "Ω")))
    print("   VBAT %s -> %s, Einbruch %s (Elko allein: %s)"
          % (_f(inrush["v_start"], 2, "V"), _f(inrush["v_ende"], 3, "V"),
             _f(inrush["einbruch_mv"], 1, "mV"),
             _f(inrush["kapazitaet_ideal_mv"], 1, "mV")))
    print("Akkulaufzeit (Zelle %s, %s nutzbar):"
          % (_f(circuit.load_system()["battery_mah"], 0, "mAh"),
             _f(circuit.load_system()["battery_usable_wh"], 2, "Wh")))
    print("   %s pro Dosis (%s), %s Dosen pro Ladung"
          % (_f(runtime["wh_dosis"], 4, "Wh"), _f(runtime["zeit_min"], 2, "min"),
             _f(runtime["dosen"], 1, "")))
    print("LDO-Erwaermung im TX-Burst (I = %s):"
          % _f(circuit.load_system()["tx_peak_ma"], 0, "mA"))
    print("   P = (VBAT - 3,3 V) · I: %s bei VBAT 4,2 V, %s bei VBAT 3,7 V"
          % (_f(data["heat_max_w"], 4, "W"), _f(data["heat_nom_w"], 4, "W")))
    tank = data["tank"]
    print("Tank-LED-Blinken (D5, R_TANK %s): %d x %s alle %s "
          "(Tastverhaeltnis %s):"
          % (_f(data["rb"]["R_TANK"] / 1000.0, 1, "kΩ"), tank["pulse"],
             _f(tank["t_on_ms"], 0, "ms"), _f(tank["periode_s"], 0, "s"),
             _f(tank["tastverhaeltnis_prozent"], 1, "%")))
    print("   Dauerbetrieb %s, Mittel %s -> %s/Tag statt %s/Tag"
          % (_f(tank["i_dauer_ma"], 2, "mA"), _f(tank["i_mittel_ma"], 2, "mA"),
             _f(tank["mittel_mah_pro_tag"], 2, "mAh"),
             _f(tank["dauer_mah_pro_tag"], 1, "mAh")))
    print("-" * 96)


def main():
    try:
        results = checks.run_all()
        simulations = sim.run_all()
    except circuit.CircuitError as exc:
        print("FEHLER: %s" % exc)
        return 1
    except FileNotFoundError as exc:
        print("FEHLER: Datei nicht gefunden: %s" % exc)
        return 1

    print_checks(results)
    print_sims(simulations)

    failed = [r for r in results if not r.bestanden]
    print("Ergebnis: %d von %d Pruefungen bestanden, %d fehlgeschlagen."
          % (len(results) - len(failed), len(results), len(failed)))
    if failed:
        print("Fehlgeschlagen:")
        for r in failed:
            print("  - %s: Ist %s, Soll %s" % (r.name, r.ist, r.soll))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
