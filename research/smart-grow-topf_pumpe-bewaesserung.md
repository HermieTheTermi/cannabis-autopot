# Pumpe + Bewässerungsmechanik — Bottom-Watering Smart-Grow-Topf (ESP32)

> Stand: 10.09.2026 · Alle Preise/Links live über Amazon.de (browser-harness) verifiziert.
> Konzept: Erde oben, Wassertank unten, Tauchpumpe pumpt bei Bedarf von unten nach oben, Überschuss tropft zurück in den Tank, kapazitiver Sensor steuert via ESP32.

---

## 1. TL;DR — Empfehlung

| Komponente | Empfehlung | Preis |
|---|---|---|
| **Pumpe** | 12V-Mini-Tauchpumpe, 240 L/h, Förderhöhe max. 3 m (2er-Pack) | **10,99 €** |
| **Schalter** | Fertiges Dual-MOSFET-Trigger-Modul DC 5–36V (8er-Pack) | **6,49 €** |
| **Netzteil** | 12V/1A Steckernetzteil (0,4 A Pumpenstrom) | ~8 € |
| **Topf** | Innentopf mit Drainage-Löchern auf Standfüßen (Luftspalt 2–5 cm) über Reservoir | – |
| **Gießmenge** | 0,5–0,8 L pro Gießvorgang (10 % des Topfvolumens bei 5–8 L) | – |
| **Laufzeit** | 12V-Pumpe: **10–20 s** pro Gießrunde (bei 0,3–0,4 m Förderhöhe) | – |

**Warum nicht die 3–5V-Mini-Pumpe?** Die günstigste 3–5V-Tauchpumpe hat laut Datenblatt **max. Förderhöhe nur 0,5 m** (Neuhold N4244). Ein 5–8L-Topf + Reservoir darunter bedeutet 30–45 cm Steighöhe → die Pumpe arbeitet nahe ihrer Grenze und liefert nur noch ~30–40 L/h. Die 12V-Variante kostet ~2 € mehr, hat 3 m Förderhöhe und damit massig Reserve.

---

## 2. Pumpenvergleich

### (a) Mini-Tauchpumpe (submersible) — EMPFOHLEN

| Produkt | Spannung | Strom | Durchfluss | Förderhöhe | Preis | Link |
|---|---|---|---|---|---|---|
| **12V Brushless-Tauchpumpe, 2 Stk.** (Kreiselpumpe, 4,8W) ⭐ Empfehlung | 12V | ~0,4 A | 240 L/h | **max. 3 m** | **10,99 €** | https://www.amazon.de/dp/B0CDK7GQF2 |
| CONQUERALL DC 5,5–12V, 200 L/h, Durchfluss einstellbar | 5,5–12V | – | 200 L/h | – | 14,99 € | https://www.amazon.de/dp/B0DLNNXGQP |
| Flintronic USB-Tauchpumpe 200 L/h (USB-Stecker) | 3,5–9V | 1–3W | 200 L/h | – | 8,49 € | https://www.amazon.de/dp/B07TW39QXP |
| RUNCCI-YUN 3er-Pack Mini-Tauchpumpe + 3 m Schlauch | 3–5V | 100–200 mA | 100 L/h | **max. 0,5 m** | 8,99 € | https://www.amazon.de/dp/B08BZBN29C |
| Neuhold N4244 (Datenblatt, einzeln) | 3–5V | max. 200 mA | 100 L/h @5V | **max. 0,5 m** | 2,95 € | https://www.neuhold-elektronik.at/pumpen/tauchpumpe-3-5v-liegend |

