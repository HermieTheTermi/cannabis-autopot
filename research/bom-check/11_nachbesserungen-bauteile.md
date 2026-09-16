# 11 — Nachbesserungen: konkrete, bestellbare Bauteile für die 5 Review-Punkte

**Projekt:** SmartGrowTopf_V1 (ESP32-C6, 2S-Akku 6,0–8,4 V, IP2326-Boost-Lader, 5-V- und 3,3-V-Buck)
**Stand:** 16.09.2026
**Methode:** JLCPCB-Parts-API `selectSmtComponentList/v2` (live abgefragt am 16.09.2026 — jede Zeile ein echter API-Treffer) + Herstellerdatenblätter, die über die LCSC/wmsc-Datenblatt-URLs der jeweiligen Position geladen und im Textlayer geprüft wurden (IP2326 V1.11, AP63203 DS41326 Rev 3-2, AO3401A AOS Rev 3.1, Sunlord SDNT-Serie Rev 2021/05/15, Littelfuse 452-Serie Rev 11/23/16, Jinkaisheng 2410 A/2).

**Legende:**

| Kürzel | Bedeutung |
|---|---|
| **basic** (`base`) | Grundsortiment — keine Handling-Gebühr |
| **preferred** | „Preferred Extended" — Extended, aber **von der Feeder-Gebühr der Economic-PCBA befreit** (JLCPCB-FAQ) |
| **extend.** (`expand`) | Extended — **+3 USD je Position** (Handling), bei JLCPCB bestückbar |
| Bestand | `stockCount` aus der API (Stück), Stand 16.09.2026 |
| Preis | 1-Stück-Staffel in USD (PCBA-Preis, nicht LCSC-Retail) |

> **Nachkontrolle:** Alle unten empfohlenen Codes (`C919175`, `C23254`, `C158012`, `C66503`, `C5220743`, `C780769`, `C17901`, `C15127`, `C110499`) wurden am 16.09.2026 um **12:27 Uhr** ein zweites Mal live abgefragt — Bestand, Library-Typ und Preis **unverändert**.

---

## 0. Kurzfassung — Empfehlungen

| # | Lücke | Empfehlung (LCSC) | Bauteil | Bauform | Typ | Bestand | $/Stk | 1 Zeile Begründung |
|---|---|---|---|---|---|---|---|---|
| 1 | **NTC am Akku** | **`C919175`** + `C23254` + `C158012` | NTC 100 kΩ ±1 %, B 3950 K ±1 % + 82 kΩ ∥ + JST-XH-2P | 0805 / 0603 / THT | extend. / **basic** / extend. | 72.524 / 1.408.937 / 432.144 | 0,0445 / 0,0042 / 0,0406 | 100 k ∥ 82 k reproduziert exakt die Datenblatt-Schwellen (0 / 45 / 55 °C), 82 k ist **Basic**, der XH-2P ist schon in der Stückliste (J4/J16/J17) |
| 2 | **Sicherung** | **`C66503`** (Alt.: `C5220743`) | Littelfuse NANO2 Slo-Blo 5 A träge, 125 V AC/DC | 2410 (6,1×2,7 mm) | extend. | 25.526 (Alt. 1.581) | 0,2821 (Alt. 0,0541) | 3,6 A = 72 % Nennstrom (kein Auslösen), Kurzschluss → ≈ 17 ms; kleinste Bauform mit ≥ 4 A, Littelfuse mit dokumentierter **DC**-Abschaltleistung |
| 3 | **3,3-V-Buck** | **`C780769`** (bleibt) — Teiler **entfällt** | AP63203WU-7 (feste 3,3 V) | TSOT-23-6 | extend. | 25.499 | 1,1794 | Einstellbare **AP63200 ist bei JLCPCB nicht verfügbar** (0 bzw. 1 Stück) ⇒ Festspannungsvariante **ohne** Teiler, FB direkt an VOUT (Datenblatt-Bild 21) |
| 4 | **R_CB 100 Ω / 0,25 W** | **`C17901`** (Alt.: `C83143`) | 100 Ω ±1 %, 250 mW | 1206 (Alt. 1210) | **basic** (Alt. extend.) | 2.913.449 (Alt. 14.218) | 0,0066 (Alt. 0,0246) | 176 mW = 70,6 % von 250 mW im 1206 — **als Basic-Part ohne Handling-Gebühr**; 1210 mit 500 mW = 35 % als Reserve |
| 5 | **P-Kanal-Lastschalter** | **`C15127`** (Alt.: `C110499`) | AO3401A, P-MOSFET −30 V, R_DS(on) 85 mΩ @ −2,5 V | SOT-23 | **basic** (Alt. extend.) | 477.015 (Alt. 114.698) | 0,0942 (Alt. 0,1297) | **Basic**, schon als Q2 in der Stückliste (VCC_EXT) ⇒ gleicher Footprint/Typ, günstigster Kandidat; Alternative mit besserem R_DS(on) |

**Kostenwirkung:** nur **eine** neue Extended-Position (Sicherung) = **+3 USD Handling**; NTC, 82 kΩ und 1206-100 Ω sind Basic bzw. werden lose gekauft ⇒ Bauteilmehrkosten < 0,40 USD.

---

## 1. Akku-Temperatursensor (NTC) + 2-poliger Stecker

