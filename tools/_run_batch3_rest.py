# -*- coding: utf-8 -*-
"""Write results JSON and run findbook_writer for batch3 books 37-40."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_lines(path: Path) -> list[str]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    lines = list(mod.LINES)
    if len(lines) != 150:
        raise ValueError(f"{path.name} has {len(lines)} lines")
    return lines


def process(book_id: str, module_path: Path) -> tuple[bool, str]:
    lines = load_lines(module_path)
    highlights = [f"{i:03d}、{text.strip()}" for i, text in enumerate(lines, 1)]
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": highlights}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "findbook_writer.py"),
        "complete",
        "--category-id",
        "01_business_startup",
        "--results",
        str(out),
    ]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True)
    stdout = proc.stdout.decode("utf-8", errors="replace")
    stderr = proc.stderr.decode("utf-8", errors="replace")
    msg = (stdout + stderr).strip()
    return proc.returncode == 0, msg


def main() -> int:
    jobs = [
        ("01_business_startup-20260718-37", ROOT / "tools" / "_batch3_book37.py"),
        ("01_business_startup-20260718-38", ROOT / "tools" / "_batch3_book38.py"),
        ("01_business_startup-20260718-39", ROOT / "tools" / "_batch3_book39.py"),
        ("01_business_startup-20260718-40", ROOT / "tools" / "_batch3_book40.py"),
    ]
    ok, fail = [], []
    for book_id, path in jobs:
        success, msg = process(book_id, path)
        if success:
            ok.append(book_id)
            print(msg)
        else:
            fail.append((book_id, msg))
            print(f"FAIL {book_id}: {msg}", file=sys.stderr)
    print("OK:", ok)
    print("FAIL:", fail)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
