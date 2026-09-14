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
# Achtung: "Strapping" != "boot-kritisch". IO4/IO5 sind nur SDIO-Strap
# (Flankenneigung) und beeinflussen den Boot NICHT.
STRAPPING_GPIOS = frozenset({4, 5, 8, 9, 15})

# Boot-kritische Strapping-Pins des ESP32-C6. Nur diese duerfen NICHT fuer
# Sensor oder Pumpe verwendet werden: GPIO8/GPIO9 bestimmen den Boot-Modus
# (nur 8=0 UND 9=0 ist ungueltig), GPIO15 waehlt die JTAG-Quelle (mit den
# Default-eFuses wirkungslos).
BOOT_CRITICAL_STRAPPING_GPIOS = frozenset({8, 9, 15})

# Modulpin der ESP32-C6-MINI-1 fuer die Erweiterungspins (aus dem Modulsymbol
# bzw. dem Espressif-Datenblatt, Pin-Tabelle).
EXT_IO_PIN = {
    0: 12,   # ADC1_CH0, J2 Feuchtesensor
    4: 9,    # ADC1_CH4, J7 Lichtsensor
    5: 10,   # ADC1_CH5, J9 Reserve-Analog
    8: 22,   # Strapping (Boot-Modus), nur Pull-up
    9: 23,   # Strapping (Boot-Modus), Boot-Taster
    15: 20,  # Strapping (JTAG-Quelle); J10, Serien-R schuetzt den Pin
    18: 24,  # I2C SDA
    19: 25,  # I2C SCL
    20: 26,  # Load-Switch-Eingang (WPU beim Reset)
    21: 27,  # J13 Reserve-Digital
    22: 28,  # J14 Reserve-Digital
    23: 29,  # J15 Reserve-Digital
    16: 31,  # TXD0
    17: 30,  # RXD0
}

# 3-polige Sensor-/Reserve-Stecker mit der Ordnung GND-VCC-SIG:
# Stecker -> (Signalnetz an Pin 3, erwartetes Versorgungsnetz an Pin 2).
DREIPOL_STECKER = {
    "J2": ("SENSOR_RAW", "SENSOR_PWR"),
    "J7": ("LIGHT_RAW", "SENSOR_PWR"),
    "J9": ("SPARE_AIN_RAW", "VCC_EXT"),
    "J10": ("SPARE_IO15_RAW", "VCC_EXT"),
    "J11": ("SPARE_IO16", "VCC_EXT"),
    "J12": ("SPARE_IO17", "VCC_EXT"),
    "J13": ("SPARE_IO21_RAW", "VCC_EXT"),
    "J14": ("SPARE_IO22_RAW", "VCC_EXT"),
    "J15": ("SPARE_IO23_RAW", "VCC_EXT"),
}

# 4-poliger I2C-Stecker J8: GND-VCC-SDA-SCL (VCC innen, wie Qwiic/STEMMA).
I2C_STECKER = "J8"

# Signaleingang am Stecker -> (Stecker, Signalpin, Serien-R, Steckernetz,
# MCU-Netz, erwartete IO-Nummer). Der Serienwiderstand muss zwischen Stecker
# und MCU liegen.
SERIEN_EINGAENGE = (
    ("J2", "3", "R6", "SENSOR_RAW", "SENSOR_AOUT", 0),
    ("J7", "3", "R_LIGHT_S", "LIGHT_RAW", "LIGHT_AOUT", 4),
    ("J9", "3", "R_SPARE_AIN", "SPARE_AIN_RAW", "SPARE_AIN", 5),
    ("J10", "3", "R_SPARE_IO15", "SPARE_IO15_RAW", "SPARE_IO15", 15),
    ("J11", "3", "R_SPARE_IO16", "SPARE_IO16", "UART_TX", 16),
    ("J12", "3", "R_SPARE_IO17", "SPARE_IO17", "UART_RX", 17),
    ("J13", "3", "R_SPARE_IO21", "SPARE_IO21_RAW", "SPARE_IO21", 21),
    ("J14", "3", "R_SPARE_IO22", "SPARE_IO22_RAW", "SPARE_IO22", 22),
    ("J15", "3", "R_SPARE_IO23", "SPARE_IO23_RAW", "SPARE_IO23", 23),
    ("J8", "3", "R_SDA_S", "SDA", "SDA_MCU", 18),
    ("J8", "4", "R_SCL_S", "SCL", "SCL_MCU", 19),
)

