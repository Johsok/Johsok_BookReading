# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).with_name("_gen_pg_38_42.py")
text = p.read_text(encoding="utf-8")
needle = '        "被推遲的事被看見，粗暴改道才可能轉成有意識的轉向。",'
start = text.find(needle)
if start < 0:
    raise SystemExit("needle missing")
end = text.find("    ],\n))\n\n\ndef main()", start)
if end < 0:
    raise SystemExit("end missing")
new = text[:start] + needle + "\n" + text[end:]
p.write_text(new, encoding="utf-8")
print("trimmed")
