# -*- coding: utf-8 -*-
"""Apply 150 highlights to 06_computer_info 20260717-21..30 JSON files."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(r"C:\Users\johso\OneDrive\Desktop\Johsok_BookReading")
BASE = ROOT / "Books" / "06_computer_info"
TMP = ROOT / "_tmp"
TAIPEI = ZoneInfo("Asia/Taipei")
NUMBER_RE = re.compile(r"^\d{3}、")


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def now_iso() -> str:
    return datetime.now(TAIPEI).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def to_numbered(bodies: list[str]) -> list[str]:
    out = []
    for i, body in enumerate(bodies, 1):
        text = body.strip()
        if NUMBER_RE.match(text):
            text = NUMBER_RE.sub("", text, count=1).strip()
        out.append(f"{i:03d}、{text}")
    return out


def validate_highlights(book_id: str, highlights: list[str], title: str, author: str) -> list[str]:
    if len(highlights) != 150:
        raise ValueError(f"{book_id} 必須剛好 150 點，實際 {len(highlights)}")
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
        body = NUMBER_RE.sub("", line, count=1).strip()
        if not body:
            raise ValueError(f"{book_id} 第 {index} 點沒有正文")
        if len(body) < 12:
            raise ValueError(f"{book_id} 第 {index} 點正文過短")
        if any(prefix in body for prefix in forbidden_prefixes):
            raise ValueError(f"{book_id} 第 {index} 點含禁用來源前綴")
        if re.search(r".{1,8}面第\d+步[，,]", body) or re.match(r"^第\d+步[，,]", body):
            raise ValueError(f"{book_id} 第 {index} 點含面向／步驟贅詞")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(("是", "為", "在於", "說", "問", "提醒", "表示", "指出")):
            short_colon_lines.append(index)
        cleaned.append(line.strip())
        bodies.append(body)
    if len(short_colon_lines) >= 3:
        raise ValueError(f"{book_id} 有 {len(short_colon_lines)} 點疑似短標籤加冒號: {short_colon_lines[:8]}")
    if len(set(bodies)) != len(bodies):
        raise ValueError(f"{book_id} 含完全重複重點")
    repeated_starts = Counter(body[:18] for body in bodies if len(body) >= 18)
    if repeated_starts and repeated_starts.most_common(1)[0][1] >= 4:
        raise ValueError(f"{book_id} 有大量重複固定開頭 {repeated_starts.most_common(3)}")
    for label, value in (("書名", title), ("作者", author)):
        normalized = str(value).strip()
        if normalized and sum(normalized in body for body in bodies) >= 2:
            raise ValueError(f"{book_id} 正文反覆出現完整{label}")
    return cleaned


def atomic_write(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=path.stem + ".", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with open(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        tmp_path.replace(path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def main() -> None:
    mods = {
        21: load_mod("hl_06_21_22", TMP / "hl_06_21_22.py"),
        23: load_mod("hl_06_23_24", TMP / "hl_06_23_24.py"),
        25: load_mod("hl_06_25_26", TMP / "hl_06_25_26.py"),
        27: load_mod("hl_06_27_28", TMP / "hl_06_27_28.py"),
        29: load_mod("hl_06_29_30", TMP / "hl_06_29_30.py"),
    }
    mapping = {
        21: mods[21].HL21,
        22: mods[21].HL22,
        23: mods[23].HL23,
        24: mods[23].HL24,
        25: mods[25].HL25,
        26: mods[25].HL26,
        27: mods[27].HL27,
        28: mods[27].HL28,
        29: mods[29].HL29,
        30: mods[29].HL30,
    }
    captured = now_iso()
    updated = datetime.now(TAIPEI).date().isoformat()
    for n, bodies in mapping.items():
        filename = f"06_computer_info-20260717-{n:02d}.json"
        path = BASE / filename
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        highlights = validate_highlights(
            data["id"],
            to_numbered(list(bodies)),
            str(data.get("title", "")),
            str(data.get("author", "")),
        )
        data["chatgptHighlights"] = highlights
        data["chatgptStatus"] = "complete"
        data["highlightsSource"] = "grok"
        data["highlightsCapturedAt"] = captured
        data["updatedAt"] = updated
        atomic_write(path, data)
        check = json.loads(path.read_text(encoding="utf-8-sig"))
        validate_highlights(
            check["id"],
            check["chatgptHighlights"],
            str(check.get("title", "")),
            str(check.get("author", "")),
        )
        print(f"written\t{filename}\t{len(check['chatgptHighlights'])}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL\t{exc}", file=sys.stderr)
        raise
