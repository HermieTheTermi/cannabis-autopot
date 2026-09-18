# 14 — Bauteilfläche und Platinengröße (Rechnung)

Stand: 18.09.2026 · Projekt SmartGrowTopf_V1
Nachbau: `python3 scripts/bauteilflaeche.py` (holt die Footprints live, cached in
`hardware/pcb/footprint_bbox.json`)

---

## 1. Frage

Wie groß ist die Fläche der Footprints in der aktuellen Stückliste, wie lang muss die
Platine bei **max. 54 mm Breite** werden, und was wäre die **optimale Größe**, wenn Länge
und Breite frei wählbar wären?

## 2. Datengrundlage (und wie belastbar sie ist)

| Größe | Quelle | Prüfung |
|---|---|---|
| Bestückung | `hardware/pcba_bom_jlc.csv` | 45 Zeilen, 116 Designatoren |
| **Bauteil-Fläche** | EasyEDA-Produkt-API `easyeda.com/api/products/<LCSC>/svgs`, Feld `bbox` des Footprints (`docType 4`), Einheit 0,01 inch → mm = Wert · 0,254 | Gegenprobe gegen das **live gemessene** `pcb dump` des alten Boards (40 Roheinheiten = 1 mm) — Abweichung 0,1–0,3 mm je Achse (das Live-Bbox enthält zusätzlich den Seidenrahmen) |
| Dichte-Anker | Diktiergerät-Board (Projekt `optimistic-hubble`), `easyeda/pcb_dump.json` | 37 Teile, 312,1 mm² Bauraum auf 19,9 × 36,7 mm = **731 mm² → 42,7 %**, beidseitig bestückt (oben 247 mm² / 28 Teile, unten 65 mm² / 27 Teile). Dieses Board ist laut Skill *am Limit der Autoroutbarkeit* |
| Mechanik | `cad/params.py` (`wc_*`, `wulst_*`) | siehe §6 |

**Nicht** in der Fläche enthalten: Freistellung der Antenne, Randaufschlag zur Platinenkante,
Lotpads J6 und das DNP-Bauteil R_UART (499 R).

## 3. Bauteilfläche — Summe **1.731,6 mm²** (114 bestückte Teile)

| Gruppe | Fläche | Anteil |
|---|---|---|
| Steckverbinder (USB-C + 6× JST-XH + 8× Stiftleiste) | 552,0 mm² | 31,9 % |
| Passive 0805/0603/1206 + Diode SOD-323 | 533,4 mm² | 30,8 % |
| MCU-Modul ESP32-C6-MINI-1 | 235,8 mm² | 13,6 % |
| ICs/MOSFETs (SOT-23, TSOT, VQFN, LFPAK) | 146,1 mm² | 8,4 % |
| Induktivitäten (2× 6×6, 1× 4,6×4,1) | 102,6 mm² | 5,9 % |
| Elko 100 µF + Sicherung 2410 | 88,6 mm² | 5,1 % |
| Taster (2× 5,1×5,1) | 73,0 mm² | 4,2 % |

