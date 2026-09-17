# Marktvergleich 09/2026 — „Gibt es sowas schon zu kaufen?"

**Frage:** Existiert das Konzept des Smart Grow Topfs (akku-autonomer Einzeltopf, geschlossener
Regelkreis aus kapazitivem Bodensensor + Peristaltik-Dosierpumpe, Top-Drip mit Rücklauf,
Licht-Gate, Push-Alarm) als Fertigprodukt?

**Antwort:** **Nein — nicht als Gesamtpaket.** Jede Einzelachse gibt es am Markt (Akku-Pumpe,
Bodensensor+App, Top-Drip mit Rücklauf, Grow-Kabinen), aber kein Produkt kombiniert sie.
Der nächstliegende Verwandte ist **LazyLeaf** (Einzeltopf, Akku, Pumpe, 1,1 l Tank, 60 € UVP) —
dem fehlt aber der Sensor-Regelkreis und jede Vernetzung.

Stand: 17.09.2026 · Preise Online-Handel, ohne Versand

---

## 1. Verwandte Produkte (nach Nähe zum eigenen Konzept)

| # | Produkt | Preis | Antrieb | Bodenfeuchte-Sensor | App/Alarm | Format | Was gegenüber unserem Konzept fehlt |
|---|---|---|---|---|---|---|---|
| 1 | **LazyLeaf** (Georg Pröpper, „Höhle der Löwen“) | UVP 60 €, Netto-Aktion 9,99 € (ausverkauft) | **Akku 3,7 V / 1200 mAh ≈ 12 Wochen**, Pumpe | ✗ (nur Raumtemperatur) | ✗ (LED + Signalton) | Ø17/13 cm, 16 cm hoch, **1,1 l Tank** | kein Feuchte-Feedback (gießt nach 10 Stufen/Zeit), kein WLAN/Telegram, Tageslicht-Gate statt Dunkelphase, Ø13 cm Innentopf = zu klein für Cannabis |
| 2 | **Ivy Smart Planter** (PlantsIO/Tuya) | ~45–90 € (AliExpress ~50 $, DE-Handel bis ~90 €) | Akku 2000 mAh, USB-C, ~15 Tage | ✓ (kapazitiv, plus Licht/T/rH) | ✓ Tuya-App, Push, HA via `tuya-local` | 11,4 × 10 × 9,6 cm | **kein aktiver Pumpen-Regelkreis** (Selbstbewässerung aus Reservoir per Kapillarwirkung), Cloud-Zwang, Topf winzig, kein Rücklauf |
| 3 | **Botanium** | 65–70 € | Netz/USB, Pumpe alle 3 h | ✗ | ✗ | Einzeltopf, Hydroponik | **hat unser Rücklauf-Prinzip** (Überwasser läuft in den Tank zurück) — aber Netzbetrieb, keine Sensorik, kein Alarm, kein Erde/Substrat |
| 4 | **AutoPot 1Pot 15 l** | 58,90 € (growmart.de) | **stromlos** (AQUAvalve, Schwerkraft) | ✗ (Schwimmerventil) | ✗ | Einzeltopf + Tank, Grow-Maßstab | keine Elektronik, kein Akku, kein Alarm, keine Dosierung — passives Bottom-Feeding |
| 5 | **Blumat Tropf** (Tonkegel) | Set12 59,90 €, Einzelkegel 9,49 € | **stromlos**, Tonkegel = Feuchtefühler | „analog“ (Quellverhalten) | ✗ | beliebig skalierbar | dito; der Grower-Standard für Erde, aber rein mechanisch |
| 6 | **AC Infinity Self-Watering Fabric Pot Base** | 59,99 $ / 4er | **stromlos** (Docht) | ✗ | ✗ | Untersetzer für Stofftöpfe | reine Docht-Bewässerung, kein Akku, kein Sensor |
| 7 | **Gardena AquaBloom L Set** | 119,95 € (idealo), mittlerer Preis laut Stiftung Warentest 146 € | **Solar + Akku + Pumpe**, autark | ✗ (Zeitpläne, 14 Programme) | ✗ (kein WLAN) | 30 Tropfer, 20 m Schlauch, externer Tank | kein Bodensensor (reiner Zeitplan), kein Einzeltopf, kein Push-Alarm |
| 8 | **LetPot Automatic Watering System 2.0** | 69 € / 56,52 $ | USB/Netz (5 V 1 A) | ✗ | ✓ WLAN+BLE-App, Wasserwarnung | Pumpe + 10 m Schlauch, bis 20 Töpfe | kein Akku (im Betrieb netzgebunden), Zeitschaltung statt Feuchteregelung, kein Einzeltopf |
| 9 | **RainPoint IK10PW** (WLAN-Tankpumpe) | ~35–60 $ | **Akku oder USB**, WLAN | ✗ (Zeitplan) | ✓ App | externer Tank + Tropfer | wie LetPot; Eimer-Pumpe, kein Topf |
| 10 | **Ecowitt WFC01 + Bodenfeuchtesensor** | ~60–90 € + Hub | Batterie/Netz am Wasserhahn | ✓ (mit Sensor) | ✓ App | Garten/Wasserhahn | braucht Wasseranschluss + Gateway, kein Akku-Topf |
| 11 | **Vivosun VGrow Smart Grow Box** | 539,99 $ / 599,99 € (DWC-Kit +) | Netz 12 V | ✓ (Wasserstand, T, rH; Erd-Version mit 1,6-gal-Selbstbewässerungs-Reservoir) | ✓ App, Grow-Rezepte | Schrank 45×45×122 cm | Möbelgroß, Netzbetrieb, Preis ≈ 8–12× unser BOM, keine Einzelpflanz-Topf-Lösung |
| 12 | **Hey Abby Grow Box** | ab 699 $ | Netz | ✓ (Ultraschall, T, rH, Wasserstand) | ✓ App | 40×40×122 cm | Kabine mit DWC, **Wasser- UND Luftpumpe**, aber 700 $+, Netz, Abo-Modell |
| 13 | Grobo / Annaboto / SuperCloset | 695–1.895 $ / Grobo insolvent | Netz | ✓ | ✓ | Möbel/Kabine | dito, Premium-Segment |

