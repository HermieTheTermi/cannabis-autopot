"""Design-Regelpruefungen fuer den Schaltplan V1.

Jede Pruefung liest die echten Dateien ueber :mod:`design.circuit` und liefert
ein :class:`CheckResult` mit (name, bestanden, ist_wert, soll_kriterium,
begruendung).  Hart verdrahtet sind nur Datenblatt-Grenzwerte; die Quelle steht
jeweils in der Begruendung.
"""
from __future__ import annotations

from collections import defaultdict, namedtuple

from . import circuit

CheckResult = namedtuple("CheckResult", "name bestanden ist soll begruendung")


def _f(value, decimals, unit=""):
    text = ("%%.%df" % decimals) % value
    return text.replace(".", ",") + ((" " + unit) if unit else "")


def _err(designator):
    return circuit.CircuitError("fehlender Designator: %s" % designator)


def check_ladestrom():
    """MCP73831: I = 1000 / R_PROG[kΩ], Ziel 180-350 mA."""
    r_prog = circuit.parse_ohm(circuit.part("R_PROG")["value"])
    i_ma = 1000.0 / (r_prog / 1000.0)
    led = ("MCP73831-Datenblatt: RPROG 10 kΩ → 100 mA, 2 kΩ → 500 mA; "
           "I = 1000/RPROG[kΩ]")
    return CheckResult(
        "Ladestrom", 180.0 <= i_ma <= 350.0,
        "%s (R_PROG %s)" % (_f(i_ma, 1, "mA"), _f(r_prog / 1000.0, 1, "kΩ")),
        "180-350 mA", led)


def check_laderkondensatoren():
    """MCP73831: Ein-/Ausgang mindestens 4,7 uF."""
    c7 = circuit.parse_farad(circuit.part("C7")["value"])
    c8 = circuit.parse_farad(circuit.part("C8")["value"])
    limit = 4.7e-6
    return CheckResult(
        "Laderkondensatoren", c7 >= limit and c8 >= limit,
        "C7 %s, C8 %s" % (_f(c7 * 1e6, 1, "µF"), _f(c8 * 1e6, 1, "µF")),
        "C7 >= 4,7 µF und C8 >= 4,7 µF",
        "MCP73831-Datenblatt: Bypass mit mindestens 4,7 µF")


def check_max809_klemmstrom():
    """MAX809-Ausgang nur bis ISINK = 1,2 mA belasten."""
    r1 = circuit.parse_ohm(circuit.part("R1")["value"])
    i_ma = (3.0 - 0.3) / r1 * 1000.0
    return CheckResult(
        "MAX809-Klemmstrom", i_ma <= 1.2,
        "%s (R1 %s)" % (_f(i_ma, 3, "mA"), _f(r1 / 1000.0, 1, "kΩ")),
        "<= 1,2 mA",
        "MAX809-Datenblatt: ISINK = 1,2 mA bei VOL <= 0,3 V; "
        "I = (3,0 V - 0,3 V)/R1")


def check_gate_spannung():
    """Gate-Spannung aus dem Teiler R1/R2 im Betrieb."""
    r1 = circuit.parse_ohm(circuit.part("R1")["value"])
    r2 = circuit.parse_ohm(circuit.part("R2")["value"])
    rail = circuit.load_system()["rail_3v3"]
    v = rail * r2 / (r1 + r2)
    return CheckResult(
        "Gate-Spannung", v >= 2.5 and v > 1.45,
        "%s (%.0f %% von %s)" % (_f(v, 2, "V"), r2 / (r1 + r2) * 100.0,
                                 _f(rail, 1, "V")),
        ">= 2,5 V und > 1,45 V",
        "AO3400A-Datenblatt: RDS(on) bei VGS = 2,5 V spezifiziert, "
        "VGS(th) max = 1,45 V")


def check_mosfet_verlust():
    """Leitverluste des Pumpen-MOSFET Q1."""
    i_pump = circuit.load_system()["pump_current_a"]
    rds_on = 0.048  # AO3400A-Datenblatt: < 48 mΩ bei VGS = 2,5 V
    p = i_pump * i_pump * rds_on
    return CheckResult(
        "MOSFET-Verlustleistung", p <= 0.25,
        "%s (I %s, RDS(on) 48 mΩ)" % (_f(p * 1000.0, 1, "mW"),
                                      _f(i_pump * 1000.0, 0, "mA")),
        "<= 0,25 W",
        "AO3400A-Datenblatt: 48 mΩ bei VGS = 2,5 V; P = I_pump² · RDS(on)")