# IO20 soll beim Reset einen internen Weak-Pull-up haben (Espressif
# ESP32-C6-Datenblatt, Abschnitt Strapping/Reset). Der Wert steht als Konstante
# hier, damit die Aussage an einer Stelle dokumentiert und pruefbar ist.
IO20_WPU_AT_RESET = True

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


def _pins_of(designator):
    """Pin -> Netz fuer alle Pins eines Bauteils aus der Netzliste.

    Pin-Nummern werden auf die fuehrende Ziffer reduziert ("3 Drain" -> "3",
    "24 IO18" -> "24"), damit Stecker- und Halbleiterpins vergleichbar sind.
    """
    result = {}
    for net, nodes in circuit.load_netlist().items():
        for comp, pin in nodes:
            if comp != designator:
                continue
            m = re.match(r"\s*([0-9]+)\b", pin)
            key = m.group(1) if m else pin.strip()
            result.setdefault(key, net)
    return result


def _u1_pin_on_net(net):
    """Modulpin-Nummer des U1-Pins auf einem Netz, sonst Fehler.

    Robuster als :func:`_u1_io_on_net`, weil auch TXD0/RXD0 (IO16/IO17) keine
    IO-Nummer im Pin-Namen tragen.
    """
    for comp, pin in circuit.load_netlist().get(net, []):
        if comp == "U1":
            m = re.match(r"\s*([0-9]+)\b", pin.strip())
            if m:
                return int(m.group(1)), pin.strip()
    raise circuit.CircuitError("kein U1-Pin auf Netz %s" % net)


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


def _u1_io_on_net(net):
    """(IO-Nummer, roher Pinname) des U1-Pins auf einem Netz, sonst Fehler."""
    for comp, pin in circuit.load_netlist().get(net, []):
        if comp == "U1":
            m = re.search(r"IO([0-9]+)", pin)
            if m:
                return int(m.group(1)), pin.strip()
    raise circuit.CircuitError("kein U1-IO-Pin auf Netz %s" % net)


def _light_dark_counts(r_load):
    """ADC-Counts im Dunkeln aus ICEO_max am Lastwiderstand."""
    v_dark = circuit.LIGHT_SENS_DARK_UA * 1e-6 * r_load
    return v_dark / (circuit.ADC_VREF_MV_ATTEN12 / 1000.0) * circuit.ADC_COUNTS_12BIT


def _light_counts_at(lux, r_load):
    """ADC-Counts bei einer Beleuchtungsstaerke, gesaettigt auf den Vollausschlag."""
    vref = circuit.ADC_VREF_MV_ATTEN12 / 1000.0
    i = circuit.LIGHT_SENS_UA_REF * 1e-6 * (lux / circuit.LIGHT_SENS_LUX_REF)
    return min(i * r_load, vref) / vref * circuit.ADC_COUNTS_12BIT


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
    """Ruhestrom und Monatsverbrauch im Deep-Sleep; Lichtsensor geschaltet."""
    sys = circuit.load_system()
    # Der Lichtsensor haengt an SENSOR_PWR (IO3, im Deep-Sleep aus) und traegt
    # deshalb nichts zum Ruhestrom bei. An +3V3 wuerde er das Budget sprengen.
    # Pinordnung seit 13.09.2026: GND-VCC-SIG, VCC liegt auf Pin 2.
    j7_net = circuit.net_of("J7", "2")
    switched = j7_net == "SENSOR_PWR"
    light_ua = 0.0  # nur waehrend der Messung; SENSOR_PWR ist im Sleep aus
    total_ua = (sys["module_sleep_ua"] + sys["ldo_quiescent_ua"]
                + sys["max809_quiescent_ua"] + sys["divider_current_ua"]
                + light_ua)
    monthly_mah = total_ua / 1000.0 * 24.0 * 30.0
    ok = (total_ua <= 100.0 and monthly_mah <= 0.05 * sys["battery_mah"]
          and switched)
    return CheckResult(
        "Standby-Budget", ok,
        "%s, %s/Monat (%s der Zelle); Lichtsensor an %s %s (+%s)"
        % (_f(total_ua, 1, "µA"), _f(monthly_mah, 1, "mAh"),
           _f(monthly_mah / sys["battery_mah"] * 100.0, 2, "%"),
           j7_net, "geschaltet" if switched else "DAUERHAFT -> FEHLER",
           _f(light_ua, 1, "µA")),
        "<= 100 µA und <= 5 %/Monat von 1500 mAh, Sensor an SENSOR_PWR",
        "Summe Modul 7 µA + LDO 40 µA + MAX809 12 µA + Teiler 10,5 µA "
        "(schaltplan_v1.md 6.3); Lichtsensor an geschaltetem SENSOR_PWR "
        "=> 0 µA im Deep-Sleep")


