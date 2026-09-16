"""Design-Regelpruefungen fuer den Schaltplan V1 (2S-Umbau, 16.09.2026).

Jede Pruefung liest die echten Dateien ueber :mod:`design.circuit` und liefert
ein :class:`CheckResult` mit (name, bestanden, ist_wert, soll_kriterium,
begruendung).  Hart verdrahtet sind nur Datenblatt-Grenzwerte; die Quelle steht
jeweils in der Begruendung.  Systemgroessen kommen aus ``circuit.SYSTEM`` und
werden von :func:`check_system_quellen` gegen die Dokumente belegt.
"""
from __future__ import annotations

import re
from collections import defaultdict, namedtuple

from . import circuit

CheckResult = namedtuple("CheckResult", "name bestanden ist soll begruendung")


class PruefFehler(Exception):
    """Werkzeugfehler: Pruefmodell und Netzliste passen nicht zusammen.

    Anders als :class:`circuit.CircuitError` ist das **kein Design-Fehler**:
    Eine Pruefung darf gar nicht erst laufen, weil sie einen Pin-/Bauteilnamen
    verwendet, den die Netzliste nicht kennt.  Der Bericht weist das getrennt
    als "Werkzeugfehler" aus (eigener Exit-Code) und zaehlt es nicht als
    "Pruefung fehlgeschlagen" -- sonst haelt man einen veralteten Pruefstand
    faelschlich fuer einen bestandenen oder fehlgeschlagenen Test.
    """

# ===========================================================================
# Datenblattgrenzen (jede mit Quelle)
# ===========================================================================

# --- IP2326 (Injoinic, LCSC C2832094), Datenblatt V1.11 --------------------
IP2326_ICHG_K = 90000.0          # ICHG = 90000/R_ISET[Ohm], §"充电电流设置" S. 11
IP2326_ICHG_MAX_A = 1.5          # §7 Elektrische Eigenschaften S. 4
IP2326_VSET_OPEN_V = 8.4         # VSET offen ⇒ 8,4 V (8,3-8,5), §7/S. 4
IP2326_VSET_TOL_V = 0.1          # Toleranz 8,3-8,5 V
IP2326_EFF = 0.94                # Wirkungsgrad 94 % (5 V→8 V/1 A), §1 S. 1
IP2326_VIN_MIN_V = 4.5           # Eingang 4,5-9,5 V, S. 3
IP2326_VIN_MAX_V = 9.5
IP2326_CELL_MAX_V = 4.2          # Li-Ion-Ladeschluss 4,2 V/Zelle
IP2326_CHARGE_PHASES = (         # §9, S. 9: Phasen-Stroeme
    (3.7, 0.050),                # < 3,7 V -> 50 mA
    (6.0, 0.100),                # 3,7-6 V -> 100 mA
)
IP2326_8V8_V = 8.8               # Variante IP2326_8V8: 8,8 V Ladeschluss
                                 # (fuer Li-Ion unzulaessig, schaltplan §3.1)

# --- HY2120-CB (HYCON, LCSC C116509), 2-Zellen-Schutz-IC -------------------
# Schwellen stehen im HY2120-Datenblatt und sind in schaltplan_v1.md §3.1/§6.3
# belegt; die Pruefungen check_schutz_schwellen / check_schutz_ueberstrom lesen
# sie zusaetzlich woertlich aus dem Dokument (keine Tautologie).
HY2120_OC_DELAY_MS = 10.0        # interne Verzoegerung Ueberstrom, §3.1

# --- PSMN4R2-30MLDX (Nexperia, LCSC C179452), Schalterpaar -----------------
PSMN4R2_RDSON_MAX_OHM = 5.7e-3   # 5,7 mOhm max bei V_GS = 4,5 V (schaltplan
                                 # §3.1: PSMN4R2-30MLDX, LFPAK33-8), 4,3 mOhm
                                 # bei 10 V. Paar = 2 x 5,7 mOhm = 11,4 mOhm.
SCHUTZ_DAUER_DROP_MAX_V = 0.050  # Auslegungsgrenze: Abfall des Paares bei
                                 # Dauerlast <= 50 mV (Review-Vorgabe).
BUCK_INRUSH_EFF = 0.90           # Buck-Wirkungsgrad beim Anlauf (bom_entscheidung.md:
                                 # "Buck aus 2S (eta 0,90)")

# --- SY8113B (Silergy, C78989), Datenblatt AN_SY8113B ----------------------
BUCK5_VIN_MIN_V, BUCK5_VIN_MAX_V = 4.5, 18.0
BUCK5_IOUT_MAX_A = 3.0          # 3 A Ausgang, S. 1
BUCK5_FSW_HZ = 500e3            # 500 kHz
BUCK5_EN_HIGH_V = 1.5           # EN High-Schwelle, "Do not float"
BUCK5_EN_LOW_V = 0.4
BUCK5_UVLO_V = 4.5              # Input-UVLO
BUCK5_VALLEY_MIN_A, BUCK5_VALLEY_MAX_A = 3.0, 4.25   # Stromgrenzen (EC)
BUCK5_PEAK_A = 6.0              # Top-FET-Peak
L_BUCK_ISAT_A = 4.0             # PRS6045-Datenblatt: Isat 4,0 A (L_BUCK5/3)

# --- AP63203 (Diodes, C780769), Datenblatt DS41326 -------------------------
BUCK3_VIN_MIN_V, BUCK3_VIN_MAX_V = 3.8, 32.0
BUCK3_IOUT_MAX_A = 2.0          # 2 A
BUCK3_FSW_HZ = 1.1e6            # 1,1 MHz
MODULE_VDD33_MIN_V = 3.0        # Espressif ESP32-C6-MINI-1: V_DD33 3,0-3,6 V
MODULE_VDD33_MAX_V = 3.6

# --- TPS3839G33 (TI, C485802), Datenblatt SBVS193D -------------------------
TPS3839_VIT_MIN_V, TPS3839_VIT_MAX_V = 3.003, 3.126   # negativ, S. 7
TPS3839_VIT_NOM_V = 3.08        # im Projekt verwendeter Wert
TPS3839_HYST_V = 0.031          # Hysterese 31 mV
TPS3839_IQ_TYP_UA, TPS3839_IQ_MAX_UA = 0.15, 0.5      # Iq 150 nA typ / 500 nA max
TPS3839_VDD_MIN_V, TPS3839_VDD_MAX_V = 0.9, 6.5       # V_DD-Bereich
TPS3839_VOL_V = 0.4             # V_OL <= 0,4 V bei I_OL = 2 mA (2,8-6,5 V)
TPS3839_IOL_A = 2e-3            # Ausgangsstrom 2 mA
TPS3839_VOH_DROP_V = 0.4        # V_OH >= V_DD - 0,4 V
TPS3839_RESET_DELAY_MS = 200.0  # Reset-Delay 200 ms
WATCHDOG_TRIP_MIN_V, WATCHDOG_TRIP_MAX_V = 6.0, 6.6   # Ziel: 2 x 3,0 .. 2 x 3,3 V

# --- 1N5819WS (C191023) -----------------------------------------------------
DIODE_VF_SCHOTTKY_V = 0.3       # Flussspannung bei kleinem Strom (Auslegung)

# --- ADC (Espressif ESP32-C6) ----------------------------------------------
ADC_MIN_USEFUL_MV = 1000.0      # Aufloesungsreserve am unteren Ende

# ===========================================================================
# Annahmen des Modells (keine Datenblattwerte), zentral in circuit.ASSUMPTIONS
# ===========================================================================
EN_INPUT_LEAK_UA = circuit.ASSUMPTIONS.get("en_input_leak_ua", 0.0)

# Datenblatt-Fakten zum ESP32-C6 (als Konstanten mit Quelle hart verdrahtet).
# Espressif ESP32-C6-Datenblatt: LP-/RTC-GPIOs sind GPIO0 bis GPIO7.
LP_GPIO_MIN, LP_GPIO_MAX = 0, 7
# Strapping-Pins: GPIO8/GPIO9 (Boot-Modus) und GPIO15 (JTAG-Quelle), dazu
# IO4/IO5 (nur SDIO-Strap, nicht boot-kritisch).
STRAPPING_GPIOS = frozenset({4, 5, 8, 9, 15})
BOOT_CRITICAL_STRAPPING_GPIOS = frozenset({8, 9, 15})

# Modulpin der ESP32-C6-MINI-1 fuer die Erweiterungspins (aus dem Modulsymbol
# bzw. dem Espressif-Datenblatt, Pin-Tabelle).  IO22 ist seit 15.09.2026 keine
# Reserve mehr, sondern PUMP2_EN (Sauerstoffpumpe) -> kein Eintrag.
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
    23: 29,  # J15 Reserve-Digital
    16: 31,  # TXD0
    17: 30,  # RXD0
}

