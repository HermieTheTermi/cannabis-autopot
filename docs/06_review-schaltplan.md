# Review: Schaltplan V1

Stand: 11.09.2026 · Geprüft: `hardware/schaltplan_v1.md` gegen die Herstellerdatenblätter
(Espressif ESP32-C6-MINI-1 + Hardware Design Guidelines, Microchip MCP73831, Microne ME6211,
Maxim MAX809, Alpha&Omega AO3400A, Heketai 1N5819WS, ST USBLC6-2SC6).

**Ergebnis: 2 Fehler gefunden und behoben, 5 Schwachstellen entschärft, 7 Punkte dokumentiert
oder als Option hinterlegt.** Der Plan ist damit bestell- und layoutfähig — die unten genannten
offenen Punkte (Pinbelegungs-Bilder, Power-Path-Entscheidung) bleiben bewusst offen.

---

## 1. Fehler (behoben)

### F1 🔴 Klemmzweig zog mehr Strom, als der MAX809-Ausgang liefern darf
- **Befund:** Datenblatt MAX809: „RESET Output Voltage Low … **ISINK = 1,2 mA**, MAX803R/S/T/Z,
  MAX809R/S/T/Z" (nur die L/M/J-Varianten sind mit 3,2 mA spezifiziert). Meine erste Auslegung
  hatte R1 = 1 kΩ → im Sperrfall (MCU will pumpen, Wächter sperrt) flossen
  (3,0 V − 0,3 V) / 1 kΩ = **3 mA** — das 2,5-fache des spezifizierten Werts. Folge wäre ein
  angehobener RESET-Pegel (im schlimmsten Fall oberhalb der MOSFET-Schwelle) und eine
  Überlastung des Ausgangs.
- **Korrektur:** R1 = **4,7 kΩ** → **0,57 mA**; VOL bleibt sicher ≤ 0,3 V, also klar unter
  VGS(th) = 0,65 V (min) des AO3400A.
- **Folgekorrektur:** R2 von 10 kΩ auf **47 kΩ**, weil R1/R2 sonst einen Spannungsteiler bilden:
  mit 1 kΩ + 10 kΩ käme am Gate nur 3,0 V an (bei 4,7 kΩ + 10 kΩ wären es 2,24 V — unter dem
  2,5-V-Spec-Punkt des MOSFET). Mit 4,7 kΩ + 47 kΩ sind es **3,0 V** Gate-Ansteuerung, und ein
  unbestückter MCU-Ausgang entlädt das Gate in ~30 µs.