- ✅ Sehr günstig, leise (Brushless), einfach im Tank zu versenken, Schlauch meist dabei.
- ⚠️ Nur für Kurzbetrieb konzipiert (Herstellerhinweis „nicht für Dauergebrauch") — für uns egal, gepumpt wird ja nur sekundenweise.
- ⚠️ **Förderhöhe ist der kritische Parameter**: Fließformel `Q(H) ≈ Qmax × (1 − H/Hmax)`. Bei 0,35 m Steighöhe liefert die 3–5V-Pumpe nur noch ~30 L/h, die 12V-Pumpe noch ~210 L/h.

### (b) Peristaltikpumpe (Schlauchpumpe) — präzise, aber langsam

| Produkt | Spannung | Durchfluss | Preis | Link |
|---|---|---|---|---|
| Kamoer NKP (Snap-In-Pumpenkopf) | 12V | ≥ 70 ml/min | **12,40 €** | https://www.amazon.de/dp/B0DYTYPHX5 |
| G528 Mini-Peristaltikpumpe | 12V | 60–150 ml/min | 16,14 € | https://www.amazon.de/dp/B0F99R78ML |

- ✅ Selbstansaugend, **dosiert exakt**, Richtung per Umpolung umkehrbar, **kein Rückfluss/Siphon** im Stillstand (Schlauch dichtet ab) — ideal für Dünger/Nährstoff-Dosierung in den Tank.
- ❌ 0,5 L dauert bei 100 ml/min **5 Minuten** — als alleinige Gießpumpe zu langsam. Als Zusatz für Nährlösung sinnvoll.

### (c) Luftpumpe + Venturi — ❌ NICHT geeignet

Venturi/Airlift ist eine Hydroponik-Technik (Blasen transportieren Wasser im Rohr mit). Für das Pumpen in Erde zu schwach und ungenau — für dieses Projekt keine Option.

---

## 3. ESP32-Ansteuerung der Pumpe

**Grundregel:** Ein ESP32-GPIO liefert max. ~12 mA (sicher) / 40 mA (absolut) bei 3,3V — eine 200–400-mA-Pumpe **niemals direkt** anschließen.

### MOSFET (empfohlen, lautlos, PWM-fähig)

**Variante A — Fertigmodul (ohne Löten):**
- Dual-MOSFET-Trigger-Modul **DC 5–36V, 15A/400W**, Trigger ab **3,3V** → direkt am GPIO. 8 Stk für **6,49 €**: https://www.amazon.de/dp/B0DG8B58PM
- Verdrahtung: 12V-Netzteil → Modul-IN → Modul-OUT → Pumpe; GND gemeinsam mit ESP32; Signal-Pin → GPIO.

**Variante B — diskret (IRLZ44N, Logic-Level):**
- 10 Stk IRLZ44N für 6,99 €: https://www.amazon.de/dp/B0H4ZQBY7W
- Schaltung (Low-Side-Schalter):
  - GPIO → 220 Ω → Gate
  - Gate → 10 kΩ → GND (Pull-Down: Pumpe aus, wenn GPIO floatet/Reset)
  - Drain → Pumpe(−), Pumpe(+) → 12V; Source → GND
  - **Freilaufdiode (Flyback) antiparallel zur Pumpe**: 1N4007 reicht bei 0,4 A, besser 1N5819 (Schottky) — schützt den MOSFET vor Spannungsspitzen beim Abschalten der Motorspule
  - IRLZ44N leitet bei Vgs = 3,3V bei diesen Mini-Strömen (≤0,5 A) problemlos (Rds(on) 22 mΩ @ 10V, bei 3,3V etwas höher, bei 0,5 A unkritisch)

### Relais-Modul (Alternative — hörbar, verschleißt)

- 5V-1-Kanal-Relais mit Optokoppler, 4 Stk für 8,99 €: https://www.amazon.de/dp/B0GCYPQQKR
- ✅ Galvanische Trennung, einfache Verdrahtung; die meisten Module triggern mit 3,3V-Logik (prüfen: Jumper/Opto-Typ).
- ❌ Klickgeräusch, mechanischer Verschleiß (bei täglichen Gießzyklen hält es trotzdem Jahre), **kein PWM** möglich; Spule zieht ~70 mA aus der 5V-Schiene (nicht vom GPIO!).

### L298N / DRV8833 — Overkill

L298N hat ~2V Spannungsabfall → für eine 5V-Pumpe bräuchte man ≥7V — unpraktisch. DRV8833 (H-Brücke) lohnt nur, wenn die Pumpe **beide Richtungen** laufen soll (z. B. Peristaltikpumpe für Dosieren + Rückspülen). Für eine Richtung ist ein MOSFET billiger und besser.

### Stromversorgung

| Verbraucher | Versorgung |
|---|---|
| ESP32 | eigenes USB-Netzteil (oder 5V-Pin) |
| 12V-Pumpe | 12V/1A-Steckernetzteil (Pumpe zieht nur ~0,4 A) |
| 5V-Pumpe | 5V/1–2A-USB-Ladegerät |
| **Immer:** GND von Netzteil und ESP32 verbinden! | |

---

## 4. Topf-Mechanik (Bottom-Watering konkret)

### Die 4 Konzepte

**a) Docht-System (Wick)** — passiv, ohne Pumpe: Ein Polyester-/Nylon-Docht hängt aus dem Topf ins Reservoir; die Erde saugt per Kapillarwirkung. ❌ Für diesen Aufbau nur als **Backup** sinnvoll: Dochte heben Wasser nur ~10–20 cm und sind langsam; bei unserem aktiven Pumpen-Design unnötig kompliziert.

