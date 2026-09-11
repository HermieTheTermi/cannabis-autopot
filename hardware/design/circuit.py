"""Schaltplan-Modell fuer den Smart Grow Topf V1.

Liest die Verbindungen aus ``schaltplan_v1_netzliste.csv`` und die Bauteilwerte
aus ``schaltplan_v1.md``. Zusaetzlich werden die Systemkenngroessen (Pumpe,
Akku, Modul, Lader) aus ``bom_entscheidung.md`` und ``schaltplan_v1.md``
gelesen, damit in den Pruefungen nichts hart verdrahtet werden muss.

Nur Standardbibliothek, Python 3.9-kompatibel.
"""
from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HARDWARE_DIR = BASE_DIR.parent
NETLIST_PATH = HARDWARE_DIR / "schaltplan_v1_netzliste.csv"
SCHEMATIC_PATH = HARDWARE_DIR / "schaltplan_v1.md"
BOM_DECISION_PATH = HARDWARE_DIR / "bom_entscheidung.md"

# Einpolige Elemente (Testpunkte), die nur auf einem Netz liegen duerfen.
ONE_PIN_OK_PREFIX = ("TP",)

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
            if not net or not comp:
                continue
            nets.setdefault(net, [])
            if (comp, pin) not in nets[net]:
                nets[net].append((comp, pin))
    if not nets:
        raise CircuitError("Netzliste enthaelt keine Netze: %s" % p)
    return nets


@lru_cache(maxsize=None)
def load_values(path=None):
    """Designator -> {'designator', 'value', 'lcsc'} aus schaltplan_v1.md."""
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
        lcsc_i = idx.get("lcsc")
        for row in rows:
            if pos_i >= len(row):
                continue
            pos_raw = _clean(row[pos_i])
            if not pos_raw:
                continue
            value = _clean(row[val_i]) if val_i is not None and val_i < len(row) else None
            lcsc = None
            if lcsc_i is not None and lcsc_i < len(row):
                lcsc = _clean(row[lcsc_i]) or None
            for des in re.split(r"\s*,\s*", pos_raw):
                des = des.strip()
                if not des:
                    continue
                entry = parts.setdefault(des, {"designator": des, "value": None, "lcsc": None})
                if value:
                    entry["value"] = value
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


def _grab(pattern, text, label):
    m = re.search(pattern, text)
    if not m:
        raise CircuitError("Kennwert '%s' nicht gefunden (Muster: %s)" % (label, pattern))
    return m.groups()


