"""Schaltplan-Modell fuer den Smart Grow Topf V1 (Stand 2S-Umbau, 16.09.2026).

Liest die Verbindungen aus ``schaltplan_v1_netzliste.csv`` und die Bauteilwerte
aus ``schaltplan_v1.md``.  Bauteilwerte kommen ausschliesslich ueber
:func:`part` aus den Tabellen §3.1-§3.4.  Systemkenngroessen (Pumpe, Pack,
Modul, ADC) stehen in dem klar markierten :data:`SYSTEM`-Block; jede Zahl
traegt eine woertliche Belegstelle, die :func:`check_system_quellen` in
``checks.py`` gegen die Dokumente prueft.

Nur Standardbibliothek, Python 3.9-kompatibel.
"""
from __future__ import annotations

import csv
import re
from collections import namedtuple
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HARDWARE_DIR = BASE_DIR.parent
NETLIST_PATH = HARDWARE_DIR / "schaltplan_v1_netzliste.csv"
SCHEMATIC_PATH = HARDWARE_DIR / "schaltplan_v1.md"
BOM_PATH = HARDWARE_DIR / "pcba_bom_jlc.csv"
BOM_DECISION_PATH = HARDWARE_DIR / "bom_entscheidung.md"

# Einpolige Elemente (Testpunkte), die nur auf einem Netz liegen duerfen.
ONE_PIN_OK_PREFIX = ("TP",)

# ---------------------------------------------------------------------------
# DATENBLATTGRENZEN, die das Modell selbst braucht (jede mit Quelle).
# ---------------------------------------------------------------------------
VREF_BUCK5 = 0.6   # SY8113B (Silergy) Datenblatt AN_SY8113B S.1/S.2: V_REF 0,6 V
# AP63203 (Diodes) ist die FESTSPANNUNGSVERSION (AP63203 = 3,3 V, AP63205 = 5 V,
# Datenblatt DS41326 Fig. 21: FB direkt auf den Ausgang).  Der frueher hier
# gerechnete Teiler R_FB3_TOP/R_FB3_BOT existiert seit dem Review 16.09.2026
# nicht mehr -- V_OUT wird nicht mehr aus Widerstaenden, sondern als
# Datenblatt-Festwert angenommen (3,27/3,30/3,33 V).
VOUT_BUCK3_FIXED = 3.30

# ---------------------------------------------------------------------------
# SYSTEM - Systemkenngroessen aus den Projektdokumenten.
#
# Jeder Eintrag traegt seinen Wert, die Einheit, die Datei und ein woertliches
# Textfragment (Beleg).  check_system_quellen() weist nach, dass der Beleg
# wirklich in der Datei steht.  Das Dokument ist die einzige Quelle dieser
# Zahlen; im uebrigen Code sind sie ausschliesslich an dieser Stelle erlaubt.
# ---------------------------------------------------------------------------
SystemEntry = namedtuple("SystemEntry", "key wert einheit datei beleg")