### Anforderung & Datenblatt-Vorgabe
Der IP2326 (Pin 4 = NTC) speist **20 µA** in einen NTC und wertet die Spannung aus (Datenblatt V1.11 §9, „充电NTC"):

| Spannung am NTC-Pin | Bedeutung | Reaktion |
|---|---|---|
| > 1,32 V | **zu kalt** | Laden **aus** |
| 0,56 … 1,32 V | normal | normal laden |
| 0,43 … 0,56 V | **warm** | Ladestrom **halbiert** |
| < 0,43 V | **zu heiß** | Laden **aus** |

**Datenblatt-Beispiel (verbindlich):** R_NTC = **100 kΩ** (B = 4100) **∥ R2 = 82 kΩ** ⇒ 0 °C → 1,32 V, 45 °C → 0,56 V, 55 °C → 0,43 V. Der feste 51-kΩ-Widerstand (`R_NTC` = `C17737`, „NTC stillgelegt") entfällt und wird durch **NTC ∥ 82 kΩ** ersetzt.

### Empfehlung
| Rolle | LCSC | Bauteil | Bauform | Typ | Bestand | $/Stk |
|---|---|---|---|---|---|---|
| **NTC (im Pack, am Kabel)** | **`C919175`** | Sunlord **SDNT2012X104F3950FTF**: 100 kΩ **±1 %**, B(25/50) = **3950 K ±1 %**, 200 mW, Imax 0,14 mA, τ < 5 s, −55…+125 °C | 0805 | extend. | **72.524** | 0,0445 |
| **Parallel-R2 (auf der Platine)** | **`C23254`** | UNI-ROYAL 0603WAF8202T5E: **82 kΩ ±1 %**, 100 mW, −55…+155 °C | 0603 | **basic** | **1.408.937** | 0,0042 |
| **Stecker (auf der Platine)** | **`C158012`** | JST **B2B-XH-A(LF)(SN)**, XH 2-pol. aufrecht THT, 2,5 mm, 3 A / 250 V, −25…+85 °C | THT | extend. | **432.144** | 0,0406 |

* **Alternative NTC-Kandidaten:** `C919169` — Sunlord SDNT1608X104F3950FTF, 100 kΩ ±1 %, B3950 ±1 %, **0603**, 100 mW, **122.302 lagernd, 0,0227 $** (kleiner/günstiger, gleiche Schwellen); `C17443468` (SDNT1608…HTF, 0603, 0 Stück — **nicht** verwenden).
* **Alternative für R2:** `C17840` — UNI-ROYAL 0805W8F8202T5E, 82 kΩ ±1 %, 0805, 125 mW, **expand aber „Preferred"** (bei Economic-PCBA ohne Feeder-Gebühr), 123.326 lagernd, 0,0052 $. Damit wäre R2 mechanisch robuster bei praktisch gleichem Preis.
* **Stecker-Empfehlung:** `C158012` ist **dieselbe Position wie J4/J16/J17** ⇒ nur die Menge 3 → **4** erhöhen (kein neuer BOM-Eintrag, keine zusätzliche Extended-Position). Gegenstück: XH-2P-Gehäuse + Crimpkontakte (bzw. fertiges 2-pol. XH-Kabel).

### Rechnung (nachgerechnet, Modell R(T) = 100 kΩ · e^(3950·(1/T − 1/298,15)))
| R2 | „zu kalt" (1,32 V) | „warm" (0,56 V) | „zu heiß" (0,43 V) |
|---|---|---|---|
| **82 kΩ** (`C23254`) | **−0,1 °C** | **45,6 °C** | **55,6 °C** |
| 83 kΩ (68 k + 15 k in Serie, beides Basic/BOM) | +0,8 °C | 45,7 °C | 55,7 °C |
| 75 kΩ (nur BOM-Wert) | −9,2 °C ✗ | 45,6 °C | 55,6 °C ✗ |

⇒ **82 kΩ ist nicht beliebig, sondern das Datenblatt-Äquivalent**; 75 kΩ (ein bereits vorhandener Basic-Wert) verschöbe die Kalt-Schwelle auf −9 °C und würde Laden unter 0 °C erlauben — **unzulässig** für Li-Ion.

**Fail-safe-Verhalten (wichtig):** Stecker abgezogen oder NTC-Kabel gebrochen ⇒ am Pin liegen 20 µA × 82 kΩ = **1,64 V > 1,32 V** ⇒ Lader interpretiert „zu kalt" und **schaltet das Laden ab** (kein Laden ohne Sensor). ✔

**Montagehinweis:** Der NTC ist kein Bestückungsteil — er wird mit zwei kurzen Adern verlötet (Lötstelle + Schrumpfschlauch) und **thermisch an die Zellen gekoppelt** (zwischen/auf die Zellen geklebt, unter dem Schrumpfschlauch des Packs), die andere Seite geht auf den XH-2P-Stecker. Pin 1 = NTC-Signal, Pin 2 = GND. Der 0805-NTC muss dafür **lose bei LCSC** bestellt werden (min. 1 Stück), er erscheint **nicht** in der JLC-Bestückungsliste (keine +3 USD).

**Datenblatt-Quellen:** IP2326 V1.11 §9 (NTC-Schwellen, Beispielkurve) — `https://www.lcsc.com/datasheet/lcsc_datasheet_2304062030_INJOINIC-IP2326_C2832094.pdf`; Sunlord SDNT-Serie — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2110081730_Sunlord-SDNT2012X104F3950FTF_C919175.pdf`

---

## 2. Sicherung zwischen Akkupack und Platine

### Anforderung
Normale Last **2,8–3,6 A** aus dem Pack; der elektronische Schutz (HY2120) greift erst bei ca. **17 A** — zu spät für Leitung und Stecker. Die Sicherung liegt in der **BAT+-Leitung (J1 Pin 3 → VBAT-Knoten)**, also vor Lader-VOUT und vor beiden Bucks.

### Auslegung
| Kriterium | Wert | Bewertung der Empfehlung (5 A träge) |
|---|---|---|
| Dauerstrom | 2,8–3,6 A | **56–72 %** des Nennstroms — laut UL248-14 kein Auslösen (100 % = min. 4 h) |
| Motor-/Einschaltstromspitzen (Pumpen) | kurzzeitig | **träge (T/Slo-Blo)** statt flink ⇒ keine Fehlauslösung |
| Kurzschluss 2S-Pack | ≈ 8,4 V / 0,15 Ω ≈ **56 A** | Schmelz-I²t 53,7 A²s ⇒ **≈ 17 ms** Abschmelzzeit (weit vor Kabelerwärmung) |
| Auslöseverhalten | 200 % = 1–60 s · 300 % = 0,2–3 s · 800 % = 20–100 ms | Datenblatt Littelfuse 452 / Jinkaisheng 2410 |
| Spannung | Pack max. 8,4 V DC | 125 V-Typen, Littelfuse explizit **125 V AC/DC** (50 A) bzw. **300 A @ 32 V DC** |

### Empfehlung
| Rolle | LCSC | Bauteil | Bauform | Typ | Bestand | $/Stk |
|---|---|---|---|---|---|---|
| **Empfehlung** | **`C66503`** | **Littelfuse `0452005.MRL`** — NANO2® **Slo-Blo® 452-Serie**, **5 A träge**, **125 V AC/DC**, Abschaltvermögen **50 A @ 125 V AC/DC / 300 A @ 32 V DC**, I²t **53,72 A²s**, R_kalt 13,6 mΩ, −55…+125 °C, UL/CSA | **2410** (6,1 × 2,7 mm) | extend. | **25.526** | 0,2821 |
| **Gleichwertige, günstige Alternative** | **`C5220743`** | Jinkaisheng **2410 T5A/125V** — **5 A träge**, 125 V, I²t 58 A²s, Temperaturanstieg ≤ 75 K @1,0 In, UL248-14 / C-UR (E358589) | 2410 | extend. | **1.581** | **0,0541** |
| Flinke Variante (falls gewünscht) | `C48467` / `C5220741` | Littelfuse 0451005.MRL (5 A flink) / Jinkaisheng 2410 F5A (5 A flink) | 2410 | extend. | 18.143 / 1.510 | 0,2543 / 0,0541 |
| Engere Auslegung (knapper Lagerbestand) | `C5220739` | Jinkaisheng **2410 T4A/125V** (4 A träge) — nur sinnvoll, wenn 3,6 A dauerhaft sicher eingehalten werden | 2410 | extend. | **143** | 0,0523 |

**Warum die Littelfuse-Empfehlung, obwohl die Jinkaisheng billiger ist?** Die Jinkaisheng gibt das Abschaltvermögen **nur für AC** an (100 A @ 125 V AC); ein **DC-Wert fehlt im Datenblatt**. Im Akkukreis (DC) ist `C66503` die einzige geprüfte Option mit **dokumentierter DC-Abschaltleistung** (125 V AC/DC, 300 A @ 32 V DC) — bei 20-fachem Lagerbestand. Wer die 0,23 USD Differenz sparen will, nimmt `C5220743` und akzeptiert die AC-Angabe.

**Layout:** 2410-Bauform braucht ca. **6,5 × 3,2 mm** (plus Pads) — in der Platine einzuplanen; im 1206-Format gibt es bei JLCPCB nur bis **3,5 A** (`C2874918`, 1206, 3,5 A, 1147 Stück) bzw. 3 A (`C21261120`) ⇒ **zu knapp** für 3,6 A Dauerstrom, deshalb 2410.

**Datenblatt-Quellen:** Littelfuse 452/454 — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2304140030_Littelfuse-0452005-MRL_C66503.pdf` (Zeit-Strom-Tabelle S. 1, I²t-Tabelle S. 2); Jinkaisheng 2410 — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2210271630_Shenzhen-Jinkaisheng-Elec-2410-T5A-125V_C5220743.pdf`

---

## 3. 3,3-V-Buck: feste Ausführung **ohne** Teiler (oder einstellbare Variante?)

### Live-Prüfung „ist die einstellbare Variante bei JLCPCB verfügbar?"
| Kandidat | LCSC | Bestand | Presale | Bewertung |
|---|---|---|---|---|
| **AP63200WU-7** (einstellbar, 500 kHz, der eigentlich gesuchte Typ) | `C2071868` | **0** | **−355 (kein Presale)** | ❌ **nicht bestellbar** |
| AP63200QWU-7 (einstellbar, AEC-Q100, 450–550 kHz) | `C5248534` | **1** | −18 | ❌ faktisch nicht bestückbar |
| AP63201WU-7 (einstellbar, aber PWM-only, 500 kHz) | `C2071044` | 126 | −95 | ⚠️ verfügbar, aber zu kleiner Bestand + anderes Regelverhalten |
| AP63202 | — | — | — | ❌ **0 Treffer** in der JLCPCB-Bibliothek |

⇒ **Die einstellbare Variante ist bei JLCPCB nicht praktikabel verfügbar.** Die saubere Lösung ist die zweite Review-Option.

### Empfehlung: AP63203 behalten (feste 3,3 V) und den Feedbackteiler **entfernen**
| Rolle | LCSC | Bauteil | Bauform | Typ | Bestand | $/Stk |
|---|---|---|---|---|---|---|
| **U_BUCK3 (bleibt)** | **`C780769`** | **AP63203WU-7** — „Fixed 3.3V", 3,8–32 V, 2 A, 1,1 MHz, Iq 22 µA, TSOT-23-6 | TSOT-23-6 | extend. | 25.499 | 1,1794 |
| **entfällt** | — | `R_FB3_TOP` 47 kΩ (`C17713`), `R_FB3_BOT` 15 kΩ (`C17475`) — beide Positionen **löschen** | 0805 | basic | — | — |

**Begründung / Beleg aus dem Datenblatt (DS41326 Rev. 3-2, S. 9):**
* Bild 20 (**AP63200/AP63201**) = einstellbare Version: FB (Pin 1) hängt am **Teiler R1 = 30,9 kΩ / R2 = 62 kΩ + C4 = 100 pF**.
* Bild 21 (**AP63203/AP63205**) = Festspannungsversion: **kein Teiler, kein C4** — im Bild ist **Pin 1 (FB) direkt mit dem Ausgangsknoten VOUT** (hinter L, an C2) verbunden (am gerenderten Datenblattbild verifiziert).
* Pinbelegung damit ebenfalls bestätigt: **1 FB · 2 EN · 3 VIN · 4 GND · 5 SW · 6 BST** (DS41326, „Pin Descriptions" — die in `schaltplan_v1.md` §… noch offene Frage ist damit beantwortet).
* Der bisherige Teiler 47 k/15 k (→ 0,8 V an FB) kann an einem **festen** Regler den internen Abgleich belasten; das erlaubte Ziel von 3,31 V ist nicht garantiert. **Korrekte Beschaltung: FB = VOUT** (Teiler und `R_FB3_TOP/BOT` raus).
* Nebeneffekt: −2 Bauteile, −2 Bestückungspunkte, kein neuer LCSC-Code.

**Falls doch einstellbar zwingend gewünscht ist:** Der **SY8113B** ist bereits in der Stückliste (5-V-Buck, `C78989`, 50.655 lagernd, einstellbar ab 0,6 V: Vout = 0,6 × (1 + R_top/R_bot), 3 A) — aber **andere Pinbelegung** (1 BS · 2 GND · 3 FB · 4 EN · 5 IN · 6 LX) ⇒ Layout-/Netzlistenänderung, höherer Ruhestrom als die 22 µA des AP63203. Nicht empfohlen, nur als Rückfalloption genannt.

**Datenblatt:** `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2201131130_Diodes-Incorporated-AP63203WU-7_C780769.pdf`

---

## 4. Balancing-Widerstand R_CB: 100 Ω in 0,25-W-Bauform

**Fehlerfall-Rechnung (nachgerechnet):** Liegt eine Zelle bei 4,2 V gegen den Mittelabgriff, fällt genau diese Spannung über R_CB ab:
`P = U²/R = 4,2² / 100 Ω = 176,4 mW` (42 mA — innerhalb der Balancing-Grenze des IP2326).

| Kandidat | LCSC | Bauteil | Bauform | Leistung | Auslastung bei 176 mW | Typ | Bestand | $/Stk |
|---|---|---|---|---|---|---|---|---|
| **Empfehlung** | **`C17901`** | UNI-ROYAL **1206W4F1000T5E**: **100 Ω ±1 %**, 200 V, −55…+155 °C | **1206** | **250 mW** | **70,6 %** | **basic** | **2.913.449** | **0,0066** |
| **Alternative (mehr Reserve)** | **`C83143`** | YAGEO **RC1210FR-07100RL**: 100 Ω ±1 %, 200 V, −55…+155 °C | **1210** | **500 mW** | 35,3 % | extend. | 14.218 | 0,0246 |
| (billiger, 5 %) | `C118845` | FH RS-06K101JT, 100 Ω ±5 %, 1206, 250 mW | 1206 | 250 mW | 70,6 % | extend. | 257.649 | 0,0047 |
| (Bauteil-Splitting, bleibt 0805) | `C17540` | 2 × **200 Ω ±1 % 0805** (125 mW) parallel = 100 Ω / 250 mW | 0805 | 2 × 125 mW | 70,6 % je R | **basic** | 1.468.608 | 0,0073 |

**Empfehlung: `C17901`** — ein 1206-Widerstand mit 250 mW als **Basic-Part** (identischer Wert/Toleranz wie bisher, nur größere Bauform). Die übliche Derating-Kurve (100 % bis 70 °C, linear auf 0 % bei 155 °C) erlaubt 176 mW bis ≈ **+95 °C** Umgebungstemperatur. Wer zusätzliche Reserve will (z. B. wenn die Platine ohne Derating-Reserve bis 105 °C spezifiziert werden soll), nimmt **`C83143`** (1210, 500 mW) — Aufpreis 0,018 USD, aber +3 USD Handling, da Extended.

**Datenblatt-Quelle:** LCSC-Produktdaten `C17901` (250 mW, ±1 %, 1206) — `https://www.lcsc.com/datasheet/lcsc_datasheet_2411221126_UNI-ROYAL-Uniroyal-Elec-1206W4F1000T5E_C17901.pdf`

---

## 5. P-Kanal-MOSFET als Lastschalter für die Sensorversorgung

### Anforderung
High-Side-Schalter an **+3V3** (Source = Rail, Drain = SENSOR_PWR, Gate = GPIO), damit der GPIO nicht selbst die Sensorströme liefert; **fail-safe aus** bei Reset (Gate-Pull-up 47 kΩ `C17713`, bereits in der Stückliste). Logikpegel-Tauglichkeit bei V_GS = −3,3 V ist Pflicht.

### Empfehlung
| Rolle | LCSC | Bauteil | Bauform | Typ | Bestand | $/Stk |
|---|---|---|---|---|---|---|
| **Empfehlung** | **`C15127`** | **AOS AO3401A**, P-Kanal, SOT-23 | SOT-23 | **basic** | **477.015** | **0,0942** |
| **Gleichwertige Alternative** | **`C110499`** | **Diodes DMP2035U-7**, P-Kanal, SOT-23, AEC-Q101, ESD 3 kV | SOT-23 | extend. | 114.698 | 0,1297 |
| Zweite Alternative (preiswerter) | `C102619` | Diodes DMG2301L-7, P-Kanal, SOT-23 | SOT-23 | extend. | 20.011 | 0,1243 |

### Datenblatt-Kenndaten (AO3401A, AOS-Datenblatt Rev 3.1)
| Parameter | Wert | Quelle/Anmerkung |
|---|---|---|
| **V_DS** | **−30 V** (BVDSS −30 V) | Absolute Maximum Ratings |
| **V_GS max** | **±12 V** | Absolute Maximum Ratings (GPIO 3,3 V ⇒ unkritisch) |
| **I_D** | **−4,0 A** (T_A = 25 °C) / −3,2 A (T_A = 70 °C), V_GS = −10 V | für Sensorbetrieb (~0,2 A) um Faktor > 15 überdimensioniert |
| **R_DS(on) max** | **< 50 mΩ @ V_GS = −10 V** · **< 60 mΩ @ V_GS = −4,5 V** · **< 85 mΩ @ V_GS = −2,5 V** (jeweils max) | genau die geforderten beiden Stützstellen inkl. −2,5 V vorhanden |
| **V_GS(th)** | **−0,5 V (min) / −0,9 V (typ) / −1,3 V (max)** bei V_DS = V_GS, I_D = −250 µA | ⇒ bei V_GS = **−3,3 V** sicher voll durchgesteuert (Faktor 2,5 über V_GS(th),max) |
| **Gehäuse/Pinbelegung** | **SOT-23: Pin 1 = G · Pin 2 = S · Pin 3 = D** | AOS-Bild „Top View": einzelner Anschluss = **D**, Pin-1-Punkt an der **G**-Seite; **numerisch bestätigt** durch das LCSC/EasyEDA-Pinout-Diagramm zu C15127 (Bildbeschreibung „D3 G1 S2" = D→Pin 3, G→Pin 1, S→Pin 2) und identisch mit dem bereits verdrahteten Q2/AO3401A und Q1/Q_PUMP/AO3400A |
| Verlustleistung im Einsatz | 0,2 A × 85 mΩ = **17 mV** Drop / **3,4 mW** | Rechnung |

**Alternative DMP2035U-7** (Diodes, Datenblatt DS31830 Rev. 4-2, S. 3, aus dem Datenblatttext gelesen): V_DS **−20 V** (BVDSS), I_D −3,6 A, **R_DS(on) 23 mΩ typ / 35 mΩ max @ V_GS = −4,5 V** und **30 mΩ typ / 45 mΩ max @ V_GS = −2,5 V** (I_D = −4,0 A) bzw. 41/62 mΩ @ −1,8 V, **V_GS(th) −0,4 / −0,7 / −1,0 V** (min/typ/max), V_GS max ±8 V, P_D 810 mW, T_j −55…+150 °C, SOT-23, **AEC-Q101**, ESD-Schutz 3 kV — elektrisch besser als der AO3401A, dafür Extended (+3 USD) und teurer (0,1297 USD).
**DMG2301L-7** (Diodes, DS37540 Rev. 4-2): V_DS −20 V, I_D −3 A, R_DS(on) **max 120 mΩ @ V_GS = −4,5 V / 150 mΩ @ V_GS = −2,5 V**, V_GS ±8 V, P_D 1,5 W, −55…+150 °C — günstiger, aber deutlich schlechteres R_DS(on) als der AO3401A.

**Empfehlung:** **`C15127`** — Basic (keine Handling-Gebühr), billigster Kandidat, **identisch mit Q2 (AO3401A)**, d. h. es wird kein neuer Typ/datenblattloser Code in die Bibliothek aufgenommen und der bestehende SOT-23-Footprint bleibt gültig. Nur wenn ein niedrigeres R_DS(on) oder AEC-Q101 gefordert wird, ist `C110499` die bessere Wahl.

**Wichtiger Hinweis zur Beschaltung:** Der GPIO muss das Gate **nach GND ziehen** (Source = 3,3 V ⇒ V_GS = −3,3 V = ein). Die Sensorschiene darf dafür **3,3 V** sein. Sollte die Sensorik später an **5 V** gehängt werden, reicht der 3,3-V-GPIO-Pegel nicht mehr für V_GS = −5 V und es bräuchte einen kleinen N-Kanal-Treiber/Gate-Widerstandsteiler — für die aktuelle 3,3-V-Sensorversorgung (SENSOR_PWR per IO3) ist **keine** Zusatzbeschaltung nötig.

**Datenblatt-Quellen:** AO3401A — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2412061733_Alpha---Omega-Semicon-AO3401A_C15127.pdf`; LCSC-Pinout C15127 — `https://www.lcsc.com/product-detail/mosfets_alpha-omega-semicon-ao3401a_C15127.html`; DMP2035U-7 — `https://www.lcsc.com/product-detail/mosfets_diodes-incorporated-dmp2035u-7_C110499.html`; DMG2301L-7 — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2002181031_Diodes-Incorporated-DMG2301L-7_C102619.pdf`

---

## 6. Gesamttabelle aller geprüften Kandidaten

| # | Zweck | LCSC | Bauteil / Wert | Bauform | Toleranz | Leistung / Temp. | Bestand | $/Stk | basic/expand | JLC-Bestückung |
|---|---|---|---|---|---|---|---|---|---|---|
| 1a | **NTC (Empfehlung)** | **C919175** | Sunlord SDNT2012X104F3950FTF, 100 kΩ, B 3950 K | 0805 | ±1 % / B ±1 % | 200 mW / −55…+125 °C, Imax 0,14 mA | 72.524 | 0,0445 | expand | bestückbar, hier **Handmontage am Kabel** |
| 1b | NTC (kleiner) | C919169 | Sunlord SDNT1608X104F3950FTF, 100 kΩ, B 3950 K | 0603 | ±1 % | 100 mW / −55…+125 °C | 122.302 | 0,0227 | expand | bestückbar (Handmontage) |
| 1c | **Parallel-R2 (Empfehlung)** | **C23254** | 82 kΩ | 0603 | ±1 % | 100 mW / −55…+155 °C | 1.408.937 | 0,0042 | **basic** | ja (0 USD Gebühr) |
| 1d | R2 (Alternative) | C17840 | 82 kΩ | 0805 | ±1 % | 125 mW / −55…+155 °C | 123.326 | 0,0052 | expand (**preferred**) | ja, bei Economic ohne Feeder-Gebühr |
| 1e | **NTC-Stecker** | **C158012** | JST B2B-XH-A, XH 2P aufrecht | THT 2,5 mm | — | 3 A / 250 V / −25…+85 °C | 432.144 | 0,0406 | expand (schon vorhanden) | ja (Menge 3 → **4**) |
| 1f | R_NTC 51 kΩ **entfällt** | C17737 | 51 kΩ (NTC-Stilllegung) | 0805 | ±1 % | 125 mW | 957.221 | 0,0068 | basic | **streichen** |
| 2a | **Sicherung (Empfehlung)** | **C66503** | Littelfuse 0452005.MRL, 5 A träge, 125 V AC/DC, I²t 53,7 A²s | 2410 | — | 50 A@125 V AC/DC, 300 A@32 V DC, −55…+125 °C | 25.526 | 0,2821 | expand | ja (2410-Footprint anlegen) |
| 2b | Sicherung (billiger) | C5220743 | Jinkaisheng 2410 T5A/125V, 5 A träge, 125 V, I²t 58 A²s | 2410 | — | 100 A@125 V AC, UL248-14 | 1.581 | 0,0541 | expand | ja |
| 2c | Sicherung 4 A träge | C5220739 | 2410 T4A/125V | 2410 | — | 100 A@125 V AC | 143 | 0,0523 | expand | ja (knapper Bestand) |
| 2d | Sicherung 1206 (geprüft, **zu klein**) | C2874918 | 1206 3,5 A / 125 V | 1206 | — | I²t 2,2 A²s | 1.147 | 0,0654 | expand | ja, aber 3,5 A zu knapp |
| 3a | **3,3-V-Buck (bleibt)** | **C780769** | AP63203WU-7 (fest 3,3 V, 2 A, 1,1 MHz, Iq 22 µA) | TSOT-23-6 | V_out fest | −40…+85 °C | 25.499 | 1,1794 | expand | ja |
| 3b | einstellbar (**nicht verfügbar**) | C2071868 | AP63200WU-7 | TSOT-23-6 | — | — | **0** (kein Presale) | 1,3437 | expand | ❌ nicht bestellbar |
| 3c | einstellbar (1 Stück) | C5248534 | AP63200QWU-7 | TSOT-23-6 | — | −40…+125 °C | **1** | 0,7597 | expand | ❌ nicht bestückbar |
| 3d | einstellbar (Notreserve) | C2071044 | AP63201WU-7 (PWM-only) | TSOT-23-6 | — | — | 126 | 0,7174 | expand | ⚠️ bestückbar, Bestand zu klein |
| 4a | **R_CB (Empfehlung)** | **C17901** | 100 Ω | 1206 | ±1 % | **250 mW** / −55…+155 °C | 2.913.449 | 0,0066 | **basic** | ja |
| 4b | R_CB (mehr Reserve) | C83143 | 100 Ω | 1210 | ±1 % | **500 mW** / −55…+155 °C | 14.218 | 0,0246 | expand | ja |
| 4c | R_CB (5 %, günstig) | C118845 | 100 Ω | 1206 | ±5 % | 250 mW | 257.649 | 0,0047 | expand | ja |
| 5a | **P-Lastschalter (Empfehlung)** | **C15127** | AO3401A, −30 V, R_DS(on) 85 mΩ @ −2,5 V, V_GS(th) −0,5…−1,3 V | SOT-23 (1 = G, 2 = S, 3 = D) | — | I_D −4,0 A (25 °C) / −3,2 A (70 °C); T_J/T_stg −55…+150 °C | 477.015 | 0,0942 | **basic** | ja |
| 5b | P-Lastschalter (Alternative) | C110499 | DMP2035U-7, −20 V, R_DS(on) 30 mΩ typ / 45 mΩ max @ −2,5 V, V_GS(th) −0,4…−1,0 V, AEC-Q101 | SOT-23 | — | I_D −3,6 A / 810 mW; −55…+150 °C | 114.698 | 0,1297 | expand | ja |
| 5c | P-Lastschalter (Alternative 2) | C102619 | DMG2301L-7, −20 V, 150 mΩ @ −2,5 V | SOT-23 | — | I_D −3 A / 1,5 W | 20.011 | 0,1243 | expand | ja |

*Alle Bestände/Preise/Typen: JLCPCB-Parts-API, Abfrage 16.09.2026. Basic/Extended/„Preferred" gemäß JLCPCB-FAQ („Basic components" = kein Handling, „Preferred Extended Parts" = ohne Feeder-Loading-Fee in der Economic-PCBA, „Extended" = +3 USD).*

