# Review V1 — passt alles zusammen?

Stand: 11.09.2026 · Prüfmaßstab: `docs/02_architektur-und-geometrie.md` (Geometrie-Wahrheit),
`hardware/bom_entscheidung.md` (BOM), `hardware/pcba_verfuegbarkeit_jlc.md` (PCBA), `case/params.scad` (CAD).

**Ergebnis:** Elektrik, Bauteile und Fertigung passen zusammen. **Ein blockierender Punkt ist die
Gehäusekammer: die geplante Platine passt dort nicht hinein.** Details unten.

---

## 1. 🔴 Blockierend: Platine 42 mm breit, Kammer nur 40 mm

Aus `case/params.scad`:

| Größe | Formel | Wert |
|---|---|---|
| Kammertiefe (Y) | `wc_y1 - wc_y0` = 112 − 72 | 40 mm |
| Kammerhöhe (Z) | `wc_z1 - wc_z0` = 244 − 92 | **152 mm** |
| Kammerbreite (X) | `2 × wc_x` = 2 × 20 | **40 mm** |
| Wulst außen / Wand | `wulst_w` 60 / `wulst_wall` 6 | innen wären **48 mm** |

Gegen die deklarierten Bauteil-Footprints: `pcb_l` **52 mm**, `pcb_w` **42 mm**, `pcb_t` 1,6 mm.

- **42 mm > 40 mm** → die Platine passt in der Breite nicht in die Kammer. Die 52 mm können nur
  entlang der Höhe laufen (152 mm vorhanden, unkritisch), aber die zweite Kante muss durch die
  40-mm-Kammer.
- Auffällig: die Wulst ist außen 60 mm breit mit 6 mm Wandung, das ergäbe **48 mm** Innenbreite —
  `wc_x = 20` verschenkt davon 8 mm. Das sieht nach einem Parameterfehler aus, nicht nach Absicht.

**Fix (empfohlen):** `wc_x` von 20 auf **24** setzen → 48 mm Kammerbreite. Dann passt eine 42 mm
breite Platine mit je 3 mm Luft. Alternativ die Platine auf ≤ 38 mm Breite schrumpfen — bei unserem
Schaltungsumfang (XIAO 21 × 17,8 mm + MOSFET + Passive) ist das machbar, aber unnötig eng, solange
die Wulst den Platz hergibt.

## 2. 🟡 Eng, aber lösbar: Höhen- und Tiefenbudget

- **Höhe:** Pumpe 44 mm + Platine 52 mm + Zelle 59 mm = **155 mm** gegen 152 mm Kammerhöhe → passt
  **nur**, wenn Platine und Zelle sich denselben Höhenbereich teilen (nebeneinander in der Tiefe)
  statt hintereinander. Regel fürs Layout: **im Pumpenbereich (Z 92–136) nur Pumpe und Schläuche**;
  ab ~140 mm liegen Platine und Zelle nebeneinander in der Tiefe. Dann ist die Höhe unkritisch
  (max(52, 59) = 59 mm ≤ 108 mm freie Höhe über der Pumpe).
- **Tiefe:** In der Tiefe stehen 40 mm zur Verfügung; Pumpe Ø32 + Platine 1,6 + Zelle 5 = 38,6 mm —
  rechnerisch passend, aber **nur 1,4 mm Rest**. Der JST-Akku-Stecker (baut ~6–7 mm über die
  Platine) und der 100-µF-Elko (Ø6,3 × 5,4 mm) passen in diesen Streifen **nicht**.
  → Steckverbinder und hohe Bauteile müssen in den Höhenbereich **über** der Pumpe, Abgangsrichtung
  zum Deckel (+Y), oder es werden gewinkelte SMD-Buchsen eingesetzt (bei JLC verfügbar, siehe
  `pcba_verfuegbarkeit_jlc.md` J1: gewinkelte PH-Buchse).

## 3. ✅ Elektrik — geprüft und stimmig

