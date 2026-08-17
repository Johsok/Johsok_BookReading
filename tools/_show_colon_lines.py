# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from findbook_writer import NATURAL_COLON_SUFFIXES, NUMBER_RE  # noqa: E402

COLON_RE = re.compile(r"^([^：:]{1,12})[：:]")
book_id = sys.argv[1]
payload = json.loads((TOOLS / f".findbook_results_grok_{book_id}.json").read_text(encoding="utf-8-sig"))
out = []
for line in payload["highlights"]:
    body = NUMBER_RE.sub("", line, count=1).strip()
    match = COLON_RE.match(body)
    if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
        out.append(line)
    for prefix in ("本書", "作者指出", "本章", "這一章"):
        if prefix in body:
            out.append(f"FORBIDDEN {prefix}: {line}")
report = TOOLS / f".redo_colon_{book_id}.txt"
report.write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(out))
