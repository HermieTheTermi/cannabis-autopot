# 3D-Drucker-Mainboards & Maschinensteuerungen als Fertigplatine

Projekt: „Smart Grow Topf" (cannabis-autopot) — automatisch bewässernder Topf, 1 Pflanze, Akku, ESP32, WLAN/Telegram-Alarm.
Frage: Taugt ein 3D-Drucker-Mainboard als **fertige** Platine statt Eigenentwicklung?

Stand: 2026-10-09 · Quellen = Links; Nicht-Belegbares = **unbelegt**.

## 1. Anforderungen (Prüfliste)

| # | Anforderung | 3D-Drucker-Mainboards |
|---|-------------|-----------------------|
| 1 | ESP32-Klasse MCU (WLAN + Deep-Sleep + ADC) | **teilweise** — meist STM32 (kein WLAN/kein Deep-Sleep); ESP32 nur bei TinyBee, Mellow-Boards (optional) |
| 2 | 2S-Akku laden/Balancieren/UVLO über USB-C | **nicht** — nur 12–24 V DC-Netzeingang, kein Ladepfad, kein BMS |
| 3 | 5 V/3 A + 3,3 V/2 A | **teilweise** — Buck TPS5450 liefert 5 V/5 A (6 A peak), 3,3 V logik onboard |
| 4 | Unterspannungswächter ~6,16 V | **nicht** — Schwellen liegen auf 12/24-V-Netz ausgelegt |
| 5 | 2× Low-Side-MOSFET-Ausgänge | **erfüllt** — Heizung/Bett/Lüfter sind genau Low-Side-MOSFETs |
| 6 | 2× Analog 0–3,3 V | **teilweise** — Thermistor-ADC 0–3,3 V, aber mit Pull-up/Spannungsteiler |
| 7 | Wake-Taster, 2 LEDs, freie GPIOs | **teilweise** — viele IO frei, aber kein Deep-Sleep-Wake-Konzept |
| 8 | Baugröße ≤ 54 × 80 mm | **nicht** — kleinste Boards ~110 × 85 mm |
| 9 | Preis + Verfügbarkeit DE | **erfüllt** — günstig und in DE lieferbar |

## 2. Kandidaten im Detail

