# BOM-Check 01 — Seeed Studio XIAO ESP32-C6 (+ Alternative XIAO ESP32-C3)

- Projekt: cannabis-autopot (Eigenbau-PCB, Akkubetrieb, LiPo)
- Stand: 2026-09-11 (Freitag), Momentaufnahme — Preise/Lager können sich täglich ändern
- Methodik: Jede Produktseite wurde am 11.09.2026 per HTTP-Abruf (curl, Browser-User-Agent) und/oder web_extract geprüft. Nicht prüfbare Angaben sind als **NICHT VERIFIZIERT** markiert. Keine erfundenen Preise/Links.

---

## 1. Board-Spezifikationen (projekt-relevant)

| Merkmal | XIAO ESP32-C6 | XIAO ESP32-C3 |
|---|---|---|
| Abmessungen | 21 × 17,8 mm (Seeed Wiki) | 21 × 17,8 mm (Seeed Wiki, Stand heute) |
| Pins | XIAO-Standard: 14 Pins (7 je Seite), castellated → direkt auf eigene PCB auflötbar. („14 Pins" = XIAO-Serien-Standard; auf der Wiki-Seite nur als Pinout-Diagramm, nicht als Textzeile — Grafik vor PCB-Fertigung gegenprüfen) | dito (gleicher Footprint) |
| GPIO | 11 nutzbare GPIO (D0–D10), WiFi 6 / BLE 5.3 / Zigbee / Thread, 512 KB SRAM, 4 MB Flash, RISC-V 160 MHz | 11 GPIO (D0–D10), WiFi / BLE 5.0, 400 KB SRAM, 4 MB Flash, RISC-V 160 MHz |
| LiPo-Ladepads | JA — „Battery Usage"-Abschnitt im Hersteller-Wiki verifiziert (3,7-V-Li-Ion-Akku anlöten, rote Lade-LED, USB Type-C zum Laden). BAT+ / BAT- Lötpads auf der Board-Rückseite (Beschriftung nicht per Textabruf verifiziert, XIAO-Standard) | JA — eigenes „Battery Usage"-Kapitel im Wiki verifiziert |
| USB-C | An der Board-Stirnseite (schmale Seite); Board-Stirnseite = Steckrichtung → passt zur Gehäuseöffnung. Hinweis: Lage anhand Pinout-Diagramm im Wiki final gegenprüfen, da es nicht als Textzeile im Datenblatt steht | dito |
| Besonderheit | moderner (WiFi 6, mehr RAM), pin-kompatibel im Footprint, aber einzelne Pin-Funktionen können abweichen → beim PCB-Design Pinout C6 vs. C3 prüfen | günstiger, sehr ausgereift, riesige Community |

Beide Boards haben integrierten LiPo-Ladekreis (lädt über USB-C) und lassen sich per Stiftleiste oder direkt (castellated) auf die eigene Platine löten. Für das Projekt ist die C6 die naheliegende Wahl, da die reale Preisdifferenz in DE klein ist.

---

## 2. Preise & Verfügbarkeit — XIAO ESP32-C6 (Momentaufnahme 11.09.2026)

| # | Händler | Preis (inkl. MwSt.*) | Lager | Lieferzeit | Link | Prüf-Status |
|---|---|---|---|---|---|---|
| 1 | **Reichelt.de** | **6,99 €** | „ab Lager" (status_1) | N.V. (nicht auf Seite geprüft) | https://www.reichelt.de/de/de/shop/produkt/xiao_esp32c6_wifi_6_bt5_0_zigbee_thread-379732 | Seite 200 ✔, Preis+Lager per Extraktion verifiziert |
| 2 | BerryBase.de | 8,50 € (Variante „Ohne Header", so im EN-Shop) bzw. 8,90 € laut JSON der DE-Seite — Zuordnung nicht 100 % eindeutig | „Sofort verfügbar", 64–100+ Stück | 1–3 Tage | https://www.berrybase.de/seeed-xiao-esp32-c6-wi-fi-6-ble-5.0-zigbee-thread-512kb-sram-4mb-flash-uart-spi-risc-v-019f466b67fa700690e84a8dff9cbf19 | Seite 200 ✔ |
| 3 | Seeed Studio (Original) | $5.20 USD (ohne Versand/Zoll) | „In stock" | Versand wählbar (US/CN/**DE-Warehouse** verfügbar) | https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-p-5884.html | Seite 200 ✔ |
| 4 | Amazon.de | 19,00 € (Marketplace) | „Auf Lager" | Prime-typisch (N.V.) | https://www.amazon.de/dp/B0D2NKVB34 | GET-Abruf erfolgreich (200 mit Inhalt; HEAD 405 = Amazon-typisch), Preis per curl verifiziert — deutlich überteuert |
| 5 | DigiKey.de | — | — | — | C6-Produktseite nicht gefunden (auch über Katalogsuche) | **NICHT VERIFIZIERT** |
| 6 | Mouser.de | — | — | — | — | **NICHT VERIFIZIERT** — Mouser blockt automatisierte Abrufe („Access to this page has been denied") |
| 7 | eBay.de | — | — | — | https://www.ebay.de/sch/i.html?_nkw=xiao+esp32c6 | **NICHT VERIFIZIERT** (Abruf geblockt, Seite liefert real 200) |

*Reichelt/Amazon-Preise sind die im Shop angezeigten Endpreise (Reichelt DE zeigt inkl. MwSt.). Seeed = USD ohne Steuern/Versand.

## 3. Preise & Verfügbarkeit — XIAO ESP32-C3 (Alternative)

| # | Händler | Preis (inkl. MwSt.*) | Lager | Lieferzeit | Link | Prüf-Status |
|---|---|---|---|---|---|---|
| 1 | **BerryBase.de** | **7,90 €** | „Sofort verfügbar", 58 Stück | 1–3 Tage | https://www.berrybase.de/seeed-xiao-esp32c3-winziges-mcu-board-mit-wlan-und-ble | Seite 200 ✔, Preis per JSON-LD verifiziert |
| 2 | DigiKey.de | **5,34 € brutto** (4,49 € netto, im Shop: „Stückpreis mit MwSt.: 5,34310 €") | **Auf Lager: 10.542 Stück** | Standardversand (Dauer N.V.) | https://www.digikey.de/de/products/detail/seeed-technology-co-ltd/113991054/16652880 | Seite per Extraktion verifiziert (direkter curl: 403 = Bot-Schutz, Seite existiert aber) |
| 3 | Reichelt.de | 7,50 € | **z.Zt. nicht lieferbar** | — | https://www.reichelt.de/de/de/shop/produkt/xiao_esp32c3_wifi_bt_ohne_header-358356 | Seite 200 ✔ |
| 4 | Seeed Studio (Original) | $4.99 USD | „In stock" | DE-Warehouse wählbar | https://www.seeedstudio.com/Seeed-XIAO-ESP32C3-p-5431.html | Seite 200 ✔ |
| 5 | Amazon.de | 13,99 € (Marketplace) | „Auf Lager" | N.V. | https://www.amazon.de/dp/B0B94JZ2YF | GET-Abruf erfolgreich (200 mit Inhalt; HEAD 405 = Amazon-typisch), Preis per curl verifiziert |
| 6 | Mouser.de | — | — | — | — | **NICHT VERIFIZIERT** (Bot-Block) |
| 7 | eBay.de | — | — | — | https://www.ebay.de/sch/i.html?_nkw=xiao+esp32c3 | **NICHT VERIFIZIERT** (Abruf geblockt) |

## 4. Versandkosten
**NICHT VERIFIZIERT** für alle Händler (Versandkosten-Seiten nicht einzeln geprüft). Erfahrungswerte bewusst nicht eingetragen (Regel: nichts erfinden). Vor Bestellung Versandkosten im Checkout prüfen.

## 5. Empfehlung (Top-Pick)

**Reichelt.de — Seeed XIAO ESP32C6 für 6,99 € — ab Lager.** Günstigster verifizierter DE-Preis, Direktlink oben (#1). 
Alternative bei Reichelt-Ausverkauf: **BerryBase.de — XIAO ESP32-C6 für 8,50/8,90 €, sofort verfügbar, 1–3 Tage.**
Von der C3 als Sparvariante wird abgeraten: Reichelt-C3 nicht lieferbar, BerryBase-C3 nur 0,60–1,60 € günstiger als das C6 — dafür älterer Funkstandard. C6 nehmen, ggf. 1 Ersatzboard (BerryBase hat 64+ auf Lager).

## 6. Offene Punkte / NICHT VERIFIZIERT
- Mouser.de: automatisierter Abruf geblockt — Preise/Verfügbarkeit offen
- DigiKey.de: kein C6-Listing gefunden; C3-Seite existiert und ist per Extraktion lesbar (direkter curl: 403 Bot-Schutz)
- eBay.de: Abruf geblockt — Preise offen; Suchlinks funktionieren im Browser
- Versandkosten & Lieferzeiten der Händler: nicht verifiziert
- BerryBase C6: exakte Preiszuordnung Variante ohne/mit Header (8,50 vs. 8,90 €) nicht 100 % eindeutig
- USB-C-Lage (Stirnseite) aus Produktbildern/Wiki-Pinout abgeleitet — vor PCB-Fertigung Pinout-Diagramm gegenprüfen
