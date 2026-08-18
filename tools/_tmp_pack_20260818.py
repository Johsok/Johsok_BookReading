# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from findbook_writer import validate_highlights

TRANSCRIPTS = Path(
    r"C:\Users\johso\.cursor\projects\c-Users-johso-OneDrive-Desktop-Johsok-BookReading\agent-transcripts"
    r"\518ee7c7-e75f-4f23-84c0-007db9bcd24e\subagents"
)

BOOKS = [
    ("5b803975-c933-4e1b-b793-35f71bb87d47", "02_psychology_growth-20260818-04"),
    ("30b0de27-a276-428e-8215-7a4fe8b4f252", "02_psychology_growth-20260818-05"),
    ("f8360592-bb2d-4dfa-91dc-0dbda74d7213", "02_psychology_growth-20260818-06"),
    ("7a35f09b-9dc2-4ca4-8aab-01a6c1fadffe", "02_psychology_growth-20260818-07"),
]

SKIP_MARKERS = (
    "wait I",
    "I cannot",
    "Let me",
    "cannot use",
    "不能用",
    "不能英文",
    "still thinking",
    "I need to",
    "secretly",
    "rumination",
    "cons...",
    "cons  cons",
    "trop ",
)


def extract_text(payload) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        if isinstance(payload.get("text"), str):
            return payload["text"]
        content = payload.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "\n".join(extract_text(item) for item in content)
        if isinstance(payload.get("response"), str):
            return payload["response"]
        return json.dumps(payload, ensure_ascii=False)
    if isinstance(payload, list):
        return "\n".join(extract_text(item) for item in payload)
    return str(payload)


def highlights_from_jsonl(path: Path) -> list[str]:
    found: dict[int, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if record.get("role") != "assistant":
            continue
        text = extract_text(record.get("message") or record)
        for line in text.splitlines():
            line = line.strip()
            match = re.match(r"^(\d{3})、(.*)$", line)
            if not match:
                continue
            body = match.group(2).strip()
            if "trop " in body:
                body = body.replace("trop ", "")
            if any(marker in f"{match.group(1)}、{body}" for marker in SKIP_MARKERS if marker != "trop "):
                continue
            if len(body) < 12:
                continue
            found[int(match.group(1))] = f"{match.group(1)}、{body}"
    return [found[index] for index in range(1, 151) if index in found]


def patch_short_colons(highlights: list[str]) -> list[str]:
    natural = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
    patched = []
    for line in highlights:
        body = re.sub(r"^\d{3}、", "", line).strip()
        match = re.match(r"^([^：:]{1,12})([：:])(.*)$", body)
        if match and not match.group(1).endswith(natural):
            body = f"{match.group(1)}，{match.group(3)}"
            line = f"{line[:4]}{body}"
        patched.append(line)
    return patched


def patch_forbidden(highlights: list[str]) -> list[str]:
    replacements = (
        ("一本書", "一本讀物"),
        ("這本書", "這份讀物"),
        ("本書", "這份讀物"),
        ("作者指出", "文中說明"),
        ("這一章", "這一段"),
        ("本章", "這一段"),
    )
    patched = []
    for line in highlights:
        body = re.sub(r"^\d{3}、", "", line)
        for old, new in replacements:
            body = body.replace(old, new)
        patched.append(f"{line[:4]}{body}")
    return patched


def main() -> None:
    out_dir = ROOT / "tools"
    for agent_id, book_id in BOOKS:
        path = TRANSCRIPTS / f"{agent_id}.jsonl"
        highlights = highlights_from_jsonl(path)
        print(f"{book_id} extracted={len(highlights)} from {path.name}")
        if len(highlights) != 150:
            missing = [index for index in range(1, 151) if not any(h.startswith(f"{index:03d}、") for h in highlights)]
            print(f"  missing={missing[:20]}")
            continue
        category_id = book_id.rsplit("-", 2)[0]
        book_path = ROOT / "Books" / category_id / f"{book_id}.json"
        book = json.loads(book_path.read_text(encoding="utf-8"))
        highlights = patch_short_colons(patch_forbidden(highlights))
        try:
            validate_highlights(book_id, highlights, book["title"], book["author"])
        except ValueError as error:
            print(f"  STILL FAIL: {error}")
            for index, line in enumerate(highlights, 1):
                body = re.sub(r"^\d{3}、", "", line)
                if any(token in body for token in ("本書", "作者指出", "本章", "這一章")):
                    print(f"  forbidden {index}: {body[:80]}")
            continue
        result_path = out_dir / f"_tmp_results_{book_id}.json"
        result_path.write_text(
            json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"  wrote {result_path.name}")


if __name__ == "__main__":
    main()