### Bestückbarkeit bei JLCPCB — Economic vs. Standard (Gehäuse-Check)

Alle neuen Positionen nutzen **Standard-SMD-Gehäuse** (0603, 0805, 1206, 2410, SOT-23) bzw. das **schon verwendete THT-2,5-mm-Raster** — keine Fine-Pitch-/BGA-Themen, also in beiden Services bestückbar. Die Gebührenlogik (JLCPCB-FAQ, Stand 08.09.2026):

| Neue Position | Gehäuse | Bibliothek | Economic-PCBA | Standard-PCBA |
|---|---|---|---|---|
| `C23254` 82 kΩ (R2) | 0603 | **Basic** | ✅ bestückbar, keine Gebühr | ✅ bestückbar, keine Gebühr |
| `C17737` 51 kΩ (entfällt) | 0805 | Basic | — | — |
| `C17840` 82 kΩ (R2-Alternative) | 0805 | Extended, **preferred** | ✅ bestückbar, **keine** Feeder-Gebühr | ✅ bestückbar, keine Gebühr |
| `C17901` 100 Ω 0,25 W (R_CB) | 1206 | **Basic** | ✅ bestückbar, keine Gebühr | ✅ bestückbar, keine Gebühr |
| `C83143` 100 Ω 0,5 W (Alternative) | 1210 | Extended | ✅ bestückbar, **+3 USD** | ✅ bestückbar, +3 USD |
| `C66503` bzw. `C5220743` Sicherung | **2410** (6,1 × 2,7 mm) | Extended | ✅ bestückbar, **+3 USD** (Standard-SMD-Footprint, in der JLC-Bibliothek vorhanden) | ✅ bestückbar, +3 USD |
| `C15127` AO3401A (Q_SENS) | SOT-23 | **Basic** | ✅ bestückbar, keine Gebühr | ✅ bestückbar, keine Gebühr |
| `C158012` XH-2P (J_NTC) | **THT 2,5 mm** | Extended, „wave soldering" | ✅ **Wellenlöten/Handlötung**: 3,50 USD Handlöt-Gebühr + 0,0173 USD je Lötstelle (2 Lötstellen ⇒ ≈ 0,03 USD) | ✅ dito |
| `C919175`/`C919169` NTC | 0805 / 0603 | Extended | **nicht in der JLC-BOM** — Handmontage am Kabel, lose bei LCSC gekauft | — |
| `C780769` AP63203 | TSOT-23-6 | Extended | ✅ bestückbar (bleibt, +3 USD wie bisher) | ✅ bestückbar |


