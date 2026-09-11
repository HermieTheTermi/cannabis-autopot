# EU-Beschaffung Pumpe + Sensor — konsolidiert (Stand 12.09.2026)

**Anlass:** Die im BOM gewählte OEM-Peristaltikpumpe (anodas.lt, 7,74 €) ist praktisch nicht
bestellbar — Versand nach DE laut Checkout **24,20 € brutto (Express International, einzige Methode)**
→ Gesamt **31,94 €**. Gesucht: EU-/DE-Quellen für Pumpe, Sensor und den noch offenen Schlauch.

Alle Preise am 12.09.2026 live auf der Produktseite geprüft (curl/web_extract bzw. browser-harness).
Detailreports dieser Runde: `05_pumpe-de-shops.md`, `06_pumpe-eu-quellen.md`,
`07_sensor-quellen.md`, `08_pumpe-ebay-aliexpress.md`.

---

## 1. Kritischer Filter zuerst: 1S-Akku

Das Design hängt die Pumpe **direkt an die 1S-Zelle (3,0–4,2 V)** — kein Boost.
Damit fallen **alle reinen „6 V"-Pumpen aus** (starten unter 6 V nicht):

- Tyenaza 0–150 ml/min (17,79 €), Dioche 100 ml/min (12,09 €), FTVOGUE 100 ml/min (13,12 €),
  Whadda WPM447 (39 ml/min), DFRobot DFR0523 (1,8 A), Kamoer NKP-DC-B10B (12 V) → **ungeeignet**.

1S-taugliche Kandidaten sind nur: **OEM ABC-12527 (3,7–6 V)**, **Funduino (3–12 V)** und die
generischen **3,7–5-V-Listings**.

## 2. Pumpe

