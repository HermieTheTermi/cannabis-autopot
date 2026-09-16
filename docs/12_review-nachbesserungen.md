# Nachbesserungen aus dem externen Review (Fable 5, 16.09.2026)

Der Review bezog sich auf `hardware/schaltplan_v1_komplett.md` (maschinell aus der IR erzeugte
Schaltungsbeschreibung) und die Netzliste. **Bearbeitungsstand dieser Datei: lokal umgesetzt, noch
nicht in EasyEDA nachgezogen.**

## A. Umgesetzt (Schaltplan lokal korrigiert)

| Nr. | Befund | Beleg / Rechnung | Änderung |
|---|---|---|---|
| 1 | **AP63203 ist die Festspannungsversion** und darf nicht mit einem Feedbackteiler betrieben werden | Datenblatt des Herstellers: „The AP63203 and AP63205 have fixed output voltages of 3.3V and 5V"; im Kennwertblatt ist **VFB für den AP63203 = 3,27/3,30/3,33 V** (nicht 0,8 V). Fig. 21 („Typical Application Circuit of AP63203/AP63205") führt FB **ohne Teiler** direkt auf den Ausgang, Fig. 20 (einstellbare Version) zeigt dagegen R1/R2. Mit dem alten 47k/15k-Teiler hätte die Schleife ≈ 3,3 V × (1 + 47/15) = **13,6 V** angefordert → Überhöhung der 3,3-V-Schiene, Gefahr für U1 | Netz `FB_3V3` entfernt; **U_BUCK3 Pin 1 (FB) liegt direkt auf `+3V3`**; `R_FB3_TOP` (47 kΩ) und `R_FB3_BOT` (15 kΩ) entfallen |
| 2 | Der Gate-Klemmzweig (10 kΩ) kann gegen den 1-kΩ-GPIO-Zweig nicht abschalten | Mit 3,3 V am GPIO und 0,3 V Diodenspannung bleibt das Gate bei ≈ **2,97 V** — über der Schwellenspannung des AO3400A, der MOSFET bleibt an | `D3`, `D8`, `R_CLAMP1`, `R_CLAMP2` und die Netze `KLAMP1`/`KLAMP2` **entfallen ersatzlos**. Wirksam bleiben: (a) U7 sperrt `U_BUCK5 EN` → Pumpenversorgung aus, (b) im Reset sind die GPIOs hochohmig, die 47-kΩ-Pulldowns halten beide Gates auf 0 V |
| 3 | Das eingebettete Prüfprotokoll enthielt einen Fehler (`Pin 'mb (Drain)' an Q_PROT1 fehlt in der Netzliste`) | Eigener Werkzeugfehler: `hardware/design/checks.py` verwendete den **alten** Pin-Namen; dadurch liefen alle Prüfungen danach nie durch | Pin-Name auf den **am EasyEDA-Symbol gemessenen** Pin `5 D` gezogen (PSMN4R2-30MLDX: 1/2/3 = S, 4 = G, 5 = D). Zusätzlich: ein unbekannter Pin-Name muss künftig als **Werkzeugfehler** erscheinen, nicht als Design-Fehler |
| 8 | UV-Teiler mit 200 k/200 k ist zu hochohmig | Wächterstrom laut TPS3839-Datenblatt **150 nA typ., 500 nA max.**: über 200 kΩ ergibt das bis zu **0,1 V** Verschiebung am Teilerknoten ⇒ **~0,2 V** auf die Packspsannung | `R3a`/`R3b` auf **51 kΩ** (beide). Neuer Offset **+15 … +50 mV**, Teilerstrom 82 µA = **2 mAh/Tag** (0,1 % eines 2000-mAh-Packs) |
| 9 | Sensorversorgung direkt aus GPIO3 (U1 Pin 6) | Für frei anschließbare Sensormodule ist ein GPIO keine robuste Versorgung (Dauer-/Einschaltstrom, Kapazität) | Neu: **`Q_SENS`** (AO3401A, gleicher Typ wie Q2) als High-Side-Lastschalter von `+3V3` nach `SENSOR_PWR`, Gate über `EXT_SENS_EN` (IO3) mit **`R_SENS_GATE` 47 kΩ Pull-up** ⇒ ohne Freigabe sicher aus |

