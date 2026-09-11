# BOM-Check 03: Bodenfeuchte-Sensor v1.2 + Kleinteile

**Projekt:** cannabis-autopot | **Datum:** 2026-09-11 | **Recherche:** Hermes Subagent (Web, Live-Abruf der Shopseiten)

**Legende:**
- ✅ **VERIFIZIERT** — Preis/Status direkt von der Shopseite gelesen
- ⚠️ **TEILWEISE VERIFIZIERT** — Preis/Status nur auf Such-/Listenansicht gesehen, Produktseite nicht geöffnet
- ❌ **NICHT VERIFIZIERT** — kein belastbarer Beleg in dieser Recherche (bitte vor Kauf prüfen)

---

## A) Kapazitiver Bodenfeuchte-Sensor v1.2 (LDO, analog)

### A1) AZ-Delivery v1.2 — Preis- und Datencheck

- **Preis:** 4,99 € ✅ (Bestätigt auf Produktseite 11.09.2026)
- **Link:** https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2
- **Abmessungen (Herstellerangabe):** **22 × 97 × 9 mm**, 3-adriges Kabel 190 mm, Schnittstelle PH2.0-3P, Betriebsspannung 5 V ✅
- **Lieferung:** Versand aus Deutschland; versandkostenfrei ab 25 € (Shop-Banner). ⚠️ Aktueller Hinweis auf der Seite: „Aufgrund des aktuellen hohen Bestellaufkommens kann es zu leichten Versandverzögerungen kommen." Exakte Lieferzeit nicht angegeben.
- **LDO-Regler explizit ausgewiesen?** ❌ NICHT VERIFIZIERT — die Produktbeschreibung nennt nur „integrierter Verstärker", nicht explizit den LDO-Typ. Die v1.2-Boards mit AMS1117-LDO gelten projektintern als geprüfte Empfehlung; ob genau das AZ-Board die LDO-Variante ist, auf dem Foto prüfen (Bestückung oben links neben dem 3-Pin-Stecker).

### A2) Abmessungen / Einstecktiefe — kritisch für 85 mm Einbau

- Gesamtlänge 97 mm, davon 9 mm Dicke (inkl. Stecker/Bauteile). Bei **85 mm Einstecktiefe** verbleiben ca. **12 mm über dem Boden** — die JST-PH-Buchse und das Kabel bleiben erreichbar. ✅ (Ableitung aus Herstellerangabe)
- **Länge des Elektrodenbereichs:** ❌ **NICHT VERIFIZIERT.** Keine belastbare Quelle in dieser Recherche gefunden. Bekannt (nicht verifiziert): Beim v1.2-Board sitzen Oszillator + LDO im oberen Drittel, die Messelektroden im unteren Bereich der Platine. **Vor dem finalen Design das reale Board vermessen** — relevant, weil bei 85 mm Einstecktiefe sichergestellt sein muss, dass die Elektroden vollständig in der Erde liegen und die Elektronik nicht dauerhaft im Nassen sitzt.

### A3) Weitere Quellen für den Sensor