| Rang | Produkt | Preis | Versand DE | Gesamt | Specs | Status |
|---|---|---|---|---|---|---|
| 1 | **Funduino Peristaltik 0–90 ml/min, 3–12 V** | 9,11 € (Amazon, ASIN `B0DT1JCFNV`) | 0 € (Gratislieferung 16.09.) / 4,90 € im Funduino-Shop (7,92 €) / 4,90 € auf eBay (8,71 €) | **9,11 €** | 60 × 40 × 40 mm · 250 mA · Schlauch 3 × 5 mm · bei 6 V ca. 45 ml/min (Schätzung, nicht belegt) | ✅ ab Lager (Verkäufer funduino, DE) |
| 2 | **Generische 3,7–5-V-Mini-Peristaltik** (`B0H5JLWBMW` 5,23 € / `B0H4MNN2MN` 7,03 € / `B0H4ZXYCDX` 10,28 € / `B0H4KVYL69` 13,40 €, „200 ml/min") | 5,23–13,40 € | 0 € | **5,23–13,40 €** | **keine ml/min-, Strom- oder Maßangabe** in den Listings · 3,7–5 V | ⚠️ ab Lager, aber Specs unbelegt → nur nach eigener Messung |
| 3 | **OEM ABC-12527** (anodas.lt, Litauen) | 7,74 € | **24,20 €** (einzige Methode) | **31,94 €** | 3,7–6 V · 3 V/400 mA, 6 V/540 mA · ~250 ml/min · Ø32 × 44 mm · Schlauch 3 × 5 mm | ✅ Lager Vilnius/Kaunas, 1–3 WT · Versand laut Seite „negotiated individually" |
| — | **Baugleiche Pumpe bei abc-rc.pl (PL)** | **21,80 zł ≈ 4,99 €** | 7,90 zł ≈ 1,81 € *laut hinterlegtem Versandschema* | **~6,80 €** | identisch (Shop-Code 12527, EAN 5904384778034, gleicher Spec-Block) | ❌ **liefert nicht nach DE** (Zielländer-Dropdown ohne Deutschland) → nur per Mail-Anfrage/Weiterleitung |
| — | Adafruit 3910 (DigiKey DE) | 25,42 € | 18 € (**frei ab 50 € Warenkorb**) | 43,42 € / 25,42 € im Sammelkorb | 5–6 V, bis 100 ml/min, 500 mA, 3,5 × 5 mm | ✅ 82 lagernd · BerryBase-Exemplar weiterhin nicht lieferbar |
| — | 42project.net 6 V / 90 ml/min | 15,99 € | 1,45 € | 17,44 € | — | ❌ nicht vorrätig |

**Weitere geprüfte Quellen ohne verwertbares Angebot:** Reichelt (0 Treffer), AZ-Delivery (keine Pumpen),
TME/RS/Farnell/Distrelec (Industrie bzw. <45 ml/min), Conrad (nur WPM447), eBay.de (ABC-12527: 0 Treffer),
AliExpress: 3,7–6-V-Peristaltikpumpen **ausschließlich aus dem CN-Lager** (EU-Lager DE/CZ/ES: keine).

**Empfehlung (Kosten/Nutzen):** Funduino für 9,11 € als Arbeitspumpe, plus — falls der präzise
Energiewert aus dem BOM gebraucht wird — ein generisches 3,7-V-Listing (5,23 €) als Messmuster.
Damit kostet die Pumpe ≤ 15 € statt 31,94 €. Förderrate bei 3,7 V **in beiden Fällen messen**
(30 s in den Messbecher), das war im BOM ohnehin als offener Punkt vermerkt.
Wer exakt das BOM-Modell will: abc-rc.pl per Mail fragen (pomoc@abc-rc.pl) — 4,99 € sind der
günstigste EU-Preis für die identische Pumpe.

## 3. Sensor (kapazitiv, analog)

| Rang | Produkt | Preis | Versand | pro Stück | Status |
|---|---|---|---|---|---|
| 1 | **ARCELI 6er-Pack V1.2 kapazitiv** (Amazon `B0FPRBY7LW`) | **7,49 €** | 0 € (Gratislieferung 16.09.) | **1,25 €** | ✅ ab Lager |
| 2 | 5er-Pack kapazitiv analog (Amazon `B0CQNF7S7L`) | 7,99 € | 0 € (16.09.) | 1,60 € | ✅ ab Lager |
| 3 | 10er-Pack 3,3–5,5 V, 98 × 23 mm (`B0H5K1JRW8` / `B0GV3BJHZB`) | 9,45 € / 9,77 € | 0 € | 0,95 / 0,98 € | ✅ ab Lager (Lieferzeit teils bis 05.10.) |
| 4 | Botland.de **DFRobot SEN0193** | 6,50 € | 4,99 € | — | ≈ 11,49 € · ✅ lieferbar |
| 5 | Reichelt **SEEED** kapazitiv | 5,99 € | 5,95 € | — | ≈ 11,94 € · ✅ wieder „ab Lager" |
| — | DigiKey DE **SEN0193** | 6,01 € | 18 € (frei ab 50 €) | — | ✅ 236 lagernd |
| — | **AZ-Delivery V1.2 (bisherige Wahl 4,99 €)** | — | — | — | ❌ **alle Varianten ausverkauft** (Shopify `available:false`) |
| — | Funduino 1,61 € / BerryBase & Reichelt DEBO 2,60–2,80 € | — | — | — | ❌ nicht lieferbar |

**Empfehlung:** 6er-Pack ARCELI für 7,49 € — günstiger als ein einzelner AZ-Sensor und liefert
Ersatz für die erwartbare Korrosions-/Bruchreserve.

⚠️ **Weiterhin unbelegt (kein Anbieter dokumentiert es):** die Elektrodenlänge ≥ 75 mm. Alle Quellen
nennen nur Gesamtlängen von 92–100 mm. Bei 75–85 mm Einstecktiefe ragen also 7–25 mm heraus →
Elektronikbereich muss gegen Spritzwasser geschützt werden. **Am Muster nachmessen** (offener Punkt
bleibt bestehen).

## 4. Nebenbefund — BOM-Position 8 (Silikonschlauch) ist damit auch lösbar

- **Silikonschlauch 3 mm ID × 5 mm OD, lebensmittelecht, 3 m — 6,99 €** (Amazon `B0CMQJDJ2H`, Gratislieferung 16.09.)
- Alternativen: 6 m für 8,99 € (`B0CYPKY54S`), 2 m für 6,99 € (`B0CYPHGKCQ`)

Damit liegt die Zeile „Schlauch — Preis/Link offen" (bisher 3–5 € geschätzt) belegbar bei ~7 €.

## 5. Summe Bestellvorschlag (alles DE-Versand, alles ab Lager)

| Position | Betrag |
|---|---|
| Pumpe Funduino 3–12 V, 0–90 ml/min | 9,11 € |
| Sensor ARCELI 6er-Pack V1.2 | 7,49 € |
| Silikonschlauch 3 × 5 mm, 3 m | 6,99 € |
| **Summe** | **23,59 €** |
| *(optional)* zweites Pumpenmuster 3,7–5 V zum Messen | +5,23 € |
