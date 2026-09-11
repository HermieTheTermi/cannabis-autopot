# Architektur & Geometrie — Smart Grow Topf (V1)

Stand: 11.09.2026 · Grundlage: Festlegungen des Users vom Projektstart (Sprachnachricht)

Dieses Dokument ist die **verbindliche Geometrie- und Architekturvorgabe** für Gehäuse-CAD (OpenSCAD) und PCB.

---

## 1. Entscheidungen (heute festgelegt)

| # | Frage | Entscheidung | Konsequenz |
|---|---|---|---|
| 1 | Topfgröße | **Ø 140 mm bleibt**, Erdbehälterhöhe **150 mm** (nur der Erdebehälter) | Wassertank liegt **darunter** im gleichen Ø 140-Grundriss → Höhe rechnerisch bestimmt (§2) |
| 2 | MCU | **ESP32-C6-MINI-1 direkt auf der eigenen PCB** (kein Dev-Board) | Antenne/Quarz/Flash stecken im Modul, alles andere stellen wir selbst: LDO 3,3 V (ME6211, 500 mA), 1S-Lader (MCP73831T-2), USB-C nativ über GPIO12/13. **Antennen-Freistellung ≥ 15 mm im Gehäuse** und bauteilfreier Bereich im oberen Kammerteil sind Pflicht (siehe §5.4) |
| 3 | Topf-Innengeometrie | Unten Wassertank · **seitliche Wulst** für Akku + Controller + Schlauchkanal · Pumpe fördert nach **oben** auf einen **3D-gedruckten Verteilerring auf der Erdoberfläche** · kapazitiver Sensor **von oben eingesteckt**, seitlich am Controller angeschlossen | Neue Architektur: **Top-Drip statt Bottom-Watering** (siehe §5 – das ändert Regelkreis, Luftspalt-Begründung und Salzthema) |
| 4 | Alarm-Weg | **Telegram final** | ntfy.sh entfällt; WLAN nur für Ereignismeldungen |
| 5 | Nährlösung | **Nur Wasser** im Tank, ein Behälter, keine automatische Düngerdosierung | Dünger ausschließlich ins Substrat (Top-Dressing / Einmischen). **Nie Flüssigdünger in den Tank** (§5.3) |

---

## 2. Höhenberechnung (Rechenweg nachvollziehbar)

Randbedingungen: Außen-Ø 140 mm, Wandstärke 3,0 mm → **Innen-Ø 134 mm** → Grundfläche **141,0 cm²**.
Wassertank nutzt den vollen Grundriss.

| Zielvolumen | Wasserstand (geometrisch) |
|---|---|
| 800 ml | **56,7 mm** |
| 1000 ml | **71,0 mm** |

Gewählt: **1,0 L nutzbar** → max. Wasserstand 71 mm, Kammerhöhe **82 mm** (11 mm Reserve gegen Überlauf beim Rücklauf).

### Höhenstapel (Gesamthöhe ohne Pflanze: **278 mm**)

| y von–bis | Bauteil | Maße |
|---|---|---|
| 0–82 mm | **Wassertank** | Ø 134 mm innen, max. Wasserstand 71 mm = **1,0 L** |
| 82–86 mm | Trenn-/Auflageplatte mit Filterrost | 4 mm, abnehmbar (Blähton-Rückhalt) |
| 86–116 mm | **Luftspalt (Gießfüße)** | 30 mm über max. Wasserstand |
| 116–266 mm | **Innentopf (Erdbehälter)** | 150 mm, Ø 132 außen / **127 mm innen** |
| 266–278 mm | Kragen / Ringauflage | 12 mm (deckt Kabel- und Schlauchaustritt ab) |

**Erdvolumen:** π·(63,5 mm)² · 150 mm = **1,90 L**, davon 25 mm Blähton-Dränage (317 ml) → **≈ 1,58 L Substrat**. Entspricht der Klasse eines 14-cm-Topfs (1,5–2 L).

---

## 3. Wulst (Elektronik + Kanal)

Die Wulst sitzt seitlich am Mantel und **vollständig über dem Wasserstand** (kein Wasserkontakt der Elektronik).

