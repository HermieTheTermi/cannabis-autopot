# BOM-Entscheidung V1 — Smart Grow Topf

Stand: 11.09.2026, nachrecherchiert 12.09.2026 · Preise direkt auf der Produktseite geprüft (Spalte „Prüfung“)
Grundlage: `../research/bom-check/01…04` · **Nachrecherche 12.09.2026: `../research/bom-check/09_eu-quellen-konsolidiert.md`** (Pumpe/Sensor/Schlauch, EU-Quellen) · Geometrie: `../docs/02_architektur-und-geometrie.md`

---

## 1. Entscheidung (final)

| # | Bauteil | Wahl | Preis | Bezug / Link | Prüfung |
|---|---|---|---|---|---|
| 1 | **MCU** | **ESP32-C6-MINI-1** (nacktes Modul auf eigener PCB) | **≈ 3,60 €** (3,8871 $) | JLCPCB `C5736265` | ✅ API + Espressif-Datasheet |
| 1b | MCU-Alternative | ESP32-C6-MINI-1**U** (IPEX, externe Antenne) | ≈ 3,99 € (4,3051 $) | JLCPCB `C20627095` | ✅ API (1.352 lagernd) |
| 1c | **2S-Lader** ⭐ | **IP2326**, 2S-Boost-Lader aus 5 V USB, 8,4 V / 0,90 A | ≈ 0,62 $ | JLCPCB `C2832094` | ✅ API (18.074 lagernd) + Datenblatt V1.11 (VSET offen = 8,4 V; ICHG = 90000/R_ISET; kein Power-Path). ⚠️ Variante **IP2326_8V8 = 8,8 V** nicht verwenden |
| 1d | **3,3-V-Buck** ⭐ | **AP63203WU-7**, 2 A, 3,8–32 V, **Iq 22 µA** (ersetzt den LDO) | ≈ 1,18 $ | JLCPCB `C780769` | ✅ API (25.645) + Datenblatt DS41326. Der ME6211 entfällt: V_IN,max 6,0 V und 0,26 W Verlust bei 8,4 V → 3,3 V |
| 1e | **USB-C + Schutz** | Buchse 16-pol `C165948` + USBLC6-2SC6 `C7519` + 2 × 5,1 kΩ `C27834` | ≈ 0,40 € | JLCPCB | ✅ API |
| 1f | **Unterspannungswächter (2S)** ⭐ | **TPS3839G33DBZR**, 3,08 V, **Iq 150 nA**, Push-Pull | ≈ 0,45 $ | JLCPCB `C485802` | ✅ API (3.502) + Datenblatt (V_IT 3,003–3,126 V, Hysterese 31 mV). Am 1:2-Teiler ⇒ **6,16 V Pack**. Der MAX809 scheidet aus: V_DD,max 5,5 V |
| 2 | **Pumpe** | **CONQUERALL DC-5-V-Mikro-Peristaltikpumpe** (Amazon `B0DHVMZ27Y`) — Nennspannung **DC 5 V**, Leerlaufstrom 0,4 A, **Anlaufstrom 3 A (bei 5 V)**, Fördermenge **≤ 150 ml/min**, Silikonschlauch **3 × 5 mm**, Bauhöhe **42 mm**, Ansaugbereich 0,5 m, umpolbar | **11,99 €** (2er-Pack `B0DJ78W43W` **16,61 €**) | https://www.amazon.de/dp/B0DHVMZ27Y (Verkäufer EASFFY, auf Lager, 4,2★/11) | ✅ Preis + Specs 14.09.2026 (Amazon) · ⚠️ **Ø nicht dokumentiert** → vor Einbau messen (Wulst ist auf Ø 32 gerechnet) · ⚠️ Betrieb an 1S (3,0–4,2 V) liegt **unter** der Nennspannung → Förderrate + Anlauf **messen** · ⚠️ **Anlaufstrom** → siehe §4c: PWM-Softstart ist Pflicht |
| 2b | ~~OEM-Peristaltik ABC-12527~~ | **abgelöst (14.09.2026)** — war fachlich passend (3,7–6 V, ab 3 V dokumentiert, Ø32 × 44 mm, ~250 ml/min), aber **31,94 €** inkl. 24,20 € Versand aus Litauen (anodas.lt) | – | anodas.lt | Historie: `../research/bom-check/06_pumpe-eu-quellen.md` |
| 3 | **Sensor** | Kapazitiv **v1.2**, analog — **AZ-Delivery ausverkauft (12.09.)**, Ersatz: **ARCELI 6er-Pack V1.2 kapazitiv** (1,25 €/St.) | **7,49 €** (6 St.) | Amazon `B0FPRBY7LW` · AZ (falls wieder lieferbar) https://www.az-delivery.de/products/bodenfeuchte-sensor-modul-v1-2 | ✅ selbst 12.09. (7,49 €, ab Lager, Gratislieferung 16.09.) · ⚠️ Elektrodenlänge bleibt unbelegt |
| 4 | **Akku (2S)** ⭐ | **2S-Pack 7,4 V, 1500–2500 mAh, mit BMS/PCM *und Balancierung*, 2-poliger Ausgang (JST-PH 2,0 bevorzugt)** | offen | Quellenrecherche liegt vor (Stand 16.09.2026), Entscheidung offen | ⚠️ **Pflicht: Balancing** — ohne Balancer kann eine Zelle über 4,25 V kommen (der Lader lädt nur die Reihenschaltung auf 8,4 V). Betrieb 6,0–8,4 V, Wächter-Abschaltung bei 6,16 V |
| 5 | **MOSFET** | **AO3400A** (SOT-23), 10 St | **1,67 €** | Reichelt, ab Lager — https://www.reichelt.de/de/de/shop/produkt/mosfet_n-ch_30v_5_7a_0_018r_sot-23-166490 | ✅ selbst (0,167 €/St ab 10) |
| 6 | **Freilaufdiode** | 1N5819 (DO-41), 10 St | ~1,00 € | Reichelt | ⚠️ Subagent, nicht selbst geprüft |
| 7 | **Sensor-Stecker** | JST-XH 2,54 3-pol Buchse, 10 St | 3,00 € | Funduinoshop | ⚠️ Subagent |
| 8 | **Schlauch** | Silikon **3 mm ID × 5 mm OD, lebensmittelecht, 3 m** | **6,99 €** | Amazon `B0CMQJDJ2H` (Gratislieferung 16.09.) | ✅ selbst 12.09. |
| | **Zwischensumme** (Position 1–7) | | **≈ 38.64 €** | | |
| 9 | **Passive** (Werte jetzt aus dem Schaltplan): R 1 kΩ/3,9 kΩ/4,7 kΩ/10 kΩ/47 kΩ/200 kΩ/5,1 kΩ · C 100 nF/1 µF/4,7 µF/10 µF/22 µF/100 µF · 2 Taster | ~5 € | JLCPCB (PCBA, Basic-Teile) | ✅ LCSC-Codes in `pcba_bom_jlc.csv`; ⚠️ Hinweis: „220 Ω" und „Stiftleisten" aus der alten Zeile sind **entfallen** (Gate-Widerstand jetzt 4,7 kΩ, kein XIAO-Sockel mehr) |
| 10 | Ansaugfilter/-gewicht | optional | Badshop/Aquaristik, Preis offen | ❌ |
| | **Gesamt (realistisch)** | | **≈ 47–49 €** | inkl. Schlauch (3–5 €) und Passiven (~5 €) | |
| | **+ JLCPCB-Kosten (nicht in dieser BOM)** | | **≈ 28 € Handling** | 10 Extended-Positionen à 3 $ + Platinenfertigung (noch kein Angebot eingeholt) | |

