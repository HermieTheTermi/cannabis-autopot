# IP2326 – Sicherheitsrelevante Beschaltung: Massepins, Strommessung, Eingangsstrom, NTC

**Datum:** 2026-09-16
**Status:** fertig (alle fünf Fragen beantwortet; jede Aussage mit Fassung + Seite belegt; nicht Belegbares ist ausdrücklich als „im Datenblatt nicht gefunden“ markiert)
**Kontext:** 2S-Boost-Lader IP2326 (LCSC C2832094, QFN24 4×4 mm) lädt 2 Zellen Li-Ion aus USB-C 5 V auf 8,4 V.
Externer Low-Side-Schutz zwischen Pack-Minus und Board-Masse: Schutz-IC HY2120-CB + 2× N-Kanal-MOSFET (Nexperia PSMN4R2-30MLDX, LFPAK33), Schwellen 4,28 V Überladung / 2,90 V Tiefentladung pro Zelle, Überstrom ca. 17 A.
Schaltplan-Details: Pin 24 → Pack-Minus; Pin 18 (PGND) und Pin 25 (EPAD) → Board-Masse; ISET mit Widerstand; VSET/CON_SEL offen (8,4 V / 2S); DM/DP unbeschaltet; NTC mit 51 kΩ gegen Masse.

## Quellen und Methode

| Kürzel | Fassung | Umfang | Quelle / lokale Kopie |
|---|---|---|---|
| **V1.11 (zh)** | Injoinic IP2326 **V1.11**, Copyright 2019, www.injoinic.com | 17 S. | offizielle Fassung, von LCSC (C2832094) verlinkt — `/tmp/ip2326/ip2326_lcsc.pdf`, Textextrakt `/tmp/ip2326/ip2326_lcsc.txt` |
| **V1.6 (zh)** | Injoinic IP2326 **V1.6**, Copyright 2020, www.injoinic.com | 18 S. | `/tmp/ip2326/ip2326_cn.pdf`, Text `/tmp/ip2326/ip2326_cn.txt` |
| **V1.2 (en)** | „IP2326 Boost Charging IC for 2/3 Serial Lithium Battery“, **englische Fassung** (Übersetzung d. zh-Fassung, Stand V1.2) | 19 S. | `/tmp/done_land.pdf`, Text `/tmp/ip2326/en_v12.txt` |

Methode: Textlayer-Extraktion (PyMuPDF) aller Seiten; Bildschirm-/Applikationsseiten als Bild gerendert und visuell ausgewertet (Pin-Tabellen, Bild 3 Funktionsblock, Bild 4 NTC-Block, Bild 5 typische Applikationsschaltung). **Zusätzlich wurde der Applikationsschaltplan (Bild 5, S. 14 der Fassung V1.11) aus den Vektor-Objekten der PDF rekonstruiert und vernetzt** (Liniensegmente, T-Verbindungen, Bauteilsymbole), damit die Aussagen zur Masseführung nicht auf Augenmaß beruhen. Zitate sind im Original (zh) plus deutscher Übersetzung angegeben; wo nur die en-Fassung zitiert wird, ist das vermerkt.

> Hinweis zu den Fassungen: Die Abschnitts-, Pin- und Funktionsaussagen sind zwischen V1.11, V1.6 und der en-Übersetzung inhaltsgleich (Stichproben: Pin-Tabelle, NTC-Regeln, DM/DP-Anforderungstabelle, Absolutmaxima). Unterschiede bestehen nur bei einzelnen Tabellenwerten (z. B. Ladestrom-Tabelle: V1.11 nennt RISET = 75 K → 1,2 A, V1.6 nennt RISET = 90 K → 1,0 A; beides erfüllt ICHG = 90000/RISET). Seitenzahlen unten beziehen sich, sofern nicht anders angegeben, auf **V1.11 (17 S.)**.

---

## Frage 1 – Sind Pin 24 (VBAT_GND) und Pin 18 (PGND)/Pin 25 (EPAD) intern niederohmig verbunden?

### Antwort: **NEIN.**

Nach Datenblatt ist Pin 24 **kein Masse-/Leistungspfad**, sondern ein **hochohmiger Detektions-Eingang der Zell-Balancing-Funktion** („电池地检测 PIN“ = Batteriemasse-*Detektions*-Pin). Ein interner niederohmiger Pfad zwischen Pin 24 und PGND/EPAD – etwa ein interner Ladestrom-Messwiderstand – ist **im Datenblatt nicht dokumentiert**. Der externe Low-Side-Schutz wird durch die Beschaltung Pin 24 → Pack-Minus daher **nicht** überbrückt.

### Beleg 1: Pin-Tabelle (V1.11 zh, S. 2; V1.6 zh, S. 2; V1.2 en, S. 3)

Wörtlich (V1.11 zh, S. 2):