## 2. Was es am Markt **nicht** gibt

1. **Akku-Autonomie + geschlossener Feuchte-Regelkreis** in einem Topf. Ivy hat Sensorik + Akku,
   aber bewässert kapillar (kein Pumpen-Regelkreis); LazyLeaf hat Akku + Pumpe, aber keinen Sensor.
2. **Peristaltik-Dosierpumpe** in einem Pflanzgefäß. Dosierpumpen gibt es nur als Aquaristik-Geräte
   (Netz) oder in teuren Grow-Controllern — nicht im Topf.
3. **Push-Alarm ohne Cloud** (Telegram). Alle Consumer-Geräte laufen über Hersteller-Cloud
   (Tuya/LetPot/Gardena/App), Telegram-Benachrichtigung existiert nur in DIY-Projekten.
4. **Licht-Gate auf die Dunkelphase** — LazyLeaf nutzt seinen Lichtsensor umgekehrt (gates auf Tageslicht;
   dient primär der Nacht-Ruhe), Grow-Kabinen steuern das Licht selbst, statt auf Fremdlicht zu hören.
5. **Sauerstoff-/Luftpumpe in Bodenkultur.** Luftpumpen gibt es nur in DWC-Systemen
   (Hey Abby 2 W, Vivosun DWC-Kit) — als Ergänzung zum Erdtopf ist das unüblich.
6. **Ein Gerät in Cannabis-tauglicher Topfgröße (Ø 140 mm) mit Elektronik.** Entweder klein und smart
   (Ivy Ø 10 cm) oder groß und dumm (AutoPot 15 l) oder groß, smart und 700 $+ (Kabinen).

