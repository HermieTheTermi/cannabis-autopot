# SmartGrowTopf_V1 - vollstaendige Schaltungsbeschreibung (Maschinenfassung)

Stand 16.09.2026, **inklusive der Nachbesserungen aus dem externen Review** (siehe
`docs/12_review-nachbesserungen.md`). Erzeugt **maschinell aus der Netzliste**
(`hardware/schaltplan_v1_netzliste.csv`), der Stueckliste (`hardware/pcba_bom_jlc.csv`) und dem
Protokoll der Design-Pruefsuite (`hardware/design/report.py`). Keine Zahl ist abgetippt.

> Hinweis: Die EasyEDA-Bauseite wird erst im naechsten Durchgang auf diesen Stand gezogen; die
> Blockkoordinaten des Blatts (Abschnitt 4) sind daher noch der Stand vor dieser Runde.

## 1. Kennzahlen und Versorgungskette

| Kennzahl | Wert |
|---|---|
| Bauteile mit Bezeichner | **122** |
| Netze | **76** |
| Verbindungen (Pin -> Netz) | **342** |
| Module | **12** |
| Steckverbinder (J*) | **16** |
| Testpunkte (TP*) | **6** |

**Versorgungskette (2S):**

```
USB-C 5 V --> IP2326 (Boost-Lader, 8,4 V / 0,90 A) --> VBAT = 2S-Pack (6,0 - 8,4 V)
                                                            |
2S-Pack an J1 (3-polig: B- / Mittelabgriff / B+) --> F1 5 A traege
     --> HY2120-Schutz (Q3/Q4 in der Minusleitung; BAT_MINUS ist NICHT Board-GND)
                                                            |
                       +------------------------------------+------------------------------------+
                       |                                                                         |
          SY8113B-Buck 3 A --> +5 V                                  AP63203-Buck 2 A --> +3,3 V
          (Dosierpumpe J4, Sauerstoffpumpe J16,                       (ESP32-C6, Sensorik ueber
           Sensor-5-V-Ausgang J17)                                    Q_SENS, LEDs, I2C)

Akku-Temperatur: J18 (XH-2P) --> NTC 100 kOhm B3950 || 82 kOhm --> IP2326 Pin 4 (NTC)
     Schwellen 0 / 45 / 55 Grad C; Stecker ab ==> Lader laedt nicht (fail-safe)
```

In Worten: 5 V kommen ueber USB-C; der **IP2326** laedt daraus den 2S-Pack auf 8,4 V. Der Pack geht
ueber den **3-poligen Stecker J1** und die **Sicherung F1** auf die Platine. Der **HY2120** trennt
mit zwei MOSFETs Pack-Minus und Board-Masse und ueberwacht jede Zelle; der **IP2326** nutzt den
Mittelabgriff zusaetzlich zum Balancieren. Aus VBAT erzeugen zwei Abwaertswandler **+5 V** und
**+3,3 V**. Es gibt **keinen LDO** und keinen zusaetzlichen Aufwaertswandler fuer die Lastversorgung
(der IP2326 ist selbst ein Boost-Lader).

## 2. Was ist verbaut

| Ref | Modul | Typ / Wert | Gehaeuse | LCSC | Funktion |
|---|---|---|---|---|---|
| **C1a** | - | 100nF | 0805 | `C49678` | 100nF |
| **C1b** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_B3_BST** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_B3_IN** | - | 22uF 25V | 0805 | `C45783` | 22uF 25V |
| **C_B3_IN_HF** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_B3_OUT** | - | 22uF 25V | 0805 | `C45783` | 22uF 25V |
| **C_B3_OUT_HF** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_B5_BST** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_B5_IN** | - | 22uF 25V | 0805 | `C45783` | 22uF 25V |
| **C_B5_IN_HF** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_B5_OUT** | - | 22uF 25V | 0805 | `C45783` | 22uF 25V |
| **C_B5_OUT_HF** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_BST_CHG** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_BTN** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_CHG_IN** | - | 10uF 25V | 0805 | `C15850` | 10uF 25V |
| **C_CHG_OUT** | - | 10uF 25V | 0805 | `C15850` | 10uF 25V |
| **C_CHG_VIN** | - | 10uF 25V | 0805 | `C15850` | 10uF 25V |
| **C_LIGHT** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_PROT_VC** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_PROT_VDD** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_PUMP2_EMI** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_SPARE** | - | 100nF | 0805 | `C49678` | 100nF |
| **C_VSYS_A** | - | 22uF 25V | 0805 | `C45783` | 22uF 25V |
| **C_VSYS_B** | - | 22uF 25V | 0805 | `C45783` | 22uF 25V |
| **D_FLY2** | - | 1N5819WS | SOD-323 | `C191023` | 1N5819WS |
| **D_LEDCHG** | - | LED-RED | 0805 | `C84256` | LED-RED |
| **L_BUCK3** | - | 4.7uH Isat 4,0A DCR 31mR | SMD 6x6mm | `C105660` | 4.7uH Isat 4,0A DCR 31mR |
| **L_BUCK5** | - | 4.7uH Isat 4,0A DCR 31mR | SMD 6x6mm | `C105660` | 4.7uH Isat 4,0A DCR 31mR |
| **L_CHG** | - | 2.2uH Isat 5,0A DCR 58mR | SMD 4.6x4.1mm | `C142096` | 2.2uH Isat 5,0A DCR 58mR |
| **Q_PROT1** | - | PSMN4R2-30MLDX | LFPAK33-8 | `C179452` | PSMN4R2-30MLDX |
| **Q_PROT2** | - | PSMN4R2-30MLDX | LFPAK33-8 | `C179452` | PSMN4R2-30MLDX |
| **Q_PUMP2** | - | AO3400A | SOT-23 | `C20917` | AO3400A |
| **R3a** | - | 51k | 0805 | `C17737` | 51k |
| **R3b** | - | 51k | 0805 | `C17737` | 51k |
| **R5a** | - | 5.1k | 0805 | `C27834` | 5.1k |
| **R5b** | - | 5.1k | 0805 | `C27834` | 5.1k |
| **R_BOOT** | - | 10k | 0805 | `C17414` | 10k |
| **R_BTN** | - | 10k | 0805 | `C17414` | 10k |
| **R_CB** | - | 100R 0,25W | 1206 | `C17901` | 100R 0,25W |
| **R_EN** | - | 10k | 0805 | `C17414` | 10k |
| **R_EN_CHG** | - | 100k 1% | 0805 | `C96346` | 100k 1% |
| **R_FB5_BOT** | - | 10k | 0805 | `C17414` | 10k |
| **R_FB5_TOP** | - | 75k | 0805 | `C17819` | 75k |
| **R_GATE** | - | 47k | 0805 | `C17713` | 47k |
| **R_GATE2** | - | 1k | 0805 | `C17513` | 1k |
| **R_GATE2_PD** | - | 47k | 0805 | `C17713` | 47k |
| **R_GPIO8** | - | 10k | 0805 | `C17414` | 10k |
| **R_ISET** | - | 100k 1% | 0805 | `C96346` | 100k 1% |
| **R_LEDCHG** | - | 1k | 0805 | `C17513` | 1k |
| **R_LIGHT** | - | 10k | 0805 | `C17414` | 10k |
| **R_LIGHT_S** | - | 1k | 0805 | `C17513` | 1k |
| **R_PROT_CS** | - | 2k | 0805 | `C17604` | 2k |
| **R_PROT_VC** | - | 330R | 0805 | `C17630` | 330R |
| **R_PROT_VDD** | - | 330R | 0805 | `C17630` | 330R |
| **R_SCL_PU** | - | 4.7k | 0805 | `C17673` | 4.7k |
| **R_SCL_S** | - | 1k | 0805 | `C17513` | 1k |
| **R_SDA_PU** | - | 4.7k | 0805 | `C17673` | 4.7k |
| **R_SDA_S** | - | 1k | 0805 | `C17513` | 1k |
| **R_SENSE_BOT** | - | 68k | 0805 | `C17801` | 68k |
| **R_SENSE_TOP** | - | 200k | 0805 | `C17539` | 200k |
| **R_SPARE_AIN** | - | 1k | 0805 | `C17513` | 1k |
| **R_SPARE_IO15** | - | 1k | 0805 | `C17513` | 1k |
| **R_SPARE_IO16** | - | 1k | 0805 | `C17513` | 1k |
| **R_SPARE_IO17** | - | 1k | 0805 | `C17513` | 1k |
| **R_SPARE_IO21** | - | 1k | 0805 | `C17513` | 1k |
| **R_SPARE_IO23** | - | 1k | 0805 | `C17513` | 1k |
| **R_TANK** | - | 1k | 0805 | `C17513` | 1k |
| **R_UART** | - | 499R | 0805 | - | 499R |
| **R_UVSET** | - | 68k | 0805 | `C17801` | 68k |
| **R_VIN_CHG** | - | 0.5R | 0805 | `C28319` | 0.5R |
| **U_BUCK3** | - | AP63203WU-7 | TSOT-23-6 | `C780769` | AP63203WU-7 |
| **U_BUCK5** | - | SY8113B ADC | TSOT-23-6 | `C78989` | SY8113B ADC |
| **U_CHG** | - | IP2326 | VQFN-24-EP(4x4) | `C2832094` | IP2326 |
| **U_PROT** | - | HY2120-CB | SOT-23-6 | `C116509` | HY2120-CB |
| **C3** | Akku und Pack | 100uF 16V | SMD D6.3x5.4 | `C970684` | Elko 100 uF Pumpenpuffer auf +5V |
| **F1** | Akku und Pack | 5A traege 2410 | 2410 | `C66503` | Sicherung in der Pack-Plus-Leitung, 5 A traege (2410) |
| **J1** | Akku und Pack | JST-XH-3P | THT P2.5 aufrecht (Top-Entry) | `C5258884` | Akku JST-XH 3P (B-/MID/B+), aufrecht |
| **TP3** | Akku und Pack | - | - | - | Testpad GND |
| **TP4** | Akku und Pack | - | - | - | Testpad VBAT |
| **TP1** | UART-Debug-Pads (DNP) | - | - | - | Testpad TXD0 |
| **J10** | Erweiterung | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO15 Stiftleiste 1x3 |
| **J11** | Erweiterung | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO16 (TXD0) Stiftleiste 1x3 |
| **J12** | Erweiterung | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO17 (RXD0) Stiftleiste 1x3 |
| **J13** | Erweiterung | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO21 Stiftleiste 1x3 |
| **J15** | Erweiterung | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO23 Stiftleiste 1x3 |
| **J8** | Erweiterung | Stiftleiste-1x4-2.54mm | THT P2.54 gerade | `C2691448` | I2C-Stiftleiste 1x4 (GND-VCC-SDA-SCL) |
| **J9** | Erweiterung | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve-Analog Stiftleiste 1x3 (IO5) |
| **Q2** | Erweiterung | AO3401A | SOT-23 | `C15127` | P-Kanal-Load-Switch VCC_EXT |
| **J18** | Laden (IP2326, 2S) | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Stecker fuer den Akku-Temperatursensor (XH-2P, 1 = NTC-Signal, 2 = GND) |
| **R_NTC_PAR** | Laden (IP2326, 2S) | 82k 1% | 0805 | `C17840` | 82 kOhm parallel zum NTC - legt die Schwellen auf 0 / 45 / 55 Grad C |
| **TP5** | 3V3-Buck (AP63203) | - | - | - | Testpad +3V3 |
| **J7** | Lichtsensor | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Lichtsensor-Stiftleiste 1x3 2,54 mm |
| **C10** | ESP32-C6 | 100nF | 0805 | `C49678` | ADC-Filter VBAT 100 nF |
| **C13** | ESP32-C6 | 100nF | 0805 | `C49678` | Decoupling Modul 100 nF |
| **C2** | ESP32-C6 | 22uF 25V | 0805 | `C45783` | Bulk 22 uF am Modul-3V3 |
| **C4** | ESP32-C6 | 1uF | 0603 | `C15849` | EN-RC 1 uF |
| **C9** | ESP32-C6 | 100nF | 0805 | `C49678` | ADC-Filter Sensor 100 nF |
| **D2** | ESP32-C6 | LED-GREEN | 0805 | `C2297` | Status-LED gruen 525 nm |
| **D5** | ESP32-C6 | LED-RED | 0805 | `C84256` | Tank-leer-LED rot |
| **R4** | ESP32-C6 | 220R | 0805 | `C17557` | Status-LED 220 R |
| **SW1** | ESP32-C6 | SW-SMD | SMD-4P 5.1x5.1 | `C318884` | Reset-Taster |
| **SW2** | ESP32-C6 | SW-SMD | SMD-4P 5.1x5.1 | `C318884` | Boot-Taster |
| **TP2** | ESP32-C6 | - | - | - | Testpad RXD0 |
| **U1** | ESP32-C6 | ESP32-C6-MINI-1 | SMD-53P | `C5736265` | ESP32-C6-MINI-1 WLAN-Modul |
| **C11** | Pumpentreiber | 100nF | 0805 | `C49678` | EMI an den Pumpenklemmen 100 nF |
| **D1** | Pumpentreiber | 1N5819WS | SOD-323 | `C191023` | Freilaufdiode Dosierpumpe |
| **J16** | Pumpentreiber | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Sauerstoffpumpe JST-XH 2P, aufrecht |
| **J4** | Pumpentreiber | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Dosierpumpe JST-XH 2P, aufrecht |
| **Q1** | Pumpentreiber | AO3400A | SOT-23 | `C20917` | N-MOSFET Pumpentreiber Dosierpumpe |
| **R1** | Pumpentreiber | 1k | 0805 | `C17513` | Gate-Serie 1 k |
| **R2** | Pumpentreiber | 47k | 0805 | `C17713` | Gate-Pulldown 47 k |
| **J17** | Sensor-Eingang | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | 5-V-Ausgang fuer Sensorik JST-XH 2P |
| **J2** | Sensor-Eingang | JST-XH-3P | THT P2.5 aufrecht (Top-Entry) | `C5258884` | Feuchtesensor JST-XH 3P, aufrecht |
| **Q_SENS** | Sensor-Eingang | AO3401A | SOT-23 | `C15127` | P-Kanal-Lastschalter der Sensorversorgung (Source +3V3, Drain SENSOR_PWR) |
| **R6** | Sensor-Eingang | 1k | 0805 | `C17513` | Sensor-AOUT Serie 1 k |
| **R_SENS_GATE** | Sensor-Eingang | 47k | 0805 | `C17713` | 47 kOhm Gate-Pull-up: Sensor-Lastschalter ohne Freigabe sicher aus |
| **TP6** | Sensor-Eingang | - | - | - | Testpad SENSOR_AOUT |
| **J6** | Taster und LEDs | - | 2x Loch 1.0mm Raster 2.54mm | - | 2 Loetpads externer Taster |
| **J5** | USB-C Eingang | USB-C-16P | SMD | `C165948` | USB-C 16P Buchse (Laden + Programmieren) |
| **U6** | USB-C Eingang | USBLC6-2SC6 | SOT-23-6L | `C7519` | USB-ESD-Schutz USBLC6-2SC6 |
| **C12** | Unterspannungswaechter | 100nF | 0805 | `C49678` | Decoupling Waechter 100 nF |
| **U7** | Unterspannungswaechter | TPS3839G33DBZR | SOT-23-3 | `C485802` | Unterspannungswaechter TPS3839G33 (3,08 V) |