### 2.1 MKS TinyBee (ESP32) — bester „Kandidat"
- MCU **ESP32-WROOM-32U** (240 MHz, 8 MB Flash, 520 KB RAM), WLAN onboard · Eingang **DC 12–24 V**, Verpol- + Spannungsspitzenschutz → [github.com/makerbase-mks/mks-tinybee](https://github.com/makerbase-mks/mks-tinybee)
- 2 Heizausgänge (E0/E1) + 1 Bett, 3× NTC100K (TH1/TB/TH2), 2 Kanal + 2 Power-Ausgänge XH2.54-2p, 5 Achsen/6 Motoren; Größe **kompatibel zu MKS Gen-L / Nano V3** (exakte mm **unbelegt**) → ebd.
- ESP32 kann Deep-Sleep, aber Board ist für Dauernetzbetrieb ausgelegt; realistischer µA-Wert **unbelegt**.
- Preis: **26,09 €** [filamente.de](https://filamente.de/shop/teile-und-zubehor/3d-drucker-controller/3d-drucker-steuerplatine-mks-tinybee-v1-0-3d-drucker-steuerplatine-mit-esp32-wifi2-0-kompatiblem-lcd2004-12864-tft-circboard-prototyping-boards/) · **29,99 €** [amazon.de](https://www.amazon.de/-/en/3D-Printer-Motherboard-Marlin2-0-Firmware/dp/B0B2RFYNPJ)

### 2.2 BIGTREETECH SKR 3 / SKR 3 EZ
- MCU **STM32H743VI** (480 MHz), **kein WLAN onboard**, nur Steckplatz für ESP-12S/ESP32-Modul · Eingang **DC 12/24 V** → [bttwiki SKR 3](https://global.bttwiki.com/SKR%203.html)
- MOSFET-Strome: Bett **10 A** Dauer / 11 A peak, Heizpatrone **5,5 A** / 6 A, Lüfter **1 A** / 1,5 A; Thermistor 2× NTC/PTC umschaltbar, Pull-up per Jumper → ebd.
- Größe **110 × 85 mm** (SKR 3) bzw. **109,7 × 98 mm** (SKR 3 EZ, [botland.de](https://botland.de/motherboards-und-elektronik-fuer-3d-drucker/21679-bigtreetech-skr-3-ez-motherboard-fuer-3d-drucker.html))
- Preis: SKR 3 EZ **90,36 USD** [biqu.equipment](https://biqu.equipment/de/products/btt-skr-3-ez-control-board); DE-Ladenpreis bei Botland **unbelegt** (Preis per JS gerendert).

### 2.3 BIGTREETECH Manta M4P/M5P/M8P
- MCU **STM32G0B0RE** (bzw. G0B1VET6), **braucht CB1 / Raspberry-Pi-CM4** als Linux/Klipper-Host → [anodas.lt](https://anodas.lt/en/bigtreetech-manta-m4p-v2-1-single-board), [neo.bttwiki](https://neo.bttwiki.com/en/docs/board-docs/manta-series/manta-m4p)
- Eingang **DC 12/24 V**; Größe **160 × 95 mm** (M4P), M8P 170 × 102,7 mm → [biqu.equipment](https://biqu.equipment/en-gb/collections/control-board/products/manta-m4p-m8p)
- Kein Akku, kein Deep-Sleep; CB1 = voller Linux-SBC → hoher Ruhestrom. Preis **unbelegt**.

### 2.4 Mellow FLY Super8 Pro / FLY E3
- Super8 Pro: **STM32H723ZGT6** (550 MHz), 12/24/48 V, **6 ADC** (Thermistoren), 10 PWM-Lüfter, 5 Extruder; WLAN nur über **optionales ESP32-Modul** → [mellow.klipper.cn](https://mellow.klipper.cn/en/docs/ProductDoc/MainBoard/fly-super/fly-super8-pro)
- FLY RRF E3 Pro / CDY V3: STM32F407 mit **ESP32 onboard** (WLAN) → [mellow-3d.github.io](https://mellow-3d.github.io/supported_boards.html) · Kein Akku/Deep-Sleep; Preis **unbelegt**.

### 2.5 Fysetc
- Gleiche Klasse (STM32, 12–24 V); **nicht recherchiert/unbelegt**.

### 2.6 Creality Sonic Pad — **kein Mainboard**
- 7"-Klipper-**Host-Pad** (SoC, 2 GB RAM/8 GB ROM, USB ×4, RJ45, WLAN), steuert einen **separaten** Drucker-Mainboard über USB → [all3dp.com](https://all3dp.com/4/creality-sonic-pad-review)
- Hat selbst keine Motor-/Heiz-MOSFETs, keine Stepper-Sockel → als Platine für den Topf **nicht** geeignet.

## 3. Baugröße im Vergleich (Ziel: ≤ 54 × 80 mm)

| Board | Größe | Quelle |
|-------|-------|--------|
| BIGTREETECH M8P | 170 × 102,7 mm | biqu.equipment |
| BIGTREETECH M4P | 160 × 95 mm | biqu.equipment |
| SKR 3 | 110 × 85 mm | bttwiki |
| SKR 3 EZ | 109,7 × 98 mm | botland.de |
| MKS TinyBee | Footprint ≈ MKS Gen-L (**maße unbelegt**) | github.com/makerbase-mks |

→ **Kein** Board erreicht 54 × 80 mm; selbst das kleinste liegt fast doppelt so tief.

## 4. Fazit-Verdikt (ein Satz)

**Nein** — ein 3D-Drucker-Mainboard taugt nicht als Fertigplatine für diesen Topf, weil ihm der entscheidende Baustein fehlt: **Akkuladung inkl. BMS/Balancing und Unterspannungsabschaltung für einen 2S-Pack**, dazu 12–24-V-Dauernetzbetrieb ohne µA-Deep-Sleep — und die Boards sind zudem zu groß.

## 5. Vergleichstabelle

| Kandidat | Preis | MCU | Spannungseingang | MOSFET-Ausgänge | ADC-Eingänge | Akku/Deep-Sleep | Größe | Fazit | Link |
|---|---|---|---|---|---|---|---|---|---|
| MKS TinyBee | 26,09 € / 29,99 € | ESP32-WROOM-32U | 12–24 V | 2 Heizer + Bett + 2 Fan (Low-Side) | 3× NTC (Pull-up, 0–3,3 V) | nein / µA unbelegt | ≈ MKS Gen-L (mm unbelegt) | bester ESP32-Kandidat, Rest fehlt | [github](https://github.com/makerbase-mks/mks-tinybee) |
| BTT SKR 3 | 90,36 USD (EZ) | STM32H743VI | 12/24 V | HB 10 A, Heizer 5,5 A, Fan 1 A | 2× NTC/PTC + Pull-up | nein / nein | 110 × 85 mm | nein | [bttwiki](https://global.bttwiki.com/SKR%203.html) |
| BTT SKR 3 EZ | 90,36 USD | STM32H743VI | 12–24 V | HB 10 A, Heizer 5,5 A, Fan 1 A | 2× NTC/PTC | nein / nein | 109,7 × 98 mm | nein | [botland](https://botland.de/motherboards-und-elektronik-fuer-3d-drucker/21679-bigtreetech-skr-3-ez-motherboard-fuer-3d-drucker.html) |
| BTT Manta M4P | unbelegt | STM32G0B0RE | 24 V (+CB1) | Fan 1 A, Heizer 5 A, Bett 10 A | Thermistor-ADC | nein / nein | 160 × 95 mm | nein (SBC-Host) | [biqu](https://biqu.equipment/en-gb/collections/control-board/products/manta-m4p-m8p) |
| Mellow FLY Super8 Pro | unbelegt | STM32H723ZGT6 | 12/24/48 V | 5 Heizer, 10 PWM-Fan | 6× ADC | nein / nein | groß (unbelegt) | nein | [mellow](https://mellow.klipper.cn/en/docs/ProductDoc/MainBoard/fly-super/fly-super8-pro) |
| Mellow FLY RRF E3 Pro | unbelegt | STM32F407 | 12/24 V | 2 Heizer, 4 Fan | Thermistor-ADC | nein / nein | klein (unbelegt) | ESP32-WLAN, sonst nein | [mellow](https://mellow-3d.github.io/supported_boards.html) |
| Fysetc (Klasse) | unbelegt | STM32 | 12–24 V | ja | ja | nein / nein | ~100 mm+ | nicht recherchiert | — |
| Creality Sonic Pad | ~ (unbelegt) | 64-bit SoC (Klipper-Host) | USB-Strom | keine | keine | – / – | 7"-Pad | kein Mainboard | [all3dp](https://all3dp.com/4/creality-sonic-pad-review) |

## 6. Empfehlung / nächstbeste Optionen

- **Kein** Board als Fertigplatine übernehmen. Ein ESP32-Klasse-MCU gibt es dort zwar (TinyBee, Mellow E3 Pro), aber Zu- und Abschaltung/ Akkuladung müssten **extern** gelöst werden.
- Übertragbare Teile als **Bauteil-Spender** nutzen: Low-Side-MOSFET-Ausgänge, XH2.5-Buchsen, Stepper-/Heiz-Anschlussblöcke.
- Falls überhaupt: **MKS TinyBee** als ESP32-Basis + separates **2S-BMS + UVLO-Modul + eigenes 5-V/3-A-Buck** — dann ist die Eigenentwicklung trotzdem kleiner und billiger, weil die halbe Board-Fläche ungenutzt bleibt.
- Tatsächlich passende Alternativen (ESP32-C3/C6 mit Deep-Sleep + integriertem Laderegler) → siehe Schwester-Recherche.
