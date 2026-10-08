# To-Do-Liste: PCB-Autorouting, Neck-Down & Designregeln (EasyEDA – 4 Lagen)

Stand: **Oktober 2026** · Projekt: **SmartGrowTopf_V1 (2S-Architektur, 4-Layer-Board)**  
Zugehörige Dokumente:
* [`docs/10_pcb-leiterbahnbreiten.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/docs/10_pcb-leiterbahnbreiten.md) (Berechnungsgrundlagen nach IPC-2221A)
* [`docs/11_review-2s-umbau.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/docs/11_review-2s-umbau.md) (2S-Strom- und Leistungsanalyse)
* [`hardware/schaltplan_v1.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/hardware/schaltplan_v1.md) (Schaltplan und Pin-Belegung)
* [`hardware/easyeda/scripts/pcb_widths.py`](file:///c:/Users/mgasc/Documents/cannabis-autopot/hardware/easyeda/scripts/pcb_widths.py) (Prüfskript für Leiterbahnbreiten)

---

## 1. Das 4-Lagen-Schichtenmodell (JLCPCB Standard-Stackup JLC04161H)

Durch die Umstellung auf **4 Lagen** profitiert das Design von einer durchgehenden Massefläche, exzellenter Entwärmung und sauberer Signalintegrität:

* **Layer 1 (TopLayer, 1 oz / 35 µm):**  
  Bauteile, ESP32-C6-Antenne, HF-Leitungen, differentielle Signale (`USB_DP`/`USB_DM`), lokale Leistungsflächen (für direkte, niederohmige Verbindungen ohne Vias).
* **Layer 2 (Inner1 – Solide GND Plane, 0.5 oz / 17.5 µm):**  
  **100 % durchgehende Massefläche.** Keine Signalleiterbahnen hier durchrouten! Dient als niederinduktiver Rückstrompfad und direkte Wärmesenke für das EPAD des IP2326.  
  *(⚠️ Ausnahme: Absolutes Keepout unter der ESP32-C6-Antenne!)*
* **Layer 3 (Inner2 – Power Plane / Split Plane, 0.5 oz / 17.5 µm):**  
  Stromversorgungen als Flächen/Polygone (`VBAT`, `+5V`, `+3V3`) und kreuzungsfreie Signalüberquerungen.
* **Layer 4 (BottomLayer, 1 oz / 35 µm):**  
  Zusätzliche Signale, Testpunkte, rückseitige Kühl- und GND-Flächen.

---

## 2. Übersicht der Designregeln & Leiterbahnbreiten

> [!IMPORTANT]
> **Thermische Besonderheit bei 4 Lagen (IPC-2221A):**  
> Innenlagen (Inner1 / Inner2) kühlen im Epoxidharz schlechter ab als Außenlagen ($k = 0{,}024$ innen vs. $k = 0{,}048$ außen).  
> **Leistungspfade (`VBAT`, `+5V`) mit 2,8–3 A daher bevorzugt auf Layer 1 (Top) führen ODER auf Layer 3 als breite Kupferfläche (Polygon Pour) anlegen!**

| Netz / Funktion | Sollbreite (Außenlage) | Min. (Neck-Down) | Max. Strom | Lage & Routing-Vorgabe |
|---|---|---|---|---|
| **VBAT / PACK_PLUS** | **≥ 1,00 mm** (40 mil) bzw. **Fläche** | 0,50 mm (nur am Pad) | **~2,8 A** | TopLayer (1 oz) oder Layer 3 als Fläche. Speist den 5V-Buck für 3-A-Pumpenanlauf. |
| **+5V** (Pumpenschiene) | **≥ 1,00 mm** (40 mil) bzw. **Fläche** | 0,50 mm | **3,0 A** | TopLayer direkt zu C3, Q1, Q3, J4, J16. Deckt den Motoranlauf ab. |
| **PUMP_N / PUMP2_N** | **0,50 mm** (20 mil) | 0,40 mm | 3,0 A (Puls) / 0,6 A Dauer | TopLayer. Drain von Q1/Q3 → J4/J16. (Nicht als simples Signal routen!). |
| **VBUS** (USB 5 V) | **0,60 – 0,80 mm** | 0,50 mm | **~1,6 A** | Ladeeingangsstrom zu IP2326 Pin 13. |
| **+3V3** (Logik-Rail) | **0,40 mm** (16 mil) | 0,25 mm | 0,50 A (382 mA TX-Peak) | Vom AP63203-Buck zum ESP32-C6-Modul (Layer 1 oder Layer 3). |
| **VCC_EXT** | **0,50 mm** (20 mil) | 0,25 mm | ~0,10 A | Geschaltete Sensorversorgung (Q2 → J8/J9–J15). |
| **GND** | **Solide Ebene (Layer 2)** | Vias direkt ins Pad | bis 3 A | Layer 2 als Plane. Kurze Stiche/Vias direkt an die Pads (keine Leiterschleifen). |
| **USB_DP / USB_DM** | **0,23 mm / 0,20 mm Gap** | 0,15 mm | 12 Mbit/s FS | **90 Ω diff. Impedanz** mit Layer 2 (GND) als Referenz! Parallel und symmetrisch. |
| **Signale** (I²C, ADC, GPIOs) | **0,25 mm** (10 mil) | 0,15 mm | < 20 mA | Layer 1 oder Layer 4. |

### JLCPCB 4-Lagen Standardparameter
- **Min. Trace / Spacing:** `0,127 mm` (5 mil) – wir nutzen 0,25 mm für maximale Prozesssicherheit.
- **Via-Bohrung / Pad:** `0,30 mm Drill / 0,60 mm Pad`.
- **Clearance (Abstand):** `0,20 mm` (empfohlen), minimal `0,15 mm`.

---

## 3. Das Neck-Down-Verfahren (Leiterbahnverjüngung)

### Warum ist Neck-Down auch bei 4 Lagen zwingend?
Feinpitch-Bauteile wie der **IP2326 im QFN-24 (4×4 mm)** haben einen Pin-Mittenabstand (Pitch) von nur **0,50 mm** und Padbreiten von **0,25 mm**. Eine 1,0-mm-Leiterbahn kann dort physikalisch nicht direkt an ein einzelnes Pad andocken, ohne benachbarte Pins kurzzuschließen.

### Neck-Down-Regeln für kritische Bauteile:

1. **U_CHG (IP2326 – VQFN-24 4×4 mm, Pitch 0,5 mm):**
   * **VOUT (Pins 21 & 22) an VBAT:** Beide Nachbarpins gemeinsam mit einer ca. **0,6 – 0,7 mm** breiten Leiterbahn anfahren. Nach $\le 0,8\text{ mm}$ Abstand zum Chip sofort auf die volle 1,0 mm Breite bzw. Kupferfläche aufweiten.
   * **LX (Pins 15, 16, 17) an L1:** Alle 3 Pins gemeinsam mit einer breiten Polygonbrücke direkt an das Pad der Speicherinduktivität L1 führen.
   * **VSYS (Pins 19 & 20):** Als 2er-Block direkt auf die Pads von `C_VSYS_A` und `C_VSYS_B` (22 µF) legen.
   * **EPAD (Thermal Pad in der Mitte):**
     * Bildet die Hauptmasse und Wärmeabfuhr des Laders.
     * **4 bis 6 Thermal Vias (0,3 mm Bohrung / 0,6 mm Pad)** direkt im EPAD platzieren, die unmittelbar in die **Layer 2 GND-Plane** eintauchen!

2. **MOSFETs (AO3400A / AO3401A – SOT-23):**
   * Drain- und Source-Pads haben ca. 0,6 mm Breite.
   * 1,0-mm-Bahnen (+5V, VBAT) ca. 0,5–1,0 mm vor dem Pad auf **0,50 mm** verjüngen.

3. **Buck-Wandler (SY8113B TSOT-23-6 & AP63203 TSOT-26):**
   * Eingangs- und Ausgangspins auf kürzestem Weg mit kurzem 0,5-mm-Stutzen an die Kondensatoren (`C_B5_IN`, `C3`) führen, dort sofort zur vollen Breite / Fläche aufweiten.

---

## 4. Konfiguration des Auto-Routers in EasyEDA (4 Lagen)

### 4.1 Lagen-Setup im PCB-Editor
1. Im Menü **`Design` → `Layer Manager...`** (oder Lagen-Leiste) auf **4 Layers** umstellen.
2. Lagen benennen und konfigurieren:
   * **TopLayer:** Signal / Component
   * **Inner1:** Plane / GND (Netz: `GND`)
   * **Inner2:** Signal / Power (für `+5V`, `VBAT`, `+3V3` oder Routing)
   * **BottomLayer:** Signal

---

### 4.2 Design Rules (Netzklassen) anlegen
Unter **`Design` → `Design Rule...`** (oder Rule Manager → *Net Class*):

* **Klasse `HIGH_CURRENT`:**
  - Netze: `VBAT`, `PACK_PLUS`, `+5V`
  - Track Width: `1.00 mm` (40 mil) | Min: `0.50 mm` | Max: `2.00 mm`
  - Clearance: `0.25 mm`
  - Via Hole: `0.35 mm` | Via Diameter: `0.70 mm`
* **Klasse `POWER_MEDIUM`:**
  - Netze: `VBUS`, `PUMP_N`, `PUMP2_N`, `VCC_EXT`, `+3V3`
  - Track Width: `0.50 mm` (20 mil) | Min: `0.35 mm` | Max: `0.80 mm`
  - Clearance: `0.20 mm`
  - Via Hole: `0.30 mm` | Via Diameter: `0.60 mm`
* **Klasse `DEFAULT` (Signale):**
  - Netze: Alle restlichen Netze (I²C, ADC, EN, BOOT, LEDs, etc.)
  - Track Width: `0.25 mm` (10 mil) | Min: `0.15 mm` | Max: `0.40 mm`
  - Clearance: `0.20 mm`
  - Via Hole: `0.30 mm` | Via Diameter: `0.60 mm`

---

### 4.3 Der „Fan-Out / Stub“-Trick: Vorarbeiten vor dem Router-Start
> [!IMPORTANT]
> **Warum scheitert der Auto-Router sonst?**  
> Der Auto-Router versucht stur, mit 1,0 mm Breite an die 0,25 mm breiten Pins des IP2326 heranzufahren. Das verletzt sofort die Abstandsregeln zu den Nachbarpins. Der Router bricht ab.

**5 Minuten Vorbereitung vor dem Router-Start:**
1. **Stubs (kurze Ausfädelungen) manuell zeichnen:**
   - Am **IP2326 (`U_CHG`)**: Von den Nachbarpins **21 & 22** (VOUT/VBAT) gemeinsam mit einer 0,5 mm breiten Bahn ca. 0,8 mm gerade vom Gehäuse wegziehen.
   - An den **TSOT- und SOT-23-Leistungspins** (MOSFETs Q1/Q3, Buck-Regler): Jeweils mit 0,5 mm ein kurzes Stück (ca. 0,5–1 mm) aus dem Pad herausführen.
2. **Stubs sperren (`Lock`):**
   - Die gezeichneten kurzen Stummel markieren und im Eigenschaften-Panel auf **`Locked: Yes`** setzen.
3. **USB-Paar und Thermal Vias sperren:**
   - `USB_DP` / `USB_DM` manuell auf TopLayer verlegen (0,23 mm Breite, 0,20 mm Abstand, Referenz Layer 2) und sperren (`Locked: Yes`).
   - Die 4–6 Thermal Vias im EPAD des IP2326 setzen und sperren.

---

### 4.4 Auto-Router-Dialog konfigurieren
1. Menü öffnen: **`Route` → `Auto Router...`**
2. **General Settings:**
   * **Routing Layers:** Aktivieren: `TopLayer`, `BottomLayer` (und optional `Inner2`, falls Signale innen kreuzen sollen).  
     *(⚠️ `Inner1` bleibt deaktiviert, da dies die reine GND-Plane ist!)*
   * **General Track Width:** `0.25 mm`.
   * **General Clearance:** `0.20 mm`.
   * **Via Diameter:** `0.60 mm` | **Via Hole:** `0.30 mm`.
3. **Wichtigste Optionen:**
   * [x] **`Skip Pre-routed Tracks` / `Ignore Frozen Tracks`** aktivieren!  
     *(Dadurch dockt der Auto-Router an die gesperrten Stubs und Vias an, ohne sie zu verändern).*
   * [x] **`Remove Loops`** aktivieren.
4. **Router starten:** Auf **`Run`** klicken und 100 % Complete abwarten.

---

## 5. To-Do-Liste für das PCB-Autorouting (Checkliste)

### Phase A: Vorbereitung (Vor dem Autorouting)
- [ ] **A.1 Netzliste aktualisieren:** Aktuelle 2S-Netzliste (68 Netze) in EasyEDA importieren.
- [ ] **A.2 Lagen auf 4 Layers umstellen:** `TopLayer`, `Inner1` (GND), `Inner2` (Power/Signal), `BottomLayer`.
- [ ] **A.3 Antennen-Keepout auf ALLEN 4 LAGEN setzen:**
  - Unter und um die PCB-Antenne des ESP32-C6-MINI-1 muss **auf allen 4 Lagen absolutes Kupferverbot (Keepout)** herrschen!
  - Keine GND-Fläche auf Layer 2 unter der Antenne! Mindestens 15 mm Freiraum in alle Richtungen.
- [ ] **A.4 Manuelle Platzierung fixieren & sperren:**
  - [ ] USB-C-Buchse `J5` an der Gehäusekante ausrichten.
  - [ ] ESP32-C6-MINI-1 ganz oben positionieren (Antenne zeigt nach außen/oben).
  - [ ] `U_CHG` (IP2326) samt Spule L1 und Kondensatoren kompakt zusammenhalten.
  - [ ] `U_BUCK5` und `U_BUCK3` nahe an `VBAT` platzieren.
  - [ ] Stecker `J1` (Akku), `J4`/`J16` (Pumpen), `J18` (NTC) am Platinenrand platzieren.
  - [ ] Bauteile sperren (`Lock Component`).
- [ ] **A.5 Masseverbindung & Thermal Vias manuell setzen:**
  - [ ] 4–6 Vias im EPAD von `U_CHG` (IP2326) direkt zur Layer 2 GND-Plane platzieren und sperren.
- [ ] **A.6 Differentielles USB-Paar manuell routen & sperren:**
  - [ ] `USB_DP` und `USB_DM` auf TopLayer verlegen (0,23 mm Bahn, 0,20 mm Abstand, parallel, längengleich) und sperren (`Locked: Yes`).
- [ ] **A.7 Neck-Down-Stubs vorab zeichnen & sperren:**
  - [ ] Pins 21 & 22 am IP2326 mit 0,5 mm Stub herausziehen und sperren (`Locked: Yes`).
  - [ ] Pins an Q1, Q3, U_BUCK5 mit 0,5 mm Stub herausführen und sperren.

---

### Phase B: Netzklassen & Designregeln konfigurieren
- [ ] **B.1 Netzklasse `HIGH_CURRENT` anlegen:**
  - Netze: `VBAT`, `PACK_PLUS`, `+5V`.
  - Default Track Width: **1,00 mm** (40 mil) | Clearance: `0,25 mm`.
- [ ] **B.2 Netzklasse `POWER_MEDIUM` anlegen:**
  - Netze: `VBUS`, `PUMP_N`, `PUMP2_N`, `VCC_EXT`, `+3V3`.
  - Default Track Width: **0,50 mm** (20 mil) | Clearance: `0,20 mm`.
- [ ] **B.3 Netzklasse `DEFAULT` / `SIGNAL` prüfen:**
  - Default Track Width: **0,25 mm** (10 mil) | Clearance: `0,20 mm`.
- [ ] **B.4 Spezielle Router-Ausnahme für PUMP_N prüfen:**
  - Verifizieren, dass `PUMP_N` und `PUMP2_N` in `POWER_MEDIUM` (0,50 mm) liegen und nicht als 0,25-mm-Signal geroutet werden.

---

### Phase C: Autorouting durchführen
- [ ] **C.1 Routing Layers prüfen:**
  - `TopLayer` und `BottomLayer` (optional `Inner2`) aktiv. `Inner1` (GND) inaktiv.
- [ ] **C.2 Schutz-Optionen aktivieren:**
  - `Skip Pre-routed / Frozen Tracks`: **AKTIVIERT**.
- [ ] **C.3 Autorouter starten:** Lokalen oder Cloud-Router starten bis 100 % Complete.
- [ ] **C.4 Routing-Erfolg kontrollieren:** Keine ungerouteten Netze (0 Unrouted Nets).

---

### Phase D: Nachbereitung & Flächen fluten (Post-Routing)
- [ ] **D.1 Neck-Down-Übergänge glätten:**
  - Übergänge von den Stubs zu den 1,0-mm-Bahnen auf saubere 45°-Winkel prüfen.
  - Pins 19 & 20 (VSYS) und Pins 15–17 (LX) am IP2326 vollflächig an L1 / Kondensatoren anbinden.
- [ ] **D.2 Kupferflächen fluten (Copper Pour):**
  - **Layer 2 (Inner1):** Als durchgehende `GND`-Plane fluten (Keepout an der Antenne beachten!).
  - **Layer 3 (Inner2):** Falls für Power genutzt: Polygone für `VBAT` / `+5V` / `+3V3` gießen.
  - **Layer 1 & Layer 4:** Restflächen mit `GND` füllen.
  - Inseln ohne Verbindung (Dead Copper) entfernen oder via Via-Stitching an die GND-Plane tackern.
- [ ] **D.3 Teardrops aktivieren:**
  - In EasyEDA *Tools → Teardrop* auf alle Pads und Vias anwenden.
- [ ] **D.4 45°-Winkel kontrollieren:**
  - Keine spitzen Winkel (< 90°) im Leistungspfad belassen.

---

### Phase E: Verifikation & Abnahme (Definition of Done)
- [ ] **E.1 EasyEDA DRC (Design Rule Check):**
  - `DRC Check` ausführen → **0 Fehler**, **0 Kurzschlüsse**, **0 Abstandsverletzungen**.
- [ ] **E.2 Leiterbahnbreiten-Prüfung per Skript:**
  - Skript im Terminal ausführen:
    ```bash
    python hardware/easyeda/scripts/pcb_widths.py --check
    ```
  - Muss Exit 0 liefern (keine unzulässig dünnen Leistungsbahnen).
- [ ] **E.3 Sichtprüfung Antennenbereich (ALLE 4 LAGEN):**
  - Antenne des ESP32-C6 ist auf Layer 1, 2, 3 und 4 **zu 100 % kupferfrei**.
- [ ] **E.4 Polung & Stecker prüfen:**
  - J1 (Akku 2S: 1 = BAT-, 2 = MID, 3 = BAT+).
  - J4/J16 (Pumpen), J5 (USB-C), C3 (Elko-Polarität).
