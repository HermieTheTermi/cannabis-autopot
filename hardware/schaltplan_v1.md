# Schaltplan V1 — Smart Grow Topf

Stand: 11.09.2026 · **Diese Datei ist die Verbindungsvorgabe für das Layout.**
Alle Bauteilwerte sind aus den Herstellerdatenblättern abgeleitet (Quelle jeweils in der Spalte
„Warum"). Bauteile, deren Pinbelegung nur als Bild im Datenblatt vorliegt, sind unten als
**„noch gegenprüfen"** markiert — dort steht die Standardbelegung, nicht ein Beleg.

Maschinenlesbare Fassung derselben Verbindungen: **`schaltplan_v1_netzliste.csv`**
(`Netz, Bauteil, Pin`) — gedacht für die Übernahme ins EDA-Tool und als Prüfliste.

---

## 1. Blöcke

```
   USB-C (J5) ──VBUS──┬──────────────────────────────► U3 MCP73831 (1S-Lader, 4,20 V)
                      │                                   │
                      ├── CC1/CC2 ─ 5,1 kΩ ─ GND          ├──VBAT──┬── J1 Akku (1S, PCM)
                      └── D+/D− ─ U6 ESD ─ U1 GPIO13/12    │         ├── Q1 AO3400A ─ J4 Pumpe
                                                           │         ├── U7 MAX809 (3,08 V)
   +3V3 ◄── U4 ME6211 (500 mA) ◄──VBAT────────────────────┤         ├── R3a/R3b Teiler → ADC
             │                                             │         └── C3 100 µF (Pumpenpuffer)
             ├── U1 ESP32-C6-MINI-1 (Pin 3 + VDD33-Pins)
             └── Sensor-VCC (über GPIO3 geschaltet, J2)
```

**Versorgungskette:** USB-C 5 V → Lader → **VBAT** (3,0–4,2 V) → { Pumpe direkt, MAX809, Teiler,
LDO → 3,3 V }. Es gibt **keinen Schaltregler** — bewusst, siehe `bom_entscheidung.md` §3.

---

## 2. Netze (was womit verbunden wird)

| Netz | Verbindungen | Zweck |
|---|---|---|
| **VBUS** | J5 VBUS ↔ U3 Pin 4 (VDD) ↔ C7 4,7 µF ↔ U6 Pin 5 ↔ R_LEDCHG (Lade-LED) | 5-V-Eingang, Ladestrom, LED-Versorgung |
| **PROG** | U3 Pin 5 (PROG) ↔ R_PROG 3,9 kΩ ↔ GND | Ladestrom-Programmierung (256 mA) |
| **VBAT** | U3 Pin 3 (VBAT) ↔ C8 4,7 µF ↔ J1 Pin 1 (Akku +) ↔ C3 100 µF ↔ J4 Pin 1 (Pumpe +) ↔ D1 Kathode ↔ U7 Pin 3 (VCC) ↔ U4 VIN ↔ C5 10 µF ↔ R3a | Energiebus, alles außer Logik |
| **+3V3** | U4 VOUT ↔ C6 1 µF ↔ U1 Pin 3 **und alle VDD33-Pins** ↔ C2 22 µF ↔ C1a/C1b 100 nF ↔ R_EN ↔ R_BOOT ↔ R_GPIO8 | Logikversorgung |
| **GND** | U1 (alle GND-Pins), U3 Pin 2, U4 GND, U6 Pin 2, U7 Pin 1, Q1 Source, C1–C10, R2, R3b, R5a/R5b, R4/D2, SW1/SW2, J1 Pin 2, J2 Pin 3, J4 Pin 2, J5 GND + Schirm | Masse |
| **EN** | U1 **Pin 8** ↔ R_EN 10 kΩ → +3V3 · C4 1 µF → GND · SW1 → GND | Reset; RC **10 kΩ + 1 µF** (Espressif) |
| **BOOT** | U1 **Pin 23 (IO9)** ↔ R_BOOT 10 kΩ → +3V3 · SW2 → GND | Download-Modus; **kein großer C** an GPIO9! |
| **GPIO8_STRAP** | U1 **Pin 22 (IO8)** ↔ R_GPIO8 10 kΩ → +3V3 | Strapping-Pin nicht floaten lassen |
| **PUMP_EN** | U1 **Pin 5 (IO2)** → R1 **4,7 kΩ** → **Gate-Knoten** von Q1 | Pumpensteuerung (PWM-fähig) |
| **GATE** | Q1 Gate ↔ R1 4,7 kΩ ↔ R2 **47 kΩ** → GND ↔ D3 **Anode** | Abschaltung bei MCU-Tod (Pull-down) bzw. Unterspannung (D3 → MAX809) |
| **PUMP_N** | Q1 Drain ↔ J4 Pin 2 (Pumpe −) ↔ D1 **Anode** | geschaltete Pumpenmasse (Low-Side) |
| **RESET_UV** | U7 Pin 2 (RESET) ↔ D3 **Kathode** | zieht bei VBAT < 3,08 V den Gate-Knoten auf ~0,3 V |
| **SENSOR_RAW → SENSOR_AOUT** | J2 Pin 2 → R6 1 kΩ → U1 **Pin 12 (IO0, ADC1_CH0)** ↔ C9 100 nF → GND | Bodenfeuchte. Zwei getrennte Netze: R6 liegt **in Reihe**, nicht parallel |
| **SENSOR_PWR** | U1 **Pin 6 (IO3)** → J2 Pin 1 (Sensor-VCC) | Sensor nur während der Messung versorgen |
| **VBAT_SENSE** | R3a 200 kΩ (von VBAT) ↔ Knoten ↔ R3b 200 kΩ → GND · Knoten ↔ U1 **Pin 13 (IO1, ADC1_CH1)** ↔ C10 100 nF → GND | Zellspannung für Pumpstopp/Warnung (§4b BOM) |
| **USB_DM** | J5 D− ↔ U6 Pin 3 → U6 Pin 4 ↔ [R 22 Ω optional] ↔ U1 **Pin 17 (IO12)** | USB-Daten, nativ |
| **USB_DP** | J5 D+ ↔ U6 Pin 1 → U6 Pin 6 ↔ [R 22 Ω optional] ↔ U1 **Pin 18 (IO13)** | USB-Daten, nativ |
| **LED_STAT** | U1 **Pin 19 (IO14)** → R4 1 kΩ → D2 → GND | Status; **nicht IO4/IO5** (MTMS/MTDI = Strapping) |
| **LED_CHG / STAT_CHG** | VBUS → R_LEDCHG 1 kΩ → D_LEDCHG **Anode** · D_LEDCHG **Kathode** → U3 Pin 1 (STAT) | Ladestatus (STAT ist Tri-State, senkt Strom). **Achtung:** die LED-Kathode gehört an STAT, **nicht** an GND — sonst leuchtet sie dauerhaft |
| **UART_DBG** (optional, DNP) | U1 **Pin 31 (TXD0)** → R_UART 499 Ω → Testpad · U1 **Pin 30 (RXD0)** → Testpad | Notfall-Debug, Espressif empfiehlt den 499-Ω-Widerstand |

---

## 3. Bauteile mit Werten und Begründung

### ICs und Halbleiter

| Pos | Bauteil | Wert | LCSC | Warum / Quelle |
|---|---|---|---|---|
| U1 | ESP32-C6-MINI-1 | Modul | `C5736265` | MCU, Antenne/Flash im Modul |
| U3 | MCP73831T-2ACI/OT | 4,20 V, SOT-23-5 | `C424093` | 1S-Lader; **-2** = 4,20 V Ladeschluss (Datenblatt: Optionen 4,20/4,35/4,40/4,50 V) |
| U4 | ME6211C33M5G | 500 mA, 3,3 V | `C82942` | TX-Peak des C6 = **382 mA**; Espressif fordert ≥ 500 mA |
| U6 | USBLC6-2SC6 | ESD, SOT-23-6 | `C7519` | Datenleitungen schützen (USB-Vorgabe, nicht von Espressif) |
| U7 | MAX809TEUR+T | 3,08 V, SOT-23 | `C16711` | Unterspannungsschutz; Espressif empfiehlt für Akkubetrieb einen Power-Monitor ~3,0 V |
| Q1 | AO3400A | N-MOSFET SOT-23 | `C20917` | Pumpentreiber; RDS(on) < 48 mΩ @ VGS 2,5 V |
| D1 | 1N5819WS | 40 V / 1 A | `C191023` | Freilaufdiode der Pumpe (Kathode an VBAT) |
| D3 | 1N5819WS | 40 V / 1 A | `C191023` | Klemmzweig: Anode am Gate, Kathode an U7-RESET |
| D2 | LED rot | 0805 | `C84256` | Status-LED |
| D_LEDCHG | LED rot, **gleicher Typ wie D2** | 0805 | `C84256` | Ladestatus. **Grund für rot:** bei JLC ist **keine** grüne 0805-LED mit Bestand verfügbar (geprüft) → derselbe Basic-Typ spart eine Extended-Position. Alternative: STAT (U3 Pin 1) auf einen freien GPIO legen und den Ladestatus per Telegram melden |
| ~~D4~~ | **entfernt** | – | – | **Gefunden in Review 3:** eine bestückte Schottky-Brücke VBUS → VBAT würde die Zelle **ungeregelt über 5 V laden** (nur Diodenabfall) → Überladung/Schaden. Option ersatzlos gestrichen; für Reprogrammierung ohne Akku ein Labornetzteil auf VBAT oder die Zelle stecken |

### Kondensatoren

| Pos | Wert | Typ | Wofür | Quelle |
|---|---|---|---|---|
| C1a, C1b | 2 × 100 nF | 0805 | Decoupling am Modul | Sollwerte der Modul-Typenschaltung (22 µF + 2 × 0,1 µF) |
| C10 | 100 nF | 0805 | ADC-Filter VBAT | Espressif-ADC-Empfehlung; macht zusätzlich die hohe Teiler-Impedanz für den ADC niederohmig |
| C2 | 22 µF | 0805 | Bulk am Modul-3V3 | dito |
| C3 | 100 µF | Elko 16 V | Puffer für den Pumpenstrom | eigene Auslegung (Motoranlauf) |
| C4 | 1 µF | 0603 | EN-RC-Glied | Espressif: „R = 10 kΩ and C = 1 µF" |
| C5 | **10 µF** | 0805 | LDO-Eingang (CIN) | **Erhöht:** ME6211 verlangt min. 1 µF, Espressif dazu ≥ 10 µF am Leistungseingang → Reserve für die 382-mA-TX-Spitzen bei fast leerer Zelle |
| C6 | 1 µF | 0603 | LDO-Ausgang (COUT) | ME6211-Datenblatt: CL = 1 µF Low-ESR |
| C7 | 4,7 µF | 0805 | Lader-Eingang | MCP73831-Datenblatt: „Bypass to VSS with a **minimum of 4,7 µF**" |
| C8 | 4,7 µF | 0805 | Lader-Ausgang/Akku | MCP73831: „4,7 µF … at the output is usually sufficient for up to 500 mA" |
| C9 | 100 nF | 0805 | ADC-Filter Sensor | Espressif: „add a 0,1 µF filter capacitor between ESP pins and ground when using the ADC" |
| C11 | 100 nF | 0805 | **direkt an den Pumpenklemmen** | **neu (Review 3):** Bürstenstörungen des DC-Motors abfangen, damit sie nicht über VBAT in ADC/LDO einstreuen |
| C12 | 100 nF | 0805 | Decoupling am Unterspannungswächter | Standardpraxis; der MAX809 selbst braucht laut Datenblatt keine externen Bauteile |

### Widerstände

| Pos | Wert | Wofür | Quelle |
|---|---|---|---|
| R1 | **4,7 kΩ** | Gate-Serie | **Korrigiert:** der MAX809-T-Ausgang ist für **ISINK = 1,2 mA** spezifiziert (Datenblatt, VOL ≤ 0,3 V). 1 kΩ hätte 3 mA gezogen — über Spec. 4,7 kΩ → **0,57 mA** |
| R2 | **47 kΩ** | Gate-Pulldown | Größer gewählt, weil R1/R2 sonst einen Spannungsteiler bilden: 3,3 V × 47/51,7 = **3,0 V** Gate-Ansteuerung (über dem 2,5-V-Spec-Punkt des AO3400A). MCU unbestückt → Gate entlädt in ~30 µs |
| R_EN | 10 kΩ | EN-Pull-up | Espressif: RC-Glied 10 kΩ + 1 µF, EN nie floaten |
| R_BOOT | 10 kΩ | Pull-up an GPIO9 | Espressif: „It is recommended to place a pull-up resistor at the GPIO9 pin" |
| R_GPIO8 | 10 kΩ | Pull-up an GPIO8 | **eigene Auslegung** (Strapping-Pin nicht floaten) |
| R_PROG | **3,9 kΩ** | Ladestrom | MCP73831: RPROG = 2 kΩ → 500 mA, 10 kΩ → 100 mA ⇒ 3,9 kΩ ≈ **256 mA** (≈0,17 C der 1500-mAh-Zelle). 3,9 kΩ gewählt, weil es ein **Basic**-Teil ist (4,02 kΩ wäre Extended +3 $) |
| R_LEDCHG | **1 kΩ** | Lade-LED | **vereinfacht:** statt der 470 Ω aus dem Datenblatt-Applikationsbild derselbe 1-kΩ-Basic-Typ wie R4 → 3 mA LED-Strom reichen, eine Position weniger |
| R4 | 1 kΩ | Status-LED | eigene Auslegung |
| R3a, R3b | 2 × 200 kΩ | VBAT-Teiler 1:2 | Prinzip aus der Seeed-Doku (200 k in 1:2); ADC sieht max. 2,1 V |
| R5a, R5b | 2 × 5,1 kΩ | USB-C CC1/CC2 → GND | USB-C-Vorgabe (nicht von Espressif dokumentiert) |
| R6 | 1 kΩ | Sensor-AOUT in Reihe | **neu im Review:** schützt den ADC, wenn der Sensor unbversorgt ist |
| R_UART | 499 Ω (DNP) | TXD0-Serie | Espressif: „connect a 499 Ω series resistor to the U0TXD line" |

### Steckverbinder und Schalter

| Pos | Bauteil | LCSC | Anschluss |
|---|---|---|---|
| J1 | JST PH 2,0 mm, 2-pol | `C54582899` | Akku (Pin 1 = +, Pin 2 = −) — **Polung im Layout prüfen** |
| J2 | JST-XH 2,54 mm, 3-pol | `C157928` | Sensor: 1 = VCC, 2 = AOUT, 3 = GND |
| J4 | JST-XH 2,54 mm, 2-pol | `C157931` | Pumpe: 1 = VBAT, 2 = geschaltete Masse |
| J5 | USB-C 16-pol | `C165948` | VBUS, GND/Schirm, CC1/CC2, D+/D− |
| SW1 | Taster 5,1 × 5,1 mm | `C318884` | Reset (EN gegen GND) |
| SW2 | Taster 5,1 × 5,1 mm | `C318884` | Boot (GPIO9 gegen GND) |

---

## 4. Modul-Pinbelegung (verifiziert aus der Espressif-Datasheet v1.5)

Herausgeführt sind 22 GPIOs. Verwendet werden:

| Modulpin | Name | Verwendung hier |
|---|---|---|
| 3 | 3V3 | +3V3 (zusammen mit allen VDD33-Pins) |
| 5 | IO2 | **PUMP_EN** |
| 6 | IO3 | **SENSOR_PWR** (ADC1_CH3) |
| 8 | EN | Reset-RC + SW1 |
| 19 | IO14 | **LED_STAT** — *korrigiert:* nicht IO4, denn IO4 ist **MTMS** (Strapping-/JTAG-Pin) |
| 12 | IO0 | **SENSOR_AOUT** (ADC1_CH0) |
| 13 | IO1 | **VBAT_SENSE** (ADC1_CH1) |
| 17 | IO12 | **USB_D−** |
| 18 | IO13 | **USB_D+** |
| 22 | IO8 | Strapping-Pin, nur Pull-up |
| 23 | IO9 | **BOOT** (Strapping) + Pull-up |
| 30 / 31 | RXD0 / TXD0 | optional UART-Debug (DNP) |
| 1, 2, 11, 14, 36–53 | GND | Masse |
| 49 | EPAD | Thermo-Pad — mit GND verbinden (Espressif: nicht Pflicht, verbessert die Wärmeabfuhr) |
| div. | VDD33 | **alle** an +3V3, jeweils 100 nF in der Nähe |

**Nicht benutzt:** IO5, IO6, IO7, IO14, IO15, IO18–IO23. Espressif: unbenutzte hochohmige Pins
mit Pull-up/down versehen oder internen Pull aktivieren (verhindert Mehrverbrauch im Schlaf).

**GPIO9-Regel beachten:** kein großer Kondensator am Pin, sonst startet der Chip in den
Download-Modus statt in die Anwendung.

---

## 5. Pinbelegungen der ICs — Stand der Belege

| Bauteil | Pinbelegung | Belegstatus |
|---|---|---|
| **USBLC6-2SC6** | 1 = I/O1 · 2 = GND · 3 = I/O2 · 4 = I/O2 · 5 = VBUS · 6 = I/O1 | ✅ aus dem Datenblatttext verifiziert (1/6 und 3/4 sind die Durchschleifpaare) |
| **MCP73831 (SOT-23-5)** | 1 = STAT · 2 = VSS · 3 = VBAT · 4 = VDD · 5 = PROG | ⚠️ aus dem „Package Types"-Text des Datenblatts abgeleitet; **Pin-Configuration-Bild nicht textlich prüfbar → beim Footprint gegenprüfen** |
| **ME6211 (SOT-23-5)** | 1 = VIN · 2 = GND · 3 = EN · 4 = NC · 5 = VOUT | ⚠️ **noch gegenprüfen** (Datenblatt zeigt nur Bild). **EN an VIN/VBAT** legen — auf +3V3 gelegt könnte der Regler nicht starten |
| **MAX809 (SOT-23)** | 1 = GND · 2 = RESET · 3 = VCC | ⚠️ **noch gegenprüfen** (Bild) |
| **AO3400A (SOT-23)** | 1 = Gate · 2 = Source · 3 = Drain | ⚠️ **noch gegenprüfen** (Bild) |

---

## 6. Auslegungsnotizen und offene Punkte

0. **Prüfwerkzeug:** `../../scripts/check_netlist.py` prüft die Netzliste auf Strukturfehler
   (Bauteil nur auf einem Netz, Netz mit nur einem Knoten, Pin auf zwei Netzen, im Schaltplan
   dokumentierte Bauteile, die in der Netzliste fehlen). Läuft mit `python3 scripts/check_netlist.py`
   und muss **exit 0** liefern, bevor das Layout beginnt.

1. **Ladestrom:** 256 mA (R_PROG 3,9 kΩ). Zusammen mit der Logik (max. ~80 mA) bleibt man unter den 500 mA, die
   USB 2.0 liefert. Wenn der Sensor aktiv ist und WLAN sendet, kurzzeitig mehr — für die USB-Spec
   unkritisch, USB-C-Netzteile liefern ohnehin ≥ 1 A.
2. **Betrieb ohne Akku:** VBUS → Lader → VBAT steigt auf ~4,2 V, die Logik läuft also auch ohne
   Zelle. Das ist **nicht belastbar** (Pumpe zieht 450 mA, der Lader liefert max. 500 mA nur in
   CC-Phase). Für Reprogrammierung daher die Zelle stecken oder ein Labornetzteil auf VBAT legen.
   **Bewusst keine Brücke von VBUS auf VBAT** (siehe Review 3: ungeregelter Ladepfad).
3. **Standby-Budget:** Modul-Deep-Sleep 7 µA + LDO 40 µA + MAX809 12 µA + Spannungsteiler 10,5 µA
   ≈ **70 µA** → ~1,7 mAh/Tag. Der Teiler dominiert mit 10,5 µA; wenn das stört, Teiler über einen
   GPIO schaltbar machen oder auf 2 × 1 MΩ erhöhen (dann ist C10 zwingend).
4. **Kein Verpolschutz im Hauptpfad** — die Zelle hat ein PCM, und ein Schottky in Reihe würde 0,3 V
   kosten. Die früher angedachte SS34 (D4) ist in Review 3 **komplett entfallen** (siehe Bauteiltabelle).
   Verpolsicherung ist damit allein die mechanische Kodierung der JST-Stecker.
5. **Testpunkte im Layout vorsehen:** VBAT, +3V3, GND, SENSOR_AOUT, VBAT_SENSE, EN, PUMP_EN.
6. **Layout-Vorgaben aus Espressif:** EN-Leitung kurz halten; USB als 90-Ω-Differentialpaar mit
   GND-Referenzlage; Antenne → siehe `bom_entscheidung.md` §6 (bauteilfreier Bereich, dünnere
   Wulstwand, 15 mm Freistellung im Gehäuse).
7. **Vor dem Bestücken zu klären:** die vier mit ⚠️ markierten Pinbelegungen, die Polarität von J1,
   und die Farbwahl der Lade-LED.