| Quelle | Produkt | Preis | Verfügbarkeit | Link | Status |
|---|---|---|---|---|---|
| DigiKey DE | DFRobot **SEN0193** (Gravity, kapazitiv, korrosionsfest) | **6,01 € brutto** (5,05 € netto) | **237 Stück auf Lager** | https://www.digikey.de/de/products/detail/dfrobot/SEN0193/6588605 | ✅ |
| BerryBase | DFRobot kapazitiver Bodenfeuchtigkeitssensor (3-Pin, analog) | — | laut Shopseite **derzeit nicht verfügbar** | https://berrybase.de/en/dfrobot-capacitive-soil-moisture-sensor-3-pin-analogue-output-corrosion-resistant-3.3-5.5v | ⚠️ (Status aus Suche, Preis ❌) |
| Reichelt | SEEED kapazitiver Bodenfeuchtesensor | **5,99 €** | **nicht lieferbar** („Nachricht bei Verfügbarkeit") | https://www.reichelt.de/de/de/shop/produkt/arduino_-_feuchtigkeitssensor_boden_korrosionsbestaendig_-369415 | ✅ Preis+Status |
| Amazon.de | DFRobot Gravity kapazitiv (SEN0193) | ❌ NICHT VERIFIZIERT | unbekannt | https://www.amazon.de/DFRobot-Gravity-Kapazitive-Feuchtigkeit-korrosionsbest%C3%A4ndig/dp/B01GHY0N4K | ❌ |
| Chipglobe | — | ❌ | Seite lieferte bei Abruf keine Daten | — | ❌ |
| Farnell | SEN0193 | ❌ (nicht geprüft, Zeitbudget) | — | — | ❌ |
| Amazon | **Aideepen 6er-Pack V1.2 kapazitiv** | 8,99 € behauptet → ❌ NICHT VERIFIZIERT | Listing gefunden (ASIN **B08GCRZVSR**, „Aideepen 6 Pcs V1.2 Capacitive Hygrometer Module") | https://www.amazon.com.be/-/en/Aideepen-Capacitive-Hygrometer-Corrosion-Resistant/dp/B08GCRZVSR (DE-Variante: amazon.de/dp/B08GCRZVSR — ❌ nicht getestet, Amazon blockt Abruf) | ❌ Preis |

**Fazit A:** Günstigste verifizierte Option für das Projekt bleibt **AZ-Delivery v1.2 für 4,99 €** (DE-Versand). DFRobot SEN0193 bei DigiKey ist die verifizierte „Marken"-Alternative (6,01 € brutto, 237 auf Lager). Reichelt/BerryBase führen den kapazitiven Sensor aktuell nicht lieferbar. Das Aideepen-6er-Pack wäre pro Stück günstiger (~1,50 €/St bei 8,99 €), Preis aber nicht verifiziert — Amazon-Listing prüfen.

---

## B) Kleinteile für die eigene Platine

### B1) Logic-Level N-Kanal-MOSFET

| Teil | Bauform | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| **AO3400A** (AOS) bei Reichelt | SOT-23 | 10 St | **0,167 €/St ab 10 St → 1,67 €** (Einzel: 0,18 €). Ab Lager, **Lieferzeit 1–2 Werktage** | https://www.reichelt.de/de/de/shop/produkt/mosfet_n-ch_30v_5_7a_0_018r_sot-23-166490 | ✅ |
| AO3400A bei LCSC (C20917, AOS) | SOT-23 | 10 St | **$0,0853/St @5+** → 10 St ≈ **$0,85** (≈ 0,78 € netto, USD-Liste) | https://www.lcsc.com/product-detail/C20917.html | ✅ (USD) |
| IRLZ44N bei Reichelt | TO-220 | 1–10 St | ⚠️ ~**0,67–0,70 €/St** (Suchseite, 1 Treffer; Produktseite nicht geöffnet) | https://www.reichelt.de/de/de/shop/suche/irlz44n | ⚠️ |
| IRLML6344 | SOT-23 | — | ❌ NICHT VERIFIZIERT | — | ❌ |

### B2) Schottky-Freilaufdiode

| Teil | Bauform | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| **1N5819** bei Reichelt | DO-41 | 10 St | ab **0,10 €/St** (ab Lager, Lieferzeit 1–2 Werktage; ab 100 St 0,08 €/St) → 10 St ≈ **1,00 €**. Hinweis: 4 Treffer, günstigster Artikel nicht eindeutig zugeordnet | https://www.reichelt.de/de/de/shop/suche/1n5819 | ⚠️ |
| **SS14** bei LCSC (C2480, MDD) | SMA (DO-214AC) | 10 St | **$0,0181/St** → 10 St ≈ **$0,18** | https://www.lcsc.com/product-detail/C2480.html | ✅ (USD) |

### B3) Widerstände (0402/0603)

| Teil | Bauform | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| 10 kΩ, UNI-ROYAL 0603WAF1002T5E | 0603 | 100 St (MOQ-Tier) | **$0,0022/St @100+** → 100 St ≈ **$0,22** | https://www.lcsc.com/product-detail/C25804.html | ✅ (USD) |
| 220 Ω | 0603 | — | ❌ NICHT VERIFIZIERT (LCSC-Suchseite rendert nicht; gleiche Preisklasse wie 10 kΩ zu erwarten, aber nicht belegt) | — | ❌ |
| Widerstände bei Reichelt (DE-Quelle) | 0603 | — | ❌ Preise nicht verifiziert; Kategorie: https://www.reichelt.de/de/de/shop/kategorie/widerstandssortimente-9088 | — | ❌ |

### B4) Kondensatoren

| Teil | Bauform | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| 100 nF, Samsung CL10B104KB8NNNC | 0603 | **MOQ 100 St** | **$0,016/St @100+** → 100 St ≈ **$1,60**; In Stock ~2,7 Mio. | https://www.lcsc.com/product-detail/C1591.html | ✅ (USD) |
| 10 µF, Samsung CL21A106KAYNNNE | 0805 | 20 St (MOQ-Tier) | **$0,0871/St @20+** → 20 St ≈ **$1,74**; In Stock ~2,4 Mio. | https://www.lcsc.com/product-detail/C15850.html | ✅ (USD) |
| 100 µF Elko (SMD) | — | — | ❌ NICHT VERIFIZIERT | — | ❌ |

### B5) Steckverbinder

| Teil | Bauform | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| **JST-XH 2,54 Buchse 3-polig (gerade)** bei Funduino | XH 2.54 | 10 St | **0,30 €/St → 3,00 €**, Lieferzeit 1–3 Werktage | https://funduinoshop.com/bauelemente/kabel/kabeltypen/jst-system/3p-jst-xh-2-54-mm-buchse-3-polig-gerade | ✅ |
| **JST-PH 2.0 2-polig**, Amazon 20er-Set (Stecker+Buchse+Kabel) | PH 2.0 | 20 Sets | ❌ Preis NICHT VERIFIZIERT (Amazon blockt Abruf) | https://www.amazon.de/St%C3%BCck-Stecker-Schwarz-Silikon-Buchse/dp/B07449V33P | ❌ |
| Alternativ JST-PH/XH bei LCSC (BOOMELE) | — | — | ❌ nicht einzeln geprüft | https://www.lcsc.com | ❌ |

### B6) Silikonschlauch (Ansaugschlauch Pumpe)

| Teil | Spec | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| Silikonschlauch 3×5 mm, lebensmittelecht | 3 mm ID / 5 mm AD | 1 m | **AUSVERKAUFT** („derzeit leider ausverkauft") — kein Preis | https://funduinoshop.com/werkstatt/schlaeuche-und-zubehoer/schlaeuche/meterware-silikonschlauch-3x5-5mm-aussendurchmesser-lebensmittelecht | ✅ Status |
| Alternative 3×5/4×6 mm Quellen (Lindemann Silikon etc.) | — | 1 m | ❌ NICHT VERIFIZIERT | — | ❌ |

### B7) Schlauchgewicht / Ansaugfilter (optional)

| Teil | Spec | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| Edelstahl Filter Guard (Aquasabi) | für 10/13/17 mm Glas | 1 | ❌ Preis NICHT VERIFIZIERT | https://www.aquasabi.de/Stainless-Steel-Filter-Guard | ❌ |
| Filter Guard Edelstahl (Garnelio) | 12/16 mm | 1 | ❌ Preis NICHT VERIFIZIERT | https://www.garnelio.de/filter-guard-garnelen-edelstahl-ansaugschutz?number=6090 | ❌ |

### B8) Taster (Reset/Boot) + Pin-Header

| Teil | Spec | Menge | Preis | Link | Status |
|---|---|---|---|---|---|
| Mikro-Taster Set (HeyNana, 10er-Pack Miniatur-Taster) | THT/SMD? | 10 St | ❌ Preis NICHT VERIFIZIERT (Amazon blockt Abruf) | https://www.amazon.de/HeyNana-10er-Pack-Miniatur-Mikro-Taster-Tastschalter-Qualit%C3%A4tsschalter-Miniature/dp/B09B45KLW9 | ❌ |
| 2-Pin-Header | 2,54 mm | — | ❌ NICHT VERIFIZIERT | — | ❌ |

---

## C) Günstigere Gesamtquelle für die SMD-Bestückung (LCSC / JLCPCB)

**Hinweis:** Relevant, sobald die Platine bei JLCPCB bestückt wird (PCBA) — LCSC ist der JLCPCB-Schwester-Distributor, Bauteile können direkt in die JLC-BOM (LCSC-Codes) übernommen werden. Versand aus China, Preise in USD, MOQ-Tiers beachten.

Verifizierte LCSC-Preise (11.09.2026):

| Teil | LCSC-Code | Preis (Tier) | 10-100 St |
|---|---|---|---|
| AO3400A (AOS), SOT-23 | C20917 | $0,0853 @5+ / $0,0683 @50+ | ≈ $0,85 für 10 |
| SS14 (MDD), SMA | C2480 | $0,0181 | ≈ $0,18 für 10 |
| 10 kΩ 0603 (UNI-ROYAL) | C25804 | $0,0022 @100+ | ≈ $0,22 für 100 |
| 100 nF 0603 (Samsung) | C1591 | $0,016 @100+ (MOQ 100) | $1,60 für 100 |
| 10 µF 0805 (Samsung) | C15850 | $0,0871 @20+ | $1,74 für 20 |

→ Für die eigentliche PCBA deutlich günstiger als Einzelkauf in DE; für Handlöten-Prototypen lohnt sich der China-Versand aber erst ab größeren Mengen. 100 µF Elko, JST-Connectors und Widerstand 220 Ω bei LCSC ebenfalls in Cent-Beträgen erhältlich, in dieser Recherche aber **nicht einzeln verifiziert**. ❌

---

## Gesamtsummen (nur verifizierte/teilverifizierte Posten, DE-Quellen)

| Posten | Summe | Status |
|---|---|---|
| AO3400A, 10 St (Reichelt) | 1,67 € | ✅ |
| 1N5819, 10 St (Reichelt, 0,10 €/St) | ≈ 1,00 € | ⚠️ |
| JST-XH 3P Buchse, 10 St (Funduino) | 3,00 € | ✅ |
| **Summe verifiziert/teilverifiziert** | **≈ 5,67 €** | — |
| Sensor AZ-Delivery v1.2 (separat, Posten A) | 4,99 € | ✅ |

**Offen (Preise noch zu verifizieren):** JST-PH 2-pol, Taster + Header, Widerstände/Kondensatoren aus DE-Quellen, Silikonschlauch, Schlauchgewicht. Eine belastbare Gesamtsumme + Sensor ist daher erst nach Nachtrag dieser Posten möglich — genehmigte, belegte Teilsumme siehe oben.

---

## Wichtige Prüfhinweise vor Bestellung

1. **Elektrodenlänge des v1.2 messen** (nicht verifiziert) — entscheidend für 85 mm Einstecktiefe.
2. **LDO-Bestückung am AZ-Board auf Foto prüfen** (nicht aus Beschreibung ersichtlich).
3. **Aideepen-6er-Pack (B08GCRZVSR) nur bei verifiziertem Preis und DE-Versand** kaufen — Listing auf amazon.de prüfen; die 8,99-€-Angabe stammt nicht aus dieser Recherche.
4. Amazon blockiert automatisierte Abrufe — Amazon-Preise bitte manuell im Browser prüfen (alle Amazon-Positionen oben sind deshalb ❌).
