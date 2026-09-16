# SmartGrowTopf_V1 - vollstaendige Schaltungsbeschreibung (Maschinenfassung)

Generiert am 16.09.2026 **maschinell aus der Projekt-IR** (`hardware/easyeda/raw/ir_numbered.json`,
`placement.json`, `modules.json`, `pcba_bom_jlc.csv`) plus dem Protokoll der Design-Pruefsuite
(`hardware/design/report.py`). Revision **2S-Umbau + Akku-Schutz**. Keine Zahl ist abgetippt - alle
Werte sind gezaehlt oder gerechnet. Quellen im Repo: `hardware/schaltplan_v1.md` (Wahrheit),
`hardware/schaltplan_v1_netzliste.csv` (Netzliste), `hardware/pcba_bom_jlc.csv` (Stueckliste).

## 1. Kennzahlen und Versorgungskette

| Kennzahl | Wert |
|---|---|
| Bauteile mit Bezeichner | **124** |
| Netze | **77** |
| Verbindungen (Pin -> Netz) | **351** |
| Module / Bloecke auf dem Blatt | **14** |
| Steckverbinder (J*) | **15** |
| Testpunkte (TP*) | **6** |

**Versorgungskette (2S):**

```
USB-C 5 V --> IP2326 (Boost-Lader, 8,4 V / 0,90 A) --> VBAT = 2S-Pack (6,0 - 8,4 V)
                                                            |
2S-Pack an J1 (3-polig: B- / Mittelabgriff / B+) --> HY2120-Schutz
      Pack-Minus (BAT_MINUS) und Board-Masse (GND) sind getrennt;
      dazwischen liegt das MOSFET-Paar Q3/Q4 (gemeinsamer Drain)
                                                            |
                       +------------------------------------+------------------------------------+
                       |                                                                         |
          SY8113B-Buck 3 A --> +5 V                                  AP63203-Buck 2 A --> +3,3 V
          (Dosierpumpe J4, Sauerstoffpumpe J16,                        (ESP32-C6, Sensorik,
           Sensor-5-V-Ausgang J17)                                     LEDs, Erweiterungs-Rails)
```

In Worten: 5 V kommen ueber USB-C; der **IP2326** laedt daraus den 2S-Pack auf 8,4 V.
Der Pack geht ueber den **3-poligen Stecker J1** (Minus / Mittelabgriff / Plus) auf die Platine.
Der **HY2120** trennt mit zwei MOSFETs Pack-Minus und Board-Masse und ueberwacht jede Zelle;
der **IP2326** nutzt den Mittelabgriff zusaetzlich zum **Balancieren** (R_CB). Aus VBAT erzeugen
zwei Abwaertswandler **+5 V** und **+3,3 V**. Es gibt **keinen LDO und keinen Aufwaertswandler**.

## 2. Was ist verbaut