SYSTEM = (
    # Pack (2S)
    SystemEntry("pack_v_min", 6.0, "V", "schaltplan_v1.md", "6,0\u20138,4 V"),
    SystemEntry("pack_v_max", 8.4, "V", "schaltplan_v1.md", "8,4 V"),
    SystemEntry("pack_capacity_mah", 2000.0, "mAh", "bom_entscheidung.md", "2000 mAh"),
    SystemEntry("cell_v_nom", 3.7, "V", "bom_entscheidung.md", "3,7 V"),
    SystemEntry("cell_firmware_stop_v", 3.4, "V", "bom_entscheidung.md", "3,4 V Pumpstopp"),
    SystemEntry("cell_pcm_v", 2.5, "V", "bom_entscheidung.md", "2,5 V"),
    # Pumpen
    SystemEntry("pump_v", 5.0, "V", "bom_entscheidung.md", "DC 5 V"),
    SystemEntry("pump_i_nom_a", 0.4, "A", "bom_entscheidung.md", "0,4 A"),
    SystemEntry("pump_i_inrush_a", 3.0, "A", "bom_entscheidung.md", "Anlaufstrom 3 A"),
    SystemEntry("o2_pump_i_a", 0.2, "A", "bom_entscheidung.md", "0,20 A"),
    SystemEntry("pump_flow_ml_min", 150.0, "ml/min", "bom_entscheidung.md", "150 ml/min"),
    SystemEntry("dose_ml", 300.0, "ml", "bom_entscheidung.md", "300 ml"),
    SystemEntry("pwm_hz", 20000.0, "Hz", "bom_entscheidung.md", "20 kHz"),
    # Modul (ESP32-C6-MINI-1)
    SystemEntry("module_tx_peak_ma", 382.0, "mA", "schaltplan_v1.md", "382 mA"),
    SystemEntry("module_sleep_ua", 7.0, "\u00b5A", "schaltplan_v1.md", "7 \u00b5A"),
    # Ruhestrom der Bausteine (aus den Datenblaettern, im Dokument belegt)
    SystemEntry("iq_buck5_ua", 100.0, "\u00b5A", "schaltplan_v1.md", "100 \u00b5A"),
    SystemEntry("iq_buck3_ua", 22.0, "\u00b5A", "schaltplan_v1.md", "22 \u00b5A"),
    SystemEntry("iq_watchdog_ua", 0.15, "\u00b5A", "schaltplan_v1.md", "0,15 \u00b5A"),
    # Netzteilannahme
    SystemEntry("supply_v", 5.0, "V", "schaltplan_v1.md", "USB-C 5 V"),
    SystemEntry("supply_i_a", 2.5, "A", "schaltplan_v1.md", "\u2265 2,5 A"),
    # ADC (Espressif ESP32-C6, ADC_ATTEN_DB_12)
    SystemEntry("adc_vref_mv", 3300.0, "mV", "schaltplan_v1.md", "3300 mV"),
    SystemEntry("adc_bits", 12.0, "", "schaltplan_v1.md", "12 Bit"),
)

# ---------------------------------------------------------------------------
# ANNAHMEN - bewusst keine Datenblattwerte, sondern Modellannahmen.  Sie sind
# hier zentral dokumentiert und werden in der Ausgabe als Annahme genannt.
# ---------------------------------------------------------------------------
ASSUMPTIONS = {
    "r_bat_ohm": 0.15,        # Innenwiderstand eines 2S-Rundzellenpacks, typ. 2 x 60-100 mOhm
    "cc_frac": 0.8,           # Anteil der Ladung in der CC-Phase (Rest CV)
    "cv_i_frac": 0.4,         # mittlerer Ladestrom in der CV-Phase, bezogen auf ICHG
    "usable_frac": 0.8,       # nutzbarer Anteil der Packkapazitaet
    "en_input_leak_ua": 1.0,  # EN-Eingangsleckstrom des SY8113B, konservativ (Datenblatt nennt keinen Einzelwert)
}

# Datenblatt-Fakten zum Lichtsensor ALS-PT19-315C/L177/TR8 (LCSC C146233).
# Der Sensor haengt extern an J7 und ist KEINE BOM-/PCBA-Position.
LIGHT_SENS_LUX_REF = 100.0        # Bezugsbeleuchtungsstaerke des Datenblatts
LIGHT_SENS_UA_REF = 15.0          # Kollektorstrom typisch bei 100 lx [µA]
LIGHT_SENS_DARK_UA = 0.1          # ICEO max. im Dunkeln [µA]
LIGHT_GROW_LUX = 10000.0          # typische LED-Growlampe am Canopy [lx]
ADC_VREF_MV_ATTEN12 = 3300.0      # ADC_ATTEN_DB_12 (ATTEN3): 0..3300 mV
ADC_COUNTS_12BIT = 4095.0         # 12-Bit-Vollausschlag
LIGHT_DARK_COUNTS = 200.0         # absoluter Notwert "dunkel" [ADC-Counts]
LIGHT_BRIGHT_COUNTS = 3000.0      # absoluter Notwert "hell" [ADC-Counts]
LIGHT_HYSTERESE_COUNTS = 300.0    # Mindestabstand dunkel/hell [ADC-Counts]

# SI-Praefixe in Basiseinheiten.
_SI_PREFIX = {
    "p": 1e-12,
    "n": 1e-9,
    "µ": 1e-6,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
    "K": 1e3,
    "M": 1e6,
    "G": 1e9,
}

_NUM = r"([0-9]+(?:[.,][0-9]+)?)"
_PFX = r"([pnu\u00b5mMkKG]?)"


class CircuitError(Exception):
    """Fehler beim Laden oder Auswerten der Schaltplandaten."""


def _clean(text):
    """Entfernt Markdown-Zeichen und Leerraum aus einer Tabellenzelle."""
    return str(text).replace("`", "").replace("*", "").replace("~", "").strip()


