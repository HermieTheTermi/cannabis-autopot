# BOM-Entscheidung V1 — Smart Grow Topf

Stand: 11.09.2026 · Preise am 11.09.2026 direkt auf der Produktseite geprüft (Spalte „Prüfung")
Grundlage: `../research/bom-check/01…04` · Geometrie: `../docs/02_architektur-und-geometrie.md`

---

## 1. Entscheidung (final)

| # | Bauteil | Wahl | Preis | Bezug / Link | Prüfung |
|---|---|---|---|---|---|
| 1 | **MCU** | **ESP32-C6-MINI-1** (nacktes Modul auf eigener PCB) | **≈ 3,60 €** (3,8871 $) | JLCPCB `C5736265` | ✅ API + Espressif-Datasheet |
| 1b | MCU-Alternative | ESP32-C6-MINI-1**U** (IPEX, externe Antenne) | ≈ 3,99 € (4,3051 $) | JLCPCB `C20627095` | ✅ API (1.352 lagernd) |
| 1c | **1S-Lader** | **MCP73831T-2ACI/OT**, 4,20 V | ≈ 0,76 € (0,8181 $) | JLCPCB `C424093` | ✅ MPN + Datenblatt (4,20-V-Variante geprüft) |
| 1d | **3,3-V-LDO** | **ME6211C33M5G**, 500 mA, 40 µA | ≈ 0,06 € | JLCPCB `C82942` | ✅ Datenblatt (500 mA / 100 mV @100 mA / 40 µA) |
| 1e | **USB-C + Schutz** | Buchse 16-pol `C165948` + USBLC6-2SC6 `C7519` + 2 × 5,1 kΩ `C27834` | ≈ 0,40 € | JLCPCB | ✅ API |
| 1f | **Unterspannungswächter** | **MAX809TEUR+T**, Schwelle 3,08 V | ≈ 0,52 € (0,5628 $) | JLCPCB `C16711` | ✅ Datenblatt VTH 3,04/3,08/3,11 V |
| 2 | **Pumpe** | **OEM-Peristaltik ABC-12527**, 3,7–6 V, Ø32 × 44 mm | **7,74 €** | anodas.lt (EU/Litauen, lagernd) — https://anodas.lt/en/peristaltic-liquid-pump-with-silicone-tubing-3-7-6vdc | ✅ selbst (Spec-Block + Preis auf der Seite) |
| 3 | **Sensor** | Kapazitiv **v1.2**, analog | **4,99 €** | AZ-Delivery — https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2 | ✅ selbst (JSON-LD 4.99, V1.2 kapazitiv) |
| 4 | **Akku** | **EFASO 503759** 3,7 V ~1500 mAh, **PCM**, JST PH2.0 | **14,90 €** | efaso.de (Kassel) — https://efaso.de/produkt/503759-3-7v-1500-mah-pcm-jst-ph2-0-2p/ | ✅ selbst (14,90 €, PCM + JST bestätigt) |
| 5 | **MOSFET** | **AO3400A** (SOT-23), 10 St | **1,67 €** | Reichelt, ab Lager — https://www.reichelt.de/de/de/shop/produkt/mosfet_n-ch_30v_5_7a_0_018r_sot-23-166490 | ✅ selbst (0,167 €/St ab 10) |
| 6 | **Freilaufdiode** | 1N5819 (DO-41), 10 St | ~1,00 € | Reichelt | ⚠️ Subagent, nicht selbst geprüft |
| 7 | **Sensor-Stecker** | JST-XH 2,54 3-pol Buchse, 10 St | 3,00 € | Funduinoshop | ⚠️ Subagent |
| 8 | **Schlauch** | Silikon 3 × 5 mm, ~1 m (**neu: nicht mehr im Lieferumfang**) | ~3–5 € | offen | ❌ Preis/Link offen |
| | **Zwischensumme** | | **≈ 42,85 €** | | |
| 9 | Widerstände 220 Ω/10 kΩ, Kondensatoren 100 nF/10 µF/100 µF, Taster, Stiftleisten | ~5 € | überwiegend LCSC (PCBA) oder Reichelt | ❌ Preise DE nicht belegt |
| 10 | Ansaugfilter/-gewicht | optional | Badshop/Aquaristik, Preis offen | ❌ |
| | **Gesamt (realistisch)** | | **≈ 43–48 €** | | |

**Was die Pumpenwahl geändert hat:** Die frühere Adafruit 3910 (24,50 €) ist entfallen, weil die
OEM-Pumpe im Datenblatt **3,7–6 V** abdeckt — und in der Praxis besser fördert (siehe §2/§3).
Ersparnis 16,76 € bei besserer Energiebilanz. Der Schlauch ist jetzt **kostenpflichtig**, weil die
OEM-Pumpe nur ca. 5 cm Schlauch mitbringt (die Adafruit brachte 530 mm mit).

---

## 2. Warum diese Pumpe — die Kennzahl ist Wh pro Liter

Für ein Akkugerät entscheidet nicht der Preis allein, sondern die Energie pro gefördertem Liter.
Alle Werte aus Produktseiten/Datenblättern, Umrechnung in Wh/L aus Leistung und Förderrate:

| Pumpe | Preis | Leistung | Förderrate | **Wh/L** | Quelle |
|---|---|---|---|---|---|
| **OEM ABC-12527** @3,7 V | **7,74 €** | 1,67 W | ~154 ml/min* | **0,18** | anodas.lt (Spannung + Strom dokumentiert) |
| OEM ABC-12527 @6 V | 7,74 € | 3,24 W | ~250 ml/min* | 0,22 | anodas.lt |
| Adafruit 3910 @5 V | 24,50 € | 2,50 W | 100 ml/min | 0,42 | adafruit.com/product/3910 |
| Whadda WPM447 @6 V | 12,90 € | 5,00 W | 39 ml/min | 2,14 | whadda.com + electrokit.se |

\* Förderrate der OEM-Pumpe skaliert nicht linear mit der Spannung — die Linearskalierung ist meine
Annahme, die Seite nennt nur „1L – 4 min" ohne Spannungsbezug. **Vor dem Einbau messen.**

Nicht gewählt: **Funduino „0-90 ml/min, 3-12 V"** (7,92 €) — im Titel 3–12 V, in den Produktdetails aber „Betriebsspannung 12 V DC" und **keine Stromangabe**, damit ist die Akku-Auslegung nicht belegbar. **Adafruit 3910**: dreifacher Preis bei halber Förderrate. **Whadda WPM447**: fünffache Energie pro Liter.

Verifizierter Spec-Block der OEM-Pumpe (Wortlaut der Produktseite):
> „Rated voltage: 3.7V to 6V · Current: 3V – 400mA, 6V – 540mA · Engine: DC with pinion ·
> Number of satellites: 3 · Productivity: 1L – 4 min · Dimensions: Diameter: 32 mm. Height: 44 mm ·
> Mounting holes diameter: 2.5 mm · Mounting hole layout 44mm · Silicone tube: inner 3 mm / outer 5 mm"

**Einschränkung:** kein deutscher Shop — EU-Versand aus Litauen (Vilnius/Kaunas lagernd), Versand
nach DE laut Seite „auf Anfrage". Das ist der Preis für 17 € Ersparnis; Lieferzeit und Versandkosten
vor der Bestellung klären.

---

## 3. Betriebsspannung — der frühere offene Punkt ist geschlossen

**Entscheidung: 1S-Akku (3,7 V) direkt an der Pumpe, kein Boost, kein Buck.**

Der Grund ist der Wechsel der Pumpe. Die frühere Planung stand auf der Prämisse, dass die Pumpe
5–6 V braucht (Adafruit 3910, Herstellerangabe „Motor voltage: 5 to 6 VDC") und der Direktbetrieb an
einer 1S-Zelle damit undokumentiert war — zusätzlich liefert der XIAO im Akkubetrieb **keine 5 V**
(Seeed-Wiki, wörtlich: „When using battery power, no voltage will be present on the 5V pin"), es
hätte also zwingend einen Wandler gebraucht.

Diese Prämisse ist mit der OEM-Pumpe weg: sie ist **ab 3 V dokumentiert** (3 V – 400 mA) und für
**3,7–6 V** ausgelegt. Eine 1S-Zelle liefert 3,0–4,2 V — die Pumpe läuft damit **innerhalb** ihres
Datenblattbereichs, über den ganzen Entladezyklus.

**Das 2S-Konzept (2 Zellen + Step-Down) wurde geprüft und verworfen:**
- **Wirkungsgrad bringt nichts:** Buck aus 2S (η 0,90) gegen Boost aus 1S (η 0,88) — Laufzeit
  praktisch identisch (32 vs. 31 Tage gerechnet). Und mit der neuen Pumpe entfällt die Wandlung
  komplett, das ist besser als jede Wandlung.
- **Kosten:** 2S braucht einen **eigenen Lader plus Balancer**, weil der Onboard-Lader des XIAO für
  eine Zelle (3,7 V / 4,2 V Ladeschluss) ausgelegt ist. Das sind zusätzliche Bauteile und
  Platinenfläche — bei einem Konzept, dessen Ziel „günstig" ist, der falsche Hebel.
- **Kapazität wird nicht gebraucht:** siehe §4 — die 1S-Zelle reicht für ~85 Dosiervorgänge.
- **Sicherheit:** Reihenschaltung ohne sauberes Balancing ist in einem feuchten Gehäuse ein
  echtes Risiko, nicht nur ein Schönheitsfehler.

Wenn 2S später doch gewünscht wird (z. B. für mehr Reserven), ist der Weg dokumentiert: 2S-Lader
mit Balancer + Buck auf 5 V, und der Onboard-Lader des XIAO wird nicht mehr genutzt.

---

## 4. Akku und Laufzeit

- **EFASO 503759**: ~**59 × 37 × 5 mm** (Typcode; Maße am Listing **nicht** bestätigt → vor Bestellung
  Specblock prüfen), mit **PCM** (Über-/Tiefentladung, Kurzschluss) und **JST PH2.0-2P**.
- **Laden:** eigener **MCP73831T-2** auf der Platine, USB-C-Buchse direkt daneben. Die **-2-Variante**
  ist die 4,20-V-Ausführung (aus dem Datenblatt geprüft); die Familie hat auch 4,35/4,40/4,50 V,
  die unsere Zelle zerstören würden. Ladestrom über einen Widerstand programmierbar (15–500 mA),
  sinnvoll ~250 mA für die 1500-mAh-Zelle. Lade-LED am Tri-State-Statusausgang.
  Der XIAO ist nicht mehr im Design — sein Onboard-Lader (SGM40567-4.2) wäre bei JLC ohnehin nicht beschaffbar. (Beim späteren Aufbau mit nacktem ESP32-Modul muss ein eigener 1S-Lader
  vorgesehen werden, z. B. MCP73831.)
- **Laufzeit neu gerechnet** (Pumpe @3,7 V: 1,67 W, ~154 ml/min): ein Dosiervorgang von 300 ml
  braucht ~1,9 min und **0,052 Wh**. Aus 1500 mAh @ 3,7 V (5,55 Wh brutto, ~4,44 Wh nutzbar) →
  **≈ 85 Dosiervorgänge pro Ladung**, bei 1× täglich also rund **3 Monate**. Die alte „4 Wochen\"-Angabe
  galt für die Adafruit-Pumpe mit 2,5 W bei 100 ml/min — die neue Pumpe ist der Grund für den Sprung.
- **Warum keine 18650:** geschützte 18650 ist Ø18,85 × 69 mm und passt in die Wulst (40 mm tief),
  bringt aber ~3× Kapazität, die bei 85 Dosen pro Ladung niemand braucht. Option für später.

---

## 4b. Unterspannungsschutz — die Zelle nicht töten

Der Lader schützt **nicht** vor Tiefentladung. Belegt aus dem MCP73831-Datenblatt: der Chip hat
„Reverse Discharge Protection" (verhindert nur Rückstrom in den Lader) und eine UVLO von
**3,45 V Start / 3,38 V Stop** — die regelt aber nur, wann das *Laden* beginnt. Entladeschutz ist
nicht Teil des Chips. Deshalb vier Ebenen, von harmlos bis Notabschaltung:

| Ebene | Schwelle | Wirkt | Bauteil |
|---|---|---|---|
| 1 · Firmware | ~3,5 V Warnung, ~3,4 V Pumpstopp | normaler Betrieb, Telegram-Meldung | 200-k-Teiler + ADC (§6.3b) |
| 2 · Hardware | **3,08 V** (Datenblatt VTH 3,04/3,08/3,11 V) | sperrt die Pumpe **unabhängig von der Firmware** | **MAX809TEUR+T** `C16711` + Schottky |
| 3 · MCU tot | – | Gate-Pulldown 10 kΩ: hängender/gebrannter MCU = Pumpe AUS | R2 |
| 4 · Zelle | ~2,5 V (**nicht dokumentiert**) | letzte Notabschaltung | PCM in der EFASO-Zelle |

**Verschaltung von Ebene 2:** der RESET-Ausgang des MAX809 (aktiv low, push-pull, 12 µA) liegt über
eine Schottky-Diode am Gate-Knoten des Pumpen-MOSFET (Anode am Gate, Kathode an RESET). Fällt VBAT
unter 3,08 V, zieht RESET low und klemmt das Gate auf ~0,3 V — unter der Schwellenspannung des
AO3400A (0,65–1,45 V) → Pumpe aus, egal was die Firmware tut. Über 3,08 V liegt RESET auf VBAT,
die Diode sperrt, und der GPIO steuert normal.

→ kostet **ein zusätzliches Bauteil** (MAX809, 0,56 $, 13.783 lagernd) plus eine Diode, die wir
ohnehin im BOM haben. Den Gate-Widerstand R1 dafür von 220 Ω auf **1 kΩ** erhöhen: im Fehlerfall
(MCU will pumpen, Hardware sperrt) fließen dann 3 mA statt 14 mA durch den Klemmzweig; bei
Qg 6 nC bleibt das Schalten mit 20 kHz PWM unkritisch.

**Nicht doppelt bauen:** ein eigenes DW01A + FS8205A Schutzpaar ist bei JLC für 0,09 $ zu haben,
schaltet aber erst bei ~2,5 V ab — unterhalb unserer Hardware-Schwelle. Es dupliziert nur den
PCM der Zelle.

---

## 5. Wulst-Maße (aus den finalen Bauteilen abgeleitet)

| Innenmaß | Wert | Bestimmt durch |
|---|---|---|
| Breite | **60 mm** | Pumpe Ø32 + Wandungen, PCB ~52 mm, Zelle 37 mm |
| Tiefe (radial) | **40 mm** | Pumpe Ø32 + 2 × 2,5 mm Wand + Montagefreiheit |
| Höhe | **160 mm** (y = 90–250) | Pumpe 44 mm (+ Halterung), darüber Platine + Zelle |
| Gesamtbreite Topf an der Wulst | **≈ 180 mm** | 140 mm + 40 mm |

Einbau von unten nach oben: **Pumpe** (44 mm Bauhöhe, dadurch deutlich mehr Luft als vorher mit
66,8 mm) → **Platine** → **Zelle** hinter/über der Platine.

**Parameter nachzuziehen (OpenSCAD, `case/params.scad`):**
`pump_d` 27.8 → **32** · `pump_l` 66.8 → **44** · `pump_mount_cc` 50 → **44** · `pump_mount_d` 3.7 → **2.5**.
Die Wulst selbst (60 × 40 × 160) bleibt gültig.

---

## 6. Konsequenzen für die PCB

1. **ESP32-C6-MINI-1** direkt auf der Platine (13,2 × 16,6 mm, `C5736265`), **Antenne am
   Platinenrand** (Punkt 6). Pflichtbeschaltung laut Espressif: **EN über RC-Glied 10 kΩ + 1 µF**,
   EN nie floaten lassen, Leitung kurz halten; **GPIO9 mit Pull-up** (Boot), **keine großen
   Kondensatoren an GPIO9** (sonst Download-Modus); am 3V3-Netz **22 µF Bulk + 2 × 0,1 µF**; am
   Stromeingang **≥ 10 µF + ESD-Diode** (Espressif Hardware Design Guidelines).
2. **Versorgung:** LDO **ME6211C33** (500 mA) — Pflicht, weil der ESP32-C6 im WLAN-TX **382 mA Peak**
   zieht (Espressif-Datasheet Tab. 6-4, selbst nachgeprüft) und Espressif ≥ 500 mA Ausgangsstrom
   verlangt. 200–250-mA-Regler (XC6206, HT7333, MCP1700) brownen bei TX aus; ein Pufferkondensator
   deckt nur sehr kurze Bursts.
2b. **Zelle + Laden:** **JST PH2.0-Buchse** + **MCP73831T-2** (4,20 V) + USB-C-Buchse mit
   2 × 5,1 kΩ (CC, USB-C-Pflicht) und USBLC6-2SC6 (ESD). USB-Daten gehen **nativ** auf
   **GPIO12 = D−** und **GPIO13 = D+** (Espressif) — kein USB-UART-Brückenchip nötig; optional
   22/33-Ω-Serienwiderstände vorsehen.
3. Pumpe: AO3400A Low-Side, Gate 220 Ω, Pulldown 10 kΩ, 1N5819 antiparallel, **100 µF Pufferelko**.
   Pumpe hängt **direkt an VBAT** — kein Wandler, kein Boost-Layout.
3b. **Zellspannung überwachen:** 200-k-Widerstand in 1:2-Beschaltung auf einen **ADC1**-Pin, plus
   **0,1 µF Filterkondensator** am ADC-Pin (Espressif-Empfehlung für ADC-Genauigkeit). Grundlage für
   Pumpstopp und Warnung in §4b. Der ADC des ESP32-C6 ist verrauscht → im Code vielfach mitteln und
   die Schwelle erst **im Ruhezustand** auswerten (während des Pumpens sackt die Spannung ab).
4. Sensor: 3-poliger JST-XH, **VCC über GPIO schaltbar** (nur während der Messung), AOUT auf ADC1.
5. Taster Reset/Boot, Status-LED sichtbar durch das LED-Fenster.
6. **Antenne — der Punkt, der die Mechanik betrifft.** Espressif wörtlich: „Ensure that the PCB
   antenna on the base board also has a sufficiently large clearance area inside the housing.
   A clearance of at least **15 mm** is recommended in all directions." Dazu: Antenne möglichst über
   den Platinenrand hinaus, sonst die Platine **beidseitig und unter der Antenne freischneiden**
   (nicht in der Mitte der Platine „freihöhlen"), Kupfer + dichte GND-Vias in Antennennähe, USB- und
   UART-Leitungen weit weg von der Antenne.
   → Für uns heißt das: **obere ~25 mm der Kammer bausteilfrei**, Modul mit der Antenne nach oben,
   und die **Wulstwand über der Antenne dünner** (6 mm → ~2 mm). Das ist eine Geometrie-Änderung in
   `case/params.scad`. Espressif schreibt außerdem vor, das **Endprodukt zu testen** (Durchsatz +
   Reichweite); fällt der Test schlecht aus, ist die Alternative das Modul **-1U** (`C20627095`) mit
   IPEX-Buchse und externer Antenne.
6b. **Espressif empfiehlt bei Akkubetrieb ausdrücklich einen Power-Monitor-Chip mit ~3,0-V-Schwelle** —
   genau das ist unser MAX809TEUR+T (3,08 V, §4b). Zwei unabhängige Quellen treffen sich hier.
7. **Kein XIAO mehr:** Lader, LDO und USB sind komplett durch eigene Bauteile ersetzt, die geplante
   V1/V2-Unterscheidung entfällt — es gibt **eine** Platine.

---

## 7. Noch offen / bewusst nicht behauptet

- **Förderrate der OEM-Pumpe bei 3,7 V** nicht dokumentiert (Seite nennt nur „1L – 4 min" ohne
  Spannung) → nach dem Aufbau 60 s in den Messbecher pumpen und auf ml/min umrechnen.
- **Versandkosten/Lieferzeit** der OEM-Pumpe nach DE (anodas.lt: „negotiated individually").
- **Schlauch** muss beschafft werden (3 × 5 mm Silikon, ~1 m) — Position 8.
- **Elektrodenlänge des Sensor v1.2** nicht belegt → am realen Board messen (Messebene liegt 75 mm tief).
- **LDO-Bestückung** des AZ-Boards nur im Foto prüfbar (nicht im Text).
- **Maße der EFASO-Zelle** am Listing nicht bestätigt.
- **Abschaltspannung des EFASO-PCM** nicht dokumentiert → beim Hersteller erfragen oder am Prototyp messen (Ebene 4 in §4b).
- **RF-Endtest** am fertigen Gehäuse (Espressif-Vorgabe) — ohne Test ist die Antennenperformance unbelegt.
- **Ruhestrom des ME6211** (40 µA) kostet ~29 mAh/Monat; Alternative TPS7A02 (25 nA) fällt weg, weil er
  nur 200 mA kann und der TX-Peak 382 mA ist.
- Versandkosten der übrigen Shops nicht geprüft (AZ-Delivery versandkostenfrei ab 25 €).
- Amazon-Preise von Agenten im Browser gesehen, nicht selbst nachprüfbar (Amazon blockt Skript-Abrufe).