| Ref | Modul | Typ / Wert | Gehaeuse | LCSC | Funktion |
|---|---|---|---|---|---|
| **C3** | Akku & Puffer | 100uF 16V | SMD D6.3x5.4 | `C970684` | Elko 100 uF Pumpenpuffer auf +5V |
| **J1** | Akku & Puffer | JST-XH-3P | THT P2.5 aufrecht (Top-Entry) | `C5258884` | Akku JST-XH 3P (B-/MID/B+), aufrecht |
| **TP3** | Akku & Puffer | 5010-Testpoint | - | - | Testpad GND |
| **TP4** | Akku & Puffer | 5010-Testpoint | - | - | Testpad VBAT |
| **C14** | 5-V-Buck (SY8113B) | 100nF | 0805 | `C49678` | 100 nF HF Buck-Eingang |
| **C21** | 5-V-Buck (SY8113B) | 100nF | 0805 | `C49678` | Bootstrap 100 nF |
| **C22** | 5-V-Buck (SY8113B) | 22uF 25V | 0805 | `C45783` | 22 uF Buck-Ausgang |
| **C23** | 5-V-Buck (SY8113B) | 100nF | 0805 | `C49678` | 100 nF HF Buck-Ausgang |
| **C8** | 5-V-Buck (SY8113B) | 22uF 25V | 0805 | `C45783` | 22 uF Buck-Eingang |
| **L2** | 5-V-Buck (SY8113B) | 4.7uH Isat 4,0A DCR 31mR | SMD 6x6mm | `C105660` | Buck-Induktivitaet 4,7 uH |
| **R19** | 5-V-Buck (SY8113B) | 75k | 0805 | `C17819` | Feedback oben 75 k -> 5,10 V |
| **R20** | 5-V-Buck (SY8113B) | 10k | 0805 | `C17414` | Feedback unten 10 k |
| **U3** | 5-V-Buck (SY8113B) | SY8113B ADC | TSOT-23-6 | `C78989` | 5-V-Buck SY8113B, 5,10 V / 3 A |
| **R47** | UART-Debug-Pads (DNP) | 499R | 0805 | - | UART-Serie 499 R (DNP) |
| **TP1** | UART-Debug-Pads (DNP) | 5010-Testpoint | - | - | Testpad TXD0 |
| **C31** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 100nF | 0805 | `C49678` | ADC-Filter Reserve-Analog 100 nF |
| **J10** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO15 Stiftleiste 1x3 |
| **J11** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO16 (TXD0) Stiftleiste 1x3 |
| **J12** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO17 (RXD0) Stiftleiste 1x3 |
| **J13** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO21 Stiftleiste 1x3 |
| **J15** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO23 Stiftleiste 1x3 |
| **J8** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x4-2.54mm | THT P2.54 gerade | `C2691448` | I2C-Stiftleiste 1x4 (GND-VCC-SDA-SCL) |
| **J9** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve-Analog Stiftleiste 1x3 (IO5) |
| **Q2** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | AO3401A | SOT-23 | `C15127` | P-Kanal-Load-Switch VCC_EXT |
| **R25** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 47k | 0805 | `C17713` | Gate-Pull-up Load-Switch 47 k |
| **R36** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | I2C-SDA-Serienschutz 1 k |
| **R37** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 4.7k | 0805 | `C17673` | I2C-SDA-Pull-up 4,7 k an VCC_EXT |
| **R38** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | I2C-SCL-Serienschutz 1 k |
| **R39** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 4.7k | 0805 | `C17673` | I2C-SCL-Pull-up 4,7 k an VCC_EXT |
| **R40** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | Reserve-AIN-Serienschutz 1 k |
| **R41** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | Reserve-IO15-Serienschutz 1 k |
| **R42** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | Reserve-IO16-Serienschutz 1 k |
| **R43** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | Reserve-IO17-Serienschutz 1 k |
| **R44** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | Reserve-IO21-Serienschutz 1 k |
| **R45** | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | 1k | 0805 | `C17513` | Reserve-IO23-Serienschutz 1 k |
| **C1** | Laden (IP2326, 2S) | 10uF 25V | 0805 | `C15850` | Lader-Eingang 10 uF (Datenblatt C1) |
| **C19** | Laden (IP2326, 2S) | 22uF 25V | 0805 | `C45783` | 22 uF direkt am VSYS-Pin (Datenblatt C4) |
| **C20** | Laden (IP2326, 2S) | 22uF 25V | 0805 | `C45783` | 22 uF direkt am VSYS-Pin (Datenblatt C5) |
| **C5** | Laden (IP2326, 2S) | 10uF 25V | 0805 | `C15850` | 10 uF direkt am VIN-Pin (Datenblatt C3) |
| **C6** | Laden (IP2326, 2S) | 100nF | 0805 | `C49678` | Bootstrap 100 nF (Datenblatt C2) |
| **C7** | Laden (IP2326, 2S) | 10uF 25V | 0805 | `C15850` | 10 uF am Boost-Ausgang (Datenblatt C6/C7) |
| **L1** | Laden (IP2326, 2S) | 2.2uH Isat 5,0A DCR 58mR | SMD 4.6x4.1mm | `C142096` | Boost-Induktivitaet 2,2 uH |
| **LED1** | Laden (IP2326, 2S) | LED-RED | 0805 | `C84256` | Ladestatus-LED rot |
| **R10** | Laden (IP2326, 2S) | 100k 1% | 0805 | `C96346` | Ladestrom 100 k -> 0,90 A |
| **R11** | Laden (IP2326, 2S) | 51k | 0805 | `C17737` | NTC-Funktion stillgelegt 51 k |
| **R12** | Laden (IP2326, 2S) | 68k | 0805 | `C17801` | Eingangs-Unterspannungsschwelle 68 k (4,35 V) |
| **R3** | Laden (IP2326, 2S) | 0.5R | 0805 | `C28319` | VIN-Filterwiderstand 0,5 Ohm (kein Shunt) |
| **R5** | Laden (IP2326, 2S) | 1k | 0805 | `C17513` | Lade-LED-Vorwiderstand 1 k |
| **R7** | Laden (IP2326, 2S) | 100k 1% | 0805 | `C96346` | Lader-EN-Pull-up 100 k |
| **U2** | Laden (IP2326, 2S) | IP2326 | VQFN-24-EP(4x4) | `C2832094` | 2S-Boost-Lader IP2326, Ladeschluss 8,4 V |
| **C15** | 3V3-Buck (AP63203) | 22uF 25V | 0805 | `C45783` | 22 uF Buck-Eingang |
| **C16** | 3V3-Buck (AP63203) | 100nF | 0805 | `C49678` | 100 nF HF Buck-Eingang |
| **C25** | 3V3-Buck (AP63203) | 100nF | 0805 | `C49678` | Bootstrap 100 nF |
| **C26** | 3V3-Buck (AP63203) | 22uF 25V | 0805 | `C45783` | 22 uF Buck-Ausgang |
| **C27** | 3V3-Buck (AP63203) | 100nF | 0805 | `C49678` | 100 nF HF Buck-Ausgang |
| **L3** | 3V3-Buck (AP63203) | 4.7uH Isat 4,0A DCR 31mR | SMD 6x6mm | `C105660` | Buck-Induktivitaet 4,7 uH |
| **R26** | 3V3-Buck (AP63203) | 47k | 0805 | `C17713` | Feedback oben 47 k -> 3,31 V |
| **R27** | 3V3-Buck (AP63203) | 15k | 0805 | `C17475` | Feedback unten 15 k |
| **TP5** | 3V3-Buck (AP63203) | 5010-Testpoint | - | - | Testpad +3V3 |
| **U4** | 3V3-Buck (AP63203) | AP63203WU-7 | TSOT-23-6 | `C780769` | 3,3-V-Buck AP63203, 3,31 V / 2 A |
| **C30** | Lichtsensor-Eingang | 100nF | 0805 | `C49678` | ADC-Filter Licht 100 nF |
| **J7** | Lichtsensor-Eingang | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Lichtsensor-Stiftleiste 1x3 2,54 mm |
| **R34** | Lichtsensor-Eingang | 10k | 0805 | `C17414` | Licht-Lastwiderstand 10 k nach GND |
| **R35** | Lichtsensor-Eingang | 1k | 0805 | `C17513` | Licht-Serienschutz 1 k zum ADC |
| **C10** | ESP32-C6-MCU + Beschaltung | 100nF | 0805 | `C49678` | ADC-Filter VBAT 100 nF |
| **C13** | ESP32-C6-MCU + Beschaltung | 100nF | 0805 | `C49678` | Decoupling Modul 100 nF |
| **C2** | ESP32-C6-MCU + Beschaltung | 22uF 25V | 0805 | `C45783` | Bulk 22 uF am Modul-3V3 |
| **C28** | ESP32-C6-MCU + Beschaltung | 100nF | 0805 | `C49678` | Decoupling Modul 100 nF |
| **C29** | ESP32-C6-MCU + Beschaltung | 100nF | 0805 | `C49678` | Decoupling Modul 100 nF |
| **C4** | ESP32-C6-MCU + Beschaltung | 1uF | 0603 | `C15849` | EN-RC 1 uF |
| **C9** | ESP32-C6-MCU + Beschaltung | 100nF | 0805 | `C49678` | ADC-Filter Sensor 100 nF |
| **D2** | ESP32-C6-MCU + Beschaltung | LED-GREEN | 0805 | `C2297` | Status-LED gruen 525 nm |
| **D5** | ESP32-C6-MCU + Beschaltung | LED-RED | 0805 | `C84256` | Tank-leer-LED rot |
| **R14** | ESP32-C6-MCU + Beschaltung | 200k | 0805 | `C17539` | ADC-Teiler oben 200 k (1:3,94) |
| **R21** | ESP32-C6-MCU + Beschaltung | 10k | 0805 | `C17414` | EN-Pull-up 10 k |
| **R22** | ESP32-C6-MCU + Beschaltung | 10k | 0805 | `C17414` | GPIO9-Pull-up 10 k |
| **R23** | ESP32-C6-MCU + Beschaltung | 10k | 0805 | `C17414` | GPIO8-Strap-Pull-up 10 k |
| **R33** | ESP32-C6-MCU + Beschaltung | 68k | 0805 | `C17801` | ADC-Teiler unten 68 k |
| **R4** | ESP32-C6-MCU + Beschaltung | 220R | 0805 | `C17557` | Status-LED 220 R |
| **R46** | ESP32-C6-MCU + Beschaltung | 1k | 0805 | `C17513` | Tank-LED 1 k |
| **SW1** | ESP32-C6-MCU + Beschaltung | SW-SMD | SMD-4P 5.1x5.1 | `C318884` | Reset-Taster |
| **SW2** | ESP32-C6-MCU + Beschaltung | SW-SMD | SMD-4P 5.1x5.1 | `C318884` | Boot-Taster |
| **TP2** | ESP32-C6-MCU + Beschaltung | 5010-Testpoint | - | - | Testpad RXD0 |
| **U1** | ESP32-C6-MCU + Beschaltung | ESP32-C6-MINI-1 | SMD-53P | `C5736265` | ESP32-C6-MINI-1 WLAN-Modul |
| **C11** | Pumpentreiber Dosier- + Sauerstoffpumpe | 100nF | 0805 | `C49678` | EMI an den Pumpenklemmen 100 nF |
| **C24** | Pumpentreiber Dosier- + Sauerstoffpumpe | 100nF | 0805 | `C49678` | EMI an den Klemmen Sauerstoffpumpe 100 nF |
| **D1** | Pumpentreiber Dosier- + Sauerstoffpumpe | 1N5819WS | SOD-323 | `C191023` | Freilaufdiode Dosierpumpe |
| **D3** | Pumpentreiber Dosier- + Sauerstoffpumpe | 1N5819WS | SOD-323 | `C191023` | Klemmzweig-Diode Dosierpumpe |
| **D4** | Pumpentreiber Dosier- + Sauerstoffpumpe | 1N5819WS | SOD-323 | `C191023` | Freilaufdiode Sauerstoffpumpe |
| **D8** | Pumpentreiber Dosier- + Sauerstoffpumpe | 1N5819WS | SOD-323 | `C191023` | Klemmzweig-Diode Sauerstoffpumpe |
| **J16** | Pumpentreiber Dosier- + Sauerstoffpumpe | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Sauerstoffpumpe JST-XH 2P, aufrecht |
| **J4** | Pumpentreiber Dosier- + Sauerstoffpumpe | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Dosierpumpe JST-XH 2P, aufrecht |
| **Q1** | Pumpentreiber Dosier- + Sauerstoffpumpe | AO3400A | SOT-23 | `C20917` | N-MOSFET Pumpentreiber Dosierpumpe |
| **Q5** | Pumpentreiber Dosier- + Sauerstoffpumpe | AO3400A | SOT-23 | `C20917` | N-MOSFET Sauerstoffpumpe |
| **R1** | Pumpentreiber Dosier- + Sauerstoffpumpe | 1k | 0805 | `C17513` | Gate-Serie 1 k |
| **R2** | Pumpentreiber Dosier- + Sauerstoffpumpe | 47k | 0805 | `C17713` | Gate-Pulldown 47 k |
| **R29** | Pumpentreiber Dosier- + Sauerstoffpumpe | 10k | 0805 | `C17414` | Klemmzweig-Serie 10 k Dosierpumpe |
| **R30** | Pumpentreiber Dosier- + Sauerstoffpumpe | 10k | 0805 | `C17414` | Klemmzweig-Serie 10 k Sauerstoffpumpe |
| **R31** | Pumpentreiber Dosier- + Sauerstoffpumpe | 1k | 0805 | `C17513` | Gate-Serie 1 k Kanal 2 |
| **R32** | Pumpentreiber Dosier- + Sauerstoffpumpe | 47k | 0805 | `C17713` | Gate-Pulldown 47 k Kanal 2 |
| **C17** | Akku-Schutz (HY2120-CB + PSMN4R2) | 100nF | 0805 | `C49678` | VDD-Filter 100 nF nach Pack-Minus |
| **C18** | Akku-Schutz (HY2120-CB + PSMN4R2) | 100nF | 0805 | `C49678` | VC-Filter 100 nF nach Pack-Minus |
| **Q3** | Akku-Schutz (HY2120-CB + PSMN4R2) | PSMN4R2-30MLDX | LFPAK33-8 | `C179452` | Entlade-MOSFET PSMN4R2-30MLDX |
| **Q4** | Akku-Schutz (HY2120-CB + PSMN4R2) | PSMN4R2-30MLDX | LFPAK33-8 | `C179452` | Lade-MOSFET PSMN4R2-30MLDX |
| **R15** | Akku-Schutz (HY2120-CB + PSMN4R2) | 330R | 0805 | `C17630` | 330 R zum VC-Pin des Schutz-IC |
| **R16** | Akku-Schutz (HY2120-CB + PSMN4R2) | 100R | 0805 | `C17408` | Balancing-Widerstand 100 R zum Mittelabgriff |
| **R17** | Akku-Schutz (HY2120-CB + PSMN4R2) | 330R | 0805 | `C17630` | 330 R zum VDD-Pin des Schutz-IC |
| **R18** | Akku-Schutz (HY2120-CB + PSMN4R2) | 2k | 0805 | `C17604` | CS-Widerstand 2 k zum Board-GND |
| **U5** | Akku-Schutz (HY2120-CB + PSMN4R2) | HY2120-CB | SOT-23-6 | `C116509` | 2-Zellen-Schutz-IC HY2120-CB |
| **J17** | Sensor-Eingang | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | 5-V-Ausgang fuer Sensorik JST-XH 2P |
| **J2** | Sensor-Eingang | JST-XH-3P | THT P2.5 aufrecht (Top-Entry) | `C5258884` | Feuchtesensor JST-XH 3P, aufrecht |
| **R6** | Sensor-Eingang | 1k | 0805 | `C17513` | Sensor-AOUT Serie 1 k |
| **TP6** | Sensor-Eingang | 5010-Testpoint | - | - | Testpad SENSOR_AOUT |
| **C32** | Taster & LEDs | 100nF | 0805 | `C49678` | Taster-Entprellung 100 nF |
| **J6** | Taster & LEDs | HDR-TH 2P, 2,54 mm | 2x Loch 1.0mm Raster 2.54mm | - | 2 Loetpads externer Taster |
| **R24** | Taster & LEDs | 10k | 0805 | `C17414` | Taster-Pull-up 10 k |
| **J5** | USB-C Eingang & ESD | USB-C-16P | SMD | `C165948` | USB-C 16P Buchse (Laden + Programmieren) |
| **R8** | USB-C Eingang & ESD | 5.1k | 0805 | `C27834` | CC1-Pulldown 5,1 k |
| **R9** | USB-C Eingang & ESD | 5.1k | 0805 | `C27834` | CC2-Pulldown 5,1 k |
| **U6** | USB-C Eingang & ESD | USBLC6-2SC6 | SOT-23-6L | `C7519` | USB-ESD-Schutz USBLC6-2SC6 |
| **C12** | Unterspannungswaechter (TPS3839) | 100nF | 0805 | `C49678` | Decoupling Waechter 100 nF |
| **R13** | Unterspannungswaechter (TPS3839) | 200k | 0805 | `C17539` | UVLO-Teiler oben 200 k |
| **R28** | Unterspannungswaechter (TPS3839) | 200k | 0805 | `C17539` | UVLO-Teiler unten 200 k |
| **U7** | Unterspannungswaechter (TPS3839) | TPS3839G33DBZR | SOT-23-3 | `C485802` | Unterspannungswaechter TPS3839G33 (3,08 V) |

