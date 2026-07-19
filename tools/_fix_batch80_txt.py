# -*- coding: utf-8 -*-
"""Clean and pad batch80 highlight text files to exactly 150 lines."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "tools" / "_batch80_highlights"

REPLACEMENTS = [
    (r"\s*generational trauma\s*", "跨代創傷"),
    (r"\s*determin\s*", ""),
    (r"kombin\s*", "組合"),
    (r"復古cosplay", "復古扮演"),
    (r"cosplay", "扮演"),
    (r"未必 intra 任期內負責", "未必在任期內負責"),
    (r"\s*intra\s*", ""),
    ("口号", "口號"),
    ("邻里", "鄰里"),
    ("却是", "卻是"),
    ("边疆", "邊疆"),
    ("占领", "佔領"),
    ("叙事", "敘事"),
    ("剧场", "劇場"),
    ("城里", "城裡"),
    ("当代", "當代"),
    ("毁基", "毀基"),
    ("崩坏", "崩壞"),
]


def load(name: str) -> list[str]:
    return [ln.strip() for ln in (DIR / name).read_text(encoding="utf-8").splitlines() if ln.strip()]


def save(name: str, lines: list[str]) -> None:
    assert len(lines) == 150, (name, len(lines))
    (DIR / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_line(line: str) -> str:
    for old, new in REPLACEMENTS:
        if old.startswith("(") or "\\" in old or old.endswith("*"):
            line = re.sub(old, new, line)
        else:
            line = line.replace(old, new)
    line = re.sub(r"\s+", "", line) if False else line  # noqa: keep spaces
    line = line.strip()
    # fix double spaces from removals
    line = re.sub(r" {2,}", " ", line)
    return line


def dedupe_clean(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in lines:
        line = clean_line(raw)
        if not line or "\ufffd" in line:
            continue
        if re.search(r"[A-Za-z]", line):
            print("DROP EN:", line)
            continue
        if line not in seen:
            seen.add(line)
            out.append(line)
    return out


EXTRAS = {
    "b39.txt": [
        "把軸心突破當成資源庫而非化石，現代爭論才有可取用的深度。",
        "深度不保證正確答案，但能避免只用四年選期思考百年問題。",
        "百年問題包括教育、生態、人口與制度信任，恰好都是大歷史題材。",
        "題材讀完若只剩慨嘆興亡，等於把結構分析又縮回命運論。",
        "命運論退場後，才能把責任分給可替換的職位與可修正的規則。",
        "規則修正需要公開理由，公開理由需要最低限度的共同事實。",
        "共同事實崩解時，軸心留下的對話理想最先受傷。",
        "受傷之後修復很難，卻比讓社會改用純暴力協調更值得嘗試。",
        "嘗試的起點可以很小：先把一個政策的成本承擔者說清楚。",
        "說清楚本身就是倫理動作，也是對抗空轉大詞的技術。",
    ],
    "b40.txt": [
        "把凱旋門與里程碑並讀，會看懂宣傳石與實用石如何分工。",
        "分工清楚後，較不容易被單一華麗遺跡帶走全部注意力。",
        "注意力回到路基層理時，帝國史才從觀光轉成研究。",
        "研究旅行不必否定感動，但感動之後要留下可檢驗的筆記。",
        "筆記裡記下坡度、鋪面與沿線聚落，比只寫心潮澎湃有用。",
        "有用知識能遷移到自己城市的人行道爭議與公交路權分配。",
        "路權分配永遠政治，羅馬只是把這件事用石頭寫得特別久。",
        "寫得久不代表正義，只代表某套動員能力曾經強大。",
        "強大動員留下的遺產，後人可以繼承技術、同時拒絕征服邏輯。",
        "拒絕征服邏輯後，條條大路才可能通向較平等的共同抵達。",
    ],
}


def pad(name: str, lines: list[str]) -> list[str]:
    lines = dedupe_clean(lines)
    seen = set(lines)
    for extra in EXTRAS.get(name, []):
        if len(lines) >= 150:
            break
        extra = clean_line(extra)
        if extra and extra not in seen and not re.search(r"[A-Za-z]", extra):
            seen.add(extra)
            lines.append(extra)
    if len(lines) < 150:
        raise SystemExit(f"{name} still short: {len(lines)}")
    if len(lines) > 150:
        lines = lines[:150]
    return lines


def main() -> None:
    for name in ("b36.txt", "b37.txt", "b38.txt", "b39.txt", "b40.txt"):
        lines = pad(name, load(name))
        save(name, lines)
        # final check
        bad = [l for l in lines if re.search(r"[A-Za-z]", l) or "\ufffd" in l]
        print(name, len(lines), "bad", len(bad))
        if bad:
            for b in bad:
                print(" ", b)


if __name__ == "__main__":
    main()
