# 06 – Peristaltikpumpe „ABC-12527": EU-Beschaffungsquellen & Versandkosten nach Deutschland

**Prüfdatum:** 12.09.2026 · **Methode:** web_search/web_extract + curl (Checkout-Simulation, r.jina.ai für JS-Seiten). Kein Browser.
**Auftrag:** Beschaffbarkeit anodas.lt + baugleiche EU-Quellen, exakte Versandkosten nach DE.

---

## TL;DR (Ergebnis in 3 Zeilen)

1. **anodas.lt ist bestellbar** (Add-to-Cart getestet, 7,74 €), aber Versand nach Deutschland **24,20 € brutto** (einzige Checkout-Methode, verifiziert) → **Gesamt 31,94 €**. Zentrallager „Out of Stock", nur Filialbestand Vilnius/Kaunas.
2. **Modell identifiziert:** Die Pumpe ist ein OEM-Artikel von **Wide Top Industrial Ltd (Chaozhou, CN)**; identisch geführt als **ABC-RC.pl Artikel 12527**, EAN **5904384778034** – für umgerechnet ~4,99 €, aber abc-rc.pl **liefert nicht nach Deutschland** (Länderliste ohne DE, verifiziert).
3. **Günstigste verifizierte DE-Alternative:** Funduino „0–90 ml/min" für 9,90 € + 4,90 € = **14,80 €** (Förderleistung unter Ziel-Spec). Einzige weitere ≥100-ml/min-Option: **Adafruit 3910 bei DigiKey DE 25,42 € + 18 € Versand = 43,42 €** (bzw. versandfrei ab 50 € Warenkorb).

---

## 1) Status anodas.lt (verifiziert am 12.09.2026)

| Merkmal | Wert |
|---|---|
| Produkt | Peristaltic Liquid Pump with Silicone Tubing – 3.7-6VDC |
| Produktcode | **ABC-12527** (Brand: OEM) |
| URL | https://anodas.lt/en/peristaltic-liquid-pump-with-silicone-tubing-3-7-6vdc |
| Preis | **7,74 €** inkl. VAT (durchgestrichen: 8,60 €; ex Tax: 6,40 €) |
| Lagerstand | Vilnius Store **In Stock** · Kaunas Store **In Stock** · **Central Warehouse: Out of Stock** |
| Bestellbarkeit | ✅ online bestellbar – Add-to-Cart getestet: Warenkorb „1 item(s) – 7,74 €" |
| Bearbeitung | 1–3 Werktage, Versand aus Filial-/Lagerbestand |
| Versand nach DE | Offizielle Seite: „other countries – **negotiated individually**". Checkout-Quote (simuliert mit Lieferland Deutschland, PLZ 10115): **„Express International Shipping" = 20,00 € netto = 24,20 € brutto** (inkl. 21 % LT-VAT, + bis zu 2 Werktage) – dies ist die **einzige** angebotene Versandmethode nach DE |
| Nutzer-Beobachtung „~27 € Versand" | plausibel/bestätigt: 24,20 € inkl. VAT (bzw. 20 € netto) |
| **Gesamtkosten 1 Pumpe nach DE** | **31,94 €** (7,74 + 24,20) |

Kontakte für Versandverhandlung/Sammelversand: kaunas@anodas.lt · vilnius@anodas.lt (Telefon siehe Shop-Impressum).

Hinweis: Da „negotiated individually" gilt, kann per E-Mail ein günstigerer Versand ausgehandelt werden – die 24,20 € sind der automatisierte Checkout-Preis.

---

## 2) Modell-Identifikation

- **Identisches Produkt (verifiziert über Spec-Fingerprint, Bauteile & Herstellerangabe):**
  **ABC-RC.pl, Artikel 12527 „Mini Pompa Perystaltyczna – DC 6V"**
  - PL: https://abc-rc.pl/pl/products/mini-pompa-perystaltyczna-dc-6v-pompka-dozujaca-z-rurka-silikonowa-12527.html (21,80 zł)
  - EN: https://abc-rc.pl/en/products/mini-peristaltic-pump-dc-6v-dispensing-pump-with-silicone-tube-12527.html (zeigt $5,93; Shop-Kurs 1 zł = 0,229 € → ~4,99 €)
  - EAN/Producer code: 5904384778034 · Hersteller („Entity responsible"): **Wide Top Industrial Limited**, Chaozhou, CN · verantwortliche EU-Entity: Leda ABC-RC, Nidek (PL)
  - Der anodas-Code „ABC-12527" entspricht exakt der ABC-RC-Artikelnummer 12527 (anodas listet als „Brand: OEM").
