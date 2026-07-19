# -*- coding: utf-8 -*-
"""Write highlights list into results JSON then call findbook_writer complete."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: _write_grok_highlights.py <book_id> <highlights.jsonl|json>")
        return 2
    book_id = sys.argv[1]
    src = Path(sys.argv[2])
    raw = src.read_text(encoding="utf-8").strip()
    if src.suffix == ".jsonl" or (not raw.startswith("{") and not raw.startswith("[")):
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    else:
        data = json.loads(raw)
        if isinstance(data, dict) and "highlights" in data:
            lines = data["highlights"]
        elif isinstance(data, list):
            lines = data
        else:
            raise ValueError("unsupported highlights file")
    if len(lines) != 150:
        raise SystemExit(f"need 150 lines, got {len(lines)}")
    out = ROOT / "tools" / f".findbook_results_grok_{book_id}.json"
    out.write_text(
        json.dumps({"id": book_id, "highlights": lines}, ensure_ascii=False, indent=2) + "\n",
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
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