def check_freilaufdiode():
    """Freilaufdiode D1: Stromreserve und Sperrspannung."""
    sys = circuit.load_system()
    i_pump = sys["pump_current_a"]
    if_a = sys["diode_if_a"]
    vrrm = sys["diode_vrrm"]
    vbat_max = sys["charge_voltage"]
    ok = i_pump <= 0.5 * if_a and vrrm >= 4.0 * vbat_max
    return CheckResult(
        "Freilaufdiode", ok,
        "I %s (<= 50 %% von %s), VRRM %s (>= 4 x %s)"
        % (_f(i_pump * 1000.0, 0, "mA"), _f(if_a, 1, "A"),
           _f(vrrm, 0, "V"), _f(vbat_max, 1, "V")),
        "I_pump <= 0,5 A und VRRM >= 4 x VBAT_max",
        "1N5819WS-Datenblatt: 1 A / 40 V; Stromreserve und Spannungsreserve "
        "fuer die Induktivitaet der Pumpe")


def check_vbat_teiler():
    """ADC-Spannung am VBAT-Teiler R3a/R3b (11 dB-Bereich)."""
    sys = circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    vbat_max = sys["charge_voltage"]
    v = vbat_max * r3b / (r3a + r3b)
    return CheckResult(
        "VBAT-Teiler", 1.25 <= v <= 2.5,
        "%s bei VBAT %s" % (_f(v, 2, "V"), _f(vbat_max, 2, "V")),
        "1,25 V bis 2,5 V",
        "Espressif-ADC (11 dB): Messbereich bis ca. 2,5 V; "
        "Teiler 1:2 haelt VBAT_max darunter")


def check_teilerstrom():
    """Ruhestrom des VBAT-Teilers."""
    sys = circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    i_ua = sys["charge_voltage"] / (r3a + r3b) * 1e6
    return CheckResult(
        "Teilerstrom", i_ua <= 15.0,
        "%s bei %s" % (_f(i_ua, 1, "µA"), _f(sys["charge_voltage"], 2, "V")),
        "<= 15 µA",
        "Standby-Budget: Teiler dominiert den Ruheverbrauch; "
        "I = VBAT_max/(R3a+R3b)")


def check_ldo_reserve():
    """LDO-Ausgangsstrom gegen den WLAN-TX-Peak."""
    sys = circuit.load_system()
    ldo_ma = sys["ldo_current_a"] * 1000.0
    tx_ma = sys["tx_peak_ma"]
    return CheckResult(
        "LDO-Stromreserve", ldo_ma >= 1.1 * tx_ma,
        "%s (>= 1,1 x %s)" % (_f(ldo_ma, 0, "mA"), _f(tx_ma, 0, "mA")),
        "ME6211 500 mA >= 1,1 x TX-Peak",
        "Espressif-Datenblatt Tab. 6-4: 382 mA TX-Peak, "
        "Espressif fordert >= 500 mA Regler")


def check_ldo_headroom():
    """LDO-Headroom bei niedriger Zellspannung."""
    sys = circuit.load_system()
    vbat_low = sys["firmware_stop_v"]
    dropout = 0.3  # ME6211-Datenblatt: Dropout ca. 0,3 V bei hohem Strom
    v_min_module = 3.0  # Espressif: Modul-Minimum 3,0 V
    v = vbat_low - dropout
    return CheckResult(
        "LDO-Headroom", v >= v_min_module,
        "%s bei VBAT %s (Dropout %s)"
        % (_f(v, 2, "V"), _f(vbat_low, 1, "V"), _f(dropout, 1, "V")),
        "VBAT - Dropout >= 3,0 V",
        "Espressif: Modul-Minimum 3,0 V; ME6211-Dropout ca. 0,3 V")


def check_uv_staffelung():
    """Die Unterspannungsschwellen muessen monoton fallen."""
    sys = circuit.load_system()
    fw = sys["firmware_stop_v"]
    m809 = sys["max809_v"]
    pcm = sys["pcm_v"]
    return CheckResult(
        "Unterspannungsstaffelung", fw > m809 > pcm,
        "Firmware %s > MAX809 %s > PCM %s"
        % (_f(fw, 2, "V"), _f(m809, 2, "V"), _f(pcm, 1, "V")),
        "Firmware > MAX809 > PCM",
        "Firmware stoppt zuerst, dann Hardware, zuletzt die Zelle "
        "(bom_entscheidung.md 4b)")


def check_standby_budget():
    """Ruhestrom und Monatsverbrauch im Deep-Sleep."""
    sys = circuit.load_system()
    total_ua = (sys["module_sleep_ua"] + sys["ldo_quiescent_ua"]
                + sys["max809_quiescent_ua"] + sys["divider_current_ua"])
    monthly_mah = total_ua / 1000.0 * 24.0 * 30.0
    ok = total_ua <= 100.0 and monthly_mah <= 0.05 * sys["battery_mah"]
    return CheckResult(
        "Standby-Budget", ok,
        "%s, %s/Monat (%s der Zelle)"
        % (_f(total_ua, 1, "µA"), _f(monthly_mah, 1, "mAh"),
           _f(monthly_mah / sys["battery_mah"] * 100.0, 2, "%")),
        "<= 100 µA und <= 5 %/Monat von 1500 mAh",
        "Summe Modul 7 µA + LDO 40 µA + MAX809 12 µA + Teiler 10,5 µA "
        "(schaltplan_v1.md 6.3)")


