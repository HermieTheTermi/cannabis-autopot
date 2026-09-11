# Mutationstest: beißen die Prüfungen wirklich?

Stand: 11.09.2026 · Verifikation des Prüfpakets `hardware/design/` durch den Koordinator
(**nicht** durch den Code-Autor). Ein Test, der immer besteht, ist wertlos — deshalb wurde
**jede der 20 Prüfungen einzeln sabotiert** (16 im ersten Durchgang, 3 für Taster/Tank-LED, 1 für den LED-Headroom) und geprüft, ob der Test rot wird.

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

**Ergebnis: 20 von 20 Prüfungen sind nachweislich wirksam.** Der Exit-Code ist im Fehlerfall
1, im Gutfall 0 — die Prüfungen sind damit als Gate einsetzbar.

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
python3 design/report.py            # 20 Prüfungen, Exit 0 = alles im Rahmen
python3 ../scripts/check_netlist.py         # Netzlisten-Struktur
python3 ../scripts/check_bom_consistency.py # Schaltplan ↔ JLCPCB-BOM
```
