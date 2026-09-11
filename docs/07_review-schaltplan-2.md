# Review 2: Schaltplan V1 — Netzliste und Auslegungsdetails

Stand: 11.09.2026 · Zweiter Durchgang, anderer Blickwinkel als `06_review-schaltplan.md`:
Diesmal wurde nicht die Auslegung gegen die Datenblätter geprüft (das war Review 1), sondern die
**maschinenlesbare Netzliste strukturell** — plus die Punkte, die Review 1 nicht angesehen hat.

Werkzeug: **`scripts/check_netlist.py`** (neu, im Repo). Es prüft vier Dinge:
Bauteil liegt nur auf einem Netz · Netz hat nur einen Knoten · ein Pin liegt auf zwei Netzen ·
im Schaltplan dokumentierte Bauteile, die in der Netzliste fehlen.

**Ergebnis: 6 Fehler in der Netzliste gefunden und behoben, 3 neue Hinweise, 1 Entscheidung
vorbereitet.** Der Schaltplan-*Text* war in allen Fällen korrekt — fehlerhaft war nur die
Netzliste, also genau die Datei, die später ins EDA-Tool importiert wird.

---

## 1. 🔴 Fehler in der Netzliste (alle behoben)

| # | Fehler | Wie er gefunden wurde | Auswirkung ohne Korrektur |
|---|---|---|---|
| N1 | **R_PROG fehlte komplett** (keine einzige Zeile) | Lint-Regel 4 (Abgleich gegen die Bauteiltabelle des Schaltplans) | Ladestrom nicht programmiert → der Lader hätte mit ungültigem PROG-Pin gearbeitet, Ladestrom undefiniert |
| N2 | **R6 kurzgeschlossen** (beide Anschlüsse auf `SENSOR_AOUT`) | Lint-Regel 1 | Serienwiderstand wirkungslos → ADC-Pin ungeschützt (der Fehler, den Review 1 gerade behoben hatte) |
| N3 | **Status-LED-Kette unterbrochen:** R4 Pin 2 lag auf `GND` statt am LED-Anodenknoten; D2 hatte nur seinen Kathodenanschluss | Lint-Regel 1 (D2 nur ein Netz) + manuelles Nachlesen | LED dauerhaft aus, R4 als nutzloser Widerstand nach GND |
| N4 | **Lade-LED-Kathode auf `GND`** statt auf U3 Pin 1 (STAT) | Lint-Regel 1 + Datenblattlogik (STAT ist der Senken-Ausgang) | LED leuchtet **dauerhaft**, unabhängig vom Ladestatus — und der Laderausgang arbeitet gegen GND |
| N5 | **LDO-Enable (U4 Pin 3) auf `+3V3`** statt auf VBAT/VIN | manuelle Prüfung der Netzliste | Der Regler soll sich selbst freischalten — er startet dann möglicherweise nie. `EN` gehört an `VIN` |
| N6 | **UART-Serienwiderstand R_UART hing in der Luft** (nur ein Netz) | Lint-Regel 1 | kein funktionierender Debug-Pfad |

Zusätzlich aufgeräumt: die Netzliste enthielt eine Zeile `GND,R4,3` — ein **dritter Anschluss an
einem 2-poligen Widerstand**, also ein reiner Tippfehler.

**Neue Struktur nach der Korrektur:** 119 Zeilen · 27 Netze · 48 Bauteile · Lint **exit 0**.
Neu hinzugekommen sind die Netze `PROG`, `LED_STAT_A`, `STAT_CHG`, `SENSOR_RAW`, `UART_TP` sowie
sechs Testpunkte (TP1–TP6) — womit auch die Testpunkt-Forderung aus Review 1 erfüllt ist.

## 2. 🟠 Neuer Hinweis: ADC-Eingangsbereich könnte im trockenen Bereich sättigen

- Der kapazitive Sensor v1.2 wird mit 3,3 V versorgt und gibt laut Projekt-Doku im **trockenen**
  Zustand die **höhere** Spannung aus.
- Der ESP32-C6-ADC liegt bei 11 dB Dämpfung bei etwa **0–2500 mV** Messbereich. Liegt der
  Sensorausgang im trockenen Zustand über ~2,5 V, **sättigt der ADC** — und ausgerechnet der
  Bereich „trocken" (der die Pumpe auslöst!) verliert seine Auflösung.