| Pin | Name | Originalzitat | Übersetzung |
|---|---|---|---|
| 18 | PGND | „PGND 18 功率地“ | „PGND 18 Leistungsmasse“ |
| 23 | VBATM | „VBATM 23 充电均衡功能，中间电池电压检测 PIN，未使用该功能时悬空“ | „VBATM 23 Balancing-Funktion, Pin zur Messung der mittleren Batteriespannung; bei Nichtnutzung offen lassen“ |
| 24 | VBAT_GND | „VBAT_GND 24 充电均衡功能，电池地检测 PIN，未使用该功能时悬空“ | „VBAT_GND 24 Balancing-Funktion, **Batteriemasse-Detektions-Pin**; bei Nichtnutzung offen lassen“ |
| 25 | GND | „GND EPAD 功率地“ | „GND (EPAD) Leistungsmasse“ |

Englische Fassung, gleiche Tabelle (V1.2 en, S. 3):
> „PGND 18 – Power ground“
> „VBATM 23 – Charging equalization function, Middle Battery Voltage Detection Pin, it should be left floating when doesn't use“
> „VBAT_GND 24 – Charge equalization function, detecting whether the battery pull down to ground pin, it should be left floating when doesn't use“
> „GND EPAD – Power ground“

**Argument:** Pin 18 und EPAD sind ausdrücklich als *Leistungsmasse* deklariert; Pin 24 dagegen als *Detektion*s-Pin, der bei Nichtnutzung **offen bleiben soll** („悬空“). Ein Pin, den der Hersteller offenlassen lässt, kann keinen internen niederohmigen Massepfad haben – die Anweisung wäre sonst technisch sinnlos (Kurzschluss der internen Quelle im IC). Zusätzlich fehlt Pin 24 in der Absolutmaximum-Liste (S. 3), während Leistungspins dort gelistet sind – siehe Frage 2.

### Beleg 2: Der einzige dokumentierte interne Pfad ist der Balancing-MOS, begrenzt auf < 40 mA

V1.11 zh, **S. 10**:
> „IP2326 集成 2 串充电均衡功能； 未使用均衡功能时，相关引脚（第 23、24 脚）悬空即可；“
> „可以通过调整 RCB 来设置均衡电流，均衡电流会以发热的形式消耗在内部均衡 MOS 和 RCB 上，所以均衡电流设置应小于 40mA（**RCB 应大于 100 欧姆**），ICB=VCB/RCB； 标准品的均衡开启电压 VCBON =4.1V；“

Übersetzung:
> „Der IP2326 integriert eine Balancing-Funktion für 2S-Ladung; wenn die Balancing-Funktion nicht genutzt wird, können die zugehörigen Pins (Pin 23, 24) offen bleiben.“
> „Der Balancing-Strom wird über RCB eingestellt; er wird als Wärme im **internen Balancing-MOS** und im RCB verbraucht, deshalb muss der Balancing-Strom **kleiner als 40 mA** eingestellt werden (**RCB muss größer als 100 Ω sein**), ICB = VCB/RCB; die Einschaltschwelle des Standardtyps ist VCBON = 4,1 V.“

Im Funktionsblock (V1.11 zh, **S. 6**, Bild 3) sind genau **zwei** interne Schalter zwischen den Pins 23/24 und VOUT/BAT- gezeichnet (Balancing-MOS über jede der beiden Zellen) – sonst keine Verbindung dieser Pins nach innen.

**Bewertung der Schutzwirkung:** Selbst wenn man den Balancing-Pfad als Verbindung Pin 24 ↔ Pin 23 betrachtet, ist er (a) nur im Balancing aktiv (Abschaltbedingungen S. 10: beide Zellen über VCBON, oder Verlassen des Normalzustands z. B. NTC-Schutz, Eingangsüberspannung, Volladung) und (b) durch den **externen RCB ≥ 100 Ω** auf **< 40 mA** begrenzt. Gegen einen Schutzpfad, der für ca. 17 A ausgelegt ist, ist das 5 Größenordnungen entfernt – keine Überbrückung.

### Beleg 3: Referenzschaltung – was Injoinic tatsächlich verdrahtet (V1.11 zh, S. 14, Bild 5)

Aus dem vektorrekonstruierten Applikationsschaltplan (Fassung V1.11, S. 14) ergeben sich folgende Netze (Pin-Nummern aus der Pin-Beschriftung des Schaltplans 13…18 bzw. 19…24):

- **BAT− (Pack-Minus) → Pin 24 (VBATGND): direkte Drahtverbindung, ohne Bauteil.** (Verfolgter Leitungszug: BAT−-Klemme → horizontale Leitung → vertikaler Knoten → horizontale Leitung auf Höhe der Pin-Zeile → Pin 24 des IC-Symbols; der Zug endet unmittelbar am Pin-Stub, kein Serienbauteil.)
- **BAT+ → Pin 21/Pin 22 (VOUT)** (direkte Verdrahtung).
- **BATM (Mittelabgriff) → RCB (100 Ω, 1206) → Pin 23 (VBATM)**; **C8 (104)** liegt zwischen Pin-23-Netz und dem BAT−/Pin-24-Netz (Verbindungspunkt auf der Pin-23-Zuleitung), **C7 (104)** zwischen VOUT-Netz und dem BAT−/Pin-24-Netz – dabei kreuzt C7 die Pin-23-Zuleitung im Bild mit einem Leitungssprung (Hop-Symbol, also ohne Verbindung).
- **Pin 18 (PGND) → GND-Netz** (Leitungszug mit Masse-Symbol).
- **BAT− trägt im Applikationsschaltplan ein Masse-Symbol**, d. h. **Pack-Minus = Board-Masse = GND = PGND** ist im Referenzdesign **ein und derselbe Knoten**.