- **Specs (beide Shops identisch):** 3,7–6 V DC · 3 V/400 mA, 6 V/540 mA · DC-Motor mit Getriebe · **3 Rollen („Satellites")** · Förderleistung **1 L / 4 min (=250 ml/min)** · Ø 32 mm, Höhe 44 mm · Montagelöcher 2,5 mm / Lochabstand 44 mm · Silikonschlauch i≈3 mm (abc-rc: 3,6 mm) / a 5 mm, ca. 25 cm beiliegend.
- **Verwandte Bezeichnungen derselben Modellfamilie** (nicht verwechseln, andere Leistung/Spannung): „G528 / G328"-Mini-Laborpumpen (12 V, 0–150 ml/min, 3×5 mm) und div. „Mini Dosierpumpe 6V 1L/4min"-Aliase auf Amazon/eBay.
- Nützlicher Such-Fingerprint für weitere Quellen: `"3.7V to 6V" "540mA" "1L" "4 min" peristaltic` bzw. EAN `5904384778034`.

---

## 3) Gefundene Angebote (nach Gesamtkosten)

| # | Shop | Produkt / Specs | Preis | Versand → DE | Lieferzeit | Lager | Link |
|---|---|---|---|---|---|---|---|
| 1 | **anodas.lt (LT)** | **Original ABC-12527** (3,7–6 V, 250 ml/min, 3×5 mm, 3 Rollen) | **7,74 €** | **24,20 €** (Express Intl., verifiziert) | Bearbeitung 1–3 WT + ~2 WT Versand | Filialen ja / Zentrallager nein | https://anodas.lt/en/peristaltic-liquid-pump-with-silicone-tubing-3-7-6vdc |
| 2 | abc-rc.pl (PL) | **Original, Code 12527** (identisch) | **21,80 zł ≈ 4,99 €** | **kein Versand nach DE** – Ziel-Länderliste: CZ, DK, FI, FR, GR, NL, LT, LV, PL, SK, SE, UA, IT (verifiziert) | national ~1 Tag | k.A. (Status „New") | https://abc-rc.pl/pl/products/mini-pompa-perystaltyczna-dc-6v-pompka-dozujaca-z-rurka-silikonowa-12527.html |
| 3 | Funduino (DE) | Peristaltik-Dosierpumpe **0–90 ml/min, 3–12 V**, Schlauch 3×5 mm, selbstansaugend (bei 6 V nur ~45 ml/min lt. Beschreibung) | 9,90 € | **4,90 €** (DHL, verifiziert) | 1–3 Werktage | **63 Stk.** | https://funduinoshop.com/en/electronic-modules/valves-pumps/pumps/peristaltic-peristaltic-and-dosing-pump-0-90ml/min-3-12v |
| 4 | Funduino (DE) | Peristaltikpumpe 12 V, 60–150 ml, Ø32×23 mm, 3×5 mm | 15,65 € | 4,90 € | 1–3 Werktage | 1 Stk. | https://funduinoshop.com/en/electronic-modules/valves-pumps/pumps/peristaltic-pump-dosing-pump-12v-60-150ml |
| 5 | 42project.net (DE) | Peristaltikpumpe **6 V DC, 5 W, 90 ml/min**, 3 Rollen, Silikon | 15,99 € | **1,45 €** (Hermes, verifiziert) | k.A. | **Nicht vorrätig** | https://42project.net/shop/aktoren-motoren-servos/peristaltikpumpe-6v-dc-5w-90ml-min-dosierpumpe-chemiepumpe-pumpe-silikon |
| 6 | **DigiKey DE** | **Adafruit 3910** (5–6 V, bis 100 ml/min, Schlauch 3,5×5 mm, selbstansaugend), Teilenr. 1528-2708-ND | **21,36 € netto / 25,42 € brutto** | **18,00 €** (< 50 €), **gratis ab 50 €** (offizielle DigiKey-DE-Seite) | ab Lager | **82 Stk.** | https://www.digikey.de/de/products/detail/adafruit-industries-llc/3910/9658066 |
| 7 | Mouser (EU/DE) | Adafruit 3910 | **nicht verifizierbar** (Bot-Block „Access denied"); US-Seite: $24.95 | versandfrei ab 50 € (EU-Seiten); darunter k.A. | „In Stock: 7" (US-Seite) | 7 Stk. (US-Zählung) | https://www.mouser.com/ProductDetail/Adafruit/3910 |
| 8 | BerryBase (DE) | Adafruit 3910 (5–6 V) | 24,50 € | DHL 4,95 € (gratis ab 79 €) | — | **„Artikel aktuell nicht lieferbar"** | https://www.berrybase.de/adafruit-peristaltische-fluessigkeitspumpe-mit-silikonschlauch-5v-bis-6v-dc |
| 9 | BerryBase (DE) | Adafruit **1150** (12 V, bis 100 ml/min) | 28,90 € | 4,95 € | 1–3 Tage | 10 Stk. | https://www.berrybase.de/adafruit-peristaltische-fluessigkeitspumpe-mit-silikonschlauch-12v-dc |
| 10 | Botland (PL/DE) | Velleman WPM447 (39 ml/min) bzw. DFRobot Gravity (45 ml/min) | 15,90 € | (nicht geprüft, da ungeeignet) | 1–3 Tage | lagernd | https://botland.de/pumps/15387-elektrische-peristaltische-pumpe-6v-velleman-wpm447-5410329703073.html |
| 11 | robot-italy (IT) | Adafruit 3910 | 36,53 € | k.A. | — | — | https://robot-italy.com/products/3910-peristaltic-liquid-pump-with-silicone-tubing-5v-to-6v-dc-power |

**Nicht konform / keine Treffer (geprüft):**

| Shop | Ergebnis |
|---|---|
| TME.eu | Kein passendes Mikro-Modell; nur FISNAR PPD-130 Industriespender (Detail-Suche 403-blockiert) |
| Farnell | Nur CPC-UK WPM447 (39 ml/min) und DFRobot Gravity (45 ml/min) – beide ungeeignet + UK-Versand |
| Conrad | Kein passendes Produkt gefunden (nur Garten-/Druckluftpumpen) |
| RS Components | Nur Industriepumpen (Verderflex, ProMinent) – kein Hobby-Segment |
| Distrelec | Nur Industrie-/Dosiertechnik (ProMinent, Loctite) – kein Treffer |
| eBay.de | **Nicht verifizierbar** (HTTP 403 für Agent-Zugriff). Kategorie-Snippets: gewerbl. Angebote ab ~10,89 € („Peristaltik-Dosierpumpe 0–90 ml/min, 3–12 V") und „12 V/24 V, 40 ml/min" 9,50 € + 5,90 € Versand – Durchfluss teils < 100 ml/min |
| Amazon.de | **Nicht verifizierbar** (503/Bot-Wall). Existierende Listings (via Aggregator-Cache): 6-V-Dosierpumpen ~12–25 €, z. B. ASIN B098SC32VJ (DC 6 V, Varianten 1×3/2×4/3×5 mm) – Preis/Versand/Lager nicht prüfbar |
| AliExpress | Listings vorhanden (z. B. „6V DC Dosing Pump Head 0–150 ml/min", 732 sold); **EU-Lager & Versand nach DE nicht verifizierbar** (JS/Bot-Wall) |

---

## 4) Vergleich gegen Ziel-Specs (peristaltisch · 3,7–6 V · ≥100 ml/min · 3×5 mm · selbstansaugend)

| Kandidat | Spec-Treue | Gesamtkosten DE |
|---|---|---|
| **anodas ABC-12527** | ✔ voll (250 ml/min @ 6 V) | **31,94 €** |
| abc-rc 12527 | ✔ voll | ~4,99 € + Weiterleitung (nicht direkt lieferbar) |
| DigiKey Adafruit 3910 | ✔ nahezu („bis 100 ml/min", Schlauch 3,5×5 mm) | 43,42 € (1 Stk.) / 25,42 € je Stk. bei 2 Stk. (50,84 € → versandfrei) |
| Funduino 0–90 ml/min | ⚠ 90 ml/min max (bei 6 V ~45 ml/min) | **14,80 €** |
| 42project 6 V 90 ml/min | ⚠ 90 ml/min; derzeit nicht lieferbar | 17,44 € (wenn verfügbar) |
| Funduino 12 V 60–150 ml | ✘ 12 V | 20,55 € |
| Botland/Farnell (WPM447/DfRobot) | ✘ 39–45 ml/min | — |

---

## 5) Empfehlung

**Empfehlung 1 – Spez-konform & günstigste verifizierte Bestelloption:**
**anodas.lt · Gesamtpreis 31,94 €** (7,74 € Pumpe + 24,20 € Express International). Bestellung online möglich (Warenkorb getestet); da Zentrallager leer, ggf. Versand aus Filialbestand – bei Bedarf Versandkosten per E-Mail verhandeln („negotiated individually", kaunas@anodas.lt).

**Empfehlung 2 – Bestes Preis-/Leistungs-Fallback (mit Spec-Abstrich beim Durchfluss):**
**Funduino 14,80 €** (9,90 € + 4,90 €, 63 Stk. lagernd, 1–3 Werktage). Nur wählen, wenn ≤90 ml/min ausreichend sind bzw. die Pumpe per PWM/zusätzlicher Spannung betrieben wird.

**Empfehlung 3 – wenn Groß-Distributor gewünscht / für Sammelbestellung:**
**DigiKey DE · Adafruit 3910** – 43,42 € bei Einzelkauf, **versandkostenfrei ab 50 € Warenkorb** (2 Stk. = 50,84 € → 25,42 €/Stk. inkl. Versand). 82 Stk. ab Lager.

**Preis-Ausreißer (falls Weiterleitung organisierbar):** abc-rc.pl verkauft dieselbe Pumpe für ~4,99 € – bei Option „Weiterleitung durch Dritte" (PL-Versand an Sammeladresse/Paketweiterleiter) Gesamtkosten grob 10–15 €.

---

## 6) Methodik / Quellen

- anodas.lt: Produktseite + OpenCart-Add-to-Cart (curl, Session-Cookies) + Checkout-Versandquote `route=total/shipping/quote` mit `country_id=81` (Deutschland) → JSON-Quote 24,20 €. Preis/Lager/Specs via curl-HTML (12.09.2026).
- abc-rc.pl: Produktseiten PL/EN + Delivery-Seite (via r.jina.ai, da Site Agent-Zugriffe blockt) – Ziel-Länderliste ohne Deutschland; PL-Preis 21,80 zł; EAN 5904384778034.
- DigiKey DE: Produktseite (via r.jina.ai): netto 21,36 € / brutto 25,42 €, „Auf Lager: 82"; Versandregeln von digikey.de Hilfe-Seite: 18 € unter 50 €, gratis ab 50 €.
- Funduino: Produkt- und Versandseite (Versand DE 4,90 €).
- 42project.net: Produktseite + Versandseite (1,45 € Hermes; Artikel „Nicht vorrätig").
- BerryBase: Produktseiten (3910 nicht lieferbar; 1150 lagernd) + Versandkosten (DHL 4,95 €, frei ab 79 €).
- Mouser: US-Produktseite (Stock 7) – EU-Preis blockiert.
- eBay.de/Amazon.de/AliExpress: blockiert bzw. nicht verifizierbar (403/503/JS); Angaben nur aus Suchmaschinen-Snippets, als solche gekennzeichnet.
- Alle Preise inkl. MwSt. soweit nicht anders vermerkt. Keine Schätzungen – nicht verifizierbare Punkte sind explizit als solche gekennzeichnet.
