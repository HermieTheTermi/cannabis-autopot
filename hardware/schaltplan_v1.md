# Schaltplan V1 — Smart Grow Topf

Stand: **16.09.2026, Revision „2S-Umbau"** · **Diese Datei ist die Verbindungsvorgabe für das Layout.**
Alle Bauteilwerte sind aus den Herstellerdatenblättern abgeleitet (Quelle jeweils in der Spalte „Warum").
Maschinenlesbare Fassung derselben Verbindungen: **`schaltplan_v1_netzliste.csv`** (`Netz, Bauteil, Pin, Bemerkung`).

> ⚠️ **Was diese Revision geändert hat (Kurzfassung, Details in §13):**
> 1S-LiPo → **2S-Pack (6,0–8,4 V)**, 1S-Lader → **IP2326** (Boost-Lader aus 5 V USB, 8,4 V / 0,90 A),
> 5-V-**Boost** → 5-V-**Buck**, 3,3-V-**LDO** → 3,3-V-**Buck**, Unterspannungswächter **MAX809 (3,08 V an 1S)**
> → **TPS3839G33 (3,08 V an einem 1:2-Teiler ⇒ 6,16 V Pack)**. Der frühere Klemmzweig war im Bestand
> **unwirksam** (Parallelschaltung statt Serienkette) und ist hier korrigiert (§13.4).

---

## 1. Blöcke

```
   USB-C (J5) ──VBUS 5 V──┬────────────────────────────────► U_CHG  IP2326  (2S-Boost-Lader, 8,4 V)
                          │                                    │
                          ├── L_CHG 2,2 µH ──► LX (15/16/17)    │ VOUT (21/22)
                          ├── R_VIN_CHG 0,5 Ω ─► VIN (13) + C   └──► VBAT ──┬── J1  2S-Pack (6,0–8,4 V, mit BMS)
                          ├── R_LEDCHG 1 k ─► D_LEDCHG ─► LED (6)           │
                          └── D+/D− ── U6 ESD ── U1 IO13/IO12              │
   (DP/DM des Laders bleiben OFFEN — kein Fast-Charge-Request, die Datenleitungen gehören dem ESP32)

   VBAT ─┬── U_BUCK5  SY8113B   (3 A, 500 kHz) ──► +5V ──┬── Q1 ──► J4   Dosierpumpe
         │                                               ├── Q3 ──► J16  Sauerstoffpumpe
         │                                               ├── J17        5-V-Ausgang für Sensorik (neu)
         │                                               └── C3 100 µF (Pumpenpuffer, von VBAT hierher)
         ├── U_BUCK3  AP63203    (2 A, 1,1 MHz)  ──► +3V3 ──► ESP32-C6 (U1), Sensorspeisung (IO3),
         │                                                   LEDs, I2C/VCC_EXT über Q2
         ├── R3a/R3b 200 k/200 k ──► U7 TPS3839G33 (3,08 V) ──► RESET_UV ──┬── U_BUCK5 EN  (5-V-Schiene AUS)
         │                                                                 └── D3/D8 über R35/R36 (Gate-Klemmen)
         └── R_SENSE_TOP/BOT 200 k/68 k ──► VBAT_SENSE (U1 IO1, ADC 1:3,94 → 2,13 V bei 8,4 V)
```

**Logik-Ein-/Ausgänge (unverändert):** IO0 Feuchte-ADC · IO1 **Packspannung (neu 1:3,94)** · IO2 Pumpe ·
IO3 Sensor-Versorgung · IO4 Lichtsensor-ADC · IO5 Reserve-ADC (J9) · IO6 externer Taster (LP_GPIO6) ·
IO7 Tank-LED (LP_GPIO7) · IO14 Status-LED · IO9 Boot · IO12/13 USB · IO15–IO17, IO21–IO23 Reserve ·
IO18/IO19 I²C (J8) · IO20 Load-Switch VCC_EXT · IO22 Sauerstoffpumpe.

**Versorgungskette (Stand 16.09.2026):** USB-C 5 V → **IP2326-Boost-Lader** → **VBAT (2S, 6,0–8,4 V)** →
{ **Buck U_BUCK5 → +5 V → beide Pumpen · Buck U_BUCK3 → +3,3 V → Logik** }.
Es gibt **keinen** Aufwärtswandler und **keinen** LDO mehr.

### 1.1 Warum 2S + zwei Abwärtswandler (und nicht mehr 1S + Boost)

| Kriterium | 1S + Boost (bis 15.09.2026) | **2S + zwei Bucks (jetzt)** |
|---|---|---|
| Pumpenanlauf 3 A | ❌ Boost kann nur 2 A Schalterstrom → Softstart **Pflicht** | ✅ 3-A-Buck **am Nennstrom der Pumpe**; Softstart nur noch empfohlen |
| Logikversorgung | ❌ LDO kann aus 3,0 V keine 3,3 V machen → nutzbarer Bereich nur 4,2 → ~3,5 V | ✅ Buck regelt bis 6,0 V (Wächter-Schwelle) herunter → **volle Ausnutzung bis 6,16 V Pack** |
| Wirkungsgrad 3,3 V | LDO: (3,3/4,2) = **79 %**, bei 5-V-Einspeisung nur 66 % | Buck: **≈ 88 %** (8,4 V → 3,3 V) |
| Ladestrom | 256 mA (MCP73831) | **0,90 A** (IP2326, ICHG = 90000/R_ISET) |
| Energie im Pack | 5,55 Wh (1500 mAh, 1S) | **11,1 Wh** (1500 mAh, 2S) |
| Nachteile | — | 2 Zellen müssen **gebalt** werden (BMS-Pflicht, §6.3); Ruhestrom steigt von 70 µA auf ~160 µA (§6.2) |

---

## 2. Netze (was womit verbunden wird)

### 2.1 Ladepfad / Eingang (geändert)

| Netz | Verbindungen | Zweck |
|---|---|---|
| **VBUS** | J5 VBUS (4 Pins) ↔ U6 Pin 5 ↔ **C_CHG_IN 10 µF** ↔ **R_VIN_CHG 0,5 Ω** ↔ **L_CHG 2,2 µH** ↔ **R_LEDCHG 1 kΩ** ↔ **R_EN_CHG 100 kΩ** | 5-V-Eingang, Eingangspuffer, Boost-Induktivität, LED-Vorwiderstand, EN-Pull-up |
| **VBUS_CHG** | R_VIN_CHG Pin 2 ↔ **U_CHG Pin 13 (VIN)** ↔ **C_CHG_VIN 10 µF** | gefilterte Steuerversorgung des Laders (0,5 Ω + 10 µF) — **kein** Ladestrompfad, die Leistung fließt über L_CHG → LX |
| **LX_CHG** | **U_CHG Pin 15/16/17 (LX)** ↔ **L_CHG Pin 2** ↔ **C_BST_CHG Pin 2** | Schaltknoten des Boost-Laders |
| **BST_CHG** | U_CHG Pin 14 (BST) ↔ **C_BST_CHG 100 nF** | Bootstrap für den High-Side-Treiber (Pin-Abstand einhalten!) |
| **VSYS_CHG** | U_CHG Pin 19/20 (VSYS) ↔ **C_VSYS_A 22 µF** ↔ **C_VSYS_B 22 µF** | Zwischenknoten des Boost-Ausgangs, **nicht** extern mit VBAT verbunden (Datenblatt: „2× 22 µF direkt am Pin") |
| **ISET_CHG** | U_CHG Pin 11 (ISET) ↔ **R_ISET 100 kΩ 1 %** → GND | Ladestrom: **ICHG = 90000 / 100000 = 0,90 A** (ISET darf laut Datenblatt **nicht** offen bleiben) |
| **NTC_DIS** | U_CHG Pin 4 (NTC) ↔ **R_NTC 51 kΩ** → GND | NTC-Funktion stillgelegt: 20 µA × 51 kΩ = **1,02 V** = Normalbereich (0,56–1,32 V) |
| **UVSET_CHG** | U_CHG Pin 8 (VIN_UVSET) ↔ **R_UVSET 68 kΩ** → GND | Eingangs-Unterspannungsschwelle **4,35 V** (statt 4,65 V) → mehr Kopfraum für dünne USB-Kabel bei ~1,6–1,8 A |
| **EN_CHG** | U_CHG Pin 12 (EN) ↔ **R_EN_CHG 100 kΩ** → VBUS | Laden ist **an, sobald USB steckt** — unabhängig von der Firmware (§6.1) |
| **LED_CHG / STAT_CHG** | VBUS → R_LEDCHG 1 kΩ → **D_LEDCHG Anode** · **Kathode → U_CHG Pin 6 (LED)** | Ladeanzeige; der LED-Pin ist eine **Senke** (max. 5 mA) → ~2,7 mA |
| **CC1 / CC2** | J5 A5 ↔ **R5a 5,1 kΩ** → GND · J5 B5 ↔ **R5b 5,1 kΩ** → GND | USB-C-Senke (unverändert). **Kein** Rp, **kein** PD — die Quelle darf 5 V/2,4 A liefern |
| **offen (NC)** | U_CHG Pin 1 (DM), Pin 2 (DP), Pin 3 (VSET), Pin 5 (BAT_STAT), Pin 7 (TIME_SET), Pin 9 (VIN_OVSET), Pin 10 (CON_SEL), Pin 23 (VBATM), Pin 24 (VBAT_GND) | **VSET** offen ⇒ 8,4 V (die 8V8-Variante wäre 8,8 V → **nicht** verwenden!); **CON_SEL** offen ⇒ 2S; **TIME_SET** offen ⇒ 24 h Timeout; **VIN_OVSET** offen ⇒ 8,75 V (bei 5-V-Quelle irrelevant); **DM/DP** offen ⇒ kein Fast-Charge-Request (§6.1); **VBATM/VBAT_GND** offen ⇒ internes Balancing aus (§6.3) |

### 2.2 Batterie und Wächter (geändert)

| Netz | Verbindungen | Zweck |
|---|---|---|
| **VBAT** | U_CHG Pin 21/22 (VOUT) ↔ **C_CHG_OUT 10 µF** ↔ **J1 Pin 1 (2S-Pack +)** ↔ TP4 ↔ U_BUCK5 IN ↔ C_B5_IN 22 µF ↔ C_B5_IN_HF ↔ U_BUCK3 VIN ↔ U_BUCK3 EN ↔ C_B3_IN 22 µF ↔ C_B3_IN_HF ↔ R3a ↔ R_SENSE_TOP | Energiebus. **Kein Boost, kein LDO** hängt mehr daran; die Pumpen hängen an +5V |
| **UV_REF** | **R3a 200 kΩ** (von VBAT) ↔ Knoten ↔ **R3b 200 kΩ** → GND · Knoten ↔ **U7 Pin 3 (VDD)** | Versorgung des Wächters = **VBAT/2**. Auslösung bei VDD = 3,08 V ⇒ **6,16 V Pack** (Offset durch Iq 150 nA ≈ +30 mV ⇒ ~6,19 V) |
| **RESET_UV** | **U7 Pin 2 (RESET)** ↔ **U_BUCK5 Pin 4 (EN)** ↔ D3 Kathode ↔ D8 Kathode ↔ R_CLAMP1/R_CLAMP2 | aktiv-low; **schaltet die 5-V-Schiene wirklich ab** (Buck: EN low ⇒ Ausgang 0 V, kein Diodenpfad wie beim alten Boost) **und** klemmt beide Pumpengates |
| **GATE / GATE2** | IO2 → R1 1 kΩ → Q1 Gate ↔ R2 47 kΩ → GND · IO22 → R_GATE2 1 kΩ → Q3 Gate ↔ R_GATE2_PD 47 kΩ → GND | Pumpensteuerung (PWM-fähig) |
| **KLAMP1 / KLAMP2** | **R_CLAMP1 10 kΩ** (vom Gate-Knoten) ↔ **D3 Anode → Kathode RESET_UV** · **R_CLAMP2 10 kΩ** ↔ **D8 Anode → Kathode RESET_UV** | **korrigiert 16.09.2026:** Serienkette Gate → 10 kΩ → Diode → RESET (vorher war R_CLAMPx **parallel** zur Diode und der Knoten lag nicht am Gate ⇒ Klemmung wirkungslos, §13.4) |
| **VBAT_SENSE** | **R_SENSE_TOP 200 kΩ** (von VBAT) ↔ Knoten ↔ **R_SENSE_BOT 68 kΩ** → GND · Knoten ↔ U1 **Pin 13 (IO1, ADC1_CH1)** ↔ C10 100 nF → GND | **neu 1 : 3,94** (vorher 1:2): 8,4 V → **2,13 V**, 6,16 V → **1,56 V** am ADC. Teilerstrom 31,5 µA. Verhältnis bewusst nicht exakt 1:4, damit beide Widerstände Basic-Positionen bleiben (§3.3) |

### 2.3 5-V-Schiene und Pumpen (Wandler gewechselt)

| Netz | Verbindungen | Zweck |
|---|---|---|
| **LX_5V** | U_BUCK5 Pin 6 (LX) ↔ **L_BUCK5 4,7 µH** ↔ C_B5_BST Pin 2 | Schaltknoten des 5-V-Bucks |
| **BST_5V** | U_BUCK5 Pin 1 (BS) ↔ **C_B5_BST 100 nF** | Bootstrap |
| **FB_5V** | U_BUCK5 Pin 3 (FB) ↔ **R_FB5_TOP 110 kΩ** (von +5V) ↔ **R_FB5_BOT 15 kΩ** → GND | V_out = 0,6 V × (1 + 75/10) = **5,10 V** |
| **+5V** | **L_BUCK5 Pin 2** ↔ C_B5_OUT 22 µF ↔ C_B5_OUT_HF 100 nF ↔ **C3 100 µF Elko** ↔ R_FB5_TOP ↔ **J4 Pin 1**, **J16 Pin 1**, **J17 Pin 1** ↔ D1 Kathode ↔ D7 Kathode ↔ C11 Pin 2 ↔ C20 Pin 2 | 5-V-Schiene: **beide Pumpen**, der neue 5-V-Sensorausgang und der Pumpenpuffer |
| **PUMP_N / PUMP2_N** | Q1 Drain ↔ J4 Pin 2 ↔ D1 Anode ↔ C11 · Q3 Drain ↔ J16 Pin 2 ↔ D7 Anode ↔ C20 | geschaltete Pumpenmasse (Low-Side, unverändert) |

### 2.4 3,3-V-Schiene (Logik)

| Netz | Verbindungen | Zweck |
|---|---|---|
| **LX_3V3 / BST_3V3** | U_BUCK3 Pin 5 (SW) ↔ **L_BUCK3 4,7 µH** ↔ C_B3_BST · Pin 6 (BST) ↔ C_B3_BST 100 nF | Schaltknoten + Bootstrap |
| **FB_3V3** | U_BUCK3 Pin 1 (FB) ↔ **R_FB3_TOP 100 kΩ** (von +3V3) ↔ **R_FB3_BOT 31,6 kΩ** → GND | V_out = 0,8 V × (1 + 100/31,6) = **3,33 V** |
| **+3V3** | **L_BUCK3 Pin 2** ↔ C_B3_OUT 22 µF ↔ C_B3_OUT_HF 100 nF ↔ **U1 Pin 3** ↔ C1a/C1b/C2/C13 ↔ R_EN, R_BOOT, R_GPIO8, R_BTN ↔ **Q2 Source** ↔ TP5 | Logikversorgung. **Kein LDO mehr** — die Rail entsteht direkt als Buck-Ausgang |

### 2.5 Unveränderte Netze

`GND` · `EN` · `BOOT` · `GPIO8_STRAP` · `PUMP_EN` · `GATE` · `PUMP_N` · `PUMP2_EN` · `GATE2` · `PUMP2_N` ·
`SENSOR_RAW` · `SENSOR_AOUT` · `SENSOR_PWR` · `LIGHT_RAW` · `LIGHT_AOUT` · `SDA` / `SDA_MCU` · `SCL` / `SCL_MCU` ·
`VCC_EXT` · `EXT_EN` · `SPARE_AIN[_RAW]` · `SPARE_IO15[_RAW]` · `SPARE_IO16` · `SPARE_IO17` ·
`SPARE_IO21[_RAW]` · `SPARE_IO23[_RAW]` · `USB_DM` · `USB_DP` · `LED_STAT[_A]` · `LED_TANK[_A]` · `BTN` ·
`UART_TX` · `UART_RX` · `UART_TP`

**Entfallene Netze:** `PROG` (MCP73831-Ladestrom), `SW_BOOST` / `FB_5V`-Boost (MT3608) — der Name `FB_5V`
wird jetzt vom Buck-Feedback benutzt.

---
## 3. Bauteile mit Werten und Begründung

### 3.1 ICs, Wandler und Halbleiter

| Pos | Bauteil | Wert | LCSC | Warum / Quelle |
|---|---|---|---|---|
| **U_CHG** | **IP2326** (Injoinic) | 2S/3S-Boost-Lader, QFN-24 4×4 mm | `C2832094` | **neu:** 5 V → 8,4 V bei bis zu 15 W Eingang, 94 % Wirkungsgrad (5 V→8 V/1 A), 500 kHz, Leistungs-MOSFETs integriert. **VSET offen ⇒ 8,4 V** (die Variante `IP2326_8V8` lädt auf **8,8 V** → für Li-Ion unzulässig, **nicht** verwenden). **Ladestrom ICHG = 90000/R_ISET = 0,90 A** (±10 %). Trickle 50 mA (<3,7 V), 100 mA (3,7–6 V), CV-Ende: Stopp bei <200 mA. **Kein Power-Path** (Volltext-Grep beider Datenblatt-Versionen: 0 Treffer). Balancing integriert (Pins 23/24) — hier **unbeschaltet**, weil der Pack ein eigenes BMS hat (§6.3) |
| **U_BUCK5** | **SY8113B ADC** (Silergy) | 3 A, 4,5–18 V, synchron, 500 kHz, TSOT-23-6 | `C78989` | **neu:** erzeugt die **5-V-Schiene** für beide Pumpen aus VBAT. V_REF 0,6 V ±1,5 % ⇒ V_out = 0,6 × (1 + 75/10) = **5,10 V**. Iq 100 µA, Shutdown 5–10 µA, EN-Schwelle 1,5 V, Stromgrenze 3 A (Valley) / 6 A (Peak), Sanftanlauf 800 µs intern. **Damit liegt der 3-A-Pumpenanlauf innerhalb der Nennlast** (beim alten MT3608-Boost war er es nicht) |
| **U_BUCK3** | **AP63203 WU-7** (Diodes) | 2 A, 3,8–32 V, synchron, 1,1 MHz, TSOT-26 | `C780769` | **neu:** erzeugt **+3V3** direkt aus VBAT (ersetzt den ME6211-LDO). V_REF 0,8 V ±1 % ⇒ V_out = 0,8 × (1 + 47/15) = **3,31 V**. **Iq 22 µA** (niedrigster Wert der geprüften Auswahl), Präzisions-EN (an VIN gelegt), 89 °C/W. Vorteil gegenüber dem LDO: bei 8,4 V → 3,3 V **88 %** statt 66 %, keine Verlustwärme bei den 382-mA-TX-Spitzen |
| **U7** | **TPS3839G33DBZR** (TI) | Unterspannungswächter, **3,08 V**, SOT-23-3 | `C485802` | **neu (ersetzt MAX809TEUR+T):** gleiche Schwelle 3,08 V (V_IT 3,003–3,126 V, Hysterese 31 mV), aber **Iq 150 nA statt 12 µA** — nötig, weil er jetzt an einem 200 kΩ-Teiler hängt (Iq × R_top = Offset; bei 12 µA wären das 2,4 V Fehler). **Push-Pull-Ausgang** (treibt den Buck-EN direkt, kein Pull-up nötig), V_DD 0,9–6,5 V, **200 ms Reset-Delay** nach dem Anlaufen, Ausgangsstrom 2 mA bei V_OL ≤ 0,4 V |
| **U1** | ESP32-C6-MINI-1 | Modul | `C5736265` | MCU (unverändert). TX-Peak **382 mA**, Deep-Sleep 7 µA |
| **U6** | USBLC6-2SC6 | ESD, SOT-23-6 | `C7519` | USB-Datenleitungen (unverändert) |
| **Q1** | AO3400A | N-MOSFET SOT-23 | `C20917` | Dosierpumpe (Low-Side, IO2) — unverändert |
| **Q_PUMP2** | AO3400A | N-MOSFET SOT-23 | `C20917` | Sauerstoffpumpe (Low-Side, IO22) — unverändert |
| **Q2** | AO3401A | P-MOSFET SOT-23 | `C15127` | Load-Switch VCC_EXT (unverändert) |
| **D1** | 1N5819WS | 40 V / 1 A, SOD-323 | `C191023` | Freilauf Dosierpumpe an **+5V** |
| **D_FLY2** | 1N5819WS | 40 V / 1 A, SOD-323 | `C191023` | Freilauf Sauerstoffpumpe an **+5V** |
| **D3** | 1N5819WS | SOD-323 | `C191023` | Klemmzweig Dosierpumpe (**Kathode an RESET_UV**) |
| **D8** | 1N5819WS | SOD-323 | `C191023` | Klemmzweig Sauerstoffpumpe |
| **D2** | LED grün 525 nm | 0805 | `C2297` | Status-LED (IO14) |
| **D5** | LED rot | 0805 | `C84256` | Tank-leer (IO7) |
| **D_LEDCHG** | LED rot | 0805 | `C84256` | Ladestatus — **jetzt am LED-Pin des IP2326** (der Pin ist eine Senke; leuchtet beim Laden, aus bei Voll, **blinkt bei Fehler**) |
| **L_CHG** | **2,2 µH**, 4,6 × 4,1 mm | Isat 5,0 A · Irms 3,0 A · DCR 58 mΩ | `C142096` | Boost-Induktivität. Datenblatt fordert 2,2 µH @ 500 kHz, Isat/Idc > 5 A — **Isat 5,0 A erfüllt**; DCR 58 mΩ liegt über den empfohlenen 20 mΩ ⇒ 0,13 W Verlust bei 1,5 A (~1,5 %), bewusst akzeptiert (die <20-mΩ-Typen sind ≥ 7 × 7 mm) |
| **L_BUCK5** | **4,7 µH**, 6 × 6 mm | Isat 4,0 A · DCR 31 mΩ | `C105660` | Buck-Induktivität 5 V: Rippel ΔI = 0,86 A (29 %), Spitzenstrom bei 3 A Last **3,43 A < Isat 4,0 A**. Bei max. Eingang liegt der DCR-Verlust bei 0,28 W |
| **L_BUCK3** | **4,7 µH**, 6 × 6 mm | Isat 4,0 A · DCR 31 mΩ | `C105660` | **gleicher Typ** wie L_BUCK5 (Menge 2, eine BOM-Zeile, ein Footprint). Bei 1,1 MHz ist der Rippel nur 0,35 A (18 %), Last real ≤ 0,5 A ⇒ 8× Reserve |
| ~~U3~~ | ~~MCP73831T-2ACI/OT~~ | — | — | **entfällt:** 1S-Lader, kann 2S nicht laden |
| ~~U4~~ | ~~ME6211C33M5G~~ | — | — | **entfällt:** LDO durch Buck ersetzt. ⚠️ Sein V_IN-Maximum ist **6,0 V** — er hätte an 8,4 V ohnehin nicht betrieben werden dürfen |
| ~~U8~~ | ~~MT3608~~ | — | — | **entfällt:** Aufwärtswandler nicht mehr nötig (2S liegt über 5 V) |
| ~~L1 (22 µH)~~ | ~~YNR6045~~ | — | — | **entfällt** mit dem Boost. ⚠️ **Achtung:** der alte L1 hatte nur **2,05 A** Sättigungsstrom |
| ~~D6~~ | ~~SS34~~ | — | — | **entfällt** (Boost-Diode) |
| ~~R31 75 k / R32 10 k~~ | — | — | — | **entfallen** (Boost-Feedback auf 5,10 V) |
| ~~R37 47 k~~ | — | — | — | **entfällt:** Boost-EN-Pull-up; der TPS3839 treibt den Buck-EN push-pull |
| ~~R13 / R_PROG~~ | — | — | — | **entfällt** (Ladestromprogrammierung des MCP73831) |
| ~~D7~~ | → heißt jetzt **D_FLY2** | — | — | Umbenennung nur zur Klarheit (funktionaler Name wie Q_PUMP2) |

### 3.2 Kondensatoren

| Pos | Wert | Typ | Wofür | Quelle |
|---|---|---|---|---|
| **C_CHG_IN** | **10 µF / 25 V** | 0805 | Eingangspuffer des Laders | IP2326-Datenblatt BOM: „10 µF/25 V, **Spannungsfestigkeit > 16 V**, muss Keramik sein" (C1) |
| **C_CHG_VIN** | **10 µF / 25 V** | 0805 | direkt am VIN-Pin (Pin 13) | dito (C3) |
| **C_CHG_OUT** | **10 µF / 25 V** | 0805 | Ausgang/Batterieknoten | dito (C6/C7) |
| **C_VSYS_A, C_VSYS_B** | 2 × **22 µF / 25 V** | 0805 | **direkt an den VSYS-Pins** (19/20) | IP2326-Datenblatt: „2× 22 µF Keramik direkt am Pin platzieren" (C4/C5) |
| **C_BST_CHG** | 100 nF | 0805 | Bootstrap **zwischen BST (14) und LX** | IP2326-Datenblatt: 0,1 µF nahe BST/LX |
| **C_B5_IN** | 22 µF | 0805 | Buck-Eingang 5 V | SY8113B: „X5R oder besser, > 22 µF" (unverändert C45783) |
| **C_B5_IN_HF** | 100 nF | 0805 | HF-Stützung am Buck-Eingang | Standardpraxis, gleicher Typ wie alle 100-nF-Positionen |
| **C_B5_OUT** | 22 µF | 0805 | 5-V-Ausgang | Buck-Ausgangsfilter |
| **C_B5_OUT_HF** | 100 nF | 0805 | HF am 5-V-Ausgang | dämpft den 500-kHz-Schaltknoten |
| **C_B5_BST** | 100 nF | 0805 | Bootstrap 5-V-Buck | SY8113B: 0,1 µF zwischen BS und LX |
| **C3** | **100 µF / 16 V (Elko)** | SMD D6,3×5,4 | **Pumpenpuffer — von VBAT nach +5V verschoben** | Polster für die Pulsströme der Pumpen auf der Schiene, die sie tatsächlich speist. ⚠️ Polarität im Layout prüfen |
| **C_B3_IN** | 22 µF | 0805 | Buck-Eingang 3,3 V | AP63203-Typenschaltung |
| **C_B3_IN_HF** | 100 nF | 0805 | HF-Stützung am Buck-Eingang | Standardpraxis |
| **C_B3_OUT** | 22 µF | 0805 | 3,3-V-Ausgang | AP63203-Typenschaltung |
| **C_B3_OUT_HF** | 100 nF | 0805 | HF am 3,3-V-Ausgang | für den Modul-Bulk-Pfad (C2) vorgeschaltet |
| **C_B3_BST** | 100 nF | 0805 | Bootstrap 3,3-V-Buck | AP63203: „100 nF from SW to BST" |
| **C12** | 100 nF | 0805 | Decoupling des Wächters — **jetzt an UV_REF** | TPS3839-Messbedingung nennt C1 = 0,1 µF; der MAX809 hatte dieselbe Bestückung |
| C1a, C1b, C13 | 3 × 100 nF | 0805 | Decoupling am Modul | Espressif: 22 µF + 2 × 0,1 µF (unverändert) |
| C2 | 22 µF / 25 V | 0805 | Bulk am Modul-3V3 | unverändert |
| C4 | 1 µF | 0603 | EN-RC-Glied | unverändert (Espressif: 10 k + 1 µF) |
| C9, C10 | 2 × 100 nF | 0805 | ADC-Filter Feuchte / Packspannung | Espressif-ADC-Empfehlung |
| C11 | 100 nF | 0805 | EMI **an den Pumpenklemmen** J4 | unverändert (Minus ist über Q1 geschaltet) |
| C_PUMP2_EMI | 100 nF | 0805 | EMI an den Klemmen J16 | unverändert (über Q3 geschaltet) |
| C_LIGHT | 100 nF | 0805 | ADC-Filter Licht | wie bisher |
| C_SPARE | 100 nF | 0805 | ADC-Filter Reserve-Analog | wie bisher |
| C_BTN | 100 nF | 0805 | Taster-Entprellung | wie bisher |
| ~~C5~~ | ~~10 µF~~ | — | entfällt mit dem LDO | — |
| ~~C6~~ | ~~1 µF~~ | — | entfällt mit dem LDO | — |
| ~~C17/C18/C19~~ | — | — | entfallen mit dem Boost (durch C_B5_* ersetzt) | — |
| ~~C7/C8 (4,7 µF)~~ | — | — | ersetzt durch 10 µF (C_CHG_IN/C_CHG_OUT, Datenblattwert) | — |

### 3.3 Widerstände

| Pos | Wert | Wofür | Quelle |
|---|---|---|---|
| **R_ISET** | **100 kΩ 1 %** | Ladestrom des IP2326 | Datenblatt: ICHG = 90000/R_ISET ⇒ **0,90 A**; 1 %-Genauigkeit gefordert. ISET darf **nicht** offen bleiben |
| **R_NTC** | **51 kΩ** | NTC-Funktion stilllegen | Datenblatt: „nicht benötigt ⇒ 51 kΩ nach GND" (20 µA × 51 k = 1,02 V = Normalbereich) |
| **R_UVSET** | **68 kΩ** | Eingangs-Unterspannungsschwelle | Datenblatt-Tabelle: 68 k ⇒ **4,35 V** (Standard 4,65 V). Ziel: die Eingangsregelschleife soll bei einem dünnen Kabel erst spät den Ladestrom senken |
| **R_EN_CHG** | **100 kΩ** | Pull-up des Lader-EN nach VBUS | Datenblatt: EN ≥ 1,4 V = an. Damit lädt das Gerät **ohne** Firmware (kein GPIO nötig) |
| **R_VIN_CHG** | **0,5 Ω** | Filter zum VIN-Pin | Datenblatt-Applikationsbild (R1). **Kein** Shunt — der Ladestrom wird im IC gemessen (0,5 Ω bei 1,8 A wären 1,6 W in 0805) |
| **R_LEDCHG** | 1 kΩ | Vorwiderstand der Lade-LED | ~2,7 mA an 5 V, LED-Pin kann max. 5 mA. Gleicher Basic-Typ wie R_TANK |
| **R3a** | **200 kΩ** | Wächter-Teiler (oberer Zweig, von VBAT) | C17539 (Basic) — bewusst **getrennte Zeilen** für R3a/R3b, damit eine Wertänderung an genau einem der beiden den Teiler verschiebt (Mutationstest der Verhältnis-Prüfung) |
| **R3b** | **200 kΩ** | Wächter-Teiler (unterer Zweig, nach GND) | Schwelle 3,08 V ⇒ Auslösung bei **6,16 V** Pack (= 3,08 V/Zelle). Teilerstrom 21 µA. Offset durch Iq 150 nA: +30 mV |
| **R_SENSE_TOP** | **200 kΩ** | Packspannungsmessung (oberer Zweig) | **neu:** 8,4 V → **2,13 V**, 6,16 V → 1,56 V — passt in den 12-dB-Bereich (0–3300 mV) mit Reserve. Teilerstrom 31,5 µA. **Verhältnis 1 : 3,94** statt exakt 1:4, dafür bleiben **beide Widerstände Basic-Positionen** |
| **R_SENSE_BOT** | **68 kΩ** | Packspannungsmessung (unterer Zweig) | gleicher Basic-Typ wie R_UVSET |
| **R_FB5_TOP** | **75 kΩ** | Feedback 5-V-Buck (oben) | V_out = 0,6 V × (1 + 75/10) = **5,10 V** — derselbe Basic-Wert wie beim alten Boost (C17819) |
| **R_FB5_BOT** | **10 kΩ** | Feedback 5-V-Buck (unten) | C17414 (Basic) |
| **R_FB3_TOP** | **47 kΩ** | Feedback 3,3-V-Buck (oben) | C17713 (Basic) |
| **R_FB3_BOT** | **15 kΩ** | Feedback 3,3-V-Buck (unten) | V_out = 0,8 V × (1 + 47/15) = **3,31 V** (0,3 % unter 3,3 V — weit innerhalb 3,0–3,6 V des Moduls) |
| **R_CLAMP1, R_CLAMP2** | 2 × **10 kΩ** | Serienwiderstand **im** Klemmzweig | begrenzt den Sinkstrom in U7 auf **0,29 mA** (Ausgang darf 2 mA). **Korrigiert:** liegt in Reihe mit D3/D8, vorher parallel (§13.4) |
| **R1, R_GATE2** | 2 × 1 kΩ | Gate-Serie beider Pumpen | schnelle PWM-Flanken; identisch für beide Kanäle |
| **R2, R_GATE2_PD** | 2 × 47 kΩ | Gate-Pulldown | hält die Pumpen bei totem MCU aus; Ansteuerpegel 3,3 V × 47/48 = 3,23 V |
| R4 | 220 Ω | Status-LED grün (Vf 2,85 V) | 3,3 V − 2,85 V = 0,45 V ⇒ 1,4–2,7 mA |
| R_TANK | 1 kΩ | Tank-LED | ~1,3 mA |
| R6, R_LIGHT_S, R_SDA_S, R_SCL_S, R_SPARE_AIN, R_SPARE_IO15, R_SPARE_IO16, R_SPARE_IO17, R_SPARE_IO21, R_SPARE_IO23 | 10 × 1 kΩ | Serienschutz aller Steckerleitungen | Fehlerstrom in einen Pin ≤ 3,3 mA |
| R_LIGHT | 10 kΩ | Lastwiderstand Lichtsensor | offener Stecker ⇒ 0 V ⇒ „dunkel" |
| R_EN, R_BOOT, R_GPIO8, R_BTN | 4 × 10 kΩ | Pull-ups (EN, GPIO9, GPIO8, Taster) | Espressif + eigene Auslegung |
| R_SDA_PU, R_SCL_PU | 2 × 4,7 kΩ | I²C-Pull-ups **an VCC_EXT** | im ausgeschalteten Zustand kein Busstrom |
| R_GATE | 47 kΩ | Gate-Pull-up des Load-Switch | Fail-safe: ohne GPIO ist VCC_EXT aus |
| R5a, R5b | 2 × 5,1 kΩ | USB-C CC1/CC2 nach GND | USB-C-Vorgabe |
| R_UART | 499 Ω | TXD0-Serie | Espressif-Empfehlung, **DNP** |
| ~~R_PROG (3,9 k)~~ | — | entfällt mit dem MCP73831 | — |
| ~~R37 (47 k)~~ | — | entfällt: EN-Pull-up des Boosts | — |
| ~~R31/R32 (75 k/10 k)~~ | — | entfallen: Boost-Feedback | — |

### 3.4 Steckverbinder und Schalter

| Pos | Bauteil | LCSC | Anschluss |
|---|---|---|---|
| **J1** | JST PH 2,0 mm, 2-pol, aufrecht | `C160352` | **Akku = 2S-Pack** (Pin 1 = +, Pin 2 = −). ⚠️ **Pflicht: Pack mit BMS/Balancer** (§6.3) |
| J2 | JST-XH 2,5 mm, 3-pol, aufrecht | `C493416` | Feuchtesensor: 1 = GND · 2 = SENSOR_PWR · 3 = SENSOR_RAW |
| J4 | JST-XH 2,5 mm, 2-pol, aufrecht | `C158012` | Dosierpumpe: 1 = **+5V** · 2 = PUMP_N |
| J16 | JST-XH 2,5 mm, 2-pol, aufrecht | `C158012` | Sauerstoffpumpe: 1 = **+5V** · 2 = PUMP2_N |
| **J17** | JST-XH 2,5 mm, 2-pol, aufrecht | `C158012` | **neu: 5-V-Ausgang für Sensorik** — 1 = **+5V** · 2 = GND. Gleicher Steckertyp wie J4/J16 (eine Crimpzange, eine BOM-Zeile mit Menge 3) |
| J5 | USB-C 16-pol | `C165948` | Laden **und** Programmieren (USB-Serial-JTAG auf IO12/13) |
| J6 | 2 Lötpads Ø 1,0 mm, Raster 2,54 mm | — | externer Taster (keine Bestückung) |
| J7, J9–J13, J15 | Stiftleiste 1×3, 2,54 mm | `C2937625` | GND–VCC_EXT–SIG (VCC in der Mitte) |
| J8 | Stiftleiste 1×4, 2,54 mm | `C2691448` | GND–VCC_EXT–SDA–SCL |
| SW1, SW2 | Taster 5,1 × 5,1 mm | `C318884` | Reset / Boot |

---

## 4. Modul-Pinbelegung (ESP32-C6-MINI-1, unverändert)

| Modulpin | Name | Verwendung hier |
|---|---|---|
| 3 | 3V3 | +3V3 (jetzt aus dem AP63203-Buck) |
| 5 | IO2 | PUMP_EN |
| 6 | IO3 | SENSOR_PWR |
| 8 | EN | Reset-RC + SW1 |
| 9 | IO4 | LIGHT_AOUT (ADC1_CH4) |
| 12 | IO0 | SENSOR_AOUT (ADC1_CH0) |
| 13 | IO1 | **VBAT_SENSE (jetzt 1:3,94)** |
| 15 | IO6 | BTN (LP_GPIO6, weckt) |
| 16 | IO7 | LED_TANK (LP_GPIO7) |
| 17 / 18 | IO12 / IO13 | USB_D− / USB_D+ |
| 19 | IO14 | LED_STAT |
| 20, 24, 25, 26, 27, 28, 29, 30, 31 | IO15, IO18, IO19, IO20, IO21, IO22, IO23, RXD0, TXD0 | wie bisher (Reserve/I²C/EXT_EN/O2-Pumpe/UART) |
| 22, 23 | IO8, IO9 | Strapping-Pull-ups + Boot-Taster |
| 10 | IO5 | SPARE_AIN (J9) |
| 1, 2, 11, 14, 36–53 | GND | Masse |

⚠️ **Firmware-Änderung (nicht Hardware):** Der ADC-Faktor der Packspannung ist jetzt **4** statt 2
(8,4 V ⇒ 2,10 V). Die Schwellen aus `bom_entscheidung.md` §4b sind auf Packspannung umzurechnen
(Messauftrag §6.7).

---

## 5. Pinbelegungen der ICs — Stand der Belege

| Bauteil | Pinbelegung | Belegstatus |
|---|---|---|
| **IP2326 (QFN-24 + EPAD)** | 1 DM · 2 DP · 3 VSET · 4 NTC · 5 BAT_STAT · 6 LED · 7 TIME_SET · 8 VIN_UVSET · 9 VIN_OVSET · 10 CON_SEL · 11 ISET · 12 EN · 13 VIN · 14 BST · **15/16/17 LX** · 18 PGND · **19/20 VSYS** · **21/22 VOUT** · 23 VBATM · 24 VBAT_GND · EPAD GND | ✅ **als Text aus der Pin-Tabelle** des Datenblatts V1.11 §4 (S. 2) extrahiert (17-seitiges PDF, Textlayer vorhanden) |
| **SY8113B (TSOT-23-6)** | 1 BS · 2 GND · 3 FB · 4 EN · 5 IN · 6 LX | ✅ Datenblatttext (AN_SY8113B, „Pinout/Pin Description", S. 2) |
| **AP63203 (TSOT-26)** | 1 FB · 2 EN · 3 VIN · 4 GND · 5 SW · 6 BST | ⚠️ Die Pin-**Tabelle** des Datenblatts (DS41326) liegt nur als Bild vor; die Reihenfolge stammt aus dem beschrifteten Pinout-Block (Text „1 FB 2 EN 3 VIN 4 GND 5 SW 6 BST") → **beim Footprint gegenprüfen** |
| **TPS3839 (SOT-23-3)** | 1 GND · 2 RESET · 3 VDD | ✅ Datenblatttext (SBVS193D §6 Pin Functions: „GND 1 · RESET 2 · VDD 3") |
| **USBLC6-2SC6** | 1 = I/O1 · 2 = GND · 3 = I/O2 · 4 = I/O2 · 5 = VBUS · 6 = I/O1 | ✅ Datenblatttext (unverändert) |
| **AO3400A / AO3401A** | 1 = Gate · 2 = Source · 3 = Drain | ⚠️ wie bisher: Standardbelegung, im Footprint gegenprüfen |
| ~~MCP73831 / ME6211 / MAX809~~ | — | entfallen. **Hinweis für die Nachwelt:** der ME6211 hat V_IN,max = 6,0 V — genau deshalb ist der Umbau auf 2S nur *mit* einem anderen Regler zulässig |

---

## 6. Auslegungsnotizen und offene Punkte

### 6.1 Laden (neu dimensioniert)

- **Ladestrom 0,90 A** (R_ISET 100 kΩ) ⇒ bei 8,4 V sind das 7,6 W Ausgang, bei 94 % Wirkungsgrad
  ≈ **1,6 A Eingangsstrom** aus 5 V, plus Systemlast (max. 0,6 A, wenn beide Pumpen laufen).
  ⇒ **Es braucht ein 5-V-Netzteil mit ≥ 2,5 A** (USB-C-Netzteile mit ≥ 3 A sind üblich).
- Der IP2326 hat eine **Eingangsregelschleife**: sinkt V_USB unter die per R_UVSET gesetzten 4,35 V,
  reduziert er selbsttätig den Ladestrom („adaptiver Adapter-Schutz") — ein schwaches Netzteil wird
  also nicht „abgerissen", das Laden dauert nur länger.
- **Kein Power-Path** (im Datenblatt beider Versionen nicht vorhanden): Während des Ladens kann
  das System weiterlaufen, weil der Akkuknoten geladen wird. Betriebsregel bleibt wie in §12.3:
  **beim Pumpen möglichst nicht laden** (der Lader deckt die Last nicht, sondern reduziert sie höchstens).
- **Kein Fast-Charge-Request:** DM/DP bleiben offen, weil diese Leitungen dem ESP32 gehören
  (USB-Serial-JTAG auf IO12/13). Das ist datenblattkonform („wenn die Anforderung scheitert, wird
  dauerhaft mit 5 V geladen"); die 15-W-Fähigkeit des ICs wird damit **nicht** ausgenutzt.
- **Ladezeit:** 0,6 C bei 1000 mAh-Pack ≈ 1,7 h, bei 2000 mAh ≈ 3,3 h (plus CV-Phase).

### 6.2 Ruhestrom (neu gerechnet)

| Posten | vorher (1S) | jetzt (2S) |
|---|---|---|
| Buck 5 V (SY8113B, Iq) | — | **100 µA** |
| Buck 3,3 V (AP63203, Iq) | — | **22 µA** |
| LDO (ME6211) | 40 µA | — (entfallen) |
| Unterspannungswächter | 12 µA (MAX809) | **0,15 µA** (TPS3839) |
| Teiler (Wächter 1:2 + ADC) | 10,5 µA | **52,4 µA** (21 + 31,4) |
| ESP32-C6 Deep-Sleep | 7 µA | 7 µA |
| **Summe** | **≈ 70 µA** (1,7 mAh/Tag) | **≈ 182 µA** (4,4 mAh/Tag = **0,29 %/Tag** bei 1500 mAh) |

Bei 1500 mAh stehen 4,4 mAh/Tag = **0,29 %/Tag** den 1,7 mAh/Tag = 0,11 %/Tag des 1S-Stands gegenüber —
die Verdopplung des Ruhestroms kostet also **nichts** an Laufzeit, weil der Pack doppelt so groß ist.
**Sparoption (V2):** den 5-V-Buck per GPIO nur während des Pumpens einschalten (spart 100 µA,
erfordert dann aber eine Einschaltverzögerung in der Firmware, weil der Buck nach dem EN 800 µs
Sanftanlauf braucht, plus die 200 ms des Wächters beim Kaltstart).

### 6.3 ⚠️ Der Akku-Pack **muss** eine Schutzplatine (PCM/BMS) haben — Balancing ist die zweite Ebene

**Pflicht (Sicherheit):** Der Pack braucht ein **PCM/BMS mit Zellschutz** (Überladung **pro Zelle**,
Tiefentladung, Überstrom, Kurzschluss). Das ist bei 2S kein Luxus: der Lader lädt nur die
**Reihenschaltung** auf 8,4 V und kann eine einzelne Zelle nicht sehen.

**Was ohne Balancing wirklich passiert (präzisiert 16.09.2026):** Solange der Pack ein PCM hat, ist
die Folge von Zell-Drift **kein Brandrisiko**, sondern **Kapazitätsverlust und schnelleres Altern**:
die schwächere Zelle erreicht ihre Ladeschlussspannung nicht mehr, die stärkere läuft in die
PCM-Abschaltung (typisch 4,25–4,3 V/Zelle) und beendet die Ladung früher. Gefährlich wird es **erst
ohne jede Zellschutzschaltung** (dann kann eine Zelle über 4,3 V kommen).
→ Die frühere Formulierung „ohne Balancing besteht ein Brandrisiko" war zu scharf und ist hiermit ersetzt.

**Balancing — drei Wege, bewertet:**

| Weg | Aufwand | Bewertung |
|---|---|---|
| **a) Der Pack balanciert selbst** (BMS mit Balancer-Funktion) | keiner | Wunschfall. ⚠️ Alle am 16.09.2026 geprüften 2S-Packs aus dem deutschen Handel (Keeppower 2×18500 2000 mAh 10,90 € / 2×18650 3400 mAh 14,90 €, akkuteile.de, Seiko-PCM) **dokumentieren kein Balancing** — nur Schutz. Vor dem Kauf beim Händler erfragen (`research/bom-check/10_2s-akku-quellen.md`) |
| **b) 2 Einzelzellen + 2S-BMS-Board mit Balancer** | 1 Steckverbinder + 1 Widerstand + 2 Kondensatoren, Mittelabgriff herausführen | technisch die beste Lösung: unser IP2326 kann dann mitbalancieren (Pins 23/24). Der Mittelabgriff ist bei einem BMS-Board zugänglich, bei einem verschweißten Fertigpack nicht |
| **c) Nichts tun** | keiner | zulässig, **weil** der PCM die Zellen schützt — kostet aber nutzbare Kapazität und Lebensdauer |

**Wenn Balancing gewünscht wird (Weg b), ändert sich in dieser Schaltung:**
- **VBATM (Pin 23)** ← **R_CB 100 Ω 1206** ← **Mittelabgriff des Packs** (Datenblatt: I_CB = V_CB/R_CB, < 40 mA)
- **VBAT_GND (Pin 24)** ← **BAT−** des Packs; **2 × 100 nF** als Filter an beiden Pins
- J1 wird **3-polig** (BAT− / MID / BAT+, z. B. JST-XH-3P `C493416`, dasselbe Teil wie J2)
- Aktivierung ab `V_CBON = 4,1 V` (Standardtyp); Balancing endet, wenn beide Zellen darüber liegen
- ⚠️ Diese Verdrahtung liegt im Datenblatt **nur als Bild** vor (图5): BAT+ → VOUT, Mittelabgriff →
  R_CB → Pin 23, BAT− → Pin 24. **Vor dem Layout am Bild gegenprüfen** (Belegstatus wie in §5)

**Pack-Kandidaten (geprüft 16.09.2026, Links in `../research/bom-check/10_2s-akku-quellen.md`):**
Keeppower 2S1P 2×18500 **2000 mAh** (10,90 €, akkuteile.de, 18,5 × 103 mm, 70 g, Seiko-Schutz) oder
2×18650 **3400 mAh** (14,90 €, 18,7 × 134 mm, 100 g). ⚠️ **Mechanik-Folge:** der bisherige 1S-Pouch
war 59 × 37 × 5 mm flach — ein Rundzellenpack ist 18,5 mm dick und ~103 mm lang. Das passt in die
160 mm hohe Wulst, aber **nicht** mehr hinter die Platine → Einbauort in `docs/02`/`cad/params.py`
nachziehen (Auftrag, nicht Teil dieses Schaltplan-Schritts).

### 6.4 Was der Wächter jetzt wirklich abschaltet

Unter 6,16 V Pack: RESET_UV low ⇒ (a) **U_BUCK5 Pin 4 (EN)** sperrt — der Buck-Ausgang ist dann
**wirklich 0 V** (kein Diodenpfad wie beim alten Boost über L1/D6) und (b) D3/D8 klemmen beide
Pumpengates über je 10 kΩ auf ~0,3 V. Die **3,3-V-Schiene bleibt an**, damit der MCU melden und
loggen kann (bewusste Entscheidung, wie in §12.3 dokumentiert). Der Pack entlädt sich im
Wächterzustand weiter mit ~182 µA (beide Buck-Iq + Teiler) — das PCM der Zellen ist die letzte Ebene.

### 6.5 Verpol-, Kurzschluss- und Steckerschutz (unverändert)

Alle Außenstecker bleiben **GND–VCC–SIG** (VCC in der Mitte) mit 1 kΩ in jeder Signalleitung;
J17 (neu) ist eine reine **Ausgangs**-Buchse (5 V/GND) — ein Kurzschluss dort wird durch die
Strombegrenzung des 5-V-Bucks begrenzt. Kein Verpolschutz in Reihe zum Akku (das PCM des Packs
ist der Schutz; mechanische Kodierung durch JST).

### 6.6 Wärme

- SY8113B: 0,6 A Last, R_DS(on) 80/40 mΩ ⇒ < 50 mW Verlust; θ_JA 100 °C/W.
- AP63203: 0,15 A Last ⇒ < 60 mW.
- IP2326: bei 8,4 V/0,9 A ≈ 4 % von 8 W ≈ **0,3 W** im QFN-24 mit EPAD (θ_JA 60 °C/W) ⇒ ~20 K
  Überhöhung — das EPAD muss über Vias an eine Kupferfläche angebunden werden (**Layout-Vorgabe**).
- Der **Elko C3** sitzt jetzt auf +5V (vorher VBAT) — thermisch unkritisch.

### 6.7 Offene Punkte / Messaufträge (Stand 16.09.2026)

1. **Akku-Pack auswählen** (2S, 1500–2500 mAh, mit BMS + Balancing, 2-poliger Ausgang) — Recherche
   liegt vor, Entscheidung offen. Maße müssen in die Wulst passen (`docs/02`).
2. **Eingangsstrom messen** (5-V-Seite bei 0,9 A Ladestrom + Pumpenbetrieb) → entscheidet über die
   Netzteilanforderung (≥ 2,5 A) und ggf. über R_ISET (0,75 A/0,9 A).
3. **VSYS-Verhalten:** im Applikationsbild sind VSYS-Pins nur kapazitiv beschaltet (2 × 22 µF) und
   **nicht** extern mit BAT+ verbunden — so ist es hier umgesetzt. Falls die Messung zeigt, dass der
   Ausgang ohne externe Verbindung nicht hochläuft, VSYS extern auf VBAT legen (Lötbrücke).
4. **Pin-Footprints der 4 neuen ICs** (IP2326 QFN-24 EPAD, SY8113B TSOT-23-6, AP63203 TSOT-26,
   TPS3839 SOT-23-3) vor dem Layout gegen die Datenblatt-Bilder prüfen (§5).
5. **Leerlaufstrom beider Bucks messen** (Akku-Standby) → bestätigt die 182 µA aus §6.2.
6. **Pumpenanlauf ohne Softstart** testen: der 3-A-Anlauf liegt jetzt innerhalb der 3-A-Nennlast —
   die Messung entscheidet, ob der Softstart weiterhin zwingend ist.
7. **Firmware:** ADC-Faktor 4:1, neue Schwellen, Warten auf die 5-V-Schiene nach dem Kaltstart.

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
| **J2** | JST-XH 3P (`C493416`, aufrecht) | GND | SENSOR_PWR | SENSOR_RAW | – | R6 1 kΩ → IO0 (Pin 12) |
| **J7** | Stiftleiste 1×3 (`C2937625`) | GND | SENSOR_PWR | LIGHT_RAW | – | R_LIGHT_S 1 kΩ → IO4 (Pin 9) |
| **J8** | Stiftleiste 1×4 (`C2691448`) | GND | VCC_EXT | SDA | SCL | R_SDA_S/R_SCL_S 1 kΩ → IO18/IO19 (Pin 24/25) |
| **J9** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_AIN_RAW | – | R_SPARE_AIN 1 kΩ → IO5 (Pin 10) |
| **J10** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO15_RAW | – | R_SPARE_IO15 1 kΩ → IO15 (Pin 20) |
| **J11** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO16 | – | R_SPARE_IO16 1 kΩ → IO16/TXD0 (Pin 31) |
| **J12** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO17 | – | R_SPARE_IO17 1 kΩ → IO17/RXD0 (Pin 30) |
| **J13** | Stiftleiste 1×3 (`C2937625`) | GND | VCC_EXT | SPARE_IO21_RAW | – | R_SPARE_IO21 1 kΩ → IO21 (Pin 27) |
| ~~J14~~ | **entfällt seit 15.09.2026** | – | – | – | – | IO22 ist **PUMP2_EN** (Sauerstoffpumpe) → Stecker **J16**; die Reserve-Funktion ist gestrichen |
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
| J7 LIGHT_RAW | R_LIGHT_S | *(J14 entfällt)* | – |
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

**R_SDA_PU und R_SCL_PU (je 4,7 kΩ, Revision 15.09.2026)** hängen an **VCC_EXT**, nicht an +3V3. Ist VCC_EXT aus,
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

## 10. Sauerstoffpumpe + 5-V-Boost (Historie, 15.09.2026)

> ⚠️ **Abgelöst am 16.09.2026:** Der Boost U8 (MT3608) ist durch den **5-V-Buck U_BUCK5 (SY8113B)**
> ersetzt (§13). Die Auslegung unten bleibt als Begründung stehen, warum es bis dahin einen Boost
> gab — die darin genannte harte Grenze („Boost kann den 3-A-Anlauf nicht liefern") **gilt nicht mehr**.

### 10.1 Was gefordert war

> „für die Pumpe haben wir ja ein Mosfet, ich brauche noch ein zweites Mosfet + Anschlussmöglichkeit
> und **beide sollen 5 V liefern** — das eine für Dosierpumpe, das andere für eine Sauerstoffpumpe."

Daraus folgen **zwei** Änderungen: ein zweiter, baugleicher Leistungspfad — und eine **5-V-Schiene**,
die es im Akkubetrieb bisher nicht gab.

### 10.2 Warum ein Boost und keine direkte 1S-Versorgung mehr

| Zustand | Spannung an der Pumpe | Bewertung |
|---|---|---|
| vorher (Pumpe an VBAT) | **3,0–4,2 V** | Die CONQUERALL ist mit **5 V** spezifiziert; Betrieb/Anlauf bei 3,7 V waren **nicht belegt** (offener Messauftrag, siehe `bom_entscheidung.md` §3b/§7) |
| **jetzt (Boost U8)** | **5,10 V, geregelt** | Beide Pumpen laufen in ihrer Nennspannung → Drehzahl, Fördermenge und Anlaufstrom werden **reproduzierbar**; der Messauftrag reduziert sich auf den Anlaufstrom |

**Topologie (MT3608, Standardbeschaltung):** VBAT → **L1 22 µH** → **SW (Pin 1)** ·
**D6 SS34** von SW nach **+5 V** · **C17 22 µF** am Eingang, **C18 22 µF + C19 100 nF** am Ausgang ·
**R31 75 kΩ / R32 10 kΩ** am FB-Pin ⇒ **V_out = 0,6 V × (1 + 7,5) = 5,10 V** ·
**EN (Pin 4) fest an VBAT** (der Boost läuft dauerhaft; Abschaltung erfolgt über die beiden MOSFETs).

### 10.3 Der zweite Leistungspfad ist eine Kopie des ersten

| | Dosierpumpe | Sauerstoffpumpe |
|---|---|---|
| Stecker | **J4** (JST-XH 2P, aufrecht) | **J16** (JST-XH 2P, aufrecht, **gleicher Typ `C158012`**) |
| Schalter | **Q1** AO3400A | **Q3** AO3400A (baugleich) |
| Gate-Serie | R1 4,7 kΩ | **R33 4,7 kΩ** |
| Gate-Pulldown | R2 47 kΩ | **R34 47 kΩ** |
| Freilauf | D1 1N5819WS an **+5V** | **D7** 1N5819WS an **+5V** |
| Klemmzweig (UV) | D3 an U7-RESET | **D8** an U7-RESET |
| Steuersignal | **IO2** (PUMP_EN) | **IO22** (PUMP2_EN) — vorher Reserve an J14 |

Bewusst **symmetrisch**: gleiche Teile, gleiche Rechenwege, ein Crimp-Werkzeug für beide Stecker —
und bei Unterspannung (< 3,08 V) klemmt der MAX809 über **D3 *und* D8 beide** Pumpen zwangsweise aus.

### 10.4 Strombedarf und die harte Boost-Grenze

| Fall | Strom @ 5 V | Eingangsstrom @ 3,0 V (η ≈ 85 %) | Boost (2 A Schalter) |
|---|---|---|---|
| Dosierpumpe allein | 0,40 A | 0,78 A | ✅ |
| Sauerstoffpumpe allein (Annahme 0,30 A) | 0,30 A | 0,59 A | ✅ |
| **beide gleichzeitig** | **0,70 A** | **1,37 A** | ✅ mit Reserve |
| **Anlauf Dosierpumpe** (3 A laut Datenblatt) | **3,0 A** | ~5,9 A | ❌ **nicht lieferbar** |

⚠️ **Der Boost kann den Anlaufstrom nicht liefern — und ein Ausgangskondensator kann das auch nicht.**
Rechnung: **t = C · ΔU / I** → 22 µF halten 3 A nur **~7 µs** bei 1 V Einbruch (selbst 1000 µF reichen
nur ~0,3 ms). Der Motoranlauf dauert aber ~100 ms.

⇒ **Der PWM-Softstart ist damit nicht mehr „empfohlen", sondern Pflicht:** Rampe über 100–300 ms
(GPIO2 bzw. GPIO22, 20 kHz), damit der Einschaltstrom **≤ 1 A** bleibt und in die Boost-Reserve passt.
Gilt für **beide** Pumpen (die Membranpumpe zieht beim Anlauf ebenfalls ein Mehrfaches ihres Nennstroms).
Ersatzweise (nicht vorgesehen): MT3608**B** (`C19189893`, **4 A** Schalterstrom) statt `C84817`.

### 10.5 ⚠️ Die Sauerstoffpumpe darf **nicht** dauerhaft laufen

| Betriebsart | Leistung aus der Zelle | Laufzeit mit 4,44 Wh nutzbar |
|---|---|---|
| Dosierpumpe 1 × 300 ml | ~0,08 Wh | 62–67 Dosen (wie bisher) |
| O2-Pumpe **dauerhaft** (0,30 A @ 5 V) | ~1,76 W | **≈ 2,5 Stunden** ❌ |
| O2-Pumpe **dauerhaft** (kleine Variante, 0,10 A) | ~0,59 W | ≈ 7,5 Stunden ❌ |
| **O2-Pumpe als Intervall** (5 × 10 min/Tag, 0,30 A) | ~0,15 Wh/Tag | ✅ neben der Bewässerung |

**Empfehlung:** Sauerstoffpumpe **nur in Intervallen** (Firmware-Zeitplan, z. B. 5 × 10 min/Tag).
Für Dauerbetrieb ist die 1500-mAh-Zelle zu klein — dann größere Zelle (18650, 3500 mAh ≈ 12,6 Wh),
oder die Pumpe hängt am USB-Netzteil. **Der Wandler ist hier die Hauptlast**, nicht die Dosierpumpe:
Er verliert ~15 % und zieht im Leerlauf zusätzlich ~1,6 mA (~38 mAh/Tag, ≈ 2,5 % der Zelle pro Tag).

### 10.6 Offene Punkte (in diesem Schritt bewusst nicht entschieden)

1. **Welche Sauerstoffpumpe genau?** Ausgelegt ist der Pfad für **5 V / bis 1 A / JST-XH 2P** (Stecker
   und MOSFET tragen 2–3 A). Die konkrete Pumpe (Membran-Luftpumpe, meist 0,3–1 W) ist noch nicht
   gewählt — bei der Auswahl auf **5 V Nennspannung** achten (nicht „3–12 V", das ist das bekannte
   Amazon-Fallmuster aus der Pumpenrecherche).
2. **Platz.** Platine: **80 → 94 Positionen** (neu: U8, L1, D6, D7, D8, C13–C16, R18–R21, Q3, J16;
   entfallen: J14). Neu dazukommen u. a. eine **6 × 6 mm Induktivität** und eine **SMA-Diode** — das ist
   deutlich mehr als der bisherige Reserve-Stecker. Die Platine ist mit der Zielgröße ≤ 38 mm Breite
   (Wulst 60 mm) **dicht**; entweder wächst die Platine/die Wulst, oder weitere Reserve-Stecker
   (J10–J13, J15) weichen.
3. **Einbauort der Sauerstoffpumpe.** Sie sollte **außerhalb des Topfs** stehen: eine Membran-Luftpumpe
   braucht **frische Luft** (im geschlossenen Gehäuse ist die Anreicherung sinnlos), und sie ist die
   zweite Wärmequelle. Das Kabel führt durch den vorhandenen Schlauchkanal; der Stecker J16 sitzt auf
   der Platine und geht **nach oben** raus (Top-Entry, wie J2/J4).
4. **Firmware:** zweiter PWM-Kanal auf IO22 (LEDC, 20 kHz), gleicher Softstart, Zeitplan + Watchdog.

---

## 12. Revision nach externem Schaltplan-Review (Historie, 15.09.2026)

Ein zweites Sprachmodell hat die Textbeschreibung (`schaltplan_v1_komplett.md`) geprüft. Jeder harte
Befund wurde gegen die IR verifiziert. Ergebnis: **drei echte Schaltungsänderungen** (hier umgesetzt),
mehrere Doku-Fehler (in der Textdatei korrigiert) und eine Reihe **berechtigter Auslegungspunkte**, die
bewusst **nicht** in V1 geändert werden.

### 12.1 Umgesetzte Änderungen (in der Netzliste, IR-neu gebaut, 0 Abweichungen)

| # | Änderung | Grund |
|---|---|---|
| 1 | **Klemmzweig entkoppelt:** `D3`/`D8` hängen nicht mehr am Gate, sondern über **R35/R36 (10 kΩ)** am `RESET_UV`. Gate-Serienwiderstände **R1/R33: 4,7 kΩ → 1 kΩ** | Der 4,7-kΩ-Gatewiderstand war nur wegen des Klemmstroms so groß (0,57 mA in den MAX809). Für **PWM** sind 4,7 kΩ zu träge. Jetzt ist die Klemmung über eigene Serienwiderstände begrenzt (**0,30 mA**, Spec 1,2 mA) und das Gate mit 1 kΩ schnell genug (τ ≈ 0,8 µs bei C_iss ≈ 800 pF → PWM bis ~1 kHz sauber) |
| 2 | **Boost-EN am Wächter:** `U8 Pin 4 (EN)` liegt nicht mehr fest an VBAT, sondern an `RESET_UV` mit **R37 47 kΩ Pull-up** nach VBAT | Bisher lief der Boost auch unter der Wächter-Schwelle weiter. Jetzt schaltet die **5-V-Schiene beim Auslösen wirklich ab** — doppelte Sperre zusätzlich zur Gateklemmung. ⚠️ Allein reicht der EN nicht: der MT3608 hat einen Pfad über L1/D6 zum Ausgang, deshalb bleibt die Gateklemmung nötig |
| 3 | **I²C-Pull-ups R19/R20: 10 kΩ → 4,7 kΩ** | Bei Buskapazität > 100 pF ist 10 kΩ zu hoch (100 kHz erlaubt t_r ≈ 1 µs, Fast-Mode 300 ns). Serienschutz R21/R22 bleiben **1 kΩ** — Low-Pegel 0,30 V, gültig; die 47 kΩ aus dem Review stammten aus der **fehlerhaften BOM**, nicht aus der Schaltung |

### 12.2 Zusätzlich gefundene und behobene Fehler

- **C11** lag zwischen `PUMP_N` und **VBAT** statt über den Motorklemmen (Altstand aus der VBAT-Ära) →
  jetzt an `+5V`, damit der EMI-Kondensator auch wirklich über der Pumpe liegt.
- **C20** lag zwischen `PUMP2_N` und **GND** (also über Drain–Source von Q3) → jetzt an `+5V`.
- **Fertigungs-BOM war inkonsistent:** funktionale Bezeichner (`C1a`, `C_BTN`, `R_GATE`) und verrutschte
  Zuordnungen — `R20` stand in der Gate-Zeile, `R21` mit **47 kΩ** statt 1 kΩ. Das wäre eine
  **Fehlbestellung** gewesen. BOM jetzt KI-frei aus der IR erzeugt: **90 bestückte Refs**, keine Lücken.

### 12.3 Bewusst NICHT in V1 geändert (Entscheidungen für V2 / Messauftrag)

| Punkt | Bewertung | Warum nicht jetzt |
|---|---|---|
| **Pumpenanlauf 3 A** (15,3 W, aus 3,0 V ≈ **6 A**) — der MT3608 kann das nicht, Softstart ist **kein** Nachweis | **berechtigt, offen** | Erfordert entweder stärkeren Boost (z. B. TPS61088), eine Pumpe mit kleinerem Anlaufstrom oder eine echte Anlaufstrombegrenzung. **Erst messen** (Messauftrag §10): realer Anlaufstrom der CONQUERALL am Prüfstand |
| **+3V3 aus 3,0 V VBAT** — der ME6211 ist ein LDO und kann nicht hochregeln; unter ≈ 3,5 V bricht die Logikversorgung ein | **berechtigt** | Buck-Boost wäre ein Umbau. Konsequenz dokumentiert: nutzbarer Zellbereich **4,2 → ~3,5 V** (die Angabe „3,0–4,2 V → +3V3" war irreführend) |
| **UVLO sperrt nur die Pumpen**, nicht das System | teilweise behoben (12.1 #2) | Der Akku hat ein PCM (Tiefentladung/Kurzschluss) — das ist aber ein Bauteil, kein Schaltungsschutz. Vollständige Systemabschaltung = V2 |
| **Kein Power-Path** (MCP73831 lädt den Lastknoten) | **berechtigt** | Lader mit Power-Path (MCP73871/BQ24074) = neuer IC, neue Platine → V2. Betriebsregel: **während des Ladens nicht pumpen** |
| **Mehr Ausgangsbulk** gegen den Anlauf | **nicht wirksam** | 22 µF puffern 3 A nur ~7 µs; selbst 220 µF nur ~73 µs. Der Hebel ist der Anlaufstrom, nicht der Kondensator |
| **IO3 versorgt J2 und J7 direkt** | berechtigt | Für die vorgesehenen Sensoren (< 20 mA) vertretbar; ein Load-Switch ist V2 |
| **Strapping-Pins GPIO4/5/15** (Licht/Reserve) | berechtigt zu prüfen | Firmware-Thema: Strap-Pegel beim Reset verifizieren (nicht jede Last stört den Boot) |

### 12.4 Was das Review bestätigt hat

Zwei getrennte 5,1-kΩ-CC-Pulldowns · USB D−/D+ an GPIO12/13 · USBLC6-Zuordnung · EN-Pull-up und
Reset-RC · GPIO8/9-Pull-ups und Boot-Taster · Low-Side-MOSFETs mit Gate-Pulldowns · Freilaufdioden
D1/D7 richtig gepolt · Boost-Feedback 0,6 × (1 + 75/10) = 5,10 V · VBAT-Teiler und ADC-Filter.

## 11. Rückschau

- 15.09.2026: **Sauerstoffpumpe + 5-V-Boost.** Zweiter, baugleicher Leistungspfad: **Q3** (AO3400A),
  **R33/R34** (Gate 4,7 kΩ / Pulldown 47 kΩ), **D7** (Freilauf), **D8** (UV-Klemmzweig), Stecker
  **J16** (JST-XH 2P aufrecht, `C158012`) — gesteuert über **IO22** (vorher Reserve **J14**, die
  entfällt). Weil **beide** Pumpen **5 V** bekommen sollen, sitzt jetzt ein **Boost U8 MT3608** mit
  **L1 22 µH**, **D6 SS34**, **C17/C18 22 µF + C19 100 nF**, **R31 75 kΩ / R32 10 kΩ** ⇒ **5,10 V**
  zwischen VBAT und den Pumpen (J4 Pin 1 und D1-Kathode liegen damit an **+5V**, nicht mehr an VBAT).
  ⚠️ Zwei Konsequenzen, die bewusst dokumentiert sind: **der PWM-Softstart ist jetzt Pflicht** (der
  Boost liefert den 3-A-Anlauf nicht, und kein Kondensator puffert ihn — 22 µF ≈ 7 µs) und **die
  Sauerstoffpumpe darf nicht dauerhaft laufen** (sonst ist die 1500-mAh-Zelle in ~2,5 h leer).
  Details, Rechnungen und offene Punkte in **§10**.
- 15.09.2026: **Steckertypen J1/J2/J4 von gewinkelt (Side-Entry) auf aufrecht (Top-Entry) umgestellt** —
  die Stecker gehen jetzt **nach oben** aus der Platine, nicht zur Seite. Neue LCSC-Codes:
  **J1 `C160352`** (JST `B2B-PH-SM4-TB`, SMD, vorher `C54582899` = `S2B-…` liegend „卧贴"),
  **J2 `C493416`** (JST `B3B-XH-A-BK`, THT, vorher `C157928` = `S3B-…` gewinkelt „弯插"),
  **J4 `C158012`** (JST `B2B-XH-A`, THT, vorher `C157931` = `S2B-…` gewinkelt — Lager war auf 2 Stück gefallen).
  Die aufrechten Typen haben deutlich mehr Lager (J4: 203.889, J2: 19.594). Pinbelegung unverändert;
  Belegung geprüft: **Pin-für-Pin-Diff gegen die Baseline = 0 Abweichungen, 50 Netze unverändert**.
  Die Gehäuse-UUIDs (`uniqueId`) der drei Stecker wurden bewahrt, damit `pcb import-changes` den
  Footprint **aktualisiert** („Modify Footprint") statt Bauteil zu löschen und neu zu setzen —
  die Platzierung auf der Platine bleibt damit erhalten (PCB: 80 Bauteile vor und nach dem Import).
  Restpunkt: `sch gate` meldet in der Stage `clusters` einen **Lesbarkeits**-Overlap J1 ↔ TP3
  (10 × 3 Einheiten); `layout-lint`, `check`, `bridge-check` und `drc` sind grün.
- 14.09.2026: GPIO-Erweiterung (J8/J9/J10/Q2/TP7–TP11) auf Wunsch des Nutzers wieder entfernt.
- 14.09.2026: GPIO-Erweiterung auf 2,54-mm-Stiftleisten wieder eingebaut (je Signal ein
  3-pol GND–VCC–SIG-Stecker, I²C als 4-pol).

---

## 13. Revision „2S-Umbau" (16.09.2026)

Auftrag: *„Wechsel den 1S-Akku zu einem 2S-Akku. Ein IP2326-Board, damit man per USB-C laden kann.
Die Step-Ups für 5 V können raus, aber ein Step-Down rein für den ESP32 und ggf. ein 5 V für Sensoren."*

### 13.1 Was geändert wurde

| # | Änderung | Begründung |
|---|---|---|
| 1 | **Akku 1S → 2S** (VBAT 3,0–4,2 V → **6,0–8,4 V**) | Vorgabe. Nutzen: doppelte Energie (11,1 statt 5,55 Wh) und die Pumpe läuft in ihrer Nennspannung |
| 2 | **U_CHG = IP2326** statt MCP73831 | 1S-Lader kann 2S nicht laden. Der IP2326 lädt aus **5 V USB** auf **8,4 V** (Boost-Lader, 15 W), Ladestrom per R_ISET |
| 3 | **5-V-Boost (MT3608) → 5-V-Buck (SY8113B)** | Aus 6,0–8,4 V muss man 5 V **herunter**regeln, nicht hoch. Nebenwirkung: der 3-A-Pumpenanlauf liegt jetzt **innerhalb** der Nennlast (der Boost konnte ihn nicht liefern, deshalb war der Softstart Pflicht) |
| 4 | **3,3-V-LDO (ME6211) → 3,3-V-Buck (AP63203)** | Auftrag („Step-Down für den ESP32"). 88 % statt 66 % Wirkungsgrad; der LDO hätte aus 8,4 V 0,65 W in SOT-23-5 verheizt und darf laut Datenblatt ohnehin nur 6,0 V Eingang |
| 5 | **U7 = TPS3839G33** statt MAX809T (beide 3,08 V) | ⚠️ Der MAX809 verträgt nur **5,5 V** Versorgung und 12 µA Eigenstrom — an einem 2S-Teiler wäre der Iq-Fehler 2,4 V. Der TPS3839 zieht **150 nA** (Offset 30 mV) und hat einen Push-Pull-Ausgang |
| 6 | **Wächter-Teiler bleibt 200 k/200 k**, Versorgung = VBAT/2 | gleiche Schwellenlogik wie vorher: **6,16 V Pack = 3,08 V/Zelle** |
| 7 | **ADC-Teiler 1:2 → 1:3,94** (200 k/68 k) | vorher „max. 2,1 V" aus 4,2 V; 8,4 V hätten am 1:2-Teiler **4,2 V** ergeben und den ADC (max. 3,3 V) überfahren |
| 8 | **C3 (100 µF) von VBAT nach +5V** | der Puffer gehört an die Schiene, die die Pumpen wirklich speist |
| 9 | **J17 (JST-XH 2P) = 5-V-Sensorausgang** | „ggf. ein 5 V für Sensoren" — die Sensorik selbst bleibt an SENSOR_PWR (3,3 V, per IO3 geschaltet), J17 ist der zusätzliche 5-V-Abgriff |
| 10 | **EN-Pull-up R37 entfällt**, EN direkt am Wächter | Push-Pull-Ausgang darf direkt treiben (2 mA bei V_OL ≤ 0,4 V — nötig für die Klemmzweige) |
| 11 | **Ladeschaltung neu beschaltet:** L_CHG 2,2 µH, R_VIN_CHG 0,5 Ω, C_CHG_IN/VIN/OUT 10 µF, 2 × 22 µF an VSYS, C_BST_CHG 100 nF, R_ISET 100 k, R_NTC 51 k, R_UVSET 68 k, R_EN_CHG 100 k | komplett nach Datenblatt-BOM/Applikationsbild; alle Werte mit Quelle in §3 |
| 12 | **DP/DM des Laders offen** (kein Fast-Charge) | die Datenleitungen gehören dem ESP32 (USB-Serial-JTAG). Datenblattkonform: ohne Request wird dauerhaft mit 5 V geladen |

### 13.2 Was **nicht** geändert wurde (bewusst)

- **Kein Power-Path:** der IP2326 hat keinen (Datenblatt-Grep: 0 Treffer). Betriebsregel bleibt:
  beim Pumpen möglichst nicht laden. Ein Lader mit Power-Path wäre ein anderes IC (z. B. BQ25887,
  bei JLC lagernd, aber I²C-konfiguriert und mit Balancing) — bewusst **nicht** gewählt, weil der
  Auftrag den IP2326 nennt und der Aufwand (I²C-Anbindung + Firmware) nicht im Verhältnis steht.
- **Balancing des IP2326 bleibt unbeschaltet** (2-poliger Akku-Stecker) → §6.3.
- **Die 3,3-V-Schiene hängt nicht am Wächter** (MCU soll melden können).
- **PWM-Softstart bleibt empfohlen** (Thermik, Akku-Einbruch, EMV), ist aber nicht mehr Bedingung.

### 13.3 Bauteilbilanz

| | vorher | jetzt |
|---|---|---|
| Bauteile in der Netzliste | 96 | **115** |
| Netze | 56 | **68** |
| Verbindungen | 268 | **314** |
| Positionen in der JLC-BOM | 90 bestückte Refs | **neu erzeugt (siehe `pcba_bom_jlc.csv`)** |
| Extended-Positionen (Handling) | 12 | **15** (neu: U_CHG, U_BUCK5, U_BUCK3, L_CHG, L_BUCK5/3, TPS3839 …; entfallen: MCP73831, ME6211, MT3608, SS34, 22-µH-L1) |

### 13.4 ⚠️ Dabei gefundener Fehler im Altstand (Klemmzweig war wirkungslos)

In der Netzliste vom 15.09.2026 standen:

```
KLAMP1,D3,Anode          KLAMP1,R_CLAMP1,1         (Kommentar: "zum Gate-Knoten")
RESET_UV,D3,Kathode      RESET_UV,R_CLAMP1,2
```

`R_CLAMP1` lag damit **parallel** zur Diode D3 zwischen denselben zwei Netzen, und der Knoten
`KLAMP1` war **an kein Gate angeschlossen** (das Gate heißt `GATE` bzw. `GATE2`). Folge: die
Unter­spannungsklemmung der Pumpen war **funktionslos**; nur der Weg über den Boost-EN (R37) wirkte.
Der Netzlisten-Lint konnte das nicht sehen (beide Bauteile liegen auf zwei Netzen, das Netz hat
zwei Bauteile). **Jetzt korrekt als Serienkette:** `GATE → R_CLAMPx (10 k) → Dx → RESET_UV`.
Der IR-EasyEDA-Stand vom 15.09.2026 trägt denselben Fehler — beim Neuaufbau mit korrigieren.

### 13.5 Folgeauftrag (nächster Schritt)

1. **EasyEDA-Neuaufbau:** die 4 neuen IC-Geräte-UUIDs per `easyeda lib by-lcsc` auflösen
   (`C2832094`, `C780769`, `C78989`, `C485802`), in `build_ir.py` (`COMPS`) eintragen, IR neu bauen,
   Netzklassen/Layout-Input neu erzeugen → erst danach `pcb import-changes`.
2. **Design-Checks** (`hardware/design/`) auf 2S umstellen: `circuit.py` liest U3/U4/U7-Werte aus
   diesem Dokument (U4 entfällt!) — die Prüfungen für LDO-Headroom/Boost-Feedback sind zu ersetzen
   durch Buck-Feedback, Wächter-/Teiler-Rechnung und Ladepfad-Rechnung.
3. Akku-Pack bestellen (§6.7 Nr. 1) und die Messungen aus §6.7 abarbeiten.
