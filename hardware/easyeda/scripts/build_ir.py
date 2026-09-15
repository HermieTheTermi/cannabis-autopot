#!/usr/bin/env python3
"""SmartGrowTopf_V1 — S0/S1-Datenschicht.

Baut aus der Netzliste (hardware/schaltplan_v1_netzliste.csv) und den am lebenden
EasyEDA-Symbol gemessenen Pin-Tabellen die kanonische Connectivity-IR (schemaVersion 1.4)
für den easyeda CLI-Designflow S0-S6.

Quellen (unveraendert gelesen):
  - hardware/schaltplan_v1_netzliste.csv   (Netz, Bauteil, Pin, Bemerkung)
  - hardware/pcba_bom_jlc.csv              (Werte, LCSC-Codes)
  - raw/lib_by_lcsc.json                   (Device-Identitaet, per easyeda lib by-lcsc)
  - raw/probe*.json                        (echte Pin-Tabellen aus easyeda sch list --include-pins)

Aufruf:
  python3 scripts/build_ir.py            -> raw/ir_draft.json, raw/ir_numbered.json,
                                            raw/no_place.json, raw/ir_report.txt

Die Designator-Nummerierung (S2, `sch designators allocate`) ist hier als reine
Datei-Transformation nachgebildet: `raw/designator_changes.json` bildet funktionale
Namen (R_LIGHT, C_BTN, ...) auf numerische Refdes ab. So laufen die nachfolgenden
Generatoren (plan_layout, build_autoconnect) ohne Live-Aufruf der easyeda-CLI.
"""
import csv
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # hardware/easyeda
REPO = os.path.dirname(os.path.dirname(ROOT))  # repo root
RAW = os.path.join(ROOT, 'raw')

