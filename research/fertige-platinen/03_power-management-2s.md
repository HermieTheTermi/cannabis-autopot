# 03 — Fertige Stromversorgungs-Platinen/Module für 2S-LiIon (Laden + Balancing + Schutz + 5 V/3 A + 3,3 V/2 A)

**Stand:** 2026-10-09 · **Projekt:** cannabis-autopot · **Auftrag:** Gibt es ein FERTIGES Board statt der Eigenentwicklung (IP2326 + HY2120-CB)?
**Prüfliste:** 1) 2S-Laden 5 V USB-C → 8,4 V/~0,9 A · 2a) Zellschutz (OV 4,28 V / UV 2,90 V / Überstrom) · 2b) Passiv-Balancing · 3) 5 V/3 A Spitze · 4) 3,3 V/2 A · 5) UV-Wächter ~6,16 V Pack · 6) Ein/Aus + Ladestatus + µA-Schlaf.
**Ziel:** ≤ 54 × 80 mm, Module flach.
**Budget/Methode:** 12 Websuchen/-abrufe (ausgeschöpft). Preise nur von Produktseiten; sonst **unbelegt**.

---

## 0. Nachprüfung Hermes 09.10.2026 (Ergänzung zu diesem Report)

- **HX-2S-JH20 — Preis jetzt belegt:** **2,22 € netto/Stück** (1+), 1,69 € ab 5, 1,60 € ab 10 bei
  [hestore.eu (HU/EU)](https://www.hestore.eu/de/prod_10046818.html); laut Datenblattfeld zusätzlich
  **Balancer-IC HY2213-BB3A** (nicht nur HY2120-CB — Schutz und Balancing sind zwei Chips).
  Herstellerhinweis auf derselben Seite: *„BMS modules do not replace the charging circuits! The charging
  current is not regulated!"* → Schutz/Balancing-Modul und Lader bleiben zwei Bauteile.
- **⚠️ LaskaKit PD-IP2326 eingeschränkt:** Der Shop antwortet im Produkt-Q&A: *„tento modul vyžaduje PD
  zdroj s napětím 20V. Jiné varianty nebudou fungovat."* (Modul braucht eine **PD-Quelle mit 20 V**;
  andere Varianten funktionieren nicht.) Damit ist es für den **5-V-USB-C-Eingang des Projekts nicht
  geeignet**, obwohl derselbe IC (IP2326) auf der eigenen Platine sitzt. Preis 7,30 € (164 St. lagernd)
  bleibt korrekt.
