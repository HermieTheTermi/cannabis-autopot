# SmartGrowTopf V1 — Schaltplan (EasyEDA Pro) als Code erzeugt

Dieses Verzeichnis enthält den **kompletten, reproduzierbaren Bau des Schaltplans** für den
Autopot "SmartGrowTopf_V1" in EasyEDA Pro — gebaut mit der `easyeda-agent` CLI in der Reihenfolge
des Design-Flows S0–S6 (`docs/09_easyeda-schaltplan-uebergabe.md`). Quelle der Schaltung ist die
Handnetzliste `../schaltplan_v1_netzliste.csv`.

> **Stand-Hinweis (13.09.2026):** Der hier eingecheckte EasyEDA-Bau ist ein **Schnappschuss vom
> 11.09.2026** (30 Netze) und enthält **weder den Lichtsensor (J7) noch die Erweiterungsstecker
> J8–J10/TP7–TP11**. Die **Quellnetzliste hat heute 45 Netze / 64 bestückte Positionen**. Der
> EasyEDA-Bau ist damit **veraltet und muss aus der aktuellen Netzliste neu erzeugt werden**;
> die Netzklassen-Spezifikation `netclass_spec.json` ist bereits auf 45 Netze nachgezogen.
> Die unten genannten Prüfzahlen beziehen sich auf den historischen Bau.
>
> **Nachtrag 13.09.2026:** Die Generator-Artefakte unter `raw/` sind aus der neuen Netzliste
> **neu erzeugt** (45 Netze, 75 Bauteile inkl. 5 Lötpads, 64 BOM-Positionen, 213 Verbindungen;
> `check_ir_netlist.py` 0 Abweichungen, inkl. TP7–TP11). Die **Live-Seite in EasyEDA wurde
> dabei nicht angefasst** — S1–S6 sind vom Anwender noch anzuwenden.
> **Nachbesserung 13.09.2026:** Die Device-UUIDs der neuen Teile `C157925`/`C15127` sind
> live aufgelöst (Bibliothek `0819f05c4eef4c71ace90d822a990e87`, `a65b5fe9…` bzw.
> `f58385f6…`) und im Generator fest eingetragen. `raw/no_place.json` ist leer; TP7–TP11
> werden als Lötpads im MCU-Block platziert (`place_all.sh`: **75** Platzierungszeilen) und
> als `netport` verdrahtet (Autoconnect **213** Verbindungen, **0** übersprungen).
>
> **Nachbesserung 13.09.2026 (Massepads):** Die frühere Sammelzeile `U1 1/2/11/14/36-53` in
> der Netzliste ist in Einzelzeilen aufgelöst. Das ESP32-C6-MINI-1-Symbol hat **keinen
> Bus-/Sammelpin** — alle 22 GND-Pads (1, 2, 11, 14, 36–53) haben live geprüfte eigene
> Koordinaten und werden einzeln verdrahtet. Der frühere Autoconnect-Skip der „18
> U1-GND-Buspins" ist entfernt: Die IR bleibt bei 213 Verbindungen, die Autoconnect-Specs
> steigen von 195 auf **213**, übersprungen von 18 auf **0**. Die Zeile `EPAD (Pin 49)` ist
> als Kommentar erhalten (Pad 49 ist in 36–53 enthalten, kein Phantompin).

Stand des eingecheckten Baus: 11.09.2026 · Tool: `easyeda-agent` 1.4.8 · Blatt: **A2 Querformat** (594 × 420 mm)

---

## Ergebnis

