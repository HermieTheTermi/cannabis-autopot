# Architektur & Geometrie — Smart Grow Topf (V1)

Stand: 11.09.2026 · Grundlage: Festlegungen des Users vom Projektstart (Sprachnachricht)

Dieses Dokument ist die **verbindliche Geometrie- und Architekturvorgabe** für Gehäuse-CAD (OpenSCAD) und PCB.

---

## 1. Entscheidungen (heute festgelegt)

| # | Frage | Entscheidung | Konsequenz |
|---|---|---|---|
| 1 | Topfgröße | **Ø 140 mm bleibt**, Erdbehälterhöhe **150 mm** (nur der Erdebehälter) | Wassertank liegt **darunter** im gleichen Ø 140-Grundriss → Höhe rechnerisch bestimmt (§2) |
| 2 | MCU | **ESP32-C6-MINI-1 direkt auf der eigenen PCB** (kein Dev-Board) | Antenne/Quarz/Flash stecken im Modul, alles andere stellen wir selbst: **Buck 3,3 V (AP63203, 2 A)** und **Buck 5 V (SY8113B, 3 A)** aus einem **2S-Pack (6,0–8,4 V)**, **2S-Lader IP2326** (8,4 V / 0,90 A), USB-C nativ über GPIO12/13. **Antennen-Freistellung ≥ 15 mm im Gehäuse** und bauteilfreier Bereich im oberen Kammerteil sind Pflicht (siehe §6.4) |
| 3 | Topf-Innengeometrie | Unten Wassertank · **seitliche Wulst** für Akku + Controller + Schlauchkanal · Pumpe fördert nach **oben** auf einen **3D-gedruckten Verteilerring auf der Erdoberfläche** · kapazitiver Sensor **von oben eingesteckt**, seitlich am Controller angeschlossen | Neue Architektur: **Top-Drip statt Bottom-Watering** (siehe §6 – das ändert Regelkreis, Luftspalt-Begründung und Salzthema) |
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
| Inhalt | ESP32-C6-MINI-1 (13,2 × 16,6 mm) + Lader/Wandler/USB auf eigener PCB (Zielgröße ≤ 38 mm breit) + 2 Lötpads für den externen Taster, LiPo-Pack **2S** (Maße nach Auswahl, siehe §7), **Pumpe CONQUERALL 5 V (Bauhöhe 42 mm, Ø nicht dokumentiert — Wulst ist auf Ø 32 gerechnet)**, Taster, LED |
| Kanäle | **2 getrennte Schlitze**: Schlauchkanal (6 × 6 mm) für Saug- und Druckschlauch sowie Kabelkanal. Mit der GPIO-Erweiterung (14.09.2026) steigt die Zahl der durchzuführenden Kabel deutlich: **Feuchtesensor (J2)**, **Lichtsensor (J7)**, **I²C (J8)** und **sieben Reserve-Kabel (J9–J15)** sowie die **Taster-Rückleitung (J6)** — insgesamt **11 Kabel** (der Auftrag nennt „9 Kabel"; die aufgeführten Posten summieren sich auf 11, siehe offener Punkt). Die Reserve-Leitungen werden nur nach Bedarf gesteckt; der vorhandene Ø-4-mm-Kanal reicht für zwei dünne Sensorleitungen, für die Gesamtzahl ist ein **breiterer/mehrkammeriger Kabelaustritt** nötig. |
| Öffnungen | USB-C-Durchbruch (Laden), **LED-Fenster (muss D2 und D5 abdecken)**, **Bohrung für den externen Taster** in der Außenwand, **Kabelaustritte für Feuchte-/Licht-/I²C-/Reserve-Sensoren** mit Tropfschlaufe, Deckel mit Dichtung |

**Einbau von unten nach oben (Innenmaß):** Pumpe y 92–136 (Bauhöhe 42 mm) · Platine darüber · Zelle hochkant dahinter (59 mm Höhe, 5 mm Bautiefe). Maße stammen aus den final gewählten Bauteilen — siehe `../hardware/bom_entscheidung.md`. ⚠️ Die Pumpenparameter in `cad/params.py` (Ø32 / 44 mm / Lochbild 44 / Ø2,5) sind die Werte der **alten** Pumpe, werden von keinem CAD-Modul verwendet und sind nach dem Ausmessen der CONQUERALL nachzuziehen — deren **Ø ist nicht dokumentiert** (Bauhöhe 42 mm ist bestätigt).

**Pumpenposition:** Pumpe in der Wulst (oberhalb des Wassers), **Saugschlauch** durch den Kanal bis auf den Tankboden (y ≈ 8 mm, Ansaugkorb/Gewicht), **Druckschlauch** nach oben zum Verteilerring. Peristaltik ist selbstansaugend (Eigenschaft der Bauart; für diese Pumpe nicht ausdrücklich zugesichert → im Aufbau prüfen) → Position unkritisch. **Förderhöhe nachgerechnet (14.09.2026):** 200 mm Hub = 0,0196 bar gegen typ. 0,5–1 bar Pumpendruck → **20–40× Reserve**, Saughöhe 106 mm gegen „Ansaugbereich 0,5 m" = 4,7× Reserve. **Betrieb jetzt an der geregelten 5-V-Schiene** — ⚠️ **geändert 15.09.2026, Wandler seit 16.09.2026 ein Buck:** Bis dahin hing die Pumpe direkt an der 1S-Zelle, im Betrieb unterhalb ihrer Nennspannung (Messauftrag). Auf Wunsch bekommen **beide** Pumpen (Dosier- **und** Sauerstoffpumpe) **5 V**: **U_BUCK5 SY8113B** erzeugt eine geregelte **+5-V-Schiene (5,10 V)** aus dem **2S-Pack (6,0–8,4 V)**, jede Pumpe hängt über einen eigenen AO3400A (Q1/Q3) daran (`hardware/schaltplan_v1.md` §2.3); die Logik versorgt der zweite Buck (AP63203 → +3V3). Der **PWM-Softstart bleibt empfohlen** — nicht mehr wegen der Zellspannung (der 3-A-Buck deckt den 3-A-Anlauf), sondern wegen der knappen Reserve der 4,7-µH-Induktivität (Isat 4,0 A gegen 3,43 A Spitze, `docs/11_review-2s-umbau.md` §4.4). **Die Sauerstoffpumpe darf nicht dauerhaft laufen** (Pack in wenigen Stunden leer) und gehört **außerhalb des Gehäuses** (frische Luft).

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

### Lichtsensor (extern, ergänzt 13.09.2026)
- **Sitzt nicht auf der Platine**, sondern am Ende eines Kabels: Der Nutzer platziert den Sensor
  selbst am **Topfrand bzw. im Tent** — dort, wo das Growlicht tatsächlich ankommt (nicht im
  Schatten der Wulst).
- **Kabelabgang:** eigener kleiner Durchbruch/Schlitz in der Kragenauflage direkt neben dem
  Feuchtesensor-Kabel; die ersten ~150 mm zusammen mit diesem im vorhandenen **Kabelkanal (Ø 4 mm)**
  der Wulst führen und mit derselben **Tropfschlaufe** vor der Platinenkante enden. Der Kanal ist
  mit zwei dünnen Sensorleitungen nicht überfüllt.
- **Halteclip am Topfrand:** ein kleiner 3D-gedruckter Clip (Teil von `cad/params.py`) hält den
  Sensorkopf nach außen/oben zeigend am Kragenrand fest — lösbar, ohne den Sensor zu verkleben.
- **Kein eigenes Fenster in der Wulst nötig.** Das LED-Fenster im Deckel bleibt unverändert
  (es deckt weiterhin nur D2 und D5 ab). Der Sensor wird **außerhalb** der geschlossenen
  Elektronikkammer montiert, sodass auch die Dichtigkeit der Kammer unberührt bleibt.
- **Leitungslänge:** standardmäßig ~300–500 mm (analoger Spannungsausgang, hochohmig); bei
  Bedarf verdrillt mit GND führen. Der ADC-Pin ist durch R_LIGHT_S/C_LIGHT gegen Einstreuung
  geschützt (siehe `hardware/schaltplan_v1.md` §8).

### Erweiterungs-Kabelaustritte (14.09.2026, offener Gehäuse-Punkt)

Die freien GPIOs und der I²C-Bus sind auf **2,54-mm-Stiftleisten** herausgeführt (J8 I²C 4-pol,
J9–J15 Reserve je 3-pol). Damit steigt die Zahl der möglichen Kabelaustritte aus der dichten
Elektronikkammer:

| Stecker | Kabel | Bemerkung |
|---|---|---|
| J2 | Feuchtesensor | vorhanden |
| J7 | Lichtsensor | vorhanden (jetzt Stiftleiste) |
| J8 | I²C (VCC_EXT, SDA, SCL, GND) | neu |
| J9–J15 | 7 × Reserve (GND, VCC_EXT, SIG) | neu, nur nach Bedarf gesteckt |
| J6 | Taster-Rückleitung | vorhanden |

Das sind **11 Kabel** (der Auftrag nennt 9). Die Reserve-Stecker werden nicht alle gleichzeitig
benutzt; trotzdem braucht der Kabelaustritt in der Wulst **Platzreserve** für bis zu sieben
3-adrige Dupont-Leitungen plus I²C. Das ist bewusst als **offener Gehäuse-Punkt** geführt (siehe
§7) und im CAD nicht vorwegzunehmen.

---

## 5. Tankfüllung und LST-Ankerpunkte (14.09.2026)

### 5.1 Einfüllstutzen am Wassertank (`shell_lower`)

Bisher musste zum Nachfüllen die obere Schale (mit Innentopf) abgenommen werden. Jetzt sitzt am
unteren Segment ein **45° nach oben/außen geneigter Einfüllstutzen** auf der **−Y-Seite**
(Wulst-Gegenseite, dort ist nichts im Weg).

| Parameter | Wert |
|---|---|
| Achsneigung | 45° über der Horizontalen |
| Achshöhe an der Außenwand (r = 70) | z = 68 mm |
| lichte Bohrung | Ø 16 mm |
| Stutzenaußen-Ø / Länge (ab Außenwand, entlang der Achse) | Ø 25 / 22 mm |
| Mundmitte | r = 85,6 mm, z = 83,6 mm |
| Mundaufweitung (Trichterlippe) | Ø 22 mm über die letzten 3 mm |
| Öffnung in der Innenwand (r = 67) | z ≈ 54…76 mm (bleibt 2,7 mm unter der Rostauflage) |

Folgen:

- **Kein Abnehmen der Schale mehr**: Kappe (`fill_cap`) abziehen, mit Trichter einfüllen.
- Der Stutzen ist rechnerisch **stützfrei** (Achse und Mundaufweitung genau 45°) und ragt
  **nicht** in das Volumen der oberen Schale (oberhalb z = 90 bleibt seine Oberfläche bei
  r ≥ 74 mm; die obere Schale hat dort außen r = 70).
- Die Öffnung liegt mit ihrem unteren Rand unter dem max. Wasserstand — das ist gewollt: die
  Wasseroberfläche steht im Stutzen auf demselben Niveau wie im Tank, auslaufen kann sie erst
  am Mund.
- **Füllgrenze ≈ 76 mm = 1,07 L** (Konstruktionswert 71 mm = 1,0 L): läuft Wasser am Mund
  zurück, ist der Tank voll. Bleibt unter der Reserve von 82 mm (Überlaufschutz beim Rücklauf).
- **Kappe** `fill_cap`: Ø 30 (Rippen bis Ø 32), 8 mm hoch, Sackloch Ø 24,8 × 4 mm (Klemmsitz,
  0,2 mm Übermaß), **Lüftungsloch Ø 2 mm** im Deckel. Das Loch ist Pflicht: ein luftdicht
  verschlossener Tank würde die Pumpe gegen Unterdruck ziehen lassen.
- **Dichtigkeitsgrenze:** nur die Strecke bis zur Füllgrenze; der Tank selbst bleibt unverändert.

### 5.2 LST-Ankerlöcher im Kragen (`shell_upper`)

Für **Low-Stress-Training** werden Fäden gebraucht, die die Äste herunterziehen. Der Innentopf
scheidet als Anker aus (er sitzt 1 mm hinter der Außenschale, Wandlöcher wären von außen nicht
fädelbar und lägen unter der Substratoberfläche). Ankerpunkt ist deshalb der **Kragen**
(r 67…72, z 266…278) — das oberste, außen sichtbare Ringband:

| Parameter | Wert |
|---|---|
| Reihen | 2 (z = 269,5 und 274,5 mm) |
| Löcher je Reihe | 24, gleichmäßig über den Umfang (15°), zweite Reihe um 7,5° versetzt |
| Durchmesser | Ø 2,2 mm gezeichnet → gedruckt ca. 2,0 mm (Schnur 1,5–2 mm) |
| Freihaltung | nur um den Sensorkabel-Ausschnitt (+Y); **47 Löcher** (23 + 24) |

Die Löcher öffnen sich innen in den **Luftraum über dem Topfrand** (z > 266 mm) — dort ist kein
Substrat und kein Wasser, es kann also nichts austreten oder verstopfen. Die volle Kragenwand
bleibt oben und unten ≥ 2 mm stark.

**Betriebshinweis:** Vor dem Abnehmen der oberen Schale (z. B. Tankreinigung) die LST-Fäden
lösen — sie hängen am Kragen der oberen Schale.

---

## 6. Design-Folgen der Festlegungen (das ist die eigentliche inhaltliche Änderung)

### 6.1 Bottom-Watering → Top-Drip
Bisher: Wasser stand unten, Substrat zog per Kapillarwirkung. **Jetzt:** Pumpe fördert nach oben, das Wasser läuft von oben durch das Substrat und tropft unten wieder in den Tank.

Folgen:
- Der **Luftspalt (30 mm) bleibt Pflicht**, sonst steht der Topf dauerhaft im Wasser → Wurzelfäule und der Sensor meldet permanent „nass".
- Blähton-Schicht (25 mm) unten = Dränage **und** Partikelfilter gegen den Rücklauf in den Tank.
- Regelkreis: nach dem Pumpen dauert es **10–20 min** (nicht 5–15), bis das Wasser bei 75 mm Tiefe ankommt — erst danach darf „Feuchte steigt nicht → Tank leer" ausgewertet werden. Hysterese bleibt (Schwelle ±100–150 ADC).
- Der Sensor darf **nicht** zu flach sitzen: bei Top-Drip trocknet die oberste Schicht zuerst → zu hoher Sensor = Dauerpumpen.

### 6.2 Verbrauchsabschätzung / reicht 1 L?
Faustwert für 1,9-L-Topf: 0,15–0,35 L pro Gießvorgang, im Wachstum alle 3–5 Tage, in der Blüte alle 1–2 Tage.
→ **1,0 L ≈ 1–2 Wochen in der Vegetation, ≈ 3–6 Tage in der Blüte.** *(Schätzung, nicht gemessen — nach dem ersten Durchlauf mit echten Werten ersetzen.)*
→ Der Tank-leer-Alarm ist damit im Hochsommer/Blüte ein **echtes Betriebsereignis**, keine Ausnahme.

### 6.3 Salz- und Nährstoffverhalten (deutlich entschärft, aber nicht weg)
- Kein Dünger im Tank → die frühere Hauptfalle (Salzanreicherung durch Dünger-Rezirkulation) ist **entschärft**.
- Es bleibt: Rücklauf wäscht Nährsalze aus dem Substrat in den Tank → Wasser reichert langsam auf, Substrat magert unten aus.
- **Regel: Tankwasser alle 2 Wochen wechseln** (und dabei den Rücklauf verwerfen). Vorher/nachher Sensorwert notieren (Driftdiagnose).
- **Kein Flüssigdünger in den Tank** — bei einem Rezirkulationssystem konzentriert er sich auf. Düngen ausschließlich über das Substrat (Einmischen beim Topfen, Top-Dressing, gelegentlich von oben mit klarem Wasser nachspülen).

### 6.4 HF / Elektronik
- **Antenne des ESP32-C6-MINI-1** im obersten Wulstbereich halten, damit sie nach oben/außen frei strahlen kann: Espressif fordert wörtlich **≥ 15 mm Freistellung in alle Richtungen** innerhalb des Gehäuses, Modul möglichst am Platinenrand bzw. Platine unter/hinter der Antenne freigeschnitten. Die Wulstwand über der Antenne ist dünner auszuführen (Ziel ~2 mm statt 6 mm), obere ~25 mm der Kammer bauteilfrei. Abstand zu Akku/Metall: **≥ 10 mm** (eigene Auslegung, von Espressif nicht beziffert); Substrat (feucht, εr hoch) bedämpft → Wulst nach außen, nicht innen. **RF-Endtest am fertigen Gehäuse ist vorgeschrieben und noch offen.**
- Elektronikkammer dicht (Deckel + Dichtung, Kabeldurchführung als Tropfschlaufe) — sie sitzt zwar über dem Wasser, aber das Mikroklima am Topf ist feucht.

---

## 7. Offene Punkte

- [ ] **2S-Pack final** (1500–2500 mAh, **3-polig B− / Mittelabgriff / B+**, JST-XH-3P `C5258884`; **Schutz und Balancing macht die Platine** — ein BMS im Pack ist nicht nötig, aber unschädlich; Einbau-Maße gegen die Wulst prüfen — Auswahl offen, `docs/11_review-2s-umbau.md` §8.1)
- [ ] Pumpenabmessungen → Wulstbreite ggf. anpassen (parametrisch in `cad/` vorgesehen)
- [ ] Sensor-Länge real messen (Clone-Streuung ±5 mm) vor dem Einbau
- [ ] Optionale Tanküberwachung: float switch / Drucksensor am Tankboden (Redundanz zum Feuchte-Kriterium) — V2-Thema
- [ ] Kalibrierwerte `dry`/`wet` am echten Substrat aufnehmen (nach erstem Bewässerungsdurchlauf)
- [ ] **Taster-Bohrung** in der Außenwand festlegen (Position so, dass der Taster **ohne Öffnen** erreichbar ist) + Kabelweg für das zweiadrige Tasterkabel zur Platine
- [ ] **LED-Fenster für zwei LEDs:** D2 (Status) und D5 (Tank leer) — ein gemeinsames Fenster oder zwei kleine Lichtleiter; beide Plätze müssen **außerhalb** des antennenfreien Bereichs oben liegen
- [ ] **Halteclip + Kabeldurchbruch für den externen Lichtsensor** festlegen (Topfrand/Kragen, außerhalb der dichten Elektronikkammer) → `cad/params.py`
- [ ] **Kabelaustritt für die GPIO-/I²C-Erweiterung** (J8 + J9–J15) dimensionieren: Platzreserve für bis zu 8 Kabel (I²C + 7 Reserve, zusammen mit Feuchte/Licht/Taster 11) durch die Wulst, als mehrkammeriger oder breiterer Austritt mit Tropfschlaufe — offener Gehäuse-Punkt
- [ ] Firmware-Regel für D5 aufnehmen (blinken statt dauerleuchten: 1,3 mA dauerhaft wären 31 mAh/Tag und damit das 19-fache des Standby-Budgets)
- [ ] **Einfüllstutzen und Kappe am gedruckten Teil prüfen:** Klemmsitz (`cap_id` 24,8 auf Stutzen-Ø 25,0) je nach Drucker um ±0,2 mm anpassen; Füllgrenze messen (Soll ≈ 76 mm = 1,07 L)
- [ ] **LST-Ankerlöcher im Praxistest:** brauchbarer Schnurdurchmesser (1,5–2 mm) und Anzahl der tatsächlich genutzten Löcher/Reihen

