# Firmware- & Systemlogik-Konzept: Bottom-Watering Smart-Grow-Topf (ESP32)

**Projekt:** Selbstbewässernder Topf — Erde oben, Wassertank unten, Tauchpumpe pumpt bei Trockenheit Wasser von unten nach oben in die Erde; Überschuss tropft über Drainage zurück in den Tank. Kapazitiver Bodensensor (analog) + ESP32 steuern den Zyklus und erkennen einen leeren Tank daran, dass nach dem Pumpen **keine** Feuchtigkeitszunahme gemessen wird.

---

## 1. Systemüberblick

```
┌─────────────────────────────── Topf ───────────────────────────────┐
│  Erde / Substrat                                                  │
│    ├─ kapazitiver Feuchtesensor (analog) ──────────► D0 (ADC1)    │
│    └─ Bewässerung / Tropfschlauch ◄── Tauchpumpe ────────┐         │
│  Drainage: Überschuss läuft zurück in den Tank           │         │
│  ─────────────────── Trennebene ───────────────────      │         │
│  Wassertank  │  Tauchpumpe (5 V, MOSFET getrieben) ◄─────┘         │
└───────────────────────────────────────────────────────────────────┘
              │                              │
              ▼                              ▼
      XIAO ESP32-C6                Status-LED / 0,96"-OLED (I2C)
              │
              └─► WiFi: Webserver http://growpot.local  ·  Telegram-Bot (Push)
```

**Regelkreis:** messen → zu trocken? → pumpen → kurz warten → erneut messen → Vergleich. Der *Delta-Vergleich* ist das Herz der Leer-Erkennung: Wenn die Erde nach dem Pumpen nicht feuchter wird, obwohl der Sensor in der Erde steckt, kam kein Wasser an → Tank leer (oder Pumpe defekt/verstopft).

---

## 2. ESP32-Board-Wahl

### Vergleich (Preise verifiziert am 10.09.2026)

