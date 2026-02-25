#!/usr/bin/env python3
import os
import re
import json

BASE = os.path.expanduser("~/ .openclaw/workspace-donna/openapi-all".replace(" ", ""))
OUT = os.path.join(os.path.dirname(__file__), "..", "MODULES.md")

files = sorted([f for f in os.listdir(BASE) if f.endswith(".yml")])

modules = []
for f in files:
    path = os.path.join(BASE, f)
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    title = None
    for line in text.splitlines():
        if line.startswith("  title:"):
            title = line.split(":",1)[1].strip()
            break
        if line.startswith("title:"):
            title = line.split(":",1)[1].strip()
            break
    endpoints = []
    in_paths = False
    for line in text.splitlines():
        if line.startswith("paths:"):
            in_paths = True
            continue
        if in_paths:
            if re.match(r"^\S", line):
                # left root level
                in_paths = False
                continue
            m = re.match(r"^\s{2}(/[^:]+):", line)
            if m:
                endpoints.append(m.group(1))
    modules.append({
        "file": f,
        "title": title or f,
        "endpoints": endpoints,
        "count": len(endpoints),
    })

with open(OUT, "w", encoding="utf-8") as out:
    out.write("# Zoho Books API Modules (from openapi-all)\n\n")
    out.write(f"Source: {BASE}\n\n")
    for m in modules:
        out.write(f"## {m['title']} ({m['count']})\n")
        out.write(f"File: `{m['file']}`\n\n")
        if m['endpoints']:
            out.write("Endpoints:\n")
            for ep in m['endpoints']:
                out.write(f"- `{ep}`\n")
        out.write("\n")

print(f"Wrote {OUT}")