@lru_cache(maxsize=None)
def load_system():
    """Systemkenngroessen aus den Dokumenten (Pumpe, Akku, Modul, Lader)."""
    if not BOM_DECISION_PATH.exists():
        raise CircuitError("Datei fehlt: %s" % BOM_DECISION_PATH)
    bom = BOM_DECISION_PATH.read_text(encoding="utf-8")
    sch = SCHEMATIC_PATH.read_text(encoding="utf-8")
    vals = load_values()

    sys = {}

    (power,) = _grab(r"([0-9]+,[0-9]+)\s*W\s*\|\s*~[0-9]+\s*ml/min", bom, "Pumpenleistung")
    (flow,) = _grab(r"[0-9]+,[0-9]+\s*W\s*\|\s*~([0-9]+)\s*ml/min", bom, "Foerderrate")
    sys["pump_power_w"] = _to_float(power)
    sys["pump_flow_ml_min"] = _to_float(flow)

    (pump_v,) = _grab(r"@\s*([0-9]+[,.][0-9]+)\s*V", bom, "Pumpenspannung")
    sys["pump_voltage"] = _to_float(pump_v)

    (i3,) = _grab(r"3V\s*[\u2013-]\s*([0-9]+)\s*mA", bom, "Pumpenstrom 3 V")
    (i6,) = _grab(r"6V\s*[\u2013-]\s*([0-9]+)\s*mA", bom, "Pumpenstrom 6 V")
    sys["pump_current_3v_a"] = _to_float(i3) / 1000.0
    sys["pump_current_6v_a"] = _to_float(i6) / 1000.0
    # Betriebsstrom bei 3,7 V aus Leistung/Spannung (Datenblatt: 1,67 W @ 3,7 V)
    sys["pump_current_a"] = sys["pump_power_w"] / sys["pump_voltage"]

    (mah,) = _grab(r"~([0-9]+)\s*mAh", bom, "Zellkapazitaet")
    (batt_v,) = _grab(r"([0-9]+,[0-9]+)\s*V\s*~[0-9]+\s*mAh", bom, "Zellspannung")
    (wh,) = _grab(r"([0-9]+,[0-9]+)\s*Wh\s*nutzbar", bom, "nutzbare Energie")
    sys["battery_mah"] = _to_float(mah)
    sys["battery_voltage"] = _to_float(batt_v)
    sys["battery_usable_wh"] = _to_float(wh)

    (dose,) = _grab(r"Dosiervorgang von\s*([0-9]+)\s*ml", bom, "Dosismenge")
    (tx,) = _grab(r"([0-9]+)\s*mA\s*Peak", bom, "TX-Peak")
    (pwm,) = _grab(r"([0-9]+)\s*kHz\s*PWM", bom, "PWM-Frequenz")
    (fw,) = _grab(r"([0-9]+,[0-9]+)\s*V\s*Pumpstopp", bom, "Firmware-Pumpstopp")
    (pcm,) = _grab(r"Zelle\s*\|\s*~?\s*([0-9]+,[0-9]+)\s*V", bom, "PCM-Schwelle")
    sys["dose_ml"] = _to_float(dose)
    sys["tx_peak_ma"] = _to_float(tx)
    sys["pwm_hz"] = _to_float(pwm) * 1000.0
    sys["firmware_stop_v"] = _to_float(fw)
    sys["pcm_v"] = _to_float(pcm)

    (sleep,) = _grab(r"Modul-Deep-Sleep\s*([0-9]+)\s*\u00b5A", sch, "Modul-Schlafstrom")
    sys["module_sleep_ua"] = _to_float(sleep)
    (ldo_q,) = _grab(r"LDO\s*([0-9]+)\s*\u00b5A", sch, "LDO-Ruhestrom")
    sys["ldo_quiescent_ua"] = _to_float(ldo_q)
    (m809_q,) = _grab(r"MAX809\s*([0-9]+)\s*\u00b5A", sch, "MAX809-Ruhestrom")
    sys["max809_quiescent_ua"] = _to_float(m809_q)
    (div,) = _grab(r"Spannungsteiler\s*([0-9]+,[0-9]+)\s*\u00b5A", sch, "Teilerstrom")
    sys["divider_current_ua"] = _to_float(div)

    u4 = vals.get("U4", {}).get("value") or ""
    u3 = vals.get("U3", {}).get("value") or ""
    u7 = vals.get("U7", {}).get("value") or ""
    if not u4 or not u3 or not u7:
        raise CircuitError("U3/U4/U7 fehlen in schaltplan_v1.md")
    sys["ldo_current_a"] = parse_ampere(u4)
    sys["rail_3v3"] = parse_volt(u4)
    sys["charge_voltage"] = parse_volt(u3)
    sys["max809_v"] = parse_volt(u7)

    d1 = vals.get("D1", {}).get("value") or ""
    if not d1:
        raise CircuitError("D1 fehlt in schaltplan_v1.md")
    sys["diode_vrrm"] = parse_volt(d1)
    sys["diode_if_a"] = parse_ampere(d1)

    return sys


if __name__ == "__main__":
    print("Netze:     %d" % len(load_netlist()))
    print("Bauteile:  %d" % len(load_values()))
    for key, value in sorted(load_system().items()):
        print("  %-24s %s" % (key, value))
