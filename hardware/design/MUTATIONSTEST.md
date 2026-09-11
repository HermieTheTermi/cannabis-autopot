# Mutationstest: beißen die Prüfungen wirklich?

Stand: 11.09.2026 · Verifikation des Prüfpakets `hardware/design/` durch den Koordinator
(**nicht** durch den Code-Autor). Ein Test, der immer besteht, ist wertlos — deshalb wurde
**jede der 16 Prüfungen einzeln sabotiert** und geprüft, ob der Test rot wird.

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

**Ergebnis: 16 von 16 Prüfungen sind nachweislich wirksam.** Der Exit-Code ist im Fehlerfall
1, im Gutfall 0 — die Prüfungen sind damit als Gate einsetzbar.

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
python3 design/report.py            # 16 Prüfungen, Exit 0 = alles im Rahmen
python3 ../scripts/check_netlist.py         # Netzlisten-Struktur
python3 ../scripts/check_bom_consistency.py # Schaltplan ↔ JLCPCB-BOM
```