**b) Gießfüßchen / Standfüße (SIP-Prinzip, „Sub-Irrigated Planter")** — der wichtigste Baustein: Der Innentopf steht **nicht** direkt im Wasser, sondern auf Füßen/Rost **2–5 cm über dem Wasserspiegel** (Luftspalt = Wurzelbelüftung). Wasser kommt nur bei Bedarf (bei uns: aktiv gepumpt) von unten.

**c) Kapillarwirkung der Erde** — Erde (Torf/Coco-Mix) saugt Wasser je nach Substrat ~15–30 cm hoch. Deshalb: gepumptes Wasser in den **unteren** Topfbereich leiten — von dort verteilt es sich von selbst nach oben. Eine 2–3 cm dicke Schicht Blähton/Perlit am Topfboden verteilt das Wasser gleichmäßig und verhindert Staunässe am Topfboden.

**d) „Reservoir unterm Topf + Loch im Topf"** — einfache, aber riskante Variante: Steht die Erde dauerhaft im Wasser, werden die Wurzeln erstickt (Sauerstoffmangel). Cannapot warnt explizit: Bottom-Watering nur punktuell, nie als Dauerzustand — „ständig nasse Füße" riskieren. → Genau deshalb pumpt unser Design **nur bei trockenem Sensor** und der Überschuss tropft ab.

### Konkreter Aufbau (empfohlen)

```
┌─────────────────────────┐
│  Innentopf (5–8 L Erde) │  ← kapazitiver Sensor in der Erde
│  Boden: Drainage-Löcher │
│  2–3 cm Blähton-Schicht │  ← verteilt gepumptes Wasser
│  Docht (optional Backup)│
├─────────────────────────┤
│  Standfüße/Rost (2–5 cm)│  ← Luftspalt = Wurzelatmung
├─────────────────────────┤
│  Außentopf/Reservoir    │  ← Tauchpumpe liegt im Wasser
│  Pumpe → Schlauch →     │     Schlauch endet am Topfboden
│  Überlauf zurück in Tank│     (oberhalb des Wasserspiegels
│                         │      = kein Siphon-Rückfluss!)
└─────────────────────────┘
```

- **Pumpe → Schlauch → Topf:** Schlauch von der Tauchpumpe durch ein Loch im Reservoir direkt in den Innentopf-Bodenbereich (oder ein dünner Bewässerungsring auf der Erde). Wasser steigt, durchfeuchtet die Erde kapillar, **Überschuss tropft durch die Drainage-Löcher zurück ins Reservoir** (Wasserkreislauf, kein Nährstoffverlust).
- **Rückfluss verhindern:** Schlauch-Ende immer **oberhalb des Wasserspiegels** enden lassen, sonst saugt der Siphon-Effekt das Reservoir nach dem Abschalten langsam in den Topf. (Peristaltikpumpe hätte dieses Problem konstruktionsbedingt nicht.)
- **Tank-leer-Erkennung:** Pumpe 10–20 s laufen lassen → 2–3 min warten → Sensor vergleichen. Kein Feuchteanstieg = Tank leer (oder Schlauch verstopft / Pumpe trocken gelaufen). Erst nach 2–3 Fehlversuchen Alarm melden (Erde braucht Zeit, Wasser aufzunehmen — Messung direkt nach dem Pumpen ist trügerisch).

---

## 5. Wassermenge + Timing (berechnet)

### Gießmenge

Richtwert (Cannapot-Guide, verifiziert): **10–20 % des Topfvolumens** pro Gießvorgang bei Erde.

| Topfgröße | Gießmenge (10 %) | Gießmenge (20 %) |
|---|---|---|
| 5 L | **0,5 L** | 1,0 L |
| 6 L | 0,6 L | 1,2 L |
| 8 L | 0,8 L | 1,6 L |

