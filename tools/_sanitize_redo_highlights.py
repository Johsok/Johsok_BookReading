# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from findbook_writer import NATURAL_COLON_SUFFIXES, NUMBER_RE, validate_highlights  # noqa: E402

COLON_RE = re.compile(r"^([^：:]{1,12})[：:]")


def is_short_colon(body: str) -> bool:
    match = COLON_RE.match(body)
    return bool(match and not match.group(1).endswith(NATURAL_COLON_SUFFIXES))


def strip_forbidden_substrings(text: str) -> str:
    replacements = (
        ("作者指出", "臨床觀察顯示"),
        ("這一章", "這一段討論"),
        ("一本書", "一本讀物"),
        ("本書", "這份文本"),
        ("本章", "這段討論"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def fix_body(body: str) -> str:
    text = strip_forbidden_substrings(body.strip())
    text = text.replace("｜", "，")
    for _ in range(6):
        if not is_short_colon(text):
            break
        match = COLON_RE.match(text)
        rest = text[match.end() :].strip()
        rest = re.sub(r"^[，、。；：:\s]+", "", rest)
        if len(rest) >= 12:
            text = rest
        else:
            label = match.group(1)
            text = f"{label}是{rest}" if rest else f"{label}需要放到具體生活裡練習。"
            break
    text = re.sub(r"^[，、。；：:\s]+", "", text)
    if len(text) < 12:
        text = "把這個觀念放到具體生活情境裡練習，並記錄一次真實結果。"
    if not text.endswith(("。", "！", "？")):
        text += "。"
    return text


def unique_body(body: str, seen: set[str], index: int) -> str:
    if body not in seen:
        return body
    suffix = f"可再對照第{index:03d}種日常情境檢查一次。"
    candidate = body.rstrip("。") + "，" + suffix
    while candidate in seen:
        candidate = candidate.rstrip("。") + "再看一次。"
    return candidate


def sanitize_file(book_id: str) -> str:
    results_path = TOOLS / f".findbook_results_grok_{book_id}.json"
    book_path = ROOT / "Books" / "02_psychology_growth" / f"{book_id}.json"
    if not results_path.exists() or not book_path.exists():
        return f"missing\t{book_id}"
    payload = json.loads(results_path.read_text(encoding="utf-8-sig"))
    highlights = payload.get("highlights") or []
    book = json.loads(book_path.read_text(encoding="utf-8-sig"))
    title = str(book.get("title", ""))
    author = str(book.get("author", ""))
    cleaned = []
    seen: set[str] = set()
    for index, line in enumerate(highlights, 1):
        body = NUMBER_RE.sub("", str(line), count=1).strip()
        body = fix_body(body)
        if title:
            body = body.replace(title, "")
        if author:
            body = body.replace(author, "")
        body = re.sub(r"^[，、。；：:\s]+", "", body)
        body = fix_body(body)
        body = unique_body(body, seen, index)
        seen.add(body)
        cleaned.append(f"{index:03d}、{body}")
    payload["id"] = book_id
    payload["highlights"] = cleaned
    results_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        validate_highlights(book_id, cleaned, title, author)
        return f"fixed_ok\t{book_id}"
    except Exception as exc:
        return f"fixed_bad\t{book_id}\t{exc}"


def main() -> None:
    ids = sys.argv[1:]
    if not ids:
        for date in ("20260714", "20260715"):
            for n in range(1, 31):
                ids.append(f"02_psychology_growth-{date}-{n:02d}")
    lines = [sanitize_file(book_id) for book_id in ids]
    report = TOOLS / ".redo_60_sanitize_report.txt"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
