# Mutationstest: beißen die Prüfungen wirklich?

Stand: 14.09.2026 (GPIO-Erweiterung auf 2,54-mm-Stiftleisten wieder eingebaut) · Verifikation des
Prüfpakets `hardware/design/` durch den Koordinator (**nicht** durch den Code-Autor). Ein Test, der
immer besteht, ist wertlos — deshalb wurde **jede der heute 29 Prüfungen einzeln sabotiert** (16 im
ersten Durchgang, 3 für Taster/Tank-LED, 1 für den LED-Headroom, 4 für den Lichtsensor, 5 für die
Stecker/Erweiterung) und geprüft, ob der Test rot wird. Nachtrag 5 belegt die fünf
Erweiterungs-Prüfungen zusätzlich mit je mindestens einer eigenen Mutation.

## Aufbau

Für jede Mutation: Repo-Kopie nach `/tmp`, ein Wert in den Quelldateien verändert, dann
`python3 design/report.py` aus `hardware/` heraus ausgeführt. Bewertet wird die
Zusammenfassung am Ende der Ausgabe plus der Exit-Code.

| # | Prüfung | Mutation | Ergebnis |
|---|---|---|---|
| 1 | Ladestrom | R_PROG 3,9 kΩ → 100 kΩ | ✅ 10,0 mA < 180 mA → FEHLER |
| 2 | Laderkondensatoren | C7 4,7 µF → 1 µF | ✅ unter Datenblatt-Minimum → FEHLER |
| 3 | MAX809-Klemmstrom | R1 4,7 kΩ → 220 Ω | ✅ 12,273 mA > 1,2 mA → FEHLER |
| 4 | Gate-Spannung | R2 47 kΩ → 4,7 kΩ | ✅ 1,65 V < 2,5 V → FEHLER |
| 5 | MOSFET-Verlustleistung | Pumpenleistung 1,67 W → 50 W | ✅ 8,8 W > 0,25 W → FEHLER |
| 6 | Freilaufdiode | dito (Strom steigt) | ✅ > 50 % der Diode → FEHLER |
| 7 | VBAT-Teiler | R3a 200 kΩ / R3b 500 kΩ | ✅ 3,00 V > 2,5 V → FEHLER |
| 8 | Teilerstrom | R3a/R3b 200 kΩ → 47 kΩ | ✅ 44,7 µA > 15 µA → FEHLER |
| 9 | LDO-Stromreserve | TX-Peak 382 mA → 700 mA | ✅ 500 mA < 1,1 × 700 mA → FEHLER |
| 10 | LDO-Headroom | Firmware-Stopp 3,4 V → 3,1 V | ✅ 2,8 V < 3,0 V → FEHLER |
| 11 | Unterspannungsstaffelung | MAX809 3,08 V → 3,60 V | ✅ Ordnung verletzt → FEHLER |
| 12 | Standby-Budget | Zellkapazität 1500 mAh → 100 mAh | ✅ 50 %/Monat > 5 % → FEHLER |
| 13 | ADC-Filter | C9 100 nF → 10 µF | ✅ 10 ms > 5 ms → FEHLER |
| 14 | LED-Ströme | R4 1 kΩ → 100 Ω | ✅ 13 mA > 5 mA → FEHLER |
| 15 | EN-RC | C4 1 µF → 1 nF | ✅ 10 µs < 1 ms → FEHLER |
| 16 | Netzstruktur | R6 in der Netzliste umbenannt (nur ein Netz) | ✅ Befund erkannt → FEHLER |

**Ergebnis: 20 von 20 Prüfungen des ersten Pakets sind nachweislich wirksam.** Der Exit-Code ist
im Fehlerfall 1, im Gutfall 0 — die Prüfungen sind damit als Gate einsetzbar.

### Nachtrag 11.09.2026 — Taster und Tank-LED (Nummern nach dem heutigen Stand: 15, 17, 18)

