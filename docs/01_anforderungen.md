# Anforderungen — Smart Grow Topf

Stand: 11.09.2026 (Projektstart) · Geometrie-Details: [`02_architektur-und-geometrie.md`](02_architektur-und-geometrie.md)

## Entscheidungen (vom User festgelegt)

| Bereich | Entscheidung |
|---|---|
| **Topfgröße** | **Ø 140 mm** (bleibt), Erdbehälter **150 mm hoch** — nur der Erdebehälter; die Wassertankhöhe darunter wurde berechnet |
| **Wassertank** | **1,0 L** nutzbar, im gleichen Ø 140-Grundriss unter dem Erdbehälter → Wasserstand 71 mm, Kammer 82 mm |
| **Pumpe** | **Peristaltische Dosierpumpe 6 V** (quetscht einen Schlauch) — Medium kommt nie mit der Pumpenmechanik in Kontakt, selbstansaugend, präzise dosierbar |
| **Energie** | **Akku** (nicht Netz) |
| **Elektronik** | **Eigene Platine (PCB)**, untergebracht in einer **seitlichen Wulst** am Topf |
| **MCU** | **ESP32-C6-MINI-1** (nacktes Modul) auf der eigenen PCB (korrigiert 11.09.2026, Review 3: XIAO verworfen) |
| **Feuchte-Sensor** | **Kapazitiv v1.2 (mit LDO), analoger Ausgang**, von oben in die Erde gesteckt, seitlich am Controller angeschlossen |
| **Bewässerungsweg** | Pumpe fördert nach **oben** auf einen **3D-gedruckten Verteilerring auf der Erdoberfläche** (Top-Drip), Rücklauf tropft in den Tank |
| **Nährlösung** | **Nur Wasser** — ein Behälter, keine automatische Düngerdosierung. Dünger nur ins Substrat |
| **Leer-Meldung** | Bei leerem Tank: kurz ins WLAN → **Telegram** (final, keine Alternative) |
| **Versionierung** | **GitHub-Repository**, Fortschritt wird laufend committet und gepusht |

## System-Konzept (Top-Drip mit Rücklauf)

```
        Verteilerring (3D-Druck, Ø ≤ 105 mm)
   ┌──────────◉───────────◉──────────┐   ← Wasser von oben auf die Erdoberfläche
   │        ERDE / SUBSTRAT          │   Erdbehälter Ø127 innen × 150 mm (≈1,6 L)
   │        ⊗ Sensor (75 mm tief)    │   analog an Controller
   │        ▒▒ Blähton 25 mm ▒▒      │   Dränage + Partikelfilter
   └──────────────┬──────────────────┘
        Luftspalt 30 mm (Gießfüße)
   ┌──────────────┴──────────────────┐
   │      WASSERTANK 1,0 L           │   Ø134 innen, max. Wasserstand 71 mm
   │   ⌄ Saugschlauch → Pumpe ──┐    │
   └────────────────────────────┼────┘
              Wulst: Pumpe, PCB, ESP32-C6-Modul, Akku, Kanal
```

## Regelkreis (Firmware-State-Machine)

1. Kapazitiver Sensor (analog) liest die Substratfeuchte (Messebene 75 mm).
2. ADC **>** Schwelle (zu trocken — Sensor ist invertiert!) → **Pumpe EIN**, dosiert in Portionen.
3. Überschüssiges Wasser läuft durch das Substrat, durch die Blähton-Dränage, zurück in den Tank.
4. **10–20 min** nach Pumpenende erneut messen (Wicking-Verzögerung, Top-Drip):
   - ADC **fällt** → Feuchte steigt → ok → Cooldown bis zum nächsten Zyklus.
   - ADC **fällt nicht** → **Tank leer / Pumpe verstopft / Sensor nicht im Substrat** → **Telegram-Alarm**.
5. Hysterese ±100–150 ADC gegen Flattern; Median-Filter über 10–20 Samples.

## Technische Eckpunkte

- **MCU:** ESP32-C6-MINI-1 (WiFi 6, Deep-Sleep 7 µA, ADC1 auf IO0–IO6), 13,2 × 16,6 mm — Lader, LDO und USB sind eigene Bauteile (siehe `hardware/schaltplan_v1.md`).
- **Pumpen-Ansteuerung:** Logic-Level-N-MOSFET (Low-Side) + Freilaufdiode 1N5819, **Gate 4,7 kΩ, Pulldown 47 kΩ** (Werte aus Review 1 korrigiert — maßgeblich ist `hardware/schaltplan_v1.md`).
- **Sensor:** analoger Ausgang direkt an ADC1, VCC per GPIO schalten (nur während der Messung an); invertierte Kennlinie (trocken ≈ 2100–2600, nass ≈ 1200–1500).
- **Akku:** Zelle mit Schutz-PCB, Laden über **MCP73831T-2 auf unserer Platine** (USB-C-Durchbruch in der Wulst).
- **Strombudget:** Deep-Sleep µA-Bereich, Pumpe nur Minuten pro Zyklus → Versorgung für Wochen.

## Offene Punkte

- Batteriezelle final (Bautiefe Wulst 30 mm) — BOM-Check läuft.
- Pumpen-Abmessungen → Wulstbreite parametrisch anpassen.
- Kalibrierwerte `dry`/`wet` am echten Substrat (nach dem ersten Durchlauf).
- Optional V2: Tankstand-Sensor (float switch) als Redundanz zum Feuchte-Kriterium.
