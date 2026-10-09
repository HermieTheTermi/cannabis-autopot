# 02 – Entwicklungs-/Bench-Board: MCU-IO-Boards mit Schraubklemmen

Projekt: Smart Grow Topf (Autopot). Bench: alles anschließbar, Baugröße egal, MCU/WLAN frei
programmierbar (ESPHome/Arduino/Tasmota).
**Analog-Bedarf:** kapazitiver Bodenfeuchtesensor (Out ~0–3,0 V, Vs 3,3–5 V) + Fototransistor.
**Aktor-Bedarf:** Pumpe 5 V/0,4 A Nenn, **3 A Anlauf** (PWM-Softstart geplant) + Luftpumpe 0,2 A.

## 0. Nachprüfung Hermes 09.10.2026 (Korrektur + Preisbelege)

- **⚠️ Korrektur: „PWM-Fähigkeit" des TinyBee ist nur Software-PWM.** Die Heiz- und Lüfter-Ausgänge liegen
  hinter einem **I²C-I/O-Expander** (Marlin `pins_MKS_TINYBEE.h`: `HEATER_0_PIN 145`, `FAN0_PIN 147`,
  Kommentar „MAX_EXPANDER_BITS is defined for MKS TinyBee") — über einen Expander ist **kein Hardware-PWM
  (LEDC)** möglich, nur Software-PWM mit niedriger Frequenz. Für einen echten Softstart-Rampentest:
  freier GPIO + MOSFET-Modul. Frei verfügbare **ADC1**-Pins laut Pinmap: **IO32, IO33, IO34, IO35, IO36, IO39**
  (WLAN-sicher); die NTC-Eingänge wegen Pull-up-Teiler **nicht** für den Feuchtesensor nehmen.
  Weitere freie GPIOs für Taster/LEDs: IO0, 4, 5, 12–17, 21–23 (EXP1/EXP2).
- **Preise geprüft:** MKS TinyBee **29,99 €** (Amazon `B0B2RFYNPJ`, lagernd — bestätigt über nozzlenerds.de,
  Stand 09.10.2026); KinCony **KC868-A6 = $50** (shop.kincony.com, „Regular price"), KC868-A4 = $35, A8 = $55,
  A8v3 = $80 — jeweils **netto + Versand/EUSt**; KinCony ist **offiziell ESPHome-unterstützt**
  (<https://devices.esphome.io/devices/kincony-kc868-a6/>). Bestätigt: A6 = 4× Analog-In 0–5 V (LM224-Op-Amp-
  Eingangsstufe), 6× Relais 10 A (NO/COM/NC), 6× opto-entkoppelte Digitaleingänge, 2× DAC 0–10 V
  (<https://www.kincony.com/kc868-a6-hardware-design-details.html>).
- **Für den Tisch relevanter Nachteil, hier ergänzt:** KinCony A6 hat nur **~2 freie GPIOs** → für zwei
  Status-LEDs **und** einen externen MOSFET (Softstart-Experiment) zu knapp.

---

## (a) Board-Vergleich

| Board | Preis (Produktseite) | MCU | WLAN | Analog-In (Bereich) | Aktorkanäle (Typ/Strom) | freie IO | Versorgung | Deep-Sleep |
|---|---|---|---|---|---|---|---|---|
| **KinCony KC868-A4** | $35 Shop · ~72,38 € eBay.de | ESP32 | Ja | 2×0–5 V **+ 2×4–20 mA**; +2×0–10 V DAC | 4× Relais AC277V/10 A (COM,NO,NC) | 1 GPIO | USB / 12 V | mögl., Ruhestrom unbelegt |
| **KinCony KC868-A6** | unbelegt | ESP32 | Ja | **4×0–5 V** + 2×4–20 mA; +2×0–10 V DAC | 6× Relais AC277V/10 A | 2 GPIO | USB / 12 V | mögl., unbelegt |
| **KinCony KC868-A8** | $55 Shop | ESP32 | Ja | 2×0–5 V | 8× Relais AC277V/10 A | 4 GPIO | USB / 12 V | mögl., unbelegt |
| **KinCony KC868-A8v3** (S3) | $80 Shop | ESP32-S3-WROOM-1U | Ja | **kein Analog-Eingang dokumentiert** | 8× Relais 250 V/10 A | 4× 1-Wire + 6 GPIO | 12/24 V, USB-C | mögl., unbelegt |
| **LILYGO T-Relay-8** | 23,25 € tinytronics · $22,38 Hersteller | ESP32-WROVER-E | Ja | ESP32-ADC auf GPIO (**0–3,3 V**, kein 5-V-Teiler) | 8× Relais HRS4H-S-DC5V, 10 A/250 VAC bzw 10 A/28 VDC, Optokoppler | 16-Pin-Header (GPIO/3,3 V/GND) | 12–24 V (2-Pin-Klemme) | mögl., unbelegt |
| **Waveshare ESP32-S3-Relay-6CH** | 27,85 € openelab.io | ESP32-S3 | Ja (BT/RS485) | **kein Analog-Eingang dokumentiert** | 6× Relais ≤10 A/250 VAC bzw ≤10 A/30 VDC, Optokoppler+Power-Isolation | WS2812(IO38), Buzzer(IO21), RS485, Pico-HAT | 7–36 V oder 5 V Type-C | mögl., unbelegt |
| **MKS TinyBee** | 29,99 € nozzlenerds · 33,56 € Amazon.de | ESP32-WROOM-32U | Ja | 3× NTC100K-ADC (IO34/36/39, ~0–3,3 V Thermistorteiler) | 2× Heater + 1× Bed **MOSFET**, 2× PWM-Fan-**MOSFET** (Low-Side, schaltet GND) | viele (Endstopps/LCD/EXP) | 12–24 V (**XH2.54**, keine Klemmen) | mögl., unbelegt |

Bezugslinks: [KinCony A4](https://shop.kincony.com/products/kc868-a4-arduino-esp32-4-channel-relay-module) · [eBay.de A4](https://www.ebay.de/itm/235599000205) · [KinCony A8](https://shop.kincony.com/products/kc868-a8-esp32-8-channel-relay-module) · [KinCony A8v3](https://shop.kincony.com/products/kc868-a8v3-esp32-s3-8-channel-relay-module) · [T-Relay-8](https://www.cnx-software.com/2022/06/11/t-relay-8-an-esp32-board-with-8-relays/) · [Waveshare 6CH](https://docs.waveshare.com/ESP32-S3-Relay-6CH), [Preis](https://openelab.io/products/waveshare-relay-6ch) · [TinyBee](https://github.com/makerbase-mks/MKS-TinyBee), [Preis](https://www.nozzlenerds.de/produkt/mks-tinybee-steuerplatine-3d-drucker-32-bit-silent-platine)
Zusatz: generische ESP32-4/8-Kanal-Relais (AliExpress/Amazon), ESP32-WROOM + 10 A/250 VAC-Relais, ADC nur 0–3,3 V ([Quelle](https://industrialmonitordirect.com/ko/blogs/knowledgebase/wifi-mqtt-relay-boards-esp32esp8266-4-8-channel-options-for-node-red)). LILYGO **T-Relay-S3** (ESP32-S3, 6 Relais via SN74HC595) ab $6,30 ([Shop](https://lilygo.cc/en-us/collections/t-relay-series), [Wiki](https://wiki.lilygo.cc/products/t-relay-series/t-relay-s3)).

## Prüfliste je Board (Kurz)

- **KinCony A4/A6/A8:** ① ✅ ESPHome/Arduino/Tasmota offiziell ([Params-PDF](https://www.kincony.com/download/KC868-Smart-Controller-parameters-v3.2.pdf)). ② ✅ 0–5 V (Teiler vor 3,3-V-ADC) bzw. 4–20 mA; **A6 = 4× 0–5 V** (bestes Board für 0–3-V-Bodenfeuchte). ③ Relais nur EIN/AUS → **kein PWM-Softstart**. ④ A4=1/A6=2/A8=4 GPIO → reicht für Taster+LEDs. ⑤⑥ Deep-Sleep möglich (nicht dok.); USB/12 V. ⑦ Shop.kincony.com/eBay.de.
- **KinCony A8v3/A6v3 (S3):** 8 Digital-In + Relais, RTC, SD, 1-Wire — **kein Analog-In** → ② nicht erfüllt.
- **LILYGO T-Relay-8:** ① ✅ Arduino/PlatformIO. ② ADC chip-nativ **0–3,3 V** (kein 5-V-Teiler); 12 Bit; ADC2 kollidiert mit WiFi. ③ 8 Relais EIN/AUS, kein MOSFET. ④ 16-Pin-Header (GPIO35–37 durch Octal-SPI belegt). ⑥ 12–24 V.
- **Waveshare 6CH:** ① ✅ (RS485/Pico/USB). ② kein Analog-Pad. ③ 6 Relais ≤10 A, **kein MOSFET**. ④ nur WS2812+Buzzer-Pins dok. ⑥ 7–36 V/Type-C.
- **MKS TinyBee:** ① ✅ (Marlin; ESP32 frei mit Arduino/ESPHome). ② 3 NTC-Eingänge (Thermistorteiler, kein Allzweck-0–3,3-V) → teilweise. ③ **MOSFET Low-Side, PWM-fähig** → einzige Klasse mit echtem Softstart-Potenzial; **Stromrating nicht dokumentiert** → für 3 A unbelegt. ④ viele freie IO. ⑥ 12–24 V, XH2.54 statt Klemmen.

## (b) Top-2-Empfehlung

1. **KinCony KC868-A6** (bzw. A4 bei 1–2 Sensoren) — beste Prüflisten-Abdeckung: 4/6× Relais 10 A + **4× 0–5 V Analog-In** (ideal für 0–3-V-Bodenfeuchte + Fototransistor) + 2× 4–20 mA + 2× 0–10 V DAC + 2 freie GPIO + Schraubklemmen + 12 V + ESPHome/Arduino/Tasmota. **Zusätzlich nötig:** 5-V-Netzteil für die Pumpenschiene, ein **Low-Side-MOSFET-Modul (z. B. IRLZ44N)** an einem freien GPIO für den PWM-Softstart, DIN-Gehäuse. Grund: nur die KinCony-A-Serie liefert echte 0–5-V-Analog-**Klemmen** UND Relais UND freie GPIO auf einem Board.
2. **MKS TinyBee** — wenn der **PWM-Softstart** gegen 3 A Anlauf im Vordergrund steht: einzige gelistete Klasse mit **MOSFET-Ausgängen** (PWM-fähig, Low-Side). **Zusätzlich nötig:** 12–24 V-Netzteil, 5-V-Pumpenschiene (separates Netzteil), XH2.54→Klemmen-Adapter; MOSFET-Rating vor 3 A verifizieren (unbelegt).

## (c) Grenzen der Klasse + PWM-Softstart

- **Relais = nur EIN/AUS.** Ein Relais lässt sich nicht weich anfahren und nicht PWM-takten (Kontakt klappert, Verschleiß, kein definierter Zwischenzustand). Für den 3-A-Anlaufstrom sind **alle reinen Relais-Boards (KinCony A4/A6/A8/A8v3, LILYGO T-Relay, Waveshare 6CH) für einen Softstart ungeeignet** — sie schalten die Pumpe hart ein.
- **MOSFET/PWM kann Softstart.** Nur **MKS TinyBee** hat werksseitig MOSFET-Ausgänge (Low-Side, schaltet GND, PWM-fähig). Damit ist eine LEDC-PWM-Rampe möglich — **sofern** der MOSFET ≥3 A verträgt (Rating nicht dok. → prüfen); ein Heater/Fan-MOSFET mit Freilaufdiode ist dafür grundsätzlich geeignet.
- **Relais + MOS kombinieren: ja.** Bench-Muster: **PWM-Softstart über Low-Side-MOSFET** (Rampe 0→100 %), optional **Relais als Bypass** parallel zum MOSFET, um nach dem Anlauf Verluste zu senken. Auf KinCony/Waveshare/LILYGO den MOSFET extern an einen freien GPIO hängen (ESP32 hat LEDC-PWM); auf dem TinyBee direkt an einen Heater-/Fan-Ausgang.
- **Kein µA-Sleep.** Keines ist ein µA-Standby-Gerät: Ethernet-PHY/RTC/RS485 (KinCony), isolierte Versorgung (Waveshare), Stepper-Treiber (TinyBee) ziehen Ruhestrom. Deep-Sleep chip-seitig möglich, **board-spezifischer Sleep-Strom nirgends dokumentiert → unbelegt**. Für echten µA-Betrieb später ein nacktes ESP32-Modul.
- **ADC-Grenzen.** Nur KinCony liefert 0–5-V-Eingänge (Spannungsteiler vor 3,3-V-ADC); nackte ESP32-ADC-Pins sind auf **0–3,3 V** begrenzt (kein 5-V-Teiler), ADC2 bei aktivem WiFi unbrauchbar. Auflösung 12 Bit (ESP32/S3, 4096 Stufen); der 0–3,0-V-Sensor passt nur knapp in den 0–3,3-V-Bereich.