**Was die Pumpenwahl geändert hat (14.09.2026):** Die Pumpe ist jetzt die **CONQUERALL DC 5 V**
(11,99 €, Amazon, sofort lieferbar) — statt 31,94 € für die OEM-Pumpe aus Litauen. Das spart
**19,95 €**, verschiebt aber ein Risiko: die OEM war **ab 3 V dokumentiert**, die CONQUERALL ist mit
**5 V Nennspannung** spezifiziert und läuft an der 1S-Zelle (3,0–4,2 V) *unterhalb* ihrer Nennspannung.
Förderrate bei 3,7 V und Anlaufverhalten sind damit **nicht belegt → messen** (§7). Der Anlaufstrom
(3 A bei 5 V) ist der zweite neue Punkt und in §4c gegen die Schaltung geprüft.

---

## 2. Warum diese Pumpe — die Kennzahl ist Wh pro Liter

Für ein Akkugerät entscheidet nicht der Preis allein, sondern die Energie pro gefördertem Liter.
Alle Werte aus Produktseiten/Datenblättern, Umrechnung in Wh/L aus Leistung und Förderrate:

| Pumpe | Preis | Leistung | Förderrate | **Wh/L** | Quelle |
|---|---|---|---|---|---|
| **CONQUERALL DC 5 V** @5 V (Nenn) | **11,99 €** | 2,0 W (5 V × 0,4 A) | ≤ 150 ml/min | **0,22** | Amazon `B0DHVMZ27Y` (Datenblattangaben des Händlers) |
| CONQUERALL DC 5 V @3,7 V (1S-Betrieb) | 11,99 € | ~1,5 W* | ~111 ml/min* | **0,22** | *lineare Skalierung — **Annahme, nicht belegt** |
| ~~OEM ABC-12527~~ @3,7 V (abgelöst) | 7,74 € + 24,20 € Versand | 1,67 W | ~154 ml/min* | 0,18 | anodas.lt (Spannung + Strom dokumentiert) |
| Adafruit 3910 @5 V | 24,50 € | 2,50 W | 100 ml/min | 0,42 | adafruit.com/product/3910 |
| Whadda WPM447 @6 V | 12,90 € | 5,00 W | 39 ml/min | 2,14 | whadda.com + electrokit.se |

