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

- **MCU:** ESP32-C6-MINI-1 (WiFi 6, Deep-Sleep 7 µA, ADC1 auf IO0–IO6), 13,2 × 16,6 mm — Lader, LDO und USB sind eigene Bauteile (siehe `hardware/schaltplan_v1.md`).
- **Pumpen-Ansteuerung:** Logic-Level-N-MOSFET (Low-Side) + Freilaufdiode 1N5819, **Gate 4,7 kΩ, Pulldown 47 kΩ** (Werte aus Review 1 korrigiert — maßgeblich ist `hardware/schaltplan_v1.md`).
- **Sensor:** analoger Ausgang direkt an ADC1, VCC per GPIO schalten (nur während der Messung an); invertierte Kennlinie (trocken ≈ 2100–2600, nass ≈ 1200–1500).
- **Lichtsensor (extern):** analoger Fototransistor (z. B. ALS-PT19, LCSC `C146233`) an **J7**
  (JST-XH 3P wie J2), Ausgang über R_LIGHT_S 1 kΩ an **IO4 (Pin 9, ADC1_CH4)**, R_LIGHT 10 kΩ
  nach GND, C_LIGHT 100 nF Filter. Versorgung über **SENSOR_PWR** (IO3, geschaltet) — nicht
  dauerhaft an +3V3. ADC-Bereich `ADC_ATTEN_DB_12` (0–3300 mV) wie der VBAT-Teiler.
  **Ausfallsicher:** offener/gebrochener Sensor ⇒ 0 V ⇒ „dunkel" ⇒ Bewässerung bleibt erlaubt.
- **Pin-Korrektur (13.09.2026):** IO4/IO5 sind **keine boot-kritischen** Strapping-Pins — ihre
  Strap-Funktion ist nur die SDIO-Slave-Flankenneigung (Wert 0 erlaubt/ohne SDIO wirkungslos).
  Boot-kritisch sind ausschließlich **GPIO8, GPIO9, GPIO15**. IO4 ist damit als ADC1_CH4 nutzbar.
- **Pinordnung (13.09.2026):** Alle 3-poligen Stecker (J2 Feuchte, J7 Licht, J9 Reserve-Analog,
  J10 Reserve-Digital) haben **GND–VCC–SIG**: Pin 1 = GND, **Pin 2 = VCC** (geschaltetes
  SENSOR_PWR), Pin 3 = Signal. Nur der mittlere Pin ist gegen Umdrehen invariant; liegt dort VCC,
  kann ein verkehrt gecrimpter Stecker **nie 3,3 V auf einen MCU-Pin** legen und **nie die
  Sensorversorgung über unsere Masse kurzschließen**. Fehlerfall neu: GND/SIG tauschen, der
  1-kΩ-Serienwiderstand je Signalleitung (zwischen Stecker und MCU) begrenzt den Strom auf ≈ 3 mA
  → **keine Funktion, kein Schaden**. Aderfarben-Empfehlung: schwarz = GND, rot = VCC, gelb = SIG.
- **Erweiterungsstecker (13.09.2026):** Die freien GPIOs werden herausgeführt, damit später
  weitere Sensoren möglich sind, **ohne** die 38-mm-Platine neu zu layouten:
  **J8** = JST-XH 4-pol **I²C** (1 = GND · 2 = SDA/IO18 · 3 = SCL/IO19 · 4 = VCC_EXT) mit
  **P-Kanal-Load-Switch Q2**; VCC_EXT ist nur auf Anforderung an (Gate-Pull-up = **aus beim Reset**,
  Fail-safe), die 2 × 10 kΩ Pull-ups hängen an VCC_EXT (nicht +3V3) → kein Busstrom im Aus-Zustand.
  **J9** = Reserve-Analog an **IO5 (ADC1_CH5)**, **J10** = Reserve-Digital an **IO21** (WPU beim
  Reset dokumentiert). Die restlichen Pins **IO15, IO16, IO17, IO22, IO23** liegen als **Lötpads
  TP7–TP11** (keine Stecker, keine BOM-Position). Alle Stecker sind **gerastete JST-XH**
  (physischer Verpolschutz); Stecker-Typen nicht mischen.
- **Akku:** Zelle mit Schutz-PCB, Laden über **MCP73831T-2 auf unserer Platine** (USB-C-Durchbruch in der Wulst).
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
