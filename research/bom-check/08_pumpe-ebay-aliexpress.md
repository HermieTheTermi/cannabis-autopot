# 08 — Peristaltikpumpe 3,7–6 V: eBay.de & AliExpress (nur EU-Lager)

**Projekt:** cannabis-autopot · selbstbewässernder Topf, Akkubetrieb (1S-LiPo 3,0–4,2 V)
**Anforderung:** peristaltisch/Schlauchpumpe · 3,7–6 V DC · Förderrate ≥ 100 ml/min · Strom ≤ ~600 mA · kompakt (Ø 30–35 mm, L 40–70 mm) · Schlauchanschluss 3×5 mm Silikon · selbstansaugend
**Referenzprodukt:** OEM ABC-12527 (3,7–6 V, 6 V/540 mA, 1 L in 4 min) — 7,74 € bei anodas.lt, aber derzeit nur mit 27 € Versand
**Stand:** 12.09.2026, ~13:00 CEST · Alle Preise/Links am 12.09. live abgerufen

> ⚠️ **Methodik:** Kein Browser. eBay.de per curl (Cookie-Handshake; Item-Seiten + Beschreibungen via itm.ebaydesc.com). AliExpress per SEO-Server-Rendering (Googlebot-UA) inkl. Lagerfilter `shipFromCountry=CZ/PL/ES/DE` (Filterwert muss GROSS geschrieben werden, sonst 0 Treffer). eBay-Itemseiten liefern Preise/Versand/Standort/Lieferdatum als strukturiertes JSON (verifiziert); AliExpress-Produktdetailseiten (PDP) waren nur JS-Shells → Detail-Specs dort **NICHT VERIFIZIERT** (Suchkarten-Daten = Momentaufnahme).

---

## 1. eBay.de — verifizierte Angebote (Artikelstandort DE/EU, Sofort-Kauf, inkl. Versand nach DE)

### 1.1 🥇 Funduino GmbH — 0–90 ml/min, 3–12 V — **13,61 € inkl. Versand** (günstigster EU-Treffer)
| Feld | Wert |
|---|---|
| **Link** | https://www.ebay.de/itm/165380385274 |
| **Händler** | Funduino GmbH (funduino_de), gewerblich, 99,8 % positiv, ~31.400 Bewertungen |
| **Preis** | **8,71 €** (verifiziert) |
| **Versand** | **4,90 €** (Deutsche Post Warenpost, DE) → **Gesamt 13,61 €**; Abholstation möglich |
| **Lieferung** | **Di, 15.09. – Mi, 16.09.2026** (2–3 Tage, bei Zahlung heute) |
| **Standort** | **Nordhorn, Deutschland** (verifiziert) |
| **Spannung** | **3–12 V** (bei 6 V lauffähig) |
| **Förderrate** | 0–90 ml/min (90 ml/min bei 12 V); bei 6 V ca. **45 ml/min — lineare Schätzung, NICHT VERIFIZIERT** |
| **Maße** | ca. 60 × 40 × 40 mm (L×B×H) |
| **Schlauch** | Silikon 2,5×4,7 mm **und 3×5 mm**, beidseitig bereits montiert |
| **Sonstiges** | selbstansaugend, Motor 5000 U/min @12 V, Pumpenkopf werkzeuglos abnehmbar, Strömungsrichtung per Polung; Stromaufnahme **nicht angegeben** (NICHT VERIFIZIERT) |

*Bewertung:* Bester verifizierter Gesamttreffer < 20 € aus DE mit 2–3 Tagen Lieferzeit. Erfüllt 6-V-Betrieb und 3×5-mm-Schlauch, verfehlt aber das 100-ml/min-Ziel bei 6 V (bei 12 V wären 90 ml/min erreichbar — inkompatibel mit 1S-Akku).