def check_adc_filter():
    """RC-Zeitkonstanten der ADC-Kanaele (Feuchte, VBAT, Reserve-Analog)."""
    r6 = circuit.parse_ohm(circuit.part("R6")["value"])
    c9 = circuit.parse_farad(circuit.part("C9")["value"])
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    c10 = circuit.parse_farad(circuit.part("C10")["value"])
    r_spare = circuit.parse_ohm(circuit.part("R_SPARE_AIN")["value"])
    c_spare = circuit.parse_farad(circuit.part("C_SPARE")["value"])
    t_sensor = r6 * c9
    r_par = 1.0 / (1.0 / r3a + 1.0 / r3b)
    t_vbat = r_par * c10
    t_spare = r_spare * c_spare
    ok = t_sensor <= 5e-3 and t_vbat <= 50e-3 and t_spare <= 5e-3
    return CheckResult(
        "ADC-Filter", ok,
        "R6·C9 %s, (R3a||R3b)·C10 %s, R_SPARE_AIN·C_SPARE %s"
        % (_f(t_sensor * 1000.0, 2, "ms"), _f(t_vbat * 1000.0, 1, "ms"),
           _f(t_spare * 1000.0, 2, "ms")),
        "R6·C9 <= 5 ms, (R3a||R3b)·C10 <= 50 ms und R_SPARE_AIN·C_SPARE <= 5 ms",
        "Espressif-ADC: 0,1 µF Filter; Zeitkonstante begrenzt das Einschwingen "
        "(Reserve-Analog J9 im Muster von SENSOR_AOUT)")


def check_light_adc_filter():
    """RC-Zeitkonstante des Licht-ADC-Kanals (R_LIGHT_S + C_LIGHT)."""
    r = circuit.parse_ohm(circuit.part("R_LIGHT_S")["value"])
    c = circuit.parse_farad(circuit.part("C_LIGHT")["value"])
    tau = r * c
    return CheckResult(
        "Licht-ADC-Filter", tau <= 5e-3,
        "R_LIGHT_S·C_LIGHT %s (R %s, C %s)"
        % (_f(tau * 1000.0, 3, "ms"), _f(r / 1000.0, 1, "kΩ"),
           _f(c * 1e9, 0, "nF")),
        "R_LIGHT_S·C_LIGHT <= 5 ms",
        "Espressif-ADC: 0,1 µF Filter; die Zeitkonstante begrenzt das "
        "Einschwingen (gleiche Grenze wie R6·C9)")


def check_light_contrast():
    """Dunkel/Hell-Kontrast des ALS-PT19 am ADC (ADC_ATTEN_DB_12)."""
    r = circuit.parse_ohm(circuit.part("R_LIGHT")["value"])
    dark = _light_dark_counts(r)
    bright = _light_counts_at(circuit.LIGHT_GROW_LUX, r)
    vref = circuit.ADC_VREF_MV_ATTEN12 / 1000.0
    lux_full = (vref / r) / (circuit.LIGHT_SENS_UA_REF * 1e-6) * circuit.LIGHT_SENS_LUX_REF
    span = bright - dark
    ok = (dark <= circuit.LIGHT_DARK_COUNTS
          and bright >= circuit.LIGHT_BRIGHT_COUNTS
          and span > 2.0 * circuit.LIGHT_HYSTERESE_COUNTS)
    return CheckResult(
        "Licht-Kontrast", ok,
        "dunkel %s Counts, bei %s lx %s Counts (Spanne %s, Saettigung ab %s lx)"
        % (_f(dark, 1, ""), _f(circuit.LIGHT_GROW_LUX, 0, ""),
           _f(bright, 0, ""), _f(span, 0, ""), _f(lux_full, 0, "")),
        "dunkel <= %s, hell >= %s, Spanne > 2 x %s Counts"
        % (_f(circuit.LIGHT_DARK_COUNTS, 0, ""),
           _f(circuit.LIGHT_BRIGHT_COUNTS, 0, ""),
           _f(circuit.LIGHT_HYSTERESE_COUNTS, 0, "")),
        "ALS-PT19-Datenblatt: ICEO <= 0,1 µA (dunkel), 15 µA typ @ 100 lx; "
        "R_LIGHT 10 kΩ; ADC_ATTEN_DB_12 (0-3300 mV, 12 Bit)")


