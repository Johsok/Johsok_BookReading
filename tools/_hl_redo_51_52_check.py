# -*- coding: utf-8 -*-
"""Check highlight scripts for count, zhconv, openings."""
from __future__ import annotations

import ast
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights  # noqa: E402

try:
    import zhconv
except ImportError:
    zhconv = None


def load_bodies(path: Path) -> list[str]:
    mod = ast.parse(path.read_text(encoding="utf-8"))
    for node in mod.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "BODIES":
                    return ast.literal_eval(node.value)
    raise RuntimeError(path)


def report(path: Path, book_id: str, title: str, author: str) -> list[str]:
    lines = [f"==== {path.name} ===="]
    bodies = load_bodies(path)
    lines.append(f"count={len(bodies)}")
    lines.append(f"short={[i + 1 for i, s in enumerate(bodies) if len(s) < 12]}")
    starts = Counter(s[:18] for s in bodies)
    lines.append(f"repeat2+={[(k, v) for k, v in starts.items() if v >= 2]}")
    lines.append(f"dup={len(bodies) - len(set(bodies))}")
    latin = [(i + 1, s) for i, s in enumerate(bodies) if re.search(r"[A-Za-z]", s)]
    lines.append(f"latin={latin}")
    if zhconv:
        diffs = []
        for i, s in enumerate(bodies, 1):
            trad = zhconv.convert(s, "zh-hant")
            if trad != s:
                pairs = [f"{a}->{b}" for a, b in zip(s, trad) if a != b]
                extra = ""
                if len(trad) != len(s):
                    extra = f" len {len(s)}->{len(trad)}"
                diffs.append(f"{i:03d} {pairs}{extra}\n  SRC {s}\n  HANT {trad}")
        lines.append(f"zhconv_diffs={len(diffs)}")
        lines.extend(diffs)
    else:
        lines.append("zhconv=unavailable")
    su_open = sum(1 for s in bodies if s.startswith("蘇軾") or s.startswith("蘇東坡"))
    lines.append(f"su_open={su_open}")
    lines.append(f"author_hits={sum(author in s for s in bodies)}")
    lines.append(f"title_hits={sum(title in s for s in bodies)}")
    hl = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    validate_highlights(book_id, hl, title, author)
    lines.append("validate=OK")
    lines.append(hl[0])
    lines.append(hl[-1])
    return lines


def main() -> None:
    tools = Path(__file__).resolve().parent
    out_lines = []
    out_lines.extend(
        report(
            tools / "_hl_redo_07_other-20260716-51.py",
            "07_other-20260716-51",
            "圖解中世紀歐洲世界觀：從階級體制、社會規範到日常生活",
            "祝田秀全、秀島迅",
        )
    )
    out_lines.extend(
        report(
            tools / "_hl_redo_07_other-20260716-52.py",
            "07_other-20260716-52",
            "人間有味蘇東坡：大宋文豪與美食的隨緣相遇",
            "劉陽",
        )
    )
    out = tools / "_hl_redo_51_52_check.txt"
    out.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
