# 07 – Sensorquellen: kapazitive Bodenfeuchte-Sensoren (analog, 3,3 V)

**Projekt:** cannabis-autopot (ESP32, eigener ADC, Einstecktiefe ~75–85 mm, VCC per GPIO schaltbar)
**Stand:** 12.09.2026, ~01:25 CEST · **Methode:** nur web_search / web_extract / curl (kein Browser)
**Alle Preise in EUR inkl. MwSt.** · Abweichungen zum Stand 11.09.2026 sind markiert.

---

## 1. TL;DR – Rangliste (günstigste Optionen inkl. Versand nach DE)

| # | Option | Sensorpreis | Versand DE | Gesamt | €/Stk. | Verfügbarkeit | Beleg |
|---|--------|------------|-----------|--------|--------|---------------|-------|
| 1 | **Amazon 10er-Pack** „Bodenfeuchtigkeitssensor-Modul, 10 Stück, kapazitiv, 3,3–5,5 V“ (ASIN **B0H5K1JRW8**) | 9,45 € (10 Stk.) | „GRATIS Lieferung“ angezeigt (bedingt: „für qualifizierte Erstbestellung“), sonst Amazon-Standard | **9,45 €** (+ evtl. Versand) | **0,95 €** | Auf Lager; Lieferfenster 25.09.–05.10.2026 (CN-Versender JUWORDKING) | ✅ Produktseite per curl verifiziert |
| 2 | **Amazon 10er-Pack** „Kapazitives Bodenfeuchtigkeitssensor-Modul, 10 Stück, Analogausgang 0–3,0 V“ (ASIN **B0GV3BJHZB**) | 9,77 € (10 Stk.) | wie oben | **9,77 €** (+ evtl. Versand) | 0,98 € | Auf Lager; 23.09.–01.10.2026 (Elchuiaby) | ✅ verifiziert |
| 3 | **Amazon ARCELI 6er-Pack V1.2** (ASIN **B0FPRBY7LW**) | 7,49 € (6 Stk.) | wie oben | **7,49 €** (+ evtl. Versand) | 1,25 € | Auf Lager; Lieferung ab 14.–16.09. (lingyunfeng) | ✅ verifiziert |

**Einzelkauf (1 Sensor), nur verifizierte, aktuell bestellbare Quellen:**

| # | Option | Sensor | Versand | Gesamt | Beleg |
|---|--------|--------|---------|--------|-------|
| a | Botland.de (PL) – DFRobot SEN0193 | 6,50 € | ab 4,99 € (frei ab 100 €) | **≈ 11,49 €** | ✅ Preis/„Erhältlich/66 Stk. auf Lager“ vom Produktseiten-HTML |
| b | Reichelt.de – SEEED 101020614 (Grove, korrosionsbeständig) | 5,99 € | 5,95 € (DHL bis 10 kg) | **11,94 €** | ✅ „ab Lager, Lieferzeit 1–2 Werktage“ (per jina/Web-Extract) |
| c | AZ-Delivery V1.2 1x Modul | 4,99 € | 3,90 € (unter 25 € Bestellwert) | **8,89 €** | ⚠️ **derzeit AUSVERKAUFT** (Preis/Status von Produktseite; Status kann sich täglich ändern) |

**Nicht mehr gültig / Achtung:**
- **AZ-Delivery ist am 12.09.2026 ausverkauft** (`schema.org/OutOfStock`, Shopify `available:false` für alle Varianten). Variantenpreise (Sonderpreis, Normalpreis 1x 5,99 €): **1x 4,99 € · 3x 7,99 € (2,66 €/Stk) · 5x 9,99 € (2,00 €/Stk)** — alle ausverkauft. AZ-Delivery füllt das Lager erfahrungsgemäß wieder auf; Preise gelten als Referenz.
- Funduino (1,61 €) und BerryBase/reichelt „DEBO CAP SENS“ (2,60/2,80 €) sind die absoluten Preisbrecher, aber **alle derzeit nicht lieferbar** (Details unten).
- **DigiKey:** Einzelbestellung lohnt nicht — 6,01 € Sensor + **18 € Versand** unter 50 € Bestellwert (= 24,01 €). Erst ab 50 € Warenwert versandkostenfrei.

---

## 2. Detailtabelle: alle geprüften Shops