- **Fehlende Klasse ergänzt:** billige **Type-C-2S-Boost-Lader** (5 V → 8,4 V, CC/CV, 1,1–2,2 A,
  **39 × 18 × 6,3 mm**, ~8–10 $ je 3 St.) — z. B. [Adeept](http://www.adeept.com/type-c-bms-2s-2a-18650-21700-37v-lithium-battery-charge-board-step-up-boost-li-po-polymer-usb-c-to-84v_p0374.html),
  [Amazon.com](https://www.amazon.com/Lithium-Battery-Charger-Step-up-Polymer/dp/B0BZC7TWC7).
  ⚠️ Zwei Einschränkungen aus Käuferberichten: funktioniert nur an **dummen 5-V-Quellen** (echte
  USB-C-PD-Netzteile verweigern), und Schutz/Balancing fehlen → Kombination mit HX-2S-JH20 nötig.
  **EU-Preis unbelegt.**

---

## VERDIKT

**NEIN** — kein einzelnes Fertigboard liefert 2S-Laden + Balancing + Schutz + 5 V/3 A in einem. **ABER:** Die projekteigene 2S-Versorgung (IP2326-Lader + externer HY2120-CB-Schutz) ist aus **zwei Fertigmodulen fast 1:1 nachbaubar**: (A) IP2326-2S-Lademodul (LaskaKit, **7,30 €** verifiziert) + (B) **HX-2S-JH20**-BMS (Schutz+Balancing) — dieses nutzt **dasselbe Schutz-IC HY2120-CB** wie die Eigenentwicklung und exakt deren Schwellen (OV 4,28 V / UV 2,9 V/Zelle). Fehlende Achsen (5 V/3 A, 3,3 V/2 A, µA-Aus-Schalter, **einstellbarer** 6,16-V-Wächter) kommen als Buck-Module bzw. bleiben diskret.

---

## Legende

| # | Achse | Kürzel |
|---|---|---|
| 1 | 2S-Laden 5 V→8,4 V (~0,9 A) | **Laden** |
| 2a | Zellschutz (OV/UV/Überstrom) | **Schutz** |
| 2b | Passiv-Balancing | **Bal.** |
| 3 | 5 V/3 A Spitze | **5V** |
| 4 | 3,3 V/2 A | **3V3** |
| 5 | UV-Wächter ~6,16 V Pack | **Wächter** |
| 6 | Ein/Aus + Ladestatus + µA | **μA/SW** |

---

## 1. Einzelne „All-in-One"-Boards

| Produkt | Preis | Zellen | Laden | Bal. | Schutz | Ausgänge (V/A) | Größe | fehlende Achsen | Link |
|---|---|---|---|---|---|---|---|---|---|
| **LaskaKit PD-IP2326** (IP2326) | **7,30 €** (verif.) | 2S/3S (DIP) | ✓ 5 V→8,4/12,6 V, CC/CV, LED | **✗ (ausdrücklich: „does not provide balancing")** | nur OV; **„no overcurrent and short circuit protection"** | — | unbelegt | Bal., Überstrom/SCP, 5V, 3V3, Wächter, μA/SW | https://www.laskakit.cz/en/la123029 |
| Generisches **IP2326-2S-BMS-Modul** (15 W) | unbelegt | 2S/3S | ✓ 8,4 V, 1,5 A, QC | laut Shop ✓ („built-in balance charging") — **widersprüchlich zu LaskaKit** | laut Shop OVP/UVP/OCP/SCP/Timeout | — | unbelegt | 5V, 3V3, Wächter, μA/SW; Bal./Schutz unbelegt | https://electronics.com.bd/type-c-usb-2s-bms-15w · https://electrogearbd.com/product/13110 |
| **Waveshare Solar Power Manager (D)** | unbelegt | **nur 1S (3,7 V)** | ✓ (Solar/Type-C) | n/a (1S) | „over-charge/discharge/overheat/over-current/short" | **5 V/3 A ✓**, PD/QC-Protokolle | unbelegt | 2S, Bal., 3V3, Wächter, μA/SW | https://www.waveshare.com/product/solar-power-manager-d.htm |
| Waveshare Solar Power Manager (B) | unbelegt | 1S (10000 mAh eingebaut) | ✓ | n/a | ✓ mehrfach | 5 V (I max unbelegt) | unbelegt | 2S, 3V3, Wächter | https://www.waveshare.com/product/solar-power-manager-b.htm |

**Fazit Abschnitt 1:** Kein Board erfüllt alle Achsen. Waveshare (D) ist das einzige mit **5 V/3 A**, aber nur 1S. IP2326-Module liefern nur Laden (Balancing strittig).

---

## 2. „UPS"- / Powerbank- / Solar-Power-Manager-Module

| Produkt/Modul | Preis | Zellen | Laden | Bal. | Schutz | Ausgänge (V/A) | Größe | fehlende Achsen | Link |
|---|---|---|---|---|---|---|---|---|---|
| **Waveshare Solar Power Manager (D)** | unbelegt | 1S | ✓ | n/a | ✓ | 5 V/3 A | unbelegt | 2S, Bal., 3V3, Wächter | s. o. |
| **Waveshare Solar Power Manager** (Basis) | unbelegt | 1S (3,7 V) | ✓ Solar/USB | n/a | ✓ | 5 V | unbelegt | 2S … | https://www.waveshare.com/solar-power-manager.htm |
| Waveshare SPM (B, 10000 mAh) | unbelegt | 1S | ✓ | n/a | ✓ mehrfach | 5 V | unbelegt | 2S, 3V3 | s. o. |
| Consumer-Powerbank mit USV/Pass-Through | — | 1S (intern, nicht zugänglich) | ✓ | n/a | ✓ | 5 V, typ. ~2–2,4 A (**unbelegt**) | — | kein 2S, kein Zugriff auf Pack/Bal., Ausgangsstrom unbelegt | – |
| DFRobot / Geekworm / Adafruit / Pololu UPS-Serie | unbelegt | **überwiegend 1S** | ✓ | n/a | ✓ | 5 V | — | kein 2S-Balancing; 3V3 nicht als separate 2-A-Schiene | (nicht einzeln belegt) |

**Fazit Abschnitt 2:** Die UPS/Solar-Manager-Klasse ist **durchweg 1S** (3,7 V) — genau wegen 1S braucht sie **kein Balancing**, kann aber die geforderte **2S-Topologie nicht** bedienen. Consumer-Powerbanks stellen kein zugängliches 2S-Pack bereit. Alle Achsen 2S/Bal. fehlen.

---

## 3. Baustein-Kombination aus fertigen Modulen

**Empfehlung = genau die Aufteilung der Eigenentwicklung, in Fertigmodulen:**

| Teil | Aufgabe | Produkt | Preis | Größe (mm) | Link |
|---|---|---|---|---|---|
| **A · Lader** | Laden 5 V→8,4 V (Achse 1) | IP2326-2S-Lademodul (**LaskaKit PD-IP2326**; 2S per DIP, µA-Standby, LED) | **7,30 €** verif. | unbelegt (~50×30) | https://www.laskakit.cz/en/la123029 |
| **B · Schutz+Balancing** | Achse 2a+2b | **HX-2S-JH20 BMS** (HY2120-CB; OV 4,28 V±0,05, UV 2,9 V±0,08/Zelle, 10 A / 20 A Puls, 2,5–9 µA) | unbelegt | **47,5 × 24 × 3,6** (verif.) | https://www.hestore.eu/en/prod_10046818.html |
| **C · 5-V-Schiene** | Achse 3 | **MINI560** Buck (in→5 V, 3 A) | unbelegt | ~22×17 (unbelegt) | https://www.amazon.de/-/en/Binghe-DC-DC-Regulator-Power-Module/dp/B0DJX9TNMT |
| **D · 3,3-V-Schiene** | Achse 4 | MINI560-3,3 V-Variante **oder** XIAO-ESP32-C6-eigener 3,3-V-Regler (Board nimmt 5 V) | unbelegt | ~22×17 (unbelegt) | https://www.amazon.de/-/en/Binghe-DC-DC-Regulator-Power-Module/dp/B0DJX9TNMT |

**Summe: ~8–15 € (nur A sicher belegt mit 7,30 €; B/C/D unbelegt), Fläche ~1.140 mm² belegt (HX-2S 47,5×24) + ~1.500 + 2×~370 mm² geschätzt ≈ ~3.400 mm²** (Schätzung, teils unbelegt). Passt flach unter die 54×80 mm (4.320 mm²).

**Nicht durch Fertigmodule gedeckt (bleibt Eigenanteil/diskret):**
- **Achse 5 · UV-Wächter 6,16 V:** HX-2S schaltet fest bei 2,9 V/Zelle = **5,8 V Pack** (nicht einstellbar, nicht 6,16 V) → Markt bietet hier **kein** passendes Fertigmodul; nur feste BMS-Schwellen.
- **Achse 6 · µA-Aus-Schalter + Ladestatus:** Lade-LED vorhanden (A), aber **kein µA-Hauptschalter** als Fertigmodul in Kombination; HX-2S-Ruhestrom allein 2,5–9 µA (verif.) — ein echten „Aus"-Schalter (Load-Switch/eFuse) müsste ergänzt werden.

**Wichtig:** IP2326-Modul A hat laut LaskaKit **kein Überstrom-/Kurzschluss-Schutz und kein Balancing** — beides übernimmt B (HX-2S-JH20). Genau so, wie im Projekt geplant (Schutz extern, nicht im Lader).

---

## 4. Zusammenfassung Lücken / Empfehlung

- **Ein Board für alles: nein.** Maximalleistung „ein Board": Waveshare SPM (D) mit 5 V/3 A — aber 1S.
- **2S-Kern (Laden + Schutz + Balancing) aus Fertigmodulen: ja.** IP2326-2S-Lader (LaskaKit) + HX-2S-JH20-BMS (HY2120-CB, identische Schwellen zur Eigenentwicklung).
- **Offene Achsen:** 5 V/3 A (MINI560-Buck), 3,3 V/2 A (MINI560-3,3 V **oder** XIAO-Regler), 6,16-V-einstellbarer Wächter (kein Fertigmodul — nur feste 5,8 V), µA-Aus-Schalter (diskret ergänzen).
- **Preisdisziplin:** Nur LaskaKit **7,30 €** direkt von Produktseite verifiziert; alle übrigen Preise **unbelegt** (Amazon.de/hestore blockten bzw. Budget erschöpft). HX-2S ist in DE u. a. als 5er-Pack bei https://zimmer-fewo.de/Li-Po-Li-Ion-Protection-Board-With-Balancer-Overcharge-r-753048 und https://www.doggysplayground.de/Board-7-4V-8-4V-Lithium-Battery-Charger-Module-With-Balance/615523 gelistet.
- **Nebenbefund:** Zwei Module (A+B) reproduzieren die Eigen-Platine fast 1:1 — wer trotzdem eine eigene Platine will (Platz/Wulst, µA-Schalter), hat mit HY2120-CB + IP2326 die exakt marktüblichen ICs.
