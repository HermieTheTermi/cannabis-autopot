#!/usr/bin/env python3
"""Splittet docs/04_bildkonzepte-prompts.md in eine reine Copy-Paste-Datei.

Quelle ist die .md (Single Source of Truth) - hier wird nur extrahiert, nie neu getextet.
Aufruf:  python3 scripts/split_prompts.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "04_bildkonzepte-prompts.md"
DST = ROOT / "docs" / "04_bildkonzepte-prompts.txt"

H2 = re.compile(r"^##\s+(\d+)\s*·\s*(.+?)\s*$", re.M)
BLOCK = re.compile(r"^```text\s*$(.*?)^```\s*$", re.S | re.M)


def main() -> int:
    md = SRC.read_text(encoding="utf-8")

    # Abschnitte "## 1 · Titel" mit dem jeweils folgenden ```text-Block
    sections: list[tuple[str, str]] = []
    heads = list(H2.finditer(md))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(md)
        body = md[h.end():end]
        m = BLOCK.search(body)
        if not m:
            print(f"FEHLER: kein ```text-Block in Abschnitt {h.group(1)}", file=sys.stderr)
            return 1
        sections.append((f"{h.group(1)} · {h.group(2)}", m.group(1).strip()))

    if len(sections) < 5:
        print(f"FEHLER: nur {len(sections)} Prompts gefunden (erwartet >= 5)", file=sys.stderr)
        return 1

    out = [
        "SMART GROW TOPF - KI-IMAGE-PROMPTS (Copy-Paste)",
        "=" * 60,
        "",
        "Jeder Block ist vollstaendig: Geometrie + Stil + Negative.",
        "Generiert aus docs/04_bildkonzepte-prompts.md - nicht hier editieren.",
        "",
    ]
    for title, prompt in sections:
        out += ["-" * 60, f"PROMPT {title}", "-" * 60, "", prompt, ""]

    DST.write_text("\n".join(out), encoding="utf-8")
    print(f"{len(sections)} Prompts -> {DST.relative_to(ROOT)} ({DST.stat().st_size} Bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