def check_adc_filter():
    """RC-Zeitkonstanten der beiden ADC-Kanaele."""
    r6 = circuit.parse_ohm(circuit.part("R6")["value"])
    c9 = circuit.parse_farad(circuit.part("C9")["value"])
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    c10 = circuit.parse_farad(circuit.part("C10")["value"])
    t_sensor = r6 * c9
    r_par = 1.0 / (1.0 / r3a + 1.0 / r3b)
    t_vbat = r_par * c10
    ok = t_sensor <= 5e-3 and t_vbat <= 50e-3
    return CheckResult(
        "ADC-Filter", ok,
        "R6·C9 %s, (R3a||R3b)·C10 %s"
        % (_f(t_sensor * 1000.0, 2, "ms"), _f(t_vbat * 1000.0, 1, "ms")),
        "R6·C9 <= 5 ms und (R3a||R3b)·C10 <= 50 ms",
        "Espressif-ADC: 0,1 µF Filter; Zeitkonstante begrenzt das Einschwingen")


def check_led_stroeme():
    """LED-Stroeme von Status- und Lade-LED."""
    sys = circuit.load_system()
    r4 = circuit.parse_ohm(circuit.part("R4")["value"])
    r_chg = circuit.parse_ohm(circuit.part("R_LEDCHG")["value"])
    vf = 2.0        # rote 0805-LED, typische Flussspannung (Datenblatt)
    vbus = 5.0      # USB-C-VBUS
    i_stat = (sys["rail_3v3"] - vf) / r4
    i_chg = (vbus - vf) / r_chg
    ok = i_stat <= 5e-3 and i_chg <= 5e-3
    return CheckResult(
        "LED-Stroeme", ok,
        "Status %s, Laden %s"
        % (_f(i_stat * 1000.0, 2, "mA"), _f(i_chg * 1000.0, 2, "mA")),
        "Status- und Lade-LED <= 5 mA",
        "LED-Vorwiderstaende R4 bzw. R_LEDCHG; Vf rot ca. 2,0 V")


def check_en_rc():
    """EN-RC-Glied laut Espressif (10 kΩ + 1 µF, tSTBL 50 µs)."""
    r_en = circuit.parse_ohm(circuit.part("R_EN")["value"])
    c4 = circuit.parse_farad(circuit.part("C4")["value"])
    t = r_en * c4
    return CheckResult(
        "EN-RC", t >= 1e-3,
        "%s (R_EN %s, C4 %s)"
        % (_f(t * 1000.0, 1, "ms"), _f(r_en / 1000.0, 1, "kΩ"),
           _f(c4 * 1e6, 1, "µF")),
        "R_EN·C4 >= 1 ms",
        "Espressif: R = 10 kΩ und C = 1 µF am EN-Pin; tSTBL nur 50 µs")


def check_netzstruktur():
    """Strukturpruefung der Netzliste (wie scripts/check_netlist.py)."""
    netlist = circuit.load_netlist()
    comp_nets = defaultdict(set)
    for net, nodes in netlist.items():
        for comp, _pin in nodes:
            comp_nets[comp].add(net)
    findings = []
    for comp in sorted(comp_nets):
        if comp.startswith(circuit.ONE_PIN_OK_PREFIX):
            continue
        if len(comp_nets[comp]) < 2:
            findings.append("%s nur auf einem Netz" % comp)
    for net, nodes in sorted(netlist.items()):
        if len(nodes) < 2:
            findings.append("Netz %s hat nur einen Knoten" % net)
    ok = not findings
    ist = "%d Netze, %d Bauteile, %d Befunde" % (len(netlist), len(comp_nets), len(findings))
    detail = "" if ok else " (" + "; ".join(findings) + ")"
    return CheckResult(
        "Netzstruktur", ok, ist + detail,
        "jedes Bauteil auf >= 2 Netzen, jedes Netz mit >= 2 Knoten",
        "Strukturfehler wie Kurzschluss oder fehlender Anschluss "
        "(scripts/check_netlist.py)")


def run_all():
    """Fuehrt alle Pruefungen in fester Reihenfolge aus."""
    checks = [
        check_ladestrom,
        check_laderkondensatoren,
        check_max809_klemmstrom,
        check_gate_spannung,
        check_mosfet_verlust,
        check_freilaufdiode,
        check_vbat_teiler,
        check_teilerstrom,
        check_ldo_reserve,
        check_ldo_headroom,
        check_uv_staffelung,
        check_standby_budget,
        check_adc_filter,
        check_led_stroeme,
        check_en_rc,
        check_netzstruktur,
    ]
    return [fn() for fn in checks]


if __name__ == "__main__":
    for result in run_all():
        print("%-28s %s  %s" % (result.name, "OK" if result.bestanden else "FEHLER",
                                 result.ist))
