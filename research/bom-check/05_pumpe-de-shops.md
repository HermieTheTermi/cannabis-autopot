# 05 – Peristaltische Schlauchpumpen (Dosierpumpen) in deutschen Shops

**Stand:** 12.09.2026 (Abrufdatum aller Shopseiten) · **Projekt:** cannabis-autopot (1S-LiPo 3,0–4,2 V, eigene PCB)
**Methodik:** nur `web_search` + `web_extract` + `curl` (kein Browser). **Jeder Preis/jede Lagerangabe stammt direkt von der jeweiligen Shopseite** (Direktabruf am 12.09.2026); Suchsnippets wurden nur zur Auffindung benutzt (§-Angaben unten). JS-/bot-blockierte Seiten sind explizit als „nicht verifiziert" gekennzeichnet.
**Anforderungsprofil:** peristaltisch, ≥100 ml/min (Ziel 60–150), 3,7–6 V (oder 5–6 V), ≤ ~600 mA, kompakt (≈Ø30–35 × 40–70 mm), Schlauch 3×5 mm Silikon, selbstansaugend.

> Kernbefund vorab: **Unter 25 € inkl. Versand liefert derzeit kein deutscher Shop eine verifizierte Peristaltikpumpe, die bei 5–6 V die Ziel-Förderrate (60–150 ml/min) erreicht.** Die beiden günstigsten/geeignetsten Optionen: **Funduino 0–90 ml/min (3–12 V, Schlauch 3×5 mm!, 12,82 € inkl. Versand – mit 12-V-Nominal-Vorbehalt)** und das **Whadda/Velleman WPM447 (6 V, 39 ml/min, 20,13 € inkl. Versand, sofort lieferbar)**. Der perfekte Spec-Match (42project, 6 V, 90 ml/min, 17,44 € inkl. Versand) ist **derzeit nicht vorrätig**.

---

## 1. Verifizierte Treffer (Preis + Versand direkt von Shopseite)

### 1.1 Funduino „Peristaltik-, Schlauch- und Dosierpumpe – 0-90 ml/min, 3-12 V“ — **12,82 € inkl. Versand**
| Feld | Wert |
|---|---|
| Shop | funduinoshop.com (Funduino GmbH) |
| Produkt | Peristaltik-, Schlauch- und Dosierpumpe – 0-90ml/min, 3-12V (Art.-Nr. F23107341) |
| Spannung | 3–12 V (Eigenschaften: min. 3 V / max. 12 V; Beschreibung: „Betriebsspannung 12 V DC … Regelung auf kleinere Spannungen reduziert die Förderrate proportional“) |
| Förderrate | bis 90 ml/min (bei 12 V; bei 5–6 V proportional weniger, **Kennlinie nicht angegeben**) |
| Stromaufnahme | Nennstrom 0,25 A (250 mA) |
| Maße | 60 × 40 × 40 mm (L×B×H), 100 g |
| Schlauch | **Silikon, Innendurchmesser 3 mm / Außendurchmesser 5 mm (3×5 mm)** laut Eigenschaften; Beschreibung nennt zusätzlich Anschlüsse für 6-mm-AD-Schläuche |
| Preis | **7,92 €** (−20 % von 9,90 €), inkl. MwSt. |
| Versand DE | **4,90 €** (Versandkostentabelle Funduino) |
| Lieferzeit | 1–3 Werktage |
| Verfügbarkeit | **55 Stück lagernd** (Stand 12.09.2026) |
| Gesamt | **12,82 €** |
| Link | https://funduinoshop.com/elektronische-module/ventile-pumpen/pumpen/peristaltik-schlauch-und-dosierpumpe-0-90ml/min-3-12v |

