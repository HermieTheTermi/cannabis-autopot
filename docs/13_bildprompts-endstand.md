# Bild-Prompts für den fertigen Smart Grow Topf (Vollausstattung, inkl. Sprudler)

Stand: 17.09.2026 · Geometrie-Quelle: `docs/02_architektur-und-geometrie.md` + `cad/params.py`
Ergänzt (nicht ersetzt) `docs/04_bildkonzepte-prompts.md` — dort stehen die fünf Konzept-Prompts aus
der V1-Phase; hier stehen **drei Prompts für den gebauten Topf im Endzustand**, geschrieben für
**Gemini (Google), ohne Negativ-Prompt**.

**Aufbau:** Jeder der drei Prompts ist vollständig und self-contained — reinkopieren, fertig. Der
Geometrie-Absatz steckt in allen dreien wortgleich drin, damit die drei Bilder dasselbe Gerät zeigen.
Wenn sich eine Geometrie ändert: den Absatz **in allen drei Prompts** gleichzeitig nachziehen.

**Zwei Korrekturen gegenüber der ersten Fassung (17.09.2026):**
1. Die **Sauerstoffpumpe sitzt innen im Elektronik-Turm** — außen ist nichts zu sehen, nur der Topf.
   (Bisher stand in der Doku „außerhalb montieren" — siehe „Offene Punkte" unten, die Doku ist
   nachzuziehen.)
2. Der **Einfüllstutzen sitzt unten am Wassertank**, knapp über der Trennfuge bei ca. 68–84 mm Höhe,
   **nicht** oben am Kragen.

---

## Was das Gerät ist (Kurzfassung, damit die Bilder stimmen)

Ein automatisch bewässernder Smart-Grow-Topf für **eine** Cannabis-Pflanze:

- **Außen:** ein durchgehender Zylinder, Ø 140 mm, **278 mm hoch** (ohne Pflanze), 3D-gedruckt aus
  mattem hellgrauem PETG. An einer Seite angedruckt: der **Elektronik-Turm** („Wulst", 60 × 40 mm,
  y 90–250 mm) mit Deckel, USB-C und LED-Fenster. Unten, auf der Gegenseite, der
  **45°-Einfüllstutzen** für den Wassertank mit Kappe. Oben der **Kragen** mit zwei Reihen
  LST-Ankerlöchern.
- **Innen:** **Top-Drip**. Unten der **1,0-L-Wassertank**, darüber 30 mm Luftspalt, darüber der
  **Erdbehälter mit 25 mm Blähton-Drainage**. Eine kleine **Peristaltikpumpe** im Turm zieht Wasser aus
  dem Tank und drückt es nach oben auf den **gedruckten Verteilerring** auf dem Substrat; das Wasser
  sickert durchs Substrat und läuft über eine Lochplatte in den Tank zurück.
- **Sensorik:** kapazitiver **Bodenfeuchtesensor**, von oben eingesteckt, Messebene 75 mm tief →
  regelt das Gießen. **Lichtsensor** extern am Kragenrand → es wird nur in der Dunkelphase gegossen.
- **Strom:** **2S-Akkupack (6,0–8,4 V)** im Turm, Lader, Zellschutz und Balancing auf der eigenen
  Platine, USB-C zum Laden, ESP32-C6 mit WLAN → **Telegram-Alarm**, wenn der Tank leer ist.
- **Sprudler:** eine zweite, kleine **Membran-Luftpumpe sitzt mit im Turm** und bläst über einen
  Silikonschlauch, der im Turm nach unten in den Tank führt, Luft auf einen **Luftsprudlerstein am
  Boden des Wassertanks** — daher das Sprudeln im Wasser. Außen ist davon nichts zu sehen.

---

# Prompt 1 · Außenansicht des fertigen Topfs (Vollausstattung)