\* Die Förderrate der CONQUERALL ist nur als **Obergrenze bei Nennspannung** angegeben und die
Spannungsskalierung ist meine Annahme → **vor dem Einbau messen** (§7). Bei 3,7 V ergibt sich damit
eine Laufzeit von ~2,7 min für 300 ml.

**Was an der CONQUERALL gemessen wurde (14.09.2026, Amazon-Produktdaten):**
> „Nennspannung: DC 5V · Leerlaufstrom: 0,4 A · Ansaugbereich: 0,5 m · Anlaufstrom: 3 A ·
> Fördermenge: ≤150 ml/min · Pumpe Gesamthöhe: 42 mm · Schlauchdurchmesser: 3 × 5 mm"

**Warum diese und nicht die anderen Amazon-Typen:** Die billigen „6-V-Mini-Peristaltikpumpen"
(5,99–6,69 €, z. B. `B0HC8WF98P`, `B0H7R9XYJ5`) schreiben im Produkttext ausdrücklich
**„Spannungen unter 6 V betreiben den Motor nicht"** → an der 1S-Zelle unbrauchbar. Die
12-V-Klasse (G528/G928/Kamoer NKP) bräuchte einen Boost, den die Platine bewusst nicht hat.
Schrittmotor-Mikropumpen (3–5 V) fördern nur 0,5 ml/min, die G10-Klasse 1 ml/min → beide
viel zu langsam. „Peristaltikpumpe 3,7/6/12 V … Membran Luftpumpe" sind **keine** Peristaltikpumpen
(Titel-Fehler der Händler) → kommen für „Medium berührt die Mechanik nicht" nicht infrage.

Verifizierter Spec-Block der OEM-Pumpe (Wortlaut der Produktseite):
> „Rated voltage: 3.7V to 6V · Current: 3V – 400mA, 6V – 540mA · Engine: DC with pinion ·
> Number of satellites: 3 · Productivity: 1L – 4 min · Dimensions: Diameter: 32 mm. Height: 44 mm ·
> Mounting holes diameter: 2.5 mm · Mounting hole layout 44mm · Silicone tube: inner 3 mm / outer 5 mm"

**Einschränkung:** kein deutscher Shop — EU-Versand aus Litauen (Vilnius/Kaunas lagernd), Versand
nach DE laut Seite „auf Anfrage". Das ist der Preis für 17 € Ersparnis; Lieferzeit und Versandkosten
vor der Bestellung klären.

---

## 3. Betriebsspannung — ~~der frühere offene Punkt ist geschlossen~~ **revidiert am 15.09.2026**

> **⚠️ NEU (15.09.2026): Es gibt jetzt einen Boost.** Auf Wunsch des Nutzers sollen **beide** Pumpen
> (Dosier- **und** Sauerstoffpumpe) **5 V** bekommen. Damit ist der Direktbetrieb an der 1S-Zelle
> gestrichen: **U8 MT3608** erzeugt eine geregelte **+5-V-Schiene (5,10 V)** aus VBAT, und **beide**
> Pumpen hängen über je einen AO3400A (Q1/Q3) daran. Auslegung, Rechnungen und die zwei harten
> Konsequenzen (**PWM-Softstart Pflicht**, **O2-Pumpe nicht im Dauerbetrieb**) stehen in
> `hardware/schaltplan_v1.md` **§10**. Die Absätze unten bleiben als Begründung stehen, warum es
> vorher keinen Wandler gab.

**Entscheidung bis 14.09.2026: 1S-Akku (3,7 V) direkt an der Pumpe, kein Boost, kein Buck.**