### 1.2 Funduino „Peristaltik-, Schlauch- und Dosierpumpe“ — 80 ml/min (Angaben widersprüchlich 5 V/12 V) — **8,82 € inkl. Versand**
| Feld | Wert |
|---|---|
| Shop | funduinoshop.com |
| Produkt | Seitentitel: „80ml/min, 5V“; Artikelname im Shop: „80ml/min, 12V“ (Art.-Verpackung 4×3×4 cm, 0,4 kg) |
| Spannung | **widersprüchlich:** Seitentitel „5 V“, Artikelname „12 V“, Beschreibung „Motor: 12V“ |
| Förderrate | „Pumpleistung: bei 5V ca. 80 ml pro Minute (selbstansaugend), variable Pumpleistung je nach angelegter Spannung“ (Shop-Zitat; physikalisch nicht plausibel bzgl. 12-V-Motor → **nicht plausibilisiert, Shop-Angabe übernommen**) |
| Stromaufnahme | nicht angegeben |
| Maße | nicht angegeben (Verpackung 4×3×4 cm) |
| Schlauch | Silikon (Maße nicht angegeben) |
| Preis | **3,92 €** (−20 % von 4,90 €), inkl. MwSt. |
| Versand DE | 4,90 € |
| Lieferzeit | 1–3 Werktage |
| Verfügbarkeit | **119 Stück lagernd** |
| Gesamt | **8,82 €** |
| Link | https://funduinoshop.com/elektronische-module/ventile-pumpen/pumpen/peristaltik-schlauch-und-dosierpumpe-80ml/min-12v |

### 1.3 Funduino „Peristaltik-, Schlauch- und Dosierpumpe – 60 ml/min, 12 V“ — **8,82 € inkl. Versand** (12 V → für 1S nicht direkt geeignet)
| Feld | Wert |
|---|---|
| Spannung | 12 V DC |
| Förderrate | bis 60 ml/min |
| Stromaufnahme | nicht angegeben |
| Maße | 30 × 40 × 37 mm (B×L×H), 2 Kontakte, Lötanschluss |
| Schlauch | Silikon, ID 3 mm / AD 5 mm (**3×5 mm**) |
| Preis | **3,92 €** (−20 % von 4,90 €) |
| Versand/Lieferzeit | 4,90 € / 1–3 Werktage |
| Verfügbarkeit | **„Noch 1 auf Lager!“** |
| Gesamt | **8,82 €** |
| Link | https://funduinoshop.com/elektronische-module/ventile-pumpen/pumpen/peristaltik-schlauch-und-dosierpumpe-60ml/min-12v |

### 1.4 Whadda/Velleman WPM447 bei **voelkner** — **20,13 € inkl. Versand** ⭐ günstigste sofort lieferbare 6-V-Pumpe
| Feld | Wert |
|---|---|
| Produkt | Whadda WPM447 Mini-Peristaltikpumpe (Art.-Nr. W690972) |
| Spannung | 6 V DC |
| Förderrate | ≥ 39 ml/min |
| Stromaufnahme | nicht separat angegeben; „6 VDC / 5 W“ → **rechnerisch bis ~0,83 A** (über dem 600-mA-Budget bei Volllast) |
| Maße | 65 × 40 mm, 95 g |
| Schlauch | Silikon, 2,0 × 4,0 mm, Lötfahne 3 mm; selbstansaugend, < 40 dB |
| Preis | **14,18 €** inkl. MwSt. (ab 3 Stk. 14,03 €) |
| Versand DE | **5,95 €** (frei ab 150 €) |
| Lieferzeit | 1–2 Tage |
| Verfügbarkeit | **auf Lager** |
| Gesamt | **20,13 €** |
| Link | https://www.voelkner.de/products/5169170/Whadda-WPM447-Mini-Peristaltikpumpe-1-St.-Passend-fuer-Entwicklungskits-Arduino.html |

### 1.5 WPM447 bei **Botland.de** (PL, deutschsprachiger Shop) — **20,89 € inkl. Versand**
| Feld | Wert |
|---|---|
| Spannung | 6 V (6 V / 6 W laut Shop) |
| Förderrate | ≥ 39 ml/min |
| Strom | nicht angegeben (6 W → rechnerisch bis ~1 A) |
| Maße | 65 × 40 mm, 95 g; Schlauch 2×4 mm Silikon |
| Preis | **15,90 €** inkl. MwSt. (netto 13,36 €) |
| Versand DE | ab **4,99 €** (GLS/DHL/Hermes) |
| Lieferzeit | 2–3 Tage (GLS/DHL), 2–4 Tage (Hermes) |
| Verfügbarkeit | **Derzeit auf Lager: 11 Stück** |
| Gesamt | **ab 20,89 €** |
| Link | https://botland.de/pumps/15387-elektrische-peristaltische-pumpe-6v-velleman-wpm447-5410329703073.html |

