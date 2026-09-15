# SmartGrowTopf V1 — Schaltplan (EasyEDA Pro) als Code erzeugt

Dieses Verzeichnis enthält den **kompletten, reproduzierbaren Bau des Schaltplans** für den
Autopot "SmartGrowTopf_V1" in EasyEDA Pro — gebaut mit der `easyeda-agent` CLI in der Reihenfolge
des Design-Flows S0–S6 (`docs/09_easyeda-schaltplan-uebergabe.md`). Quelle der Schaltung ist die
Handnetzliste `../schaltplan_v1_netzliste.csv`.

> **Stand 15.09.2026 (Sauerstoffpumpe + 5-V-Boost, Neuaufbau der Seite):** Die Generatorkette läuft
> wieder vollständig und die Seite wurde **von Grund auf neu gebaut** (kein Flicken, kein manuelles
> Umplatzieren): **93 Bauteile, 54 Netze, 262 Verbindungen, 13 Modulgruppen, 13 Modulrahmen**.
> `check_ir_netlist.py` = **0 Abweichungen**; `plan_layout.py` = kein Planungsproblem (Blattnutzung
> **78,7 %**); `check_plan_fit.py` = **Exit 0** (0 überlappende Rahmen, kleinster Volumenabstand 25);
> `build_autoconnect.py` = **13 Spec-Dateien mit 261 Verbindungen**.
> Live: **93 Bauteile platziert (0 FAIL)**, 13 Rahmen + 13 Titel gezeichnet (die Rücklese-Prüfung
> meldet `verified:false` wegen des bekannten Vorzeichenfehlers — `sch clear --dry-run` beweist
> `rectangles: 13, texts: 13`), 13 Gruppen angelegt, **261 von 262 Pins verdrahtet**,
> **Pin-für-Pin-Diff gegen die Ziel-IR = 0 Abweichungen**, `sch gate`: `layout-lint` pass (0/0),
> `check` pass, `bridge-check` pass (**0 Waisen**), `drc` pass — **einziger Restpunkt** ist ein
> Cluster-Overlap `D7 ↔ D8` (22 × 6 Einheiten, reine Lesbarkeit) im Pumpenblock.
> Blattbild: `.easyeda/artifacts/20260915-090028-schematic_export-63b30385.png`.
>
> **Neu inhaltlich:** zweiter, baugleicher Pumpenpfad für die **Sauerstoffpumpe** (`Q3`, `R33`, `R34`,
> `D7`, `D8`, `C20`, `J16`) an **IO22** — der Reserve-Stecker **J14** entfällt dafür — und ein
> **5-V-Boost** (`U8 MT3608`, `L1`, `D6`, `C17/C18` 22 µF, `C19` 100 nF, `R31/R32`) aus VBAT, damit
> **beide** Pumpen an **+5V** hängen. ⚠️ Folgepflichten: **PWM-Softstart zwingend** (der Boost liefert
> den 3-A-Anlauf nicht) und die Sauerstoffpumpe **nicht im Dauerbetrieb** (Akku in ~2,5 h leer).
> Details + Rechnungen: `../schaltplan_v1.md` §10.
>
> ⚠️ **Arbeitsweise (User-Vorgabe 15.09.2026):** Bei Schaltplan-Änderungen **immer** diese Kette
> benutzen — `sch clear` → `raw/place_all.sh` → Rahmen (je Rahmen eigene Datei!) → Gruppen →
> `autoconnect --spec raw/ac_<MODUL>.json` je Modul → NC-Marker → Pin-für-Pin-Diff → `gate`.
> **Nichts manuell nachrücken**, **keine Designatoren selbst vergeben** (das macht die Allokation in
> `raw/designator_changes.json`), **keine Rahmen/Gruppen vergessen**. Neue Bauteile gehören mit
> funktionalem Namen in `COMPS`/`modules.json`, ihre Pin-Tabellen als `raw/probe*.json`, ihre Volumen
> in `raw/measured_volumes_<datum>.json`.
>
> **Stand 14.09.2026 (GPIO-Erweiterung auf 2,54-mm-Stiftleisten):** Die Offline-Generatoren
> (`build_ir.py`, `plan_layout.py`, `build_autoconnect.py`, `netclass_spec.py`) wurden auf die
> erweiterte Netzliste gezogen: **80 Bauteile, 50 Netze, 233 Verbindungen, 12 Modulgruppen**;
> `check_ir_netlist.py` = **0 Abweichungen**; `plan_layout.py` packt jetzt mit den live
> gemessenen Bauteil-Volumen (`raw/measured_volumes_2026-09-14.json`, Koerper + Marker/Stiche)
> ohne Planungsproblem (`raw/frames.json` = **12 Rahmen**, Blattnutzung **71,1 %**);
> `check_plan_fit.py` = **Exit 0**; `raw/ac_ERWEITERUNG.json` wieder vorhanden.
> Der **Live-Bau in EasyEDA ist noch auf dem Rückbau-Stand** (58 Bauteile, 32 Netze, 171
> Verbindungen, 11 Modulgruppen, `sch gate` = pass) und muss vom Koordinator mit
> `sch clear → place → frames → autoconnect` auf den neuen Stand gezogen werden. Live-Nachweise
> des alten Stands: `s5/live_connectivity_2026-09-14.json`, `s5/FINAL_gate_2026-09-14.json`,
> Blattbild `../../out/schaltplan_2026-09-14.png` (+ `.svg`).
>
> **Erweiterung 14.09.2026:** Freie GPIOs + I²C als **2,54-mm-Stiftleisten** — **J8** (I²C 4-pol,
> GND–VCC_EXT–SDA–SCL), **J9–J15** (je 3-pol, GND–VCC–SIG), Lichtsensor **J7** ebenfalls
> Stiftleiste, **Q2 AO3401A** als Load-Switch für VCC_EXT, 1 kΩ in jeder Signalleitung,
> I²C-Pull-ups an VCC_EXT, `C_SPARE` am Reserve-ADC. Live-Device-Identitäten der drei neuen
> LCSC-Positionen am 14.09.2026 per `easyeda lib by-lcsc --include-device-identity` aufgelöst;
> das gemessene Library-Präfix der Stiftleisten ist **`H?`** (projektseitig bewusst als J-Refdes
> geführt, wie schon J2/J7 mit Präfix `CN?`).
>
> **Rückbau 14.09.2026:** Die GPIO-Erweiterung vom 13.09. (J8/J9/J10/Q2/TP7–TP11) war zwischen-
> zeitlich wieder entfernt und ist mit dieser Änderung in neuer Form (Stiftleisten) zurück.
>
> **Nachbesserung 13.09.2026 (Massepads):** Die frühere Sammelzeile `U1 1/2/11/14/36-53` in
> der Netzliste ist in Einzelzeilen aufgelöst. Das ESP32-C6-MINI-1-Symbol hat **keinen
> Bus-/Sammelpin** — alle 22 GND-Pads (1, 2, 11, 14, 36–53) haben live geprüfte eigene
> Koordinaten und werden einzeln verdrahtet. Die Zeile `EPAD (Pin 49)` ist als Kommentar
> erhalten (Pad 49 ist in 36–53 enthalten, kein Phantompin).
>
> **Historisch (11.09.2026):** Der erste eingecheckte Bau hatte 30 Netze und **keinen**
> Lichtsensor; die Zahlen in den Prüfberichten vom 11.09. beziehen sich darauf.