| Shop | Produkt | Preis | Versand DE | Verfügbarkeit | Link |
|------|---------|-------|-----------|---------------|------|
| **az-delivery.de** | Bodenfeuchte-Sensor Modul V1.2 (kapazitiv, analog) | 4,99 € (1x), 7,99 € (3x = 2,66/Stk), 9,99 € (5x = 2,00/Stk) | 3,90 € bis 24,99 €; **frei ab 25 €** | ❌ **AUSVERKAUFT** (alle Varianten, 12.09.2026) | https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2 |
| **reichelt.de** | SEEED Grove 101020614 kapazitiv korrosionsbeständig | 5,99 € | 5,95 € (DHL bis 10 kg) | ✅ **„ab Lager, Lieferzeit 1–2 Werktage“** (Stand 12.09.; frühere Angabe „nicht lieferbar“ überholt) | https://www.reichelt.de/de/de/shop/produkt/arduino_-_feuchtigkeitssensor_boden_korrosionsbestaendig_-369415 |
| **reichelt.de** | FREI „Entwicklerboards – Feuchtesensor (Bodenfeuchte)“ = DEBO CAP SENS (EAN 4251266700777) | 2,80 € | s.o. | ❌ nicht lieferbar („Voraussichtlich lieferbar ab 30.5.2026“ – Datum bereits verstrichen, Status unklar) | https://www.reichelt.de/de/de/shop/produkt/entwicklerboards_-_feuchtesensor_bodenfeuchte_-223620 |
| **berrybase.de** | Analoger kapazitiver Bodenfeuchtesensor (CAP-SHYG, baugleich DEBO/Typ „100×22×10 mm“) | 2,60 € | frei ab 150 €; konkrete Paketpreise nicht maschinell auslesbar (**nicht verifiziert**) | ❌ „Artikel aktuell nicht lieferbar“ | https://www.berrybase.de/analoger-kapazitiver-bodenfeuchtesensor |
| **funduinoshop.com** | Kapazitiver Feuchtigkeitssensor – 1.2 Version (98×23 mm) | **1,61 €** (statt 2,01 €) | 4,90 € (DE) | ❌ **Ausverkauft** | https://funduinoshop.com/elektronische-module/sensoren/feuchtigkeitssensoren/kapazitiver-feuchtigkeitssensor-1.2-version |
| **eckstein-shop.de** | DFRobot Gravity Analog Capacitive SEN0193 | 8,00 € | DHL/DPD ab 6,50 €; Warenpost ab 2,60 € | ❌ Nachbestellung: „voraussichtlich ab 02.09.2026, Lieferfrist ca. 4 Wochen“ (Text widersprüchlich, faktisch nicht ab Lager) | https://eckstein-shop.de/DFRobot-Gravity-Analog-Capacitive-Soil-Moisture-Sensor-Corrosion-Resistant |
| **digikey.de** | DFRobot SEN0193 | **6,01 € brutto** (5,05 € netto), 1er-Staffel | **18 €** unter 50 €; frei ab 50 € | ✅ „Auf Lager: 236“ (verifiziert 12.09.2026) | https://www.digikey.de/de/products/detail/dfrobot/SEN0193/6588605 |
| **botland.de** (PL) | DFRobot Gravity SEN0193 | 6,50 € brutto (5,46 € netto) | ab 4,99 €; frei ab 100 € | ✅ erhältlich, „auf Lager 66 Stck.“, Versand 24 h | https://botland.de/schwerkraft-wettersensoren/10305-dfrobot-gravity-analoger-bodenfeuchtesensor-korrosionsbestandig-sen0193-6959420910434.html |
| **amazon.de** | 10er B0H5K1JRW8 (3,3–5,5 V) | 9,45 € | s. Rangliste | ✅ Auf Lager | https://www.amazon.de/dp/B0H5K1JRW8 |
| **amazon.de** | 10er B0GV3BJHZB (Analog 0–3 V) | 9,77 € | s.o. | ✅ Auf Lager | https://www.amazon.de/dp/B0GV3BJHZB |
| **amazon.de** | 10er Fasizi B09Z2HBL8R | 9,99 € | s.o. | ✅ (Liefertermin 14.–16.09. genannt) | https://www.amazon.de/dp/B09Z2HBL8R |
| **amazon.de** | ARCELI 6er V1.2 B0FPRBY7LW | 7,49 € | s.o. | ✅ Auf Lager | https://www.amazon.de/dp/B0FPRBY7LW |
| **amazon.de** | BerryBase V1.2 Einzelmodul B07L4VP3DW | 2,60 € | 5,95 € | ✅ „Auf Lager“ (Marketplace-Angebot BerryBase) → total 8,55 € | https://www.amazon.de/dp/B07L4VP3DW |
| **ebay.de** | Einzelmodul (Verkäufer roboter-bausatz, MakerMind) | 4,39 € | – | ❌ Angebot **beendet** (05.07.) | https://www.ebay.de/itm/174939673471 |
| **ebay.de** | „10 Stück“ (Verkäufer buyasport) | Anzeige „EUR 20,72/Stk.“ – **mehrdeutig** (je 10er-Pack ≈ 2,07 €/Stk oder je Einzelmodul; nicht abschließend verifiziert) | Gratis-Versand-Claim unklar | ✅ verfügbar (früherer Abruf; aktuell erneuter Abruf von eBay geblockt) | https://www.ebay.de/itm/307097025373 |
| **tme.eu** (PL) | SEN0193 (Artikel df-sen0193) gelistet | **Preis nicht verifizierbar** (Cloudflare/Cookie-Wall bei curl + jina) | nicht geprüft | keine Preisangabe erhaltbar | https://www.tme.eu/de/details/df-sen0193/environmental-sensors/dfrobot/sen0193/ |
| **conrad.de** | – | – | – | kein passendes Produkt gefunden (nur industrielle kapazitive Näherungsschalter) | – |
| **pollin.de** | – | – | – | kein kapazitiver Arduino-Bodenfeuchtesensor im Sortiment gefunden | – |
| **exp-tech.de** | – | – | – | kein günstiger Einsteck-Sensor; nur Dragino-LoRaWAN-Sensoren (34–46 €+) | – |
| **sertronics.de / voelkner.de** | – | – | – | per Web-Suche keine Treffer (nicht weiter verifiziert) | – |

