# Review „2S-Umbau" — Ausführliche Prüfung der neuen Schaltung (16.09.2026)

Gegenstand: der lokal geänderte Schaltplan (`hardware/schaltplan_v1.md` §1–§6, §13 +
`hardware/schaltplan_v1_netzliste.csv` + `hardware/pcba_bom_jlc.csv`).
Auftrag: 1S → 2S, IP2326-Lader über USB-C, Step-Ups weg, Step-Down für den ESP32, ggf. 5 V für Sensoren,
**alle Bauteile bei JLCPCB verfügbar**.

## 1. Prüfmethode (3 Durchgänge, jeder mit anderem Werkzeug)

1. **Auslegung gegen Datenblätter** — jede Zahl aus einem Datenblatt oder aus einer Rechnung, mit Quelle.
   Datenblätter selbst geladen und als Text extrahiert: IP2326 V1.11 (17 S.), SY8113B (AN, 10 S.),
   AP63203 (DS41326, 18 S.), TPS3839 (SBVS193D, 34 S.), ME6211, MT3608, MAX809. Bei den beiden
   Stellen, die im Datasheet nur als **Bild** vorliegen (Applikationsbild IP2326, Pin-Tabelle AP63203),
   wurde die Seite gerendert und angesehen — das Ergebnis ist als „am Bild geprüft" markiert.
2. **Maschinenlesbare Artefakte** — Netzlisten-Lint (`scripts/check_netlist.py`) und Querabgleich
   Schaltplan ↔ BOM ↔ Netzliste (`scripts/check_bom_consistency.py`), beide **exit 0**.
   Die BOM wurde nicht per Hand getippt, sondern aus der Netzliste erzeugt und **bidirektional**
   geprüft (jeder Ref genau einmal, `Menge` = Anzahl Refs, Testpunkte/J6 nicht bestückt).
3. **Querabgleich aller Dokumente** — Konsistenz von Versorgungskette, Bauteiltabellen,
   Bestellliste und Textbeschreibung (Zählungen: 68 Netze · 115 Bauteile · 314 Verbindungen ·
   109 bestückte Refs). Alte Angaben sind als Historie markiert (§10/§12).

## 2. Die neue Kette in Zahlen

| Schiene | Bereich | Quelle | Bemerkung |
|---|---|---|---|
| VBUS | 5 V (±5 %) | USB-C-Netzteil | Ladung **und** Programmierung über **eine** Buchse |
| VBAT | **6,0 … 8,4 V** | 2S-Pack | „6,0" = Wächter-Schwelle 6,16 V, darunter wird abgeschaltet |
| +5V | **5,10 V** | SY8113B-Buck, 3 A | beide Pumpen + J17; V_out = 0,6 × (1 + 75/10) |
| +3V3 | **3,31 V** | AP63203-Buck, 2 A | Modul (3,0–3,6 V erlaubt), Sensorik, LEDs, VCC_EXT |
| Ladestrom | **0,90 A** (±10 %) | IP2326, R_ISET = 100 k | 0,6 C bei 1500-mAh-Pack |
| Ladeschluss | **8,4 V** (8,3–8,5 V) | IP2326, VSET offen | 4,2 V/Zelle |
| UV-Abschaltung | **6,16 V** (6,10–6,28 V) | TPS3839 + 200 k/200 k | 3,08 V/Zelle |
| ADC Packspannung | 8,4 V → **2,13 V** | Teiler 200 k/68 k | 12-Bit, 12-dB-Bereich (0–3,3 V) |
| Ruhestrom (Standby) | **≈ 182 µA** | 100 + 22 + 31,5 + 21 + 7 + 0,15 | = 4,4 mAh/Tag ≈ 0,29 %/Tag bei 1500 mAh |

## 3. Bauteil-Auswahl: jedes neue Teil mit Beleg und JLC-Status

Live gegen die JLCPCB-Parts-API geprüft (16.09.2026), **alle lagernd**:

| Pos | Bauteil | LCSC | Paket | Typ | Lager | $/Stk | Datenblatt-Anker |
|---|---|---|---|---|---|---|---|
| U_CHG | IP2326 | `C2832094` | VQFN-24-EP 4×4 | extended | 18.074 | 0,6182 | 2S/3S-Boost-Lader, ICHG = 90000/R_ISET, VOUT→Akku+, VSYS = Zwischenknoten, kein Power-Path, Balancing nur 2S |
| U7 | TPS3839G33DBZR | `C485802` | SOT-23-3 | extended | 3.502 | 0,4458 | V_IT 3,003–3,126 V, Hysterese 31 mV, **Iq 150 nA**, Push-Pull (2 mA @ V_OL ≤ 0,4 V), 200 ms Reset-Delay |
| U_BUCK5 | SY8113B ADC | `C78989` | TSOT-23-6 | extended | 50.655 | 0,2403 | 3 A, 4,5–18 V, 500 kHz, V_REF 0,6 V ±1,5 %, **Iq 100 µA**, Valley-Limit 3 A / Peak 6 A |
| U_BUCK3 | AP63203WU-7 | `C780769` | TSOT-23-6 | extended | 25.645 | 1,1794 | 2 A, 3,8–32 V, 1,1 MHz, V_REF 0,8 V ±1 %, **Iq 22 µA** |
| L_CHG | MHCI04020-2R2M-R8 | `C142096` | 4,6 × 4,1 mm | extended | 3.096 | 0,2538 | 2,2 µH, **Isat 5,0 A**, Irms 3,0 A, DCR 58 mΩ |
| L_BUCK5/3 | PRS6045-4R7MT | `C105660` | 6 × 6 mm | extended | 1.571 | 0,0776 | 4,7 µH, **Isat 4,0 A**, DCR 31 mΩ |
| R_ISET | 100 kΩ 1 % | `C96346` | 0805 | expand | 853.728 | 0,0094 | 1 % ist vom Datenblatt gefordert |
| R_NTC | 51 kΩ | `C17737` | 0805 | **base** | 958.911 | 0,0068 | „ohne NTC 51 k nach GND" |
| R_UVSET | 68 kΩ | `C17801` | 0805 | **base** | 348.040 | 0,0037 | Eingangs-Unterspannung 4,35 V |
| R_EN_CHG | 100 kΩ | `C96346` | 0805 | expand | — | — | EN-Pull-up (kein GPIO nötig) |
| R_VIN_CHG | 0,5 Ω | `C28319` | 0805 | expand | 15.532 | 0,0054 | Bild-Beleg: in Reihe zum VIN-Pin |
| C_CHG_* | 3 × 10 µF 25 V | `C15850` | 0805 | **base** | 6,5 Mio | 0,0843 | Datenblatt-BOM (C1/C3/C6/C7), >16 V gefordert |
| C_VSYS_A/B | 2 × 22 µF 25 V | `C45783` | 0805 | **base** | 4,7 Mio | 0,2431 | „2× 22 µF direkt am VSYS-Pin" |
| C_B* | 7 × 22 µF 25 V | `C45783` | 0805 | **base** | — | — | Buck Ein-/Ausgänge |
| C_B*_BST | 4 × 100 nF | `C49678` | 0805 | **base** | 17,9 Mio | 0,0194 | Bootstrap (0,1 µF) |
| R_FB5/3, R3a/R3b, R_SENSE | 75k/10k, 47k/15k, 200k/68k | `C17819`, `C17414`, `C17713`, `C17475`, `C17539`, `C17801` | 0805 | **base** | alle > 300 k | ≤ 0,0068 | bewusst auf Basic-Werte gelegt (§7.1) |
| J17 | JST-XH 2P | `C158012` | THT aufrecht | extended | 434.009 | 0,0406 | 5-V-Ausgang für Sensorik |

**Handling-Kosten:** **17 Extended-Positionen** ≈ 51 USD (vorher 12 ≈ 36 USD) + Platinenfertigung.
Sparpotenzial: U_BUCK3 (1,18 $) ist das teuerste neue Teil — Alternativen in §7.

