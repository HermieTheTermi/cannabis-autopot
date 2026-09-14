# Gehäuse-CAD (build123d) — Smart Grow Topf V1

Parametrisches Modell in **Python/build123d** (ersetzt das frühere OpenSCAD-Modell in `case/`,
das am 14.09.2026 abgelöst wurde; die SCAD-Quellen liegen weiter in der Git-Historie).
Alle Maße stehen in **`params.py`** — nichts in den Bauteilen hart verdrahten.

## Aufbau

| Datei | Inhalt |
|---|---|
| `params.py` | alle Maße, benannt (Geometrie-Wahrheit: `../docs/02_architektur-und-geometrie.md`) |
| `lib.py` | gemeinsame Helfer: `rrect`, `hole_grid`, Wulst-Grundriss, Stutzenachse, Zylinderkette, Sonden-Messung |
| `parts/shell_upper.py` | Aussenschale oben (Wulst + Kragen + 47 LST-Ankerlöcher) |
| `parts/shell_lower.py` | Aussenschale unten (Wassertank + Einfüllstutzen + Steckzapfen) |
| `parts/inner_pot.py` | Innentopf mit Gießfüßen, Drainage und Schlauchdurchlass |
| `parts/grid.py` | Auflagerost / Blähton-Rückhalt |
| `parts/distribution_ring.py` | Verteilerring (Top-Drip) |
| `parts/wulst_lid.py` | Wulstdeckel (Dichtungsnut, USB-C, LED) |
| `parts/cover.py` | optionale Substrat-Abdeckung |
| `parts/fill_cap.py` | Kappe auf dem Einfüllstutzen (Klemmsitz, Lüftungsloch) |
| `assembly.py` | Baugruppe: alle Teile über benannte `RigidJoint`s + `connect_to()` verbunden |
| `export_all.py` | baut, prüft und exportiert **alle** Bauteile (STL + STEP) |

Konvention je Bauteil: `NAME`, `build()` → `Part`, `check(part)` → Asserts + Kennzahlen.
`export_all.py` findet die Module selbst (`parts/*.py`) und bricht mit Exit-Code 1 ab, wenn
eine Prüfung nicht hält.

## Bauen und prüfen

```bash
cd ~/Projekte/cannabis-autopot
/Users/manuel/.venvs/cad/bin/python cad/export_all.py   # alle Teile: prüfen + cad/export/*.stl + *.step
/Users/manuel/.venvs/cad/bin/python cad/assembly.py     # Baugruppe + Interferenzprüfung
f3d --output=/tmp/teil.png --resolution=1100,800 cad/export/teil.stl   # Ansicht erzeugen
```

Explosionsansicht aller 8 Druckteile: `cad/exploded.py` schreibt `cad/export/exploded.step`/`.stl`, gerendert z. B. mit `f3d --output=/tmp/exploded.png --resolution=1500,1100 --camera-position=-850,-1130,1150 --camera-focal-point=0,0,380 --camera-view-up=0,0,1 cad/export/exploded.stl`.

`cad/export/` ist Build-Artefakt und per `.gitignore` ausgenommen — versioniert werden nur die
Python-Quellen.

## Bauteile, Drucklage, Bauraum (220 × 220 × 250 mm)

| Teil | Bauraum (X × Y × Z) | passt |
|---|---|---|
| shell_upper | 144 × 184 × 188 | ✅ (Drucklage: um 90 mm nach unten verschoben, Kragen oben) |
| shell_lower | 140 × 140 × 96 | ✅ |
| inner_pot | 132 × 132 × 180 | ✅ (Gießfüße ragen nach unten, z −30…150) |
| distribution_ring | 105 × 113 × 16 (Stutzen +Y) | ✅ |
| grid | 132 × 132 × 4 | ✅ |
| wulst_lid | 60 × 160 × 4 | ✅ |
| cover | 136 × 136 × 3 | ✅ |
| fill_cap | 32 × 32 × 8 | ✅ |

Verbindung der beiden Schalensegmente: Steckzapfen Ø 136 / Sockel Ø 137,2 an der Trennebene
**z = 90 mm** (0,6 mm radial Spiel), Dichtung optional mit Silikon.

## Druck