### 1.6 WPM447 bei **Conrad** — **22,94 € inkl. Versand**
| Feld | Wert |
|---|---|
| Preis | Shopseite zeigt **15,12 € zzgl. MwSt.** (Netto-Ansicht) = **17,99 € inkl. 19 % MwSt. (umgerechnet)** |
| Versand DE | **4,95 €** inkl. MwSt. (Privatkunden), frei ab 100 € brutto |
| Lieferzeit | „Sofort-Lieferung morgen“ |
| Verfügbarkeit | **14 Stück** |
| Gesamt | **22,94 €** (17,99 + 4,95) |
| Link | https://www.conrad.de/de/p/whadda-wpm447-mini-peristaltikpumpe-1-st-passend-fuer-entwicklungskits-arduino-2481910.html |

### 1.7 WPM447 bei **Pollin** — wäre 22,94 €, aber **aktuell nicht lieferbar**
| Feld | Wert |
|---|---|
| Preis | **16,95 €** inkl. MwSt. |
| Versand DE | **5,99 €** (Sparversand 3,99 € für ausgewählte Artikel) |
| Verfügbarkeit | **„aktuell nicht lieferbar“** (Stand 12.09.2026) |
| Lieferzeit | 1–3 Werktage (wenn verfügbar) |
| Link | https://www.pollin.de/p/whadda-mini-schlauchpumpe-6-v-330139 |

### 1.8 **42project.net** – Peristaltikpumpe 6V-DC 5W 90 ml/min — wäre **17,44 €**, aber **nicht vorrätig** ⭐ bester Spec-/Preis-Treffer
| Feld | Wert |
|---|---|
| Spannung | **6 V DC** (exakt im Zielbereich) |
| Förderrate | **90 ml/min** |
| Stromaufnahme | nicht angegeben (5 W bei 6 V → rechnerisch ~0,83 A) |
| Maße | Länge 65 mm (Motor 48,5 mm); Ø nicht angegeben |
| Schlauch | Silikon, 2× Silikon-Schlauchadapter im Lieferumfang; Maß nicht angegeben |
| Preis | **15,99 €** inkl. MwSt. |
| Versand DE | **1,45 €** (Hermes) — günstigster Versand aller Shops |
| Verfügbarkeit | **„Nicht vorrätig“** (Stand 12.09.2026) |
| Gesamt | **17,44 €** (sobald lieferbar) |
| Link | https://42project.net/shop/aktoren-motoren-servos/peristaltikpumpe-6v-dc-5w-90ml-min-dosierpumpe-chemiepumpe-pumpe-silikon/ |

### 1.9 BerryBase: DFRobot Gravity DFR0523 (5–6 V) — **28,45 € inkl. Versand** (über Budget)
| Feld | Wert |
|---|---|
| Spannung | 5–6 V, 5 W |
| Förderrate | ≥ 45 ml/min |
| Stromaufnahme | **max. Dauerstrom 1,8 A**, Spitzenstrom 2,5 A (deutlich über 600-mA-Budget) |
| Maße | 27,4 × 28,7 mm (Pumpenkopf) |
| Schlauch | BPT, ID 2,5 mm / AD 4,5 mm; 1 m Silikonschlauch im Lieferumfang |
| Preis | **23,50 €** inkl. MwSt. |
| Versand DE | 4,95 € (DHL, frei ab 150 €) |
| Lieferzeit / Verfügbarkeit | 1–3 Tage / **Sofort verfügbar · 12 Stück** |
| Gesamt | **28,45 €** |
| Link | https://www.berrybase.de/gravity-digitale-peristaltik-pumpe-fluessigkeitssystem-5w-45ml-min-bpt-schlauch-5-6v |

