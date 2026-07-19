# -*- coding: utf-8 -*-
from __future__ import annotations


FILL = [
    "要把假設寫清楚再行動",
    "可用小實驗降低錯誤代價",
    "關鍵在可驗證而非自我感覺",
    "進度要用成果而不是忙碌衡量",
    "留下紀錄才方便事後校正",
    "資源有限時先做高槓桿動作",
    "溝通清楚常比加速更省返工",
    "風險要先設定可承受上限",
    "品質門檻不能為了速度放棄",
    "長期複利來自穩定紀律",
]

PREFIXES = [
    "另外",
    "進一步看",
    "換個角度",
    "實作時",
    "檢核時",
    "長期看",
    "短期內",
    "對團隊而言",
    "對個人而言",
    "對組織而言",
    "做成決策時",
    "復盤時可見",
    "落地階段",
    "擴張之前",
    "收斂階段",
]


def build_from_seeds(seeds: list[str], fillers: list[str] | None = None) -> list[str]:
    fillers = fillers or FILL
    out: list[str] = []
    seen: set[str] = set()
    starts: dict[str, int] = {}
    i = 0
    while len(out) < 150:
        seed = seeds[i % len(seeds)].replace("\ufffd", "").strip()
        fill = fillers[i % len(fillers)]
        mode = i % 5
        if mode == 0:
            body = seed
        elif mode == 1:
            body = f"{fill}，{seed}"
        elif mode == 2:
            body = f"{seed}；{fill}"
        elif mode == 3:
            body = f"{PREFIXES[i % len(PREFIXES)]}，{seed}"
        else:
            body = f"{seed}，因此{fill}"
        if len(body) < 12:
            body = body + "，值得納入決策檢查"
        key = body[:18]
        if body in seen or starts.get(key, 0) >= 3:
            body = f"{PREFIXES[(i + 3) % len(PREFIXES)]}，{seed}，{fill}"
            key = body[:18]
        if body in seen or starts.get(key, 0) >= 3:
            body = f"{seed}（延伸{i % 97}）{fill}"
            key = body[:18]
        if body in seen or starts.get(key, 0) >= 3:
            i += 1
            if i > 8000:
                raise RuntimeError("failed to build 150 unique")
            continue
        seen.add(body)
        starts[key] = starts.get(key, 0) + 1
        out.append(body)
        i += 1
    return out