## 3. Wie ist verkabelt (jedes Netz mit jedem Pin)

### `+3V3`

Pins: 19

- `C13:1` - ESP32-C6  *(Hinweis: 100 nF)*
- `C1a:1` - -  *(Hinweis: 100 nF)*
- `C1b:1` - -  *(Hinweis: 100 nF)*
- `C2:1` - ESP32-C6  *(Hinweis: 22 uF Bulk am Modul)*
- `C_B3_OUT:1` - -  *(Hinweis: 22 uF Keramik am Ausgang nach GND)*
- `C_B3_OUT_HF:1` - -  *(Hinweis: 100 nF HF am Ausgang nach GND)*
- `L_BUCK3:2` - -  *(Hinweis: Ausgangsknoten der Logikversorgung)*
- `Q2:2 Source` - Erweiterung  *(Hinweis: P-Kanal-Load-Switch Source)*
- `Q_SENS:2 Source` - Sensor-Eingang  *(Hinweis: P-Kanal-Lastschalter Sensorversorgung (Source an 3,3 V))*
- `R_BOOT:1` - -  *(Hinweis: 10 kOhm Pull-up GPIO9)*
- `R_BTN:1` - -  *(Hinweis: 10 kOhm Pull-up fuer den externen Taster)*
- `R_EN:1` - -  *(Hinweis: 10 kOhm Pull-up EN)*
- `R_GATE:1` - -  *(Hinweis: 47 kOhm Gate-Pull-up des Load-Switch (aus = Fail-safe))*
- `R_GPIO8:1` - -  *(Hinweis: 10 kOhm Pull-up GPIO8 (eigene Auslegung))*
- `R_SENS_GATE:2` - Sensor-Eingang  *(Hinweis: 47 k Gate-Pull-up: ohne Freigabe ist der Lastschalter sicher aus)*
- `TP5:1` - 3V3-Buck (AP63203)  *(Hinweis: Testpad +3V3)*
- `U1:3 3V3` - ESP32-C6  *(Hinweis: Modulversorgung)*
- `U1:VDD33 (alle)` - ESP32-C6  *(Hinweis: mehrere Pins laut Espressif Pin-Layout)*
- `U_BUCK3:1 FB` - -  *(Hinweis: Festspannungsversion AP63203: FB direkt auf den Ausgang, VFB = 3,30 V - kein Teiler (Datenblatt Fig. 21))*

### `+5V`

Pins: 12

- `C11:2` - Pumpentreiber  *(Hinweis: EMI-Kondensator ueber den Motorklemmen (Minus geschaltet ueber Q1))*
- `C3:+` - Akku und Pack  *(Hinweis: 100 uF Elko (von VBAT hierher verschoben) - POLARITAET beachten)*
- `C_B5_OUT:1` - -  *(Hinweis: 22 uF Keramik am Ausgang nach GND)*
- `C_B5_OUT_HF:1` - -  *(Hinweis: 100 nF HF am Ausgang nach GND)*
- `C_PUMP2_EMI:2` - -  *(Hinweis: EMI-Kondensator ueber den Klemmen der Sauerstoffpumpe (Minus geschaltet ueber Q3))*
- `D1:Kathode` - Pumpentreiber  *(Hinweis: Freilaufdiode Dosierpumpe)*
- `D_FLY2:Kathode` - -  *(Hinweis: Freilaufdiode Sauerstoffpumpe)*
- `J16:1` - Pumpentreiber  *(Hinweis: Sauerstoffpumpe +)*
- `J17:1` - Sensor-Eingang  *(Hinweis: 5-V-Ausgang fuer Sensorik (neu) - Pin 1)*
- `J4:1` - Pumpentreiber  *(Hinweis: Dosierpumpe +)*
- `L_BUCK5:2` - -  *(Hinweis: Ausgangsknoten der 5-V-Schiene)*
- `R_FB5_TOP:1` - -  *(Hinweis: Feedback oben 75 k -> Vout = 0,6 V x (1 + 75/10) = 5,10 V)*

### `VBAT`

Pins: 15

- `C_B3_IN:1` - -  *(Hinweis: 22 uF Keramik am Buck-Eingang nach GND)*
- `C_B3_IN_HF:1` - -  *(Hinweis: 100 nF HF am Buck-Eingang nach GND)*
- `C_B5_IN:1` - -  *(Hinweis: 22 uF Keramik am Buck-Eingang nach GND)*
- `C_B5_IN_HF:1` - -  *(Hinweis: 100 nF HF am Buck-Eingang nach GND)*
- `C_CHG_OUT:1` - -  *(Hinweis: 10 uF Keramik am Ausgang (Datenblatt C6/C7))*
- `F1:2` - Akku und Pack  *(Hinweis: 5-A-Sicherung (traege, 2410): schuetzt Akkukabel und Stecker. Die 17-A-Schwelle des HY2120 ist dafuer zu hoch (Review 16.09.2026))*
- `R3a:1` - -  *(Hinweis: UVLO-Teiler oben 51 k)*
- `R_PROT_VDD:1` - -  *(Hinweis: 330 R zum VDD-Pin des Schutz-IC (Datenblatt-Typwert))*
- `R_SENSE_TOP:1` - -  *(Hinweis: ADC-Teiler oben 200 k)*
- `TP4:1` - Akku und Pack  *(Hinweis: Testpad VBAT)*
- `U_BUCK3:2 EN` - -  *(Hinweis: EN fest an VIN - 3,3-V-Schiene ist immer an (MCU muss im Waechterfall leben))*
- `U_BUCK3:3 VIN` - -  *(Hinweis: Eingang 3,3-V-Buck)*
- `U_BUCK5:5 IN` - -  *(Hinweis: Eingang 5-V-Buck)*
- `U_CHG:21 VOUT` - -  *(Hinweis: Boost-Ausgang -> Akku-Plus (Datenblatt: "VOUT 接电池正极"))*
- `U_CHG:22 VOUT` - -

### `PACK_PLUS`

Pins: 2

- `F1:1` - Akku und Pack
- `J1:3` - Akku und Pack  *(Hinweis: Akku-Pack Plus (Zelle 2 +) - Packseite, VOR der Sicherung)*

### `VBUS`

Pins: 7