Ergänzend korrigiert: `schaltplan_v1.md` §2.4/§3.3 und die Stückliste waren in sich widersprüchlich
(§2.4 nannte für den 3,3-V-FB 100 kΩ/31,6 kΩ, §3.3 dagegen 47 kΩ/15 kΩ), und die Bauteiltabelle führte
den Pin `mb (Drain)`. Beides ist bereinigt; Netzlisten-Lint und BOM-Abgleich laufen grün
(**114 Bauteile** auf beiden Seiten).

## B. Offen — brauchen Datenblattbelege oder Bauteilauswahl

| Nr. | Befund | Stand |
|---|---|---|
| 4 | 17 A Überstromschwelle schützt Kabel, Stecker und Leiterbahnen nicht | **umgesetzt:** **F1** = Littelfuse 0452005.MRL, 5 A träge, 2410 (`C66503`, extended, +3 USD) in der Pack-Plus-Leitung vor allen Verbrauchern. Dauerlast 2,8–3,6 A = 56–72 % Nennstrom; Kurzschluss ~56 A ⇒ ~17 ms. Die Sicherung liegt bewusst im **Plus**-Zweig: der Lader misst den Strom batterieseitig intern, ein Bauteil in der Minusleitung würde nur den Massebezug verschieben. Ergänzend dokumentiert: zusätzlich vorhandene Schutzeinrichtung des Packs nutzen |
| 5 | Massepins des IP2326 (BAT_GND / PGND / EP) bei externem Low-Side-Schutz | **geklärt und entlastet** (`research/ip2326-schutz-massen.md`, belegt an den Datenblattfassungen V1.11/V1.6): Pin 24 ist ein **Detektionspin der Balancing-Funktion**, kein Massepfad, und soll bei Nichtnutzung offen bleiben. Ein intern niederohmiger Pfad zu PGND/EPAD ist **nicht dokumentiert**; einziger interner Pfad ist der Balancing-MOS, über `R_CB` (100 Ω) auf < 40 mA begrenzt — keine Überbrückung des 17-A-Schutzes. **Aber:** laut Datenblatt nicht ausgeschlossen (Massepins fehlen in den Absolutmaxima) und das Referenzdesign führt BAT− = GND als **einen** Knoten ⇒ unsere Trennung ist eine Abweichung. **Pflicht vor Inbetriebnahme:** Widerstand Pin 24 ↔ Pin 18 am unbestromten IC messen (muss hochohmig sein) und **BAT_MINUS nie mit Board-GND verbinden** |
| 6 | Akku-NTC fehlt (`R_NTC` 51 kΩ legt die Temperaturüberwachung still) | **umgesetzt:** **J18** (JST-XH-2P, dieselbe BOM-Position wie J4/J16/J17) + **R_NTC_PAR 82 kΩ 1 % 0805** (`C17840`). NTC = **100 kΩ B3950 ±1 %**, 0805 (`C919175`, Sunlord SDNT2012, **lose bestellen** — Handmontage am Kabel, nicht in der JLC-Bestückung). Schwellen damit **−0,1 / 45,6 / 55,6 °C** (Datenblatt: 0 / 45 / 55 °C). **Fail-safe:** Stecker ab ⇒ 1,64 V ⇒ Lader lädt nicht. **Achtung:** ohne den 82-kΩ-Parallelwiderstand liegen 2,0 V an ⇒ Lader blockiert dauerhaft als „zu kalt" |
| 7 | USB-C: 5,1-kΩ-Rd allein sagt nichts über den erlaubten Quellenstrom | **geklärt, Maßnahme dokumentiert:** Der IP2326 hat laut Datenblatt **keine BC1.2-/DCP-Erkennung** (DP/DM dienen nur einer Spannungsanforderung 5,4/6/7 V) und **keine einstellbare Eingangsstrombegrenzung**; zahlenmäßig belegt ist nur „max. 15 W Eingang" und die VIN-Unterspannungs-Regelschleife über `R_UVSET` (68 kΩ ⇒ 4,35 V). Aufgabe: 8,4 V × 0,90 A = 7,56 W ⇒ bei 90 % Wirkungsgrad ≈ **1,68 A** aus 5 V — es ist eine **5-V/2-A-Quelle** zu verwenden (Ladegerät, kein beliebiger PC-Port). DM/DP des Laders bleiben **bewusst unbestückt**, weil diese Leitungen im Projekt die **MCU-USB-Daten** (U1 IO12/IO13) führen. Bei schwacher Quelle regelt die Eingangsunterspannungsschleife den Strom von selbst herunter |