| Board | Preis (verifiziert) | Link | ADC | Deep Sleep | Besonderheiten |
|---|---|---|---|---|---|
| **Seeed XIAO ESP32-C6** ⭐ | ab **5,20 $** (10er-Pack), Einzelpreis im Shop ~6 $ | [seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-p-5884](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-p-5884.html) | **7 Kanäle, alle ADC1** | **15 µA** (bester der Serie) | WiFi 6 + BLE 5.3 + **Thread/Zigbee (Matter-native)**, 2× RISC-V (HP + LP-Core), 512 KB SRAM / 4 MB Flash, LiPo-Lader onboard |
| Seeed XIAO ESP32-C3 | **4,99 $** | [seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431](https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html) | 4 Kanäle, aber **nur 3 zuverlässig** (A3/GPIO5 = ADC2, bekannt unzuverlässig) | 44 µA | RISC-V 160 MHz, 400 KB SRAM, LiPo-Lader onboard |
| Seeed XIAO ESP32-S3 | ab **7,49 $** (10er-Pack) | [seeedstudio.com/XIAO-ESP32S3-p-5627](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html) | 9 Kanäle | 14 µA | Dual-Core 240 MHz, 8 MB PSRAM — für dieses Projekt **Overkill** |
| ESP32 DevKit C V2 (WROOM-32, AZ-Delivery) | **10,99 €** (statt 13,99 €; **aktuell ausverkauft**) | [az-delivery.de/products/esp32-developmentboard](https://www.az-delivery.de/products/esp32-developmentboard) | 18 Kanäle, aber ADC2 + WiFi-Konflikt | ~10 µA (Modem-Sleep aber deutlich höher) | Riesen-Ökosystem, 56×28 mm (groß), kein LiPo-Lader |

Alle XIAO-Boards: 21 × 17,8 mm, gleicher Footprint, 3V3-Out max. 700 mA. Seeed liefert aus dem Deutschland-Warehouse steuerfrei innerhalb der EU.

### Empfehlung: **Seeed XIAO ESP32-C6**

Begründung:
1. **Konsistenz:** Gleiche Board-Familie wie im GrowTower-BOM → gleiche Toolchain (Arduino-Board-Paket), gleiche Hülle/Footprint, Code-Muster übertragbar.
2. **ADC ohne Fallstricke:** Alle 7 ADC-Kanäle liegen auf **ADC1**. Beim C3 ist der vierte Analog-Pin (A3/GPIO5) auf ADC2 und laut Seeed-Wiki durch „false sampling signals" unzuverlässig — das C6 hat dieses Problem gar nicht. Für Sensor + evtl. Tank-Level-Reserve ist das sauberer.
3. **Bester Low-Power-Wert der Serie** (15 µA Deep Sleep) + **LP-Core** → späterer Akkubetrieb möglich, falls der Topf vom USB-Kabel weg soll.
4. **Matter/Thread nativ:** Der Topf kann später ohne Bridge direkt als Matter-Device in Home Assistant eingebunden werden — kein WLAN-Polling nötig.
5. Preislich zwischen C3 und S3, aber technisch die modernste Wahl (WiFi 6, Bluetooth 5.3).

**Alternativen:** C3, wenn es um jeden Cent geht (reicht für dieses Projekt trotzdem: 1 Sensor = 1 ADC1-Pin). WROOM-DevKit nur, wenn man es schon besitzt oder Breadboard-Arbeiten plant — zu groß für den Topf, kein Laderegler. S3 nur, wenn später Kamera/PSRAM-Features geplant sind.

---

## 3. Pinbelegung (XIAO ESP32-C6, laut Seeed-Wiki-Pinmap)

| Funktion | XIAO-Pin | GPIO | Anmerkung |
|---|---|---|---|
| Bodensensor (analog) | **D0** | GPIO0 | ADC1_CH0, auch LP_GPIO0 |
| Sensor-VCC (nur während Messung) | **D1** | GPIO1 | Versorgung per GPIO schaltbar → kein Korrosionsstrom, Stromersparnis |
| Pumpe (via MOSFET) | **D3** | GPIO21 | rein digital, sonst ungenutzt |
| Status-LED (extern, aktiv via GPIO) | **D2** | GPIO2 | ADC-fähig als Reserve |
| OLED (I2C) | **D4 = SDA, D5 = SCL** | GPIO22/23 | 0,96" SSD1306 |
| Optional: Tank-Level-Sensor | MTDI-Pad | GPIO5 | JTAG-Pad auf der Rückseite, ADC-fähig |

**Pumpen-Treiber:** **Peristaltische Mini-Schlauchpumpe 3–6 V** (Funduino 0–90 ml/min, ~9 €; oder 6V-G10-Variante ~6 €) über **Logic-Level-N-MOSFET** (z. B. IRLZ44N oder AO3400): Pumpe an 3,7–6 V (LiPo-Zelle), Drain am Pumpe-minus, Source an GND, Gate mit 220 Ω + **10 kΩ Pull-down** (Pumpe ist bei Boot sicher AUS, bevor der GPIO konfiguriert ist!) und **Freilaufdiode** (z. B. 1N5819) parallel zur Pumpe. Versorgung über die Zelle/niedrige Schiene — **nicht** am 3V3-Pin. Fertige Relais-Module gehen auch, aber billige sind active-low und können beim Boot kurz schalten; MOSFET + Pull-down ist robuster und lautlos. (Peristaltik = Flüssigkeit bleibt im Schlauch → Dünger kommt nie mit der Mechanik in Kontakt.)

---

## 4. Messkette & ADC-Konfiguration (kapazitiver Sensor an C3/C6)

Der Sensor ist ein kapazitiver Bodenfeuchtesensor mit Analogausgang (v1.2/v2.0, Versorgung 3,3 V ok, Ausgang 0–3 V). **Keine Library nötig** — nur `analogRead`/`analogReadMilliVolts`.

```cpp
analogReadResolution(12);          // 12-Bit-Auflösung
analogSetAttenuation(ADC_11db);    // Dämpfung: Messbereich bis ~3,1 V (C3/C6/S3);
                                   // beim C6 zusätzlich ADC_12db möglich (bis ~3,3 V)
uint32_t mV = analogReadMilliVolts(PIN_SENSOR);  // kalibrierter Wert, chipunabhängig
```

Wichtige Punkte:
- **`analogReadMilliVolts` statt roher Counts** verwenden: Die Counts hängen von Chip und Attenuation ab; Millivolt sind vergleichbar und eFuse-kalibriert.
- **Kein ADC2 verwenden:** Beim C3 nur D0–D2 (ADC1), A3/GPIO5 meiden (Seeed-Wiki bestätigt das Problem). Beim C6 entfällt das komplett (alle Kanäle ADC1).
- **Sensor-VCC per GPIO schalten:** Nur während der Messung an, ~10–20 ms Einschwingzeit vor dem ersten Read. Verhindert Korrosion/„Galvanik-Drift" (auch kapazitive Sensoren danken es) und spart Strom.
- **Glättung:** N = 8–16 Messungen im 10-ms-Abstand → **Median** bilden (Ausreißer raus), dann Mittelwert. Zusätzlich gleitender Mittelwert über die letzten Messintervalle (z. B. 5 Werte) als Anzeige-/Triggerwert.
- **Kalibrierung:** Zwei Referenzpunkte in der eigenen Erde aufnehmen (Sensor in trockener Erde = 0 %, in gesättigter Erde = 100 %) und mit `map()`/linearer Funktion in Prozent umrechnen, Werte in `Preferences` (NVS) speichern.
- **⚠️ ADC ist INVERTIERT:** Trocken = **hoher** Wert (2100–2600), nass = **niedriger** Wert (1000–1500), roh: 2,9 V trocken / 1,0 V nass. Steuerlogik: **pumpen, wenn ADC > Schwelle** (zu trocken); stoppen, wenn ADC unter Schwelle − Hysterese. Steigt die Feuchtigkeit → ADC **fällt**.
- **⚠️ Sensor-Position:** In Bottom-Watering gibt es ein vertikales Feuchtegefälle (unten nass, oben trocken). Sensor **auf halber Topfhöhe in der Wurzelzone** platzieren — steckt er zu hoch, meldet er „trocken", während unten alles schwimmt → Überpumpen.
- **Plausibilitäts-Check:** Dauerhaft < 100 mV oder > 2900 mV = Sensor defekt/abgezogen → eigener Fehlerzustand, Pumpe sperren.

---

## 4b. Licht-Gate: Bewässerung nur in der Dunkelphase (ergänzt 13.09.2026)

Der Regelkreis bekommt ein **Licht-Gate**: gepumpt wird nur, wenn das Growlicht aus ist.
Sensor: **externer analoger Fototransistor an J7** (ADC1_CH4 = **IO4**), Versorgung über
**SENSOR_PWR (IO3)** nur während der Messung. Der Sensor ist **keine** PCBA-Position.
Hardware-Details: `hardware/schaltplan_v1.md` §8.

### Messung & Bewertung

1. **Messung:** Lichtwert bei jeder Messung (Median über 10–20 Samples wie der Feuchtekanal),
   Sensor dabei über SENSOR_PWR versorgt. Danach `light_glatt` = gleitender Mittelwert.
2. **Adaptive Schwelle statt fester Kalibrierung:** rollierendes **24-h-Fenster**;
   „dunkel" = Wert unter `LIGHT_DARK_FRACTION` (Default **0,30**) des Tagesmaximums.
   Zusätzlich **absolute Notwerte** in ADC-Counts, per NVS einstellbar:
   - `light <= LIGHT_DARK_COUNTS` (Default 200) ⇒ dunkel (fängt auch den abgezogenen Sensor ab),
   - `light >= LIGHT_BRIGHT_COUNTS` (Default 3000) ⇒ hell/Sättigung,
   - dazwischen entscheidet die adaptive 30-%-Schwelle.
3. **Dunkel bestätigt** erst nach `LIGHT_CONFIRM_SAMPLES` (Default **2**) Messungen unter der
   Schwelle → **erst dann darf die Pumpe laufen**. Ist es zu trocken **und** hell, wird der
   Bedarf vorgemerkt (`pending_water_ml`) und in der nächsten Dunkelphase ausgeführt.
4. **Polarität konfigurierbar:** `LIGHT_INVERT` (Default `false`) — fertige Sensormodule liefern
   teils invertiert (LDR gegen VCC); die Firmware muss beide Verdrahtungen verkraften.
5. **Plausibilität / Ausfallsicherheit:** Ändert sich der Rohwert über **24 h** nicht (kein
   Tag/Nacht-Wechsel erkennbar) oder liegt er **dauerhaft an der Sättigung** ⇒ Telegram-Alarm
   „**Licht-Sensor unplausibel**". Standardverhalten `LIGHT_GATE_FAILSAFE = time_window`:
   Fallback auf ein per NVS/Telegram gesetztes Zeitfenster (`LIGHT_OFF_START`/`LIGHT_OFF_END`),
   damit die Pflanze versorgt bleibt; alternativ `block` = strikt sperren.
   **Wichtig:** ein offener/gebrochener Sensor liefert über R_LIGHT **0 V ⇒ „dunkel"**, das Gate
   öffnet also — der unkritische Fehler. Ein blockierender Fehler (dauerhaft „hell") würde die
   Pflanze vertrocknen lassen und wird deshalb erkannt und gemeldet.
6. **Anzeige/Log:** der erkannte Tag/Nacht-Wechsel wird mitgeloggt und im Telegram-Tagesreport
   als **Lichtstunden** gemeldet (Plausibilitätskontrolle für den Nutzer).

### Zusätzliche Parameter (Defaults, per NVS/Telegram änderbar)

| Parameter | Default | Erklärung |
|---|---|---|
| `LIGHT_DARK_FRACTION` | 0,30 | dunkel = unter 30 % des rollierenden 24-h-Maximums |
| `LIGHT_DARK_COUNTS` | 200 | absoluter Notwert „dunkel" [ADC-Counts] |
| `LIGHT_BRIGHT_COUNTS` | 3000 | absoluter Notwert „hell"/Sättigung [ADC-Counts] |
| `LIGHT_CONFIRM_SAMPLES` | 2 | aufeinanderfolgende Dunkel-Messungen bis zur Freigabe |
| `LIGHT_INVERT` | false | Sensorpolarität (fertige Module teils invertiert) |
| `LIGHT_GATE_FAILSAFE` | time_window | `time_window` (Zeitfenster-Fallback) oder `block` |
| `LIGHT_OFF_START` / `LIGHT_OFF_END` | 20:00 / 08:00 | Zeitfenster-Fallback, wenn der Sensor unplausibel ist |

---

## 4c. I²C- und GPIO-Erweiterung (J8–J15, wieder aufgenommen 14.09.2026)

Hardware: `hardware/schaltplan_v1.md` §9. Alle freien GPIOs und der I²C-Bus sind als
**2,54-mm-Stiftleisten** herausgeführt: **J8** (I²C 4-pol, **GND · VCC_EXT · SDA(IO18) · SCL(IO19)**),
**J9** (Reserve-ADC **IO5**), **J10–J15** (Reserve **IO15/IO16/IO17/IO21/IO22/IO23**). Jede
Signalleitung hat **1 kΩ in Reihe** zum MCU. Die I²C-Pull-ups (2 × 10 kΩ) hängen an **VCC_EXT**.

**VCC_EXT / Load-Switch (Fail-safe):** VCC_EXT kommt aus dem **P-Kanal-MOSFET Q2 (AO3401A)**,
Source an +3V3, Drain an VCC_EXT. Das Gate hängt über **47 kΩ auf +3V3** (Quellpotential) und wird
von **IO20 (`EXT_EN`)** nach unten gezogen. **Polarität:** IO20 `LOW` ⇒ Q2 leitet ⇒ **Rail an**;
IO20 `HIGH`/hochohmig ⇒ Q2 sperrt ⇒ **Rail aus**. Beim Reset hat IO20 einen internen
**Weak-Pull-up** ⇒ **VCC_EXT ist beim Start aus**.

**Firmware-Option (noch nicht implementiert):**

1. **Rail schalten:** `EXT_EN` (IO20) als Ausgang. Im Deep-Sleep IO20 hoch ⇒ Rail aus ⇒ **kein
   Standby-Strom** über angeschlossene Module und keiner über die I²C-Pull-ups.
2. **Bus-Scan:** mit `Wire.begin(/*SDA=*/18, /*SCL=*/19)` und einem Scan der Adressen 0x08–0x77
   prüfen, welche Module stecken; Ergebnis im Telegram-Tagesreport / `/status` ausgeben.
3. **Autarkie:** Module nur während der Messung bestromen (Rail an, 5–10 ms warten, lesen, Rail
   aus) — analog zum geschalteten SENSOR_PWR der analogen Sensoren.
4. **Reserve-ADC IO5 (J9):** zweiter analoger Kanal (ADC1_CH5) mit R_SPARE_AIN 1 kΩ + C_SPARE
   100 nF, gleiche Median-/Kalibrierlogik wie der Feuchtekanal; z. B. zweiter Feuchtesensor, NTC
   oder Pegel-Trigger. `ADC_ATTEN_DB_12` (0–3300 mV).
5. **Reserve-Digital IO15/16/17/21/22/23 (J10–J15):** frei als Ein-/Ausgang nutzbar. Beachten:
   IO15 ist Strapping (JTAG-Quelle, mit Default-eFuses wirkungslos), IO16/IO17 sind UART0
   (TXD0/RXD0, Debug — mit dem 1-kΩ-Serien-R bleibt der Pin geschützt), IO21 hat beim Reset einen
   WPU (ein angeschlossenes Modul sieht kurz High).
6. **Option:** den analogen Lichtsensor auf J7 durch einen digitalen I²C-Lichtsensor ersetzen
   (dann das Licht-Gate aus 4b auf den digitalen Wert umstellen).

---

## 5. State-Machine (Kern der Firmware)

**Regel:** komplett `millis()`-getrieben, **kein `delay()`** — der Webserver und Telegram-Polling müssen parallel weiterlaufen.

### Zustände

`INIT → MESSEN ⇄ PUMPEN → ABWARTEN → AUSWERTEN`, dazu Fehlerzustände `TANK_LEER` und `SENSOR_FEHLER`.

### Parameter (Defaults zum Tunen, per Webserver/NVS änderbar)

| Parameter | Default | Erklärung |
|---|---|---|
| `MESS_INTERVALL` | 60 s | (Akku-Betrieb: 300 s) |
| `SCHWELLE_TROCKEN` | 35 % | **unter** diesem Wert → Pumpbedarf (nach Kalibrierung) |
| `SCHWELLE_NASS` | 50 % | Hysterese für Auto-Recovery nach Befüllen |
| `PUMPZEIT` | 5–10 min | Peristaltik ~60 ml/min: 0,3–0,6 L ÷ 60 ml/min (kalibrieren!) |
| `MAX_PUMPZEIT_HW` | 45 s | Software-Watchdog gegen Dauerläufer (gilt je Pump-Portion) |
| `SETTLE_ZEIT` | **10 min** | ⚠️ Wicking-Verzögerung: Wasser braucht 5–15 min bis zum Sensor (Recherche) — 90 s war zu kurz → falsche Leer-Alarme |
| `DELTA_MIN` | 2–3 %-Pkt. | nötiger Anstieg (= 3× Rauschamplitude des Signals) |
| `COOLDOWN` | 15 min | Mindestabstand zwischen Pumpvorgängen (Duty-Cycle) |
| `MAX_VERSUCHE` | 3 | erfolglose Pumpvorgänge → TANK_LEER |

### Pseudocode

```
GLOBAL: state, feuchte_glatt, feuchte_vor, pumpVersuche, letztePumpzeit

setup():
    Pumpe-GPIO = OUTPUT, LOW            // Pull-down → sicher AUS beim Boot
    Sensor-VCC-GPIO = OUTPUT, LOW
    LED-GPIO = OUTPUT; OLED-Init (I2C)
    ADC-Init (12 Bit, ADC_11db)
    WiFi verbinden; mDNS "growpot.local"; Webserver-Routen; Telegram-Init
    Kalibrierdaten + Parameter aus Preferences laden
    state = INIT

loop():                                  // nie blockieren!
    webserver.handleClient()
    telegramPoll()                       // alle ~2 s, non-blocking
    LED/OLED-Ausgabe aktualisieren

    switch (state):
      INIT:
          erste Messung + Plausibilitätscheck
          state = MESSEN

      MESSEN:
          alle MESS_INTERVALL:
              feuchte = messen()                       // Median+Mittelwert, %
              feuchte_glatt = gleitenderMittelwert(feuchte)
              licht = messen_licht()                   // Median, ueber SENSOR_PWR
              licht_glatt = gleitenderMittelwert(licht)
              licht_fenster_aktualisieren(licht_glatt) // rollierendes 24-h-Maximum
              wenn Sensorwert unplausibel:  state = SENSOR_FEHLER
              wenn licht_unplausibel():                // 24 h unveraendert / gesaettigt
                  telegram("Licht-Sensor unplausibel")
                  // LIGHT_GATE_FAILSAFE: time_window -> Zeitfenster, block -> sperren
              wenn feuchte_glatt < SCHWELLE_TROCKEN:
                  wenn dunkel_bestaetigt():            // ═══ Licht-Gate ═══
                     UND now - letztePumpzeit >= COOLDOWN:
                        feuchte_vor = feuchte_glatt     // Referenz fuer Delta
                        pumpe(EIN); pumpStart = now
                        state = PUMPEN
                  sonst:
                     pending_water_ml += fuellmenge()  // merken, in der Dunkelphase ausfuehren

      PUMPEN:
          wenn now - pumpStart >= PUMPZEIT
             ODER now - pumpStart >= MAX_PUMPZEIT_HW:   // Watchdog
                pumpe(AUS)
                settleStart = now
                state = ABWARTEN

      ABWARTEN:
          wenn now - settleStart >= SETTLE_ZEIT:
                feuchte_nach = messen()
                state = AUSWERTEN

      AUSWERTEN:                                          // ═══ Kern: Leer-Erkennung ═══
          delta = feuchte_nach - feuchte_vor
          wenn delta >= DELTA_MIN:
              // Erde hat das Wasser aufgenommen → alles normal
              pumpVersuche = 0
              letztePumpzeit = now
              log/OLED/Web: "Bewässert (+delta %)"
              state = MESSEN
          sonst:
              // gepumpt, aber Erde nicht feuchter → kein Wasser angekommen
              pumpVersuche = pumpVersuche + 1
              wenn pumpVersuche < MAX_VERSUCHE:
                  Meldung (Warnstufe): "Pumpversuch N ohne Wirkung"
                  state = MESSEN        // nächster Versuch erst nach COOLDOWN
              sonst:
                  state = TANK_LEER

      TANK_LEER:
          pumpen gesperrt
          melden_TANK_LEER()            // LED rot blinken, OLED, Web-Banner, Telegram
          alle 30 min:
              feuchte = messen()
              wenn feuchte > SCHWELLE_NASS:   // Nutzer hat nachgefüllt / von oben gegossen
                  pumpVersuche = 0
                  melden("Tank nachgefüllt, System normal")
                  state = MESSEN

      SENSOR_FEHLER:
          pumpen gesperrt; melden()
          alle 5 min erneut messen → bei plausiblen Werten zurück nach MESSEN
```

### Hilfsfunktion `messen()`

```
messen():
    Sensor-VCC-GPIO = HIGH;  warte 15 ms          // Einschwingzeit
    n = 12 Messungen im 10-ms-Abstand sammeln (analogReadMilliVolts)
    Sensor-VCC-GPIO = LOW                          // sofort wieder stromlos
    Median der n Messungen (Ausreißerschutz)
    → in Prozent umrechnen (Kalibrierkurve, geclampt auf 0–100)
    zurückgeben
```

---

## 6. Schutzmechanismen

| Schutz | Umsetzung |
|---|---|
| **Dauerläufer** | `MAX_PUMPZEIT_HW`-Watchdog (Software) + optional Hardware-Watchdog (`esp_task_wdt`). Pumpe wird im PUMPEN-Zustand nach Max-Zeit hart abgeschaltet. |
| **Überpumpen / Duty-Cycle** | `COOLDOWN`-Sperre zwischen Pumpvorgängen; optional Tageslimit (max. X Liter/Tag über Pumpzeit-Aufsummierung). |
| **Trockenlauf** | Leer-Erkennung sperrt die Pumpe nach `MAX_VERSUCHE` erfolglosen Versuchen dauerhaft — kein sinnloses Weiterpumpen, Pumpe läuft nie lange trocken. |
| **Boot-Sicherheit** | MOSFET-Gate mit 10 kΩ Pull-down → Pumpe ist AUS, solange der GPIO nicht aktiv HIGH treibt (auch beim Reset). |
| **Sensor-Fehler** | Plausibilitätsbereich → SENSOR_FEHLER sperrt das Pumpen (verhindert Fluten bei Sensor-Ausfall). |
| **Licht-Fail-safe** | Sensor unplausibel (24 h keine Änderung oder dauerhafte Sättigung) → Telegram-Alarm + Zeitfenster-Fallback (`LIGHT_GATE_FAILSAFE = time_window`) oder Sperren (`block`). Ein offener/gebrochener Sensor liefert über R_LIGHT **0 V ⇒ „dunkel"** → Bewässerung bleibt erlaubt (Pflanze vertrocknet nicht). |
| **Hysterese** | `SCHWELLE_TROCKEN` (starten) vs. `SCHWELLE_NASS` (Recovery) — kein Flackern an der Kippgrenze. |
| **Watchdog gesamt** | Task-Watchdog mit sauberem Restart; Zustand „letzte Bewässerung" in NVS/RTC-RAM halten. |

**Erkennungs-Blindspot (ehrliche Grenze der Methode):** Ein leerer Tank wird erst bemerkt, wenn die Erde nach einem Pumpversuch trocken genug ist, um den Delta-Test auszulösen. Daher als **Ausbaustufe V2** eine direkte Tank-Überwachung ergänzen:
- Berührungsloser Kapazitiv-Sensor (Typ XKC-Y25) an der Tank-Außenwand oder Schwimmerschalter (digital, ein GPIO), oder
- Pumpstrom-Messung (INA219, I2C): leere Pumpe zieht *weniger* Strom (Luft), verstopfte Pumpe *mehr* — damit lassen sich „Tank leer" und „Pumpe verstopft" sogar unterscheiden. V1 meldet bewusst nur „Tank leer oder Pumpe defekt".

---

## 7. Leer-Meldung & Bedienoberfläche

### Vergleich der Kanäle

| Kanal | Kosten | Aufwand | Funktioniert ohne Internet? | Bewertung |
|---|---|---|---|---|
| **Status-LED** (RGB) | < 1 € | trivial | ✅ | **Pflicht** — Blink-Codes als letzte Instanz |
| **OLED 0,96" SSD1306** (I2C) | wenige € | gering (2 Drähte) | ✅ | **Empfohlen** — Feuchte/Zustand auf einen Blick |
| **Webserver `http://growpot.local`** (mDNS) | 0 € | mittel | ✅ (nur WLAN) | **Pflicht** — zentrale UI, Steuerung, Reset-Button |
| **Telegram-Bot** (UniversalTelegramBot) | 0 €, kein Cloud-Abo | mittel | ❌ (Internet nötig) | **Empfohlen** — echte Push-Meldung aufs Handy |
| **ntfy.sh** (HTTP-POST) | 0 € | sehr gering | ❌ | schlanke Alternative zu Telegram (nur Empfangen) |
| **MQTT / Home Assistant** | 0 € (Broker vorausgesetzt) | mittel | ✅ | optional, wenn HA existiert |
| **Matter** (nativ auf C6) | 0 € | höher | ✅ | Option für später: Topf direkt als Matter-Device |
| Blynk | Freemium/Abo | mittel | ❌ | möglich, aber Cloud-Abhängigkeit — hier unnötig |

### Empfehlung (dreistufig)

1. **Lokal:** RGB-Status-LED + 0,96"-OLED. Blink-Codes: grün = ok, blau = pumpt, gelb = Warnung, **rot blinkend = TANK LEER**.
2. **Zentrale UI:** ESP32-Webserver mit mDNS — gleiche Bedienidee wie beim GrowTower: `http://growpot.local` zeigt Feuchte, Zustand, letzte Bewässerung und Fehler-Banner; Buttons für manuelles Pumpen und Fehler-Reset; `/status` liefert JSON (Brücke für Home Assistant).
3. **Fernmeldung (Push):** **Telegram-Bot** mit `UniversalTelegramBot` — bei leerem Tank kommt eine aktive Nachricht aufs Handy:

   > ⚠️ *GrowPot: Tank LEER — nach 3 Pumpversuchen keine Feuchtigkeitszunahme. Bitte nachfüllen. (Feuchte: 31 %, Zustand: TANK_LEER)*

   Und nach dem Befüllen (Auto-Recovery):
   > ✅ *GrowPot: Tank nachgefüllt — System läuft wieder normal (Feuchte: 62 %).*

   Telegram kann zusätzlich Kommandos: `/status`, `/pump` (manuell), `/reset`. Kein Blynk-Konto, keine laufenden Kosten. Wer gar keinen Bot einrichten will: ein `HTTP-POST` an einen **ntfy.sh**-Topic (eine Zeile Code) erreicht das Handy genauso als Push.

**Ausfall-Sicherheit:** Wenn WiFi/Internet weg ist, läuft die Bewässerung autark weiter und die LED/OLED zeigt den Leer-Zustand lokal; die Telegram-Meldung wird beim Reconnect erneut gesendet (Zustands-Flag, kein Einmal-Feuern).

### Webserver-Routen (Überblick)

```
GET  /        → Statusseite: Feuchte, Zustand, letzte Pumpe, Fehler-Banner
GET  /status  → JSON für Home Assistant / MQTT-Bridge
POST /pump    → manueller Pumpvorgang (COOLDOWN-Schutz greift)
POST /reset   → Fehler-Reset (nur sinnvoll nach Befüllen)
GET/POST /config → Schwellwerte & Zeiten ändern (in Preferences gespeichert)
```

---

## 8. Arduino-Bibliotheken & Toolchain

| Zweck | Library / Board-Paket | Anmerkung |
|---|---|---|
| Board-Paket | **esp32 by Espressif** (Board-Manager-URL: `https://espressif.github.io/arduino-esp32/package_esp32_index.json`) | Für XIAO_ESP32C6 ist **Core ≥ 3.0.0** nötig (laut Seeed-Wiki); C3 läuft ab 2.0.8 |
| WiFi/Webserver/mDNS | `WiFi.h`, `WebServer.h`, `ESPmDNS.h` | im Core enthalten; für `growpot.local` |
| Bodensensor | **keine Library** | `analogReadMilliVolts()` + Glättung selbst |
| OLED | `Adafruit SSD1306` + `Adafruit GFX` (oder `U8g2`) | I2C an D4/D5 |
| Telegram | `UniversalTelegramBot` + `ArduinoJson` | HTTPS per `WiFiClientSecure` — C6/C3 haben HW-Krypto |
| Parameter-Speicher | `Preferences.h` | NVS, im Core — Kalibrierung + Schwellwerte |
| Optional OTA | `ArduinoOTA.h` | Updates ohne USB-Kabel am Topf |
| Optional MQTT | `PubSubClient` | falls Home Assistant per MQTT (Alternative: Matter) |
| Optional nicht-blockender Webserver | `ESPAsyncWebServer` + `AsyncTCP` (me-no-dev) | sauberer als `WebServer.h`, wenn UI komplexer wird |

---

## 9. Energie-Optionen (Kurzfassung)

- **Standard:** USB-Netzteil 5 V ≥ 1 A (dauerhaft an). Pumpe hängt an der 5-V-Schiene, ESP läuft durch.
- **Akkubetrieb:** XIAO lädt LiPo onboard. Zwischen Messungen `light_sleep` (C6: ~3,1 mA, WiFi bleibt über Modem-Sleep erreichbar) oder Deep Sleep mit Timer-Wakeup (15 µA, Webserver dann nur periodisch erreichbar — Trade-off). Der LP-Core des C6 könnte später sogar den kompletten Messzyklus im Schlaf abwickeln.

---

## 10. Ausbaustufen (Roadmap)

| Stufe | Inhalt |
|---|---|
| **V1** (dieses Konzept) | Sensor → Pumpe → Delta-Erkennung, LED + OLED + Webserver + Telegram |
| V1.5 | Manuelle Kalibrier-Routine im Webserver (trocken/nass-Taste), Tagesliter-Limit |
| V2 | Direkte Tank-Überwachung (XKC-Y25 oder Schwimmerschalter) + INA219-Pumpstrom → „leer" vs. „verstopft" unterscheidbar, Vorwarnung bei niedrigem Pegel statt erst bei Leer |
| V3 | Matter-Integration (C6 nativ) in Home Assistant; Deep-Sleep-Akkubetrieb mit LP-Core |
