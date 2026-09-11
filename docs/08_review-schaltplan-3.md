# Review 3 (+ Durchgang 4 und 5): Querprüfung aller Dokumente

Stand: 11.09.2026 · Dritter Review-Zyklus. **Andere Methode als Review 1 (Auslegung gegen
Datenblätter) und Review 2 (Netzlisten-Struktur):** diesmal Querabgleich **zwischen allen
Dokumenten** (Schaltplan ↔ JLCPCB-BOM ↔ Netzliste ↔ BOM ↔ Anforderungen ↔ README), mit zwei
neuen, im Repo liegenden Prüfprogrammen.

**Ergebnis: 11 Befunde in diesem Zyklus, 4 zusätzliche in Durchgang 4, in Durchgang 5 keine neuen.**
Nach den Korrekturen sind beide Prüfer sauber (`exit 0`) und die Textabgleiche leer.

---

## 1. Neue Prüfwerkzeuge (beide im Repo, beide `exit 0`)

| Werkzeug | Prüft |
|---|---|
| `scripts/check_netlist.py` | Bauteil nur auf einem Netz · Netz mit nur einem Knoten · Pin auf zwei Netzen · im Schaltplan dokumentierte Bauteile, die in der Netzliste fehlen |
| `scripts/check_bom_consistency.py` | Designatoren in beide Richtungen · LCSC-Codes · **Werte bei R/C numerisch normiert** (100 nF = 100nF, 4,7 kΩ = 4.7k, 499 Ω = 499R) · Bauteile der Netzliste, die in Dokument oder BOM fehlen · **doppelte Designatoren** in der BOM |

**Ehrlich dazu:** beide Prüfer brauchten selbst drei Iterationen, bis sie verlässlich waren.
Version 1 verglich Werte als Text (25 Falschmeldungen), Version 2 sah nur zwei Richtungen
(übersah C11/C12), Version 3 fand doppelte Designatoren nicht. Die Fehlalarme sind im Verlauf
dieses Zyklus dokumentiert — ein Prüfer, der Falschmeldungen produziert, ist gefährlicher als
keiner, weil man ihn ignoriert.

## 2. 🔴 Sicherheitsrelevanter Befund

**D4 (SS34, Brücke VBUS → VBAT) stand noch in der JLCPCB-BOM.** Der Prüfer meldete nur „D4 fehlt
im Schaltplan" — beim Nachsehen war es umgekehrt schlimmer: das Bauteil war aus dem Schaltplan
entfernt, aber in der Bestellliste geblieben.
- **Wirkung, wäre es bestückt worden:** bei gestecktem USB-C fließt Strom über die Schottky direkt
  in den Akku — **ungeregelt**, nur durch den Diodenabfall begrenzt (5 V − 0,4 V ≈ 4,6 V an der
  Zelle). Das ist ein Überladepfad, der die Zelle zerstören oder in Brand setzen kann.
- **Korrektur:** D4 aus BOM und Netzliste entfernt, im Schaltplan als „entfernt" mit Begründung
  dokumentiert.
- **Konsequenz, die jetzt klar dasteht:** es gibt **keinen Verpolschutz** — Verpolsicherung ist
  allein die mechanische Kodierung der JST-Stecker.

## 3. Querabgleich: veraltete Angaben (alle korrigiert)

| # | Befund | Betroffen |
|---|---|---|
| Q1 | **Ladestrom 249 mA** stand noch in den Auslegungsnotizen, während R_PROG auf 3,9 kΩ (256 mA) geändert war | `schaltplan_v1.md` |
| Q2 | **XIAO an vier Stellen** (ASCII-Schema, Entscheidungszeile, BOM-Zeile, nächste Schritte) | `README.md` |
| Q3 | **XIAO, Gate 220 Ω, XIAO-Onboard-Lader** als Anforderungsstand | `docs/01_anforderungen.md` |
| Q4 | **Gate 220 Ω / Pulldown 10 kΩ** in §4b und §6, obwohl Review 1 auf 4,7 kΩ / 47 kΩ korrigiert hatte | `bom_entscheidung.md` |
| Q5 | Alte Gate-Beschaltung als „✅ geprüft" geführt, XIAO-Platine in den nächsten Schritten | `docs/05_review-v1.md` |
| Q6 | **SS34 als „Verpolschutz optional"** gelistet, obwohl das Bauteil entfallen ist; R1/R2 mit alten Werten | `pcba_verfuegbarkeit_jlc.md` |
| Q7 | Recherche-Ebene ohne Warnhinweis (nennt XIAO, Adafruit-Pumpe, 220 Ω) | `hardware_auswahl_bom.md` |
| Q8 | **BOM-Summen falsch:** als Zwischensumme standen 42,85 €, tatsächlich 38,64 €; das **JLCPCB-Handling (~28 € für 10 Extended-Positionen) fehlte komplett** — die BOM sah billiger aus, als die Bestellung wird | `bom_entscheidung.md`, `README.md` |