Stand des Offline-Aufbaus: **14.09.2026** · Tool: `easyeda-agent` 1.4.8 · Blatt: **A1 Querformat** (841 × 594 mm; 3304 × 2338 raw)

---

## Ergebnis (Offline-Generatoren, Stand 14.09.2026)

| Prüfung | Werkzeug | Stand |
|---|---|---|
| Bauteile / Netze | `raw/ir_report.txt` | **80 Bauteile, 50 Netze, 233 Verbindungen**, 16 NC-Pins, keine Probleme |
| Module | `raw/modules.json` | **12 Module** (USB, LADER, DEBUG, MCU, WAEChTER, LDO, AKKU, SENSOR, PUMPE, TASTER, LICHT, ERWEITERUNG) |
| Rahmen | `raw/frames.json` | **12 Rahmen** (11 bestehende + `frame-erweiterung`) |
| Netzlisten-Treue | `check_ir_netlist.py` (Pin-für-Pin gegen `raw/ir_numbered.json`) | **0 Abweichungen** (233 Verbindungen, 50 Netze) |
| Platzierung | `plan_layout.py` | kein Planungsproblem; 12 Blöcke aus den gemessenen Volumen gepackt, Blattnutzung 71,1 % (Volumen 15,2 %) |
| Platzierungs-Fit (offline) | `check_plan_fit.py` | **Exit 0** — 80 Volumen im Nutzbereich, kleinster Volumen-Abstand 25,00, kleinster Rahmen-Rand 150, 0 Blocküberlappungen |
| Autoconnect-Specs | `build_autoconnect.py` | **12** Spec-Dateien, `raw/ac_ERWEITERUNG.json` mit **54** Verbindungen |