- **Schichthöhe** 0,20 mm · **Wandzahl** 3 (≈ 1,2 mm) · Top/Bottom ≥ 4.
- Material PLA oder PETG. **Keine Stützstrukturen nötig** — Wulstboden und Einfüllstutzen sind
  als 45°-Fasen ausgeführt, alles andere steht auf ebenen Flächen.
- Ausrichtung: Schalen und Innentopf **stehend** (Kragen/Wulst bzw. Füße nach unten), Rost,
  Ring, Deckel, Abdeckung und Kappe **flach** (Kappe mit der Öffnung nach oben).
- Die LST-Löcher im Kragen sind Ø 2,2 mm gezeichnet → gedruckt bleiben ca. 2,0 mm (nimmt
  1,5–2 mm Schnur). Sie sind im Ausdruck nicht zuzustopfen notwendig; bei Bedarf mit einer
  Nadel nachfädeln.

## Montage

1. `shell_lower` aufstellen, `grid` auf den Auflagering (z = 79–82) einlegen.
2. `shell_upper` auf den Zapfen stecken (ggf. Silikon-Dichtnaht).
3. Saugschlauch vom Wulst durch den 6 × 6-Kanal in den Tank führen, Filtergewicht anhängen;
   Pumpe anschließen; Druckschlauch durch die Ø-6,5-Bohrung oben nach außen zum Verteilerring.
4. `inner_pot` (Füße nach unten auf den Rost) einsetzen, 25 mm Blähton als Drainage, darüber
   Substrat.
5. `distribution_ring` auf die Substratoberfläche legen (Stutzen zeigt nach **+Y** zur Wulst),
   Druckschlauch aufstecken — **nicht** durch den Sensorkabel-Ausschnitt am Kragen führen.
6. Feuchtesensor bei r ≈ 55 mm auf 75 mm Tiefe stecken, Kabel über die Kragenaussparung in den
   Ø-4,5-Kabelkanal führen (Tropfschlaufe vor dem Eintritt).
7. Elektronik einlegen, `wulst_lid` mit Dichtung aufsetzen, mit 4 × M2,5 verschrauben.
8. `fill_cap` auf den Mund des Einfüllstutzens drücken (Klemmsitz, Lüftungsloch bleibt frei).
9. `cover` optional auf den Kragen legen.

**Wasser nachfüllen:** Kappe abziehen, durch den 45°-Stutzen auf der Wulst-Gegenseite (−Y)
einfüllen (Trichter empfohlen). Kein Abnehmen der oberen Schale mehr nötig. Läuft Wasser aus dem
Mund zurück, ist der Tank voll (≈ 1,07 L, Konstruktionswert 1,0 L bei 71 mm = max. Wasserstand).

**LST (Low-Stress-Training):** Fäden durch die Löcher im Kragen fädeln (2 Reihen, versetzt,
47 Löcher, Ø 2,2 mm) — von außen erreichbar, innen öffnen sie sich in den Luftraum über dem
Topfrand, also nicht im Substrat. **Vor dem Abnehmen der oberen Schale die Fäden lösen.**

## Annahmen / Abweichungen gegenüber der SCAD-Vorlage

- **LST-Löcher korrigiert:** In der SCAD-Vorlage war die Freihaltung am Sensorkabel-Ausschnitt um
  90° verdreht (sie sparte bei 180° aus, gemessen: 44 Löcher). Jetzt 24 Positionen je Reihe,
  zweite Reihe um 7,5° versetzt, ausgespart wird nur, was im Kragenausschnitt (+Y) läge →
  **23 + 24 = 47 Löcher**.
- Der Einfüllstutzen ist gegenüber dem SCAD-Stand 4 mm länger (`fill_len` 22 statt 18) und die
  Kappe flacher (8 mm, Nut 4 mm), weil der Kappenrand sonst an der Tankwand anlag (im SCAD
  224 mm³ Überlappung, jetzt nur noch der Klemmsitz).
- Zwei Überlappungen in der Baugruppe sind **von der SCAD-Vorlage geerbt** und bewusst nicht
  geändert: die Wulst-Tropfkante berührt die Innentopfwand (≈ 14,5 mm³) und der Rost berührt
  den Kappenrand (≈ 0,1 mm³). Beide sind in der Fertigung unkritisch (Toleranz/Spiel).
- Die Ansichtsdateien der Vorlage (`outer_shell`, `case`-Gesamtlayout) sind **nicht** portiert;
  die Übersicht liefert `assembly.py` (montierte Baugruppe als STEP/STL).
