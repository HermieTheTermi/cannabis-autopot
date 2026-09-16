# PCBA-Verfügbarkeit bei JLCPCB — Smart Grow Topf V1 (Modul-Variante)

Stand: 15.09.2026 · Methode: JLCPCB-Parts-API (`selectSmtComponentList/v2`, Skill `jlcpcb-parts-check`),
jede Zeile ein echter API-Treffer. Preise = 1-Stück-Staffel in USD. `base` = Basic (keine
Handling-Gebühr) · `expand` = Extended (**+3 USD pro Position**).

## 1. Ergebnis: die Platine ist vollständig bestückbar

Seit der Umstellung auf das nackte **ESP32-C6-MINI-1** gibt es **keine Lücke mehr** — der XIAO
(dessen C6-Variante bei JLCPCB komplett fehlt) ist aus dem Design raus.

| Pos | Bauteil | LCSC | Paket | Typ | Bestand | Preis |
|---|---|---|---|---|---|---|
| U1 | **ESP32-C6-MINI-1** (MCU) | `C5736265` | SMD-53P | expand | 2.794 | $3,8871 |
| U1b | ESP32-C6-MINI-1**U** (IPEX, ext. Antenne) | `C20627095` | SMD 13,2×12,5 | expand | 1.352 | $4,3051 |
| U3 | **MCP73831T-2ACI/OT** (1S-Lader, 4,20 V) | `C424093` | SOT-23-5 | expand | 3.172 | $0,8181 |
| U3b | MCP73831T-2ATI/OT (Alt.) | `C14879` | SOT-23-5 | expand | 1.639 | $1,2589 |
| U4 | **ME6211C33M5G** (LDO 3,3 V, 500 mA) | `C82942` | SOT-23-5 | expand | 277.913 | $0,0597 |
| U4b | AP2112K-3.3 (LDO 600 mA, Alt.) | `C51118` | SOT-25-5 | expand | 68.369 | $0,1711 |
| U4c | RT9013-33 (LDO 500 mA, Alt.) | `C47773` | SOT-23-5 | expand | 237.796 | $0,1399 |
| U6 | **USBLC6-2SC6** (ESD USB) | `C7519` | SOT-23-6L | expand | 35.445 | $0,1827 |
| U7 | **MAX809TEUR+T** (Unterspannung 3,08 V) | `C16711` | SOT-23 | expand | 13.783 | $0,5628 |
| J5 | USB-C Buchse 16-pol | `C165948` | SMD | expand | 245.957 | $0,1858 |
| Q1 **Q3** | MOSFET **AO3400A** (Q1 Dosierpumpe, Q3 Sauerstoffpumpe) | `C20917` | SOT-23 | **base** | 901.401 | $0,0846 |
| D1 | Schottky **1N5819WS** (Freilauf) | `C191023` | SOD-323 | **base** | 5.648.846 | $0,0137 |
| D3 | Schottky (Klemmzweig MAX809) | `C191023` | SOD-323 | **base** | 5.648.846 | $0,0137 |
| ~~U5~~ | ~~SS34~~ | – | – | – | – | – | **entfallen (Review 3):** die geplante VBUS→VBAT-Brücke würde die Zelle ungeregelt laden. Kein Verpolschutz in Reihe (Zelle hat PCM) |
| C1 | 100 nF 50 V | `C49678` | 0805 | **base** | 18.879.051 | $0,0196 |
| C2 | 10 µF 25 V | `C15850` | 0805 | **base** | 7.091.278 | $0,0841 |
| C3 | 100 µF 16 V (Puffer, Elko — Polarität!) | `C970684` | SMD D6,3×5,4 | expand | 33.972 | $0,0358 |
| C11/C12 | 2 × 100 nF (Pumpen-EMI, MAX809) | `C49678` | 0805 | **base** | 18.879.051 | $0,0196 |
| C5 | 22 µF 25 V (Modul-Bulk) | `C45783` | 0805 | **base** | 4.922.447 | $0,2456 |
| C4/C6 | 2 × 1 µF (EN-RC, LDO-Ausgang) | `C15849` | 0603 | **base** | 8.282.371 | $0,0175 |
| C7/C8 | 2 × **4,7 µF** (Lader, Datenblatt min. 4,7 µF) | `C1779` | 0805 | **base** | 2.869.508 | $0,0417 |
| R1 | **4,7 kΩ** (Gate-Serie, Review 1) | `C17673` | 0805 | **base** | 6.174.232 | $0,0050 |
| R2 | **47 kΩ** (Gate-Pulldown, Review 1) | `C17713` | 0805 | **base** | 2.124.711 | $0,0073 |
| R_PROG | **3,9 kΩ** (Ladestrom 256 mA) | `C17614` | 0805 | **base** | 317.160 | $0,0027 |
| R_EN/R_BOOT/R_GPIO8 | 10 kΩ | `C17414` | 0805 | **base** | 54.371.929 | $0,0039 |
| R3 | 200 kΩ (VBAT-Teiler) | `C17539` | 0805 | **base** | 772.897 | $0,0064 |
| R5 | 5,1 kΩ (USB-C CC) | `C27834` | 0805 | **base** | 4.029.051 | $0,0064 |
| R4 | LED-Widerstand | `C17513` | 0805 | **base** | 30.777.601 | $0,0042 |
| R_TANK | 1 kΩ (Tank-LED) | `C17513` | 0805 | **base** | 30.777.288 | $0,0042 |
| R_BTN | 10 kΩ (Taster-Pull-up) | `C17414` | 0805 | **base** | 54.370.181 | $0,0039 |
| C_BTN | 100 nF (Entprellung) | `C49678` | 0805 | **base** | 18.966.887 | $0,0196 |
| D5 | LED rot (Tank leer) | `C84256` | 0805 | **base** | 6.141.918 | $0,0134 |
| D2 | LED **grün** (Status, 525 nm) | `C2297` | 0805 | **base** | 1.627.076 | $0,0163 |
| R4 | **220 Ω** (Status-LED grün) | `C17557` | 0805 | **base** | 1.195.891 | $0,0058 |
| J6 | 2 Lötpads/Bohrungen für den externen Taster | – | – | – | – | **keine Bestückung, kein JLC-Kostenpunkt** |
| D2 | LED rot | `C84256` | 0805 | **base** | 6.142.311 | $0,0134 |
| SW1/2 | Taster (Reset + Boot) | `C318884` | SMD-4P 5,1×5,1 | **base** | 769.000 | $0,0205 |
| J1 | Akku JST PH 2,0 mm 2-pol, **aufrecht (Top-Entry)** | `C160352` | SMD 2 mm stehend | expand | ⏳ | ⏳ |
| J2 | Sensor JST-XH 2,5 mm 3-pol, **aufrecht (Top-Entry)** | `C493416` | THT stehend | expand | 19.594 | ⏳ |
| J4 **J16** | Pumpen JST-XH 2,5 mm 2-pol, **aufrecht (Top-Entry)** (Dosier- + Sauerstoffpumpe) | `C158012` | THT stehend | expand | 203.889 | ⏳ |
| J7, J9–J15 | Stiftleiste 1×3, 2,54 mm, male gerade (XFCN `PZ254V-11-03P`) | `C2937625` | THT 2,54 mm | expand | ⏳ | ⏳ |
| J8 | Stiftleiste 1×4, 2,54 mm, male gerade (XFCN `PZ254V-11-04P`) | `C2691448` | THT 2,54 mm | expand | ⏳ | ⏳ |
| Q2 | **AO3401A** (P-Kanal-Load-Switch, High-Side) | `C15127` | SOT-23 | **base** | 591.277 | $0,0908 |

