# Smart Grow Topf

Automatisch bewässernder Topf für eine Cannabis-Pflanze, gesteuert über ein **ESP32-C6-Modul direkt auf der eigenen PCB** (eigener 1S-Lader, eigener 3,3-V-Regler), Akkubetrieb. **Eigenes Projekt** (unabhängig vom GrowTower).

![Smart Grow Topf – KI-Konzeptbild im Stand V1](docs/img/konzeptbild-v1-ki.jpg)

*KI-generiertes Konzeptbild (Prompts: [`docs/04_bildkonzepte-prompts.md`](docs/04_bildkonzepte-prompts.md)) — zeigt Wulst mit Deckel und USB-C, Verteilerring auf dem Substrat, Kragen. Keine CAD-Ableitung: verbindliche Maße stehen in [`docs/02_architektur-und-geometrie.md`](docs/02_architektur-und-geometrie.md).*

## Konzept (Top-Drip mit Rücklauf)

![Funktionsbild Smart Grow Topf – Weg des Wassers im Schnitt](docs/img/funktionsbild-v1-ki.jpg)

*KI-generiertes Funktionsbild (Prompt 3 aus [`docs/04_bildkonzepte-prompts.md`](docs/04_bildkonzepte-prompts.md)) — Weg des Wassers: Peristaltikpumpe in der Wulst → Druckleitung über den Kragen → Gießring → Tropfen ins Substrat → Drainage-Sieb → zurück in den Sammeltank. Bild und Beschriftung sind KI-generiert und nicht maßhaltig. Was im Bild fehlt: der kapazitive Sensor (bei r ≈ 55 mm, Messebene 75 mm tief) und die 25 mm Blähton-Drainageschicht über dem Sieb; „Suctionshöhe" ist ein KI-Sprachfehler (gemeint: Saughöhe). Verbindlich bleibt [`docs/02_architektur-und-geometrie.md`](docs/02_architektur-und-geometrie.md).*

```
        Verteilerring (3D-Druck)          ← Wasser von oben
   ┌──────────────────────────────┐
   │  ERDE / SUBSTRAT             │   Ø127 innen × 150 mm (≈1,6 L)
   │  ⊗ kapazitiver Sensor        │   Messebene 75 mm = halbe Topfhöhe
   │  ▒▒ Blähton 25 mm ▒▒         │   Dränage + Partikelfilter
   └──────────────┬───────────────┘
        Luftspalt 30 mm (Gießfüße)
   ┌──────────────┴───────────────┐
   │  WASSERTANK 1,0 L            │   Ø134 innen, max. 71 mm Wasserstand
   └──────────────────────────────┘
        Wulst seitlich: Pumpe, PCB (ESP32-C6-Modul), Akku, Schlauch-/Kabelkanal
```

**Gesamthöhe 278 mm**, Grundriss Ø 140 mm (mit Wulst ≈ 180 mm breit).

**Regelkreis:**
1. Kapazitiver Sensor (analog, **invertiert**: trocken = hoher ADC) misst die Substratfeuchte.
2. Zu trocken → **Pumpe EIN** (Peristaltik, Wasser von oben auf den Verteilerring).
3. Überschuss läuft durchs Substrat und zurück in den Tank.
4. **10–20 min** später erneut messen: ADC gefallen → ok. ADC nicht gefallen → **Tank leer / Pumpe verstopft** → Telegram-Alarm.

## Warum dieses Design
- **Peristaltik:** Medium bleibt im Schlauch, kommt nie mit der Pumpenmechanik in Kontakt → sauber, kleine Mengen, akkutauglich, selbstansaugend.
- **Top-Drip:** gezielte Dosierung von oben, kein dauerhaft wassergesättigter Topfboden (Luftspalt), Wurzeln bleiben belüftet.
- **Kapazitiver Sensor:** korrosionsfrei, analog direkt am ADC, Messebene in der Wurzelzone.
- **Wulst statt Innenraum:** Elektronik komplett über dem Wasserstand, Sensor/Kabel/Schlauch sauber geführt.

