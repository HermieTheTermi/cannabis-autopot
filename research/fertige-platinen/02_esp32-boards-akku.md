# 02 — Fertige ESP32-Entwicklungsboards mit Akkuladung (Akkukandidaten)

**Frage:** Welche Fertig-Boards/Module (ESP32-C3/C6/S3) bringen möglichst viel der Prüfliste
ab Werk mit — MCU + WLAN + Deep-Sleep + Akkuladung + 5-V/3-A-Pumpenversorgung? Reicht EIN
Board, oder braucht es Zusatzkauf?

**Stand:** 09.10.2026 · Preise nur aus Produktseiten geprüft; nicht Verifizierbares als „unbelegt".

---

## Kurzbefund

**Kein Fertigboard** vereint MCU + Akkuladung + 5-V-Pumpenversorgung + MOSFET. Alle
Marken-ESP32-Boards mit Akkulader sind **1S (3,7 V)** und liefern **im Akkubetrieb keine 5 V** —
der 5-V-Pin ist reiner USB-Ausgang (Seeed-Wiki wörtlich: *„5V – This is 5v out from the USB port"* ·
[wiki.seeedstudio.com](https://wiki.seeedstudio.com/xiao_pin_multiplexing_esp32c6/)). **2S-Ladung
(8,4 V) ist on-board praktisch nicht vorhanden** — nur als separates BMS-Modul. Für die Pumpe ist
daher in jedem Fall ein **zusätzlicher 1S→5V-Boost + MOSFET-Schalter** nötig. **Bester Kandidat:
DFRobot FireBeetle 2 ESP32-C6** (meiste GPIO/ADC, echte µA-Deep-Sleep, 1S-Lader, passende Größe,
günstig), ergänzt um Boost- und MOSFET-Modul.

## 1. Prüfliste gegen die Anforderungen

| # | Anforderung | Zielwert | Erfüllbar ab Werk? |
|---|---|---|---|
| 1 | MCU | ESP32-C6/S3, WLAN, Deep-Sleep µA, 12-bit-ADC, ≥10 GPIO | ja (Board) |
| 2 | Akkuladung | Lade-IC + Akku-Stecker; **2S (8,4 V)?** | 1S ja, **2S nein** |
| 3 | 5-V-Schiene | 5 V @ 3 A Spitze + 3,3 V Logik | **nein** → Boost nötig |
| 4 | MOSFET-Ausgang ≥3 A | Low-Side für Pumpe | **nein** → MOSFET-Modul nötig |
| 5 | Analoge Eingänge | 0–3,3 V, Sensor + Fototransistor, schaltbare Versorgung | ja (Board-ADC) |
| 6 | Bedienung | Taster mit EXT1-Wake, 2 LEDs, Dupont-Leisten | ja (BOOT-Taster + LEDs) |
| 7 | Baugröße | ≤ 54 × 80 mm | ja |
| 8 | Bezug DE/EU | Amazon.de/BerryBase/Eckstein/Botland/Reichelt | ja |

## 2. Kandidatentabelle

| Board | Preis | MCU | Akku (1S/2S, Ladestrom) | 5 V aus Akku? | MOSFET-Ausgang | ADC-Pins | Deep-Sleep | Fazit (was fehlt) | Link |
|---|---|---|---|---|---|---|---|---|---|
| **DFRobot FireBeetle 2 ESP32-C6** | **6,30 €** (BerryBase, z. Z. nicht lieferbar) / **9,95 €** (Eckstein) | ESP32-C6, 160 MHz, 19× digital I/O | **1S**, Ladestrom **max. 0,5 A**, BAT-Stecker + Batteriespannungsmessung | **nein** (nur 5 V *Eingang* VCC/Type-C, Betrieb 3,3 V) | **nein** | **7×, 12-bit SAR** | **16–16,5 µA** | Boost + MOSFET fehlen; nur 1S | [DFRobot](https://wiki.dfrobot.com/dfr1075/) · [BerryBase](https://www.berrybase.de/en/dfrobot-firebeetle-2-esp32-c6-iot-dev-board-wi-fi-6-bt-5-zigbee-3.0-solar-operation-160mhz-3.3v) · [Eckstein](https://eckstein-shop.de/DFRobot-FireBeetle-2-ESP32-C6-IoT-Development-Board-EN) |
| **Seeed XIAO ESP32-C6** | *unbelegt* (Botland/BerryBase: Preis auf Produktseite nicht abrufbar) | ESP32-C6, 160 MHz, nur **11× GPIO** | **1S**, Ladestrom **100 mA**, BAT-Anschluss | **nein** (5 V = USB) | **nein** | **7× ADC** | **15 µA** | 11 GPIO zu knapp (MOSFET+2 LED+Wake+2 Analog+Sensor-Power); Boost+MOSFET fehlen | [Seeed-Wiki](https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/) · [Botland](https://botland.de/xiao/24783-seeed-xiao-esp32-c6-wifi-bluetooth-seeedstudio-113991254-5904422385705.html) |
| *LILYGO/M5Stack/Heltec/Adafruit Feather/SparkFun Thing Plus* | – | ESP32 | 1S | **nein** | nein | teils | µA | gleiches Muster: kein 5 V aus Akku | – |
| **Board mit 2S-Ladung on-board** | – | – | 2S | – | – | – | – | **nicht gefunden (Negativbefund, unbelegt)** | – |

## 3. 2S-Akkuladung — gibt es das?

- **Kein Marken-ESP32-Dev-Board mit 2S-Lade-IC gefunden** (Negativbefund, unbelegt als „nicht
  existent", aber innerhalb der geprüften Quellen nicht auffindbar). ESP32-Boards sind durchweg 1S.
- **2S gibt es nur als separates BMS-/Lademodul**, z. B. „Type-C USB 2S BMS 15 W 8,4 V/12,6 V
  1,5 A mit Balancing" ([docs.cirkitdesigner.com](https://docs.cirkitdesigner.com/component/0e62f3af-f612-4872-999f-5491813837a4/type-c-usb-2s-bms-15w-84v-126v-15a-battery-charging-boost-module-with-balanced))
  oder das weit verbreitete 2S-BMS **HW-391** ([renewspark.com](https://renewspark.com/blogs/news/2s-8-4v-bms-hw391-troubleshooting-guide)).
  → Damit würde man 2S laden, bräuchte aber einen **2S→5 V-Buck** für die Pumpe und einen
  **3,3-V-Regler** für Logik; das eigentliche Board-Lade-IC (1S) bliebe ungenutzt.
- **Fazit:** Bei einem 1S-Board bleibt man am einfachsten bei **1S**. 2S lohnt nur, wenn man die
  Ladung bewusst separat aufbaut (kein Board-Vorteil).

## 4. 1S → 5 V Boost-Module mit 3 A Anlauf (Zusatzkauf)

| Modul | Ausgang | Spitze | Preis | Bezug | Quelle |
|---|---|---|---|---|---|
| **Adafruit PowerBoost 1000C** | 5,2 V, Load-Sharing-Lader (1 A) | interner Schalter 2 A (**~2,5 A Peak-Limit**) | **19,95 $** (z. Z. out of stock; DigiKey-Link) | Adafruit/BerryBase/Eckstein (Distributor) | [adafruit.com/product/2465](https://www.adafruit.com/product/2465) |
| **MT3608-Modul** | einstellbar 5–28 V | **max. 2 A** | *unbelegt* (Amazon.de/Reichelt, typ. <2 €) | Amazon.de | [alldatasheet](https://www.alldatasheet.com/datasheet-pdf/pdf/1131968/ETC1/MT3608.html) |

**Wichtig (Anlauf 3 A):** Kein kleines 1S→5V-Modul liefert dauerhaft 3 A — MT3608 (2 A) und
PowerBoost 1000C (~2,5 A Peak) liegen beide darunter. Der 3-A-Wert ist der **kurze Einschalt-Strom-
peak** der Pumpe. Lösung: Boost auf **Dauerstrom der Pumpe (0,4 A)** auslegen und den Anlauf mit
einem **dicken Stütz-Elko (≥1000 µF) am 5-V-Rail** puffern, plus **PWM-Softstart** in der Firmware.
Alternativ ein Boost mit ≥3–4 A Nennstrom (z. B. XL6009-Klasse) — unbelegt, hier nicht verifiziert.

## 5. Bestes Board + Einkaufsliste

**Bester Kandidat: DFRobot FireBeetle 2 ESP32-C6** — ESP32-C6/WLAN, 19 GPIO, 7× 12-bit-ADC,
16,5 µA Deep-Sleep (gemessen, BerryBase-Review), 1S-Lader (0,5 A, Batteriespannungsmessung),
25,4 × 60 mm, 6,30 € (BerryBase) / 9,95 € (Eckstein). Deckt Anforderung 1, 2 (1S), 5, 6, 7, 8 ab.

**Zusätzlich zu kaufen (fehlt bei jedem Board):**
1. **1S-LiPo-Zelle** (z. B. 18650 + Halter oder LiPo-Pouch).
2. **1S→5V-Boost** ≥ 2 A mit Stütz-Elko ≥1000 µF — Adafruit PowerBoost 1000C (19,95 $) **oder**
   MT3608-Modul (unbelegt, <2 €) + Elko. (Softstart per PWM.)
3. **Leistungs-MOSFET-Modul ≥3 A** (Low-Side, z. B. IRLZ44N/AOD4184-Board) — oder als SMD auf
   ein kleines Trägerboard, da keines der Boards einen MOSFET-Ausgang hat.
4. *(nur bei 2S-Strategie)* 2S-BMS (HW-391 o. ä.) + 2S→5V-Buck — siehe Abschnitt 3.

**FAZIT in einem Satz:** **Nein** — es gibt kein fertiges Board, das MCU + Akkuladung +
5-V/3-A-Pumpenversorgung + MOSFET-Ausgang in einem abdeckt; bestes Basis-Board ist der FireBeetle 2
ESP32-C6, alles Übrige (Boost, MOSFET, Zelle) muss **separat** dazugekauft werden.

## 6. Quellen

- DFRobot FireBeetle 2 ESP32-C6 — Wiki/Specs: https://wiki.dfrobot.com/dfr1075/ (25,4×60 mm, 7× 12-bit-ADC, 19 I/O, max. 0,5 A Laden, 16/36 µA Sleep)
- FireBeetle 2 ESP32-C6 — Preis BerryBase: https://www.berrybase.de/en/dfrobot-firebeetle-2-esp32-c6-iot-dev-board-wi-fi-6-bt-5-zigbee-3.0-solar-operation-160mhz-3.3v (6,30 €, nicht lieferbar)
- FireBeetle 2 ESP32-C6 — Preis Eckstein: https://eckstein-shop.de/DFRobot-FireBeetle-2-ESP32-C6-IoT-Development-Board-EN (9,95 €)
- Seeed XIAO ESP32-C6 — Specs: https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/ (11 GPIO, 7 ADC, 15 µA, 21×17,8 mm)
- Seeed XIAO ESP32-C6 — 5 V nur aus USB: https://wiki.seeedstudio.com/xiao_pin_multiplexing_esp32c6/
- Seeed XIAO ESP32-C6 — Preise/Ladestrom 100 mA: https://botland.de/xiao/24783-seeed-xiao-esp32-c6-wifi-bluetooth-seeedstudio-113991254-5904422385705.html
- Adafruit PowerBoost 1000C: https://www.adafruit.com/product/2465 (19,95 $, 5,2 V, 2 A interner Schalter/~2,5 A Peak)
- 2S-BMS-Modul: https://docs.cirkitdesigner.com/component/0e62f3af-f612-4872-999f-5491813837a4/type-c-usb-2s-bms-15w-84v-126v-15a-battery-charging-boost-module-with-balanced
- 2S-BMS HW-391: https://renewspark.com/blogs/news/2s-8-4v-bms-hw391-troubleshooting-guide
- MT3608 (2 A): https://www.alldatasheet.com/datasheet-pdf/pdf/1131968/ETC1/MT3608.html