## 3. DIY-Szene (nicht kaufbar, als Referenz)

- **Plantwatery** (ESP32, Solar, Bodensensor, Pumpe, MQTT, OTA) — github.com/Lumics/Plantwatery
- **Plantidote** (ESP32/Lolin D32, 0,5 l Tank, Peristaltik-Diaphragmapumpe, Deep-Sleep, 3D-Druck) —
  github.com/MikeBailleul/plantidote-smart-flower-pot
- **Flaura** (ESP32, App, 3D-Gehäuse, nie in Serie gegangen — ESP32-Forum 2021)
- Stiftung Warentest 05/2026 testete 7 Tropfsysteme (17–136 €): Bewertung „sehr gut“ bis
  „befriedigend“, Testsieger mit Solarpanel; Kritikpunkt sind ungleichmäßige Tropfmengen.

## 4. Positionierung

| | Preis | Akku | Feuchte-Regelkreis | Push-Alarm | Dunkel-Gate | O₂ |
|---|---|---|---|---|---|---|
| LazyLeaf | 60 € | ✓ | ✗ | ✗ | ✗ | ✗ |
| Ivy (Tuya) | 45–90 € | ✓ | ✗ (Kapillar) | ✓ cloud | ✗ | ✗ |
| Botanium | 65–70 € | ✗ | ✗ | ✗ | ✗ | ✗ |
| AutoPot / Blumat | 59 € / 9,50 € | – | ✗ | ✗ | – | ✗ |
| AquaBloom / LetPot | 120–146 € / 69 € | teils Solar | ✗ | ✗ / ✓ | ✗ | ✗ |
| Grow-Kabine (Vivosun/Hey Abby) | 540–700 $ | ✗ | ✓ | ✓ | – | ✓ (DWC) |
| **Smart Grow Topf (Projekt)** | **≈ 48 € BOM + ~28 € JLCPCB** | **✓** | **✓** | **✓ Telegram** | **✓** | **✓** (Zusatzpumpe) |

→ Der eigene Topf liegt **auf Marktniveau** (zwischen LazyLeaf und Botanium) und ist die einzige Lösung,
die alle sechs Achsen gleichzeitig abdeckt. Kein Wettbewerber wird durch dieses Ergebnis obsolet;
die Recherche bestätigt die Lücke, statt sie zu schließen.

**Nebenbefund (rechtlich):** Ein *kommerzielles* Produkt speziell „für Cannabis“ wäre in DE im
KCanG-Umfeld werblich heikel — ein Grund, warum die Nische leer ist. Als Eigenbau-Projekt irrelevant.

## Quellen

- LazyLeaf (Produktdaten, UVP/Aktion): netto-online.de Art. 2158028000 · gadget-rausch.de (2020)
- Ivy Smart Planter: cnx-software.com (Hardware: ESP32-WROVER, 7 Sensoren) · smarthomescene.com (Review, Tuya-Local)
- Botanium: newtechstore.eu 65 € · hydroponics.co.uk £69,95
- AutoPot 1Pot: growmart.de 58,90 € · Blumat: blumat.com, growmart.de (Set12 59,90 €)
- AC Infinity Self-Watering Fabric Pot Base: acinfinity.com 59,99 $/4er
- Gardena AquaBloom L: test.de (Stiftung Warentest 05/2026, mittlerer Preis 146 €) · idealo.de 119,95 €
- LetPot 2.0: letpot.com 69,99 $ · indoorgarden.ee 69 € · smarthomeexplorer.com
- RainPoint IK10PW: rainpointonline.com · Ecowitt WFC01: ecowitt.net Handbuch
- Vivosun VGrow: vivosun.com 539,99 $/599,99 € · Hey Abby: heyabby.com, chinagadgetsreviews.com (ab 699 $, Wasser- + Luftpumpe)
- DIY: github.com/Lumics/Plantwatery · github.com/MikeBailleul/plantidote-smart-flower-pot · esp32.com/viewtopic.php?t=21428 (Flaura)
