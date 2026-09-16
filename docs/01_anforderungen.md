# Anforderungen — Smart Grow Topf

Stand: 11.09.2026 (Projektstart) · Geometrie-Details: [`02_architektur-und-geometrie.md`](02_architektur-und-geometrie.md)

## Entscheidungen (vom User festgelegt)

| Bereich | Entscheidung |
|---|---|
| **Topfgröße** | **Ø 140 mm** (bleibt), Erdbehälter **150 mm hoch** — nur der Erdebehälter; die Wassertankhöhe darunter wurde berechnet |
| **Wassertank** | **1,0 L** nutzbar, im gleichen Ø 140-Grundriss unter dem Erdbehälter → Wasserstand 71 mm, Kammer 82 mm |
| **Pumpe** | **Peristaltische Dosierpumpe 6 V** (quetscht einen Schlauch) — Medium kommt nie mit der Pumpenmechanik in Kontakt, selbstansaugend, präzise dosierbar |
| **Energie** | **Akku** (nicht Netz) |
| **Elektronik** | **Eigene Platine (PCB)**, untergebracht in einer **seitlichen Wulst** am Topf |
| **MCU** | **ESP32-C6-MINI-1** (nacktes Modul) auf der eigenen PCB (korrigiert 11.09.2026, Review 3: XIAO verworfen) |
| **Feuchte-Sensor** | **Kapazitiv v1.2 (mit LDO), analoger Ausgang**, von oben in die Erde gesteckt, seitlich am Controller angeschlossen |
| **Bewässerung** | **Nur in der Dunkelphase** (Growlicht aus). **Externer Lichtsensor am Kabel** (Stecker J7 am Board, Sensor separat beschafft — **keine** PCBA-Position) |
| **Erweiterung (14.09.2026)** | Alle **freien GPIOs + I²C** auf **2,54-mm-Stiftleisten (male, gerade)** — Kabel mit Dupont-Buchse werden direkt aufgesteckt (keine Crimpzange). **Je freiem GPIO ein eigener 3-pol Stecker**, I²C als 4-pol. Pinordnung **GND–VCC–SIG**, I²C **GND–VCC–SDA–SCL** |
| **Bewässerungsweg** | Pumpe fördert nach **oben** auf einen **3D-gedruckten Verteilerring auf der Erdoberfläche** (Top-Drip), Rücklauf tropft in den Tank |
| **Nährlösung** | **Nur Wasser** — ein Behälter, keine automatische Düngerdosierung. Dünger nur ins Substrat |
| **Leer-Meldung** | Bei leerem Tank: kurz ins WLAN → **Telegram** (final, keine Alternative) |
| **Versionierung** | **GitHub-Repository**, Fortschritt wird laufend committet und gepusht |

## System-Konzept (Top-Drip mit Rücklauf)

```
        Verteilerring (3D-Druck, Ø ≤ 105 mm)
   ┌──────────◉───────────◉──────────┐   ← Wasser von oben auf die Erdoberfläche
   │        ERDE / SUBSTRAT          │   Erdbehälter Ø127 innen × 150 mm (≈1,6 L)
   │        ⊗ Sensor (75 mm tief)    │   analog an Controller
   │        ▒▒ Blähton 25 mm ▒▒      │   Dränage + Partikelfilter
   └──────────────┬──────────────────┘
        Luftspalt 30 mm (Gießfüße)
   ┌──────────────┴──────────────────┐
   │      WASSERTANK 1,0 L           │   Ø134 innen, max. Wasserstand 71 mm
   │   ⌄ Saugschlauch → Pumpe ──┐    │
   └────────────────────────────┼────┘
              Wulst: Pumpe, PCB, ESP32-C6-Modul, Akku, Kanal
```

## Regelkreis (Firmware-State-Machine)

1. Kapazitiver Sensor (analog) liest die Substratfeuchte (Messebene 75 mm).
2. **Licht-Gate:** Der externe Lichtsensor (ADC1_CH4, IO4) wird bei jeder Messung mitgelesen
   (Median wie beim Feuchtekanal). „Dunkel" = Wert unter ~30 % des rollierenden 24-h-Maximums
   (`LIGHT_DARK_FRACTION`, Default 0,30), zusätzlich absolute Notwerte in ADC-Counts.
   Erst nach `LIGHT_CONFIRM_SAMPLES` (Default 2) bestätigten Dunkel-Messungen darf gepumpt werden.