## C. Einzelpunkte aus der Mängelliste (bewertet, teils Maßnahme, teils Messauftrag)

| Punkt | Bewertung | Maßnahme |
|---|---|---|
| `R_CB` = 100 Ω, 0805 | Bei ~4,2 V über dem Widerstand sind das **176 mW** — ein 0805 mit 125 mW wäre überlastet | **umgesetzt:** **1206 / 0,25 W** (`C17901`, Basic, gleicher Wert und Toleranz; 70,6 % Auslastung, nach Derating bis ≈ +95 °C Umgebung zulässig). Das Datenblatt-Referenzdesign verwendet dort ebenfalls 100 Ω in 1206 |
| 22-µF-MLCCs in 0805 | Wirksame Kapazität unter DC-Bias deutlich kleiner als Nennwert | Vor der Bestellung Datenblattkurve prüfen oder auf 1210 ausweichen; betrifft Ein-/Ausgangskondensatoren der Wandler |
| `C3` 100 µF gegen Anlaufströme | 1 A für 1 ms entlädt 100 µF bereits um 10 V | Bleibt als Transientenpuffer; die **Anlaufströme der Pumpen müssen gemessen** werden (siehe unten) |
| I²C mit 1 kΩ Serie + 4,7 kΩ Pull-up | Low-Pegel am Stecker idealisiert 3,3 V × 1 k/(1 k + 4,7 k) = **0,58 V**, das liegt unter dem üblichen V_IL-Grenzwert (0,3 × VDD = 0,99 V) | Kein Fehler; Hinweis in der Doku, dass Modul-eigene Pull-ups den Pegel verschlechtern können |
| `VCC_EXT` abgeschaltet | Angeschlossene Module können über ihre Schutzdioden rückspeisen, wenn Signale HIGH bleiben | `Q2` ist keine Rückstromsperre. Firmware-Pflicht: GPIO-Zustände beim Abschalten definieren (Doku) |
| GPIO4/5/15 (Strapping) | Nur relevant, wenn diese Pins beim Reset extern belastet werden | Belegung prüfen und in der Doku festhalten; die Reserve-Stecker (IO15/16/17/21/23) sind alle herausgeführt |
| USB-Datenleitungen (D− GPIO12, D+ GPIO13) | Plausibel; ESD-Platzierung und differentielle Führung sind PCB-Themen | Layout: Längen/Gleichlauf prüfen, Serienwiderstände nur falls Espressif sie fordert |
| `D1`/`D4` (1N5819WS, SOD-323) | Freilaufstrom, Pulsdauer und Tastverhältnis gegen den exakten Typ prüfen | Messauftrag: Strom am Prüfstand aufnehmen, dann Datenblattvergleich |
| Pumpenanlauf | Dauer-, Anlauf- und Blockierstrom beider Pumpen fehlen vollständig | **Messauftrag am Aufbau.** Bis dahin sind U_BUCK5, L_BUCK5, Q1/Q5, D1/D4 und C3 nur vorgedimensioniert |
| Ladebetrieb ohne Power-Path | Verbraucher und Akku teilen sich den Laderausgang: 0,90 A sind kein Nettoladestrom, bei Pumpenbetrieb ist Nettoentladung möglich | Nutzungskonzept dokumentieren; Ladeterminierung im Aufbau prüfen |
| „Kein Aufwärtswandler" | Widersprüchlich formuliert | Gemeint ist „kein zusätzlicher Boost-Wandler für die Lastversorgung"; der IP2326 ist selbst ein Boost-Lader. Formulierung in §1 des Dokuments wurde präzisiert |
| Blattkoordinaten statt PCB-Layout | Schaltstromschleifen, Thermal-Pads, ADC-Masse, Antennen-Keep-out sind erst im Layout beurteilbar | Arbeitsteilung bleibt: Layout und Routing macht der Nutzer |