def _to_float(text):
    """Wandelt '4,7' oder '4.7' in float um."""
    s = str(text).strip().replace(" ", "")
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    elif "," in s and "." in s:
        s = s.replace(",", "")
    return float(s)


def _strip_multiplier(text):
    """Entfernt einen Mengen-Vorspann wie '2 × ' vor dem eigentlichen Wert."""
    return re.sub(r"^\s*[0-9]+\s*[\u00d7xX]\s*", "", text)


def _si(value):
    """Normalisiert auf 12 signifikante Stellen (vermeidet 1e-07-Ungenauigkeit)."""
    return float("%.12g" % value)


def _parse_unit(text, unit_pattern, fallback=False):
    """Liest die erste Zahl mit SI-Praefix vor einer Einheit in Basiseinheiten."""
    s = _strip_multiplier(_clean(text))
    m = re.search(_NUM + r"\s*" + _PFX + r"\s*(?:" + unit_pattern + r")", s)
    if m is None and fallback:
        m = re.search(_NUM + r"\s*" + _PFX, s)
    if m is None:
        raise CircuitError("keine Zahl mit Einheit '%s' in %r" % (unit_pattern, text))
    return _si(_to_float(m.group(1)) * _SI_PREFIX.get(m.group(2), 1.0))


def parse_ohm(text):
    """Widerstand in Ohm. Beispiele: '4,7 kΩ' -> 4700.0, '499 Ω', '200k'."""
    return _parse_unit(text, r"\u03a9|ohm|Ohm|R\b", fallback=True)


def parse_farad(text):
    """Kapazitaet in Farad. Beispiele: '100 nF' -> 1e-07, '4.7uF' -> 4.7e-06."""
    return _parse_unit(text, r"F\b|Farad|farad", fallback=True)


def parse_henry(text):
    """Induktivitaet in Henry. Beispiele: '4,7 µH' -> 4.7e-06, '2,2 µH'."""
    return _parse_unit(text, r"H\b|Henry|henry")


def parse_ampere(text):
    """Strom in Ampere. Beispiele: '500 mA', '40 µA'."""
    return _parse_unit(text, r"A\b")


def parse_volt(text):
    """Spannung in Volt. Beispiele: '4,20 V', '3,3 V'."""
    return _parse_unit(text, r"V\b")


def parse_second(text):
    """Zeit in Sekunden. Beispiele: '1 ms', '50 µs'."""
    return _parse_unit(text, r"s\b")


def parse_hertz(text):
    """Frequenz in Hertz. Beispiel: '20 kHz'."""
    return _parse_unit(text, r"Hz")