Wörtliche Annotation im Applikationsschaltplan (V1.11 zh, S. 14):
> „PIN23、24，均衡检测脚，未使用时悬空NC“ → „PIN 23, 24 = Balancing-Detektionspins; bei Nichtnutzung offen (NC)“

### Wichtige Einschränkung (bitte beachten)

Das Datenblatt **garantiert keine** interne Trennung von Pin 24 gegen PGND/EPAD – es *dokumentiert* nur keine Verbindung, und im Referenzdesign sind BAT−, GND und PGND ohnehin derselbe Knoten. Die geplante Topologie (Schutz-MOSFETs **zwischen** Pack-Minus und Board-Masse, Pin 24 am Pack-Minus) ist im Datenblatt **nicht abgebildet und nicht bewertet**.

**Konsequenz (Prüfempfehlung):** Am Muster den Widerstand Pin 24 ↔ Pin 18/EPAD am **unbestromten** Bauteil messen (Bauteil bestückt oder als Einzel-IC):
- hochohmig bzw. nur Dioden-/ESD-Strecke (Größenordnung ≥ MΩ bzw. ca. 0,6 V Diodenmessung) → Beschaltung zulässig wie geplant;
- niederohmig (Ω- bis wenige Ω-Bereich) → Pin 24 auf Board-Masse legen und auf die interne Balancing-Funktion verzichten (externes Balancing wie im EEWorld-Referenzdesign mit HY2213 verwenden).

---

## Frage 2 – Zulässige Spannungsdifferenz zwischen den Massepins? Verhalten bei unterbrochener Verbindung Pack-Minus ↔ Board-Masse?

### Antwort: **im Datenblatt nicht gefunden** – für beide Teilfragen.

1. **Zulässige Spannungsdifferenz zwischen den Massepins: im Datenblatt nicht gefunden.** In den Absolute Maximum Ratings (V1.11 zh, **S. 3**) sind **PGND, EPAD und VBAT_GND gar nicht aufgeführt**; es existiert also kein spezifizierter Grenzwert für die Differenzspannung zwischen diesen Pins.
   Wörtlich (V1.11 zh, S. 3):
   > „VIN 电压范围 VIN −0.3 ~ 25 V“
   > „VOUT、VSYS、LX、BST、VBATM、DM、DP 电压范围 V −0.3 ~ 20 V“
   > „结温范围 TJ −40 ~ 150 ℃“ · „热阻（结温到环境）θJA 60 ℃/W“ · „人体模型（HBM）ESD 4 KV“
   (V1.6 zh, S. 3 führt BST getrennt: „BST 电压范围 VBST −0.3 ~ VLX+8 V“ – sonst gleich.)
   **Auffällig:** VBAT_GND fehlt in der Liste, VBATM ist dagegen mit −0,3 … 20 V gegenüber GND geführt.

2. **Verhalten bei unterbrochener Verbindung Pack-Minus ↔ Board-Masse (ausgelöster Schutz): im Datenblatt nicht gefunden.** Es gibt
   - keine Aussage, kein Verbot und **keine Open-GND-/Batteriemasse-Erkennung**. Die aufgeführten Schutzfunktionen sind (V1.11 zh, **S. 9–10**): „输出过流、输入欠压、过压、过温等保护功能“ = Ausgangs-Überstrom, Eingangs-Unter-/Überspannung, IC-Übertemperatur (135 ℃, S. 10) sowie Ladezeit-Timeout (ROT, S. 12);
   - **keine Referenzschaltung**, in der der IP2326 hinter einem externen Low-Side-Schutz in der Minusleitung betrieben wird. Im Gegenteil: im Applikationsschaltplan (S. 14) ist BAT− direkt mit GND/Masse verbunden (siehe Frage 1, Beleg 3).
   - Auch in der BOM (S. 15) und im NTC-/Balancing-Kapitel finden sich keine Hinweise zu getrennter Batteriemasse.

### Eigene Risikobewertung (ausdrücklich **nicht** Datenblattinhalt)

- Bei geöffnetem Low-Side-Schutz und weiterhin anliegender Ladequelle wird der IC (VOUT/VSYS-Ausgang, Pin 24 am Pack-Minus, Pin 18/EPAD an Board-Masse) **zwischen Pack-Minus und Board-Masse** betrieben; zwischen beiden Pins kann theoretisch die volle Packspannung (bis ca. 8,4 V) stehen, ohne dass das Datenblatt dafür einen Grenzwert oder ein Verhalten nennt.
- Belegt begrenzt sind nur die Pins, die in der Absolutmaximum-Liste stehen (VBATM ≤ 20 V); für VBAT_GND existiert kein Wert. Welche Ströme über die Detektions-/Balancing-Struktur oder ESD-Dioden fließen, ist nicht spezifiziert.
- Empfehlung: Entweder (a) Pin 24 nicht am Pack-Minus, sondern an Board-Masse betreiben (dann ist die Balancing-Funktion des IP2326 nicht nutzbar – vgl. Referenzdesign EEWorld mit externem HY2213), oder (b) die Topologie messtechnisch verifizieren (Spannungsfestigkeit Pin 24 ↔ Pin 18 bei offenem Schutz nachstellen: Pack-Minus und Board-Masse trennen, Ladequelle anlegen, Strom und Spannung an Pin 24 beobachten). Ein Test mit Labornetzteil und Strombegrenzung ist hier ohnehin sinnvoll.

