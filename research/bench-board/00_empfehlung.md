# Empfehlung: Entwicklungs-Board für den Labortisch (Größe/MCU egal)

Stand: **09.10.2026** · Frage: „Ich will ein Board, an das ich alles anschließen kann zum Entwickeln —
Größe egal, ESP32 egal, Hauptsache der MCU kann alles." (Endplatine kommt später.)

Basis: `01`…`03` in diesem Ordner. **Alle Preise hier am 09.10.2026 selbst an der Produktseite geprüft**
(BerryBase/Eckstein/Reichelt per Browser, KinCony-/MKS-Seiten per API) — die Reports `01`/`02` enthalten
noch „unbelegt"-Lücken, die hier geschlossen sind.

---

## 1. Verdikt

**Ein einzelnes Board, das die komplette Anforderung ab Werk erfüllt, gibt es nicht** (2S-Laden,
6,16-V-Wächter, µA-Schlaf fehlen überall). Für die **Entwicklung** sind drei Wege sinnvoll — je nachdem,
was ihm wichtiger ist:

| Weg | Board | Preis (geprüft) | Alles anschließbar ohne Löten? | Softstart/PWM? | Akku? |
|---|---|---|---|---|---|
| **A · MCU-treu (Empfehlung)** | **FireBeetle 2 ESP32-C6** (DFR1075) | **9,95 €** Eckstein (BerryBase 6,30 € — z. Zt. nicht lieferbar) · DFRobot $6,90 | nein (Breadboard/Dupont) | ja (LEDC-PWM + MOSFET-Modul) | **ja** (1S-Lader onboard) |
| A2 · MCU-treu, mehr Pins | **ESP32-C6-DevKitC-1** | **11,95 €** Reichelt (ab Lager, 1–2 Tage) | nein | ja | nein |
| **B · Klemmen & Relais ab Werk** | **KinCony KC868-A6** | **$50** shop.kincony.com (+ Versand/EUSt ≈ 55–65 € gelandet) | **ja** — Schraubklemmen | **nein** (Relais = nur EIN/AUS) | nein |
| **C · MOSFET-Ausgänge ab Werk** | **MKS TinyBee** | **29,99 €** Amazon `B0B2RFYNPJ` (lagernd) | ja (XH2.54, Stecker liegen in der Projekt-BOM) | ⚠️ nur **Software**-PWM (s. §3) | nein |
| D · Stecksystem | XIAO ESP32-C6 + Grove-Shield | XIAO **7,49 €** Reichelt · Grove-Shield **5,00 €** BerryBase (**z. Zt. nicht lieferbar**) | ja (Grove-4-pol) | nein (Grove-Relais) | ja (Shield hat Lademanagement) |

**Empfehlung für dieses Projekt: Weg A** — FireBeetle 2 ESP32-C6. Begründung in drei Sätzen:
Er hat **denselben MCU wie die geplante Endplatine** (ESP32-C6) → die Firmware, die hier entsteht, läuft
später ohne Umbau auf der eigenen Platine (gleiches ADC- und Deep-Sleep-Verhalten, gleiche LEDC-PWM).
Er hat **7 ADC-Kanäle** (beide Sensoren + Reserve) und einen **1S-Lader mit Akku-Stecker onboard**, damit
auch der Akkubetrieb und das Taster-Aufwachen echt getestet werden können. Und er kostet **9,95 €** — die
teuren Bestandteile des Projekts (2S, Schutz, Wächter) bleiben ohnehin Eigenbau.

**Weg B** ist die Antwort, wenn „alles anschrauben, nichts fliegen lassen" die Hauptsorge ist: der
KC868-A6 ist von **ESPHome offiziell unterstützt**, hat **4 analoge Eingänge 0–5 V** (beide Sensoren
direkt, mit Op-Amp-Eingangsstufe), **6 Relais 10 A** (beide Pumpen), **6 opto-entkoppelte Digitaleingänge**
(Taster) und Schraubklemmen für alles. Er kann aber **keinen PWM-Softstart** (Relais) und hat nur
**~2 freie GPIOs** — für LED-Ausgänge und Softstart-Experimente zu knapp.

**Weg C** (TinyBee) ist die ursprüngliche Idee des Users und für die Pumpenseite reizvoll (MOSFETs,
12–24 V, viele Stecker), hat aber die in §3 genannte Einschränkung.

---

## 2. Einkaufsliste Weg A (Entwicklungsträger)