- `C_CHG_IN:1` - -  *(Hinweis: 10 uF Keramik am Eingang (Datenblatt C1) - 25 V, weil Eingang bis 9,5 V zugelassen)*
- `J5:VBUS (A4/A9/B4/B9)` - USB-C Eingang  *(Hinweis: USB-Eingang 5 V - alle vier VBUS-Pins verbinden)*
- `L_CHG:1` - -  *(Hinweis: Induktivitaet 2.2 uH - andere Seite am Schaltknoten LX_CHG)*
- `R_EN_CHG:1` - -  *(Hinweis: 100 kOhm Pull-up des Lader-EN - Laden ist an, sobald USB steckt, ohne MCU)*
- `R_LEDCHG:1` - -  *(Hinweis: 1 kOhm Vorwiderstand der Lade-LED (ca. 2,7 mA aus 5 V))*
- `R_VIN_CHG:1` - -  *(Hinweis: 0.5 Ohm Filterwiderstand zum VIN-Pin (Datenblatt R1) - KEIN Ladestrom-Shunt)*
- `U6:5 VBUS` - USB-C Eingang  *(Hinweis: ESD-Referenz)*

### `VBUS_CHG`

Pins: 3

- `C_CHG_VIN:1` - -  *(Hinweis: 10 uF direkt am VIN-Pin (Datenblatt C3))*
- `R_VIN_CHG:2` - -  *(Hinweis: Filterspannung fuer den VIN-Pin)*
- `U_CHG:13 VIN` - -  *(Hinweis: mit C_CHG_VIN gepuffert)*

### `VSYS_CHG`

Pins: 4

- `C_VSYS_A:1` - -  *(Hinweis: 22 uF direkt am VSYS-Pin (Datenblatt C4))*
- `C_VSYS_B:1` - -  *(Hinweis: 22 uF direkt am VSYS-Pin (Datenblatt C5))*
- `U_CHG:19 VSYS` - -  *(Hinweis: Zwischenknoten des Boost-Ausgangs)*
- `U_CHG:20 VSYS` - -

### `BAT_MINUS`

Pins: 8

- `C_PROT_VC:2` - -  *(Hinweis: VC-Filterkondensator nach Pack-Minus)*
- `C_PROT_VDD:2` - -  *(Hinweis: VDD-Filterkondensator nach Pack-Minus)*
- `J1:1` - Akku und Pack  *(Hinweis: Akku-Pack-Minus (Zelle 1 -) - liegt NICHT auf Board-GND)*
- `Q_PROT1:1 S` - -  *(Hinweis: Source des Entlade-MOSFET (Pinning: 1/2/3 = Source))*
- `Q_PROT1:2 S` - -
- `Q_PROT1:3 S` - -
- `U_CHG:24 BAT_GND` - -  *(Hinweis: Bezug des internen Balancing (Datenblatt-Applikation: BAT- an Pin 24))*
- `U_PROT:6 VSS` - -  *(Hinweis: Masse des Schutz-IC = Pack-Minus (Datenblatt 5.2))*

### `VCC_EXT`

Pins: 10

- `J10:2` - Erweiterung  *(Hinweis: Reserve IO15 VCC (geschaltet))*
- `J11:2` - Erweiterung  *(Hinweis: Reserve IO16 VCC (geschaltet))*
- `J12:2` - Erweiterung  *(Hinweis: Reserve IO17 VCC (geschaltet))*
- `J13:2` - Erweiterung  *(Hinweis: Reserve IO21 VCC (geschaltet))*
- `J15:2` - Erweiterung  *(Hinweis: Reserve IO23 VCC (geschaltet))*
- `J8:2` - Erweiterung  *(Hinweis: geschaltete Erweiterungsversorgung)*
- `J9:2` - Erweiterung  *(Hinweis: Reserve-Analog VCC (geschaltet))*
- `Q2:3 Drain` - Erweiterung  *(Hinweis: P-Kanal-Load-Switch)*
- `R_SCL_PU:2` - -
- `R_SDA_PU:2` - -

### `GND`

Pins: 89

