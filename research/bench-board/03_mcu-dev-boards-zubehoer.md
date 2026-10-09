# 03 — MCU-Entwicklungsboards als Labortisch-Träger (Größe/MCU egal) + Zubehör

**Frage:** Bestes MCU-Entwicklungsboard als *Träger am Labortisch* (Größe/MCU egal) + Zubehör.
**Peripherie:** 2× analog (Bodenfeuchte 0–3,0 V, invertiert trocken=hoch; Lichtsensor) · 2× Pumpe (Peristaltik 5 V/0,4 A, **~3 A Anlauf** → PWM-Softstart; Luftpumpe 5 V/0,2 A) · Taster mit **Wake aus Deep-Sleep** · 2× LED · **Telegram über WLAN/TLS**. Endgerät-Ziel = **ESP32-C6**.

> Specs aus Hersteller-Seiten (verlinkt); Preise nur mit Produktseiten-Beleg, sonst „unbelegt" (Preis-Runde außer Budget). Abk.: **A**=Arduino, **PIO**=PlatformIO, **IDF**=ESP-IDF, **MPY**=MicroPython, **CPS**=CircuitPython; alle ADC 0–3,3 V.

## (a) Board-Vergleich

| Board | Preis | MCU | WLAN | ADC (bit/K.) | freie GPIO | Sleep | Lader onboard | Umgebung | **Nachteil** | Link |
|---|---|---|---|---|---|---|---|---|---|---|
| **ESP32-C6-DevKitC-1** | **11 €** (Reichelt) | ESP32-C6 | ja (WiFi6) | 1× 12 / **7** (ADC1 IO0–IO6) | ~15 | ~7 µA SoC / 15 µA Board | – | A/PIO/IDF/MPY | kein Lader; nur 1 ADC; C6-ADC am rauschigsten | [Espressif](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/user_guide.html) |
| **ESP32-S3-DevKitC-1** | unbelegt (US $15,95) | ESP32-S3 | ja | **2× 12 / 20** (ADC1 IO1–10, ADC2 IO11–20) | **~34** | ~10 µA SoC | – | A/PIO/IDF/MPY | kein Lader; ADC unkalibriert → Rauschen | [Espressif](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html) |
| **ESP32-WROVER-KIT** | unbelegt | ESP32 (classic) | ja | 2× 12 / 18 (ADC1 IO32–39) | viele, LCD/Kamera belegen | ~10 µA | – | A/IDF | alt/groß; LCD+Kamera unnötig; kein Lader | [Espressif](https://docs.espressif.com/projects/esp-dev-kits/en/latest/) |
| **Pi Pico 2 W** | unbelegt (~7 €) | RP2350 | ja | 12 / **3** (IO26–28)+Temp | ~26 | ~**1,4–1,6 mA** dormant; deepsleep ~30–100 µA | – | C-SDK/MPY/Arduino-Pico | kein Lader; 3 ADC-Kanäle; hoher Sleep; TLS/Telegram mühsamer | [RPi-Forum](https://forums.raspberrypi.com/viewtopic.php?t=390230) |
| **Teensy 4.1** | unbelegt (~30 €) | i.MX RT1062 M7 600 MHz | **nein** | 12 / ~18 analoge Pins | ~40+ | kein tiefer Sleep (unbelegt) | – | A/PIO | **kein WLAN** → Telegram-Bruch; kein Lader | [PJRC](https://www.pjrc.com/store/teensy41.html) |
| **Nucleo-F411RE** | unbelegt (~15 €) | STM32F411 M4 100 MHz | nein | 1× 12 / **16**, 2,4 MSPS | ~50 | µA (STOP/STANDBY) | – | CubeIDE/PIO | kein WLAN/Lader; 5-V-Arduino-Header | [ST](https://www.st.com/en/evaluation-tools/nucleo-f411re.html) |
| **Nucleo-H723ZG** | unbelegt (~25–30 €) | STM32H723 M7 550 MHz | nein | **3× 16**, differenziell | sehr viele | µA | – | CubeIDE/PIO | kein WLAN/Lader; überdimensioniert | [ST](https://www.st.com/en/evaluation-tools/nucleo-h723zg.html) |
| **Arduino Giga R1 WiFi** | unbelegt (~75 €) | STM32H747 (M7+M4) | ja (Murata) | 12 (16-fähig) / 12 | viele | unbelegt | – | A/PIO | teuer; kein Lader; 5-V/3,3-V-Mix | [Arduino](https://docs.arduino.cc/tutorials/giga-r1-wifi/giga-audio) |
| **Arduino UNO R4 WiFi** | unbelegt (~30 €) | RA4M1 (+ESP32-S3 Co-Proz.) | ja (Co-Proz.) | **14** / 6, 0–5 V | ~20 | unbelegt | – | A/PIO | 5-V-Referenz; kein Lader; WLAN über Co-Prozessor | [Arduino](https://docs.arduino.cc/) |
| **Adafruit Feather ESP32-S3 (#5323)** | unbelegt (DE ~22–26 €) | ESP32-S3 | ja | 12 / mehrere | ~21 + **STEMMA QT** | ~100 µA (Board-Regler) | **✓ USB-C+LiPo, MAX17048** | A/PIO/CPS | teurer; weniger Pins; hoher Sleep | [Adafruit](https://adafruit.com/product/5323) |
| **FireBeetle 2 ESP32-C6 (DFR1075)** | unbelegt (~10–12 €) | **ESP32-C6** | ja | 12 / ADC1 IO0–IO6 | ~15 | ~15 µA | **✓ Type-C/5 V/Solar** | A/PIO/IDF | Batterie-Teiler **1 MΩ** zu hochohmig; dünnere Doku | [DFRobot](https://wiki.dfrobot.com/dfr1075/) |
| **Seeed XIAO ESP32C6** | unbelegt (~7–9 €) | ESP32-C6 | ja | 12 / ~7 | **11** | **15 µA** | **✓ Lade-/Entlademgmt.** | A/PIO/MPY/IDF | nur 11 GPIO; SMD-fummelig; zu klein für Tisch | [Seeed](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/) |

## (b) Empfehlung

### ★ #1 — Adafruit ESP32-S3 Feather (#5323)
Einziges Board, das alles **gleichzeitig** kann bei minimalem Verdrahtungsaufwand: **ESP32-S3 + natives WLAN** (gleicher Arduino/ESP-IDF-Stack, gleiche LEDC-/ADC-API wie das C6-Endgerät → Code-Reuse; `UniversalTelegramBot`+`WiFiClientSecure` können TLS), **Onboard-1S-Ladung + MAX17048-Fuel-Gauge** (läuft akkulos wie das Produkt), **STEMMA-QT/Qwiic** für Sensoren ohne Löten; zwei getrennte SAR-ADCs trennen Boden- und Lichtsensor, 16 LEDC-PWM-Kanäle decken den Softstart.
**Nachteil:** ~**100 µA** Deep-Sleep (Board-Regler, nicht SoC) und weniger gebrochene Pins als ein DevKitC.

### #2 (ohne ESP32) — Raspberry Pi Pico 2 W
Natives WLAN, saubererer 12-bit-ADC, großes Ökosystem, billig; Telegram via `urequests`/`ssl` (MPY) bzw. `WiFiClientSecure` (arduino-pico). **Nachteile:** kein Onboard-Lader; **~1,4–1,6 mA** dormant (schlecht für wochenlangen Akku-Deep-Sleep); nur **3** Nutz-ADC-Kanäle.

**Ebenfalls:** exakt gleicher MCU wie im Endgerät → **FireBeetle 2 ESP32-C6** (C6-Zielplattform + Akku/Solar-Ladung; Haken: 1-MΩ-Batterie-Teiler). Max. Pins, günstigst → **ESP32-S3-DevKitC-1** (alle GPIO auf 2,54 mm, 20 ADC-Kanäle, kein Lader).

> **Fazit:** WLAN **+** reifste Telegram/TLS-Bibliothek liefert nur die ESP32-Familie; STM32/Nucleo/Teensy haben bessere ADCs, aber **kein** WLAN → die WLAN-/Telegram-Anforderung entscheidet. Die ESP32-ADC-Schwäche ist per Median/Mittelung + Substratkalibrierung abgefangen (`research/kapazitiver-bodenfeuchtesensor-esp32-recherche.md`).

## (c) Einkaufsliste (Labortisch, Variante #1)

| Pos. | Artikel | Preis | Link |
|---|---|---|---|
| 1 | **Adafruit ESP32-S3 Feather (#5323)** (Lader + STEMMA QT) | unbelegt | https://adafruit.com/product/5323 |
| 2 | 2-Kanal-MOSFET-Modul (Logikpegel, ≥ 3 A) — o. 2× AO3400A + 220 Ω/10 kΩ/100 µF (Projekt-Stand) | unbelegt | Reichelt/Amazon |
| 3 | Breadboard + Dupont-Kabel + Schraubklemmen-Adapter auf 2,54 mm | unbelegt | BerryBase/Reichelt |
| 4 | STEMMA-QT-Kabel (I²C) | unbelegt | https://adafruit.com/product/4209 |
| 5 | USB-C-Netzteil 5 V **≥ 3 A** (Anlaufstrom!) | unbelegt | Amazon |
| 6 | 1S-LiPo (EFASO 503759 1500 mAh, JST PH) | ~14,90 € | efaso.de |
| | **Summe** | **unbelegt** | |

**Variante „Budget/Max-Pins":** Pos. 1 → [ESP32-S3-DevKitC-1](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html) + zusätzlich **TP4056-1S-Lader** (USB-C).

**Verifikation:** Nur **ESP32-C6-DevKitC-1 = 11 € (Reichelt)** + BOM **EFASO 14,90 €** belegt; alle übrigen Preise **unbelegt**. Aktuell prüfen (BerryBase, Eckstein, Reichelt, Mouser/DigiKey, Amazon.de).

## Quellen (09.10.2026)
- **Espressif:** [C6-DevKitC-1](https://documentation.espressif.com/esp-dev-kits/en/latest/esp32c6/esp32-c6-devkitc-1/user_guide.html) · [S3-DevKitC-1](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html) · [ADC-Doku](https://docs.espressif.com/projects/esp-idf/en/v4.4/esp32/api-reference/peripherals/adc.html)
- **Pico 2 W:** [RPi-Forum](https://forums.raspberrypi.com/viewtopic.php?t=390230) · **Teensy 4.1:** [PJRC](https://www.pjrc.com/store/teensy41.html) · **Nucleo:** [ST](https://www.st.com/en/evaluation-tools/nucleo-f411re.html) · [Zephyr](https://docs.zephyrproject.org/latest/boards/st/nucleo_f411re/doc/index.html)
- **Arduino:** [Giga R1 ADC](https://docs.arduino.cc/tutorials/giga-r1-wifi/giga-audio) · **Feather:** [Adafruit](https://adafruit.com/product/5323) · **FireBeetle:** [DFRobot](https://wiki.dfrobot.com/dfr1075/) · **XIAO:** [Seeed](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/)
- **Preis belegt:** [Reichelt ESP32-C6-DevKitC-1 = 11 €](https://www.reichelt.com/de/en/shop/product/esp32-c6-wroom-1_u_development_board-380385) · **Projekt:** `research/kapazitiver-bodenfeuchtesensor-esp32-recherche.md`, `research/smart-grow-topf-esp32-firmware-konzept.md`
