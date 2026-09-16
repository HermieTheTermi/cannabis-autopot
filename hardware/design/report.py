"""CLI-Bericht fuer den Schaltplan V1 (2S-Umbau).

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
    print("-" * 100)
    print("%-2s %-28s %-8s %-34s %s" % ("#", "Pruefung", "Ergebnis", "Ist", "Soll"))
    print("-" * 100)
    for nr, r in enumerate(results, 1):
        status = "OK" if r.bestanden else "FEHLER"
        print("%-2d %-28s %-8s %-34s %s" % (nr, r.name, status, r.ist, r.soll))
        print("   Begruendung: %s" % r.begruendung)
    print("-" * 100)


def print_sims(data):
    sys = circuit.load_system()
    rb = data["rb"]
    gate = data["gate"]
    charge = data["charge"]
    runtime = data["runtime"]
    inrush = data["inrush"]
    print("Simulationen (Annahmen sind unten genannt)")
    print("-" * 100)
    print("Gate-Treiber @ %s PWM (R1 %s, R2 %s, Ciss %s):"
          % (_f(sys["pwm_hz"] / 1000.0, 0, "kHz"),
             _f(rb["R1"] / 1000.0, 1, "kΩ"),
             _f(rb["R2"] / 1000.0, 0, "kΩ"),
             _f(rb["ciss"] * 1e12, 0, "pF")))
    print("   Zeitkonstante tau = %s, VGS-Endwert = %s, Zeit bis 2,5 V = %s"
          % (_f(gate["tau_us"], 2, "µs"), _f(gate["v_ziel"], 2, "V"),
             _f(gate["t_ein_us"], 2, "µs")))
    print("   GPIO-Strom: Peak %s, Mittel %s (Periode %s)"
          % (_f(gate["i_peak_ma"], 3, "mA"), _f(gate["i_mittel_ma"], 3, "mA"),
             _f(gate["periode_us"], 1, "µs")))
    print("Ladezeit 2S (%s, ICHG %s):"
          % (_f(charge["capacity_mah"], 0, "mAh"),
             _f(charge["i_charge_a"], 2, "A")))
    print("   CC %s + CV %s = %s (grob, CC/CV-Anteile sind Annahmen)"
          % (_f(charge["t_cc_h"], 2, "h"), _f(charge["t_cv_h"], 2, "h"),
             _f(charge["t_total_h"], 2, "h")))
    print("Dosiervorgang aus der 5-V-Schiene (Pumpe %s, %s):"
          % (_f(sys["pump_i_nom_a"], 1, "A"), _f(runtime["p_w"], 2, "W")))
    print("   %s pro %s => %s; nutzbar %s => %s Dosen pro Ladung"
          % (_f(runtime["wh_dosis"], 4, "Wh"), _f(sys["dose_ml"], 0, "ml"),
             _f(runtime["t_min"], 2, "min"),
             _f(rb["usable_wh"], 2, "Wh"), _f(runtime["dosen"], 1, "")))
    print("Pumpenanlauf (%s, R_BAT %s):"
          % (_f(sys["pump_i_inrush_a"], 1, "A"), _f(inrush["r_bat"], 2, "Ω")))
    print("   Packstrom %s, VBAT %s -> %s, Einbruch %s"
          % (_f(inrush["i_bat"], 2, "A"), _f(sys["pack_v_min"], 1, "V"),
             _f(inrush["v_min"], 2, "V"), _f(inrush["einbruch_v"] * 1000.0, 0, "mV")))
    for name, key in (("5-V-Buck", "ripple5"), ("3,3-V-Buck", "ripple3")):
        r = data[key]
        print("%s-Rippel (Vin %s): D %s, dI %s, I_peak %s"
              % (name, _f(sys["pack_v_max"], 1, "V"), _f(r["d"], 3, ""),
                 _f(r["di"], 2, "A"), _f(r["i_peak"], 2, "A")))
    print("Teilerstroeme bei %s:"
          % _f(sys["pack_v_max"], 1, "V"))
    print("   Waechter (R3a/R3b) %s, ADC (R_SENSE_*) %s"
          % (_f(data["divider"]["uvlo_a"] * 1e6, 1, "µA"),
             _f(data["divider"]["adc_a"] * 1e6, 1, "µA")))
    print("Standby in mAh/Tag: %s = %s/Tag (%s der %s-Packkapazitaet)"
          % (_f(data["standby"]["total_ua"], 1, "µA"),
             _f(data["standby"]["mah_day"], 2, "mAh"),
             _f(data["standby"]["mah_day"] / sys["pack_capacity_mah"] * 100.0, 3, "%"),
             _f(sys["pack_capacity_mah"], 0, "mAh")))
    tank = data["tank"]
    print("Tank-LED-Blinken (D5, R_TANK %s, Vf 2,0 V): %d x %s alle %s "
          "(Tastverhaeltnis %s):"
          % (_f(rb["R_TANK"] / 1000.0, 1, "kΩ"), tank["pulse"],
             _f(tank["t_on_ms"], 0, "ms"), _f(tank["periode_s"], 0, "s"),
             _f(tank["tastverhaeltnis_prozent"], 1, "%")))
    print("   Dauerbetrieb %s, Mittel %s -> %s/Tag statt %s/Tag"
          % (_f(tank["i_dauer_ma"], 2, "mA"), _f(tank["i_mittel_ma"], 2, "mA"),
             _f(tank["mittel_mah_pro_tag"], 2, "mAh"),
             _f(tank["dauer_mah_pro_tag"], 1, "mAh")))
    light = data["light"]
    print("Licht-ADC (ALS-PT19, R_LIGHT %s, ATTEN3 0-3300 mV, 12 Bit):"
          % _f(rb["R_LIGHT"] / 1000.0, 0, "kΩ"))
    print("   " + "; ".join(
        "%s lx -> %s Counts (%s V)"
        % (_f(e["lux"], 0, ""), _f(e["counts"], 0, ""), _f(e["v"], 3, ""))
        for e in light))
    print("Annahmen: " + "; ".join(data["assumptions"]))
    print("-" * 100)


def main():
    try:
        results = checks.run_all()
        simulations = sim.run_all()
    except checks.PruefFehler as exc:
        # Werkzeugfehler: das Pruefmodell passt nicht zur Netzliste.  Das ist
        # KEIN Design-Fehler und wird nicht als "Pruefung fehlgeschlagen"
        # gezaehlt -- eigener Exit-Code 2 macht das unmissverstaendlich.
        print("Werkzeugfehler: %s" % exc)
        return 2
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