- `C10:2` - ESP32-C6
- `C12:2` - Unterspannungswaechter
- `C13:2` - ESP32-C6
- `C1a:2` - -
- `C1b:2` - -
- `C2:2` - ESP32-C6
- `C3:-` - Akku und Pack  *(Hinweis: Elko-Minus (liegt auf der 5-V-Schiene))*
- `C4:2` - ESP32-C6
- `C9:2` - ESP32-C6
- `C_B3_IN:2` - -
- `C_B3_IN_HF:2` - -
- `C_B3_OUT:2` - -
- `C_B3_OUT_HF:2` - -
- `C_B5_IN:2` - -
- `C_B5_IN_HF:2` - -
- `C_B5_OUT:2` - -
- `C_B5_OUT_HF:2` - -
- `C_BTN:2` - -
- `C_CHG_IN:2` - -
- `C_CHG_OUT:2` - -
- `C_CHG_VIN:2` - -
- `C_LIGHT:2` - -  *(Hinweis: ADC-Filter Lichtsensor)*
- `C_SPARE:2` - -  *(Hinweis: ADC-Filter Reserve-Analog)*
- `C_VSYS_A:2` - -
- `C_VSYS_B:2` - -
- `D2:Kathode` - ESP32-C6
- `D5:Kathode` - ESP32-C6
- `J10:1` - Erweiterung  *(Hinweis: Reserve IO15 GND)*
- `J11:1` - Erweiterung  *(Hinweis: Reserve IO16 GND)*
- `J12:1` - Erweiterung  *(Hinweis: Reserve IO17 GND)*
- `J13:1` - Erweiterung  *(Hinweis: Reserve IO21 GND)*
- `J15:1` - Erweiterung  *(Hinweis: Reserve IO23 GND)*
- `J17:2` - Sensor-Eingang  *(Hinweis: 5-V-Ausgang GND - Pin 2)*
- `J18:2` - Laden (IP2326, 2S)  *(Hinweis: NTC-Rueckleitung)*
- `J2:1` - Sensor-Eingang  *(Hinweis: Sensor GND)*
- `J5:GND (A1/A12/B1/B12) + Schirm` - USB-C Eingang
- `J6:2` - Taster und LEDs  *(Hinweis: Lotpad/Bohrung - Taster-Rueckleitung)*
- `J7:1` - Lichtsensor  *(Hinweis: Lichtsensor GND)*
- `J8:1` - Erweiterung  *(Hinweis: I2C GND)*
- `J9:1` - Erweiterung  *(Hinweis: Reserve-Analog GND)*
- `Q1:2 Source` - Pumpentreiber
- `Q_PROT2:1 S` - -  *(Hinweis: Source des Lade-MOSFET = Board-GND - traegt den gesamten Systemstrom)*
- `Q_PROT2:2 S` - -
- `Q_PROT2:3 S` - -
- `Q_PUMP2:Source` - -  *(Hinweis: Source AO3400A)*
- `R2:2` - Pumpentreiber
- `R3b:2` - -  *(Hinweis: UVLO-Teiler unten)*
- `R5a:2` - -
- `R5b:2` - -
- `R_FB5_BOT:2` - -
- `R_GATE2_PD:2` - -  *(Hinweis: Pulldown Q3)*
- `R_ISET:2` - -
- `R_LIGHT:2` - -  *(Hinweis: Lastwiderstand Lichtsensor nach GND)*
- `R_NTC_PAR:2` - Laden (IP2326, 2S)
- `R_PROT_CS:2` - -
- `R_SENSE_BOT:2` - -  *(Hinweis: ADC-Teiler unten)*
- `R_UVSET:2` - -
- `SW1:2` - ESP32-C6
- `SW2:2` - ESP32-C6
- `TP3:1` - Akku und Pack  *(Hinweis: Testpad GND)*
- `U1:1` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:11` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:14` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:2` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:36` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:37` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:38` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:39` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:40` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:41` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:42` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:43` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:44` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:45` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:46` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:47` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:48` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:49` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:50` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:51` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:52` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:53` - ESP32-C6  *(Hinweis: Modul-Masse)*
- `U1:EPAD (Pin 49)` - ESP32-C6  *(Hinweis: # Kommentar: EPAD = Pad 49 und damit in U1 Pin 36-53 enthalten; das Symbol hat keinen eigenen EPAD-Pin - keine eigene Verbindung (kein Phantompin))*
- `U6:2 GND` - USB-C Eingang
- `U7:1 GND` - Unterspannungswaechter
- `U_BUCK3:4 GND` - -
- `U_BUCK5:2 GND` - -
- `U_CHG:18 PGND` - -  *(Hinweis: Leistungsmasse des Boost-Laders)*
- `U_CHG:EPAD` - -  *(Hinweis: Thermo-Pad - mit GND verbinden (Datenblatt))*

### `BOOT`

Pins: 3

- `R_BOOT:2` - -
- `SW2:1` - ESP32-C6  *(Hinweis: Taster gegen GND)*
- `U1:23 IO9` - ESP32-C6  *(Hinweis: Strapping - KEIN grosser C)*

### `BST_3V3`

Pins: 2

- `C_B3_BST:1` - -  *(Hinweis: 100 nF Bootstrap)*
- `U_BUCK3:6 BST` - -  *(Hinweis: Bootstrap-Pin)*

### `BST_5V`

Pins: 2

- `C_B5_BST:1` - -  *(Hinweis: 100 nF Bootstrap)*
- `U_BUCK5:1 BS` - -  *(Hinweis: Bootstrap-Pin)*

### `BST_CHG`

Pins: 2

- `C_BST_CHG:1` - -  *(Hinweis: 100 nF Bootstrap (Datenblatt C2))*
- `U_CHG:14 BST` - -

### `BTN`

Pins: 4

- `C_BTN:1` - -  *(Hinweis: 100 nF Entprellung)*
- `J6:1` - Taster und LEDs  *(Hinweis: Lotpad/Bohrung fuer den externen Taster (sitzt im Gehaeuse))*
- `R_BTN:2` - -
- `U1:15 IO6` - ESP32-C6  *(Hinweis: LP_GPIO6 - weckt aus dem Deep-Sleep (EXT1 ANY_LOW))*

### `CC1`

Pins: 2

- `J5:A5 CC1` - USB-C Eingang
- `R5a:1` - -  *(Hinweis: 5.1 kOhm nach GND (USB-C-Senke))*

### `CC2`

Pins: 2

- `J5:B5 CC2` - USB-C Eingang
- `R5b:1` - -  *(Hinweis: 5.1 kOhm nach GND (USB-C-Senke))*

### `EN`

Pins: 4

- `C4:1` - ESP32-C6  *(Hinweis: 1 uF RC-Glied)*
- `R_EN:2` - -
- `SW1:1` - ESP32-C6  *(Hinweis: Taster gegen GND)*
- `U1:8 EN` - ESP32-C6  *(Hinweis: Reset)*

### `EN_CHG`

Pins: 2

- `R_EN_CHG:2` - -  *(Hinweis: Lader-Enable (High = laden))*
- `U_CHG:12 EN` - -  *(Hinweis: EN niemals floaten)*

### `EXT_EN`

Pins: 3

- `Q2:1 Gate` - Erweiterung
- `R_GATE:2` - -
- `U1:26 IO20` - ESP32-C6  *(Hinweis: Load-Switch-Eingang (interner WPU beim Reset))*

### `EXT_SENS_EN`

Pins: 3

- `Q_SENS:1 Gate` - Sensor-Eingang  *(Hinweis: Gate des Sensor-Lastschalters)*
- `R_SENS_GATE:1` - Sensor-Eingang
- `U1:6 IO3` - ESP32-C6  *(Hinweis: Sensor-Lastschalter (low = ein; Pull-up haelt ihn im Reset aus))*

### `FB_5V`

Pins: 3

- `R_FB5_BOT:1` - -  *(Hinweis: Teiler unten 10 k)*
- `R_FB5_TOP:2` - -  *(Hinweis: Teiler oben)*
- `U_BUCK5:3 FB` - -  *(Hinweis: Feedback-Eingang (0,6 V intern))*

### `GATE`

Pins: 3

- `Q1:1 Gate` - Pumpentreiber
- `R1:2` - Pumpentreiber
- `R2:1` - Pumpentreiber  *(Hinweis: 47 kOhm Pulldown)*

### `GATE2`

Pins: 3

- `Q_PUMP2:Gate` - -  *(Hinweis: Gate AO3400A)*
- `R_GATE2:2` - -  *(Hinweis: Gate-Knoten Q3)*
- `R_GATE2_PD:1` - -  *(Hinweis: Pulldown 47 k nach GND)*

### `GPIO8_STRAP`

Pins: 2

- `R_GPIO8:2` - -
- `U1:22 IO8` - ESP32-C6  *(Hinweis: Strapping-Pin)*

### `ISET_CHG`

Pins: 2

- `R_ISET:1` - -  *(Hinweis: 100 kOhm 1 Prozent -> ICHG = 90000/100000 = 0,90 A)*
- `U_CHG:11 ISET` - -  *(Hinweis: ISET darf NICHT offen bleiben (Datenblatt))*

### `LED_CHG`

Pins: 2

- `D_LEDCHG:Anode` - -  *(Hinweis: Lade-LED (leuchtet beim Laden, aus bei Voll, blinkt bei Fehler))*
- `R_LEDCHG:2` - -  *(Hinweis: Knoten zwischen Vorwiderstand und LED-Anode)*

### `LED_STAT`

Pins: 2

- `R4:1` - ESP32-C6  *(Hinweis: 220 Ohm (gruene LED, Vf 2,85 V))*
- `U1:19 IO14` - ESP32-C6  *(Hinweis: Status-LED (NICHT IO4 = MTMS/Strapping))*

### `LED_STAT_A`

Pins: 2

- `D2:Anode` - ESP32-C6  *(Hinweis: LED gruen)*
- `R4:2` - ESP32-C6

### `LED_TANK`

Pins: 2

- `R_TANK:1` - -  *(Hinweis: 1 kOhm)*
- `U1:16 IO7` - ESP32-C6  *(Hinweis: LP_GPIO7 - Tank-leer-Anzeige)*

### `LED_TANK_A`

Pins: 2

- `D5:Anode` - ESP32-C6  *(Hinweis: LED rot)*
- `R_TANK:2` - -

### `LIGHT_AOUT`

Pins: 3

- `C_LIGHT:1` - -  *(Hinweis: 100 nF Filter)*
- `R_LIGHT_S:2` - -
- `U1:9 IO4` - ESP32-C6  *(Hinweis: ADC1_CH4 - Lichtsensor)*

### `LIGHT_RAW`

Pins: 3

- `J7:3` - Lichtsensor  *(Hinweis: Sensorausgang - definierter Zustand bei offenem Stecker)*
- `R_LIGHT:1` - -  *(Hinweis: 10 kOhm Lastwiderstand)*
- `R_LIGHT_S:1` - -  *(Hinweis: 1 kOhm Serienschutz)*

### `LX_3V3`

Pins: 3

- `C_B3_BST:2` - -  *(Hinweis: Bootstrap-Kondensator zwischen BST und SW)*
- `L_BUCK3:1` - -  *(Hinweis: Induktivitaet 4.7 uH - andere Seite an +3V3)*
- `U_BUCK3:5 SW` - -  *(Hinweis: Schaltknoten des 3,3-V-Bucks)*

### `LX_5V`

Pins: 3

- `C_B5_BST:2` - -  *(Hinweis: Bootstrap-Kondensator zwischen BS und LX)*
- `L_BUCK5:1` - -  *(Hinweis: Induktivitaet 4.7 uH - andere Seite an +5V)*
- `U_BUCK5:6 LX` - -  *(Hinweis: Schaltknoten des 5-V-Bucks)*

### `LX_CHG`

Pins: 5

- `C_BST_CHG:2` - -  *(Hinweis: Bootstrap-Kondensator zwischen BST und LX)*
- `L_CHG:2` - -  *(Hinweis: Schaltknoten des Boost-Laders)*
- `U_CHG:15 LX` - -
- `U_CHG:16 LX` - -
- `U_CHG:17 LX` - -

### `MID`

Pins: 3

- `J1:2` - Akku und Pack  *(Hinweis: Mittelabgriff (Zelle 1 + / Zelle 2 -) - erst mit diesem Stecker ist Balancing moeglich)*
- `R_CB:1` - -  *(Hinweis: Balancing-Widerstand zum VBATM-Pin des Laders)*
- `R_PROT_VC:1` - -  *(Hinweis: 330 R zum VC-Pin (Datenblatt-Typwert))*

### `NTC_CHG`

Pins: 3

- `J18:1` - Laden (IP2326, 2S)  *(Hinweis: NTC-Signal vom Akku-Temperatursensor (XH-2P, Gegenstueck am Kabel))*
- `R_NTC_PAR:1` - Laden (IP2326, 2S)  *(Hinweis: 82 k parallel zum NTC - Datenblatt-Wert, legt die Schwellen auf 0 / 45 / 55 Grad C)*
- `U_CHG:4 NTC` - -  *(Hinweis: Akku-NTC (100 kOhm B3950) ueber Stecker J18; 82 k parallel laut Datenblatt-Beispiel)*

### `PROT_COMMON`

Pins: 2

- `Q_PROT1:5 D` - -  *(Hinweis: Gemeinsamer Drain beider Schalter (Symbol-Pin 5 = D, Datenblatt: Montagebasis ist Drain))*
- `Q_PROT2:5 D` - -

### `PROT_CS`

Pins: 2

- `R_PROT_CS:1` - -  *(Hinweis: 2 k zum Board-GND (Datenblatt R3 typ 2 k))*
- `U_PROT:3 CS` - -  *(Hinweis: Strommessung + Ladeerkennung (Datenblatt Pin 3))*

### `PROT_GATE_C`

Pins: 2

- `Q_PROT2:4 G` - -  *(Hinweis: Gate des Lade-MOSFET)*
- `U_PROT:2 OC` - -  *(Hinweis: Lade-Steuerung (Datenblatt Pin 2))*

### `PROT_GATE_D`

Pins: 2

- `Q_PROT1:4 G` - -  *(Hinweis: Gate des Entlade-MOSFET (Pin 4 = Gate))*
- `U_PROT:1 OD` - -  *(Hinweis: Entlade-Steuerung (Datenblatt Pin 1))*

### `PROT_VC`

Pins: 3

- `C_PROT_VC:1` - -  *(Hinweis: 0)*
- `R_PROT_VC:2` - -
- `U_PROT:4 VC` - -  *(Hinweis: Mittelabgriff-Messung (Datenblatt Pin 4))*

### `PROT_VDD`

Pins: 3

- `C_PROT_VDD:1` - -  *(Hinweis: 0)*
- `R_PROT_VDD:2` - -
- `U_PROT:5 VDD` - -  *(Hinweis: Versorgung (Datenblatt Pin 5))*

### `PUMP2_EN`

Pins: 2

- `R_GATE2:1` - -  *(Hinweis: Gate-Serie 1 kOhm (Kanal 2))*
- `U1:28 IO22` - ESP32-C6  *(Hinweis: Gate-Steuersignal Sauerstoffpumpe)*

### `PUMP2_N`

Pins: 4

- `C_PUMP2_EMI:1` - -  *(Hinweis: 100 nF an den Klemmen nach GND)*
- `D_FLY2:Anode` - -  *(Hinweis: Freilaufdiode)*
- `J16:2` - Pumpentreiber  *(Hinweis: Sauerstoffpumpe - (Pin 2))*
- `Q_PUMP2:Drain` - -  *(Hinweis: geschaltete Masse Sauerstoffpumpe)*

### `PUMP_EN`

Pins: 2

- `R1:1` - Pumpentreiber  *(Hinweis: Gate-Serie 1 kOhm (schnelle Flanken fuer PWM))*
- `U1:5 IO2` - ESP32-C6  *(Hinweis: Pumpen-PWM)*

### `PUMP_N`

Pins: 4

- `C11:1` - Pumpentreiber  *(Hinweis: 100 nF direkt an den Pumpenklemmen (Buerstenstoerung))*
- `D1:Anode` - Pumpentreiber
- `J4:2` - Pumpentreiber  *(Hinweis: Pumpe -)*
- `Q1:3 Drain` - Pumpentreiber  *(Hinweis: Low-Side-Schalter)*

### `RESET_UV`

Pins: 2

- `U7:2 RESET` - Unterspannungswaechter  *(Hinweis: Push-Pull aktiv-low; 200 ms Verzoegerung nach dem Anlaufen)*
- `U_BUCK5:4 EN` - -  *(Hinweis: unter 6,16 V schaltet die 5-V-Schiene wirklich ab (Buck: EN low = 0 V))*

### `SCL`

Pins: 3

- `J8:4` - Erweiterung  *(Hinweis: I2C-Takt (Steckerseite))*
- `R_SCL_PU:1` - -  *(Hinweis: 4.7 kOhm Pull-up nach VCC_EXT)*
- `R_SCL_S:2` - -  *(Hinweis: 1 kOhm Serienschutz)*

### `SCL_MCU`

Pins: 2

- `R_SCL_S:1` - -
- `U1:25 IO19` - ESP32-C6  *(Hinweis: I2C-Takt am Modul)*

### `SDA`

Pins: 3

- `J8:3` - Erweiterung  *(Hinweis: I2C-Daten (Steckerseite))*
- `R_SDA_PU:1` - -  *(Hinweis: 4.7 kOhm Pull-up nach VCC_EXT)*
- `R_SDA_S:2` - -  *(Hinweis: 1 kOhm Serienschutz)*

### `SDA_MCU`

Pins: 2

- `R_SDA_S:1` - -
- `U1:24 IO18` - ESP32-C6  *(Hinweis: I2C-Daten am Modul)*

### `SENSOR_AOUT`

Pins: 4

- `C9:1` - ESP32-C6  *(Hinweis: 100 nF Filter)*
- `R6:2` - Sensor-Eingang
- `TP6:1` - Sensor-Eingang  *(Hinweis: Testpad SENSOR_AOUT)*
- `U1:12 IO0` - ESP32-C6  *(Hinweis: ADC1_CH0)*

### `SENSOR_PWR`

Pins: 3

- `J2:2` - Sensor-Eingang  *(Hinweis: Sensor VCC (Feuchte))*
- `J7:2` - Lichtsensor  *(Hinweis: Lichtsensor VCC (extern, geschaltet))*
- `Q_SENS:3 Drain` - Sensor-Eingang  *(Hinweis: geschaltete Sensorversorgung (Feuchte J2 + Licht J7))*

### `SENSOR_RAW`

Pins: 2

- `J2:3` - Sensor-Eingang  *(Hinweis: Sensor AOUT unbeschaltet)*
- `R6:1` - Sensor-Eingang  *(Hinweis: 1 kOhm Serienwiderstand)*

### `SPARE_AIN`

Pins: 3

- `C_SPARE:1` - -  *(Hinweis: 100 nF ADC-Filter)*
- `R_SPARE_AIN:2` - -
- `U1:10 IO5` - ESP32-C6  *(Hinweis: ADC1_CH5)*

### `SPARE_AIN_RAW`

Pins: 2

- `J9:3` - Erweiterung  *(Hinweis: Reserve-Analog am Stecker)*
- `R_SPARE_AIN:1` - -

### `SPARE_IO15`

Pins: 2

- `R_SPARE_IO15:2` - -
- `U1:20 IO15` - ESP32-C6  *(Hinweis: Strapping JTAG-Quelle (Default-eFuses inert))*

### `SPARE_IO15_RAW`

Pins: 2

- `J10:3` - Erweiterung  *(Hinweis: Reserve IO15 am Stecker)*
- `R_SPARE_IO15:1` - -

### `SPARE_IO16`

Pins: 2

- `J11:3` - Erweiterung
- `R_SPARE_IO16:2` - -  *(Hinweis: Reserve IO16 (TXD0) am Stecker)*

### `SPARE_IO17`

Pins: 2

- `J12:3` - Erweiterung
- `R_SPARE_IO17:2` - -  *(Hinweis: Reserve IO17 (RXD0) am Stecker)*

### `SPARE_IO21`

Pins: 2

- `R_SPARE_IO21:2` - -
- `U1:27 IO21` - ESP32-C6  *(Hinweis: WPU beim Reset (angehaengtes Modul sieht kurz High))*

### `SPARE_IO21_RAW`

Pins: 2

- `J13:3` - Erweiterung  *(Hinweis: Reserve IO21 am Stecker)*
- `R_SPARE_IO21:1` - -

### `SPARE_IO23`

Pins: 2

- `R_SPARE_IO23:2` - -
- `U1:29 IO23` - ESP32-C6

### `SPARE_IO23_RAW`

Pins: 2

- `J15:3` - Erweiterung  *(Hinweis: Reserve IO23 am Stecker)*
- `R_SPARE_IO23:1` - -

### `STAT_CHG`

Pins: 2

- `D_LEDCHG:Kathode` - -  *(Hinweis: Kathode an den LED-Pin des Laders (Senke, max. 5 mA))*
- `U_CHG:6 LED` - -  *(Hinweis: LED-Senke max. 5 mA)*

### `UART_RX`

Pins: 3

- `R_SPARE_IO17:1` - -  *(Hinweis: 1 kOhm Serienschutz zum Reserve-Stecker)*
- `TP2:1` - ESP32-C6  *(Hinweis: Testpad RXD0)*
- `U1:30 RXD0` - ESP32-C6  *(Hinweis: IO17 - optional DNP)*

### `UART_TP`

Pins: 2

- `R_UART:2` - -
- `TP1:1` - UART-Debug-Pads (DNP)  *(Hinweis: Testpad TXD0)*

### `UART_TX`

Pins: 3

- `R_SPARE_IO16:1` - -  *(Hinweis: 1 kOhm Serienschutz zum Reserve-Stecker)*
- `R_UART:1` - -  *(Hinweis: 499 Ohm)*
- `U1:31 TXD0` - ESP32-C6  *(Hinweis: IO16 - optional DNP)*

### `USB_DM`

Pins: 4

- `J5:D- (A7/B7)` - USB-C Eingang
- `U1:17 IO12` - ESP32-C6  *(Hinweis: USB D-)*
- `U6:3 I/O2` - USB-C Eingang  *(Hinweis: ESD)*
- `U6:4 I/O2` - USB-C Eingang  *(Hinweis: ESD durchgeschleift)*

### `USB_DP`

Pins: 4

- `J5:D+ (A6/B6)` - USB-C Eingang
- `U1:18 IO13` - ESP32-C6  *(Hinweis: USB D+)*
- `U6:1 I/O1` - USB-C Eingang  *(Hinweis: ESD)*
- `U6:6 I/O1` - USB-C Eingang  *(Hinweis: ESD durchgeschleift)*

### `UVSET_CHG`

Pins: 2

- `R_UVSET:1` - -  *(Hinweis: 68 kOhm -> Eingangs-Unterspannungsschwelle 4,35 V)*
- `U_CHG:8 VIN_UVSET` - -  *(Hinweis: mehr Kopfraum fuer duenne USB-Kabel bei ~1,8 A Eingangsstrom)*

### `UV_REF`

Pins: 4

- `C12:1` - Unterspannungswaechter  *(Hinweis: 100 nF Decoupling am Waechter (Datenblatt-Messbedingung C1 = 0,1 uF))*
- `R3a:2` - -  *(Hinweis: Teilerknoten = Versorgung des Waechters (VBAT/2))*
- `R3b:1` - -  *(Hinweis: Teiler unten 51 k)*
- `U7:3 VDD` - Unterspannungswaechter  *(Hinweis: Schwelle 3,08 V -> Ausloesung bei VBAT = 6,16 V (plus ~30 mV Offset durch Iq))*

### `VBATM_CHG`

Pins: 2

- `R_CB:2` - -
- `U_CHG:23 VBATM` - -  *(Hinweis: Balancing-Ausgang (Datenblatt Pin 23))*

### `VBAT_SENSE`

Pins: 4

- `C10:1` - ESP32-C6  *(Hinweis: 100 nF Filter)*
- `R_SENSE_BOT:1` - -
- `R_SENSE_TOP:2` - -  *(Hinweis: Teilerknoten)*
- `U1:13 IO1` - ESP32-C6  *(Hinweis: ADC1_CH1 - 8,4 V ergeben 2,13 V am ADC (12-dB-Bereich 0-3300 mV))*

## 4. Wo ist was

Die Blockaufteilung (14 Rahmen auf Blatt A1) und ihre Koordinaten stammen aus der EasyEDA-Kette
und werden im naechsten Durchgang neu erzeugt - nach den Aenderungen dieser Runde (entfallene
Feedback- und Klemmbauteile, neue Bauteile F1/J18/R_NTC_PAR/Q_SENS/R_SENS_GATE) ist der alte Plan
nicht mehr aktuell.

## 5. Anschluesse

### J1 - Akku JST-XH 3P (B-/MID/B+), aufrecht

| Pin | Netz |
|---|---|
| 1 | BAT_MINUS |
| 2 | MID |
| 3 | PACK_PLUS |

### J2 - Feuchtesensor JST-XH 3P, aufrecht

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | SENSOR_PWR |
| 3 | SENSOR_RAW |

### J4 - Dosierpumpe JST-XH 2P, aufrecht

| Pin | Netz |
|---|---|
| 1 | +5V |
| 2 | PUMP_N |

### J5 - USB-C 16P Buchse (Laden + Programmieren)

| Pin | Netz |
|---|---|
| A5 CC1 | CC1 |
| B5 CC2 | CC2 |
| D+ (A6/B6) | USB_DP |
| D- (A7/B7) | USB_DM |
| VBUS (A4/A9/B4/B9) | VBUS |
| GND (A1/A12/B1/B12) + Schirm | GND |

### J6 - 2 Loetpads externer Taster

| Pin | Netz |
|---|---|
| 1 | BTN |
| 2 | GND |

### J7 - Lichtsensor-Stiftleiste 1x3 2,54 mm

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | SENSOR_PWR |
| 3 | LIGHT_RAW |

### J8 - I2C-Stiftleiste 1x4 (GND-VCC-SDA-SCL)

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SDA |
| 4 | SCL |

### J9 - Reserve-Analog Stiftleiste 1x3 (IO5)

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SPARE_AIN_RAW |

### J10 - Reserve IO15 Stiftleiste 1x3

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SPARE_IO15_RAW |

### J11 - Reserve IO16 (TXD0) Stiftleiste 1x3

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SPARE_IO16 |

### J12 - Reserve IO17 (RXD0) Stiftleiste 1x3

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SPARE_IO17 |

### J13 - Reserve IO21 Stiftleiste 1x3

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SPARE_IO21_RAW |

### J15 - Reserve IO23 Stiftleiste 1x3

| Pin | Netz |
|---|---|
| 1 | GND |
| 2 | VCC_EXT |
| 3 | SPARE_IO23_RAW |

### J16 - Sauerstoffpumpe JST-XH 2P, aufrecht

| Pin | Netz |
|---|---|
| 1 | +5V |
| 2 | PUMP2_N |

### J17 - 5-V-Ausgang fuer Sensorik JST-XH 2P

| Pin | Netz |
|---|---|
| 1 | +5V |
| 2 | GND |

### J18 - Stecker fuer den Akku-Temperatursensor (XH-2P, 1 = NTC-Signal, 2 = GND)

| Pin | Netz |
|---|---|
| 1 | NTC_CHG |
| 2 | GND |

### Testpunkte

| Ref | Netz |
|---|---|
| TP1 | (frei) |
| TP2 | (frei) |
| TP3 | (frei) |
| TP4 | (frei) |
| TP5 | (frei) |
| TP6 | (frei) |

## 6. MCU-Pinbelegung (U1, ESP32-C6-MINI-1)

| Pin | Symbolname | Netz |
|---|---|---|
| 1 | GND | GND |
| 2 | GND | GND |
| 3 | 3V3 | +3V3 |
| 5 | IO2 | PUMP_EN |
| 6 | IO3 | EXT_SENS_EN |
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
| VDD33 | (alle) | +3V3 |
| EPAD | (Pin 49) | GND |

## 7. Betriebs- und Randbedingungen

### 7.1 Protokoll der Design-Pruefsuite (gerechnete Werte gegen Grenzwerte)

```
Pruefungen: 42
----------------------------------------------------------------------------------------------------
#  Pruefung                     Ergebnis Ist                                Soll
----------------------------------------------------------------------------------------------------
1  Ladestrom IP2326             OK       0,90 A (R_ISET 100 kΩ)             <= 1,5 A und <= 1 C = 2,00 A
   Begruendung: IP2326-Datenblatt V1.11: ICHG = 90000/R_ISET[Ohm] (S. 11); Grenze 1,5 A (§7, S. 4); ISET darf nicht offen bleiben (§4); Li-Ion erlaubt 1 C (Review §4.1)
