# -*- coding: utf-8 -*-
import json
from pathlib import Path

old = json.loads(
    Path("Books/02_psychology_growth/02_psychology_growth-20260716-101.json").read_text(
        encoding="utf-8-sig"
    )
)
oldb = {x.split("、", 1)[1].strip() for x in old["chatgptHighlights"]}
text = Path("tools/_gen_grok_253_257.py").read_text(encoding="utf-8")
start = text.index("B256 = [")
end = text.index("assert len(B256)")
chunk = text[start:end]
bodies = []
for line in chunk.splitlines():
    s = line.strip()
    if s.startswith('"') and s.endswith('",'):
        bodies.append(json.loads(s[:-1]))
    elif s.startswith('"') and s.endswith('"'):
        bodies.append(json.loads(s))
print("count", len(bodies))
Path("tools/_tmp_overlap256.txt").write_text(
    "\n".join(["COPY: " + b for b in bodies if b in oldb]),
    encoding="utf-8",
)
