#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "MODULES.md"
OUT = ROOT / "COMMAND_MATRIX.md"

SECTION_RE = re.compile(r"^##\s+(.+?)\s+\(\d+\)")


def main():
    sections = []
    for line in MODULES.read_text().splitlines():
        m = SECTION_RE.match(line.strip())
        if m:
            sections.append(m.group(1))

    lines = [
        "# Zoho Books Command Matrix (WIP)",
        "",
        "Generated from MODULES.md — fill in concrete CLI commands per module.",
        "",
    ]
    for name in sections:
        lines += [
            f"## {name}",
            "",
            "- list",
            "- get",
            "- create",
            "- update",
            "- delete",
            "- actions: (status/email/submit/approve/etc — fill per module)",
            "",
        ]

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