---

## 3. Amazon-Mehrpackungen – komplette Trefferliste (Suchseite, 12.09.2026)

Fette Einträge wurden einzeln auf der Produktseite verifiziert; die übrigen sind Suchseiten-Daten (nicht einzeln verifiziert).

| ASIN | Beschreibung | Preis | Stück | €/Stk. |
|------|--------------|-------|------|--------|
| **B0H5K1JRW8** | Bodenfeuchtigkeitssensor-Modul, kapazitiv, 3,3–5,5 V, analog | **9,45 €** | 10 | **0,95 €** |
| B0GWJ9RXJR | 10 Stück, PH2.54-Anschluss, Echtzeit-Tracking | 9,64 € | 10 | 0,96 € |
| **B0GV3BJHZB** | 10 Stück, Analogausgang 0–3,0 V | **9,77 €** | 10 | 0,98 € |
| **B09Z2HBL8R** | Fasizi 10 Stück, korrosionsbeständig | **9,99 €** | 10 | 1,00 € |
| **B0FPRBY7LW** | ARCELI 6 Stück V1.2 | **7,49 €** | 6 | 1,25 € |
| B0H1H92T7H | 6 Stück, korrosionsfrei | 8,59 € | 6 | 1,43 € |
| B0FPFTS2BF | 6 PCS, analog | 8,99 € | 6 | 1,50 € |
| B0D8Q6PDXL | Heevhas 5 Stück | 7,65 € | 5 | 1,53 € |
| B0CQNF7S7L | 5 Stück | 7,99 € | 5 | 1,60 € |
| B07DDFZ3MD | iHaospace 10 Stück V2.0 | 16,67 € | 10 | 1,67 € |
| B0H9SMWFKF | 5 Stück Modul | 8,49 € | 5 | 1,70 € |
| B07L2RV1D2 | DollaTek 3 Stück | 5,99 € | 3 | 2,00 € |
| B0FVMG6KCC | Einzelmodul | 4,49 € | 1 | 4,49 € |
| **B07L4VP3DW** | BerryBase Einzelmodul V1.2 | **2,60 €** + 5,95 € Versand | 1 | 8,55 € (inkl. Versand) |

**Versand-Hinweis Amazon:** Bei den o.g. Angeboten wird „GRATIS Lieferung“ nur „für qualifizierte Erstbestellung“ angezeigt (Amazon-Kondition, nicht ohne Login/Warenkorb final prüfbar). Fällt sie weg, gelten die normalen Amazon-Versandkosten (i.d.R. kostenpflichtig unter 39 € Warenwert bzw. Verkäufer-Versandkosten). Lieferzeiten der CN-Versender: 1–4 Wochen (schnellste Angebote ARCELI/Fasizi: ab 14.–16.09.).

---

## 4. Erfüllung der Anforderungen

