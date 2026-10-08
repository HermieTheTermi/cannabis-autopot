# To-Do-Liste: PCB-Autorouting, Neck-Down & Designregeln (EasyEDA)

Stand: **Oktober 2026** · Projekt: **SmartGrowTopf_V1 (2S-Architektur)**  
Zugehörige Dokumente:
* [`docs/10_pcb-leiterbahnbreiten.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/docs/10_pcb-leiterbahnbreiten.md) (Berechnungsgrundlagen nach IPC-2221A)
* [`docs/11_review-2s-umbau.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/docs/11_review-2s-umbau.md) (2S-Strom- und Leistungsanalyse)
* [`hardware/schaltplan_v1.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/hardware/schaltplan_v1.md) (Schaltplan und Pin-Belegung)
* [`hardware/easyeda/scripts/pcb_widths.py`](file:///c:/Users/mgasc/Documents/cannabis-autopot/hardware/easyeda/scripts/pcb_widths.py) (Prüfskript für Leiterbahnbreiten)

---

## 1. Übersicht der Designregeln & Leiterbahnbreiten

Basierend auf **1 oz Kupfer (35 µm)** Außenlage bei JLCPCB (Standardprozess ohne Aufpreis):

| Netz / Funktion | Sollbreite | Minimalbreite (Neck-Down) | Max. Strom | Grund & Besonderheit |
|---|---|---|---|---|
| **VBAT / PACK_PLUS** | **≥ 1,00 mm** (40 mil) bzw. **Fläche** | 0,50 mm (nur direkt am Pad) | **~2,8 A** | Speist 5V-Buck für 3-A-Pumpenanlauf. Dünnere Bahnen führen zu >45 K Erwärmung und Brownout! |
| **+5V** (Pumpenschiene) | **≥ 1,00 mm** (40 mil) bzw. **Fläche** | 0,50 mm | **3,0 A** | Anlaufstrom der CONQUERALL-Pumpe. Von U_BUCK5 zu C3, Q1, Q3, J4, J16. |
| **PUMP_N / PUMP2_N** | **0,50 mm** (20 mil) | 0,40 mm | 3,0 A (Puls) / 0,6 A Dauer | Geschalteter Rückweg (MOSFET Drain → J4/J16). **Achtung:** EasyEDA stuft dies fälschlich als Signal ein! |
| **VBUS** (USB 5 V) | **0,60 – 0,80 mm** | 0,50 mm | **~1,6 A** | Ladeeingangsstrom des IP2326 (lädt 2S-Pack mit 0,90 A @ 8,4 V). |
| **+3V3** (Logik-Rail) | **0,40 mm** (16 mil) | 0,25 mm | 0,50 A (382 mA TX-Peak) | Vom AP63203-Buck zum ESP32-C6-Modul. |
| **VCC_EXT** | **0,50 mm** (20 mil) | 0,25 mm | ~0,10 A | Geschaltete Sensorversorgung (Q2 → J8/J9–J15), bewusst mit Sicherheitsreserve. |
| **GND / BAT_MINUS** | **Kupferfläche (Pour)** | Kurze Stiche ≥ 0,50 mm | bis 2,8 A | Durchgehende Massefläche auf Unterseite (Bottom Layer). Keine langen Einzelleiterbahnen! |
| **USB_DP / USB_DM** | **0,25 mm** (10 mil) | 0,15 mm | Signale | Differentielles Paar (12 Mbit/s), parallel, gleiche Länge, keine Layer-Splits queren. |
| **Alle Signale** (I²C, ADC, GPIOs, LEDs) | **0,25 mm** (10 mil) | 0,15 mm | < 20 mA | Standardleiterbahn für Steuersignale. |

### JLCPCB Standard-Fertigungsgrenzen (2-Lagen)
- **Minimale Leiterbahnbreite / Abstand:** `0,127 mm` (5 mil) – wir nutzen 0,25 mm für Signale (robuste Fertigung).
- **Via-Bohrung / Pad:** `0,30 mm Drill / 0,60 mm Pad` (Standard).
- **Clearance (Abstand Leiterbahn zu Leiterbahn / Pad):** `0,20 mm` (empfohlen), mindestens `0,15 mm`.

---

## 2. Das Neck-Down-Verfahren (Leiterbahnverjüngung)

### Warum ist Neck-Down notwendig?
Beim Autorouting oder manuellem Routing versucht das CAD-System, z. B. eine 1,0-mm-Bahn an ein Pinpad eines Bauteils anzuschließen. Bei Feinpitch-Komponenten (wie dem IP2326 im QFN-24 mit nur **0,5 mm Padabstand** und **0,25 mm Padbreite**) führt das zu sofortigen DRC-Clearance-Fehlern oder der Autorouter bricht ab.

### Neck-Down-Regeln für kritische Bauteile:

1. **U_CHG (IP2326 – VQFN-24 4×4 mm, Pitch 0,5 mm):**
   * **VOUT (Pins 21 & 22) an VBAT:** Beide Nachbarpins mit einer gemeinsamen Leiterbahn von ca. **0,6 – 0,7 mm** Breite anfahren. Sofort nach Verlassen des IC-Körpers (ca. 0,5 mm Abstand) auf **1,0 mm** erweitern oder in die VBAT-Kupferfläche übergehen lassen.
   * **LX (Pins 15, 16, 17) an L1:** Alle 3 Pins gemeinsam mit einer kurzen Kupferbrücke/Fläche direkt an das Pad der Ladeinduktivität L1 führen.
   * **VSYS (Pins 19 & 20):** Als Zweierpaar direkt auf die Pads von `C_VSYS_A` und `C_VSYS_B` (22 µF) legen.
   * **EPAD (Thermal Pad in der Mitte):**
     * Bildet die Masseverbindung und Hauptkühlung.
     * **Zwingend 4 bis 6 Thermal Vias (0,3 mm Bohrung)** im EPAD direkt auf die untere GND-Fläche platzieren.
     * Keine dünne Leiterbahn an das EPAD anschließen, sondern Vias setzen!

2. **MOSFETs (AO3400A / AO3401A – SOT-23):**
   * Drain- und Source-Pads haben ca. 0,6 mm Breite.
   * 1,0-mm-Bahnen (+5V, VBAT) ca. 0,5–1,0 mm vor dem Pad auf **0,50 mm** verjüngen.

3. **Buck-Wandler (SY8113B TSOT-23-6 & AP63203 TSOT-26):**
   * Eingangs- und Ausgangspins auf kürzestem Weg mit kurzem 0,5-mm-Stutzen an die Kondensatoren (`C_B5_IN`, `C3`) führen, dort sofort zur vollen Breite / Fläche aufweiten.

---

## 3. Konfiguration des Auto-Routers in EasyEDA (Schritt für Schritt)

Damit der Auto-Router von EasyEDA die unterschiedlichen Breiten versteht und nicht am 0,5-mm-Pitch des QFN-24 scheitert, muss er wie folgt eingerichtet werden:

### 3.1 Design Rules (Netzklassen) vorab anlegen
1. Im Menü auf **`Design` → `Design Rule...`** (oder Tab *Net Class* im Rule Manager) klicken.
2. Drei Klassen mit folgenden Parametern anlegen und die Netze zuweisen:
   * **Klasse `HIGH_CURRENT`:**
     - Netze: `VBAT`, `PACK_PLUS`, `+5V`
     - Track Width: `1.00 mm` (40 mil) | Min: `0.50 mm` | Max: `2.00 mm`
     - Clearance: `0.25 mm`
     - Via Hole: `0.40 mm` | Via Diameter: `0.80 mm`
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

### 3.2 Der „Fan-Out / Stub“-Trick: Neck-Down für den Auto-Router vorbereiten
> [!IMPORTANT]
> **Warum scheitert der Auto-Router sonst?**  
> Der Auto-Router versucht stur, mit der vorgegebenen 1,0-mm-Bahn bis an das Pinpad zu fahren. Beim IP2326 (QFN-24 mit nur 0,25 mm Padabstand) verletzt eine 1,0-mm-Bahn sofort die Abstandsregeln (Clearance) zu den Nachbarpins. Der Router bricht ab oder meldet ein ungeroutetes Netz.

**Die Lösung vor dem Router-Start (5 Minuten Vorarbeit):**
1. **Stubs (kurze Ausfädelungen) manuell zeichnen:**
   - Am **IP2326 (`U_CHG`)**: Von den Nachbarpins **21 & 22** (VOUT/VBAT) gemeinsam mit einer 0,5 mm breiten Bahn ca. 0,8 mm gerade vom Gehäuse wegziehen.
   - An den **TSOT- und SOT-23-Leistungspins** (MOSFETs Q1/Q3, Buck-Regler): Jeweils mit 0,5 mm ein kurzes Stück (ca. 0,5–1 mm) aus dem Pad herausführen.
2. **Stubs sperren (`Lock`):**
   - Die gezeichneten kurzen Stummel markieren und im rechten Eigenschaften-Panel auf **`Locked: Yes`** setzen.
3. **USB-Paar und Thermal Vias sperren:**
   - Das differenzielle Paar `USB_DP` / `USB_DM` manuell mit 0,25 mm verlegen und sperren.
   - Die 4–6 Thermal Vias im EPAD des IP2326 platzieren und sperren.

---

### 3.3 Auto-Router-Dialog konfigurieren
1. Menü öffnen: **`Route` → `Auto Router...`**
2. **General Settings konfigurieren:**
   - **Routing Layers:** Nur `TopLayer` und `BottomLayer` aktivieren (2-Lagen-Board).
   - **Track Width:** `0.25 mm` (als Basis für nicht zugewiesene Netze).
   - **Clearance:** `0.20 mm`.
   - **Via Diameter:** `0.60 mm` | **Via Hole Size:** `0.30 mm`.
3. **Wichtigste Optionen für das Vor-Routing aktivieren:**
   - [x] **`Skip Pre-routed Tracks` / `Ignore Frozen Tracks`** aktivieren!  
     *(Dadurch rührt der Auto-Router die gesperrten Neck-Down-Stubs, das USB-Paar und die Thermal Vias nicht an, sondern dockt mit der vollen Klassenbreite direkt daran an!)*
   - [x] **`Remove Loops`** aktivieren.
4. **Router-Auswahl:**
   - **Local Router** (lokaler Server via Plugin) ist stabiler und erlaubt höhere Ripup-Zyklen.
   - Falls nicht installiert: **Cloud Router** wählen (Routing Priority für `HIGH_CURRENT` auf Hoch/Priorität 1 stellen).
5. Auf **`Run`** klicken und warten, bis 100 % Complete erreicht ist.

---

## 4. To-Do-Liste für das PCB-Autorouting

### Phase A: Vorbereitung (Vor dem Autorouting)
- [ ] **A.1 Netzliste aktualisieren:** Sicherstellen, dass die aktuelle 2S-Netzliste (68 Netze) in EasyEDA importiert ist.
- [ ] **A.2 Board-Outline & Wulst-Maße festlegen:** Platinenabmessungen gemäß Gehäusevorgabe prüfen (max. 38 mm Breite im Wulst).
- [ ] **A.3 Antennen-Keepout zwingend setzen:**
  - Unter und um die PCB-Antenne des ESP32-C6-MINI-1 muss **in allen Lagen absolutes Kupferverbot (Keepout)** herrschen.
  - Mindestens 15 mm Abstand zu leitenden Teilen nach oben/außen einhalten.
- [ ] **A.4 Manuelle Platzierung der Schlüsselbauteile fixieren:**
  - [ ] USB-C-Buchse `J5` an der Gehäusekante ausrichten.
  - [ ] ESP32-C6-MINI-1 ganz oben positionieren (Antenne nach außen).
  - [ ] `U_CHG` (IP2326) samt Spule L1 und Kondensatoren kompakt zusammenhalten.
  - [ ] `U_BUCK5` und `U_BUCK3` nahe an `VBAT` und ihren Ausgangs-Elkos/Kondensatoren platzieren.
  - [ ] Stecker `J1` (Akku), `J4`/`J16` (Pumpen), `J18` (NTC) am Platinenrand platzieren.
  - [ ] Bauteile sperren (`Lock Component`).
- [ ] **A.5 Masseverbindung & Thermal Vias manuell setzen:**
  - [ ] 4–6 Vias im EPAD von `U_CHG` (IP2326) platzieren.
  - [ ] Massepads der Buck-Regler und Schaltkreise mit Vias direkt zur Bottom-Layer vorsehen.
- [ ] **A.6 Differentielles Paar routen & sperren:**
  - [ ] `USB_DP` und `USB_DM` manuell als 0,25-mm-Paar, parallel und längengleich vom USB-C-Port zum ESP32-C6 (GPIO12/13) verlegen.
  - [ ] Bahnen sperren (`Lock Track`).
- [ ] **A.7 Neck-Down-Stubs vorab zeichnen & sperren:**
  - [ ] Pins 21 & 22 am IP2326 mit 0,5 mm Stub herausziehen und sperren (`Locked: Yes`).
  - [ ] Pins an Q1, Q3, U_BUCK5 mit 0,5 mm Stub herausführen und sperren.

---

### Phase B: Netzklassen & Designregeln in EasyEDA konfigurieren
- [ ] **B.1 Netzklasse `HIGH_CURRENT` anlegen:**
  - Netze: `VBAT`, `PACK_PLUS`, `+5V`.
  - Default Track Width: **1,00 mm** (40 mil) | Clearance: `0,25 mm`.
- [ ] **B.2 Netzklasse `POWER_MEDIUM` anlegen:**
  - Netze: `VBUS`, `PUMP_N`, `PUMP2_N`, `VCC_EXT`, `+3V3`.
  - Default Track Width: **0,50 mm** (20 mil) | Clearance: `0,20 mm`.
- [ ] **B.3 Netzklasse `DEFAULT` / `SIGNAL` prüfen:**
  - Default Track Width: **0,25 mm** (10 mil) | Clearance: `0,20 mm`.
- [ ] **B.4 Spezielle Router-Ausnahme für PUMP_N prüfen:**
  - Verifizieren, dass `PUMP_N` und `PUMP2_N` **nicht** als 0,25-mm-Signalbahn geroutet werden, sondern in `POWER_MEDIUM` liegen!

---

### Phase C: Autorouting durchführen
- [ ] **C.1 Vias-Einstellungen im Router-Dialog prüfen:**
  - Drill: `0,30 mm` / Pad: `0,60 mm`.
- [ ] **C.2 Schutz-Optionen aktivieren:**
  - `Skip Pre-routed / Frozen Tracks`: **AKTIVIERT**.
- [ ] **C.3 Autorouter starten:**
  - Lokalen oder Cloud-Router starten und warten bis Abschluss.
- [ ] **C.4 100% Routing-Erfolg kontrollieren:** Keine ungerouteten Netze (0 Unrouted Nets).

---

### Phase D: Nachbereitung & Neck-Down Manuell Anpassen (Post-Routing)
- [ ] **D.1 Neck-Down-Übergänge glätten:**
  - Die Übergänge von den gesperrten Stubs zu den 1,0-mm-Bahnen auf harmonische 45°-Übergänge prüfen.
  - Pins 19 & 20 (VSYS) und Pins 15–17 (LX) am IP2326 auf maximale Breite zu Spule/Kondensatoren nachziehen.
- [ ] **D.2 Masseflächen fluten (Copper Pour):**
  - Unterseite (Bottom Layer): Vollflächiges `GND`-Polygon gießen.
  - Oberseite (Top Layer): Freie Flächen ebenfalls mit `GND` füllen.
  - Unverbundene Inseln (Dead Copper) entfernen oder mit GND-Vias anbinden.
- [ ] **D.3 Teardrops aktivieren:**
  - In EasyEDA *Tools → Teardrop* auf alle Pads und Vias anwenden (erhöht die mechanische und elektrische Zuverlässigkeit).
- [ ] **D.4 Winkel kontrollieren:**
  - Keine spitzen Winkel (< 90°) im Leistungspfad belassen (nur 45° oder Rundungen).

---

### Phase E: Verifikation & Abnahme (Definition of Done)
- [ ] **E.1 EasyEDA DRC (Design Rule Check):**
  - `DRC Check` im Editor ausführen → **0 Fehler**, **0 Kurzschlüsse**, **0 Abstandsverletzungen**.
- [ ] **E.2 Leiterbahnbreiten-Prüfung per Skript:**
  - Skript im Terminal ausführen:
    ```bash
    python hardware/easyeda/scripts/pcb_widths.py --check
    ```
  - Muss Exit 0 zurückgeben (keine unzulässig dünnen Leistungsbahnen).
- [ ] **E.3 Sichtprüfung Antennenbereich:**
  - Keine Leiterbahnen, keine Massefläche auf mindestens 15 mm um die ESP32-C6-Antenne.
- [ ] **E.4 Polung & Stecker prüfen:**
  - J1 (Akku 2S: 1 = BAT-, 2 = MID, 3 = BAT+).
  - J4/J16 (Pumpen), J5 (USB-C), C3 (Elko-Polarität).

