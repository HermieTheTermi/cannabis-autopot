# Leiterbahnbreiten auf der Platine (Akku, Pumpe, Versorgung)

Stand: 14.09.2026 · Projekt SmartGrowTopf_V1 · gehört zur Schaltplan-/PCB-Phase
Rechenweg: `../hardware/easyeda/scripts/netclass_spec.py` → Ergebnis `../hardware/easyeda/netclass_spec.json`

## 1. Kurzantwort

| Leitung | Breite | Warum |
|---|---|---|
| **Akku + (VBAT)** von J1 zum Lader, LDO, Wächter und Pumpenzweig | **0,5 mm (20 mil)**, nie unter 0,4 mm | trägt im schlechtesten Fall ~1,3 A → Erwärmung 7,8 K |
| **Pumpenleitung (PUMP_N)**: Q1 Drain → J4 | **0,5 mm (20 mil)**, nie unter 0,4 mm | Pumpe zieht 0,4 A Dauer, **2,2–2,5 A Anlauf** (~100 ms) |
| **Masse (GND)** | **keine dünne Bahn** — Kupferfläche auf der Unterseite + kurze Stiche ≥ 0,5 mm | derselbe Strom fließt zurück |
| **+3V3** vom LDO zum Modul | **0,4 mm**, mindestens 0,25 mm | 0,5 A max (TX-Spitze 0,38 A) |
| **VBUS** (USB 5 V → Lader) | 0,5 mm | Lader zieht bis 0,5 A |
| **VCC_EXT** (Q2 → J8/J9–J15) | **0,5 mm**, mindestens 0,25 mm | geschaltete Erweiterungsversorgung (Sensor-Module), bewusst mit Reserve |
| Alle Signale (LED, Sensor, Taster, UART, Gate, **I²C/Reserve**) | 0,25 mm | wenige mA |
| **USB_DP/USB_DM** | 0,25 mm, paarweise + gleich lang | 12 Mbit/s Full Speed |

Ein 2-Lagen-Board mit 1 oz Kupfer (35 µm) bei JLCPCB kann minimal 0,127 mm (5 mil) —
die Werte oben liegen also bequem im Standardprozess und kosten keinen Aufpreis.

## 2. Herleitung

**Ströme** (aus Datenblättern, nicht geschätzt):

- Pumpe **CONQUERALL DC 5 V** (Amazon `B0DHVMZ27Y`, seit 14.09.2026): Nennstrom **0,4 A**
  (5 V Nennspannung); an unserer 1S-Zelle (3,0–4,2 V) ist sie **unterspannungsbetrieben** →
  Laststrom ~0,4 A, **Anlaufstrom 2,2–2,5 A** (aus den 3 A @5 V des Datenblatts, ohmsch auf die
  Zellspannung umgerechnet). Die abgelöste OEM ABC-12527 lag bei 0,45–0,54 A Dauerstrom.
- ⚠️ **Der Anlaufstrom ist der kritische Fall dieser Platine** (nicht der Dauerstrom): bei 2,2 A
  bricht VBAT über den 254-mΩ-Gesamtpfad um **0,56 V** ein → siehe `../hardware/bom_entscheidung.md`
  §4c. Gegenmaßnahme ist **PWM-Softstart in der Firmware**, nicht breitere Bahnen.
- LDO ME6211C33: **500 mA** Ausgang; der ESP32-C6 zieht im WLAN-TX **382 mA** Spitze
  (Espressif Tab. 6-4) — beides gleichzeitig mit der Pumpe ist der Lastfall.
- Lader MCP73831 mit R_PROG 3,9 kΩ: **256 mA** (max 500 mA).
  Die Firmware pumpt nicht während des Ladens (Review-Befund F6), der Vollastfall
  wäre 0,54 + 0,50 + 0,26 = **1,30 A** auf dem Akkuknoten.

**Rechnung** nach IPC-2221A, Außenlage:

```
A [mil²] = (I / (k · ΔT^0.44))^(1/0.725)      k = 0,048 (außen)
Breite   = A / 1,378 mil                       (1 oz = 35 µm)
ΔT = 10 K (üblich für Handgeräte mit Kunststoffgehäuse)
```

