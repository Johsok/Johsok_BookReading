# -*- coding: utf-8 -*-
from pathlib import Path

p = Path("tools/_hl_batch_183_187.py")
text = p.read_text(encoding="utf-8")
old = '。"\n        "'
new = '。",\n        "'
count = text.count(old)
text = text.replace(old, new)
p.write_text(text, encoding="utf-8")
print("replacements", count)
