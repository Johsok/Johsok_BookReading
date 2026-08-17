# -*- coding: utf-8 -*-
"""Write one book's results JSON from a BODIES list file."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights  # noqa: E402
from _hl_validate import validate_highlights as extra_validate  # noqa: E402

META = {
    "02_psychology_growth-20260716-184": (
        "今天，你會有好事發生：願我們的好運，可以抵抗世間所有的堅硬",
        "序詩",
        "tools/_hl_184.py",
    ),
    "02_psychology_growth-20260716-185": (
        "人生每件事，都是取捨的練習",
        "吳若權",
        "tools/_hl_185.py",
    ),
    "02_psychology_growth-20260716-186": (
        "不是別人不懂你，而是你不懂得愛自己",
        "叢非從",
        "tools/_hl_186.py",
    ),
    "02_psychology_growth-20260716-187": (
        "誰也偷不走你的專注力：堵住分心漏洞，做得更好，犯錯更少",
        "奧斯卡．德．博斯、馬克．提赫拉爾",
        "tools/_hl_187.py",
    ),
}


def load_bodies(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "BODIES":
                    return ast.literal_eval(node.value)
    raise ValueError(f"BODIES not found in {path}")


def main(book_id: str) -> None:
    title, author, rel = META[book_id]
    bodies = load_bodies(ROOT / rel)
    highlights = [f"{i:03d}、{body}" for i, body in enumerate(bodies, 1)]
    extra_validate(book_id, highlights, title, author)
    validate_highlights(book_id, highlights, title, author)
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"ok\t{book_id}\t{len(highlights)}")


if __name__ == "__main__":
    main(sys.argv[1])