# 3-polige Sensor-/Reserve-Stecker mit der Ordnung GND-VCC-SIG.
# J14 ist seit 15.09.2026 entfernt (IO22 = PUMP2_EN/J16).
DREIPOL_STECKER = {
    "J2": ("SENSOR_RAW", "SENSOR_PWR"),
    "J7": ("LIGHT_RAW", "SENSOR_PWR"),
    "J9": ("SPARE_AIN_RAW", "VCC_EXT"),
    "J10": ("SPARE_IO15_RAW", "VCC_EXT"),
    "J11": ("SPARE_IO16", "VCC_EXT"),
    "J12": ("SPARE_IO17", "VCC_EXT"),
    "J13": ("SPARE_IO21_RAW", "VCC_EXT"),
    "J15": ("SPARE_IO23_RAW", "VCC_EXT"),
}

# 4-poliger I2C-Stecker J8: GND-VCC-SDA-SCL (VCC innen, wie Qwiic/STEMMA).
I2C_STECKER = "J8"

# Signaleingang am Stecker -> (Stecker, Signalpin, Serien-R, Steckernetz,
# MCU-Netz, erwartete IO-Nummer).  J14 entfaellt (15.09.2026).
SERIEN_EINGAENGE = (
    ("J2", "3", "R6", "SENSOR_RAW", "SENSOR_AOUT", 0),
    ("J7", "3", "R_LIGHT_S", "LIGHT_RAW", "LIGHT_AOUT", 4),
    ("J9", "3", "R_SPARE_AIN", "SPARE_AIN_RAW", "SPARE_AIN", 5),
    ("J10", "3", "R_SPARE_IO15", "SPARE_IO15_RAW", "SPARE_IO15", 15),
    ("J11", "3", "R_SPARE_IO16", "SPARE_IO16", "UART_TX", 16),
    ("J12", "3", "R_SPARE_IO17", "SPARE_IO17", "UART_RX", 17),
    ("J13", "3", "R_SPARE_IO21", "SPARE_IO21_RAW", "SPARE_IO21", 21),
    ("J15", "3", "R_SPARE_IO23", "SPARE_IO23_RAW", "SPARE_IO23", 23),
    ("J8", "3", "R_SDA_S", "SDA", "SDA_MCU", 18),
    ("J8", "4", "R_SCL_S", "SCL", "SCL_MCU", 19),
)

# IO20 soll beim Reset einen internen Weak-Pull-up haben (Espressif
# ESP32-C6-Datenblatt, Abschnitt Strapping/Reset).
IO20_WPU_AT_RESET = True

# Typische Flussspannung der 0805-LEDs je LCSC-Code (Datenblattwerte).
LED_VF_BY_LCSC = {
    "C84256": 2.0,    # NATIONSTAR NCD0805R1, rot, 615-630 nm
    "C2297": 2.85,    # KENTO KT-0805G, gruen, 525 nm (InGaN)
}

# Aktive Bauteile auf dem VBAT-Netz mit ihrer Datenblatt-Eingangsspannung
# (V_IN,max).  Fehlt ein Bauteil hier und ist es kein zugelassenes Passiv, ist
# es ein harter Fehler -- genau die ME6211-Lektion (V_IN,max 6,0 V, Review §5
# Befund 4).
VBAT_IC_VIN_MAX = {
    "U_CHG": (IP2326_VIN_MAX_V, "IP2326 S. 3: Eingang 4,5-9,5 V (VOUT erzeugt 8,4 V)"),
    "U_BUCK5": (BUCK5_VIN_MAX_V, "SY8113B S. 1: Eingang 4,5-18 V"),
    "U_BUCK3": (BUCK3_VIN_MAX_V, "AP63203 DS41326: Eingang 3,8-32 V"),
}
# Passive/steckbare VBAT-Teilnehmer (Widerstaende, Kondensatoren, Stecker, TP).
# R_PROT_VDD ist der neue 330-Ohm-VDD-Vorwiderstand des Schutz-IC (U_PROT) nach
# VBAT. Ein 0805-Dickschichtwiderstand hat eine Nenn-Gleichspannungs-
# festigkeit von >= 50 V (typ. 150 V bei den ueblichen 0805-Typen, z. B.
# Yageo RC0805: V_working 150 V) und liegt damit weit ueber den 8,4 V des
# 2S-Packs -- zugelassen (schaltplan §3.3: R_PROT_VDD 330 Ohm, HY2120-Datenblatt
# 100..470 Ohm Typ 330; JLC-Basic C17630).
# F1 sitzt in der Pack-Plus-Leitung (PACK_PLUS -> F1 -> VBAT): Littelfuse
# 0452005.MRL (452-Serie, 2410) ist mit 125 V AC/DC weit ueber den 8,4 V des
# 2S-Packs zugelassen (Datenblatt Littelfuse 452-Serie; LCSC C66503).
VBAT_PASSIV = frozenset({
    "C_CHG_OUT", "J1", "TP4", "C_B5_IN", "C_B5_IN_HF",
    "C_B3_IN", "C_B3_IN_HF", "R3a", "R_SENSE_TOP", "R_PROT_VDD", "F1",
})