**Live-Bau in EasyEDA (Stand 14.09.2026, Blatt A1 = 3304 × 2338):** 80 Bauteile, 50 Netze,
233 Verbindungen, pin-für-pin **0 Abweichungen** zur Netzliste, 12 Modulgruppen, 12 Modulrahmen,
NC-Marker auf allen 16 freien Pins. `sch gate` = **pass**; `sch gate --strict` = fail
(einziger Blocker: `missing-titleblock`, Host-Eigenheit). Nachweise:
`out/schaltplan_2026-09-14_A1.png` / `.svg`, `s5/live_connectivity_2026-09-14_A1.json`,
`s5/FINAL_gate_2026-09-14_A1.json`.

---

## Bekannte Restpunkte (rein kosmetisch)

1. **`missing-titleblock`** — die Prüfung sucht ein Titelblock-Feld namens `Drawed`; diese
   EasyEDA-Version kennt nur `Drawn`. Nicht behebbar, Host-Eigenheit. Der **einzige** Grund,
   warum `sch gate --strict` nicht grün ist (`sch gate` ohne `--strict` ist pass).
2. **Modulrahmen berühren sich teils** (z. B. LDO/DEBUG, TASTER/AKKU, USB/PUMPE) — erlaubt (nur
   Überlappung ist verboten), lässt aber keinen Zwischenraum für modulübergreifende Verdrahtung.
   Bei Bedarf später ein kleiner Zwischenabstand zwischen den Blöcken.
3. **Offline-Plan kennt nur die Fächer-Größe, nicht die -Richtung.** `plan_layout.py` rechnet je
   Bauteil die gemessenen Volumen (inkl. eigener Marker/Stiche) und 150 Einheiten Blockrand
   Reserve ein; ob der Autoconnect-Solver den Fächer live genau dorthin legt, entscheidet erst
   der Live-Lauf. Auf A2 ist genau daran `clusters` gescheitert (bis −92 out-of-sheet) — der
   Grund für den Wechsel auf A1.
4. **PCB** ist am 14.09.2026 neu aufgesetzt worden (nach dem Blatt-Neuaufbau): `pcb clear`
   (58 alte Bauteile weg, Blattkontur bleibt) + `pcb import-changes` → **80 Bauteile, 50 Netze,
   0 Leitungen**; Belege `s5/archiv/pcb_vor_neuaufbau_2026-09-14.json` (Zustand davor) und
   `s5/pcb_after_import_2026-09-14.json` (danach). Die Bauteile liegen als Streuung außerhalb der
   Blattkontur und sind **nicht** platziert/geroutet — Platzieren, Verdrahten und Routen macht der
   Nutzer selbst.



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
                                                              #   raw/no_place.json  (32 Umbenennungen)
