# -*- coding: utf-8 -*-
import json
import re
from collections import defaultdict
from pathlib import Path


def cjk(s: str) -> int:
    return sum(1 for c in s if "\u4e00" <= c <= "\u9fff")


def check(path: Path) -> str:
    d = json.loads(path.read_text(encoding="utf-8-sig"))
    hs = d["chatgptHighlights"]
    bodies = [h.split("、", 1)[1] for h in hs]
    errs = []
    if len(hs) != 150:
        errs.append(f"count={len(hs)}")
    if d.get("chatgptStatus") != "complete":
        errs.append("status")
    if d.get("highlightsSource") != "grok":
        errs.append("source")
    if d.get("highlightsCapturedAt") != "2026-08-18T09:10:00+08:00":
        errs.append("cap")
    if d.get("updatedAt") != "2026-08-18":
        errs.append("upd")
    g = defaultdict(list)
    colon = 0
    yanyi = 0
    ns = [cjk(b) for b in bodies]
    for i, b in enumerate(bodies, 1):
        n = ns[i - 1]
        if n < 32 or n > 68:
            errs.append(f"len{i}:{n}")
        colon += len(re.findall(r"[：:]", b))
        if b.startswith("演義"):
            yanyi += 1
        for bad in ("本書", "作者指出", "本章", "這一章", "｜", "盛唐也瘋狂"):
            if bad in b:
                errs.append(f"ban{i}:{bad}")
        if re.search(r"[A-Za-z]", b):
            errs.append(f"lat{i}")
        if not hs[i - 1].startswith(f"{i:03d}、"):
            errs.append(f"num{i}")
        g[b[:18]].append(i)
    for pref, ids in g.items():
        if len(ids) >= 4:
            errs.append(f"pref {pref} {ids}")
    if colon > 2:
        errs.append(f"colon{colon}")
    if yanyi >= 15:
        errs.append(f"yanyi{yanyi}")
    if len(set(bodies)) != 150:
        errs.append("dup")
    lines = [
        f"FILE {path.name}",
        f"ID {d['id']}",
        f"COUNT {len(hs)}",
        f"FIRST {hs[0]}",
        f"LAST {hs[-1]}",
        f"STATUS {d['chatgptStatus']}",
        f"SOURCE {d['highlightsSource']}",
        f"CAPTURED {d['highlightsCapturedAt']}",
        f"UPDATED {d['updatedAt']}",
        f"CJK_MIN {min(ns)} CJK_MAX {max(ns)}",
        f"ERRORS {errs if errs else 'none'}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    root = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\Books\07_other")
    text = check(root / "07_other-20260717-49.json") + check(root / "07_other-20260717-50.json")
    Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading\_tmp\_verify_49_50.txt").write_text(
        text, encoding="utf-8"
    )


if __name__ == "__main__":
    main()