---

## Frage 3 – Wie genau wird der Ladestrom gemessen? Wo sitzt der Messwiderstand?

### Antwort: **Der Ladestrom wird IC-intern gemessen** (batterieseitig), **nicht** über einen externen Shunt in der Minusleitung. Belegt sind: Einstellung über RISET, Formel ICHG = 90000/RISET, **Genauigkeit ±10 %** und dass der eingestellte Strom der **maximale Ladestrom an der Batterie** ist. **Welcher interne Pin-Pfad den Strom erfasst, ist im Datenblatt nicht benannt** (im Datenblatt nicht gefunden). Ein externer Widerstand in der Minusleitung ist in keiner Datenblatt-Fassung und in keiner BOM enthalten – er wird also nicht zur Messgröße und verfälscht die Stromregelung nicht; er verschiebt lediglich den Massebezug.

### Belege

V1.11 zh, **S. 10** (Einstellung):
> „IP2326支持ISET脚外接电阻RISET，来设置恒流充电电流，所设定的电流是电池端最大充电电流(**精度±10%**)。“

Übersetzung: „Der IP2326 stellt über den externen Widerstand RISET am ISET-Pin den Konstantstrom ein; der eingestellte Strom ist der maximale Ladestrom an der Batterie (Genauigkeit ±10 %).“

V1.11 zh, **S. 11**:
> „ISET / RISET / **ICHG=90000 / RISET**“ — „RISET设置电池端充电电流“ mit „180K → 0.5A；90K → 1A；75K → 1.2A；60K → 1.5A“ sowie Fußnote „小于700mA 的充电电流，请使用IP2326_NPD 的型号“ (Ströme < 700 mA: Typ IP2326_NPD verwenden)

V1.11 zh, **S. 4** (Kenndaten, 2S-Betrieb):
> „充电电流 ICHRG … **恒定输出端的电池电流**，2 串充电 VOUT=7.6V，RISET=75K → **1.08 / 1.2 / 1.32 A“**
→ Min/Typ/Max = ±10 % um 1,2 A. Entsprechend V1.6 zh, S. 4: „VOUT=7.6V，RISET=90K → 0.9 / 1.0 / 1.1 A“.

V1.11 zh, **S. 15** (BOM):
> „11 贴片电阻 0603 **1%** PCS 1 RISET 设置充电电流；1%精度“ → Einstellwiderstand mit 1 % Toleranz.

### Wie das im geplanten Board wirkt

- **Messwiderstand:** kein externer Shunt – weder in der BOM (S. 15) noch im Applikationsbild (S. 14). Der einzige 0,5-Ω-Widerstand der Referenzschaltung ist **R1 (0603, 0.5 R, 5 %)**, der laut BOM **ohne Funktionsangabe** geführt wird; im Schaltplanbild liegt er als **RC-Filter** in der Zuleitung des VIN-Pins (Pin 13) – auf der Pin-Seite liegt C3 (10 µF), auf der anderen Seite der Eingangsknoten mit L1/C1 (Bildanalyse, S. 14). Er ist **nicht** der Ladestrom-Messwiderstand.
- **Der Ladestrom wird also intern erfasst**, die Regelgröße ist der Strom **an der Batterie** (VOUT-Seite).
- **Ein zusätzlicher Widerstand in der Minusleitung** (z. B. Shunt einer weiteren Überwachung, Leiterbahn, Stecker) liegt im Rückstrompfad. Beispiele für den Spannungsabfall mit dem geplanten Schutz: 2 × PSMN4R2-30MLDX (Rds(on) ca. 4,2 mΩ typ.) ⇒ **ca. 8,4 mV bei 1,0 A / 10,1 mV bei 1,2 A / 12,6 mV bei 1,5 A** (eigene Rechnung; nur ein Beispiel, keine Datenblattangabe).
  Folge: Die Stromregelung bleibt korrekt (derselbe Strom fließt durch IC-Masse und externen Pfad), aber die **CV-Spannung an den Zellen liegt um diesen Betrag unter der intern geregelten Ausgangsspannung** – bei mΩ-Widerständen unkritisch (< 15 mV), bei absichtlichen Shunts (z. B. 50 mΩ) aber bereits 60–100 mV. Wer einen Shunt in der Minusleitung plant, muss ihn bei der Zielspannung einkalkulieren – **eine Aussage des Datenblatts dazu gibt es nicht** (im Datenblatt nicht gefunden).
