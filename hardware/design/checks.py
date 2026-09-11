"""Design-Regelpruefungen fuer den Schaltplan V1.

Jede Pruefung liest die echten Dateien ueber :mod:`design.circuit` und liefert
ein :class:`CheckResult` mit (name, bestanden, ist_wert, soll_kriterium,
begruendung).  Hart verdrahtet sind nur Datenblatt-Grenzwerte; die Quelle steht
jeweils in der Begruendung.
"""
from __future__ import annotations

import re
from collections import defaultdict, namedtuple

from . import circuit

CheckResult = namedtuple("CheckResult", "name bestanden ist soll begruendung")

# Datenblatt-Fakten zum ESP32-C6 (als Konstanten mit Quelle hart verdrahtet).
# Espressif ESP32-C6-Datenblatt: LP-/RTC-GPIOs sind GPIO0 bis GPIO7.
LP_GPIO_MIN, LP_GPIO_MAX = 0, 7
# Espressif-Modul-Datenblatt: "Strapping pin: GPIO8 and GPIO9 · MTMS and MTDI",
# "GPIO15". MTMS = GPIO4, MTDI = GPIO5, dazu GPIO8, GPIO9 und GPIO15.
STRAPPING_GPIOS = frozenset({4, 5, 8, 9, 15})

# Typische Flussspannung der 0805-LEDs je LCSC-Code (Datenblattwerte).
# C84256: NATIONSTAR NCD0805R1, rot, 615-630 nm -> Vf ca. 2,0 V
# C2297:  KENTO KT-0805G, gruen, 525 nm (InGaN) -> Vf ca. 2,85 V
LED_VF_BY_LCSC = {
    "C84256": 2.0,
    "C2297": 2.85,
}


def _f(value, decimals, unit=""):
    text = ("%%.%df" % decimals) % value
    return text.replace(".", ",") + ((" " + unit) if unit else "")


def _err(designator):
    return circuit.CircuitError("fehlender Designator: %s" % designator)


def led_vf(designator):
    """Typische Flussspannung einer LED aus ihrem LCSC-Code in schaltplan_v1.md.

    Unbekannte Codes sind ein harter Fehler, damit nicht stillschweigend eine
    falsche Flussspannung angenommen wird.
    """
    lcsc = circuit.part(designator).get("lcsc")
    if not lcsc:
        raise circuit.CircuitError(
            "kein LCSC-Code fuer %s in schaltplan_v1.md" % designator)
    if lcsc not in LED_VF_BY_LCSC:
        raise circuit.CircuitError(
            "unbekannter LCSC-Code %r fuer %s: Flussspannung in "
            "LED_VF_BY_LCSC ergaenzen" % (lcsc, designator))
    return LED_VF_BY_LCSC[lcsc]


def _nets_of(designator):
    """Netz -> Pin fuer alle Pins eines Bauteils aus der Netzliste."""
    result = {}
    for net, nodes in circuit.load_netlist().items():
        for comp, pin in nodes:
            if comp == designator:
                result.setdefault(net, pin)
    return result


def _btn_net():
    """Name des Tasternetzes, auf dem R_BTN und C_BTN gemeinsam liegen."""
    r_nets = _nets_of("R_BTN")
    c_nets = _nets_of("C_BTN")
    shared = sorted(set(r_nets) & set(c_nets))
    if len(shared) != 1:
        raise circuit.CircuitError(
            "Tasternetz nicht eindeutig: R_BTN auf %s, C_BTN auf %s"
            % (sorted(r_nets), sorted(c_nets)))
    return shared[0]


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
    """LED-Stroeme von Status- und Lade-LED, je LED mit eigener Vf."""
    sys = circuit.load_system()
    r4 = circuit.parse_ohm(circuit.part("R4")["value"])
    r_chg = circuit.parse_ohm(circuit.part("R_LEDCHG")["value"])
    vf_stat = led_vf("D2")            # gruene Status-LED, C2297
    vf_chg = led_vf("D_LEDCHG")       # rote Lade-LED, C84256
    vbus = 5.0                        # USB-C-VBUS
    i_stat = (sys["rail_3v3"] - vf_stat) / r4
    i_chg = (vbus - vf_chg) / r_chg
    ok = i_stat <= 5e-3 and i_chg <= 5e-3
    return CheckResult(
        "LED-Stroeme", ok,
        "Status (Vf %s, R4 %s) %s, Laden (Vf %s, R_LEDCHG %s) %s"
        % (_f(vf_stat, 2, "V"), _f(r4, 0, "Ω"),
           _f(i_stat * 1000.0, 2, "mA"),
           _f(vf_chg, 2, "V"), _f(r_chg / 1000.0, 1, "kΩ"),
           _f(i_chg * 1000.0, 2, "mA")),
        "Status- und Lade-LED <= 5 mA",
        "I = (U - Vf)/R; D2 gruen Vf 2,85 V ueber R4, "
        "D_LEDCHG rot Vf 2,0 V ueber R_LEDCHG")


def check_tank_led():
    """Tank-LED D5 mit Vorwiderstand R_TANK."""
    sys = circuit.load_system()
    r_tank = circuit.parse_ohm(circuit.part("R_TANK")["value"])
    vf = led_vf("D5")                 # rote Tank-LED, C84256
    i = (sys["rail_3v3"] - vf) / r_tank
    return CheckResult(
        "Tank-LED", i <= 5e-3,
        "%s bei Vf %s (R_TANK %s)"
        % (_f(i * 1000.0, 2, "mA"), _f(vf, 1, "V"),
           _f(r_tank / 1000.0, 1, "kΩ")),
        "I <= 5 mA, Vf rot ca. 2,0 V",
        "LED-Vorwiderstand R_TANK; D5 und D_LEDCHG sind die roten "
        "0805-LEDs (Vf 2,0 V), D2 ist die gruene")


