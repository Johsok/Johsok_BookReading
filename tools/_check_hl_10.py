# -*- coding: utf-8 -*-
"""Validate tools/_hl_10.json against hard highlight rules."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from findbook_writer import validate_highlights

PATH = Path(__file__).resolve().parent / "_hl_10.json"
TITLE = "人間天宮：非凡造詣的媽祖廟宇"
AUTHOR = "肖東發 主編 秦貝臻 編著"
FORBIDDEN = ["本書", "作者指出", "本章", "書名", "肖東發", "秦貝臻", "｜"]
NATURAL = ("是", "為", "在於", "說", "問", "提醒", "表示", "指出")
SIMP = set("国发会时从来说对开关经还过这来与无个们样种现实应当历礼仪庙妈册传护渔进绕辞抢头祷风涛岛门钟楼顺济阁观画栋飞额为于里")


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8-sig"))
    hls = data["highlights"]
    errors: list[str] = []
    if data.get("id") != "07_other-20260724-10":
        errors.append(f"id mismatch: {data.get('id')}")
    if len(hls) != 150:
        errors.append(f"count={len(hls)} not 150")

    short_colon: list[int] = []
    bodies: list[str] = []
    for i, line in enumerate(hls, 1):
        expected = f"{i:03d}、"
        if not isinstance(line, str) or not line.startswith(expected):
            errors.append(f"{i}: bad prefix")
            continue
        if "\n" in line or "\r" in line:
            errors.append(f"{i}: newline")
        body = line[len(expected) :]
        bodies.append(body)
        if len(body) < 20:
            errors.append(f"{i}: short {len(body)}")
        for word in FORBIDDEN:
            if word in body:
                errors.append(f"{i}: forbidden {word}")
        match = re.match(r"^([^：:]{1,12})[：:]", body)
        if match and not match.group(1).endswith(NATURAL):
            short_colon.append(i)
        tmp = body.replace("天后", "")
        for ch in tmp:
            if ch in SIMP:
                errors.append(f"{i}: simp {ch} :: {body[:28]}")
                break

    if short_colon:
        errors.append(f"short-colon lines: {short_colon}")
    if len(set(bodies)) != len(bodies):
        errors.append("duplicate bodies")
    starts = Counter(body[:18] for body in bodies if len(body) >= 18)
    bad_starts = {key: val for key, val in starts.items() if val >= 4}
    if bad_starts:
        errors.append(f"repeated starts: {bad_starts}")
    for i in range(len(bodies) - 3):
        chunk = [body[:18] for body in bodies[i : i + 4]]
        if len(set(chunk)) == 1:
            errors.append(f"4 consecutive same start at {i + 1}: {chunk[0]}")

    try:
        validate_highlights(data["id"], hls, TITLE, AUTHOR)
        validate_msg = "OK"
    except Exception as exc:
        validate_msg = f"FAIL {exc}"
        errors.append(validate_msg)

    print(f"path={PATH}")
    print(f"count={len(hls)}")
    if bodies:
        print(f"min_len={min(len(b) for b in bodies)} max_len={max(len(b) for b in bodies)}")
    print(f"short_colon={len(short_colon)}")
    print(f"validate_highlights={validate_msg}")
    if errors:
        print(f"ERRORS {len(errors)}")
        for item in errors[:50]:
            print(f" - {item}")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