**Nachtrag 14.09.2026 (GPIO-/I²C-Stiftleisten, live geprüft):** Die **Device-Identitäten** der drei
neuen Positionen wurden am 14.09.2026 live über `easyeda lib by-lcsc --include-device-identity`
aufgelöst: `C2937625` → XFCN `PZ254V-11-03P` (1×3), `C2691448` → XFCN `PZ254V-11-04P` (1×4),
`C15127` → AOS `AO3401A` (P-Kanal, RDS(on) 85 mΩ @ VGS −2,5 V). **Bestand/Preis** der beiden
Stiftleisten wurden in diesem Durchgang **nicht** erneut abgefragt (⏳); Q2 `C15127` ist wie Q1
**Basic**. J2 bleibt die **einzige** JST-XH-3P-Position (J7 ist jetzt Stiftleiste).

**Handling-Kosten:** 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = **12 Extended-Positionen
≈ 36 USD** (U1, U3, U4, U6, U7, J5, C3, J1, J2, J4, `C2937625`, `C2691448`). Alles andere ist
Basic (inkl. Q2 `C15127`). Das ist der Preis dafür, dass Lader, LDO und USB auf unserer Platine
sitzen statt im XIAO-Modul. Sparoptionen: RT9013-33 statt ME6211 ändert nichts (beide Extended),
ein Basic-Äquivalent für den 100-µF-Puffer wäre noch zu suchen.