```text
Fotorealistisches 3D-Produktrendering eines 3D-gedruckten, zylindrischen Pflanzentopfs, Dreiviertelansicht von schräg vorn, der Topf steht allein und vollständig im Bild, nichts steht daneben.

Der Topf: Außendurchmesser 140 mm, Gesamthöhe 278 mm ohne Pflanze, die Höhe ist also etwa das Doppelte des Durchmessers. Werkstoff mattes hellgraues PETG mit feinen, sichtbaren FDM-Schichtlinien, keine glänzende Spielzeugoptik. Eine glatte waagerechte Trennfuge läuft bei etwa 90 mm Höhe um den Zylinder, dort sitzen die beiden gedruckten Schalenhälften aufeinander. Der untere Teil ist der geschlossene Wassertank mit 1,0 Liter Inhalt, darüber folgt eine 30 mm hohe Luftkammer, darüber der Erdbehälter, und ganz oben schließt ein 12 mm hoher, leicht überstehender Kragenring ab. In diesem Kragenring sitzen zwei versetzte, umlaufende Reihen kleiner Ankerlöcher von 2 mm Durchmesser, die nur bei einem Kabelausschnitt unterbrochen sind.

An einer Seite ist ein rechteckiger Elektronik-Turm direkt an den Zylinder angedruckt: 60 mm breit, 40 mm tief, von 90 mm bis 250 mm Höhe, mit weich gerundeten Kanten, einem flachen Deckel auf vier kleinen M2,5-Schrauben, einer USB-C-Buchse und einem kleinen LED-Fenster mit einer roten und einer grünen Leuchtdiode in der Deckelfläche; unten endet der Turm mit einer 45-Grad-Abschärfung und einer Tropfkante. Der Turm ist allseitig geschlossen, seine Innereien sind von außen nicht sichtbar.

Unten, knapp über der Trennfuge in etwa 68 bis 84 mm Höhe und auf der dem Turm gegenüberliegenden Seite, sitzt ein kurzer Einfüllstutzen, der 45 Grad nach oben und außen aus der unteren Schale herausragt: 25 mm Außendurchmesser, 22 mm Länge, mit einer gerippten Steckkappe von 30 mm Durchmesser und einem kleinen Lüftungsloch in der Kappe. Er gehört zum Wassertank, nicht zum Erdbehälter, und liegt deutlich unterhalb der Topfmitte.

Im Erdbehälter wächst eine gesunde, buschige Cannabis-Pflanze mit breiten, gezackten Blättern mittig aus dem Topf. Auf der dunklen, leicht feuchten Substratoberfläche liegt lose ein gedruckter Verteilerring von 105 mm Durchmesser mit acht bis zwölf feinen Austrittsbohrungen nach innen unten und einem kurzen Silikon-Schlauchstutzen, der zum Elektronik-Turm zeigt; der Ring ist nicht in die Erde gedrückt. Ein schmaler grüner kapazitiver Feuchtesensor, ein langes Platinenband von etwa 98 mal 23 mm, steckt von oben senkrecht im Substrat, knapp innerhalb der Topfwand, sodass seine Elektrodenmitte 75 mm tief liegt und die Oberkante nur knapp über dem Substrat herausschaut; sein dünnes Kabel verlässt den Topf über den Kragen, hängt in einer kleinen Tropfschlaufe und verschwindet im Turm. Am Kragenrand klemmt ein kleiner 3D-gedruckter Clip, in dem ein kleiner externer Lichtsensor an kurzem Kabel sitzt.

Der Topf besteht ausschließlich aus gedrucktem Kunststoff. Er ist ein einziges Objekt ohne Zubehör: kein Alu-Profil, kein Metallrahmen, keine Griffe, kein zweiter Turm, kein Display, kein Sichtfenster, kein Aufdruck, kein Logo, keine Schrift, kein Wasserstand von außen sichtbar, kein Schlauch und kein Kabel außerhalb des Topfs, keine zweite Pumpe daneben auf dem Boden, kein Aquarium-Look, keine Pfütze.

Beleuchtung und Optik: Dreiviertelansicht leicht über Augenhöhe des Topfs, sodass der Verteilerring auf dem Substrat und der Kragen mit den Ankerlöchern sichtbar sind. 85 mm Objektiv bei Blende f/8, praktisch verzeichnungsfrei, knackscharf auf Turmdeckel, Kragen, Substrat und Einfüllstutzen, nur die äußersten Blattspitzen laufen weich. Große Softbox von oben links, schmaler Strip als Kante von hinten rechts, sehr weiche, kurze Schlagschatten unter dem Topf. Nahtloser heller Studiohintergrund, cremeweiß nach hellgrau verlaufend, keine Requisiten, kein Bodenmuster. Farbklima neutral bis leicht kühl, ehrlich statt werblich: Substrat dunkelbraun, Blätter sattes Grün, Topf hellgrau mit sauber lesbaren Druckschichten. Hochauflösend, detailreich, wie ein Katalogfoto eines Prototyps. Hochformat 4:5.
```