# Woertliche Belegstellen der SYSTEM-Zahlen (Datei -> Pfad).
_SYSTEM_FILES = {
    "schaltplan_v1.md": circuit.SCHEMATIC_PATH,
    "bom_entscheidung.md": circuit.BOM_DECISION_PATH,
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
    Nicht-numerische Pins (z. B. "Anode") bleiben als Name erhalten.
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
    """Modulpin-Nummer des U1-Pins auf einem Netz, sonst Fehler."""
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


def _uvlo_trip(sys=None):
    """Ausloesespannung des TPS3839 am 1:2-Teiler (Packspannung)."""
    sys = sys or circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    iq = sys["iq_watchdog_ua"] * 1e-6
    return TPS3839_VIT_NOM_V * (1.0 + r3a / r3b) + iq * r3a


# ===========================================================================
# Neue Pruefungen (2S)
# ===========================================================================

def check_ladestrom_ip2326():
    """IP2326: ICHG = 90000/R_ISET, Grenze 1,5 A und 1 C des Packs."""
    r_iset = circuit.parse_ohm(circuit.part("R_ISET")["value"])
    sys = circuit.load_system()
    i_chg = IP2326_ICHG_K / r_iset
    c_rate = sys["pack_capacity_mah"] / 1000.0
    ok = i_chg <= IP2326_ICHG_MAX_A and i_chg <= c_rate
    return CheckResult(
        "Ladestrom IP2326", ok,
        "%s (R_ISET %s)" % (_f(i_chg, 2, "A"), _f(r_iset / 1000.0, 0, "kΩ")),
        "<= 1,5 A und <= 1 C = %s" % _f(c_rate, 2, "A"),
        "IP2326-Datenblatt V1.11: ICHG = 90000/R_ISET[Ohm] (S. 11); "
        "Grenze 1,5 A (§7, S. 4); ISET darf nicht offen bleiben (§4); "
        "Li-Ion erlaubt 1 C (Review §4.1)")


def check_ladeschluss_2s():
    """Ladeschluss = 2 x 4,2 V, VSET/CON_SEL offen, keine 8V8-Variante im BOM."""
    v_target = 2.0 * IP2326_CELL_MAX_V
    within = abs(v_target - IP2326_VSET_OPEN_V) <= IP2326_VSET_TOL_V
    bom = circuit.BOM_PATH.read_text(encoding="utf-8") if circuit.BOM_PATH.exists() else ""
    no_8v8 = "8V8" not in bom and "8v8" not in bom
    # Pin 3 = VSET (offen ⇒ 8,4 V), Pin 10 = CON_SEL (offen ⇒ 2S).
    offen = {}
    for pin_no in ("3", "10"):
        offen[pin_no] = all(
            not (comp == "U_CHG" and re.match(r"\s*%s\b" % pin_no, pin))
            for _net, nodes in circuit.load_netlist().items()
            for comp, pin in nodes)
    ok = within and no_8v8 and all(offen.values())
    return CheckResult(
        "Ladeschluss 2S", ok,
        "%s (2 x %s), VSET %s, CON_SEL %s, 8V8 im BOM %s"
        % (_f(v_target, 2, "V"), _f(IP2326_CELL_MAX_V, 1, "V"),
           "offen" if offen["3"] else "VERDRAHTET",
           "offen" if offen["10"] else "VERDRAHTET",
           "nein" if no_8v8 else "JA -> FEHLER"),
        "8,4 V +-0,1 V, VSET/CON_SEL offen, kein IP2326_8V8",
        "IP2326 S. 4/S. 5: VSET offen ⇒ 8,4 V (8,3-8,5 V) = 4,2 V/Zelle, "
        "CON_SEL offen ⇒ 2S (S. 8); IP2326_8V8 waere 8,8 V (4,4 V/Zelle) "
        "und fuer Li-Ion unzulaessig")


def check_ladeeingang_strom():
    """Eingangsstrom aus 5 V: Ladeleistung/eta plus Systemlast."""
    sys = circuit.load_system()
    r_iset = circuit.parse_ohm(circuit.part("R_ISET")["value"])
    i_chg = IP2326_ICHG_K / r_iset
    i_sys = sys["pump_i_nom_a"] + sys["o2_pump_i_a"]
    i_in = sys["pack_v_max"] * i_chg / (IP2326_EFF * sys["supply_v"]) + i_sys
    ok = i_in <= sys["supply_i_a"]
    return CheckResult(
        "Ladeeingangsstrom", ok,
        "%s (Ladung %s + System %s)"
        % (_f(i_in, 2, "A"),
           _f(sys["pack_v_max"] * i_chg / (IP2326_EFF * sys["supply_v"]), 2, "A"),
           _f(i_sys, 2, "A")),
        "<= %s (Netzteilannahme)" % _f(sys["supply_i_a"], 1, "A"),
        "IP2326 S. 1: eta 94 % (5 V->8 V/1 A); I_in = V_out*I_CHG/(eta*V_USB) "
        "+ Systemlast (beide Pumpen, schaltplan §6.1)")


def check_buck5_ausgang():
    """5-V-Buck SY8113B: V_out = 0,6 V x (1 + R_FB5_TOP/R_FB5_BOT)."""
    v = circuit.rail_5v()
    sys = circuit.load_system()
    nominal = sys["pump_v"]
    ok = abs(v - nominal) <= 0.05 * nominal
    return CheckResult(
        "5-V-Buck-Ausgang", ok,
        "%s (+-5 %% von %s)" % (_f(v, 3, "V"), _f(nominal, 1, "V")),
        "5,0 V +-5 %",
        "SY8113B-Datenblatt S. 1/S. 2: V_REF 0,6 V +-1,5 %, "
        "V_out = 0,6 x (1 + R_FB5_TOP/R_FB5_BOT); Pumpennennspannung 5 V")


def check_buck3_ausgang():
    """AP63203-Festspannungsversion: FB (Pin 1) direkt auf +3V3, kein Teiler.

    Geprueft wird beides: der Ausgangswert liegt im Modulfenster, UND FB ist
    wirklich direkt am Ausgang (nicht ueber einen Teiler), UND es existiert
    kein Teilerbauteil R_FB3_TOP/R_FB3_BOT und kein Netz FB_3V3 mehr.
    """
    v = circuit.rail_3v3()
    fb_net = _pin_net("U_BUCK3", "1")
    fb_direct = fb_net == "+3V3"
    rest_teiler = [d for d in circuit.parts() if d.startswith("R_FB3")]
    netz_fb = "FB_3V3" in circuit.load_netlist()
    spannung_ok = MODULE_VDD33_MIN_V <= v <= MODULE_VDD33_MAX_V
    ok = spannung_ok and fb_direct and not rest_teiler and not netz_fb
    return CheckResult(
        "3,3-V-Buck-Ausgang", ok,
        "%s (FB Pin 1 auf %s %s, Teiler %s, Netz FB_3V3 %s)"
        % (_f(v, 3, "V"), fb_net, "OK" if fb_direct else "FEHLER",
           ", ".join(rest_teiler) or "keiner",
           "vorhanden -> FEHLER" if netz_fb else "entfallen"),
        "3,0 V bis 3,6 V (Modul); FB direkt auf +3V3, kein Teiler",
        "AP63203-Datenblatt DS41326: Festspannungsversion, VFB 3,27/3,30/3,33 V "
        "bzw. 'AP63203 ... fixed output voltages of 3.3V'; Fig. 21 fuehrt FB "
        "direkt auf den Ausgang. Der frueher geprüfte Teiler R_FB3_TOP/BOT ist "
        "entfallen (Review 16.09.2026); Espressif ESP32-C6-MINI-1: "
        "V_DD33 3,0-3,6 V")


def check_buck5_induktivitaet():
    """Rippelstrom und Spitzenstrom des 5-V-Bucks bei Last bis 3 A."""
    l = circuit.parse_henry(circuit.part("L_BUCK5")["desc"])
    isat = circuit.parse_ampere(circuit.part("L_BUCK5")["value"])
    sys = circuit.load_system()
    v_out = circuit.rail_5v()
    i_last = sys["pump_i_inrush_a"]
    ok = i_last <= BUCK5_IOUT_MAX_A
    teile = []
    for v_in in (sys["pack_v_max"], _uvlo_trip(sys)):
        d = v_out / v_in
        di = (v_in - v_out) * d / (l * BUCK5_FSW_HZ)
        i_peak = i_last + di / 2.0
        teile.append("Vin %s: dI %s, I_peak %s"
                     % (_f(v_in, 2, "V"), _f(di, 2, "A"), _f(i_peak, 2, "A")))
        ok = ok and i_peak < isat
    return CheckResult(
        "5-V-Buck-Induktivitaet", ok,
        "%s (I_Last %s, Isat %s); %s"
        % (_f(l * 1e6, 1, "µH"), _f(i_last, 1, "A"), _f(isat, 1, "A"),
           "; ".join(teile)),
        "I_peak < Isat 4,0 A und I_Last <= 3 A",
        "PRS6045-Datenblatt: L_BUCK5 4,7 µH, Isat 4,0 A; SY8113B S. 1: 3 A, "
        "500 kHz; dI = (Vin-Vout)*D/(L*f) mit D = Vout/Vin; "
        "I_Last = Pumpenanlauf 3 A (bom §4c)")


def check_buck3_induktivitaet():
    """Rippelstrom und Spitzenstrom des 3,3-V-Bucks bei 1,1 MHz."""
    l = circuit.parse_henry(circuit.part("L_BUCK3")["desc"])
    isat = circuit.parse_ampere(circuit.part("L_BUCK3")["value"])
    sys = circuit.load_system()
    v_out = circuit.rail_3v3()
    i_last = sys["module_tx_peak_ma"] / 1000.0
    ok = True
    teile = []
    for v_in in (sys["pack_v_max"], _uvlo_trip(sys)):
        d = v_out / v_in
        di = (v_in - v_out) * d / (l * BUCK3_FSW_HZ)
        i_peak = i_last + di / 2.0
        teile.append("Vin %s: dI %s, I_peak %s"
                     % (_f(v_in, 2, "V"), _f(di, 2, "A"), _f(i_peak, 2, "A")))
        ok = ok and i_peak < isat
    return CheckResult(
        "3,3-V-Buck-Induktivitaet", ok,
        "%s (I_Last TX-Peak %s, Isat %s); %s"
        % (_f(l * 1e6, 1, "µH"), _f(i_last, 3, "A"), _f(isat, 1, "A"),
           "; ".join(teile)),
        "I_peak < Isat 4,0 A",
        "PRS6045-Datenblatt: L_BUCK3 4,7 µH, Isat 4,0 A; AP63203 DS41326: "
        "2 A, 1,1 MHz; I_Last = Modul-TX-Peak 382 mA (Espressif Tab. 6-4)")


def check_uvlo_schwelle():
    """TPS3839-Ausloesung: V_trip = V_IT x (1 + R3a/R3b) + Iq x R3a."""
    sys = circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    v_trip = _uvlo_trip(sys)
    ok = WATCHDOG_TRIP_MIN_V <= v_trip <= WATCHDOG_TRIP_MAX_V
    return CheckResult(
        "UVLO-Schwelle", ok,
        "%s (V_IT %s, R3a %s, Iq %s)"
        % (_f(v_trip, 3, "V"), _f(TPS3839_VIT_NOM_V, 2, "V"),
           _f(r3a / 1000.0, 0, "kΩ"), _f(sys["iq_watchdog_ua"], 2, "µA")),
        "6,0 V bis 6,6 V Pack (2 x 3,0..3,3 V)",
        "TPS3839 S. 7: V_IT 3,003-3,126 V, Hysterese 31 mV; "
        "V_trip = V_IT x (1 + R3a/R3b) + Iq x R3a (Teiler 51 k/51 k, "
        "Iq typ. 0,15 µA bzw. max. 0,5 µA)")


def check_uvlo_teiler():
    """UV-Teiler 51 k/51 k: Teilerstrom, Tagesverbrauch und Iq-Offset.

    Rechnet die Verschiebung der Schwelle durch den Waechter-Ruhestrom als
    Iq_max x R3a (nicht geschaetzt) und den Teilerstrom als
    V_Pack,max/(R3a+R3b).  Beides muss im Rahmen bleiben: der Offset unter
    50 mV, der Teilerstrom als kleiner Posten des Standby-Budgets.
    """
    sys = circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    i_div = sys["pack_v_max"] / (r3a + r3b)
    mah_day = i_div * 1e6 / 1000.0 * 24.0
    offset_max = TPS3839_IQ_MAX_UA * 1e-6 * r3a
    offset_typ = TPS3839_IQ_TYP_UA * 1e-6 * r3a
    symmetrisch = abs(r3a - r3b) < 1.0
    ok = (abs(r3a - 51000.0) < 1.0 and symmetrisch
          and offset_max <= 0.050 and i_div <= 100e-6)
    return CheckResult(
        "UV-Teiler-Offset", ok,
        "R3a %s/%s, Teilerstrom %s (%s/Tag), Offset Iq_max x R3a = %s "
        "(typ. %s)"
        % (_f(r3a / 1000.0, 0, "kΩ"), _f(r3b / 1000.0, 0, "kΩ"),
           _f(i_div * 1e6, 1, "µA"), _f(mah_day, 2, "mAh"),
           _f(offset_max * 1000.0, 1, "mV"), _f(offset_typ * 1000.0, 1, "mV")),
        "R3a = R3b = 51 kΩ, Iq-Offset <= 50 mV, Teilerstrom <= 100 µA",
        "Fix 16.09.2026 (Review): von 200 k/200 k auf 51 k/51 k verkleinert. "
        "TPS3839-Datenblatt SBVS193D: Iq 150 nA typ., 500 nA max.; der Strom "
        "fließt durch R3a und verschiebt die Schwelle um Iq x R3a "
        "(200 k waeren bis ~0,2 V gewesen, jetzt +15..+50 mV). Teilerstrom "
        "82 µA = ~2 mAh/Tag, Teil des 250-µA-Standby-Budgets (schaltplan "
        "§3.2/§13.5)")



def _ohms(designator):
    """Widerstand eines Bauteils aus dem Wertfeld, ersatzweise dem Bauteilfeld.

    In schaltplan_v1.md tragen einzelne Zeilen (z. B. R_SENS_GATE) den Wert in
    der zweiten Spalte statt in "Wert"; beide Felder werden daher versucht.
    """
    entry = circuit.part(designator)
    for key in ("value", "desc"):
        text = entry.get(key)
        if not text:
            continue
        try:
            return circuit.parse_ohm(text)
        except circuit.CircuitError:
            continue
    raise circuit.CircuitError(
        "kein Widerstandswert fuer %s in schaltplan_v1.md" % designator)


def check_gate_pulldowns():
    """Beide Pumpen-Gates haengen ueber 47 kOhm auf GND (Aus bei toter MCU).

    Ersetzt den frueheren Klemmzweig-Sinkstrom: der Dioden-Klemmzweig ist
    entfallen.  Die wirksame zweite Ebene ist der Gate-Pulldown -- ist die MCU
    hochohmig (Reset, Deep-Sleep, Absturz), zieht R2/R_GATE2_PD das jeweilige
    Gate auf 0 V und der Low-Side-MOSFET sperrt.
    """
    teile = []
    ok = True
    for r_des, gate in (("R2", "GATE"), ("R_GATE2_PD", "GATE2")):
        r_nets = set(_nets_of(r_des))
        good = r_nets == {gate, "GND"} and abs(_ohms(r_des) - 47000.0) < 1.0
        ok = ok and good
        teile.append("%s %s an %s/GND %s"
                     % (r_des, "47 kΩ" if abs(_ohms(r_des) - 47000.0) < 1.0
                        else _f(_ohms(r_des) / 1000.0, 1, "kΩ"),
                        gate, "OK" if good else "FEHLER"))
    # Die Gates muessen ueber einen Serien-R von der MCU kommen (R1/R_GATE2),
    # damit der Pulldown bei hochohmigem GPIO den Knoten wirklich auf 0 V zieht.
    serie = (set(_nets_of("R1")) == {"PUMP_EN", "GATE"}
             and set(_nets_of("R_GATE2")) == {"PUMP2_EN", "GATE2"})
    ok = ok and serie
    teile.append("Gate-Serie R1/R_GATE2 %s" % ("OK" if serie else "FEHLER"))
    return CheckResult(
        "Gate-Pulldowns", ok, "; ".join(teile),
        "R2 (GATE/GND) und R_GATE2_PD (GATE2/GND) je 47 kΩ; Gates ueber "
        "Serien-R1/R_GATE2 von der MCU",
        "Review 16.09.2026: der alte Dioden-Klemmzweig (D3/D8 + R_CLAMP1/2) "
        "konnte das Gate gegen den 1-kΩ-GPIO-Zweig rechnerisch nicht "
        "abschalten (~2,97 V) und ist entfallen. Wirksam bleiben (a) die "
        "5-V-Abschaltung durch U7 und (b) diese 47-kΩ-Pulldowns: bei "
        "hochohmigem GPIO liegt V_GS = 0 V, der MOSFET sperrt")


def check_waechter_abschaltung():
    """Waechter schaltet die 5-V-Schiene wirklich ab (RESET_UV -> U_BUCK5 EN).

    Ersetzt die frueher geprüfte Klemmzweig-Serie.  Geprueft wird der
    verbliebene Mechanismus: der TPS3839-Ausgang (Pin 2) liegt auf RESET_UV und
    U_BUCK5 Pin 4 (EN) haengt am selben Netz -> unter der Schwelle ist der
    Buck-Ausgang 0 V und damit die Pumpenversorgung aus.  Zugleich darf kein
    Rest des entfernten Klemmzweigs mehr existieren (D3/D8/R_CLAMP*/KLAMP*).
    """
    reset_u7 = _pin_net("U7", "2")
    en_buck5 = _pin_net("U_BUCK5", "4")
    verdrahtet = reset_u7 == "RESET_UV" and en_buck5 == "RESET_UV"
    rest = [d for d in circuit.parts()
            if d in ("R_CLAMP1", "R_CLAMP2", "D3", "D8")]
    nets = set(circuit.load_netlist())
    rest_nets = sorted(n for n in nets if n.startswith("KLAMP"))
    ok = verdrahtet and not rest and not rest_nets
    return CheckResult(
        "Waechter-Abschaltung", ok,
        "U7 Pin 2 (RESET) auf %s, U_BUCK5 Pin 4 (EN) auf %s %s; Klemmzweig-Rest "
        "%s %s"
        % (reset_u7, en_buck5, "OK" if verdrahtet else "FEHLER",
           ", ".join(rest) or "keiner", "" if not rest_nets else
           "-> Netze " + ", ".join(rest_nets) + " FEHLER"),
        "U7-RESET und U_BUCK5-EN auf RESET_UV; kein D3/D8/R_CLAMP*/KLAMP*",
        "TPS3839 SBVS193D: Push-Pull-Ausgang aktiv-low; SY8113B: EN low => "
        "Ausgang 0 V. Damit ist die Pumpenversorgung im Waechterfall sicher "
        "aus. Der Dioden-Klemmzweig D3/D8/R_CLAMP1/2 ist im Review 16.09.2026 "
        "als wirkungslos entfernt worden (§13.5)")



def check_adc_teiler_max():
    """ADC-Teiler R_SENSE_TOP/BOT: Spannung an IO1 im ganzen Packbereich."""
    sys = circuit.load_system()
    r_top = circuit.parse_ohm(circuit.part("R_SENSE_TOP")["value"])
    r_bot = circuit.parse_ohm(circuit.part("R_SENSE_BOT")["value"])
    v_ref = sys["adc_vref_mv"] / 1000.0
    v_max = sys["pack_v_max"] * r_bot / (r_top + r_bot)
    v_min = sys["pack_v_min"] * r_bot / (r_top + r_bot)
    ok = v_max <= v_ref and (v_min * 1000.0) >= ADC_MIN_USEFUL_MV
    return CheckResult(
        "ADC-Teiler Packspannung", ok,
        "8,4 V -> %s, 6,0 V -> %s (V_ref %s)"
        % (_f(v_max, 3, "V"), _f(v_min, 3, "V"), _f(v_ref, 2, "V")),
        "<= 3,3 V und >= 1,0 V",
        "Espressif ESP32-C6 ADC1: 12 Bit, ADC_ATTEN_DB_12 = 0..3300 mV; "
        "V_ADC = VBAT x R_bot/(R_top+R_bot), Teiler 200 k/68 k")


def check_buck_en_pegel():
    """High-Pegel des Waechter-Ausgangs gegen die EN-Schwelle des 5-V-Bucks."""
    sys = circuit.load_system()
    v_dd = _uvlo_trip(sys) / 2.0   # UV_REF = VBAT/2 am Freigabepunkt
    v_oh = v_dd - TPS3839_VOH_DROP_V
    ok = v_oh > BUCK5_EN_HIGH_V
    return CheckResult(
        "Buck-EN-Pegel", ok,
        "V_OH %s (V_DD %s - 0,4 V)" % (_f(v_oh, 2, "V"), _f(v_dd, 2, "V")),
        "> 1,5 V (EN High)",
        "TPS3839 SBVS193D: V_OH >= V_DD - 0,4 V (Push-Pull); "
        "SY8113B: EN-High-Schwelle 1,5 V, 'Do not float'")


def check_kein_low_vin_am_vbat():
    """Kein Bauteil mit zu kleiner Eingangsspannung auf dem VBAT-Netz."""
    sys = circuit.load_system()
    v_max = sys["pack_v_max"]
    comps = sorted({comp for comp, _pin in circuit.parts_on("VBAT")})
    findings = []
    for comp in comps:
        if comp in VBAT_IC_VIN_MAX:
            limit = VBAT_IC_VIN_MAX[comp][0]
            if limit < v_max:
                findings.append("%s V_IN,max %s V < %s V"
                                % (comp, _f(limit, 1, "V"), _f(v_max, 1, "V")))
        elif comp in VBAT_PASSIV or comp.startswith(circuit.ONE_PIN_OK_PREFIX):
            continue
        else:
            findings.append("%s nicht als VBAT-tauglich gelistet" % comp)
    ok = not findings
    return CheckResult(
        "VBAT-Spannungsfestigkeit", ok,
        "%d Teilnehmer: %s%s"
        % (len(comps), ", ".join(comps),
           "" if ok else " -> " + "; ".join(findings)),
        "nur zugelassene Teilnehmer, V_IN,max >= 8,4 V",
        "ME6211-Lektion (V_IN,max 6,0 V) aus Review §5 Befund 4: passive "
        "VBAT-Teilnehmer sind gelistet, aktive werden gegen ihre "
        "Datenblatt-Eingangsspannung geprueft (IP2326 9,5 V, SY8113B 18 V, "
        "AP63203 32 V)")


def check_standby_budget():
    """Ruhestrom im Deep-Sleep und Tagesverbrauch; Lichtsensor geschaltet."""
    sys = circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    r_top = circuit.parse_ohm(circuit.part("R_SENSE_TOP")["value"])
    r_bot = circuit.parse_ohm(circuit.part("R_SENSE_BOT")["value"])
    uvlo_ua = sys["pack_v_max"] / (r3a + r3b) * 1e6
    adc_ua = sys["pack_v_max"] / (r_top + r_bot) * 1e6
    total_ua = (sys["module_sleep_ua"] + sys["iq_buck5_ua"] + sys["iq_buck3_ua"]
                + sys["iq_watchdog_ua"] + uvlo_ua + adc_ua)
    mah_day = total_ua / 1000.0 * 24.0
    # Lichtsensor haengt an SENSOR_PWR (ueber Q_SENS geschaltet, IO3 treibt
    # nur das Gate) -> im Deep-Sleep kein Strom.
    j7_net = circuit.net_of("J7", "2")
    switched = j7_net == "SENSOR_PWR"
    ok = total_ua <= 250.0 and switched
    return CheckResult(
        "Standby-Budget", ok,
        "%s, %s/Tag; Lichtsensor an %s %s"
        % (_f(total_ua, 1, "µA"), _f(mah_day, 2, "mAh"),
           j7_net, "geschaltet" if switched else "DAUERHAFT -> FEHLER"),
        "<= 250 µA; Sensor an SENSOR_PWR (ueber Q_SENS geschaltet)",
        "Datenblaetter: SY8113B Iq 100 µA, AP63203 22 µA, TPS3839 0,15 µA "
        "(schaltplan §6.2) + Teiler 82/31,4 µA (§13.5) + Modul 7 µA; "
        "Lichtsensor an geschaltetem SENSOR_PWR, das Gate treibt IO3")


def check_system_quellen():
    """Jede Zahl des SYSTEM-Blocks steht woertlich in ihrer Quelldatei."""
    missing = []
    for entry in circuit.system_quellen():
        path = _SYSTEM_FILES.get(entry.datei)
        if path is None or not path.exists():
            missing.append("%s: Datei %s fehlt" % (entry.key, entry.datei))
            continue
        text = path.read_text(encoding="utf-8")
        if entry.beleg not in text:
            missing.append("%s: %r nicht in %s"
                           % (entry.key, entry.beleg, entry.datei))
    ok = not missing
    return CheckResult(
        "Systemquellen", ok,
        "%d Systemwerte belegt" % len(circuit.system_quellen()) if ok
        else "; ".join(missing),
        "jeder SYSTEM-Wert hat sein woertliches Belegfragment in der Datei",
        "Regel: Systemgroessen stammen ausschliesslich aus den Dokumenten. "
        "Prueft fuer jeden Eintrag den Belegtext in schaltplan_v1.md bzw. "
        "bom_entscheidung.md")


# ===========================================================================
# Akku-Schutz auf der Platine (HY2120-CB + Schalterpaar) - neu 16.09.2026
# ===========================================================================

def _doc_values(pattern, name):
    """Alle Zahlen zu einem Muster in schaltplan_v1.md (Komma -> Punkt).

    Fehlt das Muster ganz, bricht die Pruefung laut ab (CircuitError) statt
    still zu bestehen.
    """
    text = circuit.SCHEMATIC_PATH.read_text(encoding="utf-8")
    raw = re.findall(pattern, text)
    if not raw:
        raise circuit.CircuitError(
            "kein Dokumentwert fuer %s in schaltplan_v1.md (Muster %r)"
            % (name, pattern))
    return [float(v.replace(",", ".")) for v in raw]


def _doc_consistent(values):
    """True, wenn alle Fundstellen denselben Wert tragen."""
    return all(abs(v - values[0]) <= 1e-9 for v in values[1:])


def _pin_net(designator, pin):
    """Netz eines Pins; kennt die Netzliste den Pin nicht, Werkzeugfehler.

    Akzeptiert sowohl den rohen Pin-Namen aus der Netzliste ("5 D", "4 G",
    "3 VDD") als auch die auf die fuehrende Ziffer reduzierte Form ("5", "4"),
    damit Aufrufer nicht von der Schreibweise des Symbols abhaengen.  Ein
    Name, den weder die rohe noch die reduzierte Form trifft, ist ein
    **Werkzeugfehler** (:class:`PruefFehler`), kein Design-Fehler: das
    Pruefmodell ist veraltet und hat den Pin nie gesehen.
    """
    raw_pin, reduced = {}, {}
    for net, nodes in circuit.load_netlist().items():
        for comp, p in nodes:
            if comp != designator:
                continue
            raw_pin.setdefault(p.strip(), net)
            m = re.match(r"\s*([0-9]+)\b", p)
            reduced.setdefault(m.group(1) if m else p.strip(), net)
    if pin in raw_pin:
        return raw_pin[pin]
    if pin in reduced:
        return reduced[pin]
    raise PruefFehler(
        "Pin %r an %s existiert nicht in der Netzliste \u2014 checks.py veraltet"
        % (pin, designator))


def check_schutz_serie():
    """Serienkette des Platinen-Schutzes in der Minusleitung (Topologie)."""
    j1_src = _pin_net("J1", "1")
    q1_s = [_pin_net("Q_PROT1", p) for p in ("1", "2", "3")]
    q1_drain = _pin_net("Q_PROT1", "5 D")
    q1_gate = _pin_net("Q_PROT1", "4")
    q2_s = [_pin_net("Q_PROT2", p) for p in ("1", "2", "3")]
    q2_drain = _pin_net("Q_PROT2", "5 D")
    q2_gate = _pin_net("Q_PROT2", "4")
    vss = _pin_net("U_PROT", "6")
    od = _pin_net("U_PROT", "1")
    oc = _pin_net("U_PROT", "2")
    cs = _pin_net("U_PROT", "3")
    vdd = _pin_net("U_PROT", "5")
    vc = _pin_net("U_PROT", "4")
    chg_vbatm = _pin_net("U_CHG", "23")
    chg_gnd = _pin_net("U_CHG", "24")

    pack_minus = (j1_src == q1_s[0] == q1_s[1] == q1_s[2] == vss)
    common = q1_drain == q2_drain
    q2_on_gnd = q2_s[0] == q2_s[1] == q2_s[2] == "GND"
    od_only_q1 = (od == q1_gate and od != q2_gate)
    oc_only_q2 = (oc == q2_gate and oc != q1_gate)
    gate_ok = od_only_q1 and oc_only_q2
    cs_ok = set(_nets_of("R_PROT_CS")) == {cs, "GND"} and cs != "GND"
    vdd_ok = set(_nets_of("R_PROT_VDD")) == {vdd, "VBAT"}
    vc_ok = set(_nets_of("R_PROT_VC")) == {vc, "MID"}
    cb_ok = set(_nets_of("R_CB")) == {chg_vbatm, "MID"}
    chg_gnd_ok = chg_gnd == vss
    # Gegenprobe: Pack-Minus und Schalterpaar duerfen NICHT auf GND liegen,
    # sonst ist der Schutz kurzgeschlossen und wirkungslos.
    pair_off_gnd = (j1_src != "GND" and q1_s[0] != "GND"
                    and q1_drain != "GND")
    checks = (
        ("Pack-Minus J1.1/Q_PROT1-S/U_PROT-VSS", pack_minus),
        ("Drains beider auf einem Netz (PROT_COMMON)", common),
        ("Q_PROT2-S auf GND", q2_on_gnd),
        ("OD an Q_PROT1-Gate, OC an Q_PROT2-Gate (kein Tausch)", gate_ok),
        ("R_PROT_CS CS<->GND", cs_ok),
        ("R_PROT_VDD VDD<->VBAT", vdd_ok),
        ("R_PROT_VC VC<->MID", vc_ok),
        ("R_CB VBATM<->MID", cb_ok),
        ("U_CHG.24 auf BAT_MINUS", chg_gnd_ok),
        ("Schalterpaar nicht auf GND", pair_off_gnd),
    )
    ok = all(good for _label, good in checks)
    ist = "; ".join("%s %s" % (label, "OK" if good else "FEHLER")
                    for label, good in checks)
    ist += " (Netze: J1-1 %s, Q_PROT1-S %s, Drains %s/%s, Q_PROT2-S %s, " \
          "OD %s, OC %s, U_CHG-24 %s)" % (
              j1_src, q1_s[0], q1_drain, q2_drain, q2_s[0], od, oc, chg_gnd)
    return CheckResult(
        "Schutz-Serienkette", ok, ist,
        "J1-1 = Q_PROT1-S = U_PROT-VSS (BAT_MINUS), beide Drains auf "
        "PROT_COMMON, Q_PROT2-S auf GND, OD nur an Q_PROT1-Gate (Entlader, "
        "packseitig), OC nur an Q_PROT2-Gate, R_PROT_CS CS<->GND, R_PROT_VDD "
        "VDD<->VBAT, R_PROT_VC VC<->MID, R_CB VBATM<->MID, U_CHG-24 auf "
        "BAT_MINUS; Schalterpaar nicht auf GND",
        "Regressionsschutz der Topologie (Review 16.09.2026): der Schutz "
        "sitzt in der Minusleitung zwischen Pack-Minus (BAT_MINUS) und "
        "Board-GND. Q_PROT1 (Entlader, Gate an OD) liegt packseitig, Q_PROT2 "
        "(Lader, Gate an OC) an GND, gemeinsamer Drain PROT_COMMON. Wird ein "
        "Source auf GND gelegt oder OD/OC getauscht, ist der Schutz "
        "wirkungslos bzw. die Entlade-/Ladetrennung vertauscht")


def check_schutz_schwellen():
    """Abschaltstaffelung: Zellenschutz gegen Lader, Waechter und Zelle."""
    ov_vals = _doc_values(
        r"berlad(?:ung|en)\s*\*\*\s*([0-9]+(?:[.,][0-9]+)?)\s*V",
        "Ueberladung je Zelle")
    uv_vals = _doc_values(
        r"Tiefentlad(?:ung|en)\s*\*\*\s*([0-9]+(?:[.,][0-9]+)?)\s*V",
        "Tiefentladung je Zelle")
    ov_doc_ok = _doc_consistent(ov_vals)
    uv_doc_ok = _doc_consistent(uv_vals)
    ov_cell = ov_vals[0]
    uv_cell = uv_vals[0]
    sys = circuit.load_system()
    ov_pack = 2.0 * ov_cell
    uv_pack = 2.0 * uv_cell
    trip = _uvlo_trip(sys)
    fw = 2.0 * sys["cell_firmware_stop_v"]
    pcm = 2.0 * sys["cell_pcm_v"]
    over_ok = IP2326_VSET_OPEN_V < ov_pack < IP2326_8V8_V
    under_ok = pcm < uv_pack < trip
    staffel_ok = fw > trip > uv_pack
    ok = ov_doc_ok and uv_doc_ok and over_ok and under_ok and staffel_ok
    return CheckResult(
        "Schutz-Schwellen", ok,
        "Ueberladung %s/Zelle = %s Pack (%s < x < %s) %s; Tiefentladung "
        "%s/Zelle = %s Pack (%s < x < Waechter %s) %s; Staffelung FW %s > "
        "Waechter %s > Zelle %s %s; Dokument konsistent Ueberladung %s/"
        "Tiefentladung %s"
        % (_f(ov_cell, 2, "V"), _f(ov_pack, 2, "V"),
           _f(IP2326_VSET_OPEN_V, 1, "V"), _f(IP2326_8V8_V, 1, "V"),
           "OK" if over_ok else "FEHLER",
           _f(uv_cell, 2, "V"), _f(uv_pack, 2, "V"), _f(pcm, 1, "V"),
           _f(trip, 2, "V"), "OK" if under_ok else "FEHLER",
           _f(fw, 2, "V"), _f(trip, 2, "V"), _f(uv_pack, 2, "V"),
           "OK" if staffel_ok else "FEHLER",
           "ja" if ov_doc_ok else "NEIN", "ja" if uv_doc_ok else "NEIN"),
        "8,4 V (Ladeschluss) < Ueberladung Pack < 8,8 V; 5,0 V "
        "(2 x 2,5 V Zelle) < Tiefentladung Pack < Waechter 6,19 V; "
        "FW-Stopp 6,8 V > Waechter > Zelle 5,80 V",
        "HY2120-Datenblatt (schaltplan §3.1/§6.3): Ueberladung 4,28 V/Zelle, "
        "Tiefentladung 2,90 V/Zelle, jeweils woertlich aus dem Dokument "
        "gelesen; Ladeschluss IP2326 8,4 V (VSET offen) bzw. 8,8 V der "
        "verbotenen 8V8-Variante; Waechter aus den echten R3a/R3b (TPS3839 "
        "V_IT 3,08 V); Firmware-Stopp 2 x 3,4 V (bom §4b). Ueberladung muss "
        "das normale Laden ueberleben, Tiefentladung vor dem Waechter greifen")


def check_schutz_ueberstrom():
    """Reserve der Ueberstromabschaltung gegen den Pumpenanlauf."""
    dip_vals = _doc_values(
        r"berstrom(?:schwelle)?\s*\*\*\s*([0-9]+(?:[.,][0-9]+)?)\s*mV",
        "Entlade-Ueberstrom")
    dur_vals = _doc_values(r"Dauer\s+([0-9]+(?:[.,][0-9]+)?)\s*A",
                           "Dauerlast")
    dip_doc_ok = _doc_consistent(dip_vals)
    dur_doc_ok = _doc_consistent(dur_vals)
    v_dip = dip_vals[0] / 1000.0
    i_dauer = dur_vals[0]
    sys = circuit.load_system()
    r_pair = 2.0 * PSMN4R2_RDSON_MAX_OHM
    i_trip = v_dip / r_pair
    p_pump = sys["pump_v"] * sys["pump_i_inrush_a"]
    i_inrush = p_pump / (BUCK_INRUSH_EFF * sys["pack_v_min"])
    reserve = i_trip / i_inrush
    reserve_ok = reserve >= 2.0
    drop = i_dauer * r_pair
    drop_ok = drop <= SCHUTZ_DAUER_DROP_MAX_V
    ok = dip_doc_ok and dur_doc_ok and reserve_ok and drop_ok
    return CheckResult(
        "Schutz-Ueberstrom", ok,
        "Ausloesung %s / Paar %s = %s; Anlauf %s/(%s x %s) = %s "
        "(Reserve %s) %s; Abfall bei %s = %s %s; Dokument konsistent %s/%s"
        % (_f(v_dip * 1000.0, 0, "mV"), _f(r_pair * 1000.0, 1, "mΩ"),
           _f(i_trip, 1, "A"), _f(p_pump, 1, "W"),
           _f(BUCK_INRUSH_EFF, 2, ""), _f(sys["pack_v_min"], 1, "V"),
           _f(i_inrush, 2, "A"), _f(reserve, 1, "x"),
           "OK" if reserve_ok else "FEHLER",
           _f(i_dauer, 2, "A"), _f(drop * 1000.0, 1, "mV"),
           "OK" if drop_ok else "FEHLER",
           "ja" if dip_doc_ok else "NEIN",
           "ja" if dur_doc_ok else "NEIN"),
        "Ausloesestrom >= 2 x Anlaufstrom und Abfall des Paares bei Dauerlast "
        "<= %s" % _f(SCHUTZ_DAUER_DROP_MAX_V * 1000.0, 0, "mV"),
        "HY2120-Datenblatt: V_DIP 200 mV (+-30 mV) ueber dem Paar "
        "(schaltplan §3.1); PSMN4R2-30MLDX: R_DS(on,max) 5,7 mOhm bei "
        "V_GS 4,5 V => Paar 11,4 mOhm (schaltplan §6.3); Pumpenanlauf "
        "5 V/3 A = %s an %s Pack ueber eta_Buck %s (bom §4c: eta 0,90), "
        "Dauerlast %s (schaltplan §6.3); die interne Verzoegerung von %s "
        "schuetzt den kurzzeitigen Anlauf"
        % (_f(p_pump, 1, "W"), _f(sys["pack_v_min"], 1, "V"),
           _f(BUCK_INRUSH_EFF, 2, ""), _f(i_dauer, 2, "A"),
           _f(HY2120_OC_DELAY_MS, 0, "ms")))


# ===========================================================================
# Bestehende Pruefungen, auf die 2S-Rails gezogen
# ===========================================================================

def check_gate_spannung():
    """Gate-Spannung aus dem Teiler R1/R2 im Betrieb."""
    r1 = circuit.parse_ohm(circuit.part("R1")["value"])
    r2 = circuit.parse_ohm(circuit.part("R2")["value"])
    rail = circuit.rail_3v3()
    v = rail * r2 / (r1 + r2)
    return CheckResult(
        "Gate-Spannung", v >= 2.5 and v > 1.45,
        "%s (%.0f %% von %s)" % (_f(v, 2, "V"), r2 / (r1 + r2) * 100.0,
                                 _f(rail, 2, "V")),
        ">= 2,5 V und > 1,45 V",
        "AO3400A-Datenblatt: RDS(on) bei VGS = 2,5 V spezifiziert, "
        "VGS(th) max = 1,45 V; Rail +3V3 aus dem AP63203 in der "
        "Festspannungsversion")


def check_mosfet_verlust():
    """Leitverluste des Pumpen-MOSFET Q1 im Nennbetrieb."""
    i_pump = circuit.load_system()["pump_i_nom_a"]
    rds_on = 0.048  # AO3400A-Datenblatt: < 48 mΩ bei VGS = 2,5 V
    p = i_pump * i_pump * rds_on
    return CheckResult(
        "MOSFET-Verlustleistung", p <= 0.25,
        "%s (I %s, RDS(on) 48 mΩ)"
        % (_f(p * 1000.0, 1, "mW"), _f(i_pump * 1000.0, 0, "mA")),
        "<= 0,25 W (Nennbetrieb)",
        "AO3400A-Datenblatt: 48 mΩ bei VGS = 2,5 V; P = I_pump² · RDS(on); "
        "I_pump = 0,4 A (Pumpennennstrom); der 3-A-Anlauf ist transient "
        "(~100 ms, Review §4.4)")


def check_freilaufdiode():
    """Freilaufdiode D1: Stromreserve und Sperrspannung."""
    sys = circuit.load_system()
    d1 = circuit.part("D1")["value"]
    i_pump = sys["pump_i_nom_a"]
    if_a = circuit.parse_ampere(d1)
    vrrm = circuit.parse_volt(d1)
    vbat_max = sys["pack_v_max"]
    ok = i_pump <= 0.5 * if_a and vrrm >= 4.0 * vbat_max
    return CheckResult(
        "Freilaufdiode", ok,
        "I %s (<= 50 %% von %s), VRRM %s (>= 4 x %s)"
        % (_f(i_pump * 1000.0, 0, "mA"), _f(if_a, 1, "A"),
           _f(vrrm, 0, "V"), _f(vbat_max, 1, "V")),
        "I_pump <= 0,5 A und VRRM >= 4 x VBAT_max (8,4 V)",
        "1N5819WS-Datenblatt: 1 A / 40 V; Stromreserve und Spannungsreserve "
        "fuer die Induktivitaet der Pumpe (Freilauf gegen +5V)")


def check_teilerstrom():
    """Ruhestrom beider Spannungsteiler (Waechter 1:2 + ADC 1:3,94)."""
    sys = circuit.load_system()
    r3a = circuit.parse_ohm(circuit.part("R3a")["value"])
    r3b = circuit.parse_ohm(circuit.part("R3b")["value"])
    r_top = circuit.parse_ohm(circuit.part("R_SENSE_TOP")["value"])
    r_bot = circuit.parse_ohm(circuit.part("R_SENSE_BOT")["value"])
    uvlo_ua = sys["pack_v_max"] / (r3a + r3b) * 1e6
    adc_ua = sys["pack_v_max"] / (r_top + r_bot) * 1e6
    total = uvlo_ua + adc_ua
    return CheckResult(
        "Teilerstrom", total <= 130.0,
        "Waechter %s + ADC %s = %s bei %s"
        % (_f(uvlo_ua, 1, "µA"), _f(adc_ua, 1, "µA"),
           _f(total, 1, "µA"), _f(sys["pack_v_max"], 1, "V")),
        "<= 130 µA (beide Teiler zusammen)",
        "Teiler duerfen im Standby-Budget (250 µA) nur ein Teilbudget "
        "verbrauchen; I = VBAT_max/(R_top+R_bot) je Teiler. Seit dem "
        "UV-Teiler-Fix 16.09.2026 (51 k/51 k) zieht der Waechterteiler ~82 µA "
        "statt 21 µA -- die Obergrenze ist entsprechend angehoben "
        "(Waechter + ADC = ~113 µA, schaltplan §3.2/§13.5)")


def check_uv_staffelung():
    """Die Unterspannungsschwellen muessen monoton fallen (Packspannung)."""
    sys = circuit.load_system()
    fw = 2.0 * sys["cell_firmware_stop_v"]
    trip = _uvlo_trip(sys)
    pcm = 2.0 * sys["cell_pcm_v"]
    return CheckResult(
        "Unterspannungsstaffelung", fw > trip > pcm,
        "Firmware %s > Waechter %s > PCM %s"
        % (_f(fw, 2, "V"), _f(trip, 2, "V"), _f(pcm, 1, "V")),
        "Firmware > TPS3839 (6,16 V) > PCM",
        "Firmware stoppt zuerst, dann Hardware, zuletzt die Zelle. "
        "1S-Schwellen aus bom §4b (3,4 V / 2,5 V) auf 2S = x2 gerechnet "
        "(Auftrag in schaltplan §4)")


def check_adc_filter():
    """RC-Zeitkonstanten der ADC-Kanaele (Feuchte, Pack, Reserve-Analog)."""
    r6 = circuit.parse_ohm(circuit.part("R6")["value"])
    c9 = circuit.parse_farad(circuit.part("C9")["value"])
    r_top = circuit.parse_ohm(circuit.part("R_SENSE_TOP")["value"])
    r_bot = circuit.parse_ohm(circuit.part("R_SENSE_BOT")["value"])
    c10 = circuit.parse_farad(circuit.part("C10")["value"])
    r_spare = circuit.parse_ohm(circuit.part("R_SPARE_AIN")["value"])
    c_spare = circuit.parse_farad(circuit.part("C_SPARE")["value"])
    t_sensor = r6 * c9
    r_par = 1.0 / (1.0 / r_top + 1.0 / r_bot)
    t_vbat = r_par * c10
    t_spare = r_spare * c_spare
    ok = t_sensor <= 5e-3 and t_vbat <= 50e-3 and t_spare <= 5e-3
    return CheckResult(
        "ADC-Filter", ok,
        "R6·C9 %s, (R_SENSE_TOP||BOT)·C10 %s, R_SPARE_AIN·C_SPARE %s"
        % (_f(t_sensor * 1000.0, 2, "ms"), _f(t_vbat * 1000.0, 1, "ms"),
           _f(t_spare * 1000.0, 2, "ms")),
        "R6·C9 <= 5 ms, (R_SENSE_TOP||BOT)·C10 <= 50 ms und "
        "R_SPARE_AIN·C_SPARE <= 5 ms",
        "Espressif-ADC: 0,1 µF Filter; Zeitkonstante begrenzt das Einschwingen "
        "(Packteiler jetzt R_SENSE_TOP/BOT statt R3a/R3b)")


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
    vbus = sys["supply_v"]
    i_stat = (circuit.rail_3v3() - vf_stat) / r4
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
        "I = (U - Vf)/R; D2 gruen Vf 2,85 V ueber R4 an +3V3, "
        "D_LEDCHG rot Vf 2,0 V ueber R_LEDCHG an VBUS 5 V")