def check_light_open_connector():
    """Offener Stecker J7 darf den ADC nicht floaten lassen (R_LIGHT nach GND)."""
    r_light = _nets_of("R_LIGHT")
    r_series = _nets_of("R_LIGHT_S")
    c_light = _nets_of("C_LIGHT")
    j7 = _nets_of("J7")
    r_ok = set(r_light) == {"LIGHT_RAW", "GND"} and r_light.get("GND") == "2"
    series_ok = (set(r_series) == {"LIGHT_RAW", "LIGHT_AOUT"}
                 and r_series.get("LIGHT_RAW") == "1"
                 and r_series.get("LIGHT_AOUT") == "2")
    c_ok = set(c_light) == {"LIGHT_AOUT", "GND"}
    # Pinordnung seit 13.09.2026: GND-VCC-SIG, das Signal liegt auf Pin 3.
    j7_ok = j7.get("LIGHT_RAW") == "3"
    io, _pin = _u1_io_on_net("LIGHT_AOUT")
    adc_ok = io == 4
    ok = r_ok and series_ok and c_ok and j7_ok and adc_ok
    r = circuit.parse_ohm(circuit.part("R_LIGHT")["value"])
    rs = circuit.parse_ohm(circuit.part("R_LIGHT_S")["value"])
    return CheckResult(
        "Licht-Stecker offen", ok,
        "R_LIGHT LIGHT_RAW/GND %s, R_LIGHT_S in Reihe %s, C_LIGHT "
        "LIGHT_AOUT/GND %s, J7-3 auf LIGHT_RAW %s, ADC IO%d %s (Pfad nach "
        "GND ueber %s)"
        % ("OK" if r_ok else "FEHLER", "OK" if series_ok else "FEHLER",
           "OK" if c_ok else "FEHLER", "OK" if j7_ok else "FEHLER",
           io, "OK" if adc_ok else "FEHLER",
           _f((r + rs) / 1000.0, 0, "kΩ")),
        "R_LIGHT LIGHT_RAW->GND, R_LIGHT_S LIGHT_RAW->LIGHT_AOUT, "
        "C_LIGHT LIGHT_AOUT->GND, J7 Pin 3 auf LIGHT_RAW, ADC = IO4",
        "offener Stecker: R_LIGHT zieht LIGHT_RAW auf 0 V, ueber R_LIGHT_S "
        "liegt der ADC auf 0 V -> kein schwebender Eingang")


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