| Strom | nötige Breite bei ΔT = 10 K | bei ΔT = 20 K |
|---|---|---|
| 0,50 A | 0,12 mm | 0,08 mm |
| 0,54 A | 0,13 mm | 0,08 mm |
| 1,20 A | 0,39 mm | 0,25 mm |
| 1,30 A | 0,44 mm | 0,28 mm |
| 1,50 A | 0,53 mm | 0,35 mm |
| 2,00 A | 0,78 mm | 0,51 mm |

Umgekehrt: **0,5 mm trägt 1,45 A bei 10 K** und 1,96 A bei 20 K Erwärmung;
0,4 mm trägt 1,23 A / 1,67 A. Unsere 1,3 A liegen damit bei 0,5 mm → **7,8 K**
und bei 0,4 mm → 12 K (deshalb 0,4 mm als Untergrenze, nicht als Ziel).

**Spannungsabfall** (Kupfer bei 70 °C) — der eigentliche Grund für die 0,5 mm
ist nicht die Erwärmung, sondern dass die Pumpe ihre Spannung behalten soll:

| Strecke | Widerstand | Abfall @0,4 A (Dauer) | @2,2 A Anlauf | @2,5 A Anlauf |
|---|---|---|---|---|
| 0,4 mm × 40 mm | 59 mΩ | 23 mV (0,6 %) | 129 mV (3,5 %) | 146 mV (4,0 %) |
| **0,5 mm × 40 mm** | **47 mΩ** | **19 mV (0,5 %)** | **103 mV (2,8 %)** | 117 mV (3,2 %) |
| 0,25 mm × 40 mm | 94 mΩ | 37 mV (1,0 %) | 206 mV (5,6 %) | 234 mV (6,3 %) |

Zum Vergleich der Bauteile: der AO3400A hat **48 mΩ** Rds(on), die 1N5819WS
verliert ~0,35 V in Durchlassrichtung, die JST-Buchse ~20 mΩ pro Pol.
**Die Leiterbahn ist damit nicht der begrenzende Widerstand** — ab 0,5 mm ist der
Rest des Pfades die Grenze, nicht das Kupfer.

## 3. Warum nicht dünner (0,25 mm)?

Thermisch würde 0,25 mm reichen (0,88 A bei 10 K). Dagegen spricht:

1. Die Pumpe ist ein Motor mit Bürsten — der Anlaufstrom ist **seit 14.09.2026 bekannt**:
   Datenblatt der CONQUERALL nennt **3 A bei 5 V**, an der 1S-Zelle sind es 2,2–2,5 A. Bei 2,2 A
   hat eine 0,25-mm-Bahn **5,6 %** Spannungsverlust, eine 0,5-mm-Bahn **2,8 %**.
2. Jede Erwärmung im Wulst ist unerwünscht (geschlossene Kammer, LiPo daneben).
3. Eine breitere Bahn ist bei JLCPCB kostenlos — Sparsamkeit an dieser Stelle
   spart nichts.

## 4. Was in der PCB-Phase konkret zu tun ist

```bash
# 1) Masse- und Schienenverteilung als Fläche, nicht als dünne Bahnen (2 Lagen)
easyeda pcb power-pour ...          # GND beidseitig + lokale Schienen-Flächen
# 2) Kritische Netze deterministisch zuerst: Flächen + USB-Diff-Paar + Lock
easyeda pcb diff-pair create --name USB --positive USB_DP --negative USB_DM
easyeda pcb route-critical ...
# 3) VBAT / PUMP_N / VBUS mit voller Breite legen (20 mil = 0,5 mm)
easyeda pcb track --x1 .. --y1 .. --x2 .. --y2 .. --net VBAT   --width 20
easyeda pcb track --x1 .. --y1 .. --x2 .. --y2 .. --net PUMP_N --width 20
# 4) Rest routen (Signale); route-short nimmt Kraft-/Massennetze standardmäßig
#    als 20-mil-„power" an, Signale als 10 mil
easyeda pcb route-short ...
# 5) Prüfen
easyeda pcb check      # findet u. a. Kraftbahnen, die dünner als ihre Rolle sind
easyeda pcb drc
```