def check_tank_led():
    """Tank-LED D5 mit Vorwiderstand R_TANK."""
    r_tank = circuit.parse_ohm(circuit.part("R_TANK")["value"])
    vf = led_vf("D5")                 # rote Tank-LED, C84256
    i = (circuit.rail_3v3() - vf) / r_tank
    return CheckResult(
        "Tank-LED", i <= 5e-3,
        "%s bei Vf %s (R_TANK %s)"
        % (_f(i * 1000.0, 2, "mA"), _f(vf, 1, "V"),
           _f(r_tank / 1000.0, 1, "kΩ")),
        "I <= 5 mA, Vf rot ca. 2,0 V",
        "LED-Vorwiderstand R_TANK an +3V3; D5 und D_LEDCHG sind die roten "
        "0805-LEDs (Vf 2,0 V), D2 ist die gruene")


def check_led_headroom():
    """Headroom am 3,3-V-Rail und nutzbares Stromfenster je LED."""
    rail = circuit.rail_3v3()
    vbus = circuit.load_system()["supply_v"]
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
        "3,3-V-Rail-Headroom (aus dem AP63203-Feedback) und Stromfenster je "
        "LED; Strom aus der jeweiligen Versorgung "
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
        "(J2/J7/J9-J13/J15); J8 = GND-VCC_EXT-SDA-SCL",
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
        "R_SPARE_IO15/16/17/21/23); J14 entfaellt")


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


