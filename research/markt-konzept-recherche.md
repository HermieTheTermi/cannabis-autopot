# Markt & Konzept — Smart Grow Topf (Agent-Ergebnis, kompakt)

> ⚠️ Agent 4 lief in ein 600s-Timeout, bevor er seine finale Markdown-Datei schrieb.
> Die Kerninhalte (Marktprodukte, Open-Source-Repos, Kritik an der User-Idee) wurden aus dem Live-Transcript extrahiert und hier konsolidiert.
> Stand: 10.09.2026

---

## 1. Fertige Produkte (Marktvergleich, aus dem Transcript)

| Produkt | Preis | Bemerkung |
|---|---|---|
| Lechuza-Classico/Color-Serie (selbstbewässernd) | ~110 € | keine Pumpe, Wicking-Prinzip, kein ESP32 — teuer |
| Parrot Pot (Smart Planter, 2016) | eingestellt | Sensor + App, im Markt nicht mehr verfügbar |
| Click and Grow Smart Garden | ~70–130 € | kompakt, kein Cannabis-fähiges Erd-/Pumpen-Design |
| AutoPot / Blumendünger-Systeme (AquaValve) | ~40–90 € | passives Bottom-Feeding via Ventil, keine Elektronik — der engste Verwandte zum Konzept |

**Positionierung:** Die eigene Lösung (ESP32 + Peristaltik + kapazitiver Sensor + Telegram) ist **günstiger als Lechuza** und **elektronisch smarter als AutoPot**. Das ist die Lücke, die das Projekt füllt.

## 2. Open-Source-Vorbilder (GitHub, aus dem Transcript)

| Repo | Ansatz | Übernehmbar |
|---|---|---|
| **Lumics/Plantwatery** | ESP32, Solarzelle, Bodensensor, Pumpe, MQTT, OTA | die engste Vorlage: Solar zu ersetzen durch LiPo, MQTT durch Telegram |
| **DanielFang88/esp32-auto-watering** | ESP32 + Sensorn + Pumpe | Grundschema Sensor→Pumpe |
| **SethCSanti/SelfWateringPlantSystem** | selbstbewässerndes System | Reservoir/Kapillar-Mechanik |
| **Chrissyuh/SmartWateringFlowerPot** | Smart Watering Pot | kompakte Firmware-Logik |

Nützlich als Lektüre / Referenz für die eigene State-Machine — nicht copy-paste, da Prozess (Telegram + Peristaltik + Akku) abweicht.

## 3. Kritische Bewertung der User-Idee („Wasser von unten pumpen, Überschuss zurücktropft")

**Kern-Fachfrage:** Ist das für Cannabis in **Erde** sinnvoll?

- **Ja, wenn richtig gemacht** — das ist im Kern ein **Bottom-Watering / Sub-Irrigated-Planter (SIP)** Skid. Der große Vorteil: Wurzeln werden von unten gleichmäßig versorgt, Pflanzenseite bleibt trocken, weniger Pilzdruck, Nährstoffe werden von unten zugeführt. AutoPot und viele Grower nutzen genau dieses Prinzip.
- **Die zwei Hauptfallen (aus der Recherche):**
  1. **Salzanreicherung (der größte Punkt):** Weil der Überschuss in den Tank *zurücktropft und rezirkuliert*, konzentrieren sich Düngersalze im Substrat- bzw. im Tank über Wochen auf → Sensor driftet Richtung „nass", Nährstoffe klettern in Symptome der Überdüngung. **Gegenmittel:** Tank regelmäßig wechseln/leeren (nicht endlos rezirkulieren), EC prüfen, gelegentlich von oben mit reinem Wasser spülen („flush").
  2. **Staunässe / Sauerstoffmangel:** Erde darf nie *dauerhaft* im Wasser stehen (Wurzelfäule). Deshalb ist die **Gießfüßchen-/Luftspalt-Trennung** im Inneren zwingend: Topf auf Standfüßen, 2–5 cm Luftspalt überm Wasserspiegel. Genau deshalb muss die Pumpe **nur bei Bedarf** (trockener Sensor) laufen — nicht als Dauersättigung.
- **Mechanik:`** Erde/Dochte heben Wasser nur ~15–30 cm — das gepumpte Wasser in den **unteren Topfbereich** (oder ein Bewässerungsring) geben, von dort verteilt Kapillarwirkung nach oben. Eine 2–3 cm Blähton-Drainageschicht am Topfboden hilft.

## 4. Empfehlung für den Prototyp (einfache, robuste Richtung)

1. **Außentopf/Reservoir** mit **Gießfüßen** für den Innentopf (Luftspalt) + 2–3 cm Blähton-Drainage.
2. **Peristaltische Pumpe** (6 V) im Tank → Schlauch nach oben in den Topfboden-Bereich.
3. **Kapazitiver Sensor** auf halber Topfhöhe (Wurzelzone), analog am ESP32 (v1.2 mit LDO).
4. **ESP32** im Deep-Sleep, Sensor-VCC geschaltet, Pumpe über MOSFET + Pull-down + Freilaufdiode.
5. **Leer-Meldung** per Telegram, LED/OLED lokal als Fallback.
6. **Erste Testphase:** Reservoir frisch halten, EC beobachten, ggf. wöchentlich Flush.

---

## Referenzen (aus dem Transcript verifiziert)

- AutoPot AquaValve / Bottom-Feeding: https://www.autopot.co.uk
- Lumics/Plantwatery: https://github.com/Lumics/Plantwatery
- DanielFang88/esp32-auto-watering: https://github.com/DanielFang88/esp32-auto-watering
- SethCSanti/SelfWateringPlantSystem: https://github.com/SethCSanti/SelfWateringPlantSystem
- Chrissyuh/SmartWateringFlowerPot: https://github.com/Chrissyuh/SmartWateringFlowerPot
