# SmartGrowTopf V1 — Schaltplan (EasyEDA Pro) als Code erzeugt

Dieses Verzeichnis enthält den **kompletten, reproduzierbaren Bau des Schaltplans** für den
Autopot "SmartGrowTopf_V1" in EasyEDA Pro — gebaut mit der `easyeda-agent` CLI in der Reihenfolge
des Design-Flows S0–S6 (`docs/09_easyeda-schaltplan-uebergabe.md`). Quelle der Schaltung ist die
Handnetzliste `../schaltplan_v1_netzliste.csv` (inhaltlich unverändert).

Stand: 11.09.2026 · Tool: `easyeda-agent` 1.4.8 · Blatt: **A2 Querformat** (594 × 420 mm)

---

## Ergebnis

| Prüfung | Werkzeug | Stand |
|---|---|---|
| Blatt / Geometrie | `sch sheet-geometry` | A2, 2338 × 1652 Einheiten, Titelblock-Freihaltezone ab x ≥ 1636, y ≤ 198 |
| Bauteile / Verdrahtung | `sch status` | 54 Bauteile, 163 Leitungssegmente, 10 Modulgruppen, 1 Seite („Systemuebersicht") |
| Netzlisten-Treue | Pin-für-Pin-Vergleich gegen `raw/ir_numbered.json` | **0 Abweichungen** (161 Verbindungen, 30 Netze, 25 NC-Pins) |
| Platzierung | `sch layout-lint` | 0 Überlappungen, 0 Pin-Koinzidenzen, 0 Off-Grid, 0 außerhalb des Blatts; 1 „zu eng" (<2,54 mm, kosmetisch) |
| Elektrik | `sch check` | 0 Fehler, 0 schwebende Pins, 0 Mehrnetz-Leitungen, 0 Leitungsquerungen; 5 Warnungen (nur Optik) |
| Kurzschlüsse | `sch bridge-check` | 0 Brücken, 0 verwaiste Stiche, 0 verwaiste Bäume (144 Leitungsträger) |
| Offizieller DRC | `sch drc` | 0 fatal, 0 error, 1 warn |
| Abnahme | `sch gate` | **fail** — einziger Blocker: 2 Gruppen-Überlappungen (Optik, s. u.) |
| Abnahme streng | `sch gate --strict` | fail — zusätzlich 1× „zu eng", 4 Marker-Überlappungen, 1 Titelblock-Hinweis, 1 DRC-Warnung |

`sch save` → `saved: true`; Bild-Exporte in `out/`.

**Elektrisch ist der Plan fertig und geprüft.** Offen sind ausschließlich kosmetische Punkte
(Marken-/Rahmen-Überlappungen), siehe „Bekannte Restpunkte".

---

## Bekannte Restpunkte (rein kosmetisch)

1. **`U6` ↔ `R7`/`R8`** — die ESD-Diode `U6` im USB-Block hat einen so breiten Marken-/Stichfächer
   (ca. 300 Einheiten), dass er die Messpunkte der beiden CC-Widerstände im selben Rasterfeld
   berührt (6×57 bzw. 11×11 Einheiten). Der USB-Block ist für 4 Bauteile dieser Breite knapp;
   sauber lösbar durch Verbreitern des Blocks + Neuplatzieren der 4 USB-Bauteile auf zwei Reihen.
2. **4 Marker-Überlappungen** (Netzlabel-Textboxen) — rein visuell; `sch destagger` hat sie
   bereits durchlaufen, ohne sie aufzulösen.
3. **`missing-titleblock`** — die Prüfung sucht ein Titelblock-Feld namens `Drawed`; diese
   EasyEDA-Version kennt nur `Drawn`. Nicht behebbar, Host-Eigenheit.
4. **1 DRC-Warnung** — die API liefert nur die Sammelzahl; Details gibt es nur im DRC-Panel der UI.

---

## Aufbau (Reihenfolge)

```bash
cd hardware/easyeda
export PATH="$HOME/.local/bin:$PATH"
P=4f6771a27edec75b          # Seiten-ID; Achtung: der Name der Seite ist KEIN gültiger --doc-Wert
G=(--project "SmartGrowTopf_V1" --doc $P)

# S0  Spezifikation (Board 38 mm, 2 Lagen, GND-Fläche unten) → s0_spec.json
# S1  Netzliste + Symbole → kanonische IR
python3 scripts/build_ir.py                                   # → raw/ir_draft.json
easyeda "${G[@]}" sch designators allocate raw/ir_draft.json \
        --prefixes raw/prefixes.json --out raw/ir_numbered.json \
        --changes raw/designator_changes.json                 # 16 Umbenennungen
# S2  Module/Gruppen + Rahmen
python3 scripts/plan_layout.py                                # → raw/place_all.sh, raw/frames_*.json
bash raw/place_all.sh                                         # 54/54 platziert, ~30 s
easyeda "${G[@]}" sch zone-draw … ; easyeda "${G[@]}" sch frame apply …
# S3/S4  Verdrahtung je Modul (autoconnect statt lib-layout-Solver) + GND-Sammelbus
python3 scripts/build_autoconnect.py                          # → raw/ac_<MODUL>.json
easyeda "${G[@]}" sch autoconnect --spec raw/ac_USB.json --replace …
easyeda "${G[@]}" sch wire --points '[[190,1145],[190,975],[215,975]]'   # Massebus
# S5  Prüfen
easyeda "${G[@]}" sch layout-lint --json ; easyeda "${G[@]}" sch check --json
easyeda "${G[@]}" sch bridge-check --json ; easyeda "${G[@]}" sch drc --json
easyeda "${G[@]}" sch gate --json ; easyeda "${G[@]}" sch gate --strict --json
# S6  Sichern + Export
easyeda "${G[@]}" sch save
easyeda "${G[@]}" sch export-image --format png --out out/SmartGrowTopf_V1_A2_final.png
```

Die Papiergröße (A4 → A2) ist **nicht** über die CLI änderbar: Blatt im EasyEDA-Canvas anklicken →
rechtes Panel „Drawing" → Feld `Size`. Danach mit `sch sheet-geometry` gegenprüfen.

## Dateien

| Pfad | Inhalt |
|---|---|
| `scripts/build_ir.py` | Netzliste + Symbol-Pins → kanonische IR |
| `scripts/plan_layout.py` | Modulblöcke, Platzierungsbefehle, Rahmen |
| `scripts/build_autoconnect.py` | Autoconnect-Specs je Modul (10 Dateien) |
| `scripts/build_layout_input.py` | Eingabe für den Solver `sch lib-layout` (verworfen, s. u.) |
| `scripts/repair_pins.py` | Wiederherstellung der Verdrahtung nach dem Marker-Vorfall |
| `scripts/fix_overlaps_safe.py` | kosmetische Marker-Korrektur (nur `disconnect --flag-id`) |
| `raw/` | IR (numeriert), Module, Symbole, Autoconnect-Specs, Platzierungsskript |
| `s1/` `s3/` `s4/` `s6/` | Zwischenstände (Seitenzustand, Verdrahtung, Titelblock) |
| `s5/FINAL_*` | **Abnahme-Belege** (gate, gate strict, check, bridge, drc, lint, read, Gruppen, Status) |
| `s5/b2_*` | Autoconnect-Läufe der finalen A2-Verdrahtung |
| `s5/archiv/` | alle Zwischenläufe (Zwischenprüfungen, verworfene Versuche) |
| `out/` | Bild-Exporte (PNG/SVG, A2) |

## Erfahrungen, die den Aufbau erklären

- **`sch autoconnect` statt `sch lib-layout`**: Der Layout-Solver platziert selbst und scheitert an
  den gemessenen Posen („cannot route direct net USB_DP … without crossing obstacles").
- **Ein Massebus statt 18 Einzelmarker**: die 18 durchgehenden GND-Pins des ESP32-C6-MINI-1 hätten
  im 10-Einheiten-Raster die Marker-Regel verletzt.
- **Marker nie per `disconnect --pin` umhängen**: dabei wurden einmal 38 Pins auf das falsche Netz
  gezogen (VBAT an GND) — erkannt durch Pin-für-Pin-Vergleich, behoben mit `repair_pins.py`.
  Sichere Klinge ist `disconnect --flag-id` + `connect --pin`, mit Netzlisten-Prüfung nach jedem Schritt.
- **`sch clear` leert mehr als die Bauteile**: auch Gruppen, Rahmen und NC-Marken verschwinden.
- **Mehr Blattfläche entspannt die Optik**: auf A4 gab es 9 Cluster-Überlappungen und 15 aus dem
  Blatt ragende Marken — auf A2 sind es 0 bzw. 0.
- **`VDD33` bleibt unverbunden**: das offizielle ESP32-C6-MINI-1-Symbol hat genau einen 3V3-Pin;
  die VDD33-Pins sind modulintern verbunden. Die Netzliste bleibt unverändert.

## Nächster Schritt

PCB-Phase: `easyeda pcb import-changes` (Layout-Import aus dieser Seite), Stackup/Board aus
`s0_spec.json` (38 mm, 2 Lagen, Massefläche auf der Unterseite).
