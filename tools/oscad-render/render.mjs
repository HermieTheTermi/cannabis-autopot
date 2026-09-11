#!/usr/bin/env node
/**
 * Headless OpenSCAD-Renderer (WebAssembly).
 *
 * Warum: Das Homebrew-Cask `openscad` ist seit 2026-09-01 deaktiviert (Gatekeeper),
 * Docker ist auf diesem Rechner nicht vorhanden. Dieser Renderer nutzt denselben
 * OpenSCAD-Kern über WebAssembly und läuft ohne GUI-Installation.
 *
 * Nutzung:
 *   node render.mjs <main.scad> [-o ausgabe.stl] [-D name=wert ...]
 *
 * Verhalten:
 *   - lädt ALLE .scad-Dateien aus dem Verzeichnisbaum der Hauptdatei in das
 *     virtuelle Dateisystem (damit `include`/`use` aufgelöst werden),
 *   - rendert die Hauptdatei mit voller CGAL-Geometrie (kein Preview),
 *   - schreibt das STL und meldet Fehler/Warnungen auf stderr,
 *   - Exit-Code 0 nur bei fehlerfreiem Render.
 */
import { createOpenSCAD } from "openscad-wasm-prebuilt";
import fs from "node:fs";
import path from "node:path";

const argv = process.argv.slice(2);
if (argv.length === 0) {
  console.error("Nutzung: node render.mjs <main.scad> [-o ausgabe.stl] [-D name=wert ...]");
  process.exit(2);
}

const mainArg = argv[0];
const outIdx = argv.indexOf("-o");
const outPath = outIdx >= 0 ? argv[outIdx + 1] : mainArg.replace(/\.scad$/i, ".stl");
const defines = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === "-D" && argv[i + 1]) defines.push(argv[i + 1]);
}

const mainAbs = path.resolve(mainArg);
if (!fs.existsSync(mainAbs)) {
  console.error(`FEHLER: ${mainAbs} existiert nicht`);
  process.exit(2);
}
const root = path.dirname(mainAbs);

// Alle .scad-Dateien unterhalb des Hauptverzeichnisses einsammeln (include/use).
const scadFiles = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === "node_modules" || e.name.startsWith(".") || e.name === "export") continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (e.name.toLowerCase().endsWith(".scad")) scadFiles.push(p);
  }
})(root);

const logs = [];
const oscad = await createOpenSCAD({
  print: (s) => logs.push(s),
  printErr: (s) => logs.push(s),
});
const inst = oscad.getInstance();

const toVirtual = (abs) => "/" + path.relative(root, abs).split(path.sep).join("/");

for (const f of scadFiles) {
  const vPath = toVirtual(f);
  const parts = path.posix.dirname(vPath).split("/").filter(Boolean);
  let cur = "";
  for (const p of parts) {
    cur += "/" + p;
    try {
      inst.FS.mkdir(cur);
    } catch {
      /* existiert bereits */
    }
  }
  inst.FS.writeFile(vPath, fs.readFileSync(f, "utf8"));
}

const vMain = toVirtual(mainAbs);
const vOut = "/out.stl";
const cliArgs = ["-o", vOut, ...defines.flatMap((d) => ["-D", d]), vMain];

let exitCode = 0;
try {
  exitCode = inst.callMain(cliArgs);
} catch (e) {
  // Emscripten wirft beim Programmende ExitStatus-Objekte.
  if (e && typeof e === "object" && "status" in e) exitCode = e.status ?? 0;
  else throw e;
}

const logText = logs.join("\n");
const relevant = logText
  .split("\n")
  .filter(
    (l) =>
      /ERROR|WARNING|not 2-manifold|empty|Simple:|Vertices:|Facets:|Volumes:|rendering time/i.test(
        l,
      ) && !/Could not initialize localization/i.test(l),
  )
  .join("\n");

let stl = null;
try {
  stl = Buffer.from(inst.FS.readFile(vOut, { encoding: "binary" }));
} catch {
  stl = null;
}

if (!stl || stl.length === 0) {
  console.error("RENDER FEHLGESCHLAGEN — kein STL erzeugt.\n" + relevant);
  process.exit(1);
}

const outAbs = path.resolve(outPath);
fs.mkdirSync(path.dirname(outAbs), { recursive: true });
fs.writeFileSync(outAbs, stl);

// Facettenzahl aus dem STL zählen (ASCII oder Binär).
let facets = null;
const head = stl.subarray(0, 5).toString("ascii");
if (head === "solid") {
  facets = (stl.toString("utf8").match(/facet normal/g) || []).length;
} else {
  facets = stl.readUInt32LE(80);
}

const geometrieWarnung = /not 2-manifold/i.test(logText);
// Harte Fehler, die trotz Exit-Code 0 ein kaputtes Modell bedeuten.
const harteFehler = /ERROR:|Ignoring unknown|unknown module|unknown function|unknown variable|Parse error|syntax error|Current top level object is empty/i.test(
  logText,
);
console.log(`OK  ${path.relative(process.cwd(), outAbs)}  ${stl.length} Bytes  ${facets} Facetten`);
if (relevant) console.log(relevant);
if (defines.length) console.log("Defines: " + defines.join(", "));

if (geometrieWarnung || harteFehler) {
  console.error(
    `WARNUNG: ${geometrieWarnung ? "Geometrie ist nicht 2-manifold. " : ""}${
      harteFehler ? "Modell enthält Fehler (siehe Log oben)." : ""
    }`,
  );
  process.exit(1);
}
process.exit(exitCode === 0 ? 0 : exitCode);
