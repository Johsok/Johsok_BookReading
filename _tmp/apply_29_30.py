# -*- coding: utf-8 -*-
import json
from pathlib import Path
from collections import Counter

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
TMP = ROOT / "_tmp"
META = {
    "chatgptStatus": "complete",
    "highlightsSource": "grok",
    "highlightsCapturedAt": "2026-08-18T08:40:00+08:00",
    "updatedAt": "2026-08-18",
}


def load_lines(*parts):
    rows = []
    for part in parts:
        for line in Path(part).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(line)
    return rows


def validate(label, highlights):
    if len(highlights) != 150:
        raise SystemExit(f"{label} count {len(highlights)}")
    nums = [h.split("、", 1)[0] for h in highlights]
    if nums != [f"{i:03d}" for i in range(1, 151)]:
        raise SystemExit(f"{label} numbering")
    bodies = [h.split("、", 1)[1] for h in highlights]
    if len(set(bodies)) != 150:
        raise SystemExit(f"{label} duplicate body")
    opens = [b[:2] for b in bodies]
    dups = [k for k, v in Counter(opens).items() if v > 1]
    if dups:
        raise SystemExit(f"{label} repeat openings {dups}")
    joined = "\n".join(bodies)
    for ban in ("本書", "作者指出"):
        if ban in joined:
            raise SystemExit(f"{label} banned {ban}")
    return highlights


def apply(rel, highlights):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = highlights
    data.update(META)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(rel)
    print("COUNT", len(highlights))
    print("FIRST", highlights[0])
    print("LAST", highlights[-1])


h29 = validate("29", load_lines(TMP / "h29_a.txt", TMP / "h29_rest.txt"))
h30 = validate("30", load_lines(TMP / "h30_all.txt"))
apply("Books/07_other/07_other-20260717-29.json", h29)
apply("Books/07_other/07_other-20260717-30.json", h30)