# --- Bauteile: Originalbezeichnung -> (LCSC, Modul, Rolle/Beschreibung) -------
# Die Originalbezeichnungen sind die funktionalen Namen aus dem Projekt (R_EN, C_BTN, ...).
# Nicht-nummerierte Namen sind laut Design-Flow S2 ungueltige Refdes -> sie werden per
# `sch designators allocate` auf offizielle Library-Praefixe umbenannt; der funktionale
# Name wandert in `role`.
COMPS = [
    # --- Stromversorgung / Lader ---
    ("U3", "C424093", "LADER", "1S-LiPo-Lader 4,20 V"),
    ("U4", "C82942", "LDO", "LDO 3,3 V / 500 mA"),
    ("U7", "C16711", "WAEChTER", "Unterspannungswaechter 3,08 V"),
    ("U1", "C5736265", "MCU", "ESP32-C6-MINI-1 WLAN-Modul"),
    ("U6", "C7519", "USB", "USB-ESD-Schutz USBLC6-2SC6"),
    ("Q1", "C20917", "PUMPE", "N-MOSFET Pumpentreiber"),
    ("D1", "C191023", "PUMPE", "Freilaufdiode Pumpe"),
    ("D3", "C191023", "PUMPE", "Klemmzweig Gate"),
    ("D2", "C2297", "MCU", "Status-LED gruen 525 nm"),
    ("D5", "C84256", "MCU", "Tank-leer-LED rot"),
    ("D_LEDCHG", "C84256", "LADER", "Ladestatus-LED rot"),
    ("C1a", "C49678", "MCU", "Decoupling Modul 100 nF"),
    ("C1b", "C49678", "MCU", "Decoupling Modul 100 nF"),
    ("C2", "C45783", "MCU", "Bulk 22 uF am Modul-3V3"),
    ("C3", "C970684", "AKKU", "Elko 100 uF Pumpenpuffer"),
    ("C4", "C15849", "MCU", "EN-RC 1 uF"),
    ("C5", "C15850", "LDO", "LDO-Eingang 10 uF"),
    ("C6", "C15849", "LDO", "LDO-Ausgang 1 uF"),
    ("C7", "C1779", "LADER", "Lader-Eingang 4,7 uF"),
    ("C8", "C1779", "LADER", "Lader-Ausgang 4,7 uF"),
    ("C9", "C49678", "MCU", "ADC-Filter Sensor 100 nF"),
    ("C10", "C49678", "MCU", "ADC-Filter VBAT 100 nF"),
    ("C11", "C49678", "PUMPE", "EMI an Pumpenklemmen 100 nF"),
    ("C12", "C49678", "WAEChTER", "Decoupling MAX809 100 nF"),
    ("C_BTN", "C49678", "TASTER", "Taster-Entprellung 100 nF"),
    ("R1", "C17673", "PUMPE", "Gate-Serie 4,7 k"),
    ("R2", "C17713", "PUMPE", "Gate-Pulldown 47 k"),
    ("R3a", "C17539", "WAEChTER", "VBAT-Teiler oben 200 k"),
    ("R3b", "C17539", "WAEChTER", "VBAT-Teiler unten 200 k"),
    ("R4", "C17557", "MCU", "Status-LED 220 R"),
    ("R5a", "C27834", "USB", "CC1-Pulldown 5,1 k"),
    ("R5b", "C27834", "USB", "CC2-Pulldown 5,1 k"),
    ("R6", "C17513", "SENSOR", "Sensor-AOUT Serie 1 k"),
    ("R_EN", "C17414", "MCU", "EN-Pull-up 10 k"),
    ("R_BOOT", "C17414", "MCU", "GPIO9-Pull-up 10 k"),
    ("R_GPIO8", "C17414", "MCU", "GPIO8-Strap-Pull-up 10 k"),
    ("R_BTN", "C17414", "TASTER", "Taster-Pull-up 10 k"),
    ("R_PROG", "C17614", "LADER", "Ladestrom 3,9 k -> 256 mA"),
    ("R_LEDCHG", "C17513", "LADER", "Lade-LED 1 k"),
    ("R_TANK", "C17513", "MCU", "Tank-LED 1 k"),
    ("R_UART", "C17722", "DEBUG", "TXD0-Serie 499 R (DNP)"),
    ("J1", "C160352", "AKKU", "Akku JST-PH 2P aufrecht (Top-Entry)"),
    ("J2", "C493416", "SENSOR", "Sensor JST-XH 3P aufrecht (Top-Entry)"),
    ("J4", "C158012", "PUMPE", "Dosierpumpe JST-XH 2P aufrecht (Top-Entry)"),
    ("J_PUMP2", "C158012", "PUMPE2", "Sauerstoffpumpe JST-XH 2P aufrecht"),
    # --- Boost 5 V (15.09.2026): VBAT -> +5 V fuer BEIDE Pumpen ---
    ("U_BOOST", "C84817", "BOOST", "MT3608 Aufwaertsregler 5 V"),
    ("L_BOOST", "C341068", "BOOST", "Boost-Induktivitaet 22 uH YNR6045"),
    ("D_BOOST", "C8678", "BOOST", "Boost-Diode SS34 3A/40V"),
    ("C_BST_IN", "C45783", "BOOST", "Boost-Eingang 22 uF"),
    ("C_BST_OUT", "C45783", "BOOST", "Boost-Ausgang 22 uF"),
    ("C_BST_HF", "C49678", "BOOST", "Boost-Ausgang HF 100 nF"),
    ("R_FB_TOP", "C17819", "BOOST", "Feedback oben 75 k -> 5,10 V"),
    ("R_FB_BOT", "C17414", "BOOST", "Feedback unten 10 k"),
    # --- zweiter Pumpenpfad: Sauerstoffpumpe (15.09.2026) ---
    ("Q_PUMP2", "C20917", "PUMPE2", "N-MOSFET Sauerstoffpumpe"),
    ("R_GATE2", "C17673", "PUMPE2", "Gate-Serie 4,7 k"),
    ("R_GATE2_PD", "C17713", "PUMPE2", "Gate-Pulldown 47 k"),
    ("D_FLY2", "C191023", "PUMPE2", "Freilaufdiode Sauerstoffpumpe"),
    ("D_CLAMP2", "C191023", "PUMPE2", "Klemmzweig Gate Sauerstoffpumpe"),
    ("C_PUMP2_EMI", "C49678", "PUMPE2", "EMI an den Klemmen Sauerstoffpumpe 100 nF"),
    ("J5", "C165948", "USB", "USB-C 16P Buchse"),
    ("SW1", "C318884", "MCU", "Reset-Taster"),
    ("SW2", "C318884", "MCU", "Boot-Taster"),
    ("J6", "NO_LCSC_J6", "TASTER", "2 Loetpads externer Taster"),
    ("TP1", "NO_LCSC_TP", "DEBUG", "Testpad TXD0"),
    ("TP2", "NO_LCSC_TP", "MCU", "Testpad RXD0"),
    ("TP3", "NO_LCSC_TP", "AKKU", "Testpad GND"),
    ("TP4", "NO_LCSC_TP", "AKKU", "Testpad VBAT"),
    ("TP5", "NO_LCSC_TP", "LDO", "Testpad +3V3"),
    ("TP6", "NO_LCSC_TP", "SENSOR", "Testpad SENSOR_AOUT"),
    # --- Lichtsensor (13.09.2026); J7 seit 14.09.2026 Stiftleiste statt JST-XH ---
    ("J7", "C2937625", "LICHT", "Lichtsensor Stiftleiste 1x3 2.54 mm (extern)"),
    ("R_LIGHT", "C17414", "LICHT", "Licht-Lastwiderstand 10 k nach GND"),
    ("R_LIGHT_S", "C17513", "LICHT", "Licht-Serienschutz 1 k zum ADC"),
    ("C_LIGHT", "C49678", "LICHT", "ADC-Filter Licht 100 nF"),
    # --- Erweiterung (14.09.2026): freie GPIOs + I2C auf 2,54-mm-Stiftleisten ---
    ("J8", "C2691448", "ERWEITERUNG", "I2C Stiftleiste 1x4 (GND-VCC-SDA-SCL)"),
    ("J9", "C2937625", "ERWEITERUNG", "Reserve-Analog Stiftleiste 1x3 (IO5)"),
    ("J10", "C2937625", "ERWEITERUNG", "Reserve IO15 Stiftleiste 1x3"),
    ("J11", "C2937625", "ERWEITERUNG", "Reserve IO16 (TXD0) Stiftleiste 1x3"),
    ("J12", "C2937625", "ERWEITERUNG", "Reserve IO17 (RXD0) Stiftleiste 1x3"),
    ("J13", "C2937625", "ERWEITERUNG", "Reserve IO21 Stiftleiste 1x3"),
    ("J15", "C2937625", "ERWEITERUNG", "Reserve IO23 Stiftleiste 1x3"),
    ("Q2", "C15127", "ERWEITERUNG", "P-Kanal-Load-Switch VCC_EXT"),
    ("R_GATE", "C17713", "ERWEITERUNG", "Gate-Pull-up Load-Switch 47 k"),
    ("R_SDA_PU", "C17414", "ERWEITERUNG", "I2C SDA Pull-up 10 k an VCC_EXT"),
    ("R_SCL_PU", "C17414", "ERWEITERUNG", "I2C SCL Pull-up 10 k an VCC_EXT"),
    ("R_SDA_S", "C17513", "ERWEITERUNG", "I2C SDA Serienschutz 1 k"),
    ("R_SCL_S", "C17513", "ERWEITERUNG", "I2C SCL Serienschutz 1 k"),
    ("R_SPARE_AIN", "C17513", "ERWEITERUNG", "Reserve-AIN Serienschutz 1 k"),
    ("R_SPARE_IO15", "C17513", "ERWEITERUNG", "Reserve IO15 Serienschutz 1 k"),
    ("R_SPARE_IO16", "C17513", "ERWEITERUNG", "Reserve IO16 Serienschutz 1 k"),
    ("R_SPARE_IO17", "C17513", "ERWEITERUNG", "Reserve IO17 Serienschutz 1 k"),
    ("R_SPARE_IO21", "C17513", "ERWEITERUNG", "Reserve IO21 Serienschutz 1 k"),
    ("R_SPARE_IO23", "C17513", "ERWEITERUNG", "Reserve IO23 Serienschutz 1 k"),
    ("C_SPARE", "C49678", "ERWEITERUNG", "ADC-Filter Reserve-Analog 100 nF"),
]