---

# Prompt 2 · Aufgeschnittene Ansicht — wie es funktioniert

```text
Technische 3D-Schnittdarstellung eines 3D-gedruckten, zylindrischen Pflanzentopfs als Halbschnitt: Die vordere Hälfte von Außenschale, Erdbehälter und Wassertank ist sauber weggeschnitten, die Schnittkanten sind matte, hellere Schnittflächen mit dünner dunkler Kontur, das Innere ist vollständig und räumlich klar einsehbar. Die Schnittebene geht durch die Mittelachse und durch den Elektronik-Turm.

Der Topf: Außendurchmesser 140 mm, Gesamthöhe 278 mm ohne Pflanze, die Höhe ist also etwa das Doppelte des Durchmessers. Werkstoff mattes hellgraues PETG mit feinen, sichtbaren FDM-Schichtlinien. Eine glatte waagerechte Trennfuge läuft bei etwa 90 mm Höhe um den Zylinder. Der untere Teil ist der geschlossene Wassertank mit 1,0 Liter Inhalt, darüber folgt eine 30 mm hohe Luftkammer, darüber der Erdbehälter, und ganz oben schließt ein 12 mm hoher, leicht überstehender Kragenring ab, in dem zwei versetzte umlaufende Reihen kleiner Ankerlöcher von 2 mm Durchmesser sitzen. An einer Seite ist ein rechteckiger Elektronik-Turm direkt an den Zylinder angedruckt: 60 mm breit, 40 mm tief, von 90 mm bis 250 mm Höhe, mit einem flachen Deckel auf vier kleinen M2,5-Schrauben, einer USB-C-Buchse und einem kleinen LED-Fenster in der Deckelfläche, unten mit 45-Grad-Abschärfung und Tropfkante. Der Turm ist im Schnitt ebenfalls geöffnet, sodass sein Inhalt sichtbar ist. Unten, knapp über der Trennfuge in etwa 68 bis 84 mm Höhe und auf der dem Turm gegenüberliegenden Seite, ragt ein kurzer Einfüllstutzen 45 Grad nach oben und außen aus der unteren Schale heraus, 25 mm Außendurchmesser, mit gerippter Steckkappe und kleinem Lüftungsloch; er gehört zum Wassertank und nicht zum Erdbehälter. Im Erdbehälter wächst eine buschige Cannabis-Pflanze mit breiten gezackten Blättern mittig aus dem Topf, auf dem Substrat liegt ein gedruckter Verteilerring von 105 mm Durchmesser mit acht bis zwölf feinen Austrittsbohrungen nach innen unten.

Das Innenleben, von oben nach unten: Im Erdbehälter steckt dunkles, körniges Substrat. Am Boden des Erdbehälters liegt eine 25 mm dicke Schicht aus runden braunen Blähton-Kugeln als Drainage und Partikelfilter, darunter eine abnehmbare, gelochte Auflageplatte mit feinem Sieb. Unter dieser Platte öffnet sich ein 30 mm hoher Luftspalt, der das Substrat vom Wasser trennt. Darunter liegt der zylindrische Wassertank mit 1,0 Liter Inhalt, der Wasserstand steht etwa 70 mm hoch, das Wasser ist klar. Ein schmaler grüner kapazitiver Feuchtesensor steckt senkrecht im Substrat, knapp innerhalb der Topfwand, mit seiner Elektrodenmitte 75 mm tief; sein dünnes Kabel verlässt den Topf über den Kragen und verschwindet mit einer Tropfschlaufe im Turm.

Im aufgeschnittenen Elektronik-Turm, alles vollständig über dem Wasserstand: unten zwei kleine Pumpen nebeneinander — die weiße Peristaltikpumpe mit ihrem runden Schlauchkopf und etwa 42 mm Bauhöhe, daneben die flache weiße Membran-Luftpumpe mit Gummifüßen und ihrem kleinen Luftansaugstutzen, der zu einem schmalen Lüftungsschlitz in der Turmwand zeigt. Darüber die grüne Leiterplatte von etwa 60 mal 38 mm mit dem silbernen ESP32-C6-Funkmodul, Kondensatoren, zwei kleinen aufrechten weißen Steckern, einem USB-C-Anschluss und zwei Leuchtdioden. Daneben hochkant das flache, in Schrumpffolie eingepackte 2S-Lithium-Akkupack mit dreipoligem Kabel und Stecker. Vom Tankboden führt ein dünner Silikonschlauch von 3 mal 5 mm senkrecht nach oben in die Peristaltikpumpe, unten endet er in einem kleinen Saugkorb mit Gewicht; vom Pumpenkopf läuft der Druckschlauch nach oben, über den Kragen hinweg und hinunter zum Verteilerring auf der Substratoberfläche. Von der Luftpumpe im Turm führt ein zweiter dünner Silikonschlauch nach unten in den Wassertank zu einem weißen, porösen Luftsprudlerstein, etwa ein 30 mm langer Zylinder aus Sintermaterial, der auf dem Tankboden liegt; feine Luftblasen steigen von ihm im Wasser auf.

Der Wasserweg ist als leuchtend cyanfarbener Pfad dargestellt: aus dem Tank senkrecht durch den Saugschlauch nach oben in die Pumpe, als heller Strang durch den Druckschlauch über den Kragen, in den Verteilerring und dann als acht bis zwölf feine Tropfenfäden gleichmäßig in das dunkle Substrat, dort als sickernde Flüssigkeit nach unten durch Blähton und Lochplatte zurück in den Tank. Der Luftweg ist als heller perlweißer Pfad dargestellt: aus der Luftpumpe im Turm durch den Silikonschlauch in den Tank und dort als aufsteigende Kette feiner Luftblasen aus dem Sprudlerstein.

Optik: sauberes redaktionelles Infografik-Rendering, freigestelltes Objekt vor dunklem, ruhigem Hintergrund, weiche Studiobeleuchtung, feine Maßstabsstriche ohne Zahlen. Das Bild enthält keinerlei Schrift, keine Buchstaben, keine Zahlen, keine Legende, keine Pfeilbeschriftungen, keine Maße. Hochformat (9:16).
```