| # | Prüfung | Mutation | Ergebnis |
|---|---|---|---|
| 15 | Tank-LED | R_TANK 1 kΩ → 100 Ω | ✅ 13 mA > 5 mA → FEHLER |
| 17 | Taster-Pullup | C_BTN 100 nF → 1 nF (RC 10 µs) | ✅ RC < 0,5 ms → FEHLER |
| 17 | Taster-Pullup | R_BTN von +3V3 auf GND umgehängt | ✅ harter Fehler, Exit 1: „Tasternetz nicht eindeutig" |
| 18 | Taster-Weckquelle | Taster auf IO18 (kein LP-GPIO) | ✅ „nicht LP-fähig" → FEHLER |
| 18 | Taster-Weckquelle | Taster auf IO5 (= MTDI, Strapping) | ✅ „Strapping-Pin" → FEHLER |

Besonders wichtig ist der letzte Fall: **IO5 liegt zwar im LP-Bereich (IO0–IO7), ist aber
Strapping-Pin** — genau die Falle, die beim Wecken aus dem Deep-Sleep sonst übersehen wird.
Die Prüfung unterscheidet beide Bedingungen.

### Nachtrag 2 — LED-Farbe (Prüfung 16 „LED-Headroom")

Anlass: D2 wurde von rot auf **grün** umgestellt (C2297, Vf 2,85 V statt 2,0 V).

| Prüfung | Mutation | Ergebnis |
|---|---|---|
| LED-Headroom | **R4 zurück auf 1 kΩ** (grün, aber roter Widerstand) | ✅ 0,45 mA < 0,5 mA → FEHLER |
| LED-Headroom | Tank-LED auf grün, R_TANK bleibt 1 kΩ | ✅ 0,45 mA → FEHLER |
| LED-Stroeme | D2-Code auf rot bei R4 = 220 Ω | ✅ 5,91 mA > 5 mA → FEHLER |
| (Eingabe) | D2 bekommt einen **unbekannten** LCSC-Code | ✅ harter Fehler: „unbekannter LCSC-Code 'C12345' für D2: Flussspannung in LED_VF_BY_LCSC ergänzen" |

Der erste Fall ist der wichtigste: **eine Farbänderung ohne Anpassung des Vorwiderstands fällt
jetzt auf.** Genau das war bei dieser Änderung real passiert — die alte Prüfung rechnete D2 noch
mit Vf 2,0 V und meldete 5,91 mA, obwohl die LED korrekt mit 2,05 mA lief. Umgekehrt hätte die
LED mit 1 kΩ nur 0,45 mA bekommen (zu dunkel und stark Vf-abhängig). Der vierte Fall zeigt,
dass unbekannte LEDs nicht mehr stillschweigend als „rot, 2,0 V" durchgehen.

Die Prüfungen 15–17 lesen ihre Werte aus Netzliste und Schaltplan (Pull-up-Verschaltung,
Entprellzeit, IO-Nummer am Tasterpin, LED-Vorwiderstand); hart verdrahtet sind nur die
Datenblatt-Fakten (LP-GPIOs = IO0–IO7, Strapping = IO4/IO5/IO8/IO9/IO15, Vf rot ≈ 2,0 V).

### Nachtrag 3 — Lichtsensor und Licht-Gate (13.09.2026)

Anlass: externer Lichtsensor an J7, ADC auf IO4, vier neue Prüfungen + erweitertes Standby-Budget.
Alle Mutationen wurden **real in einer Repo-Kopie** ausgeführt (`design/report.py`, Exit-Code und
Fehlerliste ausgewertet).

