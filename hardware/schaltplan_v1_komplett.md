# SmartGrowTopf V1 — kompletter Schaltplan in Textform

> **Zweck dieser Datei:** vollständige, maschinenlesbare Beschreibung der Schaltung für ein Sprachmodell:
> **was** verbaut ist, **wo** es auf dem Blatt sitzt und **wie** alles verkabelt ist. Erzeugt direkt aus der
> Projekt-IR (`hardware/easyeda/raw/ir_numbered.json`) — die Zahlen sind nicht geschätzt, sondern ausgelesen.

| Kennzahl | Wert |
|---|---|
| Bauteile | **93** |
| Netze | **54** |
| Verbindungen (Pin→Netz) | **262** |
| Pins insgesamt / davon verbunden | 279 / 262 |
| Funktionsblöcke (mit Rahmen) | **13** |
| MCU | **ESP32-C6-MINI-1** (U1, 53 Pins) |
| Versorgung | USB-C → MCP73831 Lader → 1S-LiPo (VBAT 3,0–4,2 V) → {ME6211 LDO → **+3V3** Logik · MT3608 Boost → **+5V** Pumpen} |

## 1. Versorgungskette (wie der Strom läuft)

```
USB-C (J5) ──► USBLC6 ESD (U6) ──► VBUS ──► MCP73831 Lader (U3) ──► VBAT (1S-LiPo, J1)
                                                   │
                                                   ├──► ME6211 LDO (U4) ──► +3V3 ──► ESP32-C6 (U1), Sensor, LEDs, Wächter
                                                   └──► MT3608 Boost (U8) ──► +5V ──┬──► Q1 ──► J4  Dosierpumpe
                                                        (Vout = 5,10 V)            └──► Q3 ──► J16 Sauerstoffpumpe (optional)
```

- **VBAT** = Zellspannung, ungeregelt. **+5V** gibt es nur, weil der Boost **U8** sie erzeugt — deshalb liegen
  **beide** Pumpen an +5V (früher hing die Dosierpumpe direkt an VBAT).
- **MAX809 (U7)** wacht über VBAT: unter ≈ **3,08 V** zieht er RESET_UV auf Low und sperrt über D3/D8 die
  Pumpentreiber → Pumpe kann die Zelle nicht tiefentladen.

## 2. Was ist verbaut (alle 93 Bauteile)

Spalte **Modul** = Funktionsblock auf dem Blatt (= der Rahmen, in dem das Teil sitzt).

