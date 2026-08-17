# -*- coding: utf-8 -*-
"""Local highlight validator mirroring findbook_writer.validate_highlights."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

PUNCT_RE = re.compile(r"[\s\W_]+", re.UNICODE)
NUMBER_RE = re.compile(r"^\d{3}、")
NATURAL_COLON_SUFFIXES = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")


def validate_highlights(book_id: str, highlights: object, title: str = "", author: str = "") -> list[str]:
    if not isinstance(highlights, list) or len(highlights) != 150:
        raise ValueError(f"{book_id} 必須剛好 150 點，目前 {0 if not isinstance(highlights, list) else len(highlights)}")
    short_colon_lines = []
    cleaned = []
    bodies = []
    forbidden_prefixes = ("本書", "作者指出", "本章", "這一章")
    for index, line in enumerate(highlights, 1):
        expected = f"{index:03d}、"
        if not isinstance(line, str) or not line.startswith(expected):
            raise ValueError(f"{book_id} 第 {index} 點編號錯誤")
        if "\n" in line or "\r" in line or "｜" in line:
            raise ValueError(f"{book_id} 第 {index} 點含禁用格式")
        if "*" in line or "`" in line or "#" in line:
            raise ValueError(f"{book_id} 第 {index} 點含 Markdown")
        body = NUMBER_RE.sub("", line, count=1).strip()
        if not body:
            raise ValueError(f"{book_id} 第 {index} 點沒有正文")
        if len(body) < 12:
            raise ValueError(f"{book_id} 第 {index} 點正文過短：{body}")
        if any(prefix in body for prefix in forbidden_prefixes):
            raise ValueError(f"{book_id} 第 {index} 點含禁用來源前綴")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} 第 {index} 點含面向／步驟贅詞")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES):
            short_colon_lines.append(index)
        cleaned.append(line.strip())
        bodies.append(body)
    if len(short_colon_lines) >= 3:
        raise ValueError(f"{book_id} 有 {len(short_colon_lines)} 點疑似短標籤加冒號：{short_colon_lines[:10]}")
    if len(set(bodies)) != len(bodies):
        raise ValueError(f"{book_id} 含完全重複重點")
    repeated_starts = Counter(body[:18] for body in bodies if len(body) >= 18)
    bad = [(k, v) for k, v in repeated_starts.items() if v >= 4]
    if bad:
        raise ValueError(f"{book_id} 有大量重複固定開頭：{bad[:5]}")
    for label, value in (("書名", title), ("作者", author)):
        normalized = str(value).strip()
        if normalized and sum(normalized in body for body in bodies) >= 2:
            raise ValueError(f"{book_id} 正文反覆出現完整{label}")
    return cleaned


def write_results(book_id: str, highlights: list[str], title: str, author: str) -> Path:
    validate_highlights(book_id, highlights, title, author)
    payload = {"id": book_id, "highlights": highlights}
    path = Path(__file__).resolve().parent / f".findbook_results_grok_{book_id}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"validated_and_wrote\t{path}")
    return path


if __name__ == "__main__":
    raise SystemExit("import as module")