## 3. Wie ist verkabelt (jedes Netz mit jedem Pin)

### `+3V3`

Rolle: power | Pins: 16

- `C13:1` - ESP32-C6-MCU + Beschaltung
- `C2:1` - ESP32-C6-MCU + Beschaltung
- `C26:1` - 3V3-Buck (AP63203)
- `C27:1` - 3V3-Buck (AP63203)
- `C28:1` - ESP32-C6-MCU + Beschaltung
- `C29:1` - ESP32-C6-MCU + Beschaltung
- `L3:2` - 3V3-Buck (AP63203)
- `Q2:2` (S) - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R21:1` - ESP32-C6-MCU + Beschaltung
- `R22:1` - ESP32-C6-MCU + Beschaltung
- `R23:1` - ESP32-C6-MCU + Beschaltung
- `R24:1` - Taster & LEDs
- `R25:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R26:1` - 3V3-Buck (AP63203)
- `TP5:1` - 3V3-Buck (AP63203)
- `U1:3` (3V3) - ESP32-C6-MCU + Beschaltung

### `+5V`

Rolle: power | Pins: 12

- `C11:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `C22:1` - 5-V-Buck (SY8113B)
- `C23:1` - 5-V-Buck (SY8113B)
- `C24:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `C3:1` - Akku & Puffer
- `D1:1` (K) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `D4:1` (K) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `J16:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `J17:1` - Sensor-Eingang
- `J4:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `L2:2` - 5-V-Buck (SY8113B)
- `R19:1` - 5-V-Buck (SY8113B)

### `VBAT`

Rolle: power | Pins: 15

- `C14:1` - 5-V-Buck (SY8113B)
- `C15:1` - 3V3-Buck (AP63203)
- `C16:1` - 3V3-Buck (AP63203)
- `C7:1` - Laden (IP2326, 2S)
- `C8:1` - 5-V-Buck (SY8113B)
- `J1:3` - Akku & Puffer
- `R13:1` - Unterspannungswaechter (TPS3839)
- `R14:1` - ESP32-C6-MCU + Beschaltung
- `R17:1` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `TP4:1` - Akku & Puffer
- `U2:21` (VOUT) - Laden (IP2326, 2S)
- `U2:22` (VOUT) - Laden (IP2326, 2S)
- `U3:5` (IN) - 5-V-Buck (SY8113B)
- `U4:2` (EN) - 3V3-Buck (AP63203)
- `U4:3` (VIN) - 3V3-Buck (AP63203)

### `VBUS`

Rolle: power | Pins: 8

- `C1:1` - Laden (IP2326, 2S)
- `J5:A4B9` (VBUS) - USB-C Eingang & ESD
- `J5:B4A9` (VBUS) - USB-C Eingang & ESD
- `L1:1` - Laden (IP2326, 2S)
- `R3:1` - Laden (IP2326, 2S)
- `R5:1` - Laden (IP2326, 2S)
- `R7:1` - Laden (IP2326, 2S)
- `U6:5` - USB-C Eingang & ESD

### `VBUS_CHG`

Rolle: signal | Pins: 3

- `C5:1` - Laden (IP2326, 2S)
- `R3:2` - Laden (IP2326, 2S)
- `U2:13` (VIN) - Laden (IP2326, 2S)

### `VSYS_CHG`

Rolle: signal | Pins: 4

- `C19:1` - Laden (IP2326, 2S)
- `C20:1` - Laden (IP2326, 2S)
- `U2:19` (VSYS) - Laden (IP2326, 2S)
- `U2:20` (VSYS) - Laden (IP2326, 2S)

### `BAT_MINUS`

Rolle: ground | Pins: 8

- `C17:2` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `C18:2` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `J1:1` - Akku & Puffer
- `Q3:1` (S) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `Q3:2` (S) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `Q3:3` (S) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U2:24` (VBAT_GND) - Laden (IP2326, 2S)
- `U5:6` (VSS) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `VCC_EXT`