def check_pin_disziplin():
    """PUMP_EN auf IO2, Lichtsensor auf IO4, kein boot-kritischer Strap-Pin."""
    light_io, light_pin = _u1_io_on_net("LIGHT_AOUT")
    pump_io, pump_pin = _u1_io_on_net("PUMP_EN")

    # Doppelbelegung: dieselbe U1-Pin-Nummer auf zwei Netzen. Aggregat-Zeilen
    # (GND-Bereiche, VDD33, EPAD) tragen keine einzelne Pin-Nummer.
    pin_nets = defaultdict(set)
    for net, nodes in circuit.load_netlist().items():
        for comp, pin in nodes:
            if comp != "U1":
                continue
            raw = pin.strip()
            if "/" in raw or "alle" in raw or "EPAD" in raw:
                continue
            m = re.match(r"([0-9]+)\b", raw)
            if m:
                pin_nets[int(m.group(1))].add(net)
    dupes = sorted(p for p, ns in pin_nets.items() if len(ns) > 1)

    boot = BOOT_CRITICAL_STRAPPING_GPIOS
    light_boot = light_io in boot
    pump_boot = pump_io in boot
    expected = light_io == 4 and pump_io == 2
    ok = not light_boot and not pump_boot and not dupes and expected
    return CheckResult(
        "Pin-Disziplin", ok,
        "Licht %s, Pumpe %s, boot-kritisch Licht %s/Pumpe %s, "
        "Doppelbelegung %s"
        % (light_pin, pump_pin,
           "JA" if light_boot else "nein", "JA" if pump_boot else "nein",
           ", ".join("Pin %d" % p for p in dupes) or "keine"),
        "Licht = IO4 (Pin 9, ADC1_CH4), Pumpe = IO2 (Pin 5), kein "
        "boot-kritischer Strapping-Pin (GPIO8/9/15), kein Pin doppelt",
        "ESP32-C6: boot-kritisch nur GPIO8/GPIO9 (Boot-Modus) und GPIO15 "
        "(JTAG-Quelle); IO4/IO5 sind nur SDIO-Strap und als ADC nutzbar")


def check_stecker_pinordnung():
    """Pinordnung GND-VCC-SIG aller 3-pol. Stecker, J8 = GND-VCC-SDA-SCL."""
    teile = []
    ok = True
    for ref in sorted(DREIPOL_STECKER):
        sig_net, vcc_net = DREIPOL_STECKER[ref]
        n = _pins_of(ref)
        p1, p2, p3 = n.get("1"), n.get("2"), n.get("3")
        good = p1 == "GND" and p2 == vcc_net and p3 == sig_net
        ok = ok and good
        teile.append("%s: 1=%s 2=%s 3=%s %s"
                     % (ref, p1, p2, p3, "OK" if good else "FEHLER"))
    j8 = _pins_of(I2C_STECKER)
    j8_ok = (j8.get("1") == "GND" and j8.get("2") == "VCC_EXT"
             and j8.get("3") == "SDA" and j8.get("4") == "SCL")
    ok = ok and j8_ok
    teile.append("J8: 1=%s 2=%s 3=%s 4=%s %s"
                 % (j8.get("1"), j8.get("2"), j8.get("3"), j8.get("4"),
                    "OK" if j8_ok else "FEHLER"))
    return CheckResult(
        "Stecker-Pinordnung", ok, "; ".join(teile),
        "Pin 1 = GND, Pin 2 = Versorgung (SENSOR_PWR/VCC_EXT), Pin 3 = Signal "
        "(J2/J7/J9-J15); J8 = GND-VCC_EXT-SDA-SCL",
        "3-poliger Stecker: nur der mittlere Pin ist gegen Umdrehen invariant. "
        "VCC auf Pin 2 kann nie 3,3 V auf einen MCU-Pin legen und nie die "
        "Sensorversorgung ueber unsere Masse kurzschliessen. Fehlerfall bei "
        "verkehrtem Stecker: GND/SIG tauschen, der 1-kOhm-Serienwiderstand "
        "begrenzt den Strom (ca. 3 mA, pin-sicher). J8 folgt der Qwiic-/STEMMA-"
        "Ordnung mit VCC auf Pin 2")


def check_erweiterung_serienwiderstand():
    """Jeder Signaleingang am Stecker hat einen 1-kOhm-Serienwiderstand."""
    teile = []
    ok = True
    for ref, sig_pin, r_des, conn_net, mcu_net, io_soll in SERIEN_EINGAENGE:
        r_nets = _nets_of(r_des)
        series_ok = set(r_nets) == {conn_net, mcu_net}
        try:
            r_val = circuit.parse_ohm(circuit.part(r_des)["value"])
        except circuit.CircuitError:
            r_val = None
        val_ok = r_val is not None and abs(r_val - 1000.0) < 1.0
        conn_ok = _pins_of(ref).get(sig_pin) == conn_net
        pin_soll = EXT_IO_PIN[io_soll]
        try:
            pin_ist, _ = _u1_pin_on_net(mcu_net)
        except circuit.CircuitError:
            pin_ist = None
        io_ok = pin_ist == pin_soll
        good = series_ok and val_ok and conn_ok and io_ok
        ok = ok and good
        teile.append("%s.%s->%s(%s), %s, %s, %s"
                     % (ref, sig_pin, r_des, mcu_net,
                        "Reihe" if series_ok else "NICHT-Reihe",
                        "1k" if val_ok else "Wert?",
                        "Pin %d (IO%d)" % (pin_ist, io_soll) if io_ok
                        else "IO%d?" % io_soll))
    return CheckResult(
        "Serienwiderstand Signale", ok, "; ".join(teile),
        "je Signaleingang ein 1-kOhm-Widerstand zwischen Steckerpin und MCU-Pin",
        "Steckerkabel koennen Fehlerstroeme in die Pins treiben; der Serien-R "
        "begrenzt sie. Gilt fuer Sensor/Licht, I2C (SDA/SCL) und alle "
        "Reserve-Eingaenge (R6, R_LIGHT_S, R_SDA_S, R_SCL_S, R_SPARE_AIN, "
        "R_SPARE_IO15/16/17/21/22/23)")