- **Korrektur offen bis zur Messung:** am realen Aufbau AOUT gegen GND messen (trocken und
  gesättigt). Übersteigt er 2,5 V, kommt ein **2:1-Teiler** vor den ADC (oder der Sensor läuft an
  einer niedrigeren Versorgung). Der Serienwiderstand R6 ist bereits eingeplant; ein Teiler würde
  ihn ersetzen.
- Das ist ein **Firmware-relevanter** Punkt: die Kalibrierwerte trocken/nass sind erst sinnvoll
  aufnehmbar, wenn der Messbereich geklärt ist.

## 3. 🟡 Weitere Hinweise (bewusst nicht geändert)

1. **Bürstenstörungen der Pumpe:** ein DC-Motor erzeugt am Kollektor Störspektren, die über
   VBAT auf den LDO und damit in den ADC einstreuen können. Der 100-µF-Elko fängt nur
   niederfrequent. **Empfehlung:** ein **100 nF direkt an den Pumpenklemmen** (am Stecker J4) —
   ein Basic-Teil, das Messrauschen während des Pumpens reduziert.
2. **LDO-Verlustleistung beim Senden:** (4,2 V − 3,3 V) × 0,38 A ≈ **340 mW** im SOT-23-5, also
   ~85 K Erwärmung für die Dauer eines TX-Bursts. Für Sekundenbruchteile unkritisch, für
   Dauerbetrieb (z. B. ein Firmware-Update über WLAN) wäre es zu viel. Kein Handlungsbedarf,
   aber im Hinterkopf behalten.
3. **Ladestatus nicht auslesbar:** U3 Pin 1 (STAT) steuert nur die LED. Wer den Ladestatus auch
   **in der Firmware** wissen will, führt STAT zusätzlich auf einen freien GPIO (mit
   Serienwiderstand) — nützlich für „Akku wird geladen"-Meldungen per Telegram. Option, kein Muss.
4. **VBUS-Erkennung fehlt ebenfalls:** um „nicht pumpen während des Ladens" (Review 1, F6)
   zuverlässig umzusetzen, braucht die Firmware ein Signal. Zwei Wege: VBUS über einen
   Spannungsteiler auf einen GPIO (dann ist die Regel hart umsetzbar), oder die Firmware schließt
   es aus dem Ladestatus (STAT). **Empfehlung:** Teiler auf einen freien GPIO, zwei Widerstände.

## 4. Was Review 2 bestätigt hat

- Der **Schaltplan-Text** war in allen sechs Fällen korrekt; die Fehler saßen ausschließlich in der
  CSV. Genau deshalb ist der Lint jetzt Teil des Repos: die CSV ist das, was ins Layout geht.
- Die Netzzahl ist plausibel: 27 Netze bei 48 Bauteilen, alle Netze haben ≥ 2 Knoten, kein Pin
  liegt auf zwei Netzen.
- Alle im Schaltplan dokumentierten Bauteile (U1–U7, C1a–C10, R1–R6, R_EN, R_BOOT, R_GPIO8,
  R_PROG, R_LEDCHG, R_UART, D1–D4, D_LEDCHG, D2, Q1, J1/J2/J4/J5, SW1/SW2) sind in der Netzliste
  vorhanden — der Abgleich läuft automatisch im Lint.

## 5. Stand der offenen Punkte (kumuliert aus beiden Reviews)

| # | Offen | Wo es hängt |
|---|---|---|
| 1 | Vier Pinbelegungen am Datenblattbild prüfen (MCP73831, ME6211, MAX809, AO3400A) | vor dem Footprint |
| 2 | Polung J1 (Akku) und J4 (Pumpe) festschreiben | Layout |
| 3 | ADC-Bereich des Sensors messen (Punkt 2 oben) | Prototyp |
| 4 | Entscheidung: Pumpen während Laden sperren + VBUS-/Ladestatus-Erkennung an einen GPIO | Schema-Ergänzung |
| 5 | Entscheidung: zweiter Wächter auf der 3,3-V-Schiene (Review 1, F11) | optional |
| 6 | 100 nF an den Pumpenklemmen ergänzen | Layout-nah |
