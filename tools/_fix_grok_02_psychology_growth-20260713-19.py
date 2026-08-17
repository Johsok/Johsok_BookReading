# -*- coding: utf-8 -*-
"""Fix short-colon highlights, write results, ready for writer."""
from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

GEN = Path(__file__).with_name("_gen_grok_02_psychology_growth-20260713-19.py")
REMOVE = {
    "天氣變化靠皮膚與氣壓感判斷，出門前多一層準備就能少一次慌亂。",
    "考試與學習改成語音教材後，理解深度往往不減，只是路徑更長。",
    "旅行前把動線做成口頭清單，陌生城市才不會變成無法穿越的迷宮。",
    "練習感謝仍在的感官，不是否定失去，而是避免全部注意力困在虧損裡。",
    "閱讀生命敘事時，問自己願意為包容付出哪一件具體小事。",
}
FIXES = {
    "創傷後的身體會記得恐慌：突然的聲響、擁擠的人潮，都可能觸發舊日警報。":
        "創傷後的身體會記得恐慌，突然的聲響與擁擠人潮都可能觸發舊日警報。",
    "教練的口令像臨時的視覺：左偏、加速、休息，全靠聽覺即時校正。":
        "教練口令像臨時視覺，左偏、加速與休息全靠聽覺即時校正方向。",
    "把求助清單寫清楚：交通、學習、情緒、創作，資源才找得到入口。":
        "把交通、學習、情緒與創作寫進求助清單，資源才找得到入口。",
    "開始的方式很平常：承認痛、學習新方法、找同伴，然後再走一步。":
        "開始往往很平常，先承認痛、學新方法、找同伴，然後再走一步。",
    "整理房間靠固定位置原則：每樣東西有家，手才能在黑暗中找到它。":
        "整理房間靠固定位置，每樣東西有家，手才能在黑暗中找到它。",
    "重新定義成功：能照顧自己情緒與行程，有時比站上頒獎台更關鍵。":
        "若重新定義成功，能照顧情緒與行程有時比站上頒獎台更關鍵。",
    "最後記住：走進黑暗之後仍能看見自己，是因為沒有把自我交給視力獨裁。":
        "走進黑暗之後仍能看見自己，是因為沒有把自我交給視力獨裁。",
}


def load_bodies(src: str) -> list[str]:
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "BODIES":
                    return list(ast.literal_eval(node.value))
    raise RuntimeError("BODIES not found")


def validate(bodies: list[str]) -> None:
    forbidden = ("本書", "作者指出", "本章", "這一章")
    title = "八分之一的世界：走進黑暗，我看見自己"
    author = "林芳語"
    for i, body in enumerate(bodies, 1):
        if len(body) < 12:
            raise SystemExit(f"short {i}: {body}")
        if "｜" in body or "\n" in body:
            raise SystemExit(f"bad format {i}")
        for prefix in forbidden:
            if prefix in body:
                raise SystemExit(f"forbidden {i}")
    if len(bodies) != 150 or len(set(bodies)) != 150:
        raise SystemExit(f"count/dup {len(bodies)} unique={len(set(bodies))}")
    starts = Counter(b[:18] for b in bodies)
    bad = [(k, v) for k, v in starts.items() if v >= 4]
    if bad:
        raise SystemExit(f"starts {bad}")
    if sum(title in b for b in bodies) >= 2 or sum(author in b for b in bodies) >= 2:
        raise SystemExit("title/author overuse")
    natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
    short = []
    for i, body in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(natural):
            short.append((i, body[:40]))
    if len(short) >= 3:
        raise SystemExit(f"short colon {short}")


def main() -> None:
    src = GEN.read_text(encoding="utf-8")
    bodies = load_bodies(src)
    bodies = [FIXES.get(b, b) for b in bodies if b not in REMOVE]
    # also apply fixes if already trimmed somehow
    bodies = [FIXES.get(b, b) for b in bodies]
    validate(bodies)

    start = src.index("BODIES = [")
    end = src.index("\n\n\ndef main", start)
    block = ["BODIES = ["] + [f'    "{b}",' for b in bodies] + ["]"]
    GEN.write_text(src[:start] + "\n".join(block) + src[end:], encoding="utf-8")

    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    out = Path(__file__).with_name(
        ".findbook_results_grok_02_psychology_growth-20260713-19.json"
    )
    out.write_text(
        json.dumps(
            {"id": "02_psychology_growth-20260713-19", "highlights": highlights},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("count", len(highlights))
    print("first", highlights[0])
    print("last", highlights[-1])
    print("wrote", out)


if __name__ == "__main__":
    main()