---

## 7. Konkrete Änderungen an `hardware/pcba_bom_jlc.csv`

| Aktion | Designator | Comment | Footprint | LCSC | Hinweis |
|---|---|---|---|---|---|
| **ändern** | `R_NTC` → **`R_NTC_R2`** | **82k** | 0603 | **`C23254`** | NTC-Parallelwiderstand statt NTC-Stilllegung (51 k) |
| **streichen** | `R_NTC` (bisher) | 51k | 0805 | `C17737` | entfällt mit dem echten NTC |
| **neu** | **`J_NTC`** | JST-XH-2P aufrecht | THT P2.5 | **`C158012`** | Menge J4/J16/J17 von 3 → **4** erhöhen (kein neuer Code) |
| **neu** | **`F1`** | **Fuse 5A T 125V** | SMD 2410 (6,1×2,7 mm) | **`C66503`** | in BAT+ (J1 Pin 3) vor den VBAT-Knoten; +3 USD Handling |
| **ändern** | `R_CB` | 100R | **1206** | **`C17901`** | 0,25 W statt 0,125 W |
| **streichen** | `R_FB3_TOP`, `R_FB3_BOT` | 47k / 15k | 0805 | `C17713` / `C17475` | FB wird direkt an VOUT gelegt (AP63203 = feste 3,3 V) |
| **neu** | **`Q_SENS`** | **AO3401A (P-Kanal)** | SOT-23 | **`C15127`** | Source → +3V3, Drain → SENSOR_PWR, Gate → GPIO; 47 kΩ Pull-up (`R_GATE`, vorhanden) |
| **nicht JLC** | `NTC1` | NTC 100 kΩ B3950 | 0805 (am Kabel) | `C919175` | lose bei LCSC bestellen (1–3 Stück), **Handmontage** im Pack |

