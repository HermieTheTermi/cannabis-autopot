# Fertige Bewässerungs-/Grow-Controller-Platinen für den Smart Grow Topf

Recherchestand: 2026-10-09. Ziel: Prüfen, ob eine FERTIGE Platine/Baugruppe die Anwendung
„automatische Bewässerung mit kapazitivem Bodenfeuchtesensor" ganz/teilweise abdeckt.

Projekt-Sollprofil: **Akku** (LiIon/LiPo, USB-Laden) · **analoger kapazitiver Bodenfeuchtesensor
+ echter Regelkreis** (Nachmessung) · **Peristaltik-/Dosierpumpe** (5 V, 0,4 A, 3 A Anlauf) ·
**lokale Logik** ohne Cloud-Zwang, lokaler Alarm (Telegram/Webhook/Home Assistant) ·
**Lichtsensor/Dunkel-Gate** · **offene Firmware** (ESPHome/Arduino/PlatformIO) ·
Bauform für Topf Ø 140 mm · Bezug DE/EU.

## 1. Nachprüfung Hermes 09.10.2026

**⚠️ DROPLET ist derzeit nicht kaufbar:** Produktseite am 09.10.2026 — **„Out of Stock", „Sold out since
May 04, 2026"**, Versandangaben widersprüchlich. Der Kandidat bleibt fachlich der beste, ist aber
**kein beschaffbares Produkt**; Wiederverfügbarkeit nur über Benachrichtigung abwarten.
Preis $87,00 und „ESP32 + ESPHome" sind auf der Seite bestätigt.

---

## 4. Verdikt

**Nein** — kein Fertigprodukt deckt das Gesamtpaket (Akku + Feuchte-Regelkreis + Dosierpumpe +
lokaler Alarm + Dunkel-Gate) ab; **bester Kandidat ist DROPLET** (ESP32+ESPHome, analoge
kapazitive Sensoren, Mikropumpen-Anschlüsse, lokaler Buzzer), dem aber Akkubetrieb/USB-Laden,
garantierte Peristaltik und Lichtsensor fehlen.

## 2. Prüfliste (Sollprofil) je Kandidat

| # | Kriterium | DROPLET | Smart Garden | OpenSprinkler Pro | Root-PCB / T-HiGrow |
|---|---|---|---|---|---|
| 1 | Akku/USB-Laden | **nicht** (DC-Hohlstecker DC-005 2.0) | **nicht** (USB-C + 24 VAC-Versorgung) | **teilweise** (DC-Variante für Batterie/Solar, kein onboard-Laden) | nicht (Monitor) |
| 2 | Analoger kapazitiver Sensor + Regelkreis | **teilweise** (5× analoge 3-Pin-Sensorports, Regelung selbst in ESPHome zu bauen) | **teilweise** (4 analoge Inputs, Regelung selbst) | **teilweise** (2 Sensor-Eingänge, primär Zeitplan/Wetter) | Sensor ja, Regelkreis nein |
| 3 | Peristaltik-/Dosierpumpe | **teilweise** (5× JST-2Pin „micropumps", Art nicht spezifiziert) | teilweise (Relais für „valves and/or water pumps") | **nicht** (Magnetventile 24 VAC/DC/Latch) | nicht |
| 4 | Lokale Logik + lokaler Alarm | **ja** (ESPHome lokal, Buzzer onboard, Telegram via HA) | **ja** (ESPHome/Arduino lokal, open source) | **ja** (offene Firmware, Web/App lokal, MQTT) | nein |
| 5 | Lichtsensor/Dunkel-Gate | **nicht** onboard (freie GPIOs) | **nicht** onboard | **nicht** onboard | T-HiGrow: Licht ja (nur Sensor) |
| 6 | Offene Firmware/Schnittstelle | **ja** (ESPHome, GitHub) | **ja** (ESPHome/Arduino, GitHub, OTA) | **ja** (OpenSprinkler-Firmware, GitHub) | nein (nur Sensor-Daten) |
| 7 | Bauform Topf Ø 140 mm | nein (Mainboard + Expansion, größer) | knapp (Boardfläche, unbelegt) | nein (Gehäuse, 8–72 Zonen) | nein (nur Sensor) |
| 8 | Bezug DE/EU + Preis | Tindie (FR-Shop), $87 | Tindie (ES), $34.99 | opensprinklershop.de, 269–309 € | Tindie (GR), $9.28 (Snippet) |

## 3. Kandidaten-Tabelle