### 1.10 BerryBase: Adafruit 3910 (5–6 V, 100 ml/min) — **29,45 €** (über Budget, aktuell nicht lieferbar) ⭐ bester Spec-Match
| Feld | Wert |
|---|---|
| Spannung | **5 bis 6 VDC** |
| Förderrate | **bis 100 ml/min** |
| Stromaufnahme | **500 mA** ✓ (unter 600-mA-Budget) |
| Maße | Motor Ø 27,8 mm, Gesamtlänge 66,8 mm; selbstansaugend (½ m) |
| Schlauch | **Silikon, ID 3,5 mm / AD 5 mm (3,5×5 mm)**, ca. 530 mm Gesamtschlauch |
| Preis | **24,50 €** inkl. MwSt. |
| Versand DE | 4,95 € |
| Verfügbarkeit | **„Artikel aktuell nicht lieferbar“** (Stand 12.09.2026; am selben Tag früher noch „Sofort verfügbar · 7 Stück“ → Status instabil, beobachten) |
| Gesamt | 29,45 € (wenn verfügbar) |
| Link | https://www.berrybase.de/adafruit-peristaltische-fluessigkeitspumpe-mit-silikonschlauch-5v-bis-6v-dc |

### 1.11 Weitere verifizierte Peristaltikprodukte (12 V bzw. über Budget) – Kurzliste
| Shop | Produkt | Specs | Preis | Versand | Verfügbarkeit | Link |
|---|---|---|---|---|---|---|
| BerryBase | DFR0523 via Eckstein | 5–6 V, ≥45 ml/min | **36,35 €** | ab 6,50 € | lieferbar, 1–3 Tage | https://eckstein-shop.de/dfrobot-gravity-digital-peristaltic-pump-fluessigkeitspumpenmodul-dfr0523 |
| Botland | DFRobot Gravity „Kabelpumpe – peristaltisch“ (DFR0523) | 5–6 V, ≥45 ml/min | **26,90 €** | ab 4,99 € | nicht ausgelesen | https://botland.de/schwerkraft-aktuatoren/11460-dfrobot-gravity-kabelpumpe-peristaltisch-6959420913251.html |
| BerryBase | Peristaltikpumpe für Flüssigkeiten 12 V (PPFL-1) | 12 V | 9,10 € | 4,95 € | **nicht lieferbar** | https://www.berrybase.de/peristaltikpumpe-fuer-fluessigkeiten-12v |
| BerryBase | NKP-DC-S04B 12 V, Schlauch ø1,0 mm (PPFL-2) | 12 V | 7,90 € | 4,95 € | **nicht lieferbar** | https://www.berrybase.de/peristaltikpumpe-nkp-dc-s04b-fuer-fluessigkeiten-12v-schlauch-oe1-0mm |
| Funduino | Peristaltikpumpe, Dosierpumpe – 12 V, 60–150 ml | 12 V, 60–150 ml/min | 12,52 € (−20 %) | 4,90 € | **ausverkauft** | https://funduinoshop.com/elektronische-module/ventile-pumpen/pumpen/peristaltikpumpe-dosierpumpe-12v-60-150ml |
| Funduino | Peristaltik-/Dosierpumpe 0–500 ml/min, 3–12 V | 3–12 V, bis 500 ml/min | 39,56 € (−20 %) | 4,90 € | lagernd | https://funduinoshop.com/elektronische-module/ventile-pumpen/pumpen/peristaltik-schlauch-und-dosierpumpe-0-500ml/min-3-12v |
| Funduino | Kamoer KCM 12–24 V (Schrittmotor) / KFS-ST 1–65 ml/min / KPAS100 24 V / KPCS200 24 V | über Zielbereich | 40,30–92,98 € | 4,90 € | lagernd | (Kategorie Pumpen) |

**Grenzfall (Typ NICHT durch Shop bestätigt):** Roboter-Bausatz.de „Wasserpumpe 12V DC 0-100 ml/min“ (Art. RBS11471): **6,69 €** (Staffelpreise), Versand **4,45 €**, 1–3 Werktage, sofort verfügbar → Gesamt **11,14 €**. Shoptext/Kategorie („Motorpumpe“) bezeichnen sie **nicht** als Peristaltikpumpe; auf der gesamten Seite kommt das Wort „Peristaltik“ nicht vor (verifiziert). 12 V, 80 mA, 0–100 ml/min, Motor Ø 27,6 × 37,9 mm, Kopf Ø 31,7 × 20,1 mm. **Für 1S nur mit Boost nutzbar; Typ vor Kauf verifizieren.** Link: https://www.roboter-bausatz.de/p/wasserpumpe-12v-dc-0-100-ml-min

