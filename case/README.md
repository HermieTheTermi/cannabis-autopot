# Gehäuse-CAD (OpenSCAD) — Smart Grow Topf V1

Parametrisches Modell nach `../docs/02_architektur-und-geometrie.md`.
Alle Maße stehen zentral in **`params.scad`**; Änderungen nur dort.

## Dateien

| Datei | Bauteil | STL (Export) |
|---|---|---|
| `params.scad` | alle Parameter | – |
| `modules.scad` | Geometrie-Module | – |
| `shell_upper.scad` | Aussenschale oben (Wulst + Kragen + Stecksockel) | `shell_upper.stl` |
| `shell_lower.scad` | Aussenschale unten (Wassertank + Steckzapfen) | `shell_lower.stl` |
| `outer_shell.scad` | Aussenschale gesamt (nur Vorschau, 278 mm) | `outer_shell.stl` |
| `inner_pot.scad` | Innentopf mit Gießfüßen + Drainage | `inner_pot.stl` |
| `grid.scad` | Auflagerost / Blähton-Rückhalt | `grid.stl` |
| `distribution_ring.scad` | Verteilerring (Top-Drip) | `distribution_ring.stl` |
| `wulst_lid.scad` | Wulstdeckel (Dichtungsnut, USB-C, LED) | `wulst_lid.stl` |
| `cover.scad` | optionale Substrat-Abdeckung | `cover.stl` |
| `case.scad` | Gesamt-/Drucklayout aller Teile | `gesamt.stl` |
| `assembly.scad` | Zusammenbau-Ansicht (montiert, inkl. Sensormarker + Schlauch-/Kabelweg) | `assembly.stl` |

## Segmentierung (Bauraum 220 × 220 × 250 mm)

Gesamthöhe 278 mm > 250 mm → Aussenschale zweigeteilt.

| Teil | Bauraum (X × Y × Z) | passt |
|---|---|---|
| shell_upper | 144 × 184 × 188 | ✅ |
| shell_lower | 140 × 140 × 96 | ✅ |
| inner_pot | 132 × 132 × 180 | ✅ |
| distribution_ring | 105 × 113 × 16 (Stutzen +Y) | ✅ |
| grid | 132 × 132 × 4 | ✅ |
| wulst_lid | 60 × 160 × 4 | ✅ |
| cover | 136 × 136 × 3 | ✅ |
| outer_shell (Vorschau) | 144 × 184 × **278** | ❌ nur Zusammenbau |

Verbindung: Steckzapfen Ø136 / Sockel Ø137,2 an der Trennebene **z = 90 mm**
(0,6 mm radial Spiel). Dichtung optional mit Silikon.

## Druck

- **Schichthöhe** 0,20 mm · **Wandzahl** 3 (≈ 1,2 mm) · Top/Bottom ≥ 4.
- Material PLA oder PETG. **Keine Stützstrukturen nötig** – Wulstboden ist als
  45°-Fase ausgeführt, Kragen/Deckel sitzen auf ebenen Flächen.
- Wandstärken: Mantel 3,0 mm · Innentopf 2,5 mm · Wulst 6 mm · Ring 2,2 mm.
- Ausrichtung: Schalen und Innentopf **stehend** (Wulst/Öffnung nach außen,
  Füße nach unten); Rost, Ring, Deckel und Abdeckung **flach**.

## Montage

1. `shell_lower` aufstellen, `grid` auf den Auflagering (z = 79–82) einlegen.
2. `shell_upper` auf den Zapfen stecken (ggf. Silikon-Dichtnaht).
3. Saugschlauch vom Wulst durch den 6 × 6-Kanal in den Tank führen, Filtergewicht
   anhängen; Pumpe anschließen; Druckschlauch durch die Ø-6,5-Bohrung oben nach
   außen zum Verteilerring.
4. `inner_pot` (Füße nach unten auf den Rost) einsetzen, 25 mm Blähton als
   Drainage, darüber Substrat.
5. `distribution_ring` auf die Substratoberfläche legen (Stutzen zeigt nach **+Y**
   zur Wulst). Druckschlauch von der Ø-6,5-Bohrung der Wulst über den Kragen,
   durch den 6 × 6-Schlauchdurchlass am Innentopfrand (+Y), zum Schlauchstutzen
   führen und aufstecken — **nicht** durch den Sensorkabel-Ausschnitt am Kragen.
