# Bildkonzepte & Prompts für KI-Bildmodelle

Stand: 11.09.2026 · Geometrie-Quelle: `docs/02_architektur-und-geometrie.md` + `cad/` (am Modell gerendert und visuell geprüft)

**Jeder der fünf Prompts ist vollständig und self-contained** — reinkopieren, fertig.
Der Geometrie-Absatz steckt in jedem Prompt drin (identischer Wortlaut), danach folgt der Stil-Teil
und die Negative-Zeile. Copy-Paste-Version ohne Doku: **`04_bildkonzepte-prompts.txt`**
(aus dieser Datei generiert, keine Doppelpflege).

Hinweis: KI-Bildmodelle können keine Beschriftung. Beschriftungen/Schnittmarken im Nachhinein
setzen (Figma/Canva), nicht generieren lassen.

---

## 1 · Product-Hero (Studiofreisteller)

Einsatz: Landingpage / Titelbild. Parameter: Flux dev 30–40 Steps, Guidance 3.5 · Midjourney `--ar 4:5 --style raw`

```text
3D-printed cylindrical plant pot, exactly 140 mm diameter and 278 mm total height, height about twice the diameter. Matte light-grey PETG, fine FDM layer lines visible, one smooth horizontal seam line about 90 mm above the base where two printed shell halves meet. A rectangular equipment tower is fused onto one side of the cylinder: 60 mm wide, 40 mm deep, reaching from one third of the height up to the top, with a flat lid fixed by four small M2.5 screws, a USB-C port and a tiny LED window on the lid face, and a 45-degree chamfer at its lower end. Around the open top sits a 12 mm collar ring with a small cable notch; a thin annular cover disc rests inside it. The pot is filled with dark substrate, and one healthy cannabis plant with broad serrated leaves grows out of the top. Loose on the substrate lies a printed drip ring, 105 mm diameter, with a short silicone tube stub pointing toward the equipment tower. One thin sensor cable leaves the collar notch, hangs in a small drip loop, and enters the tower. Only printed plastic parts: no metal frame, no glass, no display, no bezel, no branding, no text, no logos.

Photorealistic product photography, three-quarter front view, object centered and floating slightly above a seamless studio backdrop with a soft dark-grey to black gradient. Large octabox key light from top-left, strip light as rim from behind right, deep soft shadow under the base. Shot on 85 mm lens at f/8, low distortion, sharp on the lid seam and the collar ring, subtle softness on the leaf edges. Cold neutral color grade, product catalog style. Aspect 4:5.

Negative: text, letters, watermark, logo, labels, arrows overlay, wireframe, low-poly, distorted cylinder, oval pot, two side towers, glass window, LCD display, screws everywhere, tangled cables, aquarium reservoir, fish tank, wet floor, oversized plant, huge leaves, cluttered background, cartoon, plastic shiny toy look, overexposed, blurry
```

---

## 2 · Technische Explosionsdarstellung

Einsatz: BOM, Aufbau, Anleitung. Parameter: Flux dev Guidance 4.0

```text
3D-printed cylindrical plant pot, exactly 140 mm diameter and 278 mm total height, height about twice the diameter. Matte light-grey PETG, fine FDM layer lines visible, one smooth horizontal seam line about 90 mm above the base where two printed shell halves meet. A rectangular equipment tower is fused onto one side of the cylinder: 60 mm wide, 40 mm deep, reaching from one third of the height up to the top, with a flat lid fixed by four small M2.5 screws, a USB-C port and a tiny LED window on the lid face, and a 45-degree chamfer at its lower end. Around the open top sits a 12 mm collar ring with a small cable notch; a thin annular cover disc rests inside it. The pot is filled with dark substrate, and one healthy cannabis plant with broad serrated leaves grows out of the top. Loose on the substrate lies a printed drip ring, 105 mm diameter, with a short silicone tube stub pointing toward the equipment tower. One thin sensor cable leaves the collar notch, hangs in a small drip loop, and enters the tower. Only printed plastic parts: no metal frame, no glass, no display, no bezel, no branding, no text, no logos.

Technical exploded-view illustration in axonometric isometric projection, on a pure white background, objects separated vertically along the center axis with thin dashed leader lines between them. Top to bottom: annular cover disc, collar ring with cable notch, outer shell upper half with the equipment tower opened to show a small peristaltic pump and one printed circuit board, drip ring, inner pot with four cast feet, perforated drainage grid, outer shell lower half forming a closed water tank. Flat matte shading, thin dark outlines, soft ambient occlusion, muted grey and pale sand palette, engineering-drawing aesthetic, high clarity, no shadows on the floor. Aspect 3:2.

Negative: text, letters, watermark, logo, labels, numbers, arrows overlay, wireframe, photorealistic, depth of field, dramatic lighting, perspective, colored background, low-poly, distorted cylinder, oval pot, two side towers, glass window, LCD display, aquarium reservoir, cartoon, blurry
```

