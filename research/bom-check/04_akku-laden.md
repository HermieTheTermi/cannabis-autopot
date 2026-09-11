# 04 — Akku & Laden (BOM-Check)

Stand: 11.09.2026 · Projekt: cannabis-autopot · Recherche: Web (Preise/Links teils nicht direkt verifizierbar — siehe Statusspalten; Amazon blockt automatisierte Extraktion)

## Kontext & Anforderungen

- Verbraucher: XIAO ESP32-C6 (Deep-Sleep ~15 µA, laut Seeed-Wiki verifiziert) + kapazitiver Sensor (nur bei Messung) + peristaltische 6-V-Pumpe (~250 mA, 5–10 min/Tag).
- Strombudget (aus `hardware_auswahl_bom.md`): 1000–1500 mAh reichen rechnerisch **2–4 Wochen**; 2000 mAh großzügig.
- Die Zelle sitzt in einer **seitlichen Gehäusewulst** am Topf → **Bautiefe = wichtigstes Auswahlkriterium**.
- Feuchte Umgebung am Topf → **Zelle mit Schutz-PCB (PCM) + dichte Kapselung** (Schrumpfschlauch, ggf. Silikagel, Wulst mit Deckel/Dichtung). Kein Kontakt mit Nährlösung.
- Board: **XIAO ESP32-C6 hat Lithium-Ladeverwaltung onboard** (BAT-Eingang 3,7 V, „lithium battery charge management" — laut Seeed-Wiki verifiziert, Stand 11.09.2026) → **kein Lademodul nötig**; exakter Ladestrom-Wert NICHT VERIFIZIERT (Datenblatt/Wiki-Detail).
- Hinweis Anschluss: Der XIAO ESP32-C6 hat **BAT-Lötpads (3,7 V)**, keinen genormten Zellenstecker → Zellenkabel direkt anlöten (oder JST-Buchse auf die eigene PCB). Zelle mit JST-PH-2.0-Stecker passt für die PCB-Seite; für die Pads einfach Kabelende anlöten.

---

## 1) LiPo-Einzelzelle (Pouch) 3,7 V, 2000 mAh, mit Schutz, JST-PH 2.0

**Physik-Check:** Echte 2000-mAh-Pouches sind fast immer **8–11 mm dick** (Bauformen ~103450 = 10 mm, ~803860 = 8 mm). Bei knapper Wulsttiefe ist die 1500-mAh-Klasse (Abschnitt 2) deutlich flacher.

| Produkt | Abmessungen (L×B×T) | Preis | Link | Status |
|---|---|---|---|---|
| **EEMB 103454, 3,7 V 2000 mAh, mit Schutzplatine, JST** | 56 × 34,5 × 10,6 mm | **ca. 8,99 €** | https://www.amazon.de/dp/B08214DJLJ | Maße+Preis nur Sekundärquelle (Fremdprojekt, Stand älter) → **teilweise NICHT VERIFIZIERT** (Amazon-Seite blockt Extraktion) |
| **PKNERGY LP103450, 2000 mAh, JST-PHR-2 (Eckstein)** | Typcode ~50 × 34 × 10 mm (+PCM) | **7,95 €** | https://eckstein-shop.de/LiPo-Akku-Lithium-Ion-Polymer-Batterie-37V-2000mAh-mit-JST-PHR-2-Stecker-LP103450 | Preis + „Lieferbar, Lieferfrist ca. 1–3 Tage" **verifiziert** (Shopseite 11.09.2026); **Schutz-PCB im Listing nicht bestätigt** → NICHT VERIFIZIERT; Maße nur Typcode → NICHT VERIFIZIERT |
| **PKCELL LP803860, 2000 mAh, JST-PHR-2 (Eckstein)** | Typcode ~60 × 38 × 8 mm (+PCM) | **7,95 €** | https://eckstein-shop.de/LiPo-Akku-Lithium-Ion-Polymer-Batterie-37V-2000mAh-mit-JST-PHR-2-Stecker-LP803860 | Preis + Lieferzeit 1–3 Tage **verifiziert**; Schutz + Maße NICHT VERIFIZIERT |

---

## 2) LiPo 1000–1500 mAh mit Schutz (kleinere/flachere Alternative)

**Top-Fund:** EFASO (deutscher Shop, Kassel) führt die **503759** als 1500 mAh **mit PCM-Schutz und JST PH2.0-2P** — Typcode 503759 bedeutet **5,0 × 37 × 59 mm**, also nur **~5 mm Bautiefe** (dünnste sinnvolle Option für die Wulst).

| Produkt | Abmessungen (L×B×T) | Preis | Link | Status |
|---|---|---|---|---|
| **EFASO 503759, 3,7 V „1500 mAh", PCM, JST PH2.0-2P** | ~59 × 37 × 5 mm (Typcode) | **14,90 €**, Lieferzeit ca. 1–4 Werktage | https://efaso.de/produkt/503759-3-7v-1500-mah-pcm-jst-ph2-0-2p/ | Preis **verifiziert** (Shopseite/Preisvergleich 11.09.2026); Maße aus Typcode → **NICHT direkt am Listing verifiziert**; Hinweis: derselbe Typ wird andernorts auch als **1200 mAh** angeboten (Kapazitätsangabe optimistisch → NICHT VERIFIZIERT) |
| EFASO 603450, 3,7 V 1250 mAh, JST PH2.0 (Amazon-Variante) | ~50 × 34 × 6 mm (Typcode) | Preis NIV | https://www.amazon.de/efaso-Akku-Verschiedene-Kapazit%C3%A4ten-Stecker/dp/B0DZXV6YG1 | **NICHT VERIFIZIERT** (Amazon blockt; Preis/Maße nicht extrahierbar) |
| EFASO 553450, 3,7 V 1000 mAh, JST PH2.0 (Amazon) | ~50 × 34 × 5,5 mm (Typcode) | Preis NIV | https://www.amazon.de/Lithium-Polymer-Wiederaufladbarer-Lipo-Akku-JST-Anschluss-silber/dp/B0DKD873GC | **NICHT VERIFIZIERT** |
| EFASO 963450, 3,7 V 1800 mAh, JST PH2.0 (Amazon) | ~50 × 34 × 9,6 mm (Typcode) | Preis NIV | https://www.amazon.de/wiederaufladbarer-Lithium-Polymer-Akku-PH2-0-2PIN-Stecker-Abstand-silber/dp/B0CWFF5DRL | **NICHT VERIFIZIERT** |

---

## 3) Geschützte 18650-Zelle + Halter mit Kabel

**Zelle (empfohlen): Keeppower R 18650 3000 mAh, PCB-geschützt bis 15 A, Button-Top** (Samsung-/LG-Innenzelle):
- **Abmessungen: Ø 18,85 ± 0,10 mm × 69,0 ± 0,2 mm** — **verifiziert** (akkuteile.de Produktdatenblatt 11.09.2026). Wichtig: geschützte 18650 sind **länger/dicker** als nackte Zellen (69 statt 65 mm; Halter + Stecker brauchen ~77–80 mm).
- Preis: **9,75 € bei nkon.nl** (verifiziert per Shop-Snippet 11.09.2026; Versand NL→DE, Versandkosten/Lieferzeit **NICHT VERIFIZIERT**): https://nkon.nl/en/keeppower-18650-3000mah-protected.html
- akkuteile.de führt dieselbe Zelle — **Preis auf der Seite NICHT VERIFIZIERT** (Auto-Extraktion erfasste keinen Betrag): https://www.akkuteile.de/lithium-ionen-akkus/18650/keeppower/keeppower-r-18650-3000mah-3-6v-3-7v-li-ion-akku-pcb-geschuetzt-15a_12032_2167

**Halter mit Kabel:**
| Produkt | Maße | Preis | Link | Status |
|---|---|---|---|---|
| **BerryBase „Batteriehalter für 1x 18650 mit Anschlusskabel" (BH-1K18650)** | 76 × 21 × 18 mm (Halteklammern offen) | **0,60 €** | https://www.berrybase.de/batteriehalter-fuer-1x-18650-mit-anschlusskabel | Preis **verifiziert** (Shopseite); Lieferzeit 1–3 Tage (Shop-Angabe) |
| BerryBase „Batteriehalter 1x 18650 mit Anschlusskabel **und JST PH 2.0**" | 76 × 21 × 18 mm | 0,75 € | https://www.berrybase.de/batteriehalter-fuer-1x-18650-mit-anschlusskabel-und-jst-ph-2.0-steckverbinder | Preis verifiziert, aber **„Artikel aktuell nicht lieferbar"** (11.09.2026) |

**Gesamtpreis 18650-Lösung:** 9,75 € (Zelle) + 0,60 € (Halter) ≈ **10,35 € + 2× Versand** (Zelle+Halter aus 2 Shops; ggf. alles bei akkuteile.de bestellen, Preis dort prüfen). Bauhöhe in der Wulst: Zelle Ø18,85 mm + Halterwand ≈ **~21 mm tief**, ~80 mm lang → deutlich klobiger als die Pouch-Optionen.

*Alternative (ohne Schutz, daher nur mit TP4056-Schutzmodul oder PCM sinnvoll):* BerryBase führt ungeschützte Marken-Zellen günstig (Sony VTC6 3000 mAh Flat-Top **6,70 €**; Panasonic NCR18650GA 3450 mAh **5,90 €** — Preise verifiziert; beide **ohne PCM**).

---

## 4) USB-C-Ladeoption

**Variante A — Onboard-Lader des XIAO ESP32-C6 (empfohlen):**
- „Lithium battery charge management" onboard, BAT-Eingang 3,7 V — **verifiziert** (Seeed-Wiki, 11.09.2026): https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/
- Kosten: 0 € extra → **nur Zelle + Kabel** nötig. USB-C-Buchse des XIAO wird zum Laden genutzt. Exakter Ladestrom NICHT VERIFIZIERT (typ. 50–100 mA bei XIAO; bei 1000–2000-mAh-Zelle unkritisch, Ladezeit grob 12–30 h → für Nachts/Wochenende ok, Wert vor Inbetriebnahme im Wiki prüfen).

**Variante B — Fallback TP4056 USB-C mit Schutz (DW01A):**
| Produkt | Maße | Preis | Link | Status |
|---|---|---|---|---|
| TP4056 1A USB-C Lademodul | – | **0,65 €/Stk** (ab 5: 0,45 €) | https://www.roboter-bausatz.de/p/tp4056-1a-lithium-ionen-lipo-lademodul-fuer-arduino-usb-c | Preis **verifiziert** (Shop-Snippet) |
| TP4056-C USB-C mit Über-/Tiefentladeschutz | **29 × 17,5 × 4,5 mm** | Preis **NICHT VERIFIZIERT** | https://www.vipitec.de/produkt/tp4056-c-laderegler-fuer-einen-li-ion-lipo-akku-mit-berladeschutz-und-tiefentladeschutz-usb-c-5-v-1-a_06-0010-00002 | Maße verifiziert (Listing) |
| Alternativ: Adafruit bq25185 Ladeplatine (USB/DC/Solar) | – | 6,90 € (BerryBase-Listing) | berrybase.de (ADA6091) | teils verifiziert (Related-Listing) |

**MCP73831:** als Einzelmodul in dieser Recherche **nicht verifiziert gefunden** → wenn gewünscht, on-PCB verbauen (IC ~1 €, Bezug z. B. JLCPCB-BOM) statt als Modul.

---

## 5) Sicherheitszubehör

- **1S-Schutz-PCB (falls Zelle ohne Schutz):** In dieser Recherche **kein verifizierter DE-Direktlink mit Preis** gefunden → **NICHT VERIFIZIERT** (kein Preis/Link erfinden). Empfehlung: **direkt geschützte Zelle kaufen** (alle Empfehlungen oben haben PCM) → Schutz-PCB entfällt. Falls doch nötig: DW01A+8205A-Modul (eBay/Amazon „1S 3.7V Schutzplatine Li-Ion", Preise dort prüfen).
- **JST-PH 2.0 Steckverbinder-Set (10 Paar):**
| Produkt | Umfang | Preis | Link | Status |
|---|---|---|---|---|
| Micro JST PH 2.0 2-Pin Stecker+Buchse | **20 Stück = 10 Paare** | Preis **NICHT VERIFIZIERT** (Amazon blockt) | https://www.amazon.de/St%C3%BCck-Stecker-Schwarz-Silikon-Buchse/dp/B07449V33P | Link existiert; Preis prüfen |
| Eckstein „JST-PH 2.0 Kabel-Kit 2 Pin (20 Paare)" (Art. ZB00008) | 20 Paare | Preis **NICHT VERIFIZIERT** | https://eckstein-shop.de/2Pin-JST-PH-20-Kabel-Kit-20-Paare | Seite existiert, Preis nicht extrahierbar |
| leds-and-more.de „Micro JST Kabel mit Buchse + Platinenstecker, 2-pol., RM 2,0 mm" | Einzel (ab 25 Stk) | **0,59 €/Stk** (ab 25 Stück, heute als Shop-Snippet belegt) | https://leds-and-more.de/Micro-JST-PH-20mm | teils verifiziert (Preisangabe aus Shop-Snippet) |
| Hinweis | Alternativ Kabel direkt an XIAO-BAT-Pads löten → Steckerset nur nötig, wenn die Zelle steckbar sein soll. | | | |

---

## Empfehlung

**Primär: EFASO 503759, 3,7 V (1500 mAh), PCM-geschützt, JST PH2.0-2P — 14,90 €, efaso.de (Versand aus DE, 1–4 Werktage).**
Begründung:
1. **Bautiefe:** nur ~5 mm (Typcode 503759) — die mit Abstand flachste Lösung mit PCM; passt damit auch in eine schmale Gehäusewulst. Alle echten 2000-mAh-Zellen sind 8–11 mm dick.
2. **Sicherheit in feuchter Umgebung:** integrierter PCM (Über-/Tiefentladung, Kurzschluss) + zusätzliche Kapselung einplanen (Schrumpfschlauch, trockene Wulstkammer, Kabeldurchführung mit Zugentlastung). Kapazität reicht dem Strombudget nach für Wochen.
3. **Preis:** 14,90 € (teurer als Eckstein 7,95 €, aber mit ausdrücklich ausgewiesenem Schutz + passendem JST-PH-2.0).

**Alternativen nach Entscheidungsregel:**
- Ist die Wulst **≥ ~12 mm tief** und Preis wichtiger als Schutz-Nachweis: **Eckstein LP103450 2000 mAh (7,95 €, 1–3 Tage)** — aber Schutz im Listing unbestätigt → vor Bestellung klären; sonst **EEMB 103454 mit Schutzplatine (~9 €, Amazon)**.
- Ist **Robustheit** wichtiger als Bautiefe: **Keeppower 18650 3000 mAh geschützt (9,75 €) + BerryBase-Halter (0,60 €)** ≈ 10,35 € — Metallgehäuse zellenseitig robuster, aber Ø18,85 mm + offene Halterung → ~21 mm tief, dichte Kapselung aufwendiger; für die schmale Wulst die schlechteste Passung.
- **Laden:** XIAO-Onboard-Lader nutzen (0 €, USB-C am Board). TP4056 USB-C (0,65 €) nur als Fallback, falls die Zelle separat/ungeschützt verbaut wird.

## Vergleichstabelle

| Option | Kapazität | Abmessungen (L×B×T bzw. Ø×L) | Preis | Link | Verifiziert? |
|---|---|---|---|---|---|
| **EFASO 503759 PCM + JST PH2.0** ⭐ | 1500 mAh (Angabe; teils als 1200 mAh gelistet) | ~59 × 37 × 5 mm (Typcode) | **14,90 €** | https://efaso.de/produkt/503759-3-7v-1500-mah-pcm-jst-ph2-0-2p/ | Preis ja; Maße/Kapazität nein |
| Eckstein LP103450 (PKNERGY) JST-PHR-2 | 2000 mAh | ~50 × 34 × 10 mm (Typcode) | 7,95 € | https://eckstein-shop.de/LiPo-Akku-Lithium-Ion-Polymer-Batterie-37V-2000mAh-mit-JST-PHR-2-Stecker-LP103450 | Preis/Lieferzeit ja; Schutz+Maße nein |
| Eckstein LP803860 (PKCELL) JST-PHR-2 | 2000 mAh | ~60 × 38 × 8 mm (Typcode) | 7,95 € | https://eckstein-shop.de/LiPo-Akku-Lithium-Ion-Polymer-Batterie-37V-2000mAh-mit-JST-PHR-2-Stecker-LP803860 | Preis ja; Schutz+Maße nein |
| EEMB 103454 mit Schutzplatine (Amazon) | 2000 mAh | 56 × 34,5 × 10,6 mm (Sekundärquelle) | ca. 8,99 € | https://www.amazon.de/dp/B08214DJLJ | nein (Sekundärquelle) |
| Keeppower R 18650 3000 mAh PCB-geschützt | 3000 mAh | Ø 18,85 × 69,0 mm | 9,75 € (nkon.nl) | https://nkon.nl/en/keeppower-18650-3000mah-protected.html | Maße ja (akkuteile); Preis ja (nkon) |
| + BerryBase 18650-Halter m. Kabel | – | 76 × 21 × 18 mm | 0,60 € | https://www.berrybase.de/batteriehalter-fuer-1x-18650-mit-anschlusskabel | ja |
| XIAO ESP32-C6 Onboard-Lader (USB-C) | – | Board 21 × 17,8 mm | 0 € extra | https://wiki.seeedstudio.com/xiao_esp32c6_getting_started/ | ja (Lader vorhanden); Ladestrom nein |
| TP4056 USB-C Modul (Fallback) | – | 29 × 17,5 × 4,5 mm | 0,65 € | https://www.roboter-bausatz.de/p/tp4056-1a-lithium-ionen-lipo-lademodul-fuer-arduino-usb-c | Preis ja; Maße ja (vipitec-Listing) |
| 1S-Schutz-PCB (falls nötig) | – | – | NICHT VERIFIZIERT | NICHT VERIFIZIERT | nein |
| JST-PH 2.0 Set (10 Paare) | – | – | NICHT VERIFIZIERT | https://www.amazon.de/St%C3%BCck-Stecker-Schwarz-Silikon-Buchse/dp/B07449V33P | nein |

---
*Verifikationsmethodik: Preise/Lieferzeiten direkt von Shopseiten (Eckstein, EFASO, BerryBase, akkuteile, nkon) per Web-Extraktion am 11.09.2026; Amazon-Produktseiten blockieren automatisierte Extraktion → dortige Preise als NICHT VERIFIZIERT markiert. Typcode-Maße (z. B. 503759 = 5×37×59 mm) sind Standard-Nomenklatur, am jeweiligen Listing aber nicht einzeln bestätigt.*
