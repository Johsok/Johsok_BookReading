# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from findbook_writer import NATURAL_COLON_SUFFIXES

# Import lists without running main
path = Path(__file__).with_name("write_34_36_highlights.py")
text = path.read_text(encoding="utf-8")
# Execute only assignments
mod = {"__file__": str(path), "__name__": "x"}
exec(compile(text.replace('if __name__ == "__main__":', "if False:"), str(path), "exec"), mod)


for name in ["B34", "B35", "B36"]:
    bad = []
    for i, body in enumerate(mod[name], 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            bad.append((i, match.group(1), body[:40]))
    print(name, "short_colon", len(bad))
    for item in bad[:20]:
        print(" ", item)