## 4. Harmonie-Prüfungen (das eigentliche „passt das zusammen?")

### 4.1 Lader ↔ Akku
- Ladeschluss 8,4 V (VSET offen, 8,3–8,5 V) = **4,2 V/Zelle** ✓ Li-Ion-Standard. ⚠️ Die Variante
  **IP2326_8V8 lädt auf 8,8 V (4,4 V/Zelle)** — für Li-Ion **unzulässig**, bei der Bestellung achten.
- Ladestrom 0,90 A bei 1500-mAh-Pack = **0,6 C** ✓ (Li-Ion erlaubt 1 C). Bei 2500 mAh = 0,36 C ✓.
- Der Ladestrom sinkt automatisch: <6 V nur 100 mA, <3,7 V nur 50 mA → ein tiefentladener Pack wird
  nicht mit 0,9 A „geschockt" ✓.
- **Terminierung:** Stopp bei I < 200–300 mA; danach Wiedereinschaltung erst unter 8,0 V ✓
  (kein „Nachladen im Sekundentakt").
- **Balancing:** der Lader könnte (Pins 23/24, V_CBON 4,1 V, I_CB < 40 mA), ist aber **unbeschaltet**.
  **Präzisiert am 16.09.2026:** Pflicht ist ein Pack mit **Zellschutz-PCM** (schützt *pro Zelle*
  gegen Überladung); fehlendes Balancing kostet dann **Kapazität und Lebensdauer**, ist aber kein
  Brandrisiko — die schärfere Aussage des ersten Entwurfs ist damit korrigiert. Die drei
  Balancing-Wege (a/b/c) samt Verdrahtung stehen in `hardware/schaltplan_v1.md` §6.3.

### 4.2 Lader ↔ USB-Eingang
- Ausgang 7,56 W; bei 94 % → **1,61 A** Eingangsstrom. Mit beiden Pumpen (0,6 A @ 5 V) sind es
  2,2 A → **5-V-Netzteil mit ≥ 2,5 A** nötig. Der IP2326 hat eine Eingangs-Regelschleife und senkt
  den Ladestrom selbst, wenn V_USB unter 4,35 V fällt (R_UVSET 68 k) → ein schwaches Netzteil
  bricht nicht ab, es lädt nur langsamer ✓.
- **Kein Fast-Charge** (DP/DM offen): die 15-W-Fähigkeit bleibt ungenutzt; mehr geht nur mit
  einem zweiten USB-Port für den Lader (dann D+/D− frei). Bewusst so entschieden (§13.2).

### 4.3 Lader ↔ Last (⚠️ der einzige echte Kompromiss)
- Der IP2326 hat **keinen Power-Path**: alles läuft aus dem Akku, auch beim Laden. Beim Pumpen
  während des Ladens deckt der Lader die Last nicht — er reduziert den Ladestrom; im Extremfall
  verlängert sich das Laden, es entsteht aber kein Schaden. Betriebsregel: **möglichst nicht pumpen,
  während geladen wird** (bereits vorher im Projekt so dokumentiert).
- Wer Power-Path will: **BQ25886RGER** (`C2765094`, VQFN-24, 6.948 lagernd, ~1,75 $) ist der einzige
  **standalone-2S-Boost-Lader mit Power-Path ohne I²C** — als V2-Option notiert (§7.3).

### 4.4 5-V-Buck ↔ Pumpen
- Nennlast: Dosierpumpe 0,4 A + Sauerstoffpumpe 0,2 A = 0,6 A; Buck kann **3 A** ✓ (5× Reserve).
- **Anlaufstrom 3 A**: Rippel 0,85 A_pp bei 8,4 V Eingang ⇒ Spitzenstrom **3,43 A**, Induktivität
  **Isat 4,0 A** ✓ — aber nur **0,57 A (14 %) Reserve**, und die Valley-Stromgrenze des IC liegt
  bei **min. 3,0 A**. Der Softstart (≤1 A) ist deshalb **weiterhin empfohlen**, auch wenn er nicht
  mehr „Pflicht" ist wie beim alten 2-A-Boost. **Messauftrag §8.2.**
- „EMI"-Kondensatoren C11/C20 an den Klemmen + 100 µF C3 auf der Schiene ✓ (der Elko sitzt jetzt dort,
  wo der Motorstrom fließt — vorher lag er auf VBAT, das war nach dem Boost-Umbau die falsche Seite).
