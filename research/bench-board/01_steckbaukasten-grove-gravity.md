# 01 — Steckbaukasten-Weg für das Bench-Board (Grove / Gravity / Qwiic-STEMMA / M5Stack-Units)

Ziel: die komplette Peripherie (2 Pumpen, 2 analoge Sensoren, Taster, 2 LEDs, WLAN, Deep-Sleep, ggf. Akku)
**ohne Löten** an EIN Board stecken. Stand 2026-10-09, Preise DE aus Produktseiten (BerryBase, Seeed, DFRobot, M5Stack).

## Prüfliste, was angesteckt werden muss
Pumpe 5 V/0,4 A (3 A Anlauf) · Luftpumpe 5 V/0,2 A · kapazitiver Bodenfeuchtesensor **analog** (0–3 V) ·
Fototransistor (analog) · Taster mit Wake · 2 LEDs · WLAN · Deep-Sleep · 1S-Akku (optional).

## Nachprüfung Hermes 09.10.2026 (Preise, Verfügbarkeit)

- **Seeed XIAO ESP32-C6 = 7,49 € bei Reichelt** (Art.-Nr. `XIAO ESP32C6 H`, ab Lager, 1–2 Werktage, inkl. MwSt.):
  <https://www.reichelt.de/de/de/shop/produkt/xiao_esp32c6_wifi_6_bt5_0_zigbee_thread_mit_header-406831>.
  Bei **BerryBase 8,50 €, aber „Artikel aktuell nicht lieferbar"**.
