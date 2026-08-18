# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from findbook_writer import NATURAL_COLON_SUFFIXES

path = Path(__file__).with_name("write_34_36_highlights.py")
text = path.read_text(encoding="utf-8")
mod = {"__file__": str(path), "__name__": "x"}
exec(compile(text.replace('if __name__ == "__main__":', "if False:"), str(path), "exec"), mod)

out = []
for name in ["B34", "B35", "B36"]:
    bad = []
    for i, body in enumerate(mod[name], 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            bad.append(f"{i:03d}\t{match.group(1)}\t{body}")
    out.append(f"## {name} ({len(bad)})")
    out.extend(bad)
    out.append("")

Path(__file__).with_name("colon_bad.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote colon_bad.txt")
