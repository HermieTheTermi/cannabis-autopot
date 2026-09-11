# PCBA-Verfügbarkeit bei JLCPCB — Smart Grow Topf V1

Stand: 11.09.2026 · Methode: JLCPCB-Parts-API (`selectSmtComponentList/v2`, Skill `jlcpcb-parts-check`),
jede Zeile ein echter API-Treffer. Preise = 1-Stück-Staffel in USD. `base` = Basic (keine
Handling-Gebühr) · `expand` = Extended (**+3 USD pro Position**).

## 1. Ergebnis: PCB bestückbar — mit drei Lücken

| Pos | Bauteil | LCSC | Paket | Typ | Bestand | Preis | Bewertung |
|---|---|---|---|---|---|---|---|
| Q1 | MOSFET **AO3400A** | `C20917` | SOT-23 | **base** | 901.401 | $0,0846 | ✅ Basic |
| D1 | Schottky **1N5819WS** | `C191023` | SOD-323 | **base** | 5.648.846 | $0,0137 | ✅ Basic |
| C1 | 100 nF 50 V | `C49678` | 0805 | **base** | 18.879.051 | $0,0196 | ✅ Basic |
| C2 | 10 µF 25 V | `C15850` | 0805 | **base** | 7.091.278 | $0,0841 | ✅ Basic |
| C3 | 100 µF 16 V | `C970684` | SMD D6,3×5,4 | expand | 33.972 | $0,0358 | ✅ (keramisch 1210 `C2840614` = **0 Bestand**) |
| R1 | 220 Ω ±1 % | `C17557` | 0805 | **base** | 1.195.891 | $0,0058 | ✅ Basic |
| R2 | 10 kΩ ±1 % | `C17414` | 0805 | **base** | 54.371.929 | $0,0039 | ✅ Basic |
| R3 | 200 kΩ ±1 % | `C17539` | 0805 | **base** | 772.897 | $0,0064 | ✅ Basic (VBAT-Teiler) |
| R4 | 1 kΩ ±1 % | `C17513` | 0805 | **base** | 30.777.601 | $0,0042 | ✅ Basic (LED) |
| D2 | LED rot | `C84256` | 0805 | **base** | 6.142.311 | $0,0134 | ✅ Basic |
| SW1/2 | Taster 5,1×5,1×1,5 | `C318884` | SMD-4P | **base** | 769.000 | $0,0205 | ✅ Basic (Reset + Boot) |
| J1 | Akku **JST PH 2,0 mm** 2-pol | `C54582899` | SMD 2 mm, gewinkelt | expand | 2.308 | $0,0466 | ⚠️ Original `S2B-PH-SM4-TB` **nicht** im Sortiment → generisches PH-Äquivalent; Alternative: `C173752` (THT gewinkelt, 29.680) |
| J2 | Sensor **JST-XH 2,5 mm** 3-pol | `C157928` | THT gewinkelt | expand | 146.324 | $0,0745 | ✅ |
| J4 | Pumpe **JST-XH 2,5 mm** 2-pol | `C157931` | THT gewinkelt | expand | 50.464 | $0,1014 | ✅ |
| U7 | **MAX809TEUR+T** Spannungsdetektor 3,08 V | `C16711` | SOT-23 | expand | 13.783 | $0,5628 | ✅ Unterspannungsschutz, siehe `bom_entscheidung.md` §4b |
| D3 | Schottky (Klemmzweig) | `C191023` | SOD-323 | **base** | 5.648.846 | $0,0137 | ✅ gleicher Typ wie D1 |
| U1 | **XIAO ESP32-C6** | – | – | – | – | – | ❌ **nicht bestückbar**, siehe §2 |
| J3 | Buchsenleiste 2,54 1×7 | – | – | – | – | – | ❌ **nicht im Sortiment**, siehe §2 |

**Für V1 (XIAO-Variante) heißt das:** 4 Extended-Positionen (C3, J1, J2, J4) = **12 USD Handling**,
alles andere ist Basic. Ohne die Steckverbinder wären es 3 USD.

## 2. Die drei Lücken — und wie wir sie sauber lösen