- Freilaufdioden D1/D7 gegen **+5V** ✓, Sperrspannung 40 V ≫ 5,1 V ✓.

### 4.5 3,3-V-Buck ↔ Modul
- 2 A Nennstrom gegen 382 mA TX-Peak (Espressif fordert ≥ 500 mA) ✓ **4× Reserve**.
- Ausgang **3,31 V** liegt im erlaubten Bereich 3,0–3,6 V ✓ (0,3 % unter 3,3 V).
- ⚠️ **Der ADC des C6 nutzt V_DD33 als Referenz** — die drei ADC-Messungen skalieren minimal mit der
  Rail. Da der Teiler und die Sensoren von **derselben** Rail gespeist werden, hebt sich der Fehler
  bei Feuchte/Licht praktisch auf; die Packspannungsmessung verschiebt sich um die Rail-Toleranz
  (≤ 2 %) — für die Pumpstopp-Schwellen irrelevant (Abstand zur 6,16-V-Grenze ≫ 2 %).
- **Rauschen:** der Buck schaltet mit 1,1 MHz; die ADC-Eingänge haben 1 kΩ + 100 nF (τ = 0,1 ms) ⇒
  60 dB Dämpfung bei 1,1 MHz. Ein Restwelligkeits-Anteil bleibt Messthema (§8.4).

### 4.6 Wächter ↔ 2S-Pack
- Teilung 1:2, Schwelle 3,08 V ±1 % ⇒ Auslösung **6,10–6,22 V**; Iq-Offset 150 nA × 200 kΩ = **30 mV**;
  Hysterese 31 mV (≈ 62 mV Pack) ✓ saubere Schaltflanke.
- **Wirkung:** (a) Buck-EN low ⇒ 5-V-Schiene **echt 0 V** (beim Boost gab es einen Pfad über L1/D6,
  hier nicht) und (b) D3/D8 klemmen beide Gates. Erstmals sind **beide** Sperren wirksam — der alte
  Klemmzweig war es nicht (§5, Befund 1).
- **Ausgangsstrom:** im Fehlerfall 2 × 0,30 mA (Klemmzweige) + EN-Leckstrom ⇒ ~0,6 mA ≪ 2 mA
  (V_OL-Spec) ✓.
- **Nebenwirkung:** nach dem Einschalten startet die 5-V-Schiene erst nach den **200 ms Reset-Delay**
  — die Firmware muss darauf warten (§8.5).

### 4.7 ADC-Teiler ↔ ADC-Bereich
- Max. 2,13 V bei 8,4 V; 1,56 V bei der Abschaltschwelle. 12 Bit über 3,3 V ⇒ 0,81 mV/Count
  ⇒ **3,2 mV Packauflösung** (1,6 mV/Zelle) — feiner als jede benötigte Schwelle ✓.
- Teilerstrom 31,5 µA ist im Standby-Budget enthalten. Warum 200 k/68 k und nicht „exakt 1:4"
  (300 k/100 k): beide sind **Basic**-Werte, 300 k/100 k wären zwei Extended-Positionen (§7.1).
- ⚠️ Der 8,4-V-Grenzfall liegt mit 2,13 V **unter** der 3,3-V-Überfahrgrenze — der alte 1:2-Teiler
  hätte hier **4,2 V** geliefert und den ADC überfahren (Befund 4, §5).

