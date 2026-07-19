# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).with_name("_gen_chunk14_highlights.py")
t = p.read_text(encoding="utf-8")
# _beck() via codepoints to avoid confusion with "letter"
old = "".join(chr(c) for c in (95, 98, 101, 99, 107, 40, 41))
new = "".join(chr(c) for c in (95, 97, 110, 120, 105, 101, 116, 121, 40, 41))
print("old", old, "count", t.count(old))
t2 = t.replace(old, new)
if t == t2:
    raise SystemExit("no change")
p.write_text(t2, encoding="utf-8")
print("replaced ok")