| # | Artikel | Preis | Quelle |
|---|---|---|---|
| 1 | **FireBeetle 2 ESP32-C6** (ESP32-C6, 19 IO, 7× ADC, 1S-Lader, 15–16,5 µA Sleep, 25,4 × 60 mm) | **9,95 €** | [Eckstein](https://eckstein-shop.de/DFRobot-FireBeetle-2-ESP32-C6-IoT-Development-Board-EN) · [DFRobot $6,90](https://www.dfrobot.com/product-2771.html) |
| 2 | 2-Kanal-MOSFET-Modul Logikpegel ≥3 A **oder** 2× AO3400A + 4,7 kΩ / 47 kΩ + 1N5819 (Projektwerte aus `hardware/schaltplan_v1.md`) | ~3–5 € (**unbelegt**) | Reichelt / Amazon |
| 3 | Breadboard + Dupont-Kabel + 2,54-mm-Schraubklemmenadapter | ~10 € (**unbelegt**) | BerryBase / Reichelt |
| 4 | 5-V-Netzteil **≥3 A** für die Pumpenschiene (Anlaufstrom!) | offen | — |
| 5 | 2S-/1S-LiPo für Akkutest: EFASO 503759 1500 mAh, JST PH | 14,90 € | efaso.de (Projekt-BOM) |
| 6 | Kapazitiver Bodenfeuchtesensor **v1.2 analog** (ARCELI 6er-Pack) | 7,49 € | Amazon `B0FPRBY7LW` (Projekt-BOM) |
| 7 | Pumpe CONQUERALL DC 5 V + Mini-Luftpumpe `B0FXB5BMTT` | 11,99 € / 8,48 € | Amazon (Projekt-BOM) |

**Wichtig zur Sensorversorgung:** Sensor an **3,3 V** betreiben (nicht 5 V) — der ADC des C6 verträgt
max. 3,3 V, und Clone-Boards ohne LDO liefern an 5 V teils > 3 V (`research/kapazitiver-bodenfeuchtesensor-esp32-recherche.md` §3).

---

## 3. ⚠️ Korrektur zum TinyBee (Weg C)

Report `02` nennt den TinyBee als Board mit „PWM-fähigen MOSFET-Ausgängen". Das ist **nur halb richtig**:
Die Heizungs- und Lüfter-Ausgänge hängen im Schaltplan an einem **I²C-I/O-Expander**
(erkennbar an den Pin-Nummern ≥ 128 im Marlin-Pin-Header `pins_MKS_TINYBEE.h`,
`HEATER_0_PIN 145`, `FAN0_PIN 147`, Kommentar „MAX_EXPANDER_BITS is defined for MKS TinyBee").
Über einen I²C-Expander ist **kein Hardware-PWM (LEDC)** möglich — es bleibt Software-PWM mit niedriger
Frequenz. Für einen echten Softstart-Rampentest heißt das: **freien GPIO + MOSFET-Modul** nehmen.

**Was der TinyBee trotzdem liefert** (aus dem Marlin-Pinmap, 09.10.2026):
- Frei nutzbare ADC-Pins: **IO32, IO33, IO34, IO35, IO36, IO39** (alle ADC1 = WLAN-sicher).
  Die NTC-Eingänge **nicht** für den Feuchtesensor nehmen — sie haben einen Pull-up-Teiler.
- Viele freie GPIOs auf den EXP1/EXP2-Headern (IO0, 4, 5, 12–17, 21–23) für Taster und LEDs.
- ESP32 + WLAN, **12–24 V** Eingang, USB-Firmware-Upload, ISO-Verpolschutz.
- **Kein Akku, kein Lader, kein µA-Schlaf.** Pumpe: `+` an ein **5-V-Netzteil**, `−` an den
  Low-Side-MOSFET-Ausgang, Massen verbinden — dann schaltet der MOSFET korrekt.

---

## 4. Was kein Entwicklungsboard leistet (bleibt Eigenbau)

- **2S-Laden mit Balancing + Schutz auf einem Board** — gibt es nicht (siehe `../fertige-platinen/`).
- **Unterspannungswächter bei 6,16 V** — alle BMS schalten fest bei 2,9 V/Zelle = 5,8 V.
- **µA-Schlaf**: FireBeetle 15–16,5 µA und XIAO 15 µA sind die einzigen brauchbaren Werte; alle
  Klemmen-/Relais-Boards (KinCony, LILYGO, Waveshare, TinyBee) haben **undokumentierte** Ruhestrome
  durch RTC/RS485/Ethernet/Treiber — für die Endanwendung ungeeignet, für den Tisch egal.
- **3-A-Anlaufstrom**: kein kleines Netzteil liefert 3 A Spitze — für den Tisch ein 5-V/5-A-Netzteil
  verwenden; die Pufferung/Softstart-Logik ist genau das, was hier entwickelt werden soll.