# Loetpads/Bohrungen ohne Bestueckungsplatz (Sonderfall): sie stehen in der IR und
# werden geprueft, aber weder platziert noch verdrahtet. TP1-TP6 und J6 liegen als
# echte Loetpads/Bohrungen auf der Platine und werden platziert und verdrahtet.
# Die Ausnahmeliste bleibt fuer kuenftige Sonderfaelle bestehen.
NO_PLACE = set()

# Bauteile ohne LCSC-Code (keine JLC-Bestueckung): ueber eigene Geraete abgedeckt.
EXTRA_DEVICES = {
    # HDR-TH 2P 2,54 mm als Symbol fuer die zwei Loetbohrungen J6 (keine BOM-Position)
    "NO_LCSC_J6": ("0819f05c4eef4c71ace90d822a990e87", "72b9be21f4ad4d53a42178e79731ea2a", "HDR-TH 2P, 2,54 mm"),
    # 5010-Testpad TH (Messspitze)
    "NO_LCSC_TP": ("0819f05c4eef4c71ace90d822a990e87", "1d9ad61565194f66a2bb1c832c938c3d", "5010-Testpoint"),
}

# Neue Bibliotheksteile der Erweiterung (14.09.2026). Die Device-Identitaeten wurden live mit
# `easyeda lib by-lcsc --lcsc C2937625,C2691448,C15127 --include-device-identity` in der
# Bibliothek 0819f05c4eef4c71ace90d822a990e87 aufgeloest (14.09.2026) und haben Vorrang.
# Die Pin-Tabellen sind fuer die Steckverbinder trivial (1..N) und fuer Q2 die Standard-
# SOT-23-Belegung des AO3401A (1=Gate, 2=Source, 3=Drain, wie AO3400A).
#
# Gemessenes Library-Praefix (property.designator):
#   C2937625 / C2691448 -> "H?" (Stiftleiste), C15127 -> "Q?".
# Der Auftrag will die Stecker als J8-J15 fuehren; das Projekt vergibt die funktionalen
# J-Designatoren bewusst selbst (wie schon J2/J7, deren JST-Geraet "CN?" als Praefix hat).
NEW_PARTS = {
    "C2937625": {
        "libraryUuid": "0819f05c4eef4c71ace90d822a990e87",
        "deviceUuid": "3c2517dd0d3741b3a6071ea8b3f9b7e9",   # XFCN PZ254V-11-03P (1x3 Stiftleiste)
        "name": "HDR-TH_3P-P2.54-V-M_PZ254V-11-03P",
        "pins": [{"number": str(i), "name": str(i)} for i in range(1, 4)],
    },
    "C2691448": {
        "libraryUuid": "0819f05c4eef4c71ace90d822a990e87",
        "deviceUuid": "f70eda5267b34d9799800488a27be0c6",   # XFCN PZ254V-11-04P (1x4 Stiftleiste)
        "name": "HDR-TH_4P-P2.54-V-M",
        "pins": [{"number": str(i), "name": str(i)} for i in range(1, 5)],
    },
    "C15127": {
        "libraryUuid": "0819f05c4eef4c71ace90d822a990e87",
        "deviceUuid": "f58385f66b144586baef3753ba84f65d",   # AOS AO3401A (P-Kanal SOT-23)
        "name": "AO3401A",
        "pins": [{"number": "1", "name": "G"}, {"number": "2", "name": "S"},
                 {"number": "3", "name": "D"}],
    },
}