| Ref | Modul | Typ / Wert | Gehäuse | LCSC | Funktion |
|---|---|---|---|---|---|
| **C1** | MCU | CC0805KRX7R9BB104 | — | `—` | Decoupling Modul 100 nF |
| **C2** | MCU | 22uF | 0805 | `C45783` | Bulk 22 uF am Modul-3V3 |
| **C3** | AKKU | 100uF | SMD D6.3x5.4 | `C970684` | Elko 100 uF Pumpenpuffer |
| **C4** | MCU | 1uF | 0603 | `C15849` | EN-RC 1 uF |
| **C5** | LDO | 10uF | 0805 | `C15850` | LDO-Eingang 10 uF |
| **C6** | LDO | 1uF | 0603 | `C15849` | LDO-Ausgang 1 uF |
| **C7** | LADER | 4.7uF | 0805 | `C1779` | Lader-Eingang 4,7 uF |
| **C8** | LADER | 4.7uF | 0805 | `C1779` | Lader-Ausgang 4,7 uF |
| **C9** | MCU | 100nF | 0805 | `C49678` | ADC-Filter Sensor 100 nF |
| **C10** | MCU | 100nF | 0805 | `C49678` | ADC-Filter VBAT 100 nF |
| **C11** | PUMPE | 100nF | 0805 | `C49678` | EMI an Pumpenklemmen 100 nF |
| **C12** | WAEChTER | 100nF | 0805 | `C49678` | Decoupling MAX809 100 nF |
| **C13** | MCU | CC0805KRX7R9BB104 | — | `—` | Decoupling Modul 100 nF |
| **C14** | TASTER | CC0805KRX7R9BB104 | — | `—` | Taster-Entprellung 100 nF |
| **C15** | LICHT | 100nF | 0805 | `C49678` | ADC-Filter Licht 100 nF |
| **C16** | ERWEITERUNG | 100nF | 0805 | `C49678` | ADC-Filter Reserve-Analog 100 nF |
| **C17** | BOOST | 22uF | 0805 | `C45783` | Boost-Eingang 22 uF |
| **C18** | BOOST | 22uF | 0805 | `C45783` | Boost-Ausgang 22 uF |
| **C19** | BOOST | CC0805KRX7R9BB104 | — | `—` | Boost-Ausgang HF 100 nF |
| **C20** | PUMPE | CC0805KRX7R9BB104 | — | `—` | EMI an den Klemmen Sauerstoffpumpe 100 nF |
| **D1** | PUMPE | 1N5819WS | SOD-323 | `C191023` | Freilaufdiode Pumpe |
| **D2** | MCU | LED-GREEN | 0805 | `C2297` | Status-LED gruen 525 nm |
| **D3** | PUMPE | 1N5819WS | SOD-323 | `C191023` | Klemmzweig Gate |
| **D5** | MCU | LED-RED | 0805 | `C84256` | Tank-leer-LED rot |
| **D6** | BOOST | SS34 | SMA(DO-214AC) | `C8678` | Boost-Diode SS34 3A/40V |
| **D7** | PUMPE | 1N5819WS | SOD-323 | `C191023` | Freilaufdiode Sauerstoffpumpe |
| **D8** | PUMPE | 1N5819WS | SOD-323 | `C191023` | Klemmzweig Gate Sauerstoffpumpe |
| **J1** | AKKU | JST-PH-2P | SMD P2.0 aufrecht (Top-Entry) | `C160352` | Akku JST-PH 2P aufrecht (Top-Entry) |
| **J2** | SENSOR | JST-XH-3P | THT P2.5 aufrecht (Top-Entry) | `C493416` | Sensor JST-XH 3P aufrecht (Top-Entry) |
| **J4** | PUMPE | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Dosierpumpe JST-XH 2P aufrecht (Top-Entry) |
| **J5** | USB | USB-C-16P | SMD | `C165948` | USB-C 16P Buchse |
| **J6** | TASTER | HDR-TH 2P, 2,54 mm | 2x Loch 1.0mm Raster 2.54mm | `—` | 2 Loetpads externer Taster |
| **J7** | LICHT | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Lichtsensor Stiftleiste 1x3 2.54 mm (extern) |
| **J8** | ERWEITERUNG | Stiftleiste-1x4-2.54mm | THT P2.54 gerade | `C2691448` | I2C Stiftleiste 1x4 (GND-VCC-SDA-SCL) |
| **J9** | ERWEITERUNG | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve-Analog Stiftleiste 1x3 (IO5) |
| **J10** | ERWEITERUNG | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO15 Stiftleiste 1x3 |
| **J11** | ERWEITERUNG | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO16 (TXD0) Stiftleiste 1x3 |
| **J12** | ERWEITERUNG | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO17 (RXD0) Stiftleiste 1x3 |
| **J13** | ERWEITERUNG | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO21 Stiftleiste 1x3 |
| **J15** | ERWEITERUNG | Stiftleiste-1x3-2.54mm | THT P2.54 gerade | `C2937625` | Reserve IO23 Stiftleiste 1x3 |
| **J16** | PUMPE | JST-XH-2P | THT P2.5 aufrecht (Top-Entry) | `C158012` | Sauerstoffpumpe JST-XH 2P aufrecht |
| **L1** | BOOST | 22uH | SMD 6x6mm | `C341068` | Boost-Induktivitaet 22 uH YNR6045 |
| **LED1** | LADER | NCD0805R1 | — | `—` | Ladestatus-LED rot |
| **Q1** | PUMPE | AO3400A | SOT-23 | `C20917` | N-MOSFET Pumpentreiber |
| **Q2** | ERWEITERUNG | AO3401A | SOT-23 | `C15127` | P-Kanal-Load-Switch VCC_EXT |
| **Q3** | PUMPE | AO3400A | SOT-23 | `C20917` | N-MOSFET Sauerstoffpumpe |
| **R1** | PUMPE | 4.7k | 0805 | `C17673` | Gate-Serie 4,7 k |
| **R2** | PUMPE | 47k | 0805 | `C17713` | Gate-Pulldown 47 k |
| **R3** | WAEChTER | 0805W8F2003T5E | — | `—` | VBAT-Teiler oben 200 k |
| **R4** | MCU | 220R | 0805 | `C17557` | Status-LED 220 R |
| **R5** | WAEChTER | 0805W8F2003T5E | — | `—` | VBAT-Teiler unten 200 k |
| **R6** | SENSOR | 1k | 0805 | `C17513` | Sensor-AOUT Serie 1 k |
| **R7** | USB | 0805W8F5101T5E | — | `—` | CC1-Pulldown 5,1 k |
| **R8** | USB | 0805W8F5101T5E | — | `—` | CC2-Pulldown 5,1 k |
| **R9** | MCU | 0805W8F1002T5E | — | `—` | EN-Pull-up 10 k |
| **R10** | MCU | 0805W8F1002T5E | — | `—` | GPIO9-Pull-up 10 k |
| **R11** | MCU | 0805W8F1002T5E | — | `—` | GPIO8-Strap-Pull-up 10 k |
| **R12** | TASTER | 0805W8F1002T5E | — | `—` | Taster-Pull-up 10 k |
| **R13** | LADER | 0805W8F3901T5E | — | `—` | Ladestrom 3,9 k -> 256 mA |
| **R14** | LADER | 0805W8F1001T5E | — | `—` | Lade-LED 1 k |
| **R15** | MCU | 0805W8F1001T5E | — | `—` | Tank-LED 1 k |
| **R16** | DEBUG | 0805W8F4990T5E | — | `—` | TXD0-Serie 499 R (DNP) |
| **R17** | LICHT | 0805W8F1002T5E | — | `—` | Licht-Lastwiderstand 10 k nach GND |
| **R18** | LICHT | 0805W8F1001T5E | — | `—` | Licht-Serienschutz 1 k zum ADC |
| **R19** | ERWEITERUNG | 0805W8F1002T5E | — | `—` | I2C SDA Pull-up 10 k an VCC_EXT |
| **R20** | ERWEITERUNG | 4.7k | 0805 | `C17673` | I2C SCL Pull-up 10 k an VCC_EXT |
| **R21** | ERWEITERUNG | 47k | 0805 | `C17713` | I2C SDA Serienschutz 1 k |
| **R22** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | I2C SCL Serienschutz 1 k |
| **R23** | ERWEITERUNG | 0805W8F4702T5E | — | `—` | Gate-Pull-up Load-Switch 47 k |
| **R24** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | Reserve-AIN Serienschutz 1 k |
| **R25** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | Reserve IO15 Serienschutz 1 k |
| **R26** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | Reserve IO16 Serienschutz 1 k |
| **R27** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | Reserve IO17 Serienschutz 1 k |
| **R28** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | Reserve IO21 Serienschutz 1 k |
| **R30** | ERWEITERUNG | 0805W8F1001T5E | — | `—` | Reserve IO23 Serienschutz 1 k |
| **R31** | BOOST | 75k | 0805 | `C17819` | Feedback oben 75 k -> 5,10 V |
| **R32** | BOOST | 0805W8F1002T5E | — | `—` | Feedback unten 10 k |
| **R33** | PUMPE | 0805W8F4701T5E | — | `—` | Gate-Serie 4,7 k |
| **R34** | PUMPE | 0805W8F4702T5E | — | `—` | Gate-Pulldown 47 k |
| **SW1** | MCU | SW-SMD | SMD-4P 5.1x5.1 | `C318884` | Reset-Taster |
| **SW2** | MCU | SW-SMD | SMD-4P 5.1x5.1 | `C318884` | Boot-Taster |
| **TP1** | DEBUG | 5010-Testpoint | — | `—` | Testpad TXD0 |
| **TP2** | MCU | 5010-Testpoint | — | `—` | Testpad RXD0 |
| **TP3** | AKKU | 5010-Testpoint | — | `—` | Testpad GND |
| **TP4** | AKKU | 5010-Testpoint | — | `—` | Testpad VBAT |
| **TP5** | LDO | 5010-Testpoint | — | `—` | Testpad +3V3 |
| **TP6** | SENSOR | 5010-Testpoint | — | `—` | Testpad SENSOR_AOUT |
| **U1** | MCU | ESP32-C6-MINI-1 | SMD-53P | `C5736265` | ESP32-C6-MINI-1 WLAN-Modul |
| **U3** | LADER | MCP73831T-2ACI/OT | SOT-23-5 | `C424093` | 1S-LiPo-Lader 4,20 V |
| **U4** | LDO | ME6211C33M5G | SOT-23-5 | `C82942` | LDO 3,3 V / 500 mA |
| **U6** | USB | USBLC6-2SC6 | SOT-23-6L | `C7519` | USB-ESD-Schutz USBLC6-2SC6 |
| **U7** | WAEChTER | MAX809TEUR+T | SOT-23 | `C16711` | Unterspannungswaechter 3,08 V |
| **U8** | BOOST | MT3608 | SOT-23-6 | `C84817` | MT3608 Aufwaertsregler 5 V |

