# oscad-render — headless OpenSCAD (WebAssembly)

Kleiner Renderer, der `.scad`-Dateien ohne GUI-Installation nach STL rendert.

**Warum nicht das native OpenSCAD?** Das Homebrew-Cask `openscad` wurde am 01.09.2026
deaktiviert („does not pass the macOS Gatekeeper check"), Docker ist auf diesem Rechner nicht
installiert. Derselbe OpenSCAD-Kern läuft als WebAssembly-Build aber einwandfrei.

## Nutzung

```bash
cd tools/oscad-render && npm install     # einmalig
node render.mjs <datei.scad> -o <ausgabe.stl>

Hinweis: Das Gehaeuse-CAD wurde am 14.09.2026 auf build123d umgestellt (`cad/`, siehe
`cad/README.md`). Dieser Renderer bleibt fuer einzelne SCAD-Dateien nutzbar.
```

Optionen:
- `-o <datei>` — Ausgabepfad (Standard: neben der Quelldatei)
- `-D name=wert` — Parameter überschreiben (mehrfach möglich, für Varianten/Testdrucke)

Alle `.scad`-Dateien im Verzeichnisbaum der Hauptdatei werden automatisch mitgeladen, damit
`include`/`use` funktionieren. Gerendert wird mit voller CGAL-Geometrie.

Exit-Code 0 = fehlerfrei (Facettenzahl wird ausgegeben). Exit-Code 1 = Fehler, unbekanntes
Modul/Variable, leeres Modell oder nicht-2-manifold-Geometrie.