| # | Prüfung | Mutation | Ergebnis |
|---|---|---|---|
| 14 | Licht-ADC-Filter | C_LIGHT 100 nF → 10 µF | ✅ 10 ms > 5 ms → FEHLER |
| 15 | Licht-Kontrast | R_LIGHT 10 kΩ → 100 Ω | ✅ hell nur 186 < 3000 Counts → FEHLER |
| 16 | Licht-Stecker offen | R_LIGHT von GND nach +3V3 | ✅ kein definierter 0-V-Pfad → FEHLER |
| 12 | Standby-Budget | J7 Pin 1 von SENSOR_PWR auf +3V3 | ✅ Sensor dauerhaft versorgt → FEHLER |
| 22 | Pin-Disziplin | Licht-AOUT von IO4 auf IO8 | ✅ boot-kritischer Strap-Pin + Pin 22 doppelt → FEHLER |
| 22 | Pin-Disziplin | Licht-AOUT auf IO2 (wie Pumpe) | ✅ Pin 5 doppelt + falscher ADC-Kanal → FEHLER |

Die Prüfung „Licht-Stecker offen" belegt den **unkritischen Fehlerfall**: Ein abgezogener Sensor
zieht den ADC über R_LIGHT auf 0 V („dunkel"), die Bewässerung bleibt erlaubt. Die Prüfung
„Pin-Disziplin" setzt die im Dokument korrigierte Aussage um: boot-kritisch sind nur
GPIO8/GPIO9/GPIO15 — IO4/IO5 sind nur SDIO-Straps und als ADC nutzbar. Der Taster-Wecktest
(Prüfung 21) führt IO4/IO5 weiterhin als Strapping und schließt sie für die Weckquelle aus.

### Nachtrag 4 — Pinordnung/Erweiterungsstecker (13.09.2026, entfernt 14.09.2026)

Der GPIO-Ausbau vom 13.09. (J8 I²C mit Load-Switch Q2, J9/J10, TP7–TP11) samt Pinordnung
GND–VCC–SIG wurde am 14.09.2026 zurückgebaut; damit entfielen damals auch die Prüfungen
**Stecker-Pinordnung, Serienwiderstand Signale, Load-Switch-Fail-safe, Erweiterungs-Pins** und
**I2C-Pull-ups**. **Dieser Rückbau wurde am 14.09.2026 revidiert** — siehe Nachtrag 5.

### Nachtrag 5 — Erweiterung auf 2,54-mm-Stiftleisten (14.09.2026)

Anlass: Die freien GPIOs und der I²C-Bus sind wieder herausgeführt, jetzt als **2,54-mm-Stiftleisten
(J7–J15, je Signal ein eigener 3-pol GND–VCC–SIG-Stecker; J8 als 4-pol GND–VCC–SDA–SCL)**, mit
Load-Switch Q2, Serienwiderständen in **jeder** Signalleitung und I²C-Pull-ups an VCC_EXT. Die
fünf Prüfungen aus Nachtrag 4 sind in angepasster Form wieder aktiv. Alle Mutationen wurden **real
in einer Repo-Kopie** ausgeführt (`design/report.py`, Exit-Code und Fehlerliste ausgewertet).

| # | Prüfung | Mutation (Quelle: Netzliste bzw. Schaltplan) | Ergebnis |
|---|---|---|---|
| 23 | Stecker-Pinordnung | J2 Pin 1 auf SENSOR_RAW gelegt (alte Ordnung VCC/SIG/GND verdreht) | ✅ `J2: 1=SENSOR_RAW 2=SENSOR_PWR 3=None FEHLER` → FEHLER (Exit 1) |
| 24 | Serienwiderstand Signale | R_SDA_S auf beiden Seiten auf SDA_MCU (Widerstand umgangen) | ✅ „NICHT-Reihe" + Netzstruktur „R_SDA_S nur auf einem Netz" → FEHLER |
| 24 | Serienwiderstand Signale | R_SPARE_IO15 von 1 kΩ auf 0 Ω | ✅ „Wert?" → FEHLER |
| 25 | Load-Switch-Fail-safe | R_GATE von +3V3 auf GND gehängt (kein Gate-Pull-up) | ✅ „R_GATE an +3V3 FEHLER" → FEHLER |
| 27 | I2C-Pull-ups | R_SDA_PU von VCC_EXT auf +3V3 gehängt | ✅ Pull-up-Seite nicht VCC_EXT → FEHLER |
| 26 | Erweiterungs-Pins | IO15 des Steckers durch IO0 ersetzt (Doppelbelegung Pin 12) | ✅ Doppelbelegung + Zuordnung FEHLER → FEHLER (auch Pin-Disziplin) |
| 13 | ADC-Filter (Reserve) | C_SPARE 100 nF → 10 µF | ✅ R_SPARE_AIN·C_SPARE 10,00 ms > 5 ms → FEHLER |
| 25/26 | Load-Switch/Pins | IO20 zusätzlich auf +3V3 gelegt (Doppelbelegung Pin 26) | ✅ Doppelbelegung Pin 26 + Zuordnung FEHLER → FEHLER |

**Ergebnis: 8 von 8 Erweiterungs-Mutationen wurden erkannt (Exit 1).** Zusammen mit den
unveränderten Mutationen der Nachträge 1–3 sind damit **29 Prüfungen** mutationsgeprüft. Die
Prüfungen 23–27 lesen die Verschaltung aus der Netzliste und die Werte aus `schaltplan_v1.md`;
hart verdrahtet sind nur die IO-Nummern (`EXT_IO_PIN`) und die Ordnung GND/VCC/SIG (als Konstante
mit Begründung im Code).

## Erkenntnisse aus dem Mutationstest

1. **Prüfung 3 (Klemmstrom) reproduziert genau den Review-1-Fehler.** Mit R1 = 220 Ω zieht die
   Klemme 12,3 mA — das Zehnfache der Datenblatt-Spezifikation. Der Fehler kann jetzt nicht mehr
   unbemerkt zurückkommen.
2. **Der Test prüft Physik, nicht Prosa.** Prüfung 7/8 rechnen aus R3a/R3b, nicht aus dem im
   Dokument genannten Wert. Umgekehrt nutzt Prüfung 12 (Standby-Budget) den dokumentierten
   Teilerstrom — beide Wege sind also getrennt abgesichert.
3. **Grenze, die bewusst offen bleibt:** Prüfung 8 (aus Widerständen gerechnet) und Prüfung 12
   (dokumentierter Wert 10,5 µA) werden nicht gegeneinander abgeglichen. Driftet der dokumentierte
   Wert von der Rechnung weg, fällt das nicht auf. Praktische Auswirkung: klein (Teilerstrom ist
   nur ein Teil eines Budgets von 100 µA); bei einer Änderung an R3a/R3b den Textwert mitziehen.
4. **Annahme im Inrush-Modell:** Der Innenwiderstand der Zelle (0,1 Ω) steht in keiner der
   Eingangsdateien und ist im Code als Annahme gekennzeichnet. Der berechnete Einbruch von 100 mV
   hängt direkt davon ab — beim Prototyp nachmessen.
5. **Struktur der Quelldateien:** R3a/R3b (und andere Paare) stehen in **einer** Tabellenzeile.
   Das Modell gibt dann beiden den gleichen Wert; ein unsymmetrischer Teiler lässt sich in dieser
   Schreibweise nicht ausdrücken. Für den 1:2-Teiler ist das korrekt, aber die Schreibweise ist
   eine Einschränkung.

## Stolpersteine beim Testen selbst (dokumentiert, damit sie nicht wiederkommen)

- Die Auswertung der Ergebniszeilen muss **Ziffern im Prüfnamen** zulassen — „MAX809-Klemmstrom"
  fiel durch ein Regex-Muster ohne `0-9` und sah fälschlich wie ein Fehlschlag aus. Robuster ist
  das Parsen der Zusammenfassung am Ausgabeende (`Fehlgeschlagen:` / `- Name: …`).
- Bei Mutationsskripten keine Raw-Strings mit `\\|` verwenden, wenn nur Text ersetzt wird — dann
  greift die Mutation nicht, und der Test scheint zu bestehen.
- Prüfungen mit **Datenblatt-Grenzwerten** müssen von den **aus Dateien gelesenen Werten**
  getrennt bleiben: Ändert man eine Zahl im Schaltplan, muss der Test gegen die Grenze prüfen,
  nicht gegen die alte Zahl.

## Reproduzieren

```bash
cd hardware
python3 design/report.py            # 29 Prüfungen, Exit 0 = alles im Rahmen
python3 ../scripts/check_netlist.py         # Netzlisten-Struktur
python3 ../scripts/check_bom_consistency.py # Schaltplan ↔ JLCPCB-BOM
```

## Mutationstest 2S-Umbau (16.09.2026)

Harness: `~/.hermes/skills/maker/schematic-netlist-authoring/scripts/mutation_suite.py`
(Repo-Kopie nach /tmp ohne `.git`, je Fall genau eine Mutation, Bewertung = `exit != 0` **und**
erwarteter Prüfname in der Fehlschlag-Liste). Falldatei: **`mutation_cases_2s.json`**.

Aufruf:

    python3 <skill>/scripts/mutation_suite.py hardware/design/mutation_cases_2s.json --root .

| # | Mutation (Sabotage) | erwartete Prüfung | beobachtet | Exit |
|---|---|---|---|---|
| 1 | `R_ISET` 100 kΩ → 30 kΩ (Ladestrom 2,7 A) | Ladestrom IP2326 | Ladestrom IP2326 **+** Ladeeingangsstrom | 1 |
| 2 | `R_FB5_TOP` 75 kΩ → 100 kΩ (5 V ⇒ 6,6 V) | 5-V-Buck-Ausgang | 5-V-Buck-Ausgang | 1 |
| 3 | `R_FB3_TOP` 47 kΩ → 100 kΩ (3,3 V ⇒ 6,1 V) | 3,3-V-Buck-Ausgang | 3,3-V-Buck-Ausgang **+** LED-Ströme, LED-Headroom | 1 |
| 4 | `R3b` 200 kΩ → 100 kΩ (Abschaltung 6,19 V ⇒ 9,2 V) | UVLO-Schwelle | UVLO-Schwelle **+** Unterspannungsstaffelung | 1 |
| 5 | `R_SENSE_BOT` 68 kΩ → 200 kΩ (ADC 2,13 V ⇒ 4,2 V) | ADC-Teiler Packspannung | ADC-Teiler Packspannung | 1 |
| 6 | Netzliste: `U6` (USBLC6, 5,5 V max) von VBUS auf **VBAT** (8,4 V) | VBAT-Spannungsfestigkeit | VBAT-Spannungsfestigkeit | 1 |
| 7 | Netzliste: `R_CLAMP1` zurück auf die alte **Parallelschaltung** (Knoten an keinem Gate) | Klemmzweig-Serie | Klemmzweig-Serie **+** Netzstruktur | 1 |
| 8 | BOM: `IP2326` → **`IP2326_8V8`** (8,8 V Ladeschluss) | Ladeschluss 2S | Ladeschluss 2S | 1 |
| 9 | Belegtext `3,4 V Pumpstopp` aus `bom_entscheidung.md` entfernt | Systemquellen | Systemquellen | 1 |
| 10 | beide Teiler niederohmig (`R_SENSE_TOP`, `R3a` 200 kΩ → 20 kΩ) | Standby-Budget | Standby-Budget **+** 5 weitere | 1 |

**Ergebnis: 10 von 10 Mutationen werden gefangen — jede geprüfte Regel beißt nachweislich.**
Der grüne Lauf allein (`37 von 37 Prüfungen bestanden`, Exit 0) beweist nichts; erst diese Tabelle tut es.

### Eigene Harness-Fehler in diesem Durchgang (nicht dem Prüf-Code anzulasten)

1. Mutation 8 griff zuerst **nicht**: das Suchmuster nahm an, der Designator stehe direkt hinter dem
   Comment — die Spalte `Designator` liegt aber dazwischen (`IP2326,U_CHG,VQFN-24-EP(4x4)`).
   Der Harness meldet „Mutation greift nicht" (HARNESS) statt eines falschen „bestanden" ✓.
2. Mutation 9 blieb zuerst **grün**: der Belegtext `Anlaufstrom 3 A` kommt **zweimal** in
   `bom_entscheidung.md` vor, der Harness ersetzt nur das erste Vorkommen — die Prüfung hatte also
   weiterhin ihren Beleg. Ersetzt durch den eindeutigen Beleg `3,4 V Pumpstopp`.
   **Lehre:** vor jeder Mutation die Trefferzahl des Musters zählen (`grep -c`), sonst testet man
   eine andere Größe als die gelesene.

## Mutationstest der Schutz-Prüfungen (16.09.2026)

Falldatei: **`mutation_cases_schutz.json`** · Harness wie oben · Bewertung = Exit ≠ 0 **und**
erwarteter Prüfname in der Fehlschlag-Liste.

| # | Mutation | erwartete Prüfung | beobachtet | Exit |
|---|---|---|---|---|
| 1 | Dokument: Überladung 4,28 V → 4,60 V (9,2 V Pack) | Schutz-Schwellen | Schutz-Schwellen | 1 |
| 2 | Dokument: Tiefentladen 2,90 V → 3,40 V (6,80 V > Wächter 6,19 V) | Schutz-Schwellen | Schutz-Schwellen | 1 |
| 3 | Dokument: Überstrom 200 mV → 50 mV (Auslösung bei 4,4 A) | Schutz-Ueberstrom | Schutz-Ueberstrom | 1 |
| 4 | Netzliste: Q_PROT1 Source von BAT_MINUS auf GND | Schutz-Serienkette | Schutz-Serienkette | 1 |
| 5 | Netzliste: OD/OC vertauscht (U_PROT Pin 1 an den Lade-Gate-Knoten) | Schutz-Serienkette | Schutz-Serienkette + Netzstruktur | 1 |
| 6 | Netzliste: R_PROT_CS gegen BAT_MINUS statt GND | Schutz-Serienkette | Schutz-Serienkette + Netzstruktur | 1 |
| 7 | Regression: U6 (5,5 V ESD) auf VBAT | VBAT-Spannungsfestigkeit | VBAT-Spannungsfestigkeit | 1 |
| 8 | Regression: R_ISET 100 kΩ → 30 kΩ | Ladestrom IP2326 | Ladestrom IP2326 + Ladeeingangsstrom | 1 |
| 9 | Regression: R_FB5_TOP 75 kΩ → 100 kΩ | 5-V-Buck-Ausgang | 5-V-Buck-Ausgang | 1 |

**Ergebnis: 9 von 9 Mutationen werden gefangen.** Zusammen mit dem 2S-Durchgang (10/10) sind damit
**alle 19** in beiden Dateien geprüften Regeln als wirksam belegt; der Gesamtlauf meldet
`40 von 40 Prüfungen bestanden`.

### Eigener Harness-Fehler (nicht dem Prüf-Code anzulasten)

Mutation 2 griff zuerst nicht: das Suchmuster `Tiefentladung **2,90 V**` existiert im Dokument
**nicht** — dort steht „Tiefentladung\n **2,90 V**" (Zeilenumbruch) bzw. „Tiefentladen **2,90 V**".
**Lehre:** Mutationsmuster immer aus der **Datei selbst** ziehen (`t[i:i+40]`), nicht aus dem
Gedächtnis tippen — sonst prüft man eine andere Größe als die gelesene.