Rolle: signal | Pins: 10

- `J10:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J11:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J12:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J13:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J15:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J8:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J9:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `Q2:3` (D) - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R37:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R39:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `GND`

Rolle: ground | Pins: 93

- `C1:2` - Laden (IP2326, 2S)
- `C10:2` - ESP32-C6-MCU + Beschaltung
- `C12:2` - Unterspannungswaechter (TPS3839)
- `C13:2` - ESP32-C6-MCU + Beschaltung
- `C14:2` - 5-V-Buck (SY8113B)
- `C15:2` - 3V3-Buck (AP63203)
- `C16:2` - 3V3-Buck (AP63203)
- `C19:2` - Laden (IP2326, 2S)
- `C2:2` - ESP32-C6-MCU + Beschaltung
- `C20:2` - Laden (IP2326, 2S)
- `C22:2` - 5-V-Buck (SY8113B)
- `C23:2` - 5-V-Buck (SY8113B)
- `C26:2` - 3V3-Buck (AP63203)
- `C27:2` - 3V3-Buck (AP63203)
- `C28:2` - ESP32-C6-MCU + Beschaltung
- `C29:2` - ESP32-C6-MCU + Beschaltung
- `C3:2` - Akku & Puffer
- `C30:2` - Lichtsensor-Eingang
- `C31:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `C32:2` - Taster & LEDs
- `C4:2` - ESP32-C6-MCU + Beschaltung
- `C5:2` - Laden (IP2326, 2S)
- `C7:2` - Laden (IP2326, 2S)
- `C8:2` - 5-V-Buck (SY8113B)
- `C9:2` - ESP32-C6-MCU + Beschaltung
- `D2:2` (K) - ESP32-C6-MCU + Beschaltung
- `D5:1` (-) - ESP32-C6-MCU + Beschaltung
- `J10:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J11:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J12:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J13:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J15:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J17:2` - Sensor-Eingang
- `J2:1` - Sensor-Eingang
- `J5:1` (EH) - USB-C Eingang & ESD
- `J5:2` (EH) - USB-C Eingang & ESD
- `J5:3` (EH) - USB-C Eingang & ESD
- `J5:4` (EH) - USB-C Eingang & ESD
- `J5:A1B12` (GND) - USB-C Eingang & ESD
- `J5:B1A12` (GND) - USB-C Eingang & ESD
- `J6:2` - Taster & LEDs
- `J7:1` - Lichtsensor-Eingang
- `J8:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `J9:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `Q1:2` (S) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `Q4:1` (S) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `Q4:2` (S) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `Q4:3` (S) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `Q5:2` (S) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R10:2` - Laden (IP2326, 2S)
- `R11:2` - Laden (IP2326, 2S)
- `R12:2` - Laden (IP2326, 2S)
- `R18:2` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `R2:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R20:2` - 5-V-Buck (SY8113B)
- `R27:2` - 3V3-Buck (AP63203)
- `R28:2` - Unterspannungswaechter (TPS3839)
- `R32:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R33:2` - ESP32-C6-MCU + Beschaltung
- `R34:2` - Lichtsensor-Eingang
- `R8:2` - USB-C Eingang & ESD
- `R9:2` - USB-C Eingang & ESD
- `SW1:2` (B) - ESP32-C6-MCU + Beschaltung
- `SW2:2` (B) - ESP32-C6-MCU + Beschaltung
- `TP3:1` - Akku & Puffer
- `U1:1` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:11` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:14` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:2` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:36` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:37` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:38` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:39` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:40` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:41` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:42` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:43` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:44` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:45` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:46` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:47` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:48` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:49` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:50` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:51` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:52` (GND) - ESP32-C6-MCU + Beschaltung
- `U1:53` (GND) - ESP32-C6-MCU + Beschaltung
- `U2:18` (PGND) - Laden (IP2326, 2S)
- `U2:25` (EP) - Laden (IP2326, 2S)
- `U3:2` (GND) - 5-V-Buck (SY8113B)
- `U4:4` (GND) - 3V3-Buck (AP63203)
- `U6:2` - USB-C Eingang & ESD
- `U7:1` (GND) - Unterspannungswaechter (TPS3839)

### `BOOT`

Rolle: signal | Pins: 3

- `R22:2` - ESP32-C6-MCU + Beschaltung
- `SW2:1` (A) - ESP32-C6-MCU + Beschaltung
- `U1:23` (IO9) - ESP32-C6-MCU + Beschaltung

### `BST_3V3`

Rolle: signal | Pins: 2

- `C25:1` - 3V3-Buck (AP63203)
- `U4:6` (BST) - 3V3-Buck (AP63203)

### `BST_5V`

Rolle: signal | Pins: 2

- `C21:1` - 5-V-Buck (SY8113B)
- `U3:1` (BS) - 5-V-Buck (SY8113B)

### `BST_CHG`

Rolle: signal | Pins: 2

- `C6:1` - Laden (IP2326, 2S)
- `U2:14` (BST) - Laden (IP2326, 2S)

### `BTN`

Rolle: signal | Pins: 4

- `C32:1` - Taster & LEDs
- `J6:1` - Taster & LEDs
- `R24:2` - Taster & LEDs
- `U1:15` (IO6) - ESP32-C6-MCU + Beschaltung

### `CC1`

Rolle: signal | Pins: 2

- `J5:A5` (CC1) - USB-C Eingang & ESD
- `R8:1` - USB-C Eingang & ESD

### `CC2`

Rolle: signal | Pins: 2

- `J5:B5` (CC2) - USB-C Eingang & ESD
- `R9:1` - USB-C Eingang & ESD

### `EN`

Rolle: signal | Pins: 4

- `C4:1` - ESP32-C6-MCU + Beschaltung
- `R21:2` - ESP32-C6-MCU + Beschaltung
- `SW1:1` (A) - ESP32-C6-MCU + Beschaltung
- `U1:8` (EN) - ESP32-C6-MCU + Beschaltung

### `EN_CHG`

Rolle: signal | Pins: 2

- `R7:2` - Laden (IP2326, 2S)
- `U2:12` (EN) - Laden (IP2326, 2S)

### `EXT_EN`

Rolle: signal | Pins: 3

- `Q2:1` (G) - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R25:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:26` (IO20) - ESP32-C6-MCU + Beschaltung