2  Ladeschluss 2S               OK       8,40 V (2 x 4,2 V), VSET offen, CON_SEL offen, 8V8 im BOM nein 8,4 V +-0,1 V, VSET/CON_SEL offen, kein IP2326_8V8
   Begruendung: IP2326 S. 4/S. 5: VSET offen ⇒ 8,4 V (8,3-8,5 V) = 4,2 V/Zelle, CON_SEL offen ⇒ 2S (S. 8); IP2326_8V8 waere 8,8 V (4,4 V/Zelle) und fuer Li-Ion unzulaessig
3  Ladeeingangsstrom            OK       2,21 A (Ladung 1,61 A + System 0,60 A) <= 2,5 A (Netzteilannahme)
   Begruendung: IP2326 S. 1: eta 94 % (5 V->8 V/1 A); I_in = V_out*I_CHG/(eta*V_USB) + Systemlast (beide Pumpen, schaltplan §6.1)
4  5-V-Buck-Ausgang             OK       5,100 V (+-5 % von 5,0 V)          5,0 V +-5 %
   Begruendung: SY8113B-Datenblatt S. 1/S. 2: V_REF 0,6 V +-1,5 %, V_out = 0,6 x (1 + R_FB5_TOP/R_FB5_BOT); Pumpennennspannung 5 V
