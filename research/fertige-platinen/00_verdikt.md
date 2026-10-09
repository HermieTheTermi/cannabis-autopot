# Verdikt — „Fertige Platine statt Eigenentwicklung?" (3D-Drucker-Mainboard o. ä.)

Stand: **09.10.2026** · Frage des Users: „man könnte ja auch eine fertige Platine verwenden, z. B. ein
3D-Drucker-Mainboard oder sowas — gibt es da schon was Fertiges?"

Grundlage: vier Teilrecherchen in diesem Ordner (`01`…`04`), tragende Aussagen davon am 09.10.2026
**selbst an der Produktseite nachgeprüft** (Korrekturen unten in den Teilreports vermerkt).

---

## 1. Antwort in einem Satz

**Es gibt kein käufliches Board, das die Anforderungsliste dieses Projekts in einem erfüllt** — jede
der drei geprüften Klassen scheitert an einer *anderen* Achse: 3D-Drucker-/Maschinensteuerungen an
**Akkuladung + µA-Deep-Sleep + Baugröße**, fertige ESP32-Entwicklungsboards am **2S-Laden und an 5 V
aus dem Akku**, die Power-Manager-/UPS-Klasse am **2S-Balancing**. Die Eigenplatine wird dadurch
**nicht obsolet**.

## 2. Prüfliste gegen den Markt (Kurzfassung)

| Achse (Soll) | 3D-Drucker-Mainboards | ESP32-Dev-Boards | Power-Manager/UPS | Bestes Fundstück |
|---|---|---|---|---|
| MCU + WLAN + Deep-Sleep | nur MKS TinyBee/Mellow (Deep-Sleep-Pfad unbelegt) | ✅ | – | FireBeetle 2 ESP32-C6 (16,5 µA) |
| **2S-Laden 5 V→8,4 V** | ❌ 12–24 V Netz | ❌ nur 1S | ❌ nur 1S | **Fertigmodul Type-C 2S-Boost-Lader** (5 V→8,4 V, 39 × 18 × 6,3 mm, ~8–10 $/3 St., EU-Preis unbelegt) |
| **Zellschutz + Balancing** | ❌ | ❌ | ❌ | **HX-2S-JH20** (IC = **HY2120-CB** + Balancer **HY2213-BB3A**) |
| 5 V/3 A Spitze | teilw. (Buck 5 V/5 A) | ❌ (5 V-Pin = USB) | nur 1S (Waveshare SPM D: 5 V/3 A) | **MINI560** Buck 5 V/5 A |
| 3,3 V/2 A | ✅ onboard | ✅ | ❌ | Board-Regler / MINI560-3,3 V |
| Wächter **6,16 V** | ❌ | ❌ | ❌ (feste BMS-Schwelle 5,8 V) | **kein Fertigmodul** |
| 2× Low-Side-MOSFET | ✅ (Heizung/Lüfter) | ❌ | ❌ | MOSFET-Modul ≥3 A |
| 2× Analog 0–3,3 V | teilw. (Thermistor-Pull-up) | ✅ | – | – |
| Größe ≤ 54 × 90 mm | ❌ (≥ 109 × 85 mm) | ✅ | ❌ | – |

## 3. Die drei Kandidaten-Klassen im Klartext

**a) 3D-Drucker-Mainboards — nein.** Kein Board lädt einen 2S-Akku, keines hat einen µA-Deep-Sleep-Pfad
(alles für Dauernetzbetrieb 12–24 V ausgelegt), keines eine Unterspannungsabschaltung — und alle sind
**mindestens doppelt so lang** wie die Wulst-Kammer (kleinstes ~109 × 85 mm gegen 108 mm Kammerlänge).
Bester Kandidat wäre der **MKS TinyBee** (ESP32-WROOM-32U, WLAN, 12–24 V, Low-Side-MOSFETs, 3 NTC-Eingänge,
26,09 € bei filamente.de / 29,99 € Amazon) — trotzdem fehlen Laden, BMS, UVLO und Deep-Sleep.
Details + Quellen: [`01_3d-drucker-mainboards.md`](01_3d-drucker-mainboards.md).