---

## 3 · Funktionsbild: Bewässerungsweg (Ghost-View)

Einsatz: Story/Reel/Post — erklärt in einem Bild, *wie* es arbeitet. Parameter: Flux dev Guidance 4.5

```text
3D-printed cylindrical plant pot, exactly 140 mm diameter and 278 mm total height, height about twice the diameter. Matte light-grey PETG, fine FDM layer lines visible, one smooth horizontal seam line about 90 mm above the base where two printed shell halves meet. A rectangular equipment tower is fused onto one side of the cylinder: 60 mm wide, 40 mm deep, reaching from one third of the height up to the top, with a flat lid fixed by four small M2.5 screws, a USB-C port and a tiny LED window on the lid face, and a 45-degree chamfer at its lower end. Around the open top sits a 12 mm collar ring with a small cable notch; a thin annular cover disc rests inside it. The pot is filled with dark substrate, and one healthy cannabis plant with broad serrated leaves grows out of the top. Loose on the substrate lies a printed drip ring, 105 mm diameter, with a short silicone tube stub pointing toward the equipment tower. One thin sensor cable leaves the collar notch, hangs in a small drip loop, and enters the tower. Only printed plastic parts: no metal frame, no glass, no display, no bezel, no branding, no text, no logos.

Educational cutaway illustration, dark charcoal background, the pot rendered as a semi-transparent glass-like ghost model with glowing cyan-white edges, internal structure visible. Bright cyan water flows as a luminous path: up out of the small pump inside the side tower, through a tube over the collar, down into the drip ring, then as fine droplets falling evenly into the dark substrate, and finally trickling down and back into the closed water tank at the bottom. Small glowing droplets and a few arrow-free flow lines indicate the cycle. Contrast: warm orange LED glow at the plant canopy, cool cyan for water. Clean editorial infographic style, volumetric glow, no labels, no text. Aspect 9:16.

Negative: text, letters, watermark, logo, numbers, labels, arrows overlay, wireframe, low-poly, distorted cylinder, oval pot, two side towers, glass window, LCD display, tangled cables, aquarium reservoir, fish tank, wet floor, blender logo, sci-fi spaceship, neon pink, cartoon, blurry
```

---

## 4 · Lifestyle / Maßstabsbild im Growzelt

Einsatz: zeigt Größe (27,8 cm) und Einsatzort, bewusst unglamourös. Parameter: Flux dev 25–30 Steps

```text
3D-printed cylindrical plant pot, exactly 140 mm diameter and 278 mm total height, height about twice the diameter. Matte light-grey PETG, fine FDM layer lines visible, one smooth horizontal seam line about 90 mm above the base where two printed shell halves meet. A rectangular equipment tower is fused onto one side of the cylinder: 60 mm wide, 40 mm deep, reaching from one third of the height up to the top, with a flat lid fixed by four small M2.5 screws, a USB-C port and a tiny LED window on the lid face, and a 45-degree chamfer at its lower end. Around the open top sits a 12 mm collar ring with a small cable notch; a thin annular cover disc rests inside it. The pot is filled with dark substrate, and one healthy cannabis plant with broad serrated leaves grows out of the top. Loose on the substrate lies a printed drip ring, 105 mm diameter, with a short silicone tube stub pointing toward the equipment tower. One thin sensor cable leaves the collar notch, hangs in a small drip loop, and enters the tower. Only printed plastic parts: no metal frame, no glass, no display, no bezel, no branding, no text, no logos.

Realistic lifestyle photo inside a small home grow tent: the pod stands on a light grey tent floor, one healthy cannabis plant about 40 cm tall growing from it, full-spectrum LED grow light above casting a soft magenta-and-white wash, white Mylar tent walls slightly reflective in the background, a small circulation fan blurred behind, a fabric pot and a watering can out of focus to the side. Natural imperfect framing, shot on 35 mm at f/2.8, shallow depth of field, handheld feel, slight sensor noise, honest documentary style rather than advertising gloss. Aspect 4:5.

Negative: text, letters, watermark, logo, labels, arrows overlay, wireframe, low-poly, distorted cylinder, oval pot, two side towers, glass window, LCD display, tangled cables, aquarium reservoir, fish tank, wet floor, oversized plant, huge leaves, studio backdrop, floating object, product rendering, perfect symmetry, glossy plastic, cartoon, blurry
```

