# Hardware-Auswahl & BOM — Smart Grow Topf (V1)

Stand: 11.09.2026 · Konzept: **Top-Drip mit Rücklauf** (Pumpe fördert auf einen Verteilerring auf der Erdoberfläche), eigene PCB, Akku, peristaltische Pumpe (Schlauch quetschen), kapazitiver Sensor (analog), Telegram-Alarm.
➡️ **Finale Auswahl mit geprüften Preisen: [`bom_entscheidung.md`](bom_entscheidung.md)** · Preisrecherchen: `../research/bom-check/` · Verbindliche Maße: `../docs/02_architektur-und-geometrie.md`
Dieses Dokument ist die Recherche-/Ideenebene (inkl. Alternativen und Ausschlussgründen) und wird nicht mehr als Bestellgrundlage verwendet.

> ⚠️ **Historisch, Stand 10.09.2026.** Genannt werden hier noch der **XIAO ESP32-C6** (verworfen,
> jetzt ESP32-C6-MINI-1), die **Adafruit-Pumpe** und der **Gate-Widerstand 220 Ω** (beide verworfen).
> Verbindlich sind ausschließlich `bom_entscheidung.md` und `schaltplan_v1.md`.

---

## 1. Entscheidende Eckpunkte (vom User)

| Punkt | Vorgabe |
|---|---|
| Topf | **Ø 140 mm**, Erdbehälter **150 mm hoch**; darunter Wassertank **1,0 L** (Gesamthöhe 278 mm) |
| MCU | **XIAO ESP32-C6 als Modul** auf eigener PCB (festgelegt 11.09.2026) |
| Pumpe | **Peristaltisch** (Schlauch quetschen) — Medium kommt nie mit der Pumpenmechanik in Kontakt; **klein + günstig**, sitzt in der Seitenwulst |
| Energie | **Akku** (nicht Netz) — Kapazität selbst zu ermitteln |
| Elektronik | **eigene PCB**, in der Seitenwulst über dem Wasserstand |
| Sensor | kapazitiv v1.2 (LDO), **analoger Ausgang**, von oben eingesteckt, Messebene 75 mm |
| Leer-Meldung | kurz ins WLAN → **Telegram** (final) |
| Nährlösung | **nur Wasser** im Tank, keine Düngerdosierung |

---

## 2. Komponenten-Empfehlung

### 2.1 Peristaltische Pumpe (klein + günstig + akkutauglich)

**Empfehlung (Stand 14.09.2026): CONQUERALL DC-5-V-Mikro-Peristaltikpumpe — 11,99 €**
- **≤ 150 ml/min**, Nennspannung **DC 5 V**, Leerlaufstrom 0,4 A, **Anlaufstrom 3 A (bei 5 V)**
- Silikonschlauch **3 × 5 mm** (passt zum bestellten Schlauch), Bauhöhe 42 mm, Ansaugbereich 0,5 m
- Schlauch quetschen, selbstansaugend, Richtung per Umpolung umkehrbar
- Amazon: https://www.amazon.de/dp/B0DHVMZ27Y · 2er-Pack `B0DJ78W43W` 16,61 €
- ⚠️ Ø nicht dokumentiert, Betrieb an 1S (3,0–4,2 V) unterhalb der Nennspannung, Anlaufstrom 3 A
  → **PWM-Softstart Pflicht** und Messauftrag: `bom_entscheidung.md` §4c/§7

**Geprüft und verworfen (14.09.2026):**