def check_load_switch_failsafe():
    """VCC_EXT haengt an Q2 (P-Kanal); Gate-Pull-up nach +3V3 => aus beim Reset."""
    q2 = _pins_of("Q2")
    r_gate = _nets_of("R_GATE")
    src_ok = q2.get("2") == "+3V3"
    drain_ok = q2.get("3") == "VCC_EXT"
    gate_ok = q2.get("1") == "EXT_EN"
    r_ok = set(r_gate) == {"+3V3", "EXT_EN"} and r_gate.get("+3V3") == "1"
    try:
        r_val = circuit.parse_ohm(circuit.part("R_GATE")["value"])
    except circuit.CircuitError:
        r_val = None
    val_ok = r_val is not None and abs(r_val - 47000.0) < 1.0
    io = None
    try:
        io, _ = _u1_io_on_net("EXT_EN")
    except circuit.CircuitError:
        io = None
    io_ok = io == 20
    # Fail-safe: der Pull-up haelt das Gate ohne aktiven GPIO auf dem
    # Quellpotential (+3V3) -> VGS = 0 -> Q2 sperrt -> VCC_EXT aus.
    failsafe = src_ok and gate_ok and r_ok and val_ok and IO20_WPU_AT_RESET
    ok = src_ok and drain_ok and gate_ok and r_ok and val_ok and io_ok and failsafe
    return CheckResult(
        "Load-Switch-Fail-safe", ok,
        "Q2 S->%s D->%s G->%s, R_GATE an +3V3 %s, IO%d %s, IO20-WPU %s"
        % (q2.get("2"), q2.get("3"), q2.get("1"),
           "OK" if r_ok else "FEHLER", io if io is not None else -1,
           "OK" if io_ok else "FEHLER",
           "ja" if IO20_WPU_AT_RESET else "nein"),
        "Source +3V3, Drain VCC_EXT, Gate ueber 47 kOhm auf +3V3, IO20 zieht "
        "das Gate nach unten, IO20 hat beim Reset WPU",
        "Load-Switch aus = Fail-safe. Ohne GPIO-Treiber (Reset, Hochohmigkeit, "
        "Deep-Sleep) liegt das Gate ueber 47 kOhm auf dem Quellpotential "
        "(VGS = 0) und Q2 sperrt. IO20 hat beim Reset einen internen "
        "Weak-Pull-up (Espressif ESP32-C6-Datenblatt), der das Gate zusaetzlich "
        "hoch haelt -> VCC_EXT ist beim Start aus")