- **Grove-Shield für XIAO (mit Batteriemanagement) = 5,00 € BerryBase — ebenfalls „aktuell nicht lieferbar"**
  (<https://www.berrybase.de/seeed-grove-shield-fuer-seeeduino-xiao-mit-eingebettetem-batterie-management-chip>).
  → Der komplette Steckweg ist derzeit **nur teilweise beschaffbar**; Verfügbarkeit vor der Bestellung prüfen.
  BerryBase führt zusätzlich ein **XIAO ESP32-C6 6-Kanal-Relaismodul** (Preis nicht ausgelesen).
- **FireBeetle 2 ESP32-C6 = 9,95 € bei Eckstein**
  (<https://eckstein-shop.de/DFRobot-FireBeetle-2-ESP32-C6-IoT-Development-Board-EN>), DFRobot-Shop $6,90 (lagernd);
  BerryBase-Listing 6,30 € „nicht lieferbar". **ESP32-C6-DevKitC-1 = 11,95 € Reichelt** (ab Lager).

---

## (a) Ökosystem-Tabelle

| Ökosystem | Board | MCU | WLAN | Akku/Laden | freie IO | Analog-IN | Aktor-Kanäle | Anschlussart | Sleep | Preis (DE) | Link |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **M5Stack** | CoreS3 (K128) | ESP32-S3 @240 MHz | ja 2,4 G | LiPo onboard + USB-C/Type-C laden (PMU AXP2101) | Grove A/B/C + Unit-Port | nur über **ADC-Unit** (ADS1100, 16 bit, I2C) → nativ kaum ADC-Pins | 4-Relay Unit (4× potenzialfrei, 10 A/16 A impuls) | Grove HY2.0-4P / Unit-Port | AXP2101-Low-Power, **µA-Wert unbelegt** | **€75,60** (BerryBase, aktuell nicht lieferbar) | [1][2][4][5] |
| **Seeed XIAO/Grove** | XIAO ESP32-C6 + Grove Shield | ESP32-C6 RISC-V @160 MHz | ja Wi-Fi 6 | Ladung onboard (am Board + Batterie-Management auf Grove-Base) | ~11 GPIO, über Shield als Grove geführt | 12-bit ADC, analoge Grove-Ports am Shield | Grove-Relay (10 A) 1–2 Kanäle; Grove-MOSFET | **Grove HY2.0-4P (4-pol)** | **15 µA** Deep-Sleep | XIAO **€8,50** + Grove-Shield **€5,00** | [10][11] |
| **DFRobot Gravity** | FireBeetle 2 ESP32-C6 (DFR1075) | ESP32-C6 @160 MHz | ja Wi-Fi 6 | LiPo-Interface onboard (BAT), **0,5 A** Ladestrom, Solar/VIN 5 V | 7× ADC + viele GPIO | **1× 12-bit SAR-ADC, 7 Kanäle** | Gravity-MOSFET (20 A DC) / Gravity-Relais | **Gravity PH2.0-3P (3-pol)** + 0,1"-Header | **16 µA** (v1.0) / 36 µA (v1.2) | **€6,90** | [8][9] |
| **Adafruit STEMMA** | ESP32-S3 Feather (STEMMA QT) | ESP32-S3 @240 MHz | ja | LiPo-JST + Ladung onboard | viele GPIO | STEMMA = **nur I2C**; analog nur über JST/Header | MOSFET-/Relais-Breakouts (löten/stecken) | **STEMMA QT / Qwiic (JST-SH, I2C)** + JST-PH | tief, µA u.a. | **$17,50** | [19] |

**Steck-Falle:** Grove (4-pol HY2.0) und Gravity (3-pol PH2.0) sind **nicht** kreuzbar — innerhalb eines
Ökosystems stecken, sonst Adapterkabel nötig.

## (b) Einkaufsliste — bester Weg: **Seeed XIAO ESP32-C6 + Grove** (alles 4-pol-Plug, kein Löten)

| # | Teil | Zweck | Preis | Quelle |
|---|---|---|---|---|
| 1 | Seeed XIAO ESP32-C6 | MCU, Wi-Fi 6, 15 µA Sleep | **€8,50** | [10] |
| 2 | Grove Shield for XIAO (Batterie-Management + Grove-Ports) | Grove-Bus + 1S-Akku-Ladung | **€5,00** | [11] |
| 3 | Grove – Capacitive Soil Moisture Sensor (analog, korrosionsfest) | Feuchte (analog) | **€5,90** | [12] |
| 4 | Grove – Light Sensor (Phototransistor, analog) | Licht (analog) | **$2,90** | [14] |
| 5 | Grove – Button | Taster/Wake | ~$1,90¹ | [15] |
| 6 | 2× Grove – LED (rot/blau, „LED Button") | 2 Status-LEDs | ~2× $2,00¹ | [16] |
| 7 | Grove – Relay (mechanisch, 5 V/10 A, potenzialfrei) | schaltet 5-V-Leitung der Pumpe | ~$2,99¹ | [17] |
| 8 | Grove – MOSFET (CJQ4435), *Alternative zu #7* | schnelles Schalten | **€4,50** | [13] |
| 9 | Grove-Kabelsatz (Ersatz-/Verlängerungskabel) | Kabelvorrat | ~€4,00 | Seeed |
| 10 | 1S LiPo (z. B. 1000 mAh) + JST-Stecker | mobil testen | ~€6,00 | — |
|  | **Summe ca.** | | **≈ €44 (ohne #8) / ≈ €48 (mit #8)** |  |

¹ Seeed-Listenpreis (USD), in Deutschland zzgl. Versand/Umrechnung — als **unbelegt** markiert, da nicht in DE-Produktseite bestätigt.
Alternative mit Display statt #2: **XIAO Expansion Board mit Grove-OLED** $14,90 (inkl. I2C/UART/Analog-Digital-Grove und RTC) [18].

**Warum dieser Weg:** jedes Modul ist ein Grove-4-pol-Stecker (einfach reinstecken); 15 µA Deep-Sleep,
Wi-Fi 6, 12-bit-ADC **und** Akku-Ladung sind schon an Bord; der Grove-Relaiskontakt ist potenzialfrei
und mit 10 A/16 A impuls weit über dem Pumpen-Anlaufstrom (3 A). Sensor #3 ist der **analoge**
kapazitive Sensor (nicht das digitale Schwellwert-Modul).

## (c) Was dieser Weg NICHT kann / Grenzen

- **Pumpen-Anlaufstrom 3 A:** Grove-Relais (10 A) trägt das locker, ist aber **mechanisch** (Klacken,
  begrenzte Schaltspiele). Der Grove-MOSFET (CJQ4435, [13]) ist schnell, aber seine Dauerstrom-Grenze
  am Modul ist niedrig — für 0,4 A Nenn / 3 A Impuls am 5-V-Lastkreis ok, bei Dauerlast prüfen. Robuster:
  Gravity MOSFET Power Controller (20 A DC, $3,90, [6]) — passt aber nur ans Gravity-Ökosystem.
- **Analoger Bodenfeuchtesensor nur invertiert & unkalibriert:** Ausgang 1,2–2,5 V [12] liegt im
  ADC-Bereich, ESP32-ADC ist aber nahe den Rails nichtlinear → Software-Kalibrierung nötig.
- **Kein separater 3,3-V-Analogbereich:** XIAO/FireBeetle ADCs messen gegen 3,3 V; 5-V-Analogsensoren
  brauchen Teiler. Der Grove-Sensor liefert aber ≤2,5 V (3,3-V-kompatibel).
- **Deep-Sleep-µA exakt:** nur XIAO (15 µA) und FireBeetle (16/36 µA) sind **belegt**; beim M5Stack
  CoreS3 ist der Low-Power-Modus dokumentiert, der konkrete µA-Wert aber **unbelegt**.
- **M5Stack-Sonderfall:** analog nur über die **ADC-Unit (ADS1100, 16 bit)** — die ist **EOL** [5];
  außerdem passt der Gravity-Bodenfeuchtesensor physisch **nicht** an Grove (Adapter nötig).
- **Löten:** XIAO nur mit **Pre-Soldered**-Variante wirklich steckfertig; FireBeetle 2 kommt mit
  0,1"-Headern (Steckverbinder = Dupont, streng genommen kein „Plug"). M5Stack-CoreS3 ist als
  einziges Board ab Werk zu 100 % steckfertig — dafür teuer und derzeit nicht lieferbar [4].
- **Beide Pumpen** brauchen ein **eigenes 5-V-Netzteil** (Bench), plus gemeinsame Masse zum Board.

## Quellen
1. M5Stack CoreS3 Docs — https://docs.m5stack.com/en/core/CoreS3
2. M5Stack 4-Relay Unit (U097, 10 A/16 A) — https://shop.m5stack.com/products/4-relay-unit
4. M5Stack CoreS3 BerryBase €75,60 — https://www.berrybase.de/en/m5stack-cores3-esp32s3-lot-dev-kit
5. M5Stack ADC Unit (ADS1100, 16 bit, EOL) $5,50 — https://shop.m5stack.com/products/adc-unit
6. DFRobot Gravity MOSFET Power Controller (DFR0457, 5–36 V, 20 A DC) $3,90 — https://www.dfrobot.com/product-1567.html · Wiki https://wiki.dfrobot.com/dfr0457/
8. FireBeetle 2 ESP32-C6 Wiki (12-bit 7-Kanal-ADC, 16/36 µA, BAT, 0,5 A Laden) — https://wiki.dfrobot.com/dfr1075/
9. FireBeetle 2 ESP32-C6 BerryBase €6,90 — https://www.berrybase.de/en/dfrobot-firebeetle-2-esp32-c6-iot-dev-board-wi-fi-6-bt-5-zigbee-3.0-solar-operation-160mhz-3.3v
10. Seeed XIAO ESP32-C6 BerryBase €8,50 (15 µA Deep-Sleep, LiPo-Ladung) — https://berrybase.de/en/seeed-xiao-esp32-c6-wi-fi-6-ble-5.0-zigbee-thread-512kb-sram-4mb-flash-uart-spi-risc-v
11. Grove Shield for XIAO BerryBase €5,00 — https://berrybase.de/en/seeed-grove-shield-for-seeeduino-xiao-with-embedded-battery-management-chip · Datasheet https://files.seeedstudio.com/Bazaar/product_pdf/103020312.pdf
12. DFRobot kapazitiver Bodenfeuchtesensor SEN0193 BerryBase €5,90 (analog 1,2–2,5 V, 3,3–5,5 V) — https://www.berrybase.de/en/dfrobot-capacitive-soil-moisture-sensor-3-pin-analogue-output-corrosion-resistant-3.3-5.5v
13. Seeed Grove MOSFET (CJQ4435) BerryBase €4,50 — https://berrybase.de/en/seeed-grove-mosfet-cjq4435
14. Seeed Grove Light Sensor (analog) $2,90 — https://www.seeedstudio.com/Grove-Light-Sensor-p-746.html
15. Seeed Grove Button — https://www.seeedstudio.com/Grove-Button.html
16. Seeed Grove Red LED Button — https://www.seeedstudio.com/Grove-Red-LED-Button.html
17. Seeed Grove Relay (5 V/10 A mechanisch) — https://www.seeedstudio.com/Grove-Relay-p-769.html
18. Seeed XIAO Expansion Board m. Grove-OLED ($14,90) — siehe Listing https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html
19. Adafruit ESP32-S3 Feather STEMMA QT $17,50 — https://www.adafruit.com/product/5323
