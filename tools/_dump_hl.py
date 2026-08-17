# -*- coding: utf-8 -*-
from pathlib import Path

text = Path("tools/_rewrite_71_75.py").read_text(encoding="utf-8")
parts = text.split("r'''")
out = Path("tools/_dump_hl.txt")
chunks = []
for i, part in enumerate(parts[1:3], 1):
    body = part.split("'''", 1)[0]
    lines = [ln.strip() for ln in body.strip().splitlines() if ln.strip()]
    chunks.append(f"BOOK {i} N={len(lines)}")
    for n, ln in enumerate(lines, 1):
        chunks.append(f"{n:03d}|{ln}")
    chunks.append("---END---")
out.write_text("\n".join(chunks) + "\n", encoding="utf-8")
print(out, "written")