Der Grund ist der Pumpentyp. Die frühere Planung stand auf der Prämisse, dass die Pumpe
5–6 V braucht (Adafruit 3910, Herstellerangabe „Motor voltage: 5 to 6 VDC") und der Direktbetrieb an
einer 1S-Zelle damit undokumentiert war — zusätzlich liefert der XIAO im Akkubetrieb **keine 5 V**
(Seeed-Wiki, wörtlich: „When using battery power, no voltage will be present on the 5V pin"),
es hätte also zwingend einen Wandler gebraucht.

**Der damalige Fix war die OEM-Pumpe (ab 3 V dokumentiert). Mit der CONQUERALL ist diese Sicherheit
wieder weg** — sie ist mit **Nennspannung DC 5 V** spezifiziert (Leerlaufstrom 0,4 A), die 1S-Zelle
liefert 3,0–4,2 V. Die Pumpe läuft damit **unterhalb ihrer Nennspannung**, und daraus folgt:

- **Förderrate:** linear geschätzt ~111 ml/min bei 3,7 V statt 150 ml/min → für 300 ml noch
  2,7 min, für die größte Dosis (350 ml) unter 4 min (§4). **Annahme, nicht belegt → messen.**
- **Anlauf:** bei Unterspannung ist das Losbrechmoment nicht garantiert. Der Anlaufstrom *sinkt*
  mit der Spannung (2,5 A bei 4,2 V … 1,8 A bei 3,0 V) — das entlastet Zelle und PCM, sagt aber
  nichts darüber, ob der Motor dreht. **Messen: 3,0 / 3,7 / 4,2 V, je 30 s in den Messbecher (§7).**
- **Boost bleibt verworfen:** ein Step-Up auf 5 V kostet Wirkungsgrad und Platinenfläche. Er ist die
  **Rückfallebene**, falls die Messung zeigt, dass die Pumpe an der Zelle nicht sicher anläuft —
  nicht die Voreinstellung.

**Zum Vergleich — warum es mit der abgelösten OEM-Pumpe unkritisch war:** sie war **ab 3 V
dokumentiert** (3 V – 400 mA) und für 3,7–6 V ausgelegt, lief also **innerhalb** ihres
Datenblattbereichs über den ganzen Entladezyklus — genau dafür war sie ausgewählt worden
(`../research/bom-check/06_pumpe-eu-quellen.md`). Dieser Vorteil ist mit dem Preis der
CONQUERALL (11,99 € statt 31,94 €) bezahlt.

**Das 2S-Konzept (2 Zellen + Step-Down) wurde am 16.09.2026 auf Wunsch des Nutzers umgesetzt** —
die damalige Gegenrede ist damit überholt und bleibt nur als Historie unten stehen. Was sich geändert hat
und warum: `hardware/schaltplan_v1.md` **§13** + `docs/11_review-2s-umbau.md`.
Kernpunkte: der Lader (IP2326) bringt ein eigenes 2S-Balancing mit, der Buck deckt den 3-A-Pumpenanlauf
(der 1S-Boost konnte das nicht), und die nutzbare Zellspanne reicht jetzt bis 6,16 V statt bis ~3,5 V.

**Die frühere Gegenrede (Stand 15.09.2026, hier als Historie):**
- **Wirkungsgrad bringt nichts:** Buck aus 2S (η 0,90) gegen Boost aus 1S (η 0,88) — Laufzeit
  praktisch identisch (32 vs. 31 Tage gerechnet). Und solange die Pumpe direkt an 1S läuft,
  entfällt die Wandlung komplett, das ist besser als jede Wandlung.
- **Kosten:** 2S braucht einen **eigenen Lader plus Balancer**, weil der Onboard-Lader des XIAO für
  eine Zelle (3,7 V / 4,2 V Ladeschluss) ausgelegt ist. Das sind zusätzliche Bauteile und
  Platinenfläche — bei einem Konzept, dessen Ziel „günstig" ist, der falsche Hebel.
- **Kapazität wird nicht gebraucht:** siehe §4 — die 1S-Zelle reicht für ~65 Dosiervorgänge.
- **Sicherheit:** Reihenschaltung ohne sauberes Balancing ist in einem feuchten Gehäuse ein
  echtes Risiko, nicht nur ein Schönheitsfehler.

## 3b. Reicht die Pumpe für Hub und Volumen? — nachgerechnet (14.09.2026)

Gegen die echten Projektwerte (`../docs/02_architektur-und-geometrie.md`): Hub Pumpenmitte
(y ≈ 114) bis Verteilerring auf der Substratoberfläche (y ≈ 260) = **~200 mm**, Saughöhe bis
Tankboden (y ≈ 8) = **~106 mm**, Dosis **150–350 ml** (gerechnet mit 300 ml), Tank 1,0 L.

| Prüfung | Rechnung | Ergebnis |
|---|---|---|
| **Förderhöhe** | 200 mm Wassersäule = ρ·g·h = **0,0196 bar** | gegen typ. 0,5–1 bar Pumpendruck → **20–40× Reserve** |
| **Leitungsverlust** | Hagen-Poiseuille, 3 mm ID, ~450 mm Weg, 150 ml/min | **0,0057 bar** → Gesamt-Gegendruck **0,025 bar** |
| **Saughöhe** | 106 mm gegen Datenblatt „Ansaugbereich 0,5 m" | **4,7× Reserve** ✅ |
| **Volumen/Zeit** | 300 ml bei 111 ml/min (3,7 V) | **2,7 min** (4,2 V: 2,4 min · 3,0 V: 3,3 min); größte Dosis 350 ml < 4 min ✅ |
| **Laufzeit** | 0,068 Wh je 300-ml-Dosis, 4,44 Wh nutzbar aus 1500 mAh | **~65 Dosen pro Ladung** ≈ 2,2 Monate bei 1×/Tag |
| **Tankfüllung** | 1000 ml / 300 ml | **3,3 Dosiervorgänge** → Tank alle 3–6 Tage nachfüllen (Blüte: 1–2 Tage/Gabe) |

**Fazit:** **Hub und Volumen sind kein Ausschlusskriterium** — die Förderhöhe ist bei Peristaltik
Trivialphysik (0,02 bar gegen ≥0,5 bar Pumpendruck). Die offenen Punkte liegen ausschließlich in
der **elektrischen Anlaufbarkeit** bei Unterspannung (§4c) und in der **Dosiergenauigkeit**:
Mini-Pumpen streuen laut eigener BOM-Notiz ±30 %, d. h. 300 ml können 210–390 ml werden →
Laufzeit einmal kalibrieren (30 s in den Messbecher), nicht blind auf ml/min vertrauen.

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
- **Laufzeit neu gerechnet (14.09.2026, CONQUERALL @3,7 V: ~1,5 W, ~111 ml/min):** ein Dosiervorgang
  von 300 ml braucht **~2,7 min** und **0,068 Wh**. Aus 1500 mAh @ 3,7 V (5,55 Wh brutto,
  ~4,44 Wh nutzbar) → **≈ 65 Dosiervorgänge pro Ladung**, bei 1× täglich also rund **2,2 Monate**.
  Die Energie je Dosis ist über den ganzen Entladezyklus praktisch konstant (0,067–0,071 Wh):
  bei niedrigerer Spannung läuft die Pumpe länger, zieht aber weniger Strom.
- **Warum keine 18650:** geschützte 18650 ist Ø18,85 × 69 mm und passt in die Wulst (40 mm tief),
  bringt aber ~3× Kapazität, die bei 65 Dosen pro Ladung niemand braucht. Option für später.

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
ohnehin im BOM haben. Den Gate-Widerstand R1 dafür von 220 Ω auf **4,7 kΩ** erhöhen: im Fehlerfall
(MCU will pumpen, Hardware sperrt) fließen dann 3 mA statt 14 mA durch den Klemmzweig; bei
Qg 6 nC bleibt das Schalten mit 20 kHz PWM unkritisch.

**Nicht doppelt bauen:** ein eigenes DW01A + FS8205A Schutzpaar ist bei JLC für 0,09 $ zu haben,
schaltet aber erst bei ~2,5 V ab — unterhalb unserer Hardware-Schwelle. Es dupliziert nur den
PCM der Zelle.

---

## 4c. Anlaufstrom 3 A gegen die Schaltung geprüft (14.09.2026)

**Frage:** Die CONQUERALL nennt **3 A Anlaufstrom** — trägt unsere Kette das?
(Werte: `hardware/schaltplan_v1.md` + `../docs/10_pcb-leiterbahnbreiten.md` + Datenblätter.)

**Ergebnis in einem Satz:** Der Strompfad trägt die 3 A kurzzeitig (MOSFET, Diode, Leiterbahnen),
aber **zwei Stellen können den Anlauf abschalten** — das PCM der Zelle (Overcurrent ~2–3 A) und der
Unterspannungswächter **MAX809 (3,08 V)** über den Spannungseinbruch. Das ist ein **Funktionsrisiko,
kein Sicherheitsrisiko**: nichts wird überlastet, die Pumpe bleibt nur stehen.

**1 · Der Anlaufstrom ist an unserer Zelle kleiner als 3 A.** Ein DC-Motor ist im Stillstand ohmsch:
`R_Motor = 5 V / 3 A = 1,67 Ω` → der Startstrom skaliert mit der Spannung:

| Zellspannung | 4,2 V | 4,0 V | 3,7 V | 3,4 V | 3,0 V |
|---|---|---|---|---|---|
| Anlaufstrom | 2,52 A | 2,40 A | 2,22 A | 2,04 A | 1,80 A |

**2 · Spannungseinbruch gegen die MAX809-Schwelle.** Serienwiderstände im Pumpenpfad (worst case):
Zelle 1500 mAh **80 mΩ** (typ. 60–100) · PCM 2× FS8205A **50 mΩ** · Q1 AO3400A @VGS 3,0 V **40 mΩ** ·
Leiterbahnen 0,5 mm über ~55 mm **64 mΩ** · JST-XH **20 mΩ** = **254 mΩ**.

| Zellspannung | Einbruch bei Anlauf | VBAT während des Anlaufs | gegen 3,08 V |
|---|---|---|---|
| 4,2 V | 0,64 V | 3,56 V | ✅ |
| 4,0 V | 0,61 V | 3,39 V | ✅ |
| 3,7 V | 0,56 V | 3,14 V | ✅ (knapp) |
| 3,4 V | 0,52 V | **2,88 V** | ❌ **MAX809 sperrt die Pumpe** |
| 3,0 V | 0,46 V | **2,54 V** | ❌ **MAX809 sperrt die Pumpe** |

→ **Unterhalb ~3,4 V Zellspannung startet die Pumpe nicht mehr** (mit 80 mΩ Zellwiderstand; bei
gesunden 60 mΩ verschiebt sich die Grenze auf ~3,1 V). Folge für die Firmware: der Feuchtewert
bleibt unverändert → die Diagnose würde fälschlich **„Tank leer / Pumpe verstopft"** melden.
Deshalb **VBAT während des Pumpvorgangs mitloggen** und Unterspannung getrennt melden (§4b Ebene 1).

**3 · PCM-Overcurrent der Zelle.** Typische 1S-PCMs mit **DW01A + FS8205A** schalten bei
**150 mV / (2 × RDS(on))** ab — mit 25–37 mΩ je FET also bei **2,0–3,0 A**. Der höchste Anlaufstrom
(2,5 A bei 4,2 V) liegt damit **genau auf der Schwelle**. Die EFASO-Zelle dokumentiert ihr PCM
**nicht** (§7) → Schwellwert am Prototyp messen.

**4 · Was die 3 A sicher trägt:**

- **Q1 AO3400A:** 5,2–5,8 A Dauerstrom im SOT-23 → 2,5 A Anlauf ✅; Verlust 0,36 W für die
  Anlaufdauer (~100 ms), im Dauerbetrieb bei 0,4 A nur **6 mW**.
- **D1 1N5819WS:** **1 A Dauer / 13 A Surge (8,3 ms)** — ⚠️ die oft zitierten 25 A gehören zur
  **DO-41-Version** 1N5819, nicht zur SOD-323-Variante. 3 A Freilaufpuls liegen trotzdem weit
  unter 13 A ✅.
- **Leiterbahnen 0,5 mm:** laut `docs/10` tragen sie 1,45 A bei 10 K **dauerhaft**; der Anlaufstrom
  fließt nur ~100 ms, Spannungsabfall dabei 141 mV ✅. Ein Dauerstrom von 3 A wäre **nicht** erlaubt —
  tritt aber nicht auf.
- **C3 100 µF: kein Anlaufschutz.** Er liefert 2,5 A nur **23 µs** lang (`t = C·ΔU/I`), das ist
  gegen den 100-ms-Motoranlauf wirkungslos. Nutzen hat er für HF-Störungen — dafür sitzt C11 100 nF
  direkt an den Pumpenklemmen.

**5 · Maßnahme: PWM-Softstart ist Pflicht (Firmware).** Mit einer Rampe über 100–300 ms steigt der
Strom nicht sprunghaft: bei **1,0 A** Anlaufstrom ist der Einbruch nur **0,25 V** → selbst aus 3,4 V
bleiben 3,15 V ✅, und die PCM-Schwelle wird sicher nicht erreicht. Der Pumpentreiber hängt am
GPIO2 über R1 4,7 kΩ / R2 47 kΩ und ist bereits PWM-fähig (20 kHz) → **keine Hardwareänderung,
nur Firmware**.

**6 · Konsequenz für die Pumpenwahl.** Die abgelöste OEM-Pumpe zog **0,4–0,54 A**: Einbruch ~0,14 V,
Anlauf unkritisch ohne jede Firmware-Maßnahme. Mit der CONQUERALL ist der Softstart **Bedingung**,
nicht Kür. Läuft die Pumpe an der Zelle trotzdem nicht sicher an, sind die Optionen in dieser
Reihenfolge: (a) Softstart + Messung, (b) Boost auf 5 V, (c) 2S, (d) zurück zur OEM-Pumpe (31,94 €).

---

## 5. Wulst-Maße (aus den finalen Bauteilen abgeleitet)

| Innenmaß | Wert | Bestimmt durch |
|---|---|---|
| Breite | **60 mm** | Pumpe + Wandungen, PCB ~52 mm, Zelle 37 mm |
| Tiefe (radial) | **40 mm** | Pumpe (Ø war 32 mm angenommen) + 2 × 2,5 mm Wand + Montagefreiheit |
| Höhe | **160 mm** (y = 90–250) | Pumpe + Halterung, darüber Platine + Zelle |
| Gesamtbreite Topf an der Wulst | **≈ 180 mm** | 140 mm + 40 mm |

Einbau von unten nach oben: **Pumpe** (Bauhöhe jetzt **42 mm** statt 44 mm, dadurch noch etwas mehr
Luft) → **Platine** → **Zelle** hinter/über der Platine.

⚠️ **Offener Punkt aus dem Pumpenwechsel (14.09.2026): Die CONQUERALL gibt keinen Durchmesser an.**
Die Wulst ist mit **Ø 32 mm** gerechnet worden (OEM-Pumpe). Die Bauhöhe ist mit 42 mm bestätigt, der
Ø muss **vor dem Einbau gemessen** werden — ist er größer als ~34 mm, wird die Wulsttiefe von 40 mm
knapp (Pumpe + 2 × 2,5 mm Wand + Montagefreiheit). Notfalls Wulst auf 44 mm Tiefe ziehen
(Gesamtbreite dann ≈ 184 mm).

**CAD-Parameter (`cad/params.py`):** dort stehen noch `pump_d = 27.8` · `pump_l = 66.8` ·
`pump_mount_cc = 50.0` · `pump_mount_d = 3.7` — die Werte der ursprünglichen Pumpe. Sie werden von
**keinem** Modul verwendet (nur Doku, per grep geprüft), die Wulst selbst ist parametrisch
unabhängig. Nach dem Ausmessen der CONQUERALL auf die gemessenen Werte ziehen (oder die Zeilen
löschen, damit sie nicht als Geometrie-Wahrheit missverstanden werden).

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
3. Pumpe: AO3400A Low-Side, **Gate 4,7 kΩ, Pulldown 47 kΩ** (Review 1), 1N5819 antiparallel, **100 µF Pufferelko** + 100 nF an den Klemmen (Review 3).
   Pumpe hängt **direkt an VBAT** — kein Wandler, kein Boost-Layout.
   ⚠️ **Anlaufstrom (14.09.2026, §4c):** die aktuelle Pumpe (CONQUERALL DC 5 V) zieht beim Anlauf
   **2,2–2,5 A** — der härteste Fall des ganzen Designs. Der 100-µF-Elko deckt davon nur **23 µs** ab
   (kein Anlaufschutz, nur HF-Bedämpfung), VBAT bricht über den 254-mΩ-Pfad um ~0,56 V ein, und damit
   kann der **MAX809 (3,08 V) die Pumpe selbst abschalten**, sobald die Zelle unter ~3,4 V liegt.
   → **PWM-Softstart (Rampe 100–300 ms) ist Pflicht** — reine Firmware, keine Hardwareänderung
   (GPIO2 → R1 → Gate; 20 kHz PWM ist ohnehin vorgesehen).
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
   `cad/params.py`. Espressif schreibt außerdem vor, das **Endprodukt zu testen** (Durchsatz +
   Reichweite); fällt der Test schlecht aus, ist die Alternative das Modul **-1U** (`C20627095`) mit
   IPEX-Buchse und externer Antenne.
6b. **Espressif empfiehlt bei Akkubetrieb ausdrücklich einen Power-Monitor-Chip mit ~3,0-V-Schwelle** —
   genau das ist unser MAX809TEUR+T (3,08 V, §4b). Zwei unabhängige Quellen treffen sich hier.
7. **Kein XIAO mehr:** Lader, LDO und USB sind komplett durch eigene Bauteile ersetzt, die geplante
   V1/V2-Unterscheidung entfällt — es gibt **eine** Platine.

---

## 8. Optionale Sauerstoffpumpe (5 V) — recherchiert und ausgewählt (15.09.2026)

Die Sauerstoffpumpe hängt am zweiten Pumpenpfad (`Q3`, `R33`, `R34`, `D7`, `D8`, `C20`, Stecker **J16**
= JST-XH 2P aufrecht, Steuerung **IO22**) und wird aus dem neuen **5-V-Boost** (U8 MT3608) versorgt.
Damit sind die Randbedingungen fix: **5 V DC**, **≤ 1 A** (Pfad ausgelegt), Betrieb **im Intervall**.

### Empfehlung

**Mini USB Aquarium Luftpumpe, leise, mit Luftstein — Amazon `B0FXB5BMTT`, 8,48 €** (3,9 ★ / 45 Bewertungen)

| Kandidat | Preis | Bewertung | Spannung | Leistung | Förderleistung | Lautstärke | Lieferumfang |
|---|---|---|---|---|---|---|---|
| **`B0FXB5BMTT`** (Empfehlung) | **8,48 €** | 3,9 ★ | **5 V USB** | ~1 W | für 10–40 L | < 35 dB | **Pumpe + 1,15 m Silikonschlauch + Luftsprudler** |
| `B093GPMT1Z` | 9,99 € | 4,1 ★ | 5 V USB | 1 W | **210 L/h**, 150 g | leise (Keramikmotor) | Pumpe |
| `B0F1T8SPL3` | 9,00 € | 4,3 ★ | 5 V USB | 1 W | 130 g | „super silent" | Pumpe (Schlauch/Stein extra) |
| `B0GWMCWPNQ` | 8,99 € | 4,3 ★ | 5 V USB | 1 W | 130 g | leise (Keramikmotor) | Pumpe |
| `B0B82JX6Z4` (Colexy) | 7,29 € | 3,4 ★ | 5 V USB | 1 W | regelbar, 90 g | leise | Pumpe |
| ~~`B0FRFXMRDT`~~ (Pawfly Nano Silent) | 13,99 € | 4,2 ★ | **nicht als 5 V DC spezifiziert** | 1,3 W | 27 L/h (450 ml/min) | 30 dB (piezo) | Komplettset inkl. Rückschlagventil |
| ~~`B08MSYJRHC`~~ (Boxtech) | 32,99 € | 4,4 ★ | 2/5/8/10 W | zu groß/teuer | — | — | — |
| ~~`B0CKXKY31J`~~ (AQQA) | 37,99 € | 4,5 ★ | 4 Ausgänge, 10 W | **weit über dem Boost** | — | — | — |

**Warum der Empfehlungskandidat:** Er ist der einzige in der engen Auswahl, bei dem die Betriebsspannung
**explizit 5 V USB** ist *und* **Schlauch + Sprudelstein im Lieferumfang** sind — damit ist die Pumpe
sofort betriebsfertig, ohne Zusatzkauf. Er ist für **10–40 L** ausgelegt (unser Topf liegt deutlich
darunter) und laut Datenblatt **dauerbetriebsfähig**, was im Intervallbetrieb viel Reserve bedeutet.

**Pawfly (13,99 €, 30 dB) wäre der leiseste**, ist aber piezo-elektrisch und die Angebotsseite nennt
**keine 5-V-DC-Spannung** (Pawfly führt dieselbe Bauform auch als 230-V-Gerät) → für ein 5-V-Bordnetz
**nicht ohne Risiko**, deshalb nicht empfohlen.

### Strom- und Laufzeitrechnung (für die Auslegung)

| Größe | Wert |
|---|---|
| Leistung | 1 W bei 5 V → **0,20 A** am Boost-Ausgang |
| Strom aus der Zelle (3,7 V, η ≈ 0,85) | **≈ 0,32 A** |
| Zelle 1500 mAh, **Dauerbetrieb** | **≈ 4,7 h** bis leer |
| Intervall 6 × 15 min/Tag | 1,5 h/Tag, **≈ 0,5 Wh/Tag** — energetisch vernachlässigbar |
| Last für den Boost (1 A möglich) | 0,2 A → **unkritisch**, PWM-Softstart trotzdem sinnvoll |

### Anbindung (Hardware)

- Die Pumpe kommt mit **USB-A-Stecker**: Kabel abschneiden, **rot = +5 V**, **schwarz = GND**, auf
  **JST-XH 2P** crimpen (gleicher Steckertyp wie die Dosierpumpe an J4 → ein Crimp-Werkzeug).
- **Rückschlagventil** in die Luftleitung (sonst zieht Wasser in die Pumpe, wenn sie aus ist).
- **Membranpumpe braucht Frischluft** → außerhalb des Topfs montieren, Luftleitung in die Nährlösung.
- Betrieb über **IO22** (`PUMP2_EN`) mit **PWM-Softstart** (gleiche Rampe wie die Dosierpumpe).
- ⚠️ Energetisch gilt weiter: **nicht dauerhaft laufen lassen** — bei 1 W sind es ~4,7 h, das reicht
  für Intervall-Sauerstoffgabe, nicht für 24/7.

### Kaufquellen
- Empfehlung: https://www.amazon.de/dp/B0FXB5BMTT (8,48 €)
- Alternative kräftiger (210 L/h): https://www.amazon.de/dp/B093GPMT1Z (9,99 €)
- Alternative günstig: https://www.amazon.de/dp/B0B82JX6Z4 (7,29 €, regelbar)

## 7. Noch offen / bewusst nicht behauptet

**Zur neuen Pumpe (CONQUERALL `B0DHVMZ27Y`) — der Messauftrag vor dem Einbau:**

- **Förderrate bei 3,0 / 3,7 / 4,2 V** nicht dokumentiert (Angabe „≤150 ml/min" gilt bei 5 V Nennspannung).
  → Labornetzteil, je 30 s in den Messbecher, auf ml/min umrechnen. **Entscheidet über die Dosiermenge
  in der Firmware.**
- **Läuft sie bei Unterspannung überhaupt an?** Bei 3,0/3,4 V ist das Losbrechmoment nicht belegt — genau
  die Spannungslage, in der der MAX809 zusätzlich sperrt (§4c). Test an einer echten Zelle mit
  Ladezuständen ~100 % / ~60 % / ~30 %.
- **Anlaufstrom am realen Aufbau messen** (Shunt/Stromzange) und mit der PCM-Schwelle vergleichen (§4c).
- **Ø der Pumpe** nicht dokumentiert → ausmessen (Wulst auf Ø 32 gerechnet, §5).
- **PWM-Softstart in der Firmware implementieren** — mit dieser Pumpe Bedingung, nicht optional (§4c).
- **Firmware:** VBAT während des Pumpvorgangs mitloggen und Unterspannung getrennt von „Tank leer" melden,
  sonst wird der MAX809-Eingriff als Verstopfung fehlgedeutet (§4c Punkt 2).

**Bestehende offene Punkte:**

- **Schlauch** muss beschafft werden (3 × 5 mm Silikon, ~1 m) — Position 8. Passt zur CONQUERALL
  (Schlauchdurchmesser 3 × 5 mm bestätigt).
- **Elektrodenlänge des Sensor v1.2** nicht belegt → am realen Board messen (Messebene liegt 75 mm tief).
- **LDO-Bestückung** des AZ-Boards nur im Foto prüfbar (nicht im Text).
- **Maße der EFASO-Zelle** am Listing nicht bestätigt.
- **Abschaltspannung *und* Abschaltstrom des EFASO-PCM** nicht dokumentiert → beim Hersteller erfragen
  oder am Prototyp messen (Ebene 4 in §4b, Strom in §4c Punkt 3).
- **RF-Endtest** am fertigen Gehäuse (Espressif-Vorgabe) — ohne Test ist die Antennenperformance unbelegt.
- **Ruhestrom des ME6211** (40 µA) kostet ~29 mAh/Monat; Alternative TPS7A02 (25 nA) fällt weg, weil er
  nur 200 mA kann und der TX-Peak 382 mA ist.
- Versandkosten der übrigen Shops nicht geprüft (AZ-Delivery versandkostenfrei ab 25 €).
- Amazon-Preise von Agenten im Browser gesehen, nicht selbst nachprüfbar (Amazon blockt Skript-Abrufe).
