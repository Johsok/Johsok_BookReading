# -*- coding: utf-8 -*-
import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
os.chdir(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\02_psychology_growth")
files = sorted(glob.glob("02_psychology_growth-20260724-*.json"))
out = []
for f in files:
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
    n = len(d.get("chatgptHighlights", []))
    out.append({"id": d["id"], "title": d["title"], "author": d["author"], "n": n, "file": f})
dest = r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\tools\_psych_book_list.json"
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(f"wrote {len(out)} books to {dest}")