**Handling-Kosten:** Die aktuelle `pcba_bom_jlc.csv` hat **18 Extended-Positionen** (≈ 54 USD); **neu** kommt nur die **Sicherung** hinzu ⇒ **19 Positionen ≈ 57 USD**. AO3401A (`C15127`), 82 kΩ (`C23254`) und der 1206-100 Ω (`C17901`) sind **Basic** ⇒ keine zusätzliche Gebühr; der NTC läuft nicht über JLC (lose bestellt).

---

## 8. Geprüft und verworfen (damit es nicht erneut gesucht wird)

* **Selbstrückstellende PTC-Sicherung („Polyfuse") statt Einmalsicherung:** Es gibt viele 1812/1210/1206-Typen mit **2,6 A Halte- / 5 A Auslösestrom bei 16 V** (z. B. `C269148` 2,6 A/16 V, 8371 Stück, 0,0648 $; `C70129` 2,6 A/16 V, 8057 Stück; `C22379949` 1210, 2919 Stück) — **unbrauchbar**, weil der Halte-Strom von 2,6 A unter der normalen Last von 2,8–3,6 A liegt und der Halte-Strom bei erhöhter Umgebungstemperatur zusätzlich abfällt ⇒ Fehlauslösungen im Betrieb. Größere Halte-Ströme (≥ 5 A) bei ≥ 16 V sind in dieser Bauform bei JLCPCB nicht lagernd.
* **1206-Sicherung (kleiner als 2410):** maximal 3,5 A (`C2874918`) bzw. 3 A (`C21261120`) verfügbar ⇒ zu knapp für 3,6 A Dauerlast. Nächste geeignete Bauform ist 2410.
* **AP63200 (einstellbar):** siehe §3 — Bestand 0 / 1 Stück, kein Presale ⇒ **nicht verwenden**.
* **75 kΩ als NTC-Parallelwiderstand** (wäre als Basic/BOM-Wert verfügbar): verschiebt die „zu kalt"-Schwelle auf **−9,2 °C** ⇒ Laden unter 0 °C möglich ⇒ **unzulässig**.
* **2 × 200 Ω 0805 parallel** statt 1206 (beide 125 mW): funktioniert rechnerisch (je 70,6 %), kostet aber eine zusätzliche Position/Netzänderung und bringt gegenüber dem 1206 in Basic keinen Vorteil.

---

## 9. Offene Punkte / Risiken

1. **Lagerbestand ist Momentaufnahme (16.09.2026).** Vor der Bestellung jeden Code erneut über die API prüfen — im Projekt hat sich das bereits mehrfach bewährt (z. B. `C493416` war plötzlich nicht mehr auffindbar).
2. **Sicherung + NTC = Änderungen an Layout und Netzliste** (2410-Footprint, XH-2P, FB-Netz umverdrahten, R_FB3_* löschen) — die Angaben hier sind Bauteilauswahl, keine Layoutfreigabe.
3. **Der NTC muss mechanisch an die Zellen** (nicht nur an die Platine); sonst regelt der Lader die Umgebungstemperatur statt der Zelltemperatur. Kabelbruch/Steckerabzug ist durch die Auslegung fail-safe (Laden aus).
4. **NTC-Toleranz:** Der Sunlord SDNT mit B ±1 % ist spezifiziert; die Schwellen (±1 % R, ±1 % B) verschieben sich um < 1 K — unkritisch.
5. **DC-Abschaltvermögen** ist nur bei der Littelfuse-452-Serie datenblattbelegt; die Jinkaisheng-Alternative nennt nur AC-Werte (bei 8,4 V DC praktisch unkritisch, aber nicht dokumentiert).
6. **Preise** sind JLCPCB-PCBA-Stückpreise in USD (1er-Staffel), ohne USt./Versand; EUR-Umrechnung nicht enthalten.

---

## 10. Quellen (alle am 16.09.2026 abgerufen)

**API:** `POST https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList/v2` (Keyword = LCSC-Code/MPN) — Bestand, Preis, `componentLibraryType`, `preferredComponentFlag`, Bauform, Datenblatt-URL je Position.

**Datenblätter:**
* IP2326 V1.11 (Injoinic) — `https://www.lcsc.com/datasheet/lcsc_datasheet_2304062030_INJOINIC-IP2326_C2832094.pdf` (§9 NTC-Schwellen + Beispiel 100 k/B4100 ∥ 82 k)
* AP63203/AP63200 DS41326 Rev 3-2 (Diodes, 11/2024) — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2201131130_Diodes-Incorporated-AP63203WU-7_C780769.pdf` (Bild 20/21, Pin Descriptions, „Fixed Output Voltage")
* AO3401A Rev 3.1 (AOS) — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2412061733_Alpha---Omega-Semicon-AO3401A_C15127.pdf`
* Sunlord SDNT-Serie (Chip NTC Thermistor, Rev 2021/05/15) — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2110081730_Sunlord-SDNT2012X104F3950FTF_C919175.pdf`
* Littelfuse NANO2 Slo-Blo 452/454 (Rev 11/23/16) — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2304140030_Littelfuse-0452005-MRL_C66503.pdf`
* Jinkaisheng 2410 SA/B/CT (A/2) — `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2210271630_Shenzhen-Jinkaisheng-Elec-2410-T5A-125V_C5220743.pdf`

**Produktseiten / Regeln:**
* LCSC-Pinout AO3401A (Bildbeschreibung „D3 G1 S2"): `https://www.lcsc.com/product-detail/mosfets_alpha-omega-semicon-ao3401a_C15127.html`
* LCSC DMP2035U-7: `https://www.lcsc.com/product-detail/mosfets_diodes-incorporated-dmp2035u-7_C110499.html`
* LCSC DMG2301L-7: `https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2002181031_Diodes-Incorporated-DMG2301L-7_C102619.pdf`
* JLCPCB FAQ „Basic/Preferred/Extended" (3 USD je Extended-Position; Preferred = ohne Feeder-Gebühr in Economic-PCBA): `https://jlcpcb.com/help/article/pcb-assembly-faqs`

**Projekt-Dateien (Kontext):** `hardware/pcba_bom_jlc.csv`, `hardware/pcba_verfuegbarkeit_jlc.md`, `hardware/schaltplan_v1.md` (§6.3 Balancing, §9.4 Load-Switch, §12 Pumpen/Sensorik)