def check_erweiterung_pins():
    """Kein U1-Pin doppelt; Erweiterungspins wie geplant; GPIO8/9 unveraendert."""
    pin_net = defaultdict(set)
    for net, nodes in circuit.load_netlist().items():
        for comp, pin in nodes:
            if comp != "U1":
                continue
            raw = pin.strip()
            if "/" in raw or "alle" in raw or "EPAD" in raw:
                continue
            m = re.match(r"([0-9]+)\b", raw)
            if m:
                pin_net[int(m.group(1))].add(net)
    dupes = sorted(p for p, ns in pin_net.items() if len(ns) > 1)

    expected = {5: "SPARE_AIN", 15: "SPARE_IO15", 16: "UART_TX", 17: "UART_RX",
                18: "SDA_MCU", 19: "SCL_MCU", 20: "EXT_EN", 21: "SPARE_IO21",
                22: "SPARE_IO22", 23: "SPARE_IO23"}
    zuord_ok = all(pin_net.get(EXT_IO_PIN[io], set()) == {net}
                   for io, net in expected.items())
    # GPIO8/GPIO9 bleiben auf ihren bestehenden Strapping-Netzen.
    strap_ok = (pin_net.get(22) == {"GPIO8_STRAP"} and pin_net.get(23) == {"BOOT"})
    ok = not dupes and zuord_ok and strap_ok
    return CheckResult(
        "Erweiterungs-Pins", ok,
        "Doppelbelegung %s; Zuordnung %s; GPIO8/9 %s"
        % (", ".join("Pin %d" % p for p in dupes) or "keine",
           "OK" if zuord_ok else "FEHLER", "OK" if strap_ok else "FEHLER"),
        "kein U1-Pin doppelt, Erweiterungspins wie geplant, GPIO8/GPIO9 "
        "unveraendert auf ihren Strapping-Netzen",
        "Mengenpruefung der Netzliste gegen Pin-Doppelbelegung. IO15 waehlt nur "
        "die JTAG-Quelle (Default-eFuses = wirkungslos) und ist ueber einen "
        "1-kOhm-Serienwiderstand an J10 gefuehrt; IO16/IO17 bleiben UART0 und "
        "sind ebenfalls nur ueber Serienwiderstaende erreichbar")


def check_i2c_pullups():
    """I2C-Pull-ups 10k an VCC_EXT (nicht +3V3); VCC_EXT ist geschaltet."""
    sda = _nets_of("R_SDA_PU")
    scl = _nets_of("R_SCL_PU")
    r_sda = circuit.parse_ohm(circuit.part("R_SDA_PU")["value"])
    r_scl = circuit.parse_ohm(circuit.part("R_SCL_PU")["value"])
    sda_ok = sda.get("SDA") == "1" and sda.get("VCC_EXT") == "2"
    scl_ok = scl.get("SCL") == "1" and scl.get("VCC_EXT") == "2"
    val_ok = abs(r_sda - 10000.0) < 1.0 and abs(r_scl - 10000.0) < 1.0
    q2 = _pins_of("Q2")
    switched = q2.get("3") == "VCC_EXT" and q2.get("2") == "+3V3"
    auf_rail = "+3V3" in (set(sda.values()) | set(scl.values()))
    ok = sda_ok and scl_ok and val_ok and switched and not auf_rail
    return CheckResult(
        "I2C-Pull-ups", ok,
        "R_SDA_PU %s an VCC_EXT (Pin %s), R_SCL_PU %s an VCC_EXT (Pin %s), "
        "VCC_EXT geschaltet %s"
        % (_f(r_sda / 1000.0, 1, "kΩ"), sda.get("VCC_EXT"),
           _f(r_scl / 1000.0, 1, "kΩ"), scl.get("VCC_EXT"),
           "OK" if switched else "FEHLER"),
        "beide 10 kOhm, Pull-up-Seite VCC_EXT (nicht +3V3), VCC_EXT geschaltet",
        "Im ausgeschalteten Zustand zieht der Bus keinen Strom, weil die "
        "Pull-ups am geschalteten VCC_EXT haengen. 10 kOhm sind fuer kurze "
        "Kabel (wenige cm bis ca. 30 cm) und die ueblichen 100-kHz/400-kHz-"
        "I2C-Module plausibel")


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
        check_light_adc_filter,
        check_light_contrast,
        check_light_open_connector,
        check_led_stroeme,
        check_tank_led,
        check_led_headroom,
        check_btn_pullup,
        check_btn_wake,
        check_pin_disziplin,
        check_stecker_pinordnung,
        check_erweiterung_serienwiderstand,
        check_load_switch_failsafe,
        check_erweiterung_pins,
        check_i2c_pullups,
        check_en_rc,
        check_netzstruktur,
    ]
    return [fn() for fn in checks]


if __name__ == "__main__":
    for result in run_all():
        print("%-28s %s  %s" % (result.name, "OK" if result.bestanden else "FEHLER",
                                 result.ist))