| Parameter | Wert |
|---|---|
| Höhe | y = 90–250 mm (160 mm) |
| Breite (tangential) | **60 mm** |
| Tiefe (radial) | **40 mm** → Gesamtbreite an dieser Stelle ≈ **180 mm** |
| Inhalt | ESP32-C6-MINI-1 (13,2 × 16,6 mm) + Lader/LDO/USB auf eigener PCB (Zielgröße ≤ 38 mm breit) + 2 Lötpads für den externen Taster, LiPo-Zelle 59 × 37 × 5 mm, Pumpe Ø 32 × 44 mm (OEM ABC-12527), Taster, LED |
| Kanäle | **2 getrennte Schlitze**: Kabelkanal (Ø 4 mm) für den Sensor, Schlauchkanal (6 × 6 mm) für Saug- und Druckschlauch |
| Öffnungen | USB-C-Durchbruch (Laden), **LED-Fenster (muss D2 und D5 abdecken)**, **Bohrung für den externen Taster** in der Außenwand, Deckel mit Dichtung |

**Einbau von unten nach oben (Innenmaß):** Pumpe y 92–136 (44 mm Bauhöhe) · Platine darüber · Zelle hochkant dahinter (59 mm Höhe, 5 mm Bautiefe). Maße stammen aus den final gewählten Bauteilen — siehe `../hardware/bom_entscheidung.md`. Die Pumpenparameter in `case/params.scad` (Ø32 / 44 mm) sind noch nachzuziehen.

**Pumpenposition:** Pumpe in der Wulst (oberhalb des Wassers), **Saugschlauch** durch den Kanal bis auf den Tankboden (y ≈ 8 mm, Ansaugkorb/Gewicht), **Druckschlauch** nach oben zum Verteilerring. Peristaltik ist selbstansaugend (Eigenschaft der Bauart; für diese Pumpe nicht ausdrücklich zugesichert → im Aufbau prüfen) → Position unkritisch, Förderhöhe ~200 mm ist irrelevant. **Betrieb ohne Wandler direkt an der 1S-Zelle** (Pumpe ist für 3,7–6 V spezifiziert, siehe `../hardware/bom_entscheidung.md` §3).

---

## 4. Verteilerring (Top-Drip) und Sensor

### Ring
- 3D-gedruckter Ring, **Ø außen ≤ 105 mm**, liegt auf der Substratoberfläche auf.
- Innere Ringkammer, **8–12 Austrittsbohrungen nach unten/innen** (nicht zur Topfwand! sonst läuft das Wasser an der Wand direkt in den Tank = Channeling).
- Zulauf über 4/6-mm-Schlauch aus der Wulst, Abgang am Ring mit Kabel-/Schlauchbogen.
- Ring wird **nicht** in die Erde gedrückt, nur aufgelegt (Wurzelschonung, einfache Reinigung).

### Sensor (kapazitiv v1.2 mit LDO, analog)
- **Messebene: halbe Topfhöhe → 75 mm unter der Substratoberfläche.**
- Der Sensor (Board ~98 × 23 mm, Elektrodenzone ~untere 60 mm) wird von oben eingesteckt, sodass die **Elektrodenmitte auf 75 mm Tiefe** liegt → Oberkante Board ca. 5–10 mm über der Substratoberfläche.
- **Radialposition r ≈ 55 mm** (nah an der Innenwand, **außerhalb des Ringkreises**) → kein Tropfwasser auf die Sensor-Elektronik.
- Kabelabgang oben über den Kragen nach außen, mit **Tropfschlaufe** vor dem Eintritt in die Wulst.
- Gleiche Seite wie die Wulst (kurze Kabelführung); Ring und Sensor kollidieren nicht, da Ring-Ø ≤ 105 mm.

---

## 5. Design-Folgen der Festlegungen (das ist die eigentliche inhaltliche Änderung)

### 5.1 Bottom-Watering → Top-Drip
Bisher: Wasser stand unten, Substrat zog per Kapillarwirkung. **Jetzt:** Pumpe fördert nach oben, das Wasser läuft von oben durch das Substrat und tropft unten wieder in den Tank.

Folgen:
- Der **Luftspalt (30 mm) bleibt Pflicht**, sonst steht der Topf dauerhaft im Wasser → Wurzelfäule und der Sensor meldet permanent „nass".
- Blähton-Schicht (25 mm) unten = Dränage **und** Partikelfilter gegen den Rücklauf in den Tank.
- Regelkreis: nach dem Pumpen dauert es **10–20 min** (nicht 5–15), bis das Wasser bei 75 mm Tiefe ankommt — erst danach darf „Feuchte steigt nicht → Tank leer" ausgewertet werden. Hysterese bleibt (Schwelle ±100–150 ADC).
- Der Sensor darf **nicht** zu flach sitzen: bei Top-Drip trocknet die oberste Schicht zuerst → zu hoher Sensor = Dauerpumpen.