### F2 🔴 Status-LED hing an einem Strapping-Pin (MTMS)
- **Befund:** IO4 ist laut Espressif-Pinliste **MTMS** („MTMS, GPIO4, LP_GPIO4, ADC1_CH4,
  FSPIHD") und gehört zu den **Strapping-Pins** (GPIO8, GPIO9, GPIO15, MTMS, MTDI). Mein
  LED-Zweig an IO4 hätte den Pin über LED + 1 kΩ nach GND gezogen — ein strapping-relevanter
  Pegel zur Boot-Zeit.
- **Korrektur:** LED auf **IO14 (Pin 19)** — kein Strapping-, kein ADC-, kein USB-Pin.

## 2. Schwachstellen (behoben)

### F3 🟠 JLC-BOM war nicht synchron zum Schaltplan
- **Befund:** In der CSV fehlten die 4,7-µF-Kondensatoren des Laders, 3,9/4,02 kΩ, der
  LED-Vorwiderstand, R6 sowie die korrekten Stückzahlen (100 nF 4×, 1 µF 2×, 1 kΩ 3×, 10 kΩ 3×).
  Damit hätte die Bestellung unvollständig werden können.
- **Korrektur:** `pcba_bom_jlc.csv` **komplett neu aus dem Schaltplan erzeugt** (41 Designatoren,
  27 Wert-Zeilen). Gegenprobe per Skript: **kein Designator des Schaltplans fehlt in der CSV.**
  Dabei gleich drei Positionen auf **Basic**-Werte umgestellt (R_PROG 3,9 kΩ statt 4,02 kΩ,
  4,7 µF über `C1779`, LED-Vorwiderstände 1 kΩ) → **10 Extended-Positionen (30 $)** statt 13.

### F4 🟠 LDO-Eingangskondensator zu klein für 382-mA-Spitzen
- **Befund:** ME6211 verlangt min. 1 µF am Eingang — erfüllt. Espressif fordert aber zusätzlich
  **≥ 10 µF am Leistungseingang**; bei fast leerer Zelle (3,4 V) und einem TX-Burst von 382 mA
  kann die 3,3-V-Schiene sonst einbrechen (Brownout).
- **Korrektur:** C5 von 1 µF auf **10 µF** erhöht.

### F5 🟠 Kein Schutz am ADC-Pin, wenn der Sensor unbversorgt ist
- **Befund:** Der Sensor wird per GPIO abgeschaltet; seine AOUT-Leitung hängt dann mit
  möglicherweise angelegter Spannung am ADC-Pin (Strominjektion über die Schutzdiode).
- **Korrektur:** **R6 = 1 kΩ in Reihe** vor den ADC-Pin.

### F6 🟡 Laderegler ohne Power-Path — Laden während des Pumpens
- **Befund:** Der MCP73831 hat keine Power-Path-Funktion. Pumpe (450 mA) und Ladevorgang
  (256 mA) ziehen gleichzeitig aus demselben VBAT-Knoten; der Lader deckt den Pumpenstrom nicht,
  die Zelle liefert den Rest. Kritischer: die **Ladeabschaltung** (Terminierung bei ~5 % von
  IREG) kann durch eine dauerhafte Last auf VBAT verhindert werden → der Lader bleibt in der
  CV-Phase.
- **Korrektur (dokumentiert, nicht behoben):** Firmware-Regel **„nicht pumpen, solange VBUS
  anliegt"** bzw. Pumpen nur im Akkubetrieb. Kein Bauteil-Aufwand; für ein Gerät, das man alle
  Wochen lädt, akzeptabel. Ein Power-Path-Lader (z. B. BQ24074) wäre die Alternative.

### F7 🟡 Brownout-Gefahr gegen Ende der Entladung
- **Befund:** Bei VBAT ≈ 3,4 V und 382 mA TX-Spitze addieren sich LDO-Dropout und Innenwiderstand
  der Zelle; die 3,3-V-Schiene kann unter die 3,0-V-Minimalgrenze des Moduls rutschen.
- **Korrektur (dokumentiert):** C5 10 µF (siehe F4) verschafft Reserve; die Firmware muss den
  **Alarm spätestens bei ~3,5 V** absetzen, nicht erst bei 3,4 V, damit das Senden noch im
  sicheren Bereich liegt.

## 3. Dokumentiert / als Option hinterlegt (kein Fehler)

| # | Punkt | Einordnung |
|---|---|---|
| F8 | **VBAT-Teiler kostet 10,5 µA Dauerstrom** und dominiert damit den Standby (Modul 7 µA, LDO 40 µA, MAX809 12 µA ≈ 70 µA gesamt) | Wenn das stört: Teiler über GPIO schaltbar machen oder 2 × 1 MΩ (dann ist C10 Pflicht) |
| F9 | **Keine grüne 0805-LED bei JLC lagernd** (geprüft) | Lade-LED nutzt denselben roten Typ (`C84256`, Basic) — sonst wäre eine Extended-Position fällig. Alternative: STAT auf einen freien GPIO und Ladestatus per Telegram |
| F10 | **IO0/IO1 sind XTAL_32K_P/N** (Alternativfunktion 32,768-kHz-Quarz) | Nutzung ist zulässig, weil die Modul-Referenzschaltung X1 ausdrücklich als **„NC: No component"** führt (im Espressif-Schematic verifiziert). Abhängigkeit ist damit dokumentiert |
| F11 | **Kein Wächter auf der 3,3-V-Schiene** (unser MAX809 überwacht VBAT, für die Pumpe) | Espressif empfiehlt für Akkubetrieb einen Power-Monitor mit ~3,0 V auf der Versorgung. Der ESP32-C6 hat intern einen Brownout-Detektor; ein **zweiter MAX809 (R-Typ, 2,63 V) an EN** wäre die Hardware-Lösung — **offene Entscheidung**, +1 Bauteil |
| F12 | **Unbenutzte GPIOs** (IO5, IO6, IO7, IO15, IO18–IO23) | In der Firmware als Input mit internem Pull parken (Espressif: sonst Mehrverbrauch). IO15 ist Strapping-Pin → nicht nach außen führen |
| F13 | **Pumpenpolung** | Bei Peristaltikpumpen bestimmt die Polarität die Förderrichtung → Steckerbelegung im Layout festlegen und am Prototyp prüfen |
| F14 | **USB-Schirm direkt auf GND** | Zulässig; bei Störungen optional 1 MΩ ∥ 4,7 nF nach GND |

## 4. Was die Prüfung bestätigt hat (kein Handlungsbedarf)

| Prüfung | Beleg |
|---|---|
| AO3400A am 3,3-V-Gate ausreichend | Datenblatt: RDS(on) < 48 mΩ @ VGS 2,5 V, VGS(th) 0,65–1,45 V → bei 0,54 A < 10 mW |
| Freilaufdiode ausreichend | 1N5819WS: 40 V, 1 A Dauer, 25 A Surge bei 0,54 A Laststrom |
| Ladeschlussspannung passt zur Zelle | MCP73831**T-2** = 4,20 V (Datenblatt-Optionen 4,20/4,35/4,40/4,50 V) |
| Ladestromformel | Datenblatt: 10 kΩ → 100 mA ⇒ 1000/R(kΩ) ⇒ 3,9 kΩ ≈ 256 mA, 0,17 C der 1500-mAh-Zelle |
| Laderkondensatoren | Datenblatt: „Bypass to VSS with a **minimum of 4,7 µF**" und „4,7 µF … at the output … for up to 500 mA" |
| USB nativ, keine Brücke | Espressif: D− = GPIO12, D+ = GPIO13 (Modulpins 17/18) |
| ADC-Zuordnung | IO0–IO6 = ADC1_CH0–CH6 (Espressif-Pinliste) |
| Modul-Pins | Pin-Mapping aus der Datasheet verifiziert (z. B. IO2 = Pin 5, IO9 = Pin 23, IO12 = Pin 17, IO13 = Pin 18) |
| Unterspannungsschwelle | MAX809T: VTH 3,04/3,08/3,11 V — über dem Zell-PCM (~2,5 V), unter der Firmware-Schwelle |

## 5. Offen vor dem Layout

1. **Vier Pinbelegungen am Datenblattbild gegenprüfen** (MCP73831, ME6211, MAX809, AO3400A) —
   die Pin-Configuration-Figures waren textlich nicht extrahierbar.
2. **Polung von J1** (Akku) und **J4** (Pumpe) im Layout festschreiben.
3. **Entscheidung F6** (Pumpen während des Ladens sperren) und **F11** (zweiter Wächter auf 3V3).
4. **Testpunkte** in den Plan übernehmen: VBAT, +3V3, GND, SENSOR_AOUT, VBAT_SENSE, EN, PUMP_EN.