> **Nebenbefund:** Der TinyBee ist als *Werkstattboard* interessant (ESP32 + 24-V-Eingänge + Leistungs-MOSFETs
> + XH2.54-Buchsen — brauchbar für SPS-/IO-Experimente), aber nicht als Platine in diesem Topf.

**b) Fertige ESP32-Entwicklungsboards — nein, aber als Basis brauchbar.** Alle Marken-Boards mit Lader
(FireBeetle 2 ESP32-C6, XIAO ESP32-C6, LILYGO, M5Stack, Heltec, Feather, Thing Plus) sind **1S** und
liefern **im Akkubetrieb keine 5 V** (Seeed-Wiki wörtlich: „5V – This is 5v out from the USB port").
Bester Kandidat: **DFRobot FireBeetle 2 ESP32-C6** — 19 GPIO, 7× 12-bit-ADC, 16,5 µA Deep-Sleep,
1S-Lader 0,5 A, 25,4 × 60 mm, **6,30 € (BerryBase, gerade nicht lieferbar) / 9,95 € (Eckstein)**.
Es bleiben zwingend Zusatzkäufe: 1S→5V-Boost + MOSFET-Modul. Details:
[`02_esp32-boards-akku.md`](02_esp32-boards-akku.md).

**c) Power-Manager/UPS/Solar-Manager — nein.** Diese Klasse ist **durchweg 1S** (deshalb braucht sie kein
Balancing). Das einzige Board der ganzen Recherche mit **5 V/3 A** ist der **Waveshare Solar Power Manager (D)**
— aber 1S, also nicht die 2S-Topologie des Projekts. Details: [`03_power-management-2s.md`](03_power-management-2s.md).

**d) Fertige Bewässerungs-/Grow-Controller — nein (Anwendungsebene).** Bester Kandidat **DROPLET**
($87, ESP32 + ESPHome, 5 analoge kapazitive Sensorports, 5 Mikropumpen-Ausgänge, Buzzer) — ⚠️
**seit 04.05.2026 ausverkauft** und ohne Akku/Laden, ohne Lichtsensor, Peristaltik nicht zugesichert.
**Smart Garden** ($34,99, ESP32-S2, 4 Relais, ESPHome/OTA, quelloffen) und **OpenSprinkler Pro**
(269–309 €, Magnetventile + Zeitplan) lösen andere Probleme. Details:
[`04_bewaesserungs-controller.md`](04_bewaesserungs-controller.md).

## 4. Der eigentlich wertvolle Fund: der Strompfad ist modulweise nachbaubar

Die projekteigene 2S-Versorgung besteht aus **denselben Bausteinen, die es fertig zu kaufen gibt** —
nur als Module statt als SMD:

| Aufgabe | Fertigmodul | Preis | Größe | Quelle |
|---|---|---|---|---|
| Zellschutz + Balancing | **HX-2S-JH20** (2S, 10 A / 20 A Puls, ÜC 4,28 V ±0,05 V, TV 2,9 V ±0,08 V je Zelle, **IC HY2120-CB** + Balancer HY2213-BB3A, 2,5–9 µA) | **2,22 € netto** (1+), 1,69 € ab 5 | 47,5 × 24 × 3,6 mm | [hestore.eu](https://www.hestore.eu/de/prod_10046818.html) (EU/HU, 09.10.2026 geprüft) |
| 2S-Laden 5 V → 8,4 V | Type-C-BMS-2S-Boost-Lader (CC/CV, 8,4 V, 1,1–2,2 A) | ~8–10 $ / 3 St., EU-Preis **unbelegt** | 39 × 18 × 6,3 mm | [Adeept](http://www.adeept.com/type-c-bms-2s-2a-18650-21700-37v-lithium-battery-charge-board-step-up-boost-li-po-polymer-usb-c-to-84v_p0374.html) · [Amazon.com 3er](https://www.amazon.com/Lithium-Battery-Charger-Step-up-Polymer/dp/B0BZC7TWC7) |
| 5-V-Schiene (5 V/5 A) | **MINI560** Buck | ~2 €-Klasse, DE-Preis **unbelegt** | ~22 × 17 mm | [Amazon.de](https://www.amazon.de/-/en/Binghe-DC-DC-Regulator-Power-Module/dp/B0DJX9TNMT) |

⚠️ **Zwei Fallen bei den Fertigladern** (09.10.2026 geprüft):
- **LaskaKit PD-IP2326 (7,30 €, 164 St. lagernd)** ist verlockend (2S/3S, IP2326 = genau der Projekt-IC),
  aber der Hersteller antwortet im Produkt-Q&A: *„dieses Modul benötigt eine PD-Quelle mit 20 V"* — für
  einen **5-V-USB-C-Eingang** ist es damit **nicht** verwendbar. Überstrom-/Kurzschlussschutz hat es laut
  Shop ausdrücklich **nicht**. ([laskakit.cz](https://www.laskakit.cz/en/la123029))
- Die billigen **Type-C-2S-Boost-Lader** funktionieren nur an **dummen 5-V-Quellen**; an echten
  USB-C-PD-Netzteilen verweigern sie (Käuferberichte), und BMS-Module ersetzen generell **keinen Lader**
  (hestore: *„BMS modules do not replace the charging circuits!"*) — beides muss man kombinieren.

**Nicht durch Fertigmodule zu decken — das bleibt Eigenanteil:** der **Unterspannungswächter bei 6,16 V**
(alle BMS schalten bei 2,9 V/Zelle = 5,8 V fest; kein einstellbares Modul gefunden), der **µA-Aus-Schalter**
und die **3-A-Anlaufstrom-Pufferung** der Pumpe. Genau das ist die Eigenleistung, die die Platine heute trägt.

## 5. Was das für die Entscheidung heißt

1. **Kein Marktprodukt ersetzt die Platine** — die drei gesuchten Funktionen (2S-Laden + Balancing auf
   einem Board, µA-Schlaf, einstellbarer Wächter) gibt es nirgends zusammen.
2. **Preis spricht für den Eigenbau:** Modulweg ≈ 12–20 € (ohne Gehäuse-Aufwand, ohne Reserve) gegen
   ≈ 10 € Bauteile auf der Platine — und die Module sind **10–15 mm hoch plus Verdrahtung**, die Wulst
   hat innen 40 × 40 mm (geplant 54 mm) und wird von der Pumpe (44 mm) belegt.
3. **Fallback für den Notfall bleibt dokumentiert:** falls das Layout/Routing der 2S-Versorgung klemmt,
   ist die HX-2S-JH20 + Type-C-Lader + MINI560-Kombination der Rückfallweg — ohne Neukonstruktion der
   Mechanik, weil die Module flach unter der Platine im Wulst-Deckel Platz finden müssten (prüfen).
4. **Für den MCU-Teil wäre der beste Tausch FireBeetle 2 ESP32-C6** — aber der bringt nur 1S und kein
   5 V aus dem Akku, kostet 6,30–9,95 € und würde die ESP32-C6-MINI-1-Position (~3,60 €) plus die
   halbe Entkopplung sparen. **Nicht empfohlen**, weil er die 2S-Kette nicht bedient.

## 6. Offene Punkte / nicht Belegtes

- [ ] EU-Shop + Preis für einen **2S-USB-C-Lader ohne PD-Zwang** (die 5-V-Klasse) — bisher nur US-Preise.
- [ ] Preis/Verfügbarkeit **MINI560** in DE prüfen, falls der Modulweg ernsthaft verfolgt wird.
- [ ] Prüfen, ob der FireBeetle 2 ESP32-C6 (1S, 5 V nur aus USB) als **Prüf-/Entwicklungsboard** für die
      Firmware sinnvoll ist, während die Platine entsteht (Firmware ist der letzte offene Projektpunkt).
- [ ] Marktbeobachtung: ESP32-Board mit **2S-Lader** on-board — im Rahmen der vier Recherchen **nicht
      gefunden** (Negativbefund innerhalb der geprüften Quellen, keine Garantie der Nicht-Existenz).