5  3,3-V-Buck-Ausgang           OK       3,300 V (FB Pin 1 auf +3V3 OK, Teiler keiner, Netz FB_3V3 entfallen) 3,0 V bis 3,6 V (Modul); FB direkt auf +3V3, kein Teiler
   Begruendung: AP63203-Datenblatt DS41326: Festspannungsversion, VFB 3,27/3,30/3,33 V bzw. 'AP63203 ... fixed output voltages of 3.3V'; Fig. 21 fuehrt FB direkt auf den Ausgang. Der frueher geprüfte Teiler R_FB3_TOP/BOT ist entfallen (Review 16.09.2026); Espressif ESP32-C6-MINI-1: V_DD33 3,0-3,6 V
6  5-V-Buck-Induktivitaet       OK       4,7 µH (I_Last 3,0 A, Isat 4,0 A); Vin 8,40 V: dI 0,85 A, I_peak 3,43 A; Vin 6,17 V: dI 0,38 A, I_peak 3,19 A I_peak < Isat 4,0 A und I_Last <= 3 A
   Begruendung: PRS6045-Datenblatt: L_BUCK5 4,7 µH, Isat 4,0 A; SY8113B S. 1: 3 A, 500 kHz; dI = (Vin-Vout)*D/(L*f) mit D = Vout/Vin; I_Last = Pumpenanlauf 3 A (bom §4c)
7  3,3-V-Buck-Induktivitaet     OK       4,7 µH (I_Last TX-Peak 0,382 A, Isat 4,0 A); Vin 8,40 V: dI 0,39 A, I_peak 0,58 A; Vin 6,17 V: dI 0,30 A, I_peak 0,53 A I_peak < Isat 4,0 A
   Begruendung: PRS6045-Datenblatt: L_BUCK3 4,7 µH, Isat 4,0 A; AP63203 DS41326: 2 A, 1,1 MHz; I_Last = Modul-TX-Peak 382 mA (Espressif Tab. 6-4)
8  UVLO-Schwelle                OK       6,168 V (V_IT 3,08 V, R3a 51 kΩ, Iq 0,15 µA) 6,0 V bis 6,6 V Pack (2 x 3,0..3,3 V)
   Begruendung: TPS3839 S. 7: V_IT 3,003-3,126 V, Hysterese 31 mV; V_trip = V_IT x (1 + R3a/R3b) + Iq x R3a (Teiler 51 k/51 k, Iq typ. 0,15 µA bzw. max. 0,5 µA)
9  UV-Teiler-Offset             OK       R3a 51 kΩ/51 kΩ, Teilerstrom 82,4 µA (1,98 mAh/Tag), Offset Iq_max x R3a = 25,5 mV (typ. 7,6 mV) R3a = R3b = 51 kΩ, Iq-Offset <= 50 mV, Teilerstrom <= 100 µA
   Begruendung: Fix 16.09.2026 (Review): von 200 k/200 k auf 51 k/51 k verkleinert. TPS3839-Datenblatt SBVS193D: Iq 150 nA typ., 500 nA max.; der Strom fließt durch R3a und verschiebt die Schwelle um Iq x R3a (200 k waeren bis ~0,2 V gewesen, jetzt +15..+50 mV). Teilerstrom 82 µA = ~2 mAh/Tag, Teil des 250-µA-Standby-Budgets (schaltplan §3.2/§13.5)
10 Gate-Pulldowns               OK       R2 47 kΩ an GATE/GND OK; R_GATE2_PD 47 kΩ an GATE2/GND OK; Gate-Serie R1/R_GATE2 OK R2 (GATE/GND) und R_GATE2_PD (GATE2/GND) je 47 kΩ; Gates ueber Serien-R1/R_GATE2 von der MCU
   Begruendung: Review 16.09.2026: der alte Dioden-Klemmzweig (D3/D8 + R_CLAMP1/2) konnte das Gate gegen den 1-kΩ-GPIO-Zweig rechnerisch nicht abschalten (~2,97 V) und ist entfallen. Wirksam bleiben (a) die 5-V-Abschaltung durch U7 und (b) diese 47-kΩ-Pulldowns: bei hochohmigem GPIO liegt V_GS = 0 V, der MOSFET sperrt
11 ADC-Teiler Packspannung      OK       8,4 V -> 2,131 V, 6,0 V -> 1,522 V (V_ref 3,30 V) <= 3,3 V und >= 1,0 V
   Begruendung: Espressif ESP32-C6 ADC1: 12 Bit, ADC_ATTEN_DB_12 = 0..3300 mV; V_ADC = VBAT x R_bot/(R_top+R_bot), Teiler 200 k/68 k
12 Buck-EN-Pegel                OK       V_OH 2,68 V (V_DD 3,08 V - 0,4 V)  > 1,5 V (EN High)
   Begruendung: TPS3839 SBVS193D: V_OH >= V_DD - 0,4 V (Push-Pull); SY8113B: EN-High-Schwelle 1,5 V, 'Do not float'
13 Waechter-Abschaltung         OK       U7 Pin 2 (RESET) auf RESET_UV, U_BUCK5 Pin 4 (EN) auf RESET_UV OK; Klemmzweig-Rest keiner  U7-RESET und U_BUCK5-EN auf RESET_UV; kein D3/D8/R_CLAMP*/KLAMP*
   Begruendung: TPS3839 SBVS193D: Push-Pull-Ausgang aktiv-low; SY8113B: EN low => Ausgang 0 V. Damit ist die Pumpenversorgung im Waechterfall sicher aus. Der Dioden-Klemmzweig D3/D8/R_CLAMP1/2 ist im Review 16.09.2026 als wirkungslos entfernt worden (§13.5)
14 VBAT-Spannungsfestigkeit     OK       13 Teilnehmer: C_B3_IN, C_B3_IN_HF, C_B5_IN, C_B5_IN_HF, C_CHG_OUT, F1, R3a, R_PROT_VDD, R_SENSE_TOP, TP4, U_BUCK3, U_BUCK5, U_CHG nur zugelassene Teilnehmer, V_IN,max >= 8,4 V
   Begruendung: ME6211-Lektion (V_IN,max 6,0 V) aus Review §5 Befund 4: passive VBAT-Teilnehmer sind gelistet, aktive werden gegen ihre Datenblatt-Eingangsspannung geprueft (IP2326 9,5 V, SY8113B 18 V, AP63203 32 V)
15 Standby-Budget               OK       242,8 µA, 5,83 mAh/Tag; Lichtsensor an SENSOR_PWR geschaltet <= 250 µA; Sensor an SENSOR_PWR (ueber Q_SENS geschaltet)
   Begruendung: Datenblaetter: SY8113B Iq 100 µA, AP63203 22 µA, TPS3839 0,15 µA (schaltplan §6.2) + Teiler 82/31,4 µA (§13.5) + Modul 7 µA; Lichtsensor an geschaltetem SENSOR_PWR, das Gate treibt IO3
16 Systemquellen                OK       22 Systemwerte belegt              jeder SYSTEM-Wert hat sein woertliches Belegfragment in der Datei
   Begruendung: Regel: Systemgroessen stammen ausschliesslich aus den Dokumenten. Prueft fuer jeden Eintrag den Belegtext in schaltplan_v1.md bzw. bom_entscheidung.md
17 Schutz-Serienkette           OK       Pack-Minus J1.1/Q_PROT1-S/U_PROT-VSS OK; Drains beider auf einem Netz (PROT_COMMON) OK; Q_PROT2-S auf GND OK; OD an Q_PROT1-Gate, OC an Q_PROT2-Gate (kein Tausch) OK; R_PROT_CS CS<->GND OK; R_PROT_VDD VDD<->VBAT OK; R_PROT_VC VC<->MID OK; R_CB VBATM<->MID OK; U_CHG.24 auf BAT_MINUS OK; Schalterpaar nicht auf GND OK (Netze: J1-1 BAT_MINUS, Q_PROT1-S BAT_MINUS, Drains PROT_COMMON/PROT_COMMON, Q_PROT2-S GND, OD PROT_GATE_D, OC PROT_GATE_C, U_CHG-24 BAT_MINUS) J1-1 = Q_PROT1-S = U_PROT-VSS (BAT_MINUS), beide Drains auf PROT_COMMON, Q_PROT2-S auf GND, OD nur an Q_PROT1-Gate (Entlader, packseitig), OC nur an Q_PROT2-Gate, R_PROT_CS CS<->GND, R_PROT_VDD VDD<->VBAT, R_PROT_VC VC<->MID, R_CB VBATM<->MID, U_CHG-24 auf BAT_MINUS; Schalterpaar nicht auf GND
   Begruendung: Regressionsschutz der Topologie (Review 16.09.2026): der Schutz sitzt in der Minusleitung zwischen Pack-Minus (BAT_MINUS) und Board-GND. Q_PROT1 (Entlader, Gate an OD) liegt packseitig, Q_PROT2 (Lader, Gate an OC) an GND, gemeinsamer Drain PROT_COMMON. Wird ein Source auf GND gelegt oder OD/OC getauscht, ist der Schutz wirkungslos bzw. die Entlade-/Ladetrennung vertauscht
18 Schutz-Schwellen             OK       Ueberladung 4,28 V/Zelle = 8,56 V Pack (8,4 V < x < 8,8 V) OK; Tiefentladung 2,90 V/Zelle = 5,80 V Pack (5,0 V < x < Waechter 6,17 V) OK; Staffelung FW 6,80 V > Waechter 6,17 V > Zelle 5,80 V OK; Dokument konsistent Ueberladung ja/Tiefentladung ja 8,4 V (Ladeschluss) < Ueberladung Pack < 8,8 V; 5,0 V (2 x 2,5 V Zelle) < Tiefentladung Pack < Waechter 6,19 V; FW-Stopp 6,8 V > Waechter > Zelle 5,80 V
   Begruendung: HY2120-Datenblatt (schaltplan §3.1/§6.3): Ueberladung 4,28 V/Zelle, Tiefentladung 2,90 V/Zelle, jeweils woertlich aus dem Dokument gelesen; Ladeschluss IP2326 8,4 V (VSET offen) bzw. 8,8 V der verbotenen 8V8-Variante; Waechter aus den echten R3a/R3b (TPS3839 V_IT 3,08 V); Firmware-Stopp 2 x 3,4 V (bom §4b). Ueberladung muss das normale Laden ueberleben, Tiefentladung vor dem Waechter greifen
