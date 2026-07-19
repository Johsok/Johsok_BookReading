# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = (ROOT / "tools" / "_gen_batch77.py").read_text(encoding="utf-8")
lines = src.splitlines()
i36 = next(i for i, l in enumerate(lines) if l.startswith("BOOK36"))
i37 = next(i for i, l in enumerate(lines) if l.startswith("BOOK37"))
i38 = next(i for i, l in enumerate(lines) if l.startswith("BOOK38"))


def extract_strings(chunk: str) -> list[str]:
    items = []
    for m in re.finditer(r'^\s*"((?:\\.|[^"\\])*)"', chunk, flags=re.M):
        s = m.group(1)
        if " thrush" in s or ".replace(" in s:
            continue
        items.append(s.encode("utf-8").decode("unicode_escape") if "\\u" in s else s)
    # The strings are already unicode in the file; don't escape-decode unnecessarily
    items = []
    for m in re.finditer(r'^\s*"(.*)"\s*,?\s*$', chunk, flags=re.M):
        s = m.group(1)
        if " thrush" in s or ".replace(" in s:
            continue
        items.append(s)
    return items


chunk36 = "\n".join(lines[i36:i37])
chunk37 = "\n".join(lines[i37:i38])
chunk38 = "\n".join(lines[i38:])
out = {
    "BOOK36": extract_strings(chunk36),
    "BOOK37": extract_strings(chunk37),
    "BOOK38": extract_strings(chunk38),
}
path = ROOT / "tools" / "_b77_partial.json"
path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print({k: len(v) for k, v in out.items()})