python3 scripts/check_ir_netlist.py                           # Pin-für-Pin: 0 Abweichungen
# S2  Module/Gruppen + Rahmen
python3 scripts/plan_layout.py                                # → raw/place_all.sh, raw/frames_*.json
python3 scripts/check_plan_fit.py                             # offline: Volumen/Ränder/Blöcke, Exit 0
bash raw/place_all.sh                                         # 80/80 platziert
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
easyeda "${G[@]}" sch export-image --format png --out out/SmartGrowTopf_V1_A1_final.png
```

Die Papiergröße (A4 → A1) ist **nicht** über die CLI änderbar: Blatt im EasyEDA-Canvas anklicken →
rechtes Panel „Drawing" → Feld `Size`. Danach mit `sch sheet-geometry` gegenprüfen.

## Dateien

| Pfad | Inhalt |
|---|---|
| `scripts/build_ir.py` | Netzliste + Symbol-Pins → kanonische IR + Designator-Nummerierung |
| `scripts/check_ir_netlist.py` | Selbstkonsistenz IR ↔ Handnetzliste (Pin für Pin) |
| `scripts/plan_layout.py` | Modulblöcke, Platzierungsbefehle, Rahmen |
| `scripts/check_plan_fit.py` | Offline-Prüfer der Platzierung gegen die gemessenen Volumen |
| `scripts/build_autoconnect.py` | Autoconnect-Specs je Modul (12 Dateien) |
| `scripts/build_layout_input.py` | Eingabe für den Solver `sch lib-layout` (verworfen, s. u.) |
| `scripts/repair_pins.py` | Wiederherstellung der Verdrahtung nach dem Marker-Vorfall |
| `scripts/fix_overlaps_safe.py` | kosmetische Marker-Korrektur (nur `disconnect --flag-id`) |
| `scripts/netclass_spec.py` | Leiterbahnbreiten für die PCB-Phase (IPC-2221A) → `netclass_spec.json` |
| `scripts/pcb_widths.py` | Breiten auf der Platine prüfen/nachziehen (`--check`/`--apply`/`--route-plan`/`--selftest`) |
| `raw/` | IR (numeriert), Module, Symbole, Autoconnect-Specs, Platzierungsskript |
| `s1/` `s3/` `s4/` `s6/` | Zwischenstände (Seitenzustand, Verdrahtung, Titelblock) |
| `s5/FINAL_*` | **Abnahme-Belege** (gate, gate strict, check, bridge, drc, lint, read, Gruppen, Status) |
| `s5/b2_*` | Autoconnect-Läufe der finalen A1-Verdrahtung |
| `s5/archiv/` | alle Zwischenläufe (Zwischenprüfungen, verworfene Versuche) |
| `out/` | Bild-Exporte (PNG/SVG, A1) |

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
  Blatt ragende Marken — auf A1 sind es 0 bzw. 0.
- **`VDD33` bleibt unverbunden**: das offizielle ESP32-C6-MINI-1-Symbol hat genau einen 3V3-Pin;
  die VDD33-Pins sind modulintern verbunden. Die Netzliste bleibt unverändert.

## Nächster Schritt

PCB-Phase: `easyeda pcb import-changes` (Layout-Import aus dieser Seite), Stackup/Board aus
`s0_spec.json` (38 mm, 2 Lagen, Massefläche auf der Unterseite).
**Leiterbahnbreiten sind vorab festgelegt** (`netclass_spec.json`, Erklärung in
`docs/10_pcb-leiterbahnbreiten.md`): VBAT / PUMP_N / VBUS 0,5 mm, +3V3 0,4 mm, Signale
0,25 mm, Masse als Fläche. `PUMP_N` muss dabei explizit mit `pcb track --width 20`
gelegt werden — die Namensheuristik des Tools hält es für ein Signal.