### `FB_3V3`

Rolle: signal | Pins: 3

- `R26:2` - 3V3-Buck (AP63203)
- `R27:1` - 3V3-Buck (AP63203)
- `U4:1` (FB) - 3V3-Buck (AP63203)

### `FB_5V`

Rolle: signal | Pins: 3

- `R19:2` - 5-V-Buck (SY8113B)
- `R20:1` - 5-V-Buck (SY8113B)
- `U3:3` (FB) - 5-V-Buck (SY8113B)

### `GATE`

Rolle: signal | Pins: 4

- `Q1:1` (G) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R1:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R2:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R29:1` - Pumpentreiber Dosier- + Sauerstoffpumpe

### `GATE2`

Rolle: signal | Pins: 4

- `Q5:1` (G) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R30:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R31:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R32:1` - Pumpentreiber Dosier- + Sauerstoffpumpe

### `GPIO8_STRAP`

Rolle: signal | Pins: 2

- `R23:2` - ESP32-C6-MCU + Beschaltung
- `U1:22` (IO8) - ESP32-C6-MCU + Beschaltung

### `ISET_CHG`

Rolle: signal | Pins: 2

- `R10:1` - Laden (IP2326, 2S)
- `U2:11` (ISET) - Laden (IP2326, 2S)

### `KLAMP1`

Rolle: signal | Pins: 2

- `D3:2` (A) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R29:2` - Pumpentreiber Dosier- + Sauerstoffpumpe

### `KLAMP2`

Rolle: signal | Pins: 2

- `D8:2` (A) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `R30:2` - Pumpentreiber Dosier- + Sauerstoffpumpe

### `LED_CHG`

Rolle: signal | Pins: 2

- `LED1:2` (+) - Laden (IP2326, 2S)
- `R5:2` - Laden (IP2326, 2S)

### `LED_STAT`

Rolle: signal | Pins: 2

- `R4:1` - ESP32-C6-MCU + Beschaltung
- `U1:19` (IO14) - ESP32-C6-MCU + Beschaltung

### `LED_STAT_A`

Rolle: signal | Pins: 2

- `D2:1` (A) - ESP32-C6-MCU + Beschaltung
- `R4:2` - ESP32-C6-MCU + Beschaltung

### `LED_TANK`

Rolle: signal | Pins: 2

- `R46:1` - ESP32-C6-MCU + Beschaltung
- `U1:16` (IO7) - ESP32-C6-MCU + Beschaltung

### `LED_TANK_A`

Rolle: signal | Pins: 2

- `D5:2` (+) - ESP32-C6-MCU + Beschaltung
- `R46:2` - ESP32-C6-MCU + Beschaltung

### `LIGHT_AOUT`

Rolle: signal | Pins: 3

- `C30:1` - Lichtsensor-Eingang
- `R35:2` - Lichtsensor-Eingang
- `U1:9` (IO4) - ESP32-C6-MCU + Beschaltung

### `LIGHT_RAW`

Rolle: signal | Pins: 3

- `J7:3` - Lichtsensor-Eingang
- `R34:1` - Lichtsensor-Eingang
- `R35:1` - Lichtsensor-Eingang

### `LX_3V3`

Rolle: signal | Pins: 3

- `C25:2` - 3V3-Buck (AP63203)
- `L3:1` - 3V3-Buck (AP63203)
- `U4:5` (SW) - 3V3-Buck (AP63203)

### `LX_5V`

Rolle: signal | Pins: 3

- `C21:2` - 5-V-Buck (SY8113B)
- `L2:1` - 5-V-Buck (SY8113B)
- `U3:6` (LX) - 5-V-Buck (SY8113B)

### `LX_CHG`

Rolle: signal | Pins: 5

- `C6:2` - Laden (IP2326, 2S)
- `L1:2` - Laden (IP2326, 2S)
- `U2:15` (LX) - Laden (IP2326, 2S)
- `U2:16` (LX) - Laden (IP2326, 2S)
- `U2:17` (LX) - Laden (IP2326, 2S)

### `MID`

Rolle: signal | Pins: 3

- `J1:2` - Akku & Puffer
- `R15:1` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `R16:1` - Akku-Schutz (HY2120-CB + PSMN4R2)

### `NTC_DIS`

Rolle: signal | Pins: 2

- `R11:1` - Laden (IP2326, 2S)
- `U2:4` (NTC) - Laden (IP2326, 2S)

### `PROT_COMMON`

Rolle: signal | Pins: 2

- `Q3:5` (D) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `Q4:5` (D) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `PROT_CS`

Rolle: signal | Pins: 2

- `R18:1` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U5:3` (CS) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `PROT_GATE_C`