3. Ist es zu trocken **und** dunkel → **Pumpe EIN**, dosiert in Portionen. Ist es zu trocken,
   aber **hell**, wird der Bedarf nur vorgemerkt (`pending_water_ml`) und in der Dunkelphase
   ausgeführt.
4. Überschüssiges Wasser läuft durch das Substrat, durch die Blähton-Dränage, zurück in den Tank.
5. **10–20 min** nach Pumpenende erneut messen (Wicking-Verzögerung, Top-Drip):
   - ADC **fällt** → Feuchte steigt → ok → Cooldown bis zum nächsten Zyklus.
   - ADC **fällt nicht** → **Tank leer / Pumpe verstopft / Sensor nicht im Substrat** → **Telegram-Alarm**.
6. Hysterese ±100–150 ADC gegen Flattern; Median-Filter über 10–20 Samples.
7. **Licht-Fail-safe:** Ändert sich der Licht-Rohwert über 24 h nicht (kein Tag/Nacht-Wechsel)
   oder liegt er dauerhaft an der Sättigung ⇒ Telegram-Alarm „Licht-Sensor unplausibel".
   Standardverhalten (`LIGHT_GATE_FAILSAFE = time_window`): Fallback auf ein per NVS/Telegram
   gesetztes Zeitfenster (`LIGHT_OFF_START`/`LIGHT_OFF_END`), damit die Pflanze versorgt bleibt;
   alternativ strikt sperren (`block`). Polarität per `LIGHT_INVERT` konfigurierbar.
8. **Nachfüllen:** Der Taster wird gedrückt → Gerät wacht auf, der „Tank leer"-Zustand wird gelöscht (Quittung). Steigt der Sensorwert im nächsten Zyklus ohnehin deutlich an, gilt der Tank auch **ohne** Tastendruck als nachgefüllt.

## Technische Eckpunkte

- **MCU:** ESP32-C6-MINI-1 (WiFi 6, Deep-Sleep 7 µA, ADC1 auf IO0–IO6), 13,2 × 16,6 mm — Lader, beide Wandler (5 V/3,3 V) und USB sind eigene Bauteile (siehe `hardware/schaltplan_v1.md`).
- **Pumpen-Ansteuerung:** Logic-Level-N-MOSFET (Low-Side) + Freilaufdiode 1N5819, **Gate 4,7 kΩ, Pulldown 47 kΩ** (Werte aus Review 1 korrigiert — maßgeblich ist `hardware/schaltplan_v1.md`).
- **Sensor:** analoger Ausgang direkt an ADC1, VCC per GPIO schalten (nur während der Messung an); invertierte Kennlinie (trocken ≈ 2100–2600, nass ≈ 1200–1500).
- **Lichtsensor (extern):** analoger Fototransistor (z. B. ALS-PT19, LCSC `C146233`) an **J7**
  (seit 14.09.2026 **2,54-mm-Stiftleiste 1×3**, `C2937625`), Ausgang über R_LIGHT_S 1 kΩ an
  **IO4 (Pin 9, ADC1_CH4)**, R_LIGHT 10 kΩ nach GND, C_LIGHT 100 nF Filter. Versorgung über
  **SENSOR_PWR** (IO3, geschaltet) — nicht dauerhaft an +3V3. ADC-Bereich `ADC_ATTEN_DB_12`
  (0–3300 mV) wie der VBAT-Teiler. **Ausfallsicher:** offener/gebrochener Sensor ⇒ 0 V ⇒ „dunkel"
  ⇒ Bewässerung bleibt erlaubt.
- **GPIO-/I²C-Erweiterung (14.09.2026):** Freie Pins auf Stiftleisten: **J8** (I²C 4-pol,
  GND–VCC_EXT–SDA–SCL), **J9** (Reserve-ADC IO5), **J10–J15** (Reserve IO15/16/17/21/22/23).
  Jeder Signalpin hat einen **1-kΩ-Serienwiderstand** zum MCU. Die Erweiterungsversorgung
  **VCC_EXT** wird über einen **P-Kanal-Load-Switch Q2 (AO3401A)** geschaltet; das Gate hängt über
  **47 kΩ an +3V3** ⇒ **VCC_EXT ist beim Reset aus** (Fail-safe, IO20 zieht zum Einschalten nach
  unten). Die I²C-Pull-ups (2 × 10 kΩ) hängen an **VCC_EXT**, nicht an +3V3 (kein Busstrom im
  Aus-Zustand). `C_SPARE` 100 nF filtert den Reserve-ADC. IO5/IO15/IO16/IO17/IO21/IO22/IO23 sind
  über die Serienwiderstände sicher herausgeführt (IO15 nur JTAG-Quelle, Default-eFuses inert;
  IO16/17 sind UART0). IO20 bleibt intern (Load-Switch).