| Punkt | Prüfung | Ergebnis |
|---|---|---|
| Pumpenspannung vs. Zelle | Pumpe 3,7–6 V (Seite), Zelle 3,0–4,2 V | ✅ im Datenblattbereich, kein Wandler |
| MOSFET am 3,3-V-Gate | AO3400A Datenblatt: RDS(on) < 48 mΩ @ VGS 2,5 V | ✅ < 10 mW Verlust bei 0,45 A, logic-level |
| Freilaufdiode | 1N5819WS: 40 V / 1 A / 25 A Surge | ✅ 5× Reserve |
| Ladepfad | XIAO-Schaltplan: SGM40567-**4.2** → 1S | ✅ passt zur Zelle, kein Lade-IC nötig |
| Gate-Beschaltung | 220 Ω Serie, 10 kΩ Pulldown | ✅ Pumpe sicher AUS beim Boot |
| Sensor-Versorgung | VCC über GPIO, AOUT auf ADC1 | ✅ spart Strom, kein ADC2-Stolperstein |
| Zellüberwachung | 200 kΩ in 1:2 auf A0 (Seeed-Doku, wörtlich) | ✅ optional, ein Widerstand |
| Laufzeit | 0,052 Wh pro 300-ml-Dosis, 4,44 Wh nutzbar | ✅ ~85 Dosen pro Ladung |

## 4. ✅ Fertigung — PCBA machbar

Alles außer dem XIAO-Modul ist bei JLCPCB lagernd (Basic/Extended) — Details und LCSC-Codes in
`hardware/pcba_verfuegbarkeit_jlc.md`. Der XIAO ist dort **nicht** im Sortiment → selbst auflöten
(Castellated Pads), im BOM als „nicht bestücken" markieren. Damit entfällt auch die Buchsenleiste.

## 5. ❓ Was noch fehlt (Vollständigkeitsprüfung)

| # | Fehlt / offen | Konsequenz |
|---|---|---|
| 1 | **Silikonschlauch** 3 × 5 mm, ~1 m | Pumpe liefert nur ~5 cm → sonst kein Wasserweg |
| 2 | **Ansaugfilter/-gewicht** am Tankboden | ohne: Ansaugen von Partikeln, Pumpe verstopft |
| 3 | **4 × M2,5-Schrauben** + Dichtung Wulstdeckel | Deckel ist sonst nicht dicht |
| 4 | **Zellbefestigung** (Klemmung/Band) | Zelle darf nicht wandern (Kurzschlussgefahr) |
| 5 | **Sensorkabel** (3-adrig, Länge bis Wulst) | im Sensor-Lieferumfang unklar |
| 6 | **Förderrate bei 3,7 V** unbekannt | Dosierzeit im Code muss kalibriert werden |
| 7 | **PCB-/PCBA-Preis** | noch kein JLC-Angebot eingeholt |
| 8 | **Firmware-Aufgaben**: WLAN-Provisioning, Telegram-Token, Kalibrierroutine | noch nicht begonnen |
| 9 | **Gehäuse-Parameter** `pump_d`/`pump_l`/`pump_mount_*` + `wc_x` | Kollisionen, siehe §1/§2 |

## 6. Reihenfolge bis zur bestellbaren Platine

1. `case/params.scad`: `wc_x` 20 → 24, Pumpenwerte (Ø32 / 44 / 44 / 2,5) — **OpenCode**, danach
   Nachrender + Sichtprüfung der Freiräume.
2. Schaltplan + Layout (eigene PCB): XIAO als auflötbares Modul, Pumpe direkt an VBAT, Sensor-JST,
   Akku-PH-Buchse, VBAT-Teiler optional — Bauteile alle bei JLC verfügbar.
3. Teile, die nicht von JLC kommen, bestellen: Pumpe, Sensor, Akku, Schlauch, Filter, Schrauben.
4. Kalibrierlauf am realen Aufbau: Förderrate, Sensor trocken/nass, Tank-leer-Kriterium.