### 4.8 Thermik (gerechnet, nicht gemessen)
| Teil | Verlust | θ_JA / Gehäuse | ΔT |
|---|---|---|---|
| IP2326 @ 0,9 A | ≈ 0,45 W (6 % von 7,6 W + 0,1 W Eigenbedarf) | 60 °C/W (QFN-24 + EPAD) | **≈ +27 K** → EPAD zwingend über Vias anbinden |
| SY8113B @ 0,6 A | ≈ 0,2 W | 100 °C/W | ≈ +20 K |
| AP63203 @ 0,15 A | < 0,06 W | 89 °C/W | < +6 K |
| Elko C3 | — | 16 V Typ an 5,1 V | unkritisch |
Damit ist die frühere Sorge „LDO verheizt bei 5 V → 3,3 V" konstruktiv ausgeräumt (der ME6211 hätte
bei 0,15 A **0,26 W** in SOT-23-5 abgeführt und durfte laut Datenblatt nur **6,0 V** Eingang sehen).

### 4.9 Ruhestrom / Laufzeit
- **182 µA** Standby = **4,4 mAh/Tag** = **0,29 %/Tag** auf einem 1500-mAh-2S-Pack.
  Gegenüber dem 1S-Stand (70 µA) hat sich der Ruhestrom **verdoppelt**, aber die Energie im Pack
  ebenfalls — die Laufzeit bleibt praktisch gleich.
- Dominanter Posten ist der **Iq des 5-V-Bucks (100 µA)**. Sparoption (V2): EN dieses Bucks per GPIO
  nur während des Pumpens freigeben → ~80 µA gespart, dafür Firmware-Timing nötig.

## 5. Gefundene Fehler (mit Schweregrad und Status)

| # | Befund | Schwere | Status |
|---|---|---|---|
| 1 | **Klemmzweig der Pumpen war wirkungslos** (Altstand): `R_CLAMP1/2` lagen **parallel** zu D3/D8, und der Knoten `KLAMP1/2` hing an **keinem** Gate — die Hardware-Unterspannungsklemmung konnte nichts tun. Der Netzlisten-Lint sieht das nicht. | **hoch** (Sicherheitsfunktion fehlt) | **behoben** im neuen Plan: Serienkette Gate → 10 kΩ → Diode → RESET_UV. Beim EasyEDA-Neuaufbau mitziehen (der IR-Stand 15.09. trägt den Fehler) |
| 2 | **ADC-Teiler 1:2 war für 2S überfahren** (4,2 V an einem 3,3-V-ADC) — wäre beim bloßen Zellwechsel entstanden | hoch | behoben: 1 : 3,94 (200 k/68 k) |
| 3 | **MAX809 nicht 2S-tauglich**: V_DD,max 5,5 V und Iq 12 µA — an einem 200-kΩ-Teiler hätte allein der Iq den Schwellwert um **2,4 V** verschoben | hoch | behoben: TPS3839 (150 nA, V_DD bis 6,5 V) |
| 4 | **ME6211 hätte an VBAT nicht betrieben werden dürfen** (V_IN,max 6,0 V laut LCSC-Daten) | hoch | behoben: LDO ersetzt |
| 5 | **Alte Boost-Induktivität L1 22 µH hatte nur 2,05 A Sättigungsstrom**, der MT3608 zieht bis 2 A Schalterstrom | mittel | entfällt mit dem Boost ersetzt (jetzt 4,0 A Isat) |
| 6 | **Prüfwerkzeug-Lücke:** Beide Prüfer kannten den Designator-Präfix **`L`** nicht — Induktivitäten wurden **nie** gegen BOM/Dokument geprüft | mittel | behoben (beide Skripte geeicht, 16.09.2026) |
| 7 | **Netzname `SW_5V` wurde als Bauteil fehlinterpretiert** (Designator-Muster `SW…`) | niedrig | behoben: Netze heißen jetzt `LX_5V`/`LX_3V3` |
| 8 | **Design-Prüfsuite (`hardware/design/`) war nicht lauffähig** (`circuit.py` fand einen Kennwert in `bom_entscheidung.md` nicht) und rechnete auf 1S | mittel | **behoben (16.09.2026):** Suite auf 2S umgestellt (**37 Prüfungen, Exit 0**), fünf 1S-Prüfungen ersetzt, 14 neue; **Mutationstest 10/10** (`hardware/design/MUTATIONSTEST.md`) |
| 9 | Dokumentationsreste (J14-Tabelle in §9.1) | niedrig | behoben |