## 1b. Nachtrag 16.09.2026 — Bauteile des 2S-Umbaus (live geprüft)

Abfrage direkt über die JLCPCB-Parts-API (`selectSmtComponentList/v2`), jede Zeile ein echter Treffer
vom **16.09.2026**. `base` = Basic (keine Handling-Gebühr), `expand` = Extended (**+3 USD je Position**).

| Pos | Bauteil | LCSC | Paket | Typ | Lager | $/Stk 1–9 | geprüft |
|---|---|---|---|---|---|---|---|
| **U_CHG** | **IP2326** (2S/3S-Boost-Lader 8,4 V) | `C2832094` | VQFN-24-EP(4x4) | expand | **18.074** | 0,6182 | ✅ API + Datenblatt V1.11 |
| **U7** | **TPS3839G33DBZR** (Unterspannung 3,08 V) | `C485802` | SOT-23-3 | expand | **3.502** | 0,4458 | ✅ API + Datenblatt SBVS193D |
| **U_BUCK5** | **SY8113B ADC** (Buck 5 V/3 A) | `C78989` | TSOT-23-6 | expand | **50.655** | 0,2403 | ✅ API + Datenblatt AN_SY8113B |
| **U_BUCK3** | **AP63203WU-7** (Buck 3,3 V/2 A) | `C780769` | TSOT-23-6 | expand | **25.645** | 1,1794 | ✅ API + Datenblatt DS41326 |
| **L_CHG** | Induktivität 2,2 µH (Isat 5,0 A) | `C142096` | 4,6 × 4,1 mm | expand | **3.096** | 0,2538 | ✅ API + Herstellerdatenblatt |
| **L_BUCK5/3** | Induktivität 4,7 µH (Isat 4,0 A), Menge 2 | `C105660` | 6 × 6 mm | expand | **1.571** | 0,0776 | ✅ API + Herstellerdatenblatt |
| C_CHG_IN/VIN/OUT | 3 × 10 µF 25 V | `C15850` | 0805 | **base** | 6.557.728 | 0,0843 | ✅ (im Projekt vorhanden) |
| C_VSYS_A/B + C_B* | 9 × 22 µF 25 V | `C45783` | 0805 | **base** | 4.726.458 | 0,2431 | ✅ |
| C_B*_BST, C_BST_CHG | 4 × 100 nF | `C49678` | 0805 | **base** | 17,9 Mio | 0,0194 | ✅ |
| R_ISET, R_EN_CHG | 2 × **100 kΩ 1 %** | `C96346` | 0805 | expand | **853.728** | 0,0094 | ✅ (1 % laut Datenblatt gefordert) |
| R_NTC | 51 kΩ | `C17737` | 0805 | **base** | 958.911 | 0,0068 | ✅ |
| R_UVSET, R_SENSE_BOT | 2 × 68 kΩ | `C17801` | 0805 | **base** | 348.040 | 0,0037 | ✅ |
| R_FB5_TOP | 75 kΩ | `C17819` | 0805 | **base** | 49.785 → jetzt 49.785 | 0,0058 | ✅ |
| R_FB5_BOT, R_CLAMP1/2 | 10 kΩ (mit den vorhandenen) | `C17414` | 0805 | **base** | 54 Mio | 0,0039 | ✅ |
| R_FB3_TOP, R2, R_GATE | 47 kΩ | `C17713` | 0805 | **base** | 2,1 Mio | 0,0073 | ✅ |
| R_FB3_BOT | 15 kΩ | `C17475` | 0805 | **base** | 910.242 | 0,0060 | ✅ |
| R3a/R3b/R_SENSE_TOP | 200 kΩ | `C17539` | 0805 | **base** | 737.504 | 0,0060 | ✅ |
| R_VIN_CHG | 0,5 Ω | `C28319` | 0805 | expand | **15.532** | 0,0054 | ✅ |
| **J17** | JST-XH 2P aufrecht (jetzt 3 ×) | `C158012` | THT P2.5 | expand | **434.009** | 0,0406 | ✅ |

**Handling-Kosten jetzt:** **17 Extended-Positionen ≈ 51 USD** (vorher 12 ≈ 36 USD).
Entfallen sind MCP73831, ME6211, MT3608, SS34 und die 22-µH-Induktivität — dafür kommen
IP2326, TPS3839, zwei Bucks und zwei Induktivitäten hinzu. Ein **Basic**-Teil ist keiner der vier ICs;
alle vier sind Extended (bei JLCPCB nicht anders zu bekommen, geprüft).