- **Fehlerquellen**, die das Datenblatt selbst nennt bzw. die sich belegen lassen: Toleranz von RISET (1 % gefordert, S. 15), Gesamtgenauigkeit ±10 % (S. 4, 10), Zählung des Stroms als „电池端“-Strom (batterieseitig), Temperaturgang/Rds(on) externer Bauteile (nicht spezifiziert). Zusätzlich begrenzt die **Abschalt-/Neustartlogik** die Messaussage: Ladeende, wenn der Strom < 200 mA über 30 s fällt (S. 9).

---

## Frage 4 – Erkennt der IP2326 über DM/DP eine DCP-Ladequelle (BC1.2) und begrenzt den Eingangsstrom? Maximaler Eingangsstrom?

### Antwort: **Nein – DP/DM werden nicht zur BC1.2-/DCP-Erkennung benutzt, sondern ausschließlich für eine Spannungsanforderung (Fast-Charge-Request).** Eine **einstellbare Eingangsstrombegrenzung (Pin, Widerstand, Register) ist im Datenblatt nicht gefunden**; die Eingangsregelung ist eine *Eingangsspannungs*-Regelschleife über RUV (VIN_UVSET). Ein **maximaler Eingangsstrom ist im Datenblatt nicht zahlenmäßig spezifiziert**; belegt ist nur „max. 15 W Eingang“ und der empfohlene Eingangsspannungsbereich 4,5–9,5 V.

### Belege

Pin-Tabelle (V1.11 zh, **S. 2**): „DM 1 USB DM“, „DP 2 USB DP“ – keine weitere Funktion dokumentiert.

Fast-Charge-Anforderung über DP/DM (V1.11 zh, **S. 9**), wörtlich:
> „输入快充申请 / IP2326可以根据当前电池电压，通过DP/DM来向输入端申请快充电压；
> 配置为2串充电时：当电池电压 VBAT<6.2V 时，不申请快充，只是以5V输入充电；当电池电压 6.2V<=VBAT<6.8V，会尝试申请5.4V输入快充；当电池电压 6.8V<=VBAT<7.8V，会尝试申请6V输入快充；当电池电压 VBAT>=7.8V 后，会尝试申请7V输入快充；
> 如果不能成功申请快充输入，会一直以5V输入来充电；“

Übersetzung:
> „Fast-Charge-Anforderung am Eingang / Der IP2326 kann abhängig von der Batteriespannung über DP/DM am Eingang eine Fast-Charge-Spannung anfordern.
> Bei 2S-Konfiguration: VBAT < 6,2 V → keine Anforderung, Laden mit 5 V; 6,2 V ≤ VBAT < 6,8 V → Anforderung 5,4 V; 6,8 V ≤ VBAT < 7,8 V → Anforderung 6 V; VBAT ≥ 7,8 V → Anforderung 7 V.
> Wenn die Fast-Charge-Anforderung nicht erfolgreich ist, wird weiterhin mit 5 V Eingang geladen.“

**Einordnung:** Das ist ein reines **Spannungserhöhungs-Protokoll über DM/DP** (HVDCP-artig). Eine BC1.2-**DCP**-Erkennung (Kurzschluss D+↔D−) oder eine Stromverhandlung ist im Datenblatt **nicht gefunden** – DCP würde ohnehin nur 5 V liefern und keine Stromgrenze melden. Konsequenz: **Ohne DM/DP-Beschaltung findet keine Anforderung statt; es wird dauerhaft mit 5 V geladen** (dokumentierter Rückfallzustand, S. 9) – das ist laut Datenblatt zulässig.

Eingangsstrombegrenzung existiert nur als **Eingangsspannungs-Regelschleife** (V1.11 zh, **S. 10**, identisch in der Feature-Liste S. 1 „自动调节输入电流，自适应适配器负载“):
> „IP2326具有输入VIN输入稳压环路，在检测到输入电压接近RUV所设置的输入欠压阈值时，就会自动调整降低充电电流，保证输入电压稳定在输入欠压阈值附近，确保不会拉挂适配器。“
→ „Der IP2326 hat eine VIN-Eingangs-Regelschleife: Sobald die Eingangsspannung sich der über RUV eingestellten Unterspannungsschwelle nähert, wird der Ladestrom automatisch reduziert, um die Eingangsspannung nahe der Schwelle stabil zu halten und ein Kollabieren des Adapters zu verhindern.“

Einstellbare Eingangsschwellen (V1.11 zh, **S. 11/12**):
- RUV (VIN_UVSET): 1K → 4,25 V · 68K → 4,35 V · 120K → 4,45 V · NC → 4,65 V
- ROV (VIN_OVSET): NC → 8,75 V (2S) · 120K → 8,4 V · 68K → 8 V · 1K → deaktiviert

