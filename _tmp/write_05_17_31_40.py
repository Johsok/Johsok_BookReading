# -*- coding: utf-8 -*-
"""Validate and write 150 highlights into 05_food_wellness-20260717-31..40."""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BOOKS = ROOT / "Books" / "05_food_wellness"
TMP = ROOT / "_tmp"
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

UPDATED = "2026-08-18"
CAPTURED = "2026-08-18T10:40:00+08:00"


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def end_period(text: str) -> str:
    text = text.strip().rstrip("，、；")
    if not text.endswith("。"):
        text += "。"
    return text


PAD_TAILS = {
    "BOOK36": (
        "，家作預拌粉最怕季節食材出水",
        "，步驟照片要對準麵糊光澤",
        "，無印袋粉受潮就先過篩",
    ),
    "BOOK37": (
        "，冷藏發酵把等待交給冰箱",
        "，失敗先查粉水鹽油四項",
        "，隔夜麵團最省通勤時段",
    ),
    "BOOK38": (
        "，三種拌法走錯就救不回來",
        "，溫差比新模具更決定成敗",
        "，刮刀路徑要跟影片對齊",
    ),
    "BOOK39": (
        "，基礎工法要比新口味先熟",
        "，失敗先回三種餅乾拌合法",
        "，照片對的是乳化與泡沫",
    ),
    "BOOK40": (
        "，分蛋打發才能托住沙拉油",
        "，淡口油潤才適合長輩孩子",
        "，鎌倉細孔比盤飾更要緊",
    ),
}


def strip_pad(name: str, text: str) -> str:
    raw = text.strip().rstrip("。")
    for tail in PAD_TAILS.get(name, ()):
        if raw.endswith(tail):
            raw = raw[: -len(tail)]
            break
    return end_period(raw)


def last_clause(text: str) -> str:
    raw = text.rstrip("。")
    if "，" not in raw:
        return ""
    return raw.rsplit("，", 1)[-1]


def report_pad(name: str, items: list[str]) -> None:
    c = Counter(last_clause(t) for t in items)
    bad = [(k, v) for k, v in c.items() if k and v >= 6]
    if bad:
        print(f"PAD {name}: {bad[:8]}")


def atomic_write(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


SUMMARIES = {
    "05_food_wellness-20260717-31": "免揉日常麵包把攪拌縮到約五分鐘，靠重力與隔夜冷藏長筋，用鬆軟、Q彈、硬式三種底麵延伸到麵包卷、貝果、菠蘿與丹麥等八十多款店頭口感。",
    "05_food_wellness-20260717-32": "港式楊家雞湯以雞肉、水、薑與少許鹽在二十至四十分鐘熬出萬用湯底，再依黃帝內經五行四季與身體不適變化近五十道家常食療湯。",
    "05_food_wellness-20260717-33": "一週副食品把十倍粥到手指食物依月齡做成冰磚，一次冷凍四到六種食材，加熱即可餵，讓零到二十四個月的副食品準備能排進家庭節奏。",
    "05_food_wellness-20260717-34": "麻州餓鬼麵包店以柴燒窯與野生酵母寫下四十堂課，主張多一點水分、發酵與火力，並把巴塔、面具麵包、司康、貝果與剩麵包變身連成社區生活。",
    "05_food_wellness-20260717-35": "余市Domaine Takahiko追索曾我貴彥從小布施酒家與栃木葡萄園走到北海道種皮諾，用全串浸皮與旨味酒在二零二零年登上哥本哈根Noma酒單。",
    "05_food_wellness-20260717-36": "初學者甜點從圓蛋糕、塔、泡芙與磅蛋糕打底，再用無印烘焙包按春夏秋冬換成草莓塔、冰沙、蒙布朗與聖誕裝飾，讓零經驗也能按圖完成。",
    "05_food_wellness-20260717-37": "RoBistore把司康、戚風、蛋糕卷、吐司與貝果收成可冷藏的常備配方，用一百五十二則Q&A拆開麵粉水鹽油為何失敗，讓上班族也能零碎時間出爐。",
    "05_food_wellness-20260717-38": "DEL’IMMO主廚把YouTube熱門食譜改得更簡單，先教盆底翻拌、中心攪拌與部分回拌，再做鏟式蛋糕、手撕麵包、舒芙蕾鬆餅與免烤箱草莓塔。",
    "05_food_wellness-20260717-39": "開平餐飲以一千五百張圖拆解八十一款餅乾、塔派、蛋糕、巧克力、泡芙與布丁布蕾，並用四十九則失敗問答把工法原理講到可自行排查。",
    "05_food_wellness-20260717-40": "鎌倉戚風專賣把蛋、麵粉、砂糖與沙拉油做成分蛋打發的職人配方，再用改液體、加果泥、換粉類與油性食材變化出抹茶、紅茶與起司等口味。",
}

MAP = [
    ("05_food_wellness-20260717-31.json", "BOOK31"),
    ("05_food_wellness-20260717-32.json", "BOOK32"),
    ("05_food_wellness-20260717-33.json", "BOOK33"),
    ("05_food_wellness-20260717-34.json", "BOOK34"),
    ("05_food_wellness-20260717-35.json", "BOOK35"),
    ("05_food_wellness-20260717-36.json", "BOOK36"),
    ("05_food_wellness-20260717-37.json", "BOOK37"),
    ("05_food_wellness-20260717-38.json", "BOOK38"),
    ("05_food_wellness-20260717-39.json", "BOOK39"),
    ("05_food_wellness-20260717-40.json", "BOOK40"),
]


def main() -> None:
    a = load_mod(TMP / "hl_31_35.py", "hl3135")
    b = load_mod(TMP / "hl_36_40.py", "hl3640")
    lookup = {**{n: getattr(a, n) for n in ("BOOK31", "BOOK32", "BOOK33", "BOOK34", "BOOK35")},
              **{n: getattr(b, n) for n in ("BOOK36", "BOOK37", "BOOK38", "BOOK39", "BOOK40")}}
    errors = []
    for filename, key in MAP:
        items = [strip_pad(key, t) for t in lookup[key]]
        report_pad(key, items)
        numbered = [f"{i:03d}、{t}" for i, t in enumerate(items, 1)]
        path = BOOKS / filename
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        book_id = data["id"]
        try:
            cleaned = validate_highlights(book_id, numbered, str(data.get("title", "")), str(data.get("author", "")))
        except ValueError as e:
            errors.append(str(e))
            continue
        data["summary"] = SUMMARIES[book_id]
        data["chatgptHighlights"] = cleaned
        data["chatgptStatus"] = "complete"
        data["highlightsSource"] = "grok"
        data["highlightsCapturedAt"] = CAPTURED
        data["updatedAt"] = UPDATED
        atomic_write(path, data)
        back = json.loads(path.read_text(encoding="utf-8-sig"))
        validate_highlights(book_id, back["chatgptHighlights"], str(back.get("title", "")), str(back.get("author", "")))
        print("OK", filename)
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