# Netze: Name -> (scope, role)
NET_META = {
    "GND": ("global", "ground"),
    "VBAT": ("global", "power"),
    "+3V3": ("global", "power"),
    "+5V": ("global", "power"),
    "VBUS": ("global", "power"),
}

# --- Pin-Spezifikationen aus der Netzliste aufloesen --------------------------
# Sonderfaelle, die sich nicht rein numerisch aufloesen lassen (Pin-Namen des
# offiziellen Symbols statt Nummern).
NAME_SPECS = {
    # (Bauteil, Text) -> Liste von Pin-Namen (Praefix-Wildcard moeglich)
    ("J5", "VBUS (A4/A9/B4/B9)"): ["VBUS"],
    ("U1", "VDD33 (alle)"): [],
}

RANGE_RE = re.compile(r'^(\d+)\s*-\s*(\d+)$')


def load_pin_tables():
    """Echte Pin-Tabellen je Device-UUID aus den Live-Messungen (probe*.json)."""
    tables = {}
    for name in sorted(os.listdir(RAW)):
        if not name.startswith('probe') or not name.endswith('.json'):
            continue
        data = json.load(open(os.path.join(RAW, name)))
        for c in data['result']['components']:
            dev = c.get('device') or {}
            # --include-device-identity liefert die 32-stellige Device-Library-UUID in
            # device.libraryUuid; device.uuid bleibt die 16-stellige Instanz-ID.
            uuid = dev.get('libraryUuid')
            if not uuid or len(uuid) != 32 or not c.get('pins'):
                continue
            tables.setdefault(uuid, [
                {"number": p["pinNumber"], "name": p["pinName"]}
                for p in c["pins"]
            ])
    return tables