## 3. Wie ist verkabelt (Netz für Netz — das ist die eigentliche Verkabelung)

Jedes Netz listet **alle** Pins, die daran hängen. `Ref:Pin (Pinname)` — der Pinname ist der Name am Symbol.

### Netz `+3V3`  (power, 13 Pins)

- `C1:1`  — MCU
- `C2:1`  — MCU
- `C6:1`  — LDO
- `C13:1`  — MCU
- `Q2:2` (S)  — ERWEITERUNG
- `R9:1`  — MCU
- `R10:1`  — MCU
- `R11:1`  — MCU
- `R12:1`  — TASTER
- `R23:1`  — ERWEITERUNG
- `TP5:1`  — LDO
- `U1:3` (3V3)  — MCU
- `U4:5` (VOUT)  — LDO

### Netz `+5V`  (power, 8 Pins)

- `C18:1`  — BOOST
- `C19:1`  — BOOST
- `D1:1` (K)  — PUMPE
- `D6:1` (K)  — BOOST
- `D7:1` (K)  — PUMPE
- `J4:1`  — PUMPE
- `J16:1`  — PUMPE
- `R31:1`  — BOOST

### Netz `VBAT`  (power, 16 Pins)

- `C3:1`  — AKKU
- `C5:1`  — LDO
- `C8:1`  — LADER
- `C11:2`  — PUMPE
- `C12:1`  — WAEChTER
- `C17:1`  — BOOST
- `J1:1`  — AKKU
- `L1:1`  — BOOST
- `R3:1`  — WAEChTER
- `TP4:1`  — AKKU
- `U3:3` (VBAT)  — LADER
- `U4:1` (VIN)  — LDO
- `U4:3` (CE)  — LDO
- `U7:3` (VCC)  — WAEChTER
- `U8:4` (EN)  — BOOST
- `U8:5` (IN)  — BOOST

### Netz `VBUS`  (power, 6 Pins)

- `C7:1`  — LADER
- `J5:A4B9` (VBUS)  — USB
- `J5:B4A9` (VBUS)  — USB
- `R14:1`  — LADER
- `U3:4` (VDD)  — LADER
- `U6:5`  — USB

### Netz `GND`  (ground, 78 Pins)