## Projektstruktur
```
cannabis-autopot/
├── README.md
├── docs/
│   ├── 01_anforderungen.md              ← Festlegungen des Users
│   ├── 02_architektur-und-geometrie.md  ← verbindliche Maße (CAD/PCB-Grundlage)
│   ├── 04_bildkonzepte-prompts.md       ← KI-Image-Prompts (+ generierte .txt)
│   └── img/                             ← KI-Konzeptbilder
├── scripts/
│   ├── check_netlist.py                 ← Lint der Netzliste (exit 0 vor dem Layout nötig)
│   └── check_bom_consistency.py         ← Querabgleich Schaltplan ↔ JLCPCB-BOM
├── hardware/
│   ├── bom_entscheidung.md              ← BESTELLGRUNDLAGE: Bauteile, Preise, Links
│   ├── schaltplan_v1.md                 ← VERBINDUNGSVORGABE: Netze, Werte, Pinbelegungen
│   ├── schaltplan_v1_netzliste.csv      ← dieselben Verbindungen maschinenlesbar (Netz, Bauteil, Pin)
│   ├── pcba_bom_jlc.csv                 ← BOM im JLCPCB-Upload-Format (LCSC-Codes)
│   ├── pcba_verfuegbarkeit_jlc.md       ← JLC-Verfügbarkeitsprüfung je Position
│   └── hardware_auswahl_bom.md          ← Recherche-/Ideenebene (nicht Bestellgrundlage)
├── research/
│   ├── bom-check/                       ← aktueller Preis-/Verfügbarkeitscheck je Bauteilgruppe
│   ├── kapazitiver-bodenfeuchtesensor-esp32-recherche.md
│   ├── smart-grow-topf_pumpe-bewaesserung.md
│   ├── smart-grow-topf-esp32-firmware-konzept.md
│   └── markt-konzept-recherche.md
└── case/                                ← parametrisches Gehäuse-CAD (OpenSCAD)
```

## Status
- [x] Projektordner + Anforderungen + 4 Recherchen (10.09.2026)
- [x] **Entscheidungen 11.09.2026:** Topf Ø140×150 (Erde) + 1 L Tank darunter · ESP32-C6-MINI-1 auf eigener PCB · Wulst mit Kanal · Top-Drip-Ring · Sensor von oben · Telegram final · nur Wasser
- [x] **Höhen-/Volumenberechnung** → Gesamthöhe 278 mm, Tank 1,0 L, Erdvolumen 1,9 L (`docs/02_...`)
- [x] **BOM-Entscheidung** (11.09.2026): ESP32-C6-MINI-1 ≈ 3,60 € · OEM-Peristaltikpumpe ABC-12527 (3,7–6 V) 7,74 € · Sensor v1.2 4,99 € · EFASO-Akku 14,90 € → **≈ 47–49 €** gesamt inkl. Schlauch und Passiven (+ ~28 € JLCPCB-Handling) (`hardware/bom_entscheidung.md`)
- [x] **Versorgung festgelegt:** 1S direkt, kein Boost/Buck (Pumpe ab 3 V dokumentiert); eigener Lader **MCP73831T-2** + LDO **ME6211** auf der Platine
- [x] **MCU festgelegt:** **ESP32-C6-MINI-1** auf eigener PCB (kein Dev-Board) — Pflichtbeschaltung und Antennenregeln aus den Espressif-Docs übernommen
- [x] **PCBA geprüft:** alle Bauteile bei JLCPCB verfügbar (LCSC-Codes in `hardware/pcba_bom_jlc.csv`)
- [ ] Gehäuse-CAD (parametrisch) + PCB-Design
- [ ] Firmware (State-Machine)

## Nächste Schritte
1. BOM finalisieren (Preise, Links, Verfügbarkeit) → `research/bom-check/`
2. Gehäuse-CAD (OpenSCAD, parametrisch) aus `docs/02_architektur-und-geometrie.md`
3. PCB: ESP32-C6-Modul, MCP73831-Lader, ME6211-LDO, MOSFET-Treiber, Sensor-ADC, USB-C — Netzliste `hardware/schaltplan_v1_netzliste.csv`
4. Firmware: State-Machine, Kalibrierroutine, Telegram-Alarm
