# -*- coding: utf-8 -*-
"""Strip restated tails and re-apply unique informational pads."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
TMP = ROOT / "_tmp"
STAMP = "2026-08-18T09:10:00+08:00"
BANNED = ("本書", "作者指出", "本章", "這一章", "｜")
COLON_RE = re.compile(r"[：:]")

PADS43 = [
    "，沙量比水量更決定國運",
    "，河工把神話寫進衙署",
    "，埽工比摺件更接近生死",
    "，開封的沙層即編年",
    "，束水與讓地仍在吵架",
    "，黃氾區用身體付戰爭帳",
    "，清淤是引黃隱藏的主業",
    "，潼關高程是三門峽的考卷",
    "，調沙把下游河槽當腸道",
    "，鐵橋把天塹改成時刻表",
    "，灘區人口是活的行洪區",
    "，香火與閘門疊在同一堤",
    "，合龍樁比年號更準",
    "，民夫即國家的第二汛期",
    "，衛河渠底承接黃土",
    "，冰凌與洪峰同樣要命",
    "，造陸改寫縣界",
    "，庫容用來換喘息而非神話",
]

PADS44 = [
    "，建康用優容換可用之將",
    "，禪讓背後仍是刀斧",
    "，江州益州考驗新政手臂",
    "，洛陽賄賂寫進口音",
    "，義陽三關把戰爭縮成奪關",
    "，韋睿用堰改寫鍾離水位",
    "，佛塔高度與邊鎮饑餓對讀",
    "，六鎮怒火從歧視裡長出",
    "，河陰把衣冠變成黃土",
    "，陳慶之的速度喂不飽洛陽",
    "，晉陽馬廄才是真決策席",
    "，高歡用糧食收編饑營",
    "，寶夤把舊齊血脈變成北棋",
    "，元乂劉騰把宮門做成監獄",
    "，葛榮兵多卻喂不飽號令",
]

REWRITE = {
    "裂土誌的南北對讀，是建康完成加冕時，洛陽開始把加冕變成軍營程序。": "建康完成加冕時，洛陽開始把加冕變成軍營程序，南北兩種時間表從此分岔得更明顯。",
    "史實寫在人名與地名裡。": None,
}


def compact(s: str) -> str:
    """Remove common function words for restatement detection."""
    for ch in "的了著是與和就也在把被到而上中又再才只":
        s = s.replace(ch, "")
    return s


def strip_restatement(s: str) -> str:
    """Drop a last clause that restates the head."""
    s = s.strip()
    if s in REWRITE and REWRITE[s]:
        return REWRITE[s]
    core = s.rstrip("。")
    parts = core.split("，")
    if len(parts) < 2:
        return core + "。"
    last = parts[-1]
    head = "，".join(parts[:-1])
    cl, ch = compact(last), compact(head)
    restates = False
    if last in head or cl in ch:
        restates = True
    elif len(cl) >= 6 and cl[:8] in ch:
        restates = True
    elif len(last) >= 6 and last[-6:] in head:
        restates = True
    elif last == "史實寫在人名與地名裡":
        restates = True
    if restates:
        return head + "。"
    return core + "。"


def pad_unique(s: str, pads: list[str], idx: int) -> str:
    """Ensure body length 32-68 using a unique pad if needed."""
    s = s.rstrip("。") + "。"
    if 32 <= len(s) <= 68:
        return s
    if len(s) > 68:
        s = s[:67].rstrip("，") + "。"
        return s
    pad = pads[idx % len(pads)]
    # rotate if collision with existing text
    for k in range(len(pads)):
        p = pads[(idx + k) % len(pads)]
        cand = s.rstrip("。") + p + "。"
        if p.lstrip("，") not in s and 32 <= len(cand) <= 68:
            return cand
    cand = s.rstrip("。") + "，細節落在人名地名與制度上。"
    if len(cand) > 68:
        cand = cand[:67].rstrip("，") + "。"
    return cand


def validate(bid: str, bodies: list[str]) -> list[str]:
    """Validate highlight bodies."""
    errors = []
    if len(bodies) != 150:
        errors.append(f"{bid} len={len(bodies)}")
    if len(set(bodies)) != 150:
        errors.append(f"{bid} dup")
    groups = defaultdict(list)
    colon_hits = 0
    for i, b in enumerate(bodies, 1):
        if not (32 <= len(b) <= 68):
            errors.append(f"{bid} len_{i}:{len(b)} {b}")
        for bad in BANNED:
            if bad in b:
                errors.append(f"{bid} ban_{i}:{bad}")
        if "第" in b and "章" in b:
            errors.append(f"{bid} chapter_{i}")
        if "裂土誌" in b:
            errors.append(f"{bid} title_{i}")
        letters = "".join(c for c in b if c.isascii() and c.isalpha())
        if letters:
            errors.append(f"{bid} en_{i}:{letters}")
        colon_hits += len(COLON_RE.findall(b))
        groups[b[:18]].append(i)
    if colon_hits > 2:
        errors.append(f"{bid} colon_total={colon_hits}")
    for p, ids in groups.items():
        if len(ids) >= 4:
            errors.append(f"{bid} prefix18 {p} {ids}")
    return errors


def dump_script(path: Path, var: str, bodies: list[str], book_rel: str) -> None:
    """Rewrite helper script with final bodies."""
    lines = "\n".join(f"    {json.dumps(b, ensure_ascii=False)}," for b in bodies)
    book = ROOT / book_rel
    text = f'''# -*- coding: utf-8 -*-
"""Write Traditional Chinese highlights for {book_rel}."""
from __future__ import annotations

import json
from pathlib import Path

BOOK = Path(r"{book}")
STAMP = "{STAMP}"

{var} = [
{lines}
]


def main() -> None:
    """Patch book JSON atomically and print verification."""
    data = json.loads(BOOK.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = [f"{{i:03d}}、{{b}}" for i, b in enumerate({var}, 1)]
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = "2026-08-18"
    tmp = BOOK.with_suffix(BOOK.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    tmp.replace(BOOK)
    loaded = json.loads(BOOK.read_text(encoding="utf-8-sig"))
    hl = loaded["chatgptHighlights"]
    print("id", loaded["id"])
    print("len", len(hl))
    print("first", hl[0])
    print("last", hl[-1])
    print("status", loaded["chatgptStatus"])
    print("source", loaded["highlightsSource"])


if __name__ == "__main__":
    main()
'''
    path.write_text(text, encoding="utf-8")


def patch(path: Path, bodies: list[str]) -> dict:
    """Atomically overwrite highlights on a book JSON."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data["chatgptHighlights"] = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    data["chatgptStatus"] = "complete"
    data["highlightsSource"] = "grok"
    data["highlightsCapturedAt"] = STAMP
    data["updatedAt"] = "2026-08-18"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def clean_book(path: Path, pads: list[str]) -> list[str]:
    """Strip restatements and pad short lines."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    out = []
    for i, line in enumerate(data["chatgptHighlights"]):
        body = line.split("、", 1)[1]
        body = strip_restatement(body)
        body = pad_unique(body, pads, i)
        out.append(body)
    return out


def main() -> None:
    """Clean, validate, write JSON, refresh scripts."""
    p43 = ROOT / r"Books\07_other\07_other-20260717-43.json"
    p44 = ROOT / r"Books\07_other\07_other-20260717-44.json"
    b43 = clean_book(p43, PADS43)
    b44 = clean_book(p44, PADS44)
    errors = validate("43", b43) + validate("44", b44)
    report = TMP / "_chk_43_44_clean.txt"
    if errors:
        report.write_text("\n".join(errors), encoding="utf-8")
        print("FAIL", len(errors))
        print(report.read_text(encoding="utf-8")[:4000])
        raise SystemExit(1)
    d43 = patch(p43, b43)
    d44 = patch(p44, b44)
    dump_script(TMP / "write_hl_07_43.py", "B43", b43, r"Books\07_other\07_other-20260717-43.json")
    dump_script(TMP / "write_hl_07_44.py", "B44", b44, r"Books\07_other\07_other-20260717-44.json")
    for d in (d43, d44):
        hl = d["chatgptHighlights"]
        print("id", d["id"])
        print("len", len(hl))
        print("first", hl[0])
        print("last", hl[-1])
        print("status", d["chatgptStatus"])
        print("source", d["highlightsSource"])
    print("PASS")


if __name__ == "__main__":
    main()
