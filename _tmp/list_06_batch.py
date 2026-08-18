# -*- coding: utf-8 -*-
import json
import pathlib

files = [
    "06_computer_info-20260716-66.json",
    "06_computer_info-20260716-67.json",
    "06_computer_info-20260716-68.json",
    "06_computer_info-20260716-69.json",
    "06_computer_info-20260716-70.json",
    "06_computer_info-20260716-71.json",
    "06_computer_info-20260717-01.json",
    "06_computer_info-20260717-02.json",
    "06_computer_info-20260717-03.json",
    "06_computer_info-20260717-04.json",
    "06_computer_info-20260717-05.json",
    "06_computer_info-20260717-06.json",
    "06_computer_info-20260717-07.json",
    "06_computer_info-20260717-08.json",
    "06_computer_info-20260717-09.json",
    "06_computer_info-20260717-10.json",
]
base = pathlib.Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\06_computer_info")
out = []
for f in files:
    raw = (base / f).read_text(encoding="utf-8-sig")
    d = json.loads(raw)
    out.append({
        "file": f,
        "id": d["id"],
        "title": d["title"],
        "author": d.get("author", ""),
        "hl": len(d.get("chatgptHighlights", [])),
    })
path = pathlib.Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\meta_06_66_10.json")
path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", path)