### 1.2 🥈 outdooler01 — 6-V-Miniatur-Peristaltikpumpe — **21,59 € inkl. Versand** (über Budget, aber echte 6 V)
| Feld | Wert |
|---|---|
| **Link** | https://www.ebay.de/itm/278338751399 |
| **Händler** | outdooler01 (gewerblich, 100 % positiv, 38.192 verkauft, Shop seit 2017) |
| **Preis** | **21,59 €** (verifiziert; Suchkarte zeigt teils 20,51 € — Dynamikpreis) |
| **Versand** | **kostenlos** („Kostenloser Versand" nach DE) → **Gesamt 21,59 €** |
| **Lieferung** | **Do, 17.09. – Mi, 23.09.2026** |
| **Standort** | laut eBay-Itemseite **Hamburg, Germany, Deutschland** ⚠️ Verkäufer-Kontaktadresse ist eine **Shenzhen-Firma (CN)** → echtes Versandlager nicht sicher, NICHT VERIFIZIERT |
| **Spannung** | **6 V** (Beschreibung) |
| **Förderrate** | **0,1–100 ml/min** (Beschreibung), Drehzahl 0,1–100 U/min |
| **Maße** | Antrieb Ø27,6 × 37,9 mm; Pumpenkopf Ø31,7 × 20,1 mm; 88 g |
| **Schlauch** | 2,5 × 4,7 mm (ID×AD) — **nicht** 3×5 mm |
| **Sonstiges** | zusammenschraubbarer, reinigungsfähiger Kopf; Förderrichtung per Polung; 0–40 °C |

*Bewertung:* Einziges verifiziertes 6-V-Angebot mit DE-Artikelstandort und bis zu 100 ml/min — aber 21,59 € (über dem 20-€-Ziel), langsamerer Versand und 2,5×4,7-mm-Schlauch statt 3×5 mm.

### 1.3 Weitere geprüfte eBay-Treffer (ausgeschlossen — falsche Spannung / kein Peristaltik)
| Item | Produkt | Preis + Versand | Standort | Warum ausgeschlossen |
|---|---|---|---|---|
| [326375607292](https://www.ebay.de/itm/326375607292) (auch …287) | KAMOER NKP-DC-B10B Peristaltikpumpe, WITTKO GmbH | 9,99 € + 3,99 € = **13,98 €** | Riedenburg, DE | **12 V / 5 W, 80 ml/min** → nicht 1S-tauglich |
| [377131861654](https://www.ebay.de/itm/377131861654) | „Mikroperistaltische Pumpe" (Titel ohne Spannung!), basalkh62 | 14,50 € + 3,00 € = 17,50 € | Regensburg, DE | Beschreibung: **24 V DC**, Schlauch 2×4 mm → ungeeignet |
| [820048512108](https://www.ebay.de/itm/820048512108) | „Mini Peristaltic Pump DC12V", SaamDE | 19,99 € + 3,99 € = 23,98 € | Calmuth, DE | **12 V** |
| [357183796836](https://www.ebay.de/itm/357183796836) | „Mini Peristaltic Pump DC12V" | 23,99 € inkl. | **Paris, Frankreich** (EU) | **12 V** |
| [204311156181](https://www.ebay.de/itm/204311156181) | „Mini Luftpumpe Vakuumpumpe 3,7/6,0/12 V", fimobau2014 | 6,95 € + 3,15 € = 10,10 € | Laudenbach, DE | **keine Peristaltik** (Luft-/Vakuumpumpe) |
| [125739922986](https://www.ebay.de/itm/125739922986) | „12V/24V – 2,4 l/h (40 ml/min) Schlauchpumpe" | 9,50 € (+ Versand) | DE | **12/24 V** und nur 40 ml/min |

### 1.4 eBay.de, aber Artikelstandort China (nicht compliant — nur zur Info, günstigste 6-V-Peristaltikpumpen im Sortiment)
| Item | Produkt | Preis | Versand | Standort |
|---|---|---|---|---|
| [206220906827](https://www.ebay.de/itm/206220906827) | „1 Stück Mikro-Peristaltik-Pumpe DC 5V 6V 500" | 5,88 € | + 5,15 € | aus China |
| [407076283803](https://www.ebay.de/itm/407076283803) | dto. | 6,60 € | + 4,75 € | aus China |
| [287502035479](https://www.ebay.de/itm/287502035479) | dto. | 11,33 € | gratis | aus China |
| [366526401528](https://www.ebay.de/itm/366526401528) | „6V DC-Dosierpumpe Mini-Peristaltik-Dosierkopf" | 19,10 € | gratis | aus China |
| [298442114122](https://www.ebay.de/itm/298442114122) / [318490404810](https://www.ebay.de/itm/318490404810) | dto. (selbstansaugend) | 20,08 € / 20,09 € | gratis | aus China |

*Suche nach dem Referenzmodell: „ABC-12527" liefert auf eBay.de **0 relevante Treffer** (nur Fremdprodukte „ABC Design" etc., verifiziert 12.09.).*

---

## 2. AliExpress — nur Händler mit Versand aus EU-Lager (shipFromCountry-Filter)

**Vorgehen:** Lokalisierte Suche (de.aliexpress.com, €-Preise) mit Lagerfilter für **CZ, PL, ES, DE** über Suchbegriffe „peristaltikpumpe", „peristaltic pump", „schlauchpumpe", „dosierpumpe". EU-Lager-Artikel tragen auf der Suchkarte den Badge `localplus_flag_eu`.

**Ergebnis pro Lager:**
| Lager | Treffer | Relevante 3,7–6-V-Peristaltikpumpe? |
|---|---|---|
| **PL (Polen)** | „peristaltic pump": 13 Treffer | ✅ **2 Kandidaten** (s. u.) |
| **DE (Deutschland)** | „peristaltikpumpe"/„peristaltic pump": 11 Treffer; „dosierpumpe": 27 Treffer | ❌ keine (Membran-/Auto-/Gartentechnik, Werkzeuge, Dünger-Dosierer) |
| **CZ (Tschechien)** | „peristaltikpumpe 6v": **0 Treffer** („Keine Suchergebnisse"); „peristaltic pump": 1 irrelevanter; „dosierpumpe": 2 irrelevante | ❌ keine |
| **ES (Spanien)** | „peristaltic pump": **0 Treffer** | ❌ keine |

### 2.1 ✅ Kandidat PL-Lager: Mikro-Peristaltikpumpe DC 6V/9V/12V — **24,59 €**
| Feld | Wert |
|---|---|
| **Link** | https://de.aliexpress.com/item/1005012377170304.html |
| **Produktname** | „Mikro-Peristaltikpumpe DC 6V 9V 12V Kleiner Mini-500-Getriebemotor zur Flüssigkeitsdosierung, umkehrbar, für Labor-Tintenprobenentnahme" |
| **Preis** | **24,59 €** (Suchkarten-Momentaufnahme, inkl. MwSt.) |
| **Versand** | **kostenlos** → Gesamt 24,59 € |
| **Lagerort** | **EU-Lager (pl-PL, Badge `localplus_flag_eu`)** — konkreter Standort PL liegt nahe, NICHT einzeln verifiziert |
| **Verfügbarkeit** | „Frühbucherangebot, nur noch 3 übrig", 2 verkauft, 5,0 ★ |
| **Spannung** | DC 6 V / 9 V / 12 V (SKU-Varianten) |
| **Förderrate / Maße / Schlauch / Strom** | **NICHT VERIFIZIERT** — Produktseite nur per JS ladbar (kein Browser erlaubt); 500er-Getriebemotor-Familie, typisch eher 30–60 ml/min → für 100 ml/min zweifelhaft |
| **Lieferzeit** | NICHT VERIFIZIERT (PL→DE typisch 3–7 Tage, nicht belegt) |

### 2.2 🟡 Kandidat PL-Lager (unklar): „Aquarien-Peristaltikpumpe 2–30 mm Silikon-Gummischlauch" — 14,29 €
| Feld | Wert |
|---|---|
| **Link** | https://de.aliexpress.com/item/1005012086933036.html |
| **Preis** | **14,29 €**, kostenloser Versand, „nur noch 1 übrig", EU-Lager-Badge |
| **Status** | ⚠️ **NICHT VERIFIZIERT, ob Pumpe oder nur Schlauchmaterial** — Titel („maßgefertigter Silikon-Gummischlauch 2–30 mm Außendurchmesser") deutet eher auf Zubehür/Schlauchzuschnitt hin |

### 2.3 AliExpress: günstigste 6-V-Peristaltikpumpen — aber **alle aus China** (nicht compliant)
Bei der Suche „peristaltikpumpe 6v" (60 Suchkarten, ohne Lagerfilter) war bei **60/60 Artikeln der Standard-Variante `shipFrom=CN`** — d. h. kein EU-Lager. Preise daher nur als Referenz (Suchkarten-Momentaufnahme, Versand aus CN, Lieferzeit ungeprüft):
- **1005011738131460** — „280 Peristaltische Pumpe DC 3V-6V, 70–130 ml/min, 4 mm Schlauch, umkehrbar" — **8,29 €** — bester Spec-Match (≥100 ml/min im oberen Bereich), aber CN
  https://de.aliexpress.com/item/1005011738131460.html
- 1005012796617760 — „DC 5V 6V 500 Mikro-Peristaltikpumpe" — 2,65 €
- 1005012129947283 — „M20/N20 Mini-Getriebe-Mikro-Peristaltikpumpe 3V/3,7V/5V" — 3,39 €
- 1005012036594102 — „DC 3,7V 5V 6V Mikro-Peristaltikpumpe Mini 500" — 4,12 €
- 1005011881439504 — „DC 5V 6V 500 Metallbürsten-Getriebemotor Mikro-Peristaltikpumpe" — 4,29 €
- 1005011848394007 — „SKOOCOM SC2201RPM Mini 130 Peristaltikpumpe DC 3V/3,7V/5V/6V" — 4,35 €
- 1005007455494610 — „Kamoer KPA30 6V, 30 ml/min" — 4,99 € (Förderrate zu niedrig)
- 1005013086016597 — „P310 DC 6V, 4 Stück selbstansaugend" — 12,59 €

---

## 3. Rangliste (Gesamtkosten inkl. Versand nach DE, bestellbar am 12.09.2026)

| Rang | Angebot | Gesamt | Lieferzeit | Bewertung |
|---|---|---|---|---|
| 🥇 | **eBay: Funduino 0–90 ml/min, 3–12 V** | **13,61 €** | **2–3 Tage (15.–16.09.)** | Günstigste verifizierte EU-Quelle; 3–12 V & 3×5 mm Schlauch ✓, aber ≥100 ml/min bei 6 V unwahrscheinlich (~45 ml/min, geschätzt) |
| 🥈 | **eBay: outdooler01 6-V-Miniaturpumpe** | **21,59 €** | 4–10 Tage (17.–23.09.) | Einzige verifizierte 6-V/DE-Lager-Option, bis 100 ml/min; über 20-€-Ziel, Schlauch 2,5×4,7 mm; Lagerort Hamburg vs. CN-Kontaktadresse unklar |
| 🥉 | **AliExpress PL-Lager: Mikro-Peristaltikpumpe 6/9/12 V** | **24,59 €** | n. v. | Echtes EU-Lager (Badge) + Gratisversand; Specs (Flow/Maße) nicht verifizierbar; über Budget |
| – | (Ausschluss) eBay: Kamoer NKP-DC-B10B 12 V | 13,98 € | 2–3 Tage | Günstigste EU-Peristaltikpumpe überhaupt, aber **12 V** |

**Fazit:** Kein Angebot erfüllt gleichzeitig 3,7–6 V **und** ≥100 ml/min **und** ≤20 € **und** EU-Lager. Der beste belegte Kompromiss unter 20 € bleibt die **Funduino-Pumpe (13,61 €, DE, 2–3 Tage)**; wer strikt 6 V + bis 100 ml/min braucht, zahlt 21,59 € (outdooler01) oder 24,59 € (AliExpress PL). Die vermutlich passendste Pumpe (280er, 3–6 V, 70–130 ml/min, ~8 – 9 €) gibt es nur mit CN-Versand (AliExpress/eBay-CN-Händler) — ohne EU-Lager.

---

## 4. Explizit NICHT VERIFIZIERT
- **AliExpress PL:** Förderrate, Maße, Schlauchmaß, Stromaufnahme, tatsächliche Versanddauer des 24,59-€-Artikels (PDP nur JS-rendering). Ebenso: ob 1005012086933036 eine Pumpe oder nur Silikonschlauch ist.
- **Funduino:** Stromaufnahme bei 6 V (nicht angegeben); Förderrate @6 V nur lineare Schätzung aus 90 ml/min @12 V.
- **outdooler01:** echtes Versandlager (eBay=Hamburg vs. Kontaktadresse Shenzhen); tatsächliche Lieferzeit.
- **eBay-CN-Artikel (1.4):** dortige Förderraten/Abmessungen wurden nicht einzeln geprüft (nur gelistet, weil Standort China = nicht compliant).
- **Preise/Momentaufnahme:** Alle Preise vom 12.09.2026; eBay-Aktionen/Early-Bird-Rabatte („Frühbucherangebot") können sich ändern. AliExpress-Preise inkl. MwSt., Suchkarten-Werte.

## 5. Quellen-Status
- eBay.de: 6 Suchqueries (DE- und EU-Filter `LH_PrefLoc=1/3`, Sofort-Kauf, Sortierung Preis+Versand); Item-Seiten von 10+ Kandidaten per curl geladen → Preis/Versand/Standort/Lieferdatum aus Item-Page-JSON; 4 Produktbeschreibungen via itm.ebaydesc.com (Funduino, basalkh62, outdooler01 ×2) — alle verifiziert.
- AliExpress: 12+ Suchabfragen mit `shipFromCountry=CZ/PL/ES/DE` (Großbuchstaben!) via SEO-Render; Itemlisten-JSON ausgewertet (localplus-EU-Badge, Preise, Bestände). Produktdetailseiten nicht auslesbar (JS-Shell) → als nicht verifiziert markiert. AliExpress hat zwischenzeitlich Anti-Bot-Seiten (x5secdata) ausgeliefert; Ergebnisse daher Momentaufnahmen.