Größte Einzelposten: ESP32-C6-MINI-1 235,8 · USB-C 81,1 · JST-XH-3P 2× 122,0 ·
100 µF-Elko 59,7 · 4,7 µH 2× 80,6 · 7× Stiftleiste 1×3 = 135,9 · 4× JST-XH-2P = 185,8 ·
20× 100 nF = 142,0 · 14× 1 k = 90,4.
Einzelwerte je Position: `python3 scripts/bauteilflaeche.py` (Abschnitt „Einzelposten").

## 4. Packmaß (theoretische Untergrenze, **nicht** routbar)

MaxRects-Packung aller Bauteil-Rechtecke, 90°-Drehung erlaubt, kleinste umschließende Höhe:

| Fuge | 54 mm breit → Länge ≥ | Füllung |
|---|---|---|
| 0,2 mm (nur Courtyard) | **38,4 mm** | 83,5 % |
| 0,6 mm | **44,6 mm** | 71,8 % |
| 1,0 mm | **54,4 mm** | 59,0 % |

Das ist eine reine Geometrie-Untergrenze: keine Routingkanäle, keine Antennenfreistellung,
keine Kantenzugänglichkeit. Zum Vergleich: das reale Referenzboard liegt bei 42,7 %.

## 5. Boardgröße aus der Belegungsdichte

Rechenweg: `Boardfläche = Σ Bauteilfläche / Dichte`, `Länge = Boardfläche / Breite`.
Die Dichte ist — wie beim Referenzboard gemessen — über die **volle Boardfläche** gerechnet
(Stecker-, Rand- und Freiräume stecken darin, es kommt **kein** zusätzlicher Randaufschlag
dazu). Alle Werte gelten für **alles auf einer Seite**.

| Dichte | Boardfläche | L bei W = 54 mm | Quadrat L = B |
|---|---|---|---|
| 30 % (bequem) | 5.772 mm² | 106,9 mm | 76,0 mm |
| 35 % | 4.947 mm² | 91,6 mm | 70,3 mm |
| 40 % | 4.329 mm² | 80,2 mm | 65,8 mm |
| **42,7 % (Referenzboard)** | **4.055 mm²** | **75,1 mm** | **63,7 mm** |
| 45 % | 3.848 mm² | 71,3 mm | 62,0 mm |

**Antwort Teil 1 — bei 54 mm Breite: 75 mm bei Referenzdichte.** Für die Umsetzung
zweilagig/einseitig sind **54 × 90 mm** zu empfehlen (35,6 % Belegung, §9.1) — die Länge
kostet in der Kammer nichts und die Routingluft ist auf 2 Lagen das knappe Gut.

**Antwort Teil 2 — freie Wahl: ≈ 65 × 65 mm** (Quadrat bei Referenzdichte), mit Reserve
70 × 70 mm. Die Form ist dabei der schwache Hebel: bei 4.329 mm² Fläche hat das Quadrat
65,8 × 65,8 mm (Umfang 263,2 mm), die 54er-Variante 54 × 80,2 mm (Umfang 268,3 mm) — nur
**2 % mehr Umfang** und 4 % mehr Diagonale. Was die Größe bestimmt, ist die *Fläche bzw.
Dichte*, nicht das Seitenverhältnis. Sinnvoll ist lediglich, das Verhältnis **≤ 2 : 1** zu
halten, damit Netze nicht quer über die ganze Platine laufen.

## 6. Gegenrechnung gegen die Mechanik (⚠ offener Punkt)

Der CAD-Innenraum der Wulst ist **nicht** 54 mm breit:

| Größe | Wert | Quelle |
|---|---|---|
| Wulst außen (x) | 60 mm | `wulst_w` |
| Elektronikkammer innen (x) | **40 mm** (`wc_x = 20`) | `shell_upper._wulst_cavity()` |
| Elektronikkammer innen (y, Tiefe) | 40 mm (`wc_y0 = 72` … `wulst_y_outer+2 = 112`) | dito |
| Elektronikkammer innen (z) | 152 mm (`wc_z0 = 92` … `wc_z1 = 244`) | dito |
| Pumpe darin | y 92–136 (44 mm), Platine darüber | `docs/02` §3 |

Folgen:

- Das Zielmaß **≤ 38 mm breit** aus `docs/02` passt in die heutige 40-mm-Kammer.
- Eine **54 mm breite** Platine passt nur, wenn die Wulst-Seitenwände von heute 10 mm
  (je Seite) auf **3 mm** abgedünnt werden — das Außenmaß 60 mm bleibt, die Kammer wird
  genau 54 mm. (Die Seitenwände sind nichttragend; `wulst_wall = 6 mm` gilt nur für
  Deckel/Boden.)
- **Länge:** die Kammer ist z 92…244 = 152 mm hoch, die Pumpe belegt davon 44 mm
  (z 92…136) → **108 mm für die Platine** (praktisch ~105 mm nutzbar).
- `params.py` führt `pcb_l = 52,0` / `pcb_w = 42,0` — **von keinem Modul verwendet**
  (Altbestand aus dem 1S-Stand, wie `xiao_*` und `batt_*`). Bei einer Neuverdrahtung der
  Wulst auf 54 mm mitziehen.

## 7. Hebel, wenn es kleiner werden muss

Nach Wirkung sortiert:

1. **Zweiseitige Bestückung** (Passive nach unten): Bei gleicher Struktur wie das
   Referenzboard trägt die Oberseite 1.222 mm² (Modul, Stecker, ICs, Taster, LEDs) bei
   33,8 % Belegung (Wert des Referenzboards auf dessen Oberseite) → Boardfläche 3.617 mm²
   → **54 × 67 mm**; über die Gesamtdichte gerechnet **54 × 75 mm** (§9.2).
   Die 509 mm² Passive landen unten bei ~14 % Belegung (Referenzboard: 8,9 %).
   Espressif rät ausdrücklich davon ab, **unter Modul/Antenne/Quarz** etwas auf die
   Unterseite zu legen — dieser Bereich bleibt einseitig.
2. **Passive zusammenfassen** (0805-Anteil 533 mm² = 31 %): 20× 100 nF + 14× 1 k +
   7× 22 µF = 282 mm². Jede eingesparte 0805 bringt 6,5–7,1 mm².
3. **Steckverbinder** (552 mm² = 32 %): 8 Stiftleisten 163 mm², 6× JST-XH 308 mm².
   Die Reserve-Stecker J9–J15 kosten allein 136 mm² (= 3,4 mm Platinenlänge).
4. **4 Lagen** statt 2: Espressif empfiehlt für das Modul 4 Lagen (L2 = GND, L3 = Power).
   Mehr Lagen erlauben eine höhere Belegung bei gleichbleibender Routbarkeit.

## 8. Quellen (Primär)

- Espressif, *ESP-Hardware-Design-Guidelines (ESP32-C6), PCB Layout Design*:
  „It is suggested to place the module's on-board PCB antenna outside the base board, and
  the feed point of the antenna close to the edge of the base board." /
  „A clearance of at least 15 mm is recommended in all directions." /
  „A four-layer PCB design is recommended." /
  „It is not recommended to place any components on this layer [BOTTOM]."
  → <https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html>
- Footprint-Bounding-Boxen: EasyEDA-Produkt-API, `bbox` des Footprint-Dokuments
  (`docType 4`), abgerufen am 18.09.2026; Rohdaten in `hardware/pcb/footprint_bbox.json`.
- Referenz-Board: `~/Projekte/optimistic-hubble/easyeda/pcb_dump.json` (live `pcb dump`).

## 9. Empfehlung — zwei Varianten

### 9.1 **Zweilagig, alle Bauteile oben (JLCPCB-Standard): 54 × 90 mm**

> **54 × 90 mm · 2 Lagen · 1 oz · Bestückung nur oben · GND-Fläche auf der Unterseite ·
> ESP32-C6-MINI-1 an der Oberkante mit über die Kante hinausragender Antenne**

| Kriterium | Wert bei 54 × 90 mm | Bewertung |
|---|---|---|
| Boardfläche | 4.860 mm² | — |
| Belegung Oberseite (alle 1.731,6 mm² / 114 Teile) | **35,6 %** | deutlich unter dem Referenz-Limit 42,7 % → auf 2 Lagen routbar |
| Geometrische Packgrenze (§4) | 54 × 44,6 mm (0,6 mm Fuge) | 90 mm = 2,0× der Packgrenze → reichlich Kanäle |
| Länge in der Kammer | 90 mm + ~6 mm Antennenüberstand = 96 mm von 108 mm | 12 mm Reserve |

- **Genau Espressifs 2-Lagen-Empfehlung:** „Layer 2 (BOTTOM): Do not place any components
  on this layer and keep traces to a minimum. Please make sure there is a complete GND plane
  for the chip, RF, and crystal." Einseitige Bestückung + Massfläche unten erfüllt das
  ohne Kompromiss — RF-seitig ist diese Variante die **bessere** als die zweiseitige.
- **Warum 90 mm und nicht 75 mm (Referenzdichte):** die Länge kostet in der Kammer nichts
  (108 mm verfügbar), Routingluft ist auf 2 Lagen dagegen das knappe Gut. 75 mm ginge nur
  bei 42,7 % Belegung, also am gemessenen Limit.
- **Preis der Variante:** die Oberseite nimmt jetzt auch die 79 Passiven auf
  (509 mm² = 10,5 % der Boardfläche zusätzlich oben). Deshalb: Passive in dichten Trauben
  direkt neben ihren IC, Stecker an die beiden Längskanten (hinter ihnen läuft nichts),
  GND via-stitching.
- **Falls das Routen klemmt:** dieselbe Platine in **4 Lagen** bestellen — gleiche Outline,
  gleiche Bestückung, nur zwei Innenlagen dazu (bei JLC ein paar Dollar). Keine mechanische
  Änderung, kein neues Gehäuse. Zweite Option: die 7 Reserve-Stiftleisten J9–J15 streichen
  (136 mm² ≈ 3 mm Länge).

### 9.2 **Vierlagig, Passive auf der Unterseite (kompakt): 54 × 75 mm**

| Kriterium | Wert bei 54 × 75 mm | Bewertung |
|---|---|---|
| Belegung Oberseite (1.222 mm²) | 30,2 % | Referenzboard-Oberseite: 33,8 % |
| Belegung Unterseite (509 mm²) | 12,6 % | Referenzboard-Unterseite: 8,9 % |
| Gesamt | 42,7 % | = Referenz-Limit |
| Länge in der Kammer | 75 + 6 = 81 mm von 108 mm | 27 mm Reserve |

Kürzer, aber teurer (4 Lagen + zweite Bestückungsseite) und Espressif rät von Bauteilen auf
der Unterseite im Modul-/Antennenbereich ab (dort freihalten). **Nur wählen, wenn die Länge
wirklich drückt** — sie drückt hier nicht.

### 9.3 Was für beide gilt

- **54 mm Breite:** die Wulst ist außen 60 mm breit → mit 3 mm Seitenwänden genau 54 mm innen.
  Schmaler geht nicht: mit den heutigen 40 mm Kammerbreite bräuchte die Platine bei gleicher
  Belegung **101 mm** Länge (42,7 % Belegung — also schon am Limit) bis **124 mm** (35 %) und
  passt damit **nicht** in die 108 mm über der Pumpe. Bei der alten Zielbreite ≤ 38 mm wären
  es 107 mm (Limit) bzw. 130 mm (35 %). Die Kammer *muss* also auf 54 mm verbreitert werden
  (`params.py`: `wc_x` 20 → 27).
- **Kein Quadrat:** für ~65 × 65 mm müsste die Wulst auf ~72 mm Außenbreite wachsen — mehr
  Gehäusevolumen, mehr Material, Antenne näher am feuchten Substrat — bei 2 % Umfangsgewinn.
  Die Form ist der schwache Hebel (§5), die Fläche zählt.
- **Antenne:** Modul an die Oberkante, Antennenbereich über die Kante hinaus (Espressif:
  „place the module's on-board PCB antenna outside the base board"), 15 mm Freistellung in
  der Kammer, Wulstwand darüber dünner (`docs/02` §6.4). Der Überstand geht in die Länge ein.
- **USB-C** braucht zwingend eine Platinenkante (die Öffnung liegt in der Platinenebene) —
  Durchbruch in der Wulstwand vorher festlegen.



## 10. Offene Punkte

- [ ] Wulst-Seitenwände auf 3 mm abdünnen und Kammer auf 54 mm verbreitern — Zeichnung
      `cad/params.py` + `shell_upper.py` (`wc_x` von 20 auf 27) anpassen, Deckel mitziehen.
- [ ] Umsetzen: **54 × 90 mm**, 2 Lagen, Bestückung nur oben, GND-Fläche unten (§9.1).
      `s0_spec.json` steht schon auf 2 Lagen/top — nur `widthMm: 38` → 54 und die
      Boardlänge ergänzen.
- [ ] Passiv-Platzierung prüfen: mit einseitiger Bestückung liegen 1.731,6 mm² auf der
      Oberseite (35,6 %). Falls das Routen klemmt → gleiche Outline in 4 Lagen bestellen.
- [ ] `pcb_l` / `pcb_w` in `params.py` auf den tatsächlichen Entwurf setzen (heute unbenutzt).
- [ ] Antennenfreistellung (15 mm in alle Richtungen, `docs/02` §6.4) bei der endgültigen
      Platzierung gegen die Wulstwand prüfen; RF-Endtest bleibt vorgeschrieben.