## 4. Vollständigkeit und Kleinteile

| # | Befund | Korrektur |
|---|---|---|
| V1 | **EPAD (Pin 49) des Moduls** war in der Netzliste nicht erwähnt | auf GND ergänzt, mit Espressif-Hinweis („soldering the EPAD is not a must, however it optimizes thermal performance") |
| V2 | **C11/C12 existierten nur in der Netzliste**, nicht in Schaltplan-Dokument und BOM — und kein Prüfer hätte das gemerkt (Lücke, die zur Erweiterung des Prüfers führte) | in Dokument und BOM ergänzt; BOM jetzt 6 × 100 nF, 43 Bauteile, identisch in allen drei Dateien |
| V3 | Handling-Kosten behauptet (10 Extended), aber nie gegengeprüft | nachgezählt: **10 Extended-Positionen** — stimmt exakt |
| V4 | Ladestrom-Wert in der BOM-Rechnung nicht gepflegt | nachgerechnet: 38,64 € Zwischensumme, 47–49 € Gesamt, + ~28 € JLC |

## 5. Durchgang 4 und 5

**Durchgang 4** (systematische Suche nach Zahlen, die sich in den Reviews geändert hatten —
`249 mA`, `220 Ω`, `4,02`, `15 µA`, `52 × 42`, `SS34`): 3 weitere Reste gefunden und korrigiert
(Q1, Q6 und der SS34-Hinweis in den Auslegungsnotizen).

**Durchgang 5** (Netzliste vollständig von Hand gelesen, alle 27 Netze Knoten für Knoten):
**keine neuen Befunde.** Geprüft und für richtig befunden:
- Diodenorientierungen: D1 Kathode an VBAT / Anode an PUMP_N (Freilauf am Low-Side-Schalter) ·
  D3 Anode am Gate / Kathode am MAX809-Ausgang (Klemme bei Unterspannung) · D2 Anode über R4,
  Kathode an GND · D_LEDCHG Kathode an STAT
- Lader: PROG 3,9 kΩ gegen GND, STAT führt die LED-Kathode, VDD an VBUS mit 4,7 µF
- LDO: EN an VBAT (nicht an +3V3), CIN an VBAT, COUT an +3V3
- Sensorweg: VCC über IO3, AOUT über R6 in Reihe auf ADC1_CH0, Filterkondensator am ADC
- USBLC6 in Durchschleif-Beschaltung (Pins 3/4 bzw. 1/6 auf derselben Leitung, VBUS als Referenz)
- Alle Stecker vollständig belegt (Akku 2-pol, Sensor 3-pol, Pumpe 2-pol, USB-C inkl. Schirm)

Randfall geprüft und als **harmlos** eingestuft: liegt VBAT knapp unter +3V3 (gegen Ende der
Entladung), kann die Klemme D3 minimal in Durchlassrichtung geraten. Der Strom bleibt im
µA-Bereich, und die Firmware sperrt die Pumpe bereits bei 3,4 V. Kein Handlungsbedarf.

## 6. Konvergenz — was jetzt noch offen ist, sind keine Fehler mehr

Fünf Durchgänge, gefundene echte Fehler: **2 (Review 1) + 6 (Review 2) + 11 (Review 3) + 3
(Durchgang 4) + 0 (Durchgang 5)**. Beide Prüfprogramme laufen sauber, die Textabgleiche sind leer.
Weiteres Suchen am Schreibtisch findet nichts mehr, weil die restlichen Punkte **Messungen und
Entscheidungen** sind, keine Fehler:

1. **Messungen am Prototyp:** Förderrate der Pumpe bei 3,7 V · ADC-Ausgangsbereich des Sensors
   (Sättigung über 2,5 V?) · Zellabschaltung des PCM.
2. **Entscheidungen:** Pumpen während des Ladens sperren (F6) · zweiter Wächter auf der
   3,3-V-Schiene (F11) · Ladestatus/VBUS an einen GPIO führen (Review 2) · Gehäuseparameter per
   OpenCode nachziehen (Antennenbereich, Platinengröße).
3. **Vor dem Bestücken:** vier Pinbelegungen am Datenblattbild prüfen (MCP73831, ME6211, MAX809,
   AO3400A) · Steckerpolungen festschreiben · RF-Endtest.