Rolle: signal | Pins: 2

- `Q4:4` (G) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U5:2` (OC) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `PROT_GATE_D`

Rolle: signal | Pins: 2

- `Q3:4` (G) - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U5:1` (OD) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `PROT_VC`

Rolle: signal | Pins: 3

- `C18:1` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `R15:2` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U5:4` (VC) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `PROT_VDD`

Rolle: signal | Pins: 3

- `C17:1` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `R17:2` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U5:5` (VDD) - Akku-Schutz (HY2120-CB + PSMN4R2)

### `PUMP2_EN`

Rolle: signal | Pins: 2

- `R31:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `U1:28` (IO22) - ESP32-C6-MCU + Beschaltung

### `PUMP2_N`

Rolle: signal | Pins: 4

- `C24:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `D4:2` (A) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `J16:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `Q5:3` (D) - Pumpentreiber Dosier- + Sauerstoffpumpe

### `PUMP_EN`

Rolle: signal | Pins: 2

- `R1:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `U1:5` (IO2) - ESP32-C6-MCU + Beschaltung

### `PUMP_N`

Rolle: signal | Pins: 4

- `C11:1` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `D1:2` (A) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `J4:2` - Pumpentreiber Dosier- + Sauerstoffpumpe
- `Q1:3` (D) - Pumpentreiber Dosier- + Sauerstoffpumpe

### `RESET_UV`

Rolle: signal | Pins: 4