## 6. Bewusst **nicht** geändert (Entscheidungen mit Grund)

1. **Kein Power-Path** — der Auftrag nennt den IP2326; ein Power-Path-Lader wäre ein anderes IC
   (BQ25886, §7.3) und hätte das Konzept geändert. Betriebsregel bleibt „nicht pumpen während Laden".
2. **Kein Balancing on-chip** — wir bleiben beim 2-poligen Akku-Stecker; der Pack muss balancieren.
   Der IC könnte es, dann braucht es einen 3-poligen Stecker + R_CB (100 Ω) + 2 × 100 nF.
3. **+3V3 hängt nicht am Wächter** — der MCU soll unter Unterspannung **melden** können, nicht blind
   ausgehen. Damit zieht das System im Wächterzustand weiter ~160 µA aus dem Pack (PCM = letzte Ebene).
4. **Kein Fast-Charge über DP/DM** — die Datenleitungen gehören dem ESP32 (USB-Serial-JTAG).
5. **PWM-Softstart bleibt empfohlen** (nicht mehr Pflicht) — thermisch und für den Akku-Einbruch.
6. **`J17` (5 V für Sensorik) ohne Lastschalter** — reine Ausgangsbuchse, der Buck begrenzt den Strom.
   Die Sensorversorgung selbst bleibt bei 3,3 V über IO3 (Stromsparen).

## 7. Alternativen mit Zahlen (falls etwas umentschieden wird)

1. **Kosten sparen:** die Feedback- und Teilerwerte sind bewusst auf **Basic**-Werte gelegt
   (75 k/10 k ⇒ 5,10 V; 47 k/15 k ⇒ 3,31 V; 200 k/68 k ⇒ 1:3,94). Mit E96-Werten wären es drei
   Extended-Positionen mehr (≈ 9 USD Handling) — nicht sinnvoll.
2. **Lader-Alternativen** (alle live geprüft, lagernd): **IP2325** `C605434` (ESOP-8, 12.750 Stk,
   0,43 $, max ~1,3 A, ohne Balancing-Pins) — die günstigste Variante, wenn 0,9 A genug sind;
   **IP2320** `C19191089` (ESOP-8, 5.901 Stk, 0,28 $, **nur 1 A**); ⚠️ **IP2326_NPD** nur für
   Ladeströme **< 700 mA** gedacht — bei 0,9 A ist das Standard-IP2326 richtig.
3. **Power-Path:** **BQ25886RGER** `C2765094` (VQFN-24, 6.948 Stk, ~1,75 $) — standalone, kein I²C.
   Der V2-Weg, wenn „pumpen während des Ladens" Pflicht wird.
4. **Balancing on-board:** **ETA3000D2I** `C7465544` (5.716 Stk, 0,38 $) ist ein reiner
   2-Zellen-Balancer (kein Lader) — Option, falls der Pack kein eigenes BMS hat.
5. **Mehr Pumpen-Reserve:** statt SY8113B (3 A) den **SY8205** `C111875` (SOIC-8, 28.240 Stk, 0,45 $,
   **5 A**) — größere Bauform, dafür deckt er auch einen ungebremsten 3-A-Anlauf sicher ab.
6. **3,3-V-Rail:** AP63203 (1,18 $, 22 µA Iq) ist teurer als ein zweiter SY8113B (0,24 $), hat aber
   **5× weniger Eigenstrom** — bei einem Akkugerät der bessere Tausch.

## 8. Offene Punkte und Messaufträge

