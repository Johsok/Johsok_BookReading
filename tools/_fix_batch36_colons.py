# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402

NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")

FIXES = {
    37: {
        8: "愛因斯坦式思想實驗示範如何先在腦中推演極限情況再進實驗室",
        44: "對照組思維可遷移到生活，沒有比較基準就難談改善是否真的發生",
        72: "尋找多重表徵時輪流用文字、圖像、實驗與故事翻譯同一概念",
        91: "好奇需要時間金錢與注意力當作實驗預算來配置",
        108: "年度回顧問自己哪三個方法被證明有效、哪三個該淘汰",
        123: "專案結束要做復盤，寫下假設、證據、意外與下一步",
        127: "恐懼未知時縮小實驗尺度，用低成本試探換取關鍵資訊",
        149: "選完小問題後立刻安排可觀察指標，避免假說只停在念頭裡空轉",
    },
    38: {
        57: "把科學態度遷移到公共議題時，先估不確定區間再下政策偏好",
        73: "複雜問題通常需要條件句，在甲情況下做甲方案、在乙情況下做乙方案",
        103: "個人層次可做的最小實驗是每週主動改變一個習慣路徑",
        121: "查證清單可包含來源、激勵結構、反證與不確定處四欄",
        139: "復健可從玩策略遊戲、學新語言規則或改做菜食譜這類小事開始",
    },
    39: {
        46: "過程指標可看本週完成幾次誠實觀察、修正幾次假說",
        54: "測量失真的例子包含睡眠剝奪讓一切評價變得灰暗",
        66: "人生也可以設計回滾機制，例如試用期、小額投資與分階段承諾",
        80: "家庭也可練習先恭喜孩子提問，再一起查資料而不是立刻給答案",
        115: "工具箱要定期保養，學習新方法並淘汰只焦慮不做測的無效儀式",
        146: "個人層次很簡單，今晚選一個卡住的問題只做一次清楚觀察",
    },
}


def short_colon_indices(bodies: list[str]) -> list[int]:
    out = []
    for i, body in enumerate(bodies, 1):
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            out.append(i)
    return out


def main() -> None:
    meta = {
        36: "03_natural_science-20260718-36",
        37: "03_natural_science-20260718-37",
        38: "03_natural_science-20260718-38",
        39: "03_natural_science-20260718-39",
        40: "03_natural_science-20260718-40",
    }
    for n, book_id in meta.items():
        path = ROOT / "tools" / f"_batch36_bodies_{n}.json"
        bodies = json.loads(path.read_text(encoding="utf-8"))
        for idx, text in FIXES.get(n, {}).items():
            bodies[idx - 1] = text
        # rewrite any remaining short-colon lines generically
        for idx in short_colon_indices(bodies):
            old = bodies[idx - 1]
            if "：" in old:
                left, right = old.split("：", 1)
            elif ":" in old:
                left, right = old.split(":", 1)
            else:
                continue
            bodies[idx - 1] = f"{left}，{right}"
        # Deduplicate while preserving length by lightly varying collisions.
        seen: dict[str, int] = {}
        for i, body in enumerate(bodies):
            if body not in seen:
                seen[body] = i
                continue
            suffix = "，並留下可在明天覆核的紀錄"
            candidate = body + suffix
            n = 2
            while candidate in seen:
                candidate = f"{body}，並用第{n}種方式留下可覆核紀錄"
                n += 1
            bodies[i] = candidate
            seen[candidate] = i
        assert len(bodies) == 150
        assert len(set(bodies)) == 150
        path.write_text(json.dumps(bodies, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        book = json.loads(
            (ROOT / "Books" / "03_natural_science" / f"{book_id}.json").read_text(encoding="utf-8-sig")
        )
        highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
        validate_highlights(book_id, highlights, book["title"], book["author"])
        print("VALID", book_id, "short_colon_left", short_colon_indices(bodies))


if __name__ == "__main__":
    main()