- `C1:2`  — MCU
- `C2:2`  — MCU
- `C3:2`  — AKKU
- `C4:2`  — MCU
- `C5:2`  — LDO
- `C6:2`  — LDO
- `C7:2`  — LADER
- `C8:2`  — LADER
- `C9:2`  — MCU
- `C10:2`  — MCU
- `C12:2`  — WAEChTER
- `C13:2`  — MCU
- `C14:2`  — TASTER
- `C15:2`  — LICHT
- `C16:2`  — ERWEITERUNG
- `C17:2`  — BOOST
- `C18:2`  — BOOST
- `C19:2`  — BOOST
- `C20:2`  — PUMPE
- `D2:2` (K)  — MCU
- `D5:1` (-)  — MCU
- `J1:2`  — AKKU
- `J2:1`  — SENSOR
- `J5:1` (EH)  — USB
- `J5:2` (EH)  — USB
- `J5:3` (EH)  — USB
- `J5:4` (EH)  — USB
- `J5:A1B12` (GND)  — USB
- `J5:B1A12` (GND)  — USB
- `J6:2`  — TASTER
- `J7:1`  — LICHT
- `J8:1`  — ERWEITERUNG
- `J9:1`  — ERWEITERUNG
- `J10:1`  — ERWEITERUNG
- `J11:1`  — ERWEITERUNG
- `J12:1`  — ERWEITERUNG
- `J13:1`  — ERWEITERUNG
- `J15:1`  — ERWEITERUNG
- `Q1:2` (S)  — PUMPE
- `Q3:2` (S)  — PUMPE
- `R2:2`  — PUMPE
- `R5:2`  — WAEChTER
- `R7:2`  — USB
- `R8:2`  — USB
- `R13:2`  — LADER
- `R17:2`  — LICHT
- `R32:2`  — BOOST
- `R34:2`  — PUMPE
- `SW1:2` (B)  — MCU
- `SW2:2` (B)  — MCU
- `TP3:1`  — AKKU
- `U1:1` (GND)  — MCU
- `U1:11` (GND)  — MCU
- `U1:14` (GND)  — MCU
- `U1:2` (GND)  — MCU
- `U1:36` (GND)  — MCU
- `U1:37` (GND)  — MCU
- `U1:38` (GND)  — MCU
- `U1:39` (GND)  — MCU
- `U1:40` (GND)  — MCU
- `U1:41` (GND)  — MCU
- `U1:42` (GND)  — MCU
- `U1:43` (GND)  — MCU
- `U1:44` (GND)  — MCU
- `U1:45` (GND)  — MCU
- `U1:46` (GND)  — MCU
- `U1:47` (GND)  — MCU
- `U1:48` (GND)  — MCU
- `U1:49` (GND)  — MCU
- `U1:50` (GND)  — MCU
- `U1:51` (GND)  — MCU
- `U1:52` (GND)  — MCU
- `U1:53` (GND)  — MCU
- `U3:2` (VSS)  — LADER
- `U4:2` (VSS)  — LDO
- `U6:2`  — USB
- `U7:1` (GND)  — WAEChTER
- `U8:2` (GND)  — BOOST

### Netz `BOOT`  (signal, 3 Pins)

- `R10:2`  — MCU
- `SW2:1` (A)  — MCU
- `U1:23` (IO9)  — MCU

### Netz `BTN`  (signal, 4 Pins)

- `C14:1`  — TASTER
- `J6:1`  — TASTER
- `R12:2`  — TASTER
- `U1:15` (IO6)  — MCU

### Netz `CC1`  (signal, 2 Pins)

- `J5:A5` (CC1)  — USB
- `R7:1`  — USB

### Netz `CC2`  (signal, 2 Pins)

- `J5:B5` (CC2)  — USB
- `R8:1`  — USB

### Netz `EN`  (signal, 4 Pins)

- `C4:1`  — MCU
- `R9:2`  — MCU
- `SW1:1` (A)  — MCU
- `U1:8` (EN)  — MCU

### Netz `EXT_EN`  (signal, 3 Pins)

- `Q2:1` (G)  — ERWEITERUNG
- `R23:2`  — ERWEITERUNG
- `U1:26` (IO20)  — MCU

### Netz `FB_5V`  (signal, 3 Pins)

- `R31:2`  — BOOST
- `R32:1`  — BOOST
- `U8:3` (FB)  — BOOST

### Netz `GATE`  (signal, 4 Pins)

- `D3:2` (A)  — PUMPE
- `Q1:1` (G)  — PUMPE
- `R1:2`  — PUMPE
- `R2:1`  — PUMPE

### Netz `GATE2`  (signal, 4 Pins)

- `D8:2` (A)  — PUMPE
- `Q3:1` (G)  — PUMPE
- `R33:2`  — PUMPE
- `R34:1`  — PUMPE

### Netz `GPIO8_STRAP`  (signal, 2 Pins)

- `R11:2`  — MCU
- `U1:22` (IO8)  — MCU

### Netz `LED_CHG`  (signal, 2 Pins)

- `LED1:2` (+)  — LADER
- `R14:2`  — LADER

### Netz `LED_STAT`  (signal, 2 Pins)

- `R4:1`  — MCU
- `U1:19` (IO14)  — MCU

### Netz `LED_STAT_A`  (signal, 2 Pins)

- `D2:1` (A)  — MCU
- `R4:2`  — MCU

### Netz `LED_TANK`  (signal, 2 Pins)

- `R15:1`  — MCU
- `U1:16` (IO7)  — MCU

### Netz `LED_TANK_A`  (signal, 2 Pins)

- `D5:2` (+)  — MCU
- `R15:2`  — MCU

### Netz `LIGHT_AOUT`  (signal, 3 Pins)