---

## 2. Geprüfte Shops ohne (verifizierten) Peristaltik-Treffer

| Shop | Ergebnis | Beleg |
|---|---|---|
| **reichelt.de** | **Kein Peristaltik-/Schlauchpumpen-Sortiment.** Suche „peristaltikpumpe“, „schlauchpumpe“, „wpm447“, „peristaltik“ → je **0 Treffer**; „dosierpumpe“ → 6 Treffer, ausschließlich Kategorie *Schrittmotoren*. Versand ab 5,95 €. | Shopsuche (curl, Direktabruf) |
| **az-delivery.de** | **Kein Peristaltikprodukt.** Shopify-Suche + Suggest-API: „peristaltik“ → 5 Fuzzy-Treffer (Lötstation, Solarpanels …); „dosierpumpe“ → nur Bewässerungs-Sets mit Tauchpumpe (17,91 € / 29,99 €), keine Schlauchpumpe. | Shopsuche + suggest.json |
| **sertronics.de** | Kein Endkundenshop – Serviceunternehmen (Reparatur/IT); betreibt u. a. **BerryBase** („Maker & DIY“) → Peristaltik-Sortiment ist über BerryBase abgedeckt. | https://www.sertronics.de/ |
| **exp-tech.de** | **Nicht verifizierbar:** Produktseiten (Adafruit 3910) antworten mit **404**, Shop-Suche liefert kein Ergebnis. Suchmaschinen-Snippet nennt „€24.00, currently out of stock, back-orderable“ → **nicht von Shopseite bestätigt, daher nicht gewertet.** | curl direkt |
| **eBay.de** | **Nicht verifizierbar:** curl → HTTP 403; Extractor → eBay-Fehlerseite (JS). Snippet der eBay-Kategorie „Peristaltikpumpe“ zeigt ein gewerbliches Angebot **„Peristaltik-, Schlauch- und Dosierpumpe – 0-90ml/min, 3-12V“ für ca. EUR 10,89** → **nur Snippet, kein Seitenbeleg.** | curl 403 / Extractor-Fehler |
| **hausofrabbits.de / .com** | **Nicht auffindbar** (Domain löst nicht auf; Namenssuche findet keinen Elektronik-Shop). | DNS/curl 000 |
| **conrad.de / voelkner.de** | Je nur **1** Peristaltikprodukt (WPM447, s. o.); keine weiteren gefunden. |
| **roboter-bausatz.de** | Keine als „Peristaltikpumpe“ ausgewiesene Pumpe; nur der o. g. 12-V-Grenzfall. |
| **cre.science** | Nur Peristaltikpumpe **24 V** (nicht 1S-tauglich), daher nicht gewertet. |

---

## 3. Rangliste: günstigste sinnvolle Optionen (Gesamtkosten inkl. Versand nach DE)

| # | Option | Preis | Versand | **Gesamt** | Verfügbarkeit | Haken |
|---|---|---|---|---|---|---|
| **1** | **Funduino 0–90 ml/min, 3–12 V** (Silikonschlauch **3×5 mm**, Nennstrom 0,25 A) | 7,92 € | 4,90 € | **12,82 €** | 55 Stk. lagernd, 1–3 Werktage | Beschreibung nennt 12 V nominal → bei 5–6 V deutlich < 90 ml/min; Förderrate bei 6 V nicht spezifiziert |
| **2** | **Whadda WPM447 bei voelkner** (6 V, 39 ml/min) | 14,18 € | 5,95 € | **20,13 €** | sofort lieferbar, 1–2 Tage | nur 39 ml/min (unter Zielrate 60–150); Schlauch 2×4 mm (statt 3×5); rechnerisch bis ~0,83 A bei 5 W |
| **3** | **WPM447 bei Botland.de** (identisch) | 15,90 € | ab 4,99 € | **ab 20,89 €** | Lager 11 Stk., 2–3 Tage | wie oben; Versand aus Polen |
| 4 | WPM447 bei Conrad | 17,99 € (brutto) | 4,95 € | 22,94 € | 14 Stk., „Sofort-Lieferung morgen“ | wie oben; Preis auf Shopseite als Netto (15,12 € + MwSt.) ausgegeben |
| 5 | WPM447 bei Pollin | 16,95 € | 5,99 € | 22,94 € | **nicht lieferbar** | Nicht bestellbar |