### 5.2 Verbrauchsabschätzung / reicht 1 L?
Faustwert für 1,9-L-Topf: 0,15–0,35 L pro Gießvorgang, im Wachstum alle 3–5 Tage, in der Blüte alle 1–2 Tage.
→ **1,0 L ≈ 1–2 Wochen in der Vegetation, ≈ 3–6 Tage in der Blüte.** *(Schätzung, nicht gemessen — nach dem ersten Durchlauf mit echten Werten ersetzen.)*
→ Der Tank-leer-Alarm ist damit im Hochsommer/Blüte ein **echtes Betriebsereignis**, keine Ausnahme.

### 5.3 Salz- und Nährstoffverhalten (deutlich entschärft, aber nicht weg)
- Kein Dünger im Tank → die frühere Hauptfalle (Salzanreicherung durch Dünger-Rezirkulation) ist **entschärft**.
- Es bleibt: Rücklauf wäscht Nährsalze aus dem Substrat in den Tank → Wasser reichert langsam auf, Substrat magert unten aus.
- **Regel: Tankwasser alle 2 Wochen wechseln** (und dabei den Rücklauf verwerfen). Vorher/nachher Sensorwert notieren (Driftdiagnose).
- **Kein Flüssigdünger in den Tank** — bei einem Rezirkulationssystem konzentriert er sich auf. Düngen ausschließlich über das Substrat (Einmischen beim Topfen, Top-Dressing, gelegentlich von oben mit klarem Wasser nachspülen).

### 5.4 HF / Elektronik
- **Antenne des ESP32-C6-MINI-1** im obersten Wulstbereich halten, damit sie nach oben/außen frei strahlen kann: Espressif fordert wörtlich **≥ 15 mm Freistellung in alle Richtungen** innerhalb des Gehäuses, Modul möglichst am Platinenrand bzw. Platine unter/hinter der Antenne freigeschnitten. Die Wulstwand über der Antenne ist dünner auszuführen (Ziel ~2 mm statt 6 mm), obere ~25 mm der Kammer bauteilfrei. Abstand zu Akku/Metall: **≥ 10 mm** (eigene Auslegung, von Espressif nicht beziffert); Substrat (feucht, εr hoch) bedämpft → Wulst nach außen, nicht innen. **RF-Endtest am fertigen Gehäuse ist vorgeschrieben und noch offen.**
- Elektronikkammer dicht (Deckel + Dichtung, Kabeldurchführung als Tropfschlaufe) — sie sitzt zwar über dem Wasser, aber das Mikroklima am Topf ist feucht.

---

## 6. Offene Punkte

- [ ] Batteriezelle final (Bautiefe Wulst 30 mm!) → BOM-Check läuft (`research/bom-check/04_akku-laden.md`)
- [ ] Pumpenabmessungen → Wulstbreite ggf. anpassen (parametrisch in `case/` vorgesehen)
- [ ] Sensor-Länge real messen (Clone-Streuung ±5 mm) vor dem Einbau
- [ ] Optionale Tanküberwachung: float switch / Drucksensor am Tankboden (Redundanz zum Feuchte-Kriterium) — V2-Thema
- [ ] Kalibrierwerte `dry`/`wet` am echten Substrat aufnehmen (nach erstem Bewässerungsdurchlauf)
- [ ] **Taster-Bohrung** in der Außenwand festlegen (Position so, dass der Taster **ohne Öffnen** erreichbar ist) + Kabelweg für das zweiadrige Tasterkabel zur Platine
- [ ] **LED-Fenster für zwei LEDs:** D2 (Status) und D5 (Tank leer) — ein gemeinsames Fenster oder zwei kleine Lichtleiter; beide Plätze müssen **außerhalb** des antennenfreien Bereichs oben liegen
- [ ] Firmware-Regel für D5 aufnehmen (blinken statt dauerleuchten: 1,3 mA dauerhaft wären 31 mAh/Tag und damit das 19-fache des Standby-Budgets)
