# Design-Checks Schaltplan V1 (Stand 2S-Umbau, 16.09.2026)

Prüft den 2S-Schaltplan rechnerisch gegen die Datenblatt-Grenzwerte und
simuliert die kritischen Vorgänge. Nur Standardbibliothek, Python 3.9+.

Aufruf (aus `hardware/`):

    python3 -m design.report

Alternativ direkt: `python3 hardware/design/report.py`.
Exit-Code 0 = alle Prüfungen bestanden, 1 = mindestens eine fehlgeschlagen.

## Aufbau

* `circuit.py` — lädt Netzliste und Bauteilwerte. Bauteilwerte kommen
  ausschließlich über `circuit.part("<Designator>")` aus den Tabellen
  §3.1–§3.4 der `schaltplan_v1.md`. Systemgrößen (Pumpe, Pack, Modul, ADC,
  Netzteil) stehen im markierten `SYSTEM`-Block, jede mit ihrer wörtlichen
  Belegstelle. Annahmen stehen markiert in `ASSUMPTIONS`.
* `checks.py` — 37 Prüfungen. Jede liefert `name · Ist · Soll · Begründung`;
  hart verdrahtet sind nur Datenblattgrenzen mit Quellenangabe.
* `sim.py` — Rechenproben (Gate-Treiber, Ladezeit CC/CV, Dosiervorgang,
  Pumpenanlauf, Buck-Rippel, Teilerströme, Standby in mAh/Tag).
* `report.py` — Ausgabe der Prüfungen und Simulationen.

## 2S-Prüfungen (neu)

Ladestrom IP2326 · Ladeschluss 2S · Ladeeingangsstrom ·
5-V-Buck-Ausgang · 3,3-V-Buck-Ausgang · 5-V-Buck-Induktivität ·
3,3-V-Buck-Induktivität · UVLO-Schwelle · Wächter-Sinkstrom ·
ADC-Teiler Packspannung · Buck-EN-Pegel · Klemmzweig-Serie ·
VBAT-Spannungsfestigkeit · Standby-Budget · Systemquellen.

## Quellen

`../schaltplan_v1_netzliste.csv`, `../schaltplan_v1.md`,
`../bom_entscheidung.md`, `../pcba_bom_jlc.csv`, `../../docs/11_review-2s-umbau.md`.
Die Quelldateien werden nur gelesen, nie geändert.