**Bestes Spec-Match (außerhalb der Top-3, weil nicht lieferbar bzw. > 25 €):**
- **42project.net, 6 V / 90 ml/min, 3 Rollen — 15,99 € + 1,45 € = 17,44 €** → exakt im Spannungsziel, bester Preis; **derzeit „Nicht vorrätig“** (Restock/Alarm einrichten).
- **Adafruit 3910 bei BerryBase — 24,50 € + 4,95 € = 29,45 €** → 5–6 V, **100 ml/min, 500 mA**, Schlauch **3,5×5 mm**; **aktuell nicht lieferbar** und über Budget.
- **Funduino „80 ml/min“ — 3,92 € + 4,90 € = 8,82 €** → billigste Option, aber Shop-Angaben zu Spannung/Leistung widersprüchlich (5 V/12 V) → vor Kauf klären.

---

## 4. Fazit & Empfehlung

1. **Sofort kaufbar & am besten passend:** **Funduino 0–90 ml/min (12,82 € inkl. Versand)** – einzige <25-€-Option mit **3×5-mm-Silikonschlauch** und niedrigem Nennstrom (0,25 A); Caveat: offiziell 12 V nominal, bei 1S/5 V müsste die niedrigere Förderrate akzeptiert oder ein Boost (5–12 V) vorgesehen werden. Alternative gleichwertig: **WPM447 (6 V) ab 20,13 €** – dafür nur ~39 ml/min und 2×4-mm-Schlauch.
2. **Wenn die Ziel-Förderrate (≥60–100 ml/min bei 6 V) hart ist:** gibt es aktuell **keine** verifizierte <25-€-Option in DE-Shops. Dann entweder **42project (17,44 €) auf Nachlieferung beobachten** (bester Fit), oder Budget auf ~29,45 € erhöhen (Adafruit 3910 – sobald lieferbar), oder die bekannte anodas.lt-Pumpe mit 27-€-Versand in Kauf nehmen.
3. **Nicht verifizierbar/finger weg ohne Prüfung:** eBay-Angebote (ca. 10,89 €, nur Snippet), exp-tech (Seite 404), Roboter-Bausatz-12-V-Pumpe (Typ nicht als Peristaltik ausgewiesen).
4. **Versandkosten-Faustregel (je Bestellung):** 42project 1,45 € · Funduino 4,90 € · BerryBase/RBS 4,95/4,45 € · Conrad 4,95 € · voelkner 5,95 € · reichelt 5,95 € · Pollin 5,99 € · Botland ab 4,99 € · Eckstein ab 6,50 €.

### Versandkosten-/Quellen-Nachweise (Direktabruf 12.09.2026)
- BerryBase: https://www.berrybase.de/versand-und-zahlungsbedingungen/ (DHL 4,95 €; frei ab 150 €)
- Funduino: https://www.funduinoshop.com/versand-und-zahlungsbedingungen (DE 4,90 €)
- voelkner: https://www.voelkner.de/liefermoeglichkeiten.html (5,95 €; frei ab 150 €)
- Conrad: https://support.conrad.de/hc/de/articles/42664563928337-Versandkosten (B2C 4,95 € inkl. MwSt.; frei ab 100 €)
- Pollin: https://www.pollin.de/media/c6/a5/7b/1745828510/versand-und-bezahlen-04-25.pdf (5,99 €; Sparversand 3,99 €)
- 42project: https://42project.net/versand__lieferung/ (1,45 €, Hermes)
- Botland: https://botland.de/content/1-versandkosten (GLS/DHL/Hermes ab 4,99 €; frei ab 100 €)
- Roboter-Bausatz: https://www.roboter-bausatz.de/c/information/versand-und-zahlung/ (4,45 € DHL; frei ab 99 €)
- Eckstein: https://eckstein-shop.de/Versandinformationen (DHL/DPD ab 6,50 €)

### Rohdaten
Alle abgerufenen HTML-/Text-Stände liegen unter `research/bom-check/raw/` (Dateinamen = Shop-Token, z. B. `pollin_wpm447.html`, `fu_090_de.html`, `botland_wpm447.html`).