- `C15:1`  — LICHT
- `R18:2`  — LICHT
- `U1:9` (IO4)  — MCU

### Netz `LIGHT_RAW`  (signal, 3 Pins)

- `J7:3`  — LICHT
- `R17:1`  — LICHT
- `R18:1`  — LICHT

### Netz `PROG`  (signal, 2 Pins)

- `R13:1`  — LADER
- `U3:5` (PROG)  — LADER

### Netz `PUMP2_EN`  (signal, 2 Pins)

- `R33:1`  — PUMPE
- `U1:28` (IO22)  — MCU

### Netz `PUMP2_N`  (signal, 4 Pins)

- `C20:1`  — PUMPE
- `D7:2` (A)  — PUMPE
- `J16:2`  — PUMPE
- `Q3:3` (D)  — PUMPE

### Netz `PUMP_EN`  (signal, 2 Pins)

- `R1:1`  — PUMPE
- `U1:5` (IO2)  — MCU

### Netz `PUMP_N`  (signal, 4 Pins)

- `C11:1`  — PUMPE
- `D1:2` (A)  — PUMPE
- `J4:2`  — PUMPE
- `Q1:3` (D)  — PUMPE

### Netz `RESET_UV`  (signal, 3 Pins)

- `D3:1` (K)  — PUMPE
- `D8:1` (K)  — PUMPE
- `U7:2` (RESET)  — WAEChTER

### Netz `SCL`  (signal, 3 Pins)

- `J8:4`  — ERWEITERUNG
- `R20:1`  — ERWEITERUNG
- `R22:2`  — ERWEITERUNG

### Netz `SCL_MCU`  (signal, 2 Pins)

- `R22:1`  — ERWEITERUNG
- `U1:25` (IO19)  — MCU

### Netz `SDA`  (signal, 3 Pins)

- `J8:3`  — ERWEITERUNG
- `R19:1`  — ERWEITERUNG
- `R21:2`  — ERWEITERUNG

### Netz `SDA_MCU`  (signal, 2 Pins)

- `R21:1`  — ERWEITERUNG
- `U1:24` (IO18)  — MCU

### Netz `SENSOR_AOUT`  (signal, 4 Pins)

- `C9:1`  — MCU
- `R6:2`  — SENSOR
- `TP6:1`  — SENSOR
- `U1:12` (IO0)  — MCU

### Netz `SENSOR_PWR`  (signal, 3 Pins)

- `J2:2`  — SENSOR
- `J7:2`  — LICHT
- `U1:6` (IO3)  — MCU

### Netz `SENSOR_RAW`  (signal, 2 Pins)

- `J2:3`  — SENSOR
- `R6:1`  — SENSOR

### Netz `SPARE_AIN`  (signal, 3 Pins)

- `C16:1`  — ERWEITERUNG
- `R24:2`  — ERWEITERUNG
- `U1:10` (IO5)  — MCU

### Netz `SPARE_AIN_RAW`  (signal, 2 Pins)

- `J9:3`  — ERWEITERUNG
- `R24:1`  — ERWEITERUNG

### Netz `SPARE_IO15`  (signal, 2 Pins)

- `R25:2`  — ERWEITERUNG
- `U1:20` (IO15)  — MCU

### Netz `SPARE_IO15_RAW`  (signal, 2 Pins)

- `J10:3`  — ERWEITERUNG
- `R25:1`  — ERWEITERUNG

### Netz `SPARE_IO16`  (signal, 2 Pins)

- `J11:3`  — ERWEITERUNG
- `R26:2`  — ERWEITERUNG

### Netz `SPARE_IO17`  (signal, 2 Pins)

- `J12:3`  — ERWEITERUNG
- `R27:2`  — ERWEITERUNG

### Netz `SPARE_IO21`  (signal, 2 Pins)

- `R28:2`  — ERWEITERUNG
- `U1:27` (IO21)  — MCU

### Netz `SPARE_IO21_RAW`  (signal, 2 Pins)

- `J13:3`  — ERWEITERUNG
- `R28:1`  — ERWEITERUNG

### Netz `SPARE_IO23`  (signal, 2 Pins)

- `R30:2`  — ERWEITERUNG
- `U1:29` (IO23)  — MCU

### Netz `SPARE_IO23_RAW`  (signal, 2 Pins)

- `J15:3`  — ERWEITERUNG
- `R30:1`  — ERWEITERUNG

### Netz `STAT_CHG`  (signal, 2 Pins)

- `LED1:1` (-)  — LADER
- `U3:1` (STAT)  — LADER

### Netz `SW_BOOST`  (signal, 3 Pins)

- `D6:2` (A)  — BOOST
- `L1:2`  — BOOST
- `U8:1` (SW)  — BOOST

### Netz `UART_RX`  (signal, 3 Pins)

- `R27:1`  — ERWEITERUNG
- `TP2:1`  — MCU
- `U1:30` (RXD0)  — MCU

### Netz `UART_TP`  (signal, 2 Pins)

- `R16:2`  — DEBUG
- `TP1:1`  — DEBUG

### Netz `UART_TX`  (signal, 3 Pins)

- `R16:1`  — DEBUG
- `R26:1`  — ERWEITERUNG
- `U1:31` (TXD0)  — MCU

### Netz `USB_DM`  (signal, 5 Pins)

- `J5:A7` (DN1)  — USB
- `J5:B7` (DN2)  — USB
- `U1:17` (IO12)  — MCU
- `U6:3`  — USB
- `U6:4`  — USB

