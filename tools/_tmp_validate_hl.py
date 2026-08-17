# -*- coding: utf-8 -*-
"""Validate 150 highlights against findbook_writer rules."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def validate_highlights(book_id: str, highlights: object, title: str = "", author: str = "") -> None:
    if not isinstance(highlights, list) or len(highlights) != 150:
        raise ValueError(f"{book_id} 必須剛好 150 點，實際 {len(highlights) if isinstance(highlights, list) else type(highlights)}")
    short_colon_lines = []
    bodies = []
    forbidden_prefixes = ("本書", "作者指出", "本章", "這一章")
    starts = []
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not isinstance(line, str) or not line.startswith(expected):
            raise ValueError(f"{book_id} 第 {index} 點編號錯誤: {line[:20] if isinstance(line, str) else line}")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"{book_id} 第 {index} 點含禁用格式")
        if any(ch in line for ch in "*#_`"):
            print(f"WARN markdown-ish {index}: {line[:40]}")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if not body:
            raise ValueError(f"{book_id} 第 {index} 點沒有正文")
        if len(body) < 12:
            raise ValueError(f"{book_id} 第 {index} 點正文過短 ({len(body)}): {body}")
        if any(prefix in body for prefix in forbidden_prefixes):
            raise ValueError(f"{book_id} 第 {index} 點含禁用來源前綴")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} 第 {index} 點含面向／步驟贅詞")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon_lines.append((index, match.group(1)))
        bodies.append(body)
        starts.append(body[:18])
    if len(short_colon_lines) >= 3:
        raise ValueError(f"{book_id} 有 {len(short_colon_lines)} 點疑似短標籤加冒號: {short_colon_lines[:8]}")
    if len(set(bodies)) != len(bodies):
        dup = [b for b, c in Counter(bodies).items() if c > 1]
        raise ValueError(f"{book_id} 含完全重複重點: {dup[:3]}")
    repeated_starts = Counter(starts)
    bad = [(s, n) for s, n in repeated_starts.items() if n >= 4]
    if bad:
        raise ValueError(f"{book_id} 有大量重複固定開頭: {bad[:8]}")
    almost = [(s, n) for s, n in repeated_starts.most_common(8) if n >= 3]
    if almost:
        print("prefix x3:", almost)
    for label, value in (("書名", title), ("作者", author)):
        normalized = str(value).strip()
        if normalized:
            hits = [i for i, b in enumerate(bodies, 1) if normalized in b]
            if len(hits) >= 2:
                raise ValueError(f"{book_id} 正文反覆出現完整{label}: {hits}")
            if hits:
                print(f"{label} appears once at {hits}")
    print(f"OK {book_id} n={len(highlights)} min_len={min(len(b) for b in bodies)} max_len={max(len(b) for b in bodies)}")


if __name__ == "__main__":
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    title = sys.argv[2] if len(sys.argv) > 2 else ""
    author = sys.argv[3] if len(sys.argv) > 3 else ""
    validate_highlights(data["id"], data["highlights"], title, author)