---

## 5 · Industrial-Design-Konzeptskizze (Moodboard-Blatt)

Einsatz: Designraum öffnen — Varianten, Haptik, Materialien. Parameter: Flux dev

```text
3D-printed cylindrical plant pot, exactly 140 mm diameter and 278 mm total height, height about twice the diameter. Matte light-grey PETG, fine FDM layer lines visible, one smooth horizontal seam line about 90 mm above the base where two printed shell halves meet. A rectangular equipment tower is fused onto one side of the cylinder: 60 mm wide, 40 mm deep, reaching from one third of the height up to the top, with a flat lid fixed by four small M2.5 screws, a USB-C port and a tiny LED window on the lid face, and a 45-degree chamfer at its lower end. Around the open top sits a 12 mm collar ring with a small cable notch; a thin annular cover disc rests inside it. The pot is filled with dark substrate, and one healthy cannabis plant with broad serrated leaves grows out of the top. Loose on the substrate lies a printed drip ring, 105 mm diameter, with a short silicone tube stub pointing toward the equipment tower. One thin sensor cable leaves the collar notch, hangs in a small drip loop, and enters the tower. Only printed plastic parts: no metal frame, no glass, no display, no bezel, no branding, no text, no logos.

Industrial design concept sheet: three hand-drawn marker sketches of the same cylindrical pod in different design variants, arranged loosely on warm grey sketch paper — variant A as described, variant B with a narrower rounded tower blended into the cylinder, variant C with a two-tone upper shell in recycled-fiber dark grey and a sand-colored base. Loose confident black ballpoint construction lines, cool grey Copic marker shading, one thumbnail rendered in matte clay, dimension scribbles as abstract tick marks without readable text, a few color and material swatches (brushstroke samples: matte grey PETG, sand recycled, dark slate) in the lower corner. Designer sketchbook aesthetic, slightly imperfect, high resolution scan look. Aspect 3:2.

Negative: text, letters, watermark, logo, readable labels, numbers, digital painting, 3D render, photorealistic, neon, cyberpunk, low-poly, distorted cylinder, oval pot, two side towers, glass window, LCD display, cluttered background, cartoon, blurry
```

---

## Prüfkriterien für generierte Bilder (vor dem Verwenden)

1. Proportion: Höhe ≈ 2 × Durchmesser, zylindrisch (nicht bauchig/konisch).
2. **Genau eine** Wulst an der Seite, mit Deckel + 45°-Fase unten — nicht zwei, keine Griffe.
3. Kein sichtbares Fenster/Display, keine Metallrahmen, keine außen verlegten Schläuche.
4. Ring liegt **auf** dem Substrat, Pflanze entspringt **mittig** aus dem Topf.
5. Kein Wasserstand von außen sichtbar; kein „Aquarium"-Look.
6. Kein Text im Bild (gibt es nicht sauber — im Zweifel Bild verwerfen).

---

## Pflege

- Konzept-Änderungen: erst `docs/02_architektur-und-geometrie.md` + `cad/params.py` anpassen,
  dann den Geometrie-Absatz **in allen fünf Prompts** nachziehen — nie umgekehrt (Bild ist Ableitung,
  nicht Quelle).
- Nach jeder Änderung: `python3 scripts/split_prompts.py` → erzeugt `04_bildkonzepte-prompts.txt` neu.
- Neue Perspektiven ohne Umbau: Geometrie-Absatz behalten, Stil-Teil austauschen (Makro der Wulst,
  Draufsicht mit Verteilerring, flache Grafik/Icon).