def check_sensor_lastschalter():
    """Sensorversorgung ueber Q_SENS; IO3 treibt nur das Gate; kein GPIO an VCC.

    Neu 16.09.2026: SENSOR_PWR wird nicht mehr direkt von GPIO3 gespeist,
    sondern ueber einen P-Kanal-Lastschalter Q_SENS (AO3401A, gleicher Typ wie
    Q2).  Source an +3V3, Drain an SENSOR_PWR, Gate an EXT_SENS_EN;
    R_SENS_GATE (47 kOhm) zieht das Gate nach +3V3, damit der Schalter ohne
    Freigabe (Reset, hochohmiger GPIO) sicher aus ist.  Zusaetzlich darf kein
    GPIO direkt an einem Stecker-VCC (SENSOR_PWR/VCC_EXT) haengen.
    """
    q = _pins_of("Q_SENS")
    src_ok = q.get("2") == "+3V3"
    drain_ok = q.get("3") == "SENSOR_PWR"
    gate_ok = q.get("1") == "EXT_SENS_EN"
    r_gate = _nets_of("R_SENS_GATE")
    r_ok = set(r_gate) == {"+3V3", "EXT_SENS_EN"} and r_gate.get("+3V3") == "2"
    try:
        r_val = _ohms("R_SENS_GATE")
    except circuit.CircuitError:
        r_val = None
    val_ok = r_val is not None and abs(r_val - 47000.0) < 1.0
    io = None
    try:
        io, _ = _u1_io_on_net("EXT_SENS_EN")
    except circuit.CircuitError:
        io = None
    io_ok = io == 3
    pin6 = _pin_net("U1", "6")
    pin6_ok = pin6 == "EXT_SENS_EN"
    gpio_auf_vcc = []
    for vcc in ("SENSOR_PWR", "VCC_EXT"):
        for comp, pin in circuit.load_netlist().get(vcc, []):
            if comp == "U1":
                gpio_auf_vcc.append("U1.%s an %s" % (pin, vcc))
    ok = (src_ok and drain_ok and gate_ok and r_ok and val_ok
          and io_ok and pin6_ok and not gpio_auf_vcc)
    return CheckResult(
        "Sensor-Lastschalter", ok,
        "Q_SENS S->%s D->%s G->%s; R_SENS_GATE %s kΩ nach +3V3 %s; U1 Pin 6 "
        "auf %s, IO%d %s; GPIO direkt an VCC: %s"
        % (q.get("2"), q.get("3"), q.get("1"),
           _f((r_val or 0) / 1000.0, 0, ""), "OK" if r_ok else "FEHLER",
           pin6, io if io is not None else -1, "OK" if io_ok else "FEHLER",
           ", ".join(gpio_auf_vcc) or "keiner"),
        "Q_SENS Source +3V3, Drain SENSOR_PWR, Gate EXT_SENS_EN; R_SENS_GATE "
        "47 kΩ nach +3V3 (fail-safe aus); IO3 treibt nur das Gate; kein GPIO "
        "direkt an SENSOR_PWR/VCC_EXT",
        "Review 16.09.2026: die Sensorversorgung direkt aus GPIO3 ist fuer frei "
        "anschliessbare Module zu schwach; jetzt treibt IO3 (Pin 6) nur das "
        "Gate von Q_SENS (AO3401A, P-Kanal).  Der Pull-up haelt den Schalter "
        "bei hochohmigem GPIO aus (P-Kanal: V_GS = 0 sperrt), wie bei Q2")


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
                23: "SPARE_IO23"}
    zuord_ok = all(pin_net.get(EXT_IO_PIN[io], set()) == {net}
                   for io, net in expected.items())
    strap_ok = (pin_net.get(22) == {"GPIO8_STRAP"} and pin_net.get(23) == {"BOOT"})
    ok = not dupes and zuord_ok and strap_ok
    return CheckResult(
        "Erweiterungs-Pins", ok,
        "Doppelbelegung %s; Zuordnung %s; GPIO8/9 %s"
        % (", ".join("Pin %d" % p for p in dupes) or "keine",
           "OK" if zuord_ok else "FEHLER", "OK" if strap_ok else "FEHLER"),
        "kein U1-Pin doppelt, Erweiterungspins wie geplant (ohne J14/IO22), "
        "GPIO8/GPIO9 unveraendert auf ihren Strapping-Netzen",
        "Mengenpruefung der Netzliste gegen Pin-Doppelbelegung. IO22 ist seit "
        "15.09.2026 PUMP2_EN (J16), kein Reserve-Stecker mehr; IO15 waehlt nur "
        "die JTAG-Quelle (Default-eFuses = wirkungslos) und ist ueber einen "
        "1-kOhm-Serienwiderstand an J10 gefuehrt; IO16/IO17 bleiben UART0")