def resolve(spec, comp, pins):
    """Pin-Spezifikation -> Liste von Pin-Nummern des echten Symbols."""
    spec = spec.strip()
    numbers = {p['number'] for p in pins}
    by_name = {}
    for p in pins:
        by_name.setdefault(p['name'], []).append(p['number'])

    # 1) explizite Namensspezifikation
    if (comp, spec) in NAME_SPECS:
        out = []
        for want in NAME_SPECS[(comp, spec)]:
            hits = by_name.get(want, []) if not want.endswith('*') else [
                n for nm, nums in by_name.items() if nm.startswith(want[:-1]) for n in nums]
            if not hits:
                raise KeyError(f"{comp}: kein Pin mit Name {want!r}")
            out += hits
        return sorted(set(out))

    # 2) 'N Name' oder reine Zahl
    m = re.match(r'^(\d+)(?:\s+\S.*)?$', spec)
    if m:
        if m.group(1) not in numbers:
            raise KeyError(f"{comp}: Pin {m.group(1)} existiert nicht")
        return [m.group(1)]

    # 3) Aufzaehlung/Bereich, z. B. '1/2/11/14/36-53' (generisch; die U1-GND-Pins stehen
    #    in der Netzliste inzwischen einzeln, damit jeder Pin wirklich verdrahtet wird)
    if '/' in spec and '(' not in spec:
        out = []
        for part in spec.split('/'):
            part = part.strip()
            rng = RANGE_RE.match(part)
            if rng:
                lo, hi = int(rng.group(1)), int(rng.group(2))
                out += [str(n) for n in range(lo, hi + 1) if str(n) in numbers]
            elif part in numbers:
                out.append(part)
            else:
                raise KeyError(f"{comp}: Pin {part!r} existiert nicht")
        return sorted(set(out), key=lambda x: int(x) if x.isdigit() else 0)

    # 4) Text mit Klammer: 'D- (A7/B7)', 'GND (A1/A12/B1/B12) + Schirm', 'EPAD (Pin 49)'
    def add_name(nm):
        hits = [n for name, nums in by_name.items() if name == nm for n in nums]
        if not hits:
            raise KeyError(f"{comp}: kein Pin mit Name {nm!r}")
        return hits

    if spec.startswith('D- '):
        return sorted(set(add_name('DN1') + add_name('DN2')))
    if spec.startswith('D+ '):
        return sorted(set(add_name('DP1') + add_name('DP2')))
    if spec.startswith('GND '):
        out = add_name('GND')
        if 'Schirm' in spec:
            out += add_name('EH')
        return sorted(set(out))
    if spec.startswith('EPAD'):
        num = re.search(r'(\d+)', spec).group(1)
        if num not in numbers:
            raise KeyError(f"{comp}: Pin {num} existiert nicht")
        return [num]

    # 5) Funktionsnamen (Anode/Kathode/Gate/Drain/Source/+/-, CC1/CC2)
    alias = {
        'Anode': ['A', '+'],
        'Kathode': ['K', '-'],
        'Gate': ['G'],
        'Drain': ['D'],
        'Source': ['S'],
    }
    for key, names in alias.items():
        if spec.startswith(key):
            for nm in names:
                if nm in by_name:
                    return by_name[nm]
    # Elektrolyt-Kondensator ohne Polaritaets-Pin-Namen: + ist Pin 1, - ist Pin 2
    # (Polaritaet ist im Symbol nicht abgebildet, nur im Footprint).
    if comp == 'C3' and spec in ('+', '-'):
        return ['1'] if spec == '+' else ['2']
    if spec in ('A5 CC1', 'B5 CC2'):
        return [spec.split()[0]]
    raise KeyError(f"{comp}: Spezifikation {spec!r} nicht aufloesbar")