| Anforderung | Status |
|-------------|--------|
| Kapazitiv (nicht resistiv) | ✅ alle gelisteten Produkte |
| Analoger Ausgang | ✅ 0–3 V (ADC-freundlich, ESP32-ADC 3,3 V passt) |
| 3,3 V-tauglich | ✅ V1.2-Klasse + SEN0193: laut Funduino/DFRobot-Wiki **3,3–5,5 V**, Ausgang 0–3 V; Grove 101020614: laut Seeed **3,3 V/5 V**. ⚠️ AZ-Delivery nennt auf der Produktseite nur „Betriebsspannung 5 V DC“ (Klone laufen i.d.R. auch mit 3,3 V; für AZ nicht dokumentiert). VCC per GPIO schaltbar: alle (ca. 5 mA). |
| Platine schmal | ✅ alle ~22–23,5 mm breit (AZ 22 mm; BerryBase/Reichelt-DEBO 22 mm; SEN0193 23 mm; Grove 23,5 mm) |
| **Elektrodenlänge ≥ 75 mm** | ❌ **NIRGENDS BELEGT.** Kein Anbieter dokumentiert die Elektroden-/Messbereichslänge. Dokumentiert sind nur **Gesamtlängen**: AZ 97 mm (22×97×9), BerryBase/Reichelt-DEBO 100 mm (100×22×10), Funduino 98 mm (98×23), DFRobot SEN0193 98 mm (3.86×0.905 in), Seeed Grove 92,1 mm (92,1×23,5×6,5). |

**Wichtig zur Einstecktiefe (75–85 mm):** Bei 75–85 mm Einstecktiefe ragen von einem ~92–100 mm langen Modul nur noch **7–23 mm** aus der Erde. Der Elektronik-/Anschlussbereich (oberes Drittel des Moduls) liegt damit direkt an bzw. knapp unter dem Erdniveau → gegen Feuchtigkeit schützen (Schrumpfschlauch/Gehäuse/Schutzhülse) oder Einstecktiefe begrenzen. Ob die kapazitive Messfläche der V1.2-Klasse ≥ 75 mm lang ist, ist **nicht herstellerbelegt** — vor Serienfertigung an einem Muster nachmessen (Trace-Länge auf der Platine).

---

## 5. Verifikations-Status & Methodik

**Verifiziert (12.09.2026):**
- Amazon-Suchseite + 5 Produktseiten per curl vollständig abrufbar (in diesem Lauf **nicht** blockiert — Preise einzeln gegengeprüft, siehe Abschnitt 3). Abweichend zur Auftrags-Vorgabe, dass Amazon per curl blockiert sei.
- DigiKey: 6,01 € brutto / 236 Stück (via r.jina.ai-Leseproxy der Produktseite).
- Reichelt: SEEED 5,99 €, „ab Lager“ (Produktseite + jina); Versandkosten 5,95 € (reichelt.de/versandkosten).
- AZ-Delivery: Produktseite (Shopify-JSON `available:false`, schema.org OutOfStock) + Versandkostenseite (3,90 € bis 24,99 €).
- Botland: Produktseite (HTML) — Preis 6,50 €, 66 Stk. auf Lager, „Lieferung ab 4,99 € / Kostenlose Lieferung ab 100 Euro“.
- Funduino: Seite (data-article-price 1,61 €, „Ausverkauft“), Versandtabelle 4,90 € DE.
- Eckstein: Shop-Seite — 8,00 €, Nachbestellstatus; Versand DHL/DPD ab 6,50 €, Warenpost ab 2,60 €.

**Nicht verifiziert / offen:**
- **TME.eu:** SEN0193 gelistet, Preis nicht abrufbar (Cloudflare-/Cookiebot-Wall bei curl und jina). Nichts geraten.
- **Amazon-Versandkosten** der Multipacks („qualifizierte Erstbestellung“-Kondition) — ohne Login/Warenkorb nicht final bestimmbar.
- **eBay-Preis des 10er-Packs** (20,72 €-Angabe mehrdeutig „/Stk.“); eBay blockt aktuell Re-Abrufe. Einzel-Angebot für 4,39 € ist beendet.
- **BerryBase Versandkostenhöhe** (nur „frei ab 150 €“ auslesbar).
- Conrad, Pollin, exp-tech, sertronics, voelkner: kein passendes Produkt gefunden (Web-Suche; keine systematische Shop-Durchsuchung).

**Änderungen gegenüber dem bekannten Stand vom 11.09.2026:**
- AZ-Delivery: jetzt **ausverkauft** (gestern noch 4,99 € gelistet) — Status kurzfristig wechselnd.
- Reichelt SEEED: jetzt **wieder lieferbar** („ab Lager“) — frühere Angabe „nicht lieferbar“ überholt.
- DigiKey: 236 statt 237 Stück (Bestand sinkt langsam).

**Quellen-URLs (Versandkosten):**
- AZ: https://www.az-delivery.de/pages/versandinformation · Reichelt: https://www.reichelt.de/versandkosten · Eckstein: https://eckstein-shop.de/shipping-information · DigiKey: https://www.digikey.de/de/help-support/delivery-information/delivery-time-and-cost · Funduino: https://funduinoshop.com/versand-und-zahlungsbedingungen · Botland: Produktseite (Header) + https://botland.de
