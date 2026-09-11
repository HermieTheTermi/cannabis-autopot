# BOM-Entscheidung V1 — Smart Grow Topf

Stand: 11.09.2026 · Preise von mir am 11.09.2026 direkt auf der Produktseite nachgeprüft (Spalte „Prüfung")
Grundlage: `../research/bom-check/01…04` · Geometrie: `../docs/02_architektur-und-geometrie.md`

---

## 1. Entscheidung (final)

| # | Bauteil | Wahl | Preis | Bezug / Link | Prüfung |
|---|---|---|---|---|---|
| 1 | **MCU** | Seeed **XIAO ESP32-C6** | **6,99 €** | Reichelt, ab Lager — https://www.reichelt.de/de/de/shop/produkt/xiao_esp32c6_wifi_6_bt5_0_zigbee_thread-379732 | ✅ selbst (itemprop 6.99, „ab Lager") |
| 2 | **Pumpe** | **Adafruit 3910** Peristaltik, 5–6 V | **24,50 €** | BerryBase, 8 Stück, 1–3 Tage — https://berrybase.de/en/adafruit-peristaltic-liquid-pump-with-silicone-tube-5v-to-6v-dc | ✅ selbst (JSON-LD 24.5, „Available") |
| 3 | **Sensor** | Kapazitiv **v1.2**, analog | **4,99 €** | AZ-Delivery — https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2 | ✅ selbst (JSON-LD 4.99, V1.2 kapazitiv) |
| 4 | **Akku** | **EFASO 503759** 3,7 V ~1500 mAh, **PCM**, JST PH2.0 | **14,90 €** | efaso.de (Kassel) — https://efaso.de/produkt/503759-3-7v-1500-mah-pcm-jst-ph2-0-2p/ | ✅ selbst (14,90 €, PCM + JST bestätigt) |
| 5 | **MOSFET** | **AO3400A** (SOT-23), 10 St | **1,67 €** | Reichelt, ab Lager — https://www.reichelt.de/de/de/shop/produkt/mosfet_n-ch_30v_5_7a_0_018r_sot-23-166490 | ✅ selbst (0,167 €/St ab 10) |
| 6 | **Freilaufdiode** | 1N5819 (DO-41), 10 St | ~1,00 € | Reichelt | ⚠️ Subagent, nicht selbst geprüft |
| 7 | **Sensor-Stecker** | JST-XH 2,54 3-pol Buchse, 10 St | 3,00 € | Funduinoshop | ⚠️ Subagent |
| | **Zwischensumme** | | **≈ 57,15 €** | | |
| 8 | Widerstände 220 Ω/10 kΩ, Kondensatoren 100 nF/10 µF/100 µF, Taster, Stiftleisten | ~5 € | überwiegend LCSC (PCBA) oder Reichelt | ❌ Preise DE nicht belegt |
| 9 | Schlauch 3,5 × 5 mm | **0 €** | **im Pumpenlieferumfang: 530 mm + 2 Anschlüsse** | ✅ Hersteller |
| 10 | Ansaugfilter/-gewicht | optional | Badshop/Aquaristik, Preis offen | ❌ |
| | **Gesamt (realistisch)** | | **≈ 62–65 €** | |

**Budget-Abhängigkeit:** Position 2 ist mit 24,50 € der größte Einzelposten. Sparvariante: Funduino 0–90 ml/min, **9,11 €** (Amazon B0DT1JCFNV, laut Subagent live geprüft, ~45 ml/min bei 6 V, Lieferung 18.09.) → Gesamt ≈ 47 €. Nachteile: 60 × 40 × 40 mm Block (braucht die volle Wulsttiefe), **Stromaufnahme nicht dokumentiert**, Förderrate bei 6 V nur geschätzt. Der Aufpreis von 15 € kauft dokumentierte 500 mA, schlanke Ø27,8 mm Bauform und den mitgelieferten Schlauch.

---

## 2. Warum die Pumpe die Adafruit ist

Herstellerangaben (adafruit.com/product/3910, heute geprüft):
- **Motorstrom 500 mA**, Förderrate **bis 100 ml/min** bei 5–6 V — der Einzige im Feld mit belastbarer Stromangabe (nötig für Akku-Auslegung und Booster-Dimensionierung).
- **Ø 27,8 mm × 66,8 mm** — schlank, passt in die Wulst; die China-Blöcke sind 40 mm tief.
- Getriebemotor mit hohem Drehmoment, selbstansaugend (0,5 m), **PWM-drehzahlsteuerbar**, Montagebohrungen Ø3,7 mm / 50 mm Abstand → direkt auf eine 3D-Druck-Halterung oder die Platine schraubbar.
- **530 mm Silikonschlauch 3,5 × 5 mm + 2 Anschlüsse inklusive** → Position 9 entfällt.
- Ausschlüsse: Whadda WPM447 nur 39 ml/min; Gravity DFR0523 zieht 1,8 A Dauerstrom (akku-ungünstig); Mini-Pumpen 5,87/6,69 € ohne Förderratenangabe, Lieferung erst Ende September.

**Dosierung:** 100 ml/min × 10 min = 1 L = ganzer Tank. Deshalb ist PWM-Drosselung Pflicht: Ziel ~40–60 ml/min, Gabe in 2–3 Portionen mit 2 min Pause dazwischen (bessere Verteilung, kein Durchlaufen).

---

## 3. Betriebsspannung der Pumpe — offener Punkt mit Testplan

Die Pumpe ist für **5–6 V** spezifiziert, die Zelle liefert 3,0–4,2 V. Zwei Wege:

- **(A) Boost auf stabil 5 V** (MT3608 o. ä.): Dosierung wird spannungsunabhängig und reproduzierbar; braucht ~1 A Eingangsstrom bei leerer Zelle (2,5 W / 0,85 / 3,0 V) → der MT3608 (2 A) reicht.
- **(B) Direkt aus der Zelle** (3,0–4,2 V): einfacher, keine Verluste, aber die Förderrate schwankt mit dem Ladezustand (±25 %) und ob der Motor bei 3,0 V überhaupt sicher anläuft, ist **nicht belegt**.

**Entscheidung:** Erst messen, dann festlegen. Test im Prototyp: Pumpe direkt an die Zelle, 60 s in einen Messbecher pumpen, Spannung dabei messen. Ergebnis entscheidet:
- läuft an und liefert > 40 ml/min bei 3,4 V → Weg (B), im Code Spannungskompensation (ADC auf VBAT, Laufzeit anpassen),
- sonst Weg (A) — der Boost wird dann auf der eigenen PCB integriert (MT3608, SOT23-6, LCSC-Code beim Layout verifizieren), kein extra Modul nötig.

---

## 4. Akku und Laufzeit

- **EFASO 503759**: ~**59 × 37 × 5 mm** (Typcode; Maße am Listing **nicht** bestätigt → vor Bestellung Specblock prüfen), mit **PCM** (Über-/Tiefentladung, Kurzschluss) und **JST PH2.0-2P** → auf der PCB eine PH2.0-Buchse, Zelle steckbar.
- 1500 mAh @ 3,7 V = **5,55 Wh**. Rechnung: Pumpe 2,5 W × 3 min/Tag = 0,125 Wh, mit Boostverlusten ~0,15 Wh/Tag, plus ESP32-Deep-Sleep (µA) und WiFi nur bei Ereignis → **≈ 4 Wochen pro Ladung**. Bei 6 min/Tag noch ~2,5 Wochen.
- **Warum keine 18650:** geschützte 18650 ist Ø18,85 × 69 mm (stärkste, robusteste Zelle, ~10,35 € mit Halter) — passt nur mit deutlich tieferer Wulst. Die 5-mm-Pouchzelle ist die einzige Option, die die flache Wulst erlaubt.
- **Laden:** über den onboard-Lader des XIAO (BAT-Pads) + USB-C-Durchbruch — kein Lade-IC nötig. Zelle lieber **nicht** per JST-Direktstecker an die BAT-Pads, sondern über die PCB-Buchse, damit das Löten am Board entfällt.
- XIAO C6 hat **Lötpads, keinen Stecker** → Anschluss läuft über die eigene PCB.

---

## 5. Wulst-Maße (aus den finalen Bauteilen abgeleitet)

| Innenmaß | Wert | Bestimmt durch |
|---|---|---|
| Breite | **60 mm** | Pumpe Ø27,8 + Wandungen, PCB ~52 mm, Zelle 37 mm |
| Tiefe (radial) | **40 mm** | Pumpe Ø27,8 + 2 × 2,5 mm Wand + Montagefreiheit |
| Höhe | **160 mm** (y = 90–250) | Pumpe 66,8 mm unten, darüber Platine + Zelle |
| Gesamtbreite Topf an der Wulst | **≈ 180 mm** | 140 mm + 40 mm |

Einbau von unten nach oben: **Pumpe** (y 92–159) → **Platine** (y 162–205) → **Zelle hochkant** (y 168–227, hinter/über der Platine). Alle Maße in `docs/02_architektur-und-geometrie.md` als Parameter hinterlegt.

---

## 6. Konsequenzen für die PCB

1. XIAO ESP32-C6 als Modul (Castellated Pads), USB-C-Stirnseite zur Gehäuseöffnung.
2. **JST PH2.0-Buchse** für die Zelle, Ladepfad an die XIAO-BAT-Pads.
3. Pumpe: AO3400A Low-Side, Gate 220 Ω, Pulldown 10 kΩ, 1N5819 antiparallel, **100 µF Pufferelko** auf der 5-V-Schiene; PWM-tauglich (~20 kHz, Anlaufstrom beachten).
4. Sensor: 3-poliger JST-XH, **VCC über GPIO schaltbar** (nur während der Messung), AOUT auf ADC1.
5. Taster Reset/Boot, Status-LED sichtbar durch das LED-Fenster.
6. Boost-Stufe (MT3608) nur, falls der Pumpentest Weg (A) ergibt — Layout dafür vorsehen.

---

## 7. Noch offen / bewusst nicht behauptet

- **Elektrodenlänge des v1.2** (AZ-Delivery) nicht belegt → am realen Board messen, weil die Messebene 75 mm tief liegt.
- **LDO-Bestückung** des AZ-Boards nur im Foto prüfbar (nicht im Text).
- **Versandkosten** aller Shops nicht geprüft (→ Schwelle: AZ-Delivery versandkostenfrei ab 25 €, sonst 4,99 €-Posten mit anderer Bestellung bündeln).
- **Amazon-Preise** (Funduino-Pumpe, Zubehör) von Agenten im Browser gesehen, von mir nicht nachprüfbar (Amazon blockt Skript-Abrufe).
- Maße der EFASO-Zelle, XIAO-Ladestrom, Boost-Modul-Quelle in DE.