def main():
    tables = load_pin_tables()
    lcsc_map = json.load(open(os.path.join(RAW, 'lcsc_map.json')))

    comps, conns, problems = [], [], []
    notes = []
    by_name = {}
    for name, lcsc, module, desc in COMPS:
        if lcsc in EXTRA_DEVICES:
            lib, uuid, devname = EXTRA_DEVICES[lcsc]
            pins = tables.get(uuid)
        elif lcsc in NEW_PARTS:
            rec = NEW_PARTS[lcsc]
            lib, uuid, devname = rec['libraryUuid'], rec['deviceUuid'], rec['name']
            pins = [dict(p) for p in rec['pins']]
        else:
            rec = lcsc_map.get(lcsc)
            if not rec:
                problems.append(f"{name}: LCSC {lcsc} nicht aufgeloest")
                continue
            lib, uuid, devname = rec['libraryUuid'], rec['uuid'], rec.get('manufacturerId') or rec.get('value', '')
            pins = tables.get(uuid)
        if pins is None:
            problems.append(f"{name}: keine gemessene Pin-Tabelle fuer device {uuid}")
            continue
        comp = {
            "id": f"cmp-{name}",
            "ref": name,
            "role": f"{name} — {desc}",
            "device": {"libraryUuid": lib, "deviceUuid": uuid, "name": devname},
            "pins": [dict(p) for p in pins],
            "pageId": "4f6771a27edec75b",
            "_module": module,
            "_lcsc": lcsc,
            "_desc": desc,
        }
        comps.append(comp)
        by_name[name] = comp

    nets = {}
    with open(os.path.join(REPO, 'hardware', 'schaltplan_v1_netzliste.csv'), newline='', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            net, comp_ref, spec = row['Netz'].strip(), row['Bauteil'].strip(), row['Pin'].strip()
            # Kommentarzeilen (Netzname beginnt mit '#') sind reine Doku und werden nicht
            # als Verbindung aufgeloest. Ebenso Bemerkungs-Kommentare (z. B. U1 "EPAD (Pin 49)").
            if net.startswith('#') or row.get('Bemerkung', '').strip().startswith('#'):
                continue
            comp = by_name.get(comp_ref)
            if comp is None:
                problems.append(f"Netz {net}: unbekanntes Bauteil {comp_ref!r}")
                continue
            pins = comp['pins']
            try:
                nums = resolve(spec, comp_ref, pins)
            except KeyError as exc:
                problems.append(str(exc))
                continue
            if not nums:
                if (comp_ref, spec) in NAME_SPECS:
                    notes.append(f"{net}: {comp_ref} {spec!r} — das offizielle Symbol fuehrt keine "
                                 f"separaten VDD33-Pins (nur Pin 3 = 3V3); laut Datenblatt sind sie "
                                 f"modulintern verbunden, im Schaltplan daher nicht separat anschliessbar")
                else:
                    problems.append(f"Netz {net}: {comp_ref} {spec!r} -> keine Pins (Symbol hat diese Pins nicht)")
                continue
            nets.setdefault(net, [])
            for num in nums:
                key = (comp['id'], num)
                if any(c['componentId'] == comp['id'] and c['pinNumber'] == num for c in conns):
                    prev = next(c['netId'] for c in conns if c['componentId'] == comp['id'] and c['pinNumber'] == num)
                    if prev != net_id(net):
                        problems.append(f"{comp_ref}:{num} doppelt vergeben ({net})")
                    continue
                conns.append({"componentId": comp['id'], "pinNumber": num, "netId": net_id(net), "kind": "netlist"})

    # NC / unconnected: alles, was in keiner Verbindung steht
    connected = {(c['componentId'], c['pinNumber']) for c in conns}
    for comp in comps:
        for pin in comp['pins']:
            if (comp['id'], pin['number']) not in connected:
                pin['noConnected'] = True

    doc = {
        "schemaVersion": "1.4",
        "projectId": "51deea9fc24745be915d72e65813fa8b",
        "documentId": "4f6771a27edec75b",
        "components": [{k: v for k, v in c.items() if not k.startswith('_')} for c in comps],
        "nets": [{"id": net_id(n), "name": n,
                  "scope": NET_META.get(n, ("local", "signal"))[0],
                  "role": NET_META.get(n, ("local", "signal"))[1]}
                 for n in sorted(nets, key=lambda x: (x not in NET_META, x))],
        "connections": sorted(conns, key=lambda c: (c['componentId'], c['pinNumber'])),
    }
    json.dump(doc, open(os.path.join(RAW, 'ir_draft.json'), 'w'), ensure_ascii=False, indent=1)
    numbered, num_problems = number_designators(doc)
    problems += num_problems
    json.dump(numbered, open(os.path.join(RAW, 'ir_numbered.json'), 'w'), ensure_ascii=False, indent=1)

    # Bericht
    lines = [f"Bauteile: {len(comps)}  Netze: {len(doc['nets'])}  Verbindungen: {len(conns)}"]
    nc = sum(1 for c in comps for p in c['pins'] if p.get('noConnected'))
    lines.append(f"NC-Pins: {nc}")
    single = [n for n in nets if len({c['componentId'] for c in conns if c['netId'] == net_id(n)}) < 2]
    if single:
        lines.append("Netze mit <2 Bauteilen: " + ", ".join(single))
    lines.append("PROBLEME:" if problems else "keine Probleme")
    lines += ["  " + p for p in problems]
    if notes:
        lines.append("HINWEISE:")
        lines += ["  " + n for n in notes]
    open(os.path.join(RAW, 'ir_report.txt'), 'w').write("\n".join(lines) + "\n")
    print("\n".join(lines))
    # Zuordnung Bauteil -> Modul fuer die Layout-Planung mitschreiben (funktionale Namen,
    # so wie sie in der IR als componentId-Suffix stehen)
    json.dump({c['ref']: c['_module'] for c in comps}, open(os.path.join(RAW, 'modules.json'), 'w'), indent=1)
    # Loetpads ohne Bestueckungsplatz (funktionale Namen) fuer plan_layout/autoconnect
    json.dump(sorted(NO_PLACE), open(os.path.join(RAW, 'no_place.json'), 'w'), indent=1)
    return 0


def number_designators(doc):
    """S2: funktionale Namen -> numerische Refdes (Ersatz fuer `sch designators allocate`)."""
    changes = json.load(open(os.path.join(RAW, 'designator_changes.json')))
    after = {c['componentId']: c['after'] for c in changes}
    numbered = json.loads(json.dumps(doc))       # tiefe Kopie ohne import copy
    for c in numbered['components']:
        if c['id'] in after:
            c['ref'] = after[c['id']]
    problems = []
    for c in numbered['components']:
        if not re.match(r'^[A-Z]+[0-9]+$', c['ref']):
            problems.append(f"{c['id']}: kein numerischer Designator ({c['ref']})")
    refs = [c['ref'] for c in numbered['components']]
    dups = sorted({r for r in refs if refs.count(r) > 1})
    if dups:
        problems.append("Designator-Kollision: " + ", ".join(dups))
    return numbered, problems


def net_id(name):
    return "net-" + hashlib.sha1(("SmartGrowTopf_V1/" + name).encode()).hexdigest()


if __name__ == '__main__':
    sys.exit(main())
