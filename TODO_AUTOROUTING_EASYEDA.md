# To-Do-Liste: PCB-Autorouting mit Freerouting & EasyEDA (4 Lagen)

Stand: **Oktober 2026** · Projekt: **SmartGrowTopf_V1 (2S-Architektur, 4-Layer-Board)**  
Zugehörige Dokumente & Skripte:
* [`docs/10_pcb-leiterbahnbreiten.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/docs/10_pcb-leiterbahnbreiten.md) (Berechnungsgrundlagen nach IPC-2221A)
* [`docs/11_review-2s-umbau.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/docs/11_review-2s-umbau.md) (2S-Strom- und Leistungsanalyse)
* [`hardware/schaltplan_v1.md`](file:///c:/Users/mgasc/Documents/cannabis-autopot/hardware/schaltplan_v1.md) (Schaltplan und Pin-Belegung)
* [`hardware/easyeda/scripts/pcb_widths.py`](file:///c:/Users/mgasc/Documents/cannabis-autopot/hardware/easyeda/scripts/pcb_widths.py) (Prüfskript für Leiterbahnbreiten)

---

## 1. Freerouting: Download & Installation

Freerouting ist ein fortschrittlicher, quelloffener Autorouter für Leiterplatten, der über das standardisierte Specctra-DSN/SES-Format nahtlos mit EasyEDA zusammenarbeitet.

* **Offizielle Releases (Downloads):**  
  👉 [https://github.com/freerouting/freerouting/releases](https://github.com/freerouting/freerouting/releases)
* **Offizielle Installationsanleitung & Dokumentation:**  
  👉 [https://freerouting.org/](https://freerouting.org/) bzw. [Freerouting GitHub Installation Guide](https://github.com/freerouting/freerouting#installation)

### Installations-Optionen:
1. **Option A (Empfohlen für Windows): Standalone Installer**  
   * Lade aus den [Releases](https://github.com/freerouting/freerouting/releases) die aktuelle Datei `Freerouting-X.X.X-windows-x64.msi` herunter.
   * Der Windows-Installer bringt eine vorkonfigurierte Java-Laufzeitumgebung direkt mit. Nach der Installation kann Freerouting direkt per Startmenü geöffnet werden.
2. **Option B: Plattformunabhängiges JAR**  
   * Falls Java (Version 17 oder 21+) bereits installiert ist: Lade die Datei `freerouting-executable.jar` herunter.
   * Start über das Terminal / die PowerShell:
     ```powershell
     java -jar freerouting-executable.jar
     ```

---

## 2. Das 4-Lagen-Schichtenmodell (JLCPCB JLC04161H)

* **Layer 1 (TopLayer, 1 oz / 35 µm):**  
  Bauteile, ESP32-C6-Antenne, differenzielles USB-Paar (`USB_DP`/`USB_DM`), lokale Leistungsbahnen/-flächen.
* **Layer 2 (Inner1 – Solide GND-Plane, 0.5 oz / 17.5 µm):**  
  **100 % durchgehende Massefläche.** Keine Signalbahnen hier durchrouten! Direkte Wärmesenke und HF-Rückstrompfad für das EPAD des IP2326.  
  *(⚠️ Ausnahme: Absolutes Keepout unter der ESP32-C6-Antenne!)*
* **Layer 3 (Inner2 – Power Plane / Split Plane, 0.5 oz / 17.5 µm):**  
  Versorgungsflächen (`VBAT`, `+5V`, `+3V3`) und kreuzungsfreie Signalüberquerungen.
* **Layer 4 (BottomLayer, 1 oz / 35 µm):**  
  Zusätzliche Signale, Testpunkte und rückseitige GND-Kühlflächen.

---

## 3. Übersicht der Designregeln & Leiterbahnbreiten

> [!IMPORTANT]
> **Thermische Besonderheit bei 4 Lagen (IPC-2221A):**  
> Innenlagen kühlen im Epoxidharz schlechter ab als Außenlagen ($k = 0{,}024$ innen vs. $k = 0{,}048$ außen).  
> **Leistungspfade (`VBAT`, `+5V`) mit 2,8–3 A daher bevorzugt auf Layer 1 (Top, 1 oz) führen ODER auf Layer 3 als breite Kupferfläche (Polygon Pour) anlegen!**

| Netz / Funktion | Sollbreite (Außenlage) | Min. (Neck-Down) | Max. Strom | Lage & Routing-Vorgabe |
|---|---|---|---|---|
| **VBAT / PACK_PLUS** | **≥ 1,00 mm** (40 mil) bzw. **Fläche** | 0,50 mm (nur am Pad) | **~2,8 A** | TopLayer (1 oz) oder Layer 3 als Fläche. Speist 5V-Buck für 3-A-Pumpenanlauf. |
| **+5V** (Pumpenschiene) | **≥ 1,00 mm** (40 mil) bzw. **Fläche** | 0,50 mm | **3,0 A** | TopLayer direkt zu C3, Q1, Q3, J4, J16. Deckt den Motoranlauf ab. |
| **PUMP_N / PUMP2_N** | **0,50 mm** (20 mil) | 0,40 mm | 3,0 A (Puls) / 0,6 A Dauer | TopLayer. Drain von Q1/Q3 → J4/J16. (Nicht als simples Signal einstufen!). |
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

## 4. Das Neck-Down-Verfahren & der Freerouting „Stub“-Trick

### Warum scheitert Freerouting ohne Vorbereitung?
Freerouting hält sich strikt an die eingestellten Netzklassen. Wenn für `VBAT` eine Breite von 1,0 mm vorgegeben ist, versucht Freerouting mit dieser 1,0-mm-Bahn bis auf das 0,25 mm kleine Pad des IP2326 (QFN-24, Pinabstand 0,5 mm) zu fahren. Das verletzt sofort die Abstandsregeln (Clearance) zu den Nachbarpins, und Freerouting kann das Netz nicht fertigstellen.

### Die Lösung: Manuelle Stubs vor dem DSN-Export
1. **Kurze Ausfädelungen (Stubs) in EasyEDA zeichnen:**
   * Am **IP2326 (`U_CHG`)**: Pins **21 & 22** (VOUT/VBAT) gemeinsam mit einer kurzen 0,5-mm-Bahn ca. 0,8 mm weit aus dem Gehäuse herausziehen.
   * An den **MOSFETs (Q1/Q3, SOT-23)** und **Buck-Reglern (TSOT)**: Die Leistungspads ebenfalls mit 0,5 mm kurz (ca. 0,5–1 mm) herausführen.
2. **Stubs sperren (`Lock: Yes`):**
   * Alle gezeichneten Stummel markieren und im Eigenschaften-Panel auf **`Locked: Yes`** setzen.
3. **USB-Paar & Thermal Vias sperren:**
   * `USB_DP`/`USB_DM` manuell verlegen (0,23 mm Bahn, 0,20 mm Gap) und sperren.
   * Die 4–6 Thermal Vias im EPAD des IP2326 setzen und sperren.
4. **Ergebnis in Freerouting:**  
   Freerouting übernimmt gesperrte Elemente aus der DSN-Datei als feste (`FIXED`) Hindernisse und dockt mit der vollen 1,0-mm-Leiterbahn nahtlos an den gesperrten 0,5-mm-Stubs an!

---

## 5. Der Datenaustausch-Workflow (EasyEDA ⇄ Freerouting)

```
[EasyEDA PCB] 
     │  Export Specctra DSN
     ▼
[projekt.dsn]
     │  In Freerouting laden & autorouten
     ▼
[Freerouting]
     │  Export Specctra Session
     ▼
[projekt.ses]
     │  In EasyEDA importieren
     ▼
[EasyEDA PCB] ──► Flächen fluten, Teardrops, DRC
```

### Schritt-für-Schritt-Anleitung:

#### 1. In EasyEDA: DSN-Export
1. Netzklassen und Breiten einstellen (`Design` → `Design Rule...`).
2. Stubs, USB-Paar und Thermal Vias vorab zeichnen und auf **`Locked: Yes`** setzen.
3. Datei exportieren: **`File` → `Export` → `Specctra DSN...`** (z. B. als `SmartGrowTopf_V1.dsn` speichern).

#### 2. In Freerouting: Laden & Routing
1. Freerouting starten und auf **`Open Design`** klicken → `SmartGrowTopf_V1.dsn` auswählen.
2. **Lagen konfigurieren (`Rules` → `Layers`):**
   * `TopLayer` und `BottomLayer`: Routing **aktiviert**.
   * `Inner1` (GND): **Deaktivieren / als Plane deklarieren** (damit Freerouting dort keine Signalbahnen hindurchlegt, sondern nur Vias anbindet).
   * `Inner2`: Optional für Power/Signal freigeben.
3. Auf **`Autoroute`** klicken. Freerouting beginnt mit Ripup-and-Retry.
4. Nach Erreichen von 100 %: Auf **`Postroute`** klicken (entfernt überflüssige Vias und glättet Leiterbahnen).
5. Sitzung exportieren: **`File` → `Export Specctra Session File`** → speichert `SmartGrowTopf_V1.ses`.

#### 3. Zurück in EasyEDA: SES-Import & Finish
1. In EasyEDA: **`File` → `Import` → `Specctra Session...`** wählen und die `SmartGrowTopf_V1.ses` laden.
2. Die fertig gerouteten Bahnen und Vias werden direkt in das Board geladen.
3. **Flächen gießen:**
   * Layer 2 als durchgehende `GND`-Plane fluten.
   * Layer 1 & 4 Freiflächen mit `GND` füllen.
4. **Teardrops hinzufügen:** `Tools` → `Teardrop` ausführen.
5. **Prüfen:** DRC ausführen und Python-Prüfskript starten.

---

## 6. To-Do-Checkliste (Phase A bis E)

### Phase A: Vorbereitung in EasyEDA (Vor dem DSN-Export)
- [ ] **A.1 Freerouting installieren:**
  - Standalone-Installer von [GitHub Releases](https://github.com/freerouting/freerouting/releases) oder JAR heruntergeladen und funktionsfähig.
- [ ] **A.2 Netzliste & 4-Layer-Stackup:**
  - 2S-Netzliste (68 Netze) aktiv.
  - Lagen auf 4 Layers gestellt (`TopLayer`, `Inner1` GND, `Inner2` Power, `BottomLayer`).
- [ ] **A.3 Antennen-Keepout auf ALLEN 4 LAGEN:**
  - 15 mm Freiraum um die ESP32-C6-Antenne auf Layer 1, 2, 3 und 4 kupferfrei halten!
- [ ] **A.4 Feste Bauteile platzieren & sperren:**
  - USB-C `J5`, ESP32-C6 Modul, `U_CHG` (IP2326), `U_BUCK5`, `U_BUCK3`, Stecker `J1`, `J4`, `J16`, `J18`.
- [ ] **A.5 Thermal Vias & USB-Paar manuell vor-routen & sperren:**
  - 4–6 Thermal Vias im EPAD von `U_CHG` direkt zu Layer 2 platzieren → `Locked: Yes`.
  - `USB_DP` / `USB_DM` manuell auf TopLayer verlegen (0,23 mm / 0,20 mm Gap) → `Locked: Yes`.
- [ ] **A.6 Neck-Down-Stubs zeichnen & sperren:**
  - Pins 21 & 22 am IP2326 mit 0,5 mm Stub herausführen → `Locked: Yes`.
  - Leistungspins an Q1, Q3, U_BUCK5 mit 0,5 mm herausführen → `Locked: Yes`.
- [ ] **A.7 Netzklassen in EasyEDA definieren:**
  - `HIGH_CURRENT` (1,00 mm), `POWER_MEDIUM` (0,50 mm), `DEFAULT` (0,25 mm).

---

### Phase B: DSN-Export & Freerouting-Durchlauf
- [ ] **B.1 DSN-Datei exportieren:** In EasyEDA `File` → `Export` → `Specctra DSN...`.
- [ ] **B.2 In Freerouting öffnen:** DSN laden und Lagenregeln prüfen (`Inner1` GND nicht für Signale nutzen).
- [ ] **B.3 Autoroute starten:** Warten bis 100 % Complete erreicht ist.
- [ ] **B.4 Postroute / Optimierung ausführen:** Vias reduzieren und Ecken glätten lassen.
- [ ] **B.5 SES-Datei exportieren:** `File` → `Export Specctra Session File (.ses)`.

---

### Phase C: SES-Import & Fertigstellung in EasyEDA
- [ ] **C.1 SES-Datei importieren:** In EasyEDA `File` → `Import` → `Specctra Session...`.
- [ ] **C.2 Sichtprüfung Neck-Down:** Saubere 45°-Übergänge von den gesperrten Stubs zu den 1,0-mm-Bahnen prüfen.
- [ ] **C.3 Kupferflächen fluten:**
  - Layer 2 als durchgehende `GND`-Plane fluten.
  - Layer 3: Power-Flächen (`VBAT`, `+5V`, `+3V3`) gießen.
  - Layer 1 & 4: Restflächen mit `GND` füllen.
- [ ] **C.4 Teardrops generieren:** In EasyEDA `Tools` → `Teardrop` anwenden.

---

### Phase D: Verifikation & Abnahme (Definition of Done)
- [ ] **D.1 EasyEDA DRC:** `Design Rule Check` liefert 0 Fehler / 0 Abstandsverletzungen.
- [ ] **D.2 Skript-Prüfung:**
  ```bash
  python hardware/easyeda/scripts/pcb_widths.py --check
  ```
  Muss Exit 0 liefern.
- [ ] **D.3 Antennen-Kontrolle:** Keepout auf allen 4 Lagen intakt.
- [ ] **D.4 Stecker & Polung:**
  - J1 (Akku 2S: 1 = BAT-, 2 = MID, 3 = BAT+).
  - J4/J16 (Pumpen), J5 (USB-C), C3 (Elko-Polarität).