- `D3:1` (K) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `D8:1` (K) - Pumpentreiber Dosier- + Sauerstoffpumpe
- `U3:4` (EN) - 5-V-Buck (SY8113B)
- `U7:2` (RESET#) - Unterspannungswaechter (TPS3839)

### `SCL`

Rolle: signal | Pins: 3

- `J8:4` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R38:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R39:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SCL_MCU`

Rolle: signal | Pins: 2

- `R38:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:25` (IO19) - ESP32-C6-MCU + Beschaltung

### `SDA`

Rolle: signal | Pins: 3

- `J8:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R36:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R37:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SDA_MCU`

Rolle: signal | Pins: 2

- `R36:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:24` (IO18) - ESP32-C6-MCU + Beschaltung

### `SENSOR_AOUT`

Rolle: signal | Pins: 4

- `C9:1` - ESP32-C6-MCU + Beschaltung
- `R6:2` - Sensor-Eingang
- `TP6:1` - Sensor-Eingang
- `U1:12` (IO0) - ESP32-C6-MCU + Beschaltung

### `SENSOR_PWR`

Rolle: signal | Pins: 3

- `J2:2` - Sensor-Eingang
- `J7:2` - Lichtsensor-Eingang
- `U1:6` (IO3) - ESP32-C6-MCU + Beschaltung

### `SENSOR_RAW`

Rolle: signal | Pins: 2

- `J2:3` - Sensor-Eingang
- `R6:1` - Sensor-Eingang

### `SPARE_AIN`

Rolle: signal | Pins: 3

- `C31:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R40:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:10` (IO5) - ESP32-C6-MCU + Beschaltung

### `SPARE_AIN_RAW`

Rolle: signal | Pins: 2

- `J9:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R40:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SPARE_IO15`

Rolle: signal | Pins: 2

- `R41:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:20` (IO15) - ESP32-C6-MCU + Beschaltung

### `SPARE_IO15_RAW`

Rolle: signal | Pins: 2

- `J10:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R41:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SPARE_IO16`

Rolle: signal | Pins: 2

- `J11:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R42:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SPARE_IO17`

Rolle: signal | Pins: 2

- `J12:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R43:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SPARE_IO21`

Rolle: signal | Pins: 2

- `R44:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:27` (IO21) - ESP32-C6-MCU + Beschaltung

### `SPARE_IO21_RAW`

Rolle: signal | Pins: 2

- `J13:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R44:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `SPARE_IO23`

Rolle: signal | Pins: 2

- `R45:2` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `U1:29` (IO23) - ESP32-C6-MCU + Beschaltung

### `SPARE_IO23_RAW`

Rolle: signal | Pins: 2

- `J15:3` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R45:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch

### `STAT_CHG`

Rolle: signal | Pins: 2

- `LED1:1` (-) - Laden (IP2326, 2S)
- `U2:6` (LED) - Laden (IP2326, 2S)

### `UART_RX`

Rolle: signal | Pins: 3

- `R43:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `TP2:1` - ESP32-C6-MCU + Beschaltung
- `U1:30` (RXD0) - ESP32-C6-MCU + Beschaltung

### `UART_TP`

Rolle: signal | Pins: 2

- `R47:2` - UART-Debug-Pads (DNP)
- `TP1:1` - UART-Debug-Pads (DNP)

### `UART_TX`

Rolle: signal | Pins: 3

- `R42:1` - Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch
- `R47:1` - UART-Debug-Pads (DNP)
- `U1:31` (TXD0) - ESP32-C6-MCU + Beschaltung

### `USB_DM`

Rolle: signal | Pins: 5

- `J5:A7` (DN1) - USB-C Eingang & ESD
- `J5:B7` (DN2) - USB-C Eingang & ESD
- `U1:17` (IO12) - ESP32-C6-MCU + Beschaltung
- `U6:3` - USB-C Eingang & ESD
- `U6:4` - USB-C Eingang & ESD

### `USB_DP`

Rolle: signal | Pins: 5

- `J5:A6` (DP1) - USB-C Eingang & ESD
- `J5:B6` (DP2) - USB-C Eingang & ESD
- `U1:18` (IO13) - ESP32-C6-MCU + Beschaltung
- `U6:1` - USB-C Eingang & ESD
- `U6:6` - USB-C Eingang & ESD

### `UVSET_CHG`

Rolle: signal | Pins: 2

- `R12:1` - Laden (IP2326, 2S)
- `U2:8` (VIN_UVSET) - Laden (IP2326, 2S)

### `UV_REF`

Rolle: signal | Pins: 4

- `C12:1` - Unterspannungswaechter (TPS3839)
- `R13:2` - Unterspannungswaechter (TPS3839)
- `R28:1` - Unterspannungswaechter (TPS3839)
- `U7:3` (VDD) - Unterspannungswaechter (TPS3839)

### `VBATM_CHG`

Rolle: signal | Pins: 2

- `R16:2` - Akku-Schutz (HY2120-CB + PSMN4R2)
- `U2:23` (VBATM) - Laden (IP2326, 2S)

### `VBAT_SENSE`

Rolle: signal | Pins: 4

- `C10:1` - ESP32-C6-MCU + Beschaltung
- `R14:2` - ESP32-C6-MCU + Beschaltung
- `R33:1` - ESP32-C6-MCU + Beschaltung
- `U1:13` (IO1) - ESP32-C6-MCU + Beschaltung

## 4. Wo ist was (Bloecke auf dem Blatt, Koordinaten in 0,01 Zoll)

| Block / Modul | Rahmen x0..x1 | y0..y1 | Titel | Mitglieder |
|---|---|---|---|---|
| **USB** | 1855..2450 | 12..1006 | USB-C Eingang & ESD | J5, R8, R9, U6 |
| **LADER** | 1855..2577 | 1006..1943 | Laden (IP2326, 2S) | C1, C19, C20, C5, C6, C7, L1, LED1, R10, R11, R12, R3, R5, R7, U2 |
| **DEBUG** | 12..469 | 1863..2326 | UART-Debug-Pads (DNP) | R47, TP1 |
| **MCU** | 12..970 | 12..1063 | ESP32-C6-MCU + Beschaltung | C10, C13, C2, C28, C29, C4, C9, D2, D5, R14, R21, R22, R23, R33, R4, R46, SW1, SW2, TP2, U1 |
| **WAEChTER** | 2602..3234 | 1809..2300 | Unterspannungswaechter (TPS3839) | C12, R13, R28, U7 |
| **SCHUTZ** | 1120..1807 | 1650..2304 | Akku-Schutz (HY2120-CB + PSMN4R2) | C17, C18, Q3, Q4, R15, R16, R17, R18, U5 |
| **LDO** | 2602..3243 | 713..1328 | 3V3-Buck (AP63203) | C15, C16, C25, C26, C27, L3, R26, R27, TP5, U4 |
| **AKKU** | 2602..3013 | 1328..1809 | Akku & Puffer | C3, J1, TP3, TP4 |
| **SENSOR** | 2602..3252 | 198..713 | Sensor-Eingang | J17, J2, R6, TP6 |
| **PUMPE** | 12..1120 | 1063..1863 | Pumpentreiber Dosier- + Sauerstoffpumpe | C11, C24, D1, D3, D4, D8, J16, J4, Q1, Q5, R1, R2, R29, R30, R31, R32 |
| **BOOST** | 1120..1803 | 1059..1650 | 5-V-Buck (SY8113B) | C14, C21, C22, C23, C8, L2, R19, R20, U3 |
| **TASTER** | 1807..2417 | 1943..2311 | Taster & LEDs | C32, J6, R24 |
| **ERWEITERUNG** | 970..1855 | 12..1059 | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch | C31, J10, J11, J12, J13, J15, J8, J9, Q2, R25, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45 |
| **LICHT** | 469..1115 | 1863..2317 | Lichtsensor-Eingang | C30, J7, R34, R35 |

## 5. Anschluesse

### J1 - Akku JST-XH 3P (B-/MID/B+), aufrecht

| Pin | Netz | wozu |
|---|---|---|
| 1 | BAT_MINUS | Akku & Puffer |
| 2 | MID | Akku & Puffer |
| 3 | VBAT | Akku & Puffer |

### J10 - Reserve IO15 Stiftleiste 1x3

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SPARE_IO15_RAW | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### J11 - Reserve IO16 (TXD0) Stiftleiste 1x3

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SPARE_IO16 | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### J12 - Reserve IO17 (RXD0) Stiftleiste 1x3

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SPARE_IO17 | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### J13 - Reserve IO21 Stiftleiste 1x3

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SPARE_IO21_RAW | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### J15 - Reserve IO23 Stiftleiste 1x3

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SPARE_IO23_RAW | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### J16 - Sauerstoffpumpe JST-XH 2P, aufrecht

| Pin | Netz | wozu |
|---|---|---|
| 1 | +5V | Pumpentreiber Dosier- + Sauerstoffpumpe |
| 2 | PUMP2_N | Pumpentreiber Dosier- + Sauerstoffpumpe |

### J17 - 5-V-Ausgang fuer Sensorik JST-XH 2P

| Pin | Netz | wozu |
|---|---|---|
| 1 | +5V | Sensor-Eingang |
| 2 | GND | Sensor-Eingang |

### J2 - Feuchtesensor JST-XH 3P, aufrecht

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Sensor-Eingang |
| 2 | SENSOR_PWR | Sensor-Eingang |
| 3 | SENSOR_RAW | Sensor-Eingang |

### J4 - Dosierpumpe JST-XH 2P, aufrecht

| Pin | Netz | wozu |
|---|---|---|
| 1 | +5V | Pumpentreiber Dosier- + Sauerstoffpumpe |
| 2 | PUMP_N | Pumpentreiber Dosier- + Sauerstoffpumpe |

### J5 - USB-C 16P Buchse (Laden + Programmieren)

| Pin | Netz | wozu |
|---|---|---|
| A1B12 | GND | USB-C Eingang & ESD |
| A4B9 | VBUS | USB-C Eingang & ESD |
| B8 | (frei / NC) | USB-C Eingang & ESD |
| A5 | CC1 | USB-C Eingang & ESD |
| B7 | USB_DM | USB-C Eingang & ESD |
| A6 | USB_DP | USB-C Eingang & ESD |
| A7 | USB_DM | USB-C Eingang & ESD |
| B6 | USB_DP | USB-C Eingang & ESD |
| A8 | (frei / NC) | USB-C Eingang & ESD |
| B5 | CC2 | USB-C Eingang & ESD |
| B4A9 | VBUS | USB-C Eingang & ESD |
| B1A12 | GND | USB-C Eingang & ESD |
| 4 | GND | USB-C Eingang & ESD |
| 3 | GND | USB-C Eingang & ESD |
| 2 | GND | USB-C Eingang & ESD |
| 1 | GND | USB-C Eingang & ESD |

### J6 - 2 Loetpads externer Taster

| Pin | Netz | wozu |
|---|---|---|
| 1 | BTN | Taster & LEDs |
| 2 | GND | Taster & LEDs |

### J7 - Lichtsensor-Stiftleiste 1x3 2,54 mm

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Lichtsensor-Eingang |
| 2 | SENSOR_PWR | Lichtsensor-Eingang |
| 3 | LIGHT_RAW | Lichtsensor-Eingang |

### J8 - I2C-Stiftleiste 1x4 (GND-VCC-SDA-SCL)

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SDA | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 4 | SCL | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### J9 - Reserve-Analog Stiftleiste 1x3 (IO5)

| Pin | Netz | wozu |
|---|---|---|
| 1 | GND | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 2 | VCC_EXT | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |
| 3 | SPARE_AIN_RAW | Erweiterung: Stiftleisten (GND–VCC–SIG) + Load-Switch |

### Testpunkte

| Ref | Netz | Modul |
|---|---|---|
| TP1 | UART_TP | UART-Debug-Pads (DNP) |
| TP2 | UART_RX | ESP32-C6-MCU + Beschaltung |
| TP3 | GND | Akku & Puffer |
| TP4 | VBAT | Akku & Puffer |
| TP5 | +3V3 | 3V3-Buck (AP63203) |
| TP6 | SENSOR_AOUT | Sensor-Eingang |

## 6. MCU-Pinbelegung (U1, ESP32-C6-MINI-1)

| Pin | Symbolname | Netz |
|---|---|---|
| 1 | GND | GND |
| 2 | GND | GND |
| 3 | 3V3 | +3V3 |
| 4 | NC | (frei / NC) |
| 5 | IO2 | PUMP_EN |
| 6 | IO3 | SENSOR_PWR |
| 7 | NC | (frei / NC) |
| 8 | EN | EN |
| 9 | IO4 | LIGHT_AOUT |
| 10 | IO5 | SPARE_AIN |
| 11 | GND | GND |
| 12 | IO0 | SENSOR_AOUT |
| 13 | IO1 | VBAT_SENSE |
| 14 | GND | GND |
| 15 | IO6 | BTN |
| 16 | IO7 | LED_TANK |
| 17 | IO12 | USB_DM |
| 18 | IO13 | USB_DP |
| 19 | IO14 | LED_STAT |
| 20 | IO15 | SPARE_IO15 |
| 21 | NC | (frei / NC) |
| 22 | IO8 | GPIO8_STRAP |
| 23 | IO9 | BOOT |
| 24 | IO18 | SDA_MCU |
| 25 | IO19 | SCL_MCU |
| 26 | IO20 | EXT_EN |
| 27 | IO21 | SPARE_IO21 |
| 28 | IO22 | PUMP2_EN |
| 29 | IO23 | SPARE_IO23 |
| 30 | RXD0 | UART_RX |
| 31 | TXD0 | UART_TX |
| 32 | NC | (frei / NC) |
| 33 | NC | (frei / NC) |
| 34 | NC | (frei / NC) |
| 35 | NC | (frei / NC) |
| 36 | GND | GND |
| 37 | GND | GND |
| 38 | GND | GND |
| 39 | GND | GND |
| 40 | GND | GND |
| 41 | GND | GND |
| 42 | GND | GND |
| 43 | GND | GND |
| 44 | GND | GND |
| 45 | GND | GND |
| 46 | GND | GND |
| 47 | GND | GND |
| 48 | GND | GND |
| 49 | GND | GND |
| 50 | GND | GND |
| 51 | GND | GND |
| 52 | GND | GND |
| 53 | GND | GND |

## 7. Betriebs- und Randbedingungen

### 7.1 Protokoll der Design-Pruefsuite (gerechnete Werte gegen Grenzwerte)

```
FEHLER: Pin 'mb (Drain)' an Q_PROT1 fehlt in der Netzliste
```

### 7.2 Bewusste Eigenheiten der Schaltung

- **Pack-Minus ist nicht Board-Masse.** Zwischen BAT_MINUS (J1 Pin 1) und GND liegt das
  Schutz-MOSFET-Paar (Q3 = Entlader, Q4 = Lader, gemeinsamer Drain auf PROT_COMMON).
  Der gesamte Systemstrom laeuft darueber.
- **J1 ist 3-polig**: 1 = Pack-Minus, 2 = Mittelabgriff, 3 = Pack-Plus. Erst der Mittelabgriff
  erlaubt Zellschutz (HY2120 VC-Pin) und Balancieren (IP2326 Pin 23 ueber R_CB).
- **Kein Power-Path**: der IP2326 hat keinen; geladen wird ueber VOUT direkt in den Pack.
- **Laden startet ohne Firmware**: EN des IP2326 haengt ueber R7 (100 k) an VBUS.
- **Die 3,3-V-Schiene ist immer an** (U4 EN fest an VIN), damit die MCU auch im Waechterfall lebt.
- **Die 5-V-Schiene schaltet der Waechter ab** (U7 RESET treibt U3 EN und klemmt ueber D3/D8
  beide Pumpengates). Der 5-V-Buck braucht danach ~0,8 ms Sanftanlauf plus 200 ms Reset-Delay.
- **Steckerordnung 3-polig immer GND - VCC - SIG** (VCC auf dem mittleren Pin); 4-polig I2C als
  GND - VCC - SDA - SCL; in **jeder** Signalleitung liegt 1 k in Reihe.
- **Freie Pins sind ausdruecklich als NC markiert** (J5 A8/B8, SW1/SW2 3/4, U1 4/7/21/32-35,
  U2 1/2/3/5/7/9/10) - der IP2326 wird bewusst ohne DM/DP, VSET, BAT_STAT, TIME_SET, VIN_OVSET
  und CON_SEL betrieben (VSET offen = 8,4 V, CON_SEL offen = 2S).

### 7.3 Offene Punkte fuer einen externen Review

- Ueberstromschwelle des Schutzes (~17 A) gegen den Pumpenanlauf (~2,6 A aus dem Pack): Reserve
  bewusst gross; im Aufbau nachmessen.
- Ausloeseschwellen des HY2120 am Aufbau pruefen (4,28 V Ueberladung, 2,90 V Tiefentladung/Zelle).
- Balancing-Strom ueber R_CB (100 R) messen.
- Mechanik: der Pack ist jetzt 3-polig; Einbauort und Bauform in `docs/02` nachziehen.