1. **Akku-Pack**: konkrete Kandidaten gefunden (**Keeppower 2S1P 2×18500 2000 mAh, 10,90 €** bzw.
   **2×18650 3400 mAh, 14,90 €**, akkuteile.de — Schutz dokumentiert, **Balancing nicht**;
   `research/bom-check/10_2s-akku-quellen.md`). Zu entscheiden: (a) Pack mit Schutz nehmen und das
   Balancing dem Pack überlassen, oder (b) 2 Zellen + 2S-BMS-Board mit Balancer und den Mittelabgriff
   über die in §6.3 beschriebene Ergänzung nutzen (J1 dann 3-polig). **Mechanik:** Rundzellenpack
   18,5 × 103 mm statt flachem 5-mm-Pouch → Einbauort/Wulst in `docs/02` + `cad/params.py` nachziehen.
2. **Pumpenanlauf ohne Softstart messen** (Stromzange): entscheidet, ob 3 A sicher innerhalb
   Isat/Stromgrenze bleiben oder ob der Softstart Pflicht zurückkommt.
3. **Eingangsstrom bei 5 V messen** (Laden + Pumpen): bestätigt die ≥2,5-A-Netzteilanforderung und
   ggf. die Wahl R_ISET = 100 k.
4. **ADC-Rauschen mit dem Buck messen** (Feuchte/Licht/Pack) — entscheidet, ob eine zusätzliche
   RC-/Ferrit-Filterung der Sensorspeisung nötig wird.
5. **5-V-Schiene nach Kaltstart** messen (200 ms Wächter-Delay + 800 µs Buck-Softstart) → gehört als
   Wartezeit in die Firmware; außerdem ADC-Faktor **4** statt 2 und neue Schwellen (Warnung ~7,0 V,
   Pumpstopp ~6,8 V Pack).
6. ✅ **Design-Prüfsuite auf 2S umgestellt (16.09.2026, erledigt):** 37 Prüfungen, `exit 0`;
   neu u. a. `check_ladestrom_ip2326`, `check_ladeschluss_2s`, `check_buck5/3_ausgang`,
   `check_buck*_induktivitaet`, `check_uvlo_schwelle`, `check_waechter_sinkstrom`,
   `check_adc_teiler_max`, `check_buck_en_pegel`, **`check_klemmzweig_serie`** (Regressionsschutz
   für Befund 1), **`check_kein_low_vin_am_vbat`** (ME6211-Lektion als Test), `check_standby_budget`,
   `check_system_quellen`. Nachweis: **10 von 10 Mutationen werden gefangen**
   (`hardware/design/mutation_cases_2s.json` + `MUTATIONSTEST.md`).

   *Restpunkt:* die Firmware-Schwellen in `bom_entscheidung.md` §4b sind weiterhin **pro Zelle**
   angegeben (3,5/3,4 V) — die Suite verdoppelt sie korrekt auf 7,0/6,8 V Pack; sobald die echten
   PCM-Werte des neuen Packs bekannt sind, dort nachtragen.
7. **EasyEDA-Neuaufbau** (eigener Schritt): Geräte-Identitäten der 4 neuen ICs auflösen, IR bauen,
   Netzklassen/Layout-Input neu erzeugen, `pcb import-changes` — erst danach Layout.

## 9. Grenzen dieses Reviews

- **Nichts davon ist gemessen.** Alle Aussagen stammen aus Datenblättern, Rechnungen und der
  JLC-API (Lager/Preise zum 16.09.2026). Die Zahlen in §4.8 (Thermik) und §4.9 (Ruhestrom) sind
  Rechnungen mit benannten Annahmen.
- **Nicht geprüft:** EMV-Verhalten des 1,1-MHz-Bucks, reale ADC-Störfestigkeit, Langzeit-Drift,
  und die Pin-Footprints der neuen IC-Gehäuse (am Bild geprüft, nicht am Footprint).
- Der **VSYS-Knoten** ist bewusst nur kapazitiv beschaltet und nicht mit BAT+ verbunden (Datenblatt:
  „Zwischenknoten … 2× 22 µF direkt am Pin"). Falls die Messung ein anderes Verhalten zeigt, ist die
  externe Verbindung eine Lötbrücke (als Messauftrag in `schaltplan_v1.md` §6.7 notiert).