19 Schutz-Ueberstrom            OK       Ausloesung 200 mV / Paar 11,4 mΩ = 17,5 A; Anlauf 15,0 W/(0,90 x 6,0 V) = 2,78 A (Reserve 6,3 x) OK; Abfall bei 0,65 A = 7,4 mV OK; Dokument konsistent ja/ja Ausloesestrom >= 2 x Anlaufstrom und Abfall des Paares bei Dauerlast <= 50 mV
   Begruendung: HY2120-Datenblatt: V_DIP 200 mV (+-30 mV) ueber dem Paar (schaltplan §3.1); PSMN4R2-30MLDX: R_DS(on,max) 5,7 mOhm bei V_GS 4,5 V => Paar 11,4 mOhm (schaltplan §6.3); Pumpenanlauf 5 V/3 A = 15,0 W an 6,0 V Pack ueber eta_Buck 0,90 (bom §4c: eta 0,90), Dauerlast 0,65 A (schaltplan §6.3); die interne Verzoegerung von 10 ms schuetzt den kurzzeitigen Anlauf
20 Gate-Spannung                OK       3,23 V (98 % von 3,30 V)           >= 2,5 V und > 1,45 V
   Begruendung: AO3400A-Datenblatt: RDS(on) bei VGS = 2,5 V spezifiziert, VGS(th) max = 1,45 V; Rail +3V3 aus dem AP63203 in der Festspannungsversion
21 MOSFET-Verlustleistung       OK       7,7 mW (I 400 mA, RDS(on) 48 mΩ)   <= 0,25 W (Nennbetrieb)
   Begruendung: AO3400A-Datenblatt: 48 mΩ bei VGS = 2,5 V; P = I_pump² · RDS(on); I_pump = 0,4 A (Pumpennennstrom); der 3-A-Anlauf ist transient (~100 ms, Review §4.4)
22 Freilaufdiode                OK       I 400 mA (<= 50 % von 1,0 A), VRRM 40 V (>= 4 x 8,4 V) I_pump <= 0,5 A und VRRM >= 4 x VBAT_max (8,4 V)
   Begruendung: 1N5819WS-Datenblatt: 1 A / 40 V; Stromreserve und Spannungsreserve fuer die Induktivitaet der Pumpe (Freilauf gegen +5V)
23 Teilerstrom                  OK       Waechter 82,4 µA + ADC 31,3 µA = 113,7 µA bei 8,4 V <= 130 µA (beide Teiler zusammen)
   Begruendung: Teiler duerfen im Standby-Budget (250 µA) nur ein Teilbudget verbrauchen; I = VBAT_max/(R_top+R_bot) je Teiler. Seit dem UV-Teiler-Fix 16.09.2026 (51 k/51 k) zieht der Waechterteiler ~82 µA statt 21 µA -- die Obergrenze ist entsprechend angehoben (Waechter + ADC = ~113 µA, schaltplan §3.2/§13.5)
24 Unterspannungsstaffelung     OK       Firmware 6,80 V > Waechter 6,17 V > PCM 5,0 V Firmware > TPS3839 (6,16 V) > PCM
   Begruendung: Firmware stoppt zuerst, dann Hardware, zuletzt die Zelle. 1S-Schwellen aus bom §4b (3,4 V / 2,5 V) auf 2S = x2 gerechnet (Auftrag in schaltplan §4)
25 ADC-Filter                   OK       R6·C9 0,10 ms, (R_SENSE_TOP||BOT)·C10 5,1 ms, R_SPARE_AIN·C_SPARE 0,10 ms R6·C9 <= 5 ms, (R_SENSE_TOP||BOT)·C10 <= 50 ms und R_SPARE_AIN·C_SPARE <= 5 ms
   Begruendung: Espressif-ADC: 0,1 µF Filter; Zeitkonstante begrenzt das Einschwingen (Packteiler jetzt R_SENSE_TOP/BOT statt R3a/R3b)
26 Licht-ADC-Filter             OK       R_LIGHT_S·C_LIGHT 0,100 ms (R 1,0 kΩ, C 100 nF) R_LIGHT_S·C_LIGHT <= 5 ms
   Begruendung: Espressif-ADC: 0,1 µF Filter; die Zeitkonstante begrenzt das Einschwingen (gleiche Grenze wie R6·C9)
27 Licht-Kontrast               OK       dunkel 1,2 Counts, bei 10000 lx 4095 Counts (Spanne 4094, Saettigung ab 2200 lx) dunkel <= 200, hell >= 3000, Spanne > 2 x 300 Counts
   Begruendung: ALS-PT19-Datenblatt: ICEO <= 0,1 µA (dunkel), 15 µA typ @ 100 lx; R_LIGHT 10 kΩ; ADC_ATTEN_DB_12 (0-3300 mV, 12 Bit)
28 Licht-Stecker offen          OK       R_LIGHT LIGHT_RAW/GND OK, R_LIGHT_S in Reihe OK, C_LIGHT LIGHT_AOUT/GND OK, J7-3 auf LIGHT_RAW OK, ADC IO4 OK (Pfad nach GND ueber 11 kΩ) R_LIGHT LIGHT_RAW->GND, R_LIGHT_S LIGHT_RAW->LIGHT_AOUT, C_LIGHT LIGHT_AOUT->GND, J7 Pin 3 auf LIGHT_RAW, ADC = IO4
   Begruendung: offener Stecker: R_LIGHT zieht LIGHT_RAW auf 0 V, ueber R_LIGHT_S liegt der ADC auf 0 V -> kein schwebender Eingang
29 LED-Stroeme                  OK       Status (Vf 2,85 V, R4 220 Ω) 2,05 mA, Laden (Vf 2,00 V, R_LEDCHG 1,0 kΩ) 3,00 mA Status- und Lade-LED <= 5 mA
   Begruendung: I = (U - Vf)/R; D2 gruen Vf 2,85 V ueber R4 an +3V3, D_LEDCHG rot Vf 2,0 V ueber R_LEDCHG an VBUS 5 V
30 Tank-LED                     OK       1,30 mA bei Vf 2,0 V (R_TANK 1,0 kΩ) I <= 5 mA, Vf rot ca. 2,0 V
   Begruendung: LED-Vorwiderstand R_TANK an +3V3; D5 und D_LEDCHG sind die roten 0805-LEDs (Vf 2,0 V), D2 ist die gruene
31 LED-Headroom                 OK       D2 (Vf 2,85 V): Headroom 0,45 V OK, 2,05 mA OK; D_LEDCHG (Vf 2,00 V): Headroom 1,30 V OK, 3,00 mA OK; D5 (Vf 2,00 V): Headroom 1,30 V OK, 1,30 mA OK je LED 3,3 V - Vf >= 0,3 V und 0,5-5 mA
   Begruendung: 3,3-V-Rail-Headroom (aus dem AP63203-Feedback) und Stromfenster je LED; Strom aus der jeweiligen Versorgung (D_LEDCHG an 5 V VBUS)
32 Taster-Pullup                OK       BTN: R_BTN 10,0 kΩ +3V3-BTN, C_BTN 0,1 µF BTN-GND, R·C 1,00 ms R_BTN an +3V3/BTN, C_BTN an BTN/GND, 0,5-20 ms
   Begruendung: R_BTN zieht den offenen Taster auf High, C_BTN entprellt; Zeitkonstante lang genug zum Entprellen, kurz genug zum Wecken
33 Taster-Weckquelle            OK       U1 Pin 15 = IO6                    LP-GPIO (IO0-IO7) und kein Strapping-Pin
   Begruendung: Espressif ESP32-C6: LP-GPIOs IO0-IO7 wecken per EXT1; IO6 ist kein Strapping-Pin
34 Pin-Disziplin                OK       Licht 9 IO4, Pumpe 5 IO2, boot-kritisch Licht nein/Pumpe nein, Doppelbelegung keine Licht = IO4 (Pin 9, ADC1_CH4), Pumpe = IO2 (Pin 5), kein boot-kritischer Strapping-Pin (GPIO8/9/15), kein Pin doppelt
   Begruendung: ESP32-C6: boot-kritisch nur GPIO8/GPIO9 (Boot-Modus) und GPIO15 (JTAG-Quelle); IO4/IO5 sind nur SDIO-Strap und als ADC nutzbar
35 Stecker-Pinordnung           OK       J10: 1=GND 2=VCC_EXT 3=SPARE_IO15_RAW OK; J11: 1=GND 2=VCC_EXT 3=SPARE_IO16 OK; J12: 1=GND 2=VCC_EXT 3=SPARE_IO17 OK; J13: 1=GND 2=VCC_EXT 3=SPARE_IO21_RAW OK; J15: 1=GND 2=VCC_EXT 3=SPARE_IO23_RAW OK; J2: 1=GND 2=SENSOR_PWR 3=SENSOR_RAW OK; J7: 1=GND 2=SENSOR_PWR 3=LIGHT_RAW OK; J9: 1=GND 2=VCC_EXT 3=SPARE_AIN_RAW OK; J8: 1=GND 2=VCC_EXT 3=SDA 4=SCL OK Pin 1 = GND, Pin 2 = Versorgung (SENSOR_PWR/VCC_EXT), Pin 3 = Signal (J2/J7/J9-J13/J15); J8 = GND-VCC_EXT-SDA-SCL
   Begruendung: 3-poliger Stecker: nur der mittlere Pin ist gegen Umdrehen invariant. VCC auf Pin 2 kann nie 3,3 V auf einen MCU-Pin legen und nie die Sensorversorgung ueber unsere Masse kurzschliessen. Fehlerfall bei verkehrtem Stecker: GND/SIG tauschen, der 1-kOhm-Serienwiderstand begrenzt den Strom (ca. 3 mA, pin-sicher). J8 folgt der Qwiic-/STEMMA-Ordnung mit VCC auf Pin 2
36 Serienwiderstand Signale     OK       J2.3->R6(SENSOR_AOUT), Reihe, 1k, Pin 12 (IO0); J7.3->R_LIGHT_S(LIGHT_AOUT), Reihe, 1k, Pin 9 (IO4); J9.3->R_SPARE_AIN(SPARE_AIN), Reihe, 1k, Pin 10 (IO5); J10.3->R_SPARE_IO15(SPARE_IO15), Reihe, 1k, Pin 20 (IO15); J11.3->R_SPARE_IO16(UART_TX), Reihe, 1k, Pin 31 (IO16); J12.3->R_SPARE_IO17(UART_RX), Reihe, 1k, Pin 30 (IO17); J13.3->R_SPARE_IO21(SPARE_IO21), Reihe, 1k, Pin 27 (IO21); J15.3->R_SPARE_IO23(SPARE_IO23), Reihe, 1k, Pin 29 (IO23); J8.3->R_SDA_S(SDA_MCU), Reihe, 1k, Pin 24 (IO18); J8.4->R_SCL_S(SCL_MCU), Reihe, 1k, Pin 25 (IO19) je Signaleingang ein 1-kOhm-Widerstand zwischen Steckerpin und MCU-Pin
   Begruendung: Steckerkabel koennen Fehlerstroeme in die Pins treiben; der Serien-R begrenzt sie. Gilt fuer Sensor/Licht, I2C (SDA/SCL) und alle Reserve-Eingaenge (R6, R_LIGHT_S, R_SDA_S, R_SCL_S, R_SPARE_AIN, R_SPARE_IO15/16/17/21/23); J14 entfaellt