def check_led_headroom():
    """Headroom am 3,3-V-Rail und nutzbares Stromfenster je LED."""
    sys = circuit.load_system()
    rail = sys["rail_3v3"]
    vbus = 5.0                        # USB-C-VBUS an D_LEDCHG
    specs = (
        ("D2", "R4", rail),
        ("D_LEDCHG", "R_LEDCHG", vbus),
        ("D5", "R_TANK", rail),
    )
    headroom_min = 0.3
    i_min, i_max = 0.5e-3, 5.0e-3
    teile = []
    ok = True
    for led, r_des, supply in specs:
        vf = led_vf(led)
        r = circuit.parse_ohm(circuit.part(r_des)["value"])
        headroom = rail - vf
        i = (supply - vf) / r
        head_ok = headroom >= headroom_min
        strom_ok = i_min <= i <= i_max
        ok = ok and head_ok and strom_ok
        teile.append(
            "%s (Vf %s): Headroom %s %s, %s %s"
            % (led, _f(vf, 2, "V"), _f(headroom, 2, "V"),
               "OK" if head_ok else "FEHLER", _f(i * 1000.0, 2, "mA"),
               "OK" if strom_ok else "FEHLER"))
    return CheckResult(
        "LED-Headroom", ok,
        "; ".join(teile),
        "je LED 3,3 V - Vf >= 0,3 V und 0,5-5 mA",
        "3,3-V-Rail-Headroom und Stromfenster je LED; Headroom gegen "
        "die 3,3-V-Schiene, Strom aus der jeweiligen Versorgung "
        "(D_LEDCHG an 5 V VBUS)")


def check_btn_pullup():
    """Externer Taster: Pull-up R_BTN nach +3V3, C_BTN nach GND, RC-Zeit."""
    btn = _btn_net()
    r_nets = _nets_of("R_BTN")
    c_nets = _nets_of("C_BTN")
    r_other = sorted(n for n in r_nets if n != btn)
    c_other = sorted(n for n in c_nets if n != btn)
    r_ok = r_other == ["+3V3"]
    c_ok = c_other == ["GND"]
    r = circuit.parse_ohm(circuit.part("R_BTN")["value"])
    c = circuit.parse_farad(circuit.part("C_BTN")["value"])
    tau = r * c
    tau_ok = 0.5e-3 <= tau <= 20e-3
    return CheckResult(
        "Taster-Pullup", r_ok and c_ok and tau_ok,
        "%s: R_BTN %s %s-%s, C_BTN %s %s-%s, R·C %s"
        % (btn, _f(r / 1000.0, 1, "kΩ"), "+3V3", btn,
           _f(c * 1e6, 1, "µF"), btn, "GND",
           _f(tau * 1000.0, 2, "ms")),
        "R_BTN an +3V3/BTN, C_BTN an BTN/GND, 0,5-20 ms",
        "R_BTN zieht den offenen Taster auf High, C_BTN entprellt; "
        "Zeitkonstante lang genug zum Entprellen, kurz genug zum Wecken")


def check_btn_wake():
    """Der Taster-Pin muss ein LP-GPIO ohne Strapping-Funktion sein."""
    btn = _btn_net()
    pin_raw = None
    for comp, pin in circuit.load_netlist()[btn]:
        if comp == "U1":
            pin_raw = pin
            break
    if pin_raw is None:
        raise circuit.CircuitError("kein U1-Pin auf dem Tasternetz %s" % btn)
    m_io = re.search(r"IO([0-9]+)", pin_raw)
    if m_io is None:
        raise circuit.CircuitError("kein IO-Name am U1-Pin %r" % pin_raw)
    io_num = int(m_io.group(1))
    io_name = "IO%d" % io_num
    m_pin = re.match(r"\s*([0-9]+)", pin_raw)
    pin_no = m_pin.group(1) if m_pin else "?"
    lp = LP_GPIO_MIN <= io_num <= LP_GPIO_MAX
    strapping = io_num in STRAPPING_GPIOS
    ok = lp and not strapping
    if ok:
        grund = ("Espressif ESP32-C6: LP-GPIOs IO0-IO7 wecken per EXT1; "
                 "%s ist kein Strapping-Pin" % io_name)
    else:
        teile = []
        if not lp:
            teile.append("%s liegt ausserhalb der LP-GPIOs IO0-IO7" % io_name)
        if strapping:
            teile.append("%s ist Strapping-Pin" % io_name)
        grund = "; ".join(teile)
    return CheckResult(
        "Taster-Weckquelle", ok,
        "U1 Pin %s = %s" % (pin_no, io_name),
        "LP-GPIO (IO0-IO7) und kein Strapping-Pin",
        grund)


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
        check_tank_led,
        check_led_headroom,
        check_btn_pullup,
        check_btn_wake,
        check_en_rc,
        check_netzstruktur,
    ]
    return [fn() for fn in checks]


if __name__ == "__main__":
    for result in run_all():
        print("%-28s %s  %s" % (result.name, "OK" if result.bestanden else "FEHLER",
                                 result.ist))
