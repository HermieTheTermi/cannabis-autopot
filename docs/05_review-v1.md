# Review V1 — passt alles zusammen?

Stand: 11.09.2026 · Prüfmaßstab: `docs/02_architektur-und-geometrie.md` (Geometrie-Wahrheit),
`hardware/bom_entscheidung.md` (BOM), `hardware/pcba_verfuegbarkeit_jlc.md` (PCBA), `case/params.scad` (CAD).

**Ergebnis:** Elektrik, Bauteile und Fertigung passen zusammen. **Ein blockierender Punkt ist die
Gehäusekammer: die geplante Platine passt dort nicht hinein.** Details unten.

---

## 1. ✅ War blockierend, ist durch das Modul gelöst: Platine vs. Kammer

Aus `case/params.scad`:

| Größe | Formel | Wert |
|---|---|---|
| Kammertiefe (Y) | `wc_y1 - wc_y0` = 112 − 72 | 40 mm |
| Kammerhöhe (Z) | `wc_z1 - wc_z0` = 244 − 92 | **152 mm** |
| Kammerbreite (X) | `2 × wc_x` = 2 × 20 | **40 mm** |
| Wulst außen / Wand | `wulst_w` 60 / `wulst_wall` 6 | innen wären **48 mm** |

Gegen die deklarierten Bauteil-Footprints: `pcb_l` **52 mm**, `pcb_w` **42 mm**, `pcb_t` 1,6 mm.

- **42 mm > 40 mm** → die *früher angenommene* Platine (52 × 42 mm, dimensioniert um XIAO + dessen
  USB-Buchse) passt in der Breite nicht in die Kammer. Die 52 mm könnten nur entlang der Höhe laufen
  (152 mm vorhanden), die zweite Kante muss aber durch die 40-mm-Kammer.
- **Gelöst durch den Wechsel auf das ESP32-C6-MINI-1:** das Modul ist mit 13,2 × 16,6 mm deutlich
  kleiner als der XIAO (21 × 17,8 mm), und dessen USB-Buchse samt Randabstand fällt weg. Damit ist
  eine Platine **≤ 38 mm breit** realistisch → passt mit Luft in die 40-mm-Kammer. Die alten
  `pcb_l`/`pcb_w`-Werte (52 × 42) in `case/params.scad` sind damit überholt und nachzuziehen.
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
| Zellüberwachung | 200 kΩ in 1:2 auf A0 (Seeed-Doku, wörtlich) | ✅ Firmware-Ebene, ein Widerstand |
| **Tiefentladeschutz** | MCP73831-Datenblatt: nur „Reverse Discharge Protection" + Lade-UVLO 3,45/3,38 V → **kein Entladeschutz im Lader** | ✅ vier Ebenen ergänzt: Firmware 3,4 V · **MAX809TEUR+T bei 3,08 V** (Datenblatt VTH) · Gate-Pulldown · Zell-PCM — siehe `bom_entscheidung.md` §4b |
| **MCU-Modul** | ESP32-C6-MINI-1: EN-RC 10 kΩ/1 µF, GPIO9-Pull-up, keine großen Cs an GPIO9, 3V3 = 22 µF + 2 × 0,1 µF (Espressif) | ✅ Beschaltung übernommen, `bom_entscheidung.md` §6 |
| **3,3-V-Schiene** | ESP32-C6 TX-Peak **382 mA** (Espressif Tab. 6-4, selbst geprüft) | ✅ LDO **ME6211 (500 mA)** statt 250-mA-Typ — sonst Brownout bei TX |
| **USB** | ESP32-C6 hat USB Serial/JTAG nativ: D− = GPIO12, D+ = GPIO13 | ✅ kein USB-UART-Chip nötig; CC-Widerstände 5,1 kΩ + USBLC6-ESD ergänzt (USB-C-Vorgabe, nicht von Espressif dokumentiert) |
| **RF** | Antennen-Freistellung: Espressif fordert ≥ 15 mm in alle Richtungen im Gehäuse | ⚠️ offen — erfordert bauteilfreien oberen Kammerbereich + dünnere Wulstwand, **plus RF-Endtest** |
| Laufzeit | 0,052 Wh pro 300-ml-Dosis, 4,44 Wh nutzbar | ✅ ~85 Dosen pro Ladung |

## 4. ✅ Fertigung — PCBA machbar

**Die Platine ist jetzt vollständig bestückbar** — mit dem nackten Modul gibt es keine Lücke mehr
(der XIAO war bei JLC nicht bestückbar, das MINI-1 ist es). Alle Bauteile haben LCSC-Codes und
Lagerbestand, siehe `hardware/pcba_verfuegbarkeit_jlc.md`. Handling: **10 Extended-Positionen
≈ 30 USD** Aufpreis, weil Lader, LDO und USB jetzt auf unserer Platine sitzen statt im XIAO-Modul.

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
| 9 | **Gehäuse-Parameter** `pump_d`/`pump_l`/`pump_mount_*` + `wc_x` + `pcb_*` | Kollisionen, siehe §1/§2 |
| 10 | **Antennenbereich** im Gehäuse (obere ~25 mm frei, Wand über der Antenne ~2 mm) | ohne das ist die WLAN-Reichweite unbelegt |
| 11 | **RF-Endtest** am fertigen Aufbau (Espressif-Vorgabe) | Durchsatz/Reichweite messen, sonst ggf. auf MINI-1U mit externer Antenne |

## 6. Reihenfolge bis zur bestellbaren Platine

1. `case/params.scad`: `wc_x` 20 → 24, Pumpenwerte (Ø32 / 44 / 44 / 2,5) — **OpenCode**, danach
   Nachrender + Sichtprüfung der Freiräume.
2. Schaltplan + Layout (eigene PCB): XIAO als auflötbares Modul, Pumpe direkt an VBAT, Sensor-JST,
   Akku-PH-Buchse, VBAT-Teiler optional — Bauteile alle bei JLC verfügbar.
3. Teile, die nicht von JLC kommen, bestellen: Pumpe, Sensor, Akku, Schlauch, Filter, Schrauben.
4. Kalibrierlauf am realen Aufbau: Förderrate, Sensor trocken/nass, Tank-leer-Kriterium.