Zahlenwerte / Grenzen:
- empfohlener Eingangsspannungsbereich **4,5 V … 9,5 V**; Ladestrom 0…**1,5 A** (V1.11 zh, **S. 3**, „推荐工作条件“)
- Absolutmaximum **VIN −0,3 … 25 V** (S. 3); Feature „输入耐压25V“ (S. 1)
- „**最大15W输入充电**，5V输入，8V/1A输出转换效率94%，8V/1.5A输出转换效率92%“ (S. 1) → 15 W bei 5 V entsprechen ca. 3 A Eingangsstrom **(eigene Umrechnung)**
- Eingangs-Ruhestrom IVIN typ. 10–30 mA (S. 4) – kein Limitwert
- **Kein Eingangs-Überstromschutz** spezifiziert: die Feature-Liste nennt „输出过流、过压、短路保护“ (S. 1) – **ausgangs**seitig; ein „输入过流“ ist weder in der Feature-Liste noch in den elektrischen Kenndaten (S. 3–5) zu finden. Ebenso finden sich **keine Zahlenwerte** für die Ausgangs-Überstrom-/Kurzschlussschwelle (S. 3–5) – auch das dokumentiert das Datenblatt nicht.

### Eigene Anmerkungen zur Auslegung (nicht Datenblatt)

- Ohne PD/QC-fähige Quelle lädt das Board mit 5 V; die Ladeleistung ergibt sich aus dem Eingangsbudget: 5 V × 3 A (USB-C-Standard) = 15 W; bei ca. 90 % Wirkungsgrad und 8,4 V Ausgang bleiben ca. 1,5–1,6 A – das passt zum spezifizierten Maximum von 1,5 A Ladestrom.
- An einer schwachen 5-V-/1,5-A-Quelle (7,5 W) sind nur ca. 0,8 A Ladestrom möglich; die Reduktion erfolgt dann **nicht** über eine Strombegrenzung des IP2326, sondern nur dadurch, dass die Quelle einbricht und die VIN-Regelschleife (RUV) den Strom nachführt. Für eine verlässliche Funktion sollte RUV auf die Unterspannungsschwelle der Quelle abgestimmt werden (z. B. RUV = 120K → 4,45 V), oder der Eingangsstrom extern (eFuse/Port-Controller) begrenzt werden.
- Ist DM/DP offen (geplante Variante), werden auch 7-V-fähige Netzteile nicht angefragt; die 1,5 A werden dann bei 5 V erreicht.

---

## Frage 5 – NTC-Beschaltung: Typ, Beschaltung, Schwellen, Verhalten

### Antwort (kompakt)