def check_i2c_pullups():
    """I2C-Pull-ups 4,7 kOhm an VCC_EXT (nicht +3V3); VCC_EXT ist geschaltet."""
    sda = _nets_of("R_SDA_PU")
    scl = _nets_of("R_SCL_PU")
    r_sda = circuit.parse_ohm(circuit.part("R_SDA_PU")["value"])
    r_scl = circuit.parse_ohm(circuit.part("R_SCL_PU")["value"])
    sda_ok = sda.get("SDA") == "1" and sda.get("VCC_EXT") == "2"
    scl_ok = scl.get("SCL") == "1" and scl.get("VCC_EXT") == "2"
    val_ok = abs(r_sda - 4700.0) < 1.0 and abs(r_scl - 4700.0) < 1.0
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
        "beide 4,7 kOhm, Pull-up-Seite VCC_EXT (nicht +3V3), VCC_EXT geschaltet",
        "Im ausgeschalteten Zustand zieht der Bus keinen Strom, weil die "
        "Pull-ups am geschalteten VCC_EXT haengen (schaltplan §9.5, "
        "Revision 15.09.2026: 4,7 kOhm). 4,7 kOhm sind fuer kurze Kabel und "
        "die ueblichen 100-kHz/400-kHz-I2C-Module plausibel")


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
        # 2S-Neu
        check_ladestrom_ip2326,
        check_ladeschluss_2s,
        check_ladeeingang_strom,
        check_buck5_ausgang,
        check_buck3_ausgang,
        check_buck5_induktivitaet,
        check_buck3_induktivitaet,
        check_uvlo_schwelle,
        check_uvlo_teiler,
        check_gate_pulldowns,
        check_adc_teiler_max,
        check_buck_en_pegel,
        check_waechter_abschaltung,
        check_kein_low_vin_am_vbat,
        check_standby_budget,
        check_system_quellen,
        # Akku-Schutz auf der Platine (neu 16.09.2026)
        check_schutz_serie,
        check_schutz_schwellen,
        check_schutz_ueberstrom,
        # Bestand, auf 2S gezogen
        check_gate_spannung,
        check_mosfet_verlust,
        check_freilaufdiode,
        check_teilerstrom,
        check_uv_staffelung,
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
        check_sensor_lastschalter,
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