### Netz `USB_DP`  (signal, 5 Pins)

- `J5:A6` (DP1)  — USB
- `J5:B6` (DP2)  — USB
- `U1:18` (IO13)  — MCU
- `U6:1`  — USB
- `U6:6`  — USB

### Netz `VBAT_SENSE`  (signal, 4 Pins)

- `C10:1`  — MCU
- `R3:2`  — WAEChTER
- `R5:1`  — WAEChTER
- `U1:13` (IO1)  — MCU

### Netz `VCC_EXT`  (signal, 10 Pins)

- `J8:2`  — ERWEITERUNG
- `J9:2`  — ERWEITERUNG
- `J10:2`  — ERWEITERUNG
- `J11:2`  — ERWEITERUNG
- `J12:2`  — ERWEITERUNG
- `J13:2`  — ERWEITERUNG
- `J15:2`  — ERWEITERUNG
- `Q2:3` (D)  — ERWEITERUNG
- `R19:2`  — ERWEITERUNG
- `R20:2`  — ERWEITERUNG

## 4. Wo ist was verbaut (Funktionsblöcke mit Rahmen auf dem Blatt)

Die Blattkoordinaten sind EasyEDA-Einheiten (1/100 inch). `x0..x1` / `y0..y1` ist der Rahmen des Blocks.

| Block | Rahmen x0..x1 | y0..y1 | Bauteile | Zweck |
|---|---|---|---|---|
| **AKKU** | 2477..3013 | 1685..2068 | C3, J1, TP3, TP4 | Akku, Puffer, Ladezustands-LED |
| **BOOST** | 897..1581 | 1011..1587 | C17, C18, C19, D6, L1, R31, R32, U8 | 5-V-Boost (MT3608) aus VBAT |
| **DEBUG** | 2020..2477 | 1685..2148 | R16, TP1 | UART-Debug-Pads (unbestückt) |
| **ERWEITERUNG** | 12..897 | 12..1135 | C16, J10, J11, J12, J13, J15, J8, J9, Q2, R19, R20, R21, R22, R23, R24, R25, R26, R27, R28, R30 | freie GPIOs auf Stiftleisten |
| **LADER** | 602..1562 | 1587..2096 | C7, C8, LED1, R13, R14, U3 | 1S-Laderegler |
| **LDO** | 12..509 | 1650..2124 | C5, C6, TP5, U4 | 3,3-V-Regler |
| **LICHT** | 2330..3027 | 1174..1685 | C15, J7, R17, R18 | Lichtsensor-Eingang |
| **MCU** | 897..1810 | 12..1011 | C1, C10, C13, C2, C4, C9, D2, D5, R10, R11, R15, R4, R9, SW1, SW2, TP2, U1 | ESP32-C6 + Beschaltung |
| **PUMPE** | 2405..3168 | 198..1174 | C11, C20, D1, D3, D7, D8, J16, J4, Q1, Q3, R1, R2, R33, R34 | Pumpentreiber Dosier- **und** Sauerstoffpumpe |
| **SENSOR** | 12..602 | 1135..1650 | J2, R6, TP6 | Bodenfeuchte-Sensor Eingang |
| **TASTER** | 1562..2020 | 1599..2099 | C14, J6, R12 | Bedientaster |
| **USB** | 1810..2405 | 12..1006 | J5, R7, R8, U6 | USB-C Eingang + ESD |
| **WAEChTER** | 1810..2330 | 1006..1599 | C12, R3, R5, U7 | Unterspannungswächter |
## 5. Anschlüsse nach außen (Stecker, Buchsen, Testpunkte) — Pin für Pin

**Das ist die Liste für „was stecke ich wo an"** — jeder Außenanschluss mit seiner Belegung.

### J1 — JST-PH-2P  (AKKU)
*extended - Akku; Polung im Layout pruefen*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `VBAT` | Akku (1S LiPo) 1 |
| 2 | `GND` | Akku (1S LiPo) 2 |
| 3 | `— (unbelegt)` | Akku (1S LiPo) 3 |
| 4 | `— (unbelegt)` | Akku (1S LiPo) 4 |