**Empfehlung:** 0,5–0,8 L pro Event, in **2–3 kleine Runden mit 1–3 min Pause** (Erde braucht Zeit zum Aufsaugen; „langsam in Etappen" ist auch die Cannapot-Empfehlung). Abbruch, wenn der Sensor Feuchtigkeitsanstieg meldet — nicht stur die volle Menge pumpen.

### Pumpen-Laufzeit

Fließformel: **Q(H) ≈ Qmax × (1 − H/Hmax)**

**12V-Pumpe (240 L/h, Hmax = 3 m), Steighöhe 0,35 m:**
- Q ≈ 240 × (1 − 0,35/3) ≈ **210 L/h ≈ 3,5 L/min**
- 0,5 L → **~9 s** (real mit Verlusten: 15–20 s pro Runde)

**3–5V-Pumpe (100 L/h, Hmax = 0,5 m), Steighöhe 0,35 m:**
- Q ≈ 100 × (1 − 0,35/0,5) = **30 L/h ≈ 0,5 L/min**
- 0,5 L → **~60 s** — machbar, aber ohne Reserve; bei 0,4 m nur noch 20 L/h → 90 s+

**Peristaltikpumpe (100 ml/min):** 0,5 L → **5 min** Dauerlauf.

**Kalibrieren statt glauben:** Beim Aufbau einmal 30 s in einen Messbecher pumpen und nachmessen — Mini-Pumpen streuen in der Realität ±30 %.

### Timing-Empfehlung für die Firmware

| Phase | Dauer |
|---|---|
| Pumpen (12V-Pumpe) | 10–20 s |
| Pause (Wasser verteilt sich) | 2–3 min |
| Sensor-Check / ggf. 2. Runde | max. 3 Runden |
| Feuchte trotz 3 Runden unverändert | → Meldung „Tank leer" |
| Mindestabstand zwischen Gieß-Events | 6–12 h (Nachtruhe: Cannabis nachts weniger Wasser) |

---

## 6. Einkaufsliste (verifizierte Preise)

| # | Artikel | Menge/Preis | Link |
|---|---|---|---|
| 1 | 12V-Tauchpumpe 240 L/h, 3 m Förderhöhe (2er-Pack) | **10,99 €** | https://www.amazon.de/dp/B0CDK7GQF2 |
| 2 | Dual-MOSFET-Trigger-Modul DC 5–36V (8er-Pack) | **6,49 €** | https://www.amazon.de/dp/B0DG8B58PM |
| 3 | 12V/1A-Steckernetzteil | ~8 € (beliebig) | – |
| 4 | (Alternativ Pumpe) Flintronic USB 200 L/h, 3,5–9V | 8,49 € | https://www.amazon.de/dp/B07TW39QXP |
| 5 | (Alternativ Schalter) IRLZ44N 10er-Pack + 1N5819-Dioden | 6,99 € | https://www.amazon.de/dp/B0H4ZQBY7W |
| 6 | (Alternativ Schalter) 5V-Relais-Modul 1-Kanal (4er-Pack) | 8,99 € | https://www.amazon.de/dp/B0GCYPQQKR |
| 7 | (Optional Nährstoff-Dosierung) Kamoer NKP Peristaltikpumpe 12V | **12,40 €** | https://www.amazon.de/dp/B0DYTYPHX5 |
| 8 | (Bastel-Prototyp) 3er-Pack 3–5V-Mini-Pumpe + 3 m Schlauch | 8,99 € | https://www.amazon.de/dp/B08BZBN29C |

**Gesamtkosten Kernsystem (Pumpe + Schalter + Netzteil): ~26 €**

---

## 7. Quellen

- Amazon.de-Produktdaten (Live-Scrape über Chrome/CDP am 10.09.2026): alle ASINs wie oben verlinkt
- Neuhold Elektronik, Datenblatt „Tauchpumpe 3–5V liegend" N4244 (2,95 €, max. 200 mA, 100 L/h, Förderhöhe max. 0,5 m): https://www.neuhold-elektronik.at/pumpen/tauchpumpe-3-5v-liegend
- Cannapot Canna-Wiki „Watering Cannabis Correctly" (akt. 02/2026): 10–20 % des Topfvolumens bei Erde (5L-Topf ≈ 0,5–1,0 L), „langsam in Etappen", Warnung vor dauerhaft nassen Füßen bei Bottom-Watering: https://www.cannapot.com/shop/cannabis-seeds/canna-wiki/watering-cannabis-correctly-a-guide
- Selbstbewässerungs-/Wicking-Bed-Fachartikel (Kapillarwirkung, Reservoir-Prinzip): shuncy.com, harvestsavvy.com, lushygardens.com (via DDG-Suche verifiziert)