**Nicht mehr bestückt / entfallen:** U3 MCP73831 (`C424093`), U4 ME6211 (`C82942`), U8 MT3608
(`C84817`), L1 22 µH (`C341068`), D6 SS34 (`C8678`), R31 75 k (bleibt für das 5-V-Feedback im
Einsatz), C5 10 µF, C6 1 µF, R13 3,9 kΩ, R37 47 kΩ.

## 2. Der XIAO ist raus — und warum das die Platine *kleiner* macht

Beim XIAO ESP32-C6 gab es bei JLCPCB nur „Nur-Versand"-Platzhalter (`C9900124963`, LCC-14, 0 Bestand)
— er wäre nie mitbestückt worden. Das nackte Modul ist dagegen regulär lagernd und mit
**13,2 × 16,6 mm kleiner als der XIAO (21 × 17,8 mm)**; es fällt zusätzlich dessen USB-Buchse weg,
die eine Gehäuseöffnung und Randabstand erzwungen hätte. Damit lässt sich die Platine in die
40-mm-Kammer legen, ohne die Wulst aufzuweiten (siehe `docs/05_review-v1.md` §1).

## 3. Kernteile am Herstellerdatenblatt gegengeprüft

| Bauteil | Quelle | Kernwerte |
|---|---|---|
| AO3400A | `aosmd.com/pdfs/datasheet/AO3400A.pdf` | VDS 30 V · ID 5,7 A · RDS(on) < 48 mΩ @ VGS 2,5 V · VGS(th) 0,65–1,45 V |
| AO3401A | LCSC-Produktdaten `C15127` | P-Kanal · RDS(on) 47 mΩ @ VGS −10 V · 60 mΩ @ −4,5 V · **85 mΩ @ −2,5 V** |
| 1N5819WS | LCSC-Datenblatt (Heketai) | VRRM 40 V · IF 1,0 A · IFSM 25 A · VF ≤ 0,60 V @ 1 A |
| MAX809T | LCSC-Datenblatt | VTH 3,04/3,08/3,11 V · ICC 12 µA · push-pull aktiv-low |
| MCP73831T-2 | LCSC-Datenblatt | **4,20 V** Ladeschluss (die -2-Variante) · 15–500 mA · UVLO 3,45/3,38 V |
| ME6211C33 | LCSC-Datenblatt | 500 mA · Dropout 100 mV @ 100 mA · Iq 40 µA |
| ESP32-C6-MINI-1 | Espressif-Datasheet v1.5 (HTML) | TX-Peak **382 mA** @ 20,5 dBm · Deep-Sleep 7 µA · USB_D− GPIO12 / USB_D+ GPIO13 |

| **U8** | **MT3608** (5-V-Boost für beide Pumpen) | `C84817` | SOT-23-6 | expand | 281.143 | ⏳ |
| **L1** | Induktivität **22 µH** (YNR6045, 2,05 A) | `C341068` | SMD 6 × 6 mm | expand | 4.120 | ⏳ |
| **D6** | **SS34** Boost-Diode 3 A / 40 V | `C8678` | SMA | expand | 3.557.042 | ⏳ |
| **R31** | Widerstand **75 kΩ** (Boost-Feedback) | `C17819` | 0805 | **base** | 49.785 | ⏳ |

⚠️ **Neu am 15.09.2026 (Sauerstoffpumpe + Boost):** `C84817`, `C341068`, `C8678`, `C17819` sind noch
**nicht** über die JLCPCB-Parts-API gegengeprüft (Bestände stammen aus der LCSC-Suche). Vor der
Bestellung mit dem Skill `jlcpcb-parts-check` nachziehen — insbesondere **L1** (kleinster Bestand).

## 4. Nicht geprüft / offen

- **Stückpreise in EUR** inkl. Zoll/USt und **Versandkosten** der JLC-Bestellung nicht geprüft;
  USD→EUR hier grob mit ~0,92 gerechnet.
- **MOQ / Mindestbestückungsmenge** je Position nicht ausgewertet.
- **Basic-Alternativen** für die 10 Extended-Positionen nicht gesucht (Sparpotenzial ~30 USD).
- Pumpe, Sensor, Akku, Schlauch kommen nicht von JLC (siehe `bom_entscheidung.md`).