6. Sensor bei r ≈ 55 mm auf 75 mm Tiefe stecken, Kabel über die
   Kragenaussparung in den Ø-4,5-Kabelkanal führen (Tropfschlaufe vor dem Eintritt).
7. Elektronik einlegen (Pumpe unten, PCB darüber, Zelle dahinter), Deckel mit
   Dichtung aufsetzen und mit 4 × M2,5 verschrauben.
8. `cover` optional auf den Kragen legen.

## Annahmen / Abweichungen

- **Wulstboden 45°** abgefast (statt waagerecht), damit ohne Stützdruck möglich.
  Die Wulst bleibt nominal y = 90–250; Pumpe/Zelle sitzen an der Außenwand erst
  ab y ≈ 112 – weiterhin deutlich über dem max. Wasserstand (71 mm).
- **Drei Durchführungen statt zwei**: Kabelkanal Ø4,5 (z = 246) und Schlauchkanal
  6 × 6 (z = 100) liegen in der Innenwand; der **Druckschlauch** verlässt die
  Wulst zusätzlich oben durch Ø6,5. So bleibt je Kanal ein separater Querschnitt,
  und Saug-/Druckschlauch kollidieren nicht.
- **USB-C und LED** sitzen im Wulstdeckel (er verschließt die Frontöffnung).
- **Sensorkabel** läuft über den Kragen (7 mm Ausschnitt, z = 266–278) nach außen.
- **Rostlochung** Ø4 mm / 9 mm Raster (hält Blähton ≥ 8 mm), ungelochter Rand 4 mm,
  Ø14-Durchlass für den Saugschlauch bei r = 52.
- **Verteilerring** Ø105 außen, 10 Austrittsbohrungen Ø2,6 senkrecht nach unten/
  innen (r = 43), Schlauchstutzen 4/6 mm. Stutzenlänge **7,5 mm** (vorher 12),
  zeigt nach **+Y** (Richtung Wulst). Gemessener **max. Ringradius 60,1 mm**
  (Stutzenaußenkante) → **3,4 mm** Luft zur Innentopfwand (r = 63,5). Der
  Druckschlauch passiert den Kragen oben und den **6 × 6-Schlauchdurchlass**
  am Innentopfrand (+Y); Sensor- und Schlauchauschnitt bleiben getrennt.
- Montagehilfen für Pumpe/Akku sind als Footprint-Parameter (`pump_d`, `batt_*`,
  `xiao_*`) hinterlegt; im Gehäuse sind nur die Deckel-Schraubposten (M2,5)
  ausgeführt – die Zelle wird geklemmt/gebändert.
- Tank: 1,0 L bei 71 mm Füllstand, Innen-Ø 134 (141 cm²), Reserve bis 82 mm.

## Render / Export

```bash
cd tools/oscad-render
node render.mjs ../../case/shell_upper.scad       -o ../../case/export/shell_upper.stl
node render.mjs ../../case/shell_lower.scad       -o ../../case/export/shell_lower.stl
node render.mjs ../../case/inner_pot.scad         -o ../../case/export/inner_pot.stl
node render.mjs ../../case/grid.scad              -o ../../case/export/grid.stl
node render.mjs ../../case/distribution_ring.scad -o ../../case/export/distribution_ring.stl
node render.mjs ../../case/wulst_lid.scad         -o ../../case/export/wulst_lid.stl
node render.mjs ../../case/cover.scad             -o ../../case/export/cover.stl
node render.mjs ../../case/outer_shell.scad       -o ../../case/export/outer_shell.stl   # Vorschau
node render.mjs ../../case/case.scad              -o ../../case/export/gesamt.stl        # Gesamtlayout
node render.mjs ../../case/assembly.scad          -o ../../case/export/assembly.stl      # Zusammenbau-Ansicht
```

Alle zehn Renders laufen mit Exit-Code 0. `case/export/` ist per `.gitignore`
ausgenommen, versioniert werden nur die `.scad`-Quellen.