**(a) XIAO ESP32-C6 ist bei JLCPCB nicht bestückbar.** Die Suche liefert nur Platzhalter
(`C9900124963`, LCC-14, „邮寄专用" = *nur Versand*, 0 Bestand, kein Preis). Andere XIAO-Modelle
sind dagegen im Sortiment (ESP32-S3 `C20467913`, ESP32-C5 `C54119401`, nRF52840) — nur die C6-Variante
fehlt.
→ **Lösung:** XIAO selbst flach auflöten (Castellated Pads, dafür ist das Modul gemacht). Er wird
dann nicht von JLC bestückt und im BOM als „nicht bestücken / DNP" markiert — Standardvorgehen.
**Kein Buchsenleisten-Sockel nötig**, dadurch entfällt J3 komplett (und die Höhe über der Platine
bleibt klein).

**(b) Buchsenleiste 2,54 mm 1×7: „not in JLCPCB parts library".** Fällt mit (a) weg — direkt auflöten
statt sockeln.

**(c) Original-JST `S2B-PH-SM4-TB` fehlt** (nur Platzhalter, 0 Bestand). Es gibt aber ein
funktionsgleiches PH-2,0-mm-SMD-Äquivalent (`C54582899`, 2.308 Stück). Engpass: nur 2.308 Stück —
für ein Einzelstück irrelevant.

## 3. Kernteile am Herstellerdatenblatt gegengeprüft

**AO3400A** (Alpha & Omega, Quelle `aosmd.com/pdfs/datasheet/AO3400A.pdf`):
`VDS 30 V` · `ID 5,7 A` · `RDS(on) < 48 mΩ bei VGS = 2,5 V`, `< 32 mΩ bei 4,5 V` · `VGS(th) 0,65–1,45 V`
· `QG 6–7 nC` · `VGS max ±12 V`.
→ Für die Pumpe: bei 3,3 V Gate-Spannung liegt RDS(on) zwischen 32 und 48 mΩ; bei 0,45 A sind das
**< 10 mW** Verlustleistung. Logic-Level bestätigt, PWM-fähig, Tore nicht gefährdet. ✅

**1N5819WS** (Herstellerdatenblatt Heketai, über LCSC): `VRRM 40 V` · `IF(AV) 1,0 A` · `IFSM 25 A` ·
`VF max 0,60 V bei 1 A` · SOD-323.
→ Als Freilaufdiode an 0,45 A reichlich dimensioniert (5× Reserve beim Surge). ✅

## 4. Für die V2-Platine (nacktes ESP32-C6-Modul) — alles vorhanden

| Pos | Bauteil | LCSC | Paket | Typ | Bestand | Preis |
|---|---|---|---|---|---|---|
| U2 | **ESP32-C6-MINI-1** | `C5736265` | SMD-53P | expand | 2.824 | $3,8871 |
| U2b | ESP32-C6-MINI-1-H4 | `C6553337` | SMD 16,6×13,2 | expand | 779 | $4,5588 |
| U3 | **MCP73831** 1S-Lader | `C424093` | SOT-23-5 | expand | 3.172 | $0,8181 |
| U3b | MCP73831 (Alt.) | `C14879` | SOT-23-5 | expand | 1.639 | $1,2589 |
| U4 | **HT7333-A** 3,3 V LDO (250 mA) | `C21583` | SOT-89-3 | expand | 15.949 | $0,2414 |
| U5 | SS34 (Verpol-/Schutzdiode) | `C8678` | SMA | **base** | 5.064.497 | $0,0349 |
| Q2 | Si2301 P-MOSFET (High-Side optional) | `C10487` | SOT-23 | **base** | 163.319 | $0,1032 |
| J5 | USB-C Buchse 16-pol | `C165948` | SMD | expand | 245.957 | $0,1858 |

**Wichtig zu V2:** der Lade-IC **SGM40567** (der auf dem XIAO sitzt) ist bei JLC **nicht verfügbar**
(WLCSP, 0 Bestand) — für die eigene Platine also **MCP73831** verwenden.
Und: HT7333 statt AMS1117-3.3. Der AMS1117 ist bei JLC Basic und billiger, hat aber hohen Dropout und
mehrere mA Eigenverbrauch — bei Akkubetrieb mit Deep-Sleep wäre das der größte Dauerposten. Der
HT7333 (250 mA) passt zum Verbrauch: ESP32 + Sensor, kein Pumpenstrom über den LDO.

## 5. Nicht geprüft / offen

- **Stückpreise in EUR** inkl. Zoll/Umsatzsteuer und **Versandkosten** der JLC-Bestellung nicht geprüft.
- **Mindestbestückungsmenge (leastPatchNumber)** und MOQ je Position nicht ausgewertet.
- **Alternative Basic-Positionen** für die 4 Extended-Teile (spart 9 USD) nicht gesucht: möglich wäre
  z. B. ein Basic-100-µF oder Pin-Header statt JST. Lohnt erst, wenn das Layout steht.
- **Pumpe/Sensor/Akku** kommen nicht von JLC, sondern wie in `bom_entscheidung.md` beschrieben.
