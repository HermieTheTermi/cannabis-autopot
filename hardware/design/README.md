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
* `checks.py` — 42 Prüfungen. Jede liefert `name · Ist · Soll · Begründung`;
  hart verdrahtet sind nur Datenblattgrenzen mit Quellenangabe. Verwendet eine
  Prüfung einen Pin-/Bauteilnamen, den die Netzliste nicht kennt, bricht sie
  als **Werkzeugfehler** ab (`PruefFehler`, Exit 2) — das zählt *nicht* als
  fehlgeschlagene Prüfung und ist damit klar von einem Design-Fehler (Exit 1)
  getrennt.
* `sim.py` — Rechenproben (Gate-Treiber, Ladezeit CC/CV, Dosiervorgang,
  Pumpenanlauf, Buck-Rippel, Teilerströme, Standby in mAh/Tag).
* `report.py` — Ausgabe der Prüfungen und Simulationen.

## 2S-Prüfungen (neu)

Ladestrom IP2326 · Ladeschluss 2S · Ladeeingangsstrom ·
5-V-Buck-Ausgang · 3,3-V-Buck-Ausgang (FB direkt, kein Teiler) ·
5-V-Buck-Induktivität · 3,3-V-Buck-Induktivität · UVLO-Schwelle ·
UV-Teiler-Offset (Iq × R3a) · Gate-Pulldowns · ADC-Teiler Packspannung ·
Buck-EN-Pegel · Wächter-Abschaltung · VBAT-Spannungsfestigkeit ·
Standby-Budget · Systemquellen.

## Review-Fixes 16.09.2026 (in `checks.py` nachgezogen)

* **Pin-Name `5 D` statt `mb (Drain)`** an Q_PROT1/Q_PROT2 (gemessenes
  EasyEDA-Symbol des PSMN4R2-30MLDX). Ein unbekannter Pin-Name ist jetzt ein
  Werkzeugfehler (`PruefFehler`, Exit 2), kein Design-Fehler.
* **U_BUCK3 (AP63203) ist die Festspannungsversion:** `circuit.rail_3v3()`
  liefert den Datenblatt-Festwert 3,30 V; die Prüfung „3,3-V-Buck-Ausgang"
  bestätigt zusätzlich, dass FB (Pin 1) direkt auf `+3V3` liegt und weder
  `R_FB3_TOP/BOT` noch das Netz `FB_3V3` existieren.
* **Gate-Klemmzweig entfernt** (D3/D8/R_CLAMP1/2, KLAMP1/2): die Prüfungen
  „Wächter-Sinkstrom" und „Klemmzweig-Serie" sind durch **„Gate-Pulldowns"**
  (R2/R_GATE2_PD je 47 kΩ nach GND) und **„Wächter-Abschaltung"**
  (RESET_UV → U_BUCK5 EN; kein Klemmzweig-Rest mehr) ersetzt.
* **UV-Teiler 51 k/51 k:** neue Prüfung „UV-Teiler-Offset" rechnet den
  Iq-Offset als `Iq_max × R3a` (25,5 mV ≤ 50 mV) und den Teilerstrom
  (~82 µA ≙ ~2 mAh/Tag); „Teilerstrom" prüft beide Teiler zusammen
  (≤ 130 µA).
* **Sensorversorgung über Q_SENS:** neue Prüfung „Sensor-Lastschalter"
  (Source `+3V3`, Drain `SENSOR_PWR`, Gate `EXT_SENS_EN`, 47-kΩ-Pull-up nach
  `+3V3`, IO3 treibt nur das Gate, kein GPIO direkt an `SENSOR_PWR`/`VCC_EXT`).

## Akku-Schutz auf der Platine (neu 16.09.2026)

Serienkette · Schwellen · Überstrom. Die Schutz-Schwellen und die
Überstromschwelle werden wörtlich aus `../schaltplan_v1.md` gelesen (fehlt das
Muster, bricht die Prüfung ab); der Auslösestrom wird gegen den
Pumpenanlaufstrom gestellt.

## Quellen

`../schaltplan_v1_netzliste.csv`, `../schaltplan_v1.md`,
`../bom_entscheidung.md`, `../pcba_bom_jlc.csv`, `../../docs/11_review-2s-umbau.md`.
Die Quelldateien werden nur gelesen, nie geändert.