---

# Prompt 3 · Technische Zeichnung mit Schnitt

```text
Technische Konstruktionszeichnung eines 3D-gedruckten, zylindrischen Pflanzentopfs auf reinweißem Papier, feine schwarze Tusche- und CAD-Linien, einheitliche Strichstärken, keine Schattierung, kein Rendering, kein Foto, keine Farbe außer Schwarz auf Weiß und einem einzigen zurückhaltenden Grau für Schnittflächen. Drei orthografische Ansichten sind sauber auf dem Blatt ausgerichtet.

Der Topf: Außendurchmesser 140 mm, Gesamthöhe 278 mm ohne Pflanze, also etwa doppelt so hoch wie breit. Eine waagerechte Trennfuge bei etwa 90 mm Höhe teilt ihn in eine untere Schale, die den geschlossenen Wassertank mit 1,0 Liter bildet, und eine obere Schale mit Erdbehälter; dazwischen liegen 30 mm Luftspalt und eine gelochte Auflageplatte. Oben schließt ein 12 mm hoher Kragenring ab, in dem zwei versetzte umlaufende Reihen kleiner Ankerlöcher von 2 mm Durchmesser sitzen. An einer Seite ist ein rechteckiger Elektronik-Turm angedruckt: 60 mm breit, 40 mm tief, von 90 bis 250 mm Höhe, mit flachem Deckel auf vier kleinen Schrauben, USB-C-Buchse und einem kleinen LED-Fenster; unten endet er mit 45-Grad-Abschärfung. Unten, knapp über der Trennfuge in etwa 68 bis 84 mm Höhe und auf der dem Turm gegenüberliegenden Seite, ragt ein Einfüllstutzen 45 Grad nach oben und außen heraus, 25 mm Außendurchmesser und 22 mm lang, mit einer gerippten Steckkappe von 30 mm Durchmesser und einem kleinen Lüftungsloch in der Kappe; er gehört zum Wassertank, nicht zum Erdbehälter. Auf dem Substrat im Erdbehälter liegt ein gedruckter Verteilerring von 105 mm Durchmesser mit acht bis zwölf Austrittsbohrungen nach innen unten, und ein schmaler kapazitiver Feuchtesensor steckt senkrecht im Substrat nahe der Topfwand, mit seiner Elektrodenmitte 75 mm tief.

Die drei Ansichten: Oben links die Vorderansicht mit sichtbarem Elektronik-Turm, unten liegendem Einfüllstutzen mit Kappe, Kragen und Ankerlöchern sowie der Pflanze, versehen mit Maßlinien, Maßhilfslinien, Maßpfeilen und Maßgrenzen, aber ohne Zahlen. Oben rechts die Draufsicht von oben auf den Kragen mit den Ankerloch-Reihen, den auf dem Substrat liegenden Verteilerring mit seinen Austrittsbohrungen und den daneben eingesteckten Sensor. Darunter über die volle Blattbreite der Längsschnitt durch die Mittelachse mit dicht schraffierten Schnittflächen: darin sind Wassertank mit Wasserstandslinie, 30 mm Luftspalt, gelochte Auflageplatte, 25 mm Blähton-Schicht, Erdbehälter mit Substrat, Druckschlauch zum Verteilerring, Saugschlauch mit Saugkorb, der Luftsprudlerstein auf dem Tankboden mit aufsteigenden Blasen sowie im aufgeschnittenen Turm die Peristaltikpumpe, die flache Membran-Luftpumpe, die Leiterplatte und das hochkant stehende Akkupack klar erkennbar. Rechts unten als kleine Beigabe eine axonometrische Explosionsskizze der Druckteile, entlang der Mittelachse auseinandergezogen und mit dünnen gestrichelten Verbindungslinien: Kappe, Kragen, obere Schale mit Verteilerring und Sensor, Innentopf, Lochplatte, untere Schale mit Einfüllstutzen. Schnittmarken und Achsenkreuze sind erlaubt.

Das Blatt enthält keine Schrift und keine Zahlen: kein Titel, keine Legende, keine Positionsnummern, keine Maßzahlen, keine Notizen, kein Firmenlogo, kein Maßstabstext, keine Materialangabe. Kein kariertes Papier, kein Lineal, kein Bleistift, keine Hand im Bild, keine Hintergrundfarbe. Querformat (3:2).
```