- **Pin-Korrektur (13.09.2026):** IO4/IO5 sind **keine boot-kritischen** Strapping-Pins — ihre
  Strap-Funktion ist nur die SDIO-Slave-Flankenneigung (Wert 0 erlaubt/ohne SDIO wirkungslos).
  Boot-kritisch sind ausschließlich **GPIO8, GPIO9, GPIO15**. IO4 ist damit als ADC1_CH4 nutzbar.
- **Pinordnung (13.09.2026, erweitert 14.09.2026):** **Alle** 3-poligen Stecker (J2 Feuchte,
  J7 Licht, J9–J15 Reserve) haben **GND–VCC–SIG**: Pin 1 = GND, **Pin 2 = VCC** (geschaltetes
  SENSOR_PWR bzw. VCC_EXT), Pin 3 = Signal. Der 4-polige I²C-Stecker **J8** hat
  **GND–VCC_EXT–SDA–SCL** (VCC innen, wie Qwiic/STEMMA). Nur der mittlere Pin ist gegen Umdrehen
  invariant; liegt dort VCC, kann ein verkehrt gesteckter Stecker **nie 3,3 V auf einen MCU-Pin**
  legen und **nie die Sensorversorgung über unsere Masse kurzschließen**. Fehlerfall neu: GND/SIG
  tauschen, der 1-kΩ-Serienwiderstand je Signalleitung (zwischen Stecker und MCU) begrenzt den
  Strom auf ≈ 3 mA → **keine Funktion, kein Schaden**. Aderfarben-Empfehlung: schwarz = GND,
  rot = VCC, gelb = SIG (J8 4-pol: schwarz/rot/weiß/grün). J2 bleibt **gerastetes JST-XH**; J7 und
  J8–J15 sind **2,54-mm-Stiftleisten** für Dupont-Buchsen — Stecker-Typen nicht mischen.
- **Akku:** **2S-Pack (6,0–8,4 V) mit BMS inkl. Balancing — Pflicht** (Reihenzellen driften sonst auseinander, siehe `hardware/schaltplan_v1.md` §6.3); Laden über den **IP2326** (2S-Boost-Lader aus 5 V USB, 8,4 V / 0,90 A) auf unserer Platine (USB-C-Durchbruch in der Wulst). Aus dem Pack entstehen **+5 V (SY8113B-Buck, 3 A)** für beide Pumpen und **+3,3 V (AP63203-Buck, 2 A)** für die Logik — **kein LDO, kein Boost**.
- **Bedienung:** **externer Taster** am Gehäuse (Nachfüllen quittieren). Auf der Platine nur zwei Lötpads/Bohrungen (J6) + Pull-up 10 kΩ + 100 nF — der Taster sitzt **nicht** auf der Platine. Der Taster hängt an **IO6 (LP_GPIO6)** und **weckt das Gerät aus dem Deep-Sleep** (EXT1).
- **Anzeige:** **rote LED D5 „Tank leer"** an IO7 auf der Platine (1 kΩ, 1,3 mA — Firmware soll blinken statt dauerleuchten, siehe `hardware/schaltplan_v1.md` §7.4); **grüne Status-LED D2** an IO14 (R4 220 Ω, Vf 2,85 V — grün = Betrieb, **rot bleibt der Warnung vorbehalten**); Ladestatus zeigt der Lader selbst.
- **Strombudget:** Deep-Sleep µA-Bereich, Pumpe nur Minuten pro Zyklus → Versorgung für Wochen.

## Offene Punkte

- Batteriezelle final (Bautiefe Wulst 30 mm) — BOM-Check läuft.
- Pumpen-Abmessungen → Wulstbreite parametrisch anpassen.
- Kalibrierwerte `dry`/`wet` am echten Substrat (nach dem ersten Durchlauf).
- Licht-Schwellen (`LIGHT_DARK_FRACTION`, `LIGHT_DARK_COUNTS`, `LIGHT_BRIGHT_COUNTS`) und das
  Zeitfenster-Fallback am echten Growlicht/Ablauf verifizieren.
- Optional V2: Tankstand-Sensor (float switch) als Redundanz zum Feuchte-Kriterium.
