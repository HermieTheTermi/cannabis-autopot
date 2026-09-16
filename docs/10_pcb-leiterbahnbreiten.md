# Leiterbahnbreiten auf der Platine (Akku, Pumpe, Versorgung)

Stand: **16.09.2026 (Revision „2S-Umbau")** · Projekt SmartGrowTopf_V1 · gehört zur Schaltplan-/PCB-Phase
Rechenweg: `../hardware/easyeda/scripts/netclass_spec.py` → Ergebnis `../hardware/easyeda/netclass_spec.json`

⚠️ Diese Datei ist auf die **2S-Versorgungskette** nachgezogen (IP2326-Lader, SY8113B-Buck → +5V,
AP63203-Buck → +3V3). Die genannten EasyEDA-Artefakte (`netclass_spec.json`, `s0_spec.json`) stammen
noch aus dem **1S-Stand (50 Netze)** und müssen im EasyEDA-Neuaufbau aus der neuen Netzliste (68 Netze)
neu erzeugt werden (`docs/11_review-2s-umbau.md` §8.7).

## 1. Kurzantwort

| Leitung | Breite | Warum |
|---|---|---|
| **Akku + (VBAT)** von J1/Lader zu beiden Bucks und den Teilern | **≥ 1,0 mm (40 mil) bzw. als Fläche**, nie unter 0,5 mm | speist den 5-V-Buck, der den **3-A-Pumpenanlauf** liefert ⇒ bis **~2,8 A** auf VBAT (1S-Stand: 1,3 A) |
| **+5V-Schiene** (L_BUCK5 → C3, Q1/Q3, J4/J16/J17) | **≥ 1,0 mm bzw. Fläche**, nie unter 0,5 mm | 3 A Anlauf (kurz), 0,6 A Nennlast (beide Pumpen) |
| **Pumpenleitung (PUMP_N / PUMP2_N)**: Q1/Q3 Drain → J4/J16 | **0,5 mm (20 mil)**, nie unter 0,4 mm | Pumpe 0,4 A Dauer, **3 A Anlauf** |
| **Masse (GND)** | **keine dünne Bahn** — Kupferfläche auf der Unterseite + kurze Stiche ≥ 0,5 mm | derselbe Strom fließt zurück |
| **+3V3** vom Buck zum Modul | **0,4 mm**, mindestens 0,25 mm | 2-A-Buck gegen 0,38 A TX-Spitze (kein LDO mehr) |
| **VBUS** (USB 5 V → Lader) | **0,6 mm bzw. Fläche** (vorher 0,5 mm) | der IP2326 zieht bei 0,90 A Ladestrom **~1,6 A** aus 5 V |
| **VCC_EXT** (Q2 → J8/J9–J15) | **0,5 mm**, mindestens 0,25 mm | geschaltete Erweiterungsversorgung (Sensor-Module), bewusst mit Reserve |
| Alle Signale (LED, Sensor, Taster, UART, Gate, **I²C/Reserve**) | 0,25 mm | wenige mA |
| **USB_DP/USB_DM** | 0,25 mm, paarweise + gleich lang | 12 Mbit/s Full Speed |

Ein 2-Lagen-Board mit 1 oz Kupfer (35 µm) bei JLCPCB kann minimal 0,127 mm (5 mil) —
die Werte oben liegen also bequem im Standardprozess und kosten keinen Aufpreis.

## 2. Herleitung

**Ströme** (aus Datenblättern, nicht geschätzt):

- Pumpe **CONQUERALL DC 5 V** (Amazon `B0DHVMZ27Y`, seit 14.09.2026): Nennstrom **0,4 A**,
  **Anlaufstrom 3 A** (Datenblatt @5 V). Seit dem 2S-Umbau läuft sie an der **geregelten
  5-V-Schiene (5,10 V)**, also an ihrer Nennspannung — der unterspannungsbedingte Abschlag
  des 1S-Stands (2,2–2,5 A) entfällt. Sauerstoffpumpe zusätzlich 0,2 A ⇒ Nennlast 0,6 A.
- ⚠️ **Der Anlaufstrom ist der kritische Fall dieser Platine** (nicht der Dauerstrom): 3 A auf
  der 5-V-Schiene heißen aus dem Pack (η ≈ 0,90) **~2,8 A bei 6,16 V** bzw. ~2,0 A bei 8,4 V
  (Rechnung `docs/11_review-2s-umbau.md` §4.4). **VBAT ist damit kein 1,3-A-Netz mehr, sondern
  ein ~3-A-Netz — und VBUS trägt ~1,6 A statt 0,5 A.** Die 4,7-µH-Induktivität des 5-V-Bucks
  hat Isat 4,0 A (0,57 A Reserve gegen 3,43 A Spitze), die Valley-Stromgrenze des SY8113B liegt
  bei min. 3,0 A → **Messauftrag** (§6). Gegenmaßnahme gegen den Einbruch bleibt der
  **PWM-Softstart in der Firmware** (weiter empfohlen, nicht mehr Pflicht).
- 3,3-V-Buck **AP63203** (U_BUCK3): **2 A** Nennstrom; der ESP32-C6 zieht im WLAN-TX **382 mA**
  Spitze (Espressif Tab. 6-4) — beides gleichzeitig mit der Pumpe ist der Lastfall.
- Lader **IP2326** mit R_ISET 100 kΩ: **0,90 A** Ladestrom (bis 8,4 V) ⇒ bei 94 % Wirkungsgrad
  **~1,6 A Eingangsstrom aus 5 V**. Die Firmware pumpt nicht während des Ladens (Betriebsregel
  `hardware/schaltplan_v1.md` §6.1); der Vollastfall wäre sonst 2,8 A (Pumpenanlauf) + 0,9 A
  (Laden) auf dem Akkuknoten.

**Rechnung** nach IPC-2221A, Außenlage:

```
A [mil²] = (I / (k · ΔT^0.44))^(1/0.725)      k = 0,048 (außen)
Breite   = A / 1,378 mil                       (1 oz = 35 µm)
ΔT = 10 K (üblich für Handgeräte mit Kunststoffgehäuse)
```

| Strom | nötige Breite bei ΔT = 10 K | bei ΔT = 20 K |
|---|---|---|
| 0,50 A | 0,12 mm | 0,08 mm |
| 0,60 A | 0,14 mm | 0,09 mm |
| 0,90 A | 0,26 mm | 0,17 mm |
| 1,20 A | 0,39 mm | 0,25 mm |
| 1,60 A | 0,57 mm | 0,38 mm |
| 2,00 A | 0,78 mm | 0,51 mm |
| **2,80 A** | **1,24 mm** | **0,82 mm** |
| **3,00 A** | **1,37 mm** | **0,90 mm** |

Umgekehrt: **0,5 mm trägt nur 1,45 A bei 10 K** (1,96 A bei 20 K), 1,0 mm 2,39 A / 3,24 A,
1,5 mm 3,21 A / 4,35 A. Die 1,3 A des 1S-Stands lagen bei 0,5 mm noch bei 7,8 K — die neuen
**2,8–3 A** sind mit 0,5 mm **nicht** mehr zu halten (≈ 45 K). Deshalb: **VBAT und +5V als
Fläche bzw. ≥ 1,0 mm** legen (1,0 mm bei 2,8 A ≈ 14 K, 1,5 mm ≈ 7 K).

**Spannungsabfall** (Kupfer bei 70 °C) — der eigentliche Grund für die 0,5 mm
ist nicht die Erwärmung, sondern dass die Pumpe ihre Spannung behalten soll:

| Strecke | Widerstand | Abfall @0,6 A (Nennlast) | @2,8 A Anlauf (aus dem Pack) | @3,0 A Anlauf (5-V-Schiene) |
|---|---|---|---|---|
| 0,4 mm × 40 mm | 59 mΩ | 35 mV (0,7 %) | 165 mV (3,2 %) | 177 mV (3,5 %) |
| 0,5 mm × 40 mm | 47 mΩ | 28 mV (0,6 %) | 132 mV (2,6 %) | 141 mV (2,8 %) |
| **1,0 mm × 40 mm** | **23,5 mΩ** | **14 mV (0,3 %)** | **66 mV (1,3 %)** | **71 mV (1,4 %)** |
| 1,5 mm × 40 mm | 15,7 mΩ | 9 mV (0,2 %) | 44 mV (0,9 %) | 47 mV (0,9 %) |
| 0,25 mm × 40 mm | 94 mΩ | 56 mV (1,1 %) | 263 mV (5,2 %) | 282 mV (5,5 %) |

Zum Vergleich der Bauteile: der AO3400A hat **48 mΩ** Rds(on), die 1N5819WS
verliert ~0,35 V in Durchlassrichtung, die JST-Buchse ~20 mΩ pro Pol, und der
Buck selbst bringt den größten Posten mit (Verluste, Rippel, Regelreserve).
**Die Leiterbahn ist damit nicht der begrenzende Widerstand** — ab ~1,0 mm
(bzw. als Fläche) ist der Rest des Pfades die Grenze, nicht das Kupfer.

## 3. Warum nicht dünner (0,25 mm)?

Thermisch würde 0,25 mm reichen (0,88 A bei 10 K). Dagegen spricht:

1. Die Pumpe ist ein Motor mit Bürsten — der Anlaufstrom ist **seit 14.09.2026 bekannt**:
   Datenblatt der CONQUERALL nennt **3 A bei 5 V**; seit dem 2S-Umbau läuft sie an **5,10 V**, der
   Anlaufstrom wird also **voll wirksam** (3 A auf +5V, ≈ 2,8 A aus dem Pack). Bei 2,8 A hat eine
   0,25-mm-Bahn **5,2 %** Spannungsverlust, eine 0,5-mm-Bahn **2,6 %**, eine 1,0-mm-Bahn **1,3 %**.
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
| **VBAT** | high-current (0,5 mm) ⚠️ | **≥ 1,0 mm bzw. Fläche — die Automatik ist jetzt zu dünn** |
| **+5V** | power-branch (0,25 mm) ❌ | **≥ 1,0 mm bzw. Fläche — muss explizit gesetzt werden** |
| VBUS | high-current (0,5 mm) | 0,6 mm (1,6 A Ladestrom) |
| +3V3 | power-branch (0,25 mm) | **0,4 mm** — dicker als die Automatik |
| **PUMP_N / PUMP2_N** | **signal (0,25 mm)** ❌ | **0,5 mm — muss explizit gesetzt werden** |

`PUMP_N`/`PUMP2_N` heißen nicht wie Versorgungen, tragen aber den vollen Pumpenstrom; `+5V`
heißt wie eine Versorgung, bekommt von der Automatik aber nur 0,25 mm. Beides beim Verdrahten
explizit vorgeben (`--width 40` für VBAT/+5V, `--width 20` für die Pumpenleitungen) oder die
Strecken als Fläche legen — die Automatik allein legt sie zu dünn.

## 5. Wo die Breiten definiert sind (für die nächste Sitzung)

Die Sollbreiten liegen **nicht** in EasyEDA, sondern im Projekt — dort, wo sie
prüfbar und versioniert sind:

| Datei | Rolle |
|---|---|
| `hardware/easyeda/netclass_spec.json` | **die Definition**: je Netz Rolle, Sollbreite, Minimum, Strom, Erwärmung, Spannungsabfall — ⚠️ steht noch auf dem **1S-Stand (50 Netze)**; die 2S-Netzliste hat **68 Netze** und muss beim EasyEDA-Neuaufbau neu gerechnet werden (`docs/11_review-2s-umbau.md` §8.7) |
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
  R2/Q1) und die Breiten gegen den gemessenen Wert prüfen — erwartet werden **3 A @ 5,1 V**
  (≈ 2,8 A aus dem Pack). Auf 1,0 mm sind das ≈ 14 K (in Ordnung), auf 0,5 mm ≈ 45 K (zu viel).
- **VBAT und +5V im Layout als Fläche** führen und die Netzklassen aus der **2S-Netzliste
  (68 Netze)** neu erzeugen — `netclass_spec.json`/`s0_spec.json` sind noch 1S-Stand.
- **2 oz Kupfer** wäre die Alternative (halber Widerstand, ~45 K → ~27 K bei 0,5 mm), kostet bei
  JLCPCB aber Aufpreis und bringt beim Dauerstrom (0,6 A) nichts — für VBAT/+5V ist die
  Kupferfläche der bessere Weg.
- **Kontrollierte Impedanz** bietet JLCPCB nur ab 4 Lagen — bei 2 Lagen bleibt das
  USB-Paar kurz, parallel und gleich lang; bei 12 Mbit/s ist das ausreichend.
- **Kupfer unter der Antenne** des ESP32-C6-MINI-1 bleibt frei (Keepout) — das
  gilt auch für die GND-Fläche auf der Unterseite.