def _iter_md_tables(text):
    """Liefert (headers, rows) fuer jede Markdown-Tabelle im Text."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        head = lines[i].strip()
        sep = lines[i + 1].strip()
        if head.startswith("|") and head.endswith("|") and re.fullmatch(r"\|[\s:\-|]+", sep):
            headers = [c.strip() for c in head.strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            yield headers, rows
            i = j
        else:
            i += 1


@lru_cache(maxsize=None)
def load_netlist(path=None):
    """Netz -> Liste von (Bauteil, Pin)."""
    p = Path(path) if path else NETLIST_PATH
    if not p.exists():
        raise CircuitError("Netzliste fehlt: %s" % p)
    nets = {}
    with p.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        try:
            next(reader)
        except StopIteration:
            raise CircuitError("Netzliste ist leer: %s" % p)
        for row in reader:
            if len(row) < 3:
                continue
            net, comp, pin = row[0].strip(), row[1].strip(), row[2].strip()
            if not net or net.startswith("#") or not comp:
                continue
            nets.setdefault(net, [])
            if (comp, pin) not in nets[net]:
                nets[net].append((comp, pin))
    if not nets:
        raise CircuitError("Netzliste enthaelt keine Netze: %s" % p)
    return nets


@lru_cache(maxsize=None)
def load_values(path=None):
    """Designator -> {'designator', 'value', 'desc', 'lcsc'} aus schaltplan_v1.md.

    Die Tabellen §3.1-§3.4 haben unterschiedliche Spaltenkoepfe.  Gelesen wird
    die Spalte "Wert", sofern vorhanden, zusaetzlich die Spalte "Bauteil" als
    Beschreibung (dort steht z. B. bei Induktivitaeten der Wert '4,7 µH').
    """
    p = Path(path) if path else SCHEMATIC_PATH
    if not p.exists():
        raise CircuitError("Bauteildatei fehlt: %s" % p)
    text = p.read_text(encoding="utf-8")
    parts = {}
    for headers, rows in _iter_md_tables(text):
        idx = {h.lower(): k for k, h in enumerate(headers)}
        if "pos" not in idx:
            continue
        pos_i = idx["pos"]
        val_i = idx.get("wert")
        desc_i = idx.get("bauteil")
        lcsc_i = idx.get("lcsc")
        for row in rows:
            if pos_i >= len(row):
                continue
            pos_raw = _clean(row[pos_i])
            if not pos_raw:
                continue
            value = _clean(row[val_i]) if val_i is not None and val_i < len(row) else None
            desc = _clean(row[desc_i]) if desc_i is not None and desc_i < len(row) else None
            lcsc = None
            if lcsc_i is not None and lcsc_i < len(row):
                lcsc = _clean(row[lcsc_i]) or None
            for des in re.split(r"\s*,\s*", pos_raw):
                des = des.strip()
                if not des:
                    continue
                entry = parts.setdefault(
                    des, {"designator": des, "value": None, "desc": None, "lcsc": None})
                if value:
                    entry["value"] = value
                if desc:
                    entry["desc"] = desc
                if lcsc:
                    entry["lcsc"] = lcsc
    if not parts:
        raise CircuitError("keine Bauteilwerte in %s gefunden" % p)
    return parts


def part(designator):
    """Liefert den Werteeintrag eines Bauteils oder raist CircuitError."""
    values = load_values()
    if designator not in values:
        raise CircuitError("Bauteil nicht in schaltplan_v1.md: %s" % designator)
    return dict(values[designator])


def parts():
    """Sortierte Liste aller bekannten Designatoren."""
    return sorted(load_values())


def nets():
    """Sortierte Liste aller Netznamen."""
    return sorted(load_netlist())


def net_of(designator, pin):
    """Name des Netzes, auf dem (designator, pin) liegt, sonst CircuitError."""
    for net, nodes in load_netlist().items():
        for comp, p in nodes:
            if comp == designator and p == pin:
                return net
    raise CircuitError("Pin nicht gefunden: %s Pin %s" % (designator, pin))


def parts_on(net):
    """Liste aller (Bauteil, Pin) auf einem Netz, sonst CircuitError."""
    netlist = load_netlist()
    if net not in netlist:
        raise CircuitError("Netz nicht in der Netzliste: %s" % net)
    return list(netlist[net])


def ratio(designator):
    """R_top/R_bot eines Teilerpaares, z. B. ratio('R_FB5_TOP').

    Der Designator muss auf 'TOP' enden; der Partner ergibt sich durch 'BOT'.
    Fehlt einer der beiden Werte, bricht die Funktion mit CircuitError ab.
    """
    if not designator.endswith("TOP"):
        raise CircuitError("ratio erwartet einen Designator auf '...TOP': %s" % designator)
    bot = designator[:-3] + "BOT"
    r_top = parse_ohm(part(designator)["value"])
    r_bot = parse_ohm(part(bot)["value"])
    if r_bot == 0:
        raise CircuitError("R_bot ist 0 Ohm: %s" % bot)
    return r_top / r_bot


def rail_5v():
    """5-V-Schiene aus dem SY8113B-Feedbackteiler (V_REF 0,6 V)."""
    return VREF_BUCK5 * (1.0 + ratio("R_FB5_TOP"))


def rail_3v3():
    """3,3-V-Schiene des AP63203 in der Festspannungsversion.

    FB (Pin 1) liegt laut Netzliste direkt auf +3V3, es gibt keinen
    Rueckkopplungsteiler.  Der Wert ist der Datenblatt-Festwert (3,30 V).
    """
    return VOUT_BUCK3_FIXED


def system_quellen():
    """Liefert die SYSTEM-Eintraege fuer check_system_quellen."""
    return tuple(SYSTEM)


@lru_cache(maxsize=None)
def load_system():
    """Systemkenngroessen als dict {key: wert} aus dem SYSTEM-Block."""
    return {entry.key: entry.wert for entry in SYSTEM}


if __name__ == "__main__":
    print("Netze:     %d" % len(load_netlist()))
    print("Bauteile:  %d" % len(load_values()))
    print("Rails:     +5V %.3f V, +3V3 %.3f V" % (rail_5v(), rail_3v3()))
    for key, value in sorted(load_system().items()):
        print("  %-24s %s" % (key, value))
