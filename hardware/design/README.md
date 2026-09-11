# Design-Checks Schaltplan V1

Prüft den Schaltplan V1 rechnerisch gegen die Datenblatt-Grenzwerte und
simuliert die kritischen Vorgänge. Nur Standardbibliothek, Python 3.9+.

Aufruf (aus `hardware/`):

    python3 -m design.report

Alternativ direkt: `python3 hardware/design/report.py`.

Dateien: `circuit.py` lädt Netzliste und Werte, `checks.py` prüft,
`sim.py` rechnet, `report.py` gibt aus (Exit 1 bei Fehlschlag).
Quellen: `../schaltplan_v1_netzliste.csv`, `../schaltplan_v1.md`,
`../bom_entscheidung.md`. Grenzwerte mit Quellenangabe im Code.
