# EasyEDA-Übergabe: Schaltplan für SmartGrowTopf_V1

Dieses Dokument ist der Einstieg für die Sitzung, die den Schaltplan in EasyEDA Pro baut.
Es hält nur den Stand fest, der **verifiziert** ist — keine Annahmen.

## 1. Pflicht-Erstkommando (Version-Gate)

```bash
easyeda update --check --exit-code    # muss Exit 0 liefern
```

Erwartet: `→ READY: CLI/Skills/daemon are exactly v1.4.8; connector major.minor is compatible`.
Stand 11.09.2026: **Exit 0** (CLI 1.4.8, Daemon 1.4.8, Connector 1.4.8, 1 Fenster verbunden).

Die Dokumentation verbietet, eine Sitzung fortzusetzen, in der CLI/Daemon/Connector
ausgetauscht wurden — deshalb läuft die Design-Arbeit in einer **neuen** Sitzung, die mit
dem Gate beginnt. Danach:

```bash
easyeda health                       # Projekt, aktive Seite, Connector prüfen
easyeda doc ls                       # Dokumente + UUIDs
```

## 2. Projekt-Identitäten

| Was | Wert |
|---|---|
| Projekt | `SmartGrowTopf_V1` (uuid `51deea9fc24745be915d72e65813fa8b`) |
| Schaltplan-Seite | `P1` (uuid `4f6771a27edec75b`) — **aktiv** |
| PCB | `PCB1` (uuid `18b1cf4334ae3b53`) |
| Connector-Fenster | `windowId` ist **nicht stabil** — pro Sitzung neu bestimmen: `easyeda doc ls --window <id>` und das Fenster nehmen, das die Zieldatei listet |

Immer mit `--project SmartGrowTopf_V1` arbeiten, Mutationen mit `--doc P1`.

## 3. Eingabedaten (S0-Quellen)

Alle im Repo `~/Projekte/cannabis-autopot`:

- `hardware/schaltplan_v1.md` (Stand 14.09.2026) — **Wahrheit**: Blockbild, Netztabelle,
  Bauteilwerte, Pinbelegungen, Auslegung. **50 Netze, 80 Bauteile, 72 bestückte Positionen,
  6 Testpunkte (TP1–TP6)**. Die GPIO-/I²C-Erweiterung (J7–J15, Q2) ist als 2,54-mm-Stiftleisten
  wieder eingebaut; der **Live-Bau in EasyEDA muss dafür noch nachgezogen werden** (Offline-Stand
  der Generatoren: 80 Bauteile, 50 Netze, 233 Verbindungen, `check_ir_netlist.py` 0 Abweichungen).
- `hardware/schaltplan_v1_netzliste.csv` — maschinenlesbare Netzliste (Bauteil, Pin, Netz).
- `hardware/pcba_bom_jlc.csv` + `hardware/pcba_verfuegbarkeit_jlc.md` — LCSC-Codes,
  basic/extended, Lagerbestand.
- `hardware/design/` — Python-Designmodell mit **29 mutationsgeprüften** Prüfungen
  (`python3 hardware/design/report.py` → 29/29) und die Netzlisten-/BOM-Linter unter
  `scripts/`. Diese dienen der Gegenprüfung der EasyEDA-Ausgabe.
- `docs/02_architektur-und-geometrie.md` — mechanische Wahrheit (Platine ≤ 38 mm breit,
  Antennen-Freistellung, Kammermaße).

## 4. Ablauf nach Doku (`skills/easyeda-agent/references/design-flow.md`, S0–S6)

1. **S0** — Anforderungen und Datenquellen festhalten (aus den Dateien oben; keine neuen
   Bauteile erfinden, kein Umlabeln unvollständiger Schaltungen).
2. **S1** — `easyeda sch connectivity` exportieren (Basisschnappschuss), Papier/Zeichenfläche
   mit `sch sheet-geometry --json` prüfen (A1, 3304 × 2338 raw, Rand-Freihaltezone).
3. **S2** — Positionen: nur fehlende/ungültige Bezeichner mit `sch designators` vergeben,
   gültige behalten; Pin-/NC-Verbindungen lokal prüfbar machen.
4. **S3** — Lib-Geometrie mit `sch lib-layout` rechnen, Module mit `sch compose` setzen
   (Z-Layout ab links oben, 10 raw Rand, 20 raw Titel, rosa Modulrahmen).
5. **S4** — `sch apply <queue> --dry-run`, dann echt anwenden; Journal behalten.
6. **S5** — `sch connectivity` erneut ziehen, `sch design-diff` gegen das Ziel,
   dann **`sch gate --strict --json`** je Seite (führt `layout-lint → check →
   bridge-check → drc` aus). Offizieller DRC deckt nicht alles ab.
7. **S6** — `sch save` (explizit, autosave ist nur Netz), Ergebnis melden,
   Bilder mit **`sch export-image`** erzeugen (native Screenshots können veraltet sein).

Akzeptanz am Ende: `sch gate --strict` ohne `fail`/`blocked`, offizieller DRC berichtet,
Screenshots der nativen Seite, Liste der verbleibenden WARN/INFO.

## 5. Bekannte Stolpersteine (verifiziert)

- **Berechtigung**: Die Extension braucht im Extension Manager → Installed → **Karte des
  Connectors anklicken** → Tab **Config** → **„Allow interactive with external"**.
  Ohne diesen Haken verbindet sich der Connector **still** nicht (kein Log-Eintrag).
- **Daemon nicht von Hand starten** — LaunchAgent `ai.hermes.easyeda-daemon` (KeepAlive).
  Jeder eigene Start ersetzt ihn und löscht die Fenster-Registrierung.
- **Aktives Dokument zählt**: Mit `documentType: blank` scheitern `workflow status` und
  PCB-Aktionen. Erst `easyeda project open --uuid <page-uuid>`, dann arbeiten.
- **Kein Verpolschutz** im Design (bewusste Entscheidung, D4-Brücke wurde entfernt).