| Produkt | Preis | Warum nicht |
|---|---|---|
| „6V-Mini-Peristaltik" `B0HC8WF98P` / `B0H7R9XYJ5` | 5,99 / 6,69 € | Produkttext wörtlich: **„Spannungen unter 6 V betreiben den Motor nicht"** → an 1S unbrauchbar |
| Funduino „0–90 ml/min, 3–12 V" `B0DT1JCFNV` | 11,39 € | Titel nennt 3–12 V, Produktdetails **keine Spannung/kein Strom** → Akku-Auslegung nicht belegbar |
| Whadda WPM447 `B09L4SR2MY` | 14,18 € | 39 ml/min bei 5 W → fünffache Energie pro Liter |
| 12-V-Klasse (G528/G928, Kamoer NKP) | ab 16 € | bräuchte Boost, den die Platine bewusst nicht hat |
| Schrittmotor-Mikropumpen 3–5 V `B0GGRLZ23B` | 18,88 € | 0,5 ml/min → 10 h für eine Dosis |
| „Peristaltikpumpe 3,7/6/12 V … **Membran** Luftpumpe" | 18–19 € | sind **keine** Peristaltikpumpen (Titel-Fehler), Medium hätte Kontakt |

> **Warum 3–6V statt 12V:** Für Akkubetrieb ist eine 3–6V-Pumpe direkt an einer 3,7V-LiPo-Zelle (oder per Buck auf 3,3V) einfacher und effizienter. 12V bräuchte einen Step-Up und mehr Zellen. Bei einem kleinen Topf ist der Durchfluss eh klein — die Funduino (0–90 ml/min) reicht.

> **Durchfluss-Timing (kleiner Topf ~3–6 L):** 0,3–0,6 L pro Gießvorgang. Bei 60 ml/min → **5–10 min** Dauerlauf; kann in 2–3 Portionen mit Pausen erfolgen. Genau kalibrieren (30 s in Messbecher pumpen → nachmessen), Mini-Pumpen streuen ±30 %.

### 2.2 ESP32-Board

**Empfehlung: Seeed XIAO ESP32-C6** (~6 $) — WiFi 6, BLE, **15 µA Deep-Sleep**, alle ADC-Kanäle auf ADC1 (kein ADC2-Fallstrick), LiPo-Lader onboard (passt zum Akku), 21×17,8 mm klein.
- https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-p-5884.html

**Alternative (günstiger):** XIAO ESP32-C3 (~5 $) — reicht (1 Sensor = 1 ADC1-Pin), aber 44 µA Sleep und A3 nur 3 zuverlässige ADC-Pins.

### 2.3 Pumpen-Ansteuerung (eigene PCB)

- **N-Kanal-Logic-Level-MOSFET** (z. B. IRLZ44N oder AO3400) als Low-Side-Schalter:
  - GPIO → 220 Ω → Gate
  - Gate → 10 kΩ → GND (Pull-down: Pumpe sicher AUS beim Boot/Reset)
  - Drain → Pumpe(−), Pumpe(+) → Versorgung; Source → GND
  - **Freilaufdiode** antiparallel zur Pumpe: 1N5819 (Schottky) schützt gegen Induktionsspitzen
- **Fertiges Dual-MOSFET-Modul** (5–36V, 15A) als no-solder-Alternative: 8 Stk **6,49 €** → https://www.amazon.de/dp/B0DG8B58PM
- **Relais:** möglich, aber hörbar + kein PWM — MOSFET ist für Akku besser (kein Spulendauerstrom).

### 2.4 Kapazitiver Bodenfeuchte-Sensor (analog)

- Typ **Capacitive Soil Moisture v1.2 / v2.0** (tropfenförmige grüne Platine, analog 0–3V). Betrieb bei 3,3V ok, Ausgang direkt an ADC.
- **Sensor-VCC per GPIO schalten** (nur während Messung an) — verhindert Korrosions-/Galvanik-Drift und spart Strom.
- Keine Library — `analogReadMilliVolts()` + Median (12 Messungen) + Moving Average.
- **Kalibrierung** in der eigenen Erde: trocken = 0 %, gesättigt = 100 %, als linearer Map. Schwellwert **~35 %** (pumpen) / **~50 %** (Hysterese, Recovery).

### 2.5 Akkupack

