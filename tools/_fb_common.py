# -*- coding: utf-8 -*-
"""Shared helpers for FindBook highlight generation."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def validate_bodies(bodies: list[str], title: str, author: str) -> None:
    """Raise AssertionError if highlights violate writer rules."""
    assert len(bodies) == 150, len(bodies)
    assert len(set(bodies)) == 150
    short_colon = []
    for body in bodies:
        assert len(body) >= 12, body
        assert "｜" not in body and "\n" not in body
        assert not any(p in body for p in ("本書", "作者指出", "本章", "這一章"))
        assert not re.search(r".{1,8}面第\d+步[，,]", body)
        assert not re.match(r"^第\d+步[，,]", body)
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon.append(body[:20])
        for ban in (
            "以「商業理財」作為",
            "落到具體情境，再用可觀察的結果確認做法是否有效",
            "先界定目標，再把",
        ):
            assert ban not in body, ban
    assert len(short_colon) < 3, short_colon
    starts = Counter(b[:18] for b in bodies if len(b) >= 18)
    assert starts.most_common(1)[0][1] < 4, starts.most_common(3)
    assert sum(title in b for b in bodies) < 2, title
    # author may be multi-part; check full string
    if author.strip():
        assert sum(author in b for b in bodies) < 2, author


def write_results(book_id: str, bodies: list[str], title: str, author: str) -> Path:
    """Validate and write tools/.findbook_results_grok_{id}.json."""
    validate_bodies(bodies, title, author)
    highlights = [f"{i:03d}、{b}" for i, b in enumerate(bodies, 1)]
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out