| Prüfung | Werkzeug | Stand |
|---|---|---|
| Blatt / Geometrie | `sch sheet-geometry` | A2, 2338 × 1652 Einheiten, Titelblock-Freihaltezone ab x ≥ 1636, y ≤ 198 |
| Bauteile / Verdrahtung | `sch status` | 54 Bauteile, 163 Leitungssegmente, 10 Modulgruppen, 1 Seite („Systemuebersicht") |
| Netzlisten-Treue | Pin-für-Pin-Vergleich gegen `raw/ir_numbered.json` | **0 Abweichungen** (161 Verbindungen, **30 Netze** [historisch], 25 NC-Pins) |
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
# S1  Netzliste + Symbole → kanonische IR (Designator-Nummerierung offline nachgebildet)
python3 scripts/build_ir.py                                   # → raw/ir_draft.json, raw/ir_numbered.json,
                                                              #   raw/no_place.json  (27 Umbenennungen)
python3 scripts/check_ir_netlist.py                           # Pin-für-Pin: 0 Abweichungen
# S2  Module/Gruppen + Rahmen
python3 scripts/plan_layout.py                                # → raw/place_all.sh, raw/frames_*.json
bash raw/place_all.sh                                         # 75/75 platziert (inkl. TP7–TP11 als Lötpads)
easyeda "${G[@]}" sch zone-draw … ; easyeda "${G[@]}" sch frame apply …
# S3/S4  Verdrahtung je Modul (autoconnect statt lib-layout-Solver), inkl. 22 Einzel-GND-Pads
python3 scripts/build_autoconnect.py                          # → raw/ac_<MODUL>.json
easyeda "${G[@]}" sch autoconnect --spec raw/ac_USB.json --replace …
easyeda "${G[@]}" sch autoconnect --spec raw/ac_MCU.json --replace …   # U1 1,2,11,14,36–53 GND einzeln
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
| `scripts/build_ir.py` | Netzliste + Symbol-Pins → kanonische IR + Designator-Nummerierung |
| `scripts/check_ir_netlist.py` | Selbstkonsistenz IR ↔ Handnetzliste (Pin für Pin) |
| `scripts/plan_layout.py` | Modulblöcke, Platzierungsbefehle, Rahmen |
| `scripts/build_autoconnect.py` | Autoconnect-Specs je Modul (12 Dateien) |
| `scripts/build_layout_input.py` | Eingabe für den Solver `sch lib-layout` (verworfen, s. u.) |
| `scripts/repair_pins.py` | Wiederherstellung der Verdrahtung nach dem Marker-Vorfall |
| `scripts/fix_overlaps_safe.py` | kosmetische Marker-Korrektur (nur `disconnect --flag-id`) |
| `scripts/netclass_spec.py` | Leiterbahnbreiten für die PCB-Phase (IPC-2221A) → `netclass_spec.json` |
| `scripts/pcb_widths.py` | Breiten auf der Platine prüfen/nachziehen (`--check`/`--apply`/`--route-plan`/`--selftest`) |
| `raw/` | IR (numeriert), Module, Symbole, Autoconnect-Specs, Platzierungsskript |
| `s1/` `s3/` `s4/` `s6/` | Zwischenstände (Seitenzustand, Verdrahtung, Titelblock) |
| `s5/FINAL_*` | **Abnahme-Belege** (gate, gate strict, check, bridge, drc, lint, read, Gruppen, Status) |
| `s5/b2_*` | Autoconnect-Läufe der finalen A2-Verdrahtung |
| `s5/archiv/` | alle Zwischenläufe (Zwischenprüfungen, verworfene Versuche) |
| `out/` | Bild-Exporte (PNG/SVG, A2) |

## Erfahrungen, die den Aufbau erklären

- **`sch autoconnect` statt `sch lib-layout`**: Der Layout-Solver platziert selbst und scheitert an
  den gemessenen Posen („cannot route direct net USB_DP … without crossing obstacles").
- **Kein Buspin am Modul**: das ESP32-C6-MINI-1-Symbol hat für die durchgehenden Massepads
  36–53 je eine eigene Pin-Nummer (live geprüft, keine Stapel-/Buspins). Die 18 Pads werden
  daher einzeln verdrahtet; ein Sammelpin existiert nicht.
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
**Leiterbahnbreiten sind vorab festgelegt** (`netclass_spec.json`, Erklärung in
`docs/10_pcb-leiterbahnbreiten.md`): VBAT / PUMP_N / VBUS 0,5 mm, +3V3 0,4 mm, Signale
0,25 mm, Masse als Fläche. `PUMP_N` muss dabei explizit mit `pcb track --width 20`
gelegt werden — die Namensheuristik des Tools hält es für ein Signal.