| Komponente | Wert | Begründung |
|---|---|---|
| Zelle | **LiPo 3,7 V, 1000–2000 mAh** | Pumpe läuft nur minutenweise pro Zyklus |
| Lade-IC | **MCP73831** (oder XIAO-onboard-Lader) | ~1 € |
| Versorgung | Buck 5V→3,3V? Nein — Sensor+ESP 3,3V, Pumpe 3–6V direkt von Zelle | Sehr niedriges Strombudget |
| Tiefentladeschutz | Zellen-Schutz-PCB / BMS | LiPo-Pack mit Schutz wählen |

**Strombudget-Berechnung (Basis):**
- **Ruhe:** ESP32 Deep-Sleep **15 µA** (oder Light-Sleep ~3,1 mA mit WiFi) + Sensor nur bei Messung an.
- **Messung:** kurz (ms), ~5–10 mA währenddessen.
- **Pumpe:** z. B. 250 mA bei 6 V, aber nur **5–10 min pro Gießvorgang**, Gießen selten (alle 1–3 Tage).
- **Mess-Takt:** alle 5–10 min messen (0,1 s Messung) → vernachlässigbar.
- **Telegram:** nur bei Ereignis (Tank leer / nachgefüllt), kurz WiFi an.

**Abschätzung:** 2000-mAh-LiPo ≈ 7,4 Wh.
- Ruhe-Last (Deep-Sleep 15 µA) über 30 Tage ≈ 0,011 Wh — vernachlässigbar.
- 1 Gießvorgang: 8 min × 250 mA @ 3,7V ≈ 0,12 Wh; bei ~1×/Tag+Toleranz → **eine 1000–1500-mAh-Zelle hält problemlos 2–4 Wochen** ohne Nachladen.
- **Empfehlung: 1× 18650 (2500–3000 mAh) oder LiPo 2000 mAh** mit Schutz-PCB — großzügig dimensioniert.

---

### 2.6 Sauerstoffpumpe (optional, 5 V) — gewählt 15.09.2026

**Mini USB Aquarium Luftpumpe mit Luftstein — Amazon `B0FXB5BMTT`, 8,48 €** (3,9 ★)
5 V USB, ~1 W (0,20 A), < 35 dB, für 10–40 L, dauerbetriebsfähig; **Lieferumfang: Pumpe,
1,15 m Silikonschlauch, Luftsprudler**. Anschluss über **JST-XH 2P (J16)**, Steuerung **IO22**.
Alternativen: `B093GPMT1Z` (9,99 €, 210 L/h) · `B0B82JX6Z4` (7,29 €, regelbar).
Vollständige Tabelle, Strom-/Laufzeitrechnung und Anbindung: `bom_entscheidung.md` §8.

## 3. Gesamtkosten (Kern-Hardware, Schätzung)

| Komponente | Preis |
|---|---|
| XIAO ESP32-C6 | ~6 $ |
| Peristaltische Pumpe (CONQUERALL 5 V) | 11,99 € |
| MOSFET (IRLZ44N 10er) / Fertigmodul | ~7 € |
| Kapazitiver Sensor v2.0 | ~3–5 € |
| Freilaufdiode 1N5819 | <1 € |
| LiPo/18650 + Schutz + Lade-IC | ~8–12 € |
| **Summe (ohne PCB/Optik)** | **~35–45 €** |

---

## 4. Noch offen

- ✅ **Entschieden 11.09.2026:** MCU = **XIAO ESP32-C6 als Modul** (Castellated Pads) auf der eigenen PCB; USB-C-Buchse bleibt durch Gehäuseöffnung erreichbar, onboard-LiPo-Lader wird mitgenutzt.
- ✅ Tankvolumen / Topf-Innengeometrie → berechnet, siehe `../docs/02_architektur-und-geometrie.md` (1,0 L, Gesamthöhe 278 mm).
- ✅ Montageorte: Elektronik + Pumpe in der Seitenwulst (über dem Wasserstand), Sensor von oben, Druckschlauch auf Verteilerring.
- ✅ Telegram final (ntfy.sh verworfen).
- ⏳ Preise/Verfügbarkeit aller Teile → `../research/bom-check/` (läuft)
- ⏳ Zellenwahl final (Bautiefe ≤ 30 mm in der Wulst).
