# Kapazitiver Bodenfeuchte-Sensor für den Bottom-Watering Grow-Topf (ESP32)

Recherche-Stand: 10.09.2026 · Alle Preise/Links live verifiziert · Quellen am Ende

---

## 1. Sensoroptionen im Vergleich

### Capacitive Soil Moisture Sensor v1.2 (der klassische „Grünplatinen“-Clone)

| Merkmal | Wert |
|---|---|
| Messprinzip | Kapazitiv: zwei lackierte Leiterbahnen auf der PCB bilden einen Kondensator; Erde ist das Dielektrikum. **Kein blankes Metall im Boden → keine Korrosion, keine Galvanik** |
| Elektronik | 555-Timer erzeugt Rechtecksignal → Tiefpass mit Sensorkapazität → Glättung → analoge Gleichspannung an AOUT |
| Ausgang | Analog 0–3 V (mit intaktem LDO-Regler), **invertiert: trocken = HOHE Spannung, nass = NIEDRIGE Spannung** |
| Betriebsspannung | 3,3–5 V spezifiziert; **am ESP32 immer 3,3 V nehmen** (ADC-sicher). Achtung: nicht jede Clone-Variante läuft an 3,3 V (siehe §3) |
| Strom | < 5 mA |
| Preis | ab **1,29 €** (Chipglobe v2.0) · **4,99 €** (AZ-Delivery v1.2) · **8,99 €/6 Stück** (Amazon Aideepen ≈ 1,50 €/St.) |

**Funktionsweise kurz:** Nasse Erde hat eine hohe Dielektrizitätskonstante (Wasser ≈ 80, Luft ≈ 1). Mehr Wasser → höhere Kapazität → höhere Oszillator-Belastung → **niedrigere Ausgangsspannung**. Der umgekehrte Fall (trocken → hohe Spannung) ist das wichtigste Merkmal für die Steuerlogik.