| Produkt | Preis | Antrieb/Mechanik | Sensorik | Regelkreis/Zeitplan | Vernetzung | Akku | fehlende Achsen | Link |
|---|---|---|---|---|---|---|---|---|
| **DROPLET** (PricelessToolkt, FR) | **$87,00** | 5× JST-2Pin Mikropumpen (Art nicht spezifiziert) | 5× analoge 3-Pin Soil-Ports (1 MΩ) + DS18B20 | offen: Regelung selbst via ESPHome | ESP32 WiFi, Home Assistant | nein (Hohlstecker DC-005) | Akku/USB-Laden, Lichtsensor, Peristaltik unbelegt, Bauform | [Tindie](https://www.tindie.com/products/pricelesstoolkit/droplet-smart-irrigation-system/) |
| **Smart Garden** (J.G.Aguado, ES) | **$34,99** | 4 Relais für „valves and/or water pumps" | 4 analoge + 8 Aux-I/O, I2C/Serial | offen: Regelung selbst (ESPHome/Arduino) | ESP32-S2 WiFi, HA | nein (USB-C + 24 VAC) | Akku-Laden, Lightgate, onboard-Sensor, 5-V-Pumpe via Relais | [Tindie](https://tindie.com/products/themakerllama/smart-garden) · [GitHub](https://github.com/JGAguado/Smart_Garden) |
| **OpenSprinkler Pro** | **269–309 €** | Magnetventile 24 VAC / 9–24 V DC / Latch (8–72 Zonen) | 2 Sensor-Eingänge (Regen/Feuchte/Flow), BLE/MQTT/Modbus | primär Zeitplan + Wetter (Zimmerman/ETo), Feuchte als Restriktion | ESP32-C5, WiFi6/BLE/Zigbee/Matter, Web/App/OLED | DC-Variante für Batterie/Solar (kein Laden) | Dosierpumpe, Akku-Laden, onboard-Feuchteregelkreis, Bauform, Preis | [opensprinklershop.de](https://opensprinklershop.de/en/product/opensprinkler-pro/) |
| OpenSprinkler ESP32-Upgrade-Board | 99 € (statt 129 €) | wie oben (Ventile) | 2 Sensor-Eingänge | wie oben | wie oben | nein | wie oben | [Shop](https://opensprinklershop.de/en/product/esp32-board-fuer-opensprinkler-3-3-upgrade/) |
| **Root – Plant Monitoring PCB** (Sprig Labs, GR) | **$9,28** | *keine* (reines Monitoring) | Boden/Feuchte, Licht, Temp, Luftfeuchte | nein | ESPHome | nein | Pumpe, Regelkreis, Akku, Lichtgate steuern | [Tindie](https://www.tindie.com/products/spriglabs/root-complete-plant-monitoring-pcb/) |
| **T-HiGrow** (LILYGO) | **$10,36** | *keine* (Sensorboard) | Bodenfeuchte, BME280, Licht | nein | ESP32 WiFi/BLE | nein | Pumpe, Regelkreis, Akku | [lilygo.cc](https://lilygo.cc/en-us/products/t-higrow) |
| Solar Soil Moisture Probe (Garden Tinkerer, CA) | $40 (Snippet) | *keine* (Probe) | Bodenfeuchte | nein | HA | Solar (Sensor) | alles außer Sensor | [Tindie](https://www.tindie.com/products/gardentinkerer/solar-powered-soil-moisture-probe/) |
| Tuya/WLAN-Bewässerungstimer (allg.) | ~10–40 € | Magnetventil/Kreiselpumpe | Feuchte optional | **Zeitplan** (kein Sensorregelkreis) | Cloud/Tuya-App | teils Batterie | Regelkreis, Dosierpumpe, offene FW | [Beispiel](https://www.domadoo.fr/en/205-smart-life-tuya-compatible-products) |

*Preise: DROPLET, Smart Garden, OpenSprinkler Pro von der Produktseite geprüft; mit „(Snippet)" markierte Preise stammen nur aus dem Suchtreffer-Snippet und sind **nicht** auf der Produktseite verifiziert. „unbelegt" = keine belastbare Angabe gefunden.*

**Reine DIY-/GitHub-Projekte (nicht kaufbar, nur als Vorlage):** `ginkel/esp32-c3-irrigation-controller`
(ESP32-C3, 2× 12-V-Pumpenkanäle, custom PCB), `har-in-air/ESP32_AUTO_WATER` (C3 + kapazitiver Sensor
+ RTC), `makstech/esphome-irrigation-system`, `Plant1337`. — [github.com/ginkel/esp32-c3-irrigation-controller](https://github.com/ginkel/esp32-c3-irrigation-controller)

## 4. Modul-Baukasten (kein Löten/Routen)

**Teilweise ja.** Mit Qwiic/STEMMA/Grove lässt sich die Schaltung als Steckbaukasten
zusammenstecken: ESP32-S3-Board mit Qwiic, kapazitiver Feuchtesensor, MOSFET/Relais-Modul für
die Pumpe, LiPo-Boost/Charger — alles ohne Löten, aber **keine fertige Gesamtbaugruppe** und
kein ESPHome-Produkt „von der Stange" mit Dunkel-Gate.

## 5. Quellen

- DROPLET (Tindie, Preis $87 / Pins / DC-005): https://www.tindie.com/products/pricelesstoolkit/droplet-smart-irrigation-system/
- DROPLET Firmware/Docs: https://github.com/PricelessToolkit/Droplet
- Smart Garden (Tindie, Preis $34.99, ESP32-S2, ESPHome/OTA): https://tindie.com/products/themakerllama/smart-garden
- Smart Garden Docs/GitHub: https://smart-garden.readthedocs.io/ · https://github.com/JGAguado/Smart_Garden
- OpenSprinkler Pro (opensprinklershop.de, Preis 269–309 €, Ventile/Sensoren): https://opensprinklershop.de/en/product/opensprinkler-pro/
- OpenSprinkler ESP32-Upgrade-Board (99 €): https://opensprinklershop.de/en/product/esp32-board-fuer-opensprinkler-3-3-upgrade/
- Root Plant Monitoring PCB ($9.28 Snippet): https://www.tindie.com/products/spriglabs/root-complete-plant-monitoring-pcb/
- T-HiGrow ($10.36 Snippet): https://lilygo.cc/en-us/products/t-higrow
- Solar Soil Moisture Probe ($40 Snippet): https://www.tindie.com/products/gardentinkerer/solar-powered-soil-moisture-probe/
- Tuya/WLAN-Bewässerungstimer (Zeitplan): https://www.domadoo.fr/en/205-smart-life-tuya-compatible-products
- DIY-Vorlagen: https://github.com/ginkel/esp32-c3-irrigation-controller · https://github.com/har-in-air/ESP32_AUTO_WATER
