#!/usr/bin/env python3
"""SmartGrowTopf_V1 — S0/S1-Datenschicht.

Baut aus der Netzliste (hardware/schaltplan_v1_netzliste.csv) und den am lebenden
EasyEDA-Symbol gemessenen Pin-Tabellen die kanonische Connectivity-IR (schemaVersion 1.4)
für den easyeda CLI-Designflow S0-S6.

Quellen (unveraendert gelesen):
  - hardware/schaltplan_v1_netzliste.csv   (Netz, Bauteil, Pin, Bemerkung)
  - hardware/pcba_bom_jlc.csv              (Werte, LCSC-Codes)
  - raw/lcsc_map.json                      (LCSC -> Device-Identitaet)
  - raw/probe*.json                        (echte Pin-Tabellen aus easyeda sch list --include-pins)

Aufruf:
  python3 scripts/build_ir.py            -> raw/ir_draft.json, raw/ir_numbered.json,
                                            raw/no_place.json, raw/ir_report.txt

Die Bauteilliste (COMPS: funktionaler Name, LCSC, Modul, Rolle) wird **aus der Netzliste
abgeleitet** — maßgeblich ist ausschliesslich hardware/schaltplan_v1_netzliste.csv. Jeder
Designator der Netzliste mit LCSC-Code muss vorkommen; fehlt einer oder ist die Zuordnung
unvollstaendig, bricht das Skript laut ab (kein stilles Weglassen).

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

NETLIST = os.path.join(REPO, 'hardware', 'schaltplan_v1_netzliste.csv')
BOM = os.path.join(REPO, 'hardware', 'pcba_bom_jlc.csv')

# --- Bauteile: funktionaler Name -> (Modul, Rolle/Beschreibung) ----------------
# Die funktionalen Namen sind die Designatoren der Handnetzliste. Sie werden per
# `sch designators allocate` (raw/designator_changes.json) auf offizielle
# Library-Praefixe umbenannt; der funktionale Name wandert in `role`.
#
# Stand 16.09.2026 (2S + Schutzbeschaltung): abgeleitet aus
# hardware/schaltplan_v1_netzliste.csv. Die Schutzbeschaltung hat ein eigenes
# Modul SCHUTZ (U_PROT, Q_PROT1/Q_PROT2, R_PROT_*, C_PROT_*, R_CB).
COMP_META = {
    # --- USB-C Eingang ---
    ('J5', 'USB'): 'USB-C 16P Buchse (Laden + Programmieren)',
    ('U6', 'USB'): 'USB-ESD-Schutz USBLC6-2SC6',
    ('R5a', 'USB'): 'CC1-Pulldown 5,1 k',
    ('R5b', 'USB'): 'CC2-Pulldown 5,1 k',
    # --- Stromversorgung / Lader (2S-Boost-Lader IP2326) ---
    ('U_CHG', 'LADER'): '2S-Boost-Lader IP2326, Ladeschluss 8,4 V',
    ('C_CHG_IN', 'LADER'): 'Lader-Eingang 10 uF (Datenblatt C1)',
    ('C_CHG_VIN', 'LADER'): '10 uF direkt am VIN-Pin (Datenblatt C3)',
    ('C_CHG_OUT', 'LADER'): '10 uF am Boost-Ausgang (Datenblatt C6/C7)',
    ('R_VIN_CHG', 'LADER'): 'VIN-Filterwiderstand 0,5 Ohm (kein Shunt)',
    ('L_CHG', 'LADER'): 'Boost-Induktivitaet 2,2 uH',
    ('C_BST_CHG', 'LADER'): 'Bootstrap 100 nF (Datenblatt C2)',
    ('R_ISET', 'LADER'): 'Ladestrom 100 k -> 0,90 A',
    ('J18', 'LADER'): 'Stecker fuer den Akku-Temperatursensor (XH-2P)',
    ('R_NTC_PAR', 'LADER'): '82 kOhm parallel zum Akku-NTC (Datenblatt-Schwellen 0/45/55 Grad C)',
    ('R_UVSET', 'LADER'): 'Eingangs-Unterspannungsschwelle 68 k (4,35 V)',
    ('R_EN_CHG', 'LADER'): 'Lader-EN-Pull-up 100 k',
    ('R_LEDCHG', 'LADER'): 'Lade-LED-Vorwiderstand 1 k',
    ('D_LEDCHG', 'LADER'): 'Ladestatus-LED rot',
    ('C_VSYS_A', 'LADER'): '22 uF direkt am VSYS-Pin (Datenblatt C4)',
    ('C_VSYS_B', 'LADER'): '22 uF direkt am VSYS-Pin (Datenblatt C5)',
    # --- 5-V-Buck (SY8113B) ---
    ('U_BUCK5', 'BOOST'): '5-V-Buck SY8113B, 5,10 V / 3 A',
    ('L_BUCK5', 'BOOST'): 'Buck-Induktivitaet 4,7 uH',
    ('C_B5_BST', 'BOOST'): 'Bootstrap 100 nF',
    ('C_B5_IN', 'BOOST'): '22 uF Buck-Eingang',
    ('C_B5_IN_HF', 'BOOST'): '100 nF HF Buck-Eingang',
    ('C_B5_OUT', 'BOOST'): '22 uF Buck-Ausgang',
    ('C_B5_OUT_HF', 'BOOST'): '100 nF HF Buck-Ausgang',
    ('R_FB5_TOP', 'BOOST'): 'Feedback oben 75 k -> 5,10 V',
    ('R_FB5_BOT', 'BOOST'): 'Feedback unten 10 k',
    # --- 3,3-V-Buck (AP63203) ---
    ('U_BUCK3', 'LDO'): '3,3-V-Buck AP63203, 3,31 V / 2 A',
    ('L_BUCK3', 'LDO'): 'Buck-Induktivitaet 4,7 uH',
    ('C_B3_BST', 'LDO'): 'Bootstrap 100 nF',
    ('C_B3_IN', 'LDO'): '22 uF Buck-Eingang',
    ('C_B3_IN_HF', 'LDO'): '100 nF HF Buck-Eingang',
    ('C_B3_OUT', 'LDO'): '22 uF Buck-Ausgang',
    ('C_B3_OUT_HF', 'LDO'): '100 nF HF Buck-Ausgang',
    ('TP5', 'LDO'): 'Testpad +3V3',
    # --- Unterspannungswaechter (TPS3839) ---
    ('U7', 'WAEChTER'): 'Unterspannungswaechter TPS3839G33 (3,08 V)',
    ('R3a', 'WAEChTER'): 'UVLO-Teiler oben 200 k',
    ('R3b', 'WAEChTER'): 'UVLO-Teiler unten 200 k',
    ('C12', 'WAEChTER'): 'Decoupling Waechter 100 nF',
    # --- Akku-Schutz auf der Platine (HY2120-CB + 2x PSMN4R2-30MLDX) ---
    ('U_PROT', 'SCHUTZ'): '2-Zellen-Schutz-IC HY2120-CB',
    ('Q_PROT1', 'SCHUTZ'): 'Entlade-MOSFET PSMN4R2-30MLDX',
    ('Q_PROT2', 'SCHUTZ'): 'Lade-MOSFET PSMN4R2-30MLDX',
    ('R_PROT_VDD', 'SCHUTZ'): '330 R zum VDD-Pin des Schutz-IC',
    ('R_PROT_VC', 'SCHUTZ'): '330 R zum VC-Pin des Schutz-IC',
    ('R_PROT_CS', 'SCHUTZ'): 'CS-Widerstand 2 k zum Board-GND',
    ('C_PROT_VDD', 'SCHUTZ'): 'VDD-Filter 100 nF nach Pack-Minus',
    ('C_PROT_VC', 'SCHUTZ'): 'VC-Filter 100 nF nach Pack-Minus',
    ('R_CB', 'SCHUTZ'): 'Balancing-Widerstand 100 R zum Mittelabgriff',
    # --- Akku / Puffer ---
    ('J1', 'AKKU'): 'Akku JST-XH 3P (B-/MID/B+), aufrecht',
    ('F1', 'AKKU'): 'Sicherung in der Pack-Plus-Leitung, 5 A traege (2410)',
    ('C3', 'AKKU'): 'Elko 100 uF Pumpenpuffer auf +5V',
    ('TP3', 'AKKU'): 'Testpad GND',
    ('TP4', 'AKKU'): 'Testpad VBAT',
    # --- MCU + Beschaltung ---
    ('U1', 'MCU'): 'ESP32-C6-MINI-1 WLAN-Modul',
    ('C2', 'MCU'): 'Bulk 22 uF am Modul-3V3',
    ('C1a', 'MCU'): 'Decoupling Modul 100 nF',
    ('C1b', 'MCU'): 'Decoupling Modul 100 nF',
    ('C13', 'MCU'): 'Decoupling Modul 100 nF',
    ('C4', 'MCU'): 'EN-RC 1 uF',
    ('C9', 'MCU'): 'ADC-Filter Sensor 100 nF',
    ('C10', 'MCU'): 'ADC-Filter VBAT 100 nF',
    ('R_EN', 'MCU'): 'EN-Pull-up 10 k',
    ('R_BOOT', 'MCU'): 'GPIO9-Pull-up 10 k',
    ('R_GPIO8', 'MCU'): 'GPIO8-Strap-Pull-up 10 k',
    ('R4', 'MCU'): 'Status-LED 220 R',
    ('R_TANK', 'MCU'): 'Tank-LED 1 k',
    ('R_SENSE_TOP', 'MCU'): 'ADC-Teiler oben 200 k (1:3,94)',
    ('R_SENSE_BOT', 'MCU'): 'ADC-Teiler unten 68 k',
    ('D2', 'MCU'): 'Status-LED gruen 525 nm',
    ('D5', 'MCU'): 'Tank-leer-LED rot',
    ('SW1', 'MCU'): 'Reset-Taster',
    ('SW2', 'MCU'): 'Boot-Taster',
    ('TP2', 'MCU'): 'Testpad RXD0',
    # --- Taster ---
    ('R_BTN', 'TASTER'): 'Taster-Pull-up 10 k',
    ('C_BTN', 'TASTER'): 'Taster-Entprellung 100 nF',
    ('J6', 'TASTER'): '2 Loetpads externer Taster',
    # --- Sensor-Eingang ---
    ('J2', 'SENSOR'): 'Feuchtesensor JST-XH 3P, aufrecht',
    ('J17', 'SENSOR'): '5-V-Ausgang fuer Sensorik JST-XH 2P',
    ('R6', 'SENSOR'): 'Sensor-AOUT Serie 1 k',
    ('Q_SENS', 'SENSOR'): 'P-Kanal-Lastschalter der Sensorversorgung',
    ('R_SENS_GATE', 'SENSOR'): '47 kOhm Gate-Pull-up des Sensor-Lastschalters',
    ('TP6', 'SENSOR'): 'Testpad SENSOR_AOUT',
    # --- Pumpen ---
    ('Q1', 'PUMPE'): 'N-MOSFET Pumpentreiber Dosierpumpe',
    ('D1', 'PUMPE'): 'Freilaufdiode Dosierpumpe',
    ('R1', 'PUMPE'): 'Gate-Serie 1 k',
    ('R2', 'PUMPE'): 'Gate-Pulldown 47 k',
    ('C11', 'PUMPE'): 'EMI an den Pumpenklemmen 100 nF',
    ('J4', 'PUMPE'): 'Dosierpumpe JST-XH 2P, aufrecht',
    ('Q_PUMP2', 'PUMPE'): 'N-MOSFET Sauerstoffpumpe',
    ('R_GATE2', 'PUMPE'): 'Gate-Serie 1 k Kanal 2',
    ('R_GATE2_PD', 'PUMPE'): 'Gate-Pulldown 47 k Kanal 2',
    ('D_FLY2', 'PUMPE'): 'Freilaufdiode Sauerstoffpumpe',
    ('C_PUMP2_EMI', 'PUMPE'): 'EMI an den Klemmen Sauerstoffpumpe 100 nF',
    ('J16', 'PUMPE'): 'Sauerstoffpumpe JST-XH 2P, aufrecht',
    # --- Debug ---
    ('R_UART', 'DEBUG'): 'UART-Serie 499 R (DNP)',
    ('TP1', 'DEBUG'): 'Testpad TXD0',
    # --- Lichtsensor ---
    ('J7', 'LICHT'): 'Lichtsensor-Stiftleiste 1x3 2,54 mm',
    ('R_LIGHT', 'LICHT'): 'Licht-Lastwiderstand 10 k nach GND',
    ('R_LIGHT_S', 'LICHT'): 'Licht-Serienschutz 1 k zum ADC',
    ('C_LIGHT', 'LICHT'): 'ADC-Filter Licht 100 nF',
    # --- Erweiterung ---
    ('J8', 'ERWEITERUNG'): 'I2C-Stiftleiste 1x4 (GND-VCC-SDA-SCL)',
    ('J9', 'ERWEITERUNG'): 'Reserve-Analog Stiftleiste 1x3 (IO5)',
    ('J10', 'ERWEITERUNG'): 'Reserve IO15 Stiftleiste 1x3',
    ('J11', 'ERWEITERUNG'): 'Reserve IO16 (TXD0) Stiftleiste 1x3',
    ('J12', 'ERWEITERUNG'): 'Reserve IO17 (RXD0) Stiftleiste 1x3',
    ('J13', 'ERWEITERUNG'): 'Reserve IO21 Stiftleiste 1x3',
    ('J15', 'ERWEITERUNG'): 'Reserve IO23 Stiftleiste 1x3',
    ('Q2', 'ERWEITERUNG'): 'P-Kanal-Load-Switch VCC_EXT',
    ('R_GATE', 'ERWEITERUNG'): 'Gate-Pull-up Load-Switch 47 k',
    ('R_SDA_PU', 'ERWEITERUNG'): 'I2C-SDA-Pull-up 4,7 k an VCC_EXT',
    ('R_SCL_PU', 'ERWEITERUNG'): 'I2C-SCL-Pull-up 4,7 k an VCC_EXT',
    ('R_SDA_S', 'ERWEITERUNG'): 'I2C-SDA-Serienschutz 1 k',
    ('R_SCL_S', 'ERWEITERUNG'): 'I2C-SCL-Serienschutz 1 k',
    ('R_SPARE_AIN', 'ERWEITERUNG'): 'Reserve-AIN-Serienschutz 1 k',
    ('R_SPARE_IO15', 'ERWEITERUNG'): 'Reserve-IO15-Serienschutz 1 k',
    ('R_SPARE_IO16', 'ERWEITERUNG'): 'Reserve-IO16-Serienschutz 1 k',
    ('R_SPARE_IO17', 'ERWEITERUNG'): 'Reserve-IO17-Serienschutz 1 k',
    ('R_SPARE_IO21', 'ERWEITERUNG'): 'Reserve-IO21-Serienschutz 1 k',
    ('R_SPARE_IO23', 'ERWEITERUNG'): 'Reserve-IO23-Serienschutz 1 k',
    ('C_SPARE', 'ERWEITERUNG'): 'ADC-Filter Reserve-Analog 100 nF',
}

# Bauteile ohne LCSC-Code in der JLC-BOM: auf ein eigenes Geraet abgebildet
# (Loetpads, Testpunkte, DNP-Bauteile). Der Modulschluessel bleibt der funktionale Name.
NO_LCSC = {
    'J6': 'NO_LCSC_J6',
    'TP1': 'NO_LCSC_TP', 'TP2': 'NO_LCSC_TP', 'TP3': 'NO_LCSC_TP',
    'TP4': 'NO_LCSC_TP', 'TP5': 'NO_LCSC_TP', 'TP6': 'NO_LCSC_TP',
    'R_UART': 'NO_LCSC_R_UART',
}

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
    # R_UART (499 R) ist DNP und hat in der BOM bewusst keinen LCSC-Code; das
    # gemessene Widerstands-Symbol wird ueber die Device-UUID des 499-Ohm-Geraets
    # eingebunden (keine eigene Bestellposition).
    "NO_LCSC_R_UART": ("0819f05c4eef4c71ace90d822a990e87", "68e77fee64a84125bdea1b394c2e5985", "0805W8F4990T5E"),
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
    # --- 2S + Schutzbeschaltung (16.09.2026) ---
    "BAT_MINUS": ("global", "ground"),   # Pack-Minus hinter dem Schutz, masseartig
    "MID": ("local", "signal"),          # Mittelabgriff (Zelle 1 + / Zelle 2 -)
    "PROT_VDD": ("local", "signal"),
    "PROT_VC": ("local", "signal"),
    "PROT_GATE_D": ("local", "signal"),
    "PROT_GATE_C": ("local", "signal"),
    "PROT_CS": ("local", "signal"),
    "PROT_COMMON": ("local", "signal"),
    "VBATM_CHG": ("local", "signal"),
}

# --- Pin-Spezifikationen aus der Netzliste aufloesen --------------------------
# Sonderfaelle, die sich nicht rein numerisch aufloesen lassen (Pin-Namen des
# offiziellen Symbols statt Nummern).
NAME_SPECS = {
    # (Bauteil, Text) -> Liste von Pin-Namen (Praefix-Wildcard moeglich)
    ("J5", "VBUS (A4/A9/B4/B9)"): ["VBUS"],
    ("U1", "VDD33 (alle)"): [],
    # IP2326: das Symbol fuehrt das Thermo-Pad als Pin 25 mit Namen "EP";
    # die Netzliste schreibt dafuer "EPAD" (Datenblatt-Sprechweise).
    ("U_CHG", "EPAD"): ["EP"],
}

RANGE_RE = re.compile(r'^(\d+)\s*-\s*(\d+)$')


def load_pin_tables():
    """Echte Pin-Tabellen je Device-UUID aus den Live-Messungen (probe*.json).

    Der Device-Schluessel steckt je nach Dateigeneration in einem anderen Feld:
      * Systembibliothek (device.libraryUuid == 0819f05c...) + 32-stellige device.uuid
        -> der Schluessel ist device.uuid (die 32-stellige Device-UUID).
      * sonst (alte probe*.json) -> der Schluessel ist device.libraryUuid.
    Beide Generationen muessen ladbar bleiben.
    """
    SYS_LIB = "0819f05c4eef4c71ace90d822a990e87"
    tables = {}
    for name in sorted(os.listdir(RAW)):
        if not name.startswith('probe') or not name.endswith('.json'):
            continue
        data = json.load(open(os.path.join(RAW, name)))
        for c in data['result']['components']:
            dev = c.get('device') or {}
            lu = dev.get('libraryUuid')
            uu = dev.get('uuid')
            if lu == SYS_LIB and isinstance(uu, str) and len(uu) == 32:
                key = uu
            else:
                key = lu
            if not key or not isinstance(key, str) or len(key) != 32 or not c.get('pins'):
                continue
            tables.setdefault(key, [
                {"number": p["pinNumber"], "name": p["pinName"]}
                for p in c["pins"]
            ])
    return tables


def _read_csv(path):
    with open(path, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def _bom_lcsc():
    """Designator -> LCSC-Code aus der JLC-BOM (Quelle der Wahrheit)."""
    out = {}
    for r in _read_csv(BOM):
        for d in r['Designator'].split():
            out[d] = r['LCSC Part #'].strip()
    return out


def derive_comps():
    """COMPS ausschliesslich aus der Netzliste ableiten (maßgeblich).

    Reihenfolge = Reihenfolge des ersten Auftretens in der Netzliste.
    Bricht laut ab, wenn ein Designator kein Modul/Rolle oder keinen LCSC-Code
    (auch keinen NO_LCSC-Ersatz) hat.
    """
    bom = _bom_lcsc()
    order = []
    for r in _read_csv(NETLIST):
        if r['Netz'].strip().startswith('#'):
            continue
        c = r['Bauteil'].strip()
        if c and c not in order:
            order.append(c)
    meta_by_name = {nm: (mod, desc) for (nm, mod), desc in COMP_META.items()}
    comps, problems = [], []
    for name in order:
        meta = meta_by_name.get(name)
        if meta is None:
            problems.append(f"{name}: kein Modul/Rolle in COMP_META")
            continue
        module, desc = meta
        lcsc = bom.get(name, '')
        if not lcsc:
            lcsc = NO_LCSC.get(name)
            if lcsc is None:
                problems.append(f"{name}: kein LCSC-Code in der BOM und kein NO_LCSC-Ersatz")
                continue
        comps.append((name, lcsc, module, desc))
    if problems:
        raise SystemExit("COMPS-Ableitung unvollstaendig (Netzliste ist maßgeblich):\n  "
                         + "\n  ".join(problems))
    return comps


COMPS = derive_comps()


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
    with open(NETLIST, newline='', encoding='utf-8') as fh:
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
    numbered, num_problems, num_notes = number_designators(doc)
    problems += num_problems
    notes += num_notes
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
    """S2: funktionale Namen -> numerische Refdes (Ersatz fuer `sch designators allocate`).

    Die Allokation kommt ausschliesslich aus raw/designator_changes.json. Bauteile ohne
    Allokation behalten vorlaeufig ihren funktionalen Namen (der Koordinator vergibt sie
    live per `sch designators allocate`). Eine Kollision (zwei Bauteile mit demselben
    Designator) wird laut gemeldet.
    """
    changes = json.load(open(os.path.join(RAW, 'designator_changes.json')))
    after = {c['componentId']: c['after'] for c in changes}
    numbered = json.loads(json.dumps(doc))       # tiefe Kopie ohne import copy
    for c in numbered['components']:
        if c['id'] in after:
            c['ref'] = after[c['id']]
    problems, notes = [], []
    refs = [c['ref'] for c in numbered['components']]
    dups = sorted({r for r in refs if refs.count(r) > 1})
    if dups:
        problems.append("Designator-Kollision: " + ", ".join(dups))
    # Funktionale Namen ohne Allokation sind kein Fehler: laut Arbeitsweise fuehrt COMPS
    # bewusst funktionale Namen, die endgueltige Nummer vergibt `sch designators allocate`.
    unallocated = sorted(c['ref'] for c in numbered['components']
                         if not re.match(r'^[A-Z]+[0-9]+$', c['ref']))
    if unallocated:
        notes.append(f"{len(unallocated)} Bauteil(e) warten auf die Designator-Allokation "
                     f"(funktionaler Name bleibt vorlaeufig): " + ", ".join(unallocated))
    return numbered, problems, notes


def net_id(name):
    return "net-" + hashlib.sha1(("SmartGrowTopf_V1/" + name).encode()).hexdigest()


if __name__ == '__main__':
    sys.exit(main())
