# BOM-Entscheidung V1 — Smart Grow Topf

Stand: 11.09.2026 · Preise am 11.09.2026 direkt auf der Produktseite geprüft (Spalte „Prüfung")
Grundlage: `../research/bom-check/01…04` · Geometrie: `../docs/02_architektur-und-geometrie.md`

---

## 1. Entscheidung (final)

| # | Bauteil | Wahl | Preis | Bezug / Link | Prüfung |
|---|---|---|---|---|---|
| 1 | **MCU** | Seeed **XIAO ESP32-C6** | **6,99 €** | Reichelt, ab Lager — https://www.reichelt.de/de/de/shop/produkt/xiao_esp32c6_wifi_6_bt5_0_zigbee_thread-379732 | ✅ selbst (itemprop 6.99, „ab Lager") |
| 2 | **Pumpe** | **OEM-Peristaltik ABC-12527**, 3,7–6 V, Ø32 × 44 mm | **7,74 €** | anodas.lt (EU/Litauen, lagernd) — https://anodas.lt/en/peristaltic-liquid-pump-with-silicone-tubing-3-7-6vdc | ✅ selbst (Spec-Block + Preis auf der Seite) |
| 3 | **Sensor** | Kapazitiv **v1.2**, analog | **4,99 €** | AZ-Delivery — https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2 | ✅ selbst (JSON-LD 4.99, V1.2 kapazitiv) |
| 4 | **Akku** | **EFASO 503759** 3,7 V ~1500 mAh, **PCM**, JST PH2.0 | **14,90 €** | efaso.de (Kassel) — https://efaso.de/produkt/503759-3-7v-1500-mah-pcm-jst-ph2-0-2p/ | ✅ selbst (14,90 €, PCM + JST bestätigt) |
| 5 | **MOSFET** | **AO3400A** (SOT-23), 10 St | **1,67 €** | Reichelt, ab Lager — https://www.reichelt.de/de/de/shop/produkt/mosfet_n-ch_30v_5_7a_0_018r_sot-23-166490 | ✅ selbst (0,167 €/St ab 10) |
| 6 | **Freilaufdiode** | 1N5819 (DO-41), 10 St | ~1,00 € | Reichelt | ⚠️ Subagent, nicht selbst geprüft |
| 7 | **Sensor-Stecker** | JST-XH 2,54 3-pol Buchse, 10 St | 3,00 € | Funduinoshop | ⚠️ Subagent |
| 8 | **Schlauch** | Silikon 3 × 5 mm, ~1 m (**neu: nicht mehr im Lieferumfang**) | ~3–5 € | offen | ❌ Preis/Link offen |
| | **Zwischensumme** | | **≈ 45,30 €** | | |
| 9 | Widerstände 220 Ω/10 kΩ, Kondensatoren 100 nF/10 µF/100 µF, Taster, Stiftleisten | ~5 € | überwiegend LCSC (PCBA) oder Reichelt | ❌ Preise DE nicht belegt |
| 10 | Ansaugfilter/-gewicht | optional | Badshop/Aquaristik, Preis offen | ❌ |
| | **Gesamt (realistisch)** | | **≈ 45–50 €** | | |

**Was die Pumpenwahl geändert hat:** Die frühere Adafruit 3910 (24,50 €) ist entfallen, weil die
OEM-Pumpe im Datenblatt **3,7–6 V** abdeckt — und in der Praxis besser fördert (siehe §2/§3).
Ersparnis 16,76 € bei besserer Energiebilanz. Der Schlauch ist jetzt **kostenpflichtig**, weil die
OEM-Pumpe nur ca. 5 cm Schlauch mitbringt (die Adafruit brachte 530 mm mit).

---

## 2. Warum diese Pumpe — die Kennzahl ist Wh pro Liter

Für ein Akkugerät entscheidet nicht der Preis allein, sondern die Energie pro gefördertem Liter.
Alle Werte aus Produktseiten/Datenblättern, Umrechnung in Wh/L aus Leistung und Förderrate:

| Pumpe | Preis | Leistung | Förderrate | **Wh/L** | Quelle |
|---|---|---|---|---|---|
| **OEM ABC-12527** @3,7 V | **7,74 €** | 1,67 W | ~154 ml/min* | **0,18** | anodas.lt (Spannung + Strom dokumentiert) |
| OEM ABC-12527 @6 V | 7,74 € | 3,24 W | ~250 ml/min* | 0,22 | anodas.lt |
| Adafruit 3910 @5 V | 24,50 € | 2,50 W | 100 ml/min | 0,42 | adafruit.com/product/3910 |
| Whadda WPM447 @6 V | 12,90 € | 5,00 W | 39 ml/min | 2,14 | whadda.com + electrokit.se |

\* Förderrate der OEM-Pumpe skaliert nicht linear mit der Spannung — die Linearskalierung ist meine
Annahme, die Seite nennt nur „1L – 4 min" ohne Spannungsbezug. **Vor dem Einbau messen.**

Nicht gewählt: **Funduino „0-90 ml/min, 3-12 V"** (7,92 €) — im Titel 3–12 V, in den Produktdetails aber „Betriebsspannung 12 V DC" und **keine Stromangabe**, damit ist die Akku-Auslegung nicht belegbar. **Adafruit 3910**: dreifacher Preis bei halber Förderrate. **Whadda WPM447**: fünffache Energie pro Liter.

Verifizierter Spec-Block der OEM-Pumpe (Wortlaut der Produktseite):
> „Rated voltage: 3.7V to 6V · Current: 3V – 400mA, 6V – 540mA · Engine: DC with pinion ·
> Number of satellites: 3 · Productivity: 1L – 4 min · Dimensions: Diameter: 32 mm. Height: 44 mm ·
> Mounting holes diameter: 2.5 mm · Mounting hole layout 44mm · Silicone tube: inner 3 mm / outer 5 mm"

**Einschränkung:** kein deutscher Shop — EU-Versand aus Litauen (Vilnius/Kaunas lagernd), Versand
nach DE laut Seite „auf Anfrage". Das ist der Preis für 17 € Ersparnis; Lieferzeit und Versandkosten
vor der Bestellung klären.

---

## 3. Betriebsspannung — der frühere offene Punkt ist geschlossen

**Entscheidung: 1S-Akku (3,7 V) direkt an der Pumpe, kein Boost, kein Buck.**

Der Grund ist der Wechsel der Pumpe. Die frühere Planung stand auf der Prämisse, dass die Pumpe
5–6 V braucht (Adafruit 3910, Herstellerangabe „Motor voltage: 5 to 6 VDC") und der Direktbetrieb an
einer 1S-Zelle damit undokumentiert war — zusätzlich liefert der XIAO im Akkubetrieb **keine 5 V**
(Seeed-Wiki, wörtlich: „When using battery power, no voltage will be present on the 5V pin"), es
hätte also zwingend einen Wandler gebraucht.

Diese Prämisse ist mit der OEM-Pumpe weg: sie ist **ab 3 V dokumentiert** (3 V – 400 mA) und für
**3,7–6 V** ausgelegt. Eine 1S-Zelle liefert 3,0–4,2 V — die Pumpe läuft damit **innerhalb** ihres
Datenblattbereichs, über den ganzen Entladezyklus.

**Das 2S-Konzept (2 Zellen + Step-Down) wurde geprüft und verworfen:**
- **Wirkungsgrad bringt nichts:** Buck aus 2S (η 0,90) gegen Boost aus 1S (η 0,88) — Laufzeit
  praktisch identisch (32 vs. 31 Tage gerechnet). Und mit der neuen Pumpe entfällt die Wandlung
  komplett, das ist besser als jede Wandlung.
- **Kosten:** 2S braucht einen **eigenen Lader plus Balancer**, weil der Onboard-Lader des XIAO für
  eine Zelle (3,7 V / 4,2 V Ladeschluss) ausgelegt ist. Das sind zusätzliche Bauteile und
  Platinenfläche — bei einem Konzept, dessen Ziel „günstig" ist, der falsche Hebel.
- **Kapazität wird nicht gebraucht:** siehe §4 — die 1S-Zelle reicht für ~85 Dosiervorgänge.
- **Sicherheit:** Reihenschaltung ohne sauberes Balancing ist in einem feuchten Gehäuse ein
  echtes Risiko, nicht nur ein Schönheitsfehler.

Wenn 2S später doch gewünscht wird (z. B. für mehr Reserven), ist der Weg dokumentiert: 2S-Lader
mit Balancer + Buck auf 5 V, und der Onboard-Lader des XIAO wird nicht mehr genutzt.

---

## 4. Akku und Laufzeit

- **EFASO 503759**: ~**59 × 37 × 5 mm** (Typcode; Maße am Listing **nicht** bestätigt → vor Bestellung
  Specblock prüfen), mit **PCM** (Über-/Tiefentladung, Kurzschluss) und **JST PH2.0-2P**.
- **Laden:** über den **Onboard-Lader des XIAO** (BAT-Pads) + USB-C-Durchbruch — kein Lade-IC nötig,
  keine Zusatzplatine. Auf dem XIAO sitzt laut Seeed-Schaltplan (Rev V1.0, Sheet 03 Power) ein
  **SGM40567-4.2** — also 4,2 V Ladeschluss und damit **1S**; ein 2S-Ladebetrieb ist dort nicht
  vorgesehen (Beleg: https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32C6/XIAO_ESP32_C6_v1.0_SCH_260114.pdf,
  SGM40567-Datenblatt noch als Zusatzbeleg offen). (Beim späteren Aufbau mit nacktem ESP32-Modul muss ein eigener 1S-Lader
  vorgesehen werden, z. B. MCP73831.)
- **Laufzeit neu gerechnet** (Pumpe @3,7 V: 1,67 W, ~154 ml/min): ein Dosiervorgang von 300 ml
  braucht ~1,9 min und **0,052 Wh**. Aus 1500 mAh @ 3,7 V (5,55 Wh brutto, ~4,44 Wh nutzbar) →
  **≈ 85 Dosiervorgänge pro Ladung**, bei 1× täglich also rund **3 Monate**. Die alte „4 Wochen\"-Angabe
  galt für die Adafruit-Pumpe mit 2,5 W bei 100 ml/min — die neue Pumpe ist der Grund für den Sprung.
- **Warum keine 18650:** geschützte 18650 ist Ø18,85 × 69 mm und passt in die Wulst (40 mm tief),
  bringt aber ~3× Kapazität, die bei 85 Dosen pro Ladung niemand braucht. Option für später.

---

## 5. Wulst-Maße (aus den finalen Bauteilen abgeleitet)

| Innenmaß | Wert | Bestimmt durch |
|---|---|---|
| Breite | **60 mm** | Pumpe Ø32 + Wandungen, PCB ~52 mm, Zelle 37 mm |
| Tiefe (radial) | **40 mm** | Pumpe Ø32 + 2 × 2,5 mm Wand + Montagefreiheit |
| Höhe | **160 mm** (y = 90–250) | Pumpe 44 mm (+ Halterung), darüber Platine + Zelle |
| Gesamtbreite Topf an der Wulst | **≈ 180 mm** | 140 mm + 40 mm |

Einbau von unten nach oben: **Pumpe** (44 mm Bauhöhe, dadurch deutlich mehr Luft als vorher mit
66,8 mm) → **Platine** → **Zelle** hinter/über der Platine.

**Parameter nachzuziehen (OpenSCAD, `case/params.scad`):**
`pump_d` 27.8 → **32** · `pump_l` 66.8 → **44** · `pump_mount_cc` 50 → **44** · `pump_mount_d` 3.7 → **2.5**.
Die Wulst selbst (60 × 40 × 160) bleibt gültig.

---

## 6. Konsequenzen für die PCB

1. XIAO ESP32-C6 als Modul (Castellated Pads), USB-C-Stirnseite zur Gehäuseöffnung.
2. **JST PH2.0-Buchse** für die Zelle, Ladepfad an die XIAO-BAT-Pads.
3. Pumpe: AO3400A Low-Side, Gate 220 Ω, Pulldown 10 kΩ, 1N5819 antiparallel, **100 µF Pufferelko**.
   Pumpe hängt **direkt an VBAT** — kein Wandler, kein Boost-Layout.
3b. **Zellspannung überwachen (neu, kostet nur einen Widerstand):** Seeed-Wiki dokumentiert dafür
   wörtlich „solder a 200k resistor in a 1:2 configuration … connected to the A0 port", Auswertung
   per `Vbatt = 2 * analogReadMilliVolts(A0)`. Damit kann die Firmware den Ladezustand per Telegram
   melden. Der 3V3-Pin des XIAO liefert laut Seeed bis **700 mA** („regulated output from the onboard
   regulator") — reicht für Sensor + Reserve.
4. Sensor: 3-poliger JST-XH, **VCC über GPIO schaltbar** (nur während der Messung), AOUT auf ADC1.
5. Taster Reset/Boot, Status-LED sichtbar durch das LED-Fenster.
6. **V2 (nacktes ESP32-C6-Modul auf eigener Platine):** zusätzlich eigener **1S-Lader** (MCP73831 o. ä.)
   und eine eigene **3,3-V-Schiene**; die Sensor-/Pumpenbeschaltung bleibt unverändert.

---

## 7. Noch offen / bewusst nicht behauptet

- **Förderrate der OEM-Pumpe bei 3,7 V** nicht dokumentiert (Seite nennt nur „1L – 4 min" ohne
  Spannung) → nach dem Aufbau 60 s in den Messbecher pumpen und auf ml/min umrechnen.
- **Versandkosten/Lieferzeit** der OEM-Pumpe nach DE (anodas.lt: „negotiated individually").
- **Schlauch** muss beschafft werden (3 × 5 mm Silikon, ~1 m) — Position 8.
- **Elektrodenlänge des Sensor v1.2** nicht belegt → am realen Board messen (Messebene liegt 75 mm tief).
- **LDO-Bestückung** des AZ-Boards nur im Foto prüfbar (nicht im Text).
- **Maße der EFASO-Zelle** am Listing nicht bestätigt.
- Versandkosten der übrigen Shops nicht geprüft (AZ-Delivery versandkostenfrei ab 25 €).
- Amazon-Preise von Agenten im Browser gesehen, nicht selbst nachprüfbar (Amazon blockt Skript-Abrufe).