37 Load-Switch-Fail-safe        OK       Q2 S->+3V3 D->VCC_EXT G->EXT_EN, R_GATE an +3V3 OK, IO20 OK, IO20-WPU ja Source +3V3, Drain VCC_EXT, Gate ueber 47 kOhm auf +3V3, IO20 zieht das Gate nach unten, IO20 hat beim Reset WPU
   Begruendung: Load-Switch aus = Fail-safe. Ohne GPIO-Treiber (Reset, Hochohmigkeit, Deep-Sleep) liegt das Gate ueber 47 kOhm auf dem Quellpotential (VGS = 0) und Q2 sperrt. IO20 hat beim Reset einen internen Weak-Pull-up (Espressif ESP32-C6-Datenblatt), der das Gate zusaetzlich hoch haelt -> VCC_EXT ist beim Start aus
38 Sensor-Lastschalter          OK       Q_SENS S->+3V3 D->SENSOR_PWR G->EXT_SENS_EN; R_SENS_GATE 47 kΩ nach +3V3 OK; U1 Pin 6 auf EXT_SENS_EN, IO3 OK; GPIO direkt an VCC: keiner Q_SENS Source +3V3, Drain SENSOR_PWR, Gate EXT_SENS_EN; R_SENS_GATE 47 kΩ nach +3V3 (fail-safe aus); IO3 treibt nur das Gate; kein GPIO direkt an SENSOR_PWR/VCC_EXT
   Begruendung: Review 16.09.2026: die Sensorversorgung direkt aus GPIO3 ist fuer frei anschliessbare Module zu schwach; jetzt treibt IO3 (Pin 6) nur das Gate von Q_SENS (AO3401A, P-Kanal).  Der Pull-up haelt den Schalter bei hochohmigem GPIO aus (P-Kanal: V_GS = 0 sperrt), wie bei Q2
39 Erweiterungs-Pins            OK       Doppelbelegung keine; Zuordnung OK; GPIO8/9 OK kein U1-Pin doppelt, Erweiterungspins wie geplant (ohne J14/IO22), GPIO8/GPIO9 unveraendert auf ihren Strapping-Netzen
   Begruendung: Mengenpruefung der Netzliste gegen Pin-Doppelbelegung. IO22 ist seit 15.09.2026 PUMP2_EN (J16), kein Reserve-Stecker mehr; IO15 waehlt nur die JTAG-Quelle (Default-eFuses = wirkungslos) und ist ueber einen 1-kOhm-Serienwiderstand an J10 gefuehrt; IO16/IO17 bleiben UART0
40 I2C-Pull-ups                 OK       R_SDA_PU 4,7 kΩ an VCC_EXT (Pin 2), R_SCL_PU 4,7 kΩ an VCC_EXT (Pin 2), VCC_EXT geschaltet OK beide 4,7 kOhm, Pull-up-Seite VCC_EXT (nicht +3V3), VCC_EXT geschaltet
   Begruendung: Im ausgeschalteten Zustand zieht der Bus keinen Strom, weil die Pull-ups am geschalteten VCC_EXT haengen (schaltplan §9.5, Revision 15.09.2026: 4,7 kOhm). 4,7 kOhm sind fuer kurze Kabel und die ueblichen 100-kHz/400-kHz-I2C-Module plausibel
41 EN-RC                        OK       10,0 ms (R_EN 10,0 kΩ, C4 1,0 µF)  R_EN·C4 >= 1 ms
   Begruendung: Espressif: R = 10 kΩ und C = 1 µF am EN-Pin; tSTBL nur 50 µs
42 Netzstruktur                 OK       76 Netze, 122 Bauteile, 0 Befunde  jedes Bauteil auf >= 2 Netzen, jedes Netz mit >= 2 Knoten
   Begruendung: Strukturfehler wie Kurzschluss oder fehlender Anschluss (scripts/check_netlist.py)
----------------------------------------------------------------------------------------------------
Simulationen (Annahmen sind unten genannt)
----------------------------------------------------------------------------------------------------
Gate-Treiber @ 20 kHz PWM (R1 1,0 kΩ, R2 47 kΩ, Ciss 630 pF):
   Zeitkonstante tau = 0,62 µs, VGS-Endwert = 3,23 V, Zeit bis 2,5 V = 0,92 µs
   GPIO-Strom: Peak 3,300 mA, Mittel 1,752 mA (Periode 50,0 µs)
Ladezeit 2S (2000 mAh, ICHG 0,90 A):
   CC 1,78 h + CV 1,11 h = 2,89 h (grob, CC/CV-Anteile sind Annahmen)
Dosiervorgang aus der 5-V-Schiene (Pumpe 0,4 A, 2,04 W):
   0,0680 Wh pro 300 ml => 2,00 min; nutzbar 11,84 Wh => 174,1 Dosen pro Ladung
Pumpenanlauf (3,0 A, R_BAT 0,15 Ω):
   Packstrom 2,83 A, VBAT 6,0 V -> 5,58 V, Einbruch 425 mV
5-V-Buck-Rippel (Vin 8,4 V): D 0,607, dI 0,85 A, I_peak 3,43 A
3,3-V-Buck-Rippel (Vin 8,4 V): D 0,393, dI 0,39 A, I_peak 0,58 A
Teilerstroeme bei 8,4 V:
   Waechter (R3a/R3b) 82,4 µA, ADC (R_SENSE_*) 31,3 µA
Standby in mAh/Tag: 242,8 µA = 5,83 mAh/Tag (0,291 % der 2000 mAh-Packkapazitaet)
Tank-LED-Blinken (D5, R_TANK 1,0 kΩ, Vf 2,0 V): 3 x 50 ms alle 5 s (Tastverhaeltnis 3,0 %):
   Dauerbetrieb 1,30 mA, Mittel 0,04 mA -> 0,94 mAh/Tag statt 31,2 mAh/Tag
Licht-ADC (ALS-PT19, R_LIGHT 10 kΩ, ATTEN3 0-3300 mV, 12 Bit):
   0 lx -> 0 Counts (0,000 V); 100 lx -> 186 Counts (0,150 V); 1000 lx -> 1861 Counts (1,500 V); 10000 lx -> 4095 Counts (3,300 V)
Annahmen: Innenwiderstand des 2S-Packs R_BAT = 0,15 Ω (Annahme); Ladezeit: CC-Anteil 80 %, mittlerer CV-Strom 40 % von ICHG (Annahme); nutzbarer Anteil der Packkapazitaet 80 % (Annahme); Buck-Wirkungsgrad beim Anlauf 90 % (Annahme)
----------------------------------------------------------------------------------------------------
Ergebnis: 42 von 42 Pruefungen bestanden, 0 fehlgeschlagen.
```

### 7.2 Bewusste Eigenheiten der Schaltung

- **Pack-Minus ist nicht Board-Masse.** Zwischen BAT_MINUS (J1 Pin 1) und GND liegt das
-   Schutz-MOSFET-Paar (Q3 Entladen, Q4 Laden, gemeinsamer Drain). Der gesamte Systemstrom laeuft
-   darueber. Laut IP2326-Datenblatt existiert dort kein interner niederohmiger Pfad (Pin 24 ist
-   ein Detektionspin der Balancing-Funktion) - die Schutzfunktion wird also nicht ueberbrueckt.
-   Messpflicht am Aufbau: Pin 24 <-> Pin 18 am unbestromten IC hochohmig?
- **BAT_MINUS nie mit Board-GND verbinden** - jede solche Verbindung ueberbrueckt den Schutz.
- **Sicherung F1** (5 A traege) sitzt in der Pack-Plus-Leitung: die Ueberstromschwelle des
-   Schutz-IC (~17 A) schuetzt den Schaltkreis, aber nicht Kabel, Crimpkontakte und Leiterbahnen.
- **Akku-NTC an J18** mit 82 kOhm parallel. Ohne diesen Widerstand wuerde der Lader dauerhaft als
-   "zu kalt" blockieren; faellt der Stecker ab, laedt er ebenfalls nicht (fail-safe).
- **Sensorversorgung ueber Q_SENS** (P-Kanal-Lastschalter, Gate an IO3 mit Pull-up). Ein 5-V-Sensor
-   darf seinen Ausgang nicht ungeprueft an die 3,3-V-Eingaenge geben - der 1-kOhm-Serienwiderstand
-   macht keinen Eingang 5-V-fest.
- **3,3-V-Schiene ist immer an** (U_BUCK3 EN fest an VIN). Die 5-V-Schiene schaltet der Waechter
-   ab (U7 RESET treibt U_BUCK5 EN). Die frueheren Dioden-Klemmzweige an den Pumpengates sind
-   entfallen (wirkungslos); zweite Ebene bleibt der 47-kOhm-Pulldown bei hochohmiger MCU.
- **AP63203 ist die Festspannungsversion** - FB liegt direkt am Ausgang, kein Teiler.
- **J1 ist 3-polig**: 1 = Pack-Minus, 2 = Mittelabgriff, 3 = Pack-Plus.
- **Steckerordnung**: 3-polig immer GND - VCC - SIG (VCC in der Mitte), 4-polig I2C als
-   GND - VCC - SDA - SCL; in jeder Signalleitung liegt 1 kOhm in Reihe.

### 7.3 Offene Punkte fuer einen externen Review

- **Messauftrag am Aufbau**: Anlauf-, Dauer- und Blockierstrom beider Pumpen; Schwellen des HY2120
-   (4,28 V / 2,90 V pro Zelle); Balancing-Strom ueber R_CB; Widerstand Pin 24 <-> Pin 18 des IP2326
-   am unbestromten IC.
- **Ladestrom**: 0,90 A (+-10 %) ist gesetzt; die zulaessige Hoehe haengt am konkreten Zelltyp.
- **Quelle**: keine BC1.2-Erkennung und keine Eingangsstrombegrenzung im Lader - eine 5-V/2-A-Quelle
-   verwenden (Ladeleistung 7,56 W, rechnerisch ~1,68 A Eingangsstrom).
- **Packschutz**: zusaetzlich zur Bordsicherung die Schutzeinrichtung des Packs nutzen/dokumentieren.
- **Kondensatoren**: wirksame Kapazitaet der 22-uF-MLCCs unter DC-Bias pruefen.
- **Layout**: Schaltstromschleifen, Thermal-Pads, ADC-Masse und Antennen-Keep-out sind erst im
-   Layout beurteilbar.