**Achtung, Fallstrick:** Das Netklassen-Modell von `easyeda-agent` erkennt Netze
**am Namen** (`VBUS|VIN|VBAT|VSYS` → „high-current" 0,5 mm; Spannung im Namen →
0,25/0,4 mm; alles andere → „signal"). Unsere Netze werden damit so eingestuft:

| Netz | automatische Einstufung | Soll |
|---|---|---|
| VBAT | high-current (0,5 mm) ✅ | 0,5 mm |
| VBUS | high-current (0,5 mm) ✅ | 0,5 mm |
| +3V3 | power-branch (0,25 mm) | **0,4 mm** — dicker als die Automatik |
| **PUMP_N** | **signal (0,25 mm)** ❌ | **0,5 mm — muss explizit gesetzt werden** |

`PUMP_N` heißt nicht wie eine Versorgung, trägt aber den vollen Pumpenstrom.
Deshalb beim Verdrahten `--width 20` (0,5 mm) mitgeben oder die Strecke als
Fuellfläche legen — die Automatik allein legt sie zu dünn.

## 5. Wo die Breiten definiert sind (für die nächste Sitzung)

Die Sollbreiten liegen **nicht** in EasyEDA, sondern im Projekt — dort, wo sie
prüfbar und versioniert sind:

| Datei | Rolle |
|---|---|
| `hardware/easyeda/netclass_spec.json` | **die Definition**: je Netz Rolle, Sollbreite, Minimum, Strom, Erwärmung, Spannungsabfall (alle **50 Netze** der aktuellen Netzliste) |
| `hardware/easyeda/scripts/netclass_spec.py` | rechnet die Definition nach IPC-2221A aus (reproduzierbar) |
| `hardware/easyeda/scripts/pcb_widths.py` | **setzt sie auf der Platine durch**: `--check` (Rückgabewert 1 bei Verstoß, gate-fähig), `--apply` (zu dünne Bahnen nachziehen), `--route-plan` (Verdrahtungsbefehle ausgeben) |
| `hardware/easyeda/s0_spec.json` → `netClasses` | Kurzfassung für den P-Phasen-Import |

**EasyEDA selbst kann nur eine einzige Standardbreite.** Ausgelesen aus dem
vorhandenen PCB-Dokument (`easyeda pcb drc-rules`, Regelkatalog `Physics.Track`):

```
copperThickness1oz:  default 0,254 mm   min 0,127 mm   max 2,54 mm
```

Netzklassen gibt es im Regelsatz dieser Version **nicht** (`Spacing` enthält nur
Creepage/Safe-Spacing, keine Klassen) — deshalb lässt sich „Akku dick, Signal dünn"
nicht über die EasyEDA-Regeln definieren. Genau diese Lücke schließt die
Projekt-Definition oben plus die Durchsetzung per Skript.

**Stand der Prüfung:** `pcb_widths.py --selftest` grün (Vergleichslogik),
`--check` läuft gegen das vorhandene, noch leere PCB-Dokument `PCB1`
(UUID `18b1cf4334ae3b53`) und meldet 0 Leiterbahnen — die Platine ist bewusst noch
nicht aufgebaut. Sobald der Import läuft, prüft derselbe Aufruf die echten Bahnen.

## 6. Offene Punkte

- **Anlaufstrom der Pumpe messen** (Prototyp, Oszilloskop mit Stromzange über
  R2/Q1) und die 0,5 mm gegen den gemessenen Wert prüfen. 1,5 A = 10,9 K Erwärmung: in Ordnung.
- **2 oz Kupfer** wäre die Alternative (0,2 mm reichen dann), kostet bei JLCPCB
  aber Aufpreis und bringt bei 0,6 A Dauerstrom nichts.
- **Kontrollierte Impedanz** bietet JLCPCB nur ab 4 Lagen — bei 2 Lagen bleibt das
  USB-Paar kurz, parallel und gleich lang; bei 12 Mbit/s ist das ausreichend.
- **Kupfer unter der Antenne** des ESP32-C6-MINI-1 bleibt frei (Keepout) — das
  gilt auch für die GND-Fläche auf der Unterseite.