### v2.0 — Vorsicht, kein echtes Upgrade
- Laut [mikrocontroller.net](https://www.mikrocontroller.net/topic/554842): *„Die 2.0 hat keine inhaltliche Bedeutung.“* — gleiche Schaltung, anderes Label.
- Die Detail-Analyse von [miltschek.de](https://miltschek.de/article_2022-06-26_Soil+Moisture+Sensors.html) zeigt: v2.0-Boards haben die Oszillatorfrequenz auf ~1,5 MHz angehoben (soll Salz-Einfluss reduzieren), **aber den Tiefpass nicht angepasst** → Messung rauscht stark, sättigt schon bei wenigen Tropfen Wasser, kleiner nutzbarer Dynamikbereich. In der Praxis ist v2.0 oft **schlechter** als v1.2.
- **Empfehlung: v1.2 MIT LDO bevorzugen.**

### DFRobot SEN0193 (das „Original“)
- Identische Technik, aber geprüfte Qualität und Datenblatt ([DFRobot Wiki](https://wiki.dfrobot.com/sen0193/)).
- **6,01 € inkl. MwSt.** bei DigiKey (5,05 € netto, 237 Stück auf Lager, Lieferzeit Hersteller 9 Wochen) — plus Versand. Farnell führt ihn ebenfalls.
- In der TU-Wien-Vergleichsstudie ([Sensors 2025, 25(5):1461](https://www.mdpi.com/1424-8220/25/5/1461)): billigster der vier getesteten Sensoren, in bestimmten Substraten vergleichbar mit SMT50 und Scanntronik; am genauesten war TEROS 10 (aber ~100-€-Klasse).

### Digital/I2C-Alternativen (nur erwähnt, nicht Kernempfehlung)
- DFRobot **SEN0308** (IP65, vollvergossene wasserdichte Sonde, analog) — für Hydro/feuchtes Umfeld; bei Farnell Art.-Nr. 3769915 (Preis nicht verifiziert).
- Adafruit STEMMA Soil Sensor (I2C) — umgeht ADC-Rauschen, aber teurer und im DE-Versand schwerer zu bekommen.
- BeFlE **SoMoSe v4.2** (vergossener Sensor inkl. Temperatur, MQTT-Firmware, 15,99 € auf Amazon) — interessante deutsche Premium-Option, über Budget.

---

## 2. Anschluss am ESP32 und Kalibrierung für Erde

### Verdrahtung
```
Sensor VCC  → ESP32 3,3 V   (nicht 5 V — sonst u. U. >3,3 V am AOUT)
Sensor GND  → ESP32 GND
Sensor AOUT → GPIO32–GPIO39 (ADC1; ADC2-Pins bei aktivem WLAN meiden)
```
Arduino: `analogSetAttenuation(ADC_11db)` (12-Bit, 0–4095, ~0–3,3 V). ESPHome: `attenuation: 12db`.

### ⚠️ Wichtige Korrektur zur Projektannahme
Die Annahme **„trocken < 1500, feucht > 1700“** ist **invertiert**. Der kapazitive Sensor liefert:

| Zustand | ADC-Wert (12-Bit, 11 dB) | Quelle |
|---|---|---|
| Trocken (Luft) | **2100–2600** | newbiely (2200–2500), ComponentIndex (~2100) |
| Gesättigte Erde / Wasser | **1000–1500** | newbiely (1200–1500), ComponentIndex (~1050) |
| Rohe Spannung: trocken/nass | 2,91 V / 1,03 V | SmartHomeScene (ESPHome 12 db) |

**Steuerlogik muss also lauten:** Pumpe einschalten, wenn **ADC > Schwelle** (zu trocken); stoppen, wenn **ADC < Schwelle − Hysterese**. „Sensor misst keine Zunahme“ = ADC fällt nach dem Pumpen nicht ab.

### Kalibrierablauf (für Erde, nicht nur Wasser)
1. **Trockenwert:** Sensor an der Luft, 20 Samples mitteln → `dry` (≈ 2200–2600).
2. **Nasswert in echtem Substrat:** eigenen Topf mit der exakten Erde gesättigt durchwässern, 30 min abtropfen lassen, Sensor einstecken → `wet` (≈ 1200–1600). Ein Wasserglas liefert nur den Extremwert (≈ 1000–1100) und ist als alleinige Referenz zu nass.
3. **Schwelle:** `THRESHOLD ≈ (dry + wet) / 2` (typisch **1600–1900**), Hysterese ±100–150 ADC. Bei 12-Bit gilt grob: 100 ADC ≈ wenige % Feuchte.
4. **Glättung:** Median über 10–20 Samples (ESPHome: `median: window_size: 7`), da der ESP32-ADC rauscht und v2.0-Boards stark streuen.
5. **Nachkalibrieren:** nach jedem Umtopfen und nach einigen Wochen Betrieb erneut messen — die Einbettung ins Substrat verändert die Werte.

Werte niemals aus Tutorials kopieren — **jeder Sensor/jedes Board liefert andere Absolutwerte** (Clone-Streuung + ESP32-ADC-Toleranz + Substrat).

---

## 3. Echte Grenzen in erdbasiertem Substrat

**Vorweg:** Die Prämisse „der Sensor ist eigentlich für Wasserbehälter/Hydroponik gebaut“ stimmt so nicht — der originale DFRobot SEN0193 wurde für **Erde in Pflanztöpfen** entwickelt. Aber die folgenden Einschränkungen sind real:

1. **Salz- und Düngereinfluss (der größte Punkt bei Cannabis):**
   Gelöste Ionen erhöhen die Dielektrizitätskonstante → der Sensor liest **feuchter als real**. Die MDPI-Studie [Sensors 2024, 24(19):6323](https://www.mdpi.com/1424-8220/24/19/6323) zeigt: Salzgehalt verschlechtert die Genauigkeit aller acht getesteten Sensortypen signifikant. **In deinem Setup ist das besonders kritisch:** gedüngtes Substrat + Rezirkulation (Runoff tropft zurück in den Tank!) reichert über Wochen Salze an → **Kalibrationsdrift Richtung „nass“**. Gegenmittel: Tankwasser regelmäßig wechseln, EC im Auge behalten, Schwellwert anhand des Pflanzenzustands nachjustieren.

2. **Substratabhängigkeit & Einstecktechnik:**
   TU Wien ([Sensors 2025, 25(5):1461](https://www.mdpi.com/1424-8220/25/5/1461), 380 Messungen): die Genauigkeit variiert stark zwischen Substraten — **substratspezifische Kalibrierung ist Pflicht**; auch die Art des Einsteckens beeinflusst die Messung (Luftspalt zwischen Elektrode und Erde → falsch „trocken“).

3. **Mechanische Beschädigung beim Umtopfen:**
   Der Lack über den Elektroden ist dünn. Kratzer beim Ein-/Ausstecken legen Kupfer frei → Korrosion und Fehlmessung. Sensor nicht als Hebel benutzen, beim Umtopfen prüfen und neu kalibrieren.

4. **Temperaturdrift:**
   Keine Temperaturkompensation auf v1.2/v2.0 — bei großen Temperatursprüngen (Growzelt-Tag/Nacht) driften die Werte um einige Prozent. Nicht dramatisch für die Pumpensteuerung, aber bei Schwellwert-Entscheidungen mit einrechnen.

5. **Nur lokale Spot-Messung — wichtig für Bottom-Watering:**
   Der Sensor misst nur wenige cm³ um die Elektrode. In einem Bottom-Watering-Topf gibt es einen **vertikalen Feuchtegradienten** (unten nass, oben trocken). Steckt der Sensor zu hoch, meldet er „trocken“, während unten alles schwimmt → Überpumpen. **Sensor auf halber Topfhöhe in der Wurzelzone platzieren.** Zusätzlich ist die Wicking-Antwort langsam: Nach dem Pumpen dauert es 5–15 min, bis die Feuchte am Sensor ankommt — das „Tank leer“-Kriterium (keine ADC-Abnahme nach dem Pumpen) muss entsprechend verzögert ausgewertet werden.

6. **Gießen von oben** verursacht transiente Nass-Spikes, die nichts über die Wurzelzone aussagen. Im Bottom-Watering-Betrieb entfällt das — gut.

7. **Clone-Lotterie (wichtig beim Billigkauf):**
   Laut miltschek.de gibt es drei zufällig gestreute Varianten: v1.2 mit LDO, v2.0 mit LDO, v1.2 ohne LDO. Fehlerbilder:
   - **LDO + NE555:** NE555 braucht ≥ 4,5 V — an 3,3 V tot, an 5 V läuft er.
   - **Ohne LDO an 5 V:** AOUT kann > 3 V liefern → gefährlich für den ESP32-ADC.
   - **Falscher Timer / falsche Filterwerte:** Rauschbrei statt Messkurve.
   **Konsequenz:** Jeden Sensor nach Erhalt testen (Luft ≈ 2100–2600, Wasser ≈ 1000–1500) und defekte Ware zurückgeben — deshalb Multi-Packs oder ein seriöser Händler.

8. **Warum kein resistiver Sensor?** Die 2-Pin-Gabel mit blankem Metall korrodiert in feuchter, gedüngter Erde **innerhalb von Wochen** (Galvanik), misst dann den Elektrolyt-Übergangswiderstand statt der Bodenfeuchte und ist für den Dauereinsatz im Topf ungeeignet. Der kapazitive ist für genau diesen Zweck die richtige Wahl.

---

## 4. Konkrete Kaufempfehlung (unter 10 €)

| Priorität | Produkt | Preis | Link |
|---|---|---|---|
| ⭐ Empfehlung | **AZ-Delivery Bodenfeuchtesensor v1.2** (geprüfte Ware, DE-Versand, Kabel + E-Book) | **4,99 €** | https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2 |
| Reserve/Mehrfachmessung | **Aideepen 6er-Pack v1.2** (Amazon, ~1,50 €/St., 2–3 behalten als Ersatz für die Clone-Lotterie) | **8,99 €** | https://www.amazon.de/Aideepen-Bodenfeuchtigkeitssensor-Hygrometer-Modul-korrosionsbeständiges-Pflanzenbewässerung/dp/B0HFBS3SFD |
| Original mit Datenblatt | **DFRobot SEN0193** (DigiKey, auf Lager) | **6,01 €** + Versand | https://www.digikey.de/de/products/detail/dfrobot/SEN0193/6588605 |
| Bastel-Lotterie | Chipglobe v2.0 | 1,29 € | https://chipglobe.shop/produkte/kapazitiver-bodenfeuchtesensor-v2-0/ |

**Praxistipp für dein Projekt:** Nimm 2–3 Stück. Ein Sensor in der Wurzelzone steuert die Pumpe; ein zweiter in einer anderen Tiefe (oder als Reserve im Schrank) hilft bei der Diagnose, ob die Feuchte wirklich „durchgezogen“ ist. Bei der Clone-Lotterie kostet der Versuch fast nichts.

---

## 5. Wasserstress / Bewässerung aus dem Tank — was der Sensor nicht kann

- Der kapazitive Sensor misst **Wassergehalt** (relativer Volumen-%), **nicht Wasserstress**. Wasserstress ist eine Funktion des **Wasserpotenzials (Saugspannung, mbar)** — das hängt von Substrat, Wurzelmenge und Pflanze ab. Für die Pumpensteuerung reicht der kapazitive Sensor völlig; für „durstige Pflanze“ ist er nur ein Indikator.
- **Goldstandard-Referenz zum Kalibrieren:** **Blumat Digital Tensiometer**, **48,50 €** (https://www.blumat-shop.de/blumat-digital_2; idealo ab 50,99 €) — misst 10–750 mbar Saugspannung direkt in der Wurzelzone, hat aber **keine elektrische Schnittstelle** für den ESP32. Einsatz: einmal mit Blumat den echten Zielbereich (typisch 100–300 mbar für die meisten Pflanzen) bestimmen und damit den ADC-Schwellwert des kapazitiven Sensors festnageln.
- **Deine geplante Redundanz ist gut:** „Nach dem Pumpen sinkt der ADC nicht → Tank leer / Pumpe defekt / Sensor nicht im Substrat“ — das ist ein robuster Selbsttest. Nur die **Wicking-Verzögerung** (5–15 min) und die **Hysterese** einbauen, sonst meldet das System falsche Alarme.
- Teures Upgrade (außerhalb Budget): TEROS 10 war in der TU-Wien-Studie der genaueste Sensor, liegt aber in der ~100-€-Klasse. Für einen einzelnen Topf: Overkill.

---

## Quellen

- MDPI Sensors 2024, 24(19), 6323 — *Performance of Soil Moisture Sensors at Different Salinity Levels* — https://www.mdpi.com/1424-8220/24/19/6323
- MDPI Sensors 2025, 25(5), 1461 (TU Wien) — *A Comparison of Capacitive Soil Moisture Sensors in Different Substrates* — https://www.mdpi.com/1424-8220/25/5/1461
- miltschek.de — *Soil Moisture Sensors* (Reverse-Engineering der v1.2/v2.0-Clones) — https://miltschek.de/article_2022-06-26_Soil+Moisture+Sensors.html
- mikrocontroller.net — *Moisture Sensor 1.2 oder 2.0?* — https://www.mikrocontroller.net/topic/554842
- newbiely.com — ESP32-S3 Soil Moisture Sensor Tutorial (Kalibrierwerte) — https://newbiely.com/tutorials/esp32-s3/esp32-s3-soil-moisture-sensor
- SmartHomeScene — *DIY Capacitive Soil Moisture Sensor v1.2 with ESPHome* — https://smarthomescene.com/diy/diy-capacitive-soil-moisture-sensor-v1-2-with-esphome/
- ComponentIndex — Capacitive Soil Moisture Sensor Guide — https://componentindex.net/components/soil-moisture/
- DFRobot Wiki SEN0193 — https://wiki.dfrobot.com/sen0193/
- Preise live verifiziert: az-delivery.de, amazon.de, digikey.de, chipglobe.shop, blumat-shop.de, idealo.de (10.09.2026)