### J2 — JST-XH-3P  (SENSOR)
*extended - Feuchtesensor (gerastet*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | Bodenfeuchte-Sensor 1 |
| 2 | `SENSOR_PWR` | Bodenfeuchte-Sensor 2 |
| 3 | `SENSOR_RAW` | Bodenfeuchte-Sensor 3 |

### J4 — JST-XH-2P, aufrecht  (PUMPE)
*Kanal 1: Dosierpumpe (CONQUERALL DC 5 V, ≤150 ml/min)*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `+5V` | Dosierpumpe (+5 V geschaltet) |
| 2 | `PUMP_N` | Dosierpumpe (+5 V geschaltet) |

### J5 — USB-C-16P  (USB)
*extended - Buchse*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | USB-C Eingang (Laden + Programmieren) EH |
| 2 | `GND` | USB-C Eingang (Laden + Programmieren) EH |
| 3 | `GND` | USB-C Eingang (Laden + Programmieren) EH |
| 4 | `GND` | USB-C Eingang (Laden + Programmieren) EH |
| A5 | `CC1` | USB-C Eingang (Laden + Programmieren) CC1 |
| A6 | `USB_DP` | USB-C Eingang (Laden + Programmieren) DP1 |
| A7 | `USB_DM` | USB-C Eingang (Laden + Programmieren) DN1 |
| A8 | `— (unbelegt)` | USB-C Eingang (Laden + Programmieren) SBU1 |
| B5 | `CC2` | USB-C Eingang (Laden + Programmieren) CC2 |
| B6 | `USB_DP` | USB-C Eingang (Laden + Programmieren) DP2 |
| B7 | `USB_DM` | USB-C Eingang (Laden + Programmieren) DN2 |
| B8 | `— (unbelegt)` | USB-C Eingang (Laden + Programmieren) SBU2 |
| A4B9 | `VBUS` | USB-C Eingang (Laden + Programmieren) VBUS |
| B4A9 | `VBUS` | USB-C Eingang (Laden + Programmieren) VBUS |
| A1B12 | `GND` | USB-C Eingang (Laden + Programmieren) GND |
| B1A12 | `GND` | USB-C Eingang (Laden + Programmieren) GND |

### J6 — HDR-TH 2P, 2,54 mm  (TASTER)
*KEINE BESTUECKUNG - nur Lotpads fuer den externen Taster*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `BTN` | 1 |
| 2 | `GND` | 2 |

### J7 — Stiftleiste-1x3-2.54mm  (LICHT)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `SENSOR_PWR` | 2 |
| 3 | `LIGHT_RAW` | 3 |

### J8 — Stiftleiste-1x4-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-04P; I2C GND-VCC-SDA-SCL*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SDA` | 3 |
| 4 | `SCL` | 4 |

### J9 — Stiftleiste-1x3-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SPARE_AIN_RAW` | 3 |

### J10 — Stiftleiste-1x3-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SPARE_IO15_RAW` | 3 |

### J11 — Stiftleiste-1x3-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SPARE_IO16` | 3 |

### J12 — Stiftleiste-1x3-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SPARE_IO17` | 3 |

### J13 — Stiftleiste-1x3-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SPARE_IO21_RAW` | 3 |

### J15 — Stiftleiste-1x3-2.54mm  (ERWEITERUNG)
*extended - XFCN PZ254V-11-03P; GND-VCC-SIG (VCC immer Pin 2) fuer Lichtsensor + Reserve-IO*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `GND` | 1 |
| 2 | `VCC_EXT` | 2 |
| 3 | `SPARE_IO23_RAW` | 3 |

### J16 — JST-XH-2P, aufrecht  (PUMPE)
*Kanal 2: Sauerstoffpumpe (optional) — baugleicher Stecker wie J4, ein Crimp-Werkzeug für beide*

| Pin | Netz | wozu |
|---|---|---|
| 1 | `+5V` | Sauerstoffpumpe, optional (+5 V geschaltet) |
| 2 | `PUMP2_N` | Sauerstoffpumpe, optional (+5 V geschaltet) |

### Testpunkte (nur Messpunkte, nicht bestückt)

| Ref | Netz | Zweck |
|---|---|---|
| TP1 | `UART_TP` | UART TX (Debug) |
| TP2 | `UART_RX` | Freigabe/Reset-Netz des Wächters |
| TP3 | `GND` | Akku-Plus (VBAT) messen |
| TP4 | `VBAT` | Masse (GND) messen |
| TP5 | `+3V3` | +3V3 messen |
| TP6 | `SENSOR_AOUT` | Sensor-Analogspannung messen |

## 6. Mikrocontroller U1 (ESP32-C6-MINI-1) — komplette Pinbelegung

| Pin | Symbolname | Netz |
|---|---|---|
| 1 | GND | `GND` |
| 2 | GND | `GND` |
| 3 | 3V3 | `+3V3` |
| 4 | NC | `—` |
| 5 | IO2 | `PUMP_EN` |
| 6 | IO3 | `SENSOR_PWR` |
| 7 | NC | `—` |
| 8 | EN | `EN` |
| 9 | IO4 | `LIGHT_AOUT` |
| 10 | IO5 | `SPARE_AIN` |
| 11 | GND | `GND` |
| 12 | IO0 | `SENSOR_AOUT` |
| 13 | IO1 | `VBAT_SENSE` |
| 14 | GND | `GND` |
| 15 | IO6 | `BTN` |
| 16 | IO7 | `LED_TANK` |
| 17 | IO12 | `USB_DM` |
| 18 | IO13 | `USB_DP` |
| 19 | IO14 | `LED_STAT` |
| 20 | IO15 | `SPARE_IO15` |
| 21 | NC | `—` |
| 22 | IO8 | `GPIO8_STRAP` |
| 23 | IO9 | `BOOT` |
| 24 | IO18 | `SDA_MCU` |
| 25 | IO19 | `SCL_MCU` |
| 26 | IO20 | `EXT_EN` |
| 27 | IO21 | `SPARE_IO21` |
| 28 | IO22 | `PUMP2_EN` |
| 29 | IO23 | `SPARE_IO23` |
| 30 | RXD0 | `UART_RX` |
| 31 | TXD0 | `UART_TX` |
| 32 | NC | `—` |
| 33 | NC | `—` |
| 34 | NC | `—` |
| 35 | NC | `—` |
| 36 | GND | `GND` |
| 37 | GND | `GND` |
| 38 | GND | `GND` |
| 39 | GND | `GND` |
| 40 | GND | `GND` |
| 41 | GND | `GND` |
| 42 | GND | `GND` |
| 43 | GND | `GND` |
| 44 | GND | `GND` |
| 45 | GND | `GND` |
| 46 | GND | `GND` |
| 47 | GND | `GND` |
| 48 | GND | `GND` |
| 49 | GND | `GND` |
| 50 | GND | `GND` |
| 51 | GND | `GND` |
| 52 | GND | `GND` |
| 53 | GND | `GND` |
## 7. Betriebs- und Randbedingungen (was ein Sprachmodell wissen muss)

### Spannungen und Ströme

| Größe | Wert | Anmerkung |
|---|---|---|
| VBAT (Zelle) | 3,0 – 4,2 V | ungeregelt, direkt an Boost und Wächter |
| +3V3 | 3,3 V (ME6211) | Logik: MCU, Sensor, LED, Wächter |
| **+5V** | **5,10 V** (MT3608, V_out = 0,6 V × (1 + R31/R32)) | **beide** Pumpen; Boost-Schalterstrom-Grenze 2 A |
| Wächter-Schwelle | ≈ 3,08 V (MAX809) | darunter: RESET_UV zieht die Pumptreiber über D3/D8 ab |
| Dosierpumpe `B0DHVMZ27Y` | DC 5 V, Leerlauf 0,4 A, **Anlauf 3 A** | ≤ 150 ml/min, Schlauch 3 × 5 mm |
| Sauerstoffpumpe `B0FXB5BMTT` | 5 V, ~1 W = **0,20 A** | optional, Amazon 8,48 € |

### Steuerung / Firmware-Seite

- **Dosierpumpe:** GPIO **IO2** (`PUMP_EN`) → Q1 (AO3400A) über R1 4,7 kΩ, Pulldown R2 47 kΩ, Freilauf D1, EMI-C11, Stecker **J4**.
- **Sauerstoffpumpe:** GPIO **IO22** (`PUMP2_EN`, U1 Pin 28) → Q3 über **R33** 4,7 kΩ, Pulldown **R34** 47 kΩ, Freilauf **D7**, EMI **C20**, Stecker **J16**. Der frühere Reserve-Stecker **J14 entfällt**.
- ⚠️ **PWM-Softstart ist Pflicht** (nicht optional): Der Boost kann den **3-A-Anlauf** der Dosierpumpe nicht liefern;
  die 22 µF am Ausgang puffern 3 A nur ~7 µs. Ohne Rampe (100–300 ms) bricht +5V ein und der Wächter kann auslösen.
- ⚠️ **Sauerstoffpumpe nicht im Dauerbetrieb:** 1 W an 5 V ziehen aus der 1500-mAh-Zelle ≈ 0,32 A → **~4,7 h**;
  für Intervall-Sauerstoffgabe ausgelegt, nicht für 24/7.
- **Membranpumpe braucht Frischluft** → außerhalb des Topfs montieren, Luftschlauch in die Nährlösung,
  **Rückschlagventil** einbauen (sonst läuft Wasser in die Pumpe, wenn sie steht).

### Anschließen (Aufbau in Kurzform)

| Anschluss | Was kommt dran | Wie |
|---|---|---|
| J1 | 1S-LiPo-Akku (1500 mAh, EFASO) | Steckverbinder PH 2,0 **aufrecht**, Pin 1 = +, Pin 2 = − |
| J2 | kapazitiver Bodenfeuchte-Sensor | JST-XH 3P aufrecht, Pin 1 = +3V3, Pin 2 = Signal, Pin 3 = GND |
| J4 | Dosierpumpe | JST-XH 2P aufrecht; Pumpe mit 5 V/0,4 A, Kabel auf JST-XH crimpen |
| J16 | Sauerstoffpumpe (optional) | JST-XH 2P aufrecht (gleicher Typ wie J4 → ein Crimp-Werkzeug) |
| J5 | USB-C-Kabel | Laden + Programmieren |
| J7–J13, J15 | freie GPIOs / Erweiterung | 2,54-mm-Stiftleisten, Schaltplan-Block **ERWEITERUNG** |
| J6 | Lötpads (unbestückt) | Reserve |

### Bewusste Eigenheiten der Schaltung

- Alle Stecker sind **aufrecht (Top-Entry)** ausgeführt (`B2B…`/`B3B…`-Bauform, erster Buchstabe **B**);
  gewinkelte Bauformen heißen `S2B…`/`S3B…` (erster Buchstabe **S**) und sind hier absichtlich nicht verwendet.
- **D8** klemmt das Gate von Q3 gegen den Wächter-Ausgang (Low = Pumpe aus), baugleich zu D3 auf dem ersten Kanal.
- Der **+5V**-Knoten versorgt **beide** Pumpen; die Dosierpumpe lag früher direkt an VBAT (das ist seit dem
  15.09.2026 geändert, weil die Sauerstoffpumpe zwingend 5 V braucht).
- **EN des Boost (U8 Pin 4)** liegt fest an VBAT → der Boost läuft immer, auch wenn keine Pumpe aktiv ist.

---

**Quellen im Repository:** `hardware/schaltplan_v1.md` (ausführliche Begründungen, §10 = Boost-Auslegung),
`hardware/schaltplan_v1_netzliste.csv` (Handnetzliste, Quelle der Generatorkette),
`hardware/bom_entscheidung.md` (Bauteilentscheidungen, §8 = Sauerstoffpumpe),
`hardware/easyeda/` (Generatorkette, die diesen Plan erzeugt).
