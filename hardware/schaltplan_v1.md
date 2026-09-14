# Schaltplan V1 — Smart Grow Topf

Stand: 14.09.2026 · **Diese Datei ist die Verbindungsvorgabe für das Layout.**
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
             ├── Sensor-VCC (über GPIO3 geschaltet, J2/J7)
             └── VCC_EXT (über Q2/IO20 geschaltet, J8 I²C + J9–J15 Reserve)
```

**Logik-Ein-/Ausgänge:** IO0 Feuchte-ADC · IO1 Zellspannung · IO2 Pumpe · IO3 Sensor-Versorgung ·
**IO4 Lichtsensor-ADC (ADC1_CH4)** · **IO5 Reserve-ADC (ADC1_CH5, J9)** ·
**IO6 externer Taster (LP_GPIO6, weckt aus dem Deep-Sleep)** · **IO7 Tank-LED (rot, LP_GPIO7)** ·
IO14 Status-LED · IO9 Boot · IO12/13 USB ·
**IO15–IO17, IO21–IO23 Reserve (J10–J15, je über 1 kΩ in Reihe)** ·
**IO18/IO19 I²C (J8, je über 1 kΩ in Reihe)** · **IO20 Load-Switch VCC_EXT (intern)**.

**Versorgungskette:** USB-C 5 V → Lader → **VBAT** (3,0–4,2 V) → { Pumpe direkt, MAX809, Teiler,
LDO → 3,3 V }. Es gibt **keinen Schaltregler** — bewusst, siehe `bom_entscheidung.md` §3.

---

## 2. Netze (was womit verbunden wird)

| Netz | Verbindungen | Zweck |
|---|---|---|
| **VBUS** | J5 VBUS ↔ U3 Pin 4 (VDD) ↔ C7 4,7 µF ↔ U6 Pin 5 ↔ R_LEDCHG (Lade-LED) | 5-V-Eingang, Ladestrom, LED-Versorgung |
| **PROG** | U3 Pin 5 (PROG) ↔ R_PROG 3,9 kΩ ↔ GND | Ladestrom-Programmierung (256 mA) |
| **VBAT** | U3 Pin 3 (VBAT) ↔ C8 4,7 µF ↔ J1 Pin 1 (Akku +) ↔ C3 100 µF ↔ J4 Pin 1 (Pumpe +) ↔ D1 Kathode ↔ U7 Pin 3 (VCC) ↔ U4 VIN ↔ C5 10 µF ↔ R3a | Energiebus, alles außer Logik |
| **+3V3** | U4 VOUT ↔ C6 1 µF ↔ U1 Pin 3 **und alle VDD33-Pins** ↔ C2 22 µF ↔ C1a/C1b 100 nF ↔ R_EN ↔ R_BOOT ↔ R_GPIO8 ↔ **R_BTN** | Logikversorgung |
| **GND** | U1 (alle GND-Pins), U3 Pin 2, U4 GND, U6 Pin 2, U7 Pin 1, Q1 Source, C1–C12, C_BTN, **C_SPARE**, R2, R3b, R5a/R5b, R4/D2, **R_TANK/D5**, SW1/SW2, J1 Pin 2, **J2 Pin 1**, **J7 Pin 1**, J4 Pin 2, **J6 Pin 2**, **J8 Pin 1**, **J9–J15 Pin 1**, J5 GND + Schirm | Masse |
| **EN** | U1 **Pin 8** ↔ R_EN 10 kΩ → +3V3 · C4 1 µF → GND · SW1 → GND | Reset; RC **10 kΩ + 1 µF** (Espressif) |
| **BOOT** | U1 **Pin 23 (IO9)** ↔ R_BOOT 10 kΩ → +3V3 · SW2 → GND | Download-Modus; **kein großer C** an GPIO9! |
| **GPIO8_STRAP** | U1 **Pin 22 (IO8)** ↔ R_GPIO8 10 kΩ → +3V3 | Strapping-Pin nicht floaten lassen |
| **PUMP_EN** | U1 **Pin 5 (IO2)** → R1 **4,7 kΩ** → **Gate-Knoten** von Q1 | Pumpensteuerung (PWM-fähig) |
| **GATE** | Q1 Gate ↔ R1 4,7 kΩ ↔ R2 **47 kΩ** → GND ↔ D3 **Anode** | Abschaltung bei MCU-Tod (Pull-down) bzw. Unterspannung (D3 → MAX809) |
| **PUMP_N** | Q1 Drain ↔ J4 Pin 2 (Pumpe −) ↔ D1 **Anode** | geschaltete Pumpenmasse (Low-Side) |
| **RESET_UV** | U7 Pin 2 (RESET) ↔ D3 **Kathode** | zieht bei VBAT < 3,08 V den Gate-Knoten auf ~0,3 V |
| **SENSOR_RAW → SENSOR_AOUT** | J2 Pin 3 (SIG) → R6 1 kΩ → U1 **Pin 12 (IO0, ADC1_CH0)** ↔ C9 100 nF → GND | Bodenfeuchte. Zwei getrennte Netze: R6 liegt **in Reihe**, nicht parallel |
| **SENSOR_PWR** | U1 **Pin 6 (IO3)** → J2 Pin 2 (Feuchte-VCC) ↔ J7 Pin 2 (Licht-VCC) | **beide** externen Sensoren nur während der Messung versorgen |
| **LIGHT_RAW** | J7 Pin 3 (Sensorausgang) ↔ R_LIGHT 10 kΩ → GND ↔ R_LIGHT_S 1 kΩ | Lichtsensor-Rohsignal; **offener Stecker ⇒ R_LIGHT zieht auf 0 V ⇒ „dunkel"** (Bewässerung bleibt erlaubt) |
| **LIGHT_AOUT** | R_LIGHT_S 1 kΩ (in Reihe) ↔ U1 **Pin 9 (IO4, ADC1_CH4)** ↔ C_LIGHT 100 nF → GND | gefilterter ADC-Eingang, gegen den Sensorausgang hochohmig getrennt |
| **SDA / SDA_MCU** | J8 Pin 3 ↔ R_SDA_S 1 kΩ (in Reihe) ↔ U1 **Pin 24 (IO18)** · R_SDA_PU 10 kΩ → **VCC_EXT** | I²C-Daten; Pull-up am geschalteten Rail, Serien-R schützt den Pin |
| **SCL / SCL_MCU** | J8 Pin 4 ↔ R_SCL_S 1 kΩ (in Reihe) ↔ U1 **Pin 25 (IO19)** · R_SCL_PU 10 kΩ → **VCC_EXT** | I²C-Takt; wie SDA |
| **VCC_EXT** | Q2 **Drain** ↔ J8 Pin 2 ↔ J9–J15 Pin 2 ↔ R_SDA_PU/R_SCL_PU | geschaltete Erweiterungsversorgung (Load-Switch, beim Reset aus) |
| **EXT_EN** | U1 **Pin 26 (IO20)** ↔ Q2 **Gate** ↔ R_GATE 47 kΩ → **+3V3** | IO20 zieht das Gate nach unten ⇒ VCC_EXT an; ohne Treiber hält der Pull-up VCC_EXT aus |
| **SPARE_AIN_RAW → SPARE_AIN** | J9 Pin 3 → R_SPARE_AIN 1 kΩ → U1 **Pin 10 (IO5, ADC1_CH5)** ↔ C_SPARE 100 nF → GND | Reserve-Analog, RC-gefiltert (gleiches Muster wie SENSOR_AOUT) |
| **SPARE_IO15_RAW → SPARE_IO15** | J10 Pin 3 → R_SPARE_IO15 1 kΩ → U1 **Pin 20 (IO15)** | Reserve-IO15 (Strapping JTAG-Quelle, Default-eFuses inert) |
| **SPARE_IO16** | J11 Pin 3 → R_SPARE_IO16 1 kΩ → U1 **Pin 31 (TXD0/IO16)** | Reserve-IO16, nur über Serien-R erreichbar |
| **SPARE_IO17** | J12 Pin 3 → R_SPARE_IO17 1 kΩ → U1 **Pin 30 (RXD0/IO17)** | Reserve-IO17, nur über Serien-R erreichbar |
| **SPARE_IO21_RAW → SPARE_IO21** | J13 Pin 3 → R_SPARE_IO21 1 kΩ → U1 **Pin 27 (IO21)** | Reserve-IO21 (WPU beim Reset) |
| **SPARE_IO22_RAW → SPARE_IO22** | J14 Pin 3 → R_SPARE_IO22 1 kΩ → U1 **Pin 28 (IO22)** | Reserve-IO22 |
| **SPARE_IO23_RAW → SPARE_IO23** | J15 Pin 3 → R_SPARE_IO23 1 kΩ → U1 **Pin 29 (IO23)** | Reserve-IO23 |
| **VBAT_SENSE** | R3a 200 kΩ (von VBAT) ↔ Knoten ↔ R3b 200 kΩ → GND · Knoten ↔ U1 **Pin 13 (IO1, ADC1_CH1)** ↔ C10 100 nF → GND | Zellspannung für Pumpstopp/Warnung (§4b BOM) |
| **USB_DM** | J5 D− ↔ U6 Pin 3 → U6 Pin 4 ↔ [R 22 Ω optional] ↔ U1 **Pin 17 (IO12)** | USB-Daten, nativ |
| **USB_DP** | J5 D+ ↔ U6 Pin 1 → U6 Pin 6 ↔ [R 22 Ω optional] ↔ U1 **Pin 18 (IO13)** | USB-Daten, nativ |
| **LED_STAT** | U1 **Pin 19 (IO14)** → R4 **220 Ω** → D2 **grün** → GND | Status/Betrieb; **nicht IO4/IO5** (nur SDIO-Strap, **nicht** boot-kritisch — siehe §4) |
| **LED_CHG / STAT_CHG** | VBUS → R_LEDCHG 1 kΩ → D_LEDCHG **Anode** · D_LEDCHG **Kathode** → U3 Pin 1 (STAT) | Ladestatus (STAT ist Tri-State, senkt Strom). **Achtung:** die LED-Kathode gehört an STAT, **nicht** an GND — sonst leuchtet sie dauerhaft |
| **BTN** | U1 **Pin 15 (IO6)** ↔ R_BTN 10 kΩ → +3V3 · C_BTN 100 nF → GND · J6 Pin 1 | **Nachfüll-Bestätigung.** Externer Taster schließt auf GND; IO6 ist **LP_GPIO6** → weckt aus dem Deep-Sleep (EXT1, ANY_LOW) |
| **LED_TANK** | U1 **Pin 16 (IO7)** → R_TANK 1 kΩ → D5 **Anode** · D5 **Kathode** → GND | **Tank-leer-Anzeige (rot).** IO7 ist LP_GPIO7; D2 bleibt die Status-LED |
| **UART_DBG** (optional, DNP) | U1 **Pin 31 (TXD0)** → R_UART 499 Ω → Testpad · U1 **Pin 30 (RXD0)** → Testpad | Notfall-Debug, Espressif empfiehlt den 499-Ω-Widerstand. **TXD0/RXD0 liegen zugleich über R_SPARE_IO16/17 an J11/J12** |

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
| **Q2** | **AO3401A** | **P-MOSFET SOT-23** | `C15127` | **neu (14.09.2026):** High-Side-Load-Switch für die geschaltete Erweiterungsversorgung **VCC_EXT**. RDS(on) 85 mΩ @ VGS −2,5 V; Source → +3V3, Drain → VCC_EXT, Gate über 47 kΩ auf +3V3 (aus = Fail-safe), IO20 zieht nach unten |
| D1 | 1N5819WS | 40 V / 1 A | `C191023` | Freilaufdiode der Pumpe (Kathode an VBAT) |
| D3 | 1N5819WS | 40 V / 1 A | `C191023` | Klemmzweig: Anode am Gate, Kathode an U7-RESET |
| D2 | **LED grün** (525 nm) | 0805 | `C2297` | **Farbe geändert 11.09.2026** (vorher rot wie D5). Grün = Status/Betrieb, **rot bleibt der Warnung „Tank leer" vorbehalten**. Vf **2,85 V** (InGaN) → am 3,3-V-Rail nur **0,45 V Reserve**, deshalb R4 = 220 Ω. JLC: **basic**, 1.627.076 auf Lager. *Blau* wäre möglich, ist bei JLC aber nur **extended** (+3 $) und hätte dasselbe Vf-Problem |
| D5 | LED rot, **gleicher Typ wie D2** | 0805 | `C84256` | **neu:** Anzeige „Tank leer". Kein neues JLC-Bauteil nötig — identischer 0805-Typ, **6.141.918 auf Lager** (basic) |
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
| **C_LIGHT** | 100 nF | 0805 | ADC-Filter **Lichtsensor** | Espressif-ADC-Empfehlung; bildet mit R_LIGHT_S (1 kΩ) einen Tiefpass (τ = 0,1 ms) |
| C11 | 100 nF | 0805 | **direkt an den Pumpenklemmen** | **neu (Review 3):** Bürstenstörungen des DC-Motors abfangen, damit sie nicht über VBAT in ADC/LDO einstreuen |
| C_BTN | 100 nF | 0805 | **Entprellung des externen Tasters** | RC mit R_BTN: 10 kΩ × 100 nF = **1 ms** — entprellt und hält Einstreuungen auf der Tasterleitung fern |
| C12 | 100 nF | 0805 | Decoupling am Unterspannungswächter | Standardpraxis; der MAX809 selbst braucht laut Datenblatt keine externen Bauteile |
| **C_SPARE** | 100 nF | 0805 | **ADC-Filter Reserve-Analog (IO5, J9)** | Espressif-ADC-Empfehlung; bildet mit R_SPARE_AIN (1 kΩ) einen Tiefpass (τ = 0,1 ms), gleiches Muster wie SENSOR_AOUT |

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
| R4 | **220 Ω** | Status-LED (grün) | **Rechenweg:** 3,3 V − 2,85 V = 0,45 V → mit 220 Ω fließen **1,4–2,7 mA** über die Vf-Streuung (2,7–3,0 V) und bis 3,2 mA im Worst Case — weit unter den 25 mA der LED. Mit 1 kΩ wären es nur 0,3–0,6 mA (zu dunkel und stark Vf-abhängig) |
| **R_BTN** | 10 kΩ | Pull-up für den externen Taster | Hält IO6 auf High; Tastendruck zieht auf GND (weckt per EXT1 ANY_LOW). Ruhestrom **0 µA**, gedrückt 330 µA |
| **R_TANK** | 1 kΩ | Vorwiderstand Tank-LED | 1,3 mA bei Vf ≈ 2,0 V. **Option zum Stromsparen:** 2,2 kΩ → 0,6 mA |
| R3a, R3b | 2 × 200 kΩ | VBAT-Teiler 1:2 | Prinzip aus der Seeed-Doku (200 k in 1:2); ADC sieht max. 2,1 V |
| R5a, R5b | 2 × 5,1 kΩ | USB-C CC1/CC2 → GND | USB-C-Vorgabe (nicht von Espressif dokumentiert) |
| R6 | 1 kΩ | Sensor-AOUT in Reihe | **neu im Review:** schützt den ADC, wenn der Sensor unbversorgt ist |
| **R_LIGHT** | 10 kΩ | Lastwiderstand / definierter Zustand des Lichtsensors | offener Stecker ⇒ 0 V ⇒ Firmware liest „dunkel" (Bewässerung erlaubt, Pflanze vertrocknet nicht); begrenzt zugleich den Fotostrom des ALS-PT19 |
| **R_LIGHT_S** | 1 kΩ | Licht-AOUT in Reihe | Serienschutz für den ADC (gleiche Rolle wie R6) |
| R_UART | 499 Ω (DNP) | TXD0-Serie | Espressif: „connect a 499 Ω series resistor to the U0TXD line" |
| **R_GATE** | 47 kΩ | Gate-Pull-up Load-Switch | Hält das Gate von Q2 ohne aktiven GPIO auf **+3V3** (Quellpotential) ⇒ VGS = 0 ⇒ Q2 sperrt ⇒ **VCC_EXT ist beim Reset aus** (Fail-safe) |
| **R_SDA_PU** | 10 kΩ | I²C-SDA-Pull-up | Pull-up an **VCC_EXT**, nicht an +3V3 — im ausgeschalteten Zustand zieht der Bus keinen Strom |
| **R_SCL_PU** | 10 kΩ | I²C-SCL-Pull-up | dito, an **VCC_EXT** |
| **R_SDA_S** | 1 kΩ | I²C-SDA in Reihe | Serienschutz zwischen J8 Pin 3 und U1 Pin 24 (IO18) |
| **R_SCL_S** | 1 kΩ | I²C-SCL in Reihe | Serienschutz zwischen J8 Pin 4 und U1 Pin 25 (IO19) |
| **R_SPARE_AIN** | 1 kΩ | Reserve-Analog in Reihe | Serienschutz zwischen J9 Pin 3 und U1 Pin 10 (IO5, ADC1_CH5); Teil des ADC-Filters mit C_SPARE |
| **R_SPARE_IO15** | 1 kΩ | Reserve-IO15 in Reihe | zwischen J10 Pin 3 und U1 Pin 20 (IO15) |
| **R_SPARE_IO16** | 1 kΩ | Reserve-IO16 in Reihe | zwischen J11 Pin 3 und U1 Pin 31 (TXD0/IO16) |
| **R_SPARE_IO17** | 1 kΩ | Reserve-IO17 in Reihe | zwischen J12 Pin 3 und U1 Pin 30 (RXD0/IO17) |
| **R_SPARE_IO21** | 1 kΩ | Reserve-IO21 in Reihe | zwischen J13 Pin 3 und U1 Pin 27 (IO21) |
| **R_SPARE_IO22** | 1 kΩ | Reserve-IO22 in Reihe | zwischen J14 Pin 3 und U1 Pin 28 (IO22) |
| **R_SPARE_IO23** | 1 kΩ | Reserve-IO23 in Reihe | zwischen J15 Pin 3 und U1 Pin 29 (IO23) |

### Steckverbinder und Schalter

| Pos | Bauteil | LCSC | Anschluss |
|---|---|---|---|
| J1 | JST PH 2,0 mm, 2-pol | `C54582899` | Akku (Pin 1 = +, Pin 2 = −) — **Polung im Layout prüfen** |
| J2 | JST-XH 2,54 mm, 3-pol | `C157928` | Feuchtesensor: **1 = GND · 2 = SENSOR_PWR (VCC) · 3 = SENSOR_RAW (AOUT)** |
| J4 | JST-XH 2,54 mm, 2-pol | `C157931` | Pumpe: 1 = VBAT, 2 = geschaltete Masse |
| J5 | USB-C 16-pol | `C165948` | VBUS, GND/Schirm, CC1/CC2, D+/D− |
| SW1 | Taster 5,1 × 5,1 mm | `C318884` | Reset (EN gegen GND) |
| SW2 | Taster 5,1 × 5,1 mm | `C318884` | Boot (GPIO9 gegen GND) |
| **J6** | **2 Lötpads / Bohrungen Ø 1,0 mm, Raster 2,54 mm** | – | **kein Stecker, keine BOM-Position, keine JLC-Kosten** — der Taster sitzt außerhalb der Platine (Gehäuse) und wird mit zwei Kabeln direkt angelötet |
| **J7** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **externer Lichtsensor:** **1 = GND · 2 = SENSOR_PWR (VCC) · 3 = LIGHT_RAW (AOUT)** — **Typwechsel 14.09.2026:** der Nutzer steckt Dupont-Buchsen direkt auf (keine Crimpzange). Gleicher Stiftleistentyp wie J9–J15 |
| **J8** | **Stiftleiste 1×4, 2,54 mm, male gerade** | `C2691448` | **I²C-Erweiterung (VCC_EXT):** **1 = GND · 2 = VCC_EXT · 3 = SDA · 4 = SCL** (VCC innen, wie Qwiic/STEMMA) |
| **J9** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve-Analog:** **1 = GND · 2 = VCC_EXT · 3 = SPARE_AIN_RAW (IO5, ADC1_CH5)** |
| **J10** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve IO15:** **1 = GND · 2 = VCC_EXT · 3 = SPARE_IO15_RAW** (Strapping JTAG-Quelle, Default-eFuses inert) |
| **J11** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve IO16 (TXD0):** **1 = GND · 2 = VCC_EXT · 3 = SPARE_IO16** |
| **J12** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve IO17 (RXD0):** **1 = GND · 2 = VCC_EXT · 3 = SPARE_IO17** |
| **J13** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve IO21:** **1 = GND · 2 = VCC_EXT · 3 = SPARE_IO21_RAW** (WPU beim Reset) |
| **J14** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve IO22:** **1 = GND · 2 = VCC_EXT · 3 = SPARE_IO22_RAW** |
| **J15** | **Stiftleiste 1×3, 2,54 mm, male gerade** | `C2937625` | **Reserve IO23:** **1 = GND · 2 = VCC_EXT · 3 = SPARE_IO23_RAW** |

**Stecker-Typen (ab 14.09.2026):** J2 bleibt **JST-XH 3P** (`C157928`, gerastet). J7 und J9–J15 sind
**2,54-mm-Stiftleisten male gerade** (`C2937625`), J8 ist die 4-polige Variante (`C2691448`).
Kabel mit Dupont-Buchse werden direkt aufgesteckt. Die **Pinordnung ist überall GND–VCC–SIG**
(VCC in der Mitte), J8 als GND–VCC–SDA–SCL.

---

## 4. Modul-Pinbelegung (verifiziert aus der Espressif-Datasheet v1.5)

Der ESP32-C6-MINI-1 führt 22 GPIOs heraus. Belegt sind hier:

| Modulpin | Name | Verwendung hier |
|---|---|---|
| 3 | 3V3 | +3V3 (zusammen mit allen VDD33-Pins) |
| 5 | IO2 | **PUMP_EN** |
| 6 | IO3 | **SENSOR_PWR** (ADC1_CH3) |
| 8 | EN | Reset-RC + SW1 |
| 9 | IO4 | **LIGHT_AOUT** (ADC1_CH4, „P1" = direkter IO-MUX-Pfad). IO4 ist **kein boot-kritischer** Strapping-Pin (siehe Hinweis unten) |
| 19 | IO14 | **LED_STAT** — frei gewählt, nicht IO4; IO14 liegt außerhalb der LP-GPIOs und ist kein Strapping-Pin |
| 15 | IO6 | **BTN** — externer Taster. **LP_GPIO6** (weckt aus dem Deep-Sleep), **kein** Strapping-Pin. JTAG wird dadurch nicht genutzt (Flashen über USB-Serial-JTAG auf IO12/13) |
| 16 | IO7 | **LED_TANK** — **LP_GPIO7**, ebenfalls kein Strapping-Pin |
| 12 | IO0 | **SENSOR_AOUT** (ADC1_CH0) |
| 13 | IO1 | **VBAT_SENSE** (ADC1_CH1) |
| 17 | IO12 | **USB_D−** |
| 18 | IO13 | **USB_D+** |
| 22 | IO8 | Strapping-Pin, nur Pull-up |
| 23 | IO9 | **BOOT** (Strapping) + Pull-up |
| 10 | IO5 | **SPARE_AIN** (ADC1_CH5) — Reserve-Analog an **J9**, über R_SPARE_AIN 1 kΩ + C_SPARE 100 nF |
| 20 | IO15 | **SPARE_IO15** — Reserve an **J10** (Strapping JTAG-Quelle, Default-eFuses inert), über R_SPARE_IO15 1 kΩ |
| 24 | IO18 | **SDA_MCU** — I²C-Daten an **J8**, über R_SDA_S 1 kΩ |
| 25 | IO19 | **SCL_MCU** — I²C-Takt an **J8**, über R_SCL_S 1 kΩ |
| 26 | IO20 | **EXT_EN** — Load-Switch Q2 (interner WPU beim Reset ⇒ VCC_EXT aus) |
| 27 | IO21 | **SPARE_IO21** — Reserve an **J13**, über R_SPARE_IO21 1 kΩ (WPU beim Reset) |
| 28 | IO22 | **SPARE_IO22** — Reserve an **J14**, über R_SPARE_IO22 1 kΩ |
| 29 | IO23 | **SPARE_IO23** — Reserve an **J15**, über R_SPARE_IO23 1 kΩ |
| 30 / 31 | RXD0 / TXD0 | **UART_RX (IO17) / UART_TX (IO16)** — optional UART-Debug (DNP); zugleich über R_SPARE_IO17/16 an **J12/J11** |
| 1, 2, 11, 14, 36–53 | GND | Masse |
| 49 | EPAD | Thermo-Pad — mit GND verbinden (Espressif: nicht Pflicht, verbessert die Wärmeabfuhr) |
| div. | VDD33 | **alle** an +3V3, jeweils 100 nF in der Nähe |

**Herausgeführt als 2,54-mm-Stiftleisten (ab 14.09.2026):** IO4 (Lichtsensor) an **J7**, IO5 an
**J9**, IO15 an **J10**, IO16 an **J11**, IO17 an **J12**, IO18/IO19 (I²C) an **J8**, IO21 an
**J13**, IO22 an **J14**, IO23 an **J15**. IO20 bleibt **intern** (Load-Switch-Steuerung, nicht
auf einen Stecker geführt).
Espressif: unbenutzte hochohmige Pins mit Pull-up/down versehen oder internen Pull aktivieren
(verhindert Mehrverbrauch im Schlaf).

**GPIO9-Regel beachten:** kein großer Kondensator am Pin, sonst startet der Chip in den
Download-Modus statt in die Anwendung.

**Korrektur der Strapping-Aussage (13.09.2026):** Frühere Dokumentstände nannten IO4/IO5
pauschal „Strapping-Pins" und damit tabu. Das ist **so nicht richtig**:

- **Boot-kritische Strapping-Pins** sind nur **GPIO8, GPIO9** (Boot-Modus; nur `GPIO8 = 0`
  **und** `GPIO9 = 0` zugleich ist als ungültig markiert) und **GPIO15** (JTAG-Quellenwahl,
  mit den Default-eFuses wirkungslos).
- **IO4/IO5 (MTMS/MTDI)** sind **keine** Boot-Modus-Strapping-Pins. Ihre Strap-Funktion ist
  ausschließlich die **SDIO-Slave-Flankenneigung**; der Wert 0 ist ausdrücklich erlaubt und
  ohne SDIO-Slave wirkungslos. Beim Reset haben beide **keine** internen Pulls (nur Input
  enabled) und sind danach normale IO-Pins. Deshalb ist IO4 als ADC-Eingang (ADC1_CH4)
  auch mit hochohmiger Quelle (R_LIGHT 10 kΩ + R_LIGHT_S 1 kΩ + C_LIGHT 100 nF) zulässig.
- Einziger verbleibender Vorbehalt: **Falls Pad-JTAG** (statt USB-Serial-JTAG) je gebraucht
  wird, sind IO4/IO5 dafür freizuhalten. Geflasht wird hier über USB-Serial-JTAG auf IO12/13.

---

## 5. Pinbelegungen der ICs — Stand der Belege

| Bauteil | Pinbelegung | Belegstatus |
|---|---|---|
| **USBLC6-2SC6** | 1 = I/O1 · 2 = GND · 3 = I/O2 · 4 = I/O2 · 5 = VBUS · 6 = I/O1 | ✅ aus dem Datenblatttext verifiziert (1/6 und 3/4 sind die Durchschleifpaare) |
| **MCP73831 (SOT-23-5)** | 1 = STAT · 2 = VSS · 3 = VBAT · 4 = VDD · 5 = PROG | ⚠️ aus dem „Package Types"-Text des Datenblatts abgeleitet; **Pin-Configuration-Bild nicht textlich prüfbar → beim Footprint gegenprüfen** |
| **ME6211 (SOT-23-5)** | 1 = VIN · 2 = GND · 3 = EN · 4 = NC · 5 = VOUT | ⚠️ **noch gegenprüfen** (Datenblatt zeigt nur Bild). **EN an VIN/VBAT** legen — auf +3V3 gelegt könnte der Regler nicht starten |
| **MAX809 (SOT-23)** | 1 = GND · 2 = RESET · 3 = VCC | ⚠️ **noch gegenprüfen** (Bild) |
| **AO3400A (SOT-23)** | 1 = Gate · 2 = Source · 3 = Drain | ⚠️ **noch gegenprüfen** (Bild) |
| **AO3401A (SOT-23)** | 1 = Gate · 2 = Source · 3 = Drain | ⚠️ **noch gegenprüfen** (Bild); gleiche Pinbelegung wie AO3400A. Hier Source → +3V3, Drain → VCC_EXT (P-Kanal-High-Side) |

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
5. **Testpunkte im Layout vorsehen:** TP1/TP2 (UART-Debug), TP3 (GND), TP4 (VBAT),
   TP5 (+3V3), TP6 (SENSOR_AOUT).
6. **Layout-Vorgaben aus Espressif:** EN-Leitung kurz halten; USB als 90-Ω-Differentialpaar mit
   GND-Referenzlage; Antenne → siehe `bom_entscheidung.md` §6 (bauteilfreier Bereich, dünnere
   Wulstwand, 15 mm Freistellung im Gehäuse).
7. **Vor dem Bestücken zu klären:** die vier mit ⚠️ markierten Pinbelegungen, die Polarität von J1,
   und die Farbwahl der Lade-LED.

---

## 7. Externer Taster und Tank-LED (ergänzt 11.09.2026)

### 7.1 Warum

- **Nachfüllen bestätigen:** Ist der Tank leer, muss der Benutzer das Nachfüllen quittieren —
  sonst weiß die Firmware nicht, ob der Tank wieder voll ist. Dafür ein Taster.
- **„Tank leer" sichtbar machen:** eine rote LED auf der Platine, die den leeren Tank anzeigt.

### 7.2 Der Taster sitzt **nicht** auf der Platine

Der Taster kommt ins Gehäuse (von außen bedienbar) und wird mit zwei Kabeln an die Platine
gelötet. Auf der Platine liegen deshalb nur **zwei metallisierte Bohrungen Ø 1,0 mm im Raster
2,54 mm** (J6) — kein Stecker, keine BOM-Position, **keine JLC-Kosten**. Der Taster selbst ist
kein bestücktes Bauteil.

Was **auf** der Platine bleibt (weil es dazugehört):

| Bauteil | Wert | Zweck |
|---|---|---|
| **R_BTN** | 10 kΩ nach +3V3 | Pull-up; hält IO6 im Ruhezustand auf High. Ruhestrom **0 µA** (offener Taster), gedrückt 330 µA |
| **C_BTN** | 100 nF nach GND | Entprellung, RC = **1 ms**; hält zugleich Einstreuungen auf der Tasterleitung fern |

| Der Taster schließt **IO6 auf GND** (active low) — dieselbe Logik wie Reset und Boot.

**Option gegen Einstreuung:** Ein Serienwiderstand von 100–470 Ω zwischen J6 Pin 1 und IO6 schützt den Pin zusätzlich gegen ESD über das Tasterkabel (bei kurzen Kabeln nicht nötig; C_BTN deckt den Normalfall ab). Der Taster ist kein Strapping-Pin und beeinflusst den Boot **nicht** — ein gedrückter Taster beim Einschalten ist unkritisch.

**Reststrom, falls der Taster klemmt:** dauerhaft gedrückt = 330 µA ≈ 8 mAh/Tag. Nicht kritisch, aber die Firmware sollte eine ungewöhnlich lange Betätigung erkennen können.

### 7.3 Pinwahl: IO6 (Pin 15) ist bewusst gewählt

- Der Tastendruck muss das Gerät aus dem **Deep-Sleep wecken** — sonst reagiert es im
  Ruhezustand nicht. Das geht nur über die **LP-/RTC-GPIOs**, und das sind beim ESP32-C6
  **IO0–IO7** (Datenblatt-Modulpinbelegung: „MTCK, GPIO6, **LP_GPIO6**" = Pin 15).
- **Ausgeschlossen für die Weckquelle:** IO4/IO5 — nicht wegen des Boots (siehe Korrektur in §4),
  sondern weil ihre SDIO-Strap-Funktion für Pad-JTAG reserviert bleibt — sowie IO8/IO9/IO15
  (boot-kritische Strapping-Pins bzw. belegt).
- Folge: **JTAG steht nicht mehr zur Verfügung** — geflasht und debuggt wird über
  **USB-Serial-JTAG** auf IO12/IO13, das ist ohnehin die vorgesehene Variante.
- Firmware: Weckquelle `EXT1` mit `ESP_EXT1_WAKEUP_ANY_LOW` auf LP_GPIO6.
- **Warum der Pull-up extern sein muss:** im Deep-Sleep sind die internen Pull-ups des Chips abgeschaltet. Ohne den externen 10 kΩ läge IO6 in dieser Zeit **undefiniert** und könnte ein Aufwachen auslösen (Fehlwecken) oder den Tastendruck nicht erkennen. Der externe Pull-up wirkt in **allen** Betriebsarten — deshalb ist er keine Einsparung, sondern Voraussetzung.

### 7.4 Die LED

- **D5** (rot, gleicher 0805-Typ wie D2) an **IO7 (Pin 16, LP_GPIO7)** über **R_TANK 1 kΩ**
  → **1,3 mA** bei Vf ≈ 2,0 V.
- **D2 ist die Status-LED** (IO14) — seit 11.09.2026 **grün** (C2297), damit sie nicht mit der roten
  Warnung verwechselt wird. Die drei LEDs sind klar getrennt: **D2 grün = Status/Betrieb**,
  **D5 rot = Tank leer**, **D_LEDCHG rot = Ladestatus** (vom Lader selbst gesteuert).
- **Stromspar-Hinweis für die Firmware (wichtig):** D5 dauerhaft an würde **1,3 mA** ziehen —
  das ist das **19-fache** des gesamten Standby-Budgets (69,5 µA) und entspricht **31 mAh/Tag**;
  die Zelle wäre in ~48 Tagen leer. Richtig ist **Blinken**, z. B. 3 × 50 ms alle 5 s
  → Mittelwert **~39 µA**. Alternativ R_TANK auf 2,2 kΩ (0,6 mA) — dann ist dauerhaftes Leuchten
  vertretbar, wenn es sichtbar genug ist.
- Die Anzeige ist eine **Firmware-Aufgabe**: der leere Tank wird per Sensor erkannt, der Zustand
  wird gehalten (latch), bis der Taster gedrückt wird.
- **Dasselbe gilt für die Status-LED D2** (2,05 mA): auch sie nur **kurz blinken** lassen.
  Dauerlicht wären 2,05 mA ≈ **49 mAh/Tag** — rund das 30-fache des Standby-Budgets (69,5 µA).
  Jede LED im Dauerbetrieb kostet mehr als alles andere im Gerät zusammen; die LEDs sind
  Anzeigen, keine Beleuchtung.

### 7.5 Ablauf in der Firmware (Vorschlag)

1. Messzyklus erkennt „Tank leer" (Sensorwert nach Pumpen unverändert) → **Zustand latch**,
   D5 blinken, Telegram-Meldung „Tank leer — bitte nachfüllen und Taster drücken".
2. Benutzer füllt nach und **drückt den Taster** → das Gerät wacht auf (EXT1),
   Latch wird gelöscht, D5 aus, Bestätigung per Telegram.
3. Zusätzliche Absicherung: Steigt der Sensorwert im nächsten Messzyklus deutlich an, gilt der
   Tank auch **ohne** Tastendruck als nachgefüllt (der Taster ist Bedienkomfort, keine
   Voraussetzung für den Betrieb).

### 7.6 JLC-Verfügbarkeit (geprüft 11.09.2026, live)

| Position | LCSC | Typ | Bestand | Preis |
|---|---|---|---|---|
| D5 + D_LEDCHG (LED **rot** 0805) | `C84256` | **basic** | 6.141.918 | $0,0134 |
| D2 (LED **grün** 0805, 525 nm) | `C2297` | **basic** | 1.627.076 | $0,0163 |
| R4 (**220 Ω** 0805) | `C17557` | **basic** | 1.195.891 | $0,0058 |
| R_BTN (10 kΩ 0805) | `C17414` | **basic** | 54.370.181 | $0,0039 |
| R_TANK (1 kΩ 0805) | `C17513` | **basic** | 30.777.288 | $0,0042 |
| C_BTN (100 nF 0805) | `C49678` | **basic** | 18.966.887 | $0,0196 |
| J6 (2 Bohrungen) | – | – | – | keine Bestückung, keine Kosten |

**Es kommt kein neues Bauteil und keine neue Extended-Position hinzu** — alle vier Bauteile sind
bereits im Design und auf Lager.

### 7.7 Was im Gehäuse noch fehlt (offener Punkt für die Konstruktion)

1. **Bohrung** für den Taster in der Außenwand (Gehäuse), plus Weg für das zweiadrige Kabel zur
   Platine. Der Taster sitzt so, dass man ihn **ohne** Öffnen des Gehäuses drücken kann.
2. **LED-Fenster:** der Deckel hat ein LED-Fenster — es muss **beide** LEDs (D2 und D5)
   abdecken, oder es braucht ein zweites Fenster (z. B. zwei kleine Lichtleiter).
3. Antennen-Freistellung bleibt unberührt: die LED-Plätze liegen **nicht** im oberen,
   bauteilfreien Bereich der Kammer.
4. Diese Punkte gehören in `docs/02_architektur-und-geometrie.md` + `cad/params.py` und
   werden über OpenCode geändert (Gehäusecode schreibt OpenCode, nicht der Koordinator).

---

## 8. Externer Lichtsensor (ergänzt 13.09.2026)

### 8.1 Warum und wie

Bewässert wird **nur in der Dunkelphase** (Growlicht aus): unter Licht verdunstet mehr, und
Tropfwasser auf dem Substrat soll nicht mit der Lampenabwärme kollidieren. Der Lichtsensor
kommt **extern an einem Kabel** an den Topfrand/Tent — **nicht** auf die Platine. Auf der
Platine sitzt nur der **Stecker J7** mit dem Lastwiderstand, dem Serienschutz und dem ADC-Filter.

Der Sensor selbst ist **keine BOM-/PCBA-Position** — er wird separat beschafft.

**Typwechsel 14.09.2026:** J7 ist jetzt eine **2,54-mm-Stiftleiste 1×3, male gerade**
(`C2937625`) — derselbe Steckpins-Typ wie die Reserve-Stecker J9–J15. Der Nutzer steckt
Dupont-Buchsen direkt auf, es ist keine Crimpzange nötig. Die Pinordnung
**GND–VCC–SIG** bleibt unverändert.

### 8.2 Netze

| Netz | Verbindungen | Zweck |
|---|---|---|
| **SENSOR_PWR** | U1 **Pin 6 (IO3)** → J2 Pin 2 (Feuchte) ↔ J7 Pin 2 (Licht) | beide Sensoren nur während der Messung versorgt |
| **LIGHT_RAW** | J7 Pin 3 ↔ R_LIGHT 10 kΩ → GND ↔ R_LIGHT_S 1 kΩ | Sensorausgang; R_LIGHT gibt dem **offenen Stecker** einen definierten Pegel (0 V) |
| **LIGHT_AOUT** | R_LIGHT_S 1 kΩ ↔ U1 **Pin 9 (IO4, ADC1_CH4)** ↔ C_LIGHT 100 nF → GND | ADC-Eingang, RC-gefiltert |

### 8.3 Neue Positionen (Werte und LCSC sind schon im Projekt)

| Pos | Wert | LCSC | Zweck |
|---|---|---|---|
| **J7** | Stiftleiste 1×3, 2,54 mm, male | `C2937625` | externer Lichtsensor — Dupont-Buchse direkt aufstecken (Typwechsel 14.09.2026) |
| **R_LIGHT** | 10 kΩ | `C17414` | Lastwiderstand/definierter Zustand: **offener Stecker ⇒ 0 V ⇒ „dunkel"** |
| **R_LIGHT_S** | 1 kΩ | `C17513` | Serienschutz für den ADC (wie R6) |
| **C_LIGHT** | 100 nF | `C49678` | ADC-Filter (Espressif: 0,1 µF am ADC-Pin) |

**Belegung J7 (GND–VCC–SIG, seit 13.09.2026):** **1 = GND · 2 = VCC (SENSOR_PWR) · 3 = AOUT.**
Die Ordnung **GND–VCC–SIG** ist Absicht (Begründung in §9.1).
Der Sensor liegt bewusst an **SENSOR_PWR** und **nicht** an +3V3: ein dauerhaft versorgter
Lichtsensor (ALS-PT19 typ. < 1 mA, Module mit LDO mehr) würde das gesamte Standby-Budget
(69,5 µA) um ein Vielfaches überschreiten.

### 8.4 Begründung der Ausfallsicherheit

- Ein zweipoliger Fototransistor, der **bricht oder abgezogen wird**, liefert über R_LIGHT
  **„dunkel"** ⇒ Bewässerung **bleibt erlaubt**. Ein blockierender Fehler wäre der schlimmere
  (die Pflanze würde vertrocknen). Der offene Eingang ist durch R_LIGHT auf GND definiert und
  schwebt **nicht**.
- Damit das nicht unentdeckt bleibt, erkennt die Firmware **„seit 24 h keine Lichtänderung"**
  oder **dauerhafte Sättigung** und meldet per Telegram „Licht-Sensor unplausibel"
  (Firmware-Konzept, Licht-Gate).

### 8.5 ADC-Rechnung (ALS-PT19-315C/L177/TR8, LCSC `C146233`)

| Größe | Wert | Herleitung |
|---|---|---|
| ADC-Modus | `ADC_ATTEN_DB_12` (ATTEN3, 0–3300 mV, 12 Bit) | derselbe Bereich wie der VBAT-Teiler |
| Dunkelstrom | ICEO ≤ **0,1 µA** | Datenblatt ALS-PT19 |
| Dunkelspannung | 0,1 µA × 10 kΩ = **1 mV** | ≈ **1 Count** |
| Empfindlichkeit | 15 µA typ @ 100 lx | Datenblatt ALS-PT19 |
| Sättigung ab | I = 3,3 V / 10 kΩ = 330 µA ⇒ **≈ 2.200 lx** | darüber ADC-Vollausschlag (4095) |
| Growlicht | ≥ 10.000 lx | typische LED-Growlampe am Canopy ⇒ **Sättigung** |

Dunkel ≈ 0–1 Counts, im Growlicht Sättigung — der Abstand ist um ein Vielfaches größer als die
doppelte Hysterese. Geprüft von `check_light_contrast`, `check_light_adc_filter`,
`check_light_open_connector`, `check_standby_budget` und `check_pin_disziplin`
(siehe `design/`).

---

## 9. Pinordnung und Steckpins (GND–VCC–SIG, ab 14.09.2026)

**Alle freien GPIOs und der I²C-Bus sind als 2,54-mm-Stiftleiste (male, gerade) herausgeführt** —
Kabel mit Dupont-Buchse werden direkt aufgesteckt, es ist keine Crimpzange nötig. **Jeder freie
GPIO bekommt einen eigenen 3-poligen Stecker** (nicht kompakt, nicht 2-reihig). Alle 3-poligen
Stecker haben einheitlich die Ordnung **GND–VCC–SIG** (VCC in der Mitte, Pin 2); der 4-polige
I²C-Stecker J8 folgt **GND–VCC–SDA–SCL** (VCC innen, wie Qwiic/STEMMA). J2 bleibt JST-XH.

### 9.1 Pinbelegung aller Stecker

| Stecker | Typ | Pin 1 | Pin 2 (VCC) | Pin 3 | Pin 4 | Signal → MCU |
|---|---|---|---|---|---|---|
| **J2** | JST-XH 3P (`C157928`) | GND | SENSOR_PWR | SENSOR_RAW | – | R6 1 kΩ → IO0 (Pin 12) |
| **J7** | Stiftleiste 1×3 (`C2937625`) | GND | SENSOR_PWR | LIGHT_RAW | – | R_LIGHT_S 1 kΩ → IO4 (Pin 9) |
| **J8** | Stiftleiste 1×4 (`C2691448`) | GND | VCC_EXT | SDA | SCL | R_SDA_S/R_SCL_S 1 kΩ → IO18/IO19 (Pin 24/25) |
| **J9** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_AIN_RAW | – | R_SPARE_AIN 1 kΩ → IO5 (Pin 10) |
| **J10** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO15_RAW | – | R_SPARE_IO15 1 kΩ → IO15 (Pin 20) |
| **J11** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO16 | – | R_SPARE_IO16 1 kΩ → IO16/TXD0 (Pin 31) |
| **J12** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO17 | – | R_SPARE_IO17 1 kΩ → IO17/RXD0 (Pin 30) |
| **J13** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO21_RAW | – | R_SPARE_IO21 1 kΩ → IO21 (Pin 27) |
| **J14** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO22_RAW | – | R_SPARE_IO22 1 kΩ → IO22 (Pin 28) |
| **J15** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO23_RAW | – | R_SPARE_IO23 1 kΩ → IO23 (Pin 29) |

### 9.2 Warum GND–VCC–SIG

Bei einem 3-poligen Stecker ist **nur der mittlere Pin gegen Umdrehen invariant** (aus 1↔3 wird
2↔2). Liegt dort **VCC**, kann ein verkehrt gesteckter Stecker

- **niemals 3,3 V auf einen MCU-Pin** legen und
- **niemals die Versorgung über unsere Masse kurzschließen** —

genau der Fehler, der mit der früheren Ordnung (1 = VCC, 3 = GND) möglich war.

**Fehlerfall neu:** VCC bleibt korrekt auf Pin 2, **GND und SIG tauschen**. Der Sensor bekommt
seine Masse dann über den **1-kΩ-Serienwiderstand** unseres Signaleingangs (≈ 3 mA, pin-sicher),
der GND-Strom fließt in unseren Eingang (ESD-Dioden nach GND), das Signal landet auf unserer
Masse. Ergebnis: **keine Funktion, kein Schaden** — die gewünschte Ausfallsicherheit.

### 9.3 1 kΩ in Reihe in JEDER Signalleitung

Zwischen **jedem Stecker-Signalpin und dem MCU** liegt ein **1-kΩ-Serienwiderstand** — auch in
**SDA/SCL** und in den Reserve-Leitungen:

| Leitung | Serien-R | Leitung | Serien-R |
|---|---|---|---|
| J2 SENSOR_RAW | R6 | J13 SPARE_IO21 | R_SPARE_IO21 |
| J7 LIGHT_RAW | R_LIGHT_S | J14 SPARE_IO22 | R_SPARE_IO22 |
| J8 SDA | R_SDA_S | J15 SPARE_IO23 | R_SPARE_IO23 |
| J8 SCL | R_SCL_S | J10 SPARE_IO15 | R_SPARE_IO15 |
| J9 SPARE_AIN | R_SPARE_AIN | J11 SPARE_IO16 | R_SPARE_IO16 |
| | | J12 SPARE_IO17 | R_SPARE_IO17 |

Der Serienwiderstand liegt immer **zwischen Stecker-Pin und MCU-Pin** und begrenzt Fehlerströme
in den Pin (z. B. wenn ein Dupont-Kabel verkehrt gesteckt oder ein Sensor ohne Versorgung
angeschlossen wird).

### 9.4 Load-Switch für VCC_EXT (Fail-safe: beim Reset aus)

Die Erweiterungsversorgung **VCC_EXT** kommt **nicht** direkt vom 3,3-V-Rail und **nicht** von
einem GPIO, sondern über einen **P-Kanal-MOSFET Q2 (AO3401A)**:

- **Source → +3V3**, **Drain → VCC_EXT**, **Gate → EXT_EN (IO20)**.
- **R_GATE 47 kΩ** zieht das Gate **nach +3V3** (Quellpotential). Ohne aktiven GPIO ist damit
  **VGS = 0** ⇒ Q2 sperrt ⇒ **VCC_EXT ist aus**.
- IO20 zieht das Gate über den offenen Drain **nach unten**, um VCC_EXT einzuschalten. Beim
  Reset hat IO20 einen internen **Weak-Pull-up** (Espressif ESP32-C6) ⇒ Rail ist beim Start
  **aus** — die gewünschte Fail-safe-Richtung.
- Dadurch kann ein angeschlossenes Erweiterungsmodul den Bus **im Aus-Zustand nicht** über die
  I²C-Leitungen oder VCC_EXT rückwärts versorgen.

### 9.5 I²C-Pull-ups an VCC_EXT (nicht an +3V3)

**R_SDA_PU und R_SCL_PU (je 10 kΩ)** hängen an **VCC_EXT**, nicht an +3V3. Ist VCC_EXT aus,
liegt der Bus hochohmig an 0 V und zieht **keinen Strom**. 10 kΩ sind für kurze Kabel (wenige cm
bis ca. 30 cm) und die üblichen 100-kHz-/400-kHz-I²C-Module plausibel. Der Serien-R (1 kΩ)
begrenzt zusätzlich den Fehlerstrom in die MCU-Pins.

### 9.6 Fehlerfall-Tabelle

| Fehler | neue Ordnung GND–VCC–SIG | alte Ordnung VCC–SIG–GND |
|---|---|---|
| Stecker verkehrt gesteckt | VCC bleibt auf Pin 2; GND/SIG tauschen. Masse fließt über den 1-kΩ-Serien-R (≈ 3 mA, pin-sicher), Signal liegt auf unserer Masse. **Keine Funktion, kein Schaden.** | 3,3 V liegen auf dem MCU-Signalpin; die Versorgung wird über unsere Masse kurzgeschlossen → **Pin-/Leistungsschaden möglich** |
| Stecker offen (J2) | R6 liefert einen definierten Pegel, ADC schwebt nicht | – |
| Stecker offen (J7) | R_LIGHT zieht LIGHT_RAW auf 0 V ⇒ „dunkel" ⇒ Bewässerung bleibt erlaubt (unkritisch) | – |
| Erweiterung nicht gesteckt | VCC_EXT bleibt aus, kein Busstrom; J9–J15 unbenutzt | – |

### 9.7 Aderfarben-Empfehlung

- 3-polig: **schwarz = GND · rot = VCC · gelb = Signal (SIG)** (GND–VCC–SIG von links nach rechts).
- 4-polig (J8): **schwarz = GND · rot = VCC_EXT · weiß = SDA · grün = SCL**.
- Signaladern vor dem Anschließen auf Durchgang/Polung prüfen.

### 9.8 Hinweis zur Aufgabenliste

- **`LIGHT_RES`** wurde **nicht** als neues Netz angelegt: Die bestehenden Netze **LIGHT_RAW**
  (Steckerseite von R_LIGHT_S) und **LIGHT_AOUT** (ADC-Seite) beschreiben diese Knoten bereits.
  Ein zusätzliches Netz hätte R_LIGHT_S kurzgeschlossen und die Schutzwirkung aufgehoben.

---

## 10. Rückschau

- 14.09.2026: GPIO-Erweiterung (J8/J9/J10/Q2/TP7–TP11) auf Wunsch des Nutzers wieder entfernt.
- 14.09.2026: GPIO-Erweiterung auf 2,54-mm-Stiftleisten wieder eingebaut (je Signal ein
  3-pol GND–VCC–SIG-Stecker, I²C als 4-pol).