### Optional: Beschriftung doch generieren lassen

Gemini kann kurze Beschriftungen inzwischen halbwegs rendern (deutlich besser als Flux/SDXL), aber
Buchstabenfehler bleiben wahrscheinlich. Wenn du es probieren willst, hänge diesen Satz an Prompt 3 an:

```text
Ergänze zum Schnittbild eine Legende mit nummerierten Kreisen und kurzen deutschen Bezeichnungen: 1 Deckel, 2 Elektronik-Turm, 3 Leiterplatte, 4 Akkupack, 5 Peristaltikpumpe, 6 Luftpumpe, 7 Feuchtesensor, 8 Verteilerring, 9 Substrat, 10 Blähton, 11 Lochplatte, 12 Wassertank, 13 Sprudlerstein, 14 Einfüllstutzen, 15 Kragen mit Ankerlöchern. Saubere deutsche Schrift, korrekt geschrieben, keine Fantasiebuchstaben.
```

Für Prompt 1 und 2 würde ich ohne Schrift arbeiten — dort wirkt Text im Bild wie ein Fehler.

---

## Nutzung mit Gemini

1. **Kein Negativ-Prompt.** Gemini/Imagen nimmt keinen separaten Negativ-Block; Verbote stehen deshalb
   als Sätze **im** Prompt („Der Topf ist ein einziges Objekt ohne Zubehör: … keine zweite Pumpe
   daneben, keine Schrift im Bild"). Wenn ein Fehler trotzdem kommt: den betroffenen Satz nach oben
   ziehen und die Formulierung schärfen — nicht mehr Lob, sondern mehr Ausschluss im Fließtext.
2. **Format** über die Oberfläche/`aspect_ratio` einstellen (4:5, 9:16, 3:2); die Angabe im Prompt ist
   nur eine Zusatzhilfe.
3. **Reihenfolge:** Bei Gemini zählt der Anfang am stärksten. Deshalb steht in jedem Prompt zuerst, was
   das Bild **ist** und wie das Objekt heißt, dann die Geometrie, die Optik zuletzt.
4. **Nachfassen im Chat statt neu würfeln:** Ein fertiges Bild im selben Chat weiterbearbeiten
   („jetzt die Schnittansicht des Turms größer", „Einfüllstutzen tiefer setzen") bringt meist einen
   besseren Treffer als ein neuer Prompt-Durchlauf.

---

## Prüfkriterien für die erzeugten Bilder (vor dem Verwenden)

1. Proportion: Höhe ≈ 2 × Durchmesser, zylindrisch, nicht bauchig und nicht konisch.
2. **Genau ein** Turm an der Seite, geschlossen, mit Deckel, USB-C und LED-Fenster; **nichts steht
   neben dem Topf**, kein zweites Gerät, kein Schlauch nach draußen.
3. **Einfüllstutzen unten:** knapp über der Trennfuge, 45° nach oben außen, auf der dem Turm
   **gegenüberliegenden** Seite — nicht am Kragen, nicht neben dem Turm, nicht oben an der Erde.
4. Kragen oben trägt die Ankerloch-Reihen (feine, gleichmäßige Lochreihe), nicht nur eine Rille.
5. Ring liegt **auf** dem Substrat, Pflanze entspringt mittig, Sensor steckt **neben** dem Ring in
   Wandnähe, nicht mittig in der Erde.
6. Prompt 2/3: Beide Pumpen sind **im Turm** zu sehen; im Wasser liegt **nur** der Sprudlerstein mit
   aufsteigenden Blasen, kein Stein und keine Pumpe im Substrat.
7. Prompt 2/3: Wassertank, 30 mm Luftspalt, Lochplatte und 25 mm Blähton müssen als getrennte Zonen
   erkennbar sein — sonst erklärt der Schnitt nichts.
8. Kein sichtbarer Wasserstand von außen, kein „Aquarium"-Look, keine Kabelage oder Schläuche außen.

---

## Offene Punkte (bitte gegenprüfen)

- **Die Doku sagt noch „außen":** `docs/02_architektur-und-geometrie.md` §3/§6.4 und
  `hardware/bom_entscheidung.md` §8 verlangen den Einbauort der Sauerstoffpumpe **außerhalb des Topfs**
  (Membranpumpe braucht Frischluft). Nach deiner Vorgabe sitzt sie **im Turm** — die Dokumente und die
  Geometrie (`cad/params.py`) sind entsprechend nachzuziehen.
- **Lufteinlass:** Eine Membranpumpe im geschlossenen Turm zieht sonst ihre eigene Abluft. In den
  Prompts ist dafür ein **schmaler Lüftungsschlitz** in der Turmwand dargestellt — das ist eine
  Annahme von mir, keine festgelegte Konstruktion.
- **Platz im Turm:** 60 × 40 mm, 160 mm hoch, darin bisher Peristaltikpumpe (42 mm hoch), Platine und
  das 2S-Akkupack. Die zweite Pumpe kommt dazu — die Innenaufteilung sollte vor dem nächsten
  CAD-Schritt neu gerechnet werden.
- **Der Eintritt des Luftschlauchs in den Tank** ist konstruktiv noch nicht festgelegt; die Bilder
  zeigen ihn durch den Turm nach unten in den Tank.
- **Pflanzengröße ist Deko:** gezeigt ist eine vegetierende Pflanze; das Gerät sieht in der Blüte
  identisch aus.

## Pflege

- Geometrie ändert sich → **erst** `docs/02_architektur-und-geometrie.md` + `cad/params.py` anpassen,
  dann den Geometrie-Absatz **in allen drei Prompts** nachziehen. Nie umgekehrt: das Bild ist
  Ableitung, nicht Quelle.
- Neue Perspektiven ohne Umbau: Geometrie-Absätze behalten und nur Optik/Ansicht austauschen
  (Makro des Sprudlersteins im Tank, Detailschnitt durch den Turm mit beiden Pumpen, Draufsicht,
  Laden per USB-C).