| Punkt | Datenblattangabe |
|---|---|
| Speisung | NTC-Pin ist **Stromquelle 20 µA** (19/20/21 µA), Spannung wird am Pin gemessen |
| Empfohlener NTC | Beispiel im Datenblatt: **100 kΩ, B = 4100** |
| Widerstand | **R2 = 82 kΩ parallel zum NTC** (Tabelle rechnet mit „R2//RNTC“) |
| Schwellen | **> 1,32 V** zu kalt → Ladung stoppen · **0,56–1,32 V** normal · **0,43–0,56 V** warm → Ladestrom halbieren · **< 0,43 V** zu heiß → Ladung stoppen |
| Beispieltemperaturen | mit 100K/B4100 ∥ 82K: **0 °C → 1,32 V**, **45 °C → 0,56 V**, **55 °C → 0,43 V** |
| Deaktivierung | „如果不需要NTC功能，将NTC引脚接**51K电阻到地**“ – 51 kΩ gegen GND = Funktion nicht benutzt |
| Kondensator | im Applikationsbild **kein** Kondensator am NTC-Pin (die 104er-Kondensatoren C7/C8 gehören zum Balancing) |
| Verhalten des IC | Über-/Untertemperatur ⇒ Ladung gestoppt; „mittlere“ Übertemperatur ⇒ Strom halbiert; Störung wird zusätzlich über blinkende LED signalisiert; Balancing wird bei NTC-Schutz abgeschaltet |

### Belege

Pin-Tabelle (V1.11 zh, **S. 2**): „NTC 4 NTC温度保护，接NTC电阻，输出20uA的电流“ → „NTC 4 NTC-Temperaturschutz, NTC-Widerstand anschließen, speist 20 µA aus“.
Kenndaten (V1.11 zh, **S. 5**): „NTC 引脚电流 INTC 19 / 20 / 21 uA“.

V1.11 zh, **S. 12**:
> „IP2326支持NTC保护功能，可配合NTC电阻来检测电池温度；如果不需要NTC功能，将NTC引脚接**51K电阻到地**。IP2326通过NTC引脚放出20uA电流，然后检测该电流在NTC电阻上产生的电压，来判断温度高低，当检测温度超过设定的温度时，关闭充电。“

V1.11 zh, **S. 13** (Bild 4 NTC-Block + Regeln):
> „当IP2326检测到NTC引脚电压在**0.56V~1.32V**之间，表示电池温度正常，正常充电；
> 当IP2326检测到NTC引脚电压在**0.43V~0.56V**之间，表示电池温度偏高，**充电电流减小一半**；
> 当IP2326检测到NTC引脚电压下降到**小于0.43V**，表示电池温度过高，**停止充电**；
> 当IP2326检测到NTC引脚电压上升到**大于1.32V**，表示电池温度过低，**停止充电**；“

Auslegungsbeispiel (V1.11 zh, **S. 13**):
> „举例： RNTC=100K 热敏电阻(**B=4100**)， R2=**82K**，对应的温度和NTC引脚电压：“
> Tabelle (Spaltenkopf: „R2//RNTC 阻值“): 0 ℃ → RNTC 246,7 kΩ → R2∥RNTC 66,3 kΩ → **1,32 V**; 45 ℃ → 41,2 kΩ → 27,8 kΩ → **0,56 V**; 55 ℃ → 28,4 kΩ → 21,1 kΩ → **0,43 V**.

BOM (V1.11 zh, **S. 15**):
> „16 NTC 电阻 NTC 电阻 PCS 1 RNTC – 根据设计温度选择；**不使用时，接 51K 电阻到地**；“
> „18 贴片电容 0603 104 10% PCS 1 C7、C8 – 不使用均衡功能时可以不用“

LED/Status (V1.11 zh, **S. 13**): „充电过程LED亮，充电满后LED灭，**检测到异常后LED闪烁**“; Balancing-Abschaltung beim Verlassen des Normalzustands inkl. NTC-Schutz (S. 10).

### Nachrechnung der Schwellen (eigene Rechnung, Plausibilitätsprüfung)

V_NTC = 20 µA × R_NTC (bzw. × (R2∥R_NTC)). Mit 100 kΩ / B = 4100 und 82 kΩ parallel:

| T | R_NTC | R2∥R_NTC | V_NTC | Reaktion des IP2326 |
|---|---|---|---|---|
| −20 °C | 1152 kΩ | 76,6 kΩ | 1,53 V | zu kalt → Stopp |
| 0 °C | 352 kΩ | 66,5 kΩ | 1,33 V | zu kalt → Stopp (Schwelle 1,32 V) |
| 10 °C | 207 kΩ | 58,7 kΩ | 1,18 V | normal |
| 25 °C | 100 kΩ | 45,1 kΩ | 0,90 V | normal |
| 45 °C | 42,1 kΩ | 27,8 kΩ | 0,56 V | Grenze normal / Strom halbiert |
| 55 °C | 28,4 kΩ | 21,1 kΩ | 0,42 V | zu heiß → Stopp |
| 60 °C | 23,6 kΩ | 18,3 kΩ | 0,37 V | zu heiß → Stopp |

Die Rechnung reproduziert die Datenblatt-Tabelle (0/45/55 °C) bis auf die 0-°C-Zeile, wo das Datenblatt selbst inkonsistent ist (66,3 kΩ entspräche einem NTC-Wert von ~346 kΩ statt der angegebenen 246,7 kΩ; 61,5 kΩ wäre der korrekte Parallelwert → 1,23 V). Für die Auslegung daher die eigenen Werte verwenden. **Hinweis:** das ist eine Rechenkontrolle, keine Datenblattaussage.

### Prüfung der geplanten 51-kΩ-Deaktivierung

20 µA × 51 kΩ = **1,02 V** → liegt im Fenster 0,56–1,32 V = „Temperatur normal“ → das IC lädt mit vollem Strom. Die im Datenblatt vorgesehene 51-kΩ-Option ist also konsistent dimensioniert; das IC interpretiert sie als „normale Zelle“.
**Sicherheitsrelevant:** Damit ist der Temperaturschutz des Laders **vollständig deaktiviert** – keine Abschaltung bei Über-/Untertemperatur und keine Halbierung des Stroms. Bei einem 2S-Pack ohne eigenen NTC ist das eine bewusste Entwurfsentscheidung, die dokumentiert und (z. B. durch einen separaten Temperaturschutz im BMS) kompensiert werden muss.

### Praxisfalle (eigene Rechnung, nicht Datenblatt)

Wird ein **100-kΩ-NTC (B = 4100) ohne Parallelwiderstand** angeschlossen, ergibt sich bei 25 °C V = 20 µA × 100 kΩ = **2,0 V > 1,32 V** → das IC wertet das als **„zu kalt“ und blockiert die Ladung**. Der Parallelwiderstand (82 kΩ) ist also nicht optional, sondern notwendig, damit die Schwellen in einem sinnvollen Temperaturbereich liegen. Alternativ ist ein NTC mit kleinerem Nennwert (z. B. 10 kΩ, B ≈ 3435) mit passendem Parallelwiderstand zu dimensionieren.

---

## Zusammenfassung (Ja/Nein-Übersicht)

| # | Frage | Antwort | Belegstellen |
|---|---|---|---|
| 1 | Interne niederohmige Verbindung Pin 24 (VBAT_GND) ↔ Pin 18/EPAD (PGND)? | **NEIN** – Pin 24 ist Detektions-Pin der Balancing-Funktion („电池地检测 PIN“, bei Nichtnutzung offen); einziger dokumentierter interner Pfad ist der Balancing-MOS, extern durch RCB ≥ 100 Ω auf < 40 mA begrenzt; Absolutmaxima führen Pin 24 nicht als Leistungspfad | V1.11 zh S. 2, 3, 6, 10, 14; V1.2 en S. 3 |
| 2 | Zulässige Differenzspannung der Massepins? Verhalten bei offener Pack-Minus-Verbindung? | **im Datenblatt nicht gefunden** (PGND/EPAD/VBAT_GND fehlen in den Absolutmaxima; keine Open-GND-Erkennung; keine Referenzschaltung mit externem Low-Side-Schutz; im Referenzdesign ist BAT− = GND) | V1.11 zh S. 3, 9–10, 14 |
| 3 | Wo sitzt der Messwiderstand? Genauigkeit? | Messung **IC-intern**, Messpunkt nicht benannt (**im Datenblatt nicht gefunden**); geregelt wird der **batterieseitige** Maximalstrom; **±10 %**; ICHG = 90000/RISET; RISET 1 %; kein externer Shunt in BOM/Schaltplan | V1.11 zh S. 4, 10, 11, 14, 15 |
| 4 | DCP/BC1.2 über DM/DP? Eingangsstrombegrenzung? Max. Eingangsstrom? | **Keine DCP-Erkennung dokumentiert**; DP/DM nur für Spannungsanforderung 5,4/6/7 V (Rückfall: 5 V). Einstellbare Eingangsstrombegrenzung **im Datenblatt nicht gefunden**; nur VIN-Unterspannungs-Regelschleife (RUV). Max. Eingangsstrom **nicht zahlenmäßig spezifiziert** („max. 15 W Eingang“, VIN 4,5–9,5 V empfohlen, keinerlei Eingangs-OCP) | V1.11 zh S. 1, 2, 3, 4, 9, 10, 11, 12 |
| 5 | NTC-Beschaltung und Schwellen? | 100 kΩ **B = 4100** ∥ **R2 = 82 kΩ**, Speisung 20 µA, Schwellen 1,32 V (kalt, Stopp) / 0,56 V (warm, Strom halbiert) / 0,43 V (heiß, Stopp) ≈ 0 / 45 / 55 °C; **51 kΩ gegen GND = laut Datenblatt vorgesehene Deaktivierung** (V_NTC = 1,02 V); kein NTC-Kondensator im Applikationsbild | V1.11 zh S. 2, 5, 12, 13, 14, 15 |

## Offene Punkte / Empfehlungen

1. **Pin 24 messtechnisch verifizieren** (Widerstand Pin 24 ↔ Pin 18/EPAD am unbestromten IC). Bei niederohmigem Befund: Pin 24 auf Board-Masse, Balancing extern (HY2213 o. ä.) oder verwerfen.
2. **Offener Low-Side-Schutz ist im Datenblatt nicht bewertet** (Frage 2). Vor Serienreife: Testaufbau mit trennbarer Pack-Minus-Verbindung und Messung von Spannung/Strom an Pin 24 (Strombegrenzung im Labornetzteil!), da die Pins 23/24 nicht als Absolutmaximum gelistet sind.
3. **Temperaturschutz ist mit 51 kΩ deaktiviert** – bewusst dokumentieren; ohne NTC gibt es keine Übertemperaturabschaltung des Laders. Alternativ NTC-Netz nach Frage 5 bestücken (100K/B4100 ∥ 82K) und RUV/ROV passend wählen.
4. **Eingangsstrom**: keine harte Begrenzung im IC. RUV auf die Quelle abstimmen (z. B. 120K → 4,45 V) und/oder Eingang extern strombegrenzen; DM/DP offen lassen ist zulässig, kostet aber die 7-V-Anforderung (Ladung bleibt bei 5 V).
5. **RISET** mit 1 % bestücken (Datenblattvorgabe), Zielstrom z. B. 1,2 A → 75 kΩ (V1.11) bzw. 1,0 A → 90 kΩ (V1.6-Tabelle); Ladeströme < 700 mA erfordern den Typ **IP2326_NPD**.
6. **Datenblattversion führen**: LCSC verlinkt V1.11 (2019); V1.6 (2020) ist ebenfalls im Umlauf. Vor der Fertigung die aktuellste Fassung beim Hersteller prüfen (Datenblatt nennt dazu ausdrücklich den Vorbehalt, dass Injoinic Dokumente aktualisiert: „英集芯会不定期更新本文档内容“ S. 17).

## Anhang: lokale Dateien

- Datenblatt V1.11 (zh, 17 S.): `/tmp/ip2326/ip2326_lcsc.pdf`, Text `/tmp/ip2326/ip2326_lcsc.txt`
- Datenblatt V1.6 (zh, 18 S.): `/tmp/ip2326/ip2326_cn.pdf`, Text `/tmp/ip2326/ip2326_cn.txt`
- Datenblatt en-Fassung (19 S.): `/tmp/done_land.pdf`, Text `/tmp/ip2326/en_v12.txt`
- Bildausschnitte der ausgewerteten Seiten: `/tmp/ip2326/img/` (u. a. `zh14_*` = typische Applikationsschaltung V1.11 S. 14, `zh_v111_p6/p10/p13/p15`, `en_v12_p16`)
- Downloadquellen: LCSC-Produktseite C2832094 (dort verlinktes PDF), `https://www.chipsourcetek.com/DataSheet/IP2326.pdf`, `https://done.land/assets/files/ip2326_datasheet.pdf`
